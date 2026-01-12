"""
Service de gestion des clés API utilisateur (Key Reselling)
Supporte Firestore et fallback mémoire pour dev
"""
import logging
import secrets
import string
from datetime import datetime, timedelta
from typing import Optional, Dict
from ..models.user_key import (
    UserKey, KeyStatus, KeyValidateResponse, KeyDebitResponse,
    KeyCreateRequest, KeyBalanceResponse
)

logger = logging.getLogger(__name__)

# Storage en mémoire (fallback dev) - en production utiliser Firestore
_keys_store: Dict[str, dict] = {}

# Flag pour Firestore
_firestore_client = None


def _get_firestore():
    """Lazy init Firestore client"""
    global _firestore_client
    if _firestore_client is None:
        try:
            from google.cloud import firestore
            _firestore_client = firestore.Client()
            logger.info("Firestore client initialized")
        except Exception as e:
            logger.warning(f"Firestore not available, using memory store: {e}")
            _firestore_client = False
    return _firestore_client if _firestore_client else None


def _generate_key_code(provider: str) -> str:
    """Génère un code unique pour une clé"""
    chars = string.ascii_uppercase + string.digits
    random_part = ''.join(secrets.choice(chars) for _ in range(8))
    return f"{provider.upper()}-{random_part}"


async def create_key(request: KeyCreateRequest) -> UserKey:
    """Crée une nouvelle clé API pour un utilisateur"""
    key_code = _generate_key_code(request.provider)

    expires_at = None
    if request.expires_days:
        expires_at = datetime.utcnow() + timedelta(days=request.expires_days)

    key_data = {
        "key_code": key_code,
        "provider": request.provider,
        "user_id": request.user_id,
        "balance_usd": request.balance_usd,
        "current_usage": 0.0,
        "status": KeyStatus.ACTIVE.value,
        "created_at": datetime.utcnow(),
        "expires_at": expires_at
    }

    # Sauvegarder
    db = _get_firestore()
    if db:
        db.collection("user_keys").document(key_code).set(key_data)
    else:
        _keys_store[key_code] = key_data

    logger.info(f"Created key {key_code} for user {request.user_id}")
    return UserKey(**key_data)


async def get_key(key_code: str) -> Optional[UserKey]:
    """Récupère une clé par son code"""
    db = _get_firestore()

    if db:
        doc = db.collection("user_keys").document(key_code).get()
        if doc.exists:
            return UserKey(**doc.to_dict())
    else:
        if key_code in _keys_store:
            return UserKey(**_keys_store[key_code])

    return None


async def validate_key(key_code: str, user_id: str = None) -> KeyValidateResponse:
    """
    Valide une clé et retourne son état.
    Si user_id est fourni et la clé n'est pas attribuée, elle sera attribuée à cet utilisateur.
    """
    key = await get_key(key_code)

    if not key:
        return KeyValidateResponse(
            valid=False,
            message="Clé non trouvée"
        )

    # Vérifier expiration
    if key.expires_at and datetime.utcnow() > key.expires_at:
        await _update_key_status(key_code, KeyStatus.EXPIRED)
        return KeyValidateResponse(
            valid=False,
            provider=key.provider,
            status=KeyStatus.EXPIRED.value,
            message="Clé expirée"
        )

    # Vérifier solde
    if key.remaining_balance <= 0:
        await _update_key_status(key_code, KeyStatus.DEPLETED)
        return KeyValidateResponse(
            valid=False,
            provider=key.provider,
            remaining_balance=0,
            status=KeyStatus.DEPLETED.value,
            message="Solde épuisé"
        )

    # Vérifier statut DEPLETED/EXPIRED
    if key.status in [KeyStatus.DEPLETED, KeyStatus.EXPIRED]:
        return KeyValidateResponse(
            valid=False,
            provider=key.provider,
            status=key.status.value,
            message=f"Clé {key.status.value}"
        )

    # Vérifier attribution utilisateur
    if key.user_id and user_id and key.user_id != user_id:
        return KeyValidateResponse(
            valid=False,
            provider=key.provider,
            status="ASSIGNED",
            message="Clé déjà attribuée à un autre utilisateur"
        )

    # Première activation: attribuer la clé à l'utilisateur
    if not key.user_id and user_id:
        await _activate_key_for_user(key_code, user_id)
        logger.info(f"Key {key_code} activated for user {user_id}")

    # Activer si NEW
    if key.status == KeyStatus.NEW:
        await _update_key_status(key_code, KeyStatus.ACTIVE)

    return KeyValidateResponse(
        valid=True,
        provider=key.provider,
        remaining_balance=key.remaining_balance,
        status=KeyStatus.ACTIVE.value,
        message="Clé valide"
    )


