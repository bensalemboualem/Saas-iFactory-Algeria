"""Tests pour le Session Manager"""

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
import json

from src.sessions import Session, SessionManager


class TestSession:
    """Tests du modèle Session"""

    def test_session_creation(self):
        """Test création d'une session"""
        session = Session(user_id="user123")
        assert session.user_id == "user123"
        assert session.id is not None
        assert session.context == {}
        assert session.history == []

    def test_session_with_context(self):
        """Test session avec contexte initial"""
        session = Session(
            user_id="user123",
            context={"project": "nexus"},
            current_project="nexus"
        )
        assert session.context["project"] == "nexus"
        assert session.current_project == "nexus"

    def test_session_serialization(self):
        """Test sérialisation JSON"""
        session = Session(user_id="user123")
        json_str = session.model_dump_json()
        assert "user123" in json_str
        assert "user_id" in json_str


class TestSessionManager:
    """Tests du SessionManager"""

    @pytest_asyncio.fixture
    async def mock_redis(self):
        """Mock Redis client"""
        mock = AsyncMock()
        mock.get = AsyncMock(return_value=None)
        mock.setex = AsyncMock()
        mock.delete = AsyncMock(return_value=1)
        mock.expire = AsyncMock(return_value=True)
        mock.keys = AsyncMock(return_value=[])
        mock.close = AsyncMock()
        return mock

    @pytest_asyncio.fixture
    async def manager(self, mock_redis):
        """SessionManager avec mock Redis"""
        with patch('src.sessions.redis.from_url', return_value=mock_redis):
            mgr = SessionManager("redis://localhost:6379", ttl=3600)
            mgr.redis = mock_redis
            yield mgr

    @pytest.mark.asyncio
    async def test_create_session(self, manager):
        """Test création de session"""
        session = await manager.create("user123")
        assert session.user_id == "user123"
        assert session.id is not None
        manager.redis.setex.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_session_with_context(self, manager):
        """Test création avec contexte"""
        session = await manager.create("user123", {"project": "nexus"})
        assert session.context["project"] == "nexus"

    @pytest.mark.asyncio
    async def test_get_session_not_found(self, manager):
        """Test session non trouvée"""
        manager.redis.get = AsyncMock(return_value=None)
        session = await manager.get("nonexistent")
        assert session is None

    @pytest.mark.asyncio
    async def test_get_session_found(self, manager):
        """Test session trouvée"""
        session_data = {
            "id": "sess123",
            "user_id": "user123",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "context": {},
            "current_project": None,
            "current_task": None,
            "current_target": None,
            "history": []
        }
        manager.redis.get = AsyncMock(return_value=json.dumps(session_data))

        session = await manager.get("sess123")
        assert session is not None
        assert session.id == "sess123"
        assert session.user_id == "user123"

    @pytest.mark.asyncio
    async def test_update_session(self, manager):
        """Test mise à jour de session"""
        session_data = {
            "id": "sess123",
            "user_id": "user123",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "context": {},
            "current_project": None,
            "current_task": None,
            "current_target": None,
            "history": []
        }
        manager.redis.get = AsyncMock(return_value=json.dumps(session_data))

        updated = await manager.update("sess123", current_project="nexus")
        assert updated is not None
        assert updated.current_project == "nexus"

    @pytest.mark.asyncio
    async def test_delete_session(self, manager):
        """Test suppression de session"""
        manager.redis.delete = AsyncMock(return_value=1)
        deleted = await manager.delete("sess123")
        assert deleted is True

    @pytest.mark.asyncio
    async def test_delete_session_not_found(self, manager):
        """Test suppression session inexistante"""
        manager.redis.delete = AsyncMock(return_value=0)
        deleted = await manager.delete("nonexistent")
        assert deleted is False

    @pytest.mark.asyncio
    async def test_add_to_history(self, manager):
        """Test ajout à l'historique"""
        session_data = {
            "id": "sess123",
            "user_id": "user123",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "context": {},
            "current_project": None,
            "current_task": None,
            "current_target": None,
            "history": []
        }
        manager.redis.get = AsyncMock(return_value=json.dumps(session_data))

        session = await manager.add_to_history("sess123", {"action": "test"})
        assert session is not None
        assert len(session.history) == 1
        assert session.history[0]["action"] == "test"

    @pytest.mark.asyncio
    async def test_refresh_session(self, manager):
        """Test renouvellement TTL"""
        manager.redis.expire = AsyncMock(return_value=True)
        result = await manager.refresh("sess123")
        assert result is True

    @pytest.mark.asyncio
    async def test_close(self, manager):
        """Test fermeture connexion"""
        await manager.close()
        manager.redis.close.assert_called_once()
