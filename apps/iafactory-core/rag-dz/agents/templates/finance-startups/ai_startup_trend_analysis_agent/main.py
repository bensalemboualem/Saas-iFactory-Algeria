# main.py - FastAPI wrapper for the Startup Trends Service

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn
import logging

from startup_trends_service import StartupTrendsService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- FastAPI App Initialization ---
app = FastAPI(
    title="AI Startup Trend Analysis API",
    version="1.0.0",
    description="An API to analyze startup trends for a given topic using a multi-agent system.",
)


# --- Pydantic Models ---
class TrendAnalysisRequest(BaseModel):
    google_api_key: str = Field(..., description="Your Google Gemini API Key.")
    topic: str = Field(..., example="AI in sustainable agriculture", description="The topic or sector to analyze.")

class TrendAnalysisResponse(BaseModel):
    success: bool
    analysis: str | None = None
    summaries: str | None = None
    error: str | None = None


# --- API Endpoints ---
@app.post("/analyze-trends", response_model=TrendAnalysisResponse)
async def perform_trend_analysis(request: TrendAnalysisRequest):
    """
    Perform a multi-agent trend analysis on a given topic.
    """
    logger.info(f"API: Received trend analysis request for topic: '{request.topic}'")
    try:
        # The service's core .run() method is synchronous.
        # For a high-concurrency server, you might run this in a thread pool.
        service = StartupTrendsService(google_api_key=request.google_api_key)
        result = service.analyze_trends(request.topic)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result.get("error", "Unknown analysis error"))
            
        return TrendAnalysisResponse(
            success=True,
            analysis=result.get("analysis"),
            summaries=result.get("summaries"),
        )
        
    except ValueError as e:
        # For invalid API key from StartupTrendsService init
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"API: Unhandled exception during trend analysis: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

@app.get("/", summary="Root", description="Root endpoint to check if the API is running.")
async def root():
    return {"message": "AI Startup Trend Analysis API is running."}


# --- Entrypoint for direct execution ---
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
