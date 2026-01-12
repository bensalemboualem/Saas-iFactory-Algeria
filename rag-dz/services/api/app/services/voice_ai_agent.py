"""
IAFactory Voice AI Agent - Intelligent Multilingual Voice Assistant
Supports: Hotline, Secretary, Restaurant Orders, Personal AI Double

Features:
- Multilingual understanding (Arabic/French/English mixed - Code-switching)
- Darija (Algerian Arabic) support
- Anticipation/Prediction of user intent
- Context memory and personalization
- Real-time STT/TTS with emotion detection
"""
import asyncio
import logging
import json
import re
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from app.config import get_settings

# Memory service for persistent agent memory
try:
    from app.services.agent_memory import get_memory_service, MemoryImportance, MemoryType
    MEMORY_AVAILABLE = True
except ImportError:
    MEMORY_AVAILABLE = False

logger = logging.getLogger(__name__)
settings = get_settings()


class VoiceAgentMode(str, Enum):
    """Operating modes for Voice AI Agent"""
    HOTLINE = "hotline"           # Hotline/Call center mode
    SECRETARY = "secretary"        # Personal secretary/assistant
    RESTAURANT = "restaurant"      # Restaurant order taking
    AI_DOUBLE = "ai_double"        # Personal AI double (clone behavior)
    GENERAL = "general"            # General conversation


class LanguageCode(str, Enum):
    """Supported languages"""
    ARABIC = "ar"
    FRENCH = "fr"
    ENGLISH = "en"
    DARIJA = "dz"      # Algerian Arabic
    MIXED = "mixed"    # Code-switching detection


@dataclass
class VoiceContext:
    """Conversation context for voice agent"""
    session_id: str
    user_id: Optional[str] = None
    mode: VoiceAgentMode = VoiceAgentMode.GENERAL
    detected_language: LanguageCode = LanguageCode.FRENCH
    conversation_history: List[Dict[str, Any]] = field(default_factory=list)
    user_profile: Dict[str, Any] = field(default_factory=dict)
    anticipated_intents: List[str] = field(default_factory=list)
    current_task: Optional[str] = None
    entities: Dict[str, Any] = field(default_factory=dict)
    emotion: str = "neutral"
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_activity: datetime = field(default_factory=datetime.utcnow)


@dataclass
class VoiceResponse:
    """Voice agent response"""
    text: str
    language: LanguageCode
    emotion: str = "friendly"
    action: Optional[str] = None
    action_data: Optional[Dict[str, Any]] = None
    suggested_responses: List[str] = field(default_factory=list)
    anticipation: Optional[str] = None


