# main.py - FastAPI wrapper for the Investment Service

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn
import logging

from investment_service import InvestmentService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- FastAPI App Initialization ---
app = FastAPI(
    title="AI Investment Agent API",
    version="1.0.0",
    description="An API to compare two stocks and generate a detailed report.",
)


# --- Pydantic Models ---
class ComparisonRequest(BaseModel):
    openai_api_key: str = Field(..., description="Your OpenAI API Key.")
    stock1: str = Field(..., example="AAPL", description="First stock symbol.")
    stock2: str = Field(..., example="MSFT", description="Second stock symbol.")

class ComparisonResponse(BaseModel):
    success: bool
    report: str | None = None
    error: str | None = None


# --- API Endpoints ---
@app.post("/compare", response_model=ComparisonResponse)
async def perform_comparison(request: ComparisonRequest):
    """
    Perform a detailed comparison of two stocks.
    """
    logger.info(f"API: Received comparison request for {request.stock1} vs {request.stock2}")
    try:
        # Note: The service's core .run() method is synchronous.
        # For a high-concurrency server, you might run this in a thread pool.
        service = InvestmentService(openai_api_key=request.openai_api_key)
        result = service.compare_stocks(request.stock1, request.stock2)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result.get("error", "Unknown comparison error"))
            
        return ComparisonResponse(
            success=True,
            report=result.get("report"),
        )
        
    except ValueError as e:
        # For invalid API key from InvestmentService init
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"API: Unhandled exception during comparison: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

@app.get("/", summary="Root", description="Root endpoint to check if the API is running.")
async def root():
    return {"message": "AI Investment Agent API is running."}


# --- Entrypoint for direct execution ---
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
