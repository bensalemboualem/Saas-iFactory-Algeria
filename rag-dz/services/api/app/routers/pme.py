"""
PME Analyzer API Router
=======================
Analyse PME pour le composant PMEAnalyzer.
"""

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime, timedelta
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/pme", tags=["PME Copilot"])

# ============================================
# Models
# ============================================

class PMEInput(BaseModel):
    company_name: str = Field(..., min_length=2)
    wilaya: str = Field(default="16")  # Alger par défaut
    activity_sector: str = Field(default="services")
    legal_form: str = Field(default="SARL")
    employee_count: int = Field(default=1, ge=0)
    annual_revenue: Optional[float] = None
    creation_date: Optional[str] = None
    has_employees: bool = False
    is_exporter: bool = False
    is_importer: bool = False
    vat_registered: bool = False
    description: Optional[str] = None
    country: Literal["DZ", "CH"] = "DZ"

class Obligation(BaseModel):
    title: str
    description: str
    deadline: Optional[str] = None
    priority: Literal["high", "medium", "low"]
    category: str
    penalty: Optional[str] = None

class Risk(BaseModel):
    title: str
    description: str
    severity: Literal["critical", "high", "medium", "low"]
    mitigation: str

class ChecklistItem(BaseModel):
    task: str
    deadline: str
    completed: bool = False
    category: str

class TaxInfo(BaseModel):
    name: str
    rate: str
    frequency: str
    next_deadline: str

class EstimatedCosts(BaseModel):
    monthly_taxes: float
    annual_contributions: float
    compliance_budget: float

class CompanyProfile(BaseModel):
    name: str
    sector: str
    size_category: str
    regime_fiscal: str

class PMEAnalysisResponse(BaseModel):
    success: bool = True
    company_profile: CompanyProfile
    obligations: List[Obligation]
    risks: List[Risk]
    checklist_30_days: List[ChecklistItem]
    taxes: List[TaxInfo]
    recommendations: List[str]
    documents_required: List[str]
    estimated_costs: EstimatedCosts
    ai_summary: str
    analysis_id: str
    timestamp: str

# ============================================
# Wilayas et Secteurs
# ============================================

WILAYAS_DZ = {
    "01": "Adrar", "02": "Chlef", "03": "Laghouat", "04": "Oum El Bouaghi",
    "05": "Batna", "06": "Béjaïa", "07": "Biskra", "08": "Béchar",
    "09": "Blida", "10": "Bouira", "11": "Tamanrasset", "12": "Tébessa",
    "13": "Tlemcen", "14": "Tiaret", "15": "Tizi Ouzou", "16": "Alger",
    "17": "Djelfa", "18": "Jijel", "19": "Sétif", "20": "Saïda",
    "21": "Skikda", "22": "Sidi Bel Abbès", "23": "Annaba", "24": "Guelma",
    "25": "Constantine", "26": "Médéa", "27": "Mostaganem", "28": "M'Sila",
    "29": "Mascara", "30": "Ouargla", "31": "Oran", "32": "El Bayadh",
    "33": "Illizi", "34": "Bordj Bou Arréridj", "35": "Boumerdès",
    "36": "El Tarf", "37": "Tindouf", "38": "Tissemsilt", "39": "El Oued",
    "40": "Khenchela", "41": "Souk Ahras", "42": "Tipaza", "43": "Mila",
    "44": "Aïn Defla", "45": "Naâma", "46": "Aïn Témouchent", "47": "Ghardaïa",
    "48": "Relizane", "49": "El M'Ghair", "50": "El Meniaa", "51": "Ouled Djellal",
    "52": "Bordj Baji Mokhtar", "53": "Béni Abbès", "54": "Timimoun",
    "55": "Touggourt", "56": "Djanet", "57": "In Salah", "58": "In Guezzam"
}

SECTORS = [
    {"id": "commerce", "label": "🛒 Commerce / Distribution"},
    {"id": "services", "label": "💼 Services aux entreprises"},
    {"id": "tech", "label": "💻 Tech / IT / Digital"},
    {"id": "industrie", "label": "🏭 Industrie / Production"},
    {"id": "immobilier", "label": "🏢 Immobilier / BTP"},
    {"id": "sante", "label": "🏥 Santé / Médical"},
    {"id": "education", "label": "🎓 Éducation / Formation"},
    {"id": "transport", "label": "🚚 Transport / Logistique"},
    {"id": "agriculture", "label": "🌾 Agriculture / Agroalimentaire"},
    {"id": "tourisme", "label": "✈️ Tourisme / Hôtellerie"},
    {"id": "autre", "label": "📦 Autre"}
]

