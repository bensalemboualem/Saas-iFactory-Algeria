"""
Tests CRITIQUES - Aucun deploiement sans ces tests qui passent.

Tests:
1. Persistance apres restart
2. Isolation multi-tenant (CRITIQUE)
3. Optimistic locking / concurrence
4. Limite 100 messages

Usage:
    pytest tests/test_conversation_critical.py -v
    pytest tests/test_conversation_critical.py::TestTenantIsolation -v
"""

import pytest
import asyncio
import os
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock, patch

# Note: Ces tests necessitent une vraie DB PostgreSQL pour etre complets.
# En mode CI sans DB, on mock asyncpg.


# === FIXTURES ===

@pytest.fixture
def tenant_a():
    return uuid4()


@pytest.fixture
def tenant_b():
    return uuid4()


@pytest.fixture
def user_a():
    return uuid4()


@pytest.fixture
def user_b():
    return uuid4()


@pytest.fixture
def mock_pool():
    """Mock asyncpg pool pour tests unitaires."""
    pool = MagicMock()
    conn = AsyncMock()

    # Simuler acquire() context manager
    pool.acquire.return_value.__aenter__.return_value = conn
    pool.acquire.return_value.__aexit__.return_value = None

    return pool, conn


# === TEST CLASSES ===

class TestConversationRepository:
    """Tests unitaires du repository (mock DB)."""

    @pytest.mark.asyncio
    async def test_create_conversation(self, mock_pool, tenant_a, user_a):
        """Test creation conversation."""
        pool, conn = mock_pool

        # Mock response
        conn.fetchrow.return_value = {
            "id": uuid4(),
            "tenant_id": tenant_a,
            "user_id": user_a,
            "title": None,
            "model": "groq",
            "messages": "[]",
            "tokens_used": 0,
            "app_context": "chat",
            "version": 1,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00",
        }

        from app.repositories.conversation_repository import ConversationRepository

        repo = ConversationRepository(pool)
        result = await repo.create(tenant_a, user_a)

        assert result is not None
        assert result["version"] == 1
        assert result["messages"] == []

        # Verifier que set_tenant a ete appele
        conn.execute.assert_called_once()
        call_args = conn.execute.call_args[0]
        assert "set_config" in call_args[0]
        assert "app.current_tenant" in call_args[0]

    @pytest.mark.asyncio
    async def test_add_message_validates_content(self, mock_pool, tenant_a):
        """Test que add_message rejette les messages invalides."""
        pool, conn = mock_pool

        from app.repositories.conversation_repository import ConversationRepository

        repo = ConversationRepository(pool)
        conv_id = uuid4()

        # Message sans 'role'
        with pytest.raises(ValueError) as exc:
            await repo.add_message(
                conv_id, tenant_a,
                {"content": "test"},  # manque 'role'
                expected_version=1
            )
        assert "role" in str(exc.value)

        # Message sans 'content'
        with pytest.raises(ValueError) as exc:
            await repo.add_message(
                conv_id, tenant_a,
                {"role": "user"},  # manque 'content'
                expected_version=1
            )
        assert "content" in str(exc.value)


class TestTenantIsolation:
    """Test 2: Isolation multi-tenant (CRITIQUE)."""

    @pytest.mark.asyncio
    async def test_tenant_cannot_read_other_tenant(self, mock_pool, tenant_a, tenant_b, user_a):
        """Tenant B ne peut PAS lire les donnees de Tenant A."""
        pool, conn = mock_pool

        from app.repositories.conversation_repository import ConversationRepository

        repo = ConversationRepository(pool)
        conv_id = uuid4()

        # Simuler: conversation existe pour tenant_a mais pas tenant_b
        conn.fetchrow.return_value = None  # Pas trouve (RLS filtre)

        result = await repo.get(conv_id, tenant_b)

        # DOIT etre None
        assert result is None

    @pytest.mark.asyncio
    async def test_tenant_cannot_write_other_tenant(self, mock_pool, tenant_a, tenant_b, user_a):
        """Tenant B ne peut PAS modifier les donnees de Tenant A."""
        pool, conn = mock_pool

        from app.repositories.conversation_repository import (
            ConversationRepository,
            ConversationNotFoundError
        )

        repo = ConversationRepository(pool)
        conv_id = uuid4()

        # Simuler: SELECT retourne None (RLS filtre)
        conn.fetchrow.return_value = None

        with pytest.raises(ConversationNotFoundError):
            await repo.add_message(
                conv_id, tenant_b,  # MAUVAIS tenant
                {"role": "user", "content": "Hack attempt"},
                expected_version=1
            )


