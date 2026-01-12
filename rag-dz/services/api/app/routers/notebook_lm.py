"""
Notebook LM API Router
Interrogation de documents multi-formats avec IA (RAG)
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import os
import shutil
import sys

# Add notebook-lm backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../apps/notebook-lm/backend'))

try:
    from notebook_lm_service import notebook_lm_service
except ImportError:
    notebook_lm_service = None

router = APIRouter(
    prefix="/api/notebook-lm",
    tags=["notebook-lm"],
    responses={404: {"description": "Not found"}},
)

# Models
class QueryRequest(BaseModel):
    """Requête d'interrogation de documents"""
    question: str = Field(..., description="Question à poser aux documents")
    file_ids: List[str] = Field(..., description="IDs des fichiers à interroger")
    top_k: int = Field(5, description="Nombre de chunks à récupérer", ge=1, le=20)

class QueryResponse(BaseModel):
    """Réponse avec answer et sources"""
    answer: str = Field(..., description="Réponse générée par l'IA")
    sources: List[Dict[str, Any]] = Field(..., description="Sources utilisées")
    context_used: int = Field(..., description="Nombre de chunks utilisés")

class UploadResponse(BaseModel):
    """Réponse après upload"""
    file_id: str = Field(..., description="ID unique du fichier")
    filename: str = Field(..., description="Nom du fichier")
    chunks: int = Field(..., description="Nombre de chunks créés")
    total_chars: int = Field(..., description="Nombre total de caractères")
    indexed_at: str = Field(..., description="Date d'indexation")

# Endpoints
@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload et indexe un document

    **Formats supportés:**
    - PDF (.pdf)
    - Word (.docx, .doc)
    - Texte (.txt, .md)
    - CSV (.csv)
    - Excel (.xlsx)
    - Images avec OCR (.png, .jpg, .jpeg) [TODO]

    **Limite:** 50 MB par fichier

    **Processus:**
    1. Extraction du texte
    2. Découpage en chunks (1000 chars)
    3. Création d'embeddings
    4. Indexation dans FAISS

    **Exemple:**
    ```bash
    curl -X POST "https://api.iafactory.com/api/notebook-lm/upload" \\
      -H "Content-Type: multipart/form-data" \\
      -F "file=@document.pdf"
    ```
    """

    if notebook_lm_service is None:
        raise HTTPException(
            status_code=500,
            detail="Notebook LM service not available"
        )

    # Validate file size (50MB)
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to start

    if file_size > 50 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="File too large (max 50MB)"
        )

    # Validate file type
    allowed_types = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain",
        "text/markdown",
        "text/csv",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "image/png",
        "image/jpeg"
    ]

    if file.content_type not in allowed_types and not file.filename.endswith(('.pdf', '.docx', '.txt', '.md', '.csv', '.xlsx', '.png', '.jpg', '.jpeg')):
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type: {file.content_type}"
        )

    try:
        # Save file temporarily
        upload_dir = "./uploads"
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process and index
        result = await notebook_lm_service.upload_document(
            file_path=file_path,
            filename=file.filename,
            file_type=file.content_type
        )

        return UploadResponse(**result)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )

@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """
    Interroge les documents avec une question

    **Fonctionnalités:**
    - RAG (Retrieval Augmented Generation)
    - Recherche sémantique dans les documents
    - Génération de réponse avec Claude ou GPT-4
    - Citations des sources

    **Exemple:**
    ```json
    {
        "question": "Quels sont les principaux points du contrat?",
        "file_ids": ["abc-123", "def-456"],
        "top_k": 5
    }
    ```

    **Réponse:**
    ```json
    {
        "answer": "Les principaux points sont...",
        "sources": [
            {
                "filename": "contrat.pdf",
                "chunk": 2,
                "file_id": "abc-123"
            }
        ],
        "context_used": 5
    }
    ```
    """

    if notebook_lm_service is None:
        raise HTTPException(
            status_code=500,
            detail="Notebook LM service not available"
        )

    try:
        result = await notebook_lm_service.query_documents(
            question=request.question,
            file_ids=request.file_ids,
            top_k=request.top_k
        )

        return QueryResponse(**result)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error querying documents: {str(e)}"
        )

@router.delete("/document/{file_id}")
async def delete_document(file_id: str):
    """
    Supprime un document et son index

    **Args:**
    - file_id: ID du fichier à supprimer

    **Returns:**
    - Message de confirmation
    """

    if notebook_lm_service is None:
        raise HTTPException(
            status_code=500,
            detail="Notebook LM service not available"
        )

    if file_id in notebook_lm_service.vector_stores:
        del notebook_lm_service.vector_stores[file_id]
        return {"message": "Document deleted successfully", "file_id": file_id}
    else:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

@router.get("/health")
async def health_check():
    """Vérifie le statut du service Notebook LM"""

    has_anthropic = bool(os.getenv("ANTHROPIC_API_KEY"))
    has_openai = bool(os.getenv("OPENAI_API_KEY"))

    return {
        "status": "healthy",
        "service": "notebook-lm",
        "ai_providers": {
            "anthropic": has_anthropic,
            "openai": has_openai
        },
        "embeddings": "OpenAI" if has_openai else "HuggingFace (local)",
        "vector_store": "FAISS"
    }

@router.get("/stats")
async def get_stats():
    """Statistiques du service"""

    if notebook_lm_service is None:
        raise HTTPException(
            status_code=500,
            detail="Notebook LM service not available"
        )

    return {
        "total_documents": len(notebook_lm_service.vector_stores),
        "document_ids": list(notebook_lm_service.vector_stores.keys())
    }
