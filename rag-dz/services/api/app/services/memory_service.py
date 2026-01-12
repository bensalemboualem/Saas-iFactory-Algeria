"""
IAFactory Memory Service - Persistent Conversations & User Memory
=================================================================
Service principal pour:
- Stockage conversations (PostgreSQL)
- Cache sessions (Redis)
- Mémoire utilisateur (profile, préférences, business, faits, objectifs)
- Embeddings sémantiques (Qdrant)
- Extraction mémoire via LLM
Token tracking integre.
"""

import logging
import json
import hashlib
import asyncio
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime, timedelta
from contextlib import contextmanager
import uuid

import psycopg
from psycopg.rows import dict_row

from ..config import get_settings
from ..db import get_db_connection

# Token tracking
try:
    from app.tokens.llm_proxy import check_token_balance, deduct_after_llm_call, InsufficientTokensError
    TOKENS_AVAILABLE = True
except ImportError:
    TOKENS_AVAILABLE = False

from ..models.memory_models import (
    MemoryCategory, MessageRole, AppContext, MemorySource,
    ChatSession, ChatSessionCreate, ChatSessionUpdate, ChatSessionSummary,
    ChatMessage, ChatMessageCreate,
    UserMemory, UserMemoryCreate, UserMemoryUpdate,
    MemoryCorrection, MemoryCorrectionCreate,
    ConversationSummary, ConversationSummaryCreate,
    MemoryContext, ExtractedMemory, MemoryExtractionResult,
    SendMessageRequest, SendMessageResponse,
    GetConversationsResponse, GetMessagesResponse, GetMemoriesResponse,
    MemoryStatsResponse, SemanticSearchResult, SemanticSearchResponse
)

logger = logging.getLogger(__name__)
settings = get_settings()


# ============================================
# Memory Extraction Prompts
# ============================================

MEMORY_EXTRACTION_PROMPT = """Analyse ce message et extrait les informations importantes sur l'utilisateur.

Message: {message}

Extrait UNIQUEMENT les informations factuelles et utiles dans ces catégories:
- profile: nom, métier, localisation, entreprise
- preference: langue, style de communication, préférences
- business: secteur, taille entreprise, chiffre d'affaires
- fact: faits importants mentionnés
- goal: objectifs, projets, intentions

Réponds en JSON avec ce format:
{{
  "memories": [
    {{"category": "profile", "key": "nom", "value": "...", "confidence": 0.9}},
    {{"category": "business", "key": "secteur", "value": "...", "confidence": 0.8}}
  ]
}}

Si aucune information pertinente, réponds: {{"memories": []}}
"""


# ============================================
# Redis Cache Helper
# ============================================

class RedisCache:
    """Helper pour cache Redis"""

    def __init__(self):
        self._redis = None

    async def _get_redis(self):
        """Get async Redis connection"""
        if self._redis is None:
            try:
                import redis.asyncio as redis
                self._redis = redis.from_url(
                    settings.redis_url,
                    password=settings.redis_password or None,
                    decode_responses=True
                )
            except Exception as e:
                logger.warning(f"Redis not available: {e}")
                self._redis = False
        return self._redis if self._redis else None

    async def get(self, key: str) -> Optional[str]:
        """Get value from cache"""
        redis = await self._get_redis()
        if redis:
            try:
                return await redis.get(key)
            except Exception as e:
                logger.warning(f"Redis get error: {e}")
        return None

    async def set(self, key: str, value: str, ttl: int = 3600):
        """Set value in cache with TTL"""
        redis = await self._get_redis()
        if redis:
            try:
                await redis.setex(key, ttl, value)
            except Exception as e:
                logger.warning(f"Redis set error: {e}")

    async def delete(self, key: str):
        """Delete key from cache"""
        redis = await self._get_redis()
        if redis:
            try:
                await redis.delete(key)
            except Exception as e:
                logger.warning(f"Redis delete error: {e}")


# ============================================
# Qdrant Vector Store Helper
# ============================================

