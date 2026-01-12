"""
CRM PRO - Router FastAPI
========================
HubSpot DZ/CH powered by IA
Pipeline Kanban + Scoring IA + Actions automatiques
"""

from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query, Header
from pydantic import BaseModel

from ..models.crm_pro_models import (
    # Enums
    LeadStatus, LeadSource, LeadPriority, Sector, InteractionType, ActionType,
    # Models
    LeadPro, LeadProCreate, LeadProUpdate,
    LeadAIScoreRequest, LeadAIScoreResponse,
    LeadAIMessageRequest, LeadAIMessageResponse,
    LeadAINextActionRequest, LeadAINextActionResponse,
    InteractionCreate, Interaction,
    PipelineView, CRMStats, LeadListResponse,
    # Constants
    STATUS_NAMES, STATUS_COLORS, SOURCE_LABELS,
)
from ..services.crm_pro_service import crm_pro_service

router = APIRouter(prefix="/api/crm-pro", tags=["CRM PRO"])


# ============================================
# HELPER MODELS
# ============================================

class BulkActionRequest(BaseModel):
    """Action groupée sur plusieurs leads"""
    lead_ids: List[str]
    action: str  # "change_status", "change_priority", "delete"
    value: Optional[str] = None


class MoveLeadRequest(BaseModel):
    """Déplacer un lead dans le pipeline"""
    new_status: LeadStatus


# ============================================
# LEADS CRUD
# ============================================

@router.post("/leads", response_model=LeadPro)
async def create_lead(
    data: LeadProCreate,
    x_user_id: Optional[str] = Header(None, alias="X-User-Id"),
):
    """
    ➕ Créer un nouveau lead
    
    Le scoring IA et le statut sont calculés automatiquement.
    
    Règles de pipeline automatiques:
    - Score ≥ 85 → Proposition
    - Score ≥ 70 → Chaud
    - Score ≥ 30 → À Qualifier
    - Source PME Analyzer → À Qualifier
    - Source Referral → Chaud
    """
    lead = crm_pro_service.create_lead(data, user_id=x_user_id)
    return lead


