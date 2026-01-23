"""
Open-Sora - Open Source Sora-like Video Generation
Community-driven open-source video model
GitHub: https://github.com/hpcaitech/Open-Sora
"""

import os, logging
from typing import Optional
from ..base import *

logger = logging.getLogger(__name__)


class OpenSoraGenerator(BaseGenerator):
    """Open-Sora - Clone open source de Sora"""

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv("REPLICATE_API_TOKEN")
        self.model_version = "hpcaitech/open-sora:latest"

    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_video=True, max_duration_seconds=16.0,
            max_resolution="720p", api_cost_per_second=0.0, free_tier=True,
            quality_score=75, avg_generation_time_seconds=120.0
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.validate_request(request)
        import replicate
        pred = replicate.predictions.create(version=self.model_version, input={"prompt": request.prompt, "num_frames": 16})
        return GenerationResult(status=GenerationStatus.PROCESSING, task_id=pred.id, estimated_completion_time=120.0)

    async def check_status(self, task_id: str) -> GenerationResult:
        import replicate
        pred = replicate.predictions.get(task_id)
        status = GenerationStatus.COMPLETED if pred.status == "succeeded" else GenerationStatus.PROCESSING
        result = GenerationResult(status=status, task_id=task_id)
        if status == GenerationStatus.COMPLETED:
            result.output_url = pred.output
        return result

    async def cancel(self, task_id: str) -> bool:
        return False

    def __str__(self) -> str:
        return "OpenSoraGenerator(OpenSource, FREE, Quality=75)"
