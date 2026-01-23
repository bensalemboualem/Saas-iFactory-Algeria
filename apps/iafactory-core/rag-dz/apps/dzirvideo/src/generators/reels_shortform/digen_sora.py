"""
DIGEN Sora - Mini Sora for Short-Form Content
Unlimited FREE AI video generation for Reels/Shorts/TikTok
Official: https://digen.ai/
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


class DIGENSoraGenerator(BaseGenerator):
    """
    DIGEN Sora - Mini Sora Text-to-Video Generator

    Features:
    - UNLIMITED FREE (no credits required!)
    - Optimized for short-form content (Reels, Shorts, TikTok)
    - Max 10 seconds per video
    - 720p resolution
    - Fast generation (~20-30 seconds)
    - Perfect for viral content

    API: Public free API (no key required for basic usage)
    """

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        """
        Initialize DIGEN Sora generator

        Args:
            api_key: Optional API key for higher limits (FREE tier works without)
            **kwargs: Additional configuration
        """
        if not REQUESTS_AVAILABLE:
            raise ImportError(
                "requests package required. Install with: pip install requests>=2.31.0"
            )

        super().__init__(api_key, **kwargs)

        # DIGEN API endpoint (free tier)
        self.api_base = "https://api.digen.ai/v1"
        self.api_key = api_key or os.getenv("DIGEN_API_KEY")  # Optional

        # Session for connection pooling
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

        logger.info("DIGEN Sora generator initialized (FREE unlimited)")

    def _define_capabilities(self) -> GeneratorCapabilities:
        """Define DIGEN Sora capabilities"""
        return GeneratorCapabilities(
            # Support
            supports_text_to_video=True,
            supports_image_to_video=False,  # Text-to-video only for now
            supports_text_to_image=False,
            supports_image_to_image=False,
            supports_avatar_video=False,
            supports_reels_shortform=True,  # PRIMARY USE CASE

            # Specs
            max_duration_seconds=10.0,  # 10 seconds max (perfect for Shorts)
            min_duration_seconds=3.0,
            max_resolution="720p",  # HD quality
            supported_aspect_ratios=["9:16", "16:9", "1:1"],  # Vertical first!
            max_fps=30,

            # Pricing (FREE UNLIMITED!)
            api_cost_per_second=0.0,  # FREE!
            api_cost_per_image=0.0,
            free_tier=True,
            free_credits_per_day=-1,  # Unlimited!

            # Quality (Good for free)
            quality_score=78,  # Solid quality for short-form
            realism_score=74,
            coherence_score=82,  # Good temporal coherence
            prompt_adherence_score=80,

            # Performance (FAST!)
            avg_generation_time_seconds=25.0,  # ~25 seconds
            supports_async=True,

            # Features
            supports_negative_prompts=False,  # Simplified API
            supports_style_presets=True,  # Has preset styles
            supports_custom_dimensions=False,  # Fixed resolutions
            supports_batch_generation=False
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        """
        Generate short-form video from text prompt

        Args:
            request: Generation request

        Returns:
            GenerationResult with task ID

        Raises:
            ValueError: If request invalid
            APIError: If API call fails
        """
        # Validate request
        self.validate_request(request)

        # Build API parameters
        params = self._build_api_params(request)

        try:
            # Call DIGEN API (async)
            response = self.session.post(
                f"{self.api_base}/generate",
                json=params,
                timeout=30
            )

            if response.status_code != 200:
                error_msg = f"DIGEN API error: {response.status_code} - {response.text}"
                raise APIError(error_msg)

            data = response.json()
            task_id = data.get("task_id") or data.get("id")

            if not task_id:
                raise APIError("No task_id in DIGEN response")

            logger.info(f"DIGEN Sora generation started: task_id={task_id}")

            # Return pending result
            return GenerationResult(
                status=GenerationStatus.PROCESSING,
                task_id=task_id,
                estimated_completion_time=25.0,  # Fast!
                estimated_cost_usd=0.0  # FREE!
            )

        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling DIGEN API: {e}")
            raise APIError(f"DIGEN generation failed: {str(e)}")

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise APIError(f"DIGEN generation failed: {str(e)}")

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
                f"{self.api_base}/status/{task_id}",
                timeout=10
            )

            if response.status_code != 200:
                raise APIError(f"Status check failed: {response.status_code}")

            data = response.json()
            status_str = data.get("status", "processing").lower()

            # Map API status to our enum
            status_map = {
                "pending": GenerationStatus.PENDING,
                "processing": GenerationStatus.PROCESSING,
                "generating": GenerationStatus.PROCESSING,
                "completed": GenerationStatus.COMPLETED,
                "success": GenerationStatus.COMPLETED,
                "failed": GenerationStatus.FAILED,
                "error": GenerationStatus.FAILED
            }
            status = status_map.get(status_str, GenerationStatus.PROCESSING)

            result = GenerationResult(
                status=status,
                task_id=task_id,
                estimated_cost_usd=0.0  # Always free
            )

            # If completed, extract video URL
            if status == GenerationStatus.COMPLETED:
                video_url = data.get("video_url") or data.get("output") or data.get("url")

                if video_url:
                    result.output_url = video_url
                    result.duration_seconds = data.get("duration", 10.0)
                    result.width = 720  # Assuming 720p
                    result.height = 1280 if "9:16" in str(data.get("aspect_ratio")) else 720

                    logger.info(f"DIGEN Sora generation completed: {video_url}")
                else:
                    logger.warning("No video URL in DIGEN response")

            # If failed, extract error
            elif status == GenerationStatus.FAILED:
                result.error_message = data.get("error") or data.get("message") or "Generation failed"

            return result

        except Exception as e:
            logger.error(f"Error checking DIGEN status: {e}")
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
                response = self.session.post(
                    f"{self.api_base}/cancel/{task_id}",
                    timeout=10
                )

                if response.status_code == 200:
                    logger.info(f"DIGEN task {task_id} cancelled")
                    return True

            return False

        except Exception as e:
            logger.error(f"Error cancelling DIGEN task: {e}")
            return False

    async def wait_for_completion(
        self,
        task_id: str,
        max_wait_seconds: float = 120.0,
        poll_interval: float = 3.0
    ) -> GenerationResult:
        """
        Wait for generation to complete

        Args:
            task_id: Task identifier
            max_wait_seconds: Maximum time to wait (default 2 minutes)
            poll_interval: Seconds between status checks (faster polling for quick API)

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

            # Wait before next poll (short interval for fast API)
            await asyncio.sleep(poll_interval)

    def _build_api_params(self, request: GenerationRequest) -> Dict:
        """Build API parameters from request"""

        params = {
            "prompt": request.prompt,
            "type": "short_form"  # Optimize for Reels/Shorts
        }

        # Duration (in seconds, max 10)
        if request.duration_seconds:
            duration = min(request.duration_seconds, 10.0)
            params["duration"] = int(duration)
        else:
            params["duration"] = 5  # Default 5 seconds (perfect for Shorts)

        # Aspect ratio (9:16 prioritized for vertical video)
        if request.aspect_ratio:
            aspect_map = {
                "9:16": "vertical",   # 720x1280 (Reels/Shorts)
                "16:9": "horizontal", # 1280x720 (YouTube)
                "1:1": "square"       # 720x720 (Instagram)
            }
            aspect = aspect_map.get(request.aspect_ratio, "vertical")
            params["aspect_ratio"] = aspect
        else:
            params["aspect_ratio"] = "vertical"  # Default to 9:16

        # Style preset (DIGEN styles optimized for viral content)
        if request.style_preset and self.capabilities.supports_style_presets:
            # DIGEN styles: "dynamic", "cinematic", "vibrant", "minimalist"
            params["style"] = request.style_preset
        else:
            params["style"] = "dynamic"  # Default for engaging content

        # Motion intensity (for short-form, higher motion = more engaging)
        params["motion_level"] = "high"  # High motion for viral appeal

        # Speed (DIGEN can fast-track generation for short videos)
        params["priority"] = "fast"  # Faster generation for short clips

        # FPS (30fps for smooth Reels/Shorts)
        params["fps"] = 30

        # Optimization flags
        params["optimize_for"] = "mobile"  # Mobile-first (Shorts/Reels/TikTok)
        params["auto_enhance"] = True      # Auto color/contrast enhancement

        return params

    def __str__(self) -> str:
        return "DIGENSoraGenerator(DIGEN, FREE Unlimited, Quality=78, Reels/Shorts)"