@router.get("/leads", response_model=LeadListResponse)
async def list_leads(
    status: Optional[str] = Query(None, description="Statuts séparés par virgule: new,qualify,warm"),
    source: Optional[str] = Query(None, description="Sources séparées par virgule"),
    sector: Optional[str] = Query(None, description="Secteurs séparés par virgule"),
    priority: Optional[str] = Query(None, description="Priorités séparées par virgule"),
    min_score: Optional[int] = Query(None, ge=0, le=100),
    max_score: Optional[int] = Query(None, ge=0, le=100),
    search: Optional[str] = Query(None, description="Recherche dans nom, email, entreprise"),
    assigned_to: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort_by: str = Query("created_at", description="score, priority, status, created_at"),
    sort_order: str = Query("desc", description="asc, desc"),
):
    """
    📋 Liste paginée des leads avec filtres
    
    Supporte le tri par score, priorité, statut ou date de création.
    """
    # Parse des filtres multi-valeurs
    status_list = None
    if status:
        try:
            status_list = [LeadStatus(s.strip()) for s in status.split(",")]
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Statut invalide: {status}")
    
    source_list = None
    if source:
        try:
            source_list = [LeadSource(s.strip()) for s in source.split(",")]
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Source invalide: {source}")
    
    sector_list = None
    if sector:
        try:
            sector_list = [Sector(s.strip()) for s in sector.split(",")]
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Secteur invalide: {sector}")
    
    priority_list = None
    if priority:
        try:
            priority_list = [LeadPriority(p.strip()) for p in priority.split(",")]
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Priorité invalide: {priority}")
    
    leads, total = crm_pro_service.list_leads(
        status=status_list,
        source=source_list,
        sector=sector_list,
        priority=priority_list,
        min_score=min_score,
        max_score=max_score,
        search=search,
        assigned_to=assigned_to,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    
    total_pages = (total + page_size - 1) // page_size
    
    return LeadListResponse(
        leads=leads,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get("/leads/{lead_id}", response_model=LeadPro)
async def get_lead(lead_id: str):
    """
    📄 Détails d'un lead
    """
    lead = crm_pro_service.get_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead non trouvé")
    return lead


@router.patch("/leads/{lead_id}", response_model=LeadPro)
async def update_lead(
    lead_id: str,
    data: LeadProUpdate,
    rescore: bool = Query(True, description="Recalculer le score IA"),
    x_user_id: Optional[str] = Header(None, alias="X-User-Id"),
):
    """
    ✏️ Mettre à jour un lead
    
    Le score IA est recalculé automatiquement sauf si rescore=false.
    """
    lead = crm_pro_service.update_lead(
        lead_id=lead_id,
        data=data,
        user_id=x_user_id,
        rescore=rescore,
    )
    if not lead:
        raise HTTPException(status_code=404, detail="Lead non trouvé")
    return lead


@router.delete("/leads/{lead_id}")
async def delete_lead(lead_id: str):
    """
    🗑️ Supprimer un lead
    """
    success = crm_pro_service.delete_lead(lead_id)
    if not success:
        raise HTTPException(status_code=404, detail="Lead non trouvé")
    return {"success": True, "message": "Lead supprimé"}


# ============================================
# PIPELINE / KANBAN
# ============================================

@router.get("/pipeline", response_model=PipelineView)
async def get_pipeline():
    """
    📊 Vue Kanban du pipeline
    
    Retourne toutes les colonnes avec le nombre de leads et la valeur totale.
    """
    return crm_pro_service.get_pipeline_view()


@router.post("/leads/{lead_id}/move", response_model=LeadPro)
async def move_lead(
    lead_id: str,
    data: MoveLeadRequest,
    x_user_id: Optional[str] = Header(None, alias="X-User-Id"),
):
    """
    ↔️ Déplacer un lead dans le pipeline (Kanban drag & drop)
    """
    lead = crm_pro_service.move_lead_in_pipeline(
        lead_id=lead_id,
        new_status=data.new_status,
        user_id=x_user_id,
    )
    if not lead:
        raise HTTPException(status_code=404, detail="Lead non trouvé")
    return lead


# ============================================
# SCORING IA
# ============================================

@router.post("/leads/{lead_id}/score", response_model=LeadAIScoreResponse)
async def rescore_lead(lead_id: str):
    """
    🎯 Recalculer le score IA d'un lead
    
    Analyse les données du lead et génère:
    - Score 0-100
    - Probabilité de conversion
    - Forces et faiblesses
    - Statut et priorité recommandés
    """
    result = await crm_pro_service.rescore_lead(lead_id)
    if not result:
        raise HTTPException(status_code=404, detail="Lead non trouvé")
    return result


@router.post("/score", response_model=LeadAIScoreResponse)
async def preview_score(data: LeadProCreate):
    """
    🔮 Prévisualiser le score IA sans créer le lead
    
    Utile pour estimer le potentiel avant de créer le lead.
    """
    score_data = crm_pro_service._calculate_score(data)
    
    return LeadAIScoreResponse(
        score=score_data["score"],
        confidence=score_data["confidence"],
        probability=score_data["probability"],
        reasons=score_data["reasons"],
        recommended_status=crm_pro_service._determine_status(data, score_data["score"]),
        recommended_priority=score_data["recommended_priority"],
        strengths=[r for r in score_data["reasons"] if "+" in r],
        weaknesses=[],
        opportunities=[],
    )


# ============================================
# GÉNÉRATION MESSAGE IA
# ============================================

@router.post("/leads/{lead_id}/message", response_model=LeadAIMessageResponse)
async def generate_message(
    lead_id: str,
    channel: str = Query("whatsapp", description="whatsapp, email, sms"),
    message_type: str = Query("first_contact", description="first_contact, follow_up, proposal, thank_you"),
    tone: str = Query("professional", description="professional, friendly, formal"),
    language: str = Query("fr", description="fr, ar, en"),
    context: Optional[str] = Query(None, description="Contexte additionnel"),
):
    """
    💬 Générer un message IA personnalisé
    
    Types de messages:
    - first_contact: Premier contact
    - follow_up: Relance
    - proposal: Proposition commerciale
    - thank_you: Remerciement (après signature)
    
    Canaux:
    - whatsapp: Message court et engageant
    - email: Message formel avec objet
    - sms: Message très court
    """
    result = await crm_pro_service.generate_message(
        lead_id=lead_id,
        channel=channel,
        message_type=message_type,
        tone=tone,
        language=language,
        context=context,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Lead non trouvé")
    return result


# ============================================
# SUGGESTION PROCHAINE ACTION
# ============================================

@router.post("/leads/{lead_id}/next-action", response_model=LeadAINextActionResponse)
async def suggest_next_action(
    lead_id: str,
    context: Optional[str] = Query(None, description="Contexte additionnel"),
):
    """
    🎯 Suggérer la prochaine action pour un lead
    
    L'IA analyse le contexte et propose:
    - Action recommandée
    - Priorité
    - Date suggérée
    - Script/guide pour l'action
    - Actions alternatives
    """
    result = await crm_pro_service.suggest_next_action(
        lead_id=lead_id,
        context=context,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Lead non trouvé")
    return result


# ============================================
# INTERACTIONS / HISTORIQUE
# ============================================

@router.post("/leads/{lead_id}/interactions", response_model=Interaction)
async def add_interaction(
    lead_id: str,
    data: InteractionCreate,
    x_user_id: Optional[str] = Header(None, alias="X-User-Id"),
):
    """
    📝 Ajouter une interaction à un lead
    
    Types: note, call, email_sent, email_received, whatsapp_sent, 
    whatsapp_received, meeting, proposal_sent, document_received
    """
    # Vérifier que le lead_id correspond
    if data.lead_id != lead_id:
        data.lead_id = lead_id
    
    interaction = crm_pro_service.add_interaction(
        lead_id=lead_id,
        type=data.type,
        content=data.content,
        user_id=x_user_id,
        metadata=data.metadata,
    )
    if not interaction:
        raise HTTPException(status_code=404, detail="Lead non trouvé")
    return interaction


@router.get("/leads/{lead_id}/interactions", response_model=List[Interaction])
async def get_interactions(
    lead_id: str,
    limit: int = Query(50, ge=1, le=200),
):
    """
    📋 Historique des interactions d'un lead
    """
    lead = crm_pro_service.get_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead non trouvé")
    
    return crm_pro_service.get_interactions(lead_id, limit=limit)


# ============================================
# STATISTIQUES
# ============================================

@router.get("/stats", response_model=CRMStats)
async def get_stats():
    """
    📊 Statistiques globales du CRM
    
    Retourne:
    - Compteurs par période (semaine, mois)
    - Distribution par statut, source, secteur
    - Taux de conversion
    - Valeur du pipeline
    - Nombre de leads chauds
    """
    return crm_pro_service.get_stats()


@router.get("/stats/performance")
async def get_performance_stats():
    """
    📈 Statistiques de performance détaillées
    """
    stats = crm_pro_service.get_stats()
    pipeline = crm_pro_service.get_pipeline_view()
    
    return {
        "overview": {
            "total_leads": stats.total_leads,
            "hot_leads": stats.hot_leads_count,
            "conversion_rate": stats.conversion_rate,
            "avg_score": stats.avg_score,
        },
        "pipeline": {
            "total_value": float(stats.total_pipeline_value),
            "won_value": float(stats.total_won_value),
            "columns": [
                {
                    "status": col.status.value,
                    "name": col.name,
                    "color": col.color,
                    "count": col.count,
                    "value": float(col.total_value),
                }
                for col in pipeline.columns
            ],
        },
        "by_status": stats.by_status,
        "by_source": stats.by_source,
        "by_sector": stats.by_sector,
        "this_month": stats.leads_this_month,
        "this_week": stats.leads_this_week,
    }


# ============================================
# BULK ACTIONS
# ============================================

@router.post("/bulk")
async def bulk_action(
    data: BulkActionRequest,
    x_user_id: Optional[str] = Header(None, alias="X-User-Id"),
):
    """
    📦 Actions groupées sur plusieurs leads
    
    Actions supportées:
    - change_status: Changer le statut (value = new|qualify|warm|proposal|won|lost)
    - change_priority: Changer la priorité (value = low|medium|high|urgent)
    - delete: Supprimer les leads
    """
    results = {"success": 0, "failed": 0, "errors": []}
    
    for lead_id in data.lead_ids:
        try:
            if data.action == "change_status":
                status = LeadStatus(data.value)
                crm_pro_service.move_lead_in_pipeline(lead_id, status, x_user_id)
                results["success"] += 1
                
            elif data.action == "change_priority":
                priority = LeadPriority(data.value)
                update = LeadProUpdate(priority=priority)
                crm_pro_service.update_lead(lead_id, update, x_user_id, rescore=False)
                results["success"] += 1
                
            elif data.action == "delete":
                crm_pro_service.delete_lead(lead_id)
                results["success"] += 1
                
            else:
                results["failed"] += 1
                results["errors"].append(f"Action inconnue: {data.action}")
                
        except Exception as e:
            results["failed"] += 1
            results["errors"].append(f"{lead_id}: {str(e)}")
    
    return results


# ============================================
# ENUMS / REFERENCES
# ============================================

@router.get("/enums/status")
async def get_status_enum():
    """
    📋 Liste des statuts disponibles
    """
    return {
        "statuses": [
            {
                "value": status.value,
                "label": STATUS_NAMES.get(status, status.value),
                "color": STATUS_COLORS.get(status, "#666"),
            }
            for status in LeadStatus
        ]
    }


@router.get("/enums/source")
async def get_source_enum():
    """
    📋 Liste des sources disponibles
    """
    return {
        "sources": [
            {
                "value": source.value,
                "label": SOURCE_LABELS.get(source, source.value),
            }
            for source in LeadSource
        ]
    }


@router.get("/enums/sector")
async def get_sector_enum():
    """
    📋 Liste des secteurs disponibles
    """
    return {
        "sectors": [
            {"value": sector.value, "label": sector.value.replace("_", " ").title()}
            for sector in Sector
        ]
    }


@router.get("/enums/priority")
async def get_priority_enum():
    """
    📋 Liste des priorités disponibles
    """
    return {
        "priorities": [
            {"value": p.value, "label": p.value.title()}
            for p in LeadPriority
        ]
    }


@router.get("/enums/action-type")
async def get_action_type_enum():
    """
    📋 Liste des types d'actions disponibles
    """
    return {
        "action_types": [
            {"value": a.value, "label": a.value.replace("_", " ").title()}
            for a in ActionType
        ]
    }


# ============================================
# HEALTH CHECK
# ============================================

@router.get("/health")
async def health_check():
    """
    🏥 Vérifier l'état du service CRM PRO
    """
    stats = crm_pro_service.get_stats()
    
    return {
        "status": "healthy",
        "service": "CRM PRO",
        "version": "1.0.0",
        "leads_count": stats.total_leads,
        "hot_leads": stats.hot_leads_count,
        "conversion_rate": stats.conversion_rate,
        "features": [
            "kanban_pipeline",
            "ai_scoring",
            "ai_message_generation",
            "ai_next_action",
            "interactions_history",
            "bulk_actions",
            "advanced_filters",
        ],
        "ai_capabilities": [
            "lead_scoring_0_100",
            "whatsapp_message_generation",
            "email_generation",
            "next_action_suggestion",
            "action_scripts",
        ],
    }
