"""
IAFactory Memory System - Modèles Pydantic
==========================================
Conversations, Messages, User Memories, Embeddings
Multi-tenant avec support contexte IA
"""

from datetime import datetime
from enum import Enum
from typing import Optional, Any, List
from pydantic import BaseModel, Field
import uuid


# ============================================
# Enums
# ============================================

class MemoryCategory(str, Enum):
    """Catégories de mémoire utilisateur"""
    PROFILE = "profile"          # Infos personnelles
    PREFERENCE = "preference"    # Préférences utilisateur
    BUSINESS = "business"        # Infos entreprise
    FACT = "fact"               # Faits importants
    GOAL = "goal"               # Objectifs


class MessageRole(str, Enum):
    """Rôles dans une conversation"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"


class AppContext(str, Enum):
    """Contextes d'application"""
    CHAT = "chat"
    PME = "pme"
    RAG = "rag"
    CRM = "crm"
    BOLT = "bolt"
    COUNCIL = "council"


class MemorySource(str, Enum):
    """Sources de mémoire"""
    EXTRACTED = "extracted"      # Extrait de conversations
    EXPLICIT = "explicit"        # Défini explicitement
    SYSTEM = "system"           # Généré par le système


# ============================================
# Chat Sessions
# ============================================

class ChatSessionBase(BaseModel):
    """Base session de chat"""
    title: Optional[str] = None
    app_context: AppContext = AppContext.CHAT
    language: str = "fr"
    agent_id: Optional[str] = None
    model: str = "groq"
    metadata: dict[str, Any] = Field(default_factory=dict)


class ChatSessionCreate(ChatSessionBase):
    """Création session"""
    pass


class ChatSessionUpdate(BaseModel):
    """Mise à jour session"""
    title: Optional[str] = None
    is_archived: Optional[bool] = None
    is_starred: Optional[bool] = None
    metadata: Optional[dict[str, Any]] = None


class ChatSession(ChatSessionBase):
    """Session complète"""
    id: str
    tenant_id: str
    user_id: str
    message_count: int = 0
    total_tokens: int = 0
    is_archived: bool = False
    is_starred: bool = False
    created_at: datetime
    updated_at: datetime
    last_message_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ChatSessionWithMessages(ChatSession):
    """Session avec messages"""
    messages: List["ChatMessage"] = []


class ChatSessionSummary(BaseModel):
    """Résumé de session pour liste"""
    id: str
    title: Optional[str] = None
    app_context: AppContext
    message_count: int
    is_starred: bool
    created_at: datetime
    last_message_at: Optional[datetime] = None
    preview: Optional[str] = None  # Premier message tronqué


# ============================================
# Chat Messages
# ============================================

class ChatMessageBase(BaseModel):
    """Base message"""
    role: MessageRole
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class ChatMessageCreate(ChatMessageBase):
    """Création message"""
    tokens_input: int = 0
    tokens_output: int = 0
    model_used: Optional[str] = None
    latency_ms: Optional[int] = None
    tool_calls: Optional[List[dict]] = None
    tool_results: Optional[List[dict]] = None


class ChatMessage(ChatMessageBase):
    """Message complet"""
    id: str
    session_id: str
    parent_message_id: Optional[str] = None
    tokens_input: int = 0
    tokens_output: int = 0
    model_used: Optional[str] = None
    latency_ms: Optional[int] = None
    tool_calls: Optional[List[dict]] = None
    tool_results: Optional[List[dict]] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ChatMessageResponse(BaseModel):
    """Réponse avec message généré"""
    message: ChatMessage
    session_id: str
    tokens_used: int
    model: str
    latency_ms: int


# ============================================
# User Memories
# ============================================

class UserMemoryBase(BaseModel):
    """Base mémoire"""
    category: MemoryCategory
    key: str = Field(..., max_length=100)
    value: str
    confidence: float = Field(default=0.80, ge=0, le=1)
    source: MemorySource = MemorySource.EXTRACTED
    metadata: dict[str, Any] = Field(default_factory=dict)


class UserMemoryCreate(UserMemoryBase):
    """Création mémoire"""
    source_message_id: Optional[str] = None


class UserMemoryUpdate(BaseModel):
    """Mise à jour mémoire"""
    value: Optional[str] = None
    confidence: Optional[float] = None
    is_active: Optional[bool] = None
    metadata: Optional[dict[str, Any]] = None


class UserMemory(UserMemoryBase):
    """Mémoire complète"""
    id: str
    tenant_id: str
    user_id: str
    source_message_id: Optional[str] = None
    is_active: bool = True
    access_count: int = 0
    created_at: datetime
    updated_at: datetime
    last_accessed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserMemoryWithHistory(UserMemory):
    """Mémoire avec corrections"""
    corrections: List["MemoryCorrection"] = []


# ============================================
# Memory Corrections
# ============================================

class MemoryCorrectionCreate(BaseModel):
    """Création correction"""
    memory_id: str
    old_value: str
    new_value: str
    reason: Optional[str] = None


class MemoryCorrection(MemoryCorrectionCreate):
    """Correction complète"""
    id: str
    corrected_by: str  # user_id ou "system"
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================
# Conversation Summaries
# ============================================

class ConversationSummaryBase(BaseModel):
    """Base résumé conversation"""
    summary_text: str
    key_topics: List[str] = Field(default_factory=list)
    extracted_entities: dict[str, Any] = Field(default_factory=dict)


class ConversationSummaryCreate(ConversationSummaryBase):
    """Création résumé"""
    session_id: str
    messages_summarized: int


class ConversationSummary(ConversationSummaryBase):
    """Résumé complet"""
    id: str
    session_id: str
    messages_summarized: int
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================
# Memory Context (pour injection IA)
# ============================================