# ============================================
# Analysis Logic
# ============================================

def get_size_category(employees: int, revenue: Optional[float]) -> str:
    if employees == 0:
        return "Auto-entrepreneur"
    elif employees <= 9:
        return "Micro-entreprise"
    elif employees <= 49:
        return "Petite entreprise"
    elif employees <= 249:
        return "Moyenne entreprise"
    else:
        return "Grande entreprise"

def get_fiscal_regime(legal_form: str, revenue: Optional[float], country: str) -> str:
    if country == "CH":
        return "Impôt sur le bénéfice (CH)"
    
    if legal_form in ["Auto-entrepreneur", "EI"]:
        return "IFU (Impôt Forfaitaire Unique)"
    elif revenue and revenue < 30000000:  # < 30M DZD
        return "Régime simplifié"
    else:
        return "Régime réel"

def generate_obligations_dz(data: PMEInput) -> List[Obligation]:
    """Génère les obligations pour l'Algérie"""
    obligations = []
    now = datetime.now()
    
    # CNAS/CASNOS
    if data.has_employees:
        obligations.append(Obligation(
            title="Déclaration CNAS mensuelle",
            description="Déclaration et paiement des cotisations sociales pour les salariés",
            deadline=(now.replace(day=1) + timedelta(days=32)).replace(day=15).strftime("%Y-%m-%d"),
            priority="high",
            category="social",
            penalty="Majorations de 5% par mois de retard"
        ))
    else:
        obligations.append(Obligation(
            title="Cotisation CASNOS trimestrielle",
            description="Cotisation sociale pour travailleurs non-salariés",
            deadline=(now + timedelta(days=90)).strftime("%Y-%m-%d"),
            priority="high",
            category="social",
            penalty="Majorations de 3% par mois de retard"
        ))
    
    # TVA
    if data.vat_registered:
        obligations.append(Obligation(
            title="Déclaration G50 (TVA)",
            description="Déclaration mensuelle de TVA et taxes assimilées",
            deadline=(now.replace(day=1) + timedelta(days=32)).replace(day=20).strftime("%Y-%m-%d"),
            priority="high",
            category="fiscal",
            penalty="Amende de 25% des droits dus"
        ))
    
    # IFU ou Bilan
    if data.legal_form in ["Auto-entrepreneur", "EI"]:
        obligations.append(Obligation(
            title="Déclaration IFU annuelle",
            description="Impôt Forfaitaire Unique - Déclaration annuelle",
            deadline=f"{now.year + 1}-01-31",
            priority="medium",
            category="fiscal",
            penalty="Majoration de 25%"
        ))
    else:
        obligations.append(Obligation(
            title="Dépôt du bilan annuel",
            description="Bilan et compte de résultat à déposer aux impôts",
            deadline=f"{now.year + 1}-04-30",
            priority="high",
            category="fiscal",
            penalty="Amende + taxation d'office"
        ))
    
    # Import/Export
    if data.is_importer:
        obligations.append(Obligation(
            title="Domiciliation bancaire import",
            description="Domiciliation obligatoire pour toute opération d'importation",
            deadline="Avant chaque importation",
            priority="high",
            category="douanes",
            penalty="Blocage de l'opération"
        ))
    
    if data.is_exporter:
        obligations.append(Obligation(
            title="Rapatriement des devises",
            description="Obligation de rapatrier les devises dans les 120 jours",
            deadline="120 jours après exportation",
            priority="high",
            category="douanes",
            penalty="Sanctions de la Banque d'Algérie"
        ))
    
    return obligations

