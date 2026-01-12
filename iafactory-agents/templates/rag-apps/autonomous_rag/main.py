# main.py - FastAPI wrapper for the AutoRAG Service

import asyncio
from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn
import logging
from typing import Dict, Any, List, Optional

from autorag_service import AutoRagService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- FastAPI App Initialization ---
app = FastAPI(
    title="AutoRAG Agent API",
    version="1.0.0",
    description="An API to Autonomous RAG with GPT-4o and PgVector database.",
)


# --- Pydantic Models ---
class BaseAPIRequest(BaseModel):
    openai_api_key: str = Field(..., description="Your OpenAI API Key.")
    db_url: str = Field(..., example="postgresql+psycopg://user:pass@host:port/db", description="PostgreSQL connection string for PgVector.")

class ChatRequest(BaseAPIRequest):
    question: str = Field(..., example="What is autonomous RAG?", description="The question to ask the RAG agent.")

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
    openai_api_key: str = Form(..., description="Your OpenAI API Key."),
    db_url: str = Form(..., example="postgresql+psycopg://user:pass@host:port/db", description="PostgreSQL connection string for PgVector."),
    file: UploadFile = File(..., description="PDF document to upload.")
):
    """
    Uploads a PDF document to the RAG agent's knowledge base.
    """
    logger.info(f"API: Received PDF upload request for file: '{file.filename}'")
    try:
        service = AutoRagService(
            openai_api_key=openai_api_key,
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
    Asks a question to the RAG agent and retrieves the answer.
    """
    logger.info(f"API: Received chat request: '{request.question[:50]}...'")
    try:
        service = AutoRagService(
            openai_api_key=request.openai_api_key,
            db_url=request.db_url
        )
        result = service.query_assistant(request.question)
        
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
    return {"message": "AutoRAG Agent API is running."}


# --- Entrypoint for direct execution ---
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
