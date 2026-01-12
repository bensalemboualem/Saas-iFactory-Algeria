"""
Multi-LLM Models
================
SQLAlchemy + Pydantic models pour gestion multi-providers IA
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, Any, List
from pydantic import BaseModel, Field
import uuid


# ============================================
# Enums
# ============================================

class LLMProviderType(str, Enum):
    """Providers IA supportés"""
    # Chat LLM
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    GROQ = "groq"
    OPENROUTER = "openrouter"
    MISTRAL = "mistral"
    COHERE = "cohere"
    LOCAL = "local"  # Ollama, etc.
    
    # Image Generation
    DALLE = "dalle"              # OpenAI DALL-E
    MIDJOURNEY = "midjourney"    # Via API non-officielle ou proxy
    STABILITY = "stability"      # Stable Diffusion API
    IDEOGRAM = "ideogram"        # Ideogram AI
    LEONARDO = "leonardo"        # Leonardo.ai
    FLUX = "flux"                # Flux.1 (Black Forest Labs)
    
    # Video Generation
    RUNWAY = "runway"            # Runway Gen-2/Gen-3
    PIKA = "pika"                # Pika Labs
    KLING = "kling"              # Kling AI (Kuaishou)
    LUMA = "luma"                # Luma Dream Machine
    HEYGEN = "heygen"            # HeyGen (avatars)
    SYNTHESIA = "synthesia"      # Synthesia (avatars)
    
    # Audio/Voice
    ELEVENLABS = "elevenlabs"    # ElevenLabs TTS
    OPENAI_AUDIO = "openai_audio"  # OpenAI Whisper/TTS
    PLAY_HT = "play_ht"          # Play.ht
    MURF = "murf"                # Murf.ai
    
    # Music
    SUNO = "suno"                # Suno AI Music
    UDIO = "udio"                # Udio AI Music
    
    # Presentations
    GAMMA = "gamma"              # Gamma.app
    BEAUTIFUL_AI = "beautiful_ai"  # Beautiful.ai
    TOME = "tome"                # Tome
    
    # Code
    CURSOR = "cursor"            # Cursor IDE
    REPLIT = "replit"            # Replit AI
    GITHUB_COPILOT = "github_copilot"  # GitHub Copilot
    
    # Documents
    CLAUDE_DOCS = "claude_docs"  # Claude for long docs
    NOTEBOOKLM = "notebooklm"    # Google NotebookLM


class LLMModelType(str, Enum):
    """Types de modèles"""
    # Text
    CHAT = "chat"
    COMPLETION = "completion"
    EMBEDDING = "embedding"
    
    # Vision
    VISION = "vision"
    OCR = "ocr"
    
    # Image
    IMAGE_GEN = "image_gen"
    IMAGE_EDIT = "image_edit"
    IMAGE_UPSCALE = "image_upscale"
    
    # Video
    VIDEO_GEN = "video_gen"
    VIDEO_EDIT = "video_edit"
    VIDEO_AVATAR = "video_avatar"
    
    # Audio
    TTS = "tts"                  # Text-to-Speech
    STT = "stt"                  # Speech-to-Text
    VOICE_CLONE = "voice_clone"
    AUDIO_GEN = "audio_gen"
    
    # Music
    MUSIC_GEN = "music_gen"
    
    # Presentations
    PRESENTATION = "presentation"
    
    # Code
    CODE_GEN = "code_gen"
    CODE_REVIEW = "code_review"
    
    # Documents
    DOC_ANALYSIS = "doc_analysis"
    SUMMARIZATION = "summarization"


class LLMModelTier(str, Enum):
    """Tiers de modèles (pour pricing)"""
    FREE = "free"          # Modèles gratuits (Groq free tier)
    BASIC = "basic"        # GPT-4o-mini, Claude Haiku
    STANDARD = "standard"  # GPT-4o, Claude Sonnet
    PREMIUM = "premium"    # Claude Opus, GPT-4 Turbo
    ULTRA = "ultra"        # O1, modèles spécialisés


# ============================================
# SQLAlchemy-style Models (In-Memory pour MVP)
# ============================================

class AIProvider(BaseModel):
    """Provider IA (OpenAI, Anthropic, etc.)"""
    id: str = Field(default_factory=lambda: f"prov_{uuid.uuid4().hex[:8]}")
    name: str
    type: LLMProviderType
    base_url: Optional[str] = None
    api_key_env_var: str  # Nom de la variable d'env (jamais la clé elle-même!)
    is_active: bool = True
    supports_streaming: bool = True
    rate_limit_rpm: int = 60  # Requêtes par minute
    rate_limit_tpm: int = 100000  # Tokens par minute
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class AIModel(BaseModel):
    """Modèle IA disponible"""
    id: str = Field(default_factory=lambda: f"model_{uuid.uuid4().hex[:8]}")
    provider_id: str
    code: str  # Ex: "openai.gpt-4o", "anthropic.claude-3-5-sonnet"
    display_name: str
    type: LLMModelType = LLMModelType.CHAT
    tier: LLMModelTier = LLMModelTier.STANDARD
    
    # Coûts (en USD pour calcul interne)
    cost_usd_input_per_1k: Decimal = Decimal("0.01")  # $/1K tokens input
    cost_usd_output_per_1k: Decimal = Decimal("0.03")  # $/1K tokens output
    
    # Prix IAFactory (en crédits)
    cost_credits_per_1k: int = 1  # Crédits IAFactory par 1K tokens
    
    # Limites
    max_tokens: int = 4096
    context_window: int = 128000
    supports_vision: bool = False
    supports_tools: bool = True
    supports_streaming: bool = True
    
    # Status
    is_active: bool = True
    is_default: bool = False
    
    # Metadata
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class AIUsageLog(BaseModel):
    """Log d'utilisation d'un modèle IA"""
    id: str = Field(default_factory=lambda: f"usage_{uuid.uuid4().hex[:12]}")
    user_id: str
    model_id: str
    model_code: str
    
    # Tokens
    tokens_input: int
    tokens_output: int
    tokens_total: int
    
    # Coûts
    credits_consumed: int
    cost_usd_estimated: Decimal
    
    # Request info
    request_type: str = "chat"  # chat, completion, embedding
    success: bool = True
    error_message: Optional[str] = None
    latency_ms: int = 0
    
    # Metadata
    metadata: dict[str, Any] = Field(default_factory=dict)
    ip_address: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.now)


# ============================================
# API Request/Response Models
# ============================================

class ChatMessage(BaseModel):
    """Message dans une conversation"""
    role: str  # "user", "assistant", "system"
    content: str
    name: Optional[str] = None


class ChatRequest(BaseModel):
    """Requête de chat"""
    model: str  # Ex: "openai.gpt-4o", "groq.llama-3.1-70b"
    messages: List[ChatMessage]
    
    # Options
    temperature: float = Field(default=0.7, ge=0, le=2)
    max_tokens: Optional[int] = None
    stream: bool = False
    
    # Metadata
    session_id: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ChatResponse(BaseModel):
    """Réponse de chat"""
    success: bool
    request_id: str = Field(default_factory=lambda: f"req_{uuid.uuid4().hex[:12]}")
    
    # Réponse
    answer: str
    model: str
    model_display_name: str
    
    # Usage
    tokens_input: int
    tokens_output: int
    tokens_total: int
    
    # Crédits
    credits_used: int
    credits_remaining: int
    cost_usd_estimated: float
    
    # Performance
    latency_ms: int
    
    # Metadata
    finish_reason: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class LLMModelInfo(BaseModel):
    """Info publique sur un modèle"""
    code: str
    display_name: str
    provider: LLMProviderType
    type: LLMModelType
    tier: LLMModelTier
    
    # Prix en crédits IAFactory
    cost_credits_per_1k: int
    
    # Capacités
    max_tokens: int
    context_window: int
    supports_vision: bool
    supports_tools: bool
    supports_streaming: bool
    
    is_default: bool
    description: Optional[str] = None


class ModelsListResponse(BaseModel):
    """Liste des modèles disponibles"""
    success: bool
    models: List[LLMModelInfo]
    total: int
    default_model: Optional[str] = None


class UsageHistoryItem(BaseModel):
    """Item d'historique d'usage"""
    id: str
    model_code: str
    model_display_name: str
    tokens_input: int
    tokens_output: int
    credits_consumed: int
    cost_usd: float
    success: bool
    latency_ms: int
    created_at: datetime


class UsageHistoryResponse(BaseModel):
    """Historique d'usage"""
    success: bool
    user_id: str
    items: List[UsageHistoryItem]
    total_items: int
    total_credits_used: int
    total_cost_usd: float
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None


