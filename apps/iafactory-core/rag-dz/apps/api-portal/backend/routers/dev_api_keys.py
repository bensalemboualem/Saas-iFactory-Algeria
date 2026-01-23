"""
iaFactory API Portal - API Keys Management
Module 16 - Gestion des clés API façon OpenAI
"""

import secrets
import hashlib
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..auth import get_current_user
from ..models import User, ApiKey, ApiLog

router = APIRouter(prefix="/api/dev/api-keys", tags=["Developer - API Keys"])


# ==============================================
# SCHEMAS
# ==============================================

class ApiKeyCreate(BaseModel):
    """Schéma création clé API"""
    name: str = Field(..., min_length=1, max_length=100, description="Nom descriptif de la clé")
    

class ApiKeyResponse(BaseModel):
    """Schéma réponse clé API (sans secret)"""
    id: str
    name: str
    prefix: str  # Ex: iafk_live_1234...abcd
    created_at: datetime
    last_used_at: Optional[datetime]
    status: str  # active, revoked
    
    class Config:
        from_attributes = True


class ApiKeyCreatedResponse(BaseModel):
    """Schéma réponse après création (avec secret complet)"""
    id: str
    name: str
    key: str  # Clé complète - affichée UNE SEULE FOIS
    prefix: str
    created_at: datetime
    warning: str = "⚠️ Copiez cette clé maintenant. Vous ne pourrez plus la revoir."


class ApiKeyStats(BaseModel):
    """Statistiques d'une clé"""
    total_requests: int
    requests_today: int
    last_used_at: Optional[datetime]
    error_count: int


# ==============================================
# HELPERS
# ==============================================

def generate_api_key() -> tuple[str, str, str]:
    """
    Génère une clé API sécurisée
    Returns: (full_key, prefix, hash)
    """
    # Générer 32 bytes aléatoires
    random_bytes = secrets.token_bytes(32)
    # Encoder en base64 URL-safe
    key_suffix = secrets.token_urlsafe(32)
    
    # Format: IAFK_live_<random>
    full_key = f"IAFK_live_{key_suffix}"
    
    # Préfixe visible: premiers et derniers caractères
    prefix = f"IAFK_live_{key_suffix[:8]}...{key_suffix[-4:]}"
    
    # Hash pour stockage sécurisé
    key_hash = hashlib.sha256(full_key.encode()).hexdigest()
    
    return full_key, prefix, key_hash


def hash_api_key(key: str) -> str:
    """Hash une clé API pour comparaison"""
    return hashlib.sha256(key.encode()).hexdigest()


# ==============================================
# ENDPOINTS
# ==============================================

@router.get("", response_model=List[ApiKeyResponse])
async def list_api_keys(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Liste toutes les clés API de l'utilisateur
    """
    result = await db.execute(
        select(ApiKey)
        .where(ApiKey.user_id == current_user.id)
        .order_by(ApiKey.created_at.desc())
    )
    keys = result.scalars().all()
    
    return [
        ApiKeyResponse(
            id=str(key.id),
            name=key.name,
            prefix=key.prefix,
            created_at=key.created_at,
            last_used_at=key.last_used_at,
            status=key.status
        )
        for key in keys
    ]


@router.post("", response_model=ApiKeyCreatedResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    data: ApiKeyCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Crée une nouvelle clé API
    
    ⚠️ La clé complète n'est retournée qu'une seule fois.
    Seul le hash est stocké en base de données.
    """
    # Vérifier limite de clés (max 10 par utilisateur)
    result = await db.execute(
        select(func.count(ApiKey.id))
        .where(ApiKey.user_id == current_user.id)
        .where(ApiKey.status == "active")
    )
    active_count = result.scalar()
    
    if active_count >= 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limite de 10 clés API actives atteinte. Révoquez une clé existante."
        )
    
    # Générer la clé
    full_key, prefix, key_hash = generate_api_key()
    
    # Créer l'entrée en base
    import uuid
    new_key = ApiKey(
        id=uuid.uuid4(),
        user_id=current_user.id,
        name=data.name,
        key_hash=key_hash,
        prefix=prefix,
        status="active",
        created_at=datetime.utcnow()
    )
    
    db.add(new_key)
    await db.commit()
    await db.refresh(new_key)
    
    return ApiKeyCreatedResponse(
        id=str(new_key.id),
        name=new_key.name,
        key=full_key,  # Retournée UNE SEULE FOIS
        prefix=prefix,
        created_at=new_key.created_at,
        warning="⚠️ Copiez cette clé maintenant. Vous ne pourrez plus la revoir."
    )


@router.post("/{key_id}/revoke")
async def revoke_api_key(
    key_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Révoque une clé API
    
    La clé devient immédiatement inutilisable.
    """
    import uuid
    
    try:
        key_uuid = uuid.UUID(key_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de clé invalide"
        )
    
    # Récupérer la clé
    result = await db.execute(
        select(ApiKey)
        .where(ApiKey.id == key_uuid)
        .where(ApiKey.user_id == current_user.id)
    )
    api_key = result.scalar_one_or_none()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Clé API non trouvée"
        )
    
    if api_key.status == "revoked":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cette clé est déjà révoquée"
        )
    
    # Révoquer la clé
    api_key.status = "revoked"
    api_key.revoked_at = datetime.utcnow()
    
    await db.commit()
    
    return {
        "message": "Clé API révoquée avec succès",
        "key_id": key_id,
        "prefix": api_key.prefix,
        "revoked_at": api_key.revoked_at.isoformat()
    }


@router.get("/{key_id}/stats", response_model=ApiKeyStats)
async def get_api_key_stats(
    key_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Récupère les statistiques d'une clé API spécifique
    """
    import uuid
    from datetime import timedelta
    
    try:
        key_uuid = uuid.UUID(key_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de clé invalide"
        )
    
    # Vérifier que la clé appartient à l'utilisateur
    result = await db.execute(
        select(ApiKey)
        .where(ApiKey.id == key_uuid)
        .where(ApiKey.user_id == current_user.id)
    )
    api_key = result.scalar_one_or_none()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Clé API non trouvée"
        )
    
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Total requêtes
    total_result = await db.execute(
        select(func.count(ApiLog.id))
        .where(ApiLog.api_key_id == key_uuid)
    )
    total_requests = total_result.scalar() or 0
    
    # Requêtes aujourd'hui
    today_result = await db.execute(
        select(func.count(ApiLog.id))
        .where(ApiLog.api_key_id == key_uuid)
        .where(ApiLog.created_at >= today)
    )
    requests_today = today_result.scalar() or 0
    
    # Erreurs (status >= 400)
    error_result = await db.execute(
        select(func.count(ApiLog.id))
        .where(ApiLog.api_key_id == key_uuid)
        .where(ApiLog.status_code >= 400)
    )
    error_count = error_result.scalar() or 0
    
    return ApiKeyStats(
        total_requests=total_requests,
        requests_today=requests_today,
        last_used_at=api_key.last_used_at,
        error_count=error_count
    )
