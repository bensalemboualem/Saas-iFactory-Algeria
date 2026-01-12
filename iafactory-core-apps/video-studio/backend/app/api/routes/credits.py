import os
import stripe
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
import logging

# Import services
import sys
sys.path.insert(0, '..')
from services.credits_service import (
    CreditsService,
    credits_service,
    TransactionType,
    CREDIT_PACKS,
    CREDIT_COSTS
)

from app.schemas import (
    CreditBalanceResponse,
    CreditHistoryItem,
    PurchaseRequest,
)

logger = logging.getLogger(__name__)
router = APIRouter()

# Stripe configuration
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")

if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY

# Site URLs
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://video-studio.iafactory.ch")

# Processed events (for idempotency)
_processed_events = set()


# ============================================
# SCHEMAS
# ============================================

class EstimateCostRequest(BaseModel):
    """Requête d'estimation de coût."""
    service: str
    quantity: float = 1
    options: Optional[dict] = None


class PipelineCostRequest(BaseModel):
    """Requête d'estimation coût pipeline."""
    duration: int = Field(60, ge=15, le=300)
    include_voice: bool = True
    include_music: bool = True
    model: str = "standard"


class DeductCreditsRequest(BaseModel):
    """Requête de déduction de crédits."""
    amount: int = Field(..., gt=0)
    description: str
    reference_type: Optional[str] = None
    reference_id: Optional[str] = None


class ReserveCreditsRequest(BaseModel):
    """Requête de réservation de crédits."""
    amount: int = Field(..., gt=0)
    description: str


# ============================================
# BALANCE ENDPOINTS
# ============================================

@router.get("/balance", response_model=CreditBalanceResponse, tags=["Credits - Balance"])
async def get_balance(user_id: str = "demo"):
    """Récupère le solde actuel de crédits."""
    balance = credits_service.get_balance(user_id)
    
    return CreditBalanceResponse(
        balance=balance,
        last_updated=datetime.utcnow(),
    )


@router.get("/status", tags=["Credits - Balance"])
async def get_credits_status(user_id: str = "demo"):
    """Récupère l'état complet des crédits."""
    user_credits = credits_service.get_user_credits(user_id)
    
    return {
        "balance": user_credits.balance,
        "lifetime_total": user_credits.lifetime_total,
        "last_transaction": user_credits.last_transaction.model_dump() if user_credits.last_transaction else None
    }


@router.get("/check", tags=["Credits - Balance"])
async def check_credits(
    user_id: str = "demo",
    amount: int = 1
):
    """Vérifie si l'utilisateur a assez de crédits."""
    has_enough = credits_service.has_enough_credits(user_id, amount)
    balance = credits_service.get_balance(user_id)
    
    return {
        "has_enough": has_enough,
        "balance": balance,
        "required": amount,
        "missing": max(0, amount - balance)
    }


# ============================================
# TRANSACTION HISTORY
# ============================================

@router.get("/history", response_model=List[CreditHistoryItem], tags=["Credits - History"])
async def get_history(
    user_id: str = "demo",
    type: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
):
    """Récupère l'historique des transactions."""
    tx_type = TransactionType(type) if type else None
    
    transactions = credits_service.get_transactions(
        user_id=user_id,
        transaction_type=tx_type,
        limit=limit,
        offset=offset
    )
    
    return [
        CreditHistoryItem(
            id=tx.id,
            type=tx.type.value,
            amount=tx.amount,
            description=tx.description,
            created_at=tx.created_at
        )
        for tx in transactions
    ]


# ============================================
# COST ESTIMATION
# ============================================

@router.post("/estimate", tags=["Credits - Pricing"])
async def estimate_cost(request: EstimateCostRequest):
    """Estime le coût d'un service."""
    cost = credits_service.calculate_cost(
        service=request.service,
        quantity=request.quantity,
        options=request.options
    )
    
    return {
        "service": request.service,
        "quantity": request.quantity,
        "cost": cost,
        "currency": "credits"
    }


@router.post("/estimate/pipeline", tags=["Credits - Pricing"])
async def estimate_pipeline_cost(request: PipelineCostRequest):
    """Estime le coût d'un pipeline complet."""
    estimate = credits_service.estimate_pipeline_cost(
        duration=request.duration,
        include_voice=request.include_voice,
        include_music=request.include_music,
        model=request.model
    )
    
    return estimate


