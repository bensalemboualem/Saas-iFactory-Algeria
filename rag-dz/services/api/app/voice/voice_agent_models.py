"""
VOICE_AGENT - Modèles Pydantic
==============================
Agent vocal complet pour iaFactoryDZ
Pipeline: STT → DARIJA_NLP → BIG RAG → LLM → TTS

L'agent vocal qui comprend et parle darija algérienne.
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field
import uuid


# ============================================
# ENUMS
# ============================================

class AgentMode(str, Enum):
    """Mode de l'agent vocal"""
    CONVERSATION = "conversation"    # Chat conversationnel
    RAG_QUERY = "rag_query"          # Requête RAG
    COMMAND = "command"              # Commande spécifique
    ASSISTANT = "assistant"          # Assistant général
    PME_ADVISOR = "pme_advisor"      # Conseiller PME
    CRM_AGENT = "crm_agent"          # Agent CRM


class AgentLanguage(str, Enum):
    """Langues supportées par l'agent"""
    ARABIC = "ar"
    ARABIC_DZ = "ar-dz"
    FRENCH = "fr"
    ENGLISH = "en"
    AUTO = "auto"


class AgentDialect(str, Enum):
    """Dialectes arabes"""
    DARIJA = "darija"
    MSA = "msa"
    MIXED = "mixed"


class ConversationStatus(str, Enum):
    """Statut de la conversation"""
    ACTIVE = "active"
    PAUSED = "paused"
    ENDED = "ended"
    ERROR = "error"


class ProcessingStep(str, Enum):
    """Étapes du pipeline vocal"""
    STT = "stt"                      # Speech-to-Text
    NLP = "nlp"                      # DARIJA_NLP normalization
    INTENT = "intent"                # Intent detection
    RAG = "rag"                      # RAG retrieval
    LLM = "llm"                      # LLM generation
    TTS = "tts"                      # Text-to-Speech


class IntentType(str, Enum):
    """Types d'intentions détectées"""
    QUESTION = "question"            # Question générale
    SEARCH = "search"                # Recherche d'info
    COMMAND = "command"              # Commande action
    GREETING = "greeting"            # Salutation
    GOODBYE = "goodbye"              # Au revoir
    THANKS = "thanks"                # Remerciement
    HELP = "help"                    # Demande d'aide
    CLARIFICATION = "clarification"  # Clarification
    CONFIRMATION = "confirmation"    # Confirmation
    NEGATION = "negation"            # Négation
    PME_QUERY = "pme_query"          # Question PME
    CRM_ACTION = "crm_action"        # Action CRM
    UNKNOWN = "unknown"              # Inconnu


# ============================================
# CONVERSATION MODELS
# ============================================

