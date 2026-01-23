"""
Nano - Ultra-fast compact video generation
Optimized for speed over quality, perfect for rapid prototyping
Official: https://nano.ai/
"""

import os
import logging
from typing import Optional
import requests
from ..base import *

logger = logging.getLogger(__name__)


class NanoGenerator(BaseGenerator):
    """Nano - Fast lightweight video generation (30-40s generation time)"""

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv("NANO_API_KEY")
        if not self.api_key:
            raise ValueError("Nano API key required")
        self.api_base = "https://api.nano.ai/v1"
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_video=True,
            max_duration_seconds=5.0,
            max_resolution="720p",  # Lower res for speed
            api_cost_per_second=0.002,  # Very cheap
            free_tier=True,
            free_credits_per_day=50,  # High free quota
            quality_score=72,  # Lower quality, optimized for speed
            avg_generation_time_seconds=35.0,  # FASTEST generator
            supports_negative_prompts=False,
            supports_aspect_ratios=True,
            supports_style_presets=False
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.validate_request(request)

        try:
            params = {
                "prompt": request.prompt,
                "duration": min(request.duration_seconds, 5.0),
                "resolution": "720p",  # Fixed for speed
                "mode": "fast"  # Nano optimized mode
            }

            if request.aspect_ratio:
                params["aspect_ratio"] = request.aspect_ratio

            response = self.session.post(
                f"{self.api_base}/generate",
                json=params,
                timeout=20
            )

            if response.status_code == 402:
                raise QuotaExceededError("Nano daily quota exceeded (50 videos)")

            if response.status_code != 200:
                raise APIError(f"Nano error: {response.text}")

            data = response.json()

            return GenerationResult(
                status=GenerationStatus.PROCESSING,
                task_id=data.get("id"),
                estimated_completion_time=35.0,  # Very fast
                estimated_cost_usd=request.duration_seconds * 0.002
            )

        except QuotaExceededError:
            raise
        except Exception as e:
            logger.error(f"Nano generation error: {e}")
            raise APIError(f"Nano error: {str(e)}")

    async def check_status(self, task_id: str) -> GenerationResult:
        try:
            response = self.session.get(
                f"{self.api_base}/status/{task_id}",
                timeout=10
            )

            if response.status_code != 200:
                raise APIError(f"Status check error: {response.text}")

            data = response.json()
            status_str = data.get("status", "processing")

            status_map = {
                "done": GenerationStatus.COMPLETED,
                "failed": GenerationStatus.FAILED,
                "processing": GenerationStatus.PROCESSING,
                "queued": GenerationStatus.PROCESSING
            }
            status = status_map.get(status_str, GenerationStatus.PROCESSING)

            result = GenerationResult(status=status, task_id=task_id)

            if status == GenerationStatus.COMPLETED:
                result.output_url = data.get("url")
            elif status == GenerationStatus.FAILED:
                result.error_message = data.get("error", "Generation failed")

            return result

        except Exception as e:
            logger.error(f"Status check error: {e}")
            raise APIError(f"Status check failed: {str(e)}")

    async def cancel(self, task_id: str) -> bool:
        return False  # Nano doesn't support cancellation (too fast anyway)

    def __str__(self) -> str:
        return "NanoGenerator(Freemium $0.002/s, Quality=72, FASTEST=35s)"
