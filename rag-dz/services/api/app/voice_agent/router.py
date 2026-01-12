"""
FastAPI Router pour l'agent vocal Faster-Whisper
Endpoints API pour reconnaissance vocale souveraine
"""

from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from typing import Optional
import logging
import time

from .transcription_service import get_transcription_service
from .keywords_service import generate_keywords
from .repository import save_transcription
from .emotional_intelligence import analyze_intent_and_emotion
from ..digital_twin.repository import (
    save_emotion_analysis,
    bulk_add_to_user_lexicon,
    track_tokens_saved,
)
from ..dependencies import get_current_tenant_id

logger = logging.getLogger(__name__)

# Router FastAPI
router = APIRouter(
    prefix="/api/voice-agent",
    tags=["voice-agent"],
)


@router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(..., description="Fichier audio à transcrire"),
    tenant_id: str = Depends(get_current_tenant_id),
    language: Optional[str] = Form(None, description="Code langue (fr, en, ar) ou auto"),
    professional_context: Optional[str] = Form(None, description="Contexte: medical, legal, accounting"),
):
    """
    Transcrit un fichier audio en texte

    **Multi-Tenant**: Le tenant_id est automatiquement injecté depuis le contexte de la requête.
    Les transcriptions sont isolées par tenant via Row-Level Security (RLS).

    **Use Cases Professionnels**:
    - **Médecins**: Comptes-rendus de consultation
    - **Avocats**: Notes d'audience, dictées juridiques
    - **Experts-comptables**: Notes de rendez-vous client

    **Langues supportées**:
    - `fr` - Français (France, Suisse, Belgique, Québec)
    - `en` - Anglais (US, UK, médical)
    - `ar` - Arabe (littéraire, dialectes, darija)
    - `null` - Détection automatique

    **Formats audio supportés**:
    - WAV, MP3, M4A, FLAC, OGG, OPUS, WEBM

    **Réponse**:
    ```json
    {
      "text": "Texte complet transcrit",
      "cleaned_text": "Texte nettoyé selon contexte",
      "segments": [
        {"start": 0.0, "end": 2.5, "text": "Segment 1"},
        {"start": 2.5, "end": 5.0, "text": "Segment 2"}
      ],
      "language": "fr",
      "language_probability": 0.98,
      "duration": 45.3,
      "filename": "consultation_20250116.m4a",
      "professional_context": "medical"
    }
    ```

    **Exemple cURL**:
    ```bash
    curl -X POST "http://localhost:3000/api/voice-agent/transcribe" \\
      -F "file=@consultation.m4a" \\
      -F "language=fr" \\
      -F "professional_context=medical"
    ```
    """
    try:
        start_time = time.time()

        # Vérifier type de fichier (MP4 supporté pour WhatsApp)
        allowed_extensions = [".wav", ".mp3", ".m4a", ".mp4", ".flac", ".ogg", ".opus", ".webm", ".aac"]
        file_ext = "." + file.filename.split(".")[-1].lower()

        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Format non supporté: {file_ext}. Formats acceptés: {', '.join(allowed_extensions)}",
            )

        # Service de transcription
        service = get_transcription_service()

        # Transcription
        result = service.transcribe_file(
            audio_file=file.file,
            filename=file.filename,
            language=language,
            professional_context=professional_context,
        )

        # Mesurer temps de traitement
        processing_time_ms = int((time.time() - start_time) * 1000)

        # Générer mots-clés IA (Petit Plus pour la 'Mémoire' de l'Agent)
        keywords = generate_keywords(result.get("text", ""), context=professional_context)
        logger.info(f"🔑 Mots-clés générés: {keywords}")

        # PHASE 2: Digital Twin Intelligence - Analyse émotionnelle & culturelle
        emotion_analysis = None
        emotion_analysis_id = None
        try:
            # Analyser l'émotion, stress, et contexte culturel
            # TODO: Get user_country from tenant metadata
            user_country = "algeria"  # Default, should come from tenant metadata

            emotion_analysis = analyze_intent_and_emotion(
                text=result.get("text", ""),
                user_country=user_country,
                professional_context=professional_context,
            )

            logger.info(
                f"🧠 Analyse émotionnelle: emotion={emotion_analysis.detected_emotion}, "
                f"stress={emotion_analysis.stress_level}/10, "
                f"heritage={emotion_analysis.heritage_detected}"
            )

        except Exception as emotion_error:
            logger.warning(f"⚠️ Erreur analyse émotionnelle (non-bloquant): {emotion_error}")

        # Sauvegarder en DB avec isolation tenant (RLS)
        try:
            transcription_id = save_transcription(
                tenant_id=tenant_id,
                filename=file.filename,
                text_raw=result.get("text", ""),
                duration_seconds=result.get("duration", 0.0),
                language=result.get("language", "unknown"),
                language_confidence=result.get("language_probability", 0.0),
                audio_format=file_ext.lstrip("."),
                used_model="base",  # Auto-détecté par whisper_engine
                processing_time_ms=processing_time_ms,
                keywords=keywords,
                metadata={
                    "professional_context": professional_context,
                    "segments_count": len(result.get("segments", [])),
                },
            )

            # Ajouter ID et keywords au résultat
            result["transcription_id"] = transcription_id
            result["keywords"] = keywords
            result["processing_time_ms"] = processing_time_ms

            # PHASE 2: Sauvegarder analyse émotionnelle et mettre à jour lexique
            if emotion_analysis:
                try:
                    # TODO: Get user_id from authentication context
                    user_id = 1  # Default user for now

                    # 1. Sauvegarder analyse émotionnelle
                    emotion_analysis_id = save_emotion_analysis(
                        tenant_id=tenant_id,
                        user_id=user_id,
                        transcription_id=transcription_id,
                        emotion_data={
                            "detected_emotion": emotion_analysis.detected_emotion,
                            "stress_level": emotion_analysis.stress_level,
                            "cognitive_load": emotion_analysis.cognitive_load,
                            "heritage_detected": emotion_analysis.heritage_detected,
                            "heritage_type": emotion_analysis.heritage_type,
                            "heritage_content": emotion_analysis.heritage_content,
                            "recommended_summary_style": emotion_analysis.recommended_summary_style,
                            "ai_confidence": emotion_analysis.ai_confidence,
                            "keywords_extracted": emotion_analysis.keywords_extracted,
                            "professional_terms": emotion_analysis.professional_terms,
                        },
                    )

                    logger.info(f"💾 Emotion analysis saved: {emotion_analysis_id}")

                    # 2. Enrichir le lexique personnel avec termes professionnels
                    if emotion_analysis.professional_terms:
                        terms_count = bulk_add_to_user_lexicon(
                            tenant_id=tenant_id,
                            user_id=user_id,
                            terms=emotion_analysis.professional_terms,
                            professional_domain=professional_context,
                            transcription_id=transcription_id,
                        )
                        logger.info(f"📚 {terms_count} termes ajoutés au lexique personnel")

                    # 3. Track ROI: Tokens économisés (Faster-Whisper local vs Cloud)
                    roi_tracking_id = track_tokens_saved(
                        tenant_id=tenant_id,
                        user_id=user_id,
                        transcription_id=transcription_id,
                        audio_duration_seconds=result.get("duration", 0.0),
                        audio_format=file_ext.lstrip("."),
                        processing_time_ms=processing_time_ms,
                    )

                    logger.info(f"💰 ROI tracked: {roi_tracking_id}")

                    # Ajouter analyse émotionnelle à la réponse
                    result["emotion_analysis"] = {
                        "id": emotion_analysis_id,
                        "detected_emotion": emotion_analysis.detected_emotion,
                        "stress_level": emotion_analysis.stress_level,
                        "cognitive_load": emotion_analysis.cognitive_load,
                        "recommended_summary_style": emotion_analysis.recommended_summary_style,
                        "heritage_detected": emotion_analysis.heritage_detected,
                        "heritage_type": emotion_analysis.heritage_type,
                        "ai_confidence": emotion_analysis.ai_confidence,
                    }

                except Exception as twin_error:
                    # Ne pas bloquer si erreur Digital Twin
                    logger.error(f"⚠️ Erreur Digital Twin (non-bloquant): {twin_error}")
                    result["digital_twin_error"] = "Emotion analysis failed"

            logger.info(
                f"✅ Transcription complète: {file.filename} ({result['language']}) "
                f"- Tenant: {tenant_id} - ID: {transcription_id} - Keywords: {keywords}"
            )

        except Exception as db_error:
            # Log l'erreur mais ne bloque pas la transcription
            logger.error(f"❌ Erreur sauvegarde DB (transcription OK): {db_error}")
            result["db_error"] = "Transcription OK mais erreur sauvegarde DB"

        return JSONResponse(content=result)

    except Exception as e:
        logger.error(f"Erreur API transcribe: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/transcribe-url")
