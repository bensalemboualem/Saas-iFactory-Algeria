# -*- coding: utf-8 -*-
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from core.auth import get_current_user
from core.router import get_provider
from core.database import db

router = APIRouter(prefix="/api/llm", tags=["LLM"])

class ChatRequest(BaseModel):
    model: str
    messages: list[dict]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1000
    stream: bool = False

@router.post("/chat/completions")
async def chat_completion(request: ChatRequest):
    user_id = "test-user"
    
    # 1. Vérifie crédits (1 token = 1 crédit pour simplifier)
    credits = await db.get_user_credits(user_id)
    if credits < request.max_tokens:
        raise HTTPException(status_code=402, detail=f"Insufficient credits. Have {credits}, need {request.max_tokens}")
    
    # 2. Route vers provider
    try:
        provider, provider_name = get_provider(request.model)
        response = await provider.chat_completion(
            model=request.model, messages=request.messages,
            temperature=request.temperature, max_tokens=request.max_tokens, stream=request.stream
        )
        
        # 3. Débite crédits (tokens utilisés)
        tokens_used = response.get("usage", {}).get("total_tokens", request.max_tokens)
        await db.consume_credits(user_id, tokens_used, f"LLM call {provider_name}/{request.model}")
        
        # 4. Ajoute metadata
        response["_gateway"] = {"provider": provider_name, "tokens_debited": tokens_used, "timestamp": datetime.now().isoformat()}
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Provider error: {str(e)}")
