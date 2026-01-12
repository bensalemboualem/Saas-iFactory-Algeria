"""
PME Analyzer PRO V2 - Modèles Pydantic
=====================================
Modèles complets pour l'analyse PME algérienne avec IA + RAG
"""

from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field, EmailStr


# ============================================
# Enums
# ============================================

class LegalForm(str, Enum):
    """Formes juridiques algériennes"""
    EURL = "EURL"           # Entreprise Unipersonnelle à Responsabilité Limitée
    SARL = "SARL"           # Société à Responsabilité Limitée
    SPA = "SPA"             # Société Par Actions
    SNC = "SNC"             # Société en Nom Collectif
    SCS = "SCS"             # Société en Commandite Simple
    AUTO_ENTREPRENEUR = "AUTO_ENTREPRENEUR"
    MICRO_ENTREPRISE = "MICRO_ENTREPRISE"
    PROFESSION_LIBERALE = "PROFESSION_LIBERALE"
    ARTISAN = "ARTISAN"


class FiscalRegime(str, Enum):
    """Régimes fiscaux algériens"""
    IFU = "IFU"             # Impôt Forfaitaire Unique (< 15M DA)
    REEL = "REEL"           # Régime Réel (> 15M DA ou option)
    REEL_SIMPLIFIE = "REEL_SIMPLIFIE"
    MICRO_ENTREPRISE = "MICRO_ENTREPRISE"


class ActivitySector(str, Enum):
    """Secteurs d'activité"""
    COMMERCE = "Commerce"
    SERVICES = "Services"
    INDUSTRIE = "Industrie"
    BTP = "BTP"
    AGRICULTURE = "Agriculture"
    ARTISANAT = "Artisanat"
    IMPORT_EXPORT = "Import/Export"
    TECHNOLOGIE = "Technologie"
    SANTE = "Santé"
    EDUCATION = "Éducation"
    TRANSPORT = "Transport"
    TOURISME = "Tourisme"
    IMMOBILIER = "Immobilier"
    RESTAURATION = "Restauration"


class RiskLevel(str, Enum):
    """Niveaux de risque"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DeclarationType(str, Enum):
    """Types de déclarations"""
    G50 = "G50"             # Déclaration mensuelle TVA
    G50A = "G50A"           # Déclaration annuelle
    TAP = "TAP"             # Taxe sur l'activité professionnelle
    IRG = "IRG"             # Impôt sur le revenu global
    IBS = "IBS"             # Impôt sur les bénéfices des sociétés
    IFU = "IFU"             # Déclaration IFU
    CNAS = "CNAS"           # Cotisations sociales salariés
    CASNOS = "CASNOS"       # Cotisations non-salariés
    DAS = "DAS"             # Déclaration annuelle des salaires
    ANEM = "ANEM"           # Déclarations ANEM


# ============================================
# Input Models
# ============================================

class CompanyInput(BaseModel):
    """Données d'entrée pour l'analyse PME"""
    # Informations de base
    company_name: str = Field(..., min_length=2, max_length=200)
    legal_form: LegalForm
    sector: ActivitySector
    wilaya: str = Field(..., min_length=2)
    commune: Optional[str] = None
    
    # Données financières
    annual_revenue: Optional[Decimal] = Field(None, ge=0, description="CA annuel en DA")
    employees_count: int = Field(default=0, ge=0)
    creation_date: Optional[date] = None
    
    # Informations fiscales existantes
    has_rc: bool = Field(default=False, description="Possède un Registre de Commerce")
    rc_number: Optional[str] = None
    nif: Optional[str] = None  # Numéro d'Identification Fiscale
    nis: Optional[str] = None  # Numéro d'Identification Statistique
    has_tva: bool = Field(default=False, description="Assujetti à la TVA")
    
    # Situation sociale
    has_cnas: bool = Field(default=False)
    has_casnos: bool = Field(default=False)
    
    # Options d'analyse
    include_fiscal_simulation: bool = True
    include_declaration_calendar: bool = True
    include_risk_analysis: bool = True
    include_rag_context: bool = True  # Enrichir avec RAG DZ


class FiscalSimulationInput(BaseModel):
    """Données pour simulation fiscale"""
    annual_revenue: Decimal = Field(..., ge=0)
    annual_expenses: Decimal = Field(default=0, ge=0)
    employees_count: int = Field(default=0, ge=0)
    average_salary: Decimal = Field(default=0, ge=0)
    legal_form: LegalForm
    sector: ActivitySector
    has_tva: bool = False
    fiscal_year: int = Field(default=2025)


# ============================================
# Output Models - Fiscal Analysis
# ============================================

class TaxDetail(BaseModel):
    """Détail d'un impôt/taxe"""
    name: str
    code: str
    rate: float
    base: Decimal
    amount: Decimal
    frequency: str  # mensuel, trimestriel, annuel
    due_date: Optional[str] = None
    notes: Optional[str] = None


