"""
Conversation Router - Multi-Modal Conversational Interface
Supports: Text, Voice (STT/TTS), Image (OCR/VLLM)

Transforms conversations into contextual prompts for Bolt.diy
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional, List
import base64
import logging

from app.services.conversational_orchestrator import (
    conversational_orchestrator,
    InputType,
    ConversationMessage,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/conversation", tags=["Conversational AI"])


class TextInputRequest(BaseModel):
    """Text message input"""
    conversation_id: str
    message: str
    language: Optional[str] = "fr"


class VoiceInputRequest(BaseModel):
    """Voice message input (base64 audio)"""
    conversation_id: str
    audio_base64: str
    language: Optional[str] = "fr"


class ImageInputRequest(BaseModel):
    """Image input (base64)"""
    conversation_id: str
    image_base64: str
    input_type: str = "image"  # image, screenshot, document


class ConversationResponse(BaseModel):
    """Response with assistant message"""
    conversation_id: str
    message: str
    audio_base64: Optional[str] = None
    context_summary: dict


class PromptResponse(BaseModel):
    """Generated Bolt prompt"""
    conversation_id: str
    prompt: str
    ready_for_bolt: bool


# ==============================================
# TEXT INPUT
# ==============================================

@router.post("/text", response_model=ConversationResponse)
async def send_text_message(request: TextInputRequest):
    """
    Send a text message to the conversation

    The orchestrator will:
    1. Analyze the text with NLP
    2. Extract intent and entities
    3. Add to conversation context
    4. Generate contextual response
    """
    try:
        # Process input
        await conversational_orchestrator.process_input(
            conversation_id=request.conversation_id,
            input_type=InputType.TEXT,
            content=request.message,
            metadata={"language": request.language}
        )

        # Generate response
        result = await conversational_orchestrator.generate_response(
            conversation_id=request.conversation_id,
            use_tts=False
        )

        return ConversationResponse(
            conversation_id=request.conversation_id,
            message=result.get("text", ""),
            context_summary=result.get("context_summary", {})
        )

    except Exception as e:
        logger.error(f"Text input error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==============================================
# VOICE INPUT (STT)
# ==============================================

@router.post("/voice", response_model=ConversationResponse)
async def send_voice_message(request: VoiceInputRequest):
    """
    Send a voice message (audio will be transcribed via STT)

    The orchestrator will:
    1. Transcribe audio to text
    2. Analyze with NLP
    3. Generate response (optionally with TTS audio)
    """
    try:
        # Decode audio
        audio_bytes = base64.b64decode(request.audio_base64)

        # Process input
        await conversational_orchestrator.process_input(
            conversation_id=request.conversation_id,
            input_type=InputType.VOICE,
            content=audio_bytes,
            metadata={"language": request.language}
        )

        # Generate response with TTS
        result = await conversational_orchestrator.generate_response(
            conversation_id=request.conversation_id,
            use_tts=True
        )

        return ConversationResponse(
            conversation_id=request.conversation_id,
            message=result.get("text", ""),
            audio_base64=result.get("audio"),
            context_summary=result.get("context_summary", {})
        )

    except Exception as e:
        logger.error(f"Voice input error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/voice/upload")
async def upload_voice_message(
    conversation_id: str = Form(...),
    audio: UploadFile = File(...),
    language: str = Form("fr"),
    use_tts: bool = Form(True)
):
    """
    Upload audio file for voice input

    Supports: WAV, MP3, WebM, OGG
    """
    try:
        audio_bytes = await audio.read()

        # Process input
        await conversational_orchestrator.process_input(
            conversation_id=conversation_id,
            input_type=InputType.VOICE,
            content=audio_bytes,
            metadata={"language": language, "filename": audio.filename}
        )

        # Generate response
        result = await conversational_orchestrator.generate_response(
            conversation_id=conversation_id,
            use_tts=use_tts
        )

        return {
            "conversation_id": conversation_id,
            "transcribed_text": result.get("text", ""),
            "audio_base64": result.get("audio") if use_tts else None,
            "context_summary": result.get("context_summary", {})
        }

    except Exception as e:
        logger.error(f"Voice upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==============================================
# IMAGE INPUT (OCR / VLLM)
# ==============================================

@router.post("/image", response_model=ConversationResponse)
async def send_image(request: ImageInputRequest):
    """
    Send an image for analysis

    input_type options:
    - image: General image analysis with VLLM
    - screenshot: UI screenshot analysis for app development
    - document: Document OCR for text extraction
    """
    try:
        # Decode image
        image_bytes = base64.b64decode(request.image_base64)

        # Determine input type
        input_type_map = {
            "image": InputType.IMAGE,
            "screenshot": InputType.SCREENSHOT,
            "document": InputType.DOCUMENT
        }
        input_type = input_type_map.get(request.input_type, InputType.IMAGE)

        # Process input
        await conversational_orchestrator.process_input(
            conversation_id=request.conversation_id,
            input_type=input_type,
            content=image_bytes
        )

        # Generate response
        result = await conversational_orchestrator.generate_response(
            conversation_id=request.conversation_id,
            use_tts=False
        )

        return ConversationResponse(
            conversation_id=request.conversation_id,
            message=result.get("text", ""),
            context_summary=result.get("context_summary", {})
        )

    except Exception as e:
        logger.error(f"Image input error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/image/upload")
async def upload_image(
    conversation_id: str = Form(...),
    image: UploadFile = File(...),
    input_type: str = Form("image")
):
    """
    Upload image file for analysis

    Supports: PNG, JPG, WebP, PDF
    """
    try:
        image_bytes = await image.read()

        # Determine input type
        input_type_map = {
            "image": InputType.IMAGE,
            "screenshot": InputType.SCREENSHOT,
            "document": InputType.DOCUMENT
        }
        it = input_type_map.get(input_type, InputType.IMAGE)

        # Auto-detect document
        if image.filename and image.filename.lower().endswith('.pdf'):
            it = InputType.DOCUMENT

        # Process input
        await conversational_orchestrator.process_input(
            conversation_id=conversation_id,
            input_type=it,
            content=image_bytes,
            metadata={"filename": image.filename}
        )

        # Generate response
        result = await conversational_orchestrator.generate_response(
            conversation_id=conversation_id,
            use_tts=False
        )

        return {
            "conversation_id": conversation_id,
            "analysis": result.get("text", ""),
            "context_summary": result.get("context_summary", {})
        }

    except Exception as e:
        logger.error(f"Image upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==============================================
# PROMPT GENERATION
# ==============================================

@router.get("/{conversation_id}/prompt", response_model=PromptResponse)
async def get_bolt_prompt(conversation_id: str):
    """
    Generate Bolt prompt from conversation

    Transforms the entire conversation history into
    a contextual prompt ready for code generation.
    """
    try:
        prompt = conversational_orchestrator.generate_bolt_prompt(conversation_id)

        if not prompt:
            raise HTTPException(status_code=404, detail="Conversation not found")

        return PromptResponse(
            conversation_id=conversation_id,
            prompt=prompt,
            ready_for_bolt=True
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prompt generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==============================================
# CONVERSATION MANAGEMENT
# ==============================================

@router.get("/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation details and history"""
    context = conversational_orchestrator.get_conversation(conversation_id)

    if not context:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return {
        "conversation_id": context.conversation_id,
        "messages": [
            {
                "role": msg.role,
                "content": msg.content,
                "input_type": msg.input_type.value,
                "timestamp": msg.timestamp
            }
            for msg in context.messages
        ],
        "project_intent": context.project_intent,
        "detected_features": context.detected_features,
        "detected_tech_stack": context.detected_tech_stack,
        "language": context.language,
        "created_at": context.created_at,
        "updated_at": context.updated_at
    }


@router.post("/new")
async def create_conversation(language: str = "fr"):
    """Create a new conversation"""
    import uuid
    conversation_id = str(uuid.uuid4())[:8]

    # Initialize conversation
    await conversational_orchestrator.process_input(
        conversation_id=conversation_id,
        input_type=InputType.TEXT,
        content="[Nouvelle conversation initialisée]",
        metadata={"language": language, "system": True}
    )

    context = conversational_orchestrator.get_conversation(conversation_id)

    return {
        "conversation_id": conversation_id,
        "language": language,
        "created_at": context.created_at if context else None,
        "welcome_message": "Bonjour! Je suis prêt à vous aider à créer votre projet. Décrivez-moi votre idée ou envoyez une image/capture d'écran."
    }
