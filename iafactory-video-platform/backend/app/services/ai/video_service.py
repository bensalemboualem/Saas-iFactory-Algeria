"""
Video Service - Unified interface for video generation providers
Production-ready implementation with FAL, Runway, Luma, MiniMax, Kling
"""
from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
import httpx
import asyncio
import logging
from pathlib import Path
from app.core.config import settings

logger = logging.getLogger(__name__)


class BaseVideoProvider(ABC):
    """Base class for video providers"""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def cost_per_second(self) -> int:
        """Cost in cents per second of video"""
        pass

    @abstractmethod
    async def generate_from_text(
        self,
        prompt: str,
        duration: int = 5,
        **kwargs
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def generate_from_image(
        self,
        image_url: str,
        motion_prompt: str = "",
        duration: int = 5,
        **kwargs
    ) -> Dict[str, Any]:
        pass


class FALVideoProvider(BaseVideoProvider):
    """FAL.ai video generation provider (fast, reliable)"""

    @property
    def name(self) -> str:
        return "fal"

    @property
    def cost_per_second(self) -> int:
        return 3  # $0.03 per second

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://fal.run"

    async def generate_from_text(
        self,
        prompt: str,
        duration: int = 5,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate video from text prompt using Kling via FAL"""
        async with httpx.AsyncClient(timeout=300.0) as client:
            try:
                # Use Kling model for text-to-video
                response = await client.post(
                    f"{self.base_url}/fal-ai/kling-video/v1/standard/text-to-video",
                    headers={"Authorization": f"Key {self.api_key}"},
                    json={
                        "prompt": prompt,
                        "duration": "5",  # Kling supports "5" or "10"
                        "aspect_ratio": kwargs.get("aspect_ratio", "16:9"),
                    },
                )
                response.raise_for_status()
                data = response.json()

                video_url = data.get("video", {}).get("url") or data.get("video_url")
                return {
                    "url": video_url,
                    "duration": 5,
                    "provider": self.name,
                }

            except Exception as e:
                logger.error(f"FAL text-to-video failed: {e}")
                raise

    async def generate_from_image(
        self,
        image_url: str,
        motion_prompt: str = "",
        duration: int = 5,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate video from image using Kling via FAL"""
        async with httpx.AsyncClient(timeout=300.0) as client:
            try:
                logger.info(f"FAL image-to-video: {image_url[:50]}...")

                # Use Kling image-to-video
                response = await client.post(
                    f"{self.base_url}/fal-ai/kling-video/v1/standard/image-to-video",
                    headers={"Authorization": f"Key {self.api_key}"},
                    json={
                        "prompt": motion_prompt or "gentle camera movement, cinematic",
                        "image_url": image_url,
                        "duration": "5",
                        "aspect_ratio": kwargs.get("aspect_ratio", "16:9"),
                    },
                )
                response.raise_for_status()
                data = response.json()

                video_url = data.get("video", {}).get("url") or data.get("video_url")
                logger.info(f"FAL video generated: {video_url[:50] if video_url else 'no url'}")

                return {
                    "url": video_url,
                    "duration": 5,
                    "provider": self.name,
                }

            except Exception as e:
                logger.error(f"FAL image-to-video failed: {e}")
                raise


class MiniMaxVideoProvider(BaseVideoProvider):
    """MiniMax video generation provider"""

    @property
    def name(self) -> str:
        return "minimax"

    @property
    def cost_per_second(self) -> int:
        return 4  # $0.04 per second

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.minimaxi.chat/v1"

    async def generate_from_text(
        self,
        prompt: str,
        duration: int = 5,
        **kwargs
    ) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=300.0) as client:
            # Create task
            response = await client.post(
                f"{self.base_url}/video_generation",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": "video-01",
                    "prompt": prompt,
                },
            )
            response.raise_for_status()
            data = response.json()
            task_id = data.get("task_id")

            if not task_id:
                raise Exception("No task_id returned from MiniMax")

            # Poll for completion
            return await self._poll_task(client, task_id)

    async def generate_from_image(
        self,
        image_url: str,
        motion_prompt: str = "",
        duration: int = 5,
        **kwargs
    ) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(
                f"{self.base_url}/video_generation",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": "video-01",
                    "prompt": motion_prompt or "smooth cinematic motion",
                    "first_frame_image": image_url,
                },
            )
            response.raise_for_status()
            data = response.json()
            task_id = data.get("task_id")

            return await self._poll_task(client, task_id)

    async def _poll_task(self, client: httpx.AsyncClient, task_id: str) -> Dict[str, Any]:
        for _ in range(120):  # 10 minutes max
            await asyncio.sleep(5)
            response = await client.get(
                f"{self.base_url}/query/video_generation",
                headers={"Authorization": f"Bearer {self.api_key}"},
                params={"task_id": task_id},
            )
            data = response.json()
            status = data.get("status")

            if status == "Success":
                video_url = data.get("file_id")
                return {
                    "url": video_url,
                    "provider": self.name,
                    "task_id": task_id,
                }
            elif status in ["Failed", "Fail"]:
                raise Exception(f"MiniMax generation failed: {data}")

        raise Exception("MiniMax generation timeout")


