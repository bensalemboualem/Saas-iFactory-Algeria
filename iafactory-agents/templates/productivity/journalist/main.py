# main.py - FastAPI wrapper for the Journalist Service

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn
import logging
from typing import Dict, Any

from journalist_service import JournalistService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- FastAPI App Initialization ---
app = FastAPI(
    title="AI Journalist Agent API",
    version="1.0.0",
    description="An API to generate high-quality articles using an AI Journalist agent.",
)


# --- Pydantic Models ---
class ArticleGenerationRequest(BaseModel):
    openai_api_key: str = Field(..., description="Your OpenAI API Key.")
    serp_api_key: str = Field(..., description="Your SerpAPI Key.")
    topic: str = Field(..., example="The impact of AI on employment", description="The topic for the article.")

class ArticleGenerationResponse(BaseModel):
    success: bool
    article: str | None = None
    error: str | None = None


# --- API Endpoints ---
@app.post("/generate-article", response_model=ArticleGenerationResponse)
async def generate_article_api(request: ArticleGenerationRequest):
    """
    Generates a high-quality article on a given topic using the AI Journalist Agent.
    """
    logger.info(f"API: Received article generation request for topic: '{request.topic}'")
    try:
        # Note: The service's core .run() method is synchronous.
        # For a high-concurrency server, you might run this in a thread pool.
        service = JournalistService(
            openai_api_key=request.openai_api_key,
            serp_api_key=request.serp_api_key
        )
        result = service.generate_article(request.topic)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result.get("error", "Unknown article generation error"))
            
        return ArticleGenerationResponse(
            success=True,
            article=result.get("article"),
        )
        
    except ValueError as e:
        # For invalid API keys from JournalistService init
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"API: Unhandled exception during article generation: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

@app.get("/", summary="Root", description="Root endpoint to check if the API is running.")
async def root():
    return {"message": "AI Journalist Agent API is running."}


# --- Entrypoint for direct execution ---
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
