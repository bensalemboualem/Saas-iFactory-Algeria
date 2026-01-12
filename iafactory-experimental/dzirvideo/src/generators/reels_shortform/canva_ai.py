"""
Canva AI - AI Video Generation in Canva
Popular design platform with AI video features
Official: https://www.canva.com/
"""

import os
import logging
from typing import Optional
import requests
from ..base import *

logger = logging.getLogger(__name__)


class CanvaAIGenerator(BaseGenerator):
    """Canva AI - Video generation with design templates"""

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv("CANVA_API_KEY")
        if not self.api_key:
            raise ValueError("Canva API key required")
        self.api_base = "https://api.canva.com/v1"
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_video=True,
            supports_reels_shortform=True,
            max_duration_seconds=60.0,
            max_resolution="1080p",
            api_cost_per_second=0.005,
            free_tier=True,
            free_credits_per_day=10,
            quality_score=83,
            avg_generation_time_seconds=90.0,
            supports_style_presets=True
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.validate_request(request)

        try:
            params = {
                "type": "video",
                "prompt": request.prompt,
                "duration_seconds": int(request.duration_seconds),
                "format": "mp4"
            }

            if request.aspect_ratio:
                params["aspect_ratio"] = request.aspect_ratio

            if request.style:
                params["template"] = request.style

            response = self.session.post(
                f"{self.api_base}/autofill",
                json=params,
                timeout=30
            )

            if response.status_code == 429:
                raise QuotaExceededError("Canva daily quota exceeded")

            if response.status_code != 200:
                raise APIError(f"Canva error: {response.text}")

            data = response.json()
            job_id = data.get("job", {}).get("id")

            return GenerationResult(
                status=GenerationStatus.PROCESSING,
                task_id=job_id,
                estimated_completion_time=90.0,
                estimated_cost_usd=request.duration_seconds * 0.005
            )

        except QuotaExceededError:
            raise
        except Exception as e:
            logger.error(f"Canva generation error: {e}")
            raise APIError(f"Canva error: {str(e)}")

    async def check_status(self, task_id: str) -> GenerationResult:
        try:
            response = self.session.get(
                f"{self.api_base}/autofill/{task_id}",
                timeout=10
            )

            if response.status_code != 200:
                raise APIError(f"Status check error: {response.text}")

            data = response.json()
            job = data.get("job", {})
            status_str = job.get("status", "in_progress")

            if status_str == "success":
                status = GenerationStatus.COMPLETED
            elif status_str in ["failed", "error"]:
                status = GenerationStatus.FAILED
            else:
                status = GenerationStatus.PROCESSING

            result = GenerationResult(status=status, task_id=task_id)

            if status == GenerationStatus.COMPLETED:
                result.output_url = job.get("url")
            elif status == GenerationStatus.FAILED:
                result.error_message = job.get("error", {}).get("message", "Generation failed")

            return result

        except Exception as e:
            logger.error(f"Status check error: {e}")
            raise APIError(f"Status check failed: {str(e)}")

    async def cancel(self, task_id: str) -> bool:
        return False  # Canva doesn't support cancellation

    def __str__(self) -> str:
        return "CanvaAIGenerator(Freemium $0.005/s, Quality=83, Templates)"
