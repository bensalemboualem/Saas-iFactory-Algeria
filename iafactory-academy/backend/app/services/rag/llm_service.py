"""
LLM Service for RAG
Handles multi-provider LLM interactions including Ollama for local inference
"""

import os
from typing import List, Optional, Dict, Any
from enum import Enum
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


class LLMProvider(str, Enum):
    """Available LLM providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GROQ = "groq"
    OLLAMA = "ollama"


class LLMService:
    """Service for LLM interactions with multiple providers"""

    SYSTEM_PROMPT_RAG = """Tu es un assistant IA expert pour IAFactory-School, le Programme National IA pour l'Éducation en Algérie.

Tu as accès à une base de connaissances contenant:
- Présentation complète du programme IAFactory-School
- Modèle économique et pricing (tarification dégressive)
- Spécifications techniques (architecture, stack, API)
- Programmes pour Primaire, Collège, Lycée et Enseignants
- Contenus en Français, Arabe et Anglais

RÈGLES IMPORTANTES:
1. Réponds UNIQUEMENT basé sur le contexte fourni
2. Si l'information n'est pas dans le contexte, dis-le clairement
3. Cite tes sources entre crochets [Source X]
4. Sois précis sur les chiffres (prix, ROI, durées)
5. Adapte ton langage à la question posée

CONTEXTE PROGRAMME BBC SCHOOL:
- Partenaire stratégique: BBC School (1,600 élèves)
- Investissement IAFactory: 4.8M DA
- Lancement: Février 2026
- ROI projeté: x52 à x110 sur 3 ans
"""

    OLLAMA_MODEL = "qwen2.5:7b"  # Modèle par défaut pour Ollama
    OLLAMA_BASE_URL = "http://localhost:11434"

    def __init__(
        self,
        default_provider: LLMProvider = LLMProvider.OPENAI,
        default_model: str = "gpt-4o",
        temperature: float = 0.1
    ):
        self.default_provider = default_provider
        self.default_model = default_model
        self.temperature = temperature

        # Initialize providers (lazy loading)
        self._openai = None
        self._anthropic = None
        self._ollama = None

    @property
    def openai(self):
        """Lazy load OpenAI client"""
        if self._openai is None:
            self._openai = ChatOpenAI(
                model=self.default_model,
                temperature=self.temperature,
                openai_api_key=os.getenv("OPENAI_API_KEY")
            )
        return self._openai

    @property
    def anthropic(self):
        """Lazy load Anthropic client"""
        if self._anthropic is None:
            self._anthropic = ChatAnthropic(
                model="claude-sonnet-4-20250514",
                temperature=self.temperature,
                anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        return self._anthropic

    @property
    def ollama(self):
        """Lazy load Ollama client (local inference)"""
        if self._ollama is None:
            model = os.getenv("OLLAMA_MODEL", self.OLLAMA_MODEL)
            base_url = os.getenv("OLLAMA_BASE_URL", self.OLLAMA_BASE_URL)
            self._ollama = ChatOllama(
                model=model,
                temperature=self.temperature,
                base_url=base_url
            )
        return self._ollama

    def get_llm(self, provider: Optional[LLMProvider] = None):
        """Get LLM instance for provider"""
        provider = provider or self.default_provider

        if provider == LLMProvider.ANTHROPIC:
            return self.anthropic
        elif provider == LLMProvider.OLLAMA:
            return self.ollama
        return self.openai

    def generate_response(
        self,
        query: str,
        context: str,
        provider: Optional[LLMProvider] = None,
        system_prompt: Optional[str] = None,
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Generate a response using RAG context

        Args:
            query: User question
            context: Retrieved context from vector store
            provider: LLM provider to use
            system_prompt: Custom system prompt
            chat_history: Previous conversation history

        Returns:
            Generated response string
        """
        llm = self.get_llm(provider)
        system = system_prompt or self.SYSTEM_PROMPT_RAG

        # Build messages
        messages = [SystemMessage(content=system)]

        # Add chat history if provided
        if chat_history:
            for msg in chat_history[-10:]:  # Last 10 messages
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                else:
                    messages.append(AIMessage(content=msg["content"]))

        # Add context and query
        user_message = f"""CONTEXTE RÉCUPÉRÉ:
{context}

QUESTION:
{query}

Réponds de manière précise et structurée en citant tes sources."""

        messages.append(HumanMessage(content=user_message))

        # Generate response
        response = llm.invoke(messages)
        return response.content

    def generate_summary(
        self,
        documents: List[str],
        provider: Optional[LLMProvider] = None
    ) -> str:
        """Generate a summary of multiple documents"""
        llm = self.get_llm(provider)

        combined = "\n\n---\n\n".join(documents[:5])  # Limit to 5 docs
        messages = [
            SystemMessage(content="Tu es un expert en synthèse de documents éducatifs."),
            HumanMessage(content=f"Résume les points clés de ces documents:\n\n{combined}")
        ]

        response = llm.invoke(messages)
        return response.content

    def classify_query(
        self,
        query: str,
        provider: Optional[LLMProvider] = None
    ) -> Dict[str, Any]:
        """
        Classify a user query to determine intent and filters

        Returns:
            Dict with keys: intent, level, module, language, type
        """
        llm = self.get_llm(provider)

        messages = [
            SystemMessage(content="""Analyse cette question et retourne un JSON avec:
- intent: "search" | "quiz" | "stats" | "definition" | "comparison"
- level: "primaire" | "college" | "lycee" | "enseignants" | null
- module: "L1" | "L2" | "P1" | "C1" | etc. | null
- language: "fr" | "ar" | "en"
- type: "cours" | "quiz" | "examen" | "guide" | null

Retourne UNIQUEMENT le JSON, sans autre texte."""),
            HumanMessage(content=query)
        ]

        response = llm.invoke(messages)

        try:
            import json
            return json.loads(response.content)
        except Exception:
            return {
                "intent": "search",
                "level": None,
                "module": None,
                "language": "fr",
                "type": None
            }
