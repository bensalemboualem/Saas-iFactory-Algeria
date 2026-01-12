"""
Billing PRO - Modèles Pydantic
==============================
Système complet de crédits SaaS avec plans, usage, transactions
"""

from datetime import datetime, date
from decimal import Decimal
from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel, Field, EmailStr
import uuid


# ============================================
# Enums
# ============================================

class PlanType(str, Enum):
    """Types de plans"""
    FREE = "free"
    STARTER = "starter"
    PRO = "pro"
    ENTERPRISE = "enterprise"
    CUSTOM = "custom"


class BillingCycle(str, Enum):
    """Cycles de facturation"""
    MONTHLY = "monthly"
    YEARLY = "yearly"
    LIFETIME = "lifetime"


class TransactionType(str, Enum):
    """Types de transactions"""
    PURCHASE = "purchase"           # Achat de crédits
    CONSUMPTION = "consumption"     # Utilisation de crédits
    REFUND = "refund"              # Remboursement
    BONUS = "bonus"                # Bonus/Promo
    RESET = "reset"                # Reset mensuel
    ADJUSTMENT = "adjustment"       # Ajustement manuel
    GIFT = "gift"                  # Cadeau/Parrainage


class TransactionStatus(str, Enum):
    """Statuts de transaction"""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentProvider(str, Enum):
    """Fournisseurs de paiement"""
    STRIPE = "stripe"
    CHARGILY = "chargily"        # Paiement Algérie 🇩🇿
    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"
    MANUAL = "manual"


class ServiceType(str, Enum):
    """Types de services consommant des crédits"""
    RAG_QUERY = "rag_query"
    PME_QUICK = "pme_quick"
    PME_FULL = "pme_full"
    PME_PDF = "pme_pdf"
    FISCAL_SIM = "fiscal_simulation"
    CRM_LEAD = "crm_lead"
    CREATIVE_GEN = "creative_generation"
    VOICE_CALL = "voice_call"
    EMAIL_SEND = "email_send"
    COUNCIL = "council"
    ITHY = "ithy"


# ============================================
# Credit Costs Configuration
# ============================================

CREDIT_COSTS: dict[ServiceType, int] = {
    ServiceType.RAG_QUERY: 1,
    ServiceType.PME_QUICK: 1,
    ServiceType.PME_FULL: 5,
    ServiceType.PME_PDF: 1,
    ServiceType.FISCAL_SIM: 2,
    ServiceType.CRM_LEAD: 0,       # Gratuit
    ServiceType.CREATIVE_GEN: 3,
    ServiceType.VOICE_CALL: 10,    # Par minute
    ServiceType.EMAIL_SEND: 1,
    ServiceType.COUNCIL: 8,
    ServiceType.ITHY: 5,
}


# ============================================
# Plan Definitions
# ============================================

class PlanFeatures(BaseModel):
    """Fonctionnalités d'un plan"""
    monthly_credits: int
    max_documents: int
    max_team_members: int
    api_access: bool
    priority_support: bool
    custom_branding: bool
    webhooks: bool
    analytics: bool
    sla_guarantee: Optional[float] = None  # % uptime garanti


class Plan(BaseModel):
    """Définition d'un plan"""
    id: str
    name: str
    type: PlanType
    description: str
    price_monthly: Decimal
    price_yearly: Decimal
    currency: str = "DZD"  # Dinars algériens par défaut
    features: PlanFeatures
    is_active: bool = True
    is_popular: bool = False
    trial_days: int = 0


# Plans prédéfinis
PLANS: dict[PlanType, Plan] = {
    PlanType.FREE: Plan(
        id="plan_free",
        name="Gratuit",
        type=PlanType.FREE,
        description="Découvrez iaFactoryDZ gratuitement",
        price_monthly=Decimal("0"),
        price_yearly=Decimal("0"),
        features=PlanFeatures(
            monthly_credits=50,
            max_documents=10,
            max_team_members=1,
            api_access=False,
            priority_support=False,
            custom_branding=False,
            webhooks=False,
            analytics=False,
        ),
        trial_days=0,
    ),
    PlanType.STARTER: Plan(
        id="plan_starter",
        name="Starter",
        type=PlanType.STARTER,
        description="Pour les entrepreneurs et freelances",
        price_monthly=Decimal("4900"),    # 4 900 DA/mois
        price_yearly=Decimal("49000"),    # ~2 mois gratuits
        features=PlanFeatures(
            monthly_credits=500,
            max_documents=100,
            max_team_members=3,
            api_access=True,
            priority_support=False,
            custom_branding=False,
            webhooks=True,
            analytics=True,
        ),
        trial_days=14,
    ),
    PlanType.PRO: Plan(
        id="plan_pro",
        name="Pro",
        type=PlanType.PRO,
        description="Pour les PME en croissance",
        price_monthly=Decimal("14900"),   # 14 900 DA/mois
        price_yearly=Decimal("149000"),
        features=PlanFeatures(
            monthly_credits=2000,
            max_documents=500,
            max_team_members=10,
            api_access=True,
            priority_support=True,
            custom_branding=True,
            webhooks=True,
            analytics=True,
            sla_guarantee=99.5,
        ),
        is_popular=True,
        trial_days=14,
    ),
    PlanType.ENTERPRISE: Plan(
        id="plan_enterprise",
        name="Enterprise",
        type=PlanType.ENTERPRISE,
        description="Pour les grandes entreprises",
        price_monthly=Decimal("49900"),   # 49 900 DA/mois
        price_yearly=Decimal("499000"),
        features=PlanFeatures(
            monthly_credits=10000,
            max_documents=9999,
            max_team_members=999,
            api_access=True,
            priority_support=True,
            custom_branding=True,
            webhooks=True,
            analytics=True,
            sla_guarantee=99.9,
        ),
        trial_days=30,
    ),
}


