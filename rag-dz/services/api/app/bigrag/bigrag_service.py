"""
BIG RAG - Service Principal
============================
Service orchestrateur pour RAG multi-pays
Pipeline: Detect → Search → Rerank → LLM → Response
"""

import os
import logging
import time
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
import httpx
from pydantic import BaseModel, Field

from .country_detector import (
    CountryDetector, CountryDetectionResult, 
    Country, Language, country_detector,
    get_country_emoji, get_country_name,
)
from .embedding_pipeline import EmbeddingPipeline, embedding_pipeline
from .reranker_pipeline import RerankerPipeline, reranker_pipeline
from .qdrant_multi import (
    QdrantMultiIndex, qdrant_multi,
    IndexName, SearchResult, MultiSearchResult,
    get_index_for_country,
)

logger = logging.getLogger(__name__)


# ============================================
# ENUMS & MODELS
# ============================================

class LLMProvider(str, Enum):
    """Providers LLM pour génération"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GROQ = "groq"
    GOOGLE = "google"
    LOCAL = "local"


class LLMModel(str, Enum):
    """Modèles LLM disponibles"""
    # OpenAI
    GPT4_TURBO = "gpt-4-turbo"
    GPT4O = "gpt-4o"
    GPT4O_MINI = "gpt-4o-mini"

    # Anthropic
    CLAUDE_SONNET = "claude-sonnet-4-20250514"
    CLAUDE_HAIKU = "claude-3-5-haiku-20241022"

    # Groq
    LLAMA_70B = "llama-3.1-70b-versatile"
    MIXTRAL = "mixtral-8x7b-32768"

    # Google
    GEMINI_FLASH = "gemini-2.5-flash"
    GEMINI_PRO = "gemini-2.0-flash-exp"


class ContextChunk(BaseModel):
    """Chunk de contexte utilisé"""
    text: str
    source: str
    country: str
    score: float
    theme: Optional[str] = None
    url: Optional[str] = None


class BigRAGResponse(BaseModel):
    """Réponse complète du BIG RAG"""
    # Réponse principale
    answer: str = Field(..., description="Réponse générée")
    
    # Détection pays
    country_detected: Country = Field(..., description="Pays détecté")
    country_confidence: float = Field(..., description="Confiance détection")
    country_signals: List[str] = Field(default_factory=list)
    country_emoji: str = Field("")
    
    # Langue
    language: Language = Field(..., description="Langue détectée")
    
    # Modèle utilisé
    model_used: str = Field(..., description="Modèle LLM utilisé")
    provider: str = Field(..., description="Provider LLM")
    
    # Contextes
    contexts_used: List[ContextChunk] = Field(default_factory=list)
    total_contexts_found: int = Field(0)
    
    # Sources
    sources: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Métadonnées
    search_time_ms: float = Field(0)
    rerank_time_ms: float = Field(0)
    llm_time_ms: float = Field(0)
    total_time_ms: float = Field(0)
    
    # Index utilisés
    indexes_searched: List[str] = Field(default_factory=list)
    
    # Tokens
    tokens_used: int = Field(0)


class BigRAGRequest(BaseModel):
    """Requête BIG RAG"""
    query: str = Field(..., min_length=3, description="Question utilisateur")
    top_k: int = Field(8, ge=1, le=20, description="Nombre de contextes")
    country_hint: Optional[str] = Field(None, description="Indice pays (DZ, CH)")
    language_hint: Optional[str] = Field(None, description="Indice langue")
    include_global: bool = Field(True, description="Inclure index global")
    rerank: bool = Field(True, description="Activer le reranking")
    model: Optional[str] = Field(None, description="Modèle LLM à utiliser")


# ============================================
# PROMPTS
# ============================================

SYSTEM_PROMPT_DZ = """Tu es un expert en fiscalité, comptabilité et droit des affaires en Algérie 🇩🇿.

Tu réponds en français, de manière claire et précise.
Tu cites les sources légales algériennes quand disponibles (Journal Officiel, Code des Impôts, etc.).

