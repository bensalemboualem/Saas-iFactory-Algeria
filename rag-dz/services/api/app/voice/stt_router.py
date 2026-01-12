"""
STT_VOICE - Router FastAPI
==========================
Endpoints Speech-to-Text pour arabe/darija/français/anglais
Avec intégration DARIJA_NLP post-processing
"""

import json
import logging
from typing import Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query, Depends
from fastapi.responses import JSONResponse

from .stt_models import (
    STTRequest,
    STTResponse,
    STTStatus,
    STTError,
    STTQuickRequest,
    STTLanguage,
    STTDialect,
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE_MB,
)
from .stt_service import get_stt_service, STTService


logger = logging.getLogger(__name__)

# ============================================
# ROUTER CONFIGURATION
# ============================================

router = APIRouter(
    prefix="/api/voice",
    tags=["voice-stt"],
    responses={
        400: {"model": STTError, "description": "Format ou requête invalide"},
        413: {"model": STTError, "description": "Fichier trop volumineux"},
        503: {"model": STTError, "description": "Service STT indisponible"},
    },
)


# ============================================
# DEPENDENCIES
# ============================================

def get_service() -> STTService:
    """Dependency pour obtenir le service STT"""
    return get_stt_service()


# ============================================
# HEALTH & STATUS ENDPOINTS
# ============================================

@router.get("/stt/health", response_model=STTStatus)
async def stt_health(service: STTService = Depends(get_service)):
    """
    🏥 Health check du service STT
    
    Retourne:
    - État du service (ready/not ready)
    - Modèles disponibles
    - Backend actif (openai/local/mock)
    - Intégration DARIJA_NLP
    """
    try:
        status = await service.health()
        return status
    except Exception as e:
        logger.error(f"Health check error: {e}")
        raise HTTPException(status_code=503, detail=str(e))


