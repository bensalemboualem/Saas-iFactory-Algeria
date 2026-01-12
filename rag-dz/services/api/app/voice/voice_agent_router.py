"""
VOICE_AGENT - Router FastAPI
============================
Endpoints pour l'agent vocal iaFactoryDZ

Routes principales:
- POST /chat      - Pipeline complet (audio/texte → réponse)
- POST /text      - Pipeline texte seulement
- POST /audio     - Pipeline audio seulement
- GET  /health    - État du service
- GET  /status    - Status détaillé
- Gestion conversations
"""

import logging
from typing import Optional, List
from datetime import datetime

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query
from fastapi.responses import JSONResponse

from .voice_agent_models import (
    VoiceAgentRequest,
    VoiceAgentResponse,
    VoiceAgentTextRequest,
    VoiceAgentAudioRequest,
    VoiceAgentStatus,
    ConversationState,
    AgentMode,
    AgentLanguage,
    AgentDialect,
    ConversationSummary,
)
from .voice_agent_service import get_voice_agent_service


logger = logging.getLogger(__name__)

# Router avec prefix /api/agent/voice
router = APIRouter(prefix="/api/agent/voice", tags=["🤖 Voice Agent DZ"])


# ============================================
# HEALTH & STATUS
# ============================================

@router.get("/health")
async def health_check():
    """
    Vérification rapide de santé
    
    Returns:
        État basique du service
    """
    try:
        service = get_voice_agent_service()
        status = await service.health()
        
        return {
            "status": "healthy" if status.ready else "degraded",
            "ready": status.ready,
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "ready": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }
        )


@router.get("/status", response_model=VoiceAgentStatus)
async def detailed_status():
    """
    Status détaillé du service
    
    Returns:
        État de chaque composant: STT, TTS, LLM, RAG, DARIJA_NLP
    """
    try:
        service = get_voice_agent_service()
        return await service.health()
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# MAIN CHAT ENDPOINT
# ============================================

