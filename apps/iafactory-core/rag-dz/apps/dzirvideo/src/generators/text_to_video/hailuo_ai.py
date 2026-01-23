"""
Hailuo AI (Minimax Video-01) - Text-to-Video Generator
Chinese AI video generation, high quality, affordable pricing
Official: https://hailuoai.com/
"""

import os
import time
import logging
from typing import Optional, Dict
import asyncio

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

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


class HailuoAIGenerator(BaseGenerator):
    """
    Hailuo AI (Minimax Video-01) Text-to-Video Generator

    Features:
    - High quality Chinese AI (MiniMax Inc.)
    - Affordable pricing ($0.008/second - very cheap!)
    - Free tier: 50 credits (~10 videos)
    - Max 6 seconds per video
    - 720p resolution
    - Fast generation (~30-40 seconds)
    - Good for commercial use

    Pricing:
    - Free: 50 credits (≈10 videos)
    - Pay-as-you-go: $0.008/second
    - Pro: $29/month (unlimited)

    API: Native Hailuo API
    """

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Hailuo AI generator

        Args:
            api_key: Hailuo API key (or HAILUO_API_KEY env var)
            **kwargs: Additional configuration
        """
        if not REQUESTS_AVAILABLE:
            raise ImportError(
                "requests package required. Install with: pip install requests>=2.31.0"
            )

        super().__init__(api_key, **kwargs)

        self.api_key = api_key or os.getenv("HAILUO_API_KEY") or os.getenv("MINIMAX_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Hailuo API key required. "
                "Set HAILUO_API_KEY or pass api_key parameter. "
                "Get key from: https://hailuoai.com/"
            )

        # Hailuo API endpoint
        self.api_base = "https://api.minimax.chat/v1"

        # Session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

        logger.info("Hailuo AI (Minimax) generator initialized")

    def _define_capabilities(self) -> GeneratorCapabilities:
        """Define Hailuo AI capabilities"""
        return GeneratorCapabilities(
            # Support
            supports_text_to_video=True,
            supports_image_to_video=False,  # Text-to-video only
            supports_text_to_image=False,
            supports_image_to_image=False,
            supports_avatar_video=False,
            supports_reels_shortform=True,  # Perfect for Shorts

            # Specs
            max_duration_seconds=6.0,  # 6 seconds max
            min_duration_seconds=2.0,
            max_resolution="720p",
            supported_aspect_ratios=["16:9", "9:16", "1:1"],
            max_fps=30,

            # Pricing (VERY CHEAP!)
            api_cost_per_second=0.008,  # $0.008/sec (80% cheaper than competitors!)
            api_cost_per_image=0.0,
            free_tier=True,
            free_credits_per_day=50,  # 50 free credits

            # Quality (HIGH for Chinese model)
            quality_score=88,
            realism_score=86,
            coherence_score=90,
            prompt_adherence_score=87,

            # Performance (FAST!)
            avg_generation_time_seconds=35.0,  # ~35 seconds
            supports_async=True,

            # Features
            supports_negative_prompts=False,  # Simplified API
            supports_style_presets=True,  # Has style options
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
            # Call Hailuo API
            response = self.session.post(
                f"{self.api_base}/video/generation",
                json=params,
                timeout=30
            )

            if response.status_code == 429:
                raise QuotaExceededError("Hailuo AI rate limit exceeded")

            if response.status_code == 402:
                raise QuotaExceededError("Hailuo AI quota exceeded (no credits)")

            if response.status_code != 200:
                error_msg = f"Hailuo API error: {response.status_code} - {response.text}"
                raise APIError(error_msg)

            data = response.json()

            # Extract task ID
            task_id = data.get("task_id") or data.get("id")

            if not task_id:
                raise APIError("No task_id in Hailuo response")

            logger.info(f"Hailuo AI generation started: task_id={task_id}")

            # Return pending result
            return GenerationResult(
                status=GenerationStatus.PROCESSING,
                task_id=task_id,
                estimated_completion_time=35.0,
                estimated_cost_usd=self.estimate_cost(request)
            )

        except QuotaExceededError:
            raise

        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Hailuo API: {e}")
            raise APIError(f"Hailuo generation failed: {str(e)}")

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise APIError(f"Hailuo generation failed: {str(e)}")

    async def check_status(self, task_id: str) -> GenerationResult:
        """
        Check status of generation task

        Args:
            task_id: Task identifier from generate()

        Returns:
            GenerationResult with current status
        """
        try:
            response = self.session.get(
                f"{self.api_base}/video/generation/{task_id}",
                timeout=10
            )

            if response.status_code != 200:
                raise APIError(f"Status check failed: {response.status_code}")

            data = response.json()
            status_str = data.get("status", "processing").lower()

            # Map API status to our enum
            status_map = {
                "pending": GenerationStatus.PENDING,
                "queued": GenerationStatus.PENDING,
                "processing": GenerationStatus.PROCESSING,
                "generating": GenerationStatus.PROCESSING,
                "completed": GenerationStatus.COMPLETED,
                "success": GenerationStatus.COMPLETED,
                "done": GenerationStatus.COMPLETED,
                "failed": GenerationStatus.FAILED,
                "error": GenerationStatus.FAILED
            }
            status = status_map.get(status_str, GenerationStatus.PROCESSING)

            result = GenerationResult(
                status=status,
                task_id=task_id,
                estimated_cost_usd=0.0  # Updated after completion
            )

            # If completed, extract video URL
            if status == GenerationStatus.COMPLETED:
                video_url = (
                    data.get("video_url") or
                    data.get("output_url") or
                    data.get("result", {}).get("video_url")
                )

                if video_url:
                    result.output_url = video_url
                    result.duration_seconds = data.get("duration", 6.0)
                    result.width = 1280  # Assuming 720p
                    result.height = 720

                    # Calculate actual cost
                    duration = result.duration_seconds or 6.0
                    result.estimated_cost_usd = duration * self.capabilities.api_cost_per_second

                    logger.info(f"Hailuo AI generation completed: {video_url}")
                else:
                    logger.warning("No video URL in Hailuo response")

            # If failed, extract error
            elif status == GenerationStatus.FAILED:
                result.error_message = (
                    data.get("error") or
                    data.get("message") or
                    "Generation failed"
                )

            return result

        except Exception as e:
            logger.error(f"Error checking Hailuo status: {e}")
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
            # Check if task is still running
            result = await self.check_status(task_id)

            if result.status in [GenerationStatus.PENDING, GenerationStatus.PROCESSING]:
                # Try to cancel
                response = self.session.delete(
                    f"{self.api_base}/video/generation/{task_id}",
                    timeout=10
                )

                if response.status_code == 200:
                    logger.info(f"Hailuo AI task {task_id} cancelled")
                    return True

            return False

        except Exception as e:
            logger.error(f"Error cancelling Hailuo task: {e}")
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
            max_wait_seconds: Maximum time to wait
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
            "model": "video-01",  # Hailuo Video-01 model
            "prompt": request.prompt
        }

        # Duration (max 6 seconds)
        if request.duration_seconds:
            duration = min(request.duration_seconds, 6.0)
            params["duration"] = int(duration)
        else:
            params["duration"] = 5  # Default 5 seconds

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

        # Style (Hailuo supports style presets)
        if request.style_preset and self.capabilities.supports_style_presets:
            # Hailuo styles: "realistic", "anime", "cinematic", "vibrant"
            params["style"] = request.style_preset
        else:
            params["style"] = "realistic"  # Default

        # Motion level (for dynamic videos)
        params["motion"] = "high"  # High motion for engaging content

        # Quality preset
        params["quality"] = "high"  # High quality (vs "standard")

        return params

    def estimate_cost(self, request: GenerationRequest) -> float:
        """
        Estimate cost for generation

        Args:
            request: Generation request

        Returns:
            Estimated cost in USD
        """
        duration = request.duration_seconds or 6.0
        duration = min(duration, 6.0)  # Cap at max

        # $0.008 per second
        cost = duration * self.capabilities.api_cost_per_second

        return cost

    def __str__(self) -> str:
        return "HailuoAIGenerator(Minimax, Cheap $0.008/s, Quality=88)"
