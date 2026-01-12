"""
IAFactory Video Studio Pro - API Routes pour l'Audio
"""

from typing import List, Optional, Literal
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
import logging
from pathlib import Path
import aiofiles

from ...services.elevenlabs_service import ElevenLabsService, get_elevenlabs_service, TTSRequest, TTSResponse, VoiceConfig
from ...services.rime_service import RimeService, get_rime_service, RimeTTSRequest, RimeTTSResponse

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/audio",
    tags=["Audio"],
)


# === MODÈLES DE REQUÊTES & RÉPONSES ===

class TTSGenerateRequest(BaseModel):
    """Requête pour générer de la synthèse vocale."""
    provider: Literal["elevenlabs", "rime"] = "elevenlabs"
    text: str = Field(..., example="Bonjour, ceci est un test de synthèse vocale.")
    voice_id: Optional[str] = Field(None, example="fr_male")
    model_id: Optional[str] = None


class MusicGenerateRequest(BaseModel):
    """Requête pour générer de la musique."""
    prompt: str = Field(..., example="Musique épique et entraînante pour une intro de vidéo.")
    duration_seconds: int = Field(30, ge=10, le=120)
    mood: Optional[str] = None


class VoiceCloneRequest(BaseModel):
    """Requête pour cloner une voix."""
    name: str = Field(..., example="Ma Voix Personnelle")
    description: Optional[str] = None
    # Les fichiers audio seront passés via UploadFile


# === DÉPENDANCES ===

async def get_elevenlabs() -> ElevenLabsService:
    return get_elevenlabs_service()

async def get_rime() -> RimeService:
    return get_rime_service()


# === ROUTES ===

@router.post("/tts", response_model=TTSResponse, status_code=status.HTTP_201_CREATED)
async def generate_tts(
    request: TTSGenerateRequest,
    elevenlabs_service: ElevenLabsService = Depends(get_elevenlabs),
    rime_service: RimeService = Depends(get_rime)
):
    """
    Génère de la synthèse vocale à partir de texte.
    """
    logger.info(f"API: Demande de synthèse vocale via {request.provider} pour: '{request.text[:30]}...'")
    
    tts_response: Optional[TTSResponse | RimeTTSResponse] = None
    
    if request.provider == "elevenlabs":
        tts_response = await elevenlabs_service.text_to_speech(
            text=request.text,
            voice_preset=request.voice_id, # elevenlabs_service utilise voice_preset
            model=request.model_id
        )
    elif request.provider == "rime":
        rime_request = RimeTTSRequest(
            text=request.text,
            speaker=request.voice_id, # rime_service utilise speaker
            model=request.model_id
        )
        tts_response = await rime_service.text_to_speech(rime_request)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Fournisseur TTS non supporté.")

    if not tts_response or not tts_response.success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Échec de la génération TTS: {tts_response.error if tts_response else 'Erreur inconnue'}"
        )
        
    return TTSResponse( # Normaliser la réponse
        success=tts_response.success,
        audio_path=tts_response.audio_path,
        duration_seconds=tts_response.duration_seconds,
        characters_used=getattr(tts_response, 'characters_used', len(request.text)),
        cost_tokens=getattr(tts_response, 'cost_tokens', 0),
        error=tts_response.error
    )


@router.post("/music", status_code=status.HTTP_201_CREATED)
async def generate_music(
    request: MusicGenerateRequest
):
    """
    Génère de la musique d'ambiance à partir d'un prompt texte.
    (Implémentation fictive, nécessite un service Suno)
    """
    logger.info(f"API: Demande de génération musicale pour: '{request.prompt[:30]}...'")
    
    # Ici, on devrait appeler un service de génération musicale (ex: SunoService)
    # Pour l'instant, c'est un placeholder
    
    return {
        "message": "La génération musicale a été demandée.",
        "job_id": "music_job_123",
        "status": "queued",
        "estimated_duration": request.duration_seconds
    }


@router.post("/clone-voice", status_code=status.HTTP_201_CREATED)
async def clone_voice(
    name: str = Form(..., example="Ma nouvelle voix"),
    description: Optional[str] = Form(None, example="Une voix chaude et masculine"),
    audio_file: UploadFile = File(...),
    elevenlabs_service: ElevenLabsService = Depends(get_elevenlabs)
):
    """
    Clone une voix à partir d'un échantillon audio.
    """
    logger.info(f"API: Demande de clonage de voix pour '{name}' avec le fichier '{audio_file.filename}'")
    
    if not audio_file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nom de fichier audio manquant.")

    # Sauvegarder temporairement le fichier uploadé
    temp_file_path = Path(f"/tmp/uploaded_audio_{audio_file.filename}")
    try:
        async with aiofiles.open(temp_file_path, "wb") as out_file:
            while content := await audio_file.read(1024):  # lire par chunks
                await out_file.write(content)
        
        voice_id = await elevenlabs_service.clone_voice(name=name, audio_files=[str(temp_file_path)], description=description)
        
        if voice_id:
            return {
                "message": f"Voix '{name}' clonée avec succès.",
                "voice_id": voice_id
            }
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Échec du clonage de voix.")
            
    except Exception as e:
        logger.error(f"API: Erreur clonage voix: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erreur interne: {str(e)}")
    finally:
        if temp_file_path.exists():
            temp_file_path.unlink() # Supprimer le fichier temporaire


@router.get("/voices", response_model=List[VoiceConfig])
async def get_available_voices(
    elevenlabs_service: ElevenLabsService = Depends(get_elevenlabs)
):
    """
    Récupère la liste des voix TTS disponibles.
    """
    logger.info("API: Demande de liste des voix disponibles.")
    voices_data = await elevenlabs_service.get_voices() # ElevenLabsService a une méthode get_voices
    
    # Mapper les données brutes des voix en VoiceConfig
    # Cette partie est simplifiée et devrait être plus robuste pour mapper tous les champs
    voice_configs = []
    for voice in voices_data:
        try:
            vc = VoiceConfig(
                voice_id=voice.get("voice_id"),
                name=voice.get("name"),
                language="en", # ElevenLabs API ne retourne pas toujours la langue directement
                gender="neutral" # Déterminer le genre est plus complexe
            )
            voice_configs.append(vc)
        except Exception as e:
            logger.warning(f"Erreur de mapping de voix: {voice.get('name')} - {e}")

    # Ajouter les voix presets manuellement
    for key, value in elevenlabs_service.PRESET_VOICES.items():
        voice_configs.append(value)
    
    return voice_configs
