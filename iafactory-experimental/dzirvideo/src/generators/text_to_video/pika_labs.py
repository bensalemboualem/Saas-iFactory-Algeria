"""
Pika Labs - Text-to-Video Generator
Creative AI video generation with stylized effects
250 free credits available
Official: https://pika.art/
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


class PikaLabsGenerator(BaseGenerator):
    """
    Pika Labs Text-to-Video Generator

    Features:
    - 250 free credits
    - Creative/stylized video generation
    - Max 30 seconds per video
    - Multiple aspect ratios (16:9, 9:16, 1:1, 4:3)
    - High quality with artistic styles
    - Text-to-video & image-to-video modes

    Note: Uses Replicate API
    """

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Pika Labs generator

        Args:
            api_key: Replicate API token (or REPLICATE_API_TOKEN env var)
            **kwargs: Additional configuration
        """
        if not REPLICATE_AVAILABLE:
            raise ImportError(
                "replicate package required. Install with: pip install replicate>=0.15.0"
            )

        super().__init__(api_key, **kwargs)

        self.api_key = api_key or os.getenv("REPLICATE_API_TOKEN") or os.getenv("PIKA_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Replicate API token required for Pika Labs. "
                "Set REPLICATE_API_TOKEN or pass api_key parameter."
            )

        # Set Replicate API token
        os.environ["REPLICATE_API_TOKEN"] = self.api_key

        # Pika model on Replicate
        self.model_version = "pikaart/pika-labs:latest"

        logger.info("Pika Labs generator initialized")

    def _define_capabilities(self) -> GeneratorCapabilities:
        """Define Pika Labs capabilities"""
        return GeneratorCapabilities(
            # Support
            supports_text_to_video=True,
            supports_image_to_video=True,
            supports_text_to_image=False,
            supports_image_to_image=False,
            supports_avatar_video=False,
            supports_reels_shortform=True,

            # Specs
            max_duration_seconds=30.0,  # 30 seconds max
            min_duration_seconds=3.0,
            max_resolution="1080p",
            supported_aspect_ratios=["16:9", "9:16", "1:1", "4:3"],
            max_fps=24,

            # Pricing (FREEMIUM)
            api_cost_per_second=0.015,  # $0.015/sec after free credits
            api_cost_per_image=0.0,
            free_tier=True,
            free_credits_per_day=250,  # 250 credits (≈16 videos/day)

            # Quality (HIGH, stylized)
            quality_score=87,
            realism_score=82,
            coherence_score=90,
            prompt_adherence_score=88,

            # Performance
            avg_generation_time_seconds=45.0,  # ~45s
            supports_async=True,

            # Features
            supports_negative_prompts=True,
            supports_style_presets=True,  # Pika has creative styles
            supports_custom_dimensions=False,
            supports_batch_generation=False
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        """
        Generate video from text prompt

        Args:
            request: Generation request

        Returns:
            GenerationResult with task ID

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
            # Call Replicate async API
            prediction = replicate.predictions.create(
                version=self.model_version,
                input=params
            )

            task_id = prediction.id

            logger.info(f"Pika Labs generation started: task_id={task_id}")

            # Return pending result
            return GenerationResult(
                status=GenerationStatus.PROCESSING,
                task_id=task_id,
                estimated_completion_time=45.0,
                estimated_cost_usd=self.estimate_cost(request)
            )

        except replicate.exceptions.ReplicateError as e:
            error_msg = str(e)

            # Check for quota/rate limit errors
            if "quota" in error_msg.lower() or "rate limit" in error_msg.lower() or "credits" in error_msg.lower():
                raise QuotaExceededError(f"Pika Labs quota exceeded: {error_msg}")

            raise APIError(f"Pika Labs API error: {error_msg}")

        except Exception as e:
            logger.error(f"Error calling Pika Labs: {e}")
            raise APIError(f"Pika Labs generation failed: {str(e)}")

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
                estimated_cost_usd=0.0  # Updated after completion
            )

            # If completed, extract video URL
            if status == GenerationStatus.COMPLETED:
                output = prediction.output

                # Pika returns video URL directly or as list
                if isinstance(output, str):
                    result.output_url = output
                elif isinstance(output, list) and len(output) > 0:
                    result.output_url = output[0]
                elif isinstance(output, dict):
                    result.output_url = output.get("video") or output.get("url")

                if result.output_url:
                    logger.info(f"Pika Labs generation completed: {result.output_url}")
                else:
                    logger.warning("No video URL in Pika Labs response")

            # If failed, extract error
            elif status == GenerationStatus.FAILED:
                result.error_message = prediction.error or "Generation failed"

            return result

        except Exception as e:
            logger.error(f"Error checking Pika Labs status: {e}")
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
                logger.info(f"Pika Labs task {task_id} cancelled")
                return True

            return False

        except Exception as e:
            logger.error(f"Error cancelling Pika Labs task: {e}")
            return False

    async def wait_for_completion(
        self,
        task_id: str,
        max_wait_seconds: float = 180.0,
        poll_interval: float = 5.0
    ) -> GenerationResult:
        """
        Wait for generation to complete

        Args:
            task_id: Task identifier
            max_wait_seconds: Maximum time to wait (default 3 minutes)
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
            "prompt": request.prompt
        }

        # Duration (in seconds, max 30)
        if request.duration_seconds:
            duration = min(request.duration_seconds, 30.0)
            params["duration"] = int(duration)
        else:
            params["duration"] = 5  # Default 5 seconds

        # Aspect ratio
        if request.aspect_ratio:
            aspect_map = {
                "16:9": "16:9",
                "9:16": "9:16",
                "1:1": "1:1",
                "4:3": "4:3"
            }
            if request.aspect_ratio in aspect_map:
                params["aspect_ratio"] = aspect_map[request.aspect_ratio]

        # FPS (Pika supports 24fps)
        params["fps"] = 24

        # Negative prompt (if supported)
        if request.negative_prompt and self.capabilities.supports_negative_prompts:
            params["negative_prompt"] = request.negative_prompt

        # Style preset (Pika creative styles)
        if request.style_preset and self.capabilities.supports_style_presets:
            # Pika styles: "realistic", "anime", "3d", "cinematic", etc.
            params["style"] = request.style_preset

        # Motion intensity (Pika-specific)
        # Higher values = more movement
        params["motion"] = 3  # Medium motion (1-5 scale)

        # Image input (for image-to-video mode)
        if request.input_image_url:
            params["image"] = request.input_image_url
            params["mode"] = "image_to_video"
        else:
            params["mode"] = "text_to_video"

        # Camera motion (Pika-specific feature)
        # Options: "static", "zoom_in", "zoom_out", "pan_left", "pan_right", "orbit_left", "orbit_right"
        if hasattr(request, "camera_motion"):
            params["camera_motion"] = request.camera_motion

        return params

    def __str__(self) -> str:
        return "PikaLabsGenerator(Pika, Freemium, Quality=87)"
