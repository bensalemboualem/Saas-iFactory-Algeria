"""
FLUX.1 [schnell] - Text-to-Image Generator
Black Forest Labs' ultra-fast, free image generation
Via Together AI API (free tier available)
Official docs: https://docs.together.ai/docs/flux-1
"""

import os
import logging
from typing import Optional, Dict

try:
    from together import Together
    TOGETHER_AVAILABLE = True
except ImportError:
    TOGETHER_AVAILABLE = False

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


class FLUX1Generator(BaseGenerator):
    """
    FLUX.1 [schnell] Text-to-Image Generator via Together AI

    Features:
    - FREE via Together AI
    - Ultra-fast generation (2-5 seconds)
    - High quality (Quality Score: 90/100)
    - Multiple resolutions
    - No negative prompts (model limitation)

    Models available:
    - FLUX.1 [schnell] - Fast, free (this one)
    - FLUX.1 [dev] - Better quality, paid
    - FLUX.1 [pro] - Best quality, expensive
    """

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        """
        Initialize FLUX.1 generator

        Args:
            api_key: Together AI API key (or TOGETHER_API_KEY env var)
            **kwargs: Additional configuration
        """
        if not TOGETHER_AVAILABLE:
            raise ImportError(
                "together package required. Install with: pip install together>=1.0.0"
            )

        super().__init__(api_key, **kwargs)

        self.api_key = api_key or os.getenv("TOGETHER_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Together AI API key required for FLUX.1. "
                "Set TOGETHER_API_KEY or pass api_key parameter."
            )

        self.client = Together(api_key=self.api_key)
        self.model_name = "black-forest-labs/FLUX.1-schnell"  # Free model

        logger.info("FLUX.1 generator initialized")

    def _define_capabilities(self) -> GeneratorCapabilities:
        """Define FLUX.1 capabilities"""
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
            api_cost_per_image=0.0,  # Free on Together AI
            free_tier=True,
            free_credits_per_day=-1,  # Unlimited (with rate limits)

            # Quality (HIGH!)
            quality_score=90,
            realism_score=88,
            coherence_score=0,  # N/A
            prompt_adherence_score=92,

            # Performance
            avg_generation_time_seconds=5.0,  # Very fast!
            supports_async=False,  # Synchronous API

            # Features
            supports_negative_prompts=False,  # FLUX doesn't support negative prompts
            supports_style_presets=False,
            supports_custom_dimensions=True,
            supports_batch_generation=True
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        """
        Generate image from text prompt

        Args:
            request: Generation request

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
            # Call Together AI API (synchronous)
            response = self.client.images.generate(
                model=self.model_name,
                **params
            )

            # Extract image URL
            if not response.data or len(response.data) == 0:
                raise APIError("No images in response")

            image_url = response.data[0].url

            if not image_url:
                raise APIError("No image URL in response")

            logger.info(f"FLUX.1 generation completed: {image_url}")

            # Return completed result
            return GenerationResult(
                status=GenerationStatus.COMPLETED,
                task_id=request.task_id or "sync",
                output_url=image_url,
                width=request.width or 1024,
                height=request.height or 1024,
                estimated_cost_usd=0.0  # Free!
            )

        except Exception as e:
            error_msg = str(e)

            # Check for rate limit / quota errors
            if "rate limit" in error_msg.lower() or "quota" in error_msg.lower():
                raise QuotaExceededError(f"FLUX.1 rate limit exceeded: {error_msg}")

            logger.error(f"Error calling FLUX.1 API: {e}")
            raise APIError(f"FLUX.1 generation failed: {error_msg}")

    async def check_status(self, task_id: str) -> GenerationResult:
        """
        Check status (N/A for synchronous API)

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
        logger.warning("FLUX.1 uses synchronous API, cancellation not supported")
        return False

    def _build_api_params(self, request: GenerationRequest) -> Dict:
        """Build API parameters from request"""

        params = {
            "prompt": request.prompt,
            "steps": 4,  # FLUX.1 [schnell] optimized for 4 steps (ultra-fast)
        }

        # Size (width x height)
        if request.width and request.height:
            params["width"] = request.width
            params["height"] = request.height
        elif request.aspect_ratio:
            # Map aspect ratio to dimensions
            aspect_to_size = {
                "1:1": (1024, 1024),
                "16:9": (1024, 576),
                "9:16": (576, 1024),
                "4:3": (1024, 768),
                "3:4": (768, 1024)
            }
            width, height = aspect_to_size.get(request.aspect_ratio, (1024, 1024))
            params["width"] = width
            params["height"] = height
        else:
            params["width"] = 1024
            params["height"] = 1024

        # Number of images (batch generation)
        if self.capabilities.supports_batch_generation:
            params["n"] = 1  # Generate 1 by default

        # Seed (for reproducibility)
        if "seed" in request.__dict__:
            params["seed"] = request.seed

        return params

    def __str__(self) -> str:
        return "FLUX1Generator(BlackForestLabs, Free, Quality=90)"
