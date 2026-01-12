"""
HunyuanVideo - Tencent's Open Source Video Generation Model
High-quality Chinese video generation model
GitHub: https://github.com/Tencent/HunyuanVideo
"""

import os
import logging
from typing import Optional
from ..base import *

logger = logging.getLogger(__name__)


class HunyuanVideoGenerator(BaseGenerator):
    """HunyuanVideo - Tencent open source (self-hosted ou Replicate)"""

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv("REPLICATE_API_TOKEN")
        self.model_version = "tencent/hunyuan-video:latest"

    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_video=True,
            max_duration_seconds=5.0,
            max_resolution="720p",
            api_cost_per_second=0.0,  # Open source
            free_tier=True,
            quality_score=82,
            avg_generation_time_seconds=120.0,
            supports_negative_prompts=True
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.validate_request(request)

        try:
            import replicate

            input_params = {
                "prompt": request.prompt,
                "num_frames": int(request.duration_seconds * 24),  # 24 fps
            }

            if request.negative_prompt:
                input_params["negative_prompt"] = request.negative_prompt

            prediction = replicate.predictions.create(
                version=self.model_version,
                input=input_params
            )

            return GenerationResult(
                status=GenerationStatus.PROCESSING,
                task_id=prediction.id,
                estimated_completion_time=120.0
            )

        except Exception as e:
            logger.error(f"HunyuanVideo generation error: {e}")
            raise APIError(f"HunyuanVideo error: {str(e)}")

    async def check_status(self, task_id: str) -> GenerationResult:
        try:
            import replicate

            prediction = replicate.predictions.get(task_id)

            if prediction.status == "succeeded":
                status = GenerationStatus.COMPLETED
                output_url = prediction.output[0] if isinstance(prediction.output, list) else prediction.output
            elif prediction.status == "failed":
                status = GenerationStatus.FAILED
                output_url = None
            else:
                status = GenerationStatus.PROCESSING
                output_url = None

            result = GenerationResult(
                status=status,
                task_id=task_id,
                output_url=output_url
            )

            if prediction.status == "failed":
                result.error_message = str(prediction.error)

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
        return "HunyuanVideoGenerator(OpenSource, FREE, Quality=82, Tencent)"