class ConversationMessage(BaseModel):
    """Message dans une conversation"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: Literal["user", "assistant", "system"] = Field(..., description="Rôle du message")
    content: str = Field(..., description="Contenu textuel")
    
    # Audio (optionnel)
    audio_base64: Optional[str] = Field(None, description="Audio en base64")
    
    # Métadonnées
    language: Optional[str] = Field(None, description="Langue détectée")
    dialect: Optional[str] = Field(None, description="Dialecte")
    is_arabizi: Optional[bool] = Field(None, description="Contient de l'arabizi")
    
    # Intent
    intent: Optional[IntentType] = Field(None, description="Intention détectée")
    intent_confidence: Optional[float] = Field(None, description="Confiance intent")
    
    # Timing
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    processing_time_ms: int = Field(0, description="Temps de traitement")


class ConversationContext(BaseModel):
    """Contexte de la conversation"""
    # User info
    user_id: Optional[str] = Field(None, description="ID utilisateur")
    user_name: Optional[str] = Field(None, description="Nom utilisateur")
    user_language: AgentLanguage = Field(AgentLanguage.AUTO, description="Langue préférée")
    
    # Business context
    country: str = Field("DZ", description="Pays (DZ, CH)")
    sector: Optional[str] = Field(None, description="Secteur d'activité")
    company_name: Optional[str] = Field(None, description="Nom entreprise")
    
    # Session
    session_topic: Optional[str] = Field(None, description="Sujet de la session")
    custom_prompt: Optional[str] = Field(None, description="Prompt personnalisé")
    
    # RAG context
    rag_collection: Optional[str] = Field(None, description="Collection Qdrant")
    rag_filter: Optional[Dict[str, Any]] = Field(None, description="Filtres RAG")
    
    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ConversationState(BaseModel):
    """État complet d'une conversation"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: ConversationStatus = Field(ConversationStatus.ACTIVE)
    mode: AgentMode = Field(AgentMode.ASSISTANT)
    
    # Messages
    messages: List[ConversationMessage] = Field(default_factory=list)
    message_count: int = Field(0, description="Nombre de messages")
    
    # Context
    context: ConversationContext = Field(default_factory=ConversationContext)
    
    # Language tracking
    detected_language: Optional[str] = Field(None)
    detected_dialect: Optional[str] = Field(None)
    
    # Stats
    total_user_chars: int = Field(0)
    total_assistant_chars: int = Field(0)
    total_audio_duration_sec: float = Field(0.0)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)


# ============================================
# REQUEST MODELS
# ============================================

class VoiceAgentRequest(BaseModel):
    """Requête principale de l'agent vocal"""
    # Input (audio OU texte)
    audio_base64: Optional[str] = Field(None, description="Audio input en base64")
    text: Optional[str] = Field(None, description="Texte input (alternative à audio)")
    
    # Conversation
    conversation_id: Optional[str] = Field(None, description="ID conversation existante")
    
    # Options
    mode: AgentMode = Field(AgentMode.ASSISTANT, description="Mode de l'agent")
    language_hint: AgentLanguage = Field(AgentLanguage.AUTO, description="Indice de langue")
    dialect: AgentDialect = Field(AgentDialect.DARIJA, description="Dialecte arabe")
    
    # Output options
    return_audio: bool = Field(True, description="Retourner audio TTS")
    return_text: bool = Field(True, description="Retourner texte")
    voice_id: Optional[str] = Field(None, description="Voix TTS à utiliser")
    
    # Context
    context: Optional[ConversationContext] = Field(None, description="Contexte additionnel")
    
    # RAG options
    use_rag: bool = Field(True, description="Utiliser RAG pour contexte")
    rag_collection: Optional[str] = Field(None, description="Collection Qdrant spécifique")
    rag_top_k: int = Field(5, ge=1, le=20, description="Nombre de résultats RAG")
    
    # Advanced
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="Température LLM")
    max_tokens: int = Field(500, ge=50, le=2000, description="Tokens max réponse")
    tenant: Optional[str] = Field(None, description="Tenant ID (swiss, algeria, etc.)")
    system_prompt: Optional[str] = Field(None, description="System prompt custom")
    system_prompt: Optional[str] = Field(None, description="System prompt custom")


class VoiceAgentTextRequest(BaseModel):
    """Requête texte simplifiée"""
    text: str = Field(..., min_length=1, max_length=2000, description="Question/commande texte")
    conversation_id: Optional[str] = Field(None)
    mode: AgentMode = Field(AgentMode.ASSISTANT, description="Mode agent")
    language_hint: AgentLanguage = Field(AgentLanguage.AUTO, description="Indice langue")
    dialect: AgentDialect = Field(AgentDialect.DARIJA, description="Dialecte")
    return_audio: bool = Field(False, description="Générer audio TTS")
    voice_id: Optional[str] = Field(None, description="Voix TTS")
    use_rag: bool = Field(False, description="Utiliser RAG")
    rag_collection: Optional[str] = Field(None)
    rag_top_k: int = Field(5)
    temperature: float = Field(0.7)
    max_tokens: int = Field(500)
    tenant: Optional[str] = Field(None, description="Tenant ID (swiss, algeria, etc.)")
    system_prompt: Optional[str] = Field(None, description="System prompt custom")


