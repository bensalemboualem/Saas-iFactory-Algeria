"""
IA Factory Automation - Lead Generation Workflow
Système automatisé de capture et qualification des leads
"""

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import json
import os
import httpx
from enum import Enum

router = APIRouter(prefix="/leads", tags=["Lead Generation"])


class LeadSource(str, Enum):
    WEBSITE = "website"
    LINKEDIN = "linkedin"
    REFERRAL = "referral"
    EVENT = "event"
    COLD_OUTREACH = "cold_outreach"


class LeadCategory(str, Enum):
    HOT = "HOT"
    WARM = "WARM"
    COLD = "COLD"
    DISQUALIFIED = "DISQUALIFIED"


class LeadCapture(BaseModel):
    """Modèle de capture d'un lead"""
    name: str = Field(..., min_length=2)
    email: EmailStr
    phone: Optional[str] = None
    company: str
    job_title: Optional[str] = None
    need: str = Field(..., description="RAG, Multi-Agent, Training, etc.")
    budget: Optional[str] = None
    timeline: Optional[str] = None
    message: Optional[str] = None
    source: LeadSource = LeadSource.WEBSITE
    market: str = Field(default="CH", pattern="^(CH|DZ)$")


class LeadEnriched(LeadCapture):
    """Lead avec données enrichies"""
    id: str
    score: int = 0
    category: LeadCategory = LeadCategory.COLD
    company_size: Optional[str] = None
    company_revenue: Optional[str] = None
    industry: Optional[str] = None
    linkedin_url: Optional[str] = None
    seniority: Optional[str] = None
    created_at: datetime
    last_contact: Optional[datetime] = None
    notes: List[str] = []


