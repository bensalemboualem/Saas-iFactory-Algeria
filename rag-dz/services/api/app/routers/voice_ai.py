"""
IAFactory Voice AI Router - Unified Voice Intelligence API
===========================================================
Intègre: STT (Speech-to-Text) + TTS (Text-to-Speech) + NLP + OCR

Endpoints:
- /api/voice-ai/process      - Pipeline complet: Audio → STT → NLP → Response → TTS
- /api/voice-ai/stt          - Speech-to-Text uniquement
- /api/voice-ai/tts          - Text-to-Speech uniquement
- /api/voice-ai/ocr          - OCR (document → texte)
- /api/voice-ai/understand   - NLP: analyse de texte (intent, entities, emotion)
- /api/voice-ai/anticipate   - Anticipation des intentions
- /api/voice-ai/modes        - Modes disponibles (Hotline, Secretary, Restaurant, AI Double)
- /api/voice-ai/health       - Statut des services

Langues: AR (Arabe), FR (Français), EN (Anglais), DZ (Darija), MIXED (Code-switching)
"""
import asyncio
import logging
import base64
import io
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.dependencies import get_current_user, optional_user
from app.services.voice_ai_agent import (
    voice_ai_agent,
    VoiceAIAgent,
    VoiceAgentMode,
    VoiceContext,
    VoiceResponse,
    LanguageCode,
    MultilingualNLP,
)
from app.voice.stt_service import get_stt_service, STTRequest, STTLanguage, STTDialect
from app.voice.tts_service import get_tts_service, TTSRequest, TTSLanguage, TTSDialect
from app.ocr.ocr_dz_pipeline import ocr_pipeline, OCRResult

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/voice-ai", tags=["Voice AI Agent"])


# ============================================
# MODELS
# ============================================

class VoiceProcessRequest(BaseModel):
    """Request for full voice processing pipeline"""
    mode: str = Field("general", description="Mode: hotline, secretary, restaurant, ai_double, general")
    session_id: Optional[str] = Field(None, description="Session ID for context")
    language_hint: Optional[str] = Field(None, description="Language hint: ar, fr, en, dz")
    generate_audio: bool = Field(True, description="Generate TTS audio response")
    emotion_detection: bool = Field(True, description="Detect emotion from audio")


class TextProcessRequest(BaseModel):
    """Request for text processing (NLP only)"""
    text: str = Field(..., min_length=1, description="Text to process")
    mode: str = Field("general", description="Operating mode")
    session_id: Optional[str] = Field(None, description="Session ID")
    language: Optional[str] = Field(None, description="Language: ar, fr, en, dz")


class TTSGenerateRequest(BaseModel):
    """Request for TTS generation"""
    text: str = Field(..., min_length=1, max_length=5000, description="Text to synthesize")
    language: str = Field("ar", description="Language: ar, fr, en")
    dialect: Optional[str] = Field(None, description="Dialect: darija, msa")
    voice_id: Optional[str] = Field(None, description="Voice ID")
    speed: float = Field(1.0, ge=0.5, le=2.0, description="Speech speed")
    emotion: Optional[str] = Field(None, description="Emotion: neutral, friendly, formal")


class NLPAnalyzeRequest(BaseModel):
    """Request for NLP analysis"""
    text: str = Field(..., min_length=1, description="Text to analyze")
    mode: str = Field("general", description="Operating mode for intent detection")
    detect_entities: bool = Field(True, description="Extract entities")
    detect_emotion: bool = Field(True, description="Detect emotion")
    detect_language: bool = Field(True, description="Detect language")


class VoiceProcessResponse(BaseModel):
    """Response from voice processing"""
    # Input analysis
    transcription: str = Field(..., description="Transcribed text from audio")
    detected_language: str = Field(..., description="Detected language")
    detected_emotion: str = Field("neutral", description="Detected emotion")

    # NLP analysis
    intents: List[Dict[str, Any]] = Field(default_factory=list, description="Detected intents")
    entities: Dict[str, Any] = Field(default_factory=dict, description="Extracted entities")

    # Agent response
    response_text: str = Field(..., description="Agent response text")
    response_language: str = Field(..., description="Response language")
    action: Optional[str] = Field(None, description="Action to perform")
    action_data: Optional[Dict[str, Any]] = Field(None, description="Action data")

    # Audio response
    audio_base64: Optional[str] = Field(None, description="TTS audio as base64")
    audio_format: str = Field("mp3", description="Audio format")

    # Suggestions
    suggested_responses: List[str] = Field(default_factory=list, description="Suggested user responses")
    anticipation: Optional[str] = Field(None, description="Anticipated next action")

    # Metadata
    session_id: str = Field(..., description="Session ID")
    mode: str = Field(..., description="Operating mode")
    processing_time_ms: int = Field(0, description="Total processing time")


