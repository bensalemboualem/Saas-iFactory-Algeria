"""
IAFactory Assistant API Router
Endpoint: POST /api/iafactory-assistant
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal
import sys
from pathlib import Path

# Ajouter le parent au path pour import
sys.path.append(str(Path(__file__).parent.parent))
from iafactory_rag import answer, Region

router = APIRouter(prefix="/api", tags=["IAFactory Assistant"])

class AssistantRequest(BaseModel):
    question: str
    region: Literal["DZ", "CH"]

class AssistantResponse(BaseModel):
    answer: str
    sources: list[str]
    region: str

@router.post("/iafactory-assistant", response_model=AssistantResponse)
async def iafactory_assistant(request: AssistantRequest):
    """
    Assistant IAFactory - Répond aux questions commerciales/techniques
    
    - DZ: Algérie (contact@iafactory.dz)
    - CH: Suisse (contact@iafactory.ch)
    """
    try:
        result = answer(request.question, request.region)
        return AssistantResponse(
            answer=result["answer"],
            sources=result["sources"],
            region=request.region
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
