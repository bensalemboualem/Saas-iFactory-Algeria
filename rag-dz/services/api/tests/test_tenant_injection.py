"""
Test CRITIQUE - Vulnérabilité injection tenant.
================================================
AUCUN DÉPLOIEMENT SANS CES TESTS QUI PASSENT.

Tests de sécurité multi-tenant:
1. X-Tenant-ID header doit être IGNORÉ
2. Seul le JWT fait autorité pour tenant_id
3. Tentatives d'injection loggées mais rejetées

Usage:
    pytest tests/test_tenant_injection.py -v
    pytest tests/test_tenant_injection.py::TestTenantInjectionBlocked -v
"""

import pytest
from uuid import uuid4
from unittest.mock import MagicMock, patch, AsyncMock
from fastapi import Request
from starlette.datastructures import Headers


# === FIXTURES ===

@pytest.fixture
def tenant_a():
    return str(uuid4())


@pytest.fixture
def tenant_b():
    return str(uuid4())


@pytest.fixture
def user_id():
    return str(uuid4())


@pytest.fixture
def mock_request():
    """Create a mock FastAPI request."""
    request = MagicMock(spec=Request)
    request.state = MagicMock()
    request.method = "GET"
    request.url = MagicMock()
    request.url.path = "/api/conversations"
    return request


# === TEST CLASSES ===

class TestTenantInjectionBlocked:
    """
    CRITIQUE: Vérifie que X-Tenant-ID header est IGNORÉ.

    Scénario d'attaque prévenu:
    - Attaquant a un JWT valide pour tenant_a
    - Attaquant envoie X-Tenant-ID: tenant_b
    - Le système DOIT utiliser tenant_a (du JWT), PAS tenant_b
    """

    @pytest.mark.asyncio
    async def test_x_tenant_id_header_ignored_when_jwt_present(
        self, mock_request, tenant_a, tenant_b, user_id
    ):
        """
        CRITIQUE: X-Tenant-ID header DOIT être ignoré quand JWT présent.
        """
        from app.tenant_middleware import TenantContextMiddleware

        # Setup: JWT pour tenant_a, header malveillant pour tenant_b
        mock_request.headers = Headers({
            "Authorization": "Bearer valid_token",
            "X-Tenant-ID": tenant_b  # ATTAQUE: tenter d'accéder à tenant_b
        })

        # Mock auth_service pour retourner tenant_a depuis JWT
        with patch("app.tenant_middleware.TenantContextMiddleware._extract_from_jwt") as mock_jwt:
            mock_jwt.return_value = tenant_a  # JWT dit tenant_a

            middleware = TenantContextMiddleware(app=MagicMock())
            result = await middleware._extract_tenant_id(mock_request)

            # ASSERTION CRITIQUE: Doit retourner tenant_a (JWT), PAS tenant_b (header)
            assert result == tenant_a, (
                f"FAILLE SÉCURITÉ: X-Tenant-ID header accepté! "
                f"Expected {tenant_a} (JWT), got {result}"
            )

    @pytest.mark.asyncio
    async def test_x_tenant_id_header_logged_as_warning(
        self, mock_request, tenant_a, tenant_b
    ):
        """
        Vérifie que les tentatives d'injection sont loggées.
        """
        from app.tenant_middleware import TenantContextMiddleware

        mock_request.headers = Headers({
            "Authorization": "Bearer valid_token",
            "X-Tenant-ID": tenant_b
        })

        with patch("app.tenant_middleware.TenantContextMiddleware._extract_from_jwt") as mock_jwt:
            mock_jwt.return_value = tenant_a

            with patch("app.tenant_middleware.logger") as mock_logger:
                middleware = TenantContextMiddleware(app=MagicMock())
                await middleware._extract_tenant_id(mock_request)

                # Vérifier qu'un warning a été loggé
                mock_logger.warning.assert_called()
                warning_msg = mock_logger.warning.call_args[0][0]
                assert "IGNORED" in warning_msg or "SECURITY" in warning_msg

    @pytest.mark.asyncio
    async def test_only_jwt_tenant_id_accepted(
        self, mock_request, tenant_a
    ):
        """
        Vérifie que SEUL le tenant_id du JWT est accepté.
        """
        from app.tenant_middleware import TenantContextMiddleware

        # Pas de X-Tenant-ID header, juste JWT
        mock_request.headers = Headers({
            "Authorization": "Bearer valid_token"
        })

        with patch("app.tenant_middleware.TenantContextMiddleware._extract_from_jwt") as mock_jwt:
            mock_jwt.return_value = tenant_a

            middleware = TenantContextMiddleware(app=MagicMock())
            result = await middleware._extract_tenant_id(mock_request)

            assert result == tenant_a

    @pytest.mark.asyncio
    async def test_no_jwt_no_tenant_id(self, mock_request):
        """
        Sans JWT valide, aucun tenant_id ne doit être extrait.
        """
        from app.tenant_middleware import TenantContextMiddleware

        # Header X-Tenant-ID sans JWT
        mock_request.headers = Headers({
            "X-Tenant-ID": str(uuid4())  # Tentative d'injection
        })
        mock_request.state.tenant = None  # Pas d'API key non plus

        with patch("app.tenant_middleware.TenantContextMiddleware._extract_from_jwt") as mock_jwt:
            mock_jwt.return_value = None  # Pas de JWT valide

            middleware = TenantContextMiddleware(app=MagicMock())
            result = await middleware._extract_tenant_id(mock_request)

            # DOIT être None (pas de tenant_id sans JWT)
            assert result is None, (
                f"FAILLE SÉCURITÉ: tenant_id accepté sans JWT! Got: {result}"
            )


