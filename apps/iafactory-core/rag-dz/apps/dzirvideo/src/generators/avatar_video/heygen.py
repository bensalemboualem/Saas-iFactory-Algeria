"""
HeyGen - AI Avatar Video Platform
Create professional avatar videos with AI
Official: https://www.heygen.com/
"""

import os
import logging
from typing import Optional
import requests
from ..base import *

logger = logging.getLogger(__name__)


class HeyGenGenerator(BaseGenerator):
    """HeyGen - Avatars IA professionnels (populaire entreprises)"""

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv("HEYGEN_API_KEY")
        if not self.api_key:
            raise ValueError("HeyGen API key required")
        self.api_base = "https://api.heygen.com/v1"
        self.session = requests.Session()
        self.session.headers.update({"X-Api-Key": self.api_key})

    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_video=True, supports_avatar_video=True,
            max_duration_seconds=300.0, max_resolution="1080p",
            api_cost_per_second=0.02, free_tier=True, free_credits_per_day=3,
            quality_score=92, realism_score=94, avg_generation_time_seconds=90.0
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.validate_request(request)
        params = {"script": request.prompt, "avatar_id": "josh_professional", "voice_id": "en-US-neural"}
        resp = self.session.post(f"{self.api_base}/video.generate", json=params, timeout=30)
        if resp.status_code != 200:
            raise APIError(f"HeyGen error: {resp.text}")
        task_id = resp.json().get("data", {}).get("video_id")
        return GenerationResult(status=GenerationStatus.PROCESSING, task_id=task_id, estimated_completion_time=90.0)

    async def check_status(self, task_id: str) -> GenerationResult:
        resp = self.session.get(f"{self.api_base}/video_status.get?video_id={task_id}", timeout=10)
        data = resp.json().get("data", {})
        status_map = {"pending": GenerationStatus.PENDING, "processing": GenerationStatus.PROCESSING, "completed": GenerationStatus.COMPLETED}
        status = status_map.get(data.get("status"), GenerationStatus.PROCESSING)
        result = GenerationResult(status=status, task_id=task_id)
        if status == GenerationStatus.COMPLETED:
            result.output_url = data.get("video_url")
        return result

    async def cancel(self, task_id: str) -> bool:
        return False  # HeyGen doesn't support cancellation

    def __str__(self) -> str:
        return "HeyGenGenerator(Premium, Quality=92, Avatars)"
