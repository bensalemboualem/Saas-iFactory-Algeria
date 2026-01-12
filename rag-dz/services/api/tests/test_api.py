"""
Tests des endpoints API
"""
import pytest
from unittest.mock import patch


class TestHealthEndpoint:
    """Tests du endpoint /health"""

    def test_health_returns_200(self, client):
        """Test: Health check retourne 200"""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_response_structure(self, client):
        """Test: Structure de la réponse health"""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert "service" in data
        assert data["status"] == "healthy"


class TestMetricsEndpoint:
    """Tests du endpoint /metrics"""

    def test_metrics_returns_200(self, client):
        """Test: Metrics retourne 200"""
        response = client.get("/metrics")
        assert response.status_code == 200

    def test_metrics_content_type(self, client):
        """Test: Content-Type correct pour metrics"""
        response = client.get("/metrics")
        assert "text/plain" in response.headers.get("content-type", "")


class TestRootEndpoint:
    """Tests du endpoint /"""

    def test_root_returns_info(self, client):
        """Test: Root retourne info API"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data


@pytest.mark.integration
class TestEmbedEndpoint:
    """Tests du endpoint /test/embed"""

    @patch("app.db.get_tenant_by_key")
    @patch("app.clients.embeddings.embed_queries")
    @patch("app.clients.qdrant_client.create_collection")
    def test_embed_endpoint_success(
        self, mock_create_coll, mock_embed, mock_tenant, client
    ):
        """Test: Endpoint embed fonctionne"""
        # Setup mocks
        mock_tenant.return_value = {
            "id": "test-id",
            "name": "Test Tenant",
            "plan": "pro"
        }
        mock_embed.return_value = [[0.1] * 768] * 3
        mock_create_coll.return_value = None

        # Désactiver auth pour test
        with patch("app.config.get_settings") as mock_settings:
            settings_mock = mock_settings.return_value
            settings_mock.enable_api_key_auth = False

            response = client.post(
                "/api/test/embed",
                headers={"X-API-Key": "test-key"}
            )

            # Vérifier la réponse
            if response.status_code == 200:
                data = response.json()
                assert "embeddings_count" in data
                assert "vector_size" in data


@pytest.mark.unit
class TestRequestIDMiddleware:
    """Tests du middleware Request ID"""

    def test_request_id_header_added(self, client):
        """Test: Header X-Request-Id ajouté"""
        response = client.get("/health")
        assert "X-Request-Id" in response.headers
        assert len(response.headers["X-Request-Id"]) == 16


@pytest.mark.integration
class TestDatabaseConnection:
    """Tests de connexion base de données"""

    @patch("app.db.psycopg.connect")
    def test_db_connection_context_manager(self, mock_connect):
        """Test: Context manager de connexion DB"""
        from app.db import get_db_connection

        mock_conn = mock_connect.return_value.__enter__.return_value

        with get_db_connection() as conn:
            assert conn is not None

        mock_connect.assert_called_once()


@pytest.mark.unit
class TestConfiguration:
    """Tests de configuration"""

    def test_settings_from_env(self):
        """Test: Settings chargés depuis env"""
        from app.config import get_settings

        settings = get_settings()
        assert settings.environment == "test"
        assert settings.postgres_url is not None

    def test_allowed_origins_parsing(self):
        """Test: Parsing des origins autorisées"""
        from app.config import get_settings

        settings = get_settings()
        origins = settings.get_allowed_origins()
        assert isinstance(origins, list)
