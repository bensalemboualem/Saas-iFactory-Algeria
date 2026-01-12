"""
BIG RAG - Reranker Pipeline
============================
Pipeline de reranking pour améliorer la pertinence des résultats
Support local (BGE) et cloud (Cohere, Jina)
"""

import os
import logging
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Dict, Any
from enum import Enum
import httpx
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


# ============================================
# ENUMS & MODELS
# ============================================

class RerankerProvider(str, Enum):
    """Providers de reranking"""
    COHERE = "cohere"
    JINA = "jina"
    VOYAGE = "voyage"
    LOCAL = "local"  # BGE Reranker
    NONE = "none"    # Pas de reranking


class RerankerModel(str, Enum):
    """Modèles de reranking"""
    # Cohere
    COHERE_RERANK_3 = "rerank-v3.5"
    COHERE_RERANK_MULTILINGUAL = "rerank-multilingual-v3.0"
    
    # Jina
    JINA_RERANKER = "jina-reranker-v2-base-multilingual"
    
    # Voyage
    VOYAGE_RERANK = "rerank-2"
    
    # Local
    BGE_RERANKER_BASE = "BAAI/bge-reranker-base"
    BGE_RERANKER_LARGE = "BAAI/bge-reranker-large"
    BGE_RERANKER_V2 = "BAAI/bge-reranker-v2-m3"


class RankedDocument(BaseModel):
    """Document reranké"""
    index: int = Field(..., description="Index original")
    text: str = Field(..., description="Texte du document")
    score: float = Field(..., description="Score de relevance")
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RerankerResult(BaseModel):
    """Résultat du reranking"""
    documents: List[RankedDocument] = Field(..., description="Documents triés")
    model: str = Field(..., description="Modèle utilisé")
    provider: str = Field(..., description="Provider utilisé")
    query: str = Field(..., description="Requête originale")


# ============================================
# ABSTRACT BASE
# ============================================

class BaseReranker(ABC):
    """Classe de base pour les rerankers"""
    
    @abstractmethod
    async def rerank(
        self, 
        query: str, 
        documents: List[str],
        top_k: int = 5,
    ) -> List[RankedDocument]:
        """Reranker les documents"""
        pass


# ============================================
# COHERE RERANKER
# ============================================

class CohereReranker(BaseReranker):
    """Reranker Cohere (recommandé pour multilingual)"""
    
    def __init__(
        self,
        model: RerankerModel = RerankerModel.COHERE_RERANK_MULTILINGUAL,
        api_key: Optional[str] = None,
    ):
        self.model = model
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        self.base_url = "https://api.cohere.ai/v1/rerank"
    
    async def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 5,
    ) -> List[RankedDocument]:
        """Reranker via Cohere API"""
        if not documents:
            return []
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model.value,
                    "query": query,
                    "documents": documents,
                    "top_n": min(top_k, len(documents)),
                    "return_documents": True,
                },
            )
            response.raise_for_status()
            data = response.json()
        
        results = []
        for item in data.get("results", []):
            results.append(RankedDocument(
                index=item["index"],
                text=documents[item["index"]],
                score=item["relevance_score"],
            ))
        
        return results


# ============================================
# JINA RERANKER
# ============================================

class JinaReranker(BaseReranker):
    """Reranker Jina AI"""
    
    def __init__(
        self,
        model: RerankerModel = RerankerModel.JINA_RERANKER,
        api_key: Optional[str] = None,
    ):
        self.model = model
        self.api_key = api_key or os.getenv("JINA_API_KEY")
        self.base_url = "https://api.jina.ai/v1/rerank"
    
    async def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 5,
    ) -> List[RankedDocument]:
        """Reranker via Jina API"""
        if not documents:
            return []
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model.value,
                    "query": query,
                    "documents": documents,
                    "top_n": min(top_k, len(documents)),
                },
            )
            response.raise_for_status()
            data = response.json()
        
        results = []
        for item in data.get("results", []):
            results.append(RankedDocument(
                index=item["index"],
                text=documents[item["index"]],
                score=item["relevance_score"],
            ))
        
        return results


# ============================================
# VOYAGE RERANKER
# ============================================

