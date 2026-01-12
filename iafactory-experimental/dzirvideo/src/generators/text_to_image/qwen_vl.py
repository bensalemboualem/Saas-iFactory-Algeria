"""
Qwen-VL - Text-to-Image Generator
Alibaba Cloud's free multimodal image generation
Official docs: https://help.aliyun.com/zh/dashscope/developer-reference/tongyi-wanxiang-text-to-image
"""

import os
import logging
from typing import Optional, Dict

try:
    import dashscope
    from dashscope.aigc.multimodal_generation import MultiModalGeneration
    DASHSCOPE_AVAILABLE = True
except ImportError:
    DASHSCOPE_AVAILABLE = False

from ..base import (
    BaseGenerator,
    GeneratorCapabilities,
    GeneratorCategory,
    GenerationRequest,
    GenerationResult,
    GenerationStatus,
    APIError,
    QuotaExceededError
)

logger = logging.getLogger(__name__)


class QwenVLGenerator(BaseGenerator):
    """
    Qwen-VL Text-to-Image Generator

    Features:
    - Free tier with generous quota
    - Multiple resolutions (512x512, 1024x1024, etc.)
    - Multiple aspect ratios
    - Style presets
    - Negative prompts

    API Documentation:
    https://help.aliyun.com/zh/dashscope/developer-reference/tongyi-wanxiang-text-to-image
    """

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Qwen-VL generator

        Args:
            api_key: Alibaba DashScope API key
            **kwargs: Additional configuration
        """
        if not DASHSCOPE_AVAILABLE:
            raise ImportError(
                "dashscope package required. Install with: pip install dashscope>=1.14.0"
            )

        super().__init__(api_key, **kwargs)

        self.api_key = api_key or os.getenv("ALIBABA_DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Alibaba DashScope API key required. "
                "Set ALIBABA_DASHSCOPE_API_KEY or pass api_key parameter."
            )

        dashscope.api_key = self.api_key
        self.model_name = "wanx-v1"  # Wanxiang model for images
        logger.info("Qwen-VL generator initialized")

    def _define_capabilities(self) -> GeneratorCapabilities:
        """Define Qwen-VL capabilities"""
        return GeneratorCapabilities(
            # Support
            supports_text_to_video=False,
            supports_image_to_video=False,
            supports_text_to_image=True,
            supports_image_to_image=False,
            supports_avatar_video=False,
            supports_reels_shortform=False,

            # Specs
            max_resolution="1024x1024",
            supported_aspect_ratios=["1:1", "16:9", "9:16", "4:3", "3:4"],
            max_fps=0,  # N/A for images

            # Pricing (FREE!)
            api_cost_per_second=0.0,
            api_cost_per_image=0.0,
            free_tier=True,
            free_credits_per_day=200,  # Generous free quota

            # Quality
            quality_score=80,
            realism_score=78,
            coherence_score=0,  # N/A for images
            prompt_adherence_score=82,

            # Performance
            avg_generation_time_seconds=10.0,
            supports_async=False,  # Synchronous API

            # Features
            supports_negative_prompts=True,
            supports_style_presets=True,
            supports_custom_dimensions=True,
            supports_batch_generation=True  # Can generate multiple
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        """
        Generate image from text prompt

        Args:
            request: Generation request with prompt, dimensions, etc.

        Returns:
            GenerationResult with image URL

        Raises:
            ValueError: If request invalid
            APIError: If API call fails
            QuotaExceededError: If quota exceeded
        """
        # Validate request
        self.validate_request(request)

        # Build API parameters
        params = self._build_api_params(request)

        try:
            # Call synchronous API
            response = MultiModalGeneration.call(
                model=self.model_name,
                **params
            )

            if response.status_code != 200:
                error_msg = f"Qwen-VL API error: {response.code} - {response.message}"

                # Check for quota exceeded
                if "quota" in str(response.message).lower() or "limit" in str(response.message).lower():
                    raise QuotaExceededError(error_msg)

                raise APIError(error_msg)

            # Extract image URL(s)
            output = response.output
            results = output.get("results", [])

            if not results:
                raise APIError("No images in response")

            # Get first image URL
            image_url = results[0].get("url")

            if not image_url:
                raise APIError("No image URL in response")

            logger.info(f"Qwen-VL generation completed: {image_url}")

            # Return completed result
            return GenerationResult(
                status=GenerationStatus.COMPLETED,
                task_id=request.task_id or "sync",
                output_url=image_url,
                width=request.width or 1024,
                height=request.height or 1024,
                estimated_cost_usd=0.0  # Free!
            )

        except QuotaExceededError:
            raise
        except Exception as e:
            logger.error(f"Error calling Qwen-VL API: {e}")
            raise APIError(f"Qwen-VL generation failed: {str(e)}")

    async def check_status(self, task_id: str) -> GenerationResult:
        """
        Check status (N/A for synchronous API)

        Since Qwen-VL uses synchronous API, this always returns completed.

        Args:
            task_id: Task identifier

        Returns:
            GenerationResult with completed status
        """
        return GenerationResult(
            status=GenerationStatus.COMPLETED,
            task_id=task_id,
            estimated_cost_usd=0.0
        )

    async def cancel(self, task_id: str) -> bool:
        """
        Cancel task (N/A for synchronous API)

        Args:
            task_id: Task identifier

        Returns:
            False (synchronous API can't be cancelled)
        """
        logger.warning("Qwen-VL uses synchronous API, cancellation not supported")
        return False

    def _build_api_params(self, request: GenerationRequest) -> Dict:
        """Build API parameters from request"""

        params = {
            "task": "text-to-image",
            "text": request.prompt
        }

        # Size (resolution)
        if request.width and request.height:
            params["size"] = f"{request.width}*{request.height}"
        elif request.aspect_ratio:
            # Map aspect ratio to size
            aspect_to_size = {
                "1:1": "1024*1024",
                "16:9": "1024*576",
                "9:16": "576*1024",
                "4:3": "1024*768",
                "3:4": "768*1024"
            }
            params["size"] = aspect_to_size.get(request.aspect_ratio, "1024*1024")
        else:
            params["size"] = "1024*1024"  # Default

        # Negative prompt
        if request.negative_prompt and self.capabilities.supports_negative_prompts:
            params["negative_prompt"] = request.negative_prompt

        # Style preset
        if request.style_preset and self.capabilities.supports_style_presets:
            # Qwen-VL style options: "<auto>", "<3d cartoon>", "<anime>",
            # "<oil painting>", "<watercolor>", "<sketch>", "<chinese painting>",
            # "<flat illustration>"
            params["style"] = request.style_preset

        # Number of images (batch generation)
        if self.capabilities.supports_batch_generation:
            params["n"] = 1  # Generate 1 by default

        return params

    def __str__(self) -> str:
        return "QwenVLGenerator(Alibaba, Free, Quality=80)"
