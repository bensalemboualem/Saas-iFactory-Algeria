"""
Billing & Credits API Router
=============================
Gestion des crédits utilisateur pour les composants SaaS.
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/billing", tags=["Billing"])

# ============================================
# Models
# ============================================

class CreditsResponse(BaseModel):
    used: int
    total: int
    plan: str
    reset_date: str
    low_threshold: int = 20

class BuyCreditsRequest(BaseModel):
    amount: int
    payment_method: str = "stripe"

class BuyCreditsResponse(BaseModel):
    success: bool
    new_total: int
    transaction_id: str

# ============================================
# In-memory store (mock)
# ============================================

# Mock user credits - en production, utiliser Redis/PostgreSQL
_user_credits = {}

def get_user_credits(user_id: str) -> dict:
    """Récupère ou initialise les crédits d'un utilisateur"""
    if user_id not in _user_credits:
        # Nouveau user = plan gratuit avec 100 crédits
        reset_date = datetime.now() + timedelta(days=30)
        _user_credits[user_id] = {
            "used": 0,
            "total": 100,
            "plan": "free",
            "reset_date": reset_date.isoformat(),
            "low_threshold": 20
        }
    return _user_credits[user_id]

def consume_credits(user_id: str, amount: int) -> bool:
    """Consomme des crédits pour un utilisateur"""
    credits = get_user_credits(user_id)
    remaining = credits["total"] - credits["used"]
    if remaining < amount:
        return False
    credits["used"] += amount
    return True

# ============================================
# Endpoints
# ============================================

@router.get("/credits", response_model=CreditsResponse)
async def get_credits(
    x_user_id: Optional[str] = Header(None, alias="X-User-Id"),
    authorization: Optional[str] = Header(None)
):
    """
    Récupère le solde de crédits de l'utilisateur.
    Utilisé par le composant CreditsBadge.
    """
    # Extraire user_id du header ou utiliser un défaut pour la démo
    user_id = x_user_id or "demo_user"
    
    credits = get_user_credits(user_id)
    
    logger.info(f"Credits check for user {user_id}: {credits['total'] - credits['used']} remaining")
    
    return CreditsResponse(**credits)

@router.post("/credits/consume")
async def consume_user_credits(
    amount: int = 1,
    x_user_id: Optional[str] = Header(None, alias="X-User-Id")
):
    """Consomme des crédits pour une opération"""
    user_id = x_user_id or "demo_user"
    
    if not consume_credits(user_id, amount):
        raise HTTPException(
            status_code=402,
            detail={
                "error": "insufficient_credits",
                "message": "Crédits insuffisants. Rechargez votre compte.",
                "required": amount,
                "available": get_user_credits(user_id)["total"] - get_user_credits(user_id)["used"]
            }
        )
    
    return {
        "success": True,
        "consumed": amount,
        "remaining": get_user_credits(user_id)["total"] - get_user_credits(user_id)["used"]
    }

@router.post("/credits/buy", response_model=BuyCreditsResponse)
async def buy_credits(
    request: BuyCreditsRequest,
    x_user_id: Optional[str] = Header(None, alias="X-User-Id")
):
    """
    Acheter des crédits supplémentaires.
    En production, intégrer avec Stripe/Paddle.
    """
    user_id = x_user_id or "demo_user"
    credits = get_user_credits(user_id)
    
    # Mock: ajouter directement les crédits
    credits["total"] += request.amount
    
    # Générer un ID de transaction mock
    import uuid
    transaction_id = f"txn_{uuid.uuid4().hex[:12]}"
    
    logger.info(f"User {user_id} bought {request.amount} credits. New total: {credits['total']}")
    
    return BuyCreditsResponse(
        success=True,
        new_total=credits["total"],
        transaction_id=transaction_id
    )

@router.get("/plans")
async def get_plans():
    """Liste des plans disponibles"""
    return {
        "plans": [
            {
                "id": "free",
                "name": "Gratuit",
                "credits": 100,
                "price": 0,
                "features": ["100 crédits/mois", "Support email", "1 projet"]
            },
            {
                "id": "starter",
                "name": "Starter",
                "credits": 500,
                "price": 9.99,
                "features": ["500 crédits/mois", "Support prioritaire", "5 projets", "API access"]
            },
            {
                "id": "pro",
                "name": "Pro",
                "credits": 2000,
                "price": 29.99,
                "features": ["2000 crédits/mois", "Support 24/7", "Projets illimités", "API access", "Custom domain"]
            },
            {
                "id": "enterprise",
                "name": "Enterprise",
                "credits": 10000,
                "price": 99.99,
                "features": ["10000 crédits/mois", "Account manager", "SLA 99.9%", "On-premise option"]
            }
        ]
    }

@router.get("/health")
async def billing_health():
    """Health check du service billing"""
    return {"status": "healthy", "service": "billing"}
