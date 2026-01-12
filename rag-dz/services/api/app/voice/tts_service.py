"""
TTS_VOICE - Service Text-to-Speech
==================================
Synthèse vocale pour arabe/darija/français/anglais
Architecture extensible multi-backend

BACKENDS SUPPORTÉS:
- mock: Placeholder (pas de vrai TTS)
- openai: OpenAI TTS API (alloy, echo, fable, onyx, nova, shimmer)
- elevenlabs: ElevenLabs API (voix arabes haute qualité)
- coqui: Coqui XTTS local (multilingue, voice cloning)
- gtts: Google TTS (gratuit, basique)

LANGUES:
- ar/ar-dz: Arabe/Darija (ElevenLabs, Coqui XTTS)
- fr: Français
- en: Anglais
- de/it: Allemand/Italien (pour Suisse)
"""

import os
import io
import base64
import time
import logging
import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime

# HTTP client
import httpx

# Audio processing (optionnel)
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

# Coqui TTS (local)
try:
    from TTS.api import TTS as CoquiTTS
    import torch
    COQUI_AVAILABLE = True
except ImportError:
    COQUI_AVAILABLE = False

# gTTS (Google TTS gratuit)
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

# Models
from .tts_models import (
    TTSRequest,
    TTSResponse,
    TTSStatus,
    TTSSimpleRequest,
    TTSVoice,
    TTSBatchRequest,
    TTSBatchResponse,
    TTSBatchResultItem,
    TTSLanguage,
    TTSDialect,
    TTSBackend,
    TTSEmotion,
    AudioFormat,
    DEFAULT_VOICES,
    FORMAT_MIME_TYPES,
    MAX_TEXT_LENGTH,
)

# DARIJA_NLP integration (pour normaliser le texte avant TTS)
try:
    from app.darija.darija_normalizer import normalize_darija
    from app.darija.darija_cleaner import clean_text
    DARIJA_NLP_AVAILABLE = True
except ImportError:
    DARIJA_NLP_AVAILABLE = False
    def normalize_darija(text: str) -> Dict[str, Any]:
        return {"normalized": text}
    def clean_text(text: str) -> str:
        return text.strip()


logger = logging.getLogger(__name__)


# ============================================
# ELEVENLABS CONFIGURATION
# ============================================

# Voix ElevenLabs pré-configurées
ELEVENLABS_VOICES = {
    # Voix arabes
    "rachel": "21m00Tcm4TlvDq8ikWAM",      # Rachel - Femme anglaise (fallback)
    "adam": "pNInz6obpgDQGcFmaJgB",         # Adam - Homme anglais (fallback)
    "antoni": "ErXwobaYiN019PkySvjV",       # Antoni - Homme
    "bella": "EXAVITQu4vr4xnSDxMaL",        # Bella - Femme
    "elli": "MF3mGyEYCl7XYWbV9V6O",         # Elli - Femme
    "josh": "TxGEqnHWrfWFTfGW9XjX",         # Josh - Homme
    "sam": "yoZ06aMxZJJ28mfd3POQ",          # Sam - Homme
    "domi": "AZnzlk1XvdvUeBnXmlld",         # Domi - Femme
    "arnold": "VR6AewLTigWG4xSOukaG",       # Arnold - Homme narrateur
    "callum": "N2lVS1w4EtoT3dr4eOWO",       # Callum - Homme
    # Voix multilingues (arabe supporté)
    "charlotte": "XB0fDUnXU5powFXDhCwa",    # Charlotte - Femme multilingue
    "matilda": "XrExE9yKIg1WjnnlVkGX",      # Matilda - Femme multilingue
    "brian": "nPczCjzI2devNBz1zQrb",        # Brian - Homme multilingue
}

# Mapping langue vers voix par défaut ElevenLabs
ELEVENLABS_DEFAULT_VOICE = {
    "ar": "charlotte",    # Multilingue avec arabe
    "ar-dz": "charlotte",
    "fr": "charlotte",
    "en": "rachel",
    "de": "matilda",
    "it": "matilda",
}

# ============================================
# OPENAI TTS CONFIGURATION
# ============================================

OPENAI_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
OPENAI_MODELS = ["tts-1", "tts-1-hd"]

# Mapping langue vers voix OpenAI
OPENAI_DEFAULT_VOICE = {
    "ar": "nova",
    "ar-dz": "nova",
    "fr": "alloy",
    "en": "alloy",
}


