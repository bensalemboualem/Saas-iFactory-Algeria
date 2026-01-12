"""
CRM PRO - Modèles Pydantic
==========================
HubSpot DZ/CH powered by IA
Pipeline Kanban + Scoring IA + Actions automatiques
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr


# ============================================
# ENUMS
# ============================================

class LeadStatus(str, Enum):
    """Statut du lead dans le pipeline Kanban"""
    NEW = "new"              # Nouveau lead
    QUALIFY = "qualify"      # À qualifier
    WARM = "warm"            # Lead chaud
    PROPOSAL = "proposal"    # Proposition envoyée
    WON = "won"              # Gagné ✅
    LOST = "lost"            # Perdu ❌


class LeadSource(str, Enum):
    """Source d'acquisition du lead"""
    WEBSITE = "website"           # Site web iaFactory
    PME_ANALYZER = "pme"          # PME Analyzer
    FILE_AI = "fileai"            # FileAI / Upload
    REFERRAL = "referral"         # Recommandation
    SOCIAL = "social"             # Réseaux sociaux
    ADS = "ads"                   # Publicité
    COLD_CALL = "cold_call"       # Prospection téléphonique
    EMAIL = "email"               # Email entrant
    WHATSAPP = "whatsapp"         # WhatsApp
    PARTNER = "partner"           # Partenaire
    EVENT = "event"               # Événement / Salon
    OTHER = "other"               # Autre


class LeadPriority(str, Enum):
    """Priorité du lead"""
    LOW = "low"           # Basse
    MEDIUM = "medium"     # Moyenne
    HIGH = "high"         # Haute
    URGENT = "urgent"     # Urgente


class ActionType(str, Enum):
    """Type d'action à effectuer"""
    CALL = "call"                    # Appeler
    EMAIL = "email"                  # Envoyer email
    WHATSAPP = "whatsapp"            # Envoyer WhatsApp
    MEETING = "meeting"              # Planifier RDV
    PROPOSAL = "proposal"            # Envoyer proposition
    FOLLOW_UP = "follow_up"          # Relancer
    DEMO = "demo"                    # Faire une démo
    AUDIT = "audit"                  # Proposer audit PME
    DOCUMENT = "document"            # Demander documents
    CLOSE = "close"                  # Conclure


class Sector(str, Enum):
    """Secteur d'activité"""
    COMMERCE = "commerce"            # Commerce / Retail
    SERVICES = "services"            # Services
    TECH = "tech"                    # Technologie
    INDUSTRY = "industry"            # Industrie
    CONSTRUCTION = "construction"    # BTP / Construction
    HEALTH = "health"                # Santé
    EDUCATION = "education"          # Éducation
    FINANCE = "finance"              # Finance / Banque
    REAL_ESTATE = "real_estate"      # Immobilier
    AGRICULTURE = "agriculture"      # Agriculture
    TRANSPORT = "transport"          # Transport / Logistique
    FOOD = "food"                    # Agroalimentaire
    TOURISM = "tourism"              # Tourisme / Hôtellerie
    LEGAL = "legal"                  # Juridique
    CONSULTING = "consulting"        # Conseil
    OTHER = "other"                  # Autre


# ============================================
# LEAD PRO MODELS
# ============================================

class LeadProBase(BaseModel):
    """Base pour Lead PRO"""
    name: str = Field(..., min_length=2, max_length=200, description="Nom du contact ou entreprise")
    email: Optional[EmailStr] = Field(None, description="Email du contact")
    phone: Optional[str] = Field(None, max_length=20, description="Téléphone")
    company: Optional[str] = Field(None, max_length=200, description="Nom de l'entreprise")
    sector: Optional[Sector] = Field(None, description="Secteur d'activité")
    source: LeadSource = Field(LeadSource.WEBSITE, description="Source du lead")
    
    # Informations supplémentaires
    job_title: Optional[str] = Field(None, max_length=100, description="Poste du contact")
    employees_count: Optional[int] = Field(None, ge=1, description="Nombre d'employés")
    annual_revenue: Optional[Decimal] = Field(None, description="CA annuel (DZD)")
    country: str = Field("DZ", description="Pays (DZ, CH, FR...)")
    city: Optional[str] = Field(None, max_length=100, description="Ville")
    wilaya: Optional[str] = Field(None, max_length=100, description="Wilaya (Algérie)")
    
    # Besoin exprimé
    need_description: Optional[str] = Field(None, max_length=2000, description="Description du besoin")
    budget: Optional[Decimal] = Field(None, description="Budget estimé (DZD)")
    urgency: Optional[str] = Field(None, description="Niveau d'urgence")
    
    # Notes
    notes: Optional[str] = Field(None, description="Notes internes")


