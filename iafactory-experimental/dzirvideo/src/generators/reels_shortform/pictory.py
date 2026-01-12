"""
Pictory AI - Text/Article to Video Generator
Convert blog posts, articles, scripts into engaging videos
Popular for marketing and social media content
Official: https://pictory.ai/
"""

import os
import time
import logging
from typing import Optional, Dict, List
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


class PictoryGenerator(BaseGenerator):
    """
    Pictory AI - Text/Article to Video Generator

    Features:
    - Convert articles/blog posts → videos
    - Auto-generate scenes from text
    - Stock footage library integration
    - Auto-voiceover (text-to-speech)
    - Auto-captions/subtitles
    - Templates for social media (Instagram, YouTube, TikTok)

    Use Cases:
    - Blog post → YouTube video
    - Article → social media clips
    - Script → promo video
    - Text → explainer video

    Pricing:
    - Free trial: 3 videos (10 min each)
    - Standard: $23/month (30 videos)
    - Premium: $47/month (unlimited)

    API: Pictory native API
    """

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Pictory generator

        Args:
            api_key: Pictory API key (or PICTORY_API_KEY env var)
            **kwargs: Additional configuration
        """
        if not REQUESTS_AVAILABLE:
            raise ImportError(
                "requests package required. Install with: pip install requests>=2.31.0"
            )

        super().__init__(api_key, **kwargs)

        self.api_key = api_key or os.getenv("PICTORY_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Pictory API key required. "
                "Set PICTORY_API_KEY or pass api_key parameter. "
                "Get key from: https://pictory.ai/api"
            )

        # Pictory API endpoint
        self.api_base = "https://api.pictory.ai/pictoryapis/v1"

        # Session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            "X-Pictory-User-Id": self.api_key,  # Pictory uses custom auth header
            "Content-Type": "application/json"
        })

        logger.info("Pictory AI generator initialized")

    def _define_capabilities(self) -> GeneratorCapabilities:
        """Define Pictory capabilities"""
        return GeneratorCapabilities(
            # Support
            supports_text_to_video=True,  # PRIMARY FUNCTION
            supports_image_to_video=False,
            supports_text_to_image=False,
            supports_image_to_image=False,
            supports_avatar_video=False,
            supports_reels_shortform=True,  # Great for social media

            # Specs
            max_duration_seconds=600.0,  # 10 minutes max
            min_duration_seconds=10.0,
            max_resolution="1080p",
            supported_aspect_ratios=["16:9", "9:16", "1:1"],  # All social formats
            max_fps=30,

            # Pricing (FREEMIUM)
            api_cost_per_second=0.0,  # Subscription-based, not per-second
            api_cost_per_image=0.0,
            free_tier=True,
            free_credits_per_day=3,  # 3 videos on free trial

            # Quality (GOOD for automated content)
            quality_score=80,  # Template-based, not AI-generated scenes
            realism_score=75,  # Stock footage + voiceover
            coherence_score=85,  # Good scene transitions
            prompt_adherence_score=88,  # Accurate text parsing

            # Performance
            avg_generation_time_seconds=180.0,  # ~3 minutes (longer due to processing)
            supports_async=True,

            # Features
            supports_negative_prompts=False,
            supports_style_presets=True,  # Templates
            supports_custom_dimensions=False,
            supports_batch_generation=False
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        """
        Generate video from text/article

        Args:
            request: Generation request (prompt = article text)

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
            # Step 1: Create storyboard from text
            response = self.session.post(
                f"{self.api_base}/video/storyboard",
                json=params,
                timeout=60
            )

            if response.status_code == 429:
                raise QuotaExceededError("Pictory rate limit exceeded")

            if response.status_code == 402:
                raise QuotaExceededError("Pictory quota exceeded (no credits)")

            if response.status_code != 200:
                error_msg = f"Pictory API error: {response.status_code} - {response.text}"
                raise APIError(error_msg)

            data = response.json()

            # Extract storyboard ID
            storyboard_id = data.get("data", {}).get("storyboard_id")

            if not storyboard_id:
                raise APIError("No storyboard_id in Pictory response")

            # Step 2: Render video from storyboard
            render_response = self.session.post(
                f"{self.api_base}/video/render",
                json={"storyboard_id": storyboard_id},
                timeout=30
            )

            if render_response.status_code != 200:
                raise APIError(f"Pictory render failed: {render_response.text}")

            render_data = render_response.json()
            task_id = render_data.get("data", {}).get("job_id")

            if not task_id:
                raise APIError("No job_id in Pictory render response")

            logger.info(f"Pictory generation started: task_id={task_id}")

            # Return pending result
            return GenerationResult(
                status=GenerationStatus.PROCESSING,
                task_id=task_id,
                estimated_completion_time=180.0,  # ~3 minutes
                estimated_cost_usd=0.0  # Subscription-based
            )

        except QuotaExceededError:
            raise

        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Pictory API: {e}")
            raise APIError(f"Pictory generation failed: {str(e)}")

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise APIError(f"Pictory generation failed: {str(e)}")

    async def check_status(self, task_id: str) -> GenerationResult:
        """
        Check status of video rendering

        Args:
            task_id: Job ID from generate()

        Returns:
            GenerationResult with current status
        """
        try:
            response = self.session.get(
                f"{self.api_base}/video/status/{task_id}",
                timeout=10
            )

            if response.status_code != 200:
                raise APIError(f"Status check failed: {response.status_code}")

            data = response.json()
            status_str = data.get("data", {}).get("status", "processing").lower()

            # Map API status to our enum
            status_map = {
                "pending": GenerationStatus.PENDING,
                "queued": GenerationStatus.PENDING,
                "processing": GenerationStatus.PROCESSING,
                "rendering": GenerationStatus.PROCESSING,
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
                estimated_cost_usd=0.0  # Subscription-based
            )

            # If completed, extract video URL
            if status == GenerationStatus.COMPLETED:
                video_data = data.get("data", {})
                video_url = video_data.get("video_url") or video_data.get("output_url")

                if video_url:
                    result.output_url = video_url
                    result.duration_seconds = video_data.get("duration", 60.0)
                    result.width = 1920  # Assuming 1080p
                    result.height = 1080

                    logger.info(f"Pictory generation completed: {video_url}")
                else:
                    logger.warning("No video URL in Pictory response")

            # If failed, extract error
            elif status == GenerationStatus.FAILED:
                result.error_message = (
                    data.get("data", {}).get("error") or
                    data.get("message") or
                    "Generation failed"
                )

            return result

        except Exception as e:
            logger.error(f"Error checking Pictory status: {e}")
            raise APIError(f"Status check failed: {str(e)}")

    async def cancel(self, task_id: str) -> bool:
        """
        Cancel a running rendering job

        Args:
            task_id: Job identifier

        Returns:
            True if cancelled successfully
        """
        try:
            result = await self.check_status(task_id)

            if result.status in [GenerationStatus.PENDING, GenerationStatus.PROCESSING]:
                response = self.session.delete(
                    f"{self.api_base}/video/render/{task_id}",
                    timeout=10
                )

                if response.status_code == 200:
                    logger.info(f"Pictory job {task_id} cancelled")
                    return True

            return False

        except Exception as e:
            logger.error(f"Error cancelling Pictory job: {e}")
            return False

    async def wait_for_completion(
        self,
        task_id: str,
        max_wait_seconds: float = 600.0,  # 10 minutes max
        poll_interval: float = 10.0  # Poll every 10 seconds
    ) -> GenerationResult:
        """Wait for rendering to complete"""
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
        """Build API parameters from request"""

        params = {
            "content": request.prompt,  # Article/script text
            "format": "auto"  # Auto-detect article format
        }

        # Aspect ratio (for social media templates)
        if request.aspect_ratio:
            aspect_map = {
                "16:9": "landscape",  # YouTube
                "9:16": "portrait",   # TikTok/Reels
                "1:1": "square"       # Instagram
            }
            params["aspect_ratio"] = aspect_map.get(request.aspect_ratio, "landscape")
        else:
            params["aspect_ratio"] = "landscape"

        # Template/style
        if request.style_preset:
            # Pictory templates: "professional", "casual", "vibrant", "minimal"
            params["template"] = request.style_preset
        else:
            params["template"] = "professional"

        # Voice settings (auto TTS)
        params["voice"] = {
            "enabled": True,
            "voice_id": "en-US-Neural2-F",  # Female US English
            "speed": 1.0
        }

        # Captions/subtitles
        params["captions"] = {
            "enabled": True,
            "style": "modern",  # Modern subtitle style
            "position": "bottom"
        }

        # Music (background music)
        params["background_music"] = {
            "enabled": True,
            "genre": "upbeat",
            "volume": 0.3  # 30% volume
        }

        # Scene duration (auto-calculated, but can override)
        params["scene_duration"] = "auto"  # Auto-calculate based on text

        return params

    def __str__(self) -> str:
        return "PictoryGenerator(Pictory.ai, Freemium, Quality=80, Article→Video)"
