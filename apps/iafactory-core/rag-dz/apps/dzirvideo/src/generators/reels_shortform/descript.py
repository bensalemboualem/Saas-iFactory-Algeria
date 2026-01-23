"""
Descript - AI Video Editing + Overdub
Professional video editing with AI voice cloning and text-based editing
Official: https://www.descript.com/
"""

import os
import logging
from typing import Optional
import requests
from ..base import *

logger = logging.getLogger(__name__)


class DescriptGenerator(BaseGenerator):
    """Descript - Montage vidéo IA + clonage de voix (overdub)"""

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv("DESCRIPT_API_KEY")
        if not self.api_key:
            raise ValueError("Descript API key required")
        self.api_base = "https://api.descript.com/v1"
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Api-Key {self.api_key}"})

    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_video=True, supports_reels_shortform=True,
            max_duration_seconds=600.0, max_resolution="4K",
            api_cost_per_second=0.01, free_tier=True, free_credits_per_day=3,
            quality_score=91, avg_generation_time_seconds=150.0
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.validate_request(request)
        params = {"script": request.prompt, "voice": "overdub", "auto_edit": True}
        resp = self.session.post(f"{self.api_base}/compositions", json=params, timeout=30)
        if resp.status_code != 200:
            raise APIError(f"Descript error: {resp.text}")
        task_id = resp.json().get("id")
        return GenerationResult(status=GenerationStatus.PROCESSING, task_id=task_id, estimated_completion_time=150.0)

    async def check_status(self, task_id: str) -> GenerationResult:
        resp = self.session.get(f"{self.api_base}/compositions/{task_id}", timeout=10)
        data = resp.json()
        status = GenerationStatus.COMPLETED if data.get("status") == "ready" else GenerationStatus.PROCESSING
        result = GenerationResult(status=status, task_id=task_id)
        if status == GenerationStatus.COMPLETED:
            result.output_url = data.get("media_url")
        return result

    async def cancel(self, task_id: str) -> bool:
        try:
            resp = self.session.delete(f"{self.api_base}/compositions/{task_id}")
            return resp.status_code == 200
        except:
            return False

    def __str__(self) -> str:
        return "DescriptGenerator(Professional, Quality=91)"
