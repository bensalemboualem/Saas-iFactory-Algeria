"""
STT_VOICE - Service Speech-to-Text
==================================
Transcription audio vers texte (arabe/darija/français/anglais)
Avec intégration Whisper (OpenAI API ou local) + DARIJA_NLP
"""

import os
import io
import time
import tempfile
import logging
from pathlib import Path
from typing import Optional, Dict, Any, Tuple, List
from datetime import datetime

# Audio processing
try:
    import soundfile as sf
    SOUNDFILE_AVAILABLE = True
except ImportError:
    SOUNDFILE_AVAILABLE = False

try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False

# OpenAI
try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Models
from .stt_models import (
    STTRequest,
    STTResponse,
    STTStatus,
    STTSegment,
    DarijaNormResult,
    STTLanguage,
    STTDialect,
    STTBackend,
    STTModel,
    SUPPORTED_AUDIO_FORMATS,
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE_MB,
    MAX_DURATION_SEC,
    WHISPER_LANG_MAP,
    DARIJA_PROMPTS,
)

# DARIJA_NLP integration
try:
    from app.darija.darija_cleaner import clean_text
    from app.darija.darija_normalizer import normalize_darija
    DARIJA_NLP_AVAILABLE = True
except ImportError:
    DARIJA_NLP_AVAILABLE = False
    # Fallback functions
    def clean_text(text: str) -> str:
        return text.strip()
    def normalize_darija(text: str) -> Dict[str, Any]:
        return {"normalized": text, "is_arabizi": False, "dialect": "unknown", "confidence": 0.0}


logger = logging.getLogger(__name__)


# ============================================
# AUDIO UTILITIES
# ============================================

def detect_audio_format(file_bytes: bytes, filename: Optional[str] = None) -> Tuple[str, str]:
    """
    Détecte le format audio depuis les bytes ou le nom de fichier
    
    Returns:
        (format, mime_type)
    """
    # Par extension si disponible
    if filename:
        ext = Path(filename).suffix.lower().lstrip('.')
        if ext in ALLOWED_EXTENSIONS:
            mime_types = SUPPORTED_AUDIO_FORMATS.get(ext, [])
            return ext, mime_types[0] if mime_types else f"audio/{ext}"
    
    # Par magic bytes
    if file_bytes[:4] == b'RIFF':
        return "wav", "audio/wav"
    elif file_bytes[:3] == b'ID3' or file_bytes[:2] == b'\xff\xfb':
        return "mp3", "audio/mpeg"
    elif file_bytes[:4] == b'OggS':
        return "ogg", "audio/ogg"
    elif file_bytes[:4] == b'\x1aE\xdf\xa3':  # WebM/Matroska
        return "webm", "audio/webm"
    elif file_bytes[4:8] == b'ftyp':
        # M4A ou MP4
        subtype = file_bytes[8:12]
        if b'M4A' in subtype or b'mp4' in subtype.lower():
            return "m4a", "audio/m4a"
        return "mp4", "video/mp4"
    elif file_bytes[:4] == b'fLaC':
        return "flac", "audio/flac"
    
    # Défaut
    return "unknown", "application/octet-stream"


def get_audio_duration(file_bytes: bytes, audio_format: str) -> float:
    """
    Calcule la durée de l'audio en secondes
    """
    try:
        if SOUNDFILE_AVAILABLE and audio_format in ["wav", "flac", "ogg"]:
            with io.BytesIO(file_bytes) as f:
                data, samplerate = sf.read(f)
                return len(data) / samplerate
        
        if PYDUB_AVAILABLE:
            with io.BytesIO(file_bytes) as f:
                audio = AudioSegment.from_file(f, format=audio_format)
                return len(audio) / 1000.0  # ms to sec
        
        # Estimation basique par taille (fallback)
        # Assume 128kbps pour MP3
        size_kb = len(file_bytes) / 1024
        return size_kb / 16  # Rough estimate
        
    except Exception as e:
        logger.warning(f"Could not determine audio duration: {e}")
        return 0.0


