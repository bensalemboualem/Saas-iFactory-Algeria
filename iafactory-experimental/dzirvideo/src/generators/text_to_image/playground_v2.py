"""
Playground v2 - Advanced AI Image Generation
High-quality image generation with fine control
Official: https://playgroundai.com/
"""

import os
import logging
from typing import Optional
import requests
from ..base import *

logger = logging.getLogger(__name__)


class PlaygroundV2Generator(BaseGenerator):
    """Playground v2 - Advanced image generation with control"""

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv("PLAYGROUND_API_KEY")
        if not self.api_key:
            raise ValueError("Playground API key required")
        self.api_base = "https://api.playgroundai.com/v1"
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_image=True,
            max_resolution="1024x1024",
            api_cost_per_image=0.02,
            free_tier=True,
            free_credits_per_day=50,
            quality_score=88,
            avg_generation_time_seconds=8.0,
            supports_negative_prompts=True,
            supports_style_presets=True
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.validate_request(request)

        try:
            params = {
                "prompt": request.prompt,
                "width": 1024,
                "height": 1024,
                "guidance_scale": 7.5,
                "num_inference_steps": 50
            }

            if request.negative_prompt:
                params["negative_prompt"] = request.negative_prompt

            if request.style:
                params["filter"] = request.style

            response = self.session.post(
                f"{self.api_base}/images",
                json=params,
                timeout=30
            )

            if response.status_code == 429:
                raise QuotaExceededError("Playground daily quota exceeded")

            if response.status_code != 200:
                raise APIError(f"Playground error: {response.text}")

            data = response.json()

            # Check if async or sync
            if "images" in data:
                # Sync response
                image_url = data["images"][0] if data["images"] else None
                return GenerationResult(
                    status=GenerationStatus.COMPLETED,
                    task_id="sync",
                    output_url=image_url,
                    estimated_cost_usd=0.02
                )
            else:
                # Async response
                return GenerationResult(
                    status=GenerationStatus.PROCESSING,
                    task_id=data.get("id"),
                    estimated_completion_time=8.0,
                    estimated_cost_usd=0.02
                )

        except QuotaExceededError:
            raise
        except Exception as e:
            logger.error(f"Playground generation error: {e}")
            raise APIError(f"Playground error: {str(e)}")

    async def check_status(self, task_id: str) -> GenerationResult:
        if task_id == "sync":
            return GenerationResult(status=GenerationStatus.COMPLETED, task_id=task_id)

        try:
            response = self.session.get(
                f"{self.api_base}/images/{task_id}",
                timeout=10
            )

            if response.status_code != 200:
                raise APIError(f"Status check error: {response.text}")

            data = response.json()
            status_str = data.get("status", "processing")

            if status_str == "completed":
                status = GenerationStatus.COMPLETED
            elif status_str == "failed":
                status = GenerationStatus.FAILED
            else:
                status = GenerationStatus.PROCESSING

            result = GenerationResult(status=status, task_id=task_id)

            if status == GenerationStatus.COMPLETED:
                result.output_url = data.get("images", [None])[0]
            elif status == GenerationStatus.FAILED:
                result.error_message = data.get("error", "Generation failed")

            return result

        except Exception as e:
            logger.error(f"Status check error: {e}")
            raise APIError(f"Status check failed: {str(e)}")

    async def cancel(self, task_id: str) -> bool:
        return False

    def __str__(self) -> str:
        return "PlaygroundV2Generator(Freemium $0.02/img, Quality=88)"