def generate_risks(data: PMEInput) -> List[Risk]:
    """Génère les risques identifiés"""
    risks = []
    
    if not data.vat_registered and data.annual_revenue and data.annual_revenue > 8000000:
        risks.append(Risk(
            title="Seuil TVA dépassé",
            description="Votre CA dépasse le seuil d'assujettissement à la TVA (8M DZD)",
            severity="critical",
            mitigation="Régularisez votre situation auprès des impôts immédiatement"
        ))
    
    if data.has_employees and data.employee_count > 10 and data.legal_form == "EURL":
        risks.append(Risk(
            title="Structure juridique inadaptée",
            description="Une EURL avec plus de 10 salariés peut présenter des risques de responsabilité",
            severity="medium",
            mitigation="Envisagez une transformation en SARL ou SPA"
        ))
    
    if not data.creation_date:
        risks.append(Risk(
            title="Date de création non spécifiée",
            description="Impossible de vérifier les obligations liées à l'ancienneté",
            severity="low",
            mitigation="Renseignez la date de création pour une analyse complète"
        ))
    
    return risks

def generate_checklist(data: PMEInput) -> List[ChecklistItem]:
    """Génère la checklist 30 jours"""
    now = datetime.now()
    items = []
    
    items.append(ChecklistItem(
        task="Vérifier la validité du registre de commerce",
        deadline=(now + timedelta(days=7)).strftime("%Y-%m-%d"),
        category="administratif"
    ))
    
    items.append(ChecklistItem(
        task="Mettre à jour les statuts si nécessaire",
        deadline=(now + timedelta(days=14)).strftime("%Y-%m-%d"),
        category="juridique"
    ))
    
    if data.has_employees:
        items.append(ChecklistItem(
            task="Vérifier les contrats de travail",
            deadline=(now + timedelta(days=10)).strftime("%Y-%m-%d"),
            category="social"
        ))
        items.append(ChecklistItem(
            task="Préparer la déclaration CNAS du mois",
            deadline=(now + timedelta(days=15)).strftime("%Y-%m-%d"),
            category="social"
        ))
    
    items.append(ChecklistItem(
        task="Archiver les factures du mois précédent",
        deadline=(now + timedelta(days=5)).strftime("%Y-%m-%d"),
        category="comptabilité"
    ))
    
    if data.vat_registered:
        items.append(ChecklistItem(
            task="Préparer la déclaration G50",
            deadline=(now + timedelta(days=18)).strftime("%Y-%m-%d"),
            category="fiscal"
        ))
    
    return items

def generate_taxes(data: PMEInput) -> List[TaxInfo]:
    """Génère les informations fiscales"""
    now = datetime.now()
    taxes = []
    
    if data.country == "DZ":
        if data.legal_form in ["Auto-entrepreneur", "EI"]:
            taxes.append(TaxInfo(
                name="IFU (Impôt Forfaitaire Unique)",
                rate="5% du CA (services) ou 12% (commerce)",
                frequency="Annuel",
                next_deadline=f"{now.year + 1}-01-31"
            ))
        else:
            taxes.append(TaxInfo(
                name="IBS (Impôt sur les Bénéfices des Sociétés)",
                rate="19% (production) ou 26% (autres)",
                frequency="Annuel + acomptes",
                next_deadline=f"{now.year + 1}-04-30"
            ))
        
        if data.vat_registered:
            taxes.append(TaxInfo(
                name="TVA",
                rate="19% (normal) ou 9% (réduit)",
                frequency="Mensuel",
                next_deadline=(now.replace(day=1) + timedelta(days=32)).replace(day=20).strftime("%Y-%m-%d")
            ))
        
        taxes.append(TaxInfo(
            name="TAP (Taxe sur l'Activité Professionnelle)",
            rate="1% à 3% du CA",
            frequency="Mensuel",
            next_deadline=(now.replace(day=1) + timedelta(days=32)).replace(day=20).strftime("%Y-%m-%d")
        ))
    
    return taxes

def estimate_costs(data: PMEInput) -> EstimatedCosts:
    """Estime les coûts mensuels et annuels"""
    revenue = data.annual_revenue or 2000000  # 2M DZD par défaut
    monthly_revenue = revenue / 12
    
    # Estimations approximatives
    if data.legal_form in ["Auto-entrepreneur", "EI"]:
        monthly_taxes = monthly_revenue * 0.05  # IFU ~5%
        annual_contributions = revenue * 0.15  # CASNOS ~15%
    else:
        monthly_taxes = monthly_revenue * 0.02  # TAP ~2%
        if data.vat_registered:
            monthly_taxes += monthly_revenue * 0.19 * 0.3  # TVA collectée - déductible
        annual_contributions = revenue * 0.26 if data.has_employees else revenue * 0.15
    
    return EstimatedCosts(
        monthly_taxes=round(monthly_taxes, 2),
        annual_contributions=round(annual_contributions, 2),
        compliance_budget=round(monthly_taxes * 12 * 0.1, 2)  # 10% pour conformité
    )