class LeadProCreate(LeadProBase):
    """Création d'un lead PRO"""
    # Optionnels pour création auto
    status: Optional[LeadStatus] = Field(None, description="Statut (auto si non fourni)")
    priority: Optional[LeadPriority] = Field(None, description="Priorité (auto si non fourni)")
    
    # Métadonnées
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Métadonnées custom")


class LeadProUpdate(BaseModel):
    """Mise à jour d'un lead PRO"""
    name: Optional[str] = Field(None, min_length=2, max_length=200)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    company: Optional[str] = Field(None, max_length=200)
    sector: Optional[Sector] = None
    source: Optional[LeadSource] = None
    status: Optional[LeadStatus] = None
    priority: Optional[LeadPriority] = None
    
    job_title: Optional[str] = Field(None, max_length=100)
    employees_count: Optional[int] = Field(None, ge=1)
    annual_revenue: Optional[Decimal] = None
    country: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    wilaya: Optional[str] = Field(None, max_length=100)
    
    need_description: Optional[str] = Field(None, max_length=2000)
    budget: Optional[Decimal] = None
    urgency: Optional[str] = None
    notes: Optional[str] = None
    
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class LeadPro(LeadProBase):
    """Lead PRO complet avec scoring IA"""
    id: str = Field(..., description="ID unique du lead")
    status: LeadStatus = Field(LeadStatus.NEW, description="Statut dans le pipeline")
    priority: LeadPriority = Field(LeadPriority.MEDIUM, description="Priorité")
    
    # Scoring IA
    score: int = Field(0, ge=0, le=100, description="Score IA (0-100)")
    confidence: float = Field(0.0, ge=0.0, le=1.0, description="Confiance du score")
    score_reasons: List[str] = Field(default_factory=list, description="Raisons du score")
    
    # Actions IA
    next_action: Optional[str] = Field(None, description="Prochaine action suggérée")
    next_action_type: Optional[ActionType] = Field(None, description="Type d'action")
    next_action_date: Optional[datetime] = Field(None, description="Date suggérée")
    ai_message: Optional[str] = Field(None, description="Message IA généré")
    
    # Métadonnées
    tags: List[str] = Field(default_factory=list, description="Tags")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Métadonnées")
    
    # Statistiques
    interactions_count: int = Field(0, description="Nombre d'interactions")
    last_interaction: Optional[datetime] = Field(None, description="Dernière interaction")
    
    # Assignation
    assigned_to: Optional[str] = Field(None, description="Assigné à (user_id)")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Valeur estimée
    estimated_value: Optional[Decimal] = Field(None, description="Valeur estimée du deal")
    probability: float = Field(0.0, ge=0.0, le=1.0, description="Probabilité de conversion")


# ============================================
# IA MODELS
# ============================================

class LeadAIScoreRequest(BaseModel):
    """Requête de scoring IA"""
    lead_id: Optional[str] = Field(None, description="ID du lead (pour recalcul)")
    lead_data: Optional[LeadProCreate] = Field(None, description="Données du lead (pour nouveau)")


class LeadAIScoreResponse(BaseModel):
    """Réponse scoring IA"""
    score: int = Field(..., ge=0, le=100, description="Score 0-100")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confiance (0-1)")
    probability: float = Field(..., ge=0.0, le=1.0, description="Probabilité de conversion")
    reasons: List[str] = Field(..., description="Raisons du score")
    recommended_status: LeadStatus = Field(..., description="Statut recommandé")
    recommended_priority: LeadPriority = Field(..., description="Priorité recommandée")
    
    # Insights
    strengths: List[str] = Field(default_factory=list, description="Points forts")
    weaknesses: List[str] = Field(default_factory=list, description="Points faibles")
    opportunities: List[str] = Field(default_factory=list, description="Opportunités")


