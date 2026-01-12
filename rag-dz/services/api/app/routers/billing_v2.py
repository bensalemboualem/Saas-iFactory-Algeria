"""
Billing PRO - Router FastAPI
============================
Endpoints complets pour gestion des crédits SaaS
"""

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Request, Header, BackgroundTasks
from pydantic import BaseModel

from ..models.billing_models import (
    # Enums
    PlanType, BillingCycle, TransactionType, PaymentProvider, ServiceType,
    # Models
    Plan, CreditPackage, Transaction,
    # Constants
    PLANS, CREDIT_PACKAGES, CREDIT_COSTS,
    # Responses
    CreditsResponse, ConsumeCreditsRequest, ConsumeCreditsResponse,
    PurchaseRequest, PurchaseResponse,
)
from app.clients.gateway_client import gateway

router = APIRouter(prefix="/api/billing/v2", tags=["Billing PRO V2"])


# ============================================
# Helper Models
# ============================================

class UpgradePlanRequest(BaseModel):
    """Requête d'upgrade de plan"""
    plan: str  # "starter", "pro", "enterprise"
    billing_cycle: str = "monthly"  # "monthly", "yearly"
    payment_provider: str = "chargily"


class AddCreditsRequest(BaseModel):
    """Ajouter des crédits manuellement (admin)"""
    credits: int
    reason: str = "Manual adjustment"


class WebhookRequest(BaseModel):
    """Requête webhook générique"""
    provider: str
    payload: dict


# ============================================
# Credits Endpoints
# ============================================

@router.get("/credits", response_model=CreditsResponse)
async def get_credits(
    user_id: str = Query(..., description="ID de l'utilisateur"),
):
    """
    💰 Obtenir le solde de crédits
    
    Retourne:
    - Solde actuel (balance + bonus)
    - Plan actif
    - Quota mensuel et usage
    - Alertes (solde bas, quota atteint)
    """
    return billing_service.get_credits_response(user_id)


@router.get("/credits/check")
async def check_can_consume(
    user_id: str = Query(...),
    service: str = Query(..., description="Type de service (rag_query, pme_full, etc.)"),
):
    """
    ✅ Vérifier si l'utilisateur peut consommer un service
    
    Utile avant d'exécuter une opération coûteuse.
    """
    try:
        service_type = ServiceType(service)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Service invalide: {service}")
    
    can_consume, cost, available = billing_service.can_consume(user_id, service_type)
    
    return {
        "can_consume": can_consume,
        "service": service,
        "cost": cost,
        "available_balance": available,
        "message": "OK" if can_consume else f"Solde insuffisant: {available} < {cost}",
    }


@router.post("/credits/consume", response_model=ConsumeCreditsResponse)
async def consume_credits(
    user_id: str = Query(...),
    request: ConsumeCreditsRequest = None,
):
    """
    🔥 Consommer des crédits
    
    Appelé automatiquement par les services (PME, RAG, Creative, etc.)
    
    Coûts par service:
    - RAG Query: 1 crédit
    - PME Quick: 1 crédit
    - PME Full: 5 crédits
    - PME PDF: 1 crédit
    - Fiscal Simulation: 2 crédits
    - Creative Generation: 3 crédits
    - Voice Call: 10 crédits/min
    - Council: 8 crédits
    - Ithy: 5 crédits
    """
    if not request:
        raise HTTPException(status_code=400, detail="Request body required")
    
    result = billing_service.consume_credits(
        user_id=user_id,
        service_type=request.service_type,
        service_reference=request.service_reference,
        credits_override=request.credits_override,
        metadata=request.metadata,
    )
    
    if not result.success:
        raise HTTPException(
            status_code=402,  # Payment Required
            detail={
                "error": "insufficient_credits",
                "required": CREDIT_COSTS.get(request.service_type, 1),
                "available": result.balance_after,
                "message": "Crédits insuffisants. Veuillez recharger votre compte.",
            }
        )
    
    return result


