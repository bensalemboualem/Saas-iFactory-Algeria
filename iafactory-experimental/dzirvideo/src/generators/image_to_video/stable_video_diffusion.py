"""
Stable Video Diffusion (SVD) - Image-to-Video Generator
Open-source video generation from Stability AI
FREE via Replicate or self-hosted
Official: https://stability.ai/stable-video
"""

import os
import time
import logging
from typing import Optional, Dict
import asyncio

try:
    import replicate
    REPLICATE_AVAILABLE = True
except ImportError:
    REPLICATE_AVAILABLE = False

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


class StableVideoDiffusionGenerator(BaseGenerator):
    """
    Stable Video Diffusion (SVD) Image-to-Video Generator

    Features:
    - FREE open-source model
    - Image-to-video animation
    - Max 25 frames (~1-3 seconds at 24fps)
    - 1024x576 resolution
    - Smooth motion from still images
    - Good for product demos, logo animations

    Models:
    - SVD: Standard model (14 frames)
    - SVD-XT: Extended model (25 frames) - this one

    Pricing:
    - FREE via Replicate (with rate limits)
    - FREE self-hosted (requires GPU)

    API: Via Replicate
    """

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Stable Video Diffusion generator

        Args:
            api_key: Replicate API token (or REPLICATE_API_TOKEN env var)
            **kwargs: Additional configuration
        """
        if not REPLICATE_AVAILABLE:
            raise ImportError(
                "replicate package required. Install with: pip install replicate>=0.15.0"
            )

        super().__init__(api_key, **kwargs)

        self.api_key = api_key or os.getenv("REPLICATE_API_TOKEN") or os.getenv("STABILITY_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Replicate API token required for Stable Video Diffusion. "
                "Set REPLICATE_API_TOKEN or pass api_key parameter."
            )

        # Set Replicate API token
        os.environ["REPLICATE_API_TOKEN"] = self.api_key

        # SVD-XT model on Replicate (extended version with 25 frames)
        self.model_version = "stability-ai/stable-video-diffusion:latest"

        logger.info("Stable Video Diffusion generator initialized")

    def _define_capabilities(self) -> GeneratorCapabilities:
        """Define SVD capabilities"""
        return GeneratorCapabilities(
            # Support
            supports_text_to_video=False,  # Image-to-video ONLY
            supports_image_to_video=True,  # PRIMARY FUNCTION
            supports_text_to_image=False,
            supports_image_to_image=False,
            supports_avatar_video=False,
            supports_reels_shortform=False,  # Too short for Reels

            # Specs
            max_duration_seconds=3.0,  # ~25 frames at 8fps = 3 seconds
            min_duration_seconds=0.5,
            max_resolution="1024x576",
            supported_aspect_ratios=["16:9"],  # Fixed aspect ratio
            max_fps=24,

            # Pricing (FREE!)
            api_cost_per_second=0.0,  # Free via Replicate
            api_cost_per_image=0.0,
            free_tier=True,
            free_credits_per_day=-1,  # Unlimited (with rate limits)

            # Quality (GOOD for open-source)
            quality_score=85,
            realism_score=83,
            coherence_score=88,  # Good temporal coherence
            prompt_adherence_score=0,  # No text prompts (image input only)

            # Performance
            avg_generation_time_seconds=30.0,  # ~30 seconds
            supports_async=True,

            # Features
            supports_negative_prompts=False,  # Image input only
            supports_style_presets=False,
            supports_custom_dimensions=False,  # Fixed resolution
            supports_batch_generation=False
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        """
        Generate video from input image

        Args:
            request: Generation request (MUST have input_image_url)

        Returns:
            GenerationResult with task ID

        Raises:
            ValueError: If no input image provided
            APIError: If API call fails
            QuotaExceededError: If quota exceeded
        """
        # Validate request
        self.validate_request(request)

        # SVD requires input image
        if not request.input_image_url:
            raise ValueError("Stable Video Diffusion requires input_image_url (image-to-video only)")

        # Build API parameters
        params = self._build_api_params(request)

        try:
            # Call Replicate async API
            prediction = replicate.predictions.create(
                version=self.model_version,
                input=params
            )

            task_id = prediction.id

            logger.info(f"Stable Video Diffusion generation started: task_id={task_id}")

            # Return pending result
            return GenerationResult(
                status=GenerationStatus.PROCESSING,
                task_id=task_id,
                estimated_completion_time=30.0,
                estimated_cost_usd=0.0  # FREE!
            )

        except replicate.exceptions.ReplicateError as e:
            error_msg = str(e)

            # Check for quota/rate limit errors
            if "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
                raise QuotaExceededError(f"Stable Video Diffusion rate limit exceeded: {error_msg}")

            raise APIError(f"Stable Video Diffusion API error: {error_msg}")

        except Exception as e:
            logger.error(f"Error calling Stable Video Diffusion: {e}")
            raise APIError(f"Stable Video Diffusion generation failed: {str(e)}")

    async def check_status(self, task_id: str) -> GenerationResult:
        """
        Check status of generation task

        Args:
            task_id: Task identifier from generate()

        Returns:
            GenerationResult with current status
        """
        try:
            prediction = replicate.predictions.get(task_id)

            # Map Replicate status to our enum
            status_map = {
                "starting": GenerationStatus.PENDING,
                "processing": GenerationStatus.PROCESSING,
                "succeeded": GenerationStatus.COMPLETED,
                "failed": GenerationStatus.FAILED,
                "canceled": GenerationStatus.FAILED
            }
            status = status_map.get(prediction.status, GenerationStatus.PROCESSING)

            result = GenerationResult(
                status=status,
                task_id=task_id,
                estimated_cost_usd=0.0  # Always free
            )

            # If completed, extract video URL
            if status == GenerationStatus.COMPLETED:
                output = prediction.output

                # SVD returns video URL directly or as list
                if isinstance(output, str):
                    result.output_url = output
                elif isinstance(output, list) and len(output) > 0:
                    result.output_url = output[0]
                elif isinstance(output, dict):
                    result.output_url = output.get("video") or output.get("url")

                if result.output_url:
                    result.duration_seconds = 3.0  # ~25 frames
                    result.width = 1024
                    result.height = 576
                    logger.info(f"Stable Video Diffusion generation completed: {result.output_url}")
                else:
                    logger.warning("No video URL in SVD response")

            # If failed, extract error
            elif status == GenerationStatus.FAILED:
                result.error_message = prediction.error or "Generation failed"

            return result

        except Exception as e:
            logger.error(f"Error checking Stable Video Diffusion status: {e}")
            raise APIError(f"Status check failed: {str(e)}")

    async def cancel(self, task_id: str) -> bool:
        """
        Cancel a running generation task

        Args:
            task_id: Task identifier

        Returns:
            True if cancelled successfully
        """
        try:
            prediction = replicate.predictions.get(task_id)

            if prediction.status in ["starting", "processing"]:
                replicate.predictions.cancel(task_id)
                logger.info(f"Stable Video Diffusion task {task_id} cancelled")
                return True

            return False

        except Exception as e:
            logger.error(f"Error cancelling SVD task: {e}")
            return False

    async def wait_for_completion(
        self,
        task_id: str,
        max_wait_seconds: float = 120.0,
        poll_interval: float = 5.0
    ) -> GenerationResult:
        """
        Wait for generation to complete

        Args:
            task_id: Task identifier
            max_wait_seconds: Maximum time to wait (default 2 minutes)
            poll_interval: Seconds between status checks

        Returns:
            GenerationResult when completed

        Raises:
            TimeoutError: If max_wait_seconds exceeded
            APIError: If generation failed
        """
        start_time = time.time()

        while True:
            result = await self.check_status(task_id)

            if result.status == GenerationStatus.COMPLETED:
                return result

            if result.status == GenerationStatus.FAILED:
                raise APIError(f"Generation failed: {result.error_message}")

            # Check timeout
            elapsed = time.time() - start_time
            if elapsed > max_wait_seconds:
                # Try to cancel
                await self.cancel(task_id)
                raise TimeoutError(f"Generation timed out after {elapsed:.1f}s")

            # Wait before next poll
            await asyncio.sleep(poll_interval)

    def _build_api_params(self, request: GenerationRequest) -> Dict:
        """Build API parameters from request"""

        params = {
            "image": request.input_image_url  # Required: input image
        }

        # Number of frames (14 or 25)
        # SVD-XT supports up to 25 frames
        params["frames"] = 25  # Maximum for SVD-XT

        # FPS (frames per second)
        # Higher FPS = shorter duration
        # 25 frames at 8fps = ~3 seconds
        params["fps"] = 8  # Default 8fps (smooth motion)

        # Motion bucket ID (controls amount of motion)
        # Range: 1-255 (higher = more motion)
        # Default: 127 (medium motion)
        motion_level = 127  # Medium motion

        # Allow user to override motion level
        if hasattr(request, "motion_intensity"):
            # Map 0-100 to 1-255
            motion_level = int(1 + (request.motion_intensity / 100) * 254)

        params["motion_bucket_id"] = motion_level

        # Conditioning augmentation
        # Controls how much the video can deviate from the input image
        # Range: 0.0-1.0 (higher = more variation)
        params["cond_aug"] = 0.02  # Low deviation (stay close to input image)

        # Decoding chunk size (for memory efficiency)
        params["decoding_t"] = 14  # Process 14 frames at a time

        # Seed (for reproducibility)
        if hasattr(request, "seed"):
            params["seed"] = request.seed

        return params

    def validate_request(self, request: GenerationRequest) -> bool:
        """
        Validate generation request

        Args:
            request: Request to validate

        Returns:
            True if valid

        Raises:
            ValueError: If request is invalid
        """
        # Call parent validation
        super().validate_request(request)

        # SVD-specific: MUST have input image
        if not request.input_image_url:
            raise ValueError(
                "Stable Video Diffusion requires input_image_url. "
                "This is an image-to-video generator only."
            )

        return True

    def __str__(self) -> str:
        return "StableVideoDiffusionGenerator(StabilityAI, FREE, Quality=85, Image→Video)"
