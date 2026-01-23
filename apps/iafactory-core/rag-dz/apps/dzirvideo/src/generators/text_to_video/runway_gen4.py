"""
Runway Gen-4 - State-of-the-Art Text-to-Video
Best-in-class video generation with cinematic quality
Official: https://runwayml.com/
"""

import os
import time
import logging
from typing import Optional, Dict
import asyncio
import requests

from ..base import (
    BaseGenerator,
    GeneratorCapabilities,
    GenerationRequest,
    GenerationResult,
    GenerationStatus,
    APIError,
    QuotaExceededError
)

logger = logging.getLogger(__name__)


class RunwayGen4Generator(BaseGenerator):
    """Runway Gen-4 - Meilleur générateur vidéo au monde (Quality: 95/100)"""

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv("RUNWAY_API_KEY")
        if not self.api_key:
            raise ValueError("Runway API key required")

        self.api_base = "https://api.runwayml.com/v1"
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})
        logger.info("Runway Gen-4 generator initialized")

    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_video=True, supports_image_to_video=True,
            max_duration_seconds=60.0, max_resolution="4K",
            supported_aspect_ratios=["16:9", "9:16", "1:1", "21:9"],
            api_cost_per_second=0.05,  # Premium pricing
            free_tier=False,
            quality_score=95, realism_score=95, coherence_score=96, prompt_adherence_score=94,
            avg_generation_time_seconds=90.0, supports_async=True,
            supports_negative_prompts=True, supports_style_presets=True
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.validate_request(request)
        params = {
            "prompt": request.prompt,
            "duration": int(request.duration_seconds or 5),
            "resolution": "1080p",
            "motion": "auto",
            "quality": "highest"
        }

        try:
            resp = self.session.post(f"{self.api_base}/generations", json=params, timeout=30)
            if resp.status_code == 402:
                raise QuotaExceededError("Runway quota exceeded")
            if resp.status_code != 200:
                raise APIError(f"Runway error: {resp.text}")

            task_id = resp.json().get("id")
            logger.info(f"Runway Gen-4 started: {task_id}")
            return GenerationResult(
                status=GenerationStatus.PROCESSING,
                task_id=task_id,
                estimated_completion_time=90.0,
                estimated_cost_usd=self.estimate_cost(request)
            )

        except Exception as e:
            raise APIError(f"Runway failed: {str(e)}")

    async def check_status(self, task_id: str) -> GenerationResult:
        resp = self.session.get(f"{self.api_base}/generations/{task_id}", timeout=10)
        data = resp.json()
        status_map = {
            "pending": GenerationStatus.PENDING,
            "processing": GenerationStatus.PROCESSING,
            "succeeded": GenerationStatus.COMPLETED,
            "failed": GenerationStatus.FAILED
        }
        status = status_map.get(data.get("status"), GenerationStatus.PROCESSING)

        result = GenerationResult(status=status, task_id=task_id)
        if status == GenerationStatus.COMPLETED:
            result.output_url = data.get("outputs", [{}])[0].get("url")
            if result.output_url:
                logger.info(f"Runway Gen-4 completed: {result.output_url}")
        elif status == GenerationStatus.FAILED:
            result.error_message = data.get("failure_reason", "Generation failed")

        return result

    async def cancel(self, task_id: str) -> bool:
        try:
            resp = self.session.post(f"{self.api_base}/generations/{task_id}/cancel", timeout=10)
            return resp.status_code == 200
        except:
            return False

    def __str__(self) -> str:
        return "RunwayGen4Generator(SOTA, Premium $0.05/s, Quality=95)"
