# main.py - FastAPI wrapper for the Meeting Preparation Service

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn
import logging
from typing import Dict, Any, List

from meeting_prep_service import MeetingPrepService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- FastAPI App Initialization ---
app = FastAPI(
    title="AI Meeting Preparation Agent API",
    version="1.0.0",
    description="An API to generate comprehensive meeting preparation materials using a multi-agent system.",
)


# --- Pydantic Models ---
class MeetingRequest(BaseModel):
    anthropic_api_key: str = Field(..., description="Your Anthropic API Key.")
    serper_api_key: str = Field(..., description="Your Serper API Key.")
    company_name: str = Field(..., example="Tech Innovations Inc.", description="The company name for the meeting.")
    meeting_objective: str = Field(..., example="Discuss Q4 strategy and product roadmap.", description="The main objective of the meeting.")
    attendees: str = Field(..., example="John Doe (CEO), Jane Smith (CTO)", description="Attendees and their roles, one per line.")
    meeting_duration: int = Field(..., ge=15, le=180, description="Meeting duration in minutes.")
    focus_areas: str = Field(..., example="Market trends, competitive landscape, budget allocation", description="Specific areas of focus or concerns.")

class MeetingResponse(BaseModel):
    success: bool
    preparation_material: str | None = None
    error: str | None = None


# --- API Endpoints ---
@app.post("/prepare-meeting", response_model=MeetingResponse)
async def prepare_meeting_api(request: MeetingRequest):
    """
    Generates comprehensive meeting preparation materials.
    """
    logger.info(f"API: Received meeting preparation request for '{request.company_name}' - '{request.meeting_objective}'")
    try:
        # Note: The service's core .kickoff() method in CrewAI is synchronous.
        # For a high-concurrency server, you might run this in a thread pool.
        service = MeetingPrepService(
            anthropic_api_key=request.anthropic_api_key,
            serper_api_key=request.serper_api_key
        )
        result = service.prepare_meeting(
            company_name=request.company_name,
            meeting_objective=request.meeting_objective,
            attendees=request.attendees,
            meeting_duration=request.meeting_duration,
            focus_areas=request.focus_areas
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result.get("error", "Unknown meeting preparation error"))
            
        return MeetingResponse(
            success=True,
            preparation_material=result.get("preparation_material"),
        )
        
    except ValueError as e:
        # For invalid API keys from MeetingPrepService init
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"API: Unhandled exception during meeting preparation: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

@app.get("/", summary="Root", description="Root endpoint to check if the API is running.")
async def root():
    return {"message": "AI Meeting Preparation Agent API is running."}


# --- Entrypoint for direct execution ---
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