class QdrantVectorStore:
    """Helper pour Qdrant vector store"""

    COLLECTION_MESSAGES = "chat_messages"
    COLLECTION_MEMORIES = "user_memories"
    VECTOR_SIZE = 1536  # text-embedding-3-small

    def __init__(self):
        self._client = None
        self._embeddings_client = None

    def _get_client(self):
        """Get Qdrant client"""
        if self._client is None:
            try:
                from qdrant_client import QdrantClient
                self._client = QdrantClient(
                    host=settings.qdrant_host,
                    port=settings.qdrant_port,
                    api_key=settings.qdrant_api_key or None
                )
            except Exception as e:
                logger.warning(f"Qdrant not available: {e}")
                self._client = False
        return self._client if self._client else None

    async def _get_embedding(self, text: str) -> Optional[List[float]]:
        """Get embedding for text using OpenAI"""
        if self._embeddings_client is None:
            try:
                from openai import AsyncOpenAI
                if settings.openai_api_key:
                    self._embeddings_client = AsyncOpenAI(api_key=settings.openai_api_key)
                else:
                    self._embeddings_client = False
            except Exception as e:
                logger.warning(f"OpenAI not available: {e}")
                self._embeddings_client = False

        if not self._embeddings_client:
            return None

        try:
            response = await self._embeddings_client.embeddings.create(
                model="text-embedding-3-small",
                input=text[:8000]
            )
            return response.data[0].embedding
        except Exception as e:
            logger.warning(f"Embedding error: {e}")
            return None

    async def upsert_message(
        self,
        message_id: str,
        content: str,
        session_id: str,
        user_id: str,
        tenant_id: str
    ):
        """Index message in Qdrant"""
        client = self._get_client()
        if not client:
            return

        embedding = await self._get_embedding(content)
        if not embedding:
            return

        try:
            from qdrant_client.models import PointStruct
            client.upsert(
                collection_name=self.COLLECTION_MESSAGES,
                points=[
                    PointStruct(
                        id=message_id,
                        vector=embedding,
                        payload={
                            "session_id": session_id,
                            "user_id": user_id,
                            "tenant_id": tenant_id,
                            "content": content[:500],
                            "created_at": datetime.utcnow().isoformat()
                        }
                    )
                ]
            )
        except Exception as e:
            logger.warning(f"Qdrant upsert error: {e}")

    async def upsert_memory(
        self,
        memory_id: str,
        content: str,
        category: str,
        user_id: str,
        tenant_id: str
    ):
        """Index memory in Qdrant"""
        client = self._get_client()
        if not client:
            return

        embedding = await self._get_embedding(content)
        if not embedding:
            return

        try:
            from qdrant_client.models import PointStruct
            client.upsert(
                collection_name=self.COLLECTION_MEMORIES,
                points=[
                    PointStruct(
                        id=memory_id,
                        vector=embedding,
                        payload={
                            "category": category,
                            "user_id": user_id,
                            "tenant_id": tenant_id,
                            "content": content[:500],
                            "created_at": datetime.utcnow().isoformat()
                        }
                    )
                ]
            )
        except Exception as e:
            logger.warning(f"Qdrant upsert error: {e}")

    async def search(
        self,
        query: str,
        collection: str,
        user_id: str,
        tenant_id: str,
        limit: int = 10,
        min_score: float = 0.7
    ) -> List[Dict[str, Any]]:
        """Search similar vectors"""
        client = self._get_client()
        if not client:
            return []

        embedding = await self._get_embedding(query)
        if not embedding:
            return []

        try:
            from qdrant_client.models import Filter, FieldCondition, MatchValue

            results = client.search(
                collection_name=collection,
                query_vector=embedding,
                limit=limit,
                score_threshold=min_score,
                query_filter=Filter(
                    must=[
                        FieldCondition(key="tenant_id", match=MatchValue(value=tenant_id)),
                        FieldCondition(key="user_id", match=MatchValue(value=user_id))
                    ]
                )
            )

            return [
                {
                    "id": str(r.id),
                    "score": r.score,
                    "payload": r.payload
                }
                for r in results
            ]
        except Exception as e:
            logger.warning(f"Qdrant search error: {e}")
            return []