class VoyageReranker(BaseReranker):
    """Reranker VoyageAI"""
    
    def __init__(
        self,
        model: RerankerModel = RerankerModel.VOYAGE_RERANK,
        api_key: Optional[str] = None,
    ):
        self.model = model
        self.api_key = api_key or os.getenv("VOYAGE_API_KEY")
        self.base_url = "https://api.voyageai.com/v1/rerank"
    
    async def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 5,
    ) -> List[RankedDocument]:
        """Reranker via VoyageAI API"""
        if not documents:
            return []
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model.value,
                    "query": query,
                    "documents": documents,
                    "top_k": min(top_k, len(documents)),
                },
            )
            response.raise_for_status()
            data = response.json()
        
        results = []
        for item in data.get("data", []):
            results.append(RankedDocument(
                index=item["index"],
                text=documents[item["index"]],
                score=item["relevance_score"],
            ))
        
        return results


# ============================================
# LOCAL RERANKER (BGE)
# ============================================

class LocalReranker(BaseReranker):
    """
    Reranker local avec BGE
    Nécessite: pip install FlagEmbedding
    """
    
    def __init__(
        self,
        model: RerankerModel = RerankerModel.BGE_RERANKER_V2,
    ):
        self.model = model
        self._reranker = None
    
    def _load_model(self):
        """Charger le modèle (lazy loading)"""
        if self._reranker is None:
            try:
                from FlagEmbedding import FlagReranker
                self._reranker = FlagReranker(
                    self.model.value,
                    use_fp16=True,
                )
                logger.info(f"Loaded local reranker: {self.model.value}")
            except ImportError:
                raise RuntimeError(
                    "FlagEmbedding not installed. "
                    "Run: pip install FlagEmbedding"
                )
        return self._reranker
    
    async def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 5,
    ) -> List[RankedDocument]:
        """Reranker localement avec BGE"""
        if not documents:
            return []
        
        model = self._load_model()
        
        # Créer paires (query, doc)
        pairs = [[query, doc] for doc in documents]
        
        # Calculer scores
        scores = model.compute_score(pairs, normalize=True)
        
        # Créer résultats triés
        indexed_scores = list(enumerate(scores))
        indexed_scores.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for idx, score in indexed_scores[:top_k]:
            results.append(RankedDocument(
                index=idx,
                text=documents[idx],
                score=float(score),
            ))
        
        return results


# ============================================
# SIMPLE RERANKER (Fallback)
# ============================================

class SimpleReranker(BaseReranker):
    """
    Reranker simple basé sur la similarité de mots
    Utilisé comme fallback quand aucun provider n'est disponible
    """
    
    def __init__(self):
        pass
    
    async def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 5,
    ) -> List[RankedDocument]:
        """Reranking simple basé sur les mots communs"""
        if not documents:
            return []
        
        query_words = set(query.lower().split())
        
        scored_docs = []
        for idx, doc in enumerate(documents):
            doc_words = set(doc.lower().split())
            
            # Score = Jaccard similarity + bonus pour mots de la query
            intersection = query_words & doc_words
            union = query_words | doc_words
            
            jaccard = len(intersection) / len(union) if union else 0
            
            # Bonus pour occurrence de mots de la query
            query_coverage = len(intersection) / len(query_words) if query_words else 0
            
            score = 0.4 * jaccard + 0.6 * query_coverage
            
            scored_docs.append((idx, doc, score))
        
        # Trier par score décroissant
        scored_docs.sort(key=lambda x: x[2], reverse=True)
        
        results = []
        for idx, text, score in scored_docs[:top_k]:
            results.append(RankedDocument(
                index=idx,
                text=text,
                score=score,
            ))
        
        return results


# ============================================
# RERANKER PIPELINE
# ============================================

