from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List, Optional
from pydantic import BaseModel, Field
import logging

from app.schemas import TTSRequest, TTSResponse, VoiceResponse

# Import des services
import sys
sys.path.insert(0, '..')
from services.rime_service import (
    RimeService, 
    UnifiedTTSService, 
    RimeTTSRequest, 
    RimeDialect, 
    RimeVoiceStyle,
    VoiceCloneRequest
)
from services.elevenlabs_service import ElevenLabsService

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize services
rime_service = RimeService()
unified_tts = UnifiedTTSService()
elevenlabs = ElevenLabsService()


# ============================================
# SCHEMAS
# ============================================

class UnifiedTTSRequest(BaseModel):
    """Requête TTS unifiée."""
    text: str = Field(..., min_length=1, max_length=5000)
    language: str = Field("fr", description="Language: fr, ar, darija, en")
    voice_gender: str = Field("male", description="Gender: male, female")
    voice_id: Optional[str] = Field(None, description="Specific voice ID")
    style: str = Field("neutral", description="Style: neutral, happy, excited, calm")
    speed: float = Field(1.0, ge=0.5, le=2.0)


class DarijaTTSRequest(BaseModel):
    """Requête TTS spécifique Darija."""
    text: str = Field(..., min_length=1, max_length=5000)
    voice: str = Field("darija_male_youcef", description="Voice preset")
    style: str = Field("neutral", description="Speaking style")
    speed: float = Field(1.0, ge=0.5, le=2.0)


class MultilingualSegment(BaseModel):
    """Segment pour TTS multilingue."""
    text: str
    dialect: str = "fr"
    voice: Optional[str] = None
    style: str = "neutral"


class MultilingualTTSRequest(BaseModel):
    """Requête TTS multilingue avec plusieurs segments."""
    segments: List[MultilingualSegment]


class VoiceCloneUploadRequest(BaseModel):
    """Requête de clonage de voix."""
    voice_name: str = Field(..., min_length=2, max_length=50)
    dialect: str = Field("darija_dz")
    gender: str = Field("male")
    description: Optional[str] = None


# ============================================
# VOICES - LIST & DETAILS
# ============================================

@router.get("/voices", response_model=List[VoiceResponse], tags=["Audio - Voices"])
async def list_voices(
    language: Optional[str] = None,
    gender: Optional[str] = None
):
    """
    Liste toutes les voix disponibles.
    Inclut Rime (Darija) et ElevenLabs.
    """
    all_voices = await unified_tts.get_all_voices()
    
    result = []
    for category, voices in all_voices.items():
        for v in voices:
            if language and category != language:
                continue
            if gender and v.get("gender") != gender:
                continue
            
            result.append(VoiceResponse(
                id=v["voice_id"],
                name=v["name"],
                language=category,
                preview_url=v.get("sample_url"),
                is_custom=False,
            ))
    
    return result


@router.get("/voices/darija", tags=["Audio - Voices"])
async def list_darija_voices():
    """
    Liste les voix Darija algériennes disponibles.
    """
    voices = await rime_service.get_darija_voices()
    return {
        "count": len(voices),
        "voices": [v.model_dump() for v in voices]
    }


@router.get("/voices/{voice_id}", tags=["Audio - Voices"])
async def get_voice_details(voice_id: str):
    """
    Détails d'une voix spécifique.
    """
    # Chercher dans Rime
    for key, voice in rime_service.PRESET_VOICES.items():
        if voice.voice_id == voice_id or key == voice_id:
            return voice.model_dump()
    
    # Chercher dans ElevenLabs
    for key, voice in elevenlabs.PRESET_VOICES.items():
        if voice.voice_id == voice_id:
            return {
                "voice_id": voice.voice_id,
                "name": voice.name,
                "language": voice.language,
                "gender": voice.gender,
                "service": "elevenlabs"
            }
    
    raise HTTPException(status_code=404, detail="Voice not found")


# ============================================
# TTS - TEXT TO SPEECH
# ============================================

