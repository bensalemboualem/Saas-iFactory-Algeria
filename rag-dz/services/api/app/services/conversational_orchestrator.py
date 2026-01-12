"""
Conversational Orchestrator - Multi-Modal Input Processing
Supports: NLP, STT, TTS, OCR, VLLM (Vision LLM)

Transforms any input (text, voice, image) into contextual prompts
for the BMAD → Archon → Bolt workflow.

IMPORTANT: This orchestrator now persists conversations to PostgreSQL
via ConversationRepository with:
- Optimistic locking (version field)
- RLS tenant isolation
- Max 100 messages per conversation
"""
import asyncio
import logging
import base64
from typing import Optional, Dict, Any, List, Union
from datetime import datetime
from enum import Enum
from uuid import UUID
from pydantic import BaseModel
import httpx
import asyncpg

from app.config import get_settings
from app.repositories.conversation_repository import (
    ConversationRepository,
    ConversationConflictError,
    ConversationFullError,
    ConversationNotFoundError
)

logger = logging.getLogger(__name__)
settings = get_settings()


class InputType(str, Enum):
    """Supported input types"""
    TEXT = "text"           # Natural language text
    VOICE = "voice"         # Audio (STT)
    IMAGE = "image"         # Image (OCR/VLLM)
    DOCUMENT = "document"   # PDF/Doc (OCR)
    SCREENSHOT = "screenshot"  # UI Screenshot (VLLM)
    MIXED = "mixed"         # Multiple types


class ConversationMessage(BaseModel):
    """A single message in the conversation"""
    role: str  # user, assistant, system
    content: str
    input_type: InputType = InputType.TEXT
    metadata: Optional[Dict[str, Any]] = None
    timestamp: str = ""

    def __init__(self, **data):
        if not data.get("timestamp"):
            data["timestamp"] = datetime.utcnow().isoformat()
        super().__init__(**data)


class ConversationContext(BaseModel):
    """Full conversation context for prompt generation"""
    conversation_id: str
    messages: List[ConversationMessage] = []

    # Extracted information
    project_intent: Optional[str] = None
    detected_features: List[str] = []
    detected_tech_stack: List[str] = []
    detected_requirements: List[str] = []

    # Input processing results
    ocr_results: List[Dict[str, Any]] = []
    vision_analysis: List[Dict[str, Any]] = []

    # Metadata
    language: str = "fr"
    created_at: str = ""
    updated_at: str = ""


class STTService:
    """Speech-to-Text Service"""

    def __init__(self, api_url: str = None):
        self.api_url = api_url or f"http://localhost:{settings.port}"

    async def transcribe(self, audio_data: bytes, language: str = "fr") -> str:
        """Convert audio to text"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/api/voice/stt",
                    files={"audio": ("audio.wav", audio_data, "audio/wav")},
                    data={"language": language},
                    timeout=30.0
                )

                if response.status_code == 200:
                    return response.json().get("text", "")
                else:
                    logger.error(f"STT failed: {response.status_code}")
                    return ""
        except Exception as e:
            logger.error(f"STT error: {e}")
            return ""


class TTSService:
    """Text-to-Speech Service"""

    def __init__(self, api_url: str = None):
        self.api_url = api_url or f"http://localhost:{settings.port}"

    async def synthesize(self, text: str, language: str = "fr", voice: str = "default") -> bytes:
        """Convert text to audio"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/api/voice/tts",
                    json={"text": text, "language": language, "voice": voice},
                    timeout=30.0
                )

                if response.status_code == 200:
                    return response.content
                else:
                    logger.error(f"TTS failed: {response.status_code}")
                    return b""
        except Exception as e:
            logger.error(f"TTS error: {e}")
            return b""


