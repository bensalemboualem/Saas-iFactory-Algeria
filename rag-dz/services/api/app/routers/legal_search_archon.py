"""
IA Factory - Legal Search API for Archon
Endpoint pour recherche hybride dans les documents juridiques (DZ/CH/FR)
"""

import os
import logging
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
import httpx

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/legal", tags=["Legal Search"])

# Configuration Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "http://supabase-kong:8000")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", os.getenv("SUPABASE_SERVICE_KEY", ""))


class SearchRequest(BaseModel):
    """Requete de recherche juridique"""
    query: str = Field(..., min_length=2, description="Texte de recherche")
    jurisdiction: Optional[str] = Field(None, description="Filtrer par juridiction (DZ, CH, FR)")
    source_id: Optional[str] = Field(None, description="Filtrer par source")
    limit: int = Field(10, ge=1, le=50, description="Nombre de resultats")
    vector_weight: float = Field(0.3, ge=0, le=1, description="Poids recherche vectorielle")
    keyword_weight: float = Field(0.7, ge=0, le=1, description="Poids recherche mots-cles")
    rerank: bool = Field(True, description="Activer le re-ranking Cohere")
    min_relevance: float = Field(0.3, ge=0, le=1, description="Seuil minimum de pertinence")


class SearchResult(BaseModel):
    """Resultat de recherche"""
    article_number: Optional[str] = None
    source_title: str
    content: str
    context_prefix: str = ""
    score: float
    relevance_score: Optional[float] = None  # Score de pertinence (0-1) si reranké
    match_type: str  # "keyword", "vector", "hybrid", "reranked"


class SearchMetadata(BaseModel):
    """Métadonnées de la recherche"""
    original_count: int = 0
    reranked: bool = False
    processing_time_ms: float = 0
    avg_relevance: float = 0
    reranker_enabled: bool = False


class SearchResponse(BaseModel):
    """Reponse de recherche"""
    query: str
    total_results: int
    results: List[SearchResult]
    metadata: Optional[SearchMetadata] = None


class LegalSource(BaseModel):
    """Source juridique"""
    id: str
    code: str
    title: str
    jurisdiction: str
    legal_type: str
    is_active: bool = True


@router.post("/search", response_model=SearchResponse)
async def search_legal_documents(request: SearchRequest):
    """
    Recherche hybride dans les documents juridiques.

    Combine recherche vectorielle (semantique) et BM25 (mots-cles)
    avec ponderation configurable (defaut: 70% mots-cles, 30% vecteurs).

    Si rerank=True, applique un re-ranking Cohere pour améliorer la pertinence.
    """
    import time
    start_time = time.time()

    logger.info(f"Legal search: '{request.query}' jurisdiction={request.jurisdiction} rerank={request.rerank}")

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Utiliser la fonction RPC de Supabase
            # Récupérer plus de résultats si reranking activé
            fetch_limit = request.limit * 3 if request.rerank else request.limit

            response = await client.post(
                f"{SUPABASE_URL}/rest/v1/rpc/search_legal_bm25",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "search_query": request.query,
                    "jurisdiction_filter": request.jurisdiction,
                    "result_limit": fetch_limit
                }
            )

            if response.status_code == 404:
                logger.warning("RPC function not found, using fallback search")
                return await _fallback_search(request)

            response.raise_for_status()
            raw_results = response.json()
            original_count = len(raw_results)

            # Appliquer le re-ranking si activé
            if request.rerank and raw_results:
                reranked_results, metadata = await _apply_reranking(
                    request.query,
                    raw_results,
                    request.limit,
                    request.min_relevance
                )

                elapsed = (time.time() - start_time) * 1000

                return SearchResponse(
                    query=request.query,
                    total_results=len(reranked_results),
                    results=reranked_results,
                    metadata=SearchMetadata(
                        original_count=original_count,
                        reranked=True,
                        processing_time_ms=round(elapsed, 2),
                        avg_relevance=metadata.get("avg_relevance", 0),
                        reranker_enabled=metadata.get("reranker_enabled", False)
                    )
                )

            # Sans re-ranking
            elapsed = (time.time() - start_time) * 1000

            return SearchResponse(
                query=request.query,
                total_results=len(raw_results),
                results=[
                    SearchResult(
                        article_number=r.get("article_number"),
                        source_title=r.get("source_title", ""),
                        content=r.get("content", ""),
                        context_prefix=r.get("context_prefix", ""),
                        score=r.get("score", 0),
                        relevance_score=None,
                        match_type="keyword"
                    )
                    for r in raw_results[:request.limit]
                ],
                metadata=SearchMetadata(
                    original_count=original_count,
                    reranked=False,
                    processing_time_ms=round(elapsed, 2)
                )
            )

    except httpx.HTTPError as e:
        logger.error(f"HTTP error in legal search: {e}")
        return await _fallback_search(request)


