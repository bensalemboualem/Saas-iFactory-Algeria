"""
BIG RAG - Hybrid Search Pipeline
=================================
Combine Vector Search + BM25 (Sparse) pour meilleure couverture
Inspiré de awesome-llm-apps/rag_tutorials/hybrid_search_rag

Pattern: Dense (semantic) + Sparse (keyword) = Hybrid
"""

import os
import logging
import re
from typing import List, Optional, Dict, Any, Tuple
from enum import Enum
from pydantic import BaseModel, Field
from collections import defaultdict
import math

logger = logging.getLogger(__name__)


# ============================================
# MODELS
# ============================================

class SearchMode(str, Enum):
    """Modes de recherche disponibles"""
    VECTOR = "vector"           # Dense only (semantic)
    BM25 = "bm25"              # Sparse only (keywords)
    HYBRID = "hybrid"          # Dense + Sparse fusion
    HYBRID_RERANK = "hybrid_rerank"  # Hybrid + Reranking


class HybridResult(BaseModel):
    """Résultat de recherche hybride"""
    id: str
    text: str
    vector_score: float = 0.0
    bm25_score: float = 0.0
    combined_score: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)
    index_name: str = ""
    match_type: str = "hybrid"  # vector, bm25, hybrid


class HybridSearchResult(BaseModel):
    """Résultats de recherche hybride"""
    results: List[HybridResult]
    total: int
    mode: SearchMode
    vector_weight: float
    bm25_weight: float
    indexes_searched: List[str]
    query: str
    search_time_ms: float


# ============================================
# BM25 SCORER (Lightweight Implementation)
# ============================================

class BM25Scorer:
    """
    Implémentation légère de BM25 pour scoring sparse
    Utilisé pour le fallback local quand Qdrant sparse n'est pas disponible
    """
    
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1  # Term saturation parameter
        self.b = b    # Length normalization
        self.idf_cache: Dict[str, float] = {}
        self.avgdl = 0
        self.doc_count = 0
        self.doc_freqs: Dict[str, int] = defaultdict(int)
    
    @staticmethod
    def tokenize(text: str) -> List[str]:
        """Tokenization simple (peut être amélioré avec un tokenizer plus sophistiqué)"""
        # Lowercase + split on non-alphanumeric
        text = text.lower()
        tokens = re.findall(r'\b\w+\b', text)
        # Filtrer stopwords communs FR/AR
        stopwords = {
            'le', 'la', 'les', 'un', 'une', 'des', 'de', 'du', 'et', 'en', 
            'à', 'au', 'aux', 'ce', 'ces', 'dans', 'pour', 'par', 'sur',
            'est', 'sont', 'été', 'être', 'avoir', 'a', 'ont', 'qui', 'que',
            'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
            'في', 'من', 'على', 'إلى', 'عن', 'مع', 'هذا', 'هذه', 'التي', 'الذي',
        }
        return [t for t in tokens if t not in stopwords and len(t) > 1]
    
    def fit(self, documents: List[str]):
        """Calculer les statistiques du corpus"""
        self.doc_count = len(documents)
        total_len = 0
        
        for doc in documents:
            tokens = self.tokenize(doc)
            total_len += len(tokens)
            seen = set()
            for token in tokens:
                if token not in seen:
                    self.doc_freqs[token] += 1
                    seen.add(token)
        
        self.avgdl = total_len / self.doc_count if self.doc_count > 0 else 1
        
        # Pre-compute IDF
        for token, df in self.doc_freqs.items():
            self.idf_cache[token] = math.log(
                (self.doc_count - df + 0.5) / (df + 0.5) + 1
            )
    
    def score(self, query: str, document: str) -> float:
        """Calculer le score BM25 d'un document pour une requête"""
        query_tokens = self.tokenize(query)
        doc_tokens = self.tokenize(document)
        doc_len = len(doc_tokens)
        
        if doc_len == 0:
            return 0.0
        
        # Count term frequencies in document
        tf = defaultdict(int)
        for token in doc_tokens:
            tf[token] += 1
        
        score = 0.0
        for token in query_tokens:
            if token not in tf:
                continue
            
            # Get or compute IDF
            idf = self.idf_cache.get(token)
            if idf is None:
                # Fallback IDF pour termes inconnus
                idf = math.log((self.doc_count + 1) / 2)
            
            # BM25 formula
            term_freq = tf[token]
            numerator = term_freq * (self.k1 + 1)
            denominator = term_freq + self.k1 * (1 - self.b + self.b * (doc_len / self.avgdl))
            score += idf * (numerator / denominator)
        
        return score
    
    def score_batch(self, query: str, documents: List[str]) -> List[Tuple[int, float]]:
        """Scorer plusieurs documents"""
        scores = []
        for i, doc in enumerate(documents):
            score = self.score(query, doc)
            scores.append((i, score))
        return sorted(scores, key=lambda x: x[1], reverse=True)