@router.post("/chat", response_model=VoiceAgentResponse)
async def voice_chat(request: VoiceAgentRequest):
    """
    🎤 Pipeline vocal complet
    
    Accepte audio OU texte, retourne réponse (avec audio optionnel)
    
    Pipeline:
    1. STT: Audio → Texte (si audio fourni)
    2. NLP: Normalisation darija + détection langue
    3. Intent: Détection intention
    4. RAG: Récupération contexte (optionnel)
    5. LLM: Génération réponse
    6. TTS: Texte → Audio (si demandé)
    
    Args:
        request: VoiceAgentRequest avec audio_base64 ou text
    
    Returns:
        VoiceAgentResponse avec texte et audio de réponse
    """
    try:
        service = get_voice_agent_service()
        response = await service.process(request)
        
        return response
        
    except Exception as e:
        logger.error(f"Voice chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# TEXT-ONLY ENDPOINT
# ============================================

@router.post("/text", response_model=VoiceAgentResponse)
async def text_chat(request: VoiceAgentTextRequest):
    """
    💬 Chat texte seulement
    
    Pas de STT, entrée texte directe
    
    Args:
        request: VoiceAgentTextRequest avec text
    
    Returns:
        VoiceAgentResponse
    """
    try:
        # Convertir en VoiceAgentRequest
        agent_request = VoiceAgentRequest(
            text=request.text,
            mode=request.mode,
            language_hint=request.language_hint,
            dialect=request.dialect,
            conversation_id=request.conversation_id,
            use_rag=request.use_rag,
            rag_collection=request.rag_collection,
            rag_top_k=request.rag_top_k,
            return_audio=request.return_audio,
            voice_id=request.voice_id,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            tenant=request.tenant,
            system_prompt=request.system_prompt,
        )
        
        service = get_voice_agent_service()
        return await service.process(agent_request)
        
    except Exception as e:
        logger.error(f"Text chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# AUDIO-ONLY ENDPOINT
# ============================================

@router.post("/audio", response_model=VoiceAgentResponse)
async def audio_chat(request: VoiceAgentAudioRequest):
    """
    🎙️ Chat audio seulement
    
    Entrée audio obligatoire, retourne toujours audio
    
    Args:
        request: VoiceAgentAudioRequest avec audio_base64
    
    Returns:
        VoiceAgentResponse avec audio
    """
    try:
        # Convertir en VoiceAgentRequest
        agent_request = VoiceAgentRequest(
            audio_base64=request.audio_base64,
            mode=request.mode,
            language_hint=request.language_hint,
            dialect=request.dialect,
            conversation_id=request.conversation_id,
            use_rag=request.use_rag,
            rag_collection=request.rag_collection,
            rag_top_k=request.rag_top_k,
            return_audio=True,  # Toujours audio
            voice_id=request.voice_id,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        
        service = get_voice_agent_service()
        return await service.process(agent_request)
        
    except Exception as e:
        logger.error(f"Audio chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# FILE UPLOAD ENDPOINT
# ============================================

@router.post("/upload", response_model=VoiceAgentResponse)
async def upload_audio_chat(
    audio: UploadFile = File(..., description="Fichier audio (wav, mp3, ogg, m4a)"),
    mode: AgentMode = Form(AgentMode.ASSISTANT),
    language_hint: AgentLanguage = Form(AgentLanguage.AUTO),
    dialect: AgentDialect = Form(AgentDialect.DARIJA),
    conversation_id: Optional[str] = Form(None),
    use_rag: bool = Form(False),
    rag_collection: Optional[str] = Form(None),
    rag_top_k: int = Form(5),
    return_audio: bool = Form(True),
    voice_id: Optional[str] = Form(None),
    tenant: Optional[str] = Form(None, description="Tenant: swiss, algeria"),
):
    """
    📤 Upload fichier audio
    
    Permet d'envoyer un fichier audio au lieu de base64
    
    Args:
        audio: Fichier audio
        mode: Mode agent
        language_hint: Indice de langue
        dialect: Dialecte
        ...
    
    Returns:
        VoiceAgentResponse
    """
    try:
        import base64
        
        # Lire le fichier
        audio_bytes = await audio.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        
        # Créer la requête
        request = VoiceAgentRequest(
            audio_base64=audio_base64,
            mode=mode,
            language_hint=language_hint,
            dialect=dialect,
            conversation_id=conversation_id,
            use_rag=use_rag,
            rag_collection=rag_collection,
            rag_top_k=rag_top_k,
            return_audio=return_audio,
            voice_id=voice_id,
            tenant=tenant,
        )
        
        service = get_voice_agent_service()
        return await service.process(request)
        
    except Exception as e:
        logger.error(f"Upload chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# CONVERSATION MANAGEMENT
# ============================================

@router.get("/conversation/{conversation_id}")
async def get_conversation(conversation_id: str):
    """
    📜 Récupérer une conversation
    
    Args:
        conversation_id: ID de la conversation
    
    Returns:
        État complet de la conversation
    """
    try:
        service = get_voice_agent_service()
        conversation = service.get_conversation(conversation_id)
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Retourner sans les audio base64 (trop lourd)
        messages_light = []
        for msg in conversation.messages:
            messages_light.append({
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "language": msg.language,
                "dialect": msg.dialect,
                "is_arabizi": msg.is_arabizi,
                "intent": msg.intent.value if msg.intent else None,
                "timestamp": msg.timestamp.isoformat(),
                "has_audio": msg.audio_base64 is not None,
            })
        
        return {
            "id": conversation.id,
            "status": conversation.status.value,
            "mode": conversation.mode.value,
            "message_count": conversation.message_count,
            "messages": messages_light,
            "context": {
                "country": conversation.context.country,
                "user_id": conversation.context.user_id,
                "topic": conversation.context.topic,
            },
            "detected_language": conversation.detected_language,
            "detected_dialect": conversation.detected_dialect,
            "created_at": conversation.created_at.isoformat(),
            "updated_at": conversation.updated_at.isoformat(),
            "stats": {
                "total_user_chars": conversation.total_user_chars,
                "total_assistant_chars": conversation.total_assistant_chars,
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get conversation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/conversation/{conversation_id}/end")
async def end_conversation(conversation_id: str):
    """
    ⏹️ Terminer une conversation
    
    Args:
        conversation_id: ID de la conversation
    
    Returns:
        Confirmation
    """
    try:
        service = get_voice_agent_service()
        success = service.end_conversation(conversation_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return {
            "success": True,
            "message": "Conversation ended",
            "conversation_id": conversation_id,
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"End conversation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/conversation/new")
async def new_conversation(
    mode: AgentMode = AgentMode.ASSISTANT,
    country: str = "DZ",
    topic: Optional[str] = None,
):
    """
    🆕 Créer nouvelle conversation
    
    Args:
        mode: Mode de l'agent
        country: Pays (DZ par défaut)
        topic: Sujet de conversation
    
    Returns:
        ID de la nouvelle conversation
    """
    try:
        from .voice_agent_models import ConversationContext
        
        service = get_voice_agent_service()
        
        context = ConversationContext(
            country=country,
            topic=topic,
        )
        
        conversation = service.conversations.create(context)
        conversation.mode = mode
        service.conversations.update(conversation)
        
        return {
            "success": True,
            "conversation_id": conversation.id,
            "mode": mode.value,
            "country": country,
            "created_at": conversation.created_at.isoformat(),
        }
        
    except Exception as e:
        logger.error(f"New conversation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# DEMO ENDPOINTS
# ============================================

@router.get("/demo/greeting")
async def demo_greeting():
    """
    👋 Demo: Salutation en darija
    
    Returns:
        Réponse de démonstration
    """
    try:
        from .voice_agent_models import VoiceAgentRequest, AgentMode
        
        request = VoiceAgentRequest(
            text="السلام عليكم، واش راك؟",
            mode=AgentMode.CONVERSATION,
            return_audio=True,
        )
        
        service = get_voice_agent_service()
        response = await service.process(request)
        
        return {
            "demo": "greeting",
            "input": request.text,
            "output": response.output_text,
            "has_audio": response.output_audio_base64 is not None,
            "detected_dialect": response.detected_dialect,
            "intent": response.intent.value if response.intent else None,
            "processing_time_ms": response.total_processing_time_ms,
        }
        
    except Exception as e:
        logger.error(f"Demo greeting error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/demo/question")
async def demo_question():
    """
    ❓ Demo: Question en darija
    
    Returns:
        Réponse de démonstration
    """
    try:
        from .voice_agent_models import VoiceAgentRequest, AgentMode
        
        request = VoiceAgentRequest(
            text="واش تقدر تعاونني نفهم كيفاش نخدم مع CASNOS؟",
            mode=AgentMode.PME_ADVISOR,
            return_audio=True,
            use_rag=True,
        )
        
        service = get_voice_agent_service()
        response = await service.process(request)
        
        return {
            "demo": "question",
            "input": request.text,
            "output": response.output_text,
            "has_audio": response.output_audio_base64 is not None,
            "rag_used": response.rag_used,
            "intent": response.intent.value if response.intent else None,
            "processing_time_ms": response.total_processing_time_ms,
        }
        
    except Exception as e:
        logger.error(f"Demo question error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/demo/arabizi")
async def demo_arabizi():
    """
    🔤 Demo: Arabizi → Darija
    
    Returns:
        Réponse de démonstration avec conversion arabizi
    """
    try:
        from .voice_agent_models import VoiceAgentRequest, AgentMode
        
        request = VoiceAgentRequest(
            text="salam khoya, wach rak? ch7al el wa9t?",
            mode=AgentMode.CONVERSATION,
            return_audio=True,
        )
        
        service = get_voice_agent_service()
        response = await service.process(request)
        
        return {
            "demo": "arabizi",
            "input": request.text,
            "input_normalized": response.input_text_normalized,
            "output": response.output_text,
            "is_arabizi": response.is_arabizi,
            "has_audio": response.output_audio_base64 is not None,
            "processing_time_ms": response.total_processing_time_ms,
        }
        
    except Exception as e:
        logger.error(f"Demo arabizi error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# INFO ENDPOINTS
# ============================================

@router.get("/modes")
async def list_modes():
    """
    📋 Liste des modes disponibles
    
    Returns:
        Tous les modes de l'agent
    """
    from .voice_agent_models import SYSTEM_PROMPTS
    
    return {
        "modes": [
            {
                "id": mode.value,
                "name": mode.name,
                "description": SYSTEM_PROMPTS.get(mode, "")[:200] + "...",
            }
            for mode in AgentMode
        ]
    }


@router.get("/intents")
async def list_intents():
    """
    🎯 Liste des intentions détectables
    
    Returns:
        Toutes les intentions et leurs mots-clés
    """
    from .voice_agent_models import INTENT_KEYWORDS, IntentType
    
    return {
        "intents": [
            {
                "id": intent.value,
                "name": intent.name,
                "keywords": list(INTENT_KEYWORDS.get(intent, []))[:10],
            }
            for intent in IntentType
        ]
    }


@router.get("/info")
async def agent_info():
    """
    ℹ️ Informations sur l'agent
    
    Returns:
        Métadonnées du service
    """
    service = get_voice_agent_service()
    status = await service.health()
    
    return {
        "name": "iaFactoryDZ Voice Agent",
        "version": "1.0.0",
        "description": "Agent vocal pour l'Algérie - Comprend et parle darija",
        "capabilities": {
            "stt": status.components.get("stt", False),
            "tts": status.components.get("tts", False),
            "llm": status.components.get("llm", False),
            "rag": status.components.get("rag", False),
            "darija_nlp": status.components.get("darija_nlp", False),
        },
        "languages": ["ar", "ar-dz", "fr", "en"],
        "dialects": ["darija", "msa"],
        "features": [
            "Transcription audio → texte (STT)",
            "Synthèse vocale (TTS)",
            "Compréhension darija algérienne",
            "Conversion arabizi → arabe",
            "Recherche documentaire (RAG)",
            "Génération de réponses (LLM)",
            "Gestion de conversations",
            "Détection d'intentions",
        ],
        "modes": [m.value for m in AgentMode],
        "active_conversations": status.active_conversations,
        "ready": status.ready,
    }
