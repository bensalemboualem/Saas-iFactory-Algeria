"""
InVideo AI - AI Video Creation Platform
Generate videos from text prompts with templates
Official: https://invideo.io/
"""

import os
import logging
from typing import Optional
import requests
from ..base import *

logger = logging.getLogger(__name__)


class InVideoAIGenerator(BaseGenerator):
    """InVideo AI - Génération vidéo à partir de prompts texte (populaire marketing)"""

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv("INVIDEO_API_KEY")
        if not self.api_key:
            raise ValueError("InVideo API key required")
        self.api_base = "https://api.invideo.io/v2"
        self.session = requests.Session()
        self.session.headers.update({"x-api-key": self.api_key})

    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_video=True, supports_reels_shortform=True,
            max_duration_seconds=300.0, max_resolution="1080p",
            api_cost_per_second=0.01, free_tier=True, free_credits_per_day=10,
            quality_score=84, avg_generation_time_seconds=120.0
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.validate_request(request)
        params = {"prompt": request.prompt, "template": "social_media", "duration": int(request.duration_seconds or 30)}
        resp = self.session.post(f"{self.api_base}/videos", json=params, timeout=30)
        if resp.status_code != 200:
            raise APIError(f"InVideo error: {resp.text}")
        task_id = resp.json().get("video_id")
        return GenerationResult(status=GenerationStatus.PROCESSING, task_id=task_id, estimated_completion_time=120.0)

    async def check_status(self, task_id: str) -> GenerationResult:
        resp = self.session.get(f"{self.api_base}/videos/{task_id}", timeout=10)
        data = resp.json()
        status = GenerationStatus.COMPLETED if data.get("status") == "ready" else GenerationStatus.PROCESSING
        result = GenerationResult(status=status, task_id=task_id)
        if status == GenerationStatus.COMPLETED:
            result.output_url = data.get("download_url")
        return result

    async def cancel(self, task_id: str) -> bool:
        return False

    def __str__(self) -> str:
        return "InVideoAIGenerator(Freemium, Quality=84)"
