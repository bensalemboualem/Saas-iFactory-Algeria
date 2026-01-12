"""
Repository conversations - asyncpg + optimistic locking.
CRITIQUE: Pas de FOR UPDATE, uniquement version check.

Decisions verrouillees:
- Max 100 messages par conversation
- Optimistic lock via version field
- tenant_id depuis JWT uniquement (jamais du client)
- RLS via set_config
"""

from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
import json
import logging
import asyncpg

logger = logging.getLogger(__name__)


class ConversationRepository:
    """
    Repository avec:
    - Optimistic locking (version field, PAS de FOR UPDATE)
    - RLS via set_config
    - Limite 100 messages
    - COALESCE pour eviter NULL
    """

    MAX_MESSAGES = 100

    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def _set_tenant(self, conn: asyncpg.Connection, tenant_id: UUID):
        """
        Configure RLS pour cette transaction.
        CRITIQUE: Doit etre appele AVANT chaque requete.
        """
        await conn.execute(
            "SELECT set_config('app.current_tenant', $1, true)",
            str(tenant_id)
        )

    async def get(
        self,
        conversation_id: UUID,
        tenant_id: UUID
    ) -> Optional[Dict[str, Any]]:
        """Recupere une conversation."""
        async with self.pool.acquire() as conn:
            await self._set_tenant(conn, tenant_id)

            row = await conn.fetchrow(
                """
                SELECT id, tenant_id, user_id, title, model,
                       COALESCE(messages, '[]'::jsonb) as messages,
                       tokens_used, app_context, version,
                       created_at, updated_at
                FROM conversations
                WHERE id = $1 AND tenant_id = $2
                """,
                conversation_id, tenant_id
            )

            if not row:
                return None

            return self._row_to_dict(row)

    async def create(
        self,
        tenant_id: UUID,
        user_id: UUID,
        app_context: str = "chat",
        title: str = None,
        model: str = "groq"
    ) -> Dict[str, Any]:
        """Cree une nouvelle conversation."""
        async with self.pool.acquire() as conn:
            await self._set_tenant(conn, tenant_id)

            row = await conn.fetchrow(
                """
                INSERT INTO conversations
                    (tenant_id, user_id, app_context, title, model, messages, version)
                VALUES ($1, $2, $3, $4, $5, '[]'::jsonb, 1)
                RETURNING id, tenant_id, user_id, title, model,
                          messages, tokens_used, app_context,
                          version, created_at, updated_at
                """,
                tenant_id, user_id, app_context, title, model
            )

            result = self._row_to_dict(row)
            result["messages"] = []
            return result

    async def add_message(
        self,
        conversation_id: UUID,
        tenant_id: UUID,
        message: Dict[str, Any],
        expected_version: int
    ) -> Dict[str, Any]:
        """
        Ajoute un message avec OPTIMISTIC LOCK ONLY.

        PAS de FOR UPDATE - on fait:
        1. SELECT pour verifier taille (sans lock)
        2. UPDATE ... WHERE version = expected_version
        3. Si 0 rows -> ConversationConflictError

        Args:
            conversation_id: ID conversation
            tenant_id: Tenant (from JWT, JAMAIS du client)
            message: {"role": "user|assistant", "content": "..."}
            expected_version: Version attendue

        Raises:
            ConversationNotFoundError: Conversation inexistante
            ConversationConflictError: Version mismatch (concurrent update)
            ConversationFullError: >= 100 messages
        """
        # Valider message
        if "role" not in message or "content" not in message:
            raise ValueError("Message must have 'role' and 'content'")

        message["timestamp"] = message.get("timestamp", datetime.utcnow().isoformat())

        async with self.pool.acquire() as conn:
            await self._set_tenant(conn, tenant_id)

            # 1. Verifier taille actuelle (SANS FOR UPDATE)
            check = await conn.fetchrow(
                """
                SELECT
                    version,
                    jsonb_array_length(COALESCE(messages, '[]'::jsonb)) as msg_count
                FROM conversations
                WHERE id = $1 AND tenant_id = $2
                """,
                conversation_id, tenant_id
            )

            if not check:
                raise ConversationNotFoundError(
                    f"Conversation {conversation_id} not found for tenant {tenant_id}"
                )

            if check["msg_count"] >= self.MAX_MESSAGES:
                raise ConversationFullError(
                    f"Conversation has {check['msg_count']} messages (max {self.MAX_MESSAGES}). "
                    f"Archive required."
                )

            # 2. UPDATE avec version check (OPTIMISTIC LOCK)
            row = await conn.fetchrow(
                """
                UPDATE conversations
                SET messages = COALESCE(messages, '[]'::jsonb) || $3::jsonb
                WHERE id = $1 AND tenant_id = $2 AND version = $4
                RETURNING id, tenant_id, user_id, title, model,
                          messages, tokens_used, app_context,
                          version, created_at, updated_at
                """,
                conversation_id, tenant_id,
                json.dumps([message]), expected_version
            )

            # 3. Si 0 rows -> conflit de version
            if not row:
                raise ConversationConflictError(
                    f"Version mismatch: expected {expected_version}, "
                    f"current is {check['version']}. Reload and retry."
                )

            return self._row_to_dict(row)

    async def update_title(
        self,
        conversation_id: UUID,
        tenant_id: UUID,
        title: str,
        expected_version: int
    ) -> Dict[str, Any]:
        """Met a jour le titre avec optimistic lock."""
        async with self.pool.acquire() as conn:
            await self._set_tenant(conn, tenant_id)

            row = await conn.fetchrow(
                """
                UPDATE conversations
                SET title = $3
                WHERE id = $1 AND tenant_id = $2 AND version = $4
                RETURNING id, tenant_id, user_id, title, model,
                          messages, tokens_used, app_context,
                          version, created_at, updated_at
                """,
                conversation_id, tenant_id, title, expected_version
            )

            if not row:
                # Verifier si existe
                exists = await conn.fetchval(
                    "SELECT version FROM conversations WHERE id = $1 AND tenant_id = $2",
                    conversation_id, tenant_id
                )
                if exists is None:
                    raise ConversationNotFoundError(
                        f"Conversation {conversation_id} not found"
                    )
                raise ConversationConflictError(
                    f"Version mismatch: expected {expected_version}, current is {exists}"
                )

            return self._row_to_dict(row)

    async def list_by_user(
        self,
        tenant_id: UUID,
        user_id: UUID,
        limit: int = 20,
        offset: int = 0,
        app_context: str = None
    ) -> List[Dict[str, Any]]:
        """Liste les conversations d'un utilisateur."""
        async with self.pool.acquire() as conn:
            await self._set_tenant(conn, tenant_id)

            if app_context:
                rows = await conn.fetch(
                    """
                    SELECT id, tenant_id, user_id, title, model,
                           jsonb_array_length(COALESCE(messages, '[]'::jsonb)) as message_count,
                           tokens_used, app_context, version,
                           created_at, updated_at
                    FROM conversations
                    WHERE tenant_id = $1 AND user_id = $2 AND app_context = $3
                    ORDER BY updated_at DESC
                    LIMIT $4 OFFSET $5
                    """,
                    tenant_id, user_id, app_context, limit, offset
                )
            else:
                rows = await conn.fetch(
                    """
                    SELECT id, tenant_id, user_id, title, model,
                           jsonb_array_length(COALESCE(messages, '[]'::jsonb)) as message_count,
                           tokens_used, app_context, version,
                           created_at, updated_at
                    FROM conversations
                    WHERE tenant_id = $1 AND user_id = $2
                    ORDER BY updated_at DESC
                    LIMIT $3 OFFSET $4
                    """,
                    tenant_id, user_id, limit, offset
                )

            return [dict(row) for row in rows]

    async def count_by_user(
        self,
        tenant_id: UUID,
        user_id: UUID,
        app_context: str = None
    ) -> int:
        """Compte les conversations d'un utilisateur."""
        async with self.pool.acquire() as conn:
            await self._set_tenant(conn, tenant_id)

            if app_context:
                count = await conn.fetchval(
                    """
                    SELECT COUNT(*)
                    FROM conversations
                    WHERE tenant_id = $1 AND user_id = $2 AND app_context = $3
                    """,
                    tenant_id, user_id, app_context
                )
            else:
                count = await conn.fetchval(
                    """
                    SELECT COUNT(*)
                    FROM conversations
                    WHERE tenant_id = $1 AND user_id = $2
                    """,
                    tenant_id, user_id
                )

            return count or 0

    async def delete(
        self,
        conversation_id: UUID,
        tenant_id: UUID
    ) -> bool:
        """Supprime une conversation."""
        async with self.pool.acquire() as conn:
            await self._set_tenant(conn, tenant_id)

            result = await conn.execute(
                """
                DELETE FROM conversations
                WHERE id = $1 AND tenant_id = $2
                """,
                conversation_id, tenant_id
            )

            return result == "DELETE 1"

    async def archive_and_rotate(
        self,
        conversation_id: UUID,
        tenant_id: UUID,
        summary: str
    ) -> Dict[str, Any]:
        """
        Archive une conversation pleine et cree une nouvelle.

        Returns:
            Nouvelle conversation avec resume comme premier message
        """
        async with self.pool.acquire() as conn:
            await self._set_tenant(conn, tenant_id)

            async with conn.transaction():
                # 1. Recuperer l'ancienne
                old = await conn.fetchrow(
                    """
                    SELECT user_id, title, model, app_context
                    FROM conversations
                    WHERE id = $1 AND tenant_id = $2
                    """,
                    conversation_id, tenant_id
                )

                if not old:
                    raise ConversationNotFoundError(
                        f"Conversation {conversation_id} not found"
                    )

                # 2. Marquer comme archivee
                await conn.execute(
                    """
                    UPDATE conversations
                    SET app_context = app_context || '_archived',
                        title = COALESCE(title, 'Conversation') || ' (archivee)'
                    WHERE id = $1 AND tenant_id = $2
                    """,
                    conversation_id, tenant_id
                )

                # 3. Creer nouvelle avec resume
                summary_msg = {
                    "role": "system",
                    "content": f"[Resume conversation precedente]\n{summary}",
                    "timestamp": datetime.utcnow().isoformat()
                }

                row = await conn.fetchrow(
                    """
                    INSERT INTO conversations
                        (tenant_id, user_id, title, model, app_context, messages, version)
                    VALUES ($1, $2, $3, $4, $5, $6::jsonb, 1)
                    RETURNING id, tenant_id, user_id, title, model,
                              messages, tokens_used, app_context,
                              version, created_at, updated_at
                    """,
                    tenant_id, old["user_id"], old["title"],
                    old["model"], old["app_context"],
                    json.dumps([summary_msg])
                )

                result = self._row_to_dict(row)
                result["messages"] = [summary_msg]
                return result

    def _row_to_dict(self, row: asyncpg.Record) -> Dict[str, Any]:
        """Convertit un Record asyncpg en dict avec parsing JSONB."""
        result = dict(row)

        # Convertir UUID en string
        for key in ["id", "tenant_id", "user_id"]:
            if key in result and result[key] is not None:
                result[key] = str(result[key])

        # Convertir JSONB messages en list Python
        if "messages" in result:
            if isinstance(result["messages"], str):
                result["messages"] = json.loads(result["messages"])
            elif result["messages"] is None:
                result["messages"] = []

        return result


# === EXCEPTIONS ===

class ConversationError(Exception):
    """Base exception."""
    pass


class ConversationNotFoundError(ConversationError):
    """Conversation non trouvee."""
    pass


class ConversationConflictError(ConversationError):
    """Conflit de version (optimistic lock)."""
    pass


class ConversationFullError(ConversationError):
    """Limite 100 messages atteinte."""
    pass
