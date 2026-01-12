"""
IAFactory Memory API - User Memory Management
==============================================
Endpoints pour gerer la memoire persistante des utilisateurs:
- Profil, preferences, business, faits, objectifs
- Extraction automatique depuis conversations
- Recherche semantique

Endpoints:
- GET  /api/memory/                - Liste memoires utilisateur
- GET  /api/memory/context         - Contexte pour IA
- GET  /api/memory/stats           - Statistiques memoire
- GET  /api/memory/{id}            - Detail memoire
- POST /api/memory/                - Creer memoire explicite
- PUT  /api/memory/{id}            - Modifier memoire
- DELETE /api/memory/{id}          - Supprimer memoire
- POST /api/memory/search          - Recherche semantique
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Optional, List
from pydantic import BaseModel, Field
import logging

from app.dependencies import get_current_active_user
from app.models.user import UserInDB
from app.models.memory_models import (
    MemoryCategory, MemorySource,
    UserMemory, UserMemoryCreate, UserMemoryUpdate,
    MemoryContext, GetMemoriesResponse, MemoryStatsResponse,
    SemanticSearchRequest, SemanticSearchResponse
)
from app.services.memory_service import get_memory_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/memory", tags=["memory"])


# ============================================
# Request/Response Schemas
# ============================================

class CreateMemoryRequest(BaseModel):
    """Request creation memoire explicite"""
    category: MemoryCategory
    key: str = Field(..., max_length=100, description="Cle unique dans la categorie")
    value: str = Field(..., description="Valeur de la memoire")
    confidence: float = Field(default=1.0, ge=0, le=1, description="Niveau de confiance (1.0 pour explicite)")


class UpdateMemoryRequest(BaseModel):
    """Request mise a jour memoire"""
    value: str = Field(..., description="Nouvelle valeur")
    reason: Optional[str] = Field(None, description="Raison de la modification")


class DeleteMemoryResponse(BaseModel):
    """Response suppression"""
    success: bool
    message: str


class MemoryListResponse(BaseModel):
    """Response liste memoires"""
    memories: List[UserMemory]
    by_category: dict
    total: int


# ============================================
# Endpoints
# ============================================

@router.get(
    "/",
    response_model=MemoryListResponse,
    summary="Liste memoires utilisateur",
    description="Recupere toutes les memoires de l'utilisateur, optionnellement filtrees par categorie"
)
async def list_memories(
    category: Optional[MemoryCategory] = Query(None, description="Filtrer par categorie"),
    include_inactive: bool = Query(False, description="Inclure les memoires desactivees"),
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Liste toutes les memoires de l'utilisateur"""
    service = get_memory_service()

    memories = await service.get_memories(
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
        category=category,
        is_active=not include_inactive
    )

    # Grouper par categorie
    by_category = {}
    for mem in memories:
        cat = mem.category.value
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(mem)

    return MemoryListResponse(
        memories=memories,
        by_category=by_category,
        total=len(memories)
    )


