"""
Team Seats Models
=================
Modèles pour gestion des seats ChatGPT Team et autres abonnements IA gérés
"""

from datetime import datetime, date
from decimal import Decimal
from enum import Enum
from typing import Optional, Any, List
from pydantic import BaseModel, Field, EmailStr
import uuid


# ============================================
# Enums
# ============================================

class TeamSeatProvider(str, Enum):
    """Providers avec offres Team/Enterprise"""
    OPENAI_TEAM = "openai_team"          # ChatGPT Team
    OPENAI_ENTERPRISE = "openai_enterprise"  # ChatGPT Enterprise
    ANTHROPIC_TEAM = "anthropic_team"    # Claude for Teams (future)
    NOTION_AI = "notion_ai"              # Notion AI
    GITHUB_COPILOT = "github_copilot"    # GitHub Copilot Business
    CURSOR_PRO = "cursor_pro"            # Cursor Pro
    OTHER = "other"


class TeamSeatStatus(str, Enum):
    """Statuts d'un seat"""
    PENDING = "pending"          # Demande en attente
    PAYMENT_PENDING = "payment_pending"  # En attente de paiement
    PROCESSING = "processing"    # Paiement reçu, activation en cours
    ACTIVE = "active"            # Actif
    SUSPENDED = "suspended"      # Suspendu (impayé)
    CANCELED = "canceled"        # Annulé
    EXPIRED = "expired"          # Expiré