# ============================================
# User Credits & Subscription
# ============================================

class UserCredits(BaseModel):
    """Crédits d'un utilisateur"""
    user_id: str
    email: Optional[str] = None
    
    # Crédits actuels
    balance: int = Field(default=0, ge=0)
    bonus_balance: int = Field(default=0, ge=0)  # Crédits bonus (utilisés en premier)
    
    # Plan actif
    plan_type: PlanType = PlanType.FREE
    plan_started_at: Optional[datetime] = None
    plan_expires_at: Optional[datetime] = None
    billing_cycle: BillingCycle = BillingCycle.MONTHLY
    
    # Quotas mensuels
    monthly_limit: int = 50
    monthly_used: int = 0
    cycle_start_date: date = Field(default_factory=date.today)
    cycle_end_date: Optional[date] = None
    
    # Alertes
    low_balance_threshold: int = 20
    low_balance_notified: bool = False
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    @property
    def total_available(self) -> int:
        """Total des crédits disponibles"""
        return self.balance + self.bonus_balance
    
    @property
    def monthly_remaining(self) -> int:
        """Crédits restants pour le mois"""
        return max(0, self.monthly_limit - self.monthly_used)
    
    @property
    def usage_percentage(self) -> float:
        """Pourcentage d'utilisation mensuelle"""
        if self.monthly_limit == 0:
            return 0
        return (self.monthly_used / self.monthly_limit) * 100
    
    @property
    def is_low_balance(self) -> bool:
        """Solde bas ?"""
        return self.total_available <= self.low_balance_threshold


class Subscription(BaseModel):
    """Abonnement utilisateur"""
    id: str = Field(default_factory=lambda: f"sub_{uuid.uuid4().hex[:12]}")
    user_id: str
    
    plan_type: PlanType
    billing_cycle: BillingCycle
    
    # Dates
    started_at: datetime
    current_period_start: datetime
    current_period_end: datetime
    canceled_at: Optional[datetime] = None
    
    # Paiement
    payment_provider: PaymentProvider
    external_subscription_id: Optional[str] = None  # ID Stripe/Chargily
    
    # Prix
    amount: Decimal
    currency: str = "DZD"
    
    # Status
    is_active: bool = True
    auto_renew: bool = True
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


# ============================================
# Transactions
# ============================================

class Transaction(BaseModel):
    """Transaction (achat/consommation de crédits)"""
    id: str = Field(default_factory=lambda: f"txn_{uuid.uuid4().hex[:12]}")
    user_id: str
    
    # Type
    type: TransactionType
    status: TransactionStatus = TransactionStatus.PENDING
    
    # Montants
    credits_amount: int  # Positif = ajout, Négatif = consommation
    balance_before: int
    balance_after: int
    
    # Prix (si achat)
    price_amount: Optional[Decimal] = None
    currency: str = "DZD"
    payment_provider: Optional[PaymentProvider] = None
    external_payment_id: Optional[str] = None
    
    # Service (si consommation)
    service_type: Optional[ServiceType] = None
    service_reference: Optional[str] = None  # ID de l'audit PME, query RAG, etc.
    
    # Metadata
    description: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


class CreditPurchase(BaseModel):
    """Achat de crédits"""
    id: str = Field(default_factory=lambda: f"pur_{uuid.uuid4().hex[:12]}")
    user_id: str
    
    # Package
    credits_amount: int
    price_amount: Decimal
    currency: str = "DZD"
    
    # Prix unitaire
    price_per_credit: Decimal
    discount_percentage: float = 0
    
    # Paiement
    payment_provider: PaymentProvider
    payment_status: TransactionStatus = TransactionStatus.PENDING
    external_payment_id: Optional[str] = None
    payment_url: Optional[str] = None  # URL de paiement Chargily
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now)
    paid_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None  # Expiration du lien de paiement


# ============================================
# Usage Statistics
# ============================================

