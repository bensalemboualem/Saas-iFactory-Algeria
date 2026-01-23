"""
IAFactory Video Studio Pro - API Routes pour la Publication
"""

from typing import List, Optional, Literal
from fastapi import APIRouter, Depends, HTTPException, status
import logging
from datetime import datetime

from ...agents.distributor import DistributorAgent, create_distributor_agent, PublishRequest, PublicationStatus, PublicationMetadata

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/publish",
    tags=["Publication"],
)


# === MODÈLES DE REQUÊTES ===

class PublishContentRequest(BaseModel):
    """Requête pour publier du contenu sur une plateforme."""
    video_path: str = Field(..., example="/tmp/final_video.mp4")
    metadata: PublicationMetadata
    schedule_time: Optional[datetime] = None


# === DÉPENDANCES ===

async def get_distributor() -> DistributorAgent:
    return create_distributor_agent()


# === ROUTES ===

@router.post("/{platform}", response_model=PublicationStatus, status_code=status.HTTP_202_ACCEPTED)
async def publish_content_to_platform(
    platform: Literal["youtube", "tiktok", "instagram", "facebook"],
    request: PublishContentRequest,
    distributor: DistributorAgent = Depends(get_distributor)
):
    """
    Lance la publication d'une vidéo sur une plateforme spécifique.
    """
    logger.info(f"API: Demande de publication sur {platform} pour la vidéo: {request.video_path}")
    
    publish_req = PublishRequest(
        video_path=request.video_path,
        platform=platform,
        metadata=request.metadata,
        schedule_time=request.schedule_time
    )
    
    agent_response: AgentResponse = await distributor.publish_video(publish_req)
    
    if not agent_response.success or not agent_response.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Échec de la publication: {agent_response.error}"
        )
    
    return PublicationStatus(**agent_response.data)


@router.get("/{publication_id}/status", response_model=PublicationStatus)
async def get_publication_status(
    publication_id: str,
    platform: str, # Peut être utilisé pour router vers le bon sous-système si n8n a des statuts différents
    distributor: DistributorAgent = Depends(get_distributor)
):
    """
    Récupère le statut d'une tâche de publication.
    """
    logger.info(f"API: Vérification du statut de publication {publication_id} sur {platform}")
    
    agent_response: AgentResponse = await distributor.get_publication_status(publication_id, platform)
    
    if not agent_response.success or not agent_response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Statut de publication {publication_id} non trouvé ou erreur: {agent_response.error}"
        )
        
    return PublicationStatus(**agent_response.data)