class RerankerPipeline:
    """
    Pipeline de reranking avec fallback automatique
    
    Ordre de priorité:
    1. Cohere (si clé disponible)
    2. Jina (si clé disponible)
    3. VoyageAI (si clé disponible)
    4. Local BGE (si disponible)
    5. Simple (fallback)
    """
    
    def __init__(
        self,
        primary_provider: RerankerProvider = RerankerProvider.COHERE,
        primary_model: Optional[RerankerModel] = None,
        fallback_to_simple: bool = True,
    ):
        self.primary_provider = primary_provider
        self.fallback_to_simple = fallback_to_simple
        self._reranker: Optional[BaseReranker] = None
        self._init_reranker(primary_provider, primary_model)
    
    def _init_reranker(
        self,
        provider: RerankerProvider,
        model: Optional[RerankerModel] = None,
    ):
        """Initialiser le reranker selon le provider"""
        
        if provider == RerankerProvider.COHERE:
            api_key = os.getenv("COHERE_API_KEY")
            if api_key:
                self._reranker = CohereReranker(
                    model=model or RerankerModel.COHERE_RERANK_MULTILINGUAL,
                    api_key=api_key,
                )
                logger.info("Using Cohere reranker")
                return
        
        elif provider == RerankerProvider.JINA:
            api_key = os.getenv("JINA_API_KEY")
            if api_key:
                self._reranker = JinaReranker(
                    model=model or RerankerModel.JINA_RERANKER,
                    api_key=api_key,
                )
                logger.info("Using Jina reranker")
                return
        
        elif provider == RerankerProvider.VOYAGE:
            api_key = os.getenv("VOYAGE_API_KEY")
            if api_key:
                self._reranker = VoyageReranker(
                    model=model or RerankerModel.VOYAGE_RERANK,
                    api_key=api_key,
                )
                logger.info("Using VoyageAI reranker")
                return
        
        elif provider == RerankerProvider.LOCAL:
            try:
                self._reranker = LocalReranker(
                    model=model or RerankerModel.BGE_RERANKER_V2,
                )
                logger.info("Using local BGE reranker")
                return
            except Exception as e:
                logger.warning(f"Failed to load local reranker: {e}")
        
        # Fallback to simple
        if self.fallback_to_simple:
            logger.warning(f"No reranker available for {provider}, using simple fallback")
            self._reranker = SimpleReranker()
        else:
            raise ValueError(f"No reranker available for {provider}")
    
    async def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 5,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> RerankerResult:
        """
        Reranker les documents
        
        Args:
            query: Requête utilisateur
            documents: Liste de documents à reranker
            top_k: Nombre de documents à retourner
            metadata: Métadonnées associées aux documents
            
        Returns:
            RerankerResult avec documents triés
        """
        if not self._reranker:
            raise RuntimeError("No reranker configured")
        
        ranked = await self._reranker.rerank(query, documents, top_k)
        
        # Ajouter métadonnées si fournies
        if metadata:
            for doc in ranked:
                if doc.index < len(metadata):
                    doc.metadata = metadata[doc.index]
        
        return RerankerResult(
            documents=ranked,
            model=self._get_model_name(),
            provider=self.provider,
            query=query,
        )
    
    async def rerank_with_scores(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        text_key: str = "text",
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Reranker des documents avec leur score
        
        Args:
            query: Requête
            documents: Documents (dicts avec texte)
            text_key: Clé du texte dans les dicts
            top_k: Nombre à retourner
            
        Returns:
            Documents triés avec score de reranking ajouté
        """
        texts = [doc.get(text_key, "") for doc in documents]
        
        result = await self.rerank(
            query=query,
            documents=texts,
            top_k=top_k,
            metadata=[doc for doc in documents],
        )
        
        # Reconstruire les documents avec scores
        reranked_docs = []
        for ranked_doc in result.documents:
            original_doc = documents[ranked_doc.index].copy()
            original_doc["rerank_score"] = ranked_doc.score
            original_doc["rerank_index"] = ranked_doc.index
            reranked_docs.append(original_doc)
        
        return reranked_docs
    
    def _get_model_name(self) -> str:
        """Retourne le nom du modèle utilisé"""
        if isinstance(self._reranker, CohereReranker):
            return self._reranker.model.value
        elif isinstance(self._reranker, JinaReranker):
            return self._reranker.model.value
        elif isinstance(self._reranker, VoyageReranker):
            return self._reranker.model.value
        elif isinstance(self._reranker, LocalReranker):
            return self._reranker.model.value
        return "simple-reranker"
    
    @property
    def provider(self) -> str:
        """Retourne le provider actuel"""
        if isinstance(self._reranker, CohereReranker):
            return RerankerProvider.COHERE.value
        elif isinstance(self._reranker, JinaReranker):
            return RerankerProvider.JINA.value
        elif isinstance(self._reranker, VoyageReranker):
            return RerankerProvider.VOYAGE.value
        elif isinstance(self._reranker, LocalReranker):
            return RerankerProvider.LOCAL.value
        return RerankerProvider.NONE.value


# ============================================
# SINGLETON
# ============================================

reranker_pipeline = RerankerPipeline(
    primary_provider=RerankerProvider.COHERE,
    fallback_to_simple=True,
)