def get_audio_metadata(file_bytes: bytes, audio_format: str) -> Dict[str, Any]:
    """
    Extrait les métadonnées audio
    """
    metadata = {
        "format": audio_format,
        "size_bytes": len(file_bytes),
        "size_mb": round(len(file_bytes) / (1024 * 1024), 2),
        "duration_sec": 0.0,
        "sample_rate": None,
        "channels": None,
    }
    
    try:
        if SOUNDFILE_AVAILABLE and audio_format in ["wav", "flac", "ogg"]:
            with io.BytesIO(file_bytes) as f:
                info = sf.info(f)
                metadata["duration_sec"] = info.duration
                metadata["sample_rate"] = info.samplerate
                metadata["channels"] = info.channels
        
        elif PYDUB_AVAILABLE:
            with io.BytesIO(file_bytes) as f:
                audio = AudioSegment.from_file(f, format=audio_format)
                metadata["duration_sec"] = len(audio) / 1000.0
                metadata["sample_rate"] = audio.frame_rate
                metadata["channels"] = audio.channels
        
        else:
            metadata["duration_sec"] = get_audio_duration(file_bytes, audio_format)
            
    except Exception as e:
        logger.warning(f"Could not extract audio metadata: {e}")
        metadata["duration_sec"] = get_audio_duration(file_bytes, audio_format)
    
    return metadata


# ============================================
# STT SERVICE
# ============================================

