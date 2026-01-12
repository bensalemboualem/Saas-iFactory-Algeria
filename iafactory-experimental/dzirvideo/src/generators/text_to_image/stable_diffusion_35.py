"""
Stable Diffusion 3.5 - Latest Open Source Image Generation
Stability AI's latest open source model
Official: https://stability.ai/
"""

import os
import logging
from typing import Optional
import requests
from ..base import *

logger = logging.getLogger(__name__)


class StableDiffusion35Generator(BaseGenerator):
    """Stable Diffusion 3.5 - Latest SD model with improved quality"""

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv("STABILITY_API_KEY")
        if not self.api_key:
            raise ValueError("Stability AI API key required")
        self.api_base = "https://api.stability.ai/v2beta"
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_image=True,
            max_resolution="1536x1536",
            api_cost_per_image=0.04,
            free_tier=False,
            quality_score=90,
            avg_generation_time_seconds=10.0,
            supports_negative_prompts=True,
            supports_aspect_ratios=True
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.validate_request(request)

        try:
            # Prepare form data (Stability uses multipart/form-data)
            data = {
                "prompt": request.prompt,
                "output_format": "png",
                "model": "sd3.5-large"
            }

            if request.negative_prompt:
                data["negative_prompt"] = request.negative_prompt

            if request.aspect_ratio:
                data["aspect_ratio"] = request.aspect_ratio
            else:
                data["aspect_ratio"] = "1:1"

            response = self.session.post(
                f"{self.api_base}/stable-image/generate/sd3",
                files={"none": ''},  # Required for multipart
                data=data,
                timeout=30
            )

            if response.status_code == 402:
                raise QuotaExceededError("Stability AI credits exhausted")

            if response.status_code != 200:
                raise APIError(f"Stability AI error: {response.text}")

            # SD3 returns image directly (binary)
            # In production, you'd upload this to storage and return URL
            # For now, return a placeholder

            return GenerationResult(
                status=GenerationStatus.COMPLETED,
                task_id="sync",
                output_url="[Binary image data - needs storage upload]",
                estimated_cost_usd=0.04
            )

        except QuotaExceededError:
            raise
        except Exception as e:
            logger.error(f"Stable Diffusion 3.5 generation error: {e}")
            raise APIError(f"Stable Diffusion 3.5 error: {str(e)}")

    async def check_status(self, task_id: str) -> GenerationResult:
        # Synchronous API
        return GenerationResult(
            status=GenerationStatus.COMPLETED,
            task_id=task_id
        )

    async def cancel(self, task_id: str) -> bool:
        return False  # Synchronous, can't cancel

    def __str__(self) -> str:
        return "StableDiffusion35Generator(Premium $0.04/img, Quality=90, Latest)"