class LeadAIMessageRequest(BaseModel):
    """Requête génération message IA"""
    lead_id: str = Field(..., description="ID du lead")
    channel: str = Field("whatsapp", description="Canal: whatsapp, email, sms")
    message_type: str = Field("first_contact", description="Type: first_contact, follow_up, proposal, thank_you")
    tone: str = Field("professional", description="Ton: professional, friendly, formal")
    language: str = Field("fr", description="Langue: fr, ar, en")
    context: Optional[str] = Field(None, description="Contexte additionnel")


class LeadAIMessageResponse(BaseModel):
    """Message généré par IA"""
    message: str = Field(..., description="Message généré")
    subject: Optional[str] = Field(None, description="Objet (pour email)")
    channel: str = Field(..., description="Canal utilisé")
    message_type: str = Field(..., description="Type de message")
    
    # Variantes
    alternatives: List[str] = Field(default_factory=list, description="Messages alternatifs")
    
    # Conseils
    best_time: Optional[str] = Field(None, description="Meilleur moment pour envoyer")
    tips: List[str] = Field(default_factory=list, description="Conseils d'envoi")


class LeadAINextActionRequest(BaseModel):
    """Requête prochaine action IA"""
    lead_id: str = Field(..., description="ID du lead")
    context: Optional[str] = Field(None, description="Contexte additionnel")


class LeadAINextActionResponse(BaseModel):
    """Prochaine action suggérée par IA"""
    action: str = Field(..., description="Action recommandée")
    action_type: ActionType = Field(..., description="Type d'action")
    priority: LeadPriority = Field(..., description="Priorité")
    reason: str = Field(..., description="Raison de cette suggestion")
    
    # Timing
    suggested_date: Optional[datetime] = Field(None, description="Date suggérée")
    deadline: Optional[datetime] = Field(None, description="Date limite")
    
    # Alternatives
    alternatives: List[Dict[str, Any]] = Field(default_factory=list, description="Actions alternatives")
    
    # Script
    script: Optional[str] = Field(None, description="Script/guide pour l'action")


# ============================================
# INTERACTION / ACTIVITY MODELS
# ============================================

class InteractionType(str, Enum):
    """Type d'interaction"""
    NOTE = "note"
    CALL = "call"
    EMAIL_SENT = "email_sent"
    EMAIL_RECEIVED = "email_received"
    WHATSAPP_SENT = "whatsapp_sent"
    WHATSAPP_RECEIVED = "whatsapp_received"
    MEETING = "meeting"
    PROPOSAL_SENT = "proposal_sent"
    DOCUMENT_RECEIVED = "document_received"
    STATUS_CHANGE = "status_change"
    SCORE_UPDATE = "score_update"


class InteractionCreate(BaseModel):
    """Créer une interaction"""
    lead_id: str = Field(..., description="ID du lead")
    type: InteractionType = Field(..., description="Type d'interaction")
    content: str = Field(..., description="Contenu / Description")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class Interaction(InteractionCreate):
    """Interaction complète"""
    id: str = Field(..., description="ID de l'interaction")
    user_id: Optional[str] = Field(None, description="Utilisateur ayant créé")
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ============================================
# PIPELINE / KANBAN MODELS
# ============================================

class PipelineColumn(BaseModel):
    """Colonne du pipeline Kanban"""
    status: LeadStatus
    name: str
    color: str
    count: int = 0
    total_value: Decimal = Decimal("0")


class PipelineView(BaseModel):
    """Vue complète du pipeline"""
    columns: List[PipelineColumn]
    total_leads: int
    total_value: Decimal
    conversion_rate: float


# ============================================
# STATS / ANALYTICS MODELS
# ============================================

class CRMStats(BaseModel):
    """Statistiques globales CRM"""
    # Compteurs
    total_leads: int = 0
    leads_this_month: int = 0
    leads_this_week: int = 0
    
    # Par statut
    by_status: Dict[str, int] = Field(default_factory=dict)
    
    # Par source
    by_source: Dict[str, int] = Field(default_factory=dict)
    
    # Par secteur
    by_sector: Dict[str, int] = Field(default_factory=dict)
    
    # Conversion
    conversion_rate: float = 0.0
    avg_score: float = 0.0
    
    # Valeur
    total_pipeline_value: Decimal = Decimal("0")
    total_won_value: Decimal = Decimal("0")
    
    # Performance
    avg_days_to_close: float = 0.0
    hot_leads_count: int = 0  # Score > 70


