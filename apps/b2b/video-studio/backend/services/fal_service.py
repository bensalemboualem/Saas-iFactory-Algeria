"""
IAFactory Video Studio Pro - Service Fal.ai
Génération d'images et vidéos rapides via Fal.ai
"""

from typing import Any, Dict, List, Optional, Literal
import asyncio
import aiohttp
import logging
from pathlib import Path

from pydantic import BaseModel, Field

from config import settings


logger = logging.getLogger(__name__)


# === MODÈLES ===

class ImageGenerationRequest(BaseModel):
    """Requête de génération d'image."""
    prompt: str
    model_id: str = "sdxl-turbo" # Exemple de modèle Fal.ai
    image_size: Literal["1024x1024", "768x768", "512x512"] = "1024x1024"
    num_images: int = 1


class FalVideoGenerationRequest(BaseModel):
    """Requête de génération vidéo (texte ou image)."""
    prompt: Optional[str] = None
    image_url: Optional[str] = None # Pour image-to-video
    model_id: str = "luma-dream-machine" # Exemple de modèle Fal.ai
    duration_seconds: int = 4
    high_quality: bool = True


class FalGenerationResponse(BaseModel):
    """Réponse de l'API Fal.ai pour les tâches asynchrones."""
    success: bool
    job_id: Optional[str] = None
    status: Literal["queued", "in progress", "completed", "failed"] = "queued"
    result_url: Optional[str] = None # URL de l'image/vidéo finale
    error: Optional[str] = None
    cost_tokens: int = 0


# === SERVICE FAL.AI ===

class FalService:
    """
    Service pour la génération d'images et de vidéos via l'API Fal.ai.
    
    Fonctionnalités:
    - Génération d'images
    - Text-to-Video
    - Image-to-Video
    """
    
    BASE_URL = "https://rest.fal.ai"
    
    def __init__(self):
        self.api_key = settings.FAL_API_KEY
        self.headers = {
            "Authorization": f"Key {self.api_key}", # Fal.ai utilise "Key"
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

    async def generate_image(self, request: ImageGenerationRequest) -> FalGenerationResponse:
        """
        Génère une image à partir d'un prompt texte.
        """
        try:
            url = f"{self.BASE_URL}/sdxl-turbo/generate" # Exemple pour sdxl-turbo
            
            payload = {
                "prompt": request.prompt,
                "image_size": request.image_size,
                "num_images": request.num_images,
            }
            
            logger.info(f"[Fal.ai] Image generation request: '{request.prompt[:30]}...'")
            
            session = await self._get_session()
            
            async with session.post(url, json=payload) as response:
                if response.status != 200: # Fal.ai peut renvoyer directement le résultat
                    error_text = await response.text()
                    logger.error(f"[Fal.ai] Erreur API: {response.status} - {error_text}")
                    return FalGenerationResponse(success=False, error=f"API Error {response.status}: {error_text}")
                
                result = await response.json()
                image_url = result.get("image_url") # Supposons que l'URL est directe
                
                logger.info(f"[Fal.ai] Image générée: {image_url}")
                
                return FalGenerationResponse(success=True, status="completed", result_url=image_url, cost_tokens=5) # Coût fictif
                
        except Exception as e:
            logger.error(f"[Fal.ai] Exception in generate_image: {str(e)}")
            return FalGenerationResponse(success=False, error=str(e))

    async def text_to_video(self, request: FalVideoGenerationRequest) -> FalGenerationResponse:
        """
        Lance une tâche de génération de vidéo à partir d'un prompt texte.
        """
        try:
            url = f"{self.BASE_URL}/{request.model_id}/generate_async" # Exemple pour Luma Dream Machine
            
            payload = {
                "prompt": request.prompt,
                "duration": request.duration_seconds,
                "high_quality": request.high_quality,
            }
            
            logger.info(f"[Fal.ai] Text-to-Video request (model={request.model_id}): '{request.prompt[:30]}...'")
            
            session = await self._get_session()
            
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"[Fal.ai] Erreur API: {response.status} - {error_text}")
                    return FalGenerationResponse(success=False, error=f"API Error {response.status}: {error_text}")
                
                result = await response.json()
                job_id = result.get("job_id")
                
                logger.info(f"[Fal.ai] Tâche vidéo lancée: {job_id}")
                
                return FalGenerationResponse(success=True, job_id=job_id, status="queued")
                
        except Exception as e:
            logger.error(f"[Fal.ai] Exception in text_to_video: {str(e)}")
            return FalGenerationResponse(success=False, error=str(e))

    async def image_to_video(self, request: FalVideoGenerationRequest) -> FalGenerationResponse:
        """
        Lance une tâche de génération de vidéo à partir d'une image.
        """
        if not request.image_url:
            return FalGenerationResponse(success=False, error="Image URL is required for image-to-video")

        try:
            url = f"{self.BASE_URL}/{request.model_id}/image_to_video_async" # Exemple
            
            payload = {
                "image_url": request.image_url,
                "prompt": request.prompt, # Optionnel
                "duration": request.duration_seconds,
                "high_quality": request.high_quality,
            }
            
            logger.info(f"[Fal.ai] Image-to-Video request (model={request.model_id}): '{request.image_url}'")
            
            session = await self._get_session()
            
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"[Fal.ai] Erreur API: {response.status} - {error_text}")
                    return FalGenerationResponse(success=False, error=f"API Error {response.status}: {error_text}")
                
                result = await response.json()
                job_id = result.get("job_id")
                
                logger.info(f"[Fal.ai] Tâche vidéo image lancée: {job_id}")
                
                return FalGenerationResponse(success=True, job_id=job_id, status="queued")
                
        except Exception as e:
            logger.error(f"[Fal.ai] Exception in image_to_video: {str(e)}")
            return FalGenerationResponse(success=False, error=str(e))

    async def get_job_status(self, job_id: str) -> FalGenerationResponse:
        """
        Récupère le statut d'une tâche de génération (image ou vidéo) Fal.ai.
        """
        try:
            url = f"{self.BASE_URL}/jobs/{job_id}" # URL Générique pour le statut
            
            logger.info(f"[Fal.ai] Vérification du statut pour la tâche: {job_id}")
            
            session = await self._get_session()
            
            async with session.get(url) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"[Fal.ai] Erreur statut API: {response.status} - {error_text}")
                    return FalGenerationResponse(success=False, job_id=job_id, status="failed", error=f"API Error {response.status}: {error_text}")
                
                result = await response.json()
                status = result.get("status", "failed")
                result_url = result.get("result", {}).get("url") # Fal.ai stocke le résultat sous 'result.url'
                
                logger.info(f"[Fal.ai] Statut tâche {job_id}: {status}")
                
                return FalGenerationResponse(
                    success=True,
                    job_id=job_id,
                    status=status,
                    result_url=result_url,
                    cost_tokens=10 if status == "completed" else 0 # Coût fictif
                )
                
        except Exception as e:
            logger.error(f"[Fal.ai] Exception in get_job_status: {str(e)}")
            return FalGenerationResponse(success=False, job_id=job_id, status="failed", error=str(e))


# === FACTORY FUNCTION ===

_fal_service: Optional[FalService] = None

def get_fal_service() -> FalService:
    """Retourne l'instance singleton du service Fal.ai."""
    global _fal_service
    if _fal_service is None:
        _fal_service = FalService()
    return _fal_service