class OCRService:
    """Optical Character Recognition Service"""

    def __init__(self, api_url: str = None):
        self.api_url = api_url or f"http://localhost:{settings.port}"

    async def extract_text(self, image_data: bytes, language: str = "fra+ara+eng") -> Dict[str, Any]:
        """Extract text from image"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/api/ocr/extract",
                    files={"image": ("image.png", image_data, "image/png")},
                    data={"language": language},
                    timeout=60.0
                )

                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(f"OCR failed: {response.status_code}")
                    return {"text": "", "confidence": 0}
        except Exception as e:
            logger.error(f"OCR error: {e}")
            return {"text": "", "confidence": 0}


class VLLMService:
    """Vision Language Model Service - Analyze images with AI"""

    def __init__(self, api_url: str = None):
        self.api_url = api_url or f"http://localhost:{settings.port}"

    async def analyze_image(
        self,
        image_data: bytes,
        prompt: str = "Décris cette image en détail",
        context: str = ""
    ) -> Dict[str, Any]:
        """Analyze image with vision LLM"""
        try:
            image_b64 = base64.b64encode(image_data).decode()

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/api/bigrag/vision",
                    json={
                        "image": image_b64,
                        "prompt": prompt,
                        "context": context
                    },
                    timeout=120.0
                )

                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(f"VLLM failed: {response.status_code}")
                    return {"analysis": "", "objects": []}
        except Exception as e:
            logger.error(f"VLLM error: {e}")
            return {"analysis": "", "objects": []}

    async def analyze_ui_screenshot(self, image_data: bytes) -> Dict[str, Any]:
        """Analyze UI screenshot for app development context"""
        prompt = """Analyse cette capture d'écran d'interface utilisateur:
        1. Identifie les composants UI (boutons, formulaires, menus, etc.)
        2. Décris la structure de la page
        3. Identifie les fonctionnalités suggérées
        4. Propose un stack technique approprié
        5. Liste les features à implémenter

        Réponds en JSON avec: components, structure, features, tech_stack, requirements"""

        return await self.analyze_image(image_data, prompt)


class NLPProcessor:
    """Natural Language Processing - Intent & Entity Extraction"""

    INTENT_PATTERNS = {
        "create_app": ["créer", "développer", "construire", "faire", "build", "create"],
        "add_feature": ["ajouter", "intégrer", "inclure", "add", "include"],
        "modify": ["modifier", "changer", "update", "change"],
        "fix": ["corriger", "réparer", "fix", "debug"],
        "explain": ["expliquer", "comment", "pourquoi", "explain", "how"],
    }

    TECH_PATTERNS = {
        "react": ["react", "reactjs", "react.js"],
        "vue": ["vue", "vuejs", "vue.js"],
        "nextjs": ["next", "nextjs", "next.js"],
        "python": ["python", "django", "flask", "fastapi"],
        "nodejs": ["node", "nodejs", "express"],
        "database": ["database", "base de données", "sql", "postgres", "mongodb"],
        "auth": ["authentification", "login", "auth", "authentication"],
        "api": ["api", "rest", "graphql"],
    }

    def extract_intent(self, text: str) -> str:
        """Extract user intent from text"""
        text_lower = text.lower()
        for intent, patterns in self.INTENT_PATTERNS.items():
            if any(p in text_lower for p in patterns):
                return intent
        return "create_app"  # Default

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract entities (tech stack, features) from text"""
        text_lower = text.lower()
        entities = {
            "tech_stack": [],
            "features": [],
        }

        for tech, patterns in self.TECH_PATTERNS.items():
            if any(p in text_lower for p in patterns):
                entities["tech_stack"].append(tech)

        return entities

    def analyze(self, text: str) -> Dict[str, Any]:
        """Full NLP analysis"""
        return {
            "intent": self.extract_intent(text),
            "entities": self.extract_entities(text),
            "language": self._detect_language(text),
        }

    def _detect_language(self, text: str) -> str:
        """Simple language detection"""
        arabic_chars = sum(1 for c in text if '\u0600' <= c <= '\u06FF')
        if arabic_chars > len(text) * 0.3:
            return "ar"
        if any(word in text.lower() for word in ["the", "is", "are", "this"]):
            return "en"
        return "fr"


