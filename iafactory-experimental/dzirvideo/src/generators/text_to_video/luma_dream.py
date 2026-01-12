"""
Luma Dream Machine - Text-to-Video Generator
High-quality AI video generation with cinematic results
Freemium: Free tier + $9.99/mo unlimited
Official: https://lumalabs.ai/dream-machine
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


class LumaDreamGenerator(BaseGenerator):
    """
    Luma Dream Machine Text-to-Video Generator

    Features:
    - High quality (Quality Score: 90/100)
    - Freemium model ($9.99/mo unlimited OR pay-per-use)
    - Max 5 seconds per video (free tier), 120s (paid)
    - 1080p resolution
    - Cinematic/realistic results
    - Fast generation (~40 seconds)
    - Text-to-video & image-to-video modes

    Pricing:
    - Free tier: 30 generations/month
    - Pay-as-you-go: $0.02/second
    - Unlimited: $9.99/month

    API: Via Replicate
    """

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Luma Dream Machine generator

        Args:
            api_key: Replicate API token (or REPLICATE_API_TOKEN env var)
            **kwargs: Additional configuration
        """
        if not REPLICATE_AVAILABLE:
            raise ImportError(
                "replicate package required. Install with: pip install replicate>=0.15.0"
            )

        super().__init__(api_key, **kwargs)

        self.api_key = api_key or os.getenv("REPLICATE_API_TOKEN") or os.getenv("LUMA_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Replicate API token required for Luma Dream Machine. "
                "Set REPLICATE_API_TOKEN or pass api_key parameter."
            )

        # Set Replicate API token
        os.environ["REPLICATE_API_TOKEN"] = self.api_key

        # Luma Dream Machine model on Replicate
        self.model_version = "lucataco/luma-dream-machine:latest"

        logger.info("Luma Dream Machine generator initialized")

    def _define_capabilities(self) -> GeneratorCapabilities:
        """Define Luma Dream Machine capabilities"""
        return GeneratorCapabilities(
            # Support
            supports_text_to_video=True,
            supports_image_to_video=True,  # Extend image mode
            supports_text_to_image=False,
            supports_image_to_image=False,
            supports_avatar_video=False,
            supports_reels_shortform=True,

            # Specs
            max_duration_seconds=5.0,   # 5s free tier, 120s paid
            min_duration_seconds=1.0,
            max_resolution="1080p",
            supported_aspect_ratios=["16:9", "9:16", "1:1"],
            max_fps=30,

            # Pricing (FREEMIUM)
            api_cost_per_second=0.02,  # $0.02/sec pay-as-you-go
            api_cost_per_image=0.0,
            free_tier=True,
            free_credits_per_day=1,  # ~30 free generations/month

            # Quality (EXCELLENT!)
            quality_score=90,
            realism_score=92,  # Very realistic
            coherence_score=93,  # Excellent temporal coherence
            prompt_adherence_score=91,

            # Performance
            avg_generation_time_seconds=40.0,  # ~40 seconds
            supports_async=True,

            # Features
            supports_negative_prompts=False,  # Simplified API
            supports_style_presets=False,     # Auto-optimized
            supports_custom_dimensions=False,  # Fixed aspect ratios
            supports_batch_generation=False
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        """
        Generate video from text prompt or image

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

            logger.info(f"Luma Dream Machine generation started: task_id={task_id}")

            # Return pending result
            return GenerationResult(
                status=GenerationStatus.PROCESSING,
                task_id=task_id,
                estimated_completion_time=40.0,
                estimated_cost_usd=self.estimate_cost(request)
            )

        except replicate.exceptions.ReplicateError as e:
            error_msg = str(e)

            # Check for quota/rate limit errors
            if "quota" in error_msg.lower() or "rate limit" in error_msg.lower() or "credits" in error_msg.lower():
                raise QuotaExceededError(f"Luma quota exceeded: {error_msg}")

            raise APIError(f"Luma API error: {error_msg}")

        except Exception as e:
            logger.error(f"Error calling Luma Dream Machine: {e}")
            raise APIError(f"Luma generation failed: {str(e)}")

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

                # Luma returns video URL directly or as list
                if isinstance(output, str):
                    result.output_url = output
                elif isinstance(output, list) and len(output) > 0:
                    result.output_url = output[0]
                elif isinstance(output, dict):
                    result.output_url = output.get("video") or output.get("url")

                if result.output_url:
                    logger.info(f"Luma Dream Machine generation completed: {result.output_url}")
                else:
                    logger.warning("No video URL in Luma response")

            # If failed, extract error
            elif status == GenerationStatus.FAILED:
                result.error_message = prediction.error or "Generation failed"

            return result

        except Exception as e:
            logger.error(f"Error checking Luma status: {e}")
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
                logger.info(f"Luma Dream Machine task {task_id} cancelled")
                return True

            return False

        except Exception as e:
            logger.error(f"Error cancelling Luma task: {e}")
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

        # Mode: text-to-video or image-to-video
        if request.input_image_url:
            params["mode"] = "extend"  # Image-to-video (extend image)
            params["image"] = request.input_image_url
        else:
            params["mode"] = "generate"  # Text-to-video

        # Aspect ratio
        if request.aspect_ratio:
            aspect_map = {
                "16:9": "16:9",
                "9:16": "9:16",
                "1:1": "1:1"
            }
            if request.aspect_ratio in aspect_map:
                params["aspect_ratio"] = aspect_map[request.aspect_ratio]
        else:
            params["aspect_ratio"] = "16:9"  # Default

        # Loop (for seamless looping videos)
        params["loop"] = False  # Default no loop

        # Enhanced prompt (Luma-specific optimization)
        # Luma performs better with cinematic descriptions
        if not any(keyword in request.prompt.lower() for keyword in ["cinematic", "camera", "shot", "scene"]):
            # Auto-enhance prompt for better results
            params["prompt"] = f"Cinematic scene: {request.prompt}"
        else:
            params["prompt"] = request.prompt

        return params

    def estimate_cost(self, request: GenerationRequest) -> float:
        """
        Estimate cost for this generation

        Args:
            request: Generation request

        Returns:
            Estimated cost in USD
        """
        duration = request.duration_seconds or 5.0

        # Check if using free tier (first 30 generations/month)
        # For simplicity, assume pay-as-you-go pricing
        cost_per_second = self.capabilities.api_cost_per_second

        return duration * cost_per_second

    def __str__(self) -> str:
        return "LumaDreamGenerator(LumaLabs, Freemium, Quality=90)"
