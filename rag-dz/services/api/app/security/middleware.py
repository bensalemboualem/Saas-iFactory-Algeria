"""
Security utilities: rate limiting, CORS, authentication
"""
import time
import hashlib
import logging
from typing import Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from ..config import get_settings
from ..db import get_tenant_by_key

logger = logging.getLogger(__name__)
settings = get_settings()


class RateLimiter:
    """
    In-memory rate limiter avec sliding window
    Pour production, utiliser Redis
    """

    def __init__(self):
        self.requests: Dict[str, list] = defaultdict(list)
        self.minute_limit = settings.rate_limit_per_minute
        self.hour_limit = settings.rate_limit_per_hour
        self.burst_limit = settings.rate_limit_burst

    def _clean_old_requests(self, key: str, window_seconds: int):
        """Nettoie les requêtes expirées"""
        now = time.time()
        cutoff = now - window_seconds
        self.requests[key] = [req_time for req_time in self.requests[key] if req_time > cutoff]

    def check_rate_limit(self, identifier: str, weight: int = 1) -> tuple[bool, Optional[int]]:
        """
        Vérifie les limites de débit
        Returns: (is_allowed, retry_after_seconds)
        """
        if not settings.enable_rate_limiting:
            return True, None

        now = time.time()

        # Nettoyer les anciennes entrées
        self._clean_old_requests(identifier, 3600)  # 1 heure

        # Vérifier burst (dernières secondes)
        recent_requests = [t for t in self.requests[identifier] if now - t < 1]
        if len(recent_requests) >= self.burst_limit:
            return False, 1

        # Vérifier limite par minute
        minute_requests = [t for t in self.requests[identifier] if now - t < 60]
        if len(minute_requests) >= self.minute_limit:
            oldest = min(minute_requests)
            retry_after = int(60 - (now - oldest)) + 1
            return False, retry_after

        # Vérifier limite par heure
        hour_requests = self.requests[identifier]
        if len(hour_requests) >= self.hour_limit:
            oldest = min(hour_requests)
            retry_after = int(3600 - (now - oldest)) + 1
            return False, retry_after

        # Ajouter la requête
        self.requests[identifier].append(now)
        return True, None

    def get_usage_stats(self, identifier: str) -> dict:
        """Retourne les statistiques d'utilisation"""
        now = time.time()
        minute_requests = [t for t in self.requests[identifier] if now - t < 60]
        hour_requests = self.requests[identifier]

        return {
            "requests_last_minute": len(minute_requests),
            "requests_last_hour": len(hour_requests),
            "minute_limit": self.minute_limit,
            "hour_limit": self.hour_limit,
            "minute_remaining": max(0, self.minute_limit - len(minute_requests)),
            "hour_remaining": max(0, self.hour_limit - len(hour_requests))
        }


# Instance globale
rate_limiter = RateLimiter()


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware de rate limiting"""

    async def dispatch(self, request: Request, call_next):
        # Skip pour routes publiques
        if request.url.path in ["/health", "/metrics", "/docs", "/openapi.json", "/"]:
            return await call_next(request)

        # Identifier (IP + tenant)
        client_ip = request.client.host if request.client else "unknown"
        tenant_id = getattr(request.state, "tenant", {}).get("id", "anonymous")
        identifier = f"{tenant_id}:{client_ip}"

        # Vérifier rate limit
        is_allowed, retry_after = rate_limiter.check_rate_limit(identifier)

        if not is_allowed:
            logger.warning(f"Rate limit exceeded for {identifier}")
            return JSONResponse(
                {
                    "error": "Rate limit exceeded",
                    "retry_after": retry_after,
                    "message": f"Too many requests. Please retry after {retry_after} seconds."
                },
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                headers={"Retry-After": str(retry_after)}
            )

        # Ajouter headers de rate limit
        response = await call_next(request)
        stats = rate_limiter.get_usage_stats(identifier)
        response.headers["X-RateLimit-Limit"] = str(settings.rate_limit_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(stats["minute_remaining"])
        response.headers["X-RateLimit-Reset"] = str(int(time.time()) + 60)

        return response


class EnhancedAuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware d'authentification amélioré avec:
    - Validation tenant
    - Logging sécurisé
    - Headers de sécurité
    """

    async def dispatch(self, request: Request, call_next):
        # OPTIONS pour CORS
        if request.method == "OPTIONS":
            return await call_next(request)

        # Routes publiques
        public_routes = ["/health", "/metrics", "/docs", "/openapi.json", "/"]
        # Allow frontend access without auth for essential endpoints
        public_api_prefixes = [
            "/api/bmad",
            "/api/dzirvideo",
            "/api/agent-chat",
            "/api/credentials",  # AI models & API keys
            "/api/query",        # RAG queries
            "/api/upload",       # File uploads
            "/api/knowledge",    # Knowledge base
            "/api/progress",     # Progress tracking
            "/api/test",         # Test endpoints
            "/api/websocket"     # WebSocket
        ]

        if request.url.path in public_routes or any(request.url.path.startswith(prefix) for prefix in public_api_prefixes):
            return await call_next(request)

        # Vérifier API key si activé
        if settings.enable_api_key_auth:
            api_key = (
                request.headers.get("X-API-Key") or
                request.headers.get("Authorization", "").replace("Bearer ", "")
            )

            if not api_key:
                logger.warning(f"Missing API key from {request.client.host if request.client else 'unknown'}")
                return JSONResponse(
                    {"error": "API key required", "details": "Provide API key via X-API-Key header"},
                    status_code=status.HTTP_401_UNAUTHORIZED
                )

            # Dev bypass: accept API_SECRET_KEY directly
            if api_key == settings.api_secret_key:
                request.state.tenant = {"id": "dev", "name": "Development", "plan": "enterprise"}
            else:
                tenant = get_tenant_by_key(api_key)
                if not tenant:
                    logger.warning(f"Invalid API key attempt from {request.client.host if request.client else 'unknown'}")
                    return JSONResponse(
                        {"error": "Invalid API key"},
                        status_code=status.HTTP_401_UNAUTHORIZED
                    )
                request.state.tenant = tenant

            # Vérifier statut tenant (only if not dev tenant)
            if request.state.tenant.get("id") != "dev":
                if request.state.tenant.get("plan") == "free" and request.url.path.startswith("/api/premium"):
                    return JSONResponse(
                        {"error": "Upgrade required", "message": "This endpoint requires a Pro or Enterprise plan"},
                        status_code=status.HTTP_403_FORBIDDEN
                    )

        # Continuer avec la requête
        response = await call_next(request)

        # Ajouter headers de sécurité
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        return response


def hash_api_key(api_key: str) -> str:
    """Hash API key avec algorithme configuré"""
    return hashlib.sha256(api_key.encode()).hexdigest()


def validate_api_key_format(api_key: str) -> bool:
    """Valide le format de l'API key"""
    if not api_key or len(api_key) < 20:
        return False
    # Format attendu: ragdz_<env>_<random>
    if not api_key.startswith("ragdz_"):
        return False
    return True