@router.get(
    "/context",
    response_model=MemoryContext,
    summary="Contexte memoire pour IA",
    description="Recupere le contexte memoire formate pour injection dans prompts IA"
)
async def get_memory_context(
    include_recent_topics: bool = Query(True, description="Inclure sujets recents"),
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Recupere le contexte memoire pour l'IA"""
    service = get_memory_service()

    context = await service.get_memory_context(
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
        include_recent_topics=include_recent_topics
    )

    return context


@router.get(
    "/stats",
    response_model=MemoryStatsResponse,
    summary="Statistiques memoire",
    description="Statistiques sur les memoires et conversations de l'utilisateur"
)
async def get_memory_stats(
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Statistiques memoire utilisateur"""
    service = get_memory_service()

    stats = await service.get_memory_stats(
        tenant_id=current_user.tenant_id,
        user_id=current_user.id
    )

    return stats


@router.get(
    "/{memory_id}",
    response_model=UserMemory,
    summary="Detail memoire",
    description="Recupere une memoire specifique par ID"
)
async def get_memory(
    memory_id: str,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Detail d'une memoire"""
    service = get_memory_service()

    memories = await service.get_memories(
        tenant_id=current_user.tenant_id,
        user_id=current_user.id
    )

    # Find by ID
    for mem in memories:
        if mem.id == memory_id:
            return mem

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Memoire non trouvee"
    )


@router.post(
    "/",
    response_model=UserMemory,
    status_code=status.HTTP_201_CREATED,
    summary="Creer memoire",
    description="Cree une memoire explicite (definie par l'utilisateur)"
)
async def create_memory(
    request: CreateMemoryRequest,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Cree une nouvelle memoire explicite"""
    service = get_memory_service()

    memory_data = UserMemoryCreate(
        category=request.category,
        key=request.key,
        value=request.value,
        confidence=request.confidence,
        source=MemorySource.EXPLICIT
    )

    memory = await service.upsert_memory(
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
        memory=memory_data
    )

    logger.info(f"Memory created: {request.category}/{request.key} for user {current_user.id}")

    return memory


@router.put(
    "/{memory_id}",
    response_model=UserMemory,
    summary="Modifier memoire",
    description="Modifie une memoire existante (avec tracking des corrections)"
)
async def update_memory(
    memory_id: str,
    request: UpdateMemoryRequest,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Modifie une memoire"""
    service = get_memory_service()

    updates = UserMemoryUpdate(value=request.value)

    memory = await service.update_memory(
        memory_id=memory_id,
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
        updates=updates,
        reason=request.reason
    )

    if not memory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memoire non trouvee"
        )

    logger.info(f"Memory updated: {memory_id} for user {current_user.id}")

    return memory


@router.delete(
    "/{memory_id}",
    response_model=DeleteMemoryResponse,
    summary="Supprimer memoire",
    description="Desactive une memoire (soft delete)"
)
async def delete_memory(
    memory_id: str,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Supprime une memoire"""
    service = get_memory_service()

    deleted = await service.delete_memory(
        memory_id=memory_id,
        tenant_id=current_user.tenant_id,
        user_id=current_user.id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memoire non trouvee"
        )

    logger.info(f"Memory deleted: {memory_id} for user {current_user.id}")

    return DeleteMemoryResponse(
        success=True,
        message="Memoire supprimee"
    )


@router.post(
    "/search",
    response_model=SemanticSearchResponse,
    summary="Recherche semantique",
    description="Recherche dans les memoires et messages par similarite semantique"
)
async def search_memories(
    request: SemanticSearchRequest,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Recherche semantique dans memoires et messages"""
    service = get_memory_service()

    results = await service.semantic_search(
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
        query=request.query,
        search_type=request.search_type,
        limit=request.limit,
        min_similarity=request.min_similarity
    )

    return results


# ============================================
# Bulk Operations
# ============================================

class BulkCreateRequest(BaseModel):
    """Requete creation multiple"""
    memories: List[CreateMemoryRequest]


class BulkCreateResponse(BaseModel):
    """Response creation multiple"""
    created: int
    failed: int
    memories: List[UserMemory]


@router.post(
    "/bulk",
    response_model=BulkCreateResponse,
    summary="Creation multiple",
    description="Cree plusieurs memoires en une seule requete"
)
async def bulk_create_memories(
    request: BulkCreateRequest,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Cree plusieurs memoires"""
    service = get_memory_service()

    created_memories = []
    failed = 0

    for mem_request in request.memories:
        try:
            memory_data = UserMemoryCreate(
                category=mem_request.category,
                key=mem_request.key,
                value=mem_request.value,
                confidence=mem_request.confidence,
                source=MemorySource.EXPLICIT
            )

            memory = await service.upsert_memory(
                tenant_id=current_user.tenant_id,
                user_id=current_user.id,
                memory=memory_data
            )
            created_memories.append(memory)
        except Exception as e:
            logger.warning(f"Failed to create memory: {e}")
            failed += 1

    return BulkCreateResponse(
        created=len(created_memories),
        failed=failed,
        memories=created_memories
    )


# ============================================
# Export/Import
# ============================================

class ExportResponse(BaseModel):
    """Export memoires"""
    export_date: str
    user_id: str
    total_memories: int
    memories: List[dict]


@router.get(
    "/export",
    response_model=ExportResponse,
    summary="Exporter memoires",
    description="Exporte toutes les memoires utilisateur en JSON"
)
async def export_memories(
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Exporte les memoires utilisateur"""
    from datetime import datetime

    service = get_memory_service()

    memories = await service.get_memories(
        tenant_id=current_user.tenant_id,
        user_id=current_user.id
    )

    export_data = [
        {
            "category": m.category.value,
            "key": m.key,
            "value": m.value,
            "confidence": m.confidence,
            "source": m.source.value,
            "created_at": m.created_at.isoformat()
        }
        for m in memories
    ]

    return ExportResponse(
        export_date=datetime.utcnow().isoformat(),
        user_id=current_user.id,
        total_memories=len(export_data),
        memories=export_data
    )
