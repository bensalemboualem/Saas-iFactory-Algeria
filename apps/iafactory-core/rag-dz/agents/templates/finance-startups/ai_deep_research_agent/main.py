# main.py - FastAPI wrapper for the Research Service

import asyncio
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import logging

from research_service import ResearchService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Deep Research Agent API",
    version="1.0.0",
    description="An API to perform deep research on any topic using OpenAI and Firecrawl.",
)


# --- Pydantic Models ---
class ResearchRequest(BaseModel):
    topic: str
    openai_api_key: str
    firecrawl_api_key: str

class ResearchResponse(BaseModel):
    success: bool
    enhanced_report: str | None = None
    initial_report: str | None = None
    error: str | None = None


# --- API Endpoints ---
@app.post("/research", response_model=ResearchResponse)
async def perform_research(request: ResearchRequest):
    """
    Perform deep research on a given topic.
    """
    logger.info(f"API: Received research request for topic: '{request.topic}'")
    try:
        service = ResearchService(
            openai_api_key=request.openai_api_key,
            firecrawl_api_key=request.firecrawl_api_key
        )
        
        results = await service.run_full_research(request.topic)
        
        if not results["success"]:
            raise HTTPException(status_code=500, detail=results.get("error", "Unknown research error"))
            
        return ResearchResponse(
            success=True,
            enhanced_report=results.get("enhanced_report"),
            initial_report=results.get("initial_report"),
        )
        
    except ValueError as e:
        # For invalid API keys from ResearchService init
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"API: Unhandled exception during research: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

@app.get("/", summary="Root", description="Root endpoint to check if the API is running.")
async def root():
    return {"message": "Deep Research Agent API is running."}


# --- Global Exception Handler ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global handler for unhandled exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
        },
    )

# --- Entrypoint for direct execution ---
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
