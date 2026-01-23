"""
IAFactory Video Studio Pro - Service Rime AI
Synthèse vocale spécialisée pour le Darija algérien et les dialectes MENA
"""

from typing import Any, Dict, List, Literal, Optional
import asyncio
import aiohttp
import aiofiles
import logging
from pathlib import Path
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from config import settings


logger = logging.getLogger(__name__)


# === ENUMS ===

class RimeVoiceStyle(str, Enum):
    NEUTRAL = "neutral"
    HAPPY = "happy"
    SAD = "sad"
    EXCITED = "excited"
    CALM = "calm"
    PROFESSIONAL = "professional"
    STORYTELLING = "storytelling"


class RimeDialect(str, Enum):
    DARIJA_DZ = "darija_dz"  # Algérien
    DARIJA_MA = "darija_ma"  # Marocain
    DARIJA_TN = "darija_tn"  # Tunisien
    ARABIC_EG = "arabic_eg"  # Égyptien
    ARABIC_MSA = "arabic_msa"  # Arabe standard moderne
    FRENCH = "french"
    ENGLISH = "english"


# === MODÈLES ===

class RimeVoice(BaseModel):
    """Configuration d'une voix Rime."""
    voice_id: str
    name: str
    dialect: RimeDialect
    gender: Literal["male", "female"]
    age_range: str  # "young", "adult", "senior"
    style: RimeVoiceStyle = RimeVoiceStyle.NEUTRAL
    sample_url: Optional[str] = None
    description: str = ""


class RimeTTSRequest(BaseModel):
    """Requête de synthèse vocale Rime."""
    text: str
    voice_id: str
    dialect: RimeDialect = RimeDialect.DARIJA_DZ
    style: RimeVoiceStyle = RimeVoiceStyle.NEUTRAL
    speed: float = Field(1.0, ge=0.5, le=2.0)
    pitch: float = Field(1.0, ge=0.5, le=1.5)
    output_format: str = "mp3"
    sample_rate: int = 44100


class RimeTTSResponse(BaseModel):
    """Réponse de synthèse vocale Rime."""
    success: bool
    audio_path: Optional[str] = None
    audio_url: Optional[str] = None
    duration_seconds: Optional[float] = None
    characters_used: int = 0
    cost_tokens: int = 0
    dialect_used: str = ""
    error: Optional[str] = None


class VoiceCloneRequest(BaseModel):
    """Requête de clonage de voix."""
    audio_samples: List[str]  # Chemins vers les fichiers audio
    voice_name: str
    dialect: RimeDialect
    gender: Literal["male", "female"]
    description: Optional[str] = None


# === SERVICE RIME ===