@router.post("/tts", response_model=TTSResponse, tags=["Audio - TTS"])
async def text_to_speech(request: UnifiedTTSRequest):
    """
    Synthèse vocale unifiée.
    Choisit automatiquement le meilleur service selon la langue.
    """
    try:
        result = await unified_tts.synthesize(
            text=request.text,
            language=request.language,
            voice_gender=request.voice_gender,
            style=request.style
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error", "TTS failed"))
        
        return TTSResponse(
            audio_url=result.get("audio_path") or result.get("audio_url"),
            duration=result.get("duration_seconds", 0),
            credits=result.get("cost_tokens", 5),
        )
        
    except Exception as e:
        logger.error(f"TTS error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tts/darija", tags=["Audio - TTS"])
async def darija_text_to_speech(request: DarijaTTSRequest):
    """
    Synthèse vocale en Darija algérienne.
    Utilise Rime AI avec voix natives.
    """
    try:
        style = RimeVoiceStyle(request.style) if request.style else RimeVoiceStyle.NEUTRAL
        
        result = await rime_service.synthesize_darija(
            text=request.text,
            voice=request.voice,
            style=style
        )
        
        if not result.success:
            raise HTTPException(status_code=500, detail=result.error)
        
        return {
            "success": True,
            "audio_path": result.audio_path,
            "audio_url": result.audio_url,
            "duration": result.duration_seconds,
            "dialect": result.dialect_used,
            "credits_used": result.cost_tokens
        }
        
    except Exception as e:
        logger.error(f"Darija TTS error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tts/multilingual", tags=["Audio - TTS"])
async def multilingual_text_to_speech(request: MultilingualTTSRequest):
    """
    Synthèse vocale multilingue avec plusieurs segments.
    Idéal pour le contenu mixte (Darija + Français + Arabe).
    """
    try:
        segments_data = [
            {
                "text": seg.text,
                "dialect": seg.dialect,
                "voice": seg.voice,
                "style": seg.style
            }
            for seg in request.segments
        ]
        
        results = await rime_service.synthesize_multilingual(segments_data)
        
        return {
            "success": True,
            "segments": [
                {
                    "index": i,
                    "audio_path": r.audio_path,
                    "duration": r.duration_seconds,
                    "dialect": r.dialect_used,
                    "success": r.success,
                    "error": r.error
                }
                for i, r in enumerate(results)
            ],
            "total_credits": sum(r.cost_tokens for r in results if r.success)
        }
        
    except Exception as e:
        logger.error(f"Multilingual TTS error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# VOICE CLONING
# ============================================

@router.post("/clone-voice", tags=["Audio - Voice Cloning"])
async def clone_voice(
    voice_name: str,
    dialect: str = "darija_dz",
    gender: str = "male",
    audio_files: List[UploadFile] = File(...)
):
    """
    Clone une voix à partir d'échantillons audio.
    Nécessite 1-5 fichiers audio de 30s-3min chacun.
    """
    try:
        # Sauvegarder les fichiers uploadés
        import tempfile
        import aiofiles
        
        audio_paths = []
        for audio_file in audio_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                content = await audio_file.read()
                tmp.write(content)
                audio_paths.append(tmp.name)
        
        # Cloner la voix
        request = VoiceCloneRequest(
            audio_samples=audio_paths,
            voice_name=voice_name,
            dialect=RimeDialect(dialect),
            gender=gender
        )
        
        result = await rime_service.clone_voice(request)
        
        # Nettoyer les fichiers temporaires
        import os
        for path in audio_paths:
            try:
                os.unlink(path)
            except:
                pass
        
        return result
        
    except Exception as e:
        logger.error(f"Voice cloning error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# UTILITIES
# ============================================

@router.get("/languages", tags=["Audio - Info"])
async def get_supported_languages():
    """
    Retourne les langues supportées pour la synthèse vocale.
    """
    return {
        "languages": [
            {"code": "darija", "name": "Darija (Algérien)", "service": "rime", "voices": 4},
            {"code": "ar", "name": "Arabe MSA", "service": "rime", "voices": 2},
            {"code": "fr", "name": "Français", "service": "elevenlabs", "voices": 2},
            {"code": "en", "name": "English", "service": "elevenlabs", "voices": 2},
        ],
        "default": "fr",
        "recommended_for_algeria": "darija"
    }


@router.get("/pricing", tags=["Audio - Info"])
async def get_tts_pricing():
    """
    Retourne la grille tarifaire TTS en IAF-Tokens.
    """
    return {
        "pricing": {
            "darija": {
                "per_100_chars": 1.5,
                "description": "Voix Darija algérienne premium"
            },
            "arabic": {
                "per_100_chars": 1.0,
                "description": "Arabe standard moderne"
            },
            "french": {
                "per_100_chars": 0.8,
                "description": "Français haute qualité"
            },
            "english": {
                "per_100_chars": 0.8,
                "description": "Anglais international"
            }
        },
        "voice_cloning": {
            "cost": 50,
            "description": "Clonage de voix personnalisée"
        }
    }

