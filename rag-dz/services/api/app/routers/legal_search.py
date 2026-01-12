"""
IA Factory - Legal Search API
Endpoint pour recherche hybride dans les documents juridiques
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from typing import List, Optional
import httpx
import os

router = APIRouter(prefix="/search", tags=["Legal Search"])

# Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "http://supabase-kong:8000")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")


class SearchRequest(BaseModel):
    """Requete de recherche juridique"""
    query: str = Field(..., min_length=3, description="Texte de recherche")
    jurisdiction: Optional[str] = Field(None, description="Filtrer par juridiction (DZ, CH, FR)")
    source_id: Optional[str] = Field(None, description="Filtrer par source")
    limit: int = Field(10, ge=1, le=50, description="Nombre de resultats")
    vector_weight: float = Field(0.3, ge=0, le=1, description="Poids recherche vectorielle")
    keyword_weight: float = Field(0.7, ge=0, le=1, description="Poids recherche mots-cles")


class SearchResult(BaseModel):
    """Resultat de recherche"""
    article_number: Optional[str]
    source_title: str
    content: str
    context_prefix: str
    score: float
    match_type: str  # "keyword", "vector", "hybrid"


class SearchResponse(BaseModel):
    """Reponse de recherche"""
    query: str
    total_results: int
    results: List[SearchResult]


@router.post("/legal", response_model=SearchResponse)
async def search_legal_documents(request: SearchRequest):
    """
    Recherche hybride dans les documents juridiques.

    Combine recherche vectorielle (semantique) et BM25 (mots-cles)
    avec ponderation configurable (defaut: 70% mots-cles, 30% vecteurs).
    """

    # Construire la requete SQL pour recherche BM25
    sql_query = f"""
    SELECT
        dc.id,
        dc.content,
        dc.context_prefix,
        ld.article_number,
        ls.title as source_title,
        ts_rank_cd(dc.content_tsv, websearch_to_tsquery('french', $1)) as score
    FROM document_chunks dc
    JOIN legal_documents ld ON dc.document_id = ld.id
    JOIN legal_sources ls ON dc.source_id = ls.id
    WHERE dc.content_tsv @@ websearch_to_tsquery('french', $1)
    {"AND ls.jurisdiction = $2" if request.jurisdiction else ""}
    {"AND dc.source_id = $3" if request.source_id else ""}
    ORDER BY score DESC
    LIMIT $4
    """

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Utiliser la fonction RPC de Supabase pour executer le SQL
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
                    "result_limit": request.limit
                }
            )

            if response.status_code == 404:
                # Fallback: recherche directe via REST API
                return await _fallback_search(request)

            response.raise_for_status()
            results = response.json()

            return SearchResponse(
                query=request.query,
                total_results=len(results),
                results=[
                    SearchResult(
                        article_number=r.get("article_number"),
                        source_title=r.get("source_title", ""),
                        content=r.get("content", ""),
                        context_prefix=r.get("context_prefix", ""),
                        score=r.get("score", 0),
                        match_type="keyword"
                    )
                    for r in results
                ]
            )

    except httpx.HTTPError as e:
        # Fallback en cas d'erreur
        return await _fallback_search(request)


async def _fallback_search(request: SearchRequest) -> SearchResponse:
    """Recherche de secours via REST API simple"""

    async with httpx.AsyncClient(timeout=30.0) as client:
        # Recherche simple par contenu
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
            raise HTTPException(status_code=500, detail="Search failed")

        results = response.json()

        return SearchResponse(
            query=request.query,
            total_results=len(results),
            results=[
                SearchResult(
                    article_number=r.get("legal_documents", {}).get("article_number"),
                    source_title=r.get("legal_sources", {}).get("title", ""),
                    content=r.get("content", ""),
                    context_prefix=r.get("context_prefix", ""),
                    score=1.0,
                    match_type="fallback"
                )
                for r in results
            ]
        )


@router.get("/legal/sources")
async def list_legal_sources():
    """Liste toutes les sources juridiques disponibles"""

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
            raise HTTPException(status_code=500, detail="Failed to fetch sources")

        return response.json()


@router.get("/legal/stats")
async def get_search_stats():
    """Statistiques du systeme de recherche"""

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
            "sources_count": len(sources_resp.json()),
            "documents_count": len(docs_resp.json()),
            "chunks_count": len(chunks_resp.json()),
            "search_modes": ["keyword_bm25", "vector_similarity", "hybrid_rrf"],
            "supported_jurisdictions": ["DZ", "CH", "FR"]
        }