class MemoryContext(BaseModel):
    """Contexte mémoire pour prompt IA"""
    user_profile: dict[str, str] = Field(default_factory=dict)
    preferences: dict[str, str] = Field(default_factory=dict)
    business_info: dict[str, str] = Field(default_factory=dict)
    relevant_facts: List[str] = Field(default_factory=list)
    goals: List[str] = Field(default_factory=list)
    recent_topics: List[str] = Field(default_factory=list)

    def to_system_prompt(self) -> str:
        """Génère un prompt système avec le contexte"""
        parts = []

        if self.user_profile:
            profile_str = ", ".join(f"{k}: {v}" for k, v in self.user_profile.items())
            parts.append(f"Profil utilisateur: {profile_str}")

        if self.preferences:
            pref_str = ", ".join(f"{k}: {v}" for k, v in self.preferences.items())
            parts.append(f"Préférences: {pref_str}")

        if self.business_info:
            biz_str = ", ".join(f"{k}: {v}" for k, v in self.business_info.items())
            parts.append(f"Entreprise: {biz_str}")

        if self.relevant_facts:
            parts.append(f"Faits importants: {'; '.join(self.relevant_facts)}")

        if self.goals:
            parts.append(f"Objectifs: {'; '.join(self.goals)}")

        if self.recent_topics:
            parts.append(f"Sujets récents: {', '.join(self.recent_topics)}")

        return "\n".join(parts) if parts else ""

    def is_empty(self) -> bool:
        """Vérifie si le contexte est vide"""
        return not any([
            self.user_profile,
            self.preferences,
            self.business_info,
            self.relevant_facts,
            self.goals,
            self.recent_topics
        ])


# ============================================
# Memory Extraction (pour extraction IA)
# ============================================

class ExtractedMemory(BaseModel):
    """Mémoire extraite par IA"""
    category: MemoryCategory
    key: str
    value: str
    confidence: float = Field(ge=0, le=1)
    reasoning: Optional[str] = None


class MemoryExtractionResult(BaseModel):
    """Résultat extraction mémoire"""
    session_id: str
    message_id: str
    memories: List[ExtractedMemory] = []
    processed_at: datetime = Field(default_factory=datetime.now)


# ============================================
# API Request/Response Models
# ============================================

class SendMessageRequest(BaseModel):
    """Requête envoi message"""
    content: str
    session_id: Optional[str] = None  # Crée nouvelle session si None
    app_context: AppContext = AppContext.CHAT
    model: str = "groq"
    include_memory: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)


class SendMessageResponse(BaseModel):
    """Réponse envoi message"""
    success: bool
    session_id: str
    user_message: ChatMessage
    assistant_message: ChatMessage
    tokens_used: int
    credits_consumed: int
    memories_extracted: int = 0


class GetConversationsRequest(BaseModel):
    """Requête liste conversations"""
    app_context: Optional[AppContext] = None
    is_starred: Optional[bool] = None
    is_archived: bool = False
    limit: int = Field(default=20, le=100)
    offset: int = 0


class GetConversationsResponse(BaseModel):
    """Réponse liste conversations"""
    conversations: List[ChatSessionSummary]
    total: int
    has_more: bool


class GetMessagesRequest(BaseModel):
    """Requête messages d'une session"""
    session_id: str
    limit: int = Field(default=50, le=200)
    before_id: Optional[str] = None  # Pagination cursor


class GetMessagesResponse(BaseModel):
    """Réponse messages"""
    session_id: str
    messages: List[ChatMessage]
    has_more: bool


class GetMemoriesResponse(BaseModel):
    """Réponse mémoires utilisateur"""
    memories: List[UserMemory]
    by_category: dict[str, List[UserMemory]]
    total: int


class UpdateMemoryRequest(BaseModel):
    """Requête mise à jour mémoire"""
    value: str
    reason: Optional[str] = None


class DeleteMemoryRequest(BaseModel):
    """Requête suppression mémoire"""
    memory_id: str
    reason: Optional[str] = None


class MemoryStatsResponse(BaseModel):
    """Statistiques mémoire utilisateur"""
    user_id: str
    total_memories: int
    memories_by_category: dict[str, int]
    total_conversations: int
    total_messages: int
    average_messages_per_conversation: float
    most_discussed_topics: List[str]
    oldest_memory_date: Optional[datetime] = None
    newest_memory_date: Optional[datetime] = None


# ============================================
# Embedding Models (pour recherche sémantique)
# ============================================

class EmbeddingBase(BaseModel):
    """Base embedding"""
    content_hash: str
    model_used: str = "text-embedding-3-small"


class MessageEmbedding(EmbeddingBase):
    """Embedding de message"""
    id: str
    message_id: str
    # embedding: List[float]  # Trop lourd pour transfert API
    created_at: datetime

    class Config:
        from_attributes = True


class MemoryEmbedding(EmbeddingBase):
    """Embedding de mémoire"""
    id: str
    memory_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class SemanticSearchRequest(BaseModel):
    """Requête recherche sémantique"""
    query: str
    search_type: str = "all"  # "messages", "memories", "all"
    limit: int = Field(default=10, le=50)
    min_similarity: float = Field(default=0.7, ge=0, le=1)
    app_context: Optional[AppContext] = None


class SemanticSearchResult(BaseModel):
    """Résultat recherche sémantique"""
    id: str
    type: str  # "message" ou "memory"
    content: str
    similarity: float
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


class SemanticSearchResponse(BaseModel):
    """Réponse recherche sémantique"""
    query: str
    results: List[SemanticSearchResult]
    total_found: int
    search_time_ms: int


# Forward references resolution
ChatSessionWithMessages.model_rebuild()
UserMemoryWithHistory.model_rebuild()
