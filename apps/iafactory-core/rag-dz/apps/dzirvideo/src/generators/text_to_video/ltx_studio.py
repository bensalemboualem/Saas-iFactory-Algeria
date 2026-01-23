"""
LTX Studio - AI Film Generation Platform
Generate film-quality narratives with AI
Official: https://ltx.studio/
"""

import os
import logging
from typing import Optional
import requests
from ..base import *

logger = logging.getLogger(__name__)


class LTXStudioGenerator(BaseGenerator):
    """LTX Studio - Génération vidéo film-like de haute qualité"""

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv("LTX_API_KEY")
        if not self.api_key:
            raise ValueError("LTX Studio API key required")
        self.api_base = "https://api.ltx.studio/v1"
        self.session = requests.Session()
        self.session.headers.update({"X-API-Key": self.api_key})

    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_video=True,
            max_duration_seconds=120.0, max_resolution="4K",
            api_cost_per_second=0.03, free_tier=False,
            quality_score=93, realism_score=91,
            avg_generation_time_seconds=180.0
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.validate_request(request)
        params = {"prompt": request.prompt, "style": "cinematic", "resolution": "1080p"}
        resp = self.session.post(f"{self.api_base}/generate", json=params, timeout=30)
        if resp.status_code != 200:
            raise APIError(f"LTX error: {resp.text}")
        task_id = resp.json().get("generation_id")
        return GenerationResult(status=GenerationStatus.PROCESSING, task_id=task_id, estimated_completion_time=180.0)

    async def check_status(self, task_id: str) -> GenerationResult:
        resp = self.session.get(f"{self.api_base}/status/{task_id}", timeout=10)
        data = resp.json()
        status_map = {"pending": GenerationStatus.PENDING, "generating": GenerationStatus.PROCESSING, "complete": GenerationStatus.COMPLETED}
        status = status_map.get(data.get("status"), GenerationStatus.PROCESSING)
        result = GenerationResult(status=status, task_id=task_id)
        if status == GenerationStatus.COMPLETED:
            result.output_url = data.get("video_url")
        return result

    async def cancel(self, task_id: str) -> bool:
        try:
            resp = self.session.post(f"{self.api_base}/cancel/{task_id}")
            return resp.status_code == 200
        except:
            return False

    def __str__(self) -> str:
        return "LTXStudioGenerator(Premium, Quality=93, Cinematic)"
