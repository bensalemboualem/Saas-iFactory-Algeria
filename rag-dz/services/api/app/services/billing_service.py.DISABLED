"""
Billing PRO - Service
=====================
Logique métier complète pour gestion des crédits SaaS
"""

import uuid
from datetime import datetime, date, timedelta
from decimal import Decimal
from typing import Optional
import logging

from ..models.billing_models import (
    # Enums
    PlanType, BillingCycle, TransactionType, TransactionStatus,
    PaymentProvider, ServiceType,
    # Models
    UserCredits, Subscription, Transaction, CreditPurchase,
    DailyUsage, MonthlyUsage, UsageAlert,
    Plan, CreditPackage,
    # Constants
    CREDIT_COSTS, PLANS, CREDIT_PACKAGES,
    # Responses
    CreditsResponse, ConsumeCreditsResponse, PurchaseResponse,
)

logger = logging.getLogger(__name__)


# ============================================
# In-Memory Storage (à remplacer par PostgreSQL)
# ============================================

users_credits: dict[str, UserCredits] = {}
subscriptions: dict[str, Subscription] = {}
transactions: list[Transaction] = []
purchases: dict[str, CreditPurchase] = {}
daily_usage: dict[str, DailyUsage] = {}  # Key: "user_id:date"
monthly_usage: dict[str, MonthlyUsage] = {}  # Key: "user_id:month"
alerts: list[UsageAlert] = []


# ============================================
# Billing Service
# ============================================