class VoiceAgentAudioRequest(BaseModel):
    """Requête audio simplifiée"""
    audio_base64: str = Field(..., description="Audio en base64")
    conversation_id: Optional[str] = Field(None)
    mode: AgentMode = Field(AgentMode.ASSISTANT, description="Mode agent")
    language_hint: AgentLanguage = Field(AgentLanguage.AUTO, description="Indice langue")
    dialect: AgentDialect = Field(AgentDialect.DARIJA, description="Dialecte")
    return_audio: bool = Field(True, description="Générer audio TTS")
    voice_id: Optional[str] = Field(None, description="Voix TTS")
    use_rag: bool = Field(False, description="Utiliser RAG")
    rag_collection: Optional[str] = Field(None)
    rag_top_k: int = Field(5)
    temperature: float = Field(0.7)
    max_tokens: int = Field(500)


# ============================================
# RESPONSE MODELS
# ============================================

class ProcessingStepResult(BaseModel):
    """Résultat d'une étape du pipeline"""
    step: ProcessingStep
    success: bool
    duration_ms: int
    output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class VoiceAgentResponse(BaseModel):
    """Réponse complète de l'agent vocal"""
    # IDs
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    conversation_id: str = Field(..., description="ID de la conversation")
    
    # Résultat principal
    success: bool = Field(True)
    
    # Texte
    input_text: str = Field(..., description="Texte input (transcrit ou fourni)")
    input_text_normalized: Optional[str] = Field(None, description="Texte normalisé (darija)")
    output_text: str = Field(..., description="Réponse textuelle")
    
    # Audio
    output_audio_base64: Optional[str] = Field(None, description="Réponse audio en base64")
    audio_duration_sec: Optional[float] = Field(None, description="Durée audio réponse")
    
    # Langue
    detected_language: str = Field(..., description="Langue détectée")
    detected_dialect: Optional[str] = Field(None, description="Dialecte détecté")
    is_arabizi: bool = Field(False, description="Input était en arabizi")
    
    # Intent
    intent: IntentType = Field(IntentType.UNKNOWN, description="Intention détectée")
    intent_confidence: float = Field(0.0, description="Confiance de l'intent")
    
    # RAG
    rag_used: bool = Field(False, description="RAG utilisé")
    rag_sources: List[Dict[str, Any]] = Field(default_factory=list, description="Sources RAG")
    rag_context: Optional[str] = Field(None, description="Contexte RAG fourni au LLM")
    
    # Pipeline details
    pipeline_steps: List[ProcessingStepResult] = Field(default_factory=list)
    total_processing_time_ms: int = Field(0)
    
    # Conversation state
    message_index: int = Field(0, description="Index du message dans la conversation")
    conversation_length: int = Field(0, description="Longueur conversation")
    
    # Metadata
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    model_used: Optional[str] = Field(None, description="Modèle LLM utilisé")
    voice_used: Optional[str] = Field(None, description="Voix TTS utilisée")


class VoiceAgentStreamChunk(BaseModel):
    """Chunk pour streaming de réponse"""
    chunk_type: Literal["text", "audio", "status", "error"] = Field(...)
    content: str = Field(..., description="Contenu du chunk")
    is_final: bool = Field(False)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ============================================
# STATUS MODELS
# ============================================

class VoiceAgentStatus(BaseModel):
    """Statut du service Voice Agent"""
    ready: bool = Field(True)
    service: str = Field("VOICE_AGENT")
    version: str = Field("1.0.0")
    
    # Composants
    components: Dict[str, bool] = Field(default_factory=dict)
    
    # Capacités
    modes: List[str] = Field(default_factory=lambda: [m.value for m in AgentMode])
    languages: List[str] = Field(default_factory=lambda: ["ar", "ar-dz", "fr", "en"])
    dialects: List[str] = Field(default_factory=lambda: ["darija", "msa", "mixed"])
    
    # Stats
    active_conversations: int = Field(0)
    total_requests_today: int = Field(0)


