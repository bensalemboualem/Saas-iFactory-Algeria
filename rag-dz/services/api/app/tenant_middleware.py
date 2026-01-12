"""
Multi-Tenant Context Middleware - Phase 3
==========================================
Extrait tenant_id de chaque requête et configure la session PostgreSQL RLS

Support:
- Header X-Tenant-ID (actuel)
- JWT avec tenant_id (Phase 4)
- API Key avec tenant associé (existant)
"""

import logging
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from typing import Optional
from uuid import UUID

logger = logging.getLogger(__name__)


class TenantContextMiddleware(BaseHTTPMiddleware):
    """
    Middleware pour extraire et valider le tenant_id de chaque requête

    Ordre de priorité:
    1. Header X-Tenant-ID (direct)
    2. JWT payload (Phase 4)
    3. API Key associé à un tenant (existant)

    Stocke le tenant_id dans request.state.tenant_id pour usage par DB session
    """

    # Routes publiques ne nécessitant pas de tenant_id
    PUBLIC_ROUTES = {
        "/",
        "/health",
        "/metrics",
        "/docs",
        "/openapi.json",
        "/redoc",
        "/api/auth/login",
        "/api/auth/login/json",  # Ajouté pour support login JSON
        "/api/auth/register",
        "/api/auth/refresh",
    }

    async def dispatch(self, request: Request, call_next):
        # Autoriser OPTIONS pour CORS
        if request.method == "OPTIONS":
            return await call_next(request)

        # Autoriser routes publiques
        if self._is_public_route(request.url.path):
            return await call_next(request)

        # Extraire tenant_id
        tenant_id = await self._extract_tenant_id(request)

        if not tenant_id:
            # En développement, utiliser DEFAULT_TENANT_ID
            from app.config import get_settings
            settings = get_settings()

            if settings.environment == "development" and settings.default_tenant_id:
                tenant_id = settings.default_tenant_id
                logger.info(f"Using DEFAULT_TENANT_ID for development: {tenant_id}")
            else:
                logger.warning(f"No tenant_id for request: {request.url.path}")
                return JSONResponse(
                    status_code=403,
                    content={
                        "error": "Tenant ID required",
                        "message": "X-Tenant-ID header or valid JWT required"
                    }
                )

        # Valider format UUID
        try:
            tenant_uuid = UUID(tenant_id)
        except ValueError:
            logger.error(f"Invalid tenant_id format: {tenant_id}")
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Invalid tenant ID format",
                    "message": "Tenant ID must be a valid UUID"
                }
            )

        # Stocker dans request.state pour usage par DB session
        request.state.tenant_id = str(tenant_uuid)

        # Log pour debugging
        logger.debug(f"Request tenant_id: {tenant_uuid} | Route: {request.url.path}")

        # Continuer la requête
        response = await call_next(request)

        # Ajouter header dans la réponse (utile pour debugging)
        response.headers["X-Tenant-Context"] = str(tenant_uuid)

        return response

    def _is_public_route(self, path: str) -> bool:
        """Vérifier si la route est publique"""
        # Exact match
        if path in self.PUBLIC_ROUTES:
            return True

        # Prefix match pour /docs, /openapi, etc.
        public_prefixes = ["/docs", "/redoc", "/openapi.json"]
        if any(path.startswith(prefix) for prefix in public_prefixes):
            return True

        return False

    async def _extract_tenant_id(self, request: Request) -> Optional[str]:
        """
        Extraire tenant_id depuis différentes sources

        Priorité:
        1. Header X-Tenant-ID (actuel - pour tests et API directe)
        2. JWT payload tenant_id (Phase 4)
        3. API Key → tenant mapping (existant via request.state.tenant)
        """

        # 1. Header X-Tenant-ID (direct)
        tenant_id = request.headers.get("X-Tenant-ID")
        if tenant_id:
            logger.debug(f"Tenant ID from header: {tenant_id}")
            return tenant_id

        # 2. JWT payload (Phase 4 - à implémenter)
        tenant_id = self._extract_from_jwt(request)
        if tenant_id:
            logger.debug(f"Tenant ID from JWT: {tenant_id}")
            return tenant_id

        # 3. API Key → tenant (existant via AuthMiddleware)
        if hasattr(request.state, "tenant") and request.state.tenant:
            tenant_id = request.state.tenant.get("id")
            if tenant_id:
                logger.debug(f"Tenant ID from API key: {tenant_id}")
                return tenant_id

        # Aucune source trouvée
        return None

    def _extract_from_jwt(self, request: Request) -> Optional[str]:
        """
        Extraire tenant_id depuis JWT (Phase 4)

        Format JWT attendu:
        {
            "sub": "user_email",
            "user_id": 123,
            "tenant_id": "550e8400-e29b-41d4-a716-446655440000",
            "exp": ...,
            "iat": ...
        }
        """
        # Récupérer Authorization header
        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            return None

        token = auth_header.replace("Bearer ", "")

        # Décoder JWT et extraire tenant_id
        try:
            from app.services.auth_service import auth_service

            # Décoder le token
            token_data = auth_service.decode_access_token(token)

            # Retourner tenant_id si présent
            if token_data.tenant_id:
                logger.debug(f"JWT tenant_id extracted: {token_data.tenant_id}")
                return token_data.tenant_id

            return None

        except Exception as e:
            logger.warning(f"Failed to decode JWT: {e}")
            return None


class SuperAdminMiddleware(BaseHTTPMiddleware):
    """
    Middleware optionnel pour mode super-admin

    Permet de bypass RLS pour support technique
    Active automatiquement enable_superadmin_mode() dans la DB session
    """

    # Super-admin API keys (à configurer via env)
    SUPERADMIN_KEYS = set()  # Rempli depuis config au démarrage

    async def dispatch(self, request: Request, call_next):
        # Vérifier si c'est un super-admin
        api_key = request.headers.get("X-API-Key", "")

        if api_key in self.SUPERADMIN_KEYS:
            # Marquer comme super-admin
            request.state.is_superadmin = True
            logger.info(f"Super-admin access: {request.url.path}")
        else:
            request.state.is_superadmin = False

        return await call_next(request)


# Helper function pour récupérer tenant_id depuis request
def get_request_tenant_id(request: Request) -> Optional[str]:
    """
    Helper pour récupérer tenant_id depuis request.state

    Usage dans les routers:
        from .tenant_middleware import get_request_tenant_id

        @router.get("/api/projects")
        async def list_projects(request: Request):
            tenant_id = get_request_tenant_id(request)
            # ...
    """
    return getattr(request.state, "tenant_id", None)


def is_superadmin_request(request: Request) -> bool:
    """
    Helper pour vérifier si la requête est en mode super-admin

    Usage:
        if is_superadmin_request(request):
            # Bypass RLS, voir tous les tenants
            pass
    """
    return getattr(request.state, "is_superadmin", False)
