"""
Ideogram - AI Image Generation with Text Rendering
Best-in-class text rendering in images
Official: https://ideogram.ai/
"""

import os, logging
from typing import Optional
import requests
from ..base import *

logger = logging.getLogger(__name__)


class IdeogramGenerator(BaseGenerator):
    """Ideogram - Meilleur pour texte dans images (logos, posters)"""

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv("IDEOGRAM_API_KEY")
        if not self.api_key:
            raise ValueError("Ideogram API key required")
        self.api_base = "https://api.ideogram.ai/v1"
        self.session = requests.Session()
        self.session.headers.update({"Api-Key": self.api_key})

    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_image=True, max_resolution="1024x1024",
            api_cost_per_image=0.025, free_tier=True, free_credits_per_day=25,
            quality_score=89, avg_generation_time_seconds=15.0
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.validate_request(request)
        resp = self.session.post(f"{self.api_base}/generate", json={"prompt": request.prompt, "aspect_ratio": "1:1"}, timeout=30)
        if resp.status_code != 200:
            raise APIError(f"Ideogram error: {resp.text}")
        data = resp.json().get("data", [{}])[0]
        return GenerationResult(
            status=GenerationStatus.COMPLETED,
            task_id="sync",
            output_url=data.get("url"),
            estimated_cost_usd=0.025
        )

    async def check_status(self, task_id: str) -> GenerationResult:
        return GenerationResult(status=GenerationStatus.COMPLETED, task_id=task_id)

    async def cancel(self, task_id: str) -> bool:
        return False

    def __str__(self) -> str:
        return "IdeogramGenerator(Freemium $0.025/img, Quality=89, Text)"