class VoiceAgentError(BaseModel):
    """Erreur Voice Agent"""
    error: str
    message: str
    code: int
    step: Optional[ProcessingStep] = None
    details: Optional[Dict[str, Any]] = None


# ============================================
# INTENT DETECTION
# ============================================

class IntentDetectionResult(BaseModel):
    """Résultat de détection d'intention"""
    intent: IntentType
    confidence: float = Field(ge=0.0, le=1.0)
    entities: Dict[str, Any] = Field(default_factory=dict)
    sub_intents: List[str] = Field(default_factory=list)


# ============================================
# CONSTANTS
# ============================================

# Prompts système par mode
SYSTEM_PROMPTS = {
    AgentMode.ASSISTANT: """Tu es un assistant IA intelligent pour iaFactory, une plateforme algérienne.
Tu parles français et darija algérienne. Tu es professionnel mais amical.
Tu aides les utilisateurs avec leurs questions sur l'administration, les entreprises, et la vie quotidienne en Algérie.""",
    
    AgentMode.PME_ADVISOR: """Tu es un conseiller expert pour les PME algériennes.
Tu connais bien le contexte business en Algérie: CASNOS, CNAS, registre de commerce, impôts, etc.
Tu donnes des conseils pratiques et précis. Tu parles français et darija.""",
    
    AgentMode.CRM_AGENT: """Tu es un agent commercial pour iaFactory.
Tu qualifies les leads, réponds aux questions sur les services, et guides les prospects.
Tu es professionnel, persuasif mais pas agressif. Tu parles français et darija.""",
    
    AgentMode.RAG_QUERY: """Tu es un assistant de recherche documentaire.
Tu réponds aux questions en te basant sur les documents fournis dans le contexte.
Cite tes sources quand possible. Si tu ne trouves pas l'info, dis-le clairement.""",
    
    AgentMode.CONVERSATION: """Tu es un assistant conversationnel amical.
Tu maintiens une conversation naturelle en français ou darija.
Tu te souviens du contexte de la conversation.""",
}

# Mots-clés pour détection d'intention
INTENT_KEYWORDS = {
    IntentType.GREETING: ["salam", "مرحبا", "bonjour", "salut", "سلام", "صباح", "مساء"],
    IntentType.GOODBYE: ["bessalama", "بالسلامة", "au revoir", "bye", "مع السلامة"],
    IntentType.THANKS: ["choukran", "شكرا", "merci", "thanks", "sahit", "صحيت"],
    IntentType.HELP: ["aide", "help", "عاوني", "كيفاش", "comment", "how"],
    IntentType.PME_QUERY: ["casnos", "cnas", "registre", "impots", "entreprise", "شركة"],
}

# Limites
MAX_CONVERSATION_LENGTH = 50  # Messages max par conversation
MAX_AUDIO_DURATION_SEC = 120  # 2 minutes max par audio


# ============================================
# CONVERSATION SUMMARY
# ============================================

class ConversationSummary(BaseModel):
    """Résumé léger d'une conversation (pour liste)"""
    id: str
    status: ConversationStatus
    mode: AgentMode
    message_count: int
    
    # Aperçu
    first_message: Optional[str] = Field(None, description="Premier message user")
    last_message: Optional[str] = Field(None, description="Dernier message")
    
    # Langue
    detected_language: Optional[str] = None
    detected_dialect: Optional[str] = None
    
    # Context léger
    topic: Optional[str] = None
    user_id: Optional[str] = None
    
    # Timestamps
    created_at: datetime
    last_activity: datetime
    
    # Stats
    total_chars: int = 0
    total_audio_sec: float = 0.0