class STTService:
    """
    Service de Speech-to-Text multi-backend
    
    Supporte :
    - OpenAI Whisper API (par défaut)
    - Whisper local (GPU) - à implémenter
    
    Intègre DARIJA_NLP pour post-traitement arabe/darija
    """
    
    def __init__(
        self,
        use_openai: bool = True,
        openai_api_key: Optional[str] = None,
        default_model: str = "whisper-1",
        enable_darija_nlp: bool = True,
    ):
        """
        Initialise le service STT
        
        Args:
            use_openai: Utiliser l'API OpenAI Whisper
            openai_api_key: Clé API OpenAI (ou via env)
            default_model: Modèle Whisper par défaut
            enable_darija_nlp: Activer intégration DARIJA_NLP
        """
        self.use_openai = use_openai
        self.default_model = default_model
        self.enable_darija_nlp = enable_darija_nlp and DARIJA_NLP_AVAILABLE
        
        # OpenAI client
        self.openai_client: Optional[AsyncOpenAI] = None
        if use_openai and OPENAI_AVAILABLE:
            api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
            if api_key:
                self.openai_client = AsyncOpenAI(api_key=api_key)
                logger.info("STTService: OpenAI Whisper client initialized")
            else:
                logger.warning("STTService: No OpenAI API key, using mock mode")
        
        # Whisper local (placeholder)
        self.local_whisper_model = None
        
        logger.info(f"STTService initialized - OpenAI: {self.openai_client is not None}, DARIJA_NLP: {self.enable_darija_nlp}")
    
    # ----------------------------------------
    # MAIN TRANSCRIPTION METHOD
    # ----------------------------------------
    
    async def transcribe_audio(
        self,
        file_bytes: bytes,
        request: Optional[STTRequest] = None,
        filename: Optional[str] = None,
    ) -> STTResponse:
        """
        Transcrit un fichier audio en texte
        
        Pipeline:
        1. Détection format audio
        2. Validation (taille, durée)
        3. Transcription via backend (OpenAI/local)
        4. Nettoyage texte via darija_cleaner
        5. Normalisation darija si arabe détecté
        6. Construction réponse complète
        
        Args:
            file_bytes: Contenu du fichier audio
            request: Options de transcription
            filename: Nom du fichier (pour détection format)
            
        Returns:
            STTResponse avec texte brut, nettoyé, normalisé
        """
        start_time = time.time()
        request = request or STTRequest()
        
        # 1. Détection format
        audio_format, mime_type = detect_audio_format(file_bytes, filename)
        logger.info(f"Audio format detected: {audio_format} ({mime_type})")
        
        if audio_format == "unknown" or audio_format not in ALLOWED_EXTENSIONS:
            raise ValueError(f"Format audio non supporté: {audio_format}")
        
        # 2. Métadonnées audio
        metadata = get_audio_metadata(file_bytes, audio_format)
        duration_sec = metadata.get("duration_sec", 0.0)
        
        # Validation taille
        size_mb = len(file_bytes) / (1024 * 1024)
        if size_mb > MAX_FILE_SIZE_MB:
            raise ValueError(f"Fichier trop volumineux: {size_mb:.1f}MB (max {MAX_FILE_SIZE_MB}MB)")
        
        # Validation durée
        if duration_sec > MAX_DURATION_SEC:
            raise ValueError(f"Audio trop long: {duration_sec:.0f}s (max {MAX_DURATION_SEC}s)")
        
        # 3. Transcription via backend
        text_raw, language_detected, segments = await self._transcribe_backend(
            file_bytes=file_bytes,
            audio_format=audio_format,
            request=request,
        )
        
        logger.info(f"Transcription brute: {text_raw[:100]}..." if len(text_raw) > 100 else f"Transcription: {text_raw}")
        
        # 4. Nettoyage texte
        text_cleaned = clean_text(text_raw) if self.enable_darija_nlp else text_raw.strip()
        
        # 5. Normalisation darija si arabe
        text_normalized = None
        darija_result = None
        is_arabizi = None
        dialect = None
        
        lang_code = WHISPER_LANG_MAP.get(language_detected, language_detected)
        
        should_normalize = (
            self.enable_darija_nlp and
            request.enable_darija_normalization and
            (lang_code == "ar" or request.dialect == STTDialect.DARIJA or request.language_hint == STTLanguage.DARIJA)
        )
        
        if should_normalize:
            try:
                norm_result = normalize_darija(text_cleaned)
                text_normalized = getattr(norm_result, "normalized", text_cleaned)
                is_arabizi = getattr(norm_result, "is_arabizi", False)
                dialect = getattr(norm_result, "dialect", "unknown")
                
                darija_result = DarijaNormResult(
                    original=text_cleaned,
                    normalized=text_normalized,
                    is_arabizi=is_arabizi,
                    dialect_detected=dialect,
                    confidence=getattr(norm_result, "confidence", 0.0),
                    tokens_count=getattr(norm_result, "tokens_count", len(text_normalized.split())),
                )
                
                logger.info(f"Darija normalization: arabizi={is_arabizi}, dialect={dialect}")
                
            except Exception as e:
                logger.warning(f"Darija normalization failed: {e}")
                text_normalized = text_cleaned
        
        # 6. Déterminer dialecte si pas fait
        if dialect is None and lang_code == "ar":
            dialect = self._detect_dialect(text_cleaned, text_normalized)
        
        # Calcul processing time
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        # 7. Construire réponse
        return STTResponse(
            text_raw=text_raw,
            text_cleaned=text_cleaned,
            text_normalized=text_normalized,
            language=lang_code,
            language_confidence=0.9 if lang_code != "unknown" else 0.0,
            dialect=dialect,
            is_arabizi=is_arabizi,
            duration_sec=duration_sec,
            audio_format=audio_format,
            sample_rate=metadata.get("sample_rate"),
            used_model=request.model.value if request.model else self.default_model,
            used_backend="openai" if self.openai_client else "mock",
            confidence=0.85,  # Placeholder
            word_count=len(text_cleaned.split()),
            segments=[STTSegment(**s) for s in segments] if segments else None,
            darija_result=darija_result,
            processing_time_ms=processing_time_ms,
        )
    
    # ----------------------------------------
    # BACKEND TRANSCRIPTION
    # ----------------------------------------
    
    async def _transcribe_backend(
        self,
        file_bytes: bytes,
        audio_format: str,
        request: STTRequest,
    ) -> Tuple[str, str, List[Dict]]:
        """
        Transcrit via le backend approprié
        
        Returns:
            (text, language, segments)
        """
        if self.openai_client:
            return await self._transcribe_openai(file_bytes, audio_format, request)
        elif self.local_whisper_model:
            return await self._transcribe_local(file_bytes, audio_format, request)
        else:
            return self._transcribe_mock(file_bytes, audio_format, request)
    
    async def _transcribe_openai(
        self,
        file_bytes: bytes,
        audio_format: str,
        request: STTRequest,
    ) -> Tuple[str, str, List[Dict]]:
        """
        Transcription via OpenAI Whisper API
        """
        try:
            # Préparer le fichier
            file_tuple = (f"audio.{audio_format}", file_bytes, f"audio/{audio_format}")
            
            # Construire le prompt contextuel
            prompt = request.prompt
            if not prompt and request.dialect == STTDialect.DARIJA:
                prompt = DARIJA_PROMPTS.get("general", "")
            
            # Préparer les kwargs
            kwargs = {
                "model": request.model.value if request.model else self.default_model,
                "file": file_tuple,
                "response_format": "verbose_json" if request.enable_timestamps else "json",
            }
            
            # Langue
            if request.language_hint and request.language_hint != STTLanguage.AUTO:
                lang_map = {"ar": "ar", "fr": "fr", "en": "en", "ar-dz": "ar"}
                kwargs["language"] = lang_map.get(request.language_hint.value, None)
            
            # Prompt
            if prompt:
                kwargs["prompt"] = prompt
            
            # Température
            if request.temperature > 0:
                kwargs["temperature"] = request.temperature
            
            # Appel API
            with tempfile.NamedTemporaryFile(suffix=f".{audio_format}", delete=False) as tmp:
                tmp.write(file_bytes)
                tmp_path = tmp.name
            
            try:
                with open(tmp_path, "rb") as audio_file:
                    response = await self.openai_client.audio.transcriptions.create(
                        model=kwargs["model"],
                        file=audio_file,
                        response_format=kwargs.get("response_format", "json"),
                        language=kwargs.get("language"),
                        prompt=kwargs.get("prompt"),
                        temperature=kwargs.get("temperature", 0),
                    )
            finally:
                os.unlink(tmp_path)
            
            # Parser la réponse
            if hasattr(response, "text"):
                text = response.text
            elif isinstance(response, dict):
                text = response.get("text", "")
            else:
                text = str(response)
            
            # Langue détectée
            language = "ar"  # Default pour darija
            if hasattr(response, "language"):
                language = response.language
            elif isinstance(response, dict) and "language" in response:
                language = response["language"]
            
            # Segments
            segments = []
            if request.enable_timestamps:
                if hasattr(response, "segments"):
                    segments = [{"start": s.start, "end": s.end, "text": s.text} for s in response.segments]
                elif isinstance(response, dict) and "segments" in response:
                    segments = response["segments"]
            
            return text, language, segments
            
        except Exception as e:
            logger.error(f"OpenAI transcription error: {e}")
            raise RuntimeError(f"Erreur transcription OpenAI: {str(e)}")
    
    async def _transcribe_local(
        self,
        file_bytes: bytes,
        audio_format: str,
        request: STTRequest,
    ) -> Tuple[str, str, List[Dict]]:
        """
        Transcription via Whisper local (placeholder)
        """
        # TODO: Implémenter avec faster-whisper ou whisper
        raise NotImplementedError("Local Whisper not yet implemented")
    
    def _transcribe_mock(
        self,
        file_bytes: bytes,
        audio_format: str,
        request: STTRequest,
    ) -> Tuple[str, str, List[Dict]]:
        """
        Transcription mock pour tests sans API
        """
        logger.warning("Using mock transcription (no API configured)")
        
        # Texte mock selon langue
        mock_texts = {
            "ar": "هذا نص تجريبي باللغة العربية الجزائرية",
            "ar-dz": "سلام خويا كيفاش راك اليوم، واش من جديد؟",
            "fr": "Ceci est un texte de test en français",
            "en": "This is a test text in English",
        }
        
        lang = request.language_hint.value if request.language_hint else "ar"
        text = mock_texts.get(lang, mock_texts["ar"])
        
        return text, lang, []
    
    # ----------------------------------------
    # DIALECT DETECTION
    # ----------------------------------------
    
    def _detect_dialect(self, text_cleaned: str, text_normalized: Optional[str] = None) -> str:
        """
        Détecte le dialecte arabe (darija, msa, mixed)
        """
        # Indicateurs darija algérienne
        darija_indicators = [
            "واش", "كيفاش", "وين", "راني", "راك", "ديرو", "نديرو",
            "خويا", "ختي", "الدار", "بزاف", "شحال", "علاش", "كاين",
            "ماكانش", "والو", "غير", "برك", "هذاك", "هذيك",
        ]
        
        # Indicateurs MSA
        msa_indicators = [
            "لقد", "إن", "هذا", "تلك", "الذي", "التي",
            "سوف", "لكن", "بينما", "حيث", "إذا", "عندما",
        ]
        
        # Indicateurs français
        french_words = [
            "le", "la", "de", "et", "en", "pour", "avec", "dans",
            "je", "tu", "il", "nous", "vous", "ils",
        ]
        
        text_check = text_normalized or text_cleaned
        words = text_check.split()
        
        darija_count = sum(1 for w in words if w in darija_indicators)
        msa_count = sum(1 for w in words if w in msa_indicators)
        french_count = sum(1 for w in words if w.lower() in french_words)
        
        total = len(words) or 1
        
        if french_count / total > 0.3:
            return "mixed"  # Mélange arabe/français
        elif darija_count > msa_count:
            return "darija"
        elif msa_count > 0:
            return "msa"
        else:
            return "darija"  # Default pour DZ
    
    # ----------------------------------------
    # HEALTH CHECK
    # ----------------------------------------
    
    async def health(self) -> STTStatus:
        """
        Vérifie l'état du service STT
        """
        openai_available = self.openai_client is not None
        local_available = self.local_whisper_model is not None
        
        # Vérifier OpenAI
        if openai_available:
            try:
                # Simple check - pas d'appel API réel
                # On pourrait faire un appel models.list() pour vérifier
                pass
            except Exception:
                openai_available = False
        
        ready = openai_available or local_available
        
        # Modèles disponibles
        available_models = []
        if openai_available:
            available_models.extend(["whisper-1", "whisper-large-v3-turbo"])
        if local_available:
            available_models.extend(["whisper-large-v3", "whisper-medium", "whisper-small"])
        
        # Backend type
        if openai_available and local_available:
            backend_type = "hybrid"
        elif openai_available:
            backend_type = "openai"
        elif local_available:
            backend_type = "local"
        else:
            backend_type = "mock"
            ready = True  # Mock toujours disponible
        
        return STTStatus(
            ready=ready,
            available_models=available_models if available_models else ["mock"],
            backend_type=backend_type,
            openai_available=openai_available,
            local_available=local_available,
            darija_nlp_ready=self.enable_darija_nlp and DARIJA_NLP_AVAILABLE,
        )


# ============================================
# SINGLETON INSTANCE
# ============================================

# Instance globale (initialisée au démarrage)
_stt_service: Optional[STTService] = None


def get_stt_service() -> STTService:
    """
    Retourne l'instance singleton du service STT
    """
    global _stt_service
    if _stt_service is None:
        _stt_service = STTService(
            use_openai=True,
            enable_darija_nlp=True,
        )
    return _stt_service


def init_stt_service(**kwargs) -> STTService:
    """
    Initialise le service STT avec configuration custom
    """
    global _stt_service
    _stt_service = STTService(**kwargs)
    return _stt_service
