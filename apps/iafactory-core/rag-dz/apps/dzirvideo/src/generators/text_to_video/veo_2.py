"""
Google Veo 2 - Google DeepMind's Video Model
State-of-the-art video generation via Replicate
Official: https://deepmind.google/technologies/veo/
"""

import os
import logging
from typing import Optional
import replicate
from ..base import *

logger = logging.getLogger(__name__)


class Veo2Generator(BaseGenerator):
    """Google Veo 2 - Latest video model from DeepMind (Quality: 93/100)"""

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv("REPLICATE_API_TOKEN")
        if not self.api_key:
            raise ValueError("Replicate API token required for Veo 2")
        os.environ["REPLICATE_API_TOKEN"] = self.api_key
        self.model_version = "google-deepmind/veo-2:latest"

    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_video=True, supports_image_to_video=True,
            max_duration_seconds=30.0, max_resolution="1080p",
            api_cost_per_second=0.50,  # Expensive!
            free_tier=False,
            quality_score=93, realism_score=94, coherence_score=92,
            avg_generation_time_seconds=120.0, supports_async=True
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.validate_request(request)
        prediction = replicate.predictions.create(
            version=self.model_version,
            input={"prompt": request.prompt, "duration": int(request.duration_seconds or 5)}
        )
        return GenerationResult(status=GenerationStatus.PROCESSING, task_id=prediction.id, estimated_completion_time=120.0)

    async def check_status(self, task_id: str) -> GenerationResult:
        prediction = replicate.predictions.get(task_id)
        status_map = {"succeeded": GenerationStatus.COMPLETED, "failed": GenerationStatus.FAILED}
        status = status_map.get(prediction.status, GenerationStatus.PROCESSING)
        result = GenerationResult(status=status, task_id=task_id)
        if status == GenerationStatus.COMPLETED:
            result.output_url = prediction.output if isinstance(prediction.output, str) else prediction.output[0]
        return result

    async def cancel(self, task_id: str) -> bool:
        try:
            replicate.predictions.cancel(task_id)
            return True
        except:
            return False

    def __str__(self) -> str:
        return "Veo2Generator(Google, Premium $0.50/s, Quality=93)"
