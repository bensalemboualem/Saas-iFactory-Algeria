"""
Krea Video - AI Video Generation Platform
Creative video generation with AI
Official: https://www.krea.ai/
"""

import os
import logging
from typing import Optional
import requests
from ..base import *

logger = logging.getLogger(__name__)


class KreaVideoGenerator(BaseGenerator):
    """Krea Video - Creative AI video generation"""

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv("KREA_API_KEY")
        if not self.api_key:
            raise ValueError("Krea API key required")
        self.api_base = "https://api.krea.ai/v1"
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_video=True,
            max_duration_seconds=5.0,
            max_resolution="1080p",
            api_cost_per_second=0.015,
            free_tier=True,
            free_credits_per_day=15,
            quality_score=86,
            avg_generation_time_seconds=75.0,
            supports_negative_prompts=True,
            supports_style_presets=True
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.validate_request(request)

        try:
            params = {
                "prompt": request.prompt,
                "duration": min(request.duration_seconds, 5.0),
                "resolution": "1080p"
            }

            if request.negative_prompt:
                params["negative_prompt"] = request.negative_prompt

            if request.style:
                params["style"] = request.style

            response = self.session.post(
                f"{self.api_base}/video/generate",
                json=params,
                timeout=30
            )

            if response.status_code == 402:
                raise QuotaExceededError("Krea credits exhausted")

            if response.status_code != 200:
                raise APIError(f"Krea error: {response.text}")

            data = response.json()

            return GenerationResult(
                status=GenerationStatus.PROCESSING,
                task_id=data.get("id"),
                estimated_completion_time=75.0,
                estimated_cost_usd=request.duration_seconds * 0.015
            )

        except QuotaExceededError:
            raise
        except Exception as e:
            logger.error(f"Krea generation error: {e}")
            raise APIError(f"Krea error: {str(e)}")

    async def check_status(self, task_id: str) -> GenerationResult:
        try:
            response = self.session.get(
                f"{self.api_base}/video/{task_id}",
                timeout=10
            )

            if response.status_code != 200:
                raise APIError(f"Status check error: {response.text}")

            data = response.json()
            status_str = data.get("status", "processing")

            status_map = {
                "completed": GenerationStatus.COMPLETED,
                "failed": GenerationStatus.FAILED,
                "processing": GenerationStatus.PROCESSING,
                "queued": GenerationStatus.PROCESSING
            }
            status = status_map.get(status_str, GenerationStatus.PROCESSING)

            result = GenerationResult(status=status, task_id=task_id)

            if status == GenerationStatus.COMPLETED:
                result.output_url = data.get("video_url")
            elif status == GenerationStatus.FAILED:
                result.error_message = data.get("error_message", "Generation failed")

            return result

        except Exception as e:
            logger.error(f"Status check error: {e}")
            raise APIError(f"Status check failed: {str(e)}")

    async def cancel(self, task_id: str) -> bool:
        return False  # Krea doesn't support cancellation

    def __str__(self) -> str:
        return "KreaVideoGenerator(Freemium $0.015/s, Quality=86)"
