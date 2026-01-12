# main.py - FastAPI wrapper for the System Architect Service

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn
import logging
from typing import Dict, Any

from system_architect_service import SystemArchitectService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- FastAPI App Initialization ---
app = FastAPI(
    title="AI System Architect API",
    version="1.0.0",
    description="An API to get expert software architecture analysis using a dual-model approach.",
)


# --- Pydantic Models ---
class ArchitectureAnalysisRequest(BaseModel):
    deepseek_api_key: str = Field(..., description="Your DeepSeek API Key.")
    anthropic_api_key: str = Field(..., description="Your Anthropic API Key.")
    user_prompt: str = Field(..., example="Design a multi-tenant SaaS platform for enterprise resource planning...", description="The detailed project description and requirements.")

class ArchitectureAnalysisResponse(BaseModel):
    success: bool
    reasoning: str | None = None
    technical_analysis_json: str | None = None
    detailed_report: str | None = None
    error: str | None = None


# --- API Endpoints ---
@app.post("/analyze-architecture", response_model=ArchitectureAnalysisResponse)
async def perform_architecture_analysis(request: ArchitectureAnalysisRequest):
    """
    Perform a detailed architectural analysis for a given project description.
    """
    logger.info(f"API: Received architecture analysis request for prompt: '{request.user_prompt[:50]}...'")
    try:
        # Note: The service's core methods are synchronous.
        # For a high-concurrency server, you might run this in a thread pool.
        service = SystemArchitectService(
            deepseek_api_key=request.deepseek_api_key,
            anthropic_api_key=request.anthropic_api_key
        )
        result = service.analyze_architecture(request.user_prompt)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result.get("error", "Unknown analysis error"))
            
        return ArchitectureAnalysisResponse(**result)
        
    except ValueError as e:
        # For invalid API keys from SystemArchitectService init
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"API: Unhandled exception during analysis: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

@app.get("/", summary="Root", description="Root endpoint to check if the API is running.")
async def root():
    return {"message": "AI System Architect API is running."}


# --- Entrypoint for direct execution ---
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
