"""
Router API pour la gestion des clés API utilisateur (Key Reselling)
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..models.user_key import (
    KeyValidateRequest, KeyValidateResponse,
    KeyDebitRequest, KeyDebitResponse,
    KeyCreateRequest, KeyBalanceResponse, UserKey
)
from ..services import user_key_service
from ..dependencies import get_current_user

router = APIRouter(prefix="/api/keys", tags=["User Keys"])


@router.post("/validate", response_model=KeyValidateResponse)
async def validate_key(request: KeyValidateRequest):
    """
    Valide une clé API et retourne son état.
    Si user_id est fourni, attribue automatiquement la clé à l'utilisateur lors de la première utilisation.
    """
    return await user_key_service.validate_key(request.key_code, request.user_id)


@router.post("/debit", response_model=KeyDebitResponse)
async def debit_key(request: KeyDebitRequest):
    """
    Débite une clé du montant spécifié après une requête API.
    Appelé par le proxy après chaque requête réussie.
    """
    return await user_key_service.debit_key(
        request.key_code,
        request.amount_usd,
        request.description
    )


@router.get("/{key_code}/balance", response_model=KeyBalanceResponse)
async def get_balance(key_code: str):
    """
    Récupère le solde détaillé d'une clé.
    """
    balance = await user_key_service.get_balance(key_code)
    if not balance:
        raise HTTPException(status_code=404, detail="Clé non trouvée")
    return balance


@router.post("/create", response_model=UserKey)
async def create_key(request: KeyCreateRequest):
    """
    Crée une nouvelle clé API pour un utilisateur.
    Endpoint admin - à protéger en production.
    """
    return await user_key_service.create_key(request)


@router.get("/user/{user_id}", response_model=List[KeyBalanceResponse])
async def get_user_keys(user_id: str):
    """
    Récupère toutes les clés d'un utilisateur.
    """
    return await user_key_service.get_user_keys(user_id)


@router.get("/pricing")
async def get_pricing():
    """
    Retourne les tarifs par provider et modèle.
    Utile pour l'affichage dans l'interface.
    """
    return {
        "providers": user_key_service.PROVIDER_COSTS,
        "margin": 1.3,
        "currency": "USD"
    }
