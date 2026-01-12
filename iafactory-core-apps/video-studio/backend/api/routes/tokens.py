"""
IAFactory Video Studio Pro - API Routes pour les Tokens (Monétisation)
"""

from typing import List, Optional, Literal
from fastapi import APIRouter, Depends, HTTPException, status
import logging
from datetime import datetime

from app.clients.gateway_client import gateway

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/tokens",
    tags=["Tokens"],
)


# === MODÈLES DE REQUÊTES & RÉPONSES ===

class BalanceResponse(BaseModel):
    """Réponse du solde de tokens d'un utilisateur."""
    user_id: str
    balance: int
    last_updated: datetime


class CostEstimateRequest(BaseModel):
    """Requête pour estimer le coût d'une opération."""
    service_type: str = Field(..., example="script_generation")
    quantity: float = Field(1.0, gt=0, example=1.0)


class CostEstimateResponse(BaseModel):
    """Réponse de l'estimation de coût."""
    service_type: str
    estimated_cost: int
    currency: str = "IAF-Tokens"


class PurchaseRequest(BaseModel):
    """Requête pour acheter des tokens."""
    user_id: str
    amount: int = Field(..., gt=0, example=1000)
    payment_method: str = Field(..., example="stripe") # stripe, paypal, carte bancaire, etc.


class PurchaseResponse(BaseModel):
    """Réponse après un achat de tokens."""
    success: bool
    transaction_id: str
    new_balance: int
    message: Optional[str] = None


# === DÉPENDANCES ===

async def get_credits() -> CreditsService:
    return get_credits_service()


# === ROUTES ===

@router.get("/balance/{user_id}", response_model=BalanceResponse)
async def get_user_token_balance(
    user_id: str,
    credits_service: CreditsService = Depends(get_credits)
):
    """
    Récupère le solde de tokens d'un utilisateur.
    """
    logger.info(f"API: Demande de solde de tokens pour l'utilisateur {user_id}")
    balance = await credits_service.get_user_balance(user_id)
    if balance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Utilisateur {user_id} non trouvé.")
    
    return BalanceResponse(user_id=user_id, balance=balance, last_updated=datetime.utcnow())


@router.post("/estimate", response_model=CostEstimateResponse)
async def estimate_operation_cost(
    request: CostEstimateRequest,
    credits_service: CreditsService = Depends(get_credits)
):
    """
    Estime le coût en tokens d'une opération future.
    """
    logger.info(f"API: Estimation de coût pour {request.service_type} (x{request.quantity})")
    estimated_cost = await credits_service.estimate_cost(request.service_type, request.quantity)
    
    return CostEstimateResponse(
        service_type=request.service_type,
        estimated_cost=estimated_cost
    )


@router.get("/history/{user_id}", response_model=List[Transaction])
async def get_user_transaction_history(
    user_id: str,
    credits_service: CreditsService = Depends(get_credits)
):
    """
    Récupère l'historique des transactions de tokens d'un utilisateur.
    """
    logger.info(f"API: Demande d'historique de transactions pour l'utilisateur {user_id}")
    history = await credits_service.get_transaction_history(user_id)
    
    if history is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Utilisateur {user_id} non trouvé ou pas d'historique.")
        
    return history


@router.post("/purchase", response_model=PurchaseResponse)
async def purchase_tokens(
    request: PurchaseRequest,
    credits_service: CreditsService = Depends(get_credits)
):
    """
    Permet à un utilisateur d'acheter des tokens.
    (Implémentation fictive du paiement)
    """
    logger.info(f"API: Demande d'achat de {request.amount} tokens pour l'utilisateur {request.user_id}")
    
    # Ici, intégration avec un vrai fournisseur de paiement (Stripe, PayPal, etc.)
    # Pour l'exemple, nous allons simuler un succès
    transaction_id = f"txn_{datetime.utcnow().timestamp()}"
    
    new_balance = await credits_service.add_tokens(
        user_id=request.user_id,
        amount=request.amount,
        transaction_id=transaction_id,
        transaction_type=TransactionType.PURCHASE
    )
    
    if new_balance is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Échec de l'achat de tokens.")
        
    return PurchaseResponse(
        success=True,
        transaction_id=transaction_id,
        new_balance=new_balance,
        message="Achat de tokens réussi."
    )
