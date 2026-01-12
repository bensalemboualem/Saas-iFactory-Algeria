"""
Repository voice_conversations - asyncpg + optimistic locking.
"""

from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
import json
import logging
import asyncpg

logger = logging.getLogger(__name__)


class VoiceConversationRepository:
    """Repository pour voice_conversations avec RLS et optimistic lock."""

    MAX_MESSAGES = 100

    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def _set_tenant(self, conn: asyncpg.Connection, tenant_id: UUID):
        await conn.execute(
            "SELECT set_config('app.current_tenant', $1, true)",
            str(tenant_id)
        )

    async def get(self, conversation_id: UUID, tenant_id: UUID) -> Optional[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            await self._set_tenant(conn, tenant_id)
            row = await conn.fetchrow(
                """
                SELECT id, tenant_id, user_id, title, context,
                       COALESCE(messages, '[]'::jsonb) as messages,
                       message_count, total_audio_seconds, total_tokens,
                       status, metadata, version, created_at, updated_at
                FROM voice_conversations
                WHERE id = $1 AND tenant_id = $2
                """,
                conversation_id, tenant_id
            )
            if not row:
                return None
            result = dict(row)
            if isinstance(result["messages"], str):
                result["messages"] = json.loads(result["messages"])
            if isinstance(result["metadata"], str):
                result["metadata"] = json.loads(result["metadata"])
            return result

    async def create(
        self,
        tenant_id: UUID,
        user_id: int,
        context: str = "voice_chat",
        title: str = None
    ) -> Dict[str, Any]:
        async with self.pool.acquire() as conn:
            await self._set_tenant(conn, tenant_id)
            row = await conn.fetchrow(
                """
                INSERT INTO voice_conversations
                    (tenant_id, user_id, context, title, messages, version)
                VALUES ($1, $2, $3, $4, '[]'::jsonb, 1)
                RETURNING id, tenant_id, user_id, title, context,
                          messages, message_count, total_audio_seconds,
                          total_tokens, status, metadata, version,
                          created_at, updated_at
                """,
                tenant_id, user_id, context, title
            )
            result = dict(row)
            result["messages"] = []
            result["metadata"] = {}
            return result

    async def add_message(
        self,
        conversation_id: UUID,
        tenant_id: UUID,
        message: Dict[str, Any],
        expected_version: int,
        audio_seconds: float = 0,
        tokens: int = 0
    ) -> Dict[str, Any]:
        message["timestamp"] = message.get("timestamp", datetime.utcnow().isoformat())

        async with self.pool.acquire() as conn:
            await self._set_tenant(conn, tenant_id)

            row = await conn.fetchrow(
                """
                UPDATE voice_conversations
                SET messages = COALESCE(messages, '[]'::jsonb) || $3::jsonb,
                    message_count = message_count + 1,
                    total_audio_seconds = total_audio_seconds + $5,
                    total_tokens = total_tokens + $6,
                    version = version + 1,
                    updated_at = NOW()
                WHERE id = $1 AND tenant_id = $2 AND version = $4
                RETURNING id, tenant_id, user_id, title, context,
                          messages, message_count, total_audio_seconds,
                          total_tokens, status, metadata, version,
                          created_at, updated_at
                """,
                conversation_id, tenant_id, json.dumps([message]),
                expected_version, audio_seconds, tokens
            )

            if not row:
                raise VoiceConversationConflictError(
                    f"Version mismatch for conversation {conversation_id}"
                )

            result = dict(row)
            if isinstance(result["messages"], str):
                result["messages"] = json.loads(result["messages"])
            return result

    async def update_status(
        self,
        conversation_id: UUID,
        tenant_id: UUID,
        status: str
    ) -> bool:
        async with self.pool.acquire() as conn:
            await self._set_tenant(conn, tenant_id)
            result = await conn.execute(
                """
                UPDATE voice_conversations
                SET status = $3, updated_at = NOW()
                WHERE id = $1 AND tenant_id = $2
                """,
                conversation_id, tenant_id, status
            )
            return result == "UPDATE 1"

    async def list_active(self, tenant_id: UUID, user_id: int = None) -> List[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            await self._set_tenant(conn, tenant_id)
            if user_id:
                rows = await conn.fetch(
                    """
                    SELECT id, tenant_id, user_id, title, context,
                           message_count, status, version, created_at, updated_at
                    FROM voice_conversations
                    WHERE tenant_id = $1 AND user_id = $2 AND status = 'active'
                    ORDER BY updated_at DESC
                    """,
                    tenant_id, user_id
                )
            else:
                rows = await conn.fetch(
                    """
                    SELECT id, tenant_id, user_id, title, context,
                           message_count, status, version, created_at, updated_at
                    FROM voice_conversations
                    WHERE tenant_id = $1 AND status = 'active'
                    ORDER BY updated_at DESC
                    """,
                    tenant_id
                )
            return [dict(row) for row in rows]

    async def count_active(self, tenant_id: UUID) -> int:
        async with self.pool.acquire() as conn:
            await self._set_tenant(conn, tenant_id)
            result = await conn.fetchval(
                """
                SELECT COUNT(*) FROM voice_conversations
                WHERE tenant_id = $1 AND status = 'active'
                """,
                tenant_id
            )
            return result or 0


class VoiceConversationConflictError(Exception):
    """Version mismatch."""
    pass

class VoiceConversationNotFoundError(Exception):
    """Not found."""
    pass
