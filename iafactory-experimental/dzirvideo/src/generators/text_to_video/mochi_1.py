"""
Mochi 1 - Open Source High-Quality Video Generation
Community-driven video generation model
GitHub: https://github.com/genmoai/mochi
"""

import os
import logging
from typing import Optional
from ..base import *

logger = logging.getLogger(__name__)


class Mochi1Generator(BaseGenerator):
    """Mochi 1 - Open source video generation (Genmo AI)"""

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv("REPLICATE_API_TOKEN")
        self.model_version = "genmo/mochi-1-preview:latest"

    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_video=True,
            max_duration_seconds=6.0,
            max_resolution="720p",
            api_cost_per_second=0.0,  # Open source
            free_tier=True,
            quality_score=81,
            avg_generation_time_seconds=180.0,
            supports_aspect_ratios=True
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.validate_request(request)

        try:
            import replicate

            input_params = {
                "prompt": request.prompt,
                "num_frames": min(int(request.duration_seconds * 30), 163),  # Max 163 frames
            }

            if request.aspect_ratio:
                input_params["aspect_ratio"] = request.aspect_ratio

            prediction = replicate.predictions.create(
                version=self.model_version,
                input=input_params
            )

            return GenerationResult(
                status=GenerationStatus.PROCESSING,
                task_id=prediction.id,
                estimated_completion_time=180.0
            )

        except Exception as e:
            logger.error(f"Mochi 1 generation error: {e}")
            raise APIError(f"Mochi 1 error: {str(e)}")

    async def check_status(self, task_id: str) -> GenerationResult:
        try:
            import replicate

            prediction = replicate.predictions.get(task_id)

            status_map = {
                "succeeded": GenerationStatus.COMPLETED,
                "failed": GenerationStatus.FAILED,
                "canceled": GenerationStatus.FAILED
            }
            status = status_map.get(prediction.status, GenerationStatus.PROCESSING)

            result = GenerationResult(
                status=status,
                task_id=task_id
            )

            if status == GenerationStatus.COMPLETED:
                result.output_url = prediction.output
            elif status == GenerationStatus.FAILED:
                result.error_message = str(prediction.error) if prediction.error else "Generation failed"

            return result

        except Exception as e:
            logger.error(f"Status check error: {e}")
            raise APIError(f"Status check failed: {str(e)}")

    async def cancel(self, task_id: str) -> bool:
        try:
            import replicate
            replicate.predictions.cancel(task_id)
            return True
        except:
            return False

    def __str__(self) -> str:
        return "Mochi1Generator(OpenSource, FREE, Quality=81, Genmo)"
