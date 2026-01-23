# main.py - FastAPI wrapper for the Local Scraping Service

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn
import logging
from typing import Dict, Any, Literal, Optional

from local_scraping_service import LocalScrapingService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Web Scraping AI Agent API",
    version="1.0.0",
    description="An API to perform AI-powered web scraping using ScrapeGraphAI.",
)


# --- Pydantic Models ---
class LLMConfig(BaseModel):
    model: str = Field(..., example="gpt-4o", description="LLM model to use (e.g., gpt-4o, ollama/llama3.2).")
    api_key: Optional[str] = Field(None, description="API key for the LLM provider (e.g., OpenAI). Not needed for local Ollama.")
    base_url: Optional[str] = Field(None, example="http://localhost:11434", description="Base URL for local LLM (e.g., Ollama).")
    temperature: float = Field(0.0, ge=0.0, le=1.0)
    format: Optional[str] = None # e.g., "json" for Ollama

class ScrapingRequest(BaseModel):
    url: str = Field(..., example="https://www.cnbc.com/id/10000113", description="URL of the website to scrape.")
    user_prompt: str = Field(..., example="Extract the title and a summary of the article.", description="Natural language prompt for data extraction.")
    llm_config: LLMConfig = Field(..., description="Configuration for the LLM to be used for scraping.")

class ScrapingResponse(BaseModel):
    success: bool
    result: Any | None = None
    error: str | None = None


# --- API Endpoints ---
@app.post("/scrape", response_model=ScrapingResponse)
async def perform_scraping(request: ScrapingRequest):
    """
    Performs AI-powered web scraping on a given URL.
    """
    logger.info(f"API: Received scraping request for URL: '{request.url}' with prompt: '{request.user_prompt[:50]}...'")
    try:
        # Construct the full LLM config for SmartScraperGraph
        full_llm_config = {
            "llm": {
                "model": request.llm_config.model,
                "temperature": request.llm_config.temperature,
                **({"api_key": request.llm_config.api_key} if request.llm_config.api_key else {}),
                **({"base_url": request.llm_config.base_url} if request.llm_config.base_url else {}),
                **({"format": request.llm_config.format} if request.llm_config.format else {}),
            }
        }
        # Add embeddings config if it's an Ollama setup
        if "ollama" in request.llm_config.model.lower() and request.llm_config.base_url:
             full_llm_config["embeddings"] = {
                "model": "ollama/nomic-embed-text", # Hardcoded for now
                "base_url": request.llm_config.base_url,
            }

        service = LocalScrapingService(llm_config=full_llm_config)
        
        result = service.scrape_url(url=request.url, user_prompt=request.user_prompt)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result.get("error", "Unknown scraping error"))
            
        return ScrapingResponse(
            success=True,
            result=result.get("result"),
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"API: Unhandled exception during scraping: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

@app.get("/", summary="Root", description="Root endpoint to check if the API is running.")
async def root():
    return {"message": "Web Scraping AI Agent API is running."}


# --- Entrypoint for direct execution ---
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
