"""
IAFactory Video Studio Pro - API Routes pour les Scripts
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
import logging

from ...agents.scriptwriter import ScriptwriterAgent, create_scriptwriter_agent, VideoScript, ShortScript
from ...agents.director import DirectorRequest
from ...agents import AgentResponse

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/scripts",
    tags=["Scripts"],
)


# === MODÈLES DE REQUÊTES ===

class ScriptGenerationRequest(BaseModel):
    """Requête pour générer un nouveau script."""
    topic: str = Field(..., example="Comment investir en Algérie")
    target_audience: str = Field(..., example="Jeunes adultes algériens")
    platform: str = Field(..., example="youtube")
    duration: int = Field(300, example=300) # en secondes
    language: str = Field("fr", example="fr")
    tone: str = Field("engaging", example="engaging")
    context: Optional[str] = Field(None, example="Crise économique actuelle")


class ScriptUpdateRequest(BaseModel):
    """Requête pour mettre à jour un script existant."""
    title: Optional[str] = None
    hook: Optional[str] = None
    intro: Optional[str] = None
    segments: Optional[List[dict]] = None # Utilise dict car ScriptSegment est complexe
    outro: Optional[str] = None
    cta: Optional[str] = None
    status: Optional[str] = None # draft, approved, in_production, completed


class ScriptApprovalRequest(BaseModel):
    """Requête pour approuver un script."""
    approved_by: str = Field(..., example="admin@iafactory.ai")
    comments: Optional[str] = None


class ShortsExtractionRequest(BaseModel):
    """Requête pour extraire des shorts d'un script."""
    count: int = Field(3, ge=1, le=5) # Nombre de shorts à extraire


# === DÉPENDANCES ===

async def get_scriptwriter_agent() -> ScriptwriterAgent:
    """Dépendance pour obtenir l'agent Scriptwriter."""
    return create_scriptwriter_agent()


# === ROUTES ===

@router.post("/generate", response_model=VideoScript, status_code=status.HTTP_201_CREATED)
async def generate_new_script(
    request: ScriptGenerationRequest,
    scriptwriter: ScriptwriterAgent = Depends(get_scriptwriter_agent)
):
    """
    Génère un nouveau script vidéo en utilisant l'agent Scriptwriter.
    """
    logger.info(f"API: Génération de script demandée pour le sujet: {request.topic}")
    agent_response: AgentResponse = await scriptwriter.generate_script(**request.model_dump())
    
    if not agent_response.success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=agent_response.error)
    
    # Le data de l'agent_response est déjà un dict compatible avec VideoScript
    return VideoScript(**agent_response.data)


@router.get("/{script_id}", response_model=VideoScript)
async def get_script_by_id(
    script_id: str
):
    """
    Récupère un script vidéo par son ID.
    (Implémentation fictive, car pas encore de DB)
    """
    logger.info(f"API: Récupération du script demandé: {script_id}")
    # Ici, on devrait récupérer le script depuis une base de données
    # Pour l'instant, on retourne un script fictif
    if script_id == "dummy_script_id":
        return VideoScript(
            id="dummy_script_id",
            title="Comment devenir riche en IA",
            topic="Investissement IA",
            target_audience="Entrepreneur",
            platform="youtube",
            duration_target=300,
            language="fr",
            hook="Le secret des millionnaires de l'IA révélé !",
            intro="Bienvenue dans cette vidéo...",
            segments=[],
            outro="A bientôt !",
            cta="Abonnez-vous !",
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Script {script_id} non trouvé.")


@router.put("/{script_id}", response_model=VideoScript)
async def update_script(
    script_id: str,
    request: ScriptUpdateRequest
):
    """
    Met à jour un script vidéo existant.
    (Implémentation fictive, car pas encore de DB)
    """
    logger.info(f"API: Mise à jour du script demandé: {script_id}")
    # Ici, on devrait récupérer le script, le modifier et le sauvegarder
    # Pour l'instant, on suppose la mise à jour et on retourne un script de base
    if script_id == "dummy_script_id":
        updated_script = VideoScript(
            id="dummy_script_id",
            title=request.title or "Titre par défaut",
            topic="Investissement IA",
            target_audience="Entrepreneur",
            platform="youtube",
            duration_target=300,
            language="fr",
            hook="Le secret des millionnaires de l'IA révélé !",
            intro="Bienvenue dans cette vidéo...",
            segments=[],
            outro="A bientôt !",
            cta="Abonnez-vous !",
            status=request.status or "draft"
        )
        return updated_script
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Script {script_id} non trouvé.")


@router.post("/{script_id}/approve", response_model=VideoScript)
async def approve_script(
    script_id: str,
    approval_request: ScriptApprovalRequest
):
    """
    Approuve un script vidéo, le marquant comme prêt pour la production.
    (Implémentation fictive, car pas encore de DB)
    """
    logger.info(f"API: Approbation du script {script_id} par {approval_request.approved_by}")
    # Ici, on devrait mettre à jour le statut du script en DB
    if script_id == "dummy_script_id":
        approved_script = VideoScript(
            id="dummy_script_id",
            title="Comment devenir riche en IA",
            topic="Investissement IA",
            target_audience="Entrepreneur",
            platform="youtube",
            duration_target=300,
            language="fr",
            hook="Le secret des millionnaires de l'IA révélé !",
            intro="Bienvenue dans cette vidéo...",
            segments=[],
            outro="A bientôt !",
            cta="Abonnez-vous !",
            status="approved" # Statut mis à jour
        )
        return approved_script
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Script {script_id} non trouvé.")


@router.post("/{script_id}/extract-shorts", response_model=List[ShortScript])
async def extract_shorts_from_script(
    script_id: str,
    shorts_request: ShortsExtractionRequest,
    scriptwriter: ScriptwriterAgent = Depends(get_scriptwriter_agent)
):
    """
    Extrait les meilleurs moments d'un script pour créer des versions courtes (Shorts).
    """
    logger.info(f"API: Extraction de {shorts_request.count} shorts depuis le script {script_id}")
    
    # Ici, on devrait récupérer le script depuis la DB
    if script_id != "dummy_script_id":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Script {script_id} non trouvé.")
        
    dummy_script = VideoScript(
        id="dummy_script_id",
        title="Comment devenir riche en IA",
        topic="Investissement IA",
        target_audience="Entrepreneur",
        platform="youtube",
        duration_target=300,
        language="fr",
        hook="Le secret des millionnaires de l'IA révélé !",
        intro="Bienvenue dans cette vidéo...",
        segments=[], # Pour cet exemple, on simplifie
        outro="A bientôt !",
        cta="Abonnez-vous !",
    )
    
    agent_response: AgentResponse = await scriptwriter.extract_shorts(dummy_script, count=shorts_request.count)
    
    if not agent_response.success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=agent_response.error)
        
    return [ShortScript(**s) for s in agent_response.data.get("shorts", [])]