async def debit_key(key_code: str, amount_usd: float, description: str = None) -> KeyDebitResponse:
    """Débite une clé du montant spécifié"""
    key = await get_key(key_code)

    if not key:
        return KeyDebitResponse(
            success=False,
            new_balance=0,
            message="Clé non trouvée"
        )

    if not key.is_valid:
        return KeyDebitResponse(
            success=False,
            new_balance=key.remaining_balance,
            message=f"Clé invalide: {key.status.value}"
        )

    if amount_usd > key.remaining_balance:
        return KeyDebitResponse(
            success=False,
            new_balance=key.remaining_balance,
            message=f"Solde insuffisant. Requis: ${amount_usd:.4f}, Disponible: ${key.remaining_balance:.4f}"
        )

    # Débiter
    new_usage = key.current_usage + amount_usd
    new_balance = key.balance_usd - new_usage

    db = _get_firestore()
    if db:
        db.collection("user_keys").document(key_code).update({
            "current_usage": new_usage
        })
    else:
        _keys_store[key_code]["current_usage"] = new_usage

    # Vérifier si épuisé
    if new_balance <= 0:
        await _update_key_status(key_code, KeyStatus.DEPLETED)

    logger.info(f"Debited ${amount_usd:.4f} from key {key_code}. New balance: ${new_balance:.4f}")

    return KeyDebitResponse(
        success=True,
        new_balance=new_balance,
        message=f"Débit de ${amount_usd:.4f} effectué"
    )


async def get_balance(key_code: str) -> Optional[KeyBalanceResponse]:
    """Récupère le solde détaillé d'une clé"""
    key = await get_key(key_code)

    if not key:
        return None

    return KeyBalanceResponse(
        key_code=key.key_code,
        provider=key.provider,
        balance_usd=key.balance_usd,
        current_usage=key.current_usage,
        remaining_balance=key.remaining_balance,
        status=key.status.value,
        expires_at=key.expires_at
    )


async def get_user_keys(user_id: str) -> list[KeyBalanceResponse]:
    """Récupère toutes les clés d'un utilisateur"""
    keys = []

    db = _get_firestore()
    if db:
        docs = db.collection("user_keys").where("user_id", "==", user_id).stream()
        for doc in docs:
            key = UserKey(**doc.to_dict())
            keys.append(KeyBalanceResponse(
                key_code=key.key_code,
                provider=key.provider,
                balance_usd=key.balance_usd,
                current_usage=key.current_usage,
                remaining_balance=key.remaining_balance,
                status=key.status.value,
                expires_at=key.expires_at
            ))
    else:
        for key_data in _keys_store.values():
            if key_data.get("user_id") == user_id:
                key = UserKey(**key_data)
                keys.append(KeyBalanceResponse(
                    key_code=key.key_code,
                    provider=key.provider,
                    balance_usd=key.balance_usd,
                    current_usage=key.current_usage,
                    remaining_balance=key.remaining_balance,
                    status=key.status.value,
                    expires_at=key.expires_at
                ))

    return keys


async def _update_key_status(key_code: str, status: KeyStatus):
    """Met à jour le statut d'une clé"""
    db = _get_firestore()
    if db:
        db.collection("user_keys").document(key_code).update({
            "status": status.value
        })
    else:
        if key_code in _keys_store:
            _keys_store[key_code]["status"] = status.value


async def _activate_key_for_user(key_code: str, user_id: str):
    """Attribue une clé à un utilisateur et l'active"""
    db = _get_firestore()
    update_data = {
        "user_id": user_id,
        "status": KeyStatus.ACTIVE.value,
        "activated_at": datetime.utcnow()
    }

    if db:
        db.collection("user_keys").document(key_code).update(update_data)
    else:
        if key_code in _keys_store:
            _keys_store[key_code].update(update_data)


# Tarifs par provider (coût réel + marge)
PROVIDER_COSTS = {
    "Groq": {
        "llama-3.3-70b-versatile": {"input": 0.59, "output": 0.79},  # per 1M tokens
        "llama-3.1-8b-instant": {"input": 0.05, "output": 0.08},
        "mixtral-8x7b-32768": {"input": 0.24, "output": 0.24},
    },
    "OpenRouter": {
        "anthropic/claude-3.5-sonnet": {"input": 3.0, "output": 15.0},
        "google/gemini-2.0-flash": {"input": 0.1, "output": 0.4},
        "meta-llama/llama-3.3-70b": {"input": 0.4, "output": 0.4},
    }
}


def calculate_cost(provider: str, model: str, input_tokens: int, output_tokens: int, margin: float = 1.3) -> float:
    """Calcule le coût d'une requête avec marge"""
    if provider not in PROVIDER_COSTS:
        return 0.001  # Coût minimal par défaut

    models = PROVIDER_COSTS[provider]
    if model not in models:
        # Trouver un modèle similaire ou utiliser le premier
        model = list(models.keys())[0]

    costs = models[model]
    input_cost = (input_tokens / 1_000_000) * costs["input"]
    output_cost = (output_tokens / 1_000_000) * costs["output"]

    return (input_cost + output_cost) * margin
