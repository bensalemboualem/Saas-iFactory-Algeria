"""
Advanced RAG Service - Hybrid Search, Multi-hop Retrieval, Intelligent Reranking
Production-grade RAG with query decomposition and context optimization
Token tracking integre.
"""
import asyncio
import logging
import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

import httpx
from pydantic import BaseModel

from app.config import get_settings

# Token tracking
try:
    from app.tokens.llm_proxy import check_token_balance, deduct_after_llm_call, InsufficientTokensError
    TOKENS_AVAILABLE = True
except ImportError:
    TOKENS_AVAILABLE = False

logger = logging.getLogger(__name__)
settings = get_settings()


class SearchStrategy(str, Enum):
    """Search strategy types"""
    VECTOR = "vector"           # Pure semantic search
    KEYWORD = "keyword"         # BM25/Full-text search
    HYBRID = "hybrid"           # Combined vector + keyword
    MULTI_HOP = "multi_hop"     # Multi-step reasoning retrieval


@dataclass
class SearchResult:
    """Individual search result"""
    id: str
    content: str
    score: float
    source: str
    metadata: Dict[str, Any]
    strategy: SearchStrategy


class QueryDecomposer:
    """
    Decompose complex queries into sub-queries for multi-hop retrieval
    """

    DECOMPOSITION_PATTERNS = {
        "comparison": r"compar|diff[ée]rence|versus|vs\.?|contre",
        "causal": r"pourquoi|cause|raison|expliqu|comment",
        "temporal": r"quand|avant|après|depuis|jusqu",
        "listing": r"liste|tous les|quels sont|exemples",
        "procedural": r"étapes|processus|comment faire|procédure",
    }

    async def decompose(self, query: str) -> List[str]:
        """
        Decompose a complex query into sub-queries

        Returns list of sub-queries for multi-hop retrieval
        """
        query_lower = query.lower()
        sub_queries = [query]  # Always include original

        # Detect query type
        query_type = self._detect_query_type(query_lower)

        if query_type == "comparison":
            # Extract entities being compared
            entities = self._extract_comparison_entities(query)
            for entity in entities[:2]:
                sub_queries.append(f"Définition et caractéristiques de {entity}")

        elif query_type == "causal":
            # Add context-gathering sub-queries
            main_topic = self._extract_main_topic(query)
            sub_queries.append(f"Contexte général de {main_topic}")
            sub_queries.append(f"Facteurs influençant {main_topic}")

        elif query_type == "procedural":
            main_topic = self._extract_main_topic(query)
            sub_queries.append(f"Prérequis pour {main_topic}")
            sub_queries.append(f"Étapes de {main_topic}")

        return sub_queries[:4]  # Limit to 4 sub-queries

    def _detect_query_type(self, query: str) -> str:
        for query_type, pattern in self.DECOMPOSITION_PATTERNS.items():
            if re.search(pattern, query, re.IGNORECASE):
                return query_type
        return "simple"

    def _extract_comparison_entities(self, query: str) -> List[str]:
        # Simple entity extraction
        patterns = [
            r"entre (.+?) et (.+?)(?:\s|$|\?)",
            r"(.+?) vs\.? (.+?)(?:\s|$|\?)",
            r"(.+?) ou (.+?)(?:\s|$|\?)",
        ]
        for pattern in patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                return [match.group(1).strip(), match.group(2).strip()]
        return []

    def _extract_main_topic(self, query: str) -> str:
        # Remove question words and extract main topic
        stopwords = ["comment", "pourquoi", "quand", "où", "qui", "que", "quel", "quels", "quelle", "quelles"]
        words = query.split()
        topic_words = [w for w in words if w.lower() not in stopwords]
        return " ".join(topic_words[:5])


