"""
Vidnoz AI - Avatar Video Generator
AI avatars with voice synthesis for professional videos
Official: https://www.vidnoz.com/
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


class VidnozGenerator(BaseGenerator):
    """Vidnoz AI Avatar Video Generator - avatars + voix professionnels"""

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv("VIDNOZ_API_KEY")
        if not self.api_key:
            raise ValueError("Vidnoz API key required")

        self.api_base = "https://api.vidnoz.com/v1"
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})
        logger.info("Vidnoz AI generator initialized")

    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_video=True,
            supports_avatar_video=True,
            max_duration_seconds=300.0,
            max_resolution="1080p",
            supported_aspect_ratios=["16:9", "9:16", "1:1"],
            api_cost_per_second=0.01,
            free_tier=True,
            free_credits_per_day=10,
            quality_score=85,
            avg_generation_time_seconds=60.0,
            supports_async=True
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.validate_request(request)
        params = {"script": request.prompt, "avatar_id": "professional_female_01", "voice_id": "en-US-Neural"}

        try:
            resp = self.session.post(f"{self.api_base}/video/create", json=params, timeout=30)
            if resp.status_code != 200:
                raise APIError(f"Vidnoz error: {resp.text}")

            task_id = resp.json().get("task_id")
            logger.info(f"Vidnoz started: {task_id}")
            return GenerationResult(status=GenerationStatus.PROCESSING, task_id=task_id, estimated_completion_time=60.0)

        except Exception as e:
            raise APIError(f"Vidnoz failed: {str(e)}")

    async def check_status(self, task_id: str) -> GenerationResult:
        resp = self.session.get(f"{self.api_base}/video/status/{task_id}", timeout=10)
        data = resp.json()
        status_map = {"processing": GenerationStatus.PROCESSING, "completed": GenerationStatus.COMPLETED, "failed": GenerationStatus.FAILED}
        status = status_map.get(data.get("status", "processing"), GenerationStatus.PROCESSING)

        result = GenerationResult(status=status, task_id=task_id)
        if status == GenerationStatus.COMPLETED:
            result.output_url = data.get("video_url")
        return result

    async def cancel(self, task_id: str) -> bool:
        try:
            resp = self.session.delete(f"{self.api_base}/video/{task_id}", timeout=10)
            return resp.status_code == 200
        except:
            return False

    def __str__(self) -> str:
        return "VidnozGenerator(Avatars, Freemium, Quality=85)"
