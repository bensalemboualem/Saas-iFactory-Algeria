"""
Midjourney - Premium AI Art Generation
Best-in-class artistic image generation via unofficial API
Official: https://www.midjourney.com/
"""

import os, logging
from typing import Optional
import requests
from ..base import *

logger = logging.getLogger(__name__)


class MidjourneyGenerator(BaseGenerator):
    """Midjourney - Meilleure qualité artistique (Quality: 97/100)"""

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv("MIDJOURNEY_API_KEY")
        if not self.api_key:
            raise ValueError("Midjourney API key required (unofficial API)")
        self.api_base = "https://api.thenextleg.io/v2"  # Unofficial API wrapper
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_image=True, max_resolution="1024x1024",
            api_cost_per_image=0.05, free_tier=False,
            quality_score=97, realism_score=92, avg_generation_time_seconds=60.0
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.validate_request(request)
        resp = self.session.post(f"{self.api_base}/imagine", json={"msg": request.prompt}, timeout=30)
        if resp.status_code != 200:
            raise APIError(f"Midjourney error: {resp.text}")
        task_id = resp.json().get("messageId")
        return GenerationResult(status=GenerationStatus.PROCESSING, task_id=task_id, estimated_completion_time=60.0)

    async def check_status(self, task_id: str) -> GenerationResult:
        resp = self.session.get(f"{self.api_base}/message/{task_id}", timeout=10)
        data = resp.json()
        status = GenerationStatus.COMPLETED if data.get("progress") == 100 else GenerationStatus.PROCESSING
        result = GenerationResult(status=status, task_id=task_id)
        if status == GenerationStatus.COMPLETED:
            result.output_url = data.get("response", {}).get("imageUrl")
        return result

    async def cancel(self, task_id: str) -> bool:
        return False

    def __str__(self) -> str:
        return "MidjourneyGenerator(Premium, Quality=97, Artistic)"