# ============================================
# Endpoints
# ============================================

@router.post("/analyze", response_model=PMEAnalysisResponse)
async def analyze_pme(data: PMEInput):
    """
    Analyse complète d'une PME.
    Retourne obligations, risques, checklist, taxes et recommandations.
    """
    analysis_id = f"pme_{uuid.uuid4().hex[:12]}"
    now = datetime.now()
    
    logger.info(f"PME Analysis started: {data.company_name} ({data.country})")
    
    # Profil entreprise
    profile = CompanyProfile(
        name=data.company_name,
        sector=data.activity_sector,
        size_category=get_size_category(data.employee_count, data.annual_revenue),
        regime_fiscal=get_fiscal_regime(data.legal_form, data.annual_revenue, data.country)
    )
    
    # Générer l'analyse
    obligations = generate_obligations_dz(data)
    risks = generate_risks(data)
    checklist = generate_checklist(data)
    taxes = generate_taxes(data)
    costs = estimate_costs(data)
    
    # Recommandations
    recommendations = [
        "Tenir une comptabilité régulière et à jour",
        "Conserver tous les justificatifs pendant 10 ans",
        "Anticiper les échéances fiscales avec des provisions"
    ]
    if not data.vat_registered and data.annual_revenue and data.annual_revenue > 5000000:
        recommendations.append("Évaluez l'intérêt de vous assujettir à la TVA")
    if data.employee_count > 5:
        recommendations.append("Envisagez un logiciel de gestion RH/Paie")
    
    # Documents requis
    documents = [
        "Registre de commerce à jour",
        "Statuts de la société",
        "Carte d'identification fiscale (NIF)",
        "Attestation CNAS/CASNOS"
    ]
    if data.is_importer or data.is_exporter:
        documents.append("Carte d'importateur/exportateur")
    
    # Résumé IA
    ai_summary = f"""
## Analyse de {data.company_name}

**Profil :** {profile.size_category} dans le secteur {data.activity_sector}
**Régime fiscal :** {profile.regime_fiscal}

### Points clés :
- {len(obligations)} obligations identifiées dont {sum(1 for o in obligations if o.priority == 'high')} prioritaires
- {len(risks)} risques à surveiller
- Estimation charges mensuelles : {costs.monthly_taxes:,.0f} DZD

### Actions prioritaires :
1. {checklist[0].task if checklist else 'Aucune action immédiate'}
2. Vérifier les prochaines échéances fiscales
3. Mettre à jour la documentation administrative
""".strip()
    
    response = PMEAnalysisResponse(
        company_profile=profile,
        obligations=obligations,
        risks=risks,
        checklist_30_days=checklist,
        taxes=taxes,
        recommendations=recommendations,
        documents_required=documents,
        estimated_costs=costs,
        ai_summary=ai_summary,
        analysis_id=analysis_id,
        timestamp=now.isoformat()
    )
    
    logger.info(f"PME Analysis completed: {analysis_id}")
    
    return response

@router.get("/wilayas")
async def get_wilayas():
    """Liste des wilayas d'Algérie"""
    return {
        "wilayas": [{"code": k, "name": v} for k, v in WILAYAS_DZ.items()]
    }

@router.get("/sectors")
async def get_sectors():
    """Liste des secteurs d'activité"""
    return {"sectors": SECTORS}

@router.get("/legal-forms")
async def get_legal_forms():
    """Formes juridiques disponibles"""
    return {
        "forms": [
            {"id": "Auto-entrepreneur", "label": "Auto-entrepreneur", "description": "Statut simplifié pour activités individuelles"},
            {"id": "EI", "label": "Entreprise Individuelle", "description": "Activité en nom propre"},
            {"id": "EURL", "label": "EURL", "description": "Entreprise Unipersonnelle à Responsabilité Limitée"},
            {"id": "SARL", "label": "SARL", "description": "Société à Responsabilité Limitée"},
            {"id": "SPA", "label": "SPA", "description": "Société Par Actions"},
            {"id": "SNC", "label": "SNC", "description": "Société en Nom Collectif"}
        ]
    }

@router.get("/health")
async def pme_health():
    """Health check du service PME"""
    return {"status": "healthy", "service": "pme-copilot"}
