# main_fastapi.py - FastAPI wrapper for the Hybrid RAG Service

import asyncio
from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn
import logging
from typing import Dict, Any, List, Optional

from hybrid_rag_service import HybridRagService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Hybrid Search RAG API",
    version="1.0.0",
    description="An API for Hybrid Search RAG with Claude, OpenAI embeddings, and Cohere reranking.",
)


# --- Pydantic Models ---
class BaseAPIRequest(BaseModel):
    openai_key: str = Field(..., description="Your OpenAI API Key for embeddings.")
    anthropic_key: str = Field(..., description="Your Anthropic API Key for Claude LLM.")
    cohere_key: str = Field(..., description="Your Cohere API Key for reranking.")
    db_url: str = Field(..., example="postgresql://user:pass@host:port/db", description="PostgreSQL connection string for RAGLite.")

class ChatRequest(BaseAPIRequest):
    question: str = Field(..., example="What is hybrid search RAG?", description="The question to ask the RAG agent.")

class ChatResponse(BaseModel):
    success: bool
    answer: str | None = None
    citations: Optional[List[Dict[str, str]]] = None
    error: str | None = None

class UploadPDFResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    error: Optional[str] = None


# --- API Endpoints ---
@app.post("/upload-pdf", response_model=UploadPDFResponse)
async def upload_pdf_api(
    openai_key: str = Form(..., description="Your OpenAI API Key."),
    anthropic_key: str = Form(..., description="Your Anthropic API Key."),
    cohere_key: str = Form(..., description="Your Cohere API Key."),
    db_url: str = Form(..., example="postgresql://user:pass@host:port/db", description="PostgreSQL connection string."),
    file: UploadFile = File(..., description="PDF document to upload.")
):
    """
    Uploads a PDF document to the RAG agent's knowledge base.
    """
    logger.info(f"API: Received PDF upload request for file: '{file.filename}'")
    try:
        service = HybridRagService(
            openai_key=openai_key,
            anthropic_key=anthropic_key,
            cohere_key=cohere_key,
            db_url=db_url
        )
        file_content = await file.read()
        result = service.add_pdf_document(file_content, file.filename)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result.get("error", "Failed to upload PDF"))
            
        return UploadPDFResponse(
            success=True,
            message=result.get("message", "PDF uploaded successfully."),
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"API: Unhandled exception during PDF upload: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")


@app.post("/chat", response_model=ChatResponse)
async def chat_with_rag_agent(request: ChatRequest):
    """
    Asks a question to the Hybrid RAG agent and retrieves the answer.
    """
    logger.info(f"API: Received chat request: '{request.question[:50]}...'")
    try:
        service = HybridRagService(
            openai_key=request.openai_key,
            anthropic_key=request.anthropic_key,
            cohere_key=request.cohere_key,
            db_url=request.db_url
        )
        result = service.answer_question(request.question)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result.get("error", "Failed to get answer"))
            
        return ChatResponse(
            success=True,
            answer=result.get("answer"),
            citations=result.get("citations"),
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"API: Unhandled exception during chat: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")


@app.get("/", summary="Root", description="Root endpoint to check if the API is running.")
async def root():
    return {"message": "Hybrid Search RAG API is running."}


# --- Entrypoint for direct execution ---
if __name__ == "__main__":
    uvicorn.run(
        "main_fastapi:app", # Note the explicit app instance name
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