@router.get("/pricing", tags=["Credits - Pricing"])
async def get_pricing_grid():
    """Retourne la grille tarifaire complète."""
    return {
        "costs": CREDIT_COSTS,
        "categories": {
            "video": [k for k in CREDIT_COSTS if k.startswith("video_")],
            "image": [k for k in CREDIT_COSTS if k.startswith("image_")],
            "tts": [k for k in CREDIT_COSTS if k.startswith("tts_")],
            "pipeline": [k for k in CREDIT_COSTS if k.startswith("pipeline_")],
            "agent": [k for k in CREDIT_COSTS if k.startswith("agent_")]
        }
    }


# ============================================
# CREDIT OPERATIONS
# ============================================

@router.post("/deduct", tags=["Credits - Operations"])
async def deduct_credits(
    request: DeductCreditsRequest,
    user_id: str = "demo"
):
    """Déduit des crédits du compte (usage interne)."""
    try:
        transaction = credits_service.deduct_credits(
            user_id=user_id,
            amount=request.amount,
            transaction_type=TransactionType.GENERATION,
            description=request.description,
            reference_type=request.reference_type,
            reference_id=request.reference_id
        )
        
        return {
            "success": True,
            "transaction_id": transaction.id,
            "amount_deducted": request.amount,
            "new_balance": transaction.balance_after
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/reserve", tags=["Credits - Operations"])
async def reserve_credits(
    request: ReserveCreditsRequest,
    user_id: str = "demo"
):
    """Réserve des crédits (pré-autorisation)."""
    try:
        reservation_id = credits_service.reserve_credits(
            user_id=user_id,
            amount=request.amount,
            description=request.description
        )
        
        return {
            "success": True,
            "reservation_id": reservation_id,
            "amount_reserved": request.amount,
            "expires_in": "30 minutes"
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/reserve/{reservation_id}/confirm", tags=["Credits - Operations"])
async def confirm_reservation(reservation_id: str):
    """Confirme une réservation."""
    success = credits_service.confirm_reservation(reservation_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Reservation not found or already processed")
    
    return {"success": True, "message": "Reservation confirmed"}


@router.post("/reserve/{reservation_id}/cancel", tags=["Credits - Operations"])
async def cancel_reservation(reservation_id: str):
    """Annule une réservation et rembourse."""
    success = credits_service.cancel_reservation(reservation_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Reservation not found or already processed")
    
    return {"success": True, "message": "Reservation cancelled, credits refunded"}


# ============================================
# PACKS & PURCHASES
# ============================================

@router.get("/packs", tags=["Credits - Packs"])
async def list_packs(locale: str = "fr"):
    """Liste les packs de crédits disponibles."""
    return credits_service.get_packs(locale=locale)


@router.post("/create-checkout-session", tags=["Credits - Purchase"])
async def create_checkout_session(request: PurchaseRequest, user_id: str = "demo"):
    """Crée une session Stripe Checkout."""
    pack = CREDIT_PACKS.get(request.pack_id)
    if not pack:
        raise HTTPException(status_code=400, detail="Invalid pack ID")
    
    if not STRIPE_SECRET_KEY:
        raise HTTPException(status_code=500, detail="Stripe not configured")
    
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'eur',
                        'unit_amount': int(pack.price_eur * 100),
                        'product_data': {
                            'name': f"IA Factory Studio - Pack {pack.name['fr']}",
                            'description': f"{pack.credits} crédits pour générer des vidéos IA",
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=f"{FRONTEND_URL}/credits?success=true&session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{FRONTEND_URL}/credits?canceled=true",
            metadata={
                'pack_id': request.pack_id,
                'credits': str(pack.credits),
                'user_id': user_id,
            },
        )
        
        return {
            "checkout_url": checkout_session.url,
            "session_id": checkout_session.id,
        }
        
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/webhook", tags=["Credits - Webhook"])
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events."""
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    # Verify signature
    if STRIPE_WEBHOOK_SECRET:
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid payload")
        except stripe.error.SignatureVerificationError:
            raise HTTPException(status_code=400, detail="Invalid signature")
    else:
        import json
        event = json.loads(payload)
    
    event_id = event.get('id', '')
    event_type = event['type']
    
    # Idempotency check
    if event_id in _processed_events:
        logger.info(f"Event {event_id} already processed, skipping")
        return JSONResponse(content={"received": True, "skipped": True})
    
    logger.info(f"Processing Stripe event: {event_type}")
    
    # Handle events
    try:
        if event_type == 'checkout.session.completed':
            await _handle_checkout_completed(event['data']['object'])
        
        elif event_type == 'payment_intent.succeeded':
            await _handle_payment_succeeded(event['data']['object'])
        
        elif event_type == 'charge.refunded':
            await _handle_refund(event['data']['object'])
        
        elif event_type == 'customer.subscription.created':
            await _handle_subscription_created(event['data']['object'])
        
        elif event_type == 'customer.subscription.deleted':
            await _handle_subscription_cancelled(event['data']['object'])
        
        # Mark as processed
        _processed_events.add(event_id)
        
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    return JSONResponse(content={"received": True})


async def _handle_checkout_completed(session: dict):
    """Handle successful checkout."""
    pack_id = session.get('metadata', {}).get('pack_id')
    credits = int(session.get('metadata', {}).get('credits', 0))
    user_id = session.get('metadata', {}).get('user_id', 'demo')
    
    if pack_id and credits:
        transaction = credits_service.process_purchase(
            user_id=user_id,
            pack_id=pack_id,
            payment_reference=session.get('payment_intent')
        )
        
        logger.info(f"✅ Added {credits} credits to user {user_id}")


async def _handle_payment_succeeded(payment_intent: dict):
    """Handle successful payment."""
    logger.info(f"Payment succeeded: {payment_intent.get('id')}")


async def _handle_refund(charge: dict):
    """Handle refund."""
    amount_refunded = charge.get('amount_refunded', 0)
    logger.info(f"Refund processed: {amount_refunded}")


async def _handle_subscription_created(subscription: dict):
    """Handle new subscription."""
    customer_id = subscription.get('customer')
    plan_id = subscription.get('items', {}).get('data', [{}])[0].get('price', {}).get('id')
    logger.info(f"Subscription created for {customer_id}: {plan_id}")


async def _handle_subscription_cancelled(subscription: dict):
    """Handle cancelled subscription."""
    customer_id = subscription.get('customer')
    logger.info(f"Subscription cancelled for {customer_id}")


@router.post("/purchase", tags=["Credits - Purchase"])
async def purchase_credits(request: PurchaseRequest, user_id: str = "demo"):
    """Achète des crédits (mode démo ou Stripe)."""
    pack = CREDIT_PACKS.get(request.pack_id)
    if not pack:
        raise HTTPException(status_code=400, detail="Invalid pack ID")
    
    # If Stripe configured, redirect to checkout
    if STRIPE_SECRET_KEY:
        return await create_checkout_session(request, user_id)
    
    # Demo mode: add credits directly
    transaction = credits_service.process_purchase(
        user_id=user_id,
        pack_id=request.pack_id,
        payment_reference="demo_purchase"
    )
    
    return {
        "success": True,
        "credits_added": pack.credits,
        "new_balance": transaction.balance_after,
        "message": f"Pack {pack.name['fr']} acheté avec succès!",
    }


@router.post("/bonus", tags=["Credits - Admin"])
async def apply_bonus(
    user_id: str,
    amount: int,
    reason: str
):
    """Applique un bonus de crédits (admin)."""
    transaction = credits_service.apply_bonus(
        user_id=user_id,
        amount=amount,
        reason=reason
    )
    
    return {
        "success": True,
        "transaction_id": transaction.id,
        "credits_added": amount,
        "new_balance": transaction.balance_after
    }


@router.get("/stripe-key", tags=["Credits - Config"])
async def get_stripe_key():
    """Retourne la clé publique Stripe."""
    if not STRIPE_PUBLISHABLE_KEY:
        raise HTTPException(status_code=404, detail="Stripe not configured")
    
    return {"publishable_key": STRIPE_PUBLISHABLE_KEY}