@router.get("/stt/status")
async def stt_status(service: STTService = Depends(get_service)):
    """
    📊 Statut détaillé du service STT
    """
    status = await service.health()
    return {
        "service": "STT_VOICE",
        "version": "1.0.0",
        "description": "Speech-to-Text pour arabe + darija algérienne",
        "status": status.dict(),
        "endpoints": {
            "/api/voice/stt/health": "GET - Health check",
            "/api/voice/stt/transcribe": "POST - Transcription complète",
            "/api/voice/stt/quick": "POST - Transcription rapide (auto)",
            "/api/voice/stt/formats": "GET - Formats supportés",
        },
        "capabilities": {
            "languages": ["ar", "fr", "en", "auto"],
            "dialects": ["darija", "msa", "mixed"],
            "darija_normalization": status.darija_nlp_ready,
            "arabizi_conversion": status.darija_nlp_ready,
        },
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/stt/formats")
async def stt_formats():
    """
    📁 Formats audio supportés
    """
    return {
        "supported_formats": ALLOWED_EXTENSIONS,
        "max_file_size_mb": MAX_FILE_SIZE_MB,
        "max_duration_sec": 600,
        "recommended": {
            "format": "wav",
            "sample_rate": 16000,
            "channels": 1,
            "bit_depth": 16,
        },
        "tips": [
            "WAV 16kHz mono recommandé pour meilleure qualité",
            "MP3 128kbps minimum pour résultats acceptables",
            "WebM supporté pour enregistrements navigateur",
        ],
    }


# ============================================
# TRANSCRIPTION ENDPOINTS
# ============================================

@router.post("/stt/transcribe", response_model=STTResponse)
async def stt_transcribe(
    file: UploadFile = File(..., description="Fichier audio (WAV/MP3/OGG/WebM)"),
    payload: Optional[str] = Form(None, description="Options JSON (STTRequest)"),
    language_hint: Optional[str] = Query(None, description="Indice langue: ar, fr, en, auto"),
    dialect: Optional[str] = Query(None, description="Dialecte: darija, msa, mixed, auto"),
    service: STTService = Depends(get_service),
):
    """
    🎙️ Transcription complète audio → texte
    
    Pipeline:
    1. Upload fichier audio (WAV, MP3, OGG, WebM, M4A, FLAC)
    2. Transcription via Whisper (OpenAI ou local)
    3. Nettoyage texte via DARIJA_NLP cleaner
    4. Normalisation darija si arabe détecté
    5. Conversion arabizi → arabe si détecté
    
    Retourne:
    - text_raw: Transcription brute
    - text_cleaned: Texte nettoyé
    - text_normalized: Texte normalisé darija (si applicable)
    - Métadonnées (langue, dialecte, durée, etc.)
    
    Options (via payload JSON ou query params):
    - language_hint: Indice de langue (ar, fr, en, auto)
    - dialect: Dialecte attendu (darija, msa, mixed, auto)
    - enable_darija_normalization: Activer normalisation darija
    - enable_timestamps: Inclure timestamps par segment
    """
    try:
        # Valider extension
        if file.filename:
            ext = file.filename.split('.')[-1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                raise HTTPException(
                    status_code=400,
                    detail=f"Format non supporté: .{ext}. Formats acceptés: {', '.join(ALLOWED_EXTENSIONS)}"
                )
        
        # Lire le fichier
        file_bytes = await file.read()
        
        # Valider taille
        size_mb = len(file_bytes) / (1024 * 1024)
        if size_mb > MAX_FILE_SIZE_MB:
            raise HTTPException(
                status_code=413,
                detail=f"Fichier trop volumineux: {size_mb:.1f}MB (max {MAX_FILE_SIZE_MB}MB)"
            )
        
        # Parser les options
        request = STTRequest()
        
        if payload:
            try:
                payload_dict = json.loads(payload)
                request = STTRequest(**payload_dict)
            except json.JSONDecodeError as e:
                raise HTTPException(status_code=400, detail=f"JSON invalide: {str(e)}")
        
        # Override avec query params
        if language_hint:
            try:
                request.language_hint = STTLanguage(language_hint)
            except ValueError:
                request.language_hint = STTLanguage.AUTO
        
        if dialect:
            try:
                request.dialect = STTDialect(dialect)
            except ValueError:
                request.dialect = STTDialect.AUTO
        
        # Transcrire
        logger.info(f"Transcribing: {file.filename}, size={size_mb:.2f}MB, lang={request.language_hint}, dialect={request.dialect}")
        
        response = await service.transcribe_audio(
            file_bytes=file_bytes,
            request=request,
            filename=file.filename,
        )
        
        logger.info(f"Transcription complete: {len(response.text_raw)} chars, lang={response.language}, dialect={response.dialect}")
        
        return response
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")


@router.post("/stt/quick", response_model=STTResponse)
async def stt_quick(
    file: UploadFile = File(..., description="Fichier audio"),
    language: Optional[str] = Query(None, description="Langue optionnelle (ar, fr, en)"),
    service: STTService = Depends(get_service),
):
    """
    ⚡ Transcription rapide (tout automatique)
    
    Version simplifiée:
    - Upload fichier audio
    - Détection automatique langue et dialecte
    - Normalisation darija activée par défaut
    
    Idéal pour:
    - Tests rapides
    - Intégration simple
    - Voice chat
    """
    try:
        file_bytes = await file.read()
        
        # Valider taille
        size_mb = len(file_bytes) / (1024 * 1024)
        if size_mb > MAX_FILE_SIZE_MB:
            raise HTTPException(
                status_code=413,
                detail=f"Fichier trop volumineux: {size_mb:.1f}MB (max {MAX_FILE_SIZE_MB}MB)"
            )
        
        # Request par défaut
        request = STTRequest(
            language_hint=STTLanguage(language) if language else STTLanguage.AUTO,
            dialect=STTDialect.AUTO,
            enable_darija_normalization=True,
        )
        
        response = await service.transcribe_audio(
            file_bytes=file_bytes,
            request=request,
            filename=file.filename,
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Quick transcription error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# DEMO ENDPOINTS
# ============================================

@router.get("/stt/demo/languages")
async def stt_demo_languages():
    """
    🌍 Langues et dialectes supportés (démo)
    """
    return {
        "languages": [
            {"code": "ar", "name": "Arabe", "native": "العربية"},
            {"code": "ar-dz", "name": "Arabe Algérien", "native": "الدارجة"},
            {"code": "fr", "name": "Français", "native": "Français"},
            {"code": "en", "name": "Anglais", "native": "English"},
            {"code": "auto", "name": "Détection auto", "native": "Auto"},
        ],
        "dialects": [
            {"code": "darija", "name": "Darija algérienne", "description": "Arabe algérien parlé"},
            {"code": "msa", "name": "Arabe standard", "description": "Arabe moderne standard"},
            {"code": "mixed", "name": "Mixte", "description": "Mélange arabe/français"},
        ],
        "features": {
            "arabizi_detection": True,
            "arabizi_conversion": True,
            "darija_normalization": True,
            "french_arabic_mix": True,
        },
    }


@router.get("/stt/demo/prompts")
async def stt_demo_prompts():
    """
    💡 Prompts contextuels pour améliorer transcription
    """
    return {
        "prompts": {
            "general": {
                "ar": "هذا نص بالدارجة الجزائرية، قد يحتوي على كلمات فرنسية",
                "description": "Usage général darija",
            },
            "admin": {
                "ar": "نص إداري جزائري، casnos, cnas, registre de commerce, impôts",
                "description": "Documents administratifs (CASNOS, CNAS, etc.)",
            },
            "commerce": {
                "ar": "نص تجاري جزائري، facture, bon de livraison, prix, DZD",
                "description": "Commerce, factures, transactions",
            },
            "legal": {
                "ar": "نص قانوني جزائري، عقد، محكمة، موثق",
                "description": "Documents juridiques",
            },
            "medical": {
                "ar": "نص طبي جزائري، طبيب، مستشفى، دواء",
                "description": "Médical, santé",
            },
        },
        "usage": "Ajoutez le prompt dans le champ 'prompt' de STTRequest pour améliorer la transcription contextuelle",
    }


@router.post("/stt/demo/test")
async def stt_demo_test(service: STTService = Depends(get_service)):
    """
    🧪 Test du service STT (sans fichier)
    
    Vérifie:
    - Service actif
    - Backend disponible
    - DARIJA_NLP intégré
    """
    status = await service.health()
    
    return {
        "test": "success",
        "service_ready": status.ready,
        "backend": status.backend_type,
        "openai_available": status.openai_available,
        "darija_nlp_ready": status.darija_nlp_ready,
        "models": status.available_models,
        "message": "Service STT opérationnel ✅" if status.ready else "Service en mode dégradé ⚠️",
        "next_step": "Envoyez un fichier audio à /api/voice/stt/transcribe pour tester",
    }


# ============================================
# Note: Exception handlers are defined at app level, not router level
# ============================================