class FiscalAnalysis(BaseModel):
    """Analyse fiscale complète"""
    regime: FiscalRegime
    regime_explanation: str
    is_tva_required: bool
    tva_threshold: Decimal = Field(default=Decimal("15000000"))  # 15M DA
    
    # Détail des impôts
    taxes: list[TaxDetail]
    total_annual_taxes: Decimal
    effective_tax_rate: float  # Taux effectif d'imposition
    
    # TVA
    tva_rate: float = 19.0
    tva_collected: Optional[Decimal] = None
    tva_deductible: Optional[Decimal] = None
    tva_due: Optional[Decimal] = None
    
    # Recommandations
    optimization_tips: list[str]
    regime_comparison: Optional[dict[str, Any]] = None


class SocialChargesAnalysis(BaseModel):
    """Analyse des charges sociales"""
    # CNAS (salariés)
    cnas_employer_rate: float = 26.0  # Part patronale
    cnas_employee_rate: float = 9.0   # Part salariale
    monthly_cnas_employer: Decimal
    monthly_cnas_employee: Decimal
    annual_cnas_total: Decimal
    
    # CASNOS (non-salariés)
    casnos_rate: float = 15.0
    annual_casnos: Decimal
    
    # Autres charges
    oeuvres_sociales_rate: float = 0.5
    formation_rate: float = 1.0
    accident_travail_rate: float = 1.25
    
    total_social_charges: Decimal
    breakdown: dict[str, Decimal]


# ============================================
# Output Models - Declarations
# ============================================

class Declaration(BaseModel):
    """Une déclaration fiscale/sociale"""
    type: DeclarationType
    name: str
    description: str
    frequency: str
    due_day: int  # Jour du mois
    organism: str  # DGI, CNAS, etc.
    penalty_rate: Optional[float] = None
    required_documents: list[str]
    online_platform: Optional[str] = None
    is_mandatory: bool = True


class DeclarationCalendar(BaseModel):
    """Calendrier des déclarations"""
    company_name: str
    fiscal_year: int
    regime: FiscalRegime
    
    monthly_declarations: list[Declaration]
    quarterly_declarations: list[Declaration]
    annual_declarations: list[Declaration]
    
    next_deadlines: list[dict[str, Any]]  # Prochaines échéances
    reminders: list[str]


# ============================================
# Output Models - Risk Analysis
# ============================================

class Risk(BaseModel):
    """Un risque identifié"""
    code: str
    title: str
    description: str
    level: RiskLevel
    category: str  # fiscal, social, juridique, administratif
    impact: str
    probability: str
    mitigation: str
    deadline: Optional[date] = None
    penalty_amount: Optional[Decimal] = None


class RiskAnalysis(BaseModel):
    """Analyse des risques"""
    overall_risk_level: RiskLevel
    risk_score: int = Field(ge=0, le=100)
    
    risks: list[Risk]
    risks_by_category: dict[str, list[Risk]]
    
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    
    priority_actions: list[str]
    compliance_score: int = Field(ge=0, le=100)