class RunwayProvider(BaseVideoProvider):
    """Runway Gen-3 Alpha provider"""

    @property
    def name(self) -> str:
        return "runway"

    @property
    def cost_per_second(self) -> int:
        return 5  # $0.05 per second

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.runwayml.com/v1"

    async def generate_from_text(
        self,
        prompt: str,
        duration: int = 5,
        **kwargs
    ) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            # Create generation task
            response = await client.post(
                f"{self.base_url}/text-to-video",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "prompt": prompt,
                    "duration": min(duration, 16),  # Max 16 seconds
                    "model": "gen3a_turbo",
                },
                timeout=30.0
            )
            response.raise_for_status()
            task = response.json()
            task_id = task["id"]

            # Poll for completion
            return await self._poll_task(client, task_id)

    async def generate_from_image(
        self,
        image_url: str,
        motion_prompt: str = "",
        duration: int = 5,
        **kwargs
    ) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/image-to-video",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "image_url": image_url,
                    "prompt": motion_prompt,
                    "duration": min(duration, 10),
                    "model": "gen3a_turbo",
                },
                timeout=30.0
            )
            response.raise_for_status()
            task = response.json()
            return await self._poll_task(client, task["id"])

    async def _poll_task(self, client: httpx.AsyncClient, task_id: str) -> Dict[str, Any]:
        """Poll task until completion"""
        for _ in range(120):  # Max 4 minutes
            await asyncio.sleep(2)
            response = await client.get(
                f"{self.base_url}/tasks/{task_id}",
                headers={"Authorization": f"Bearer {self.api_key}"},
            )
            data = response.json()

            if data["status"] == "SUCCEEDED":
                return {
                    "url": data["output"]["video_url"],
                    "duration": data["output"].get("duration", 5),
                    "provider": self.name,
                }
            elif data["status"] in ["FAILED", "CANCELLED"]:
                raise Exception(f"Generation failed: {data.get('error')}")

        raise Exception("Generation timeout")


