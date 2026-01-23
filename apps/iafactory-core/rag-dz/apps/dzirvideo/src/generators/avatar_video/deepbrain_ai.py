"""
DeepBrain AI - Photorealistic AI Avatar Videos
TV presenter-quality AI humans for professional videos
Official: https://www.deepbrain.io/
"""

import os
import logging
from typing import Optional
import requests
from ..base import *

logger = logging.getLogger(__name__)


class DeepBrainAIGenerator(BaseGenerator):
    """DeepBrain AI - Avatars présentateurs TV ultra-réalistes"""

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv("DEEPBRAIN_API_KEY")
        if not self.api_key:
            raise ValueError("DeepBrain API key required")
        self.api_base = "https://api.deepbrain.io/v1"
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_video=True, supports_avatar_video=True,
            max_duration_seconds=600.0, max_resolution="4K",
            api_cost_per_second=0.02, free_tier=False,
            quality_score=95, realism_score=98, avg_generation_time_seconds=120.0
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.validate_request(request)
        params = {"script": request.prompt, "avatar": "jessica_presenter", "language": "en"}
        resp = self.session.post(f"{self.api_base}/generate", json=params, timeout=30)
        if resp.status_code != 200:
            raise APIError(f"DeepBrain error: {resp.text}")
        task_id = resp.json().get("video_id")
        return GenerationResult(status=GenerationStatus.PROCESSING, task_id=task_id, estimated_completion_time=120.0)

    async def check_status(self, task_id: str) -> GenerationResult:
        resp = self.session.get(f"{self.api_base}/video/{task_id}", timeout=10)
        data = resp.json()
        status_map = {"processing": GenerationStatus.PROCESSING, "completed": GenerationStatus.COMPLETED}
        status = status_map.get(data.get("status"), GenerationStatus.PROCESSING)
        result = GenerationResult(status=status, task_id=task_id)
        if status == GenerationStatus.COMPLETED:
            result.output_url = data.get("url")
        return result

    async def cancel(self, task_id: str) -> bool:
        try:
            resp = self.session.delete(f"{self.api_base}/video/{task_id}")
            return resp.status_code == 200
        except:
            return False

    def __str__(self) -> str:
        return "DeepBrainAIGenerator(Premium, Quality=95, Realism=98)"