@router.post("/credits/add")
async def add_credits_manual(
    user_id: str = Query(...),
    request: AddCreditsRequest = None,
    x_admin_key: str = Header(None, alias="X-Admin-Key"),
):
    """
    ➕ Ajouter des crédits manuellement (Admin only)
    
    Nécessite la clé admin X-Admin-Key
    """
    # Vérification admin simple (à renforcer en prod)
    if x_admin_key != "admin-secret-key-2025":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    if not request or request.credits <= 0:
        raise HTTPException(status_code=400, detail="Credits must be positive")
    
    credits = billing_service.get_or_create_user_credits(user_id)
    credits.balance += request.credits
    
    billing_service._record_transaction(
        user_id=user_id,
        type=TransactionType.ADJUSTMENT,
        credits_amount=request.credits,
        description=f"Ajustement manuel: {request.reason}",
    )
    
    return {
        "success": True,
        "credits_added": request.credits,
        "new_balance": credits.total_available,
        "reason": request.reason,
    }


# ============================================
# Plans Endpoints
# ============================================

@router.get("/plans")
async def list_plans():
    """
    📋 Liste des plans disponibles
    
    Retourne tous les plans avec leurs prix et fonctionnalités.
    """
    plans_list = []
    for plan_type, plan in PLANS.items():
        plans_list.append({
            "id": plan.id,
            "type": plan_type.value,
            "name": plan.name,
            "description": plan.description,
            "price": {
                "monthly": float(plan.price_monthly),
                "yearly": float(plan.price_yearly),
                "currency": plan.currency,
            },
            "features": {
                "monthly_credits": plan.features.monthly_credits,
                "max_documents": plan.features.max_documents,
                "max_team_members": plan.features.max_team_members,
                "api_access": plan.features.api_access,
                "priority_support": plan.features.priority_support,
                "custom_branding": plan.features.custom_branding,
                "webhooks": plan.features.webhooks,
                "analytics": plan.features.analytics,
                "sla_guarantee": plan.features.sla_guarantee,
            },
            "is_popular": plan.is_popular,
            "trial_days": plan.trial_days,
        })
    
    return {
        "plans": plans_list,
        "currency": "DZD",
        "currency_symbol": "DA",
    }


@router.get("/plans/{plan_type}")
async def get_plan(plan_type: str):
    """
    📄 Détails d'un plan spécifique
    """
    try:
        pt = PlanType(plan_type)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Plan {plan_type} non trouvé")
    
    plan = PLANS.get(pt)
    if not plan:
        raise HTTPException(status_code=404, detail=f"Plan {plan_type} non trouvé")
    
    return {
        "plan": {
            "id": plan.id,
            "type": pt.value,
            "name": plan.name,
            "description": plan.description,
            "price_monthly": float(plan.price_monthly),
            "price_yearly": float(plan.price_yearly),
            "currency": plan.currency,
            "features": plan.features.model_dump(),
            "is_popular": plan.is_popular,
            "trial_days": plan.trial_days,
        }
    }