class ReplicateVideoProvider(BaseVideoProvider):
    """Replicate video provider (Stable Video Diffusion, etc.)"""

    @property
    def name(self) -> str:
        return "replicate_video"

    @property
    def cost_per_second(self) -> int:
        return 2  # $0.02 per second

    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.replicate.com/v1"

    async def generate_from_text(
        self,
        prompt: str,
        duration: int = 5,
        **kwargs
    ) -> Dict[str, Any]:
        # Text-to-video using AnimateDiff Lightning - use model identifier format
        return await self._run_prediction(
            "bytedance/animatediff-lightning-4-step",
            {
                "prompt": prompt,
                "width": 512,
                "height": 512,
                "num_frames": 16,
            }
        )

    async def generate_from_image(
        self,
        image_url: str,
        motion_prompt: str = "",
        duration: int = 5,
        **kwargs
    ) -> Dict[str, Any]:
        # Image-to-video using LTX Video (Lightricks) - fast and reliable
        # Latest version ID from Replicate
        ltx_version = "8c47da666861d081eeb4d1261853087de23923a268a69b63febdf5dc1dee08e4"
        return await self._run_prediction(
            ltx_version,
            {
                "prompt": motion_prompt or "smooth cinematic motion, gentle camera movement",
                "image": image_url,
                "length": 97,  # ~4 seconds at 24fps
                "target_size": 640,
                "aspect_ratio": "16:9",
                "cfg": 3,
                "steps": 30,
            }
        )

    async def _run_prediction(self, version: str, input_data: Dict) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            # Use the predictions endpoint with version ID
            response = await client.post(
                f"{self.base_url}/predictions",
                headers={
                    "Authorization": f"Bearer {self.api_token}",
                    "Content-Type": "application/json",
                    "Prefer": "wait",  # Wait for result if possible
                },
                json={
                    "version": version,
                    "input": input_data
                },
                timeout=120.0
            )

            if response.status_code == 429:
                error_detail = response.json()
                logger.warning(f"Replicate rate limited: {error_detail}")
                # Wait and retry once
                await asyncio.sleep(5)
                response = await client.post(
                    f"{self.base_url}/predictions",
                    headers={
                        "Authorization": f"Bearer {self.api_token}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "version": version,
                        "input": input_data
                    },
                    timeout=120.0
                )

            if response.status_code == 422:
                error_detail = response.json()
                logger.error(f"Replicate 422 error: {error_detail}")
                raise Exception(f"Invalid request: {error_detail}")

            response.raise_for_status()
            prediction = response.json()

            logger.info(f"Replicate prediction started: {prediction.get('id')}")

            # If status is already completed (from Prefer: wait), return immediately
            if prediction.get("status") == "succeeded":
                output = prediction.get("output")
                video_url = output if isinstance(output, str) else output[0] if output else None
                return {"url": video_url, "provider": self.name}

            # Poll for completion
            poll_url = prediction.get("urls", {}).get("get") or f"{self.base_url}/predictions/{prediction['id']}"

            for i in range(120):  # 6 minutes max
                await asyncio.sleep(3)
                status = await client.get(
                    poll_url,
                    headers={"Authorization": f"Bearer {self.api_token}"},
                    timeout=30.0
                )
                data = status.json()

                if i % 10 == 0:
                    logger.info(f"Replicate status: {data.get('status')}")

                if data["status"] == "succeeded":
                    output = data["output"]
                    video_url = output if isinstance(output, str) else output[0] if output else None
                    logger.info(f"Replicate video generated: {video_url[:50] if video_url else 'no url'}")
                    return {
                        "url": video_url,
                        "provider": self.name,
                    }
                elif data["status"] in ["failed", "canceled"]:
                    error = data.get('error') or data.get('logs', '')
                    logger.error(f"Replicate failed: {error}")
                    raise Exception(f"Failed: {error}")

            raise Exception("Timeout waiting for video generation")


