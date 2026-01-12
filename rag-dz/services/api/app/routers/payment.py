"""
Payment Router - Intégration Chargily pour paiements DZD

Chargily: Gateway de paiement algérien
- CIB (carte bancaire algérienne)
- EDAHABIA (Algérie Poste)
- BaridiMob

Flow:
1. User clique "S'abonner ÉTUDIANT"
2. Backend créé checkout Chargily
3. User redirigé vers Chargily (paiement CIB/EDAHABIA)
4. Chargily webhook → Backend active abonnement
5. User redirigé vers /dashboard (success)
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from typing import Optional
import httpx
import hmac
import hashlib
import logging
import os
from datetime import datetime, timedelta
import asyncpg

from app.dependencies import get_current_active_user, get_db_pool
from app.models.user import UserInDB

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/payment", tags=["payment"])


class ChargilyClient:
    """
    Client Chargily API pour paiements DZD

    Docs: https://dev.chargily.com/pay-v2/
    """

    def __init__(self):
        self.api_key = os.getenv("CHARGILY_API_KEY")
        self.secret_key = os.getenv("CHARGILY_SECRET_KEY")
        self.webhook_secret = os.getenv("CHARGILY_WEBHOOK_SECRET")
        self.mode = os.getenv("CHARGILY_MODE", "test")  # test ou live

        if not self.api_key:
            logger.warning("CHARGILY_API_KEY not set - payments will fail")

        self.base_url = "https://pay.chargily.net/api/v2" if self.mode == "live" else "https://pay.chargily.net/test/api/v2"

        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            timeout=30.0
        )

    async def create_checkout(
        self,
        amount: int,
        currency: str = "dzd",
        success_url: str = "",
        failure_url: str = "",
        webhook_url: str = "",
        metadata: dict = None
    ) -> dict:
        """
        Créer une session de paiement Chargily

        Args:
            amount: Montant en DZD (ex: 1590 pour 1590 DA)
            currency: Devise (toujours "dzd")
            success_url: URL redirection si paiement réussi
            failure_url: URL redirection si paiement échoué
            webhook_url: URL webhook backend
            metadata: Données custom (user_id, tier, etc.)

        Returns:
            {
                "id": "checkout_xxx",
                "checkout_url": "https://pay.chargily.net/checkout/xxx"
            }
        """
        try:
            response = await self.client.post(
                "/checkouts",
                json={
                    "amount": amount,
                    "currency": currency,
                    "success_url": success_url,
                    "failure_url": failure_url,
                    "webhook_url": webhook_url,
                    "metadata": metadata or {},
                    "locale": "ar",  # Interface en arabe par défaut
                    "payment_method": "cib,edahabia"  # Accepter CIB et EDAHABIA
                }
            )
            response.raise_for_status()
            data = response.json()

            logger.info(f"Chargily checkout created: {data.get('id')}")

            return {
                "id": data["id"],
                "checkout_url": data["checkout_url"]
            }

        except Exception as e:
            logger.error(f"Chargily checkout creation failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erreur création paiement: {str(e)}"
            )

    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        """
        Vérifie signature webhook Chargily (sécurité)

        Args:
            payload: Corps de la requête webhook (bytes)
            signature: Header "signature" du webhook

        Returns:
            True si signature valide, False sinon
        """
        if not self.webhook_secret:
            logger.warning("CHARGILY_WEBHOOK_SECRET not set - cannot verify webhooks")
            return False

        # Calculer signature attendue (HMAC-SHA256)
        expected_signature = hmac.new(
            self.webhook_secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected_signature, signature)

    async def close(self):
        """Ferme le client HTTP"""
        await self.client.aclose()


# Singleton
_chargily_client: Optional[ChargilyClient] = None


def get_chargily() -> ChargilyClient:
    """Dependency pour FastAPI"""
    global _chargily_client
    if _chargily_client is None:
        _chargily_client = ChargilyClient()
    return _chargily_client


# === ROUTES ===

@router.post("/subscribe/{tier}")
async def create_subscription_checkout(
    tier: str,
    user: UserInDB = Depends(get_current_active_user),
    chargily: ChargilyClient = Depends(get_chargily)
):
    """
    Créer un checkout Chargily pour abonnement

    Args:
        tier: "student" ou "pro"
        user: Utilisateur connecté

    Returns:
        {"checkout_url": "https://pay.chargily.net/checkout/xxx"}
    """

    # Valider tier
    if tier not in ["student", "pro"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tier invalide: {tier}. Utilisez 'student' ou 'pro'."
        )

    # Prix par tier
    prices = {
        "student": 1590,  # DA
        "pro": 2590       # DA
    }
    amount = prices[tier]

    # URLs frontend
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    api_url = os.getenv("API_URL", "http://localhost:8000")

    # Créer checkout Chargily
    checkout = await chargily.create_checkout(
        amount=amount,
        currency="dzd",
        success_url=f"{frontend_url}/subscribe/success",
        failure_url=f"{frontend_url}/subscribe/failure",
        webhook_url=f"{api_url}/payment/webhook/chargily",
        metadata={
            "user_id": user.id,
            "tier": tier,
            "email": user.email
        }
    )

    logger.info(
        f"Subscription checkout created for user {user.id} ({user.email}): "
        f"{tier} - {amount} DA - Checkout ID: {checkout['id']}"
    )

    return {
        "checkout_url": checkout["checkout_url"],
        "checkout_id": checkout["id"],
        "amount": amount,
        "tier": tier
    }


@router.post("/webhook/chargily")
async def chargily_webhook(
    request: Request,
    db: asyncpg.Pool = Depends(get_db_pool),
    chargily: ChargilyClient = Depends(get_chargily)
):
    """
    Webhook Chargily pour activation automatique abonnement

    Flow:
    1. User paie sur Chargily
    2. Chargily envoie webhook "checkout.paid"
    3. Backend active abonnement user (tier + expires_at)
    4. User peut utiliser app tier payant

    Security:
    - Vérifie signature HMAC-SHA256
    - Idempotence (évite double activation)
    """

    # Récupérer payload brut (pour vérification signature)
    body = await request.body()

    # Récupérer signature header
    signature = request.headers.get("signature", "")

    # Vérifier signature (SÉCURITÉ CRITIQUE)
    if not chargily.verify_webhook_signature(body, signature):
        logger.error("Chargily webhook signature verification FAILED")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid webhook signature"
        )

    # Parser payload JSON
    event = await request.json()

    event_type = event.get("type")
    logger.info(f"Chargily webhook received: {event_type}")

    # Gérer événement "checkout.paid"
    if event_type == "checkout.paid":
        checkout_data = event.get("data", {})
        metadata = checkout_data.get("metadata", {})

        user_id = metadata.get("user_id")
        tier = metadata.get("tier")
        checkout_id = checkout_data.get("id")
        amount = checkout_data.get("amount")

        if not user_id or not tier:
            logger.error(f"Missing metadata in webhook: {metadata}")
            return {"status": "error", "message": "Missing metadata"}

        # Vérifier idempotence (éviter double activation)
        existing = await db.fetchrow(
            """
            SELECT * FROM user_tiers
            WHERE user_id = $1 AND chargily_checkout_id = $2
            """,
            user_id,
            checkout_id
        )

        if existing:
            logger.warning(f"Webhook already processed for checkout {checkout_id}")
            return {"status": "ok", "message": "Already processed"}

        # Activer abonnement (INSERT ou UPDATE)
        try:
            await db.execute(
                """
                INSERT INTO user_tiers (user_id, tier, subscribed_at, expires_at, chargily_checkout_id)
                VALUES ($1, $2, NOW(), NOW() + INTERVAL '30 days', $3)
                ON CONFLICT (user_id)
                DO UPDATE SET
                    tier = $2,
                    subscribed_at = NOW(),
                    expires_at = NOW() + INTERVAL '30 days',
                    chargily_checkout_id = $3
                """,
                user_id,
                tier,
                checkout_id
            )

            logger.info(
                f"✅ Subscription activated! User {user_id} upgraded to {tier} "
                f"(Checkout: {checkout_id}, Amount: {amount} DA)"
            )

            # TODO: Envoyer email confirmation
            # await send_email(user.email, "Abonnement activé!", ...)

        except Exception as e:
            logger.error(f"Failed to activate subscription: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to activate subscription"
            )

    elif event_type == "checkout.failed":
        # Paiement échoué
        logger.warning(f"Payment failed: {event.get('data', {}).get('id')}")
        # TODO: Notifier user (email)

    elif event_type == "checkout.expired":
        # Session expirée (user n'a pas payé)
        logger.info(f"Checkout expired: {event.get('data', {}).get('id')}")

    return {"status": "ok"}


@router.get("/subscription/status")
async def get_subscription_status(
    user: UserInDB = Depends(get_current_active_user),
    db: asyncpg.Pool = Depends(get_db_pool)
):
    """
    Récupère le statut d'abonnement de l'utilisateur

    Returns:
        {
            "tier": "student",
            "subscribed_at": "2024-12-23T10:00:00",
            "expires_at": "2025-01-22T10:00:00",
            "days_remaining": 30,
            "is_active": true
        }
    """
    subscription = await db.fetchrow(
        """
        SELECT tier, subscribed_at, expires_at
        FROM user_tiers
        WHERE user_id = $1
        """,
        user.id
    )

    if not subscription:
        # Pas d'abonnement → FREE tier
        return {
            "tier": "free",
            "subscribed_at": None,
            "expires_at": None,
            "days_remaining": None,
            "is_active": False
        }

    expires_at = subscription["expires_at"]
    days_remaining = (expires_at - datetime.now()).days if expires_at else None
    is_active = days_remaining > 0 if days_remaining is not None else False

    return {
        "tier": subscription["tier"],
        "subscribed_at": subscription["subscribed_at"].isoformat() if subscription["subscribed_at"] else None,
        "expires_at": expires_at.isoformat() if expires_at else None,
        "days_remaining": days_remaining,
        "is_active": is_active
    }


@router.post("/subscription/cancel")
async def cancel_subscription(
    user: UserInDB = Depends(get_current_active_user),
    db: asyncpg.Pool = Depends(get_db_pool)
):
    """
    Annuler l'abonnement (fin de période en cours, pas de renouvellement)

    Note: User garde accès jusqu'à expires_at
    """
    await db.execute(
        """
        UPDATE user_tiers
        SET auto_renew = FALSE
        WHERE user_id = $1
        """,
        user.id
    )

    logger.info(f"User {user.id} cancelled subscription (expires_at unchanged)")

    return {
        "status": "ok",
        "message": "Abonnement annulé. Vous gardez l'accès jusqu'à la fin de la période payée."
    }


# ============================================
# CREDITS SYSTEM - Plans IAFactory
# ============================================

# Prix des plans crédits
CREDIT_PLANS = {
    'starter': {
        'name': 'Starter',
        'credits': 10000,
        'price_dzd': 1500,
        'price_chf': 15,
        'description': '10,000 crédits/mois - Images incluses'
    },
    'pro': {
        'name': 'Pro',
        'credits': 30000,
        'price_dzd': 4000,
        'price_chf': 40,
        'description': '30,000 crédits/mois - Images + Vidéos'
    },
    'enterprise': {
        'name': 'Enterprise',
        'credits': 100000,
        'price_dzd': 15000,
        'price_chf': 150,
        'description': '100,000 crédits/mois - Tout illimité + Support'
    }
}


class CreateCreditsCheckoutRequest(BaseModel):
    plan: str  # 'starter', 'pro', 'enterprise'
    email: str
    name: Optional[str] = None
    success_url: Optional[str] = None
    failure_url: Optional[str] = None


@router.get("/plans")
async def get_credit_plans():
    """
    Retourne les plans de crédits disponibles avec prix DZD et CHF
    """
    return {
        "plans": CREDIT_PLANS,
        "currency": "DZD",
        "payment_methods": ["CIB", "EDAHABIA"]
    }


@router.post("/credits/checkout")
async def create_credits_checkout(
    request: CreateCreditsCheckoutRequest,
    user: UserInDB = Depends(get_current_active_user),
    chargily: ChargilyClient = Depends(get_chargily)
):
    """
    Créer un checkout Chargily pour achat de crédits (plan)

    Args:
        request: Plan choisi + email
        user: Utilisateur connecté

    Returns:
        {"checkout_url": "https://pay.chargily.net/checkout/xxx", ...}
    """

    plan_name = request.plan.lower()
    if plan_name not in CREDIT_PLANS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Plan invalide: {plan_name}. Plans valides: {list(CREDIT_PLANS.keys())}"
        )

    plan = CREDIT_PLANS[plan_name]
    amount = plan['price_dzd']

    # URLs
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    api_url = os.getenv("API_URL", "http://localhost:8000")

    # Créer checkout Chargily
    checkout = await chargily.create_checkout(
        amount=amount,
        currency="dzd",
        success_url=request.success_url or f"{frontend_url}/payment/success?plan={plan_name}",
        failure_url=request.failure_url or f"{frontend_url}/payment/failed?plan={plan_name}",
        webhook_url=f"{api_url}/payment/webhook/credits",
        metadata={
            "user_id": str(user.id),
            "tenant_id": str(getattr(user, 'tenant_id', user.id)),
            "plan": plan_name,
            "credits": plan['credits'],
            "email": request.email,
            "name": request.name or ""
        }
    )

    logger.info(
        f"Credits checkout created for user {user.id}: "
        f"{plan_name} - {amount} DA - {plan['credits']} credits - Checkout ID: {checkout['id']}"
    )

    return {
        "checkout_url": checkout["checkout_url"],
        "checkout_id": checkout["id"],
        "amount": amount,
        "plan": plan_name,
        "credits": plan['credits']
    }


@router.post("/webhook/credits")
async def credits_webhook(
    request: Request,
    db: asyncpg.Pool = Depends(get_db_pool),
    chargily: ChargilyClient = Depends(get_chargily)
):
    """
    Webhook Chargily pour achat de crédits

    Flow:
    1. User paie sur Chargily
    2. Chargily envoie webhook "checkout.paid"
    3. Backend upgrade le plan et ajoute les crédits
    """

    body = await request.body()
    signature = request.headers.get("signature", "")

    # Vérifier signature
    if signature and not chargily.verify_webhook_signature(body, signature):
        logger.error("Credits webhook signature verification FAILED")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid webhook signature"
        )

    event = await request.json()
    event_type = event.get("type")

    logger.info(f"Credits webhook received: {event_type}")

    if event_type == "checkout.paid":
        checkout_data = event.get("data", {})
        metadata = checkout_data.get("metadata", {})

        tenant_id = metadata.get("tenant_id")
        plan = metadata.get("plan")
        credits = int(metadata.get("credits", 0))
        checkout_id = checkout_data.get("id")
        amount = checkout_data.get("amount")

        if not tenant_id or not plan:
            logger.error(f"Missing metadata in credits webhook: {metadata}")
            return {"status": "error", "message": "Missing metadata"}

        # Vérifier idempotence
        existing = await db.fetchrow(
            """
            SELECT * FROM credit_transactions
            WHERE metadata->>'chargily_checkout_id' = $1
            """,
            checkout_id
        )

        if existing:
            logger.warning(f"Credits webhook already processed for checkout {checkout_id}")
            return {"status": "ok", "message": "Already processed"}

        try:
            # 1. Mettre à jour ou créer l'entrée user_credits
            await db.execute(
                """
                INSERT INTO user_credits (tenant_id, total_credits, used_credits, plan, credits_reset_at)
                VALUES ($1::uuid, $2, 0, $3, NOW() + INTERVAL '30 days')
                ON CONFLICT (tenant_id) DO UPDATE SET
                    total_credits = user_credits.total_credits + $2,
                    plan = $3,
                    credits_reset_at = NOW() + INTERVAL '30 days',
                    updated_at = NOW()
                """,
                tenant_id,
                credits,
                plan
            )

            # 2. Mettre à jour ou créer l'entrée billing_tenants
            await db.execute(
                """
                INSERT INTO billing_tenants (tenant_id, plan, credits_total, credits_used, subscription_status)
                VALUES ($1::uuid, $2, $3, 0, 'active')
                ON CONFLICT (tenant_id) DO UPDATE SET
                    plan = $2,
                    credits_total = billing_tenants.credits_total + $3,
                    subscription_status = 'active',
                    updated_at = NOW()
                """,
                tenant_id,
                plan,
                credits
            )

            # 3. Enregistrer la transaction
            await db.execute(
                """
                INSERT INTO credit_transactions (tenant_id, amount, type, service, metadata)
                VALUES ($1::uuid, $2, 'purchase', 'plan_upgrade', $3)
                """,
                tenant_id,
                credits,
                {
                    "plan": plan,
                    "chargily_checkout_id": checkout_id,
                    "amount_dzd": amount
                }
            )

            logger.info(
                f"Credits added! Tenant {tenant_id} upgraded to {plan} "
                f"(+{credits} credits, Checkout: {checkout_id}, Amount: {amount} DA)"
            )

        except Exception as e:
            logger.error(f"Failed to process credits payment: {e}")
            # Ne pas lever d'exception pour éviter que Chargily réessaie
            return {"status": "error", "message": str(e)}

    elif event_type == "checkout.failed":
        logger.warning(f"Credits payment failed: {event.get('data', {}).get('id')}")

    elif event_type == "checkout.expired":
        logger.info(f"Credits checkout expired: {event.get('data', {}).get('id')}")

    return {"status": "ok"}


# ============================================
# USER CREDITS API - Balance & History
# ============================================

from app.clients.gateway_client import gateway


@router.get("/credits/balance")
async def get_credits_balance(
    user: UserInDB = Depends(get_current_active_user)
):
    """
    Get current user's credit balance

    Returns:
        {
            "balance": 150,
            "total_purchased": 200,
            "total_consumed": 50,
            "last_updated": "2024-12-25T10:00:00"
        }
    """
    balance = await credits_service.get_balance(user.id)
    return {
        "user_id": balance.user_id,
        "balance": balance.balance,
        "total_purchased": balance.total_purchased,
        "total_consumed": balance.total_consumed,
        "last_updated": balance.last_updated.isoformat()
    }


@router.get("/credits/history")
async def get_credits_history(
    limit: int = 50,
    offset: int = 0,
    user: UserInDB = Depends(get_current_active_user)
):
    """
    Get user's credit transaction history

    Returns list of transactions with type, amount, service, etc.
    """
    transactions = await credits_service.get_transactions(user.id, limit, offset)
    return {
        "transactions": [
            {
                "id": t.id,
                "amount": t.amount,
                "type": t.transaction_type.value,
                "service": t.service_type.value if t.service_type else None,
                "description": t.description,
                "created_at": t.created_at.isoformat()
            }
            for t in transactions
        ],
        "count": len(transactions),
        "limit": limit,
        "offset": offset
    }


@router.get("/credits/pricing")
async def get_service_pricing():
    """
    Get credit costs for each service type

    Returns:
        {
            "services": {
                "rag_query": 1,
                "image_gen": 10,
                "video_gen": 50,
                ...
            }
        }
    """
    return {
        "services": {
            service_type.value: credits_service.get_service_cost(service_type)
            for service_type in ServiceType
        },
        "plans": CREDIT_PLANS
    }


class QuickCreditsPurchaseRequest(BaseModel):
    """Request for quick credits purchase"""
    amount_dzd: int  # Amount in DZD (e.g., 500, 1000, 2000)
    success_url: Optional[str] = None
    failure_url: Optional[str] = None


@router.post("/credits/quick-purchase")
async def quick_credits_purchase(
    request: QuickCreditsPurchaseRequest,
    user: UserInDB = Depends(get_current_active_user),
    chargily: ChargilyClient = Depends(get_chargily)
):
    """
    Quick credit purchase without plan subscription

    Allows users to buy any amount of credits directly
    1 DZD = 1 credit (configurable)
    """
    if request.amount_dzd < 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Minimum purchase is 100 DZD"
        )

    if request.amount_dzd > 100000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum purchase is 100,000 DZD"
        )

    credits_to_add = credits_service.calculate_credits_from_dzd(request.amount_dzd)

    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    api_url = os.getenv("API_URL", "http://localhost:8000")

    checkout = await chargily.create_checkout(
        amount=request.amount_dzd,
        currency="dzd",
        success_url=request.success_url or f"{frontend_url}/payment/success?credits={credits_to_add}",
        failure_url=request.failure_url or f"{frontend_url}/payment/failed",
        webhook_url=f"{api_url}/payment/webhook/quick-credits",
        metadata={
            "user_id": str(user.id),
            "credits": credits_to_add,
            "amount_dzd": request.amount_dzd,
            "type": "quick_purchase"
        }
    )

    logger.info(
        f"Quick credits purchase initiated: User {user.id} - {request.amount_dzd} DZD = {credits_to_add} credits"
    )

    return {
        "checkout_url": checkout["checkout_url"],
        "checkout_id": checkout["id"],
        "amount_dzd": request.amount_dzd,
        "credits": credits_to_add
    }


@router.post("/webhook/quick-credits")
async def quick_credits_webhook(
    request: Request,
    chargily: ChargilyClient = Depends(get_chargily)
):
    """
    Webhook for quick credit purchases
    Uses the new credits_service instead of raw SQL
    """
    body = await request.body()
    signature = request.headers.get("signature", "")

    if signature and not chargily.verify_webhook_signature(body, signature):
        logger.error("Quick credits webhook signature verification FAILED")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid webhook signature"
        )

    event = await request.json()
    event_type = event.get("type")

    logger.info(f"Quick credits webhook received: {event_type}")

    if event_type == "checkout.paid":
        checkout_data = event.get("data", {})
        metadata = checkout_data.get("metadata", {})

        user_id = metadata.get("user_id")
        credits = int(metadata.get("credits", 0))
        amount_dzd = metadata.get("amount_dzd", 0)
        checkout_id = checkout_data.get("id")

        if not user_id or not credits:
            logger.error(f"Missing metadata in quick credits webhook: {metadata}")
            return {"status": "error", "message": "Missing metadata"}

        try:
            # Add credits using credits_service
            await credits_service.add_credits(
                user_id=user_id,
                amount=credits,
                transaction_type=TransactionType.PURCHASE,
                description=f"Achat {amount_dzd} DZD = {credits} crédits",
                metadata={
                    "chargily_checkout_id": checkout_id,
                    "amount_dzd": amount_dzd
                }
            )

            logger.info(
                f"Quick credits added! User {user_id}: +{credits} credits "
                f"(Checkout: {checkout_id}, Amount: {amount_dzd} DA)"
            )

        except Exception as e:
            logger.error(f"Failed to add quick credits: {e}")
            return {"status": "error", "message": str(e)}

    return {"status": "ok"}
