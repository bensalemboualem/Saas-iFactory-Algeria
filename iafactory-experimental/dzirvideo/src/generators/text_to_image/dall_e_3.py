"""
DALL-E 3 - OpenAI's Image Generation Model
State-of-the-art text-to-image via OpenAI API
Official: https://openai.com/dall-e-3
"""

import os, logging
from typing import Optional
from openai import OpenAI
from ..base import *

logger = logging.getLogger(__name__)


class DALLE3Generator(BaseGenerator):
    """DALL-E 3 - Text-to-image premium OpenAI (Quality: 93/100)"""

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key required")
        self.client = OpenAI(api_key=self.api_key)

    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_image=True, max_resolution="1024x1024",
            api_cost_per_image=0.040, free_tier=False,
            quality_score=93, realism_score=95, avg_generation_time_seconds=10.0
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.validate_request(request)
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=request.prompt,
            size="1024x1024",
            quality="hd",
            n=1
        )
        return GenerationResult(
            status=GenerationStatus.COMPLETED,
            task_id="sync",
            output_url=response.data[0].url,
            estimated_cost_usd=0.040
        )

    async def check_status(self, task_id: str) -> GenerationResult:
        return GenerationResult(status=GenerationStatus.COMPLETED, task_id=task_id)

    async def cancel(self, task_id: str) -> bool:
        return False

    def __str__(self) -> str:
        return "DALLE3Generator(OpenAI, Premium $0.04/img, Quality=93)"
