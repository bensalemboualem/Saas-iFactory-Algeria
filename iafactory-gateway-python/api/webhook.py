# -*- coding: utf-8 -*-
from fastapi import APIRouter, Request, HTTPException
from core.database import db
import hmac
import hashlib

router = APIRouter(prefix="/api/webhook", tags=["Webhook"])

CHARGILY_SECRET = "test_sk4kHnTzSCgGKtiEVLFkrXJc9zNW7hQp"

@router.post("/chargily")
async def chargily_webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("signature")
    
    # Vérifie signature
    expected = hmac.new(CHARGILY_SECRET.encode(), body, hashlib.sha256).hexdigest()
    if signature != expected:
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    # Parse payload
    data = await request.json()
    
    if data.get("type") == "checkout.paid":
        user_id = data.get("metadata", {}).get("user_id")
        amount = data.get("amount", 0)
        credits = amount * 100  # 1 DZD = 100 crédits
        
        await db.add_credits(user_id, credits, f"Chargily payment {data.get('id')}")
        
        return {"status": "ok", "credits_added": credits}
    
    return {"status": "ignored"}
