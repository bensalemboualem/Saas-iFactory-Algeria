"""
TTS_VOICE - Modèles Pydantic
============================
Text-to-Speech pour arabe/darija/français/anglais
Architecture extensible (mock → Coqui → ElevenLabs → OpenAI)
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field


# ============================================
# ENUMS
# ============================================

class TTSLanguage(str, Enum):
    """Langues supportées pour TTS"""
    ARABIC = "ar"        # Arabe
    FRENCH = "fr"        # Français
    ENGLISH = "en"       # Anglais
    ITALIAN = "it"       # Italien (Suisse)
    GERMAN = "de"        # Allemand (Suisse)


class TTSDialect(str, Enum):
    """Dialectes arabes supportés"""
    DARIJA = "darija"    # Darija algérienne
    MSA = "msa"          # Arabe standard moderne
    MIXED = "mixed"      # Mélange arabe/français
    TUNISIAN = "tunisian"  # Tunisien (futur)
    MOROCCAN = "moroccan"  # Marocain (futur)


class TTSBackend(str, Enum):
    """Backends TTS disponibles"""
    MOCK = "mock"              # Mock (pas de vrai TTS)
    OPENAI = "openai"          # OpenAI TTS
    ELEVENLABS = "elevenlabs"  # ElevenLabs
    COQUI = "coqui"            # Coqui TTS (local)
    GTTS = "gtts"              # Google TTS (gratuit)
    AZURE = "azure"            # Azure Speech


class TTSVoiceGender(str, Enum):
    """Genre de voix"""
    MALE = "male"
    FEMALE = "female"
    NEUTRAL = "neutral"


class TTSEmotion(str, Enum):
    """Émotion/ton de la voix"""
    NEUTRAL = "neutral"
    FRIENDLY = "friendly"
    SERIOUS = "serious"
    PROFESSIONAL = "professional"
    WARM = "warm"
    CALM = "calm"
    EXCITED = "excited"


class AudioFormat(str, Enum):
    """Formats audio de sortie"""
    MP3 = "mp3"
    WAV = "wav"
    OGG = "ogg"
    WEBM = "webm"
    FLAC = "flac"
    PCM = "pcm"


# ============================================
# VOICE MODELS
# ============================================

class TTSVoice(BaseModel):
    """Définition d'une voix TTS"""
    id: str = Field(..., description="ID unique de la voix")
    name: str = Field(..., description="Nom de la voix")
    language: TTSLanguage = Field(..., description="Langue principale")
    dialect: Optional[TTSDialect] = Field(None, description="Dialecte (pour arabe)")
    gender: TTSVoiceGender = Field(TTSVoiceGender.NEUTRAL, description="Genre")
    backend: TTSBackend = Field(..., description="Backend TTS")
    
    # Caractéristiques
    description: Optional[str] = Field(None, description="Description de la voix")
    sample_url: Optional[str] = Field(None, description="URL échantillon audio")
    is_premium: bool = Field(False, description="Voix premium")
    is_available: bool = Field(True, description="Voix disponible")
    
    # Provider-specific
    provider_voice_id: Optional[str] = Field(None, description="ID voix chez le provider")


# ============================================
# REQUEST MODELS
# ============================================

class TTSRequest(BaseModel):
    """Requête de synthèse vocale"""
    text: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Texte à synthétiser"
    )
    language: TTSLanguage = Field(
        TTSLanguage.ARABIC,
        description="Langue (ar, fr, en)"
    )
    dialect: Optional[TTSDialect] = Field(
        TTSDialect.DARIJA,
        description="Dialecte arabe (darija, msa, mixed)"
    )
    voice_id: Optional[str] = Field(
        None,
        description="ID de la voix à utiliser"
    )
    
    # Options audio
    speed: float = Field(
        1.0,
        ge=0.25,
        le=4.0,
        description="Vitesse de lecture (0.25-4.0)"
    )
    pitch: float = Field(
        1.0,
        ge=0.5,
        le=2.0,
        description="Hauteur de la voix (0.5-2.0)"
    )
    volume: float = Field(
        1.0,
        ge=0.0,
        le=2.0,
        description="Volume (0.0-2.0)"
    )
    
    # Style
    emotion: TTSEmotion = Field(
        TTSEmotion.NEUTRAL,
        description="Ton/émotion de la voix"
    )
    
    # Format de sortie
    format: AudioFormat = Field(
        AudioFormat.MP3,
        description="Format audio de sortie"
    )
    sample_rate: int = Field(
        22050,
        description="Taux d'échantillonnage"
    )
    
    # Options avancées
    normalize_text: bool = Field(
        True,
        description="Normaliser le texte avant synthèse"
    )
    add_silence_start: float = Field(
        0.0,
        ge=0.0,
        le=5.0,
        description="Silence au début (secondes)"
    )
    add_silence_end: float = Field(
        0.0,
        ge=0.0,
        le=5.0,
        description="Silence à la fin (secondes)"
    )


class TTSSimpleRequest(BaseModel):
    """Requête simplifiée TTS"""
    text: str = Field(..., min_length=1, max_length=2000, description="Texte à synthétiser")
    language: Optional[str] = Field("ar", description="Langue (ar, fr, en)")
    voice: Optional[str] = Field(None, description="Voix optionnelle")


# ============================================
# RESPONSE MODELS
# ============================================