class HybridSearcher:
    """
    Combines vector and keyword search for optimal retrieval
    """

    def __init__(self):
        self.vector_weight = 0.7
        self.keyword_weight = 0.3

    async def search(
        self,
        query: str,
        collection: str = "default",
        limit: int = 10,
        filters: Dict[str, Any] = None
    ) -> List[SearchResult]:
        """
        Perform hybrid search combining vector and keyword methods
        """
        # Run both searches in parallel
        vector_task = self._vector_search(query, collection, limit * 2, filters)
        keyword_task = self._keyword_search(query, collection, limit * 2, filters)

        vector_results, keyword_results = await asyncio.gather(
            vector_task, keyword_task, return_exceptions=True
        )

        # Handle potential errors
        if isinstance(vector_results, Exception):
            logger.error(f"Vector search failed: {vector_results}")
            vector_results = []
        if isinstance(keyword_results, Exception):
            logger.error(f"Keyword search failed: {keyword_results}")
            keyword_results = []

        # Merge and rerank results
        merged = self._merge_results(vector_results, keyword_results)

        return merged[:limit]

    async def _vector_search(
        self,
        query: str,
        collection: str,
        limit: int,
        filters: Dict[str, Any] = None
    ) -> List[SearchResult]:
        """Semantic vector search via Qdrant"""
        try:
            # Get embeddings
            embedding = await self._get_embedding(query)

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.qdrant_url}/collections/{collection}/points/search",
                    json={
                        "vector": embedding,
                        "limit": limit,
                        "with_payload": True,
                        "filter": filters
                    },
                    timeout=30.0
                )

                if response.status_code == 200:
                    data = response.json()
                    return [
                        SearchResult(
                            id=str(hit["id"]),
                            content=hit["payload"].get("content", ""),
                            score=hit["score"],
                            source=hit["payload"].get("source", "unknown"),
                            metadata=hit["payload"],
                            strategy=SearchStrategy.VECTOR
                        )
                        for hit in data.get("result", [])
                    ]
        except Exception as e:
            logger.error(f"Vector search error: {e}")

        return []

    async def _keyword_search(
        self,
        query: str,
        collection: str,
        limit: int,
        filters: Dict[str, Any] = None
    ) -> List[SearchResult]:
        """Full-text keyword search via Meilisearch"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.meilisearch_url}/indexes/{collection}/search",
                    json={
                        "q": query,
                        "limit": limit,
                        "filter": self._build_meilisearch_filter(filters)
                    },
                    headers={"Authorization": f"Bearer {settings.meilisearch_key}"},
                    timeout=30.0
                )

                if response.status_code == 200:
                    data = response.json()
                    return [
                        SearchResult(
                            id=str(hit.get("id", "")),
                            content=hit.get("content", ""),
                            score=1.0 / (i + 1),  # Position-based score
                            source=hit.get("source", "unknown"),
                            metadata=hit,
                            strategy=SearchStrategy.KEYWORD
                        )
                        for i, hit in enumerate(data.get("hits", []))
                    ]
        except Exception as e:
            logger.error(f"Keyword search error: {e}")

        return []

    async def _get_embedding(self, text: str) -> List[float]:
        """Get text embedding"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"http://localhost:{settings.port}/api/embeddings",
                    json={"text": text},
                    timeout=30.0
                )
                if response.status_code == 200:
                    return response.json().get("embedding", [])
        except Exception as e:
            logger.error(f"Embedding error: {e}")

        # Fallback to OpenAI
        import openai
        client = openai.OpenAI(api_key=settings.openai_api_key)
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding

    def _merge_results(
        self,
        vector_results: List[SearchResult],
        keyword_results: List[SearchResult]
    ) -> List[SearchResult]:
        """
        Merge and rerank results using Reciprocal Rank Fusion (RRF)
        """
        k = 60  # RRF constant

        # Build score map
        doc_scores: Dict[str, float] = {}
        doc_map: Dict[str, SearchResult] = {}

        # Process vector results
        for rank, result in enumerate(vector_results):
            rrf_score = self.vector_weight / (k + rank + 1)
            doc_scores[result.id] = doc_scores.get(result.id, 0) + rrf_score
            doc_map[result.id] = result

        # Process keyword results
        for rank, result in enumerate(keyword_results):
            rrf_score = self.keyword_weight / (k + rank + 1)
            doc_scores[result.id] = doc_scores.get(result.id, 0) + rrf_score
            if result.id not in doc_map:
                doc_map[result.id] = result

        # Sort by combined score
        sorted_ids = sorted(doc_scores.keys(), key=lambda x: doc_scores[x], reverse=True)

        # Build merged results
        merged = []
        for doc_id in sorted_ids:
            result = doc_map[doc_id]
            result.score = doc_scores[doc_id]
            result.strategy = SearchStrategy.HYBRID
            merged.append(result)

        return merged

    def _build_meilisearch_filter(self, filters: Dict[str, Any] = None) -> str:
        if not filters:
            return ""
        # Convert to Meilisearch filter syntax
        filter_parts = []
        for key, value in filters.items():
            if isinstance(value, list):
                filter_parts.append(f"{key} IN {value}")
            else:
                filter_parts.append(f"{key} = '{value}'")
        return " AND ".join(filter_parts)