class SeatRequestPriority(str, Enum):
    """Priorité d'une demande"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


# ============================================
# Team Seat Model
# ============================================

class TeamSeat(BaseModel):
    """Seat géré pour un utilisateur"""
    id: str = Field(default_factory=lambda: f"seat_{uuid.uuid4().hex[:12]}")
    
    # Utilisateur
    user_id: str
    user_email: EmailStr
    user_name: Optional[str] = None
    
    # Provider & Plan
    provider: TeamSeatProvider
    plan_name: str  # Ex: "ChatGPT Team", "GitHub Copilot Business"
    
    # Status
    status: TeamSeatStatus = TeamSeatStatus.PENDING
    status_reason: Optional[str] = None
    
    # Prix
    price_dzd_month: Decimal  # Prix en DZD/mois
    cost_usd_month: Decimal   # Coût réel en USD/mois
    margin_percentage: float = 20.0  # Marge IAFactory
    
    # Facturation
    billing_cycle_day: int = 1  # Jour de facturation
    next_billing_date: Optional[date] = None
    last_payment_date: Optional[date] = None
    
    # Metadata
    notes: Optional[str] = None
    admin_notes: Optional[str] = None  # Notes internes admin
    metadata: dict[str, Any] = Field(default_factory=dict)
    
    # External
    external_seat_id: Optional[str] = None  # ID côté provider (si disponible)
    external_email: Optional[str] = None    # Email utilisé côté provider
    
    # Timestamps
    requested_at: datetime = Field(default_factory=datetime.now)
    activated_at: Optional[datetime] = None
    suspended_at: Optional[datetime] = None
    canceled_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


# ============================================
# Seat Request Model
# ============================================

class SeatRequest(BaseModel):
    """Demande de seat"""
    id: str = Field(default_factory=lambda: f"req_{uuid.uuid4().hex[:12]}")
    
    # Demandeur
    user_id: str
    user_email: EmailStr
    user_name: Optional[str] = None
    phone: Optional[str] = None
    
    # Demande
    provider: TeamSeatProvider
    plan_requested: str
    priority: SeatRequestPriority = SeatRequestPriority.NORMAL
    
    # Message
    message: Optional[str] = None
    reason: Optional[str] = None  # Pourquoi ce seat
    
    # Status
    status: str = "pending"  # pending, approved, rejected, converted
    admin_response: Optional[str] = None
    
    # Résultat
    seat_id: Optional[str] = None  # Si converti en seat
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now)
    processed_at: Optional[datetime] = None


# ============================================
# Pricing Configuration
# ============================================

class SeatPricing(BaseModel):
    """Configuration de prix pour un type de seat"""
    provider: TeamSeatProvider
    plan_name: str
    
    # Prix USD (coût réel)
    cost_usd_month: Decimal
    
    # Prix DZD (vente)
    price_dzd_month: Decimal
    
    # Setup fee
    setup_fee_dzd: Decimal = Decimal("0")
    
    # Infos
    description: str
    features: List[str]
    
    is_available: bool = True
    max_seats: Optional[int] = None  # Limite de seats disponibles


# Pricing prédéfini
SEAT_PRICING: dict[TeamSeatProvider, SeatPricing] = {
    TeamSeatProvider.OPENAI_TEAM: SeatPricing(
        provider=TeamSeatProvider.OPENAI_TEAM,
        plan_name="ChatGPT Team",
        cost_usd_month=Decimal("25.00"),
        price_dzd_month=Decimal("6900"),  # ~6900 DA/mois
        setup_fee_dzd=Decimal("0"),
        description="Accès ChatGPT Team officiel via IAFactory",
        features=[
            "GPT-4o avec limite élevée",
            "Création d'images DALL-E 3",
            "Analyse de données avancée",
            "Workspace partagé",
            "Pas d'entraînement sur vos données",
            "Support prioritaire",
        ],
        is_available=True,
        max_seats=50,
    ),
    TeamSeatProvider.GITHUB_COPILOT: SeatPricing(
        provider=TeamSeatProvider.GITHUB_COPILOT,
        plan_name="GitHub Copilot Business",
        cost_usd_month=Decimal("19.00"),
        price_dzd_month=Decimal("5400"),  # ~5400 DA/mois
        setup_fee_dzd=Decimal("0"),
        description="GitHub Copilot pour développeurs professionnels",
        features=[
            "Complétion de code IA",
            "Support multi-IDE (VS Code, JetBrains...)",
            "Chat Copilot intégré",
            "Suggestions contextuelles",
            "Gestion centralisée",
        ],
        is_available=True,
        max_seats=100,
    ),
    TeamSeatProvider.CURSOR_PRO: SeatPricing(
        provider=TeamSeatProvider.CURSOR_PRO,
        plan_name="Cursor Pro",
        cost_usd_month=Decimal("20.00"),
        price_dzd_month=Decimal("5700"),  # ~5700 DA/mois
        setup_fee_dzd=Decimal("0"),
        description="Cursor Pro - L'IDE IA nouvelle génération",
        features=[
            "GPT-4 + Claude intégrés",
            "500 requêtes rapides/mois",
            "Requêtes lentes illimitées",
            "10 utilisations Claude Opus/jour",
            "Codebase indexing",
        ],
        is_available=True,
        max_seats=50,
    ),
    TeamSeatProvider.NOTION_AI: SeatPricing(
        provider=TeamSeatProvider.NOTION_AI,
        plan_name="Notion AI",
        cost_usd_month=Decimal("10.00"),
        price_dzd_month=Decimal("2900"),  # ~2900 DA/mois
        setup_fee_dzd=Decimal("0"),
        description="Notion AI pour productivité",
        features=[
            "Génération de contenu",
            "Résumés automatiques",
            "Amélioration de texte",
            "Traduction",
            "Extraction d'actions",
        ],
        is_available=True,
        max_seats=100,
    ),
}


# ============================================
# API Response Models
# ============================================

class SeatRequestInput(BaseModel):
    """Input pour demander un seat"""
    email: EmailStr
    name: Optional[str] = None
    phone: Optional[str] = None
    provider: TeamSeatProvider
    plan: Optional[str] = None
    message: Optional[str] = None


class SeatRequestResponse(BaseModel):
    """Réponse à une demande de seat"""
    success: bool
    request_id: str
    message: str
    estimated_processing_time: str = "24-48h"
    next_steps: List[str]


class MySeatResponse(BaseModel):
    """Réponse pour voir ses seats"""
    success: bool
    seats: List[TeamSeat]
    total: int


class SeatPricingResponse(BaseModel):
    """Réponse pricing"""
    success: bool
    plans: List[dict]


class AdminSeatUpdateInput(BaseModel):
    """Input admin pour update un seat"""
    status: Optional[TeamSeatStatus] = None
    status_reason: Optional[str] = None
    external_seat_id: Optional[str] = None
    external_email: Optional[str] = None
    admin_notes: Optional[str] = None
    next_billing_date: Optional[date] = None