# ============================================
# Main Memory Service
# ============================================

class MemoryService:
    """
    Service principal de mémoire IAFactory

    Responsabilités:
    - Gestion sessions de conversation
    - Stockage messages
    - Mémoire utilisateur persistante
    - Extraction automatique de mémoire
    - Recherche sémantique
    """

    def __init__(self):
        self.cache = RedisCache()
        self.vector_store = QdrantVectorStore()
        logger.info("MemoryService initialized")

    # ============================================
    # Session Management
    # ============================================

    async def create_session(
        self,
        tenant_id: str,
        user_id: str,
        session_data: ChatSessionCreate
    ) -> ChatSession:
        """Create a new chat session"""
        session_id = str(uuid.uuid4())

        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute("""
                    INSERT INTO chat_sessions
                    (id, tenant_id, user_id, title, app_context, language, agent_id, model, metadata)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING *
                """, (
                    session_id,
                    tenant_id,
                    user_id,
                    session_data.title,
                    session_data.app_context.value,
                    session_data.language,
                    session_data.agent_id,
                    session_data.model,
                    json.dumps(session_data.metadata)
                ))
                row = cur.fetchone()

        # Cache session
        await self.cache.set(
            f"session:{session_id}",
            json.dumps({"id": session_id, "user_id": user_id, "tenant_id": tenant_id}),
            ttl=3600
        )

        return self._row_to_session(row)

    async def get_session(
        self,
        session_id: str,
        tenant_id: str
    ) -> Optional[ChatSession]:
        """Get session by ID"""
        # Check cache first
        cached = await self.cache.get(f"session:{session_id}")

        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute("""
                    SELECT * FROM chat_sessions
                    WHERE id = %s AND tenant_id = %s
                """, (session_id, tenant_id))
                row = cur.fetchone()

        if not row:
            return None

        return self._row_to_session(row)

    async def get_sessions(
        self,
        tenant_id: str,
        user_id: str,
        app_context: Optional[AppContext] = None,
        is_archived: bool = False,
        is_starred: Optional[bool] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Tuple[List[ChatSessionSummary], int]:
        """Get user's sessions with pagination"""
        conditions = ["tenant_id = %s", "user_id = %s", "is_archived = %s"]
        params = [tenant_id, user_id, is_archived]

        if app_context:
            conditions.append("app_context = %s")
            params.append(app_context.value)

        if is_starred is not None:
            conditions.append("is_starred = %s")
            params.append(is_starred)

        where_clause = " AND ".join(conditions)

        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                # Get total count
                cur.execute(f"""
                    SELECT COUNT(*) as total FROM chat_sessions WHERE {where_clause}
                """, params)
                total = cur.fetchone()["total"]

                # Get sessions
                cur.execute(f"""
                    SELECT cs.*,
                           (SELECT content FROM chat_messages
                            WHERE session_id = cs.id
                            ORDER BY created_at ASC LIMIT 1) as preview
                    FROM chat_sessions cs
                    WHERE {where_clause}
                    ORDER BY last_message_at DESC NULLS LAST, created_at DESC
                    LIMIT %s OFFSET %s
                """, params + [limit, offset])
                rows = cur.fetchall()

        sessions = [self._row_to_session_summary(r) for r in rows]
        return sessions, total

    async def update_session(
        self,
        session_id: str,
        tenant_id: str,
        updates: ChatSessionUpdate
    ) -> Optional[ChatSession]:
        """Update session"""
        set_parts = []
        params = []

        if updates.title is not None:
            set_parts.append("title = %s")
            params.append(updates.title)

        if updates.is_archived is not None:
            set_parts.append("is_archived = %s")
            params.append(updates.is_archived)

        if updates.is_starred is not None:
            set_parts.append("is_starred = %s")
            params.append(updates.is_starred)

        if updates.metadata is not None:
            set_parts.append("metadata = %s")
            params.append(json.dumps(updates.metadata))

        if not set_parts:
            return await self.get_session(session_id, tenant_id)

        set_parts.append("updated_at = NOW()")
        params.extend([session_id, tenant_id])

        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(f"""
                    UPDATE chat_sessions
                    SET {", ".join(set_parts)}
                    WHERE id = %s AND tenant_id = %s
                    RETURNING *
                """, params)
                row = cur.fetchone()

        if not row:
            return None

        # Invalidate cache
        await self.cache.delete(f"session:{session_id}")

        return self._row_to_session(row)

    async def delete_session(self, session_id: str, tenant_id: str) -> bool:
        """Delete session and all messages"""
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE FROM chat_sessions
                    WHERE id = %s AND tenant_id = %s
                """, (session_id, tenant_id))
                deleted = cur.rowcount > 0

        if deleted:
            await self.cache.delete(f"session:{session_id}")

        return deleted

    # ============================================
    # Message Management
    # ============================================

    async def add_message(
        self,
        session_id: str,
        tenant_id: str,
        message: ChatMessageCreate
    ) -> ChatMessage:
        """Add message to session"""
        message_id = str(uuid.uuid4())

        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                # Insert message
                cur.execute("""
                    INSERT INTO chat_messages
                    (id, session_id, role, content, tokens_input, tokens_output,
                     model_used, latency_ms, tool_calls, tool_results, metadata)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING *
                """, (
                    message_id,
                    session_id,
                    message.role.value,
                    message.content,
                    message.tokens_input,
                    message.tokens_output,
                    message.model_used,
                    message.latency_ms,
                    json.dumps(message.tool_calls) if message.tool_calls else None,
                    json.dumps(message.tool_results) if message.tool_results else None,
                    json.dumps(message.metadata)
                ))
                row = cur.fetchone()

                # Update session stats
                cur.execute("""
                    UPDATE chat_sessions
                    SET message_count = message_count + 1,
                        total_tokens = total_tokens + %s,
                        last_message_at = NOW(),
                        updated_at = NOW()
                    WHERE id = %s
                """, (message.tokens_input + message.tokens_output, session_id))

                # Get user_id for vector indexing
                cur.execute("""
                    SELECT user_id FROM chat_sessions WHERE id = %s
                """, (session_id,))
                session = cur.fetchone()

        # Index in vector store (async, non-blocking)
        if session:
            asyncio.create_task(
                self.vector_store.upsert_message(
                    message_id,
                    message.content,
                    session_id,
                    session["user_id"],
                    tenant_id
                )
            )

        return self._row_to_message(row)

    async def get_messages(
        self,
        session_id: str,
        tenant_id: str,
        limit: int = 50,
        before_id: Optional[str] = None
    ) -> Tuple[List[ChatMessage], bool]:
        """Get messages for session with pagination"""
        conditions = ["cm.session_id = %s"]
        params = [session_id]

        if before_id:
            conditions.append("""
                cm.created_at < (SELECT created_at FROM chat_messages WHERE id = %s)
            """)
            params.append(before_id)

        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                # Verify session belongs to tenant
                cur.execute("""
                    SELECT id FROM chat_sessions
                    WHERE id = %s AND tenant_id = %s
                """, (session_id, tenant_id))
                if not cur.fetchone():
                    return [], False

                # Get messages
                cur.execute(f"""
                    SELECT cm.* FROM chat_messages cm
                    WHERE {" AND ".join(conditions)}
                    ORDER BY cm.created_at DESC
                    LIMIT %s
                """, params + [limit + 1])
                rows = cur.fetchall()

        has_more = len(rows) > limit
        messages = [self._row_to_message(r) for r in rows[:limit]]
        messages.reverse()  # Chronological order

        return messages, has_more

    # ============================================
    # Memory Management
    # ============================================

    async def upsert_memory(
        self,
        tenant_id: str,
        user_id: str,
        memory: UserMemoryCreate
    ) -> UserMemory:
        """Create or update user memory"""
        memory_id = str(uuid.uuid4())

        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute("""
                    INSERT INTO user_memories
                    (id, tenant_id, user_id, category, key, value, confidence,
                     source, source_message_id, metadata)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (user_id, category, key)
                    DO UPDATE SET
                        value = EXCLUDED.value,
                        confidence = EXCLUDED.confidence,
                        source = EXCLUDED.source,
                        source_message_id = EXCLUDED.source_message_id,
                        metadata = EXCLUDED.metadata,
                        updated_at = NOW()
                    RETURNING *
                """, (
                    memory_id,
                    tenant_id,
                    user_id,
                    memory.category.value,
                    memory.key,
                    memory.value,
                    memory.confidence,
                    memory.source.value,
                    memory.source_message_id,
                    json.dumps(memory.metadata)
                ))
                row = cur.fetchone()

        # Index in vector store
        asyncio.create_task(
            self.vector_store.upsert_memory(
                row["id"],
                f"{memory.key}: {memory.value}",
                memory.category.value,
                user_id,
                tenant_id
            )
        )

        return self._row_to_memory(row)

    async def get_memories(
        self,
        tenant_id: str,
        user_id: str,
        category: Optional[MemoryCategory] = None,
        is_active: bool = True
    ) -> List[UserMemory]:
        """Get user memories"""
        conditions = ["tenant_id = %s", "user_id = %s", "is_active = %s"]
        params = [tenant_id, user_id, is_active]

        if category:
            conditions.append("category = %s")
            params.append(category.value)

        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(f"""
                    SELECT * FROM user_memories
                    WHERE {" AND ".join(conditions)}
                    ORDER BY category, key
                """, params)
                rows = cur.fetchall()

        return [self._row_to_memory(r) for r in rows]

    async def update_memory(
        self,
        memory_id: str,
        tenant_id: str,
        user_id: str,
        updates: UserMemoryUpdate,
        reason: Optional[str] = None
    ) -> Optional[UserMemory]:
        """Update a memory (with correction tracking)"""
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                # Get current memory
                cur.execute("""
                    SELECT * FROM user_memories
                    WHERE id = %s AND tenant_id = %s AND user_id = %s
                """, (memory_id, tenant_id, user_id))
                current = cur.fetchone()

                if not current:
                    return None

                # Record correction if value changed
                if updates.value and updates.value != current["value"]:
                    cur.execute("""
                        INSERT INTO memory_corrections
                        (memory_id, old_value, new_value, corrected_by, reason)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (memory_id, current["value"], updates.value, user_id, reason))

                # Build update
                set_parts = ["updated_at = NOW()"]
                params = []

                if updates.value is not None:
                    set_parts.append("value = %s")
                    params.append(updates.value)

                if updates.confidence is not None:
                    set_parts.append("confidence = %s")
                    params.append(updates.confidence)

                if updates.is_active is not None:
                    set_parts.append("is_active = %s")
                    params.append(updates.is_active)

                if updates.metadata is not None:
                    set_parts.append("metadata = %s")
                    params.append(json.dumps(updates.metadata))

                params.extend([memory_id, tenant_id, user_id])

                cur.execute(f"""
                    UPDATE user_memories
                    SET {", ".join(set_parts)}
                    WHERE id = %s AND tenant_id = %s AND user_id = %s
                    RETURNING *
                """, params)
                row = cur.fetchone()

        return self._row_to_memory(row) if row else None

    async def delete_memory(
        self,
        memory_id: str,
        tenant_id: str,
        user_id: str
    ) -> bool:
        """Delete a memory (soft delete)"""
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE user_memories
                    SET is_active = false, updated_at = NOW()
                    WHERE id = %s AND tenant_id = %s AND user_id = %s
                """, (memory_id, tenant_id, user_id))
                return cur.rowcount > 0

    # ============================================
    # Memory Context for AI
    # ============================================

    async def get_memory_context(
        self,
        tenant_id: str,
        user_id: str,
        include_recent_topics: bool = True
    ) -> MemoryContext:
        """Get memory context for AI prompt injection"""
        memories = await self.get_memories(tenant_id, user_id)

        context = MemoryContext()

        for mem in memories:
            if mem.category == MemoryCategory.PROFILE:
                context.user_profile[mem.key] = mem.value
            elif mem.category == MemoryCategory.PREFERENCE:
                context.preferences[mem.key] = mem.value
            elif mem.category == MemoryCategory.BUSINESS:
                context.business_info[mem.key] = mem.value
            elif mem.category == MemoryCategory.FACT:
                context.relevant_facts.append(f"{mem.key}: {mem.value}")
            elif mem.category == MemoryCategory.GOAL:
                context.goals.append(mem.value)

        # Get recent topics from conversations
        if include_recent_topics:
            with get_db_connection() as conn:
                with conn.cursor(row_factory=dict_row) as cur:
                    cur.execute("""
                        SELECT DISTINCT cs.title
                        FROM chat_sessions cs
                        WHERE cs.tenant_id = %s AND cs.user_id = %s
                          AND cs.title IS NOT NULL
                          AND cs.last_message_at > NOW() - INTERVAL '7 days'
                        ORDER BY cs.last_message_at DESC
                        LIMIT 5
                    """, (tenant_id, user_id))
                    rows = cur.fetchall()
                    context.recent_topics = [r["title"] for r in rows if r["title"]]

        return context

    # ============================================
    # Memory Extraction (from conversations)
    # ============================================

    async def extract_memories_from_message(
        self,
        tenant_id: str,
        user_id: str,
        message_id: str,
        content: str,
        llm_client=None
    ) -> List[UserMemory]:
        """Extract memories from a message using LLM with token tracking"""
        if not llm_client:
            # Try to get OpenAI client
            try:
                from openai import AsyncOpenAI
                if settings.openai_api_key:
                    llm_client = AsyncOpenAI(api_key=settings.openai_api_key)
                else:
                    logger.warning("No OpenAI key for memory extraction")
                    return []
            except Exception as e:
                logger.warning(f"Cannot init LLM for extraction: {e}")
                return []

        # Token tracking: verifier solde AVANT l'appel
        prompt_content = MEMORY_EXTRACTION_PROMPT.format(message=content)
        if TOKENS_AVAILABLE and tenant_id:
            estimated_tokens = len(prompt_content.split()) * 2 + 200
            try:
                check_token_balance(tenant_id, estimated_tokens)
            except InsufficientTokensError:
                logger.warning("Insufficient tokens for memory extraction, skipping")
                return []

        try:
            response = await llm_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Tu extrais des informations utilisateur en JSON."},
                    {"role": "user", "content": prompt_content}
                ],
                response_format={"type": "json_object"},
                temperature=0.1,
                max_tokens=500
            )

            # Token tracking: deduire tokens APRES l'appel
            if TOKENS_AVAILABLE and tenant_id and response.usage:
                try:
                    deduct_after_llm_call(
                        tenant_id=tenant_id,
                        provider="openai",
                        model="gpt-4o-mini",
                        tokens_input=response.usage.prompt_tokens,
                        tokens_output=response.usage.completion_tokens
                    )
                except Exception as e:
                    logger.warning(f"Token deduction failed (memory_extraction): {e}")

            result = json.loads(response.choices[0].message.content)
            extracted = result.get("memories", [])

            if not extracted:
                return []

            saved_memories = []
            for mem in extracted:
                try:
                    memory = UserMemoryCreate(
                        category=MemoryCategory(mem["category"]),
                        key=mem["key"],
                        value=mem["value"],
                        confidence=mem.get("confidence", 0.8),
                        source=MemorySource.EXTRACTED,
                        source_message_id=message_id
                    )
                    saved = await self.upsert_memory(tenant_id, user_id, memory)
                    saved_memories.append(saved)
                except Exception as e:
                    logger.warning(f"Failed to save extracted memory: {e}")

            return saved_memories

        except Exception as e:
            logger.warning(f"Memory extraction failed: {e}")
            return []

    # ============================================
    # Semantic Search
    # ============================================

    async def semantic_search(
        self,
        tenant_id: str,
        user_id: str,
        query: str,
        search_type: str = "all",
        limit: int = 10,
        min_similarity: float = 0.7
    ) -> SemanticSearchResponse:
        """Search messages and memories semantically"""
        import time
        start = time.time()

        results = []

        if search_type in ("all", "messages"):
            msg_results = await self.vector_store.search(
                query,
                QdrantVectorStore.COLLECTION_MESSAGES,
                user_id,
                tenant_id,
                limit,
                min_similarity
            )
            for r in msg_results:
                results.append(SemanticSearchResult(
                    id=r["id"],
                    type="message",
                    content=r["payload"].get("content", ""),
                    similarity=r["score"],
                    metadata=r["payload"],
                    created_at=datetime.fromisoformat(r["payload"].get("created_at", datetime.utcnow().isoformat()))
                ))

        if search_type in ("all", "memories"):
            mem_results = await self.vector_store.search(
                query,
                QdrantVectorStore.COLLECTION_MEMORIES,
                user_id,
                tenant_id,
                limit,
                min_similarity
            )
            for r in mem_results:
                results.append(SemanticSearchResult(
                    id=r["id"],
                    type="memory",
                    content=r["payload"].get("content", ""),
                    similarity=r["score"],
                    metadata=r["payload"],
                    created_at=datetime.fromisoformat(r["payload"].get("created_at", datetime.utcnow().isoformat()))
                ))

        # Sort by similarity
        results.sort(key=lambda x: x.similarity, reverse=True)
        results = results[:limit]

        return SemanticSearchResponse(
            query=query,
            results=results,
            total_found=len(results),
            search_time_ms=int((time.time() - start) * 1000)
        )

    # ============================================
    # Statistics
    # ============================================

    async def get_memory_stats(
        self,
        tenant_id: str,
        user_id: str
    ) -> MemoryStatsResponse:
        """Get user's memory statistics"""
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                # Memory stats
                cur.execute("""
                    SELECT
                        COUNT(*) as total_memories,
                        COUNT(*) FILTER (WHERE category = 'profile') as profile_count,
                        COUNT(*) FILTER (WHERE category = 'preference') as preference_count,
                        COUNT(*) FILTER (WHERE category = 'business') as business_count,
                        COUNT(*) FILTER (WHERE category = 'fact') as fact_count,
                        COUNT(*) FILTER (WHERE category = 'goal') as goal_count,
                        MIN(created_at) as oldest_memory,
                        MAX(created_at) as newest_memory
                    FROM user_memories
                    WHERE tenant_id = %s AND user_id = %s AND is_active = true
                """, (tenant_id, user_id))
                mem_stats = cur.fetchone()

                # Conversation stats
                cur.execute("""
                    SELECT
                        COUNT(*) as total_conversations,
                        SUM(message_count) as total_messages
                    FROM chat_sessions
                    WHERE tenant_id = %s AND user_id = %s
                """, (tenant_id, user_id))
                conv_stats = cur.fetchone()

                # Most discussed topics
                cur.execute("""
                    SELECT title, COUNT(*) as msg_count
                    FROM chat_sessions
                    WHERE tenant_id = %s AND user_id = %s AND title IS NOT NULL
                    GROUP BY title
                    ORDER BY msg_count DESC
                    LIMIT 5
                """, (tenant_id, user_id))
                topics = [r["title"] for r in cur.fetchall()]

        total_conv = conv_stats["total_conversations"] or 0
        total_msg = conv_stats["total_messages"] or 0

        return MemoryStatsResponse(
            user_id=user_id,
            total_memories=mem_stats["total_memories"] or 0,
            memories_by_category={
                "profile": mem_stats["profile_count"] or 0,
                "preference": mem_stats["preference_count"] or 0,
                "business": mem_stats["business_count"] or 0,
                "fact": mem_stats["fact_count"] or 0,
                "goal": mem_stats["goal_count"] or 0
            },
            total_conversations=total_conv,
            total_messages=total_msg,
            average_messages_per_conversation=total_msg / total_conv if total_conv > 0 else 0,
            most_discussed_topics=topics,
            oldest_memory_date=mem_stats["oldest_memory"],
            newest_memory_date=mem_stats["newest_memory"]
        )

    # ============================================
    # Helper Methods
    # ============================================

    def _row_to_session(self, row: Dict) -> ChatSession:
        """Convert DB row to ChatSession"""
        return ChatSession(
            id=str(row["id"]),
            tenant_id=str(row["tenant_id"]),
            user_id=str(row["user_id"]),
            title=row.get("title"),
            app_context=AppContext(row.get("app_context", "chat")),
            language=row.get("language", "fr"),
            agent_id=row.get("agent_id"),
            model=row.get("model", "groq"),
            message_count=row.get("message_count", 0),
            total_tokens=row.get("total_tokens", 0),
            is_archived=row.get("is_archived", False),
            is_starred=row.get("is_starred", False),
            metadata=json.loads(row["metadata"]) if row.get("metadata") else {},
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            last_message_at=row.get("last_message_at")
        )

    def _row_to_session_summary(self, row: Dict) -> ChatSessionSummary:
        """Convert DB row to ChatSessionSummary"""
        return ChatSessionSummary(
            id=str(row["id"]),
            title=row.get("title"),
            app_context=AppContext(row.get("app_context", "chat")),
            message_count=row.get("message_count", 0),
            is_starred=row.get("is_starred", False),
            created_at=row["created_at"],
            last_message_at=row.get("last_message_at"),
            preview=row.get("preview", "")[:100] if row.get("preview") else None
        )

    def _row_to_message(self, row: Dict) -> ChatMessage:
        """Convert DB row to ChatMessage"""
        return ChatMessage(
            id=str(row["id"]),
            session_id=str(row["session_id"]),
            role=MessageRole(row["role"]),
            content=row["content"],
            parent_message_id=str(row["parent_message_id"]) if row.get("parent_message_id") else None,
            tokens_input=row.get("tokens_input", 0),
            tokens_output=row.get("tokens_output", 0),
            model_used=row.get("model_used"),
            latency_ms=row.get("latency_ms"),
            tool_calls=json.loads(row["tool_calls"]) if row.get("tool_calls") else None,
            tool_results=json.loads(row["tool_results"]) if row.get("tool_results") else None,
            metadata=json.loads(row["metadata"]) if row.get("metadata") else {},
            created_at=row["created_at"]
        )

    def _row_to_memory(self, row: Dict) -> UserMemory:
        """Convert DB row to UserMemory"""
        return UserMemory(
            id=str(row["id"]),
            tenant_id=str(row["tenant_id"]),
            user_id=str(row["user_id"]),
            category=MemoryCategory(row["category"]),
            key=row["key"],
            value=row["value"],
            confidence=float(row.get("confidence", 0.8)),
            source=MemorySource(row.get("source", "extracted")),
            source_message_id=str(row["source_message_id"]) if row.get("source_message_id") else None,
            is_active=row.get("is_active", True),
            access_count=row.get("access_count", 0),
            metadata=json.loads(row["metadata"]) if row.get("metadata") else {},
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            last_accessed_at=row.get("last_accessed_at")
        )


# ============================================
# Singleton Instance
# ============================================

_memory_service: Optional[MemoryService] = None


def get_memory_service() -> MemoryService:
    """Get singleton memory service"""
    global _memory_service
    if _memory_service is None:
        _memory_service = MemoryService()
    return _memory_service
