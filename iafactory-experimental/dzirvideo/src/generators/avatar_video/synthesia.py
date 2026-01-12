"""
Synthesia - AI Video Platform with Avatars
Professional AI avatar videos for corporate/training
Official: https://www.synthesia.io/
"""

import os
import logging
from typing import Optional
import requests
from ..base import *

logger = logging.getLogger(__name__)


class SynthesiaGenerator(BaseGenerator):
    """Synthesia - Avatars professionnels pour entreprise/formation"""

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv("SYNTHESIA_API_KEY")
        if not self.api_key:
            raise ValueError("Synthesia API key required")
        self.api_base = "https://api.synthesia.io/v2"
        self.session = requests.Session()
        self.session.headers.update({"Authorization": self.api_key})

    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_video=True, supports_avatar_video=True,
            max_duration_seconds=600.0, max_resolution="1080p",
            api_cost_per_second=0.03, free_tier=False,
            quality_score=93, realism_score=95, avg_generation_time_seconds=180.0
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.validate_request(request)
        params = {"test": False, "input": [{"avatarSettings": {"voice": "en-US-Neural2-F"}, "scriptText": request.prompt}]}
        resp = self.session.post(f"{self.api_base}/videos", json=params, timeout=30)
        if resp.status_code != 201:
            raise APIError(f"Synthesia error: {resp.text}")
        task_id = resp.json().get("id")
        return GenerationResult(status=GenerationStatus.PROCESSING, task_id=task_id, estimated_completion_time=180.0)

    async def check_status(self, task_id: str) -> GenerationResult:
        resp = self.session.get(f"{self.api_base}/videos/{task_id}", timeout=10)
        data = resp.json()
        status_map = {"in_progress": GenerationStatus.PROCESSING, "complete": GenerationStatus.COMPLETED, "failed": GenerationStatus.FAILED}
        status = status_map.get(data.get("status"), GenerationStatus.PROCESSING)
        result = GenerationResult(status=status, task_id=task_id)
        if status == GenerationStatus.COMPLETED:
            result.output_url = data.get("download")
        return result

    async def cancel(self, task_id: str) -> bool:
        try:
            resp = self.session.delete(f"{self.api_base}/videos/{task_id}")
            return resp.status_code == 200
        except:
            return False

    def __str__(self) -> str:
        return "SynthesiaGenerator(Enterprise, Quality=93, Avatars)"
