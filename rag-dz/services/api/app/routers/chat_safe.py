"""
Chat Router - Utilise SafeLLMRouter avec fallback ZÉRO RISQUE

Cette route remplace /api/chat existante avec:
- Routing intelligent par tier (85% Groq STUDENT, 70% PRO)
- Budget caps automatiques
- Fallback 3 niveaux
- Rate limiting intégré
- Logging usage pour billing
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import asyncpg
import logging
from datetime import datetime

from app.core.safe_llm_router import SafeLLMRouter, get_llm_router, UserTier
from app.middleware.rate_limiter import RateLimiter, get_rate_limiter
from app.dependencies import get_current_user, get_db_pool
from app.models.user import UserInDB

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v2", tags=["chat"])


class ChatRequest(BaseModel):
    """Request body pour chat"""
    prompt: str
    model: str = "gpt-4o"  # claude-sonnet-4, gpt-4o, grok-2, llama-3.3
    max_tokens: int = 2000
    temperature: float = 0.7


class ChatResponse(BaseModel):
    """Response body pour chat"""
    response: str
    model: str
    provider: str
    tokens: dict
    cost: float
    cached: bool = False
    fallback: bool = False
    fallback_level: Optional[int] = None
    budget_fallback: Optional[bool] = None


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user: UserInDB = Depends(get_current_user),
    router: SafeLLMRouter = Depends(get_llm_router),
    db: asyncpg.Pool = Depends(get_db_pool)
):
    """
    Chat avec IA - Routing intelligent selon tier user

    Flow:
    1. User authentifié (JWT)
    2. Check rate limiting (middleware déjà appliqué)
    3. Récupère tier user (FREE/STUDENT/PRO)
    4. SafeLLMRouter génère réponse avec fallback
    5. Log usage dans PostgreSQL
    6. Return réponse

    Args:
        request: {
            "prompt": "Question user",
            "model": "claude-sonnet-4" | "gpt-4o" | "grok-2",
            "max_tokens": 2000,
            "temperature": 0.7
        }

    Returns:
        {
            "response": "Réponse IA",
            "model": "claude-sonnet-4",
            "provider": "openrouter",
            "tokens": {"input": 100, "output": 800},
            "cost": 0.012,
            "fallback": false
        }

    Raises:
        HTTPException 429 si rate limit dépassé (géré par middleware)
        HTTPException 401 si pas authentifié
    """

    # 1. Récupérer tier user
    tier_row = await db.fetchrow(
        """
        SELECT tier, expires_at
        FROM user_tiers
        WHERE user_id = $1
        """,
        user.id
    )

    if tier_row:
        # Vérifier si abonnement expiré
        tier_name = tier_row["tier"]
        expires_at = tier_row["expires_at"]

        if expires_at and expires_at < datetime.now():
            # Abonnement expiré → Downgrade FREE
            logger.warning(f"User {user.id} subscription expired, downgrading to FREE")
            tier_name = "free"
            await db.execute(
                """
                UPDATE user_tiers
                SET tier = 'free'
                WHERE user_id = $1
                """,
                user.id
            )
    else:
        # Pas d'abonnement → FREE par défaut
        tier_name = "free"

    user_tier = UserTier(tier_name)

    # 2. Vérifier ban (soft ban anti-abus)
    # Déjà géré dans rate_limiter, mais double check
    # TODO: Implémenter check ban si besoin

    # 3. Générer réponse avec SafeLLMRouter
    try:
        result = await router.generate(
            user_id=user.id,
            prompt=request.prompt,
            model_choice=request.model,
            user_tier=user_tier,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )

        # Si quota exceeded (retourné par router)
        if result.get("error") == "quota_exceeded":
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=result["message"]
            )

        # 4. Log usage dans PostgreSQL (billing + analytics)
        await db.execute(
            """
            INSERT INTO llm_usage_logs (
                user_id,
                provider,
                model,
                tokens_input,
                tokens_output,
                cost_usd,
                endpoint,
                error_flag
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            """,
            user.id,
            result["provider"],
            result["model"],
            result["tokens"]["input"],
            result["tokens"]["output"],
            result["cost"],
            "/api/v2/chat",
            result.get("error") is not None
        )

        logger.info(
            f"Chat success - User: {user.id} ({tier_name}), "
            f"Provider: {result['provider']}, "
            f"Tokens: {result['tokens']['input']}+{result['tokens']['output']}, "
            f"Cost: ${result['cost']:.4f}"
        )

        # 5. Return response
        return ChatResponse(**result)

    except HTTPException:
        # Re-raise HTTPExceptions (rate limit, etc.)
        raise

    except Exception as e:
        logger.error(f"Chat error for user {user.id}: {e}", exc_info=True)

        # Log error dans DB
        await db.execute(
            """
            INSERT INTO llm_usage_logs (
                user_id,
                provider,
                model,
                tokens_input,
                tokens_output,
                cost_usd,
                endpoint,
                error_flag,
                error_message
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            """,
            user.id,
            "error",
            request.model,
            0,
            0,
            0,
            "/api/v2/chat",
            True,
            str(e)
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne. Veuillez réessayer."
        )


@router.get("/models")
async def list_models(
    user: UserInDB = Depends(get_current_user),
    db: asyncpg.Pool = Depends(get_db_pool)
):
    """
    Liste les modèles disponibles selon tier user

    Returns:
        {
            "tier": "student",
            "models": [
                {
                    "id": "claude-sonnet-4",
                    "name": "Claude Sonnet 4",
                    "provider": "Anthropic",
                    "available": true,
                    "description": "Le plus intelligent"
                },
                ...
            ]
        }
    """
    # Récupérer tier
    tier_row = await db.fetchrow(
        "SELECT tier FROM user_tiers WHERE user_id = $1",
        user.id
    )
    tier_name = tier_row["tier"] if tier_row else "free"

    # Modèles disponibles par tier
    all_models = [
        {
            "id": "claude-sonnet-4",
            "name": "Claude Sonnet 4",
            "provider": "Anthropic",
            "description": "Le plus intelligent du marché",
            "icon": "🧠",
            "speed": "Rapide",
            "quality": "Excellente",
            "min_tier": "student"
        },
        {
            "id": "gpt-4o",
            "name": "GPT-4o",
            "provider": "OpenAI",
            "description": "Le modèle emblématique d'OpenAI",
            "icon": "⚡",
            "speed": "Très rapide",
            "quality": "Très bonne",
            "min_tier": "student"
        },
        {
            "id": "grok-2",
            "name": "Grok 2",
            "provider": "xAI",
            "description": "L'IA d'Elon Musk",
            "icon": "🚀",
            "speed": "Rapide",
            "quality": "Très bonne",
            "min_tier": "student"
        },
        {
            "id": "llama-3.3",
            "name": "Llama 3.3",
            "provider": "Meta",
            "description": "Open source et puissant",
            "icon": "🦙",
            "speed": "Ultra-rapide",
            "quality": "Bonne",
            "min_tier": "free"
        }
    ]

    # Filtrer selon tier
    tier_order = {"free": 0, "student": 1, "pro": 2, "enterprise": 3}
    user_tier_level = tier_order.get(tier_name, 0)

    available_models = []
    for model in all_models:
        model_tier_level = tier_order.get(model["min_tier"], 0)
        model_copy = model.copy()
        model_copy["available"] = user_tier_level >= model_tier_level
        model_copy["locked"] = not model_copy["available"]
        available_models.append(model_copy)

    return {
        "tier": tier_name,
        "models": available_models
    }


@router.get("/usage/today")
async def get_usage_today(
    user: UserInDB = Depends(get_current_user),
    db: asyncpg.Pool = Depends(get_db_pool)
):
    """
    Stats usage aujourd'hui pour ce user

    Returns:
        {
            "tier": "student",
            "messages_today": 42,
            "max_messages": 200,
            "tokens_today": 50000,
            "cost_today": 0.85,
            "percentage_used": 21.0
        }
    """
    # Tier
    tier_row = await db.fetchrow(
        "SELECT tier FROM user_tiers WHERE user_id = $1",
        user.id
    )
    tier_name = tier_row["tier"] if tier_row else "free"

    # Max messages selon tier
    max_messages = {
        "free": 3,
        "student": 200,
        "pro": 400,
        "enterprise": 999999
    }[tier_name]

    # Usage aujourd'hui
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    usage = await db.fetchrow(
        """
        SELECT
            COUNT(*) as messages_count,
            SUM(tokens_input + tokens_output) as tokens_total,
            SUM(cost_usd) as cost_total
        FROM llm_usage_logs
        WHERE user_id = $1 AND created_at >= $2
        """,
        user.id,
        today_start
    )

    messages_today = usage["messages_count"] or 0
    tokens_today = usage["tokens_total"] or 0
    cost_today = float(usage["cost_total"]) if usage["cost_total"] else 0

    percentage_used = (messages_today / max_messages * 100) if max_messages > 0 else 0

    return {
        "tier": tier_name,
        "messages_today": messages_today,
        "max_messages": max_messages,
        "tokens_today": tokens_today,
        "cost_today": round(cost_today, 2),
        "percentage_used": round(percentage_used, 1)
    }
