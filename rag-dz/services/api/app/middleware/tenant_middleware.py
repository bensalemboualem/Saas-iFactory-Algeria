"""
Middleware tenant_id - JWT ONLY.
CRITIQUE: 401 par defaut sur toutes routes non publiques.

Ce middleware extrait tenant_id et user_id du JWT et les place dans request.state.
Les routes protegees DOIVENT utiliser get_tenant_id() et get_user_id() dependencies.
"""

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from jose import jwt, JWTError
import logging
import os

logger = logging.getLogger(__name__)

# Routes publiques (pas besoin de JWT)
PUBLIC_ROUTES = {
    "/",
    "/health",
    "/metrics",
    "/docs",
    "/openapi.json",
    "/redoc",
    "/api/auth/login",
    "/api/auth/register",
    "/api/auth/refresh",
    "/api/auth/forgot-password",
    "/api/auth/reset-password",
}

# Prefixes publics (routes qui commencent par...)
PUBLIC_PREFIXES = (
    "/static",
    "/api/public",
    "/api/webhook",  # Webhooks Chargily, Stripe, etc.
)


class TenantMiddleware(BaseHTTPMiddleware):
    """
    Extrait tenant_id du JWT.
    JAMAIS du body/query.
    401 par defaut si pas de token valide sur routes protegees.
    """

    def __init__(self, app, jwt_secret: str = None, jwt_algorithm: str = "HS256"):
        super().__init__(app)
        self.jwt_secret = jwt_secret or os.getenv("API_SECRET_KEY", "")
        self.jwt_algorithm = jwt_algorithm

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # OPTIONS = toujours OK (CORS preflight)
        if request.method == "OPTIONS":
            return await call_next(request)

        # Routes publiques = skip auth
        if self._is_public_route(path):
            request.state.tenant_id = None
            request.state.user_id = None
            return await call_next(request)

        # Extraire token
        auth_header = request.headers.get("Authorization")
        api_key = request.headers.get("X-API-Key")

        # Si X-API-Key presente, laisser AuthMiddleware gerer
        if api_key and not auth_header:
            request.state.tenant_id = None
            request.state.user_id = None
            return await call_next(request)

        # Si pas de Authorization header
        if not auth_header:
            return JSONResponse(
                {"error": "Authorization header missing", "code": "AUTH_MISSING"},
                status_code=401
            )

        # Valider format Bearer
        if not auth_header.startswith("Bearer "):
            return JSONResponse(
                {"error": "Invalid authorization format. Use: Bearer <token>", "code": "AUTH_FORMAT"},
                status_code=401
            )

        token = auth_header.split(" ", 1)[1]

        try:
            payload = jwt.decode(
                token,
                self.jwt_secret,
                algorithms=[self.jwt_algorithm]
            )

            tenant_id = payload.get("tenant_id")
            user_id = payload.get("user_id") or payload.get("sub")

            if not tenant_id:
                logger.warning(f"Token missing tenant_id claim: {payload.keys()}")
                return JSONResponse(
                    {"error": "Token missing tenant_id claim", "code": "TENANT_MISSING"},
                    status_code=401
                )

            if not user_id:
                logger.warning(f"Token missing user_id claim: {payload.keys()}")
                return JSONResponse(
                    {"error": "Token missing user_id claim", "code": "USER_MISSING"},
                    status_code=401
                )

            # Stocker dans request.state
            request.state.tenant_id = tenant_id
            request.state.user_id = user_id
            request.state.user_role = payload.get("role")
            request.state.jwt_payload = payload

        except jwt.ExpiredSignatureError:
            return JSONResponse(
                {"error": "Token expired", "code": "TOKEN_EXPIRED"},
                status_code=401
            )
        except JWTError as e:
            logger.warning(f"Invalid token: {e}")
            return JSONResponse(
                {"error": "Invalid token", "code": "TOKEN_INVALID"},
                status_code=401
            )

        return await call_next(request)

    def _is_public_route(self, path: str) -> bool:
        """Verifie si la route est publique."""
        if path in PUBLIC_ROUTES:
            return True

        for prefix in PUBLIC_PREFIXES:
            if path.startswith(prefix):
                return True

        return False


# === DEPENDENCIES ===

def get_tenant_id(request: Request) -> str:
    """
    FastAPI Dependency - recupere tenant_id.
    CRITIQUE: Utiliser ceci, JAMAIS lire du body.

    Usage:
        @router.get("/data")
        async def get_data(tenant_id: str = Depends(get_tenant_id)):
            ...
    """
    tenant_id = getattr(request.state, "tenant_id", None)
    if not tenant_id:
        raise HTTPException(status_code=401, detail="Tenant not identified")
    return tenant_id


def get_user_id(request: Request) -> str:
    """
    FastAPI Dependency - recupere user_id.

    Usage:
        @router.get("/profile")
        async def get_profile(user_id: str = Depends(get_user_id)):
            ...
    """
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="User not identified")
    return user_id


def get_user_role(request: Request) -> str:
    """FastAPI Dependency - recupere user role (owner, admin, member, viewer)."""
    return getattr(request.state, "user_role", "member")


def require_role(*allowed_roles: str):
    """
    Factory dependency pour verifier le role.

    Usage:
        @router.delete("/user/{id}")
        async def delete_user(
            id: str,
            _: str = Depends(require_role("owner", "admin"))
        ):
            ...
    """
    def dependency(request: Request) -> str:
        role = getattr(request.state, "user_role", None)
        if role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=f"Insufficient permissions. Required: {allowed_roles}, got: {role}"
            )
        return role
    return dependency
