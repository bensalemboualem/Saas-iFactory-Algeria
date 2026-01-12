"""
Pollo AI - Fast Video Generation Platform
Quick video generation with multiple styles
Official: https://www.pollo.ai/
"""

import os
import logging
from typing import Optional
import requests
from ..base import *

logger = logging.getLogger(__name__)


class PolloAIGenerator(BaseGenerator):
    """Pollo AI - Fast video generation with style presets"""

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv("POLLO_API_KEY")
        if not self.api_key:
            raise ValueError("Pollo AI API key required")
        self.api_base = "https://api.pollo.ai/v1"
        self.session = requests.Session()
        self.session.headers.update({"X-API-Key": self.api_key})

    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_video=True,
            max_duration_seconds=4.0,
            max_resolution="720p",
            api_cost_per_second=0.008,
            free_tier=True,
            free_credits_per_day=30,
            quality_score=79,
            avg_generation_time_seconds=45.0,  # Fast!
            supports_style_presets=True
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.validate_request(request)

        try:
            params = {
                "text": request.prompt,
                "duration": min(int(request.duration_seconds), 4),
                "quality": "high"
            }

            if request.style:
                params["style"] = request.style

            if request.aspect_ratio:
                params["aspect_ratio"] = request.aspect_ratio

            response = self.session.post(
                f"{self.api_base}/generate",
                json=params,
                timeout=30
            )

            if response.status_code == 429:
                raise QuotaExceededError("Pollo AI daily quota exceeded")

            if response.status_code != 200:
                raise APIError(f"Pollo AI error: {response.text}")

            data = response.json()

            return GenerationResult(
                status=GenerationStatus.PROCESSING,
                task_id=data.get("generation_id"),
                estimated_completion_time=45.0,
                estimated_cost_usd=request.duration_seconds * 0.008
            )

        except QuotaExceededError:
            raise
        except Exception as e:
            logger.error(f"Pollo AI generation error: {e}")
            raise APIError(f"Pollo AI error: {str(e)}")

    async def check_status(self, task_id: str) -> GenerationResult:
        try:
            response = self.session.get(
                f"{self.api_base}/status/{task_id}",
                timeout=10
            )

            if response.status_code != 200:
                raise APIError(f"Status check error: {response.text}")

            data = response.json()
            state = data.get("state", "processing").lower()

            if state in ["completed", "done", "success"]:
                status = GenerationStatus.COMPLETED
            elif state in ["failed", "error"]:
                status = GenerationStatus.FAILED
            else:
                status = GenerationStatus.PROCESSING

            result = GenerationResult(status=status, task_id=task_id)

            if status == GenerationStatus.COMPLETED:
                result.output_url = data.get("video_url")
            elif status == GenerationStatus.FAILED:
                result.error_message = data.get("error", "Generation failed")

            if "progress" in data:
                result.progress_percentage = float(data["progress"]) * 100

            return result

        except Exception as e:
            logger.error(f"Status check error: {e}")
            raise APIError(f"Status check failed: {str(e)}")

    async def cancel(self, task_id: str) -> bool:
        try:
            response = self.session.post(f"{self.api_base}/cancel/{task_id}")
            return response.status_code == 200
        except:
            return False

    def __str__(self) -> str:
        return "PolloAIGenerator(Freemium $0.008/s, Quality=79, Fast)"
