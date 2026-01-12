"""
IAFactory Video Studio Pro - Service ElevenLabs
Synthèse vocale haute qualité multilingue
"""

from typing import Any, Dict, List, Literal, Optional
import asyncio
import aiohttp
import aiofiles
import logging
from pathlib import Path
from datetime import datetime

from pydantic import BaseModel, Field

from config import settings


logger = logging.getLogger(__name__)


# === MODÈLES ===

class VoiceConfig(BaseModel):
    """Configuration d'une voix."""
    voice_id: str
    name: str
    language: str
    gender: Literal["male", "female", "neutral"]
    style: Optional[str] = None


class TTSRequest(BaseModel):
    """Requête de synthèse vocale."""
    text: str
    voice_id: str
    model_id: str = "eleven_multilingual_v2"
    stability: float = 0.5
    similarity_boost: float = 0.75
    style: float = 0.0
    use_speaker_boost: bool = True
    output_format: str = "mp3_44100_128"


class TTSResponse(BaseModel):
    """Réponse de synthèse vocale."""
    success: bool
    audio_path: Optional[str] = None
    duration_seconds: Optional[float] = None
    characters_used: int = 0
    cost_tokens: int = 0
    error: Optional[str] = None


# === SERVICE ELEVENLABS ===

class ElevenLabsService:
    """
    Service de synthèse vocale via ElevenLabs.
    
    Fonctionnalités:
    - Text-to-Speech multilingue
    - Clonage de voix
    - Voix émotionnelles
    - Support Arabe et Darija
    """
    
    BASE_URL = "https://api.elevenlabs.io/v1"
    
    # Voix préconfigurées
    PRESET_VOICES = {
        "fr_male": VoiceConfig(
            voice_id="pNInz6obpgDQGcFmaJgB",  # Adam
            name="Adam (FR)",
            language="fr",
            gender="male"
        ),
        "fr_female": VoiceConfig(
            voice_id="EXAVITQu4vr4xnSDxMaL",  # Bella
            name="Bella (FR)",
            language="fr",
            gender="female"
        ),
        "ar_male": VoiceConfig(
            voice_id="VR6AewLTigWG4xSOukaG",  # Arabic Male
            name="Ahmad (AR)",
            language="ar",
            gender="male"
        ),
        "ar_female": VoiceConfig(
            voice_id="jBpfuIE2acCO8z3wKNLl",  # Arabic Female
            name="Fatima (AR)",
            language="ar",
            gender="female"
        ),
        "en_male": VoiceConfig(
            voice_id="TxGEqnHWrfWFTfGW9XjX",  # Josh
            name="Josh (EN)",
            language="en",
            gender="male"
        ),
        "en_female": VoiceConfig(
            voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel
            name="Rachel (EN)",
            language="en",
            gender="female"
        ),
    }
    
    def __init__(self):
        self.api_key = settings.ELEVENLABS_API_KEY
        self.headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json",
        }
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Retourne une session HTTP réutilisable."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(headers=self.headers)
        return self._session
    
    async def close(self):
        """Ferme la session HTTP."""
        if self._session and not self._session.closed:
            await self._session.close()
    
    async def text_to_speech(
        self,
        text: str,
        voice_preset: str = "fr_male",
        voice_id: Optional[str] = None,
        model: str = "eleven_multilingual_v2",
        stability: float = 0.5,
        similarity_boost: float = 0.75,
        style: float = 0.0,
        output_path: Optional[str] = None,
    ) -> TTSResponse:
        """
        Convertit du texte en audio.
        
        Args:
            text: Texte à convertir
            voice_preset: Preset de voix (fr_male, ar_female, etc.)
            voice_id: ID de voix personnalisée (optionnel)
            model: Modèle TTS
            stability: Stabilité de la voix (0-1)
            similarity_boost: Boost de similarité (0-1)
            style: Style de la voix (0-1)
            output_path: Chemin de sortie (optionnel)
            
        Returns:
            TTSResponse avec le chemin audio
        """
        try:
            # Déterminer l'ID de voix
            if voice_id is None:
                voice_config = self.PRESET_VOICES.get(voice_preset)
                if voice_config is None:
                    return TTSResponse(
                        success=False,
                        error=f"Preset de voix inconnu: {voice_preset}"
                    )
                voice_id = voice_config.voice_id
            
            # Préparer la requête
            url = f"{self.BASE_URL}/text-to-speech/{voice_id}"
            
            payload = {
                "text": text,
                "model_id": model,
                "voice_settings": {
                    "stability": stability,
                    "similarity_boost": similarity_boost,
                    "style": style,
                    "use_speaker_boost": True
                }
            }
            
            logger.info(f"[ElevenLabs] TTS request: {len(text)} chars, voice={voice_id}")
            
            session = await self._get_session()
            
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"[ElevenLabs] Erreur API: {response.status} - {error_text}")
                    return TTSResponse(
                        success=False,
                        error=f"API Error {response.status}: {error_text}"
                    )
                
                # Lire l'audio
                audio_data = await response.read()
                
                # Générer le chemin de sortie si non fourni
                if output_path is None:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_path = f"/tmp/tts_{timestamp}.mp3"
                
                # Sauvegarder le fichier
                async with aiofiles.open(output_path, "wb") as f:
                    await f.write(audio_data)
                
                # Estimer la durée (approximatif: 150 mots/minute)
                word_count = len(text.split())
                duration_seconds = (word_count / 150) * 60
                
                # Calculer le coût (30 tokens par minute)
                cost_tokens = int((duration_seconds / 60) * 30)
                
                logger.info(
                    f"[ElevenLabs] TTS success: {output_path} - "
                    f"~{duration_seconds:.1f}s - {cost_tokens} tokens"
                )
                
                return TTSResponse(
                    success=True,
                    audio_path=output_path,
                    duration_seconds=duration_seconds,
                    characters_used=len(text),
                    cost_tokens=cost_tokens
                )
                
        except Exception as e:
            logger.error(f"[ElevenLabs] Exception: {str(e)}")
            return TTSResponse(
                success=False,
                error=str(e)
            )
    
    async def get_voices(self) -> List[Dict[str, Any]]:
        """Récupère la liste des voix disponibles."""
        try:
            session = await self._get_session()
            
            async with session.get(f"{self.BASE_URL}/voices") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("voices", [])
                else:
                    logger.error(f"[ElevenLabs] Erreur récupération voix: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"[ElevenLabs] Exception get_voices: {str(e)}")
            return []
    
    async def clone_voice(
        self,
        name: str,
        audio_files: List[str],
        description: Optional[str] = None
    ) -> Optional[str]:
        """
        Clone une voix à partir d'échantillons audio.
        
        Args:
            name: Nom de la voix clonée
            audio_files: Chemins vers les fichiers audio
            description: Description de la voix
            
        Returns:
            ID de la voix clonée ou None
        """
        try:
            url = f"{self.BASE_URL}/voices/add"
            
            # Préparer le form-data
            data = aiohttp.FormData()
            data.add_field("name", name)
            if description:
                data.add_field("description", description)
            
            for audio_path in audio_files:
                async with aiofiles.open(audio_path, "rb") as f:
                    audio_data = await f.read()
                    data.add_field(
                        "files",
                        audio_data,
                        filename=Path(audio_path).name,
                        content_type="audio/mpeg"
                    )
            
            session = await self._get_session()
            
            # Headers spéciaux pour form-data
            headers = {"xi-api-key": self.api_key}
            
            async with session.post(url, data=data, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    voice_id = result.get("voice_id")
                    logger.info(f"[ElevenLabs] Voix clonée: {name} -> {voice_id}")
                    return voice_id
                else:
                    error_text = await response.text()
                    logger.error(f"[ElevenLabs] Erreur clonage: {error_text}")
                    return None
                    
        except Exception as e:
            logger.error(f"[ElevenLabs] Exception clone_voice: {str(e)}")
            return None
    
    async def get_subscription_info(self) -> Dict[str, Any]:
        """Récupère les infos d'abonnement (quota restant, etc.)."""
        try:
            session = await self._get_session()
            
            async with session.get(f"{self.BASE_URL}/user/subscription") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {}
                    
        except Exception as e:
            logger.error(f"[ElevenLabs] Exception subscription: {str(e)}")
            return {}


# === FACTORY FUNCTION ===

_elevenlabs_service: Optional[ElevenLabsService] = None

def get_elevenlabs_service() -> ElevenLabsService:
    """Retourne l'instance singleton du service ElevenLabs."""
    global _elevenlabs_service
    if _elevenlabs_service is None:
        _elevenlabs_service = ElevenLabsService()
    return _elevenlabs_service