class TestOptimisticLocking:
    """Test 3: Concurrence reelle."""

    @pytest.mark.asyncio
    async def test_version_mismatch_raises_conflict(self, mock_pool, tenant_a, user_a):
        """
        Si la version en DB != version attendue, lever ConversationConflictError.
        """
        pool, conn = mock_pool

        from app.repositories.conversation_repository import (
            ConversationRepository,
            ConversationConflictError
        )

        repo = ConversationRepository(pool)
        conv_id = uuid4()

        # SELECT retourne version=5, msg_count=10
        conn.fetchrow.side_effect = [
            {"version": 5, "msg_count": 10},  # Premier fetchrow (check)
            None  # UPDATE retourne 0 rows (version mismatch)
        ]

        with pytest.raises(ConversationConflictError) as exc:
            await repo.add_message(
                conv_id, tenant_a,
                {"role": "user", "content": "Test"},
                expected_version=3  # != 5
            )

        assert "mismatch" in str(exc.value).lower()

    @pytest.mark.asyncio
    async def test_successful_update_with_correct_version(self, mock_pool, tenant_a, user_a):
        """Update reussit avec la bonne version."""
        pool, conn = mock_pool

        from app.repositories.conversation_repository import ConversationRepository

        repo = ConversationRepository(pool)
        conv_id = uuid4()

        # SELECT retourne version=1
        # UPDATE retourne la row mise a jour
        conn.fetchrow.side_effect = [
            {"version": 1, "msg_count": 0},  # Check
            {  # UPDATE result
                "id": conv_id,
                "tenant_id": tenant_a,
                "user_id": user_a,
                "title": None,
                "model": "groq",
                "messages": '[{"role":"user","content":"Test"}]',
                "tokens_used": 0,
                "app_context": "chat",
                "version": 2,  # Incremente par trigger
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:01",
            }
        ]

        result = await repo.add_message(
            conv_id, tenant_a,
            {"role": "user", "content": "Test"},
            expected_version=1
        )

        assert result is not None
        assert result["version"] == 2


class TestMessageLimit:
    """Test 4: Limite 100 messages."""

    @pytest.mark.asyncio
    async def test_rejects_message_at_limit(self, mock_pool, tenant_a, user_a):
        """Le 101eme message est refuse."""
        pool, conn = mock_pool

        from app.repositories.conversation_repository import (
            ConversationRepository,
            ConversationFullError
        )

        repo = ConversationRepository(pool)
        conv_id = uuid4()

        # SELECT retourne msg_count=100 (a la limite)
        conn.fetchrow.return_value = {"version": 50, "msg_count": 100}

        with pytest.raises(ConversationFullError) as exc:
            await repo.add_message(
                conv_id, tenant_a,
                {"role": "user", "content": "Message 101"},
                expected_version=50
            )

        assert "100" in str(exc.value)
        assert "Archive" in str(exc.value)

    @pytest.mark.asyncio
    async def test_accepts_message_under_limit(self, mock_pool, tenant_a, user_a):
        """Message accepte si < 100."""
        pool, conn = mock_pool

        from app.repositories.conversation_repository import ConversationRepository

        repo = ConversationRepository(pool)
        conv_id = uuid4()

        # msg_count=99, donc on peut ajouter
        conn.fetchrow.side_effect = [
            {"version": 1, "msg_count": 99},
            {
                "id": conv_id,
                "tenant_id": tenant_a,
                "user_id": user_a,
                "title": None,
                "model": "groq",
                "messages": "[]",
                "tokens_used": 0,
                "app_context": "chat",
                "version": 2,
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:01",
            }
        ]

        result = await repo.add_message(
            conv_id, tenant_a,
            {"role": "user", "content": "Message 100"},
            expected_version=1
        )

        assert result is not None


class TestPersistence:
    """Test 1: Persistance apres restart."""

    @pytest.mark.asyncio
    async def test_get_returns_stored_data(self, mock_pool, tenant_a, user_a):
        """Les donnees sont recuperables apres stockage."""
        pool, conn = mock_pool

        from app.repositories.conversation_repository import ConversationRepository

        repo = ConversationRepository(pool)
        conv_id = uuid4()

        # Simuler donnees en DB
        conn.fetchrow.return_value = {
            "id": conv_id,
            "tenant_id": tenant_a,
            "user_id": user_a,
            "title": "Test Conversation",
            "model": "groq",
            "messages": '[{"role":"user","content":"Hello"}]',
            "tokens_used": 10,
            "app_context": "chat",
            "version": 2,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:01",
        }

        result = await repo.get(conv_id, tenant_a)

        assert result is not None
        assert result["title"] == "Test Conversation"
        assert len(result["messages"]) == 1
        assert result["messages"][0]["content"] == "Hello"


