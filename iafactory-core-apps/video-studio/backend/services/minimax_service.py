"""
IAFactory Video Studio Pro - Service MiniMax
Génération vidéo via l'API MiniMax/Hailuo
"""

from typing import Any, Dict, List, Literal, Optional
import asyncio
import aiohttp
import aiofiles
import logging
from pathlib import Path

from pydantic import BaseModel, Field

from config import settings


logger = logging.getLogger(__name__)


# === MODÈLES ===

class VideoGenerationRequest(BaseModel):
    """Requête de génération vidéo."""
    prompt: str
    duration_seconds: int = 10
    aspect_ratio: Literal["16:9", "9:16", "1:1"] = "16:9"
    fps: int = 24
    high_quality: bool = True
    
    
class ImageVideoGenerationRequest(BaseModel):
    """Requête de génération vidéo à partir d'une image."""
    image_path: str
    motion_prompt: Optional[str] = None
    motion_strength: float = 0.5


class VideoGenerationStatus(BaseModel):
    """Réponse de l'API de génération vidéo."""
    success: bool
    job_id: Optional[str] = None
    status: Literal["queued", "processing", "completed", "failed"] = "queued"
    progress: int = 0
    video_url: Optional[str] = None
    cost_tokens: int = 0
    error: Optional[str] = None


# === SERVICE MINIMAX ===

class MiniMaxService:
    """
    Service pour la génération vidéo via l'API MiniMax/Hailuo.
    
    Fonctionnalités:
    - Text-to-Video
    - Image-to-Video
    """
    
    BASE_URL = "https://api.minimax.cn/v1/videos/generation"  # URL Fictive
    
    def __init__(self):
        self.api_key = settings.MINIMAX_API_KEY
        self.group_id = settings.MINIMAX_GROUP_ID
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Retourne une session HTTP réutilisable."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(headers=self.headers)
        return self._session
    
    async def close(self):
        """Ferme la session HTTP."""
        if self._session and not self._session.closed:
            await self._session.close()

    async def text_to_video(self, request: VideoGenerationRequest) -> VideoGenerationStatus:
        """
        Lance une tâche de génération de vidéo à partir d'un prompt texte.
        """
        try:
            url = f"{self.BASE_URL}/text_to_video" # URL Fictive
            
            payload = {
                "prompt": request.prompt,
                "duration": request.duration_seconds,
                "aspect_ratio": request.aspect_ratio,
                "fps": request.fps,
                "hq": request.high_quality,
            }
            
            logger.info(f"[MiniMax] Text-to-Video request: '{request.prompt[:30]}...'")
            
            session = await self._get_session()
            
            async with session.post(url, json=payload) as response:
                if response.status != 202:  # 202 Accepted pour les tâches asynchrones
                    error_text = await response.text()
                    logger.error(f"[MiniMax] Erreur API: {response.status} - {error_text}")
                    return VideoGenerationStatus(success=False, error=f"API Error {response.status}: {error_text}")
                
                result = await response.json()
                job_id = result.get("job_id")
                
                logger.info(f"[MiniMax] Tâche de génération lancée: {job_id}")
                
                return VideoGenerationStatus(success=True, job_id=job_id, status="queued")
                
        except Exception as e:
            logger.error(f"[MiniMax] Exception in text_to_video: {str(e)}")
            return VideoGenerationStatus(success=False, error=str(e))

    async def image_to_video(self, request: ImageVideoGenerationRequest) -> VideoGenerationStatus:
        """
        Lance une tâche de génération de vidéo à partir d'une image.
        (Implémentation fictive, nécessite upload multipart/form-data)
        """
        logger.warning("[MiniMax] image_to_video n'est pas encore implémenté.")
        # La logique réelle impliquerait aiohttp.FormData pour uploader l'image
        # et les paramètres.
        return VideoGenerationStatus(
            success=False, 
            error="Not yet implemented",
            status="failed"
        )

    async def get_generation_status(self, job_id: str) -> VideoGenerationStatus:
        """
        Récupère le statut d'une tâche de génération vidéo.
        """
        try:
            url = f"{self.BASE_URL}/status/{job_id}" # URL Fictive
            
            logger.info(f"[MiniMax] Vérification du statut pour la tâche: {job_id}")
            
            session = await self._get_session()
            
            async with session.get(url) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"[MiniMax] Erreur statut API: {response.status} - {error_text}")
                    return VideoGenerationStatus(success=False, job_id=job_id, status="failed", error=f"API Error {response.status}: {error_text}")
                
                result = await response.json()
                status = result.get("status", "failed")
                progress = result.get("progress", 0)
                video_url = result.get("video_url")
                
                logger.info(f"[MiniMax] Statut tâche {job_id}: {status} ({progress}%)")
                
                return VideoGenerationStatus(
                    success=True,
                    job_id=job_id,
                    status=status,
                    progress=progress,
                    video_url=video_url,
                    cost_tokens=200 if status == "completed" else 0 # Coût Fictif
                )
                
        except Exception as e:
            logger.error(f"[MiniMax] Exception in get_generation_status: {str(e)}")
            return VideoGenerationStatus(success=False, job_id=job_id, status="failed", error=str(e))


# === FACTORY FUNCTION ===

_minimax_service: Optional[MiniMaxService] = None

def get_minimax_service() -> MiniMaxService:
    """Retourne l'instance singleton du service MiniMax."""
    global _minimax_service
    if _minimax_service is None:
        _minimax_service = MiniMaxService()
    return _minimax_service
