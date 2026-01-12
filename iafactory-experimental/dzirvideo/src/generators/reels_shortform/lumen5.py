"""
Lumen5 - Blog Post to Video Converter
Transform articles and blog posts into social media videos
Official: https://lumen5.com/
"""

import os
import logging
from typing import Optional
import requests
from ..base import *

logger = logging.getLogger(__name__)


class Lumen5Generator(BaseGenerator):
    """Lumen5 - Blog post → vidéo social media"""

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv("LUMEN5_API_KEY")
        if not self.api_key:
            raise ValueError("Lumen5 API key required")
        self.api_base = "https://api.lumen5.com/v1"
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_video=True, supports_reels_shortform=True,
            max_duration_seconds=180.0, max_resolution="1080p",
            api_cost_per_second=0.0, free_tier=True, free_credits_per_day=5,
            quality_score=82, avg_generation_time_seconds=120.0
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.validate_request(request)
        params = {"article_text": request.prompt, "format": "social_media"}
        resp = self.session.post(f"{self.api_base}/videos", json=params, timeout=30)
        if resp.status_code != 200:
            raise APIError(f"Lumen5 error: {resp.text}")
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
        return "Lumen5Generator(Free, Quality=82, Blog→Video)"