class LeadProcessor:
    """Processeur de leads avec scoring et qualification automatique"""
    
    def __init__(self):
        self.leads_db: Dict[str, LeadEnriched] = {}
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    
    async def process_lead(self, lead: LeadCapture) -> LeadEnriched:
        """Pipeline complet de traitement d'un lead"""
        
        # 1. Créer lead enrichi
        lead_id = f"lead_{datetime.now().strftime('%Y%m%d%H%M%S')}_{lead.email.split('@')[0]}"
        enriched = LeadEnriched(
            **lead.model_dump(),
            id=lead_id,
            created_at=datetime.now()
        )
        
        # 2. Enrichir données
        enriched = await self.enrich_lead(enriched)
        
        # 3. Scorer lead
        enriched.score = self.score_lead(enriched)
        
        # 4. Catégoriser
        enriched.category = self.categorize_lead(enriched.score)
        
        # 5. Sauvegarder
        self.leads_db[lead_id] = enriched
        
        return enriched
    
    async def enrich_lead(self, lead: LeadEnriched) -> LeadEnriched:
        """Enrichit les données du lead via APIs tierces"""
        
        # Enrichissement company
        company_data = await self.get_company_info(lead.company)
        if company_data:
            lead.company_size = company_data.get("size")
            lead.company_revenue = company_data.get("revenue")
            lead.industry = company_data.get("industry")
        
        # Déduire seniority du job title
        if lead.job_title:
            lead.seniority = self.infer_seniority(lead.job_title)
        
        return lead
    
    async def get_company_info(self, company_name: str) -> Optional[Dict]:
        """Récupère infos entreprise (placeholder - à connecter API réelle)"""
        # TODO: Intégrer Clearbit, LinkedIn, etc.
        
        # Estimation basique sur nom
        company_lower = company_name.lower()
        
        if any(word in company_lower for word in ["telecom", "bank", "ministère", "gouvernement"]):
            return {"size": "enterprise", "revenue": ">100M", "industry": "Government/Telecom"}
        elif any(word in company_lower for word in ["école", "school", "university", "lycée"]):
            return {"size": "mid-market", "revenue": "1-10M", "industry": "Education"}
        elif any(word in company_lower for word in ["startup", "labs", "tech"]):
            return {"size": "startup", "revenue": "<1M", "industry": "Technology"}
        
        return {"size": "unknown", "revenue": "unknown", "industry": "unknown"}
    
    def infer_seniority(self, job_title: str) -> str:
        """Déduit seniority du titre"""
        title_lower = job_title.lower()
        
        if any(word in title_lower for word in ["ceo", "cto", "coo", "founder", "président", "directeur général"]):
            return "C-Level"
        elif any(word in title_lower for word in ["director", "directeur", "head", "vp", "vice"]):
            return "Director"
        elif any(word in title_lower for word in ["manager", "responsable", "lead"]):
            return "Manager"
        elif any(word in title_lower for word in ["senior", "principal"]):
            return "Senior"
        
        return "Individual Contributor"
    
    def score_lead(self, lead: LeadEnriched) -> int:
        """Score le lead de 0 à 100"""
        score = 0
        
        # Market fit (20 pts)
        if lead.market == "CH":
            score += 20  # Premium market
        else:
            score += 15  # Volume market
        
        # Company size (20 pts)
        size_scores = {
            "enterprise": 20,
            "mid-market": 18,
            "startup": 12,
            "unknown": 10
        }
        score += size_scores.get(lead.company_size or "unknown", 10)
        
        # Budget indication (20 pts)
        if lead.budget:
            budget_lower = lead.budget.lower()
            if any(x in budget_lower for x in [">100k", "100k+", "unlimited"]):
                score += 20
            elif any(x in budget_lower for x in ["50k", "50-100"]):
                score += 15
            elif any(x in budget_lower for x in ["10k", "20k", "30k"]):
                score += 10
            else:
                score += 5
        else:
            score += 8  # Unknown = assume mid
        
        # Seniority / Authority (20 pts)
        seniority_scores = {
            "C-Level": 20,
            "Director": 18,
            "Manager": 15,
            "Senior": 10,
            "Individual Contributor": 5
        }
        score += seniority_scores.get(lead.seniority or "Individual Contributor", 5)
        
        # Service fit (20 pts)
        need_lower = lead.need.lower()
        if any(x in need_lower for x in ["rag", "multi-agent", "enterprise"]):
            score += 20
        elif any(x in need_lower for x in ["training", "formation", "academy"]):
            score += 15
        elif any(x in need_lower for x in ["chatbot", "automation"]):
            score += 12
        else:
            score += 8
        
        return min(score, 100)
    
    def categorize_lead(self, score: int) -> LeadCategory:
        """Catégorise lead selon score"""
        if score >= 80:
            return LeadCategory.HOT
        elif score >= 60:
            return LeadCategory.WARM
        elif score >= 40:
            return LeadCategory.COLD
        else:
            return LeadCategory.DISQUALIFIED
    
    async def generate_first_email(self, lead: LeadEnriched) -> Dict[str, str]:
        """Génère email personnalisé via Claude (style Boualem)"""
        
        # Sélectionner case study pertinent
        case_study = self.select_case_study(lead.industry, lead.need)
        
        prompt = f"""Tu es Boualem Chebaki, fondateur IA Factory.
        
Écris un email de prospection à:
- Nom: {lead.name}
- Entreprise: {lead.company} ({lead.industry or 'Tech'})
- Besoin: {lead.need}
- Marché: {'Suisse' if lead.market == 'CH' else 'Algérie'}

Style Boualem:
- Direct et concret
- Focus ROI
- Pas de blabla
- Professionnel mais pas guindé

Structure:
1. Accroche personnalisée (mentionne son besoin)
2. Case study pertinent: {case_study['name']} - {case_study['result']}
3. Proposition démo concrète
4. CTA clair

Max 120 mots. Signe "Boualem".

Retourne JSON:
{{"subject": "...", "body": "..."}}"""

        # Appel Claude API
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": self.anthropic_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json"
                    },
                    json={
                        "model": "claude-sonnet-4-20250514",
                        "max_tokens": 500,
                        "messages": [{"role": "user", "content": prompt}]
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result["content"][0]["text"]
                    return json.loads(content)
        except Exception as e:
            print(f"Error generating email: {e}")
        
        # Fallback template
        return {
            "subject": f"Solution IA pour {lead.company}",
            "body": f"""Bonjour {lead.name},

J'ai vu que vous cherchez une solution {lead.need} pour {lead.company}.

Concrètement, je propose un système qui:
✅ Réduit 70% du temps de recherche
✅ ROI mesurable en 3 mois
✅ Déploiement rapide (4-6 semaines)

On a fait ça pour {case_study['name']}: {case_study['result']}

Ça vous dit une démo de 30 min?

Boualem
IA Factory
www.iafactory.ch"""
        }
    
    def select_case_study(self, industry: Optional[str], need: str) -> Dict:
        """Sélectionne case study pertinent"""
        case_studies = {
            "Education": {
                "name": "École Nouvelle Horizon",
                "result": "70% temps gagné, 95% satisfaction, ROI 300%"
            },
            "Government": {
                "name": "Ministère de l'Éducation",
                "result": "Automatisation 80% requêtes, 50% coûts réduits"
            },
            "default": {
                "name": "nos clients",
                "result": "70% productivité augmentée en moyenne"
            }
        }
        
        return case_studies.get(industry or "default", case_studies["default"])


# Instance globale
lead_processor = LeadProcessor()


# Routes API

@router.post("/capture", response_model=Dict[str, Any])
async def capture_lead(lead: LeadCapture, background_tasks: BackgroundTasks):
    """
    Capture un nouveau lead depuis formulaire website
    """
    # Process en background pour réponse rapide
    enriched = await lead_processor.process_lead(lead)
    
    # Générer email en background si HOT
    if enriched.category == LeadCategory.HOT:
        background_tasks.add_task(handle_hot_lead, enriched)
    
    return {
        "status": "success",
        "lead_id": enriched.id,
        "score": enriched.score,
        "category": enriched.category.value,
        "message": "Merci! Nous vous recontactons sous 24h."
    }


async def handle_hot_lead(lead: LeadEnriched):
    """Traitement leads chauds - notification + email auto"""
    
    # Générer email personnalisé
    email = await lead_processor.generate_first_email(lead)
    
    # TODO: Envoyer notification WhatsApp/Telegram à Boualem
    print(f"🔥 HOT LEAD: {lead.name} ({lead.company}) - Score: {lead.score}")
    print(f"📧 Email généré: {email['subject']}")
    
    # TODO: Envoyer email via SMTP
    # TODO: Créer tâche CRM


@router.get("/stats")
async def get_lead_stats():
    """Statistiques des leads"""
    leads = list(lead_processor.leads_db.values())
    
    return {
        "total_leads": len(leads),
        "by_category": {
            "hot": len([l for l in leads if l.category == LeadCategory.HOT]),
            "warm": len([l for l in leads if l.category == LeadCategory.WARM]),
            "cold": len([l for l in leads if l.category == LeadCategory.COLD]),
            "disqualified": len([l for l in leads if l.category == LeadCategory.DISQUALIFIED])
        },
        "by_market": {
            "CH": len([l for l in leads if l.market == "CH"]),
            "DZ": len([l for l in leads if l.market == "DZ"])
        },
        "avg_score": sum(l.score for l in leads) / len(leads) if leads else 0,
        "conversion_funnel": {
            "captured": len(leads),
            "qualified": len([l for l in leads if l.score >= 60]),
            "contacted": len([l for l in leads if l.last_contact]),
        }
    }


@router.get("/{lead_id}")
async def get_lead(lead_id: str):
    """Récupère un lead par ID"""
    if lead_id not in lead_processor.leads_db:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    return lead_processor.leads_db[lead_id]


@router.get("/")
async def list_leads(category: Optional[LeadCategory] = None, market: Optional[str] = None):
    """Liste tous les leads avec filtres optionnels"""
    leads = list(lead_processor.leads_db.values())
    
    if category:
        leads = [l for l in leads if l.category == category]
    
    if market:
        leads = [l for l in leads if l.market == market]
    
    return leads
