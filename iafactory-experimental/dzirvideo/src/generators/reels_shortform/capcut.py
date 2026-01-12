"""
CapCut AI - Video Editing + AI Generation
ByteDance's ultra-popular video editor with AI features
Perfect for TikTok, Reels, Shorts
Official: https://www.capcut.com/
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


class CapCutGenerator(BaseGenerator):
    """
    CapCut AI - Video Editor + AI Generator (ByteDance)

    Features:
    - AI auto-captions (ultra-popular feature)
    - AI text-to-video
    - AI background removal
    - AI voice cloning
    - Templates for TikTok/Reels/Shorts
    - Auto-edit from footage
    - Trending effects library

    Use Cases:
    - TikTok videos
    - Instagram Reels
    - YouTube Shorts
    - Viral content creation

    Pricing:
    - FREE basic features
    - Pro: $7.99/month (AI features, no watermark)

    API: CapCut Cloud API (新接口)
    """

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        """
        Initialize CapCut generator

        Args:
            api_key: CapCut API key (or CAPCUT_API_KEY env var)
            **kwargs: Additional configuration
        """
        if not REQUESTS_AVAILABLE:
            raise ImportError(
                "requests package required. Install with: pip install requests>=2.31.0"
            )

        super().__init__(api_key, **kwargs)

        self.api_key = api_key or os.getenv("CAPCUT_API_KEY")
        if not self.api_key:
            raise ValueError(
                "CapCut API key required. "
                "Set CAPCUT_API_KEY or pass api_key parameter. "
                "Get key from: https://www.capcut.com/tools/api"
            )

        # CapCut Cloud API endpoint
        self.api_base = "https://api.capcut.com/open/v1"

        # Session
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

        logger.info("CapCut AI generator initialized")

    def _define_capabilities(self) -> GeneratorCapabilities:
        """Define CapCut capabilities"""
        return GeneratorCapabilities(
            # Support
            supports_text_to_video=True,  # AI text-to-video
            supports_image_to_video=True,  # AI image animation
            supports_text_to_image=False,
            supports_image_to_image=False,
            supports_avatar_video=False,
            supports_reels_shortform=True,  # PRIMARY USE CASE

            # Specs
            max_duration_seconds=60.0,  # 60 seconds (perfect for Shorts)
            min_duration_seconds=3.0,
            max_resolution="1080p",
            supported_aspect_ratios=["9:16", "16:9", "1:1"],  # Vertical priority
            max_fps=60,  # Supports 60fps for smooth motion

            # Pricing (FREEMIUM)
            api_cost_per_second=0.0,  # Subscription-based
            api_cost_per_image=0.0,
            free_tier=True,
            free_credits_per_day=-1,  # Unlimited free (with watermark)

            # Quality (EXCELLENT for short-form)
            quality_score=92,  # Optimized for viral content
            realism_score=88,
            coherence_score=94,  # Excellent transitions
            prompt_adherence_score=90,

            # Performance (FAST!)
            avg_generation_time_seconds=20.0,  # Very fast (~20s)
            supports_async=True,

            # Features
            supports_negative_prompts=False,
            supports_style_presets=True,  # Tons of templates
            supports_custom_dimensions=False,
            supports_batch_generation=True  # Can batch process
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        """
        Generate video using CapCut AI

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
            # Call CapCut AI API
            response = self.session.post(
                f"{self.api_base}/video/generate",
                json=params,
                timeout=30
            )

            if response.status_code == 429:
                raise QuotaExceededError("CapCut rate limit exceeded")

            if response.status_code == 402:
                raise QuotaExceededError("CapCut quota exceeded")

            if response.status_code != 200:
                error_msg = f"CapCut API error: {response.status_code} - {response.text}"
                raise APIError(error_msg)

            data = response.json()

            # Extract task ID
            task_id = data.get("data", {}).get("task_id") or data.get("task_id")

            if not task_id:
                raise APIError("No task_id in CapCut response")

            logger.info(f"CapCut generation started: task_id={task_id}")

            # Return pending result
            return GenerationResult(
                status=GenerationStatus.PROCESSING,
                task_id=task_id,
                estimated_completion_time=20.0,  # Fast!
                estimated_cost_usd=0.0
            )

        except QuotaExceededError:
            raise

        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling CapCut API: {e}")
            raise APIError(f"CapCut generation failed: {str(e)}")

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise APIError(f"CapCut generation failed: {str(e)}")

    async def check_status(self, task_id: str) -> GenerationResult:
        """Check generation status"""
        try:
            response = self.session.get(
                f"{self.api_base}/video/task/{task_id}",
                timeout=10
            )

            if response.status_code != 200:
                raise APIError(f"Status check failed: {response.status_code}")

            data = response.json()
            status_str = data.get("data", {}).get("status", "processing").lower()

            # Map status
            status_map = {
                "pending": GenerationStatus.PENDING,
                "processing": GenerationStatus.PROCESSING,
                "success": GenerationStatus.COMPLETED,
                "completed": GenerationStatus.COMPLETED,
                "failed": GenerationStatus.FAILED,
                "error": GenerationStatus.FAILED
            }
            status = status_map.get(status_str, GenerationStatus.PROCESSING)

            result = GenerationResult(
                status=status,
                task_id=task_id,
                estimated_cost_usd=0.0
            )

            # If completed, extract video URL
            if status == GenerationStatus.COMPLETED:
                video_data = data.get("data", {})
                video_url = video_data.get("video_url") or video_data.get("output_url")

                if video_url:
                    result.output_url = video_url
                    result.duration_seconds = video_data.get("duration", 30.0)
                    result.width = 1080  # Vertical format
                    result.height = 1920

                    logger.info(f"CapCut generation completed: {video_url}")
                else:
                    logger.warning("No video URL in CapCut response")

            # If failed, extract error
            elif status == GenerationStatus.FAILED:
                result.error_message = (
                    data.get("data", {}).get("error") or
                    data.get("message") or
                    "Generation failed"
                )

            return result

        except Exception as e:
            logger.error(f"Error checking CapCut status: {e}")
            raise APIError(f"Status check failed: {str(e)}")

    async def cancel(self, task_id: str) -> bool:
        """Cancel generation"""
        try:
            result = await self.check_status(task_id)

            if result.status in [GenerationStatus.PENDING, GenerationStatus.PROCESSING]:
                response = self.session.post(
                    f"{self.api_base}/video/task/{task_id}/cancel",
                    timeout=10
                )

                if response.status_code == 200:
                    logger.info(f"CapCut task {task_id} cancelled")
                    return True

            return False

        except Exception as e:
            logger.error(f"Error cancelling CapCut task: {e}")
            return False

    async def wait_for_completion(
        self,
        task_id: str,
        max_wait_seconds: float = 120.0,
        poll_interval: float = 3.0
    ) -> GenerationResult:
        """Wait for completion"""
        start_time = time.time()

        while True:
            result = await self.check_status(task_id)

            if result.status == GenerationStatus.COMPLETED:
                return result

            if result.status == GenerationStatus.FAILED:
                raise APIError(f"Generation failed: {result.error_message}")

            elapsed = time.time() - start_time
            if elapsed > max_wait_seconds:
                await self.cancel(task_id)
                raise TimeoutError(f"Generation timed out after {elapsed:.1f}s")

            await asyncio.sleep(poll_interval)

    def _build_api_params(self, request: GenerationRequest) -> Dict:
        """Build API parameters"""

        params = {
            "prompt": request.prompt,
            "mode": "ai_generate"  # AI generation mode
        }

        # Duration (max 60s)
        if request.duration_seconds:
            duration = min(request.duration_seconds, 60.0)
            params["duration"] = int(duration)
        else:
            params["duration"] = 30  # Default 30s (perfect for Shorts)

        # Aspect ratio (9:16 prioritized for vertical)
        if request.aspect_ratio:
            aspect_map = {
                "9:16": "9:16",   # TikTok/Reels (DEFAULT)
                "16:9": "16:9",   # YouTube
                "1:1": "1:1"      # Instagram
            }
            params["aspect_ratio"] = aspect_map.get(request.aspect_ratio, "9:16")
        else:
            params["aspect_ratio"] = "9:16"  # Default vertical

        # Template/style (CapCut trending templates)
        if request.style_preset:
            # CapCut styles: "trending", "minimal", "dynamic", "vintage", "neon"
            params["template"] = request.style_preset
        else:
            params["template"] = "trending"  # Use trending template

        # AI features
        params["ai_features"] = {
            "auto_captions": True,      # ULTRA-POPULAR feature
            "auto_cut": True,           # Auto-detect best cuts
            "smart_bgm": True,          # Smart background music
            "trending_effects": True,   # Add trending effects
            "color_grading": "vivid"    # Vibrant colors for viral appeal
        }

        # FPS (60fps for smooth motion)
        params["fps"] = 60  # High FPS for quality

        # Audio settings
        params["audio"] = {
            "bgm_enabled": True,
            "bgm_volume": 0.4,  # 40% volume
            "sound_effects": True
        }

        # Watermark (remove with Pro)
        params["watermark"] = False  # Requires Pro subscription

        return params

    def __str__(self) -> str:
        return "CapCutGenerator(ByteDance, FREE/Pro, Quality=92, Viral)"
