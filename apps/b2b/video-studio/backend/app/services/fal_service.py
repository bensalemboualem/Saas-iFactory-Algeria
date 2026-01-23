import httpx
import structlog
from typing import Optional
from app.core.config import settings

logger = structlog.get_logger()


class FalService:
    """Service for interacting with Fal.ai API"""
    
    BASE_URL = "https://queue.fal.run"
    
    MODELS = {
        "kling-1.6": "fal-ai/kling-video/v1.6/standard/text-to-video",
        "kling-i2v": "fal-ai/kling-video/v1.6/standard/image-to-video",
        "minimax": "fal-ai/minimax-video/video-01/text-to-video",
        "luma": "fal-ai/luma-dream-machine",
    }
    
    def __init__(self):
        self.api_key = settings.FAL_KEY
        
    async def text_to_video(
        self,
        prompt: str,
        duration: str = "5",
        aspect_ratio: str = "16:9",
        model: str = "kling-1.6",
    ) -> dict:
        """Generate video from text prompt"""
        model_path = self.MODELS.get(model, self.MODELS["kling-1.6"])
        
        async with httpx.AsyncClient(timeout=300.0) as client:
            # Submit request
            response = await client.post(
                f"{self.BASE_URL}/{model_path}",
                headers={
                    "Authorization": f"Key {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "prompt": prompt,
                    "duration": duration,
                    "aspect_ratio": aspect_ratio,
                },
            )
            response.raise_for_status()
            result = response.json()
            
            logger.info("Fal.ai text-to-video completed", model=model)
            
            return {
                "video_url": result.get("video", {}).get("url"),
                "duration": float(duration),
            }
    
    async def image_to_video(
        self,
        image_url: str,
        prompt: Optional[str] = None,
        duration: str = "5",
        aspect_ratio: str = "16:9",
    ) -> dict:
        """Animate an image into a video"""
        model_path = self.MODELS["kling-i2v"]
        
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(
                f"{self.BASE_URL}/{model_path}",
                headers={
                    "Authorization": f"Key {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "image_url": image_url,
                    "prompt": prompt or "",
                    "duration": duration,
                    "aspect_ratio": aspect_ratio,
                },
            )
            response.raise_for_status()
            result = response.json()
            
            logger.info("Fal.ai image-to-video completed")
            
            return {
                "video_url": result.get("video", {}).get("url"),
                "duration": float(duration),
            }
