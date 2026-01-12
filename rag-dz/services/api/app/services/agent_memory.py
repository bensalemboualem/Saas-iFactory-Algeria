"""
IAFactory Agent Memory Service - Persistent Memory for AI Agents
================================================================
Inspired by MemGPT - Gives agents long-term memory capabilities

Memory Types:
1. Working Memory - Current conversation context (limited size)
2. Long-term Memory - Persistent storage in database
3. Semantic Memory - Embeddings for similarity search
4. Episodic Memory - Past interaction memories
5. User Profile Memory - Learned preferences

Features:
- Automatic memory consolidation (working → long-term)
- Semantic search for relevant memories
- User preference learning
- Conversation summarization
- Memory importance scoring
"""
import asyncio
import logging
import json
import hashlib
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import os

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


# ============================================
# MEMORY TYPES & MODELS
# ============================================

class MemoryType(str, Enum):
    """Types of agent memory"""
    WORKING = "working"         # Current context, limited size
    LONG_TERM = "long_term"     # Persistent, consolidated
    EPISODIC = "episodic"       # Specific event memories
    SEMANTIC = "semantic"       # Concepts and knowledge
    PROCEDURAL = "procedural"   # How to do things
    USER_PROFILE = "user_profile"  # User preferences


class MemoryImportance(str, Enum):
    """Memory importance levels"""
    LOW = "low"           # Can be forgotten
    MEDIUM = "medium"     # Keep for some time
    HIGH = "high"         # Important, keep long
    CRITICAL = "critical" # Never forget


@dataclass
class Memory:
    """A single memory unit"""
    id: str
    memory_type: MemoryType
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    importance: MemoryImportance = MemoryImportance.MEDIUM
    embedding: Optional[List[float]] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_accessed: datetime = field(default_factory=datetime.utcnow)
    access_count: int = 0
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    agent_id: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    related_memories: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "memory_type": self.memory_type.value,
            "content": self.content,
            "metadata": self.metadata,
            "importance": self.importance.value,
            "created_at": self.created_at.isoformat(),
            "last_accessed": self.last_accessed.isoformat(),
            "access_count": self.access_count,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "agent_id": self.agent_id,
            "tags": self.tags,
        }


@dataclass
class UserProfile:
    """User preference profile learned over time"""
    user_id: str
    language_preference: str = "fr"
    communication_style: str = "professional"  # casual, professional, formal
    topics_of_interest: List[str] = field(default_factory=list)
    preferred_response_length: str = "medium"  # short, medium, long
    timezone: Optional[str] = None
    custom_preferences: Dict[str, Any] = field(default_factory=dict)
    interaction_count: int = 0
    first_interaction: datetime = field(default_factory=datetime.utcnow)
    last_interaction: datetime = field(default_factory=datetime.utcnow)
    learned_patterns: Dict[str, Any] = field(default_factory=dict)


# ============================================
# WORKING MEMORY (Short-term)
# ============================================

class WorkingMemory:
    """
    Working memory - Limited capacity, current context
    Similar to human short-term memory (7 ± 2 items)
    """

    MAX_ITEMS = 15  # Maximum items in working memory
    MAX_TOKENS = 4000  # Maximum tokens to keep

    def __init__(self):
        self.items: List[Dict[str, Any]] = []
        self.context: Dict[str, Any] = {}
        self.current_goal: Optional[str] = None
        self.attention_focus: Optional[str] = None

    def add(self, item: Dict[str, Any], importance: float = 0.5):
        """Add item to working memory, evicting if necessary"""
        item["timestamp"] = datetime.utcnow().isoformat()
        item["importance"] = importance

        self.items.append(item)

        # Evict least important items if over capacity
        if len(self.items) > self.MAX_ITEMS:
            self._consolidate()

    def _consolidate(self):
        """Remove least important items, keeping important ones"""
        # Sort by importance (descending) and recency
        self.items.sort(
            key=lambda x: (x.get("importance", 0.5), x.get("timestamp", "")),
            reverse=True
        )
        # Keep only MAX_ITEMS
        self.items = self.items[:self.MAX_ITEMS]

    def get_context_string(self, max_tokens: int = 2000) -> str:
        """Get working memory as context string for LLM"""
        context_parts = []

        for item in self.items[-10:]:  # Last 10 items
            if item.get("role") == "user":
                context_parts.append(f"User: {item.get('content', '')}")
            elif item.get("role") == "assistant":
                context_parts.append(f"Assistant: {item.get('content', '')}")
            else:
                context_parts.append(str(item.get('content', '')))

        return "\n".join(context_parts)

    def set_goal(self, goal: str):
        """Set current goal/task"""
        self.current_goal = goal

    def set_focus(self, focus: str):
        """Set attention focus"""
        self.attention_focus = focus

    def clear(self):
        """Clear working memory"""
        self.items = []
        self.context = {}
        self.current_goal = None
        self.attention_focus = None


