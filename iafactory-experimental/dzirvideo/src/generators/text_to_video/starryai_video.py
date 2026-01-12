"""
StarryAI Video - Stylized AI Video Generation
Transform text/images into artistic AI videos
Official: https://www.starryai.com/
"""

import os
import logging
from typing import Optional
import requests
from ..base import *

logger = logging.getLogger(__name__)


class StarryAIVideoGenerator(BaseGenerator):
    """StarryAI - Text/Image → Vidéo stylisée artistique"""

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv("STARRYAI_API_KEY")
        if not self.api_key:
            raise ValueError("StarryAI API key required")
        self.api_base = "https://api.starryai.com/v1"
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_video=True, supports_image_to_video=True,
            max_duration_seconds=10.0, max_resolution="1080p",
            api_cost_per_second=0.02, free_tier=True, free_credits_per_day=5,
            quality_score=86, avg_generation_time_seconds=45.0
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.validate_request(request)
        params = {"prompt": request.prompt, "style": "artistic", "duration": 5}
        resp = self.session.post(f"{self.api_base}/video/create", json=params, timeout=30)
        if resp.status_code != 200:
            raise APIError(f"StarryAI error: {resp.text}")
        task_id = resp.json().get("id")
        return GenerationResult(status=GenerationStatus.PROCESSING, task_id=task_id, estimated_completion_time=45.0)

    async def check_status(self, task_id: str) -> GenerationResult:
        resp = self.session.get(f"{self.api_base}/video/{task_id}", timeout=10)
        data = resp.json()
        status = GenerationStatus.COMPLETED if data.get("status") == "completed" else GenerationStatus.PROCESSING
        result = GenerationResult(status=status, task_id=task_id)
        if status == GenerationStatus.COMPLETED:
            result.output_url = data.get("video_url")
        return result

    async def cancel(self, task_id: str) -> bool:
        return False

    def __str__(self) -> str:
        return "StarryAIVideoGenerator(Artistic, Quality=86)"
