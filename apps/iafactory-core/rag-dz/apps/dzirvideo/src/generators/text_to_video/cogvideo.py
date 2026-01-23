"""
CogVideo - Open Source Text-to-Video (Zhipu AI / Tsinghua)
Chinese open-source video generation model
GitHub: https://github.com/THUDM/CogVideo
"""

import os, logging
from typing import Optional
from ..base import *

logger = logging.getLogger(__name__)


class CogVideoGenerator(BaseGenerator):
    """CogVideo - Open source chinois (self-hosted ou Replicate)"""

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv("REPLICATE_API_TOKEN")
        self.model_version = "thudm/cogvideo:latest"

    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_video=True, max_duration_seconds=8.0,
            max_resolution="720p", api_cost_per_second=0.0, free_tier=True,
            quality_score=78, avg_generation_time_seconds=90.0
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.validate_request(request)
        import replicate
        pred = replicate.predictions.create(version=self.model_version, input={"prompt": request.prompt})
        return GenerationResult(status=GenerationStatus.PROCESSING, task_id=pred.id, estimated_completion_time=90.0)

    async def check_status(self, task_id: str) -> GenerationResult:
        import replicate
        pred = replicate.predictions.get(task_id)
        status = GenerationStatus.COMPLETED if pred.status == "succeeded" else GenerationStatus.PROCESSING
        result = GenerationResult(status=status, task_id=task_id)
        if status == GenerationStatus.COMPLETED:
            result.output_url = pred.output[0] if isinstance(pred.output, list) else pred.output
        return result

    async def cancel(self, task_id: str) -> bool:
        return False

    def __str__(self) -> str:
        return "CogVideoGenerator(OpenSource, FREE, Quality=78)"