# ============================================
# LONG-TERM MEMORY
# ============================================

class LongTermMemory:
    """
    Long-term memory - Persistent storage
    Uses embeddings for semantic search
    """

    def __init__(self, storage_backend: str = "memory"):
        """
        Initialize long-term memory

        Args:
            storage_backend: 'memory' (in-memory), 'postgres', 'qdrant', 'supabase'
        """
        self.storage_backend = storage_backend
        self.memories: Dict[str, Memory] = {}
        self.embeddings_index: Dict[str, List[float]] = {}

        # Try to load embeddings client
        self.embeddings_client = None
        try:
            from openai import AsyncOpenAI
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.embeddings_client = AsyncOpenAI(api_key=api_key)
        except ImportError:
            logger.warning("OpenAI not available for embeddings")

    def _generate_id(self, content: str, user_id: str = None) -> str:
        """Generate unique memory ID"""
        data = f"{content}{user_id or ''}{datetime.utcnow().isoformat()}"
        return hashlib.md5(data.encode()).hexdigest()[:16]

    async def store(
        self,
        content: str,
        memory_type: MemoryType = MemoryType.LONG_TERM,
        importance: MemoryImportance = MemoryImportance.MEDIUM,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
    ) -> Memory:
        """Store a memory"""

        memory_id = self._generate_id(content, user_id)

        # Generate embedding if client available
        embedding = None
        if self.embeddings_client:
            try:
                embedding = await self._get_embedding(content)
            except Exception as e:
                logger.warning(f"Failed to generate embedding: {e}")

        memory = Memory(
            id=memory_id,
            memory_type=memory_type,
            content=content,
            importance=importance,
            embedding=embedding,
            user_id=user_id,
            session_id=session_id,
            agent_id=agent_id,
            metadata=metadata or {},
            tags=tags or [],
        )

        self.memories[memory_id] = memory

        if embedding:
            self.embeddings_index[memory_id] = embedding

        logger.debug(f"Stored memory {memory_id}: {content[:50]}...")

        return memory

    async def retrieve(
        self,
        query: str,
        user_id: Optional[str] = None,
        memory_type: Optional[MemoryType] = None,
        limit: int = 5,
    ) -> List[Memory]:
        """Retrieve relevant memories using semantic search"""

        # Filter by user and type
        candidates = [
            m for m in self.memories.values()
            if (user_id is None or m.user_id == user_id)
            and (memory_type is None or m.memory_type == memory_type)
        ]

        if not candidates:
            return []

        # If embeddings available, do semantic search
        if self.embeddings_client and self.embeddings_index:
            try:
                query_embedding = await self._get_embedding(query)
                scored = []

                for memory in candidates:
                    if memory.id in self.embeddings_index:
                        similarity = self._cosine_similarity(
                            query_embedding,
                            self.embeddings_index[memory.id]
                        )
                        scored.append((memory, similarity))

                # Sort by similarity
                scored.sort(key=lambda x: x[1], reverse=True)

                # Update access counts
                results = []
                for memory, _ in scored[:limit]:
                    memory.last_accessed = datetime.utcnow()
                    memory.access_count += 1
                    results.append(memory)

                return results

            except Exception as e:
                logger.warning(f"Semantic search failed: {e}")

        # Fallback: keyword search
        query_lower = query.lower()
        scored = []

        for memory in candidates:
            # Simple keyword matching
            content_lower = memory.content.lower()
            matches = sum(1 for word in query_lower.split() if word in content_lower)
            if matches > 0:
                scored.append((memory, matches))

        scored.sort(key=lambda x: x[1], reverse=True)

        return [m for m, _ in scored[:limit]]

    async def _get_embedding(self, text: str) -> List[float]:
        """Get embedding vector for text"""
        if not self.embeddings_client:
            raise ValueError("Embeddings client not available")

        response = await self.embeddings_client.embeddings.create(
            model="text-embedding-3-small",
            input=text[:8000]  # Limit input
        )

        return response.data[0].embedding

    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        import math

        dot_product = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x ** 2 for x in a))
        norm_b = math.sqrt(sum(x ** 2 for x in b))

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot_product / (norm_a * norm_b)

    async def forget(
        self,
        memory_id: Optional[str] = None,
        older_than: Optional[timedelta] = None,
        importance_below: Optional[MemoryImportance] = None,
    ) -> int:
        """Forget (delete) memories based on criteria"""
        deleted = 0

        if memory_id:
            if memory_id in self.memories:
                del self.memories[memory_id]
                if memory_id in self.embeddings_index:
                    del self.embeddings_index[memory_id]
                deleted = 1
        else:
            to_delete = []
            now = datetime.utcnow()

            for mid, memory in self.memories.items():
                should_delete = False

                if older_than and (now - memory.created_at) > older_than:
                    should_delete = True

                if importance_below:
                    importance_order = [
                        MemoryImportance.LOW,
                        MemoryImportance.MEDIUM,
                        MemoryImportance.HIGH,
                        MemoryImportance.CRITICAL
                    ]
                    if importance_order.index(memory.importance) < importance_order.index(importance_below):
                        should_delete = True

                if should_delete:
                    to_delete.append(mid)

            for mid in to_delete:
                del self.memories[mid]
                if mid in self.embeddings_index:
                    del self.embeddings_index[mid]
                deleted += 1

        logger.info(f"Forgot {deleted} memories")
        return deleted