async def _apply_reranking(
    query: str,
    documents: List[dict],
    top_n: int,
    min_relevance: float
) -> tuple:
    """Applique le re-ranking Cohere aux résultats"""
    try:
        from ..services.reranker import search_enhancer

        reranked, metadata = await search_enhancer.enhanced_search(
            query=query,
            raw_results=documents,
            top_n=top_n,
            min_relevance=min_relevance
        )

        results = [
            SearchResult(
                article_number=r.article_number,
                source_title=r.source_title,
                content=r.content,
                context_prefix=r.context_prefix,
                score=r.original_score,
                relevance_score=round(r.relevance_score, 4),
                match_type="reranked"
            )
            for r in reranked
        ]

        return results, metadata

    except ImportError:
        logger.warning("Reranker module not available, skipping")
        # Fallback sans reranking
        results = [
            SearchResult(
                article_number=d.get("article_number"),
                source_title=d.get("source_title", ""),
                content=d.get("content", ""),
                context_prefix=d.get("context_prefix", ""),
                score=d.get("score", 0),
                relevance_score=None,
                match_type="keyword"
            )
            for d in documents[:top_n]
        ]
        return results, {"reranker_enabled": False}


async def _fallback_search(request: SearchRequest) -> SearchResponse:
    """Recherche de secours via REST API simple (ilike)"""
    import time
    start_time = time.time()

    logger.info(f"Fallback search for: {request.query}")

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{SUPABASE_URL}/rest/v1/document_chunks",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
            },
            params={
                "select": "content,context_prefix,legal_documents(article_number),legal_sources(title)",
                "content": f"ilike.*{request.query}*",
                "limit": str(request.limit)
            }
        )

        if response.status_code != 200:
            logger.error(f"Fallback search failed: {response.status_code}")
            raise HTTPException(status_code=500, detail="Search failed")

        results = response.json()
        elapsed = (time.time() - start_time) * 1000

        return SearchResponse(
            query=request.query,
            total_results=len(results),
            results=[
                SearchResult(
                    article_number=r.get("legal_documents", {}).get("article_number") if r.get("legal_documents") else None,
                    source_title=r.get("legal_sources", {}).get("title", "") if r.get("legal_sources") else "",
                    content=r.get("content", ""),
                    context_prefix=r.get("context_prefix", ""),
                    score=1.0,
                    relevance_score=None,
                    match_type="fallback"
                )
                for r in results
            ],
            metadata=SearchMetadata(
                original_count=len(results),
                reranked=False,
                processing_time_ms=round(elapsed, 2)
            )
        )


@router.get("/sources", response_model=List[LegalSource])
async def list_legal_sources():
    """Liste toutes les sources juridiques disponibles"""
    logger.info("Fetching legal sources")

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{SUPABASE_URL}/rest/v1/legal_sources",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
            },
            params={
                "select": "id,code,title,jurisdiction,legal_type,is_active",
                "is_active": "eq.true"
            }
        )

        if response.status_code != 200:
            logger.error(f"Failed to fetch sources: {response.status_code}")
            raise HTTPException(status_code=500, detail="Failed to fetch sources")

        return response.json()


@router.get("/stats")
async def get_search_stats():
    """Statistiques du systeme de recherche juridique"""
    logger.info("Fetching legal search stats")

    async with httpx.AsyncClient(timeout=30.0) as client:
        # Compter les sources
        sources_resp = await client.get(
            f"{SUPABASE_URL}/rest/v1/legal_sources",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Prefer": "count=exact"
            },
            params={"select": "id"}
        )

        # Compter les documents
        docs_resp = await client.get(
            f"{SUPABASE_URL}/rest/v1/legal_documents",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Prefer": "count=exact"
            },
            params={"select": "id"}
        )

        # Compter les chunks
        chunks_resp = await client.get(
            f"{SUPABASE_URL}/rest/v1/document_chunks",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Prefer": "count=exact"
            },
            params={"select": "id"}
        )

        return {
            "sources_count": len(sources_resp.json()) if sources_resp.status_code == 200 else 0,
            "documents_count": len(docs_resp.json()) if docs_resp.status_code == 200 else 0,
            "chunks_count": len(chunks_resp.json()) if chunks_resp.status_code == 200 else 0,
            "search_modes": ["keyword_bm25", "vector_similarity", "hybrid_rrf"],
            "supported_jurisdictions": ["DZ", "CH", "FR"]
        }


@router.get("/article/{article_number}")
async def get_article(article_number: str, jurisdiction: Optional[str] = None):
    """Recupere un article specifique par son numero"""
    logger.info(f"Fetching article: {article_number}")

    async with httpx.AsyncClient(timeout=30.0) as client:
        params = {
            "select": "*,legal_sources(code,title,jurisdiction)",
            "article_number": f"eq.{article_number}"
        }

        response = await client.get(
            f"{SUPABASE_URL}/rest/v1/legal_documents",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
            },
            params=params
        )

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch article")

        results = response.json()
        if not results:
            raise HTTPException(status_code=404, detail=f"Article {article_number} not found")

        # Filtrer par juridiction si specifie
        if jurisdiction:
            results = [r for r in results if r.get("legal_sources", {}).get("jurisdiction") == jurisdiction]

        if not results:
            raise HTTPException(status_code=404, detail=f"Article {article_number} not found for jurisdiction {jurisdiction}")

        return results[0] if len(results) == 1 else results