# ============================================
# RECIPROCAL RANK FUSION (RRF)
# ============================================

def reciprocal_rank_fusion(
    vector_results: List[Tuple[str, float]],  # (id, score)
    bm25_results: List[Tuple[str, float]],    # (id, score)
    k: int = 60,  # RRF constant
    vector_weight: float = 0.6,
    bm25_weight: float = 0.4,
) -> List[Tuple[str, float]]:
    """
    Fusion des résultats par Reciprocal Rank Fusion
    
    RRF score = sum(1 / (k + rank_i) * weight_i)
    
    Args:
        vector_results: Résultats recherche vectorielle (id, score)
        bm25_results: Résultats recherche BM25 (id, score)
        k: Constante RRF (default 60)
        vector_weight: Poids recherche vectorielle
        bm25_weight: Poids recherche BM25
        
    Returns:
        Liste fusionnée (id, combined_score)
    """
    fusion_scores: Dict[str, float] = defaultdict(float)
    
    # Vector scores
    for rank, (doc_id, _) in enumerate(vector_results, start=1):
        fusion_scores[doc_id] += vector_weight * (1 / (k + rank))
    
    # BM25 scores
    for rank, (doc_id, _) in enumerate(bm25_results, start=1):
        fusion_scores[doc_id] += bm25_weight * (1 / (k + rank))
    
    # Sort by fusion score
    fused = sorted(fusion_scores.items(), key=lambda x: x[1], reverse=True)
    return fused


# ============================================
# HYBRID SEARCH PIPELINE
# ============================================