# ============================================
# AUDIO UTILITIES
# ============================================

def generate_silence_audio(duration_sec: float, sample_rate: int = 22050, format: str = "mp3") -> bytes:
    """
    Génère un audio silencieux
    
    Args:
        duration_sec: Durée en secondes
        sample_rate: Taux d'échantillonnage
        format: Format audio (mp3, wav)
        
    Returns:
        Bytes audio
    """
    if PYDUB_AVAILABLE:
        silence = AudioSegment.silent(duration=int(duration_sec * 1000))
        buffer = io.BytesIO()
        silence.export(buffer, format=format)
        return buffer.getvalue()
    else:
        # Fallback: retourne des bytes vides
        return b""


def audio_bytes_to_base64(audio_bytes: bytes) -> str:
    """Convertit des bytes audio en base64"""
    return base64.b64encode(audio_bytes).decode('utf-8')


def base64_to_audio_bytes(audio_base64: str) -> bytes:
    """Convertit du base64 en bytes audio"""
    return base64.b64decode(audio_base64)


def estimate_audio_duration(text: str, speed: float = 1.0) -> float:
    """
    Estime la durée audio basée sur le texte
    
    Approximation: ~150 mots/minute en arabe, ~180 en français
    """
    words = len(text.split())
    # ~2.5 caractères/seconde en moyenne
    chars = len(text)
    duration = chars / 15.0  # ~15 chars/sec
    return duration / speed


# ============================================
# TTS SERVICE
# ============================================

