"""
API Endpoints pour le système de crédits IA Factory Algeria

Endpoints:
- GET  /api/credits/balance     - Solde actuel
- GET  /api/credits/history     - Historique transactions
- GET  /api/credits/pricing     - Grille tarifaire
- GET  /api/credits/stats       - Statistiques d'usage
- POST /api/credits/upgrade     - Upgrade de plan
- POST /api/credits/purchase    - Achat de crédits (webhook Stripe/Chargily)
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
import logging
import json

from app.core.credit_service import CreditService, get_credit_service
from app.dependencies import get_current_active_user, get_db_pool

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/credits", tags=["credits"])


# ═══════════════════════════════════════════════════════════════════
# SCHEMAS
# ═══════════════════════════════════════════════════════════════════

class BalanceResponse(BaseModel):
    """Réponse solde de crédits"""
    total: int
    used: int
    remaining: int
    plan: str
    resets_at: Optional[str]
    percentage_used: float


class TransactionResponse(BaseModel):
    """Transaction de crédits"""
    id: str
    amount: int
    type: str
    service: Optional[str]
    description: Optional[str]
    metadata: dict = {}
    created_at: str


class PlanInfo(BaseModel):
    """Information sur un plan"""
    name: str
    credits_monthly: int
    price_chf: Optional[float]
    price_dzd: Optional[float]
    features: dict


class ServicePricing(BaseModel):
    """Pricing d'un service"""
    service_name: str
    service_type: str
    credits_per_unit: int
    is_unlimited: bool


class PricingResponse(BaseModel):
    """Grille tarifaire complète"""
    plans: List[PlanInfo]
    services: List[ServicePricing]


class UpgradeRequest(BaseModel):
    """Demande d'upgrade"""
    plan: str = Field(..., description="Plan cible: starter, pro, enterprise")


class PurchaseRequest(BaseModel):
    """Demande d'achat de crédits"""
    amount: int = Field(..., gt=0, description="Nombre de crédits à acheter")
    payment_method: str = Field(default="stripe", description="Méthode: stripe, chargily")


class UsageStats(BaseModel):
    """Statistiques d'utilisation"""
    period_days: int
    total_requests: int
    total_credits_used: int
    by_service: dict


# ═══════════════════════════════════════════════════════════════════
# DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════

async def get_credit_service_dep(
    db_pool = Depends(get_db_pool)
) -> CreditService:
    """Dépendance pour obtenir le CreditService"""
    return get_credit_service(db_pool)


# ═══════════════════════════════════════════════════════════════════
# ENDPOINTS PUBLICS
# ═══════════════════════════════════════════════════════════════════

@router.get("/pricing", response_model=PricingResponse)
async def get_pricing(db = Depends(get_db_pool)):
    """
    Récupère la grille tarifaire publique

    Returns:
        Plans disponibles et pricing des services
    """
    plans = await db.fetch("""
        SELECT name, credits_monthly, price_chf, price_dzd, features
        FROM subscription_plans
        WHERE is_active = true
        ORDER BY credits_monthly
    """)

    services = await db.fetch("""
        SELECT service_name, service_type, credits_per_unit, is_unlimited
        FROM service_pricing
        WHERE is_active = true
        ORDER BY service_type, credits_per_unit
    """)

    return PricingResponse(
        plans=[
            PlanInfo(
                name=p['name'],
                credits_monthly=p['credits_monthly'],
                price_chf=float(p['price_chf']) if p['price_chf'] else None,
                price_dzd=float(p['price_dzd']) if p['price_dzd'] else None,
                features=json.loads(p['features']) if isinstance(p['features'], str) else (p['features'] or {})
            )
            for p in plans
        ],
        services=[
            ServicePricing(
                service_name=s['service_name'],
                service_type=s['service_type'],
                credits_per_unit=s['credits_per_unit'],
                is_unlimited=s['is_unlimited']
            )
            for s in services
        ]
    )


# ═══════════════════════════════════════════════════════════════════
# ENDPOINTS AUTHENTIFIÉS
# ═══════════════════════════════════════════════════════════════════

@router.get("/balance", response_model=BalanceResponse)
async def get_balance(
    current_user = Depends(get_current_active_user),
    credit_service: CreditService = Depends(get_credit_service_dep)
):
    """
    Récupère le solde de crédits de l'utilisateur connecté

    Returns:
        Solde actuel avec détails du plan
    """
    tenant_id = getattr(current_user, 'tenant_id', str(current_user.id))
    balance = await credit_service.get_balance(tenant_id)

    return BalanceResponse(**balance)


@router.get("/history", response_model=List[TransactionResponse])
async def get_history(
    limit: int = Query(50, le=200, description="Nombre max de transactions"),
    offset: int = Query(0, ge=0, description="Offset pour pagination"),
    type_filter: Optional[str] = Query(None, description="Filtrer par type: usage, purchase, upgrade"),
    current_user = Depends(get_current_active_user),
    credit_service: CreditService = Depends(get_credit_service_dep)
):
    """
    Récupère l'historique des transactions de crédits

    Returns:
        Liste des transactions triées par date décroissante
    """
    tenant_id = getattr(current_user, 'tenant_id', str(current_user.id))

    transactions = await credit_service.get_history(
        tenant_id,
        limit=limit,
        offset=offset,
        type_filter=type_filter
    )

    return [TransactionResponse(**t) for t in transactions]