# ============================================
# Output Models - Checklist & Actions
# ============================================

class ChecklistItem(BaseModel):
    """Élément de checklist"""
    id: str
    title: str
    description: str
    category: str
    priority: int = Field(ge=1, le=5)
    deadline_days: Optional[int] = None  # Jours restants
    estimated_cost: Optional[str] = None
    organism: Optional[str] = None
    documents_needed: list[str] = []
    is_completed: bool = False
    notes: Optional[str] = None


class ActionPlan(BaseModel):
    """Plan d'action recommandé"""
    immediate_actions: list[ChecklistItem]  # 0-7 jours
    short_term_actions: list[ChecklistItem]  # 7-30 jours
    medium_term_actions: list[ChecklistItem]  # 1-3 mois
    long_term_actions: list[ChecklistItem]  # 3+ mois
    
    total_estimated_cost: str
    total_items: int
    completed_items: int


# ============================================
# Output Models - RAG Context
# ============================================

class RAGSource(BaseModel):
    """Source RAG utilisée"""
    title: str
    source_name: str
    source_type: str  # loi, décret, circulaire, guide
    date: Optional[str] = None
    relevance_score: float
    excerpt: str
    url: Optional[str] = None


class RAGContext(BaseModel):
    """Contexte RAG enrichi"""
    query_used: str
    sources_count: int
    sources: list[RAGSource]
    legal_references: list[str]
    key_articles: list[str]
    last_update: Optional[str] = None


# ============================================
# Main Output Models
# ============================================

class CompanyProfile(BaseModel):
    """Profil complet de l'entreprise"""
    company_name: str
    legal_form: LegalForm
    legal_form_full_name: str
    sector: ActivitySector
    wilaya: str
    wilaya_code: str
    
    # Statut
    creation_date: Optional[date] = None
    age_years: Optional[int] = None
    employees_count: int
    size_category: str  # TPE, PME, Grande entreprise
    
    # Identifiants
    has_rc: bool
    rc_number: Optional[str] = None
    nif: Optional[str] = None
    nis: Optional[str] = None
    
    # Obligations
    capital_minimum: Optional[str] = None
    required_registrations: list[str]


class AuditReport(BaseModel):
    """Rapport d'audit PME complet"""
    # Métadonnées
    audit_id: str
    generated_at: datetime
    version: str = "2.0"
    
    # Profil
    company_profile: CompanyProfile
    
    # Analyses
    fiscal_analysis: FiscalAnalysis
    social_charges: SocialChargesAnalysis
    risk_analysis: RiskAnalysis
    declaration_calendar: DeclarationCalendar
    action_plan: ActionPlan
    
    # RAG Context
    rag_context: Optional[RAGContext] = None
    
    # Résumé IA
    ai_summary: str
    key_insights: list[str]
    recommendations: list[str]
    
    # Scores
    compliance_score: int
    fiscal_health_score: int
    overall_score: int
    
    # Export
    pdf_available: bool = False
    pdf_url: Optional[str] = None


class AuditHistoryItem(BaseModel):
    """Historique d'audit"""
    audit_id: str
    company_name: str
    generated_at: datetime
    overall_score: int
    compliance_score: int
    risk_level: RiskLevel
    pdf_url: Optional[str] = None


# ============================================
# Response Models
# ============================================

class PMEAnalysisResponse(BaseModel):
    """Réponse API analyse PME"""
    success: bool
    audit: AuditReport
    processing_time: float
    credits_consumed: int = 5


class QuickAnalysisResponse(BaseModel):
    """Réponse analyse rapide"""
    success: bool
    company_name: str
    regime: FiscalRegime
    is_tva_required: bool
    estimated_annual_taxes: Decimal
    risk_level: RiskLevel
    top_3_risks: list[str]
    top_3_actions: list[str]
    ai_summary: str


class PDFExportResponse(BaseModel):
    """Réponse export PDF"""
    success: bool
    audit_id: str
    pdf_url: str
    filename: str
    size_bytes: int
    generated_at: datetime