class LumaProvider(BaseVideoProvider):
    """Luma Dream Machine provider"""

    @property
    def name(self) -> str:
        return "luma"

    @property
    def cost_per_second(self) -> int:
        return 4  # $0.04 per second

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.lumalabs.ai/dream-machine/v1"

    async def generate_from_text(
        self,
        prompt: str,
        duration: int = 5,
        **kwargs
    ) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(
                f"{self.base_url}/generations",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "prompt": prompt,
                    "model": "ray-2",  # Luma Ray 2 model
                    "aspect_ratio": kwargs.get("aspect_ratio", "16:9"),
                },
            )

            if response.status_code == 400:
                error = response.json()
                logger.error(f"Luma 400 error: {error}")
                raise Exception(f"Luma error: {error}")

            response.raise_for_status()
            gen = response.json()
            logger.info(f"Luma generation started: {gen.get('id')}")
            return await self._poll_generation(client, gen["id"])

    async def generate_from_image(
        self,
        image_url: str,
        motion_prompt: str = "",
        duration: int = 5,
        **kwargs
    ) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=300.0) as client:
            # Luma image-to-video uses keyframes
            payload = {
                "prompt": motion_prompt or "smooth cinematic motion, gentle camera movement",
                "model": "ray-2",  # Luma Ray 2 model
                "aspect_ratio": kwargs.get("aspect_ratio", "16:9"),
                "keyframes": {
                    "frame0": {
                        "type": "image",
                        "url": image_url
                    }
                }
            }

            logger.info(f"Luma image-to-video: {image_url[:50]}...")

            response = await client.post(
                f"{self.base_url}/generations",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )

            if response.status_code == 400:
                error = response.json()
                logger.error(f"Luma 400 error: {error}")
                raise Exception(f"Luma error: {error}")

            response.raise_for_status()
            gen = response.json()
            logger.info(f"Luma generation started: {gen.get('id')}")
            return await self._poll_generation(client, gen["id"])

    async def _poll_generation(self, client: httpx.AsyncClient, gen_id: str) -> Dict[str, Any]:
        for i in range(180):  # 9 minutes max (Luma can take a while)
            await asyncio.sleep(3)
            response = await client.get(
                f"{self.base_url}/generations/{gen_id}",
                headers={"Authorization": f"Bearer {self.api_key}"},
            )
            data = response.json()

            state = data.get("state", "unknown")
            if i % 10 == 0:
                logger.info(f"Luma status: {state}")

            if state == "completed":
                video_url = data.get("assets", {}).get("video")
                logger.info(f"Luma video generated: {video_url[:50] if video_url else 'no url'}")
                return {
                    "url": video_url,
                    "provider": self.name,
                }
            elif state == "failed":
                reason = data.get('failure_reason', 'Unknown error')
                logger.error(f"Luma failed: {reason}")
                raise Exception(f"Failed: {reason}")

        raise Exception("Timeout waiting for Luma generation")


class WanVideoProvider(BaseVideoProvider):
    """Wan 2.2 Video Provider via Replicate - ECONOMIQUE"""

    @property
    def name(self) -> str:
        return "wan"

    @property
    def cost_per_second(self) -> int:
        return 1  # $0.01 per second (very cheap!)

    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.replicate.com/v1"

    async def generate_from_text(
        self,
        prompt: str,
        duration: int = 5,
        **kwargs
    ) -> Dict[str, Any]:
        # Wan 2.2 text-to-video fast
        return await self._run_prediction(
            "wan-video/wan-2.2-t2v-fast",
            {
                "prompt": prompt,
                "num_frames": 81,  # ~5 seconds at 16fps
                "resolution": kwargs.get("resolution", "480p"),
                "sample_shift": 12,
                "go_fast": True,
            }
        )

    async def generate_from_image(
        self,
        image_url: str,
        motion_prompt: str = "",
        duration: int = 5,
        **kwargs
    ) -> Dict[str, Any]:
        # Wan 2.2 image-to-video fast
        return await self._run_prediction(
            "wan-video/wan-2.2-i2v-fast",
            {
                "prompt": motion_prompt or "smooth natural motion",
                "image": image_url,
                "num_frames": 81,  # ~5 seconds
                "resolution": kwargs.get("resolution", "480p"),
                "sample_shift": 12,
                "go_fast": True,
            }
        )

    async def _run_prediction(self, model: str, input_data: Dict) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=300.0) as client:
            # Create prediction using model endpoint
            response = await client.post(
                f"{self.base_url}/models/{model}/predictions",
                headers={
                    "Authorization": f"Bearer {self.api_token}",
                    "Content-Type": "application/json",
                },
                json={"input": input_data},
            )

            if response.status_code == 429:
                logger.warning("Wan rate limited, waiting...")
                await asyncio.sleep(10)
                response = await client.post(
                    f"{self.base_url}/models/{model}/predictions",
                    headers={
                        "Authorization": f"Bearer {self.api_token}",
                        "Content-Type": "application/json",
                    },
                    json={"input": input_data},
                )

            if response.status_code == 422:
                error = response.json()
                logger.error(f"Wan 422 error: {error}")
                raise Exception(f"Wan error: {error}")

            response.raise_for_status()
            prediction = response.json()
            logger.info(f"Wan prediction started: {prediction.get('id')}")

            # Poll for completion
            poll_url = prediction.get("urls", {}).get("get")
            if not poll_url:
                poll_url = f"{self.base_url}/predictions/{prediction['id']}"

            for i in range(120):  # 6 minutes max
                await asyncio.sleep(3)
                status_resp = await client.get(
                    poll_url,
                    headers={"Authorization": f"Bearer {self.api_token}"},
                )
                data = status_resp.json()

                if i % 10 == 0:
                    logger.info(f"Wan status: {data.get('status')}")

                if data.get("status") == "succeeded":
                    output = data.get("output")
                    video_url = output if isinstance(output, str) else (output[0] if output else None)
                    logger.info(f"Wan video generated: {video_url[:50] if video_url else 'no url'}")
                    return {"url": video_url, "provider": self.name}

                elif data.get("status") in ["failed", "canceled"]:
                    error = data.get("error", "Unknown error")
                    logger.error(f"Wan failed: {error}")
                    raise Exception(f"Wan failed: {error}")

            raise Exception("Wan generation timeout")