@router.get("/stats", response_model=UsageStats)
async def get_stats(
    days: int = Query(30, ge=1, le=365, description="Période en jours"),
    current_user = Depends(get_current_active_user),
    credit_service: CreditService = Depends(get_credit_service_dep)
):
    """
    Statistiques d'utilisation sur une période

    Returns:
        Stats par service et totaux
    """
    tenant_id = getattr(current_user, 'tenant_id', str(current_user.id))

    stats = await credit_service.get_usage_stats(tenant_id, days=days)

    return UsageStats(**stats)


@router.post("/upgrade")
async def upgrade_plan(
    request: UpgradeRequest,
    current_user = Depends(get_current_active_user),
    credit_service: CreditService = Depends(get_credit_service_dep)
):
    """
    Upgrade vers un nouveau plan

    Note: En production, cet endpoint devrait être appelé après
    confirmation de paiement (webhook Stripe/Chargily)

    Args:
        request: Plan cible

    Returns:
        Nouveau solde avec détails
    """
    tenant_id = getattr(current_user, 'tenant_id', str(current_user.id))

    # Vérifier que le plan existe
    valid_plans = ['starter', 'pro', 'enterprise']
    if request.plan not in valid_plans:
        raise HTTPException(400, f"Plan invalide. Choisir parmi: {valid_plans}")

    # Effectuer l'upgrade
    new_balance = await credit_service.upgrade_plan(tenant_id, request.plan)

    logger.info(f"Plan upgradé: user={current_user.email} plan={request.plan}")

    return {
        "success": True,
        "message": f"Plan upgradé vers {request.plan}",
        "balance": new_balance
    }


@router.post("/check")
async def check_credits(
    service_name: str = Query(..., description="Service à vérifier"),
    quantity: int = Query(1, ge=1, description="Quantité"),
    current_user = Depends(get_current_active_user),
    credit_service: CreditService = Depends(get_credit_service_dep)
):
    """
    Vérifie si l'utilisateur peut utiliser un service

    Utile pour afficher un warning AVANT d'appeler un service payant

    Returns:
        can_afford: bool
        cost: int (crédits requis)
        remaining: int (crédits restants)
    """
    tenant_id = getattr(current_user, 'tenant_id', str(current_user.id))

    service_info = await credit_service.get_service_cost(service_name)
    balance = await credit_service.get_balance(tenant_id)

    cost = service_info['cost'] * quantity
    can_afford = service_info['unlimited'] or balance['remaining'] >= cost

    return {
        "can_afford": can_afford,
        "service": service_name,
        "cost": cost if not service_info['unlimited'] else 0,
        "unlimited": service_info['unlimited'],
        "remaining": balance['remaining'],
        "plan": balance['plan']
    }


# ═══════════════════════════════════════════════════════════════════
# WEBHOOKS PAIEMENT (à protéger avec signature)
# ═══════════════════════════════════════════════════════════════════

@router.post("/webhook/stripe")
async def stripe_webhook(
    # payload: dict,  # Stripe webhook payload
    db = Depends(get_db_pool)
):
    """
    Webhook Stripe pour les paiements

    TODO: Implémenter la vérification de signature Stripe
    et le traitement des événements (payment_intent.succeeded, etc.)
    """
    # Placeholder - À implémenter avec Stripe SDK
    return {"status": "webhook_received", "provider": "stripe"}


@router.post("/webhook/chargily")
async def chargily_webhook(
    # payload: dict,  # Chargily webhook payload
    db = Depends(get_db_pool)
):
    """
    Webhook Chargily pour les paiements en DZD

    TODO: Implémenter la vérification de signature Chargily
    et le traitement des événements
    """
    # Placeholder - À implémenter avec Chargily SDK
    return {"status": "webhook_received", "provider": "chargily"}


# ═══════════════════════════════════════════════════════════════════
# ADMIN ENDPOINTS (à protéger)
# ═══════════════════════════════════════════════════════════════════

@router.post("/admin/add")
async def admin_add_credits(
    tenant_id: str,
    amount: int,
    reason: str = "admin_bonus",
    current_user = Depends(get_current_active_user),
    credit_service: CreditService = Depends(get_credit_service_dep)
):
    """
    [ADMIN] Ajoute des crédits à un tenant

    Requires: is_superuser = True
    """
    if not getattr(current_user, 'is_superuser', False):
        raise HTTPException(403, "Admin access required")

    result = await credit_service.add_credits(
        tenant_id,
        amount,
        reason=reason,
        metadata={"admin_user": current_user.email}
    )

    logger.info(f"Admin add credits: {amount} to {tenant_id} by {current_user.email}")

    return result


@router.get("/health")
async def credits_health():
    """Health check du service crédits"""
    return {
        "status": "healthy",
        "service": "Credits Service",
        "version": "1.0.0"
    }
