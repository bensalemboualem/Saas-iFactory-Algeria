"""
IAFactory Video Studio Pro - Agent Distributor
Publication automatisée de contenu multimédia sur les réseaux sociaux via n8n.
"""

from typing import Any, Dict, List, Literal, Optional
from datetime import datetime
import logging
import aiohttp

from pydantic import BaseModel, Field

from . import (
    BaseAgent, 
    AgentConfig, 
    AgentResponse,
    CostTrackingMixin
)
from config import settings, agent_configs


logger = logging.getLogger(__name__)


# === MODÈLES DE DONNÉES ===

class PublicationMetadata(BaseModel):
    """Métadonnées pour la publication."""
    title: str
    description: str
    tags: List[str] = Field(default_factory=list)
    category: Optional[str] = None
    visibility: Literal["public", "private", "unlisted"] = "public"
    thumbnail_path: Optional[str] = None


class PublishRequest(BaseModel):
    """Requête pour publier une vidéo."""
    video_path: str
    platform: Literal["youtube", "tiktok", "instagram", "facebook", "all"]
    metadata: PublicationMetadata
    schedule_time: Optional[datetime] = None


class PublicationStatus(BaseModel):
    """Statut d'une tâche de publication."""
    success: bool
    publication_id: Optional[str] = None # ID de la tâche n8n ou de la publication
    status: Literal["queued", "in_progress", "completed", "failed"] = "queued"
    platform: str
    error: Optional[str] = None
    published_url: Optional[str] = None


# === AGENT DISTRIBUTOR ===

class DistributorAgent(BaseAgent, CostTrackingMixin):
    """
    Agent Distributor - Gère la publication automatisée du contenu.
    """
    
    SYSTEM_PROMPT = """Tu es un expert en publication automatisée sur les réseaux sociaux.
    Ta mission est d'assurer la bonne diffusion des vidéos sur les plateformes cibles via n8n."""

    def __init__(self):
        config = AgentConfig(
            name="Distributor",
            model="", # Pas de LLM direct pour cet agent
            system_prompt=self.SYSTEM_PROMPT
        )
        super().__init__(config)
        self.n8n_webhook_base_url = settings.N8N_WEBHOOK_BASE_URL
        if not self.n8n_webhook_base_url:
            logger.warning("[DistributorAgent] N8N_WEBHOOK_BASE_URL n'est pas configurée. Les publications ne fonctionneront pas.")
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Retourne une session HTTP réutilisable."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session
    
    async def close(self):
        """Ferme la session HTTP."""
        if self._session and not self._session.closed:
            await self._session.close()

    async def process(self, input_data: Any) -> AgentResponse:
        """Point d'entrée principal pour la publication."""
        if not isinstance(input_data, dict):
            return AgentResponse(success=False, agent_name=self.name, error="Input data must be a dictionary.")
            
        try:
            request = PublishRequest(**input_data)
            return await self.publish_video(request)
        except Exception as e:
            logger.error(f"[{self.name}] Erreur traitement publication: {str(e)}")
            return AgentResponse(success=False, agent_name=self.name, error=str(e))

    async def publish_video(self, request: PublishRequest) -> AgentResponse:
        """
        Envoie une requête de publication à n8n.
        """
        if not self.n8n_webhook_base_url:
            return AgentResponse(
                success=False,
                agent_name=self.name,
                error="N8N_WEBHOOK_BASE_URL non configurée."
            )
        
        # Déterminer le webhook spécifique (exemple)
        webhook_url = f"{self.n8n_webhook_base_url}/publish-{request.platform}"
        if request.schedule_time:
            webhook_url = f"{self.n8n_webhook_base_url}/schedule-publish-{request.platform}"
        
        payload = {
            "video_path": request.video_path,
            "platform": request.platform,
            "metadata": request.metadata.model_dump(),
            "schedule_time": request.schedule_time.isoformat() if request.schedule_time else None
        }
        
        logger.info(f"[{self.name}] Envoi de la tâche de publication à n8n: {webhook_url}")
        
        session = await self._get_session()
        try:
            async with session.post(webhook_url, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    publication_id = result.get("publication_id", "n/a")
                    published_url = result.get("published_url")
                    
                    logger.info(f"[{self.name}] Publication lancée via n8n (ID: {publication_id})")
                    return AgentResponse(
                        success=True,
                        data=PublicationStatus(
                            success=True,
                            publication_id=publication_id,
                            status="queued",
                            platform=request.platform,
                            published_url=published_url
                        ).model_dump(),
                        agent_name=self.name,
                        tokens_used=self.calculate_token_cost("publication", 1)
                    )
                else:
                    error_text = await response.text()
                    logger.error(f"[{self.name}] Erreur n8n ({response.status}): {error_text}")
                    return AgentResponse(
                        success=False,
                        agent_name=self.name,
                        error=f"Erreur n8n ({response.status}): {error_text}"
                    )
        except aiohttp.ClientError as e:
            logger.error(f"[{self.name}] Erreur connexion n8n: {e}")
            return AgentResponse(
                success=False,
                agent_name=self.name,
                error=f"Erreur de connexion à n8n: {e}"
            )
        except Exception as e:
            logger.error(f"[{self.name}] Exception publication: {str(e)}")
            return AgentResponse(
                success=False,
                agent_name=self.name,
                error=str(e)
            )

    async def get_publication_status(self, publication_id: str, platform: str) -> AgentResponse:
        """
        Récupère le statut d'une publication (nécessite que n8n expose une API de statut).
        (Implémentation fictive)
        """
        logger.warning(f"[{self.name}] La récupération du statut de publication n'est pas encore implémentée pour n8n.")
        return AgentResponse(
            success=False,
            agent_name=self.name,
            error="Récupération du statut non implémentée."
        )


# === FACTORY FUNCTION ===

def create_distributor_agent() -> DistributorAgent:
    """Crée une instance de l'agent Distributor."""
    return DistributorAgent()
