"""
TTS_VOICE - Router FastAPI
==========================
Endpoints Text-to-Speech pour arabe/darija/français/anglais
Architecture extensible avec backend mock par défaut
"""

import logging
from typing import Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, Query, Body
from fastapi.responses import JSONResponse

from .tts_models import (
    TTSRequest,
    TTSResponse,
    TTSStatus,
    TTSSimpleRequest,
    TTSVoice,
    TTSBatchRequest,
    TTSBatchResponse,
    TTSError,
    TTSLanguage,
    TTSDialect,
    AudioFormat,
    DEFAULT_VOICES,
    MAX_TEXT_LENGTH,
)
from .tts_service import get_tts_service, TTSService


logger = logging.getLogger(__name__)

# ============================================
# ROUTER CONFIGURATION
# ============================================

router = APIRouter(
    prefix="/api/voice",
    tags=["voice-tts"],
    responses={
        400: {"model": TTSError, "description": "Requête invalide"},
        503: {"model": TTSError, "description": "Service TTS indisponible"},
    },
)


# ============================================
# DEPENDENCIES
# ============================================

def get_service() -> TTSService:
    """Dependency pour obtenir le service TTS"""
    return get_tts_service()


# ============================================
# HEALTH & STATUS ENDPOINTS
# ============================================

@router.get("/tts/health", response_model=TTSStatus)
async def tts_health(service: TTSService = Depends(get_service)):
    """
    🏥 Health check du service TTS
    
    Retourne:
    - État du service (ready/not ready)
    - Voix disponibles
    - Backend actif (mock/openai/elevenlabs/coqui)
    """
    try:
        status = await service.health()
        return status
    except Exception as e:
        logger.error(f"Health check error: {e}")
        raise HTTPException(status_code=503, detail=str(e))


@router.get("/tts/status")
async def tts_status(service: TTSService = Depends(get_service)):
    """
    📊 Statut détaillé du service TTS
    """
    status = await service.health()
    return {
        "service": "TTS_VOICE",
        "version": "1.0.0",
        "description": "Text-to-Speech pour arabe + darija algérienne",
        "status": status.dict(),
        "endpoints": {
            "/api/voice/tts/health": "GET - Health check",
            "/api/voice/tts/synthesize": "POST - Synthèse complète",
            "/api/voice/tts/simple": "POST - Synthèse rapide",
            "/api/voice/tts/voices": "GET - Voix disponibles",
            "/api/voice/tts/batch": "POST - Synthèse batch",
        },
        "capabilities": {
            "languages": ["ar", "fr", "en", "it", "de"],
            "dialects": ["darija", "msa", "mixed"],
            "formats": ["mp3", "wav", "ogg"],
            "max_text_length": MAX_TEXT_LENGTH,
            "darija_normalization": True,
        },
        "backends": {
            "current": status.backend_type,
            "available": status.backends_status,
        },
        "timestamp": datetime.utcnow().isoformat(),
    }


# ============================================
# SYNTHESIS ENDPOINTS
# ============================================

@router.post("/tts/synthesize", response_model=TTSResponse)
async def tts_synthesize(
    request: TTSRequest,
    service: TTSService = Depends(get_service),
):
    """
    🔊 Synthèse vocale complète
    
    Transforme un texte en audio (base64).
    
    Options:
    - text: Texte à synthétiser (max 5000 caractères)
    - language: Langue (ar, fr, en)
    - dialect: Dialecte arabe (darija, msa, mixed)
    - voice_id: ID de la voix à utiliser
    - speed: Vitesse (0.25-4.0)
    - emotion: Ton (neutral, friendly, serious, etc.)
    - format: Format audio (mp3, wav, ogg)
    
    Pipeline:
    1. Normalisation texte (DARIJA_NLP si arabe)
    2. Sélection voix
    3. Synthèse via backend
    4. Encodage base64
    
    Retourne:
    - audio_base64: Audio encodé en base64
    - mime_type: Type MIME (audio/mpeg, audio/wav)
    - Métadonnées (durée, voix utilisée, etc.)
    """
    try:
        # Validation longueur
        if len(request.text) > MAX_TEXT_LENGTH:
            raise HTTPException(
                status_code=400,
                detail=f"Texte trop long: {len(request.text)} caractères (max {MAX_TEXT_LENGTH})"
            )
        
        if not request.text.strip():
            raise HTTPException(
                status_code=400,
                detail="Le texte ne peut pas être vide"
            )
        
        logger.info(f"TTS synthesize: {len(request.text)} chars, lang={request.language}, voice={request.voice_id}")
        
        response = await service.synthesize(request)
        
        logger.info(f"TTS complete: {response.duration_sec:.1f}s, backend={response.used_backend}")
        
        return response
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"TTS synthesize error: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur synthèse: {str(e)}")


@router.post("/tts/simple", response_model=TTSResponse)
async def tts_simple(
    request: TTSSimpleRequest = Body(...),
    service: TTSService = Depends(get_service),
):
    """
    ⚡ Synthèse vocale rapide (paramètres minimaux)
    
    Version simplifiée:
    - text: Texte à synthétiser
    - language: Langue optionnelle (défaut: ar)
    - voice: Voix optionnelle
    
    Idéal pour:
    - Tests rapides
    - Intégration simple
    - Voice chat
    """
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Le texte ne peut pas être vide")
        
        if len(request.text) > 2000:
            raise HTTPException(
                status_code=400,
                detail=f"Texte trop long pour /simple: {len(request.text)} chars (max 2000)"
            )
        
        response = await service.synthesize_simple(
            text=request.text,
            language=request.language or "ar",
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"TTS simple error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tts/batch", response_model=TTSBatchResponse)
async def tts_batch(
    request: TTSBatchRequest,
    service: TTSService = Depends(get_service),
):
    """
    📦 Synthèse vocale batch (plusieurs textes)
    
    Synthétise plusieurs textes en une seule requête.
    
    Options:
    - items: Liste de textes avec leurs options
    - format: Format audio de sortie
    - merge: Fusionner tous les audios en un seul (TODO)
    
    Max 50 items par batch.
    """
    try:
        if len(request.items) > 50:
            raise HTTPException(
                status_code=400,
                detail="Maximum 50 items par batch"
            )
        
        response = await service.synthesize_batch(request)
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"TTS batch error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# VOICES ENDPOINTS
# ============================================

