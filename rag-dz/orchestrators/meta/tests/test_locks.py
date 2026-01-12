"""Tests pour le Lock Manager"""

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch
from datetime import datetime, timedelta

from src.locks import Lock, LockManager, LockError


class TestLock:
    """Tests du modèle Lock"""

    def test_lock_creation(self):
        """Test création d'un lock"""
        now = datetime.utcnow()
        lock = Lock(
            resource="src/main.py",
            holder="bolt",
            acquired_at=now,
            expires_at=now + timedelta(seconds=300)
        )
        assert lock.resource == "src/main.py"
        assert lock.holder == "bolt"

    def test_lock_not_expired(self):
        """Test lock non expiré"""
        now = datetime.utcnow()
        lock = Lock(
            resource="test",
            holder="bolt",
            acquired_at=now,
            expires_at=now + timedelta(seconds=300)
        )
        assert lock.is_expired is False
        assert lock.remaining_seconds > 0

    def test_lock_expired(self):
        """Test lock expiré"""
        now = datetime.utcnow()
        lock = Lock(
            resource="test",
            holder="bolt",
            acquired_at=now - timedelta(seconds=600),
            expires_at=now - timedelta(seconds=300)
        )
        assert lock.is_expired is True
        assert lock.remaining_seconds == 0


class TestLockManager:
    """Tests du LockManager"""

    @pytest_asyncio.fixture
    async def mock_redis(self):
        """Mock Redis client"""
        mock = AsyncMock()
        mock.get = AsyncMock(return_value=None)
        mock.setex = AsyncMock()
        mock.delete = AsyncMock(return_value=1)
        mock.ttl = AsyncMock(return_value=300)
        mock.expire = AsyncMock(return_value=True)
        mock.keys = AsyncMock(return_value=[])
        mock.close = AsyncMock()
        return mock

    @pytest_asyncio.fixture
    async def manager(self, mock_redis):
        """LockManager avec mock Redis"""
        with patch('src.locks.redis.from_url', return_value=mock_redis):
            mgr = LockManager("redis://localhost:6379", default_ttl=300)
            mgr.redis = mock_redis
            yield mgr

    @pytest.mark.asyncio
    async def test_acquire_lock_success(self, manager):
        """Test acquisition de lock réussie"""
        manager.redis.get = AsyncMock(return_value=None)

        lock = await manager.acquire("src/main.py", "bolt")
        assert lock.resource == "src/main.py"
        assert lock.holder == "bolt"
        manager.redis.setex.assert_called_once()

    @pytest.mark.asyncio
    async def test_acquire_lock_already_held_by_same(self, manager):
        """Test: même holder peut re-acquérir"""
        manager.redis.get = AsyncMock(return_value="bolt")

        lock = await manager.acquire("src/main.py", "bolt")
        assert lock.holder == "bolt"

    @pytest.mark.asyncio
    async def test_acquire_lock_conflict(self, manager):
        """Test conflit de lock"""
        manager.redis.get = AsyncMock(return_value="bmad")

        with pytest.raises(LockError) as exc_info:
            await manager.acquire("src/main.py", "bolt")

        assert "bmad" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_acquire_lock_force(self, manager):
        """Test acquisition forcée"""
        manager.redis.get = AsyncMock(return_value="bmad")

        lock = await manager.acquire("src/main.py", "bolt", force=True)
        assert lock.holder == "bolt"

    @pytest.mark.asyncio
    async def test_release_lock_success(self, manager):
        """Test libération de lock réussie"""
        manager.redis.get = AsyncMock(return_value="bolt")

        released = await manager.release("src/main.py", "bolt")
        assert released is True
        manager.redis.delete.assert_called_once()

    @pytest.mark.asyncio
    async def test_release_lock_wrong_holder(self, manager):
        """Test: ne peut pas libérer le lock d'un autre"""
        manager.redis.get = AsyncMock(return_value="bmad")

        released = await manager.release("src/main.py", "bolt")
        assert released is False

    @pytest.mark.asyncio
    async def test_is_locked_true(self, manager):
        """Test vérification lock actif"""
        manager.redis.get = AsyncMock(return_value="bolt")

        locked, holder = await manager.is_locked("src/main.py")
        assert locked is True
        assert holder == "bolt"

    @pytest.mark.asyncio
    async def test_is_locked_false(self, manager):
        """Test vérification pas de lock"""
        manager.redis.get = AsyncMock(return_value=None)

        locked, holder = await manager.is_locked("src/main.py")
        assert locked is False
        assert holder is None

    @pytest.mark.asyncio
    async def test_list_locks_empty(self, manager):
        """Test liste locks vide"""
        manager.redis.keys = AsyncMock(return_value=[])

        locks = await manager.list_locks()
        assert locks == []

    @pytest.mark.asyncio
    async def test_extend_lock(self, manager):
        """Test extension de lock"""
        manager.redis.get = AsyncMock(return_value="bolt")
        manager.redis.ttl = AsyncMock(return_value=100)

        lock = await manager.extend("src/main.py", "bolt", 200)
        assert lock is not None
        manager.redis.expire.assert_called_once()

    @pytest.mark.asyncio
    async def test_extend_lock_wrong_holder(self, manager):
        """Test: ne peut pas étendre le lock d'un autre"""
        manager.redis.get = AsyncMock(return_value="bmad")

        lock = await manager.extend("src/main.py", "bolt", 200)
        assert lock is None

    def test_is_protected_critical(self, manager):
        """Test chemin critique protégé"""
        protected, level = manager.is_protected("migrations/001.sql")
        assert protected is True
        assert level == "critical"

    def test_is_protected_important(self, manager):
        """Test chemin important protégé"""
        protected, level = manager.is_protected("config/settings.py")
        assert protected is True
        assert level == "important"

    def test_is_not_protected(self, manager):
        """Test chemin non protégé"""
        protected, level = manager.is_protected("src/utils.py")
        assert protected is False
        assert level is None

    @pytest.mark.asyncio
    async def test_close(self, manager):
        """Test fermeture connexion"""
        await manager.close()
        manager.redis.close.assert_called_once()