class HybridSearchPipeline:
    """
    Pipeline de recherche hybride (Dense + Sparse)
    
    Combine:
    1. Recherche vectorielle (Qdrant dense vectors)
    2. Recherche BM25 (keywords matching)
    3. Fusion RRF (Reciprocal Rank Fusion)
    4. Reranking optionnel (Cohere/Jina)
    """
    
    def __init__(
        self,
        vector_weight: float = 0.6,
        bm25_weight: float = 0.4,
        rrf_k: int = 60,
        use_qdrant_sparse: bool = False,  # True si Qdrant avec sparse vectors
    ):
        self.vector_weight = vector_weight
        self.bm25_weight = bm25_weight
        self.rrf_k = rrf_k
        self.use_qdrant_sparse = use_qdrant_sparse
        
        # BM25 scorer local (fallback)
        self.bm25_scorer = BM25Scorer()
        self._corpus_fitted = False
    
    def fit_corpus(self, documents: List[str]):
        """Fit BM25 sur le corpus (pour mode local)"""
        self.bm25_scorer.fit(documents)
        self._corpus_fitted = True
        logger.info(f"BM25 fitted on {len(documents)} documents")
    
    async def search(
        self,
        query: str,
        query_vector: List[float],
        qdrant_client,
        collection_name: str,
        top_k: int = 10,
        mode: SearchMode = SearchMode.HYBRID,
        documents_cache: Optional[Dict[str, str]] = None,
    ) -> HybridSearchResult:
        """
        Recherche hybride complète
        
        Args:
            query: Texte de la requête
            query_vector: Embedding de la requête
            qdrant_client: Client Qdrant
            collection_name: Nom de la collection
            top_k: Nombre de résultats
            mode: Mode de recherche
            documents_cache: Cache des documents {id: text}
            
        Returns:
            HybridSearchResult
        """
        import time
        start = time.time()
        
        results = []
        
        # 1. VECTOR SEARCH
        if mode in [SearchMode.VECTOR, SearchMode.HYBRID, SearchMode.HYBRID_RERANK]:
            try:
                vector_hits = qdrant_client.search(
                    collection_name=collection_name,
                    query_vector=query_vector,
                    limit=top_k * 2,  # Over-fetch pour fusion
                )
                vector_results = [
                    (str(hit.id), hit.score, hit.payload)
                    for hit in vector_hits
                ]
            except Exception as e:
                logger.error(f"Vector search failed: {e}")
                vector_results = []
        else:
            vector_results = []
        
        # 2. BM25 SEARCH
        if mode in [SearchMode.BM25, SearchMode.HYBRID, SearchMode.HYBRID_RERANK]:
            if self.use_qdrant_sparse:
                # TODO: Utiliser Qdrant sparse vectors quand disponible
                bm25_results = []
            else:
                # Fallback: BM25 local sur les résultats vectoriels
                if documents_cache and self._corpus_fitted:
                    all_docs = list(documents_cache.items())
                    scores = self.bm25_scorer.score_batch(
                        query, 
                        [doc for _, doc in all_docs]
                    )
                    bm25_results = [
                        (all_docs[idx][0], score, {})
                        for idx, score in scores[:top_k * 2]
                        if score > 0
                    ]
                elif vector_results:
                    # BM25 sur les résultats vectoriels
                    docs_to_score = [
                        (str(r[0]), r[2].get("text", ""), r[2])
                        for r in vector_results
                    ]
                    bm25_scores = []
                    for doc_id, text, payload in docs_to_score:
                        score = self.bm25_scorer.score(query, text)
                        bm25_scores.append((doc_id, score, payload))
                    bm25_results = sorted(
                        bm25_scores, 
                        key=lambda x: x[1], 
                        reverse=True
                    )
                else:
                    bm25_results = []
        else:
            bm25_results = []
        
        # 3. FUSION
        if mode == SearchMode.VECTOR:
            # Vector only
            for doc_id, score, payload in vector_results[:top_k]:
                results.append(HybridResult(
                    id=doc_id,
                    text=payload.get("text", ""),
                    vector_score=score,
                    combined_score=score,
                    metadata={k: v for k, v in payload.items() if k != "text"},
                    index_name=collection_name,
                    match_type="vector",
                ))
        
        elif mode == SearchMode.BM25:
            # BM25 only
            for doc_id, score, payload in bm25_results[:top_k]:
                results.append(HybridResult(
                    id=doc_id,
                    text=payload.get("text", "") if payload else "",
                    bm25_score=score,
                    combined_score=score,
                    metadata=payload if payload else {},
                    index_name=collection_name,
                    match_type="bm25",
                ))
        
        else:
            # Hybrid fusion
            vector_for_rrf = [(r[0], r[1]) for r in vector_results]
            bm25_for_rrf = [(r[0], r[1]) for r in bm25_results]
            
            fused = reciprocal_rank_fusion(
                vector_for_rrf,
                bm25_for_rrf,
                k=self.rrf_k,
                vector_weight=self.vector_weight,
                bm25_weight=self.bm25_weight,
            )
            
            # Build result map
            all_docs = {}
            for doc_id, v_score, payload in vector_results:
                all_docs[doc_id] = {
                    "vector_score": v_score,
                    "bm25_score": 0.0,
                    "payload": payload,
                }
            for doc_id, b_score, payload in bm25_results:
                if doc_id in all_docs:
                    all_docs[doc_id]["bm25_score"] = b_score
                else:
                    all_docs[doc_id] = {
                        "vector_score": 0.0,
                        "bm25_score": b_score,
                        "payload": payload,
                    }
            
            for doc_id, combined_score in fused[:top_k]:
                doc_data = all_docs.get(doc_id, {})
                payload = doc_data.get("payload", {})
                
                results.append(HybridResult(
                    id=doc_id,
                    text=payload.get("text", "") if payload else "",
                    vector_score=doc_data.get("vector_score", 0.0),
                    bm25_score=doc_data.get("bm25_score", 0.0),
                    combined_score=combined_score,
                    metadata={k: v for k, v in payload.items() if k != "text"} if payload else {},
                    index_name=collection_name,
                    match_type="hybrid",
                ))
        
        elapsed_ms = (time.time() - start) * 1000
        
        return HybridSearchResult(
            results=results,
            total=len(results),
            mode=mode,
            vector_weight=self.vector_weight,
            bm25_weight=self.bm25_weight,
            indexes_searched=[collection_name],
            query=query,
            search_time_ms=elapsed_ms,
        )
    
    async def search_multi(
        self,
        query: str,
        query_vector: List[float],
        qdrant_client,
        collections: List[str],
        top_k: int = 10,
        mode: SearchMode = SearchMode.HYBRID,
    ) -> HybridSearchResult:
        """
        Recherche hybride sur plusieurs collections
        """
        import time
        start = time.time()
        
        all_results = []
        
        for collection in collections:
            try:
                result = await self.search(
                    query=query,
                    query_vector=query_vector,
                    qdrant_client=qdrant_client,
                    collection_name=collection,
                    top_k=top_k,
                    mode=mode,
                )
                all_results.extend(result.results)
            except Exception as e:
                logger.error(f"Search in {collection} failed: {e}")
        
        # Sort by combined score
        all_results.sort(key=lambda x: x.combined_score, reverse=True)
        
        elapsed_ms = (time.time() - start) * 1000
        
        return HybridSearchResult(
            results=all_results[:top_k],
            total=len(all_results),
            mode=mode,
            vector_weight=self.vector_weight,
            bm25_weight=self.bm25_weight,
            indexes_searched=collections,
            query=query,
            search_time_ms=elapsed_ms,
        )


# Singleton instance
hybrid_search_pipeline = HybridSearchPipeline()