class TTSResponse(BaseModel):
    """Réponse synthèse vocale"""
    # Audio
    audio_base64: str = Field(..., description="Audio encodé en base64")
    mime_type: str = Field(..., description="Type MIME (audio/mpeg, audio/wav)")
    
    # Métadonnées
    language: str = Field(..., description="Langue utilisée")
    dialect: Optional[str] = Field(None, description="Dialecte utilisé")
    
    # Voix utilisée
    used_voice_id: Optional[str] = Field(None, description="ID de la voix utilisée")
    used_backend: str = Field(..., description="Backend TTS utilisé")
    
    # Stats
    duration_sec: float = Field(0.0, description="Durée audio en secondes")
    char_count: int = Field(0, description="Nombre de caractères")
    processing_time_ms: int = Field(0, description="Temps de traitement en ms")
    
    # Format
    format: str = Field("mp3", description="Format audio")
    sample_rate: int = Field(22050, description="Taux d'échantillonnage")
    
    # Timestamp
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class TTSStreamChunk(BaseModel):
    """Chunk pour streaming TTS"""
    chunk_index: int = Field(..., description="Index du chunk")
    audio_base64: str = Field(..., description="Chunk audio en base64")
    is_last: bool = Field(False, description="Dernier chunk")
    total_chunks: Optional[int] = Field(None, description="Nombre total de chunks")


# ============================================
# STATUS MODELS
# ============================================

class TTSStatus(BaseModel):
    """Statut du service TTS"""
    ready: bool = Field(..., description="Service prêt")
    available_voices: List[str] = Field(
        default_factory=list,
        description="Voix disponibles"
    )
    backend_type: str = Field(..., description="Backend actif")
    
    # Détails backends
    backends_status: Dict[str, bool] = Field(
        default_factory=dict,
        description="Statut de chaque backend"
    )
    
    # Capacités
    supported_languages: List[str] = Field(
        default_factory=lambda: ["ar", "fr", "en"],
        description="Langues supportées"
    )
    supported_formats: List[str] = Field(
        default_factory=lambda: ["mp3", "wav", "ogg"],
        description="Formats audio supportés"
    )
    max_text_length: int = Field(5000, description="Longueur max texte")
    
    # Version
    version: str = Field("1.0.0")
    service: str = Field("TTS_VOICE")


# ============================================
# BATCH MODELS
# ============================================

class TTSBatchItem(BaseModel):
    """Item pour batch TTS"""
    id: str = Field(..., description="ID unique de l'item")
    text: str = Field(..., description="Texte à synthétiser")
    language: Optional[str] = Field("ar", description="Langue")
    voice_id: Optional[str] = Field(None, description="Voix")


class TTSBatchRequest(BaseModel):
    """Requête batch TTS"""
    items: List[TTSBatchItem] = Field(..., min_length=1, max_length=50)
    format: AudioFormat = Field(AudioFormat.MP3)
    merge: bool = Field(False, description="Fusionner en un seul audio")


class TTSBatchResultItem(BaseModel):
    """Résultat d'un item batch"""
    id: str
    success: bool
    audio_base64: Optional[str] = None
    error: Optional[str] = None
    duration_sec: float = 0.0


class TTSBatchResponse(BaseModel):
    """Réponse batch TTS"""
    items: List[TTSBatchResultItem]
    total: int
    success_count: int
    error_count: int
    total_duration_sec: float
    processing_time_ms: int
    
    # Audio fusionné (si merge=True)
    merged_audio_base64: Optional[str] = None


# ============================================
# ERROR MODELS
# ============================================

class TTSError(BaseModel):
    """Erreur TTS"""
    error: str = Field(..., description="Type d'erreur")
    message: str = Field(..., description="Message d'erreur")
    code: int = Field(..., description="Code HTTP")
    details: Optional[Dict[str, Any]] = Field(None)


# ============================================
# CONSTANTS
# ============================================

# Voix par défaut (mock)
DEFAULT_VOICES = [
    TTSVoice(
        id="default",
        name="Voix par défaut",
        language=TTSLanguage.ARABIC,
        dialect=TTSDialect.DARIJA,
        gender=TTSVoiceGender.FEMALE,
        backend=TTSBackend.MOCK,
        description="Voix arabe algérienne par défaut",
    ),
    TTSVoice(
        id="female_dz",
        name="Amira (DZ)",
        language=TTSLanguage.ARABIC,
        dialect=TTSDialect.DARIJA,
        gender=TTSVoiceGender.FEMALE,
        backend=TTSBackend.MOCK,
        description="Voix féminine darija algérienne",
    ),
    TTSVoice(
        id="male_dz",
        name="Youcef (DZ)",
        language=TTSLanguage.ARABIC,
        dialect=TTSDialect.DARIJA,
        gender=TTSVoiceGender.MALE,
        backend=TTSBackend.MOCK,
        description="Voix masculine darija algérienne",
    ),
    TTSVoice(
        id="female_fr",
        name="Sophie (FR)",
        language=TTSLanguage.FRENCH,
        gender=TTSVoiceGender.FEMALE,
        backend=TTSBackend.MOCK,
        description="Voix féminine française",
    ),
    TTSVoice(
        id="male_fr",
        name="Pierre (FR)",
        language=TTSLanguage.FRENCH,
        gender=TTSVoiceGender.MALE,
        backend=TTSBackend.MOCK,
        description="Voix masculine française",
    ),
]

# Mapping format → MIME type
FORMAT_MIME_TYPES = {
    AudioFormat.MP3: "audio/mpeg",
    AudioFormat.WAV: "audio/wav",
    AudioFormat.OGG: "audio/ogg",
    AudioFormat.WEBM: "audio/webm",
    AudioFormat.FLAC: "audio/flac",
    AudioFormat.PCM: "audio/pcm",
}

# Limites
MAX_TEXT_LENGTH = 5000
MAX_BATCH_SIZE = 50