class MultilingualNLP:
    """
    Multilingual NLP processor with code-switching detection
    Handles Arabic, French, English and Darija mixed speech
    """

    # Common Darija/Algerian phrases
    DARIJA_PATTERNS = {
        r"\bki\s?rak\b": "comment vas-tu",
        r"\bwesh\s?rak\b": "comment vas-tu",
        r"\blabas\b": "ça va",
        r"\binshallah\b": "si dieu le veut",
        r"\bhamdoulah\b": "dieu merci",
        r"\bsaha\b": "merci/santé",
        r"\bbaraka\b": "assez/bénédiction",
        r"\byatik\s?saha\b": "merci beaucoup",
        r"\bkifash\b": "comment",
        r"\bweyn\b": "où",
        r"\bwaqtash\b": "quand",
        r"\bchhal\b": "combien",
        r"\bbzaf\b": "beaucoup",
        r"\bchwiya\b": "un peu",
        r"\bmazel\b": "encore/pas encore",
        r"\bkhalassna\b": "on a fini",
        r"\bndiru\b": "on fait",
        r"\bnroho\b": "on va",
        r"\bji\b": "viens",
        r"\broho\b": "allez",
    }

    # Intent patterns per mode
    INTENT_PATTERNS = {
        VoiceAgentMode.RESTAURANT: {
            "order": [r"commander", r"je veux", r"bghit", r"عايز", r"i want", r"i'd like"],
            "menu": [r"menu", r"carte", r"قائمة", r"what do you have"],
            "price": [r"prix", r"combien", r"chhal", r"كم", r"how much"],
            "delivery": [r"livraison", r"توصيل", r"delivery", r"livreur"],
            "cancel": [r"annuler", r"cancel", r"إلغاء", r"khlass"],
            "modify": [r"modifier", r"changer", r"بدل", r"change"],
        },
        VoiceAgentMode.SECRETARY: {
            "schedule": [r"rendez-vous", r"rdv", r"موعد", r"appointment", r"meeting"],
            "reminder": [r"rappel", r"remind", r"تذكير", r"n'oublie pas"],
            "message": [r"message", r"رسالة", r"envoyer", r"send"],
            "call": [r"appeler", r"call", r"اتصل", r"téléphone"],
            "email": [r"email", r"mail", r"بريد", r"envoyer un mail"],
            "note": [r"note", r"ملاحظة", r"noter", r"écrire"],
        },
        VoiceAgentMode.HOTLINE: {
            "support": [r"aide", r"help", r"مساعدة", r"problème", r"issue"],
            "complaint": [r"plainte", r"complaint", r"شكوى", r"pas content"],
            "info": [r"information", r"info", r"معلومات", r"renseignement"],
            "transfer": [r"transférer", r"transfer", r"تحويل", r"quelqu'un d'autre"],
            "status": [r"statut", r"status", r"حالة", r"où en est"],
        },
        VoiceAgentMode.AI_DOUBLE: {
            "delegate": [r"à ma place", r"instead of me", r"بدلي", r"comme moi"],
            "learn": [r"apprends", r"learn", r"تعلم", r"retiens"],
            "style": [r"mon style", r"my style", r"طريقتي", r"comme je fais"],
            "respond": [r"réponds", r"respond", r"رد", r"answer for me"],
        }
    }

    def __init__(self):
        self.language_cache = {}

    def detect_language(self, text: str) -> Tuple[LanguageCode, float]:
        """
        Detect language with code-switching awareness

        Returns:
            Tuple of (detected_language, confidence)
        """
        text_lower = text.lower()

        # Check for Darija patterns first
        darija_count = sum(1 for pattern in self.DARIJA_PATTERNS.keys()
                         if re.search(pattern, text_lower))

        # Arabic script detection
        arabic_chars = len(re.findall(r'[\u0600-\u06FF]', text))

        # French patterns
        french_patterns = len(re.findall(r'\b(le|la|les|de|du|des|un|une|et|ou|je|tu|il|nous|vous|ils|que|qui|est|sont|être|avoir)\b', text_lower))

        # English patterns
        english_patterns = len(re.findall(r'\b(the|a|an|is|are|was|were|have|has|do|does|will|would|can|could|i|you|he|she|it|we|they)\b', text_lower))

        total_words = len(text.split())
        if total_words == 0:
            return LanguageCode.FRENCH, 0.5

        # Calculate scores
        scores = {
            LanguageCode.DARIJA: darija_count / max(total_words, 1) * 3,
            LanguageCode.ARABIC: arabic_chars / max(len(text), 1),
            LanguageCode.FRENCH: french_patterns / max(total_words, 1),
            LanguageCode.ENGLISH: english_patterns / max(total_words, 1),
        }

        # Check for code-switching (multiple languages mixed)
        active_languages = sum(1 for score in scores.values() if score > 0.1)
        if active_languages >= 2:
            return LanguageCode.MIXED, max(scores.values())

        # Return highest scoring language
        best_lang = max(scores, key=scores.get)
        return best_lang, scores[best_lang]

    def extract_entities(self, text: str, mode: VoiceAgentMode) -> Dict[str, Any]:
        """Extract entities based on mode"""
        entities = {}

        # Phone numbers (Algeria format)
        phones = re.findall(r'(?:0|\+213)[567]\d{8}', text.replace(' ', ''))
        if phones:
            entities["phone_numbers"] = phones

        # Dates/Times
        times = re.findall(r'\b(\d{1,2}[h:]\d{2}|\d{1,2}\s*(?:heures?|h))\b', text.lower())
        if times:
            entities["times"] = times

        dates = re.findall(r'\b(\d{1,2}[/.-]\d{1,2}(?:[/.-]\d{2,4})?)\b', text)
        if dates:
            entities["dates"] = dates

        # Names (capitalized words not at start of sentence)
        names = re.findall(r'(?<!\.\s)(?<!^)\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b', text)
        if names:
            entities["names"] = names

        # Amounts (with DZD, DA, euros)
        amounts = re.findall(r'(\d+(?:[.,]\d+)?)\s*(?:da|dzd|€|euros?|dinars?)', text.lower())
        if amounts:
            entities["amounts"] = amounts

        # Addresses
        addresses = re.findall(r'(?:rue|avenue|boulevard|cité|quartier)\s+[^,.]+', text.lower())
        if addresses:
            entities["addresses"] = addresses

        # Restaurant-specific
        if mode == VoiceAgentMode.RESTAURANT:
            # Quantities
            quantities = re.findall(r'(\d+)\s*(?:x|fois|portions?|pièces?|unités?)', text.lower())
            if quantities:
                entities["quantities"] = quantities

        return entities

    def detect_intent(self, text: str, mode: VoiceAgentMode) -> List[Tuple[str, float]]:
        """Detect user intent based on mode"""
        text_lower = text.lower()
        intents = []

        patterns = self.INTENT_PATTERNS.get(mode, {})
        for intent_name, intent_patterns in patterns.items():
            score = 0
            for pattern in intent_patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    score += 1
            if score > 0:
                confidence = min(score / len(intent_patterns), 1.0)
                intents.append((intent_name, confidence))

        return sorted(intents, key=lambda x: x[1], reverse=True)

    def detect_emotion(self, text: str) -> str:
        """Detect emotion from text"""
        text_lower = text.lower()

        # Positive emotions
        if any(word in text_lower for word in ["merci", "شكرا", "thanks", "super", "génial", "excellent", "parfait", "hamdoulah", "saha"]):
            return "happy"

        # Negative emotions
        if any(word in text_lower for word in ["problème", "مشكلة", "problem", "énervé", "fâché", "angry", "pas content", "horrible"]):
            return "frustrated"

        # Urgent
        if any(word in text_lower for word in ["urgent", "عاجل", "vite", "rapidement", "maintenant", "dépêche"]):
            return "urgent"

        # Question
        if "?" in text or any(word in text_lower for word in ["est-ce que", "هل", "wesh", "kifash", "weyn", "chhal"]):
            return "curious"

        return "neutral"


