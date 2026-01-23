# main.py - FastAPI wrapper for the RAG-as-a-Service

import asyncio
from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn
import logging
from typing import Dict, Any, List, Optional, Literal

from rag_as_a_service_service import RagAsAService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- FastAPI App Initialization ---
app = FastAPI(
    title="RAG-as-a-Service API",
    version="1.0.0",
    description="An API to build and deploy a production-ready RAG service using Claude 3.5 Sonnet and Ragie.ai.",
)


# --- Pydantic Models ---
class BaseAPIRequest(BaseModel):
    ragie_api_key: str = Field(..., description="Your Ragie API Key.")
    anthropic_api_key: str = Field(..., description="Your Anthropic API Key for Claude.")

class UploadDocumentRequest(BaseAPIRequest):
    url: str = Field(..., example="https://www.example.com/article", description="URL of the document to upload.")
    name: Optional[str] = Field(None, description="Optional name for the document.")
    mode: Literal["fast", "accurate"] = Field("fast", description="Processing mode for Ragie.ai.")

class UploadDocumentResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class QueryRAGRequest(BaseAPIRequest):
    query: str = Field(..., example="What is RAG-as-a-Service?", description="The question to ask the RAG system.")
    scope: str = Field("tutorial", description="Scope for retrieval from Ragie.ai.")

class QueryRAGResponse(BaseModel):
    success: bool
    answer: Optional[str] = None
    citations: Optional[List[str]] = None # Simplified for now
    error: Optional[str] = None


# --- API Endpoints ---
@app.post("/upload-document", response_model=UploadDocumentResponse)
async def upload_document_api(request: UploadDocumentRequest):
    """
    Uploads a document from a URL to Ragie.ai's knowledge base.
    """
    logger.info(f"API: Received document upload request for URL: '{request.url}'")
    try:
        service = RagAsAService(
            ragie_api_key=request.ragie_api_key,
            anthropic_api_key=request.anthropic_api_key
        )
        result = service.upload_document(
            url=request.url,
            name=request.name,
            mode=request.mode
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result.get("error", "Failed to upload document"))
            
        return UploadDocumentResponse(
            success=True,
            message=result.get("message", "Document uploaded successfully."),
            data=result.get("data")
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"API: Unhandled exception during document upload: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")


@app.post("/query", response_model=QueryRAGResponse)
async def query_rag_system_api(request: QueryRAGRequest):
    """
    Queries the RAG system and retrieves an answer.
    """
    logger.info(f"API: Received RAG query: '{request.query[:50]}...'")
    try:
        service = RagAsAService(
            ragie_api_key=request.ragie_api_key,
            anthropic_api_key=request.anthropic_api_key
        )
        result = service.query_rag(
            query=request.query,
            scope=request.scope
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result.get("error", "Failed to get answer"))
            
        return QueryRAGResponse(
            success=True,
            answer=result.get("answer"),
            citations=result.get("citations"),
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"API: Unhandled exception during RAG query: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")


@app.get("/", summary="Root", description="Root endpoint to check if the API is running.")
async def root():
    return {"message": "RAG-as-a-Service API is running."}


# --- Entrypoint for direct execution ---
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
