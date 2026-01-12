"""
Quota Router - Endpoints pour gestion quotas utilisateur

Affiche usage en MESSAGES (user-friendly), gère en TOKENS (backend)
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

from app.dependencies import get_current_active_user, get_current_superuser
from app.models.user import UserInDB
from app.core.quota_manager import get_quota_manager

router = APIRouter(prefix="/api/quota")
logger = logging.getLogger(__name__)


class UsageStatsResponse(BaseModel):
    """Statistiques usage pour dashboard user"""
    messages_today: int
    messages_limit: int
    messages_remaining: int
    premium_today: int
    premium_limit: int
    premium_remaining: int
    reset_at: str
    percentage_used: float
    tier: str


class QuotaResetRequest(BaseModel):
    """Requête reset quota (admin only)"""
    user_id: int
    reason: Optional[str] = None


@router.get("/usage", response_model=UsageStatsResponse)
async def get_my_usage(user: UserInDB = Depends(get_current_active_user)):
    """
    Récupère statistiques usage pour utilisateur courant

    Returns:
        UsageStatsResponse avec:
        - messages_today: Messages utilisés aujourd'hui
        - messages_limit: Limite quotidienne
        - messages_remaining: Messages restants
        - premium_today: Messages premium utilisés
        - premium_limit: Limite premium
        - reset_at: Timestamp prochain reset
        - percentage_used: % utilisation
        - tier: Tier utilisateur
    """
    quota_manager = get_quota_manager()

    # Récupérer tier utilisateur
    # Note: Supposer que user.tier existe, sinon get depuis DB
    tier = getattr(user, 'tier', 'free')

    stats = await quota_manager.get_usage_stats(
        user_id=user.id,
        tier=tier
    )

    return UsageStatsResponse(**stats)


@router.post("/reset", status_code=200)
async def reset_user_quota(
    request: QuotaResetRequest,
    admin: UserInDB = Depends(get_current_superuser)
):
    """
    Reset quota utilisateur (admin uniquement)

    Use cases:
    - Geste commercial (user a eu problème technique)
    - Debug/testing
    - Support client

    Args:
        request.user_id: ID utilisateur
        request.reason: Raison du reset (optionnel)

    Returns:
        {"success": True, "message": "..."}
    """
    quota_manager = get_quota_manager()

    await quota_manager.reset_user_quota(request.user_id)

    logger.warning(
        f"Quota reset by admin {admin.email} for user {request.user_id}. "
        f"Reason: {request.reason or 'Not specified'}"
    )

    return {
        "success": True,
        "message": f"Quota reset pour user {request.user_id}",
        "reset_by": admin.email,
        "reason": request.reason
    }


@router.get("/health")
async def quota_health():
    """
    Health check pour quota system

    Vérifie:
    - Redis accessible
    - QuotaManager initialisé
    """
    try:
        quota_manager = get_quota_manager()

        # Test Redis ping
        await quota_manager.redis.ping()

        return {
            "status": "healthy",
            "redis": "connected",
            "quota_manager": "initialized"
        }
    except Exception as e:
        logger.error(f"Quota health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Quota system unhealthy: {str(e)}"
        )


@router.get("/quotas/info")
async def get_quotas_info():
    """
    Informations sur les quotas par tier (public)

    Retourne les limites pour chaque tier (sans nécessiter auth)
    Utile pour page pricing
    """
    quota_manager = get_quota_manager()

    return {
        "quotas_by_tier": {
            "free": {
                "messages_per_day": quota_manager.DAILY_QUOTAS["free"]["total"],
                "premium_per_day": quota_manager.DAILY_QUOTAS["free"]["premium"],
                "rate_limit_minute": quota_manager.DAILY_QUOTAS["free"]["rate_minute"],
                "max_input_tokens": quota_manager.MAX_INPUT_TOKENS["free"],
                "max_output_tokens": quota_manager.MAX_OUTPUT_TOKENS["free"],
                "features": [
                    "3 messages/jour",
                    "Modèles gratuits (Groq/Apertus/MiMo)",
                    "Rotation automatique 3 IA",
                    "Pas de carte bancaire requise"
                ]
            },
            "student": {
                "messages_per_day": quota_manager.DAILY_QUOTAS["student"]["total"],
                "premium_per_day": quota_manager.DAILY_QUOTAS["student"]["premium"],
                "rate_limit_minute": quota_manager.DAILY_QUOTAS["student"]["rate_minute"],
                "max_input_tokens": quota_manager.MAX_INPUT_TOKENS["student"],
                "max_output_tokens": quota_manager.MAX_OUTPUT_TOKENS["student"],
                "features": [
                    "200 messages/jour illimités*",
                    "10 messages premium/jour (Claude/GPT)",
                    "Modèles gratuits illimités",
                    "Idéal pour études quotidiennes",
                    "*Fair use: usage personnel raisonnable"
                ]
            },
            "pro": {
                "messages_per_day": quota_manager.DAILY_QUOTAS["pro"]["total"],
                "premium_per_day": quota_manager.DAILY_QUOTAS["pro"]["premium"],
                "rate_limit_minute": quota_manager.DAILY_QUOTAS["pro"]["rate_minute"],
                "max_input_tokens": quota_manager.MAX_INPUT_TOKENS["pro"],
                "max_output_tokens": quota_manager.MAX_OUTPUT_TOKENS["pro"],
                "features": [
                    "500 messages/jour illimités*",
                    "15 messages premium/jour",
                    "API access",
                    "Perplexity web search (20/jour)",
                    "Code Factory & Agent Studio",
                    "*Usage commercial OK, multi-users (5 max)"
                ]
            },
            "enterprise": {
                "messages_per_day": quota_manager.DAILY_QUOTAS["enterprise"]["total"],
                "premium_per_day": quota_manager.DAILY_QUOTAS["enterprise"]["premium"],
                "rate_limit_minute": quota_manager.DAILY_QUOTAS["enterprise"]["rate_minute"],
                "max_input_tokens": quota_manager.MAX_INPUT_TOKENS["enterprise"],
                "max_output_tokens": quota_manager.MAX_OUTPUT_TOKENS["enterprise"],
                "features": [
                    "2000+ messages/jour",
                    "100+ messages premium/jour",
                    "API illimité",
                    "Multi-users (10-50)",
                    "SLA 99.5%",
                    "Support dédié",
                    "Sur devis uniquement"
                ]
            }
        },
        "pricing": {
            "free": {"amount_dzd": 0, "amount_usd": 0},
            "student": {"amount_dzd": 1590, "amount_usd": 6.91},
            "pro": {"amount_dzd": 2590, "amount_usd": 11.26},
            "enterprise": {"amount_dzd": 9900, "amount_usd": 43, "note": "À partir de"}
        }
    }
