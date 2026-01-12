import replicate
import structlog
from app.core.config import settings

logger = structlog.get_logger()


class ReplicateService:
    """Service for interacting with Replicate API"""
    
    def __init__(self):
        self.client = replicate.Client(api_token=settings.REPLICATE_API_TOKEN)
    
    async def run_model(self, model_id: str, input_data: dict) -> dict:
        """Run a model on Replicate"""
        try:
            output = self.client.run(model_id, input=input_data)
            logger.info("Replicate model completed", model=model_id)
            return {"output": output}
        except Exception as e:
            logger.error("Replicate error", model=model_id, error=str(e))
            raise
    
    async def generate_music(self, prompt: str, duration: int = 30) -> str:
        """Generate background music"""
        output = self.client.run(
            "meta/musicgen:b05b1dff1d8c6dc63d14b0cdb42135378dcb87f6373b0d3d341ede46e59e2b38",
            input={
                "prompt": prompt,
                "model_version": "melody",
                "output_format": "mp3",
                "duration": duration,
            }
        )
        return output
    
    async def upscale_video(self, video_url: str) -> str:
        """Upscale video resolution"""
        output = self.client.run(
            "lucataco/real-esrgan-video:c39a23a52b6206ea9c7a31f81a1b1df8f0efbdf99b5c81aa53c5c712a8f3d44c",
            input={
                "video": video_url,
                "scale": 2,
            }
        )
        return output
