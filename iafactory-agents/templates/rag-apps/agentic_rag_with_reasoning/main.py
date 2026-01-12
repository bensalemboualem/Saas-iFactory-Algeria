# main.py - FastAPI wrapper for the Rag Reasoning Service

import asyncio
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn
import logging
from typing import Dict, Any, List, Optional

from rag_reasoning_service import RagReasoningService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Agentic RAG with Reasoning API",
    version="1.0.0",
    description="An API to perform RAG with step-by-step reasoning using Agno, Gemini, and OpenAI embeddings.",
)


# --- Pydantic Models ---
class BaseAPIRequest(BaseModel):
    google_api_key: str = Field(..., description="Your Google Gemini API Key.")
    openai_api_key: str = Field(..., description="Your OpenAI API Key for embeddings.")

class AddKnowledgeRequest(BaseAPIRequest):
    url: str = Field(..., example="https://www.example.com/article", description="URL to add to the knowledge base.")

class AddKnowledgeResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    error: Optional[str] = None

class RagQuestionRequest(BaseAPIRequest):
    query: str = Field(..., example="What is the difference between X and Y?", description="The question to ask the RAG agent.")

class RagAnswerResponse(BaseModel):
    success: bool
    reasoning: Optional[str] = None
    answer: Optional[str] = None
    citations: Optional[List[Dict[str, str]]] = None
    error: Optional[str] = None


# --- API Endpoints ---
@app.post("/add-knowledge", response_model=AddKnowledgeResponse)
async def add_knowledge_source_api(request: AddKnowledgeRequest):
    """
    Adds a URL to the agent's knowledge base.
    """
    logger.info(f"API: Received request to add knowledge source: '{request.url}'")
    try:
        service = RagReasoningService(
            google_api_key=request.google_api_key,
            openai_api_key=request.openai_api_key
        )
        result = service.add_knowledge_source(request.url)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result.get("error", "Failed to add knowledge source"))
            
        return AddKnowledgeResponse(
            success=True,
            message=result.get("message", "Knowledge source added successfully."),
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"API: Unhandled exception when adding knowledge: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")


@app.post("/answer", response_model=RagAnswerResponse)
async def answer_question_api(request: RagQuestionRequest):
    """
    Asks a question to the RAG agent and retrieves the answer with reasoning.
    """
    logger.info(f"API: Received question for RAG agent: '{request.query[:50]}...'")
    try:
        service = RagReasoningService(
            google_api_key=request.google_api_key,
            openai_api_key=request.openai_api_key
        )
        result = service.answer_question(request.query)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result.get("error", "Failed to get answer"))
            
        return RagAnswerResponse(
            success=True,
            reasoning=result.get("reasoning"),
            answer=result.get("answer"),
            citations=result.get("citations"),
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"API: Unhandled exception when answering question: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")


@app.get("/", summary="Root", description="Root endpoint to check if the API is running.")
async def root():
    return {"message": "Agentic RAG with Reasoning API is running."}


# --- Entrypoint for direct execution ---
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
