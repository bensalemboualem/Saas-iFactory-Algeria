# main.py - FastAPI wrapper for the Product Launch Service

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn
import logging
from typing import Dict, Any, Literal

from product_launch_service import ProductLaunchService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- FastAPI App Initialization ---
app = FastAPI(
    title="AI Product Launch Intelligence API",
    version="1.0.0",
    description="An API to get intelligence on product launches using a multi-agent system.",
)


# --- Pydantic Models ---
class LaunchAnalysisRequest(BaseModel):
    openai_api_key: str = Field(..., description="Your OpenAI API Key.")
    firecrawl_api_key: str = Field(..., description="Your Firecrawl API Key.")
    company_name: str = Field(..., example="OpenAI", description="The company name to analyze.")
    analysis_type: Literal["competitor", "sentiment", "metrics"] = Field(..., example="competitor", description="Type of analysis to perform.")

class LaunchAnalysisResponse(BaseModel):
    success: bool
    report: str | None = None
    error: str | None = None


# --- API Endpoints ---
@app.post("/analyze-launch", response_model=LaunchAnalysisResponse)
async def perform_launch_analysis(request: LaunchAnalysisRequest):
    """
    Perform a product launch intelligence analysis for a given company.
    """
    logger.info(f"API: Received launch analysis request for '{request.company_name}' ({request.analysis_type})")
    try:
        # Note: The service's core .run() method in Agno is synchronous.
        # For a high-concurrency server, you might run this in a thread pool.
        service = ProductLaunchService(
            openai_api_key=request.openai_api_key,
            firecrawl_api_key=request.firecrawl_api_key
        )
        result = service.analyze_launch(
            company_name=request.company_name,
            analysis_type=request.analysis_type
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result.get("error", "Unknown analysis error"))
            
        return LaunchAnalysisResponse(
            success=True,
            report=result.get("report"),
        )
        
    except ValueError as e:
        # For invalid API keys from ProductLaunchService init
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"API: Unhandled exception during launch analysis: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

@app.get("/", summary="Root", description="Root endpoint to check if the API is running.")
async def root():
    return {"message": "AI Product Launch Intelligence API is running."}


# --- Entrypoint for direct execution ---
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