# ============================================
# USER PROFILE MEMORY
# ============================================

class UserProfileMemory:
    """
    Manages user profiles and learned preferences
    """

    def __init__(self):
        self.profiles: Dict[str, UserProfile] = {}

    def get_or_create(self, user_id: str) -> UserProfile:
        """Get or create user profile"""
        if user_id not in self.profiles:
            self.profiles[user_id] = UserProfile(user_id=user_id)
        return self.profiles[user_id]

    def update_preference(self, user_id: str, key: str, value: Any):
        """Update a user preference"""
        profile = self.get_or_create(user_id)
        profile.custom_preferences[key] = value
        profile.last_interaction = datetime.utcnow()
        profile.interaction_count += 1

    def learn_from_interaction(
        self,
        user_id: str,
        interaction_type: str,
        data: Dict[str, Any]
    ):
        """Learn from user interaction"""
        profile = self.get_or_create(user_id)

        # Track interaction patterns
        if interaction_type not in profile.learned_patterns:
            profile.learned_patterns[interaction_type] = []

        profile.learned_patterns[interaction_type].append({
            "timestamp": datetime.utcnow().isoformat(),
            "data": data
        })

        # Keep only last 100 interactions per type
        if len(profile.learned_patterns[interaction_type]) > 100:
            profile.learned_patterns[interaction_type] = \
                profile.learned_patterns[interaction_type][-100:]

    def get_preference(self, user_id: str, key: str, default: Any = None) -> Any:
        """Get a user preference"""
        profile = self.profiles.get(user_id)
        if not profile:
            return default
        return profile.custom_preferences.get(key, default)

    def get_learned_pattern(self, user_id: str, pattern_type: str) -> List[Dict]:
        """Get learned patterns for a user"""
        profile = self.profiles.get(user_id)
        if not profile:
            return []
        return profile.learned_patterns.get(pattern_type, [])