# ============================================
# PRICING TIERS - For client-facing options
# ============================================
PRICING_TIERS = {
    "eco": {
        "name": "Economique",
        "name_en": "Economy",
        "providers": ["wan", "replicate"],
        "quality": "480p",
        "cost_per_clip": 0.05,  # $0.05
        "margin": 0.10,  # 100% markup
        "client_price_per_clip": 0.10,  # $0.10
        "description": "Qualite standard, ideal pour tests et reseaux sociaux",
    },
    "standard": {
        "name": "Standard",
        "name_en": "Standard",
        "providers": ["wan", "replicate", "fal"],
        "quality": "720p",
        "cost_per_clip": 0.15,
        "margin": 0.15,
        "client_price_per_clip": 0.30,
        "description": "Bonne qualite pour YouTube et presentations",
    },
    "premium": {
        "name": "Premium",
        "name_en": "Premium",
        "providers": ["luma", "runway"],
        "quality": "1080p",
        "cost_per_clip": 0.50,
        "margin": 0.25,
        "client_price_per_clip": 0.75,
        "description": "Haute qualite cinematique professionnelle",
    },
    "ultra": {
        "name": "Ultra",
        "name_en": "Ultra",
        "providers": ["luma"],
        "quality": "1080p+",
        "cost_per_clip": 0.75,
        "margin": 0.50,
        "client_price_per_clip": 1.25,
        "description": "Qualite maximale pour productions haut de gamme",
    }
}


def get_pricing_for_video(duration_seconds: int, num_scenes: int, tier: str = "standard") -> Dict[str, Any]:
    """Calculate pricing for a video based on tier"""
    tier_info = PRICING_TIERS.get(tier, PRICING_TIERS["standard"])

    # Base costs
    video_cost = num_scenes * tier_info["cost_per_clip"]
    image_cost = num_scenes * 0.04  # DALL-E 3
    llm_cost = 0.001  # Groq is almost free
    audio_cost = (duration_seconds * 150 * 15) / 1_000_000  # OpenAI TTS

    total_cost = video_cost + image_cost + llm_cost + audio_cost
    total_margin = num_scenes * tier_info["margin"]
    client_price = total_cost + total_margin

    return {
        "tier": tier,
        "tier_name": tier_info["name"],
        "quality": tier_info["quality"],
        "duration_seconds": duration_seconds,
        "num_scenes": num_scenes,
        "breakdown": {
            "video": round(video_cost, 2),
            "images": round(image_cost, 2),
            "llm": round(llm_cost, 4),
            "audio": round(audio_cost, 4),
        },
        "our_cost": round(total_cost, 2),
        "margin": round(total_margin, 2),
        "client_price": round(client_price, 2),
        "price_per_second": round(client_price / duration_seconds, 3),
    }