class DailyUsage(BaseModel):
    """Usage quotidien"""
    date: date
    user_id: str
    
    # Par service
    rag_queries: int = 0
    pme_quick: int = 0
    pme_full: int = 0
    fiscal_simulations: int = 0
    creative_generations: int = 0
    voice_minutes: int = 0
    emails_sent: int = 0
    
    # Totaux
    total_requests: int = 0
    total_credits_used: int = 0


class MonthlyUsage(BaseModel):
    """Usage mensuel"""
    month: str  # Format: "2025-11"
    user_id: str
    
    # Totaux
    total_credits_used: int = 0
    total_credits_purchased: int = 0
    total_amount_spent: Decimal = Decimal("0")
    
    # Par service
    usage_by_service: dict[str, int] = Field(default_factory=dict)
    
    # Stats
    peak_day: Optional[date] = None
    peak_usage: int = 0
    average_daily_usage: float = 0


class UsageAlert(BaseModel):
    """Alerte d'usage"""
    id: str = Field(default_factory=lambda: f"alert_{uuid.uuid4().hex[:12]}")
    user_id: str
    
    alert_type: str  # "low_balance", "quota_80", "quota_100", "unusual_activity"
    message: str
    threshold_value: Optional[int] = None
    current_value: Optional[int] = None
    
    is_read: bool = False
    is_email_sent: bool = False
    
    created_at: datetime = Field(default_factory=datetime.now)


# ============================================
# Credit Packages (Achats ponctuels)
# ============================================

class CreditPackage(BaseModel):
    """Package de crédits à acheter"""
    id: str
    name: str
    credits: int
    price: Decimal
    currency: str = "DZD"
    price_per_credit: Decimal
    discount_percentage: float = 0
    is_popular: bool = False
    is_active: bool = True


# Packages prédéfinis
CREDIT_PACKAGES: list[CreditPackage] = [
    CreditPackage(
        id="pack_100",
        name="100 Crédits",
        credits=100,
        price=Decimal("990"),       # 990 DA
        price_per_credit=Decimal("9.9"),
    ),
    CreditPackage(
        id="pack_500",
        name="500 Crédits",
        credits=500,
        price=Decimal("3990"),      # 3 990 DA
        price_per_credit=Decimal("7.98"),
        discount_percentage=20,
        is_popular=True,
    ),
    CreditPackage(
        id="pack_1000",
        name="1000 Crédits",
        credits=1000,
        price=Decimal("6990"),      # 6 990 DA
        price_per_credit=Decimal("6.99"),
        discount_percentage=30,
    ),
    CreditPackage(
        id="pack_5000",
        name="5000 Crédits",
        credits=5000,
        price=Decimal("29900"),     # 29 900 DA
        price_per_credit=Decimal("5.98"),
        discount_percentage=40,
    ),
]


# ============================================
# API Response Models
# ============================================

class CreditsResponse(BaseModel):
    """Réponse API crédits"""
    success: bool
    user_id: str
    balance: int
    bonus_balance: int
    total_available: int
    plan: PlanType
    monthly_limit: int
    monthly_used: int
    monthly_remaining: int
    usage_percentage: float
    is_low_balance: bool
    cycle_end_date: Optional[date] = None


class ConsumeCreditsRequest(BaseModel):
    """Requête de consommation de crédits"""
    service_type: ServiceType
    service_reference: Optional[str] = None
    credits_override: Optional[int] = None  # Pour override le coût par défaut
    metadata: dict[str, Any] = Field(default_factory=dict)


class ConsumeCreditsResponse(BaseModel):
    """Réponse de consommation"""
    success: bool
    credits_consumed: int
    balance_before: int
    balance_after: int
    transaction_id: str
    service_type: ServiceType


class PurchaseRequest(BaseModel):
    """Requête d'achat de crédits"""
    package_id: Optional[str] = None
    credits_amount: Optional[int] = None  # Si achat custom
    payment_provider: PaymentProvider = PaymentProvider.CHARGILY


class PurchaseResponse(BaseModel):
    """Réponse d'achat"""
    success: bool
    purchase_id: str
    credits_amount: int
    price_amount: float
    currency: str
    payment_url: Optional[str] = None
    payment_provider: PaymentProvider
    expires_at: Optional[datetime] = None


class WebhookPayload(BaseModel):
    """Payload webhook paiement"""
    provider: PaymentProvider
    event_type: str
    payment_id: str
    status: str
    amount: Optional[Decimal] = None
    currency: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)
    raw_payload: Optional[dict] = None


class UsageStatsResponse(BaseModel):
    """Réponse statistiques d'usage"""
    user_id: str
    period: str  # "daily", "monthly", "all_time"
    
    total_credits_used: int
    total_credits_purchased: int
    total_amount_spent: float
    
    usage_by_service: dict[str, int]
    usage_by_day: Optional[list[dict]] = None
    
    current_balance: int
    plan: PlanType
