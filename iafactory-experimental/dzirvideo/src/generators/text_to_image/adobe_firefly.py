"""
Adobe Firefly - Professional AI Image Generation
Adobe's enterprise-grade AI image generator
Official: https://www.adobe.com/products/firefly.html
"""

import os
import logging
from typing import Optional
import requests
from ..base import *

logger = logging.getLogger(__name__)


class AdobeFireflyGenerator(BaseGenerator):
    """Adobe Firefly - Professional image generation"""

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv("ADOBE_API_KEY")
        if not self.api_key:
            raise ValueError("Adobe Firefly API key required")
        self.api_base = "https://firefly-api.adobe.io/v2"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "x-api-key": os.getenv("ADOBE_CLIENT_ID", "")
        })

    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_image=True,
            max_resolution="2048x2048",
            api_cost_per_image=0.03,
            free_tier=False,
            quality_score=91,
            avg_generation_time_seconds=12.0,
            supports_negative_prompts=True,
            supports_style_presets=True
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.validate_request(request)

        try:
            params = {
                "prompt": request.prompt,
                "contentClass": "photo",
                "size": {"width": 1024, "height": 1024}
            }

            if request.negative_prompt:
                params["negativePrompt"] = request.negative_prompt

            if request.style:
                params["style"] = {"id": request.style}

            response = self.session.post(
                f"{self.api_base}/images/generate",
                json=params,
                timeout=30
            )

            if response.status_code != 200:
                raise APIError(f"Adobe Firefly error: {response.text}")

            data = response.json()

            # Firefly returns results synchronously
            image_url = data.get("outputs", [{}])[0].get("image", {}).get("url")

            return GenerationResult(
                status=GenerationStatus.COMPLETED,
                task_id="sync",
                output_url=image_url,
                estimated_cost_usd=0.03
            )

        except Exception as e:
            logger.error(f"Adobe Firefly generation error: {e}")
            raise APIError(f"Adobe Firefly error: {str(e)}")

    async def check_status(self, task_id: str) -> GenerationResult:
        # Synchronous API
        return GenerationResult(
            status=GenerationStatus.COMPLETED,
            task_id=task_id
        )

    async def cancel(self, task_id: str) -> bool:
        return False  # Synchronous, can't cancel

    def __str__(self) -> str:
        return "AdobeFireflyGenerator(Premium $0.03/img, Quality=91, Professional)"