class BillingService:
    """Service de gestion des crédits et facturation"""
    
    def __init__(self):
        self.chargily_api_key: Optional[str] = None
        self.stripe_api_key: Optional[str] = None
    
    # ========================================
    # User Credits Management
    # ========================================
    
    def get_or_create_user_credits(self, user_id: str, email: Optional[str] = None) -> UserCredits:
        """Récupérer ou créer les crédits d'un utilisateur"""
        if user_id not in users_credits:
            # Créer avec le plan gratuit
            plan = PLANS[PlanType.FREE]
            today = date.today()
            
            users_credits[user_id] = UserCredits(
                user_id=user_id,
                email=email,
                balance=plan.features.monthly_credits,
                plan_type=PlanType.FREE,
                plan_started_at=datetime.now(),
                monthly_limit=plan.features.monthly_credits,
                monthly_used=0,
                cycle_start_date=today,
                cycle_end_date=today.replace(day=1) + timedelta(days=32),
            )
            
            # Transaction initiale
            self._record_transaction(
                user_id=user_id,
                type=TransactionType.BONUS,
                credits_amount=plan.features.monthly_credits,
                description=f"Crédits de bienvenue - Plan {plan.name}",
            )
            
            logger.info(f"Created credits for user {user_id} with {plan.features.monthly_credits} credits")
        
        return users_credits[user_id]
    
    def get_credits_response(self, user_id: str) -> CreditsResponse:
        """Obtenir le résumé des crédits"""
        credits = self.get_or_create_user_credits(user_id)
        
        return CreditsResponse(
            success=True,
            user_id=user_id,
            balance=credits.balance,
            bonus_balance=credits.bonus_balance,
            total_available=credits.total_available,
            plan=credits.plan_type,
            monthly_limit=credits.monthly_limit,
            monthly_used=credits.monthly_used,
            monthly_remaining=credits.monthly_remaining,
            usage_percentage=credits.usage_percentage,
            is_low_balance=credits.is_low_balance,
            cycle_end_date=credits.cycle_end_date,
        )
    
    # ========================================
    # Credit Consumption
    # ========================================
    
    def consume_credits(
        self,
        user_id: str,
        service_type: ServiceType,
        service_reference: Optional[str] = None,
        credits_override: Optional[int] = None,
        metadata: Optional[dict] = None,
    ) -> ConsumeCreditsResponse:
        """
        Consommer des crédits pour un service
        
        Returns:
            ConsumeCreditsResponse avec succès ou erreur
        
        Raises:
            InsufficientCreditsError si pas assez de crédits
        """
        credits = self.get_or_create_user_credits(user_id)
        
        # Calculer le coût
        cost = credits_override if credits_override is not None else CREDIT_COSTS.get(service_type, 1)
        
        # Service gratuit ?
        if cost == 0:
            return ConsumeCreditsResponse(
                success=True,
                credits_consumed=0,
                balance_before=credits.total_available,
                balance_after=credits.total_available,
                transaction_id="free_service",
                service_type=service_type,
            )
        
        # Vérifier le solde
        if credits.total_available < cost:
            logger.warning(f"Insufficient credits for user {user_id}: {credits.total_available} < {cost}")
            return ConsumeCreditsResponse(
                success=False,
                credits_consumed=0,
                balance_before=credits.total_available,
                balance_after=credits.total_available,
                transaction_id="insufficient_credits",
                service_type=service_type,
            )
        
        balance_before = credits.total_available
        
        # Consommer les bonus d'abord
        remaining_cost = cost
        bonus_consumed = 0
        regular_consumed = 0
        
        if credits.bonus_balance > 0:
            bonus_consumed = min(credits.bonus_balance, remaining_cost)
            credits.bonus_balance -= bonus_consumed
            remaining_cost -= bonus_consumed
        
        if remaining_cost > 0:
            regular_consumed = remaining_cost
            credits.balance -= regular_consumed
        
        # Mettre à jour l'usage mensuel
        credits.monthly_used += cost
        credits.updated_at = datetime.now()
        
        # Enregistrer la transaction
        txn = self._record_transaction(
            user_id=user_id,
            type=TransactionType.CONSUMPTION,
            credits_amount=-cost,
            description=f"Consommation {service_type.value}",
            service_type=service_type,
            service_reference=service_reference,
            metadata=metadata or {},
        )
        
        # Mettre à jour l'usage quotidien
        self._update_daily_usage(user_id, service_type, cost)
        
        # Vérifier les alertes
        self._check_alerts(user_id, credits)
        
        logger.info(f"User {user_id} consumed {cost} credits for {service_type.value}")
        
        return ConsumeCreditsResponse(
            success=True,
            credits_consumed=cost,
            balance_before=balance_before,
            balance_after=credits.total_available,
            transaction_id=txn.id,
            service_type=service_type,
        )
    
    def can_consume(self, user_id: str, service_type: ServiceType) -> tuple[bool, int, int]:
        """
        Vérifier si l'utilisateur peut consommer des crédits
        
        Returns:
            (can_consume, cost, available_balance)
        """
        credits = self.get_or_create_user_credits(user_id)
        cost = CREDIT_COSTS.get(service_type, 1)
        
        if cost == 0:
            return True, 0, credits.total_available
        
        return credits.total_available >= cost, cost, credits.total_available
    
    # ========================================
    # Credit Purchase
    # ========================================
    
    def create_purchase(
        self,
        user_id: str,
        package_id: Optional[str] = None,
        custom_credits: Optional[int] = None,
        payment_provider: PaymentProvider = PaymentProvider.CHARGILY,
    ) -> PurchaseResponse:
        """Créer un achat de crédits"""
        
        # Trouver le package
        package = None
        if package_id:
            package = next((p for p in CREDIT_PACKAGES if p.id == package_id), None)
            if not package:
                return PurchaseResponse(
                    success=False,
                    purchase_id="",
                    credits_amount=0,
                    price_amount=0,
                    currency="DZD",
                    payment_provider=payment_provider,
                )
        
        # Calculer le montant
        if package:
            credits_amount = package.credits
            price_amount = package.price
            price_per_credit = package.price_per_credit
        elif custom_credits:
            credits_amount = custom_credits
            price_per_credit = Decimal("9.9")  # Prix par défaut
            price_amount = Decimal(str(custom_credits)) * price_per_credit
        else:
            return PurchaseResponse(
                success=False,
                purchase_id="",
                credits_amount=0,
                price_amount=0,
                currency="DZD",
                payment_provider=payment_provider,
            )
        
        # Créer l'achat
        purchase = CreditPurchase(
            user_id=user_id,
            credits_amount=credits_amount,
            price_amount=price_amount,
            price_per_credit=price_per_credit,
            payment_provider=payment_provider,
            expires_at=datetime.now() + timedelta(hours=24),
        )
        
        purchases[purchase.id] = purchase
        
        # Générer l'URL de paiement (simulé)
        payment_url = None
        if payment_provider == PaymentProvider.CHARGILY:
            payment_url = f"https://pay.chargily.com/test/{purchase.id}"
        elif payment_provider == PaymentProvider.STRIPE:
            payment_url = f"https://checkout.stripe.com/test/{purchase.id}"
        
        purchase.payment_url = payment_url
        
        logger.info(f"Created purchase {purchase.id} for user {user_id}: {credits_amount} credits = {price_amount} DZD")
        
        return PurchaseResponse(
            success=True,
            purchase_id=purchase.id,
            credits_amount=credits_amount,
            price_amount=float(price_amount),
            currency="DZD",
            payment_url=payment_url,
            payment_provider=payment_provider,
            expires_at=purchase.expires_at,
        )
    
    def confirm_purchase(self, purchase_id: str, payment_id: str) -> bool:
        """Confirmer un achat après paiement réussi"""
        if purchase_id not in purchases:
            logger.error(f"Purchase {purchase_id} not found")
            return False
        
        purchase = purchases[purchase_id]
        
        if purchase.payment_status == TransactionStatus.COMPLETED:
            logger.warning(f"Purchase {purchase_id} already completed")
            return True
        
        # Marquer comme payé
        purchase.payment_status = TransactionStatus.COMPLETED
        purchase.external_payment_id = payment_id
        purchase.paid_at = datetime.now()
        
        # Ajouter les crédits
        credits = self.get_or_create_user_credits(purchase.user_id)
        credits.balance += purchase.credits_amount
        credits.updated_at = datetime.now()
        
        # Enregistrer la transaction
        self._record_transaction(
            user_id=purchase.user_id,
            type=TransactionType.PURCHASE,
            credits_amount=purchase.credits_amount,
            description=f"Achat de {purchase.credits_amount} crédits",
            price_amount=purchase.price_amount,
            payment_provider=purchase.payment_provider,
            external_payment_id=payment_id,
        )
        
        logger.info(f"Purchase {purchase_id} confirmed: {purchase.credits_amount} credits added to user {purchase.user_id}")
        
        return True
    
    # ========================================
    # Subscription Management
    # ========================================
    
    def upgrade_plan(
        self,
        user_id: str,
        new_plan: PlanType,
        billing_cycle: BillingCycle = BillingCycle.MONTHLY,
        payment_provider: PaymentProvider = PaymentProvider.CHARGILY,
    ) -> dict:
        """Upgrader le plan d'un utilisateur"""
        
        if new_plan not in PLANS:
            return {"success": False, "error": "Plan invalide"}
        
        plan = PLANS[new_plan]
        credits = self.get_or_create_user_credits(user_id)
        
        # Calculer le prix
        price = plan.price_yearly if billing_cycle == BillingCycle.YEARLY else plan.price_monthly
        
        # Créer l'abonnement
        now = datetime.now()
        period_end = now + timedelta(days=365 if billing_cycle == BillingCycle.YEARLY else 30)
        
        subscription = Subscription(
            user_id=user_id,
            plan_type=new_plan,
            billing_cycle=billing_cycle,
            started_at=now,
            current_period_start=now,
            current_period_end=period_end,
            payment_provider=payment_provider,
            amount=price,
            currency="DZD",
        )
        
        subscriptions[subscription.id] = subscription
        
        # Mettre à jour les crédits
        credits.plan_type = new_plan
        credits.plan_started_at = now
        credits.plan_expires_at = period_end
        credits.billing_cycle = billing_cycle
        credits.monthly_limit = plan.features.monthly_credits
        
        # Ajouter les crédits du nouveau plan
        bonus_credits = plan.features.monthly_credits - credits.monthly_used
        if bonus_credits > 0:
            credits.balance += bonus_credits
            self._record_transaction(
                user_id=user_id,
                type=TransactionType.BONUS,
                credits_amount=bonus_credits,
                description=f"Upgrade vers plan {plan.name}",
            )
        
        logger.info(f"User {user_id} upgraded to {new_plan.value} plan")
        
        return {
            "success": True,
            "subscription_id": subscription.id,
            "plan": new_plan.value,
            "price": float(price),
            "currency": "DZD",
            "period_end": period_end.isoformat(),
        }
    
    def cancel_subscription(self, user_id: str) -> bool:
        """Annuler l'abonnement (fin de période)"""
        user_subs = [s for s in subscriptions.values() if s.user_id == user_id and s.is_active]
        
        if not user_subs:
            return False
        
        for sub in user_subs:
            sub.canceled_at = datetime.now()
            sub.auto_renew = False
        
        logger.info(f"Subscription canceled for user {user_id}")
        return True
    
    # ========================================
    # Monthly Reset
    # ========================================
    
    def reset_monthly_credits(self, user_id: str) -> bool:
        """Reset mensuel des crédits"""
        if user_id not in users_credits:
            return False
        
        credits = users_credits[user_id]
        plan = PLANS.get(credits.plan_type, PLANS[PlanType.FREE])
        
        old_used = credits.monthly_used
        
        # Reset l'usage
        credits.monthly_used = 0
        credits.cycle_start_date = date.today()
        credits.cycle_end_date = date.today().replace(day=1) + timedelta(days=32)
        
        # Remettre les crédits mensuels
        credits.balance = plan.features.monthly_credits
        credits.low_balance_notified = False
        credits.updated_at = datetime.now()
        
        # Enregistrer la transaction
        self._record_transaction(
            user_id=user_id,
            type=TransactionType.RESET,
            credits_amount=plan.features.monthly_credits,
            description=f"Reset mensuel - Plan {plan.name}",
            metadata={"previous_used": old_used},
        )
        
        logger.info(f"Monthly reset for user {user_id}: {plan.features.monthly_credits} credits")
        
        return True
    
    # ========================================
    # Usage Statistics
    # ========================================
    
    def get_usage_stats(self, user_id: str, period: str = "monthly") -> dict:
        """Obtenir les statistiques d'usage"""
        
        # Filtrer les transactions
        user_txns = [t for t in transactions if t.user_id == user_id]
        
        # Consommations uniquement
        consumptions = [t for t in user_txns if t.type == TransactionType.CONSUMPTION]
        
        # Par service
        usage_by_service = {}
        for txn in consumptions:
            if txn.service_type:
                service = txn.service_type.value
                usage_by_service[service] = usage_by_service.get(service, 0) + abs(txn.credits_amount)
        
        # Totaux
        total_consumed = sum(abs(t.credits_amount) for t in consumptions)
        total_purchased = sum(t.credits_amount for t in user_txns if t.type == TransactionType.PURCHASE)
        total_spent = sum(float(t.price_amount or 0) for t in user_txns if t.type == TransactionType.PURCHASE)
        
        credits = self.get_or_create_user_credits(user_id)
        
        return {
            "user_id": user_id,
            "period": period,
            "total_credits_used": total_consumed,
            "total_credits_purchased": total_purchased,
            "total_amount_spent": total_spent,
            "usage_by_service": usage_by_service,
            "current_balance": credits.total_available,
            "plan": credits.plan_type.value,
        }
    
    def get_transaction_history(
        self,
        user_id: str,
        limit: int = 50,
        offset: int = 0,
        type_filter: Optional[TransactionType] = None,
    ) -> list[Transaction]:
        """Obtenir l'historique des transactions"""
        user_txns = [t for t in transactions if t.user_id == user_id]
        
        if type_filter:
            user_txns = [t for t in user_txns if t.type == type_filter]
        
        # Trier par date décroissante
        user_txns.sort(key=lambda t: t.created_at, reverse=True)
        
        return user_txns[offset:offset + limit]
    
    # ========================================
    # Webhooks
    # ========================================
    
    def handle_chargily_webhook(self, payload: dict) -> bool:
        """Traiter un webhook Chargily"""
        event_type = payload.get("type")
        data = payload.get("data", {})
        
        if event_type == "checkout.paid":
            # Paiement réussi
            checkout_id = data.get("id")
            metadata = data.get("metadata", {})
            purchase_id = metadata.get("purchase_id")
            
            if purchase_id:
                return self.confirm_purchase(purchase_id, checkout_id)
        
        elif event_type == "checkout.failed":
            # Paiement échoué
            checkout_id = data.get("id")
            metadata = data.get("metadata", {})
            purchase_id = metadata.get("purchase_id")
            
            if purchase_id and purchase_id in purchases:
                purchases[purchase_id].payment_status = TransactionStatus.FAILED
                logger.warning(f"Payment failed for purchase {purchase_id}")
        
        return True
    
    def handle_stripe_webhook(self, payload: dict) -> bool:
        """Traiter un webhook Stripe"""
        event_type = payload.get("type")
        data = payload.get("data", {}).get("object", {})
        
        if event_type == "checkout.session.completed":
            session_id = data.get("id")
            metadata = data.get("metadata", {})
            purchase_id = metadata.get("purchase_id")
            
            if purchase_id:
                return self.confirm_purchase(purchase_id, session_id)
        
        elif event_type == "invoice.paid":
            # Renouvellement d'abonnement
            subscription_id = data.get("subscription")
            customer_id = data.get("customer")
            # TODO: Renouveler les crédits
        
        return True
    
    # ========================================
    # Private Helpers
    # ========================================
    
    def _record_transaction(
        self,
        user_id: str,
        type: TransactionType,
        credits_amount: int,
        description: str,
        service_type: Optional[ServiceType] = None,
        service_reference: Optional[str] = None,
        price_amount: Optional[Decimal] = None,
        payment_provider: Optional[PaymentProvider] = None,
        external_payment_id: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> Transaction:
        """Enregistrer une transaction"""
        
        credits = users_credits.get(user_id)
        balance_before = credits.total_available + abs(credits_amount) if credits else 0
        balance_after = credits.total_available if credits else credits_amount
        
        txn = Transaction(
            user_id=user_id,
            type=type,
            status=TransactionStatus.COMPLETED,
            credits_amount=credits_amount,
            balance_before=balance_before,
            balance_after=balance_after,
            description=description,
            service_type=service_type,
            service_reference=service_reference,
            price_amount=price_amount,
            payment_provider=payment_provider,
            external_payment_id=external_payment_id,
            metadata=metadata or {},
            completed_at=datetime.now(),
        )
        
        transactions.append(txn)
        return txn
    
    def _update_daily_usage(self, user_id: str, service_type: ServiceType, credits: int):
        """Mettre à jour l'usage quotidien"""
        today = date.today()
        key = f"{user_id}:{today.isoformat()}"
        
        if key not in daily_usage:
            daily_usage[key] = DailyUsage(date=today, user_id=user_id)
        
        usage = daily_usage[key]
        usage.total_requests += 1
        usage.total_credits_used += credits
        
        # Mettre à jour le compteur spécifique
        if service_type == ServiceType.RAG_QUERY:
            usage.rag_queries += 1
        elif service_type == ServiceType.PME_QUICK:
            usage.pme_quick += 1
        elif service_type == ServiceType.PME_FULL:
            usage.pme_full += 1
        elif service_type == ServiceType.FISCAL_SIM:
            usage.fiscal_simulations += 1
        elif service_type == ServiceType.CREATIVE_GEN:
            usage.creative_generations += 1
    
    def _check_alerts(self, user_id: str, credits: UserCredits):
        """Vérifier et créer des alertes si nécessaire"""
        
        # Alerte solde bas
        if credits.is_low_balance and not credits.low_balance_notified:
            alert = UsageAlert(
                user_id=user_id,
                alert_type="low_balance",
                message=f"Votre solde est bas : {credits.total_available} crédits restants",
                threshold_value=credits.low_balance_threshold,
                current_value=credits.total_available,
            )
            alerts.append(alert)
            credits.low_balance_notified = True
            logger.info(f"Low balance alert for user {user_id}")
        
        # Alerte quota 80%
        if credits.usage_percentage >= 80 and credits.usage_percentage < 100:
            # Vérifier si alerte déjà envoyée aujourd'hui
            today_alerts = [
                a for a in alerts 
                if a.user_id == user_id 
                and a.alert_type == "quota_80"
                and a.created_at.date() == date.today()
            ]
            
            if not today_alerts:
                alert = UsageAlert(
                    user_id=user_id,
                    alert_type="quota_80",
                    message=f"Vous avez utilisé {credits.usage_percentage:.0f}% de votre quota mensuel",
                    current_value=int(credits.usage_percentage),
                )
                alerts.append(alert)
        
        # Alerte quota 100%
        if credits.monthly_used >= credits.monthly_limit:
            today_alerts = [
                a for a in alerts 
                if a.user_id == user_id 
                and a.alert_type == "quota_100"
                and a.created_at.date() == date.today()
            ]
            
            if not today_alerts:
                alert = UsageAlert(
                    user_id=user_id,
                    alert_type="quota_100",
                    message="Vous avez atteint votre quota mensuel",
                )
                alerts.append(alert)


# Singleton
billing_service = BillingService()
