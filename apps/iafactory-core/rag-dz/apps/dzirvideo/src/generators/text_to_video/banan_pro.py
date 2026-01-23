"""
Banan Pro - Professional-grade video generation
High-quality commercial video generator with advanced controls
Official: https://banan.pro/
"""

import os
import logging
from typing import Optional
import requests
from ..base import *

logger = logging.getLogger(__name__)


class BananProGenerator(BaseGenerator):
    """Banan Pro - Professional video generation with advanced controls"""

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv("BANAN_PRO_API_KEY")
        if not self.api_key:
            raise ValueError("Banan Pro API key required")
        self.api_base = "https://api.banan.pro/v1"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_video=True,
            max_duration_seconds=15.0,  # Longer videos
            max_resolution="4K",  # Professional quality
            api_cost_per_second=0.08,  # Premium pricing
            free_tier=False,  # Commercial only
            free_credits_per_day=0,
            quality_score=94,  # Very high quality
            avg_generation_time_seconds=150.0,
            supports_negative_prompts=True,
            supports_aspect_ratios=True,
            supports_style_presets=True,
            supports_camera_motion=True,  # Advanced feature
            supports_lighting_control=True  # Advanced feature
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.validate_request(request)

        try:
            params = {
                "prompt": request.prompt,
                "duration": min(request.duration_seconds, 15.0),
                "resolution": "1080p",  # Default, can go up to 4K
                "quality": "professional",
                "model": "banan-pro-v2"
            }

            if request.negative_prompt:
                params["negative_prompt"] = request.negative_prompt

            if request.aspect_ratio:
                params["aspect_ratio"] = request.aspect_ratio

            if request.style:
                params["style"] = request.style

            # Advanced Banan Pro features
            if hasattr(request, 'camera_motion'):
                params["camera_motion"] = request.camera_motion

            if hasattr(request, 'lighting'):
                params["lighting"] = request.lighting

            response = self.session.post(
                f"{self.api_base}/video/generate",
                json=params,
                timeout=30
            )

            if response.status_code == 402:
                raise QuotaExceededError("Banan Pro credits exhausted")

            if response.status_code != 200:
                raise APIError(f"Banan Pro error: {response.text}")

            data = response.json()

            return GenerationResult(
                status=GenerationStatus.PROCESSING,
                task_id=data.get("generation_id"),
                estimated_completion_time=150.0,
                estimated_cost_usd=request.duration_seconds * 0.08
            )

        except QuotaExceededError:
            raise
        except Exception as e:
            logger.error(f"Banan Pro generation error: {e}")
            raise APIError(f"Banan Pro error: {str(e)}")

    async def check_status(self, task_id: str) -> GenerationResult:
        try:
            response = self.session.get(
                f"{self.api_base}/video/status/{task_id}",
                timeout=10
            )

            if response.status_code != 200:
                raise APIError(f"Status check error: {response.text}")

            data = response.json()
            status_str = data.get("status", "processing")

            status_map = {
                "completed": GenerationStatus.COMPLETED,
                "failed": GenerationStatus.FAILED,
                "processing": GenerationStatus.PROCESSING,
                "rendering": GenerationStatus.PROCESSING,
                "queued": GenerationStatus.PROCESSING
            }
            status = status_map.get(status_str, GenerationStatus.PROCESSING)

            result = GenerationResult(status=status, task_id=task_id)

            if status == GenerationStatus.COMPLETED:
                result.output_url = data.get("video_url")
                result.thumbnail_url = data.get("thumbnail")
                result.metadata = {
                    "resolution": data.get("resolution"),
                    "fps": data.get("fps"),
                    "codec": data.get("codec")
                }
            elif status == GenerationStatus.FAILED:
                result.error_message = data.get("error_message", "Generation failed")

            return result

        except Exception as e:
            logger.error(f"Status check error: {e}")
            raise APIError(f"Status check failed: {str(e)}")

    async def cancel(self, task_id: str) -> bool:
        """Banan Pro supports cancellation with refund"""
        try:
            response = self.session.post(
                f"{self.api_base}/video/cancel/{task_id}",
                timeout=10
            )
            return response.status_code == 200
        except:
            return False

    def __str__(self) -> str:
        return "BananProGenerator(Premium $0.08/s, Quality=94, 4K, Advanced)"