class UsageSummaryResponse(BaseModel):
    """Résumé d'usage"""
    success: bool
    user_id: str
    
    # Totaux
    total_requests: int
    total_tokens: int
    total_credits: int
    total_cost_usd: float
    
    # Par modèle
    usage_by_model: dict[str, dict]  # {model_code: {requests, tokens, credits}}
    
    # Par jour (7 derniers jours)
    daily_usage: List[dict]  # [{date, requests, tokens, credits}]
    
    # Période
    period: str  # "7d", "30d", "all"
    generated_at: datetime = Field(default_factory=datetime.now)


# ============================================
# Predefined Providers & Models
# ============================================

DEFAULT_PROVIDERS: dict[LLMProviderType, AIProvider] = {
    # === CHAT LLM ===
    LLMProviderType.OPENAI: AIProvider(
        id="prov_openai",
        name="OpenAI",
        type=LLMProviderType.OPENAI,
        base_url="https://api.openai.com/v1",
        api_key_env_var="OPENAI_API_KEY",
        rate_limit_rpm=500,
        rate_limit_tpm=200000,
    ),
    LLMProviderType.ANTHROPIC: AIProvider(
        id="prov_anthropic",
        name="Anthropic",
        type=LLMProviderType.ANTHROPIC,
        base_url="https://api.anthropic.com/v1",
        api_key_env_var="ANTHROPIC_API_KEY",
        rate_limit_rpm=50,
        rate_limit_tpm=100000,
    ),
    LLMProviderType.GROQ: AIProvider(
        id="prov_groq",
        name="Groq",
        type=LLMProviderType.GROQ,
        base_url="https://api.groq.com/openai/v1",
        api_key_env_var="GROQ_API_KEY",
        rate_limit_rpm=30,
        rate_limit_tpm=15000,
    ),
    LLMProviderType.GOOGLE: AIProvider(
        id="prov_google",
        name="Google AI",
        type=LLMProviderType.GOOGLE,
        base_url="https://generativelanguage.googleapis.com/v1beta",
        api_key_env_var="GOOGLE_API_KEY",
        rate_limit_rpm=60,
        rate_limit_tpm=100000,
    ),
    LLMProviderType.OPENROUTER: AIProvider(
        id="prov_openrouter",
        name="OpenRouter",
        type=LLMProviderType.OPENROUTER,
        base_url="https://openrouter.ai/api/v1",
        api_key_env_var="OPENROUTER_API_KEY",
        rate_limit_rpm=200,
        rate_limit_tpm=500000,
    ),
    LLMProviderType.MISTRAL: AIProvider(
        id="prov_mistral",
        name="Mistral AI",
        type=LLMProviderType.MISTRAL,
        base_url="https://api.mistral.ai/v1",
        api_key_env_var="MISTRAL_API_KEY",
        rate_limit_rpm=120,
        rate_limit_tpm=100000,
    ),
    
    # === IMAGE GENERATION ===
    LLMProviderType.DALLE: AIProvider(
        id="prov_dalle",
        name="DALL-E (OpenAI)",
        type=LLMProviderType.DALLE,
        base_url="https://api.openai.com/v1",
        api_key_env_var="OPENAI_API_KEY",
        rate_limit_rpm=50,
        rate_limit_tpm=0,
    ),
    LLMProviderType.STABILITY: AIProvider(
        id="prov_stability",
        name="Stability AI",
        type=LLMProviderType.STABILITY,
        base_url="https://api.stability.ai/v2beta",
        api_key_env_var="STABILITY_API_KEY",
        rate_limit_rpm=150,
        rate_limit_tpm=0,
    ),
    LLMProviderType.FLUX: AIProvider(
        id="prov_flux",
        name="Flux (Black Forest Labs)",
        type=LLMProviderType.FLUX,
        base_url="https://api.replicate.com/v1",
        api_key_env_var="REPLICATE_API_KEY",
        rate_limit_rpm=60,
        rate_limit_tpm=0,
    ),
    LLMProviderType.IDEOGRAM: AIProvider(
        id="prov_ideogram",
        name="Ideogram",
        type=LLMProviderType.IDEOGRAM,
        base_url="https://api.ideogram.ai/v1",
        api_key_env_var="IDEOGRAM_API_KEY",
        rate_limit_rpm=60,
        rate_limit_tpm=0,
    ),
    LLMProviderType.LEONARDO: AIProvider(
        id="prov_leonardo",
        name="Leonardo.ai",
        type=LLMProviderType.LEONARDO,
        base_url="https://cloud.leonardo.ai/api/rest/v1",
        api_key_env_var="LEONARDO_API_KEY",
        rate_limit_rpm=60,
        rate_limit_tpm=0,
    ),
    
    # === VIDEO GENERATION ===
    LLMProviderType.RUNWAY: AIProvider(
        id="prov_runway",
        name="Runway",
        type=LLMProviderType.RUNWAY,
        base_url="https://api.runwayml.com/v1",
        api_key_env_var="RUNWAY_API_KEY",
        rate_limit_rpm=10,
        rate_limit_tpm=0,
    ),
    LLMProviderType.PIKA: AIProvider(
        id="prov_pika",
        name="Pika Labs",
        type=LLMProviderType.PIKA,
        base_url="https://api.pika.art/v1",
        api_key_env_var="PIKA_API_KEY",
        rate_limit_rpm=20,
        rate_limit_tpm=0,
    ),
    LLMProviderType.KLING: AIProvider(
        id="prov_kling",
        name="Kling AI",
        type=LLMProviderType.KLING,
        base_url="https://api.klingai.com/v1",
        api_key_env_var="KLING_API_KEY",
        rate_limit_rpm=10,
        rate_limit_tpm=0,
    ),
    LLMProviderType.LUMA: AIProvider(
        id="prov_luma",
        name="Luma AI",
        type=LLMProviderType.LUMA,
        base_url="https://api.lumalabs.ai/v1",
        api_key_env_var="LUMA_API_KEY",
        rate_limit_rpm=20,
        rate_limit_tpm=0,
    ),
    LLMProviderType.HEYGEN: AIProvider(
        id="prov_heygen",
        name="HeyGen",
        type=LLMProviderType.HEYGEN,
        base_url="https://api.heygen.com/v2",
        api_key_env_var="HEYGEN_API_KEY",
        rate_limit_rpm=20,
        rate_limit_tpm=0,
    ),
    LLMProviderType.SYNTHESIA: AIProvider(
        id="prov_synthesia",
        name="Synthesia",
        type=LLMProviderType.SYNTHESIA,
        base_url="https://api.synthesia.io/v2",
        api_key_env_var="SYNTHESIA_API_KEY",
        rate_limit_rpm=10,
        rate_limit_tpm=0,
    ),
    
    # === AUDIO/VOICE ===
    LLMProviderType.ELEVENLABS: AIProvider(
        id="prov_elevenlabs",
        name="ElevenLabs",
        type=LLMProviderType.ELEVENLABS,
        base_url="https://api.elevenlabs.io/v1",
        api_key_env_var="ELEVENLABS_API_KEY",
        rate_limit_rpm=100,
        rate_limit_tpm=0,
    ),
    LLMProviderType.PLAY_HT: AIProvider(
        id="prov_play_ht",
        name="Play.ht",
        type=LLMProviderType.PLAY_HT,
        base_url="https://api.play.ht/api/v2",
        api_key_env_var="PLAYHT_API_KEY",
        rate_limit_rpm=60,
        rate_limit_tpm=0,
    ),
    
    # === MUSIC ===
    LLMProviderType.SUNO: AIProvider(
        id="prov_suno",
        name="Suno AI",
        type=LLMProviderType.SUNO,
        base_url="https://api.suno.ai/v1",
        api_key_env_var="SUNO_API_KEY",
        rate_limit_rpm=10,
        rate_limit_tpm=0,
    ),
    LLMProviderType.UDIO: AIProvider(
        id="prov_udio",
        name="Udio",
        type=LLMProviderType.UDIO,
        base_url="https://api.udio.com/v1",
        api_key_env_var="UDIO_API_KEY",
        rate_limit_rpm=10,
        rate_limit_tpm=0,
    ),
    
    # === PRESENTATIONS ===
    LLMProviderType.GAMMA: AIProvider(
        id="prov_gamma",
        name="Gamma",
        type=LLMProviderType.GAMMA,
        base_url="https://api.gamma.app/v1",
        api_key_env_var="GAMMA_API_KEY",
        rate_limit_rpm=30,
        rate_limit_tpm=0,
    ),
    LLMProviderType.BEAUTIFUL_AI: AIProvider(
        id="prov_beautiful_ai",
        name="Beautiful.ai",
        type=LLMProviderType.BEAUTIFUL_AI,
        base_url="https://api.beautiful.ai/v1",
        api_key_env_var="BEAUTIFULAI_API_KEY",
        rate_limit_rpm=20,
        rate_limit_tpm=0,
    ),
    LLMProviderType.TOME: AIProvider(
        id="prov_tome",
        name="Tome",
        type=LLMProviderType.TOME,
        base_url="https://api.tome.app/v1",
        api_key_env_var="TOME_API_KEY",
        rate_limit_rpm=30,
        rate_limit_tpm=0,
    ),
    
    # === CODE ===
    LLMProviderType.GITHUB_COPILOT: AIProvider(
        id="prov_github_copilot",
        name="GitHub Copilot",
        type=LLMProviderType.GITHUB_COPILOT,
        base_url="https://api.github.com/copilot",
        api_key_env_var="GITHUB_TOKEN",
        rate_limit_rpm=100,
        rate_limit_tpm=0,
    ),
    LLMProviderType.CURSOR: AIProvider(
        id="prov_cursor",
        name="Cursor",
        type=LLMProviderType.CURSOR,
        base_url="https://api.cursor.com/v1",
        api_key_env_var="CURSOR_API_KEY",
        rate_limit_rpm=60,
        rate_limit_tpm=0,
    ),
    LLMProviderType.REPLIT: AIProvider(
        id="prov_replit",
        name="Replit",
        type=LLMProviderType.REPLIT,
        base_url="https://api.replit.com/v1",
        api_key_env_var="REPLIT_API_KEY",
        rate_limit_rpm=60,
        rate_limit_tpm=0,
    ),
}