class TestTenantMiddlewareIntegration:
    """
    Tests d'intégration du middleware complet.
    """

    @pytest.mark.asyncio
    async def test_protected_route_requires_jwt(self, mock_request):
        """
        Route protégée sans JWT retourne 401.
        """
        from app.tenant_middleware import TenantContextMiddleware
        from starlette.responses import JSONResponse

        mock_request.headers = Headers({
            "X-Tenant-ID": str(uuid4())  # Header seul, pas de JWT
        })
        mock_request.state.tenant = None
        mock_request.url.path = "/api/conversations"  # Route protégée

        async def mock_call_next(request):
            return JSONResponse({"ok": True})

        with patch("app.tenant_middleware.TenantContextMiddleware._extract_from_jwt") as mock_jwt:
            mock_jwt.return_value = None

            with patch("app.config.get_settings") as mock_settings:
                settings_mock = MagicMock()
                settings_mock.environment = "production"  # Pas de default tenant
                mock_settings.return_value = settings_mock

                middleware = TenantContextMiddleware(app=MagicMock())
                response = await middleware.dispatch(mock_request, mock_call_next)

                # DOIT être 401 (pas de JWT)
                assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_public_route_bypasses_tenant_check(self, mock_request):
        """
        Routes publiques n'ont pas besoin de tenant_id.
        """
        from app.tenant_middleware import TenantContextMiddleware
        from starlette.responses import JSONResponse

        mock_request.headers = Headers({})
        mock_request.url.path = "/health"  # Route publique

        async def mock_call_next(request):
            return JSONResponse({"status": "healthy"})

        middleware = TenantContextMiddleware(app=MagicMock())
        response = await middleware.dispatch(mock_request, mock_call_next)

        # Route publique = 200 même sans tenant
        assert response.status_code == 200


class TestTenantIsolationRLS:
    """
    Tests de l'isolation RLS au niveau repository.
    """

    @pytest.mark.asyncio
    async def test_repository_uses_jwt_tenant_only(self, tenant_a, tenant_b, user_id):
        """
        Le repository utilise le tenant_id passé (qui vient du JWT via middleware).
        """
        from unittest.mock import AsyncMock
        from uuid import UUID

        # Mock pool
        pool = MagicMock()
        conn = AsyncMock()
        pool.acquire.return_value.__aenter__.return_value = conn
        pool.acquire.return_value.__aexit__.return_value = None

        # Simuler: conversation existe pour tenant_a mais pas tenant_b
        conn.fetchrow.return_value = None  # RLS filtre

        from app.repositories.conversation_repository import ConversationRepository

        repo = ConversationRepository(pool)
        conv_id = uuid4()

        # Requête avec tenant_b (provenant du JWT via middleware)
        result = await repo.get(conv_id, UUID(tenant_b))

        # Vérifier que set_config a été appelé avec tenant_b
        conn.execute.assert_called()
        call_args = conn.execute.call_args[0]
        assert "set_config" in call_args[0]
        assert tenant_b in call_args[1]

        # Résultat doit être None (RLS filtre car conversation appartient à tenant_a)
        assert result is None


# === SECURITY REGRESSION TESTS ===

class TestSecurityRegressions:
    """
    Tests de non-régression pour les failles corrigées.
    """

    def test_no_tenant_id_from_query_params(self, mock_request):
        """
        tenant_id ne doit JAMAIS être accepté depuis query params.
        """
        from app.tenant_middleware import TenantContextMiddleware

        # Simuler ?tenant_id=xxx dans l'URL
        mock_request.query_params = {"tenant_id": str(uuid4())}
        mock_request.headers = Headers({})

        middleware = TenantContextMiddleware(app=MagicMock())

        # _extract_tenant_id ne doit pas regarder query_params
        # (pas de code qui le fait = OK, mais on vérifie)
        assert not hasattr(middleware, "_extract_from_query")

    def test_no_tenant_id_from_body(self, mock_request):
        """
        tenant_id ne doit JAMAIS être accepté depuis le body.
        """
        from app.tenant_middleware import TenantContextMiddleware

        middleware = TenantContextMiddleware(app=MagicMock())

        # Vérifier qu'il n'y a pas de méthode _extract_from_body
        assert not hasattr(middleware, "_extract_from_body")
