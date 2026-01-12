"""
VOICE MODULE - Speech Processing
================================
Module voix complet pour iaFactoryDZ

Composants:
- STT_VOICE: Speech-to-Text (audio → texte)
- TTS_VOICE: Text-to-Speech (texte → audio)
- VOICE_AGENT: Agent vocal complet (STT → NLP → RAG → LLM → TTS)

STT Features:
- Transcription Whisper (OpenAI API ou local)
- Détection automatique langue
- Nettoyage texte via DARIJA_NLP
- Normalisation darija
- Conversion arabizi → arabe

TTS Features:
- Synthèse vocale multi-backend (mock/openai/elevenlabs/coqui)
- Support arabe/darija/français/anglais
- Normalisation texte avant synthèse
- Multiple voix et émotions

VOICE_AGENT Features:
- Pipeline vocal complet
- Gestion des conversations
- Détection d'intentions
- Intégration RAG documentaire
- Génération LLM contextualisée

Langues supportées:
- ar: Arabe (MSA + dialectes)
- ar-dz: Arabe algérien (darija)
- fr: Français
- en: Anglais

Endpoints STT:
- GET  /api/voice/stt/health     - Health check
- POST /api/voice/stt/transcribe - Transcription complète
- POST /api/voice/stt/quick      - Transcription rapide

Endpoints TTS:
- GET  /api/voice/tts/health     - Health check
- POST /api/voice/tts/synthesize - Synthèse complète
- POST /api/voice/tts/simple     - Synthèse rapide
- GET  /api/voice/tts/voices     - Voix disponibles

Endpoints VOICE_AGENT:
- GET  /api/agent/voice/health   - Health check
- POST /api/agent/voice/chat     - Pipeline complet
- POST /api/agent/voice/text     - Chat texte
- POST /api/agent/voice/audio    - Chat audio
- GET  /api/agent/voice/info     - Informations agent
"""

# ============================================
# STT IMPORTS
# ============================================

from .stt_models import (
    # Enums
    STTLanguage,
    STTDialect,
    STTBackend,
    STTModel,
    AudioFormat as STTAudioFormat,
    # Request models
    STTRequest,
    STTQuickRequest,
    # Response models
    STTResponse,
    STTSegment,
    DarijaNormResult,
    STTBatchItem,
    STTBatchResponse,
    # Status models
    STTStatus,
    STTModelInfo,
    STTError,
    # Constants
    SUPPORTED_AUDIO_FORMATS,
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE_MB,
    MAX_DURATION_SEC,
    WHISPER_LANG_MAP,
    DARIJA_PROMPTS,
)

from .stt_service import (
    STTService,
    get_stt_service,
    init_stt_service,
    detect_audio_format,
    get_audio_duration,
    get_audio_metadata,
)

from .stt_router import router as stt_router

# ============================================
# TTS IMPORTS
# ============================================

from .tts_models import (
    # Enums
    TTSLanguage,
    TTSDialect,
    TTSBackend,
    TTSVoiceGender,
    TTSEmotion,
    AudioFormat as TTSAudioFormat,
    # Voice model
    TTSVoice,
    # Request models
    TTSRequest,
    TTSSimpleRequest,
    TTSBatchRequest,
    TTSBatchResultItem,
    # Response models
    TTSResponse,
    TTSStreamChunk,
    TTSBatchResponse,
    # Status models
    TTSStatus,
    TTSError,
    # Constants
    DEFAULT_VOICES,
    FORMAT_MIME_TYPES,
    MAX_TEXT_LENGTH,
)

from .tts_service import (
    TTSService,
    get_tts_service,
    init_tts_service,
    audio_bytes_to_base64,
    base64_to_audio_bytes,
    estimate_audio_duration,
)

from .tts_router import router as tts_router

# ============================================
# VOICE AGENT IMPORTS
# ============================================

from .voice_agent_models import (
    # Enums
    AgentMode,
    AgentLanguage,
    AgentDialect,
    IntentType,
    ProcessingStep,
    ConversationStatus,
    # Message models
    ConversationMessage,
    ConversationContext,
    ConversationState,
    ConversationSummary,
    # Request models
    VoiceAgentRequest,
    VoiceAgentTextRequest,
    VoiceAgentAudioRequest,
    # Response models
    VoiceAgentResponse,
    ProcessingStepResult,
    IntentDetectionResult,
    VoiceAgentStatus,
    # Constants
    SYSTEM_PROMPTS,
    INTENT_KEYWORDS,
    MAX_CONVERSATION_LENGTH,
)

from .voice_agent_service import (
    VoiceAgentService,
    get_voice_agent_service,
    init_voice_agent_service,
)

from .voice_agent_router import router as voice_agent_router


__all__ = [
    # ============ STT ============
    # Router
    "stt_router",
    
    # Service
    "STTService",
    "get_stt_service",
    "init_stt_service",
    
    # Utilities
    "detect_audio_format",
    "get_audio_duration",
    "get_audio_metadata",
    
    # Enums
    "STTLanguage",
    "STTDialect",
    "STTBackend",
    "STTModel",
    "STTAudioFormat",
    
    # Models
    "STTRequest",
    "STTQuickRequest",
    "STTResponse",
    "STTSegment",
    "DarijaNormResult",
    "STTBatchItem",
    "STTBatchResponse",
    "STTStatus",
    "STTModelInfo",
    "STTError",
    
    # Constants
    "SUPPORTED_AUDIO_FORMATS",
    "ALLOWED_EXTENSIONS",
    "MAX_FILE_SIZE_MB",
    "MAX_DURATION_SEC",
    "WHISPER_LANG_MAP",
    "DARIJA_PROMPTS",
    
    # ============ TTS ============
    # Router
    "tts_router",
    
    # Service
    "TTSService",
    "get_tts_service",
    "init_tts_service",
    
    # Utilities
    "audio_bytes_to_base64",
    "base64_to_audio_bytes",
    "estimate_audio_duration",
    
    # Enums
    "TTSLanguage",
    "TTSDialect",
    "TTSBackend",
    "TTSVoiceGender",
    "TTSEmotion",
    "TTSAudioFormat",
    
    # Models
    "TTSVoice",
    "TTSRequest",
    "TTSSimpleRequest",
    "TTSResponse",
    "TTSStreamChunk",
    "TTSBatchRequest",
    "TTSBatchResultItem",
    "TTSBatchResponse",
    "TTSStatus",
    "TTSError",
    
    # Constants
    "DEFAULT_VOICES",
    "FORMAT_MIME_TYPES",
    "MAX_TEXT_LENGTH",
    
    # ============ VOICE AGENT ============
    # Router
    "voice_agent_router",
    
    # Service
    "VoiceAgentService",
    "get_voice_agent_service",
    "init_voice_agent_service",
    
    # Enums
    "AgentMode",
    "AgentLanguage",
    "AgentDialect",
    "IntentType",
    "ProcessingStep",
    "ConversationStatus",
    
    # Models
    "ConversationMessage",
    "ConversationContext",
    "ConversationState",
    "ConversationSummary",
    "VoiceAgentRequest",
    "VoiceAgentTextRequest",
    "VoiceAgentAudioRequest",
    "VoiceAgentResponse",
    "ProcessingStepResult",
    "IntentDetectionResult",
    "VoiceAgentStatus",
    
    # Constants
    "SYSTEM_PROMPTS",
    "INTENT_KEYWORDS",
    "MAX_CONVERSATION_LENGTH",
]


# Version
__version__ = "1.0.0"
__author__ = "iaFactoryDZ"
__description__ = "Voice Processing: STT + TTS + Agent Vocal pour arabe/darija algérienne"