# ============================================
# MAIN AGENT MEMORY SERVICE
# ============================================

class AgentMemoryService:
    """
    Main memory service for AI agents
    Combines all memory types with automatic management
    """

    def __init__(self, storage_backend: str = "memory"):
        """
        Initialize agent memory service

        Args:
            storage_backend: Storage backend ('memory', 'postgres', 'qdrant')
        """
        # Memory stores
        self.working_memories: Dict[str, WorkingMemory] = {}  # Per session
        self.long_term = LongTermMemory(storage_backend)
        self.user_profiles = UserProfileMemory()

        # Memory consolidation settings
        self.consolidation_threshold = 10  # Items before consolidation
        self.summarization_enabled = True

        logger.info(f"AgentMemoryService initialized with backend: {storage_backend}")

    # ------------------------------------------------
    # WORKING MEMORY
    # ------------------------------------------------

    def get_working_memory(self, session_id: str) -> WorkingMemory:
        """Get or create working memory for session"""
        if session_id not in self.working_memories:
            self.working_memories[session_id] = WorkingMemory()
        return self.working_memories[session_id]

    def add_to_working_memory(
        self,
        session_id: str,
        role: str,
        content: str,
        importance: float = 0.5,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Add item to working memory"""
        wm = self.get_working_memory(session_id)
        wm.add({
            "role": role,
            "content": content,
            "metadata": metadata or {}
        }, importance)

        # Check if consolidation needed
        if len(wm.items) >= self.consolidation_threshold:
            asyncio.create_task(self._consolidate_working_memory(session_id))

    async def _consolidate_working_memory(self, session_id: str):
        """Consolidate working memory to long-term"""
        wm = self.get_working_memory(session_id)

        if len(wm.items) < self.consolidation_threshold:
            return

        # Get items to consolidate (older half)
        items_to_consolidate = wm.items[:len(wm.items) // 2]

        # Summarize if enabled
        if self.summarization_enabled:
            summary = self._summarize_items(items_to_consolidate)
            if summary:
                await self.long_term.store(
                    content=summary,
                    memory_type=MemoryType.EPISODIC,
                    importance=MemoryImportance.MEDIUM,
                    session_id=session_id,
                    metadata={"consolidated_from": len(items_to_consolidate)}
                )
        else:
            # Store each item separately
            for item in items_to_consolidate:
                await self.long_term.store(
                    content=item.get("content", ""),
                    memory_type=MemoryType.EPISODIC,
                    importance=MemoryImportance.MEDIUM if item.get("importance", 0.5) > 0.5 else MemoryImportance.LOW,
                    session_id=session_id,
                    metadata=item.get("metadata", {})
                )

        # Remove consolidated items from working memory
        wm.items = wm.items[len(items_to_consolidate):]

        logger.debug(f"Consolidated {len(items_to_consolidate)} items from session {session_id}")

    def _summarize_items(self, items: List[Dict[str, Any]]) -> str:
        """Summarize a list of memory items"""
        # Simple summarization - could be enhanced with LLM
        messages = []
        for item in items:
            role = item.get("role", "")
            content = item.get("content", "")
            if role and content:
                messages.append(f"{role}: {content[:100]}")

        return f"Conversation summary ({len(items)} messages): " + " | ".join(messages[:5])

    # ------------------------------------------------
    # LONG-TERM MEMORY
    # ------------------------------------------------

    async def remember(
        self,
        content: str,
        user_id: Optional[str] = None,
        importance: MemoryImportance = MemoryImportance.MEDIUM,
        memory_type: MemoryType = MemoryType.LONG_TERM,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Memory:
        """Store something in long-term memory"""
        return await self.long_term.store(
            content=content,
            memory_type=memory_type,
            importance=importance,
            user_id=user_id,
            tags=tags,
            metadata=metadata
        )

    async def recall(
        self,
        query: str,
        user_id: Optional[str] = None,
        memory_type: Optional[MemoryType] = None,
        limit: int = 5,
    ) -> List[Memory]:
        """Recall relevant memories"""
        return await self.long_term.retrieve(
            query=query,
            user_id=user_id,
            memory_type=memory_type,
            limit=limit
        )

    async def forget(
        self,
        memory_id: Optional[str] = None,
        older_than_days: Optional[int] = None,
    ) -> int:
        """Forget memories"""
        older_than = timedelta(days=older_than_days) if older_than_days else None
        return await self.long_term.forget(
            memory_id=memory_id,
            older_than=older_than
        )

    # ------------------------------------------------
    # USER PROFILES
    # ------------------------------------------------

    def learn_user_preference(self, user_id: str, key: str, value: Any):
        """Learn a user preference"""
        self.user_profiles.update_preference(user_id, key, value)

    def get_user_preference(self, user_id: str, key: str, default: Any = None) -> Any:
        """Get a user preference"""
        return self.user_profiles.get_preference(user_id, key, default)

    def learn_from_interaction(
        self,
        user_id: str,
        interaction_type: str,
        data: Dict[str, Any]
    ):
        """Learn from user interaction"""
        self.user_profiles.learn_from_interaction(user_id, interaction_type, data)

    def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """Get complete user profile"""
        return self.user_profiles.profiles.get(user_id)

    # ------------------------------------------------
    # CONTEXT BUILDING
    # ------------------------------------------------

    async def build_context(
        self,
        session_id: str,
        user_id: Optional[str] = None,
        query: Optional[str] = None,
        max_tokens: int = 3000,
    ) -> str:
        """
        Build context string for LLM including:
        - Working memory (recent conversation)
        - Relevant long-term memories
        - User preferences
        """
        context_parts = []

        # 1. User profile
        if user_id:
            profile = self.get_user_profile(user_id)
            if profile:
                context_parts.append(
                    f"[User Profile]\n"
                    f"- Préférence langue: {profile.language_preference}\n"
                    f"- Style: {profile.communication_style}\n"
                    f"- Interactions: {profile.interaction_count}"
                )

        # 2. Relevant long-term memories
        if query:
            memories = await self.recall(query, user_id=user_id, limit=3)
            if memories:
                memory_texts = [f"- {m.content[:200]}" for m in memories]
                context_parts.append(
                    f"[Relevant Memories]\n" + "\n".join(memory_texts)
                )

        # 3. Working memory (recent conversation)
        wm = self.get_working_memory(session_id)
        wm_context = wm.get_context_string(max_tokens // 2)
        if wm_context:
            context_parts.append(f"[Recent Conversation]\n{wm_context}")

        return "\n\n".join(context_parts)

    # ------------------------------------------------
    # STATISTICS
    # ------------------------------------------------

    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        return {
            "working_memory_sessions": len(self.working_memories),
            "long_term_memories": len(self.long_term.memories),
            "user_profiles": len(self.user_profiles.profiles),
            "embeddings_indexed": len(self.long_term.embeddings_index),
        }


# ============================================
# SINGLETON INSTANCE
# ============================================

_memory_service: Optional[AgentMemoryService] = None


def get_memory_service() -> AgentMemoryService:
    """Get singleton memory service instance"""
    global _memory_service
    if _memory_service is None:
        _memory_service = AgentMemoryService()
    return _memory_service


def init_memory_service(storage_backend: str = "memory") -> AgentMemoryService:
    """Initialize memory service with custom backend"""
    global _memory_service
    _memory_service = AgentMemoryService(storage_backend)
    return _memory_service