class PromptTransformer:
    """Transform conversation into contextual Bolt prompt"""

    PROMPT_TEMPLATE = """# Contexte du Projet

## Résumé de la Conversation
{conversation_summary}

## Intention Détectée
{intent}

## Features Identifiées
{features}

## Stack Technique
{tech_stack}

## Requirements
{requirements}

## Analyses Visuelles
{visual_analysis}

---

# Instructions pour la Génération

Basé sur la conversation ci-dessus, génère une application complète avec:
1. Structure de fichiers organisée
2. Code fonctionnel pour chaque composant
3. Tests unitaires
4. Documentation inline

Commence par créer la structure du projet puis implémente chaque feature.
"""

    def transform(self, context: ConversationContext) -> str:
        """Transform conversation context into Bolt prompt"""

        # Summarize conversation
        conversation_summary = self._summarize_conversation(context.messages)

        # Format features
        features = "\n".join(f"- {f}" for f in context.detected_features) or "- À déterminer par l'analyse"

        # Format tech stack
        tech_stack = ", ".join(context.detected_tech_stack) or "React + Node.js (par défaut)"

        # Format requirements
        requirements = "\n".join(f"- {r}" for r in context.detected_requirements) or "- Requirements standards"

        # Format visual analysis
        visual_analysis = ""
        if context.vision_analysis:
            for va in context.vision_analysis:
                visual_analysis += f"\n### Analyse Image\n{va.get('analysis', '')}\n"
        if context.ocr_results:
            for ocr in context.ocr_results:
                visual_analysis += f"\n### Texte Extrait (OCR)\n{ocr.get('text', '')}\n"

        if not visual_analysis:
            visual_analysis = "Aucune analyse visuelle"

        return self.PROMPT_TEMPLATE.format(
            conversation_summary=conversation_summary,
            intent=context.project_intent or "Création d'application",
            features=features,
            tech_stack=tech_stack,
            requirements=requirements,
            visual_analysis=visual_analysis
        )

    def _summarize_conversation(self, messages: List[ConversationMessage]) -> str:
        """Summarize conversation messages"""
        summary_parts = []
        for msg in messages[-10:]:  # Last 10 messages
            role = "Utilisateur" if msg.role == "user" else "Assistant"
            input_info = f" [{msg.input_type.value}]" if msg.input_type != InputType.TEXT else ""
            summary_parts.append(f"**{role}**{input_info}: {msg.content[:200]}")

        return "\n\n".join(summary_parts)


