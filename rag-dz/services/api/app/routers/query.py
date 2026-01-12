from fastapi import APIRouter, Request, Query
from pydantic import BaseModel, Field
import time
from typing import Optional

from ..clients.embeddings import embed_queries
from ..clients.qdrant_client import client as qdrant_client
from ..clients.cloud_llm import llm_client
from ..pagination import PaginationParams, PaginatedResponse
from ..cache import query_cache
from ..config import get_settings

settings = get_settings()

router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    max_results: int = Field(default=5, ge=1, le=50, description="Nombre max de résultats")
    score_threshold: float = Field(default=0.3, ge=0.0, le=1.0, description="Score minimum")
    use_cache: bool = Field(default=True, description="Utiliser le cache")

@router.post("/query")
async def search_documents(request: QueryRequest, req: Request):
    """
    Recherche sémantique dans les documents avec cache
    """
    tenant = req.state.tenant
    collection_name = f"docs_{tenant['id']}"

    # Vérifier le cache
    if request.use_cache:
        cached_result = query_cache.get_query_result(
            query=request.query,
            collection=collection_name
        )
        if cached_result:
            cached_result["from_cache"] = True
            return cached_result

    start_time = time.time()

    try:
        # Générer embedding de la question (avec cache)
        query_embedding = embed_queries([request.query], use_cache=request.use_cache)[0]

        # Recherche vectorielle
        search_results = qdrant_client.search(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=request.max_results,
            score_threshold=request.score_threshold
        )
    except Exception as e:
        # Fallback si collection n'existe pas
        search_results = []

    # Formatage résultats
    results = []
    for result in search_results:
        results.append({
            "id": str(result.id),
            "title": result.payload.get("title", ""),
            "text": result.payload.get("text", "")[:300],
            "language": result.payload.get("language", "fr"),
            "score": round(result.score, 4),
            "created_at": result.payload.get("created_at")
        })

    # Génération réponse avec LLM cloud si disponible
    if results:
        if settings.enable_llm and llm_client.is_available():
            # Détection de langue basique
            language = "ar" if any(ord(c) > 1536 and ord(c) < 1792 for c in request.query) else "fr"
            answer = llm_client.generate_rag_answer(
                query=request.query,
                context_chunks=results,
                language=language
            )
        else:
            # Fallback basique
            context = results[0]["text"]
            answer = f"Basé sur les documents trouvés : {context[:200]}..."
    else:
        answer = "Aucun document pertinent trouvé dans la base de connaissances."

    search_time = (time.time() - start_time) * 1000

    response = {
        "answer": answer,
        "results": results,
        "query": request.query,
        "search_time_ms": int(search_time),
        "total_results": len(results),
        "from_cache": False
    }

    # Stocker dans le cache
    if request.use_cache and len(results) > 0:
        query_cache.set_query_result(
            query=request.query,
            collection=collection_name,
            result=response
        )

    return response


class SearchResult(BaseModel):
    """Modèle pour un résultat de recherche"""
    id: str
    title: str
    text: str
    language: str
    score: float
    created_at: Optional[int] = None


@router.get("/search")
async def search_with_pagination(
    query: str = Query(..., min_length=1, description="Texte de recherche"),
    req: Request = None,
    pagination: PaginationParams = None
):
    """
    Recherche paginée dans les documents

    Args:
        query: Texte de recherche
        pagination: Paramètres de pagination

    Returns:
        Résultats paginés
    """
    if pagination is None:
        pagination = PaginationParams()

    tenant = req.state.tenant
    collection_name = f"docs_{tenant['id']}"

    try:
        # Embedding de la query
        query_embedding = embed_queries([query], use_cache=True)[0]

        # Recherche avec limite élargie pour pagination
        total_limit = pagination.page * pagination.page_size
        search_results = qdrant_client.search(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=total_limit,
            score_threshold=0.2
        )

        # Convertir en SearchResult
        all_results = [
            SearchResult(
                id=str(r.id),
                title=r.payload.get("title", ""),
                text=r.payload.get("text", "")[:300],
                language=r.payload.get("language", "fr"),
                score=round(r.score, 4),
                created_at=r.payload.get("created_at")
            )
            for r in search_results
        ]

        # Pagination
        start = pagination.offset
        end = start + pagination.page_size
        paginated_results = all_results[start:end]

        return PaginatedResponse.create(
            items=paginated_results,
            total_items=len(all_results),
            params=pagination
        )

    except Exception as e:
        # Retour vide en cas d'erreur
        return PaginatedResponse.create(
            items=[],
            total_items=0,
            params=pagination
        )
