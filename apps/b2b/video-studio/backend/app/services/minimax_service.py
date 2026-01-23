"""
MiniMax (Hailuo AI) Video Generation Service
Génération de vidéos haute qualité avec l'API MiniMax/Hailuo
"""

import httpx
import asyncio
from typing import Optional, Dict, Any, Literal
from pydantic import BaseModel
import structlog
from enum import Enum

logger = structlog.get_logger()


class VideoStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class MiniMaxVideoRequest(BaseModel):
    prompt: str
    duration: int = 5  # 5 ou 10 secondes
    aspect_ratio: Literal["16:9", "9:16", "1:1"] = "16:9"
    quality: Literal["standard", "high"] = "high"
    motion: Literal["low", "medium", "high"] = "medium"
    image_url: Optional[str] = None  # Pour image-to-video


class MiniMaxVideoResponse(BaseModel):
    job_id: str
    status: VideoStatus
    video_url: Optional[str] = None
    progress: float = 0
    error: Optional[str] = None
    estimated_time: Optional[int] = None


class MiniMaxService:
    """Service de génération vidéo avec MiniMax/Hailuo AI"""

    def __init__(
        self,
        api_key: str,
        group_id: str,
        base_url: str = "https://api.minimaxi.chat/v1"
    ):
        self.api_key = api_key
        self.group_id = group_id
        self.base_url = base_url
        self.client = httpx.AsyncClient(
            timeout=120.0,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
        )

    async def text_to_video(
        self,
        prompt: str,
        duration: int = 5,
        aspect_ratio: Literal["16:9", "9:16", "1:1"] = "16:9",
        quality: str = "high",
        motion: str = "medium"
    ) -> MiniMaxVideoResponse:
        """
        Génère une vidéo à partir d'un prompt textuel.
        
        Args:
            prompt: Description de la vidéo
            duration: Durée en secondes (5 ou 10)
            aspect_ratio: Ratio d'aspect
            quality: Qualité de rendu
            motion: Niveau de mouvement
            
        Returns:
            MiniMaxVideoResponse avec job_id pour polling
        """
        try:
            payload = {
                "model": "video-01",
                "prompt": prompt,
                "duration": duration,
                "aspect_ratio": aspect_ratio,
                "quality": quality,
                "motion": motion,
                "group_id": self.group_id
            }

            response = await self.client.post(
                f"{self.base_url}/video/generations",
                json=payload
            )
            response.raise_for_status()
            data = response.json()

            logger.info(
                "MiniMax video generation started",
                job_id=data.get("task_id"),
                prompt=prompt[:50]
            )

            return MiniMaxVideoResponse(
                job_id=data.get("task_id", ""),
                status=VideoStatus.PENDING,
                estimated_time=duration * 20  # ~20 sec per second of video
            )

        except httpx.HTTPStatusError as e:
            logger.error("MiniMax API error", status=e.response.status_code, error=str(e))
            return MiniMaxVideoResponse(
                job_id="",
                status=VideoStatus.FAILED,
                error=f"API Error: {e.response.status_code}"
            )
        except Exception as e:
            logger.error("MiniMax error", error=str(e))
            return MiniMaxVideoResponse(
                job_id="",
                status=VideoStatus.FAILED,
                error=str(e)
            )

    async def image_to_video(
        self,
        image_url: str,
        prompt: str,
        duration: int = 5,
        motion: str = "medium"
    ) -> MiniMaxVideoResponse:
        """
        Anime une image en vidéo.
        
        Args:
            image_url: URL de l'image source
            prompt: Description du mouvement souhaité
            duration: Durée en secondes
            motion: Intensité du mouvement
            
        Returns:
            MiniMaxVideoResponse
        """
        try:
            payload = {
                "model": "video-01-img2video",
                "image_url": image_url,
                "prompt": prompt,
                "duration": duration,
                "motion": motion,
                "group_id": self.group_id
            }

            response = await self.client.post(
                f"{self.base_url}/video/generations/image",
                json=payload
            )
            response.raise_for_status()
            data = response.json()

            return MiniMaxVideoResponse(
                job_id=data.get("task_id", ""),
                status=VideoStatus.PENDING,
                estimated_time=duration * 15
            )

        except Exception as e:
            logger.error("MiniMax image-to-video error", error=str(e))
            return MiniMaxVideoResponse(
                job_id="",
                status=VideoStatus.FAILED,
                error=str(e)
            )

    async def get_status(self, job_id: str) -> MiniMaxVideoResponse:
        """
        Récupère le statut d'une génération.
        
        Args:
            job_id: ID de la tâche
            
        Returns:
            MiniMaxVideoResponse avec statut et URL si complété
        """
        try:
            response = await self.client.get(
                f"{self.base_url}/video/generations/{job_id}",
                params={"group_id": self.group_id}
            )
            response.raise_for_status()
            data = response.json()

            status = data.get("status", "").lower()
            if status == "completed":
                return MiniMaxVideoResponse(
                    job_id=job_id,
                    status=VideoStatus.COMPLETED,
                    video_url=data.get("video_url"),
                    progress=100
                )
            elif status in ["failed", "error"]:
                return MiniMaxVideoResponse(
                    job_id=job_id,
                    status=VideoStatus.FAILED,
                    error=data.get("error", "Unknown error")
                )
            else:
                return MiniMaxVideoResponse(
                    job_id=job_id,
                    status=VideoStatus.PROCESSING,
                    progress=data.get("progress", 0)
                )

        except Exception as e:
            logger.error("MiniMax status check error", job_id=job_id, error=str(e))
            return MiniMaxVideoResponse(
                job_id=job_id,
                status=VideoStatus.FAILED,
                error=str(e)
            )

    async def wait_for_completion(
        self,
        job_id: str,
        max_wait: int = 300,
        poll_interval: int = 5
    ) -> MiniMaxVideoResponse:
        """
        Attend la fin de la génération avec polling.
        
        Args:
            job_id: ID de la tâche
            max_wait: Temps max d'attente en secondes
            poll_interval: Intervalle de polling
            
        Returns:
            MiniMaxVideoResponse final
        """
        elapsed = 0
        while elapsed < max_wait:
            result = await self.get_status(job_id)
            
            if result.status in [VideoStatus.COMPLETED, VideoStatus.FAILED]:
                return result
            
            await asyncio.sleep(poll_interval)
            elapsed += poll_interval
            
            logger.debug(
                "MiniMax polling",
                job_id=job_id,
                elapsed=elapsed,
                progress=result.progress
            )

        return MiniMaxVideoResponse(
            job_id=job_id,
            status=VideoStatus.FAILED,
            error="Timeout: generation took too long"
        )

    async def close(self):
        """Ferme le client HTTP."""
        await self.client.aclose()


# Factory function
def create_minimax_service(
    api_key: str = None,
    group_id: str = None
) -> MiniMaxService:
    """
    Crée une instance du service MiniMax.
    
    Args:
        api_key: Clé API MiniMax
        group_id: Group ID MiniMax
        
    Returns:
        MiniMaxService configuré
    """
    import os
    
    api_key = api_key or os.getenv("MINIMAX_API_KEY", "")
    group_id = group_id or os.getenv("MINIMAX_GROUP_ID", "")
    
    if not api_key:
        logger.warning("MiniMax API key not configured")
    
    return MiniMaxService(api_key=api_key, group_id=group_id)