class CrossEncoderReranker:
    """
    Rerank results using cross-encoder model for better relevance
    """

    def __init__(self):
        self.model_name = "cross-encoder/ms-marco-MiniLM-L-6-v2"
        self._model = None

    async def rerank(
        self,
        query: str,
        results: List[SearchResult],
        top_k: int = 5
    ) -> List[SearchResult]:
        """
        Rerank results using cross-encoder
        """
        if not results:
            return []

        try:
            # Load model lazily
            if self._model is None:
                from sentence_transformers import CrossEncoder
                self._model = CrossEncoder(self.model_name)

            # Prepare pairs
            pairs = [(query, r.content) for r in results]

            # Get scores
            scores = self._model.predict(pairs)

            # Update result scores
            for result, score in zip(results, scores):
                result.score = float(score)

            # Sort by new scores
            results.sort(key=lambda x: x.score, reverse=True)

            return results[:top_k]

        except Exception as e:
            logger.error(f"Reranking error: {e}")
            return results[:top_k]


class AdvancedRAGService:
    """
    Production-grade RAG service with all advanced features
    """

    def __init__(self):
        self.decomposer = QueryDecomposer()
        self.hybrid_searcher = HybridSearcher()
        self.reranker = CrossEncoderReranker()

    async def retrieve(
        self,
        query: str,
        strategy: SearchStrategy = SearchStrategy.HYBRID,
        collection: str = "default",
        limit: int = 5,
        use_reranking: bool = True,
        use_multi_hop: bool = False,
        filters: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Advanced retrieval with configurable strategy

        Args:
            query: User query
            strategy: Search strategy to use
            collection: Collection to search
            limit: Max results to return
            use_reranking: Apply cross-encoder reranking
            use_multi_hop: Use query decomposition for complex queries
            filters: Optional filters

        Returns:
            Dict with results and metadata
        """
        start_time = asyncio.get_event_loop().time()

        results = []
        sub_queries = [query]

        # Multi-hop retrieval
        if use_multi_hop or strategy == SearchStrategy.MULTI_HOP:
            sub_queries = await self.decomposer.decompose(query)
            logger.info(f"Decomposed into {len(sub_queries)} sub-queries")

        # Search for each sub-query
        all_results = []
        for sq in sub_queries:
            if strategy == SearchStrategy.VECTOR:
                sq_results = await self.hybrid_searcher._vector_search(sq, collection, limit * 2, filters)
            elif strategy == SearchStrategy.KEYWORD:
                sq_results = await self.hybrid_searcher._keyword_search(sq, collection, limit * 2, filters)
            else:
                sq_results = await self.hybrid_searcher.search(sq, collection, limit * 2, filters)

            all_results.extend(sq_results)

        # Deduplicate by ID
        seen_ids = set()
        unique_results = []
        for r in all_results:
            if r.id not in seen_ids:
                seen_ids.add(r.id)
                unique_results.append(r)

        # Rerank if enabled
        if use_reranking and unique_results:
            results = await self.reranker.rerank(query, unique_results, limit)
        else:
            # Sort by score
            unique_results.sort(key=lambda x: x.score, reverse=True)
            results = unique_results[:limit]

        duration_ms = (asyncio.get_event_loop().time() - start_time) * 1000

        return {
            "query": query,
            "sub_queries": sub_queries if len(sub_queries) > 1 else None,
            "strategy": strategy.value,
            "results": [
                {
                    "id": r.id,
                    "content": r.content,
                    "score": round(r.score, 4),
                    "source": r.source,
                    "metadata": r.metadata
                }
                for r in results
            ],
            "total": len(results),
            "duration_ms": round(duration_ms, 2),
            "reranked": use_reranking
        }

    async def generate_answer(
        self,
        query: str,
        context_results: List[Dict[str, Any]],
        model: str = "gpt-4o-mini",
        system_prompt: str = None,
        tenant_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate answer from retrieved context with token tracking
        """
        # Build context
        context_parts = []
        sources = []
        for i, r in enumerate(context_results, 1):
            context_parts.append(f"[{i}] {r['content']}")
            sources.append({"index": i, "source": r.get("source", "unknown")})

        context_text = "\n\n".join(context_parts)

        # Build prompt
        augmented_prompt = f"""Contexte récupéré:
{context_text}

Question: {query}

Instructions:
- Réponds en te basant uniquement sur le contexte fourni
- Cite tes sources avec [numéro]
- Si le contexte ne permet pas de répondre, indique-le clairement"""

        sys_prompt = system_prompt or "Tu es un assistant RAG expert. Réponds de manière précise et concise."

        # Token tracking: verifier solde AVANT l'appel
        if TOKENS_AVAILABLE and tenant_id:
            estimated_tokens = len((sys_prompt + augmented_prompt).split()) * 2 + 500
            try:
                check_token_balance(tenant_id, estimated_tokens)
            except InsufficientTokensError:
                raise

        # Generate response
        import openai
        client = openai.OpenAI(api_key=settings.openai_api_key)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": augmented_prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )

        answer = response.choices[0].message.content

        # Token tracking: deduire tokens APRES l'appel
        if TOKENS_AVAILABLE and tenant_id and response.usage:
            try:
                deduct_after_llm_call(
                    tenant_id=tenant_id,
                    provider="openai",
                    model=model,
                    tokens_input=response.usage.prompt_tokens,
                    tokens_output=response.usage.completion_tokens
                )
            except Exception as e:
                logger.warning(f"Token deduction failed (advanced_rag): {e}")

        return {
            "answer": answer,
            "sources": sources,
            "model": model,
            "tokens_used": response.usage.total_tokens
        }

    async def rag_query(
        self,
        query: str,
        collection: str = "default",
        strategy: SearchStrategy = SearchStrategy.HYBRID,
        limit: int = 5,
        generate: bool = True,
        tenant_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Complete RAG pipeline: retrieve + generate with token tracking
        """
        # Retrieve
        retrieval_result = await self.retrieve(
            query=query,
            strategy=strategy,
            collection=collection,
            limit=limit,
            **kwargs
        )

        if not generate:
            return retrieval_result

        # Generate with token tracking
        if retrieval_result["results"]:
            generation_result = await self.generate_answer(
                query=query,
                context_results=retrieval_result["results"],
                tenant_id=tenant_id
            )

            return {
                **retrieval_result,
                "answer": generation_result["answer"],
                "sources": generation_result["sources"],
                "generation_model": generation_result["model"],
                "tokens_used": generation_result["tokens_used"]
            }

        return {
            **retrieval_result,
            "answer": "Aucun contexte pertinent trouvé pour répondre à cette question.",
            "sources": []
        }


# Singleton instance
advanced_rag = AdvancedRAGService()