class TTSService:
    """
    Service de Text-to-Speech multi-backend
    
    Architecture extensible pour brancher différents providers:
    - mock: Placeholder (pas de vrai TTS)
    - openai: OpenAI TTS API
    - elevenlabs: ElevenLabs API  
    - coqui: Coqui TTS local
    - gtts: Google TTS
    - azure: Azure Speech
    
    Pour l'instant, seul le backend 'mock' est implémenté.
    Les autres seront ajoutés selon les besoins.
    """
    
    def __init__(
        self,
        backend_type: str = "mock",
        openai_api_key: Optional[str] = None,
        elevenlabs_api_key: Optional[str] = None,
        enable_darija_nlp: bool = True,
    ):
        """
        Initialise le service TTS
        
        Args:
            backend_type: Type de backend (mock, openai, elevenlabs, coqui, gtts)
            openai_api_key: Clé API OpenAI (optionnel)
            elevenlabs_api_key: Clé API ElevenLabs (optionnel)
            enable_darija_nlp: Activer normalisation texte via DARIJA_NLP
        """
        self.backend_type = backend_type
        self.enable_darija_nlp = enable_darija_nlp and DARIJA_NLP_AVAILABLE
        
        # API Keys
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.elevenlabs_api_key = elevenlabs_api_key or os.getenv("ELEVENLABS_API_KEY")
        
        # Clients (à initialiser selon le backend)
        self.openai_client = None
        self.elevenlabs_client = None
        self.coqui_model = None
        
        # Voix disponibles
        self.voices: Dict[str, TTSVoice] = {v.id: v for v in DEFAULT_VOICES}
        
        logger.info(f"TTSService initialized - Backend: {backend_type}, DARIJA_NLP: {self.enable_darija_nlp}")
    
    # ----------------------------------------
    # MAIN SYNTHESIS METHOD
    # ----------------------------------------
    
    async def synthesize(self, request: TTSRequest) -> TTSResponse:
        """
        Synthèse vocale principale
        
        Pipeline:
        1. Validation texte
        2. Normalisation texte (si arabe/darija + DARIJA_NLP actif)
        3. Sélection voix
        4. Synthèse via backend
        5. Post-processing audio (silence, etc.)
        6. Encodage base64
        
        Args:
            request: Requête TTS avec texte et options
            
        Returns:
            TTSResponse avec audio en base64
        """
        start_time = time.time()
        
        # 1. Validation
        text = request.text.strip()
        if not text:
            raise ValueError("Le texte ne peut pas être vide")
        
        if len(text) > MAX_TEXT_LENGTH:
            raise ValueError(f"Texte trop long: {len(text)} caractères (max {MAX_TEXT_LENGTH})")
        
        # 2. Normalisation texte arabe/darija
        if self.enable_darija_nlp and request.language == TTSLanguage.ARABIC:
            try:
                # Nettoyer le texte
                text = clean_text(text)
                
                # Normaliser darija si nécessaire
                if request.dialect == TTSDialect.DARIJA:
                    norm_result = normalize_darija(text)
                    text = norm_result.get("normalized", text)
                    logger.debug(f"Text normalized for TTS: {text[:50]}...")
            except Exception as e:
                logger.warning(f"Text normalization failed: {e}")
        
        # 3. Sélection voix
        voice = self._select_voice(request.voice_id, request.language, request.dialect)
        
        # 4. Synthèse via backend
        audio_bytes = await self._synthesize_backend(
            text=text,
            request=request,
            voice=voice,
        )
        
        # 5. Post-processing
        if request.add_silence_start > 0 or request.add_silence_end > 0:
            audio_bytes = self._add_silence(
                audio_bytes,
                request.add_silence_start,
                request.add_silence_end,
                request.format.value,
            )
        
        # 6. Encodage base64
        audio_base64 = audio_bytes_to_base64(audio_bytes)
        
        # Calcul durée estimée
        duration_sec = estimate_audio_duration(text, request.speed)
        
        # Processing time
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        return TTSResponse(
            audio_base64=audio_base64,
            mime_type=FORMAT_MIME_TYPES.get(request.format, "audio/mpeg"),
            language=request.language.value,
            dialect=request.dialect.value if request.dialect else None,
            used_voice_id=voice.id if voice else "default",
            used_backend=self.backend_type,
            duration_sec=duration_sec,
            char_count=len(text),
            processing_time_ms=processing_time_ms,
            format=request.format.value,
            sample_rate=request.sample_rate,
        )
    
    async def synthesize_simple(self, text: str, language: str = "ar") -> TTSResponse:
        """
        Synthèse vocale simplifiée
        
        Args:
            text: Texte à synthétiser
            language: Langue (ar, fr, en)
            
        Returns:
            TTSResponse
        """
        request = TTSRequest(
            text=text,
            language=TTSLanguage(language) if language in ["ar", "fr", "en"] else TTSLanguage.ARABIC,
            dialect=TTSDialect.DARIJA if language == "ar" else None,
        )
        return await self.synthesize(request)
    
    # ----------------------------------------
    # BACKEND SYNTHESIS
    # ----------------------------------------
    
    async def _synthesize_backend(
        self,
        text: str,
        request: TTSRequest,
        voice: Optional[TTSVoice],
    ) -> bytes:
        """
        Synthèse via le backend approprié
        
        Returns:
            Audio bytes
        """
        if self.backend_type == "mock":
            return self._synthesize_mock(text, request, voice)
        elif self.backend_type == "openai":
            return await self._synthesize_openai(text, request, voice)
        elif self.backend_type == "elevenlabs":
            return await self._synthesize_elevenlabs(text, request, voice)
        elif self.backend_type == "coqui":
            return await self._synthesize_coqui(text, request, voice)
        elif self.backend_type == "gtts":
            return await self._synthesize_gtts(text, request, voice)
        else:
            return self._synthesize_mock(text, request, voice)
    
    def _synthesize_mock(
        self,
        text: str,
        request: TTSRequest,
        voice: Optional[TTSVoice],
    ) -> bytes:
        """
        Backend MOCK - génère un placeholder audio
        
        Pour les tests et le développement sans vrai TTS.
        Génère un court silence ou des bytes vides.
        """
        logger.info(f"Mock TTS: '{text[:50]}...' (lang={request.language}, voice={voice.id if voice else 'default'})")
        
        # Générer un silence de la durée estimée
        duration = estimate_audio_duration(text, request.speed)
        duration = min(duration, 5.0)  # Max 5 sec pour le mock
        
        if PYDUB_AVAILABLE:
            return generate_silence_audio(duration, request.sample_rate, request.format.value)
        else:
            # Retourne des bytes vides (placeholder)
            return b""
    
    async def _synthesize_openai(
        self,
        text: str,
        request: TTSRequest,
        voice: Optional[TTSVoice],
    ) -> bytes:
        """
        Backend OpenAI TTS
        
        Voix disponibles: alloy, echo, fable, onyx, nova, shimmer
        Modèles: tts-1 (rapide), tts-1-hd (qualité)
        """
        if not OPENAI_AVAILABLE or not self.openai_api_key:
            logger.warning("OpenAI TTS not available, falling back to mock")
            return self._synthesize_mock(text, request, voice)
        
        try:
            client = AsyncOpenAI(api_key=self.openai_api_key)
            
            # Sélection voix
            openai_voice = "nova"  # Défaut
            if voice and voice.provider_voice_id:
                openai_voice = voice.provider_voice_id
            elif request.language:
                openai_voice = OPENAI_DEFAULT_VOICE.get(request.language.value, "nova")
            
            # Valider la voix
            if openai_voice not in OPENAI_VOICES:
                openai_voice = "nova"
            
            # Synthèse
            response = await client.audio.speech.create(
                model="tts-1",  # ou tts-1-hd pour qualité
                voice=openai_voice,
                input=text,
                response_format="mp3",
                speed=request.speed,
            )
            
            # Lire le contenu
            audio_bytes = response.content
            
            logger.info(f"OpenAI TTS success: {len(audio_bytes)} bytes, voice={openai_voice}")
            return audio_bytes
            
        except Exception as e:
            logger.error(f"OpenAI TTS error: {e}")
            return self._synthesize_mock(text, request, voice)
    
    async def _synthesize_elevenlabs(
        self,
        text: str,
        request: TTSRequest,
        voice: Optional[TTSVoice],
    ) -> bytes:
        """
        Backend ElevenLabs TTS
        
        API haute qualité avec support multilingue (arabe inclus)
        Documentation: https://docs.elevenlabs.io/api-reference
        """
        if not self.elevenlabs_api_key:
            logger.warning("ElevenLabs API key not set, falling back to mock")
            return self._synthesize_mock(text, request, voice)
        
        try:
            logger.info(f"ElevenLabs: synthesizing '{text[:30]}...' lang={request.language}")
            
            # Sélection voix
            voice_name = "charlotte"  # Défaut multilingue
            if voice and voice.provider_voice_id:
                voice_name = voice.provider_voice_id
            elif request.language:
                voice_name = ELEVENLABS_DEFAULT_VOICE.get(request.language.value, "charlotte")
            
            logger.info(f"ElevenLabs: using voice {voice_name}")
            
            # Obtenir l'ID de la voix
            voice_id = ELEVENLABS_VOICES.get(voice_name, ELEVENLABS_VOICES["charlotte"])
            
            # Configuration voix
            voice_settings = {
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": 0.0,
                "use_speaker_boost": True,
            }
            
            # Ajuster selon l'émotion (avec protection)
            try:
                if hasattr(request, 'emotion') and request.emotion:
                    if request.emotion == TTSEmotion.FORMAL:
                        voice_settings["stability"] = 0.7
                    elif request.emotion == TTSEmotion.FRIENDLY:
                        voice_settings["stability"] = 0.3
                        voice_settings["style"] = 0.3
            except Exception as e:
                logger.warning(f"Emotion handling error: {e}")
            
            # Appel API
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                    headers={
                        "xi-api-key": self.elevenlabs_api_key,
                        "Content-Type": "application/json",
                        "Accept": "audio/mpeg",
                    },
                    json={
                        "text": text,
                        "model_id": "eleven_multilingual_v2",  # Supporte arabe!
                        "voice_settings": voice_settings,
                    },
                )
                
                if response.status_code != 200:
                    logger.error(f"ElevenLabs error {response.status_code}: {response.text}")
                    return self._synthesize_mock(text, request, voice)
                
                audio_bytes = response.content
                logger.info(f"ElevenLabs TTS success: {len(audio_bytes)} bytes, voice={voice_name}")
                return audio_bytes
            
        except Exception as e:
            logger.error(f"ElevenLabs TTS error: {e}")
            return self._synthesize_mock(text, request, voice)
    
    async def _synthesize_coqui(
        self,
        text: str,
        request: TTSRequest,
        voice: Optional[TTSVoice],
    ) -> bytes:
        """
        Backend Coqui TTS (local)
        
        Utilise XTTS v2 pour synthèse multilingue de haute qualité
        Supporte l'arabe avec voice cloning
        """
        if not COQUI_AVAILABLE:
            logger.warning("Coqui TTS not available, falling back to mock")
            return self._synthesize_mock(text, request, voice)
        
        try:
            # Initialiser le modèle si nécessaire
            if self.coqui_model is None:
                device = "cuda" if torch.cuda.is_available() else "cpu"
                self.coqui_model = CoquiTTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
                logger.info(f"Coqui XTTS loaded on {device}")
            
            # Mapper la langue
            lang_map = {
                "ar": "ar",
                "ar-dz": "ar",
                "fr": "fr",
                "en": "en",
                "de": "de",
                "it": "it",
            }
            language = lang_map.get(request.language.value, "en")
            
            # Fichier de référence pour cloning (optionnel)
            speaker_wav = None
            if voice and voice.sample_url:
                speaker_wav = voice.sample_url
            
            # Synthèse (synchrone, dans executor)
            loop = asyncio.get_event_loop()
            
            def run_tts():
                buffer = io.BytesIO()
                if speaker_wav:
                    # Voice cloning
                    self.coqui_model.tts_to_file(
                        text=text,
                        speaker_wav=speaker_wav,
                        language=language,
                        file_path=buffer,
                    )
                else:
                    # Voix par défaut
                    wav = self.coqui_model.tts(text=text, language=language)
                    # Convertir en bytes (wav)
                    import numpy as np
                    import wave
                    buffer = io.BytesIO()
                    with wave.open(buffer, 'wb') as wf:
                        wf.setnchannels(1)
                        wf.setsampwidth(2)
                        wf.setframerate(22050)
                        wf.writeframes((np.array(wav) * 32767).astype(np.int16).tobytes())
                return buffer.getvalue()
            
            audio_bytes = await loop.run_in_executor(None, run_tts)
            
            logger.info(f"Coqui TTS success: {len(audio_bytes)} bytes, lang={language}")
            return audio_bytes
            
        except Exception as e:
            logger.error(f"Coqui TTS error: {e}")
            return self._synthesize_mock(text, request, voice)
    
    async def _synthesize_gtts(
        self,
        text: str,
        request: TTSRequest,
        voice: Optional[TTSVoice],
    ) -> bytes:
        """
        Backend gTTS (Google TTS gratuit)
        
        Qualité basique mais gratuit et simple
        """
        if not GTTS_AVAILABLE:
            logger.warning("gTTS not available, falling back to mock")
            return self._synthesize_mock(text, request, voice)
        
        try:
            # Mapper la langue
            lang_map = {
                "ar": "ar",
                "ar-dz": "ar",  # gTTS ne supporte pas les dialectes
                "fr": "fr",
                "en": "en",
                "de": "de",
                "it": "it",
            }
            language = lang_map.get(request.language.value, "en")
            
            # Synthèse (synchrone, dans executor)
            loop = asyncio.get_event_loop()
            
            def run_gtts():
                tts = gTTS(text=text, lang=language, slow=request.speed < 0.9)
                buffer = io.BytesIO()
                tts.write_to_fp(buffer)
                buffer.seek(0)
                return buffer.read()
            
            audio_bytes = await loop.run_in_executor(None, run_gtts)
            
            logger.info(f"gTTS success: {len(audio_bytes)} bytes, lang={language}")
            return audio_bytes
            
        except Exception as e:
            logger.error(f"gTTS error: {e}")
            return self._synthesize_mock(text, request, voice)
    
    # ----------------------------------------
    # VOICE SELECTION
    # ----------------------------------------
    
    def _select_voice(
        self,
        voice_id: Optional[str],
        language: TTSLanguage,
        dialect: Optional[TTSDialect],
    ) -> Optional[TTSVoice]:
        """
        Sélectionne la voix appropriée
        """
        # Si voice_id spécifié
        if voice_id and voice_id in self.voices:
            return self.voices[voice_id]
        
        # Sinon, sélection par langue/dialecte
        for voice in self.voices.values():
            if voice.language == language:
                if dialect and voice.dialect == dialect:
                    return voice
                elif not dialect:
                    return voice
        
        # Voix par défaut
        return self.voices.get("default")
    
    def get_available_voices(self, language: Optional[str] = None) -> List[TTSVoice]:
        """
        Retourne les voix disponibles
        """
        voices = list(self.voices.values())
        
        if language:
            voices = [v for v in voices if v.language.value == language]
        
        return voices
    
    # ----------------------------------------
    # POST-PROCESSING
    # ----------------------------------------
    
    def _add_silence(
        self,
        audio_bytes: bytes,
        start_silence: float,
        end_silence: float,
        format: str,
    ) -> bytes:
        """
        Ajoute du silence au début et/ou à la fin de l'audio
        """
        if not PYDUB_AVAILABLE or not audio_bytes:
            return audio_bytes
        
        try:
            # Charger l'audio
            audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format=format)
            
            # Ajouter silence au début
            if start_silence > 0:
                silence_start = AudioSegment.silent(duration=int(start_silence * 1000))
                audio = silence_start + audio
            
            # Ajouter silence à la fin
            if end_silence > 0:
                silence_end = AudioSegment.silent(duration=int(end_silence * 1000))
                audio = audio + silence_end
            
            # Exporter
            buffer = io.BytesIO()
            audio.export(buffer, format=format)
            return buffer.getvalue()
            
        except Exception as e:
            logger.warning(f"Failed to add silence: {e}")
            return audio_bytes
    
    # ----------------------------------------
    # BATCH PROCESSING
    # ----------------------------------------
    
    async def synthesize_batch(self, batch_request: TTSBatchRequest) -> TTSBatchResponse:
        """
        Synthèse batch (plusieurs textes)
        """
        start_time = time.time()
        results: List[TTSBatchResultItem] = []
        total_duration = 0.0
        
        for item in batch_request.items:
            try:
                request = TTSRequest(
                    text=item.text,
                    language=TTSLanguage(item.language) if item.language else TTSLanguage.ARABIC,
                    voice_id=item.voice_id,
                    format=batch_request.format,
                )
                
                response = await self.synthesize(request)
                
                results.append(TTSBatchResultItem(
                    id=item.id,
                    success=True,
                    audio_base64=response.audio_base64,
                    duration_sec=response.duration_sec,
                ))
                total_duration += response.duration_sec
                
            except Exception as e:
                results.append(TTSBatchResultItem(
                    id=item.id,
                    success=False,
                    error=str(e),
                ))
        
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        return TTSBatchResponse(
            items=results,
            total=len(results),
            success_count=sum(1 for r in results if r.success),
            error_count=sum(1 for r in results if not r.success),
            total_duration_sec=total_duration,
            processing_time_ms=processing_time_ms,
        )
    
    # ----------------------------------------
    # HEALTH CHECK
    # ----------------------------------------
    
    async def health(self) -> TTSStatus:
        """
        Vérifie l'état du service TTS
        """
        # Vérifier les backends
        backends_status = {
            "mock": True,  # Toujours disponible
            "openai": self.openai_api_key is not None,
            "elevenlabs": self.elevenlabs_api_key is not None,
            "coqui": self.coqui_model is not None,
            "gtts": True,  # Gratuit, toujours disponible
        }
        
        # Voix disponibles
        available_voices = [v.id for v in self.voices.values() if v.is_available]
        
        return TTSStatus(
            ready=True,  # Mock toujours prêt
            available_voices=available_voices,
            backend_type=self.backend_type,
            backends_status=backends_status,
        )


