"""
VOICE_AGENT - Service Principal
===============================
Agent vocal complet pour iaFactoryDZ
Pipeline: Audio → STT → DARIJA_NLP → BIG RAG → LLM → TTS → Audio

Orchestre tous les composants pour créer un assistant vocal
qui comprend et parle darija algérienne.
"""

import os
import time
import logging
import base64
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime
import uuid

# Models
from .voice_agent_models import (
    VoiceAgentRequest,
    VoiceAgentResponse,
    VoiceAgentTextRequest,
    VoiceAgentAudioRequest,
    VoiceAgentStatus,
    ConversationState,
    ConversationMessage,
    ConversationContext,
    ProcessingStepResult,
    IntentDetectionResult,
    AgentMode,
    AgentLanguage,
    AgentDialect,
    ConversationStatus,
    ProcessingStep,
    IntentType,
    SYSTEM_PROMPTS,
    INTENT_KEYWORDS,
    MAX_CONVERSATION_LENGTH,
)

# STT Service
from .stt_service import get_stt_service, STTService
from .stt_models import STTRequest, STTLanguage, STTDialect

# Multi-tenant system prompts
SYSTEM_PROMPT_CH = os.getenv("SYSTEM_PROMPT_CH")

# TTS Service
from .tts_service import get_tts_service, TTSService
from .tts_models import TTSRequest, TTSLanguage, TTSDialect

# DARIJA_NLP
try:
    from app.darija.darija_normalizer import normalize_darija
    from app.darija.darija_cleaner import clean_text
    DARIJA_NLP_AVAILABLE = True
except ImportError:
    DARIJA_NLP_AVAILABLE = False
    def normalize_darija(text: str) -> Dict[str, Any]:
        return {"normalized": text, "is_arabizi": False, "dialect": "unknown", "confidence": 0.0}
    def clean_text(text: str) -> str:
        return text.strip()

# BIG RAG (optionnel)
try:
    from app.bigrag.rag_service import get_rag_service
    BIGRAG_AVAILABLE = True
except ImportError:
    BIGRAG_AVAILABLE = False
    def get_rag_service():
        return None

# LLM Client
try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


logger = logging.getLogger(__name__)


# ============================================
# CONVERSATION STORE (In-Memory)
# ============================================

class ConversationStore:
    """Store en mémoire pour les conversations (à remplacer par Redis/DB)"""
    
    def __init__(self):
        self._conversations: Dict[str, ConversationState] = {}
    
    def get(self, conversation_id: str) -> Optional[ConversationState]:
        return self._conversations.get(conversation_id)
    
    def create(self, context: Optional[ConversationContext] = None) -> ConversationState:
        state = ConversationState(
            context=context or ConversationContext()
        )
        self._conversations[state.id] = state
        return state
    
    def update(self, state: ConversationState) -> None:
        state.updated_at = datetime.utcnow()
        state.last_activity = datetime.utcnow()
        self._conversations[state.id] = state
    
    def delete(self, conversation_id: str) -> bool:
        if conversation_id in self._conversations:
            del self._conversations[conversation_id]
            return True
        return False
    
    def count_active(self) -> int:
        return sum(1 for c in self._conversations.values() 
                   if c.status == ConversationStatus.ACTIVE)
    
    def cleanup_old(self, max_age_hours: int = 24) -> int:
        """Supprime les conversations inactives"""
        now = datetime.utcnow()
        to_delete = []
        for cid, conv in self._conversations.items():
            age = (now - conv.last_activity).total_seconds() / 3600
            if age > max_age_hours:
                to_delete.append(cid)
        
        for cid in to_delete:
            del self._conversations[cid]
        
        return len(to_delete)


# Global store
_conversation_store = ConversationStore()


# ============================================
# VOICE AGENT SERVICE
# ============================================