# Modèles prédéfinis avec pricing IAFactory
DEFAULT_MODELS: List[AIModel] = [
    # === OpenAI ===
    AIModel(
        id="model_gpt4o",
        provider_id="prov_openai",
        code="openai.gpt-4o",
        display_name="GPT-4o",
        tier=LLMModelTier.STANDARD,
        cost_usd_input_per_1k=Decimal("0.005"),
        cost_usd_output_per_1k=Decimal("0.015"),
        cost_credits_per_1k=2,
        max_tokens=16384,
        context_window=128000,
        supports_vision=True,
        is_default=True,
        description="Modèle phare OpenAI, rapide et intelligent",
    ),
    AIModel(
        id="model_gpt4omini",
        provider_id="prov_openai",
        code="openai.gpt-4o-mini",
        display_name="GPT-4o Mini",
        tier=LLMModelTier.BASIC,
        cost_usd_input_per_1k=Decimal("0.00015"),
        cost_usd_output_per_1k=Decimal("0.0006"),
        cost_credits_per_1k=1,
        max_tokens=16384,
        context_window=128000,
        supports_vision=True,
        description="Économique et efficace pour tâches courantes",
    ),
    AIModel(
        id="model_o1",
        provider_id="prov_openai",
        code="openai.o1-preview",
        display_name="O1 Preview",
        tier=LLMModelTier.ULTRA,
        cost_usd_input_per_1k=Decimal("0.015"),
        cost_usd_output_per_1k=Decimal("0.060"),
        cost_credits_per_1k=5,
        max_tokens=32768,
        context_window=128000,
        supports_tools=False,
        description="Raisonnement avancé pour problèmes complexes",
    ),
    
    # === Anthropic ===
    AIModel(
        id="model_claude35sonnet",
        provider_id="prov_anthropic",
        code="anthropic.claude-3-5-sonnet",
        display_name="Claude 3.5 Sonnet",
        tier=LLMModelTier.STANDARD,
        cost_usd_input_per_1k=Decimal("0.003"),
        cost_usd_output_per_1k=Decimal("0.015"),
        cost_credits_per_1k=2,
        max_tokens=8192,
        context_window=200000,
        supports_vision=True,
        description="Excellent équilibre performance/coût",
    ),
    AIModel(
        id="model_claude3haiku",
        provider_id="prov_anthropic",
        code="anthropic.claude-3-haiku",
        display_name="Claude 3 Haiku",
        tier=LLMModelTier.BASIC,
        cost_usd_input_per_1k=Decimal("0.00025"),
        cost_usd_output_per_1k=Decimal("0.00125"),
        cost_credits_per_1k=1,
        max_tokens=4096,
        context_window=200000,
        supports_vision=True,
        description="Ultra-rapide et économique",
    ),
    AIModel(
        id="model_claudeopus",
        provider_id="prov_anthropic",
        code="anthropic.claude-3-opus",
        display_name="Claude 3 Opus",
        tier=LLMModelTier.PREMIUM,
        cost_usd_input_per_1k=Decimal("0.015"),
        cost_usd_output_per_1k=Decimal("0.075"),
        cost_credits_per_1k=4,
        max_tokens=4096,
        context_window=200000,
        supports_vision=True,
        description="Le plus puissant de Claude",
    ),
    
    # === Groq (Fast & Free tier) ===
    AIModel(
        id="model_llama31_70b",
        provider_id="prov_groq",
        code="groq.llama-3.1-70b",
        display_name="Llama 3.1 70B (Groq)",
        tier=LLMModelTier.FREE,
        cost_usd_input_per_1k=Decimal("0.0005"),
        cost_usd_output_per_1k=Decimal("0.0008"),
        cost_credits_per_1k=1,
        max_tokens=8000,
        context_window=131072,
        description="Open-source, ultra-rapide via Groq",
    ),
    AIModel(
        id="model_llama31_8b",
        provider_id="prov_groq",
        code="groq.llama-3.1-8b",
        display_name="Llama 3.1 8B (Groq)",
        tier=LLMModelTier.FREE,
        cost_usd_input_per_1k=Decimal("0.00005"),
        cost_usd_output_per_1k=Decimal("0.00008"),
        cost_credits_per_1k=1,
        max_tokens=8000,
        context_window=131072,
        description="Petit, rapide, idéal pour tests",
    ),
    AIModel(
        id="model_mixtral",
        provider_id="prov_groq",
        code="groq.mixtral-8x7b",
        display_name="Mixtral 8x7B (Groq)",
        tier=LLMModelTier.FREE,
        cost_usd_input_per_1k=Decimal("0.00027"),
        cost_usd_output_per_1k=Decimal("0.00027"),
        cost_credits_per_1k=1,
        max_tokens=32768,
        context_window=32768,
        description="Mixture of Experts, bon rapport qualité/prix",
    ),
    
    # === Google ===
    AIModel(
        id="model_gemini15pro",
        provider_id="prov_google",
        code="google.gemini-1.5-pro",
        display_name="Gemini 1.5 Pro",
        tier=LLMModelTier.STANDARD,
        cost_usd_input_per_1k=Decimal("0.00125"),
        cost_usd_output_per_1k=Decimal("0.005"),
        cost_credits_per_1k=2,
        max_tokens=8192,
        context_window=1000000,  # 1M tokens!
        supports_vision=True,
        description="Contexte massif, multimodal",
    ),
    AIModel(
        id="model_gemini15flash",
        provider_id="prov_google",
        code="google.gemini-1.5-flash",
        display_name="Gemini 1.5 Flash",
        tier=LLMModelTier.BASIC,
        cost_usd_input_per_1k=Decimal("0.000075"),
        cost_usd_output_per_1k=Decimal("0.0003"),
        cost_credits_per_1k=1,
        max_tokens=8192,
        context_window=1000000,
        supports_vision=True,
        description="Ultra économique avec grand contexte",
    ),
    
    # === Mistral ===
    AIModel(
        id="model_mistral_large",
        provider_id="prov_mistral",
        code="mistral.mistral-large",
        display_name="Mistral Large",
        tier=LLMModelTier.STANDARD,
        cost_usd_input_per_1k=Decimal("0.002"),
        cost_usd_output_per_1k=Decimal("0.006"),
        cost_credits_per_1k=2,
        max_tokens=32768,
        context_window=128000,
        description="Flagship Mistral, excellent en français",
    ),
    AIModel(
        id="model_mistral_small",
        provider_id="prov_mistral",
        code="mistral.mistral-small",
        display_name="Mistral Small",
        tier=LLMModelTier.BASIC,
        cost_usd_input_per_1k=Decimal("0.0002"),
        cost_usd_output_per_1k=Decimal("0.0006"),
        cost_credits_per_1k=1,
        max_tokens=32768,
        context_window=128000,
        description="Rapide et économique",
    ),
    
    # ============================================
    # 🎨 IMAGE GENERATION
    # ============================================
    
    # DALL-E 3
    AIModel(
        id="model_dalle3",
        provider_id="prov_openai",
        code="openai.dalle-3",
        display_name="DALL-E 3",
        type=LLMModelType.IMAGE_GEN,
        tier=LLMModelTier.STANDARD,
        cost_usd_input_per_1k=Decimal("0"),
        cost_usd_output_per_1k=Decimal("40"),  # ~$0.04/image standard
        cost_credits_per_1k=40,  # ~4 crédits/image
        max_tokens=1,
        context_window=4000,
        description="Génération d'images HD par OpenAI (1024x1024)",
    ),
    AIModel(
        id="model_dalle3_hd",
        provider_id="prov_openai",
        code="openai.dalle-3-hd",
        display_name="DALL-E 3 HD",
        type=LLMModelType.IMAGE_GEN,
        tier=LLMModelTier.PREMIUM,
        cost_usd_input_per_1k=Decimal("0"),
        cost_usd_output_per_1k=Decimal("80"),  # ~$0.08/image HD
        cost_credits_per_1k=80,  # ~8 crédits/image
        max_tokens=1,
        context_window=4000,
        description="DALL-E 3 qualité HD (1792x1024)",
    ),
    
    # Stable Diffusion (Stability AI)
    AIModel(
        id="model_sdxl",
        provider_id="prov_stability",
        code="stability.sdxl",
        display_name="Stable Diffusion XL",
        type=LLMModelType.IMAGE_GEN,
        tier=LLMModelTier.BASIC,
        cost_usd_input_per_1k=Decimal("0"),
        cost_usd_output_per_1k=Decimal("2"),  # ~$0.002/image
        cost_credits_per_1k=2,
        max_tokens=1,
        context_window=77,  # 77 tokens max prompt
        description="Open-source, très économique",
    ),
    AIModel(
        id="model_sd3",
        provider_id="prov_stability",
        code="stability.sd3",
        display_name="Stable Diffusion 3",
        type=LLMModelType.IMAGE_GEN,
        tier=LLMModelTier.STANDARD,
        cost_usd_input_per_1k=Decimal("0"),
        cost_usd_output_per_1k=Decimal("35"),  # ~$0.035/image
        cost_credits_per_1k=35,
        max_tokens=1,
        context_window=256,
        description="SD3 avec meilleure compréhension de texte",
    ),
    
    # Flux (Black Forest Labs)
    AIModel(
        id="model_flux_schnell",
        provider_id="prov_flux",
        code="flux.schnell",
        display_name="Flux Schnell",
        type=LLMModelType.IMAGE_GEN,
        tier=LLMModelTier.FREE,
        cost_usd_input_per_1k=Decimal("0"),
        cost_usd_output_per_1k=Decimal("0"),  # Gratuit
        cost_credits_per_1k=1,
        max_tokens=1,
        context_window=256,
        description="Flux rapide, gratuit via Replicate",
    ),
    AIModel(
        id="model_flux_pro",
        provider_id="prov_flux",
        code="flux.pro",
        display_name="Flux Pro",
        type=LLMModelType.IMAGE_GEN,
        tier=LLMModelTier.PREMIUM,
        cost_usd_input_per_1k=Decimal("0"),
        cost_usd_output_per_1k=Decimal("55"),  # ~$0.055/image
        cost_credits_per_1k=55,
        max_tokens=1,
        context_window=256,
        description="Meilleure qualité Flux",
    ),
    
    # Ideogram
    AIModel(
        id="model_ideogram",
        provider_id="prov_ideogram",
        code="ideogram.v2",
        display_name="Ideogram V2",
        type=LLMModelType.IMAGE_GEN,
        tier=LLMModelTier.STANDARD,
        cost_usd_input_per_1k=Decimal("0"),
        cost_usd_output_per_1k=Decimal("40"),
        cost_credits_per_1k=40,
        max_tokens=1,
        context_window=1024,
        description="Excellent pour texte dans images",
    ),
    
    # Leonardo
    AIModel(
        id="model_leonardo",
        provider_id="prov_leonardo",
        code="leonardo.phoenix",
        display_name="Leonardo Phoenix",
        type=LLMModelType.IMAGE_GEN,
        tier=LLMModelTier.STANDARD,
        cost_usd_input_per_1k=Decimal("0"),
        cost_usd_output_per_1k=Decimal("30"),
        cost_credits_per_1k=30,
        max_tokens=1,
        context_window=512,
        description="Créatif, bon pour concept art",
    ),
    
    # ============================================
    # 🎬 VIDEO GENERATION
    # ============================================
    
    # Runway
    AIModel(
        id="model_runway_gen3",
        provider_id="prov_runway",
        code="runway.gen3-alpha",
        display_name="Runway Gen-3 Alpha",
        type=LLMModelType.VIDEO_GEN,
        tier=LLMModelTier.PREMIUM,
        cost_usd_input_per_1k=Decimal("0"),
        cost_usd_output_per_1k=Decimal("500"),  # ~$0.50/sec
        cost_credits_per_1k=500,  # 50 crédits/5sec
        max_tokens=10,  # 10 secondes max
        context_window=512,
        description="Vidéo text-to-video haute qualité (5-10s)",
    ),
    
    # Pika
    AIModel(
        id="model_pika",
        provider_id="prov_pika",
        code="pika.v1.5",
        display_name="Pika 1.5",
        type=LLMModelType.VIDEO_GEN,
        tier=LLMModelTier.STANDARD,
        cost_usd_input_per_1k=Decimal("0"),
        cost_usd_output_per_1k=Decimal("200"),
        cost_credits_per_1k=200,
        max_tokens=4,  # 4 secondes
        context_window=512,
        description="Vidéo stylisée, effets créatifs",
    ),
    
    # Kling
    AIModel(
        id="model_kling",
        provider_id="prov_kling",
        code="kling.v1.5",
        display_name="Kling AI 1.5",
        type=LLMModelType.VIDEO_GEN,
        tier=LLMModelTier.PREMIUM,
        cost_usd_input_per_1k=Decimal("0"),
        cost_usd_output_per_1k=Decimal("300"),
        cost_credits_per_1k=300,
        max_tokens=10,
        context_window=512,
        description="Vidéo longue durée, mouvements réalistes",
    ),
    
    # Luma
    AIModel(
        id="model_luma",
        provider_id="prov_luma",
        code="luma.dream-machine",
        display_name="Luma Dream Machine",
        type=LLMModelType.VIDEO_GEN,
        tier=LLMModelTier.STANDARD,
        cost_usd_input_per_1k=Decimal("0"),
        cost_usd_output_per_1k=Decimal("250"),
        cost_credits_per_1k=250,
        max_tokens=5,
        context_window=512,
        description="Vidéo rapide et créative",
    ),
    
    # HeyGen (Avatars)
    AIModel(
        id="model_heygen",
        provider_id="prov_heygen",
        code="heygen.avatar",
        display_name="HeyGen Avatar",
        type=LLMModelType.VIDEO_AVATAR,
        tier=LLMModelTier.PREMIUM,
        cost_usd_input_per_1k=Decimal("0"),
        cost_usd_output_per_1k=Decimal("100"),  # ~$0.10/sec
        cost_credits_per_1k=100,
        max_tokens=300,  # 5 minutes max
        context_window=5000,
        description="Avatars IA parlants professionnels",
    ),
    
    # Synthesia
    AIModel(
        id="model_synthesia",
        provider_id="prov_synthesia",
        code="synthesia.avatar",
        display_name="Synthesia Avatar",
        type=LLMModelType.VIDEO_AVATAR,
        tier=LLMModelTier.PREMIUM,
        cost_usd_input_per_1k=Decimal("0"),
        cost_usd_output_per_1k=Decimal("120"),
        cost_credits_per_1k=120,
        max_tokens=300,
        context_window=5000,
        description="Avatars corporate, 120+ langues",
    ),
    
    # ============================================
    # 🎙️ VOICE / AUDIO
    # ============================================
    
    # ElevenLabs
    AIModel(
        id="model_elevenlabs",
        provider_id="prov_elevenlabs",
        code="elevenlabs.multilingual-v2",
        display_name="ElevenLabs V2",
        type=LLMModelType.TTS,
        tier=LLMModelTier.STANDARD,
        cost_usd_input_per_1k=Decimal("0.18"),  # $0.18/1K chars
        cost_usd_output_per_1k=Decimal("0"),
        cost_credits_per_1k=2,
        max_tokens=5000,
        context_window=5000,
        description="TTS le plus naturel, 29 langues",
    ),
    AIModel(
        id="model_elevenlabs_turbo",
        provider_id="prov_elevenlabs",
        code="elevenlabs.turbo-v2.5",
        display_name="ElevenLabs Turbo",
        type=LLMModelType.TTS,
        tier=LLMModelTier.BASIC,
        cost_usd_input_per_1k=Decimal("0.11"),
        cost_usd_output_per_1k=Decimal("0"),
        cost_credits_per_1k=1,
        max_tokens=5000,
        context_window=5000,
        description="TTS rapide et économique",
    ),
    AIModel(
        id="model_elevenlabs_clone",
        provider_id="prov_elevenlabs",
        code="elevenlabs.voice-clone",
        display_name="ElevenLabs Voice Clone",
        type=LLMModelType.VOICE_CLONE,
        tier=LLMModelTier.PREMIUM,
        cost_usd_input_per_1k=Decimal("0"),
        cost_usd_output_per_1k=Decimal("0"),  # Inclus dans abo
        cost_credits_per_1k=10,
        max_tokens=1,
        context_window=1,
        description="Clonage de voix (30sec d'audio)",
    ),
    
    # OpenAI Audio
    AIModel(
        id="model_openai_tts",
        provider_id="prov_openai",
        code="openai.tts-1-hd",
        display_name="OpenAI TTS HD",
        type=LLMModelType.TTS,
        tier=LLMModelTier.BASIC,
        cost_usd_input_per_1k=Decimal("0.030"),  # $30/1M chars
        cost_usd_output_per_1k=Decimal("0"),
        cost_credits_per_1k=1,
        max_tokens=4096,
        context_window=4096,
        description="TTS OpenAI, 6 voix",
    ),
    AIModel(
        id="model_openai_whisper",
        provider_id="prov_openai",
        code="openai.whisper-1",
        display_name="OpenAI Whisper",
        type=LLMModelType.STT,
        tier=LLMModelTier.BASIC,
        cost_usd_input_per_1k=Decimal("0.006"),  # $0.006/min
        cost_usd_output_per_1k=Decimal("0"),
        cost_credits_per_1k=1,
        max_tokens=25,  # 25 min max
        context_window=25,
        description="STT précis, 50+ langues",
    ),
    
    # Play.ht
    AIModel(
        id="model_playht",
        provider_id="prov_play_ht",
        code="play_ht.play3",
        display_name="Play.ht Play3",
        type=LLMModelType.TTS,
        tier=LLMModelTier.STANDARD,
        cost_usd_input_per_1k=Decimal("0.15"),
        cost_usd_output_per_1k=Decimal("0"),
        cost_credits_per_1k=2,
        max_tokens=5000,
        context_window=5000,
        description="TTS expressif avec émotions",
    ),
    
    # ============================================
    # 🎵 MUSIC GENERATION
    # ============================================
    
    # Suno
    AIModel(
        id="model_suno",
        provider_id="prov_suno",
        code="suno.v3.5",
        display_name="Suno V3.5",
        type=LLMModelType.MUSIC_GEN,
        tier=LLMModelTier.STANDARD,
        cost_usd_input_per_1k=Decimal("0"),
        cost_usd_output_per_1k=Decimal("50"),  # ~5 crédits Suno/chanson
        cost_credits_per_1k=50,
        max_tokens=240,  # 4 minutes max
        context_window=500,
        description="Musique + paroles, tous styles",
    ),
    
    # Udio
    AIModel(
        id="model_udio",
        provider_id="prov_udio",
        code="udio.v1.5",
        display_name="Udio 1.5",
        type=LLMModelType.MUSIC_GEN,
        tier=LLMModelTier.STANDARD,
        cost_usd_input_per_1k=Decimal("0"),
        cost_usd_output_per_1k=Decimal("40"),
        cost_credits_per_1k=40,
        max_tokens=300,  # 5 minutes
        context_window=500,
        description="Musique haute qualité, remix",
    ),
    
    # ============================================
    # 📊 PRESENTATIONS
    # ============================================
    
    # Gamma
    AIModel(
        id="model_gamma",
        provider_id="prov_gamma",
        code="gamma.presentation",
        display_name="Gamma AI",
        type=LLMModelType.PRESENTATION,
        tier=LLMModelTier.STANDARD,
        cost_usd_input_per_1k=Decimal("0"),
        cost_usd_output_per_1k=Decimal("10"),  # ~1 crédit/slide
        cost_credits_per_1k=10,
        max_tokens=50,  # 50 slides max
        context_window=10000,
        description="Présentations IA en 1 clic",
    ),
    
    # Beautiful.ai
    AIModel(
        id="model_beautiful_ai",
        provider_id="prov_beautiful_ai",
        code="beautiful_ai.designer",
        display_name="Beautiful.ai",
        type=LLMModelType.PRESENTATION,
        tier=LLMModelTier.PREMIUM,
        cost_usd_input_per_1k=Decimal("0"),
        cost_usd_output_per_1k=Decimal("50"),
        cost_credits_per_1k=50,
        max_tokens=100,
        context_window=10000,
        description="Design pro automatique",
    ),
    
    # Tome
    AIModel(
        id="model_tome",
        provider_id="prov_tome",
        code="tome.narrative",
        display_name="Tome",
        type=LLMModelType.PRESENTATION,
        tier=LLMModelTier.STANDARD,
        cost_usd_input_per_1k=Decimal("0"),
        cost_usd_output_per_1k=Decimal("15"),
        cost_credits_per_1k=15,
        max_tokens=30,
        context_window=8000,
        description="Storytelling visuel interactif",
    ),
    
    # ============================================
    # 💻 CODE ASSISTANTS
    # ============================================
    
    # GitHub Copilot (via seats)
    AIModel(
        id="model_copilot",
        provider_id="prov_github_copilot",
        code="github_copilot.copilot",
        display_name="GitHub Copilot",
        type=LLMModelType.CODE_GEN,
        tier=LLMModelTier.STANDARD,
        cost_usd_input_per_1k=Decimal("0"),
        cost_usd_output_per_1k=Decimal("0"),  # Abonnement
        cost_credits_per_1k=0,  # Géré via Team Seats
        max_tokens=8000,
        context_window=8000,
        description="Complétion code multi-IDE (via Seat)",
    ),
    
    # Cursor
    AIModel(
        id="model_cursor",
        provider_id="prov_cursor",
        code="cursor.ai",
        display_name="Cursor AI",
        type=LLMModelType.CODE_GEN,
        tier=LLMModelTier.PREMIUM,
        cost_usd_input_per_1k=Decimal("0"),
        cost_usd_output_per_1k=Decimal("0"),  # Abonnement
        cost_credits_per_1k=0,  # Géré via Team Seats
        max_tokens=16000,
        context_window=100000,
        description="IDE IA complet (via Seat)",
    ),
    
    # Replit
    AIModel(
        id="model_replit",
        provider_id="prov_replit",
        code="replit.ghostwriter",
        display_name="Replit Ghostwriter",
        type=LLMModelType.CODE_GEN,
        tier=LLMModelTier.STANDARD,
        cost_usd_input_per_1k=Decimal("0"),
        cost_usd_output_per_1k=Decimal("0"),
        cost_credits_per_1k=0,
        max_tokens=8000,
        context_window=32000,
        description="Code + déploiement cloud",
    ),
]

# Index par code pour accès rapide
MODELS_BY_CODE: dict[str, AIModel] = {m.code: m for m in DEFAULT_MODELS}
