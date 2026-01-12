"""
RAG API Endpoints
Handles document ingestion, search, and chat for BBC School IA Program
"""

from typing import Optional, List
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query
from pydantic import BaseModel, Field

from app.services.rag import get_rag_service


router = APIRouter(prefix="/rag", tags=["RAG"])


# ============================================
# Request/Response Models
# ============================================

class ChatRequest(BaseModel):
    """Request for chat endpoint"""
    question: str = Field(..., min_length=3, max_length=1000)
    language: str = Field(default="fr", pattern="^(fr|ar|en)$")
    n_results: int = Field(default=5, ge=1, le=20)
    filter_level: Optional[str] = Field(default=None)
    filter_module: Optional[str] = Field(default=None)
    chat_history: Optional[List[dict]] = Field(default=None)


class ChatResponse(BaseModel):
    """Response from chat endpoint"""
    answer: str
    sources: List[dict]
    query: str
    timestamp: str
    processing_time_ms: float


class SearchRequest(BaseModel):
    """Request for search endpoint"""
    query: str = Field(..., min_length=2, max_length=500)
    language: str = Field(default="fr", pattern="^(fr|ar|en)$")
    n_results: int = Field(default=10, ge=1, le=50)
    filter_type: Optional[str] = Field(default=None)


class SearchResult(BaseModel):
    """Search result item"""
    content: str
    metadata: dict
    score: float


class IngestionResponse(BaseModel):
    """Response from ingestion endpoint"""
    success: bool
    document_count: int
    chunk_count: int
    collection: str
    errors: List[str]
    processing_time_ms: float


class StatsResponse(BaseModel):
    """System statistics response"""
    collections: dict
    embedding_model: str
    llm_provider: str
    llm_model: str


class ValidationResponse(BaseModel):
    """Validation test results"""
    total_tests: int
    passed: int
    failed: int
    success_rate: str
    results: List[dict]


# ============================================
# Endpoints
# ============================================

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with the RAG system

    Ask questions about the BBC School IA Program and get answers
    with citations from the knowledge base.
    """
    try:
        rag_service = get_rag_service()
        response = rag_service.query(
            question=request.question,
            language=request.language,
            n_results=request.n_results,
            filter_level=request.filter_level,
            filter_module=request.filter_module,
            chat_history=request.chat_history
        )

        return ChatResponse(
            answer=response.answer,
            sources=response.sources,
            query=response.query,
            timestamp=response.timestamp,
            processing_time_ms=response.processing_time_ms or 0
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search", response_model=List[SearchResult])
async def search(request: SearchRequest):
    """
    Search the knowledge base without generating a response

    Useful for browsing and exploring the content.
    """
    try:
        rag_service = get_rag_service()
        results = rag_service.search_only(
            query=request.query,
            language=request.language,
            n_results=request.n_results,
            filter_type=request.filter_type
        )

        return [
            SearchResult(
                content=r.content,
                metadata=r.metadata,
                score=r.score
            )
            for r in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ingest", response_model=IngestionResponse)
async def ingest_file(
    file: UploadFile = File(...),
    collection_name: Optional[str] = Form(default=None),
    file_type: str = Form(default="auto")
):
    """
    Ingest a document into the knowledge base

    Supports HTML, Markdown, and JSON files.
    Files are automatically chunked and embedded.
    """
    try:
        # Read file content
        content = await file.read()
        content_str = content.decode("utf-8")

        rag_service = get_rag_service()
        result = rag_service.ingest_file(
            file_content=content_str,
            file_name=file.filename or "document",
            file_type=file_type,
            collection_name=collection_name
        )

        return IngestionResponse(
            success=result.success,
            document_count=result.document_count,
            chunk_count=result.chunk_count,
            collection=result.collection,
            errors=result.errors,
            processing_time_ms=result.processing_time_ms
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ingest-text", response_model=IngestionResponse)
async def ingest_text(
    content: str = Form(...),
    file_name: str = Form(...),
    file_type: str = Form(default="auto"),
    collection_name: Optional[str] = Form(default=None)
):
    """
    Ingest text content directly (without file upload)

    Useful for pasting content directly.
    """
    try:
        rag_service = get_rag_service()
        result = rag_service.ingest_file(
            file_content=content,
            file_name=file_name,
            file_type=file_type,
            collection_name=collection_name
        )

        return IngestionResponse(
            success=result.success,
            document_count=result.document_count,
            chunk_count=result.chunk_count,
            collection=result.collection,
            errors=result.errors,
            processing_time_ms=result.processing_time_ms
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    """
    Get statistics about the RAG system

    Returns collection counts, models in use, etc.
    """
    try:
        rag_service = get_rag_service()
        stats = rag_service.get_stats()

        return StatsResponse(
            collections=stats["collections"],
            embedding_model=stats["embedding_model"],
            llm_provider=stats["llm_provider"],
            llm_model=stats["llm_model"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/validate", response_model=ValidationResponse)
async def validate_knowledge_base():
    """
    Run validation tests on the knowledge base

    Tests predefined queries to ensure the RAG system
    can answer expected questions correctly.
    """
    try:
        rag_service = get_rag_service()
        results = rag_service.validate_knowledge_base()

        return ValidationResponse(
            total_tests=results["total_tests"],
            passed=results["passed"],
            failed=results["failed"],
            success_rate=results["success_rate"],
            results=results["results"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/collections")
async def list_collections():
    """List all available collections"""
    try:
        rag_service = get_rag_service()
        return rag_service.vector_store.get_all_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/collections/{collection_name}")
async def delete_collection(collection_name: str):
    """Delete a collection (use with caution!)"""
    try:
        rag_service = get_rag_service()
        success = rag_service.vector_store.delete_collection(collection_name)

        if success:
            return {"message": f"Collection {collection_name} deleted"}
        else:
            raise HTTPException(status_code=404, detail="Collection not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