class VoiceAgentService:
    """
    Service principal de l'agent vocal
    
    Pipeline complet:
    1. STT: Audio → Texte (via Whisper)
    2. NLP: Normalisation darija + détection langue
    3. Intent: Détection intention
    4. RAG: Récupération contexte (optionnel)
    5. LLM: Génération réponse
    6. TTS: Texte → Audio
    """
    
    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        default_model: str = "gpt-4o-mini",
        enable_rag: bool = True,
        enable_tts: bool = True,
    ):
        """
        Initialise l'agent vocal
        
        Args:
            openai_api_key: Clé API OpenAI
            default_model: Modèle LLM par défaut
            enable_rag: Activer le RAG
            enable_tts: Activer le TTS
        """
        self.default_model = default_model
        self.enable_rag = enable_rag and BIGRAG_AVAILABLE
        self.enable_tts = enable_tts
        
        # OpenAI client
        api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.openai_client = AsyncOpenAI(api_key=api_key) if OPENAI_AVAILABLE and api_key else None
        
        # Services
        self.stt_service: STTService = get_stt_service()
        self.tts_service: TTSService = get_tts_service()
        self.rag_service = get_rag_service() if self.enable_rag else None
        
        # Conversation store
        self.conversations = _conversation_store
        
        logger.info(f"VoiceAgentService initialized - LLM: {self.openai_client is not None}, "
                    f"RAG: {self.enable_rag}, TTS: {self.enable_tts}")
    
    # ----------------------------------------
    # MAIN PROCESSING METHOD
    # ----------------------------------------
    
    async def process(self, request: VoiceAgentRequest) -> VoiceAgentResponse:
        """
        Traite une requête vocale complète
        
        Pipeline:
        1. Récupérer/créer conversation
        2. STT si audio fourni
        3. Normalisation DARIJA_NLP
        4. Détection intention
        5. RAG si activé
        6. Génération LLM
        7. TTS si demandé
        """
        start_time = time.time()
        pipeline_steps: List[ProcessingStepResult] = []
        
        # 1. Conversation
        conversation = self._get_or_create_conversation(
            request.conversation_id,
            request.context
        )
        
        # 2. Obtenir le texte input (STT ou direct)
        input_text = ""
        detected_language = "ar"
        detected_dialect = "darija"
        is_arabizi = False
        
        if request.audio_base64:
            # STT
            stt_result = await self._process_stt(
                request.audio_base64,
                request.language_hint,
                request.dialect,
            )
            pipeline_steps.append(stt_result["step"])
            
            if stt_result["success"]:
                input_text = stt_result["text"]
                detected_language = stt_result.get("language", "ar")
                detected_dialect = stt_result.get("dialect", "darija")
                is_arabizi = stt_result.get("is_arabizi", False)
            else:
                return self._error_response(
                    conversation.id,
                    "Erreur transcription audio",
                    ProcessingStep.STT,
                    pipeline_steps,
                )
        elif request.text:
            input_text = request.text
        else:
            return self._error_response(
                conversation.id,
                "Aucun input (audio ou texte) fourni",
                None,
                pipeline_steps,
            )
        
        # 3. Normalisation DARIJA_NLP
        nlp_result = await self._process_nlp(input_text)
        pipeline_steps.append(nlp_result["step"])
        
        input_text_normalized = nlp_result.get("normalized", input_text)
        if nlp_result.get("is_arabizi"):
            is_arabizi = True
        if nlp_result.get("dialect"):
            detected_dialect = nlp_result["dialect"]
        
        # 4. Détection intention
        intent_result = self._detect_intent(input_text_normalized)
        pipeline_steps.append(ProcessingStepResult(
            step=ProcessingStep.INTENT,
            success=True,
            duration_ms=1,
            output={"intent": intent_result.intent.value, "confidence": intent_result.confidence}
        ))
        
        # 5. RAG (si activé et pertinent)
        rag_context = ""
        rag_sources = []
        rag_used = False
        
        if request.use_rag and self.enable_rag and self.rag_service:
            rag_result = await self._process_rag(
                input_text_normalized,
                conversation.context.country,
                request.rag_collection,
                request.rag_top_k,
            )
            pipeline_steps.append(rag_result["step"])
            
            if rag_result["success"]:
                rag_context = rag_result.get("context", "")
                rag_sources = rag_result.get("sources", [])
                rag_used = True
        
        # 6. Génération LLM
        # Sélection du prompt système selon le tenant
        system_prompt_to_use = request.system_prompt
        if not system_prompt_to_use and request.tenant:
            if request.tenant.lower() in ["swiss", "ch", "switzerland", "suisse"]:
                system_prompt_to_use = SYSTEM_PROMPT_CH
        
        llm_result = await self._process_llm(
            input_text_normalized,
            conversation,
            request.mode,
            rag_context,
            system_prompt_to_use,
            request.temperature,
            request.max_tokens,
        )
        pipeline_steps.append(llm_result["step"])
        
        if not llm_result["success"]:
            return self._error_response(
                conversation.id,
                "Erreur génération réponse",
                ProcessingStep.LLM,
                pipeline_steps,
            )
        
        output_text = llm_result["text"]
        model_used = llm_result.get("model", self.default_model)
        
        # 7. TTS (si demandé)
        output_audio_base64 = None
        audio_duration_sec = None
        voice_used = None
        
        if request.return_audio and self.enable_tts:
            tts_result = await self._process_tts(
                output_text,
                detected_language,
                detected_dialect,
                request.voice_id,
            )
            pipeline_steps.append(tts_result["step"])
            
            if tts_result["success"]:
                output_audio_base64 = tts_result.get("audio_base64")
                audio_duration_sec = tts_result.get("duration_sec")
                voice_used = tts_result.get("voice_id")
        
        # Mettre à jour la conversation
        user_message = ConversationMessage(
            role="user",
            content=input_text,
            language=detected_language,
            dialect=detected_dialect,
            is_arabizi=is_arabizi,
            intent=intent_result.intent,
            intent_confidence=intent_result.confidence,
        )
        
        assistant_message = ConversationMessage(
            role="assistant",
            content=output_text,
            audio_base64=output_audio_base64,
        )
        
        conversation.messages.append(user_message)
        conversation.messages.append(assistant_message)
        conversation.message_count = len(conversation.messages)
        conversation.total_user_chars += len(input_text)
        conversation.total_assistant_chars += len(output_text)
        conversation.detected_language = detected_language
        conversation.detected_dialect = detected_dialect
        
        self.conversations.update(conversation)
        
        # Calculer temps total
        total_time_ms = int((time.time() - start_time) * 1000)
        
        return VoiceAgentResponse(
            conversation_id=conversation.id,
            success=True,
            input_text=input_text,
            input_text_normalized=input_text_normalized if input_text_normalized != input_text else None,
            output_text=output_text,
            output_audio_base64=output_audio_base64,
            audio_duration_sec=audio_duration_sec,
            detected_language=detected_language,
            detected_dialect=detected_dialect,
            is_arabizi=is_arabizi,
            intent=intent_result.intent,
            intent_confidence=intent_result.confidence,
            rag_used=rag_used,
            rag_sources=rag_sources,
            rag_context=rag_context if rag_context else None,
            pipeline_steps=pipeline_steps,
            total_processing_time_ms=total_time_ms,
            message_index=len(conversation.messages),
            conversation_length=conversation.message_count,
            model_used=model_used,
            voice_used=voice_used,
        )
    
    # ----------------------------------------
    # PIPELINE STEPS
    # ----------------------------------------
    
    async def _process_stt(
        self,
        audio_base64: str,
        language_hint: AgentLanguage,
        dialect: AgentDialect,
    ) -> Dict[str, Any]:
        """Étape STT: Audio → Texte"""
        start = time.time()
        
        try:
            # Décoder audio
            audio_bytes = base64.b64decode(audio_base64)
            
            # Mapper les enums
            stt_lang = STTLanguage.AUTO
            if language_hint == AgentLanguage.ARABIC:
                stt_lang = STTLanguage.ARABIC
            elif language_hint == AgentLanguage.FRENCH:
                stt_lang = STTLanguage.FRENCH
            elif language_hint == AgentLanguage.ENGLISH:
                stt_lang = STTLanguage.ENGLISH
            
            stt_dialect = STTDialect.DARIJA if dialect == AgentDialect.DARIJA else STTDialect.MSA
            
            # Transcrire
            request = STTRequest(
                language_hint=stt_lang,
                dialect=stt_dialect,
                enable_darija_normalization=True,
            )
            
            response = await self.stt_service.transcribe_audio(audio_bytes, request)
            
            duration_ms = int((time.time() - start) * 1000)
            
            return {
                "success": True,
                "text": response.text_cleaned,
                "text_normalized": response.text_normalized,
                "language": response.language,
                "dialect": response.dialect,
                "is_arabizi": response.is_arabizi,
                "step": ProcessingStepResult(
                    step=ProcessingStep.STT,
                    success=True,
                    duration_ms=duration_ms,
                    output={"chars": len(response.text_cleaned), "language": response.language}
                )
            }
            
        except Exception as e:
            logger.error(f"STT error: {e}")
            return {
                "success": False,
                "error": str(e),
                "step": ProcessingStepResult(
                    step=ProcessingStep.STT,
                    success=False,
                    duration_ms=int((time.time() - start) * 1000),
                    error=str(e)
                )
            }
    
    async def _process_nlp(self, text: str) -> Dict[str, Any]:
        """Étape NLP: Normalisation darija"""
        start = time.time()
        
        try:
            # Nettoyer
            cleaned = clean_text(text)
            
            # Normaliser
            result = normalize_darija(cleaned)
            
            duration_ms = int((time.time() - start) * 1000)
            
            return {
                "success": True,
                "normalized": getattr(result, "normalized", cleaned),
                "is_arabizi": getattr(result, "is_arabizi", False),
                "dialect": getattr(result, "dialect", "unknown"),
                "confidence": getattr(result, "confidence", 0.0),
                "step": ProcessingStepResult(
                    step=ProcessingStep.NLP,
                    success=True,
                    duration_ms=duration_ms,
                    output={
                        "is_arabizi": getattr(result, "is_arabizi", False),
                        "dialect": getattr(result, "dialect", "unknown")
                    }
                )
            }
            
        except Exception as e:
            logger.error(f"NLP error: {e}")
            return {
                "success": False,
                "normalized": text,
                "step": ProcessingStepResult(
                    step=ProcessingStep.NLP,
                    success=False,
                    duration_ms=int((time.time() - start) * 1000),
                    error=str(e)
                )
            }
    
    async def _process_rag(
        self,
        query: str,
        country: str,
        collection: Optional[str],
        top_k: int,
    ) -> Dict[str, Any]:
        """Étape RAG: Récupération contexte"""
        start = time.time()
        
        try:
            # TODO: Implémenter appel BIG RAG
            # Pour l'instant, mock
            
            duration_ms = int((time.time() - start) * 1000)
            
            return {
                "success": True,
                "context": "",  # Contexte RAG
                "sources": [],  # Sources
                "step": ProcessingStepResult(
                    step=ProcessingStep.RAG,
                    success=True,
                    duration_ms=duration_ms,
                    output={"documents": 0}
                )
            }
            
        except Exception as e:
            logger.error(f"RAG error: {e}")
            return {
                "success": False,
                "step": ProcessingStepResult(
                    step=ProcessingStep.RAG,
                    success=False,
                    duration_ms=int((time.time() - start) * 1000),
                    error=str(e)
                )
            }
    
    async def _process_llm(
        self,
        user_input: str,
        conversation: ConversationState,
        mode: AgentMode,
        rag_context: str,
        custom_system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
    ) -> Dict[str, Any]:
        """Étape LLM: Génération réponse"""
        start = time.time()
        
        try:
            # Construire le system prompt
            system_prompt = custom_system_prompt or SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS[AgentMode.ASSISTANT])
            
            # Ajouter contexte RAG si disponible
            if rag_context:
                system_prompt += f"\n\nContexte documentaire:\n{rag_context}"
            
            # Construire les messages
            messages = [{"role": "system", "content": system_prompt}]
            
            # Ajouter historique conversation (limité)
            for msg in conversation.messages[-10:]:  # 10 derniers messages
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
            
            # Ajouter le nouveau message
            messages.append({"role": "user", "content": user_input})
            
            # Appeler LLM
            if self.openai_client:
                response = await self.openai_client.chat.completions.create(
                    model=self.default_model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                output_text = response.choices[0].message.content
                model_used = response.model
            else:
                # Mock response
                output_text = f"[Mock LLM] Réponse à: {user_input[:50]}..."
                model_used = "mock"
            
            duration_ms = int((time.time() - start) * 1000)
            
            return {
                "success": True,
                "text": output_text,
                "model": model_used,
                "step": ProcessingStepResult(
                    step=ProcessingStep.LLM,
                    success=True,
                    duration_ms=duration_ms,
                    output={"tokens": len(output_text.split()), "model": model_used}
                )
            }
            
        except Exception as e:
            logger.error(f"LLM error: {e}")
            return {
                "success": False,
                "text": "Désolé, je n'ai pas pu générer une réponse.",
                "step": ProcessingStepResult(
                    step=ProcessingStep.LLM,
                    success=False,
                    duration_ms=int((time.time() - start) * 1000),
                    error=str(e)
                )
            }
    
    async def _process_tts(
        self,
        text: str,
        language: str,
        dialect: str,
        voice_id: Optional[str],
    ) -> Dict[str, Any]:
        """Étape TTS: Texte → Audio"""
        start = time.time()
        
        try:
            # Mapper les paramètres
            tts_lang = TTSLanguage.ARABIC
            if language == "fr":
                tts_lang = TTSLanguage.FRENCH
            elif language == "en":
                tts_lang = TTSLanguage.ENGLISH
            
            tts_dialect = TTSDialect.DARIJA if dialect == "darija" else TTSDialect.MSA
            
            request = TTSRequest(
                text=text,
                language=tts_lang,
                dialect=tts_dialect,
                voice_id=voice_id,
            )
            
            response = await self.tts_service.synthesize(request)
            
            duration_ms = int((time.time() - start) * 1000)
            
            return {
                "success": True,
                "audio_base64": response.audio_base64,
                "duration_sec": response.duration_sec,
                "voice_id": response.used_voice_id,
                "step": ProcessingStepResult(
                    step=ProcessingStep.TTS,
                    success=True,
                    duration_ms=duration_ms,
                    output={"duration_sec": response.duration_sec}
                )
            }
            
        except Exception as e:
            logger.error(f"TTS error: {e}")
            return {
                "success": False,
                "step": ProcessingStepResult(
                    step=ProcessingStep.TTS,
                    success=False,
                    duration_ms=int((time.time() - start) * 1000),
                    error=str(e)
                )
            }
    
    # ----------------------------------------
    # INTENT DETECTION
    # ----------------------------------------
    
    def _detect_intent(self, text: str) -> IntentDetectionResult:
        """Détecte l'intention du message"""
        text_lower = text.lower()
        
        # Vérifier les mots-clés
        for intent, keywords in INTENT_KEYWORDS.items():
            for kw in keywords:
                if kw in text_lower:
                    return IntentDetectionResult(
                        intent=intent,
                        confidence=0.8,
                    )
        
        # Patterns généraux
        if "?" in text or any(q in text_lower for q in ["واش", "شكون", "وين", "علاش", "كيفاش"]):
            return IntentDetectionResult(intent=IntentType.QUESTION, confidence=0.7)
        
        return IntentDetectionResult(intent=IntentType.UNKNOWN, confidence=0.3)
    
    # ----------------------------------------
    # HELPERS
    # ----------------------------------------
    
    def _get_or_create_conversation(
        self,
        conversation_id: Optional[str],
        context: Optional[ConversationContext],
    ) -> ConversationState:
        """Récupère ou crée une conversation"""
        if conversation_id:
            existing = self.conversations.get(conversation_id)
            if existing:
                return existing
        
        return self.conversations.create(context)
    
    def _error_response(
        self,
        conversation_id: str,
        error_message: str,
        step: Optional[ProcessingStep],
        pipeline_steps: List[ProcessingStepResult],
    ) -> VoiceAgentResponse:
        """Construit une réponse d'erreur"""
        return VoiceAgentResponse(
            conversation_id=conversation_id,
            success=False,
            input_text="",
            output_text=f"Erreur: {error_message}",
            detected_language="unknown",
            pipeline_steps=pipeline_steps,
        )
    
    # ----------------------------------------
    # HEALTH & STATUS
    # ----------------------------------------
    
    async def health(self) -> VoiceAgentStatus:
        """Vérifie l'état du service"""
        stt_status = await self.stt_service.health()
        tts_status = await self.tts_service.health()
        
        components = {
            "stt": stt_status.ready,
            "tts": tts_status.ready,
            "llm": self.openai_client is not None,
            "rag": self.enable_rag and self.rag_service is not None,
            "darija_nlp": DARIJA_NLP_AVAILABLE,
        }
        
        return VoiceAgentStatus(
            ready=all([stt_status.ready, tts_status.ready, self.openai_client is not None]),
            components=components,
            active_conversations=self.conversations.count_active(),
        )
    
    def get_conversation(self, conversation_id: str) -> Optional[ConversationState]:
        """Récupère une conversation"""
        return self.conversations.get(conversation_id)
    
    def end_conversation(self, conversation_id: str) -> bool:
        """Termine une conversation"""
        conv = self.conversations.get(conversation_id)
        if conv:
            conv.status = ConversationStatus.ENDED
            self.conversations.update(conv)
            return True
        return False


# ============================================
# SINGLETON
# ============================================

_voice_agent_service: Optional[VoiceAgentService] = None


def get_voice_agent_service() -> VoiceAgentService:
    """Retourne l'instance singleton"""
    global _voice_agent_service
    if _voice_agent_service is None:
        _voice_agent_service = VoiceAgentService()
    return _voice_agent_service


def init_voice_agent_service(**kwargs) -> VoiceAgentService:
    """Initialise avec configuration custom"""
    global _voice_agent_service
    _voice_agent_service = VoiceAgentService(**kwargs)
    return _voice_agent_service