Règles:
- Sois précis sur les montants en DZD (Dinar algérien)
- Mentionne les organismes algériens (DGI, CNAS, CASNOS, CNRC, etc.)
- Si tu n'es pas sûr, dis-le clairement
- Propose de consulter un expert pour les cas complexes"""

SYSTEM_PROMPT_CH = """Tu es un expert en fiscalité, comptabilité et droit des affaires en Suisse 🇨🇭.

Tu réponds en français (ou allemand si demandé), de manière claire et précise.
Tu cites les sources légales suisses quand disponibles (Code des Obligations, Lois fédérales, etc.).

Règles:
- Sois précis sur les montants en CHF (Franc suisse)
- Mentionne les organismes suisses (AFC, AVS, LPP, SUVA, etc.)
- Distingue le niveau fédéral, cantonal et communal
- Si tu n'es pas sûr, dis-le clairement
- Propose de consulter un expert pour les cas complexes"""

SYSTEM_PROMPT_GLOBAL = """Tu es un assistant expert en affaires, fiscalité et comptabilité internationale.

Tu réponds en français, de manière claire et précise.
Tu adaptes tes réponses au contexte du pays détecté dans la question.

Règles:
- Sois précis sur les montants et devises
- Mentionne les différences entre pays si pertinent
- Si tu n'es pas sûr, dis-le clairement
- Propose de consulter un expert local pour les cas complexes"""

RAG_PROMPT_TEMPLATE = """Contexte pertinent:
{context}

Question de l'utilisateur:
{query}

Instructions:
1. Réponds à la question en utilisant UNIQUEMENT les informations du contexte ci-dessus
2. Si le contexte ne contient pas assez d'informations, dis-le clairement
3. Cite les sources quand c'est pertinent
4. Sois concis mais complet

