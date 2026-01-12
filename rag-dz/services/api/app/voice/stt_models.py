"""
STT_VOICE - Modèles Pydantic
============================
Speech-to-Text pour arabe + darija algérienne
Avec intégration DARIJA_NLP
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# ============================================
# ENUMS
# ============================================

class STTLanguage(str, Enum):
    """Langues supportées pour STT"""
    AUTO = "auto"        # Détection automatique
    ARABIC = "ar"        # Arabe (MSA + dialectes)
    FRENCH = "fr"        # Français
    ENGLISH = "en"       # Anglais
    DARIJA = "ar-dz"     # Arabe algérien (darija)


class STTDialect(str, Enum):
    """Dialectes arabes supportés"""
    AUTO = "auto"        # Détection automatique
    DARIJA = "darija"    # Darija algérienne
    MSA = "msa"          # Arabe standard moderne
    MIXED = "mixed"      # Mélange arabe/français
    TUNISIAN = "tunisian"  # Tunisien (futur)
    MOROCCAN = "moroccan"  # Marocain (futur)


class STTBackend(str, Enum):
    """Backend STT disponibles"""
    OPENAI = "openai"           # Whisper via OpenAI API
    LOCAL_WHISPER = "local"     # Whisper local (GPU)
    AZURE = "azure"             # Azure Speech (futur)
    HYBRID = "hybrid"           # Auto-switch


class STTModel(str, Enum):
    """Modèles Whisper disponibles"""
    WHISPER_1 = "whisper-1"                  # OpenAI Whisper
    WHISPER_LARGE_V3 = "whisper-large-v3"    # Local large
    WHISPER_MEDIUM = "whisper-medium"        # Local medium
    WHISPER_SMALL = "whisper-small"          # Local small (fast)
    WHISPER_TURBO = "whisper-large-v3-turbo" # Turbo (OpenAI)


class AudioFormat(str, Enum):
    """Formats audio supportés"""
    WAV = "wav"
    MP3 = "mp3"
    OGG = "ogg"
    WEBM = "webm"
    M4A = "m4a"
    FLAC = "flac"
    MP4 = "mp4"     # Pour extraction audio


# ============================================
# REQUEST MODELS
# ============================================

class STTRequest(BaseModel):
    """Requête de transcription STT"""
    language_hint: Optional[STTLanguage] = Field(
        STTLanguage.AUTO,
        description="Indice de langue (ar, fr, en, auto)"
    )
    dialect: Optional[STTDialect] = Field(
        STTDialect.AUTO,
        description="Dialecte attendu (darija, msa, mixed, auto)"
    )
    model: Optional[STTModel] = Field(
        None,
        description="Modèle Whisper à utiliser"
    )
    
    # Options avancées
    enable_darija_normalization: bool = Field(
        True,
        description="Activer normalisation darija post-transcription"
    )
    enable_timestamps: bool = Field(
        False,
        description="Inclure les timestamps par segment"
    )
    temperature: float = Field(
        0.0,
        ge=0.0,
        le=1.0,
        description="Température pour la transcription"
    )
    
    # Contexte
    prompt: Optional[str] = Field(
        None,
        max_length=500,
        description="Prompt contextuel pour améliorer transcription"
    )
    vocabulary: Optional[List[str]] = Field(
        None,
        description="Vocabulaire spécifique à privilégier"
    )


class STTQuickRequest(BaseModel):
    """Requête simplifiée STT (auto tout)"""
    language_hint: Optional[str] = Field(None, description="Indice optionnel de langue")


# ============================================
# RESPONSE MODELS
# ============================================

class STTSegment(BaseModel):
    """Segment de transcription avec timestamp"""
    start: float = Field(..., description="Début en secondes")
    end: float = Field(..., description="Fin en secondes")
    text: str = Field(..., description="Texte du segment")
    confidence: Optional[float] = Field(None, description="Confiance du segment")


class DarijaNormResult(BaseModel):
    """Résultat de normalisation darija"""
    original: str = Field(..., description="Texte original")
    normalized: str = Field(..., description="Texte normalisé")
    is_arabizi: bool = Field(False, description="Contient de l'arabizi")
    dialect_detected: str = Field("unknown", description="Dialecte détecté")
    confidence: float = Field(0.0, description="Confiance de détection")
    tokens_count: int = Field(0, description="Nombre de tokens")


class STTResponse(BaseModel):
    """Réponse complète de transcription STT"""
    # Textes
    text_raw: str = Field(..., description="Transcription brute Whisper")
    text_cleaned: str = Field(..., description="Texte nettoyé (cleaner)")
    text_normalized: Optional[str] = Field(
        None,
        description="Texte normalisé darija (si applicable)"
    )
    
    # Métadonnées langue
    language: str = Field(..., description="Langue détectée (ar, fr, en)")
    language_confidence: Optional[float] = Field(None, description="Confiance langue")
    dialect: Optional[str] = Field(None, description="Dialecte (darija, msa, mixed)")
    is_arabizi: Optional[bool] = Field(None, description="Contient de l'arabizi")
    
    # Audio info
    duration_sec: float = Field(..., description="Durée audio en secondes")
    audio_format: Optional[str] = Field(None, description="Format audio détecté")
    sample_rate: Optional[int] = Field(None, description="Taux d'échantillonnage")
    
    # Modèle utilisé
    used_model: Optional[str] = Field(None, description="Modèle Whisper utilisé")
    used_backend: Optional[str] = Field(None, description="Backend (openai/local)")
    
    # Qualité
    confidence: Optional[float] = Field(None, description="Confiance globale")
    word_count: int = Field(0, description="Nombre de mots")
    
    # Segments (optionnel)
    segments: Optional[List[STTSegment]] = Field(
        None,
        description="Segments avec timestamps"
    )
    
    # Darija details (optionnel)
    darija_result: Optional[DarijaNormResult] = Field(
        None,
        description="Détails normalisation darija"
    )
    
    # Processing
    processing_time_ms: int = Field(0, description="Temps de traitement en ms")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class STTBatchItem(BaseModel):
    """Item pour batch processing"""
    filename: str
    response: Optional[STTResponse] = None
    error: Optional[str] = None
    success: bool = True


class STTBatchResponse(BaseModel):
    """Réponse batch STT"""
    items: List[STTBatchItem]
    total: int
    success_count: int
    error_count: int
    total_duration_sec: float
    processing_time_ms: int


# ============================================
# STATUS / HEALTH MODELS
# ============================================

class STTModelInfo(BaseModel):
    """Info sur un modèle STT"""
    name: str
    backend: str
    available: bool
    description: Optional[str] = None


class STTStatus(BaseModel):
    """Statut du service STT"""
    ready: bool = Field(..., description="Service prêt")
    available_models: List[str] = Field(
        default_factory=list,
        description="Modèles disponibles"
    )
    backend_type: str = Field(..., description="Backend actif (openai/local/hybrid)")
    
    # Détails
    openai_available: bool = Field(False, description="API OpenAI accessible")
    local_available: bool = Field(False, description="Whisper local disponible")
    darija_nlp_ready: bool = Field(False, description="DARIJA_NLP intégré")
    
    # Capacités
    supported_formats: List[str] = Field(
        default_factory=lambda: ["wav", "mp3", "ogg", "webm", "m4a", "flac"],
        description="Formats audio supportés"
    )
    supported_languages: List[str] = Field(
        default_factory=lambda: ["ar", "fr", "en", "auto"],
        description="Langues supportées"
    )
    max_file_size_mb: int = Field(25, description="Taille max fichier (MB)")
    max_duration_sec: int = Field(600, description="Durée max (secondes)")
    
    # Version
    version: str = Field("1.0.0")
    service: str = Field("STT_VOICE")


# ============================================
# ERROR MODELS
# ============================================

class STTError(BaseModel):
    """Erreur STT"""
    error: str = Field(..., description="Type d'erreur")
    message: str = Field(..., description="Message d'erreur")
    code: int = Field(..., description="Code HTTP")
    details: Optional[Dict[str, Any]] = Field(None, description="Détails additionnels")


# ============================================
# CONSTANTS
# ============================================

# Formats supportés avec leurs MIME types
SUPPORTED_AUDIO_FORMATS = {
    "wav": ["audio/wav", "audio/x-wav", "audio/wave"],
    "mp3": ["audio/mpeg", "audio/mp3"],
    "ogg": ["audio/ogg", "application/ogg"],
    "webm": ["audio/webm", "video/webm"],
    "m4a": ["audio/m4a", "audio/x-m4a", "audio/mp4"],
    "flac": ["audio/flac", "audio/x-flac"],
    "mp4": ["video/mp4", "audio/mp4"],
}

# Extensions autorisées
ALLOWED_EXTENSIONS = list(SUPPORTED_AUDIO_FORMATS.keys())

# Limites par défaut
MAX_FILE_SIZE_MB = 25
MAX_DURATION_SEC = 600  # 10 minutes

# Mapping langues Whisper → codes standard
WHISPER_LANG_MAP = {
    "arabic": "ar",
    "french": "fr",
    "english": "en",
    "ar": "ar",
    "fr": "fr",
    "en": "en",
}

# Prompts contextuels pour améliorer transcription darija
DARIJA_PROMPTS = {
    "general": "هذا نص بالدارجة الجزائرية، قد يحتوي على كلمات فرنسية",
    "admin": "نص إداري جزائري، casnos, cnas, registre de commerce, impôts",
    "commerce": "نص تجاري جزائري، facture, bon de livraison, prix, DZD",
    "legal": "نص قانوني جزائري، عقد، محكمة، موثق",
}
