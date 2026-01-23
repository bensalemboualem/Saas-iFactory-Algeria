# main.py - FastAPI wrapper for the Financial Coach Service

import asyncio
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn
import logging
from typing import Dict, List, Any, Optional

from financial_coach_service import FinanceAdvisorSystem

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- FastAPI App Initialization ---
app = FastAPI(
    title="AI Financial Coach API",
    version="1.0.0",
    description="An API to get personalized financial analysis using a multi-agent system.",
)

# --- Pydantic Models ---
class Debt(BaseModel):
    name: str
    amount: float
    interest_rate: float

class FinancialDataRequest(BaseModel):
    google_api_key: str = Field(..., description="Your Google Gemini API Key.")
    monthly_income: float
    dependants: int = 0
    transactions: Optional[List[Dict[str, Any]]] = None
    manual_expenses: Optional[Dict[str, float]] = None
    debts: Optional[List[Debt]] = None

class FinancialAnalysisResponse(BaseModel):
    success: bool
    analysis: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


# --- API Endpoints ---
@app.post("/analyze", response_model=FinancialAnalysisResponse)
async def perform_analysis(request: FinancialDataRequest):
    """
    Perform a full financial analysis on the provided data.
    """
    logger.info(f"API: Received financial analysis request.")
    try:
        service = FinanceAdvisorSystem(gemini_api_key=request.google_api_key)
        
        # Convert Pydantic Debt models to simple dicts for the service
        debts_dict = [debt.model_dump() for debt in request.debts] if request.debts else None
        
        financial_data = {
            "monthly_income": request.monthly_income,
            "dependants": request.dependants,
            "transactions": request.transactions,
            "manual_expenses": request.manual_expenses,
            "debts": debts_dict
        }

        results = await service.analyze_finances(financial_data)
        
        if not results["success"]:
            raise HTTPException(status_code=500, detail=results.get("error", "Unknown analysis error"))
            
        return FinancialAnalysisResponse(
            success=True,
            analysis=results.get("analysis"),
        )
        
    except ValueError as e:
        # For invalid API key from FinanceAdvisorSystem init
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"API: Unhandled exception during analysis: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

@app.get("/", summary="Root", description="Root endpoint to check if the API is running.")
async def root():
    return {"message": "AI Financial Coach API is running."}

# --- Entrypoint for direct execution ---
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
