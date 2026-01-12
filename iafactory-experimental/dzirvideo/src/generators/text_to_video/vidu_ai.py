"""
Vidu AI - Tencent's Commercial Video Generation
High-quality video generation from Tencent
Official: https://www.vidu.ai/
"""

import os
import logging
from typing import Optional
import requests
from ..base import *

logger = logging.getLogger(__name__)


class ViduAIGenerator(BaseGenerator):
    """Vidu AI - Tencent commercial video generator"""

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv("VIDU_API_KEY")
        if not self.api_key:
            raise ValueError("Vidu AI API key required")
        self.api_base = "https://api.vidu.ai/v1"
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_video=True,
            max_duration_seconds=8.0,
            max_resolution="1080p",
            api_cost_per_second=0.012,
            free_tier=True,
            free_credits_per_day=20,
            quality_score=88,
            avg_generation_time_seconds=90.0,
            supports_style_presets=True
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.validate_request(request)

        try:
            params = {
                "prompt": request.prompt,
                "duration": int(request.duration_seconds),
                "resolution": "1080p"
            }

            if request.style:
                params["style"] = request.style

            response = self.session.post(
                f"{self.api_base}/videos/generate",
                json=params,
                timeout=30
            )

            if response.status_code == 429:
                raise QuotaExceededError("Vidu AI daily quota exceeded")

            if response.status_code != 200:
                raise APIError(f"Vidu AI error: {response.text}")

            data = response.json()
            task_id = data.get("task_id") or data.get("id")

            return GenerationResult(
                status=GenerationStatus.PROCESSING,
                task_id=task_id,
                estimated_completion_time=90.0,
                estimated_cost_usd=request.duration_seconds * 0.012
            )

        except QuotaExceededError:
            raise
        except Exception as e:
            logger.error(f"Vidu AI generation error: {e}")
            raise APIError(f"Vidu AI error: {str(e)}")

    async def check_status(self, task_id: str) -> GenerationResult:
        try:
            response = self.session.get(
                f"{self.api_base}/videos/{task_id}",
                timeout=10
            )

            if response.status_code != 200:
                raise APIError(f"Status check error: {response.text}")

            data = response.json()
            status_str = data.get("status", "").lower()

            status_map = {
                "completed": GenerationStatus.COMPLETED,
                "success": GenerationStatus.COMPLETED,
                "failed": GenerationStatus.FAILED,
                "error": GenerationStatus.FAILED
            }
            status = status_map.get(status_str, GenerationStatus.PROCESSING)

            result = GenerationResult(status=status, task_id=task_id)

            if status == GenerationStatus.COMPLETED:
                result.output_url = data.get("video_url") or data.get("url")
            elif status == GenerationStatus.FAILED:
                result.error_message = data.get("error_message", "Generation failed")

            # Progress percentage
            if "progress" in data:
                result.progress_percentage = float(data["progress"])

            return result

        except Exception as e:
            logger.error(f"Status check error: {e}")
            raise APIError(f"Status check failed: {str(e)}")

    async def cancel(self, task_id: str) -> bool:
        try:
            response = self.session.delete(f"{self.api_base}/videos/{task_id}")
            return response.status_code == 200
        except:
            return False

    def __str__(self) -> str:
        return "ViduAIGenerator(Freemium $0.012/s, Quality=88, Tencent)"
