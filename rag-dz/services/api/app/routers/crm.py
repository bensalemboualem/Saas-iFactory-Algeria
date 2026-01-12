"""
CRM Leads API Router
====================
Gestion des leads pour le composant CRMWidget.
"""

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/crm", tags=["CRM"])

# ============================================
# Models
# ============================================

class LeadCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    activity: Optional[str] = None
    message: Optional[str] = None
    source: str = "website"

class LeadResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: Optional[str]
    company: Optional[str]
    activity: Optional[str]
    message: Optional[str]
    source: str
    status: str
    created_at: str
    score: int

class LeadsList(BaseModel):
    leads: List[LeadResponse]
    total: int
    page: int
    per_page: int

# ============================================
# In-memory store (mock)
# ============================================

_leads_store: List[dict] = []

def calculate_lead_score(lead: dict) -> int:
    """Calcule un score de lead basé sur les informations fournies"""
    score = 10  # Base score
    
    if lead.get("company"):
        score += 20
    if lead.get("phone"):
        score += 15
    if lead.get("activity"):
        score += 10
    if lead.get("message") and len(lead.get("message", "")) > 50:
        score += 15
    
    # Bonus par source
    source_bonus = {
        "landing-page": 25,
        "pme-copilot": 30,
        "pricing": 35,
        "demo-request": 40,
        "website": 10
    }
    score += source_bonus.get(lead.get("source", "website"), 5)
    
    return min(score, 100)  # Cap à 100

# ============================================
# Endpoints
# ============================================

@router.post("/leads", response_model=LeadResponse, status_code=201)
async def create_lead(lead: LeadCreate):
    """
    Créer un nouveau lead.
    Utilisé par le composant CRMWidget.
    """
    # Vérifier si l'email existe déjà
    existing = next((l for l in _leads_store if l["email"] == lead.email), None)
    if existing:
        # Mettre à jour le lead existant plutôt que d'en créer un nouveau
        existing.update({
            "name": lead.name,
            "phone": lead.phone or existing.get("phone"),
            "company": lead.company or existing.get("company"),
            "activity": lead.activity or existing.get("activity"),
            "message": lead.message,
            "source": lead.source,
            "updated_at": datetime.now().isoformat()
        })
        existing["score"] = calculate_lead_score(existing)
        logger.info(f"Lead updated: {lead.email} from {lead.source}")
        return LeadResponse(**existing)
    
    # Créer un nouveau lead
    lead_id = f"lead_{uuid.uuid4().hex[:12]}"
    now = datetime.now().isoformat()
    
    new_lead = {
        "id": lead_id,
        "name": lead.name,
        "email": lead.email,
        "phone": lead.phone,
        "company": lead.company,
        "activity": lead.activity,
        "message": lead.message,
        "source": lead.source,
        "status": "new",
        "created_at": now,
        "updated_at": now,
        "score": 0
    }
    new_lead["score"] = calculate_lead_score(new_lead)
    
    _leads_store.append(new_lead)
    
    logger.info(f"New lead created: {lead.email} from {lead.source} (score: {new_lead['score']})")
    
    return LeadResponse(**new_lead)

@router.get("/leads", response_model=LeadsList)
async def list_leads(
    page: int = 1,
    per_page: int = 20,
    status: Optional[str] = None,
    source: Optional[str] = None,
    x_user_id: Optional[str] = Header(None, alias="X-User-Id")
):
    """
    Liste tous les leads avec pagination et filtres.
    """
    filtered = _leads_store.copy()
    
    if status:
        filtered = [l for l in filtered if l["status"] == status]
    if source:
        filtered = [l for l in filtered if l["source"] == source]
    
    # Trier par score décroissant puis par date
    filtered.sort(key=lambda x: (-x["score"], x["created_at"]), reverse=False)
    
    # Pagination
    start = (page - 1) * per_page
    end = start + per_page
    paginated = filtered[start:end]
    
    return LeadsList(
        leads=[LeadResponse(**l) for l in paginated],
        total=len(filtered),
        page=page,
        per_page=per_page
    )

@router.get("/leads/{lead_id}", response_model=LeadResponse)
async def get_lead(lead_id: str):
    """Récupère un lead par son ID"""
    lead = next((l for l in _leads_store if l["id"] == lead_id), None)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return LeadResponse(**lead)

@router.patch("/leads/{lead_id}/status")
async def update_lead_status(lead_id: str, status: str):
    """Met à jour le statut d'un lead"""
    valid_statuses = ["new", "contacted", "qualified", "proposal", "won", "lost"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    
    lead = next((l for l in _leads_store if l["id"] == lead_id), None)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    lead["status"] = status
    lead["updated_at"] = datetime.now().isoformat()
    
    logger.info(f"Lead {lead_id} status updated to {status}")
    
    return {"success": True, "lead_id": lead_id, "new_status": status}

@router.get("/stats")
async def get_crm_stats():
    """Statistiques CRM"""
    total = len(_leads_store)
    by_status = {}
    by_source = {}
    total_score = 0
    
    for lead in _leads_store:
        status = lead.get("status", "new")
        source = lead.get("source", "website")
        
        by_status[status] = by_status.get(status, 0) + 1
        by_source[source] = by_source.get(source, 0) + 1
        total_score += lead.get("score", 0)
    
    return {
        "total_leads": total,
        "by_status": by_status,
        "by_source": by_source,
        "average_score": round(total_score / total, 1) if total > 0 else 0,
        "conversion_rate": round(by_status.get("won", 0) / total * 100, 1) if total > 0 else 0
    }

@router.get("/health")
async def crm_health():
    """Health check du service CRM"""
    return {"status": "healthy", "service": "crm", "leads_count": len(_leads_store)}