async def transcribe_from_url(
    audio_url: str = Form(..., description="URL du fichier audio"),
    tenant_id: str = Depends(get_current_tenant_id),
    language: Optional[str] = Form(None, description="Code langue ou auto"),
):
    """
    Transcrit un fichier audio depuis une URL

    **Exemple**:
    ```bash
    curl -X POST "http://localhost:3000/api/voice-agent/transcribe-url" \\
      -F "audio_url=https://example.com/audio.m4a" \\
      -F "language=fr"
    ```
    """
    try:
        service = get_transcription_service()
        result = service.transcribe_url(
            audio_url=audio_url,
            language=language,
        )

        logger.info(f"Transcription URL réussie: {audio_url} - Tenant: {tenant_id}")
        return JSONResponse(content=result)

    except Exception as e:
        logger.error(f"Erreur transcribe-url: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/detect-language")
async def detect_language(
    file: UploadFile = File(..., description="Fichier audio"),
    tenant_id: str = Depends(get_current_tenant_id),
):
    """
    Détecte la langue d'un fichier audio

    **Réponse**:
    ```json
    {
      "language": "fr",
      "probability": 0.98
    }
    ```
    """
    try:
        service = get_transcription_service()
        result = service.detect_language(
            audio_file=file.file,
            filename=file.filename,
        )

        logger.info(f"Détection langue réussie: {file.filename} → {result.get('language')} - Tenant: {tenant_id}")
        return JSONResponse(content=result)

    except Exception as e:
        logger.error(f"Erreur detect-language: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models")