class RimeService:
    """
    Service de synthèse vocale via Rime AI.
    
    Spécialisé pour:
    - Darija algérienne (dialecte principal)
    - Dialectes maghrébins
    - Arabe MENA
    - Support multilingue
    """
    
    BASE_URL = "https://api.rime.ai/v1"
    
    # Voix préconfigurées pour IAFactory
    PRESET_VOICES = {
        # Darija Algérienne
        "darija_male_youcef": RimeVoice(
            voice_id="rime-dz-youcef-v1",
            name="Youcef",
            dialect=RimeDialect.DARIJA_DZ,
            gender="male",
            age_range="adult",
            description="Voix masculine algérienne, naturelle et chaleureuse"
        ),
        "darija_female_amina": RimeVoice(
            voice_id="rime-dz-amina-v1",
            name="Amina",
            dialect=RimeDialect.DARIJA_DZ,
            gender="female",
            age_range="adult",
            description="Voix féminine algérienne, douce et expressive"
        ),
        "darija_male_karim": RimeVoice(
            voice_id="rime-dz-karim-v1",
            name="Karim",
            dialect=RimeDialect.DARIJA_DZ,
            gender="male",
            age_range="young",
            description="Voix masculine jeune, dynamique pour contenu viral"
        ),
        "darija_female_lina": RimeVoice(
            voice_id="rime-dz-lina-v1",
            name="Lina",
            dialect=RimeDialect.DARIJA_DZ,
            gender="female",
            age_range="young",
            description="Voix féminine jeune, moderne et énergique"
        ),
        
        # Arabe MSA
        "arabic_male_ahmed": RimeVoice(
            voice_id="rime-ar-ahmed-v1",
            name="Ahmed",
            dialect=RimeDialect.ARABIC_MSA,
            gender="male",
            age_range="adult",
            description="Voix arabe classique, professionnelle"
        ),
        "arabic_female_fatima": RimeVoice(
            voice_id="rime-ar-fatima-v1",
            name="Fatima",
            dialect=RimeDialect.ARABIC_MSA,
            gender="female",
            age_range="adult",
            description="Voix arabe féminine, élégante"
        ),
        
        # Français
        "french_male_pierre": RimeVoice(
            voice_id="rime-fr-pierre-v1",
            name="Pierre",
            dialect=RimeDialect.FRENCH,
            gender="male",
            age_range="adult",
            description="Voix française masculine, claire"
        ),
        "french_female_marie": RimeVoice(
            voice_id="rime-fr-marie-v1",
            name="Marie",
            dialect=RimeDialect.FRENCH,
            gender="female",
            age_range="adult",
            description="Voix française féminine, professionnelle"
        ),
    }
    
    def __init__(self):
        self.api_key = getattr(settings, 'RIME_API_KEY', '')
        self.output_dir = Path(getattr(settings, 'AUDIO_OUTPUT_DIR', '/tmp/audio'))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Fallback to ElevenLabs if Rime not configured
        self.use_elevenlabs_fallback = not self.api_key
    
    async def synthesize(self, request: RimeTTSRequest) -> RimeTTSResponse:
        """
        Synthétise du texte en audio.
        """
        if self.use_elevenlabs_fallback:
            return await self._elevenlabs_fallback(request)
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "text": request.text,
                    "voice_id": request.voice_id,
                    "dialect": request.dialect.value,
                    "style": request.style.value,
                    "speed": request.speed,
                    "pitch": request.pitch,
                    "output_format": request.output_format,
                    "sample_rate": request.sample_rate
                }
                
                async with session.post(
                    f"{self.BASE_URL}/tts",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        return RimeTTSResponse(
                            success=False,
                            error=f"Rime API error: {error_text}"
                        )
                    
                    # Sauvegarder l'audio
                    audio_data = await response.read()
                    filename = f"rime_{datetime.now().strftime('%Y%m%d%H%M%S')}.{request.output_format}"
                    audio_path = self.output_dir / filename
                    
                    async with aiofiles.open(audio_path, 'wb') as f:
                        await f.write(audio_data)
                    
                    # Calculer la durée (estimation)
                    duration = len(request.text) / 15  # ~15 chars/sec
                    
                    # Calculer le coût en tokens
                    cost = self._calculate_cost(len(request.text), request.dialect)
                    
                    return RimeTTSResponse(
                        success=True,
                        audio_path=str(audio_path),
                        duration_seconds=duration,
                        characters_used=len(request.text),
                        cost_tokens=cost,
                        dialect_used=request.dialect.value
                    )
                    
        except Exception as e:
            logger.error(f"Rime TTS error: {e}")
            return RimeTTSResponse(
                success=False,
                error=str(e)
            )
    
    async def _elevenlabs_fallback(self, request: RimeTTSRequest) -> RimeTTSResponse:
        """
        Fallback vers ElevenLabs si Rime non configuré.
        """
        from .elevenlabs_service import ElevenLabsService, TTSRequest
        
        elevenlabs = ElevenLabsService()
        
        # Mapper les voix Rime vers ElevenLabs
        voice_mapping = {
            RimeDialect.DARIJA_DZ: "ar_male",  # Utiliser voix arabe
            RimeDialect.ARABIC_MSA: "ar_male",
            RimeDialect.FRENCH: "fr_male",
            RimeDialect.ENGLISH: "en_male",
        }
        
        voice_key = voice_mapping.get(request.dialect, "fr_male")
        voice = elevenlabs.PRESET_VOICES.get(voice_key)
        
        if not voice:
            return RimeTTSResponse(success=False, error="No voice available")
        
        el_request = TTSRequest(
            text=request.text,
            voice_id=voice.voice_id,
            output_format="mp3_44100_128"
        )
        
        result = await elevenlabs.synthesize(el_request)
        
        return RimeTTSResponse(
            success=result.success,
            audio_path=result.audio_path,
            duration_seconds=result.duration_seconds,
            characters_used=result.characters_used,
            cost_tokens=result.cost_tokens,
            dialect_used=request.dialect.value,
            error=result.error
        )
    
    def _calculate_cost(self, char_count: int, dialect: RimeDialect) -> int:
        """
        Calcule le coût en IAF-Tokens.
        Tarif différencié selon le dialecte.
        """
        base_cost = char_count // 100  # 1 token / 100 chars
        
        # Dialectes premium (plus rares)
        if dialect in [RimeDialect.DARIJA_DZ, RimeDialect.DARIJA_MA, RimeDialect.DARIJA_TN]:
            return int(base_cost * 1.5)
        
        return base_cost
    
    async def get_available_voices(
        self, 
        dialect: Optional[RimeDialect] = None,
        gender: Optional[str] = None
    ) -> List[RimeVoice]:
        """
        Retourne les voix disponibles.
        """
        voices = list(self.PRESET_VOICES.values())
        
        if dialect:
            voices = [v for v in voices if v.dialect == dialect]
        
        if gender:
            voices = [v for v in voices if v.gender == gender]
        
        return voices
    
    async def get_darija_voices(self) -> List[RimeVoice]:
        """
        Retourne les voix Darija algériennes.
        """
        return await self.get_available_voices(dialect=RimeDialect.DARIJA_DZ)
    
    async def synthesize_darija(
        self,
        text: str,
        voice: str = "darija_male_youcef",
        style: RimeVoiceStyle = RimeVoiceStyle.NEUTRAL
    ) -> RimeTTSResponse:
        """
        Synthèse rapide en Darija algérienne.
        """
        voice_config = self.PRESET_VOICES.get(voice)
        if not voice_config:
            voice_config = self.PRESET_VOICES["darija_male_youcef"]
        
        request = RimeTTSRequest(
            text=text,
            voice_id=voice_config.voice_id,
            dialect=RimeDialect.DARIJA_DZ,
            style=style
        )
        
        return await self.synthesize(request)
    
    async def synthesize_multilingual(
        self,
        segments: List[Dict[str, Any]]
    ) -> List[RimeTTSResponse]:
        """
        Synthèse multilingue - traite plusieurs segments avec différentes langues.
        
        Args:
            segments: Liste de {"text": "...", "dialect": "darija_dz", "voice": "..."}
        """
        tasks = []
        
        for segment in segments:
            dialect = RimeDialect(segment.get("dialect", "darija_dz"))
            voice_key = segment.get("voice", "darija_male_youcef")
            voice = self.PRESET_VOICES.get(voice_key)
            
            if not voice:
                # Trouver une voix par défaut pour ce dialecte
                for v in self.PRESET_VOICES.values():
                    if v.dialect == dialect:
                        voice = v
                        break
            
            request = RimeTTSRequest(
                text=segment["text"],
                voice_id=voice.voice_id if voice else "default",
                dialect=dialect,
                style=RimeVoiceStyle(segment.get("style", "neutral"))
            )
            
            tasks.append(self.synthesize(request))
        
        return await asyncio.gather(*tasks)
    
    async def clone_voice(self, request: VoiceCloneRequest) -> Dict[str, Any]:
        """
        Clone une voix à partir d'échantillons audio.
        """
        if not self.api_key:
            return {"success": False, "error": "Voice cloning requires Rime API key"}
        
        try:
            # Upload des échantillons
            async with aiohttp.ClientSession() as session:
                form_data = aiohttp.FormData()
                form_data.add_field('name', request.voice_name)
                form_data.add_field('dialect', request.dialect.value)
                form_data.add_field('gender', request.gender)
                
                if request.description:
                    form_data.add_field('description', request.description)
                
                for i, sample_path in enumerate(request.audio_samples):
                    async with aiofiles.open(sample_path, 'rb') as f:
                        content = await f.read()
                        form_data.add_field(
                            f'audio_sample_{i}',
                            content,
                            filename=f'sample_{i}.wav'
                        )
                
                headers = {"Authorization": f"Bearer {self.api_key}"}
                
                async with session.post(
                    f"{self.BASE_URL}/voices/clone",
                    headers=headers,
                    data=form_data
                ) as response:
                    if response.status != 200:
                        error = await response.text()
                        return {"success": False, "error": error}
                    
                    result = await response.json()
                    return {
                        "success": True,
                        "voice_id": result.get("voice_id"),
                        "voice_name": request.voice_name,
                        "status": result.get("status", "processing")
                    }
                    
        except Exception as e:
            logger.error(f"Voice cloning error: {e}")
            return {"success": False, "error": str(e)}


# === SERVICE UNIFIÉ TTS ===

class UnifiedTTSService:
    """
    Service unifié de Text-to-Speech.
    Utilise Rime pour Darija et dialectes MENA.
    Fallback vers ElevenLabs pour les autres langues.
    """
    
    def __init__(self):
        self.rime = RimeService()
        
        # Import lazy pour éviter les imports circulaires
        self._elevenlabs = None
    
    @property
    def elevenlabs(self):
        if self._elevenlabs is None:
            from .elevenlabs_service import ElevenLabsService
            self._elevenlabs = ElevenLabsService()
        return self._elevenlabs
    
    async def synthesize(
        self,
        text: str,
        language: str = "fr",
        voice_gender: str = "male",
        style: str = "neutral"
    ) -> Dict[str, Any]:
        """
        Synthèse vocale intelligente.
        Choisit automatiquement le meilleur service.
        """
        # Darija et dialectes arabes → Rime
        if language in ["darija", "darija_dz", "ar_dz"]:
            voice_key = f"darija_{voice_gender}_youcef" if voice_gender == "male" else f"darija_{voice_gender}_amina"
            result = await self.rime.synthesize_darija(
                text=text,
                voice=voice_key,
                style=RimeVoiceStyle(style)
            )
            return result.model_dump()
        
        # Arabe classique
        if language in ["ar", "arabic", "msa"]:
            voice = self.rime.PRESET_VOICES.get(f"arabic_{voice_gender}_ahmed")
            if voice:
                request = RimeTTSRequest(
                    text=text,
                    voice_id=voice.voice_id,
                    dialect=RimeDialect.ARABIC_MSA
                )
                result = await self.rime.synthesize(request)
                return result.model_dump()
        
        # Français et autres → ElevenLabs
        from .elevenlabs_service import TTSRequest
        
        voice_key = f"{language}_{voice_gender}"
        voice = self.elevenlabs.PRESET_VOICES.get(voice_key)
        
        if voice:
            request = TTSRequest(
                text=text,
                voice_id=voice.voice_id
            )
            result = await self.elevenlabs.synthesize(request)
            return {
                "success": result.success,
                "audio_path": result.audio_path,
                "duration_seconds": result.duration_seconds,
                "cost_tokens": result.cost_tokens,
                "error": result.error
            }
        
        return {"success": False, "error": f"No voice available for {language}"}
    
    async def get_all_voices(self) -> Dict[str, List[Dict]]:
        """
        Retourne toutes les voix disponibles de tous les services.
        """
        rime_voices = await self.rime.get_available_voices()
        
        return {
            "darija": [v.model_dump() for v in rime_voices if v.dialect == RimeDialect.DARIJA_DZ],
            "arabic": [v.model_dump() for v in rime_voices if v.dialect == RimeDialect.ARABIC_MSA],
            "french": [v.model_dump() for v in rime_voices if v.dialect == RimeDialect.FRENCH],
            "english": [v.model_dump() for v in rime_voices if v.dialect == RimeDialect.ENGLISH],
        }
