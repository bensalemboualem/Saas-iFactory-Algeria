"""
Hailuo AI 2.3 - Next-gen Video Generation (MiniMax)
Upgraded version with better quality and longer duration
Official: https://hailuoai.com/
"""

import os
import logging
from typing import Optional
import requests
from ..base import *

logger = logging.getLogger(__name__)


class Hailuo23Generator(BaseGenerator):
    """Hailuo AI 2.3 - Enhanced video generation by MiniMax"""

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv("HAILUO_AI_API_KEY")
        if not self.api_key:
            raise ValueError("Hailuo AI API key required")
        self.api_base = "https://api.minimax.chat/v1"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_video=True,
            max_duration_seconds=10.0,  # Upgraded from 5s to 10s
            max_resolution="1080p",
            api_cost_per_second=0.0,  # Free tier
            free_tier=True,
            free_credits_per_day=30,  # Upgraded from 20 to 30
            quality_score=88,  # Upgraded from 84 to 88
            avg_generation_time_seconds=80.0,  # Faster than v2
            supports_negative_prompts=True,
            supports_aspect_ratios=True,
            supports_style_presets=True
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.validate_request(request)

        try:
            params = {
                "model": "video-01",  # v2.3 model
                "prompt": request.prompt,
                "duration": min(request.duration_seconds, 10.0),
                "resolution": "1080p",
                "quality": "high"  # New parameter in 2.3
            }

            if request.negative_prompt:
                params["negative_prompt"] = request.negative_prompt

            if request.aspect_ratio:
                params["aspect_ratio"] = request.aspect_ratio

            if request.style:
                params["style"] = request.style

            response = self.session.post(
                f"{self.api_base}/video/generations",
                json=params,
                timeout=30
            )

            if response.status_code == 429:
                raise QuotaExceededError("Hailuo 2.3 daily quota exceeded (30 videos)")

            if response.status_code != 200:
                raise APIError(f"Hailuo 2.3 error: {response.text}")

            data = response.json()

            return GenerationResult(
                status=GenerationStatus.PROCESSING,
                task_id=data.get("task_id"),
                estimated_completion_time=80.0,
                estimated_cost_usd=0.0
            )

        except QuotaExceededError:
            raise
        except Exception as e:
            logger.error(f"Hailuo 2.3 generation error: {e}")
            raise APIError(f"Hailuo 2.3 error: {str(e)}")

    async def check_status(self, task_id: str) -> GenerationResult:
        try:
            response = self.session.get(
                f"{self.api_base}/video/generations/{task_id}",
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
                "pending": GenerationStatus.PROCESSING
            }
            status = status_map.get(status_str, GenerationStatus.PROCESSING)

            result = GenerationResult(status=status, task_id=task_id)

            if status == GenerationStatus.COMPLETED:
                result.output_url = data.get("video_url")
                result.thumbnail_url = data.get("thumbnail_url")  # New in 2.3
            elif status == GenerationStatus.FAILED:
                result.error_message = data.get("error", "Generation failed")

            return result

        except Exception as e:
            logger.error(f"Status check error: {e}")
            raise APIError(f"Status check failed: {str(e)}")

    async def cancel(self, task_id: str) -> bool:
        """Hailuo 2.3 supports cancellation"""
        try:
            response = self.session.delete(
                f"{self.api_base}/video/generations/{task_id}",
                timeout=10
            )
            return response.status_code == 200
        except:
            return False

    def __str__(self) -> str:
        return "Hailuo23Generator(FREE 30/day, Quality=88, Duration=10s)"