Réponse:"""


# ============================================
# BIG RAG SERVICE
# ============================================

class BigRAGService:
    """
    Service principal BIG RAG
    Orchestre: Détection → Recherche → Reranking → LLM
    """
    
    def __init__(
        self,
        country_detector: CountryDetector = country_detector,
        embedding_pipeline: EmbeddingPipeline = embedding_pipeline,
        reranker_pipeline: RerankerPipeline = reranker_pipeline,
        qdrant_multi: QdrantMultiIndex = qdrant_multi,
    ):
        self.country_detector = country_detector
        self.embedding_pipeline = embedding_pipeline
        self.reranker_pipeline = reranker_pipeline
        self.qdrant = qdrant_multi
        
        # Config LLM
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.google_api_key = os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")

        # Modèle par défaut - utiliser Google Gemini si disponible
        self.default_model = LLMModel.GPT4O_MINI
        if self.google_api_key:
            self.default_model = LLMModel.GEMINI_FLASH
        elif self.anthropic_api_key and self.anthropic_api_key.startswith("sk-ant-api03-"):
            self.default_model = LLMModel.CLAUDE_SONNET
    
    async def query(self, request: BigRAGRequest) -> BigRAGResponse:
        """
        Pipeline principal BIG RAG
        
        1. Détection pays
        2. Embedding de la requête
        3. Recherche multi-index
        4. Reranking
        5. Génération LLM
        6. Formatage réponse
        """
        start_time = time.time()
        
        # 1. Détection pays
        if request.country_hint:
            country_result = CountryDetectionResult(
                country=Country(request.country_hint),
                confidence=1.0,
                language=Language(request.language_hint or "fr"),
                signals=["User hint"],
            )
        else:
            country_result = self.country_detector.detect(request.query)
        
        # 2. Embedding de la requête
        query_embedding = await self.embedding_pipeline.embed_query(request.query)
        
        # 3. Recherche hybride
        search_start = time.time()
        
        # Index principal selon le pays
        primary_country = country_result.country.value
        
        search_result = await self.qdrant.hybrid_search(
            query_vector=query_embedding,
            primary_country=primary_country,
            top_k_primary=request.top_k,
            top_k_secondary=3 if request.include_global else 0,
        )
        
        search_time = (time.time() - search_start) * 1000
        
        # 4. Reranking
        rerank_start = time.time()
        contexts = []
        
        if request.rerank and search_result.results:
            texts = [r.text for r in search_result.results]
            reranked = await self.reranker_pipeline.rerank(
                query=request.query,
                documents=texts,
                top_k=request.top_k,
            )
            
            for ranked_doc in reranked.documents:
                original = search_result.results[ranked_doc.index]
                contexts.append(ContextChunk(
                    text=ranked_doc.text,
                    source=original.metadata.get("source", "unknown"),
                    country=original.metadata.get("country", "GLOBAL"),
                    score=ranked_doc.score,
                    theme=original.metadata.get("theme"),
                    url=original.metadata.get("url"),
                ))
        else:
            # Sans reranking, utiliser les résultats bruts
            for result in search_result.results[:request.top_k]:
                contexts.append(ContextChunk(
                    text=result.text,
                    source=result.metadata.get("source", "unknown"),
                    country=result.metadata.get("country", "GLOBAL"),
                    score=result.score,
                    theme=result.metadata.get("theme"),
                    url=result.metadata.get("url"),
                ))
        
        rerank_time = (time.time() - rerank_start) * 1000
        
        # 5. Génération LLM
        llm_start = time.time()
        
        # Préparer le contexte
        context_text = self._format_contexts(contexts)
        
        # Choisir le system prompt
        system_prompt = self._get_system_prompt(country_result.country)
        
        # Construire le prompt
        user_prompt = RAG_PROMPT_TEMPLATE.format(
            context=context_text,
            query=request.query,
        )
        
        # Appeler le LLM
        model = request.model or self.default_model.value
        answer, tokens_used = await self._call_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=model,
        )
        
        llm_time = (time.time() - llm_start) * 1000
        
        # 6. Préparer les sources
        sources = self._prepare_sources(contexts)
        
        # Temps total
        total_time = (time.time() - start_time) * 1000
        
        return BigRAGResponse(
            answer=answer,
            country_detected=country_result.country,
            country_confidence=country_result.confidence,
            country_signals=country_result.signals,
            country_emoji=get_country_emoji(country_result.country),
            language=country_result.language,
            model_used=model,
            provider=self._get_provider(model),
            contexts_used=contexts,
            total_contexts_found=len(search_result.results),
            sources=sources,
            search_time_ms=round(search_time, 2),
            rerank_time_ms=round(rerank_time, 2),
            llm_time_ms=round(llm_time, 2),
            total_time_ms=round(total_time, 2),
            indexes_searched=search_result.indexes_searched,
            tokens_used=tokens_used,
        )
    
    def _format_contexts(self, contexts: List[ContextChunk]) -> str:
        """Formater les contextes pour le prompt"""
        if not contexts:
            return "Aucun contexte pertinent trouvé."
        
        formatted = []
        for i, ctx in enumerate(contexts, 1):
            formatted.append(
                f"[Source {i}: {ctx.source} ({ctx.country})]:\n{ctx.text}"
            )
        
        return "\n\n".join(formatted)
    
    def _get_system_prompt(self, country: Country) -> str:
        """Obtenir le system prompt selon le pays"""
        prompts = {
            Country.DZ: SYSTEM_PROMPT_DZ,
            Country.CH: SYSTEM_PROMPT_CH,
        }
        return prompts.get(country, SYSTEM_PROMPT_GLOBAL)
    
    def _get_provider(self, model: str) -> str:
        """Déterminer le provider depuis le nom du modèle"""
        if "gpt" in model.lower():
            return LLMProvider.OPENAI.value
        elif "claude" in model.lower():
            return LLMProvider.ANTHROPIC.value
        elif "llama" in model.lower() or "mixtral" in model.lower():
            return LLMProvider.GROQ.value
        elif "gemini" in model.lower():
            return LLMProvider.GOOGLE.value
        return "unknown"
    
    async def _call_llm(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str,
    ) -> tuple[str, int]:
        """
        Appeler le LLM
        
        Returns:
            Tuple (réponse, tokens utilisés)
        """
        provider = self._get_provider(model)
        
        if provider == LLMProvider.OPENAI.value:
            return await self._call_openai(system_prompt, user_prompt, model)
        elif provider == LLMProvider.ANTHROPIC.value:
            return await self._call_anthropic(system_prompt, user_prompt, model)
        elif provider == LLMProvider.GROQ.value:
            return await self._call_groq(system_prompt, user_prompt, model)
        elif provider == LLMProvider.GOOGLE.value:
            return await self._call_google(system_prompt, user_prompt, model)
        else:
            # Fallback: utiliser Google si disponible, sinon OpenAI
            if self.google_api_key:
                return await self._call_google(
                    system_prompt, user_prompt, LLMModel.GEMINI_FLASH.value
                )
            elif self.openai_api_key:
                return await self._call_openai(
                    system_prompt, user_prompt, LLMModel.GPT4O_MINI.value
                )
            elif self.anthropic_api_key:
                return await self._call_anthropic(
                    system_prompt, user_prompt, LLMModel.CLAUDE_SONNET.value
                )
            else:
                return "Erreur: Aucun LLM configuré", 0
    
    async def _call_openai(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str,
    ) -> tuple[str, int]:
        """Appeler OpenAI"""
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openai_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "max_tokens": 2000,
                    "temperature": 0.3,
                },
            )
            response.raise_for_status()
            data = response.json()
        
        answer = data["choices"][0]["message"]["content"]
        tokens = data.get("usage", {}).get("total_tokens", 0)
        
        return answer, tokens
    
    async def _call_anthropic(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str,
    ) -> tuple[str, int]:
        """Appeler Anthropic Claude"""
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": self.anthropic_api_key,
                    "Content-Type": "application/json",
                    "anthropic-version": "2023-06-01",
                },
                json={
                    "model": model,
                    "system": system_prompt,
                    "messages": [
                        {"role": "user", "content": user_prompt},
                    ],
                    "max_tokens": 2000,
                },
            )
            response.raise_for_status()
            data = response.json()
        
        answer = data["content"][0]["text"]
        tokens = data.get("usage", {}).get("input_tokens", 0) + \
                 data.get("usage", {}).get("output_tokens", 0)
        
        return answer, tokens
    
    async def _call_groq(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str,
    ) -> tuple[str, int]:
        """Appeler Groq"""
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.groq_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "max_tokens": 2000,
                    "temperature": 0.3,
                },
            )
            response.raise_for_status()
            data = response.json()
        
        answer = data["choices"][0]["message"]["content"]
        tokens = data.get("usage", {}).get("total_tokens", 0)

        return answer, tokens

    async def _call_google(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str,
    ) -> tuple[str, int]:
        """Appeler Google Gemini"""
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={self.google_api_key}",
                headers={
                    "Content-Type": "application/json",
                },
                json={
                    "contents": [{
                        "parts": [{
                            "text": f"{system_prompt}\n\n{user_prompt}"
                        }]
                    }],
                    "generationConfig": {
                        "temperature": 0.3,
                        "maxOutputTokens": 2000,
                    }
                },
            )
            response.raise_for_status()
            data = response.json()

        answer = data["candidates"][0]["content"]["parts"][0]["text"]
        tokens = data.get("usageMetadata", {}).get("totalTokenCount", 0)

        return answer, tokens

    def _prepare_sources(self, contexts: List[ContextChunk]) -> List[Dict[str, Any]]:
        """Préparer les sources pour la réponse"""
        sources = []
        seen = set()
        
        for ctx in contexts:
            source_key = f"{ctx.source}:{ctx.country}"
            if source_key not in seen:
                seen.add(source_key)
                sources.append({
                    "source": ctx.source,
                    "country": ctx.country,
                    "country_emoji": get_country_emoji(Country(ctx.country) if ctx.country in ["DZ", "CH", "FR"] else Country.GLOBAL),
                    "theme": ctx.theme,
                    "url": ctx.url,
                    "relevance_score": ctx.score,
                })
        
        return sources
    
    async def detect_country(self, text: str) -> CountryDetectionResult:
        """Endpoint pour détection seule"""
        return self.country_detector.detect(text)
    
    async def search_only(
        self,
        query: str,
        top_k: int = 10,
        country: Optional[str] = None,
    ) -> MultiSearchResult:
        """Recherche seule (sans LLM)"""
        # Embedding
        query_embedding = await self.embedding_pipeline.embed_query(query)
        
        # Détection pays si non fourni
        if not country:
            detection = self.country_detector.detect(query)
            country = detection.country.value
        
        # Recherche
        result = await self.qdrant.hybrid_search(
            query_vector=query_embedding,
            primary_country=country,
            top_k_primary=top_k,
            top_k_secondary=3,
        )
        
        result.query = query
        return result
    
    async def get_status(self) -> Dict[str, Any]:
        """Obtenir le statut du service"""
        collections = await self.qdrant.get_all_collections_info()
        
        return {
            "status": "healthy",
            "service": "BIG RAG",
            "version": "1.0.0",
            "embedding_provider": self.embedding_pipeline.provider,
            "embedding_dimensions": self.embedding_pipeline.get_dimensions(),
            "reranker_provider": self.reranker_pipeline.provider,
            "llm_default": self.default_model.value,
            "llm_providers_available": {
                "openai": bool(self.openai_api_key),
                "anthropic": bool(self.anthropic_api_key),
                "groq": bool(self.groq_api_key),
            },
            "collections": collections,
            "countries_supported": ["DZ", "CH", "GLOBAL"],
            "languages_supported": ["fr", "ar", "de", "en"],
        }
    
    # ============================================
    # HELPER METHODS FOR AGENTIC RAG
    # ============================================
    
    def _get_qdrant_client(self):
        """Obtenir le client Qdrant pour les pipelines externes"""
        return self.qdrant._get_client()
    
    async def get_embedding(self, text: str) -> List[float]:
        """Obtenir l'embedding d'un texte (pour pipelines externes)"""
        return await self.embedding_pipeline.embed_query(text)
    
    async def detect_country(self, query: str) -> CountryDetectionResult:
        """Détecter le pays d'une requête"""
        return self.country_detector.detect(query)
    
    async def generate_answer(
        self,
        prompt: str,
        contexts: List[Dict[str, Any]] = None,
        model: str = None,
    ) -> str:
        """
        Générer une réponse à partir d'un prompt (pour Agentic RAG)
        
        Args:
            prompt: Prompt complet (peut inclure contextes et raisonnement)
            contexts: Contextes additionnels (optionnel)
            model: Modèle à utiliser (optionnel)
            
        Returns:
            Réponse générée
        """
        model = model or self.default_model.value
        
        # Si des contextes sont fournis, les ajouter
        if contexts:
            context_text = "\n\n".join([
                f"[{i+1}] {ctx.get('text', '')}"
                for i, ctx in enumerate(contexts)
            ])
            prompt = f"{prompt}\n\nContextes additionnels:\n{context_text}"
        
        answer, _ = await self._call_llm(
            system_prompt="Tu es un assistant expert qui répond de manière précise et structurée.",
            user_prompt=prompt,
            model=model,
        )
        
        return answer
    
    async def generate_answer_from_contexts(
        self,
        query: str,
        contexts: List[Dict[str, Any]],
        model: str = None,
        country: Country = None,
    ) -> str:
        """
        Générer une réponse à partir de contextes (pipeline classique)
        
        Args:
            query: Question utilisateur
            contexts: Liste de contextes {id, text, score, ...}
            model: Modèle à utiliser
            country: Pays pour le system prompt
            
        Returns:
            Réponse générée
        """
        model = model or self.default_model.value
        
        # Formater les contextes
        context_text = "\n\n".join([
            f"[Source {i+1}: {ctx.get('source', 'unknown')}]:\n{ctx.get('text', '')}"
            for i, ctx in enumerate(contexts)
        ])
        
        # System prompt selon le pays
        if country:
            system_prompt = self._get_system_prompt(country)
        else:
            # Détecter depuis le premier contexte
            first_country = contexts[0].get("country", "GLOBAL") if contexts else "GLOBAL"
            try:
                system_prompt = self._get_system_prompt(Country(first_country))
            except:
                system_prompt = SYSTEM_PROMPT_GLOBAL
        
        # Construire le prompt
        user_prompt = RAG_PROMPT_TEMPLATE.format(
            context=context_text,
            query=query,
        )
        
        answer, _ = await self._call_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=model,
        )
        
        return answer


# ============================================
# SINGLETON
# ============================================

bigrag_service = BigRAGService()
