"""
RateLimiter Middleware - Protection anti-abus multi-niveaux

Protection contre:
- Bots (trop rapide)
- Abus (trop de requêtes)
- Multi-comptes (même IP)

Limites par tier:
- FREE: 1 msg/min, 3 msg/heure, 3 msg/jour
- STUDENT: 10 msg/min, 100 msg/heure, 200 msg/jour
- PRO: 15 msg/min, 150 msg/heure, 400 msg/jour
- ENTERPRISE: Illimité (mais fair use monitoring)
"""
from fastapi import Request, HTTPException, status
import redis.asyncio as redis
import time
import logging
import os
from typing import Optional
from app.models.user import UserInDB

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Rate limiting multi-niveaux avec Redis

    Niveaux de protection:
    1. Par minute (protection bots)
    2. Par heure (protection abuse court terme)
    3. Par jour (protection abuse long terme)
    4. Par IP (protection multi-comptes)
    """

    def __init__(self):
        self.redis = redis.from_url(
            os.getenv("REDIS_URL", "redis://iafactory-redis:6379/0"),
            decode_responses=True
        )

        # Limites par tier (minute, heure, jour)
        self.limits = {
            "free": {
                "minute": 1,
                "hour": 3,
                "day": 3
            },
            "student": {
                "minute": 10,
                "hour": 100,
                "day": 200
            },
            "pro": {
                "minute": 15,
                "hour": 150,
                "day": 400
            },
            "enterprise": {
                "minute": 999,
                "hour": 9999,
                "day": 99999
            }
        }

        # Limites par IP (anti multi-comptes FREE)
        self.ip_limits = {
            "free_accounts_per_ip": 3,
            "signups_per_hour_per_ip": 5
        }

    async def check_rate_limit(
        self,
        user: Optional[UserInDB],
        endpoint: str = "chat",
        client_ip: str = "unknown"
    ) -> bool:
        """
        Vérifie rate limiting multi-niveaux

        Args:
            user: Utilisateur (None si pas authentifié)
            endpoint: Endpoint appelé (chat, api, etc.)
            client_ip: IP client (pour anti-multi-comptes)

        Raises:
            HTTPException 429 si limite dépassée
        """
        if user is None:
            # User non authentifié → Strict rate limit par IP
            await self._check_ip_rate_limit(client_ip)
            return True

        user_id = user.id
        tier = getattr(user, 'tier', 'free')  # Default FREE si pas de tier

        now = int(time.time())
        minute = now // 60
        hour = now // 3600
        day = now // 86400

        # Clés Redis
        key_minute = f"ratelimit:{user_id}:{endpoint}:minute:{minute}"
        key_hour = f"ratelimit:{user_id}:{endpoint}:hour:{hour}"
        key_day = f"ratelimit:{user_id}:{endpoint}:day:{day}"

        # Récupérer compteurs actuels
        pipeline = self.redis.pipeline()
        pipeline.get(key_minute)
        pipeline.get(key_hour)
        pipeline.get(key_day)
        results = await pipeline.execute()

        count_minute = int(results[0]) if results[0] else 0
        count_hour = int(results[1]) if results[1] else 0
        count_day = int(results[2]) if results[2] else 0

        # Récupérer limites pour ce tier
        limits = self.limits.get(tier, self.limits["free"])

        # Check dépassements
        if count_minute >= limits["minute"]:
            logger.warning(
                f"Rate limit MINUTE exceeded for user {user_id} ({tier}): "
                f"{count_minute}/{limits['minute']}"
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "rate_limit_minute",
                    "message": f"Trop rapide! Maximum {limits['minute']} messages par minute. Ralentis un peu 😊",
                    "retry_after": 60 - (now % 60),  # Secondes jusqu'à prochaine minute
                    "limit": limits["minute"],
                    "current": count_minute
                }
            )

        if count_hour >= limits["hour"]:
            logger.warning(
                f"Rate limit HOUR exceeded for user {user_id} ({tier}): "
                f"{count_hour}/{limits['hour']}"
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "rate_limit_hour",
                    "message": f"Limite horaire atteinte ({limits['hour']} msg/h). Pause café? ☕",
                    "retry_after": 3600 - (now % 3600),
                    "limit": limits["hour"],
                    "current": count_hour
                }
            )

        if count_day >= limits["day"]:
            logger.warning(
                f"Rate limit DAY exceeded for user {user_id} ({tier}): "
                f"{count_day}/{limits['day']}"
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "rate_limit_day",
                    "message": f"Limite quotidienne atteinte ({limits['day']} msg/jour). À demain! 🌙",
                    "retry_after": 86400 - (now % 86400),
                    "limit": limits["day"],
                    "current": count_day,
                    "upgrade_url": "https://iafactoryalgeria.com/pricing" if tier == "free" else None
                }
            )

        # Incrémenter compteurs
        pipeline = self.redis.pipeline()

        # Minute
        pipeline.incr(key_minute)
        pipeline.expire(key_minute, 60)

        # Hour
        pipeline.incr(key_hour)
        pipeline.expire(key_hour, 3600)

        # Day
        pipeline.incr(key_day)
        pipeline.expire(key_day, 86400)

        await pipeline.execute()

        # Log usage
        logger.info(
            f"Rate limit OK - User: {user_id} ({tier}), "
            f"Counts: {count_minute+1}/min, {count_hour+1}/h, {count_day+1}/day"
        )

        return True

    async def _check_ip_rate_limit(self, client_ip: str):
        """
        Rate limit par IP pour users non authentifiés

        Protège contre:
        - Spam signup
        - Scraping
        - Attaques DDoS
        """
        now = int(time.time())
        minute = now // 60

        key_minute = f"ratelimit:ip:{client_ip}:minute:{minute}"
        count = await self.redis.get(key_minute)
        count = int(count) if count else 0

        # Limite stricte pour IP non authentifiée
        max_per_minute = 5

        if count >= max_per_minute:
            logger.warning(f"IP rate limit exceeded: {client_ip} ({count}/{max_per_minute})")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "ip_rate_limit",
                    "message": "Trop de requêtes depuis votre IP. Veuillez vous connecter.",
                    "retry_after": 60 - (now % 60)
                }
            )

        # Incrémenter
        pipeline = self.redis.pipeline()
        pipeline.incr(key_minute)
        pipeline.expire(key_minute, 60)
        await pipeline.execute()

    async def check_signup_rate(self, client_ip: str) -> bool:
        """
        Vérifie rate limit signup par IP (anti multi-comptes)

        Limite: 5 signups par heure par IP
        """
        now = int(time.time())
        hour = now // 3600

        key = f"signup:ip:{client_ip}:hour:{hour}"
        count = await self.redis.get(key)
        count = int(count) if count else 0

        max_signups = self.ip_limits["signups_per_hour_per_ip"]

        if count >= max_signups:
            logger.warning(
                f"Signup rate limit exceeded for IP {client_ip}: "
                f"{count}/{max_signups}"
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "signup_rate_limit",
                    "message": f"Trop d'inscriptions depuis votre IP ({max_signups}/heure max). Réessayez plus tard.",
                    "retry_after": 3600 - (now % 3600)
                }
            )

        # Incrémenter
        pipeline = self.redis.pipeline()
        pipeline.incr(key)
        pipeline.expire(key, 3600)
        await pipeline.execute()

        return True

    async def check_free_accounts_from_ip(self, client_ip: str) -> int:
        """
        Compte le nombre de comptes FREE créés depuis cette IP

        Si > 3 comptes FREE → Demander vérification téléphone

        Returns:
            Nombre de comptes FREE depuis cette IP
        """
        key = f"free_accounts:ip:{client_ip}"
        count = await self.redis.get(key)
        return int(count) if count else 0

    async def increment_free_account_from_ip(self, client_ip: str):
        """Incrémenter compteur comptes FREE par IP (permanent)"""
        key = f"free_accounts:ip:{client_ip}"
        await self.redis.incr(key)
        # Pas d'expiry → permanent (détection multi-comptes)

    async def detect_bot_behavior(self, user_id: int) -> bool:
        """
        Détecte comportement bot

        Signes:
        - Prompts très similaires (cosine similarity > 0.95)
        - Timing régulier (toutes les 10s exactement)
        - Pas de variation dans les questions

        Returns:
            True si comportement suspect détecté
        """
        # TODO: Implémenter détection avancée avec embeddings
        # Pour l'instant, juste placeholder
        return False

    async def soft_ban(self, user_id: int, duration_hours: int = 24):
        """
        Soft ban temporaire d'un user

        Args:
            user_id: ID user à bannir
            duration_hours: Durée du ban en heures
        """
        key = f"banned:user:{user_id}"
        await self.redis.setex(key, duration_hours * 3600, "1")

        logger.warning(f"User {user_id} soft-banned for {duration_hours}h")

    async def is_banned(self, user_id: int) -> bool:
        """Vérifie si user est banni"""
        key = f"banned:user:{user_id}"
        banned = await self.redis.get(key)
        return banned == "1"

    async def close(self):
        """Ferme la connexion Redis"""
        await self.redis.close()


# Singleton instance
_limiter_instance: Optional[RateLimiter] = None


def get_rate_limiter() -> RateLimiter:
    """Dependency pour FastAPI"""
    global _limiter_instance
    if _limiter_instance is None:
        _limiter_instance = RateLimiter()
    return _limiter_instance


# Middleware FastAPI
async def rate_limit_middleware(request: Request, call_next):
    """
    Middleware global pour rate limiting sur /api/chat

    Usage dans main.py:
        app.middleware("http")(rate_limit_middleware)
    """
    # Appliquer rate limiting uniquement sur endpoints chat/api
    if request.url.path in ["/api/chat", "/api/v1/chat", "/api/generate"]:

        # Récupérer IP client
        client_ip = request.client.host if request.client else "unknown"

        # Récupérer user depuis state (set par auth middleware)
        user = getattr(request.state, "user", None)

        # Vérifier rate limit
        limiter = get_rate_limiter()
        try:
            await limiter.check_rate_limit(user, "chat", client_ip)
        except HTTPException as e:
            # Re-raise HTTPException (sera géré par FastAPI)
            raise

    # Continuer la requête
    response = await call_next(request)
    return response