@router.post("/plans/upgrade")
async def upgrade_plan(
    user_id: str = Query(...),
    request: UpgradePlanRequest = None,
):
    """
    ⬆️ Upgrader vers un nouveau plan
    
    Retourne l'URL de paiement pour finaliser l'upgrade.
    """
    if not request:
        raise HTTPException(status_code=400, detail="Request body required")
    
    try:
        plan_type = PlanType(request.plan)
        billing_cycle = BillingCycle(request.billing_cycle)
        payment_provider = PaymentProvider(request.payment_provider)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    result = billing_service.upgrade_plan(
        user_id=user_id,
        new_plan=plan_type,
        billing_cycle=billing_cycle,
        payment_provider=payment_provider,
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Upgrade failed"))
    
    return result


@router.post("/plans/cancel")
async def cancel_plan(user_id: str = Query(...)):
    """
    ❌ Annuler l'abonnement
    
    L'abonnement reste actif jusqu'à la fin de la période payée.
    """
    success = billing_service.cancel_subscription(user_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Aucun abonnement actif trouvé")
    
    return {
        "success": True,
        "message": "Abonnement annulé. Il restera actif jusqu'à la fin de la période.",
    }


# ============================================
# Packages & Purchase Endpoints
# ============================================

@router.get("/packages")
async def list_packages():
    """
    📦 Liste des packages de crédits à acheter
    """
    return {
        "packages": [
            {
                "id": p.id,
                "name": p.name,
                "credits": p.credits,
                "price": float(p.price),
                "currency": p.currency,
                "price_per_credit": float(p.price_per_credit),
                "discount_percentage": p.discount_percentage,
                "is_popular": p.is_popular,
            }
            for p in CREDIT_PACKAGES if p.is_active
        ],
        "currency": "DZD",
        "currency_symbol": "DA",
    }


@router.post("/purchase", response_model=PurchaseResponse)
async def purchase_credits(
    user_id: str = Query(...),
    request: PurchaseRequest = None,
):
    """
    💳 Acheter des crédits
    
    Choisissez un package ou spécifiez un montant personnalisé.
    Retourne l'URL de paiement (Chargily pour l'Algérie 🇩🇿).
    """
    if not request:
        raise HTTPException(status_code=400, detail="Request body required")
    
    if not request.package_id and not request.credits_amount:
        raise HTTPException(status_code=400, detail="package_id ou credits_amount requis")
    
    result = billing_service.create_purchase(
        user_id=user_id,
        package_id=request.package_id,
        custom_credits=request.credits_amount,
        payment_provider=request.payment_provider,
    )
    
    if not result.success:
        raise HTTPException(status_code=400, detail="Erreur lors de la création de l'achat")
    
    return result


@router.get("/purchase/{purchase_id}")
async def get_purchase(purchase_id: str):
    """
    📄 Statut d'un achat
    """
    from app.clients.gateway_client import gateway
    
    if purchase_id not in purchases:
        raise HTTPException(status_code=404, detail="Achat non trouvé")
    
    purchase = purchases[purchase_id]
    
    return {
        "id": purchase.id,
        "user_id": purchase.user_id,
        "credits_amount": purchase.credits_amount,
        "price": float(purchase.price_amount),
        "currency": purchase.currency,
        "status": purchase.payment_status.value,
        "payment_provider": purchase.payment_provider.value,
        "payment_url": purchase.payment_url,
        "created_at": purchase.created_at.isoformat(),
        "paid_at": purchase.paid_at.isoformat() if purchase.paid_at else None,
    }


# ============================================
# Usage & History Endpoints
# ============================================

@router.get("/usage")
async def get_usage(
    user_id: str = Query(...),
    period: str = Query("monthly", description="daily, monthly, all_time"),
):
    """
    📊 Statistiques d'utilisation
    """
    return billing_service.get_usage_stats(user_id, period)


@router.get("/transactions")
async def get_transactions(
    user_id: str = Query(...),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    type: Optional[str] = Query(None, description="purchase, consumption, refund, bonus"),
):
    """
    📋 Historique des transactions
    """
    type_filter = None
    if type:
        try:
            type_filter = TransactionType(type)
        except ValueError:
            pass
    
    transactions = billing_service.get_transaction_history(
        user_id=user_id,
        limit=limit,
        offset=offset,
        type_filter=type_filter,
    )
    
    return {
        "transactions": [
            {
                "id": t.id,
                "type": t.type.value,
                "status": t.status.value,
                "credits": t.credits_amount,
                "balance_after": t.balance_after,
                "description": t.description,
                "service": t.service_type.value if t.service_type else None,
                "created_at": t.created_at.isoformat(),
            }
            for t in transactions
        ],
        "total": len(transactions),
        "limit": limit,
        "offset": offset,
    }


@router.get("/alerts")
async def get_alerts(
    user_id: str = Query(...),
    unread_only: bool = Query(True),
):
    """
    🔔 Alertes de l'utilisateur
    """
    from app.clients.gateway_client import gateway
    
    user_alerts = [a for a in alerts if a.user_id == user_id]
    
    if unread_only:
        user_alerts = [a for a in user_alerts if not a.is_read]
    
    return {
        "alerts": [
            {
                "id": a.id,
                "type": a.alert_type,
                "message": a.message,
                "is_read": a.is_read,
                "created_at": a.created_at.isoformat(),
            }
            for a in sorted(user_alerts, key=lambda x: x.created_at, reverse=True)
        ],
        "unread_count": len([a for a in user_alerts if not a.is_read]),
    }


@router.post("/alerts/{alert_id}/read")
async def mark_alert_read(alert_id: str):
    """
    ✅ Marquer une alerte comme lue
    """
    from app.clients.gateway_client import gateway
    
    alert = next((a for a in alerts if a.id == alert_id), None)
    if not alert:
        raise HTTPException(status_code=404, detail="Alerte non trouvée")
    
    alert.is_read = True
    
    return {"success": True}


# ============================================
# Webhooks Endpoints
# ============================================

@router.post("/webhooks/chargily")
async def chargily_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    🔔 Webhook Chargily (Paiement Algérie)
    
    Appelé automatiquement par Chargily après un paiement.
    """
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    # TODO: Vérifier la signature Chargily
    
    # Traiter en background
    background_tasks.add_task(billing_service.handle_chargily_webhook, payload)
    
    return {"received": True}


@router.post("/webhooks/stripe")
async def stripe_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    🔔 Webhook Stripe
    
    Appelé automatiquement par Stripe après un paiement.
    """
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    # TODO: Vérifier la signature Stripe
    
    # Traiter en background
    background_tasks.add_task(billing_service.handle_stripe_webhook, payload)
    
    return {"received": True}


# ============================================
# Pricing & Costs Reference
# ============================================

@router.get("/pricing/services")
async def get_service_pricing():
    """
    💰 Coût en crédits par service
    """
    return {
        "services": {
            service.value: {
                "cost": cost,
                "name": service.value.replace("_", " ").title(),
            }
            for service, cost in CREDIT_COSTS.items()
        },
        "note": "Les crédits bonus sont utilisés en priorité.",
    }


# ============================================
# Admin Endpoints
# ============================================

@router.post("/admin/reset-monthly")
async def admin_reset_monthly(
    user_id: str = Query(...),
    x_admin_key: str = Header(None, alias="X-Admin-Key"),
):
    """
    🔄 Reset mensuel manuel (Admin)
    """
    if x_admin_key != "admin-secret-key-2025":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    success = billing_service.reset_monthly_credits(user_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    return {"success": True, "message": "Reset mensuel effectué"}


@router.get("/admin/stats")
async def admin_stats(
    x_admin_key: str = Header(None, alias="X-Admin-Key"),
):
    """
    📊 Statistiques globales (Admin)
    """
    if x_admin_key != "admin-secret-key-2025":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    from app.clients.gateway_client import gateway
    
    total_users = len(users_credits)
    total_credits = sum(u.total_available for u in users_credits.values())
    total_transactions = len(transactions)
    total_purchases = len([p for p in purchases.values() if p.payment_status.value == "completed"])
    
    plan_distribution = {}
    for user in users_credits.values():
        plan = user.plan_type.value
        plan_distribution[plan] = plan_distribution.get(plan, 0) + 1
    
    return {
        "total_users": total_users,
        "total_credits_in_circulation": total_credits,
        "total_transactions": total_transactions,
        "total_purchases_completed": total_purchases,
        "plan_distribution": plan_distribution,
    }


# ============================================
# Health Check
# ============================================

@router.get("/health")
async def health_check():
    """
    🏥 Vérifier l'état du service Billing
    """
    from app.clients.gateway_client import gateway
    
    return {
        "status": "healthy",
        "service": "Billing PRO V2",
        "version": "2.0.0",
        "users_count": len(users_credits),
        "transactions_count": len(transactions),
        "features": [
            "credits_management",
            "subscription_plans",
            "credit_packages",
            "usage_tracking",
            "webhooks_chargily",
            "webhooks_stripe",
            "alerts",
        ],
        "payment_providers": ["chargily", "stripe", "paypal", "bank_transfer"],
    }
