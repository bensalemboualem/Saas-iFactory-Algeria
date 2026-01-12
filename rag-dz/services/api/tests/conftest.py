"""
Pytest fixtures et configuration
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import os

# Configurer l'environnement de test
os.environ["ENVIRONMENT"] = "test"
os.environ["POSTGRES_URL"] = "postgresql://test:test@localhost:5432/test_db"
os.environ["REDIS_URL"] = "redis://localhost:6379/1"
os.environ["ENABLE_RATE_LIMITING"] = "false"
os.environ["ENABLE_API_KEY_AUTH"] = "false"


@pytest.fixture(scope="session")
def test_app():
    """Fixture pour l'application FastAPI"""
    from app.main import app
    return app


@pytest.fixture(scope="function")
def client(test_app):
    """Fixture pour le client de test"""
    return TestClient(test_app)


@pytest.fixture(scope="function")
def auth_client(test_app):
    """Fixture pour client authentifié"""
    client = TestClient(test_app)
    # Ajouter header d'authentification
    client.headers.update({"X-API-Key": "test-api-key"})
    return client


@pytest.fixture(scope="function")
def mock_db():
    """Mock de la base de données"""
    with patch("app.db.get_db_connection") as mock:
        conn_mock = Mock()
        cursor_mock = Mock()
        cursor_mock.fetchone.return_value = None
        cursor_mock.fetchall.return_value = []
        conn_mock.cursor.return_value.__enter__.return_value = cursor_mock
        mock.return_value.__enter__.return_value = conn_mock
        yield mock


@pytest.fixture(scope="function")
def mock_tenant():
    """Mock d'un tenant valide"""
    return {
        "id": "test-tenant-id",
        "name": "Test Tenant",
        "plan": "pro",
        "rate_limit_per_minute": 100,
        "quota_tokens": 1000000,
        "quota_audio_seconds": 3600,
        "quota_ocr_pages": 100
    }


@pytest.fixture(scope="function")
def mock_embeddings():
    """Mock des embeddings"""
    with patch("app.clients.embeddings.embed_queries") as mock:
        mock.return_value = [[0.1] * 768 for _ in range(3)]
        yield mock


@pytest.fixture(scope="function")
def mock_qdrant():
    """Mock de Qdrant"""
    with patch("app.clients.qdrant_client.create_collection") as mock_create:
        with patch("app.clients.qdrant_client.search_vectors") as mock_search:
            mock_search.return_value = []
            yield {"create": mock_create, "search": mock_search}


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    """Reset rate limiter entre les tests"""
    from app.security import rate_limiter
    rate_limiter.requests.clear()
    yield
