"""
Elai.io - AI Video Platform with Avatars
Text to video with AI presenters and voiceovers
Official: https://elai.io/
"""

import os
import logging
from typing import Optional
import requests
from ..base import *

logger = logging.getLogger(__name__)


class ElaiIOGenerator(BaseGenerator):
    """Elai.io - Text→Vidéo avec avatars IA et voix-off"""

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv("ELAI_API_KEY")
        if not self.api_key:
            raise ValueError("Elai.io API key required")
        self.api_base = "https://apis.elai.io/api/v1"
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Token {self.api_key}"})

    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_video=True, supports_avatar_video=True,
            max_duration_seconds=300.0, max_resolution="1080p",
            api_cost_per_second=0.015, free_tier=True, free_credits_per_day=5,
            quality_score=88, avg_generation_time_seconds=90.0
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.validate_request(request)
        params = {"text": request.prompt, "template_id": "default", "voice": "en-US-Jenny"}
        resp = self.session.post(f"{self.api_base}/videos", json=params, timeout=30)
        if resp.status_code != 200:
            raise APIError(f"Elai.io error: {resp.text}")
        task_id = resp.json().get("_id")
        return GenerationResult(status=GenerationStatus.PROCESSING, task_id=task_id, estimated_completion_time=90.0)

    async def check_status(self, task_id: str) -> GenerationResult:
        resp = self.session.get(f"{self.api_base}/videos/{task_id}", timeout=10)
        data = resp.json()
        status_map = {"in_progress": GenerationStatus.PROCESSING, "done": GenerationStatus.COMPLETED}
        status = status_map.get(data.get("status"), GenerationStatus.PROCESSING)
        result = GenerationResult(status=status, task_id=task_id)
        if status == GenerationStatus.COMPLETED:
            result.output_url = data.get("url")
        return result

    async def cancel(self, task_id: str) -> bool:
        return False  # Elai.io doesn't support cancellation

    def __str__(self) -> str:
        return "ElaiIOGenerator(Freemium, Quality=88)"
