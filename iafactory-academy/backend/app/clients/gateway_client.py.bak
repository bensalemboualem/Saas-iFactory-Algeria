# -*- coding: utf-8 -*-
from fastapi import APIRouter, HTTPException
from core.database import db

router = APIRouter(prefix="/api/credits", tags=["Credits"])

@router.get("/{user_id}")
async def get_credits(user_id: str):
    credits = await db.get_user_credits(user_id)
    return {"user_id": user_id, "credits": credits}

@router.post("/add")
async def add_credits(user_id: str, amount: int, reason: str = "purchase"):
    balance = await db.add_credits(user_id, amount, reason)
    return {"user_id": user_id, "credits": balance}

@router.post("/consume")
async def consume_credits(user_id: str, amount: int, reason: str):
    try:
        balance = await db.consume_credits(user_id, amount, reason)
        return {"user_id": user_id, "credits": balance}
    except Exception as e:
        raise HTTPException(status_code=402, detail=str(e))