# ============================================
# SINGLETON INSTANCE
# ============================================

_tts_service: Optional[TTSService] = None


def get_tts_service() -> TTSService:
    """
    Retourne l'instance singleton du service TTS
    
    Priority de backend:
    1. ElevenLabs si clé disponible (meilleure qualité arabe)
    2. OpenAI si clé disponible
    3. gTTS (gratuit)
    4. Mock (fallback)
    """
    global _tts_service
    if _tts_service is None:
        # Détecter le meilleur backend disponible
        elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")
        
        if elevenlabs_key:
            backend = "elevenlabs"
            logger.info("TTS: Using ElevenLabs (best quality for Arabic)")
        elif openai_key:
            backend = "openai"
            logger.info("TTS: Using OpenAI TTS")
        elif GTTS_AVAILABLE:
            backend = "gtts"
            logger.info("TTS: Using gTTS (free)")
        else:
            backend = "mock"
            logger.info("TTS: Using mock (no TTS backend available)")
        
        _tts_service = TTSService(
            backend_type=backend,
            elevenlabs_api_key=elevenlabs_key,
            openai_api_key=openai_key,
            enable_darija_nlp=True,
        )
    return _tts_service


def init_tts_service(**kwargs) -> TTSService:
    """
    Initialise le service TTS avec configuration custom
    """
    global _tts_service
    _tts_service = TTSService(**kwargs)
    return _tts_service