@router.get("/tts/voices")
async def tts_voices(
    language: Optional[str] = Query(None, description="Filtrer par langue (ar, fr, en)"),
    service: TTSService = Depends(get_service),
):
    """
    🎭 Liste des voix disponibles
    
    Retourne toutes les voix TTS disponibles,
    optionnellement filtrées par langue.
    """
    voices = service.get_available_voices(language)
    
    return {
        "voices": [v.dict() for v in voices],
        "total": len(voices),
        "filter": {"language": language} if language else None,
    }


@router.get("/tts/voices/{voice_id}")
async def tts_voice_detail(
    voice_id: str,
    service: TTSService = Depends(get_service),
):
    """
    🎤 Détails d'une voix spécifique
    """
    if voice_id not in service.voices:
        raise HTTPException(status_code=404, detail=f"Voix '{voice_id}' non trouvée")
    
    voice = service.voices[voice_id]
    return voice.dict()


# ============================================
# DEMO ENDPOINTS
# ============================================

@router.get("/tts/demo/languages")
async def tts_demo_languages():
    """
    🌍 Langues et dialectes supportés (démo)
    """
    return {
        "languages": [
            {"code": "ar", "name": "Arabe", "native": "العربية", "dialects": ["darija", "msa", "mixed"]},
            {"code": "fr", "name": "Français", "native": "Français", "dialects": []},
            {"code": "en", "name": "Anglais", "native": "English", "dialects": []},
            {"code": "it", "name": "Italien", "native": "Italiano", "dialects": []},
            {"code": "de", "name": "Allemand", "native": "Deutsch", "dialects": []},
        ],
        "default_language": "ar",
        "default_dialect": "darija",
    }


@router.get("/tts/demo/formats")
async def tts_demo_formats():
    """
    📁 Formats audio supportés
    """
    return {
        "formats": [
            {"code": "mp3", "mime": "audio/mpeg", "description": "MP3 (recommandé)", "default": True},
            {"code": "wav", "mime": "audio/wav", "description": "WAV (haute qualité)"},
            {"code": "ogg", "mime": "audio/ogg", "description": "OGG Vorbis"},
            {"code": "webm", "mime": "audio/webm", "description": "WebM (navigateur)"},
            {"code": "flac", "mime": "audio/flac", "description": "FLAC (lossless)"},
        ],
        "recommended": "mp3",
        "sample_rates": [16000, 22050, 44100, 48000],
        "default_sample_rate": 22050,
    }


@router.get("/tts/demo/emotions")
async def tts_demo_emotions():
    """
    😊 Émotions/tons de voix disponibles
    """
    return {
        "emotions": [
            {"code": "neutral", "name": "Neutre", "description": "Ton neutre standard"},
            {"code": "friendly", "name": "Amical", "description": "Ton chaleureux et accueillant"},
            {"code": "serious", "name": "Sérieux", "description": "Ton professionnel et formel"},
            {"code": "professional", "name": "Professionnel", "description": "Ton business"},
            {"code": "warm", "name": "Chaleureux", "description": "Ton empathique"},
            {"code": "calm", "name": "Calme", "description": "Ton apaisant"},
            {"code": "excited", "name": "Enthousiaste", "description": "Ton dynamique"},
        ],
        "default": "neutral",
        "note": "Le support des émotions dépend du backend TTS utilisé",
    }


@router.post("/tts/demo/test")
async def tts_demo_test(service: TTSService = Depends(get_service)):
    """
    🧪 Test du service TTS (sans synthèse réelle)
    
    Vérifie:
    - Service actif
    - Backend disponible
    - Voix configurées
    """
    status = await service.health()
    
    return {
        "test": "success",
        "service_ready": status.ready,
        "backend": status.backend_type,
        "backends_available": status.backends_status,
        "voices_count": len(status.available_voices),
        "voices": status.available_voices,
        "message": "Service TTS opérationnel ✅" if status.ready else "Service en mode dégradé ⚠️",
        "note": "Backend 'mock' actif - Pas de vraie synthèse vocale. À configurer avec OpenAI/ElevenLabs/Coqui.",
        "next_step": "Envoyez un texte à /api/voice/tts/synthesize pour tester",
    }


@router.post("/tts/demo/sample")
async def tts_demo_sample(
    language: str = Query("ar", description="Langue (ar, fr, en)"),
    service: TTSService = Depends(get_service),
):
    """
    🎧 Génère un sample de démonstration
    
    Synthétise un texte exemple dans la langue choisie.
    """
    samples = {
        "ar": "مرحبا بك في آي فاكتوري، المساعد الذكي للشركات الجزائرية",
        "fr": "Bienvenue sur iaFactory, l'assistant intelligent pour les entreprises algériennes",
        "en": "Welcome to iaFactory, the intelligent assistant for Algerian businesses",
    }
    
    text = samples.get(language, samples["ar"])
    
    try:
        response = await service.synthesize_simple(text, language)
        return {
            "sample_text": text,
            "language": language,
            "response": response.dict(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