class ConversationalOrchestrator:
    """
    Main orchestrator that processes multi-modal inputs
    and transforms them into contextual prompts.

    PERSISTED: Uses ConversationRepository for PostgreSQL storage.

    Constructor modes:
    1. With db_pool: Persistent mode (production)
    2. Without db_pool: In-memory fallback (testing only)
    """

    def __init__(self, db_pool: Optional[asyncpg.Pool] = None):
        self.stt = STTService()
        self.tts = TTSService()
        self.ocr = OCRService()
        self.vllm = VLLMService()
        self.nlp = NLPProcessor()
        self.prompt_transformer = PromptTransformer()

        # Database persistence
        self._db_pool = db_pool
        self._repo: Optional[ConversationRepository] = None
        if db_pool:
            self._repo = ConversationRepository(db_pool)

        # In-memory cache for NLP context (NOT for messages)
        # This caches extracted intents/features during a session
        self._context_cache: Dict[str, ConversationContext] = {}

    async def process_input(
        self,
        conversation_id: str,
        input_type: InputType,
        content: Union[str, bytes],
        tenant_id: Optional[UUID] = None,
        user_id: Optional[UUID] = None,
        expected_version: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process any type of input and add to conversation.

        Args:
            conversation_id: Conversation UUID as string
            input_type: Type of input (TEXT, VOICE, IMAGE, etc.)
            content: Input content (str or bytes)
            tenant_id: Tenant UUID (REQUIRED if using DB)
            user_id: User UUID (REQUIRED if using DB)
            expected_version: Version for optimistic lock (REQUIRED if using DB)
            metadata: Optional metadata

        Returns:
            Dict with message and updated version

        Raises:
            ConversationConflictError: Version mismatch
            ConversationFullError: 100 messages limit reached
        """
        # Get or create local context for NLP processing
        context = self._get_or_create_context(conversation_id)

        # Process based on input type
        if input_type == InputType.TEXT:
            processed_content = content if isinstance(content, str) else content.decode()

        elif input_type == InputType.VOICE:
            # STT processing
            audio_data = content if isinstance(content, bytes) else base64.b64decode(content)
            processed_content = await self.stt.transcribe(audio_data, context.language)

        elif input_type == InputType.IMAGE or input_type == InputType.SCREENSHOT:
            # VLLM processing
            image_data = content if isinstance(content, bytes) else base64.b64decode(content)

            if input_type == InputType.SCREENSHOT:
                analysis = await self.vllm.analyze_ui_screenshot(image_data)
            else:
                analysis = await self.vllm.analyze_image(image_data)

            context.vision_analysis.append(analysis)
            processed_content = analysis.get("analysis", "Image analysée")

        elif input_type == InputType.DOCUMENT:
            # OCR processing
            doc_data = content if isinstance(content, bytes) else base64.b64decode(content)
            ocr_result = await self.ocr.extract_text(doc_data)
            context.ocr_results.append(ocr_result)
            processed_content = ocr_result.get("text", "Document analysé")

        else:
            processed_content = str(content)

        # NLP analysis
        nlp_analysis = self.nlp.analyze(processed_content)

        # Update context with extracted info
        if nlp_analysis["intent"]:
            context.project_intent = nlp_analysis["intent"]

        entities = nlp_analysis.get("entities", {})
        context.detected_tech_stack.extend(entities.get("tech_stack", []))
        context.detected_features.extend(entities.get("features", []))

        # Deduplicate
        context.detected_tech_stack = list(set(context.detected_tech_stack))
        context.detected_features = list(set(context.detected_features))

        # Create message
        message = ConversationMessage(
            role="user",
            content=processed_content,
            input_type=input_type,
            metadata={
                **(metadata or {}),
                "nlp_analysis": nlp_analysis
            }
        )

        # Update local context cache
        context.messages.append(message)
        context.updated_at = datetime.utcnow().isoformat()

        # Persist to database if repository available
        new_version = expected_version
        if self._repo and tenant_id and expected_version is not None:
            try:
                conv_uuid = UUID(conversation_id) if isinstance(conversation_id, str) else conversation_id
                db_message = {
                    "role": message.role,
                    "content": message.content,
                    "input_type": message.input_type.value,
                    "metadata": message.metadata,
                    "timestamp": message.timestamp
                }
                result = await self._repo.add_message(
                    conversation_id=conv_uuid,
                    tenant_id=tenant_id,
                    message=db_message,
                    expected_version=expected_version
                )
                new_version = result.get("version", expected_version + 1)
                logger.debug(f"Message persisted, new version: {new_version}")
            except ConversationConflictError:
                # Remove from local cache on conflict
                context.messages.pop()
                raise
            except ConversationFullError:
                context.messages.pop()
                raise

        return {
            "message": message,
            "version": new_version,
            "context_summary": {
                "intent": context.project_intent,
                "features": context.detected_features,
                "tech_stack": context.detected_tech_stack
            }
        }

    async def generate_response(
        self,
        conversation_id: str,
        tenant_id: Optional[UUID] = None,
        expected_version: Optional[int] = None,
        use_tts: bool = False
    ) -> Dict[str, Any]:
        """
        Generate assistant response based on conversation.

        Args:
            conversation_id: Conversation UUID as string
            tenant_id: Tenant UUID (REQUIRED if using DB)
            expected_version: Version for optimistic lock (REQUIRED if using DB)
            use_tts: Whether to generate audio response

        Returns:
            Dict with response text, version, and optional audio
        """
        context = self._context_cache.get(conversation_id)
        if not context:
            return {"error": "Conversation not found"}

        # Generate contextual response using BMAD
        last_message = context.messages[-1] if context.messages else None
        if not last_message:
            return {"error": "No messages in conversation"}

        # Simple response logic (could be enhanced with actual BMAD call)
        response_text = self._generate_contextual_response(context)

        # Add assistant message
        assistant_message = ConversationMessage(
            role="assistant",
            content=response_text,
            input_type=InputType.TEXT
        )
        context.messages.append(assistant_message)

        # Persist assistant message to DB
        new_version = expected_version
        if self._repo and tenant_id and expected_version is not None:
            try:
                conv_uuid = UUID(conversation_id) if isinstance(conversation_id, str) else conversation_id
                db_message = {
                    "role": "assistant",
                    "content": response_text,
                    "input_type": InputType.TEXT.value,
                    "timestamp": assistant_message.timestamp
                }
                result_db = await self._repo.add_message(
                    conversation_id=conv_uuid,
                    tenant_id=tenant_id,
                    message=db_message,
                    expected_version=expected_version
                )
                new_version = result_db.get("version", expected_version + 1)
            except (ConversationConflictError, ConversationFullError):
                context.messages.pop()
                raise

        result = {
            "text": response_text,
            "conversation_id": conversation_id,
            "version": new_version,
            "context_summary": {
                "intent": context.project_intent,
                "features": context.detected_features,
                "tech_stack": context.detected_tech_stack
            }
        }

        # Generate audio if requested
        if use_tts:
            audio = await self.tts.synthesize(response_text, context.language)
            if audio:
                result["audio"] = base64.b64encode(audio).decode()

        return result

    def generate_bolt_prompt(self, conversation_id: str) -> Optional[str]:
        """Generate final Bolt prompt from conversation"""
        context = self._context_cache.get(conversation_id)
        if not context:
            return None

        return self.prompt_transformer.transform(context)

    def get_conversation_context(self, conversation_id: str) -> Optional[ConversationContext]:
        """Get cached conversation context by ID (for NLP data only)"""
        return self._context_cache.get(conversation_id)

    async def get_conversation(
        self,
        conversation_id: str,
        tenant_id: UUID
    ) -> Optional[Dict[str, Any]]:
        """
        Get full conversation from database.

        Args:
            conversation_id: Conversation UUID as string
            tenant_id: Tenant UUID (from JWT)

        Returns:
            Full conversation dict with messages, or None if not found
        """
        if not self._repo:
            # Fallback to local cache in test mode
            ctx = self._context_cache.get(conversation_id)
            if ctx:
                return {
                    "id": conversation_id,
                    "messages": [m.model_dump() for m in ctx.messages],
                    "version": 1
                }
            return None

        conv_uuid = UUID(conversation_id) if isinstance(conversation_id, str) else conversation_id
        return await self._repo.get(conv_uuid, tenant_id)

    async def create_conversation(
        self,
        tenant_id: UUID,
        user_id: UUID,
        app_context: str = "chat",
        title: str = None,
        model: str = "groq"
    ) -> Dict[str, Any]:
        """
        Create a new conversation in the database.

        Args:
            tenant_id: Tenant UUID (from JWT)
            user_id: User UUID (from JWT)
            app_context: Application context (chat, pme, rag, etc.)
            title: Optional title
            model: LLM model to use

        Returns:
            Created conversation dict with id and version
        """
        if not self._repo:
            # Fallback for test mode
            conv_id = str(UUID(int=0))  # Generate new UUID
            self._context_cache[conv_id] = ConversationContext(
                conversation_id=conv_id,
                created_at=datetime.utcnow().isoformat(),
                updated_at=datetime.utcnow().isoformat()
            )
            return {"id": conv_id, "version": 1, "messages": []}

        result = await self._repo.create(
            tenant_id=tenant_id,
            user_id=user_id,
            app_context=app_context,
            title=title,
            model=model
        )

        # Initialize local context cache
        self._context_cache[str(result["id"])] = ConversationContext(
            conversation_id=str(result["id"]),
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat()
        )

        return result

    def _get_or_create_context(self, conversation_id: str) -> ConversationContext:
        """Get existing or create new local context (for NLP data caching)"""
        if conversation_id not in self._context_cache:
            self._context_cache[conversation_id] = ConversationContext(
                conversation_id=conversation_id,
                created_at=datetime.utcnow().isoformat(),
                updated_at=datetime.utcnow().isoformat()
            )
        return self._context_cache[conversation_id]

    def _generate_contextual_response(self, context: ConversationContext) -> str:
        """Generate contextual response based on conversation state"""
        if not context.project_intent:
            return "Bonjour! Je suis là pour vous aider à créer votre projet. Pouvez-vous me décrire ce que vous souhaitez développer?"

        if not context.detected_features:
            return f"Je comprends que vous voulez {context.project_intent}. Quelles fonctionnalités principales souhaitez-vous inclure?"

        if not context.detected_tech_stack:
            return f"Très bien! J'ai noté ces fonctionnalités: {', '.join(context.detected_features)}. Avez-vous une préférence pour les technologies à utiliser (React, Vue, Python...)?"

        # Ready to generate
        return f"""Parfait! Je suis prêt à créer votre projet avec:
- **Intention**: {context.project_intent}
- **Features**: {', '.join(context.detected_features)}
- **Stack**: {', '.join(context.detected_tech_stack)}

Voulez-vous que je génère le code maintenant?"""


# Singleton instance (without DB pool - for backward compatibility)
# Use get_orchestrator() factory function for production with DB
_orchestrator_instance: Optional[ConversationalOrchestrator] = None


def get_orchestrator(db_pool: Optional[asyncpg.Pool] = None) -> ConversationalOrchestrator:
    """
    Get or create ConversationalOrchestrator instance.

    Args:
        db_pool: asyncpg pool for database persistence.
                 If provided, creates/updates the instance with DB support.
                 If None, returns existing instance or creates in-memory one.

    Returns:
        ConversationalOrchestrator instance
    """
    global _orchestrator_instance

    if db_pool is not None:
        # Create or replace with DB-enabled instance
        _orchestrator_instance = ConversationalOrchestrator(db_pool=db_pool)
        logger.info("ConversationalOrchestrator initialized with database pool")
    elif _orchestrator_instance is None:
        # Create in-memory instance (testing/backward compat)
        _orchestrator_instance = ConversationalOrchestrator()
        logger.warning("ConversationalOrchestrator running WITHOUT database persistence")

    return _orchestrator_instance


# Legacy alias - DO NOT USE in new code
conversational_orchestrator = get_orchestrator()


# FastAPI Dependency
async def get_orchestrator_dep(db_pool: asyncpg.Pool = None) -> ConversationalOrchestrator:
    """
    FastAPI dependency for ConversationalOrchestrator.

    Usage in routes:
        from app.services.conversational_orchestrator import get_orchestrator_dep
        from app.dependencies import get_db_pool

        @router.post("/messages")
        async def add_message(
            orchestrator: ConversationalOrchestrator = Depends(get_orchestrator_dep),
            db_pool: asyncpg.Pool = Depends(get_db_pool)
        ):
            # Initialize orchestrator with pool on first use
            orchestrator = get_orchestrator(db_pool)
            ...
    """
    return get_orchestrator(db_pool)
