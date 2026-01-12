"""
QuotaManager - Gestion quotas intelligente
Communique en MESSAGES (user-friendly), gère en TOKENS (backend)

Stratégie rentable:
- GRATUIT: 3 msg/jour, 100% gratuit (Groq/Apertus/MiMo)
- ÉTUDIANT: 200 msg/jour, 10 premium max → Marge 70%
- PRO: 500 msg/jour, 15 premium max → Marge 18%

Key insight:
  Users voient: "200 messages/jour"
  Backend gère: Tokens + provider routing + coûts
"""
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import redis.asyncio as redis
import logging
import os
from enum import Enum
import pytz

logger = logging.getLogger(__name__)


class ProviderType(str, Enum):
    """Type de provider (gratuit vs payant)"""
    FREE = "free"      # Groq, Apertus, MiMo, Gemini
    PREMIUM = "premium"  # Claude, GPT, Grok


class QuotaManager:
    """
    Gère quotas multi-niveaux avec psychologie user

    Principe:
    - User voit: "147 messages restants sur 200"
    - Backend gère: Tokens, coûts, routing, limites

    Quotas par tier:
    - FREE: 3 msg/jour (acquisition)
    - STUDENT: 200 msg/jour (10 premium max)
    - PRO: 500 msg/jour (15 premium max)
    - ENTERPRISE: 2000+ msg/jour (100+ premium)
    """

    # Conversion tokens → messages (conservatif)
    TOKENS_PER_MESSAGE = 1000  # 200 input + 800 output moyenne

    # Quotas par tier (en messages/jour)
    DAILY_QUOTAS = {
        "free": {
            "total": 3,
            "premium": 0,  # Pas d'accès premium
            "rate_minute": 1,
            "rate_hour": 3,
            "rate_day": 3
        },
        "student": {
            "total": 200,
            "premium": 10,  # 10 messages Claude/GPT max
            "rate_minute": 10,
            "rate_hour": 100,
            "rate_day": 200
        },
        "pro": {
            "total": 500,
            "premium": 15,  # 15 messages premium max
            "rate_minute": 15,
            "rate_hour": 200,
            "rate_day": 500
        },
        "enterprise": {
            "total": 2000,
            "premium": 100,
            "rate_minute": 30,
            "rate_hour": 500,
            "rate_day": 2000
        }
    }

    # Seuils tokens par message (protection anti-abus)
    MAX_INPUT_TOKENS = {
        "free": 500,       # ~125 mots
        "student": 2000,   # ~500 mots
        "pro": 4000,       # ~1000 mots
        "enterprise": 8000  # ~2000 mots
    }

    MAX_OUTPUT_TOKENS = {
        "free": 500,
        "student": 2000,
        "pro": 4000,
        "enterprise": 8000
    }

    # Classification providers
    FREE_PROVIDERS = {
        "groq",
        "publicai/apertus",
        "publicai/mimo",
        "gemini",
        "deepseek"
    }

    PREMIUM_PROVIDERS = {
        "openrouter/anthropic/claude-sonnet-4-20250514",
        "openrouter/openai/gpt-4o",
        "openrouter/grok-2-1212",
        "openrouter/deepseek/deepseek-chat",  # Si utilisé via OpenRouter (payant)
    }

    def __init__(self):
        """Initialize QuotaManager avec Redis"""
        redis_url = os.getenv("REDIS_URL", "redis://iafactory-redis:6379/0")
        self.redis = redis.from_url(redis_url, decode_responses=True)
        self.timezone = pytz.timezone('Africa/Algiers')

    def _get_provider_type(self, provider: str) -> ProviderType:
        """Détermine si provider est gratuit ou premium"""
        # Normaliser provider
        provider_lower = provider.lower()

        # Check exact match first
        if provider_lower in self.FREE_PROVIDERS:
            return ProviderType.FREE

        if provider_lower in self.PREMIUM_PROVIDERS:
            return ProviderType.PREMIUM

        # Check partial match (ex: "openrouter/..." → premium)
        if any(p in provider_lower for p in ["claude", "gpt", "grok"]):
            return ProviderType.PREMIUM

        # Par défaut: gratuit (safe)
        return ProviderType.FREE

    def _get_today_key(self) -> str:
        """Retourne date du jour en timezone Algérie"""
        now = datetime.now(self.timezone)
        return now.strftime("%Y-%m-%d")

    def _get_next_reset(self) -> datetime:
        """Retourne timestamp prochain reset (minuit Algérie)"""
        now = datetime.now(self.timezone)
        tomorrow = now + timedelta(days=1)
        midnight = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
        return midnight

    async def check_quota(
        self,
        user_id: int,
        tier: str,
        provider: str,
        estimated_input_tokens: int = 200
    ) -> Dict:
        """
        Vérifie quota avant génération

        Args:
            user_id: ID utilisateur
            tier: Tier utilisateur (free/student/pro/enterprise)
            provider: Provider LLM (ex: "groq", "openrouter/claude")
            estimated_input_tokens: Estimation tokens input

        Returns:
            {
                "allowed": bool,
                "reason": str (si refusé),
                "quota_info": {...}
            }
        """
        today = self._get_today_key()

        # Get quotas for tier
        quota = self.DAILY_QUOTAS.get(tier)
        if not quota:
            logger.error(f"Tier inconnu: {tier}")
            return {
                "allowed": False,
                "reason": "invalid_tier",
                "message": "Tier utilisateur invalide"
            }

        # Redis keys
        key_total = f"quota:{user_id}:{today}:total"
        key_premium = f"quota:{user_id}:{today}:premium"
        key_minute = f"quota:{user_id}:minute"

        # Compteurs actuels (en messages)
        messages_today = int(await self.redis.get(key_total) or 0)
        premium_today = int(await self.redis.get(key_premium) or 0)
        requests_minute = int(await self.redis.get(key_minute) or 0)

        # CHECK 1: Rate limiting (minute)
        if requests_minute >= quota["rate_minute"]:
            return {
                "allowed": False,
                "reason": "rate_limit_minute",
                "message": f"Trop rapide! Maximum {quota['rate_minute']} requêtes/minute.",
                "retry_after_seconds": 60
            }

        # CHECK 2: Quota quotidien total
        if messages_today >= quota["total"]:
            next_reset = self._get_next_reset()
            return {
                "allowed": False,
                "reason": "daily_limit_reached",
                "message": f"Limite quotidienne atteinte ({quota['total']} messages/jour).",
                "quota_info": {
                    "messages_used": messages_today,
                    "messages_limit": quota["total"],
                    "reset_at": next_reset.isoformat()
                }
            }

        # CHECK 3: Provider type et quota premium
        provider_type = self._get_provider_type(provider)

        if provider_type == ProviderType.PREMIUM:
            # Provider payant (Claude, GPT, Grok)

            if tier == "free":
                # Tier FREE n'a pas accès premium
                return {
                    "allowed": False,
                    "reason": "premium_not_allowed",
                    "message": "Modèle premium non disponible en tier GRATUIT. Passez à ÉTUDIANT!",
                    "upgrade_url": "/pricing",
                    "fallback_provider": "groq"
                }

            # Check quota premium
            if premium_today >= quota["premium"]:
                # Limite premium atteinte → Proposer fallback Groq
                return {
                    "allowed": False,
                    "reason": "premium_limit_reached",
                    "message": f"Limite premium atteinte ({quota['premium']}/jour). Passage automatique en mode rapide (Groq).",
                    "quota_info": {
                        "premium_used": premium_today,
                        "premium_limit": quota["premium"],
                        "fallback": "groq",
                        "fallback_message": "Groq est toujours gratuit et rapide! 🚀"
                    },
                    "auto_fallback": True  # Signale au router de fallback auto
                }

        # CHECK 4: Tokens par message (anti-abus)
        max_input = self.MAX_INPUT_TOKENS[tier]

        if estimated_input_tokens > max_input:
            return {
                "allowed": False,
                "reason": "message_too_long",
                "message": f"Message trop long. Maximum {max_input} tokens (~{max_input // 4} mots).",
                "max_tokens": max_input,
                "estimated_tokens": estimated_input_tokens
            }

        # Tout OK ✅
        messages_remaining = quota["total"] - messages_today
        premium_remaining = quota["premium"] - premium_today if provider_type == ProviderType.PREMIUM else None

        return {
            "allowed": True,
            "quota_info": {
                "messages_remaining": messages_remaining,
                "messages_used": messages_today,
                "messages_limit": quota["total"],
                "premium_remaining": premium_remaining,
                "premium_used": premium_today if provider_type == ProviderType.PREMIUM else None,
                "premium_limit": quota["premium"] if provider_type == ProviderType.PREMIUM else None,
                "provider_type": provider_type.value,
                "reset_at": self._get_next_reset().isoformat()
            }
        }

    async def increment_quota(
        self,
        user_id: int,
        tier: str,
        provider: str,
        tokens_used: Dict[str, int]
    ):
        """
        Incrémenter compteurs après génération réussie

        Args:
            user_id: ID utilisateur
            tier: Tier utilisateur
            provider: Provider utilisé
            tokens_used: {"input": X, "output": Y}
        """
        today = self._get_today_key()
        provider_type = self._get_provider_type(provider)

        # Incrémenter messages total
        key_total = f"quota:{user_id}:{today}:total"
        await self.redis.incr(key_total)
        await self.redis.expire(key_total, 86400)  # 24h

        # Si premium, incrémenter compteur premium
        if provider_type == ProviderType.PREMIUM:
            key_premium = f"quota:{user_id}:{today}:premium"
            await self.redis.incr(key_premium)
            await self.redis.expire(key_premium, 86400)

        # Rate limiting (minute)
        key_minute = f"quota:{user_id}:minute"
        await self.redis.incr(key_minute)
        await self.redis.expire(key_minute, 60)  # 1 minute

        logger.info(
            f"Quota incremented - User: {user_id}, Tier: {tier}, "
            f"Provider: {provider} ({provider_type.value}), "
            f"Tokens: {tokens_used['input']}+{tokens_used['output']}"
        )

    async def get_usage_stats(self, user_id: int, tier: str) -> Dict:
        """
        Récupère statistiques usage pour affichage dashboard user

        Returns:
            {
                "messages_today": int,
                "messages_limit": int,
                "messages_remaining": int,
                "premium_today": int,
                "premium_limit": int,
                "premium_remaining": int,
                "reset_at": str (ISO format),
                "percentage_used": float
            }
        """
        today = self._get_today_key()
        quota = self.DAILY_QUOTAS.get(tier, self.DAILY_QUOTAS["free"])

        # Redis keys
        key_total = f"quota:{user_id}:{today}:total"
        key_premium = f"quota:{user_id}:{today}:premium"

        # Compteurs actuels
        messages_today = int(await self.redis.get(key_total) or 0)
        premium_today = int(await self.redis.get(key_premium) or 0)

        messages_remaining = max(0, quota["total"] - messages_today)
        premium_remaining = max(0, quota["premium"] - premium_today) if quota["premium"] > 0 else 0

        percentage_used = (messages_today / quota["total"] * 100) if quota["total"] > 0 else 0

        return {
            "messages_today": messages_today,
            "messages_limit": quota["total"],
            "messages_remaining": messages_remaining,
            "premium_today": premium_today,
            "premium_limit": quota["premium"],
            "premium_remaining": premium_remaining,
            "reset_at": self._get_next_reset().isoformat(),
            "percentage_used": round(percentage_used, 1),
            "tier": tier
        }

    async def reset_user_quota(self, user_id: int):
        """
        Reset quota utilisateur (admin uniquement)
        Utile pour debug ou gestes commerciaux
        """
        today = self._get_today_key()

        key_total = f"quota:{user_id}:{today}:total"
        key_premium = f"quota:{user_id}:{today}:premium"
        key_minute = f"quota:{user_id}:minute"

        await self.redis.delete(key_total)
        await self.redis.delete(key_premium)
        await self.redis.delete(key_minute)

        logger.warning(f"Quota reset for user {user_id} by admin")

    async def get_all_users_usage(self, tier_filter: Optional[str] = None) -> Dict:
        """
        Récupère usage global pour dashboard admin

        Args:
            tier_filter: Filtrer par tier (optional)

        Returns:
            {
                "total_messages_today": int,
                "total_premium_today": int,
                "by_tier": {...}
            }
        """
        # Cette méthode nécessite une liste des users actifs
        # Pour une implémentation complète, il faudrait:
        # 1. Récupérer tous les users de la DB
        # 2. Pour chaque user, check leurs quotas Redis
        # 3. Agréger par tier

        # Implémentation simplifiée:
        # On suppose qu'on a une fonction pour get active users

        logger.info("get_all_users_usage called - requires DB integration")

        # Placeholder - à implémenter avec DB
        return {
            "total_messages_today": 0,
            "total_premium_today": 0,
            "by_tier": {
                "free": {"users": 0, "messages": 0},
                "student": {"users": 0, "messages": 0},
                "pro": {"users": 0, "messages": 0}
            }
        }


# Singleton instance
_quota_manager: Optional[QuotaManager] = None


def get_quota_manager() -> QuotaManager:
    """Get singleton QuotaManager instance"""
    global _quota_manager
    if _quota_manager is None:
        _quota_manager = QuotaManager()
    return _quota_manager