class NLPAnalyzeResponse(BaseModel):
    """Response from NLP analysis"""
    # Language
    detected_language: str = Field(..., description="Detected language")
    language_confidence: float = Field(0.0, description="Language detection confidence")
    is_code_switching: bool = Field(False, description="Multiple languages mixed")

    # Intents
    intents: List[Dict[str, float]] = Field(default_factory=list, description="Detected intents with confidence")
    primary_intent: Optional[str] = Field(None, description="Primary intent")

    # Entities
    entities: Dict[str, Any] = Field(default_factory=dict, description="Extracted entities")

    # Emotion
    emotion: str = Field("neutral", description="Detected emotion")

    # Darija-specific
    is_darija: bool = Field(False, description="Contains Algerian Darija")
    darija_phrases: List[str] = Field(default_factory=list, description="Detected Darija phrases")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = "ok"
    services: Dict[str, bool] = Field(default_factory=dict)
    modes: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)


# ============================================
# MAIN ENDPOINTS
# ============================================

@router.post("/process", response_model=VoiceProcessResponse)
async def process_voice(
    audio: UploadFile = File(..., description="Audio file (wav, mp3, webm, m4a)"),
    mode: str = Form("general"),
    session_id: Optional[str] = Form(None),
    language_hint: Optional[str] = Form(None),
    generate_audio: bool = Form(True),
    current_user: dict = Depends(optional_user),
):
    """
    Full voice processing pipeline:
    1. STT: Audio → Text
    2. NLP: Analyze text (language, intent, entities, emotion)
    3. Agent: Generate response based on mode
    4. TTS: Text → Audio (if requested)

    Modes:
    - hotline: Call center / support
    - secretary: Personal assistant
    - restaurant: Order taking
    - ai_double: Personal AI clone
    - general: General conversation

    Supports:
    - Arabic (MSA + Darija)
    - French
    - English
    - Mixed/Code-switching
    """
    import time
    start_time = time.time()

    try:
        # Read audio file
        audio_bytes = await audio.read()

        if not audio_bytes:
            raise HTTPException(status_code=400, detail="Empty audio file")

        # 1. STT - Speech to Text
        stt_service = get_stt_service()

        # Configure STT request
        stt_request = STTRequest(
            enable_darija_normalization=True,
            enable_timestamps=False,
        )

        if language_hint:
            lang_map = {"ar": STTLanguage.ARABIC, "fr": STTLanguage.FRENCH, "en": STTLanguage.ENGLISH, "dz": STTLanguage.DARIJA}
            stt_request.language_hint = lang_map.get(language_hint, STTLanguage.AUTO)
            if language_hint == "dz":
                stt_request.dialect = STTDialect.DARIJA

        stt_result = await stt_service.transcribe_audio(
            file_bytes=audio_bytes,
            request=stt_request,
            filename=audio.filename,
        )

        transcription = stt_result.text_cleaned or stt_result.text_raw
        detected_language = stt_result.language or "unknown"

        if not transcription.strip():
            raise HTTPException(status_code=400, detail="Could not transcribe audio - no speech detected")

        # 2. Voice AI Agent Processing
        if not session_id:
            session_id = f"session_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{id(audio_bytes) % 10000}"

        # Map mode string to enum
        mode_map = {
            "hotline": VoiceAgentMode.HOTLINE,
            "secretary": VoiceAgentMode.SECRETARY,
            "restaurant": VoiceAgentMode.RESTAURANT,
            "ai_double": VoiceAgentMode.AI_DOUBLE,
            "general": VoiceAgentMode.GENERAL,
        }
        agent_mode = mode_map.get(mode, VoiceAgentMode.GENERAL)

        user_id = current_user.get("id") if current_user else None

        # Process with voice agent
        agent_response = await voice_ai_agent.process_voice_input(
            text=transcription,
            session_id=session_id,
            user_id=user_id,
            mode=agent_mode,
        )

        # Get context for intents/entities
        context = voice_ai_agent.get_or_create_context(session_id, user_id, agent_mode)
        nlp = voice_ai_agent.nlp

        intents = nlp.detect_intent(transcription, agent_mode)
        entities = nlp.extract_entities(transcription, agent_mode)
        emotion = nlp.detect_emotion(transcription)

        # 3. TTS - Text to Speech (if requested)
        audio_base64 = None
        if generate_audio and agent_response.text:
            try:
                tts_service = get_tts_service()

                # Map language
                tts_lang_map = {
                    LanguageCode.ARABIC: TTSLanguage.ARABIC,
                    LanguageCode.FRENCH: TTSLanguage.FRENCH,
                    LanguageCode.ENGLISH: TTSLanguage.ENGLISH,
                    LanguageCode.DARIJA: TTSLanguage.ARABIC,
                    LanguageCode.MIXED: TTSLanguage.ARABIC,  # Default to Arabic for mixed
                }
                tts_lang = tts_lang_map.get(agent_response.language, TTSLanguage.ARABIC)

                tts_request = TTSRequest(
                    text=agent_response.text,
                    language=tts_lang,
                    dialect=TTSDialect.DARIJA if agent_response.language == LanguageCode.DARIJA else None,
                )

                tts_result = await tts_service.synthesize(tts_request)
                audio_base64 = tts_result.audio_base64
            except Exception as e:
                logger.warning(f"TTS failed: {e}")

        # Calculate processing time
        processing_time_ms = int((time.time() - start_time) * 1000)

        return VoiceProcessResponse(
            transcription=transcription,
            detected_language=detected_language,
            detected_emotion=emotion,
            intents=[{"intent": i[0], "confidence": i[1]} for i in intents],
            entities=entities,
            response_text=agent_response.text,
            response_language=agent_response.language.value if hasattr(agent_response.language, 'value') else str(agent_response.language),
            action=agent_response.action,
            action_data=agent_response.action_data,
            audio_base64=audio_base64,
            audio_format="mp3",
            suggested_responses=agent_response.suggested_responses,
            anticipation=agent_response.anticipation,
            session_id=session_id,
            mode=mode,
            processing_time_ms=processing_time_ms,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Voice processing error: {e}")
        raise HTTPException(status_code=500, detail=f"Voice processing failed: {str(e)}")


@router.post("/understand", response_model=NLPAnalyzeResponse)
async def understand_text(
    request: NLPAnalyzeRequest,
    current_user: dict = Depends(optional_user),
):
    """
    Analyze text with NLP:
    - Language detection (with code-switching)
    - Intent detection
    - Entity extraction
    - Emotion detection
    - Darija phrase detection
    """
    nlp = MultilingualNLP()

    # Detect language
    detected_lang, lang_conf = nlp.detect_language(request.text)
    is_code_switching = detected_lang == LanguageCode.MIXED

    # Detect intents
    mode_map = {
        "hotline": VoiceAgentMode.HOTLINE,
        "secretary": VoiceAgentMode.SECRETARY,
        "restaurant": VoiceAgentMode.RESTAURANT,
        "ai_double": VoiceAgentMode.AI_DOUBLE,
        "general": VoiceAgentMode.GENERAL,
    }
    mode = mode_map.get(request.mode, VoiceAgentMode.GENERAL)

    intents = nlp.detect_intent(request.text, mode) if request.mode != "general" else []
    primary_intent = intents[0][0] if intents else None

    # Extract entities
    entities = nlp.extract_entities(request.text, mode) if request.detect_entities else {}

    # Detect emotion
    emotion = nlp.detect_emotion(request.text) if request.detect_emotion else "neutral"

    # Check for Darija
    is_darija = detected_lang == LanguageCode.DARIJA
    darija_phrases = []

    text_lower = request.text.lower()
    for pattern, meaning in nlp.DARIJA_PATTERNS.items():
        import re
        if re.search(pattern, text_lower):
            # Find the matched phrase
            match = re.search(pattern, text_lower)
            if match:
                darija_phrases.append(f"{match.group()} ({meaning})")

    return NLPAnalyzeResponse(
        detected_language=detected_lang.value if hasattr(detected_lang, 'value') else str(detected_lang),
        language_confidence=lang_conf,
        is_code_switching=is_code_switching,
        intents=[{"intent": i[0], "confidence": i[1]} for i in intents],
        primary_intent=primary_intent,
        entities=entities,
        emotion=emotion,
        is_darija=is_darija or bool(darija_phrases),
        darija_phrases=darija_phrases,
    )


@router.post("/stt")
async def speech_to_text(
    audio: UploadFile = File(..., description="Audio file"),
    language: Optional[str] = Form(None, description="Language hint: ar, fr, en, dz"),
    normalize_darija: bool = Form(True, description="Normalize Darija text"),
    current_user: dict = Depends(optional_user),
):
    """
    Speech-to-Text only.
    Converts audio to text with optional Darija normalization.
    """
    try:
        audio_bytes = await audio.read()

        if not audio_bytes:
            raise HTTPException(status_code=400, detail="Empty audio file")

        stt_service = get_stt_service()

        stt_request = STTRequest(
            enable_darija_normalization=normalize_darija,
            enable_timestamps=False,
        )

        if language:
            lang_map = {"ar": STTLanguage.ARABIC, "fr": STTLanguage.FRENCH, "en": STTLanguage.ENGLISH, "dz": STTLanguage.DARIJA}
            stt_request.language_hint = lang_map.get(language, STTLanguage.AUTO)
            if language == "dz":
                stt_request.dialect = STTDialect.DARIJA

        result = await stt_service.transcribe_audio(
            file_bytes=audio_bytes,
            request=stt_request,
            filename=audio.filename,
        )

        return {
            "text": result.text_cleaned or result.text_raw,
            "text_raw": result.text_raw,
            "text_normalized": result.text_normalized,
            "language": result.language,
            "dialect": result.dialect,
            "is_arabizi": result.is_arabizi,
            "confidence": result.confidence,
            "duration_sec": result.duration_sec,
            "processing_time_ms": result.processing_time_ms,
        }

    except Exception as e:
        logger.error(f"STT error: {e}")
        raise HTTPException(status_code=500, detail=f"STT failed: {str(e)}")


@router.post("/tts")
async def text_to_speech(
    request: TTSGenerateRequest,
    current_user: dict = Depends(optional_user),
):
    """
    Text-to-Speech only.
    Converts text to audio with language/voice selection.
    """
    try:
        tts_service = get_tts_service()

        # Map language
        lang_map = {"ar": TTSLanguage.ARABIC, "fr": TTSLanguage.FRENCH, "en": TTSLanguage.ENGLISH}
        tts_lang = lang_map.get(request.language, TTSLanguage.ARABIC)

        dialect = None
        if request.dialect == "darija":
            dialect = TTSDialect.DARIJA

        tts_request = TTSRequest(
            text=request.text,
            language=tts_lang,
            dialect=dialect,
            voice_id=request.voice_id,
            speed=request.speed,
        )

        result = await tts_service.synthesize(tts_request)

        return {
            "audio_base64": result.audio_base64,
            "mime_type": result.mime_type,
            "format": result.format,
            "language": result.language,
            "duration_sec": result.duration_sec,
            "processing_time_ms": result.processing_time_ms,
        }

    except Exception as e:
        logger.error(f"TTS error: {e}")
        raise HTTPException(status_code=500, detail=f"TTS failed: {str(e)}")


@router.post("/tts/stream")
async def text_to_speech_stream(
    request: TTSGenerateRequest,
    current_user: dict = Depends(optional_user),
):
    """
    Text-to-Speech with audio streaming.
    Returns audio as binary stream.
    """
    try:
        tts_service = get_tts_service()

        lang_map = {"ar": TTSLanguage.ARABIC, "fr": TTSLanguage.FRENCH, "en": TTSLanguage.ENGLISH}
        tts_lang = lang_map.get(request.language, TTSLanguage.ARABIC)

        tts_request = TTSRequest(
            text=request.text,
            language=tts_lang,
            speed=request.speed,
        )

        result = await tts_service.synthesize(tts_request)

        if not result.audio_base64:
            raise HTTPException(status_code=500, detail="No audio generated")

        audio_bytes = base64.b64decode(result.audio_base64)

        return StreamingResponse(
            io.BytesIO(audio_bytes),
            media_type=result.mime_type or "audio/mpeg",
            headers={
                "Content-Disposition": "inline; filename=speech.mp3",
                "X-Duration-Sec": str(result.duration_sec),
            }
        )

    except Exception as e:
        logger.error(f"TTS stream error: {e}")
        raise HTTPException(status_code=500, detail=f"TTS stream failed: {str(e)}")


@router.post("/ocr")
async def ocr_document(
    file: UploadFile = File(..., description="Document (PDF or image)"),
    language_hint: Optional[str] = Form(None, description="Language hint: ar, fr, en"),
    current_user: dict = Depends(optional_user),
):
    """
    OCR - Extract text from documents.
    Supports PDF and images (PNG, JPG, TIFF).

    Features:
    - Multilingual (Arabic, French, English)
    - Automatic language detection
    - Darija text normalization
    - LLM Vision fallback for low-quality scans
    """
    try:
        file_bytes = await file.read()

        if not file_bytes:
            raise HTTPException(status_code=400, detail="Empty file")

        result = await ocr_pipeline.auto_ocr(
            file_data=file_bytes,
            filename=file.filename,
            language_hint=language_hint,
        )

        return {
            "text": result.text,
            "language": result.language,
            "language_name": result.language_name,
            "confidence": result.confidence,
            "is_pdf": result.is_pdf,
            "pages": result.pages,
            "engine": result.engine.value if hasattr(result.engine, 'value') else str(result.engine),
            "fallback_used": result.fallback_used,
            "extracted_dates": result.extracted_dates,
            "extracted_amounts": result.extracted_amounts,
            "processing_time_ms": result.processing_time_ms,
            "warnings": result.warnings,
            "error": result.error,
        }

    except Exception as e:
        logger.error(f"OCR error: {e}")
        raise HTTPException(status_code=500, detail=f"OCR failed: {str(e)}")


@router.post("/text")
async def process_text(
    request: TextProcessRequest,
    current_user: dict = Depends(optional_user),
):
    """
    Process text input (NLP + Agent response).
    Same as /process but for text input instead of audio.
    """
    import time
    start_time = time.time()

    try:
        session_id = request.session_id or f"text_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

        mode_map = {
            "hotline": VoiceAgentMode.HOTLINE,
            "secretary": VoiceAgentMode.SECRETARY,
            "restaurant": VoiceAgentMode.RESTAURANT,
            "ai_double": VoiceAgentMode.AI_DOUBLE,
            "general": VoiceAgentMode.GENERAL,
        }
        agent_mode = mode_map.get(request.mode, VoiceAgentMode.GENERAL)

        user_id = current_user.get("id") if current_user else None

        # Process with voice agent
        agent_response = await voice_ai_agent.process_voice_input(
            text=request.text,
            session_id=session_id,
            user_id=user_id,
            mode=agent_mode,
        )

        # Get NLP analysis
        nlp = voice_ai_agent.nlp
        detected_lang, _ = nlp.detect_language(request.text)
        intents = nlp.detect_intent(request.text, agent_mode)
        entities = nlp.extract_entities(request.text, agent_mode)
        emotion = nlp.detect_emotion(request.text)

        processing_time_ms = int((time.time() - start_time) * 1000)

        return {
            "input_text": request.text,
            "detected_language": detected_lang.value if hasattr(detected_lang, 'value') else str(detected_lang),
            "detected_emotion": emotion,
            "intents": [{"intent": i[0], "confidence": i[1]} for i in intents],
            "entities": entities,
            "response_text": agent_response.text,
            "response_language": agent_response.language.value if hasattr(agent_response.language, 'value') else str(agent_response.language),
            "action": agent_response.action,
            "action_data": agent_response.action_data,
            "suggested_responses": agent_response.suggested_responses,
            "anticipation": agent_response.anticipation,
            "session_id": session_id,
            "mode": request.mode,
            "processing_time_ms": processing_time_ms,
        }

    except Exception as e:
        logger.error(f"Text processing error: {e}")
        raise HTTPException(status_code=500, detail=f"Text processing failed: {str(e)}")


# ============================================
# MODE & SESSION ENDPOINTS
# ============================================

@router.get("/modes")
async def get_modes():
    """Get available voice agent modes with descriptions."""
    return {
        "modes": [
            {
                "id": "general",
                "name": "Général",
                "name_ar": "عام",
                "description": "Conversation générale multilingue",
                "icon": "💬",
            },
            {
                "id": "hotline",
                "name": "Hotline",
                "name_ar": "خط الدعم",
                "description": "Centre d'appels / Support client",
                "icon": "📞",
            },
            {
                "id": "secretary",
                "name": "Secrétaire",
                "name_ar": "سكرتير",
                "description": "Assistant personnel / Agenda / Rappels",
                "icon": "📋",
            },
            {
                "id": "restaurant",
                "name": "Restaurant",
                "name_ar": "مطعم",
                "description": "Prise de commandes / Livraison",
                "icon": "🍽️",
            },
            {
                "id": "ai_double",
                "name": "Double IA",
                "name_ar": "التوأم الذكي",
                "description": "Clone IA personnel - Apprend votre style",
                "icon": "🤖",
            },
        ]
    }


@router.get("/session/{session_id}")
async def get_session(
    session_id: str,
    current_user: dict = Depends(optional_user),
):
    """Get session context and history."""
    if session_id not in voice_ai_agent.contexts:
        raise HTTPException(status_code=404, detail="Session not found")

    context = voice_ai_agent.contexts[session_id]

    return {
        "session_id": session_id,
        "mode": context.mode.value,
        "detected_language": context.detected_language.value if hasattr(context.detected_language, 'value') else str(context.detected_language),
        "emotion": context.emotion,
        "entities": context.entities,
        "conversation_history": context.conversation_history[-10:],  # Last 10 messages
        "anticipated_intents": context.anticipated_intents,
        "created_at": context.created_at.isoformat(),
        "last_activity": context.last_activity.isoformat(),
    }


@router.delete("/session/{session_id}")
async def delete_session(
    session_id: str,
    current_user: dict = Depends(optional_user),
):
    """Delete a session."""
    if session_id in voice_ai_agent.contexts:
        del voice_ai_agent.contexts[session_id]
        return {"status": "deleted", "session_id": session_id}

    raise HTTPException(status_code=404, detail="Session not found")


# ============================================
# AI DOUBLE ENDPOINTS
# ============================================

@router.post("/ai-double/learn")
async def learn_user_preference(
    preference_key: str = Form(..., description="Preference key (e.g., 'greeting_style')"),
    preference_value: str = Form(..., description="Preference value"),
    current_user: dict = Depends(get_current_user),
):
    """
    Learn user preference for AI Double mode.
    The AI will remember and use these preferences.
    """
    user_id = current_user.get("id") or current_user.get("email")

    if not user_id:
        raise HTTPException(status_code=401, detail="User ID required")

    voice_ai_agent.learn_user_preference(user_id, preference_key, preference_value)

    return {
        "status": "learned",
        "user_id": user_id,
        "preference_key": preference_key,
        "preference_value": preference_value,
    }


@router.get("/ai-double/profile")
async def get_user_profile(
    current_user: dict = Depends(get_current_user),
):
    """Get learned user profile for AI Double mode."""
    user_id = current_user.get("id") or current_user.get("email")

    if not user_id:
        raise HTTPException(status_code=401, detail="User ID required")

    profile = voice_ai_agent.user_profiles.get(user_id, {})

    return {
        "user_id": user_id,
        "profile": profile,
        "preferences_count": len(profile),
    }


# ============================================
# HEALTH & STATUS
# ============================================

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check health of all voice AI services."""
    try:
        stt_service = get_stt_service()
        tts_service = get_tts_service()

        stt_health = await stt_service.health()
        tts_health = await tts_service.health()
        ocr_status = ocr_pipeline.get_status()

        return HealthResponse(
            status="ok",
            services={
                "stt": stt_health.ready,
                "tts": tts_health.ready,
                "ocr_tesseract": ocr_status.get("tesseract_available", False),
                "ocr_pdf": ocr_status.get("pdf_available", False),
                "nlp": True,
                "voice_agent": True,
            },
            modes=["general", "hotline", "secretary", "restaurant", "ai_double"],
            languages=["ar", "fr", "en", "dz", "mixed"],
        )
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return HealthResponse(
            status="error",
            services={"error": str(e)},
        )


@router.get("/languages")
async def get_supported_languages():
    """Get supported languages and dialects."""
    return {
        "languages": [
            {
                "code": "ar",
                "name": "Arabe",
                "name_native": "العربية",
                "dialects": ["msa", "darija"],
                "direction": "rtl",
            },
            {
                "code": "fr",
                "name": "Français",
                "name_native": "Français",
                "dialects": [],
                "direction": "ltr",
            },
            {
                "code": "en",
                "name": "Anglais",
                "name_native": "English",
                "dialects": [],
                "direction": "ltr",
            },
            {
                "code": "dz",
                "name": "Darija",
                "name_native": "الدارجة",
                "dialects": ["algerian", "tunisian", "moroccan"],
                "direction": "rtl",
                "note": "Algerian Arabic with French loanwords",
            },
            {
                "code": "mixed",
                "name": "Mixte",
                "name_native": "مختلط",
                "description": "Code-switching between Arabic/French/English",
                "direction": "auto",
            },
        ],
        "code_switching_supported": True,
        "darija_normalization": True,
    }