def get_all_tier_prices(duration_seconds: int, num_scenes: int) -> Dict[str, Any]:
    """Get prices for all tiers"""
    return {
        tier: get_pricing_for_video(duration_seconds, num_scenes, tier)
        for tier in PRICING_TIERS.keys()
    }


class VideoService:
    """Unified video generation service"""

    def __init__(self, default_provider: str = None):
        self.default_provider = default_provider or settings.DEFAULT_VIDEO_PROVIDER
        self._providers: Dict[str, BaseVideoProvider] = {}
        self._init_providers()

    def _init_providers(self):
        """Initialize video providers based on available API keys"""
        # Wan 2.2 - ECONOMIQUE via Replicate (priorite haute car pas cher!)
        if settings.REPLICATE_API_TOKEN:
            self._providers["wan"] = WanVideoProvider(settings.REPLICATE_API_TOKEN)
            logger.info("Wan 2.2 video provider initialized (ECO)")

            # Also add Replicate LTX as separate provider
            self._providers["replicate"] = ReplicateVideoProvider(settings.REPLICATE_API_TOKEN)
            self._providers["ltx"] = self._providers["replicate"]
            logger.info("Replicate LTX video provider initialized")

        # FAL AI
        if settings.FAL_KEY:
            self._providers["fal"] = FALVideoProvider(settings.FAL_KEY)
            logger.info("FAL video provider initialized")

        # Runway
        if settings.RUNWAY_API_KEY:
            self._providers["runway"] = RunwayProvider(settings.RUNWAY_API_KEY)
            logger.info("Runway video provider initialized")

        # Luma - PREMIUM
        if settings.LUMA_API_KEY:
            self._providers["luma"] = LumaProvider(settings.LUMA_API_KEY)
            logger.info("Luma video provider initialized (PREMIUM)")

        # MiniMax
        if settings.MINIMAX_API_KEY:
            self._providers["minimax"] = MiniMaxVideoProvider(settings.MINIMAX_API_KEY)
            logger.info("MiniMax video provider initialized")

        if not self._providers:
            logger.warning("No video providers configured! Add API keys to .env")
        else:
            logger.info(f"Available video providers: {list(self._providers.keys())}")

    def get_provider(self, name: str = None) -> BaseVideoProvider:
        provider_name = name or self.default_provider
        if provider_name not in self._providers:
            available = list(self._providers.keys())
            if not available:
                raise ValueError("No video providers configured")
            provider_name = available[0]
        return self._providers[provider_name]

    async def text_to_video(
        self,
        prompt: str,
        provider: str = None,
        duration: int = 5,
        **kwargs
    ) -> Dict[str, Any]:
        p = self.get_provider(provider)
        result = await p.generate_from_text(prompt, duration, **kwargs)
        result["cost_cents"] = p.cost_per_second * duration
        return result

    async def image_to_video(
        self,
        image_url: str,
        motion_prompt: str = "",
        provider: str = None,
        duration: int = 5,
        **kwargs
    ) -> Dict[str, Any]:
        p = self.get_provider(provider)
        result = await p.generate_from_image(image_url, motion_prompt, duration, **kwargs)
        result["cost_cents"] = p.cost_per_second * duration
        return result

    async def download_video(self, url: str, save_path: Path) -> Path:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=300.0)
            response.raise_for_status()
            save_path.parent.mkdir(parents=True, exist_ok=True)
            save_path.write_bytes(response.content)
            return save_path

    def available_providers(self) -> List[str]:
        return list(self._providers.keys())


# Singleton
video_service = VideoService()