class LeadFilters(BaseModel):
    """Filtres pour liste des leads"""
    status: Optional[List[LeadStatus]] = None
    source: Optional[List[LeadSource]] = None
    sector: Optional[List[Sector]] = None
    priority: Optional[List[LeadPriority]] = None
    country: Optional[str] = None
    assigned_to: Optional[str] = None
    min_score: Optional[int] = None
    max_score: Optional[int] = None
    tags: Optional[List[str]] = None
    search: Optional[str] = None
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None


class LeadListResponse(BaseModel):
    """Réponse liste paginée de leads"""
    leads: List[LeadPro]
    total: int
    page: int
    page_size: int
    total_pages: int
    
    # Quick stats
    stats: Optional[Dict[str, Any]] = None


# ============================================
# WORKFLOW / AUTOMATION MODELS
# ============================================

class WorkflowTrigger(str, Enum):
    """Déclencheur de workflow"""
    LEAD_CREATED = "lead_created"
    SCORE_UPDATED = "score_updated"
    STATUS_CHANGED = "status_changed"
    SCORE_ABOVE = "score_above"
    SCORE_BELOW = "score_below"
    INACTIVITY = "inactivity"


class WorkflowAction(str, Enum):
    """Action de workflow"""
    CHANGE_STATUS = "change_status"
    CHANGE_PRIORITY = "change_priority"
    SEND_EMAIL = "send_email"
    SEND_WHATSAPP = "send_whatsapp"
    CREATE_TASK = "create_task"
    NOTIFY = "notify"
    WEBHOOK = "webhook"


class WorkflowRule(BaseModel):
    """Règle de workflow automatique"""
    id: str
    name: str
    trigger: WorkflowTrigger
    conditions: Dict[str, Any]
    actions: List[Dict[str, Any]]
    is_active: bool = True
    priority: int = 0


# ============================================
# CONSTANTS
# ============================================

# Mapping statut -> couleur
STATUS_COLORS = {
    LeadStatus.NEW: "#3B82F6",       # Bleu
    LeadStatus.QUALIFY: "#F59E0B",   # Orange
    LeadStatus.WARM: "#EF4444",      # Rouge
    LeadStatus.PROPOSAL: "#8B5CF6",  # Violet
    LeadStatus.WON: "#10B981",       # Vert
    LeadStatus.LOST: "#6B7280",      # Gris
}

# Mapping statut -> nom FR
STATUS_NAMES = {
    LeadStatus.NEW: "Nouveau",
    LeadStatus.QUALIFY: "À Qualifier",
    LeadStatus.WARM: "Chaud 🔥",
    LeadStatus.PROPOSAL: "Proposition",
    LeadStatus.WON: "Gagné ✅",
    LeadStatus.LOST: "Perdu ❌",
}

# Mapping source -> label
SOURCE_LABELS = {
    LeadSource.WEBSITE: "Site Web",
    LeadSource.PME_ANALYZER: "PME Analyzer",
    LeadSource.FILE_AI: "FileAI",
    LeadSource.REFERRAL: "Recommandation",
    LeadSource.SOCIAL: "Réseaux Sociaux",
    LeadSource.ADS: "Publicité",
    LeadSource.COLD_CALL: "Prospection",
    LeadSource.EMAIL: "Email",
    LeadSource.WHATSAPP: "WhatsApp",
    LeadSource.PARTNER: "Partenaire",
    LeadSource.EVENT: "Événement",
    LeadSource.OTHER: "Autre",
}

# Règles de scoring par défaut
DEFAULT_SCORING_WEIGHTS = {
    "has_email": 10,
    "has_phone": 10,
    "has_company": 15,
    "has_sector": 10,
    "has_budget": 20,
    "has_need_description": 15,
    "employees_large": 15,      # > 50 employés
    "employees_medium": 10,     # 10-50 employés
    "high_revenue": 20,         # CA > 100M DZD
    "urgency_high": 15,
    "source_pme": 10,
    "source_referral": 15,
}
