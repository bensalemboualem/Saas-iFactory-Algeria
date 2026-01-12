"""
BIG RAG - Module Multi-Pays
===========================
RAG international pour DZ + CH + GLOBAL
Détection pays, multi-index, reranker, router IA

Nouveaux patterns (inspirés de awesome-llm-apps):
- Hybrid Search: Vector + BM25 fusion (RRF)
- Reasoning Pipeline: Step-by-step reasoning avant réponse
- Query Router: Routing intelligent vers collections
"""

from .country_detector import CountryDetector, CountryDetectionResult
from .embedding_pipeline import EmbeddingPipeline
from .reranker_pipeline import RerankerPipeline
from .qdrant_multi import QdrantMultiIndex
from .bigrag_service import BigRAGService, bigrag_service
from .bigrag_router import router as bigrag_router

# Nouveaux modules
from .hybrid_search import (
    HybridSearchPipeline, 
    hybrid_search_pipeline,
    SearchMode,
    HybridResult,
    HybridSearchResult,
)
from .reasoning_pipeline import (
    ReasoningPipeline,
    reasoning_pipeline,
    ReasoningResult,
    QueryAnalysis,
)
from .query_router import (
    HybridQueryRouter,
    KeywordRouter,
    hybrid_router,
    keyword_router,
    RoutingDecision,
    COLLECTION_REGISTRY,
)

__all__ = [
    # Original
    "CountryDetector",
    "CountryDetectionResult",
    "EmbeddingPipeline",
    "RerankerPipeline",
    "QdrantMultiIndex",
    "BigRAGService",
    "bigrag_service",
    "bigrag_router",
    # Hybrid Search
    "HybridSearchPipeline",
    "hybrid_search_pipeline",
    "SearchMode",
    "HybridResult",
    "HybridSearchResult",
    # Reasoning
    "ReasoningPipeline",
    "reasoning_pipeline",
    "ReasoningResult",
    "QueryAnalysis",
    # Query Router
    "HybridQueryRouter",
    "KeywordRouter",
    "hybrid_router",
    "keyword_router",
    "RoutingDecision",
    "COLLECTION_REGISTRY",
]