class VoiceAIAgent:
    """
    Main Voice AI Agent - Your Intelligent Voice Double

    Capabilities:
    - Hotline operator
    - Personal secretary
    - Restaurant order taker
    - AI Double (learns your style)

    Features:
    - Persistent memory across sessions
    - User preference learning
    - Conversation context recall
    - Semantic search for relevant memories
    """

    def __init__(self):
        self.nlp = MultilingualNLP()
        self.contexts: Dict[str, VoiceContext] = {}

        # User profile learning
        self.user_profiles: Dict[str, Dict[str, Any]] = {}

        # Response templates per language and mode
        self.templates = self._load_templates()

        # Memory service for persistent storage
        self.memory_service = get_memory_service() if MEMORY_AVAILABLE else None
        if self.memory_service:
            logger.info("VoiceAIAgent: Memory service enabled")

    def _load_templates(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        """Load response templates for all languages and modes"""
        return {
            "greetings": {
                LanguageCode.FRENCH: {
                    "morning": "Bonjour! Comment puis-je vous aider aujourd'hui?",
                    "afternoon": "Bon après-midi! Que puis-je faire pour vous?",
                    "evening": "Bonsoir! Je suis à votre écoute.",
                    "default": "Bonjour! Je suis votre assistant IA. Comment puis-je vous aider?",
                },
                LanguageCode.ARABIC: {
                    "morning": "صباح الخير! كيف يمكنني مساعدتك؟",
                    "afternoon": "مساء الخير! ماذا يمكنني أن أفعل لك؟",
                    "evening": "مساء النور! أنا في خدمتك.",
                    "default": "مرحبا! أنا مساعدك الذكي. كيف يمكنني مساعدتك؟",
                },
                LanguageCode.ENGLISH: {
                    "morning": "Good morning! How can I help you today?",
                    "afternoon": "Good afternoon! What can I do for you?",
                    "evening": "Good evening! I'm at your service.",
                    "default": "Hello! I'm your AI assistant. How can I help you?",
                },
                LanguageCode.DARIJA: {
                    "morning": "Sbah lkhir! Wesh nqder n3awnek?",
                    "afternoon": "Masa lkhir! Wesh bghit?",
                    "evening": "Masa nour! Hak ana.",
                    "default": "Salam! Ana l'assistant dyalek. Kifash nqder n3awnek?",
                },
                LanguageCode.MIXED: {
                    "default": "Salam! Bonjour! Ana ready bach n3awnek. Comment puis-je vous aider?",
                }
            },
            "restaurant": {
                LanguageCode.FRENCH: {
                    "welcome": "Bienvenue! Que souhaitez-vous commander?",
                    "confirm_order": "Parfait! Je récapitule votre commande: {order}. C'est bien ça?",
                    "delivery_time": "Votre commande sera livrée dans environ {time} minutes.",
                    "total": "Le total de votre commande est de {amount} DA.",
                },
                LanguageCode.ARABIC: {
                    "welcome": "أهلا بك! ماذا تريد أن تطلب؟",
                    "confirm_order": "تمام! طلبك هو: {order}. هل هذا صحيح؟",
                    "delivery_time": "طلبك سيصل خلال {time} دقيقة تقريبا.",
                    "total": "إجمالي طلبك هو {amount} دج.",
                },
                LanguageCode.DARIJA: {
                    "welcome": "Merhba bik! Wesh bghit t'commandi?",
                    "confirm_order": "Tamam! La commande dyalek: {order}. Sahih?",
                    "delivery_time": "Ghadi tosellek f {time} dqayeq.",
                    "total": "Total howa {amount} DA.",
                },
            },
            "secretary": {
                LanguageCode.FRENCH: {
                    "schedule": "Je note le rendez-vous pour {date} à {time}.",
                    "reminder": "Je vous rappellerai pour {task}.",
                    "message": "J'ai bien noté votre message pour {recipient}.",
                    "call": "Je vais appeler {contact} pour vous.",
                },
                LanguageCode.ARABIC: {
                    "schedule": "سجلت الموعد في {date} الساعة {time}.",
                    "reminder": "سأذكرك بـ {task}.",
                    "message": "سجلت رسالتك لـ {recipient}.",
                    "call": "سأتصل بـ {contact} نيابة عنك.",
                },
            },
            "ai_double": {
                LanguageCode.FRENCH: {
                    "learning": "Je comprends, j'apprends votre façon de faire.",
                    "delegating": "D'accord, je vais m'en occuper comme vous le feriez.",
                    "style_confirm": "J'ai mémorisé votre style pour ce type de situation.",
                    "anticipation": "Je pense que vous voulez {action}. C'est bien ça?",
                },
            }
        }

    def get_or_create_context(
        self,
        session_id: str,
        user_id: Optional[str] = None,
        mode: VoiceAgentMode = VoiceAgentMode.GENERAL
    ) -> VoiceContext:
        """Get or create conversation context"""
        if session_id not in self.contexts:
            self.contexts[session_id] = VoiceContext(
                session_id=session_id,
                user_id=user_id,
                mode=mode
            )

            # Load user profile if exists
            if user_id and user_id in self.user_profiles:
                self.contexts[session_id].user_profile = self.user_profiles[user_id]

        return self.contexts[session_id]

    async def process_voice_input(
        self,
        text: str,
        session_id: str,
        user_id: Optional[str] = None,
        mode: VoiceAgentMode = VoiceAgentMode.GENERAL,
        audio_emotion: Optional[str] = None
    ) -> VoiceResponse:
        """
        Process voice input and generate response

        Args:
            text: Transcribed text from STT
            session_id: Session identifier
            user_id: Optional user ID for personalization
            mode: Operating mode
            audio_emotion: Emotion detected from audio (optional)

        Returns:
            VoiceResponse with text, language, and actions
        """
        context = self.get_or_create_context(session_id, user_id, mode)
        context.last_activity = datetime.utcnow()
        context.mode = mode

        # Detect language
        detected_lang, confidence = self.nlp.detect_language(text)
        context.detected_language = detected_lang

        # Detect emotion
        text_emotion = self.nlp.detect_emotion(text)
        context.emotion = audio_emotion or text_emotion

        # Extract entities
        entities = self.nlp.extract_entities(text, mode)
        context.entities.update(entities)

        # Detect intents
        intents = self.nlp.detect_intent(text, mode)

        # --- MEMORY INTEGRATION ---
        # Store in working memory
        if self.memory_service:
            self.memory_service.add_to_working_memory(
                session_id=session_id,
                role="user",
                content=text,
                importance=0.7 if intents else 0.5,
                metadata={
                    "language": detected_lang.value,
                    "emotion": context.emotion,
                    "mode": mode.value,
                    "intents": [i[0] for i in intents],
                }
            )

            # Recall relevant memories
            memories = await self.memory_service.recall(
                query=text,
                user_id=user_id,
                limit=3
            )
            if memories:
                context.anticipated_intents = [
                    m.content[:100] for m in memories
                ]

            # Learn user preferences
            if user_id:
                self.memory_service.learn_from_interaction(
                    user_id=user_id,
                    interaction_type=mode.value,
                    data={
                        "language": detected_lang.value,
                        "intents": [i[0] for i in intents],
                        "entities": entities,
                    }
                )

        # Add to conversation history
        context.conversation_history.append({
            "role": "user",
            "text": text,
            "language": detected_lang.value,
            "emotion": context.emotion,
            "intents": intents,
            "entities": entities,
            "timestamp": datetime.utcnow().isoformat()
        })

        # Generate response based on mode
        response = await self._generate_response(text, context, intents, entities)

        # Add response to history
        context.conversation_history.append({
            "role": "assistant",
            "text": response.text,
            "language": response.language.value,
            "action": response.action,
            "timestamp": datetime.utcnow().isoformat()
        })

        # Store response in memory
        if self.memory_service:
            self.memory_service.add_to_working_memory(
                session_id=session_id,
                role="assistant",
                content=response.text,
                importance=0.6,
                metadata={
                    "action": response.action,
                    "language": response.language.value,
                }
            )

            # Store important memories long-term
            if response.action:
                await self.memory_service.remember(
                    content=f"Action: {response.action} - User: {text[:100]} - Response: {response.text[:100]}",
                    user_id=user_id,
                    importance=MemoryImportance.HIGH if response.action in ["create_appointment", "make_call", "take_order"] else MemoryImportance.MEDIUM,
                    memory_type=MemoryType.EPISODIC,
                    tags=[mode.value, response.action],
                    metadata={"session_id": session_id, "entities": entities}
                )

        # Anticipate next intent
        response.anticipation = await self._anticipate_next(context)

        return response

    async def _generate_response(
        self,
        text: str,
        context: VoiceContext,
        intents: List[Tuple[str, float]],
        entities: Dict[str, Any]
    ) -> VoiceResponse:
        """Generate response based on context and intents"""

        lang = context.detected_language
        mode = context.mode

        # Get primary intent
        primary_intent = intents[0][0] if intents else None

        # Mode-specific response generation
        if mode == VoiceAgentMode.RESTAURANT:
            return await self._handle_restaurant(text, context, primary_intent, entities)

        elif mode == VoiceAgentMode.SECRETARY:
            return await self._handle_secretary(text, context, primary_intent, entities)

        elif mode == VoiceAgentMode.HOTLINE:
            return await self._handle_hotline(text, context, primary_intent, entities)

        elif mode == VoiceAgentMode.AI_DOUBLE:
            return await self._handle_ai_double(text, context, primary_intent, entities)

        else:
            return await self._handle_general(text, context, primary_intent, entities)

    async def _handle_restaurant(
        self,
        text: str,
        context: VoiceContext,
        intent: Optional[str],
        entities: Dict[str, Any]
    ) -> VoiceResponse:
        """Handle restaurant order mode"""
        lang = context.detected_language
        templates = self.templates.get("restaurant", {}).get(lang, {})

        if intent == "order":
            # Extract order items
            order_items = entities.get("quantities", [])
            return VoiceResponse(
                text=templates.get("welcome", "Que souhaitez-vous commander?"),
                language=lang,
                emotion="friendly",
                action="take_order",
                suggested_responses=["Pizza", "Burger", "Tacos", "Menu du jour"]
            )

        elif intent == "menu":
            return VoiceResponse(
                text="Voici notre menu: Pizzas, Burgers, Tacos, Plats traditionnels. Que préférez-vous?",
                language=lang,
                action="show_menu"
            )

        elif intent == "price":
            return VoiceResponse(
                text="Quel plat souhaitez-vous connaître le prix?",
                language=lang,
                action="price_inquiry"
            )

        elif intent == "delivery":
            addresses = entities.get("addresses", [])
            if addresses:
                return VoiceResponse(
                    text=f"Parfait, livraison à {addresses[0]}. Temps estimé: 30-45 minutes.",
                    language=lang,
                    action="confirm_delivery",
                    action_data={"address": addresses[0]}
                )
            return VoiceResponse(
                text="Quelle est votre adresse de livraison?",
                language=lang,
                action="request_address"
            )

        return VoiceResponse(
            text=templates.get("welcome", "Bienvenue! Que puis-je faire pour vous?"),
            language=lang,
            emotion="friendly"
        )

    async def _handle_secretary(
        self,
        text: str,
        context: VoiceContext,
        intent: Optional[str],
        entities: Dict[str, Any]
    ) -> VoiceResponse:
        """Handle secretary/assistant mode"""
        lang = context.detected_language

        if intent == "schedule":
            dates = entities.get("dates", [])
            times = entities.get("times", [])

            if dates and times:
                return VoiceResponse(
                    text=f"Rendez-vous noté pour le {dates[0]} à {times[0]}. Avec qui?",
                    language=lang,
                    action="create_appointment",
                    action_data={"date": dates[0], "time": times[0]}
                )
            return VoiceResponse(
                text="Pour quand souhaitez-vous ce rendez-vous?",
                language=lang,
                action="request_datetime"
            )

        elif intent == "reminder":
            return VoiceResponse(
                text="Bien noté! Je vous rappellerai. Quand souhaitez-vous être rappelé?",
                language=lang,
                action="create_reminder"
            )

        elif intent == "call":
            names = entities.get("names", [])
            phones = entities.get("phone_numbers", [])

            if names:
                return VoiceResponse(
                    text=f"Je vais appeler {names[0]} pour vous.",
                    language=lang,
                    action="make_call",
                    action_data={"contact": names[0]}
                )
            elif phones:
                return VoiceResponse(
                    text=f"J'appelle le {phones[0]}...",
                    language=lang,
                    action="make_call",
                    action_data={"phone": phones[0]}
                )

        elif intent == "message":
            names = entities.get("names", [])
            return VoiceResponse(
                text="Quel message souhaitez-vous envoyer?",
                language=lang,
                action="compose_message",
                action_data={"recipient": names[0] if names else None}
            )

        return VoiceResponse(
            text="Je suis votre secrétaire IA. Comment puis-je vous aider?",
            language=lang,
            suggested_responses=["Prendre un rendez-vous", "Envoyer un message", "Créer un rappel"]
        )

    async def _handle_hotline(
        self,
        text: str,
        context: VoiceContext,
        intent: Optional[str],
        entities: Dict[str, Any]
    ) -> VoiceResponse:
        """Handle hotline/call center mode"""
        lang = context.detected_language

        if intent == "support":
            return VoiceResponse(
                text="Je suis là pour vous aider. Pouvez-vous me décrire votre problème?",
                language=lang,
                action="open_ticket",
                emotion="empathetic"
            )

        elif intent == "complaint":
            return VoiceResponse(
                text="Je suis vraiment désolé pour ce désagrément. Pouvez-vous me donner plus de détails?",
                language=lang,
                action="register_complaint",
                emotion="apologetic"
            )

        elif intent == "transfer":
            return VoiceResponse(
                text="Je vais vous transférer vers un conseiller. Un instant s'il vous plaît.",
                language=lang,
                action="transfer_call"
            )

        elif intent == "status":
            return VoiceResponse(
                text="Pour vérifier le statut, j'ai besoin de votre numéro de référence.",
                language=lang,
                action="check_status"
            )

        return VoiceResponse(
            text="Bienvenue sur notre hotline. Comment puis-je vous aider?",
            language=lang,
            suggested_responses=["J'ai un problème", "Information", "Réclamation"]
        )

    async def _handle_ai_double(
        self,
        text: str,
        context: VoiceContext,
        intent: Optional[str],
        entities: Dict[str, Any]
    ) -> VoiceResponse:
        """Handle AI Double mode - Learn and mimic user behavior"""
        lang = context.detected_language
        user_id = context.user_id

        if intent == "learn":
            # Learn from user's behavior
            return VoiceResponse(
                text="D'accord, je retiens. Comment répondriez-vous normalement?",
                language=lang,
                action="learn_behavior"
            )

        elif intent == "delegate":
            return VoiceResponse(
                text="Compris! Je vais répondre à votre place avec votre style habituel.",
                language=lang,
                action="act_as_user"
            )

        elif intent == "style":
            return VoiceResponse(
                text="J'ai analysé vos messages précédents. Votre style est: direct, amical, professionnel.",
                language=lang,
                action="analyze_style"
            )

        return VoiceResponse(
            text="Je suis votre double IA. Je peux apprendre votre style et agir à votre place.",
            language=lang,
            suggested_responses=["Apprends mon style", "Réponds à ma place", "Comment je parle?"]
        )

    async def _handle_general(
        self,
        text: str,
        context: VoiceContext,
        intent: Optional[str],
        entities: Dict[str, Any]
    ) -> VoiceResponse:
        """Handle general conversation mode"""
        lang = context.detected_language
        greetings = self.templates.get("greetings", {}).get(lang, {})

        # Check for greetings
        greeting_patterns = ["bonjour", "salam", "hello", "hi", "salut", "bonsoir", "مرحبا", "السلام"]
        if any(g in text.lower() for g in greeting_patterns):
            hour = datetime.now().hour
            if hour < 12:
                return VoiceResponse(
                    text=greetings.get("morning", greetings.get("default", "Bonjour!")),
                    language=lang,
                    emotion="friendly"
                )
            elif hour < 18:
                return VoiceResponse(
                    text=greetings.get("afternoon", greetings.get("default", "Bonjour!")),
                    language=lang,
                    emotion="friendly"
                )
            else:
                return VoiceResponse(
                    text=greetings.get("evening", greetings.get("default", "Bonsoir!")),
                    language=lang,
                    emotion="friendly"
                )

        return VoiceResponse(
            text="Je suis votre assistant IA multilingue. Comment puis-je vous aider?",
            language=lang,
            suggested_responses=["Restaurant", "Secrétaire", "Hotline", "Mode Double IA"]
        )

    async def _anticipate_next(self, context: VoiceContext) -> Optional[str]:
        """Anticipate user's next action based on conversation history"""
        history = context.conversation_history
        if len(history) < 2:
            return None

        # Pattern matching for anticipation
        mode = context.mode
        last_action = None

        for msg in reversed(history):
            if msg.get("role") == "assistant" and msg.get("action"):
                last_action = msg.get("action")
                break

        # Anticipation logic per mode
        if mode == VoiceAgentMode.RESTAURANT:
            if last_action == "take_order":
                return "Voulez-vous ajouter une boisson ou un dessert?"
            elif last_action == "confirm_delivery":
                return "Souhaitez-vous payer par carte ou en espèces?"

        elif mode == VoiceAgentMode.SECRETARY:
            if last_action == "create_appointment":
                return "Dois-je envoyer une confirmation par email?"
            elif last_action == "create_reminder":
                return "Voulez-vous que je répète ce rappel demain?"

        return None

    def learn_user_preference(
        self,
        user_id: str,
        preference_key: str,
        preference_value: Any
    ):
        """Learn and store user preferences for AI Double mode"""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {}

        self.user_profiles[user_id][preference_key] = preference_value
        logger.info(f"Learned preference for user {user_id}: {preference_key}={preference_value}")


# Singleton instance
voice_ai_agent = VoiceAIAgent()