async def list_models():
    """
    Liste les modèles Whisper disponibles

    **Réponse**:
    ```json
    {
      "models": {
        "tiny": "Plus petit, plus rapide (39M params)",
        "base": "Modèle de base (74M params)",
        "small": "Petit modèle (244M params)",
        "medium": "Modèle moyen (769M params)",
        "large-v2": "Grand modèle v2 (1550M params)",
        "large-v3": "Grand modèle v3 - Recommandé (1550M params)",
        "distil-large-v3": "Version légère de large-v3 (50% plus rapide)"
      },
      "current_model": "large-v3",
      "device": "cuda",
      "compute_type": "float16"
    }
    ```
    """
    from .whisper_engine import WhisperEngine

    return JSONResponse(
        content={
            "models": {
                "tiny": "Plus petit, plus rapide (39M params)",
                "base": "Modèle de base (74M params)",
                "small": "Petit modèle (244M params)",
                "medium": "Modèle moyen (769M params)",
                "large-v2": "Grand modèle v2 (1550M params)",
                "large-v3": "Grand modèle v3 - Recommandé (1550M params)",
                "distil-large-v3": "Version légère de large-v3 (50% plus rapide)",
            },
            "current_model": "large-v3",
            "device": "auto",
            "compute_type": "float16",
            "languages": [
                "fr (Français)",
                "en (English)",
                "ar (العربية)",
                "es (Español)",
                "de (Deutsch)",
                "it (Italiano)",
                "pt (Português)",
                "... 97 langues au total",
            ],
        }
    )


@router.get("/health")
async def health_check():
    """
    Health check de l'agent vocal

    **Réponse**:
    ```json
    {
      "status": "healthy",
      "service": "voice-agent",
      "model": "large-v3",
      "device": "cuda",
      "ready": true
    }
    ```
    """
    try:
        service = get_transcription_service()
        return JSONResponse(
            content={
                "status": "healthy",
                "service": "voice-agent",
                "model": "large-v3",
                "device": service.engine.device,
                "ready": True,
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "service": "voice-agent",
                "error": str(e),
                "ready": False,
            },
        )