class TestMiddleware:
    """Tests du TenantMiddleware."""

    def test_public_routes_bypass_auth(self):
        """Routes publiques ne requierent pas de JWT."""
        from app.middleware.tenant_middleware import TenantMiddleware

        middleware = TenantMiddleware(None, jwt_secret="test")

        # Ces routes doivent etre publiques
        assert middleware._is_public_route("/health") is True
        assert middleware._is_public_route("/docs") is True
        assert middleware._is_public_route("/api/auth/login") is True
        assert middleware._is_public_route("/static/file.js") is True

        # Ces routes doivent etre protegees
        assert middleware._is_public_route("/api/conversations") is False
        assert middleware._is_public_route("/api/memory") is False


# === INTEGRATION TESTS (require real DB) ===

@pytest.mark.skipif(
    os.getenv("TEST_DATABASE_URL") is None,
    reason="Requires TEST_DATABASE_URL for integration tests"
)
class TestIntegrationWithRealDB:
    """
    Tests d'integration avec vraie DB PostgreSQL.

    Requis:
    - TEST_DATABASE_URL env var
    - Migration 015 executee
    - Tables conversations, tenants, users creees
    """

    @pytest.fixture
    async def real_pool(self):
        """Pool asyncpg reel."""
        import asyncpg
        pool = await asyncpg.create_pool(os.getenv("TEST_DATABASE_URL"))
        yield pool
        await pool.close()

    @pytest.fixture
    async def setup_tenants(self, real_pool):
        """Creer tenants de test."""
        tenant_a = uuid4()
        tenant_b = uuid4()
        user_a = uuid4()

        async with real_pool.acquire() as conn:
            # Creer tenants
            await conn.execute("""
                INSERT INTO tenants (id, name, slug, plan, status)
                VALUES ($1, 'Tenant A', 'tenant-a', 'free', 'active'),
                       ($2, 'Tenant B', 'tenant-b', 'free', 'active')
                ON CONFLICT (id) DO NOTHING
            """, tenant_a, tenant_b)

            # Creer user
            await conn.execute("""
                INSERT INTO users (id, tenant_id, email, password_hash, name)
                VALUES ($1, $2, 'test@a.com', 'hash', 'Test User')
                ON CONFLICT (id) DO NOTHING
            """, user_a, tenant_a)

        yield {"tenant_a": tenant_a, "tenant_b": tenant_b, "user_a": user_a}

        # Cleanup
        async with real_pool.acquire() as conn:
            await conn.execute(
                "DELETE FROM conversations WHERE tenant_id IN ($1, $2)",
                tenant_a, tenant_b
            )

    @pytest.mark.asyncio
    async def test_real_tenant_isolation(self, real_pool, setup_tenants):
        """Test isolation avec vraie DB."""
        from app.repositories.conversation_repository import ConversationRepository

        repo = ConversationRepository(real_pool)
        t = setup_tenants

        # Tenant A cree une conversation
        conv = await repo.create(
            t["tenant_a"], t["user_a"],
            app_context="test"
        )

        # Tenant A peut lire
        result_a = await repo.get(conv["id"], t["tenant_a"])
        assert result_a is not None

        # Tenant B NE PEUT PAS lire (RLS)
        result_b = await repo.get(conv["id"], t["tenant_b"])
        assert result_b is None

    @pytest.mark.asyncio
    async def test_real_optimistic_locking(self, real_pool, setup_tenants):
        """Test concurrence avec vraie DB."""
        from app.repositories.conversation_repository import (
            ConversationRepository,
            ConversationConflictError
        )

        repo = ConversationRepository(real_pool)
        t = setup_tenants

        # Creer conversation
        conv = await repo.create(t["tenant_a"], t["user_a"])

        # Premier update (v1 -> v2)
        await repo.add_message(
            conv["id"], t["tenant_a"],
            {"role": "user", "content": "First"},
            expected_version=1
        )

        # Deuxieme update avec MAUVAISE version
        with pytest.raises(ConversationConflictError):
            await repo.add_message(
                conv["id"], t["tenant_a"],
                {"role": "user", "content": "Second"},
                expected_version=1  # Devrait etre 2
            )

    @pytest.mark.asyncio
    async def test_real_concurrent_updates(self, real_pool, setup_tenants):
        """Test vrai parallele - 1 succes, 1 echec."""
        from app.repositories.conversation_repository import (
            ConversationRepository,
            ConversationConflictError
        )

        repo = ConversationRepository(real_pool)
        t = setup_tenants

        conv = await repo.create(t["tenant_a"], t["user_a"])

        async def add_msg(content: str):
            return await repo.add_message(
                conv["id"], t["tenant_a"],
                {"role": "user", "content": content},
                expected_version=1
            )

        # Lancer 2 updates en parallele
        results = await asyncio.gather(
            add_msg("Message A"),
            add_msg("Message B"),
            return_exceptions=True
        )

        successes = [r for r in results if isinstance(r, dict)]
        conflicts = [r for r in results if isinstance(r, ConversationConflictError)]

        assert len(successes) == 1
        assert len(conflicts) == 1
