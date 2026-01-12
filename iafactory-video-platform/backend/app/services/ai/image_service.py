"""
Image Service - Unified interface for all image generation providers
"""
from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
import httpx
import base64
from pathlib import Path
from app.core.config import settings


class BaseImageProvider(ABC):
    """Base class for image providers"""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def cost_per_image(self) -> int:
        """Cost in cents"""
        pass

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        size: str = "1024x1024",
        n: int = 1,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Generate images, returns list of {url, b64_json}"""
        pass


class DalleProvider(BaseImageProvider):
    """OpenAI DALL-E 3 provider"""

    @property
    def name(self) -> str:
        return "dalle"

    @property
    def cost_per_image(self) -> int:
        return 4  # $0.04

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1"

    async def generate(
        self,
        prompt: str,
        size: str = "1024x1024",
        n: int = 1,
        quality: str = "standard",
        style: str = "vivid",
        **kwargs
    ) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/images/generations",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": "dall-e-3",
                    "prompt": prompt,
                    "size": size,
                    "n": 1,  # DALL-E 3 only supports n=1
                    "quality": quality,
                    "style": style,
                },
                timeout=120.0
            )
            response.raise_for_status()
            data = response.json()

            return [{"url": img["url"], "revised_prompt": img.get("revised_prompt")}
                    for img in data["data"]]


class ReplicateProvider(BaseImageProvider):
    """Replicate provider (Flux, SDXL, etc.)"""

    @property
    def name(self) -> str:
        return "replicate"

    @property
    def cost_per_image(self) -> int:
        return 2  # $0.02

    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.replicate.com/v1"

    async def generate(
        self,
        prompt: str,
        size: str = "1024x1024",
        n: int = 1,
        model: str = "flux-schnell",
        **kwargs
    ) -> List[Dict[str, Any]]:
        # Model versions
        models = {
            "flux-schnell": "black-forest-labs/flux-schnell",
            "flux-pro": "black-forest-labs/flux-pro",
            "sdxl": "stability-ai/sdxl:latest",
        }

        model_id = models.get(model, models["flux-schnell"])
        width, height = map(int, size.split("x"))

        async with httpx.AsyncClient() as client:
            # Create prediction
            response = await client.post(
                f"{self.base_url}/predictions",
                headers={"Authorization": f"Token {self.api_token}"},
                json={
                    "version": model_id,
                    "input": {
                        "prompt": prompt,
                        "width": width,
                        "height": height,
                        "num_outputs": n,
                    }
                },
                timeout=30.0
            )
            response.raise_for_status()
            prediction = response.json()

            # Poll for completion
            prediction_id = prediction["id"]
            for _ in range(60):  # Max 60 attempts
                await asyncio.sleep(2)
                status_response = await client.get(
                    f"{self.base_url}/predictions/{prediction_id}",
                    headers={"Authorization": f"Token {self.api_token}"},
                )
                status_data = status_response.json()

                if status_data["status"] == "succeeded":
                    output = status_data["output"]
                    if isinstance(output, list):
                        return [{"url": url} for url in output]
                    return [{"url": output}]
                elif status_data["status"] == "failed":
                    raise Exception(f"Generation failed: {status_data.get('error')}")

            raise Exception("Generation timeout")


class FALProvider(BaseImageProvider):
    """FAL.ai provider (fast Flux)"""

    @property
    def name(self) -> str:
        return "fal"

    @property
    def cost_per_image(self) -> int:
        return 2  # $0.02

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://fal.run"

    async def generate(
        self,
        prompt: str,
        size: str = "1024x1024",
        n: int = 1,
        model: str = "flux/schnell",
        **kwargs
    ) -> List[Dict[str, Any]]:
        width, height = map(int, size.split("x"))

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/fal-ai/{model}",
                headers={"Authorization": f"Key {self.api_key}"},
                json={
                    "prompt": prompt,
                    "image_size": {"width": width, "height": height},
                    "num_images": n,
                },
                timeout=120.0
            )
            response.raise_for_status()
            data = response.json()

            return [{"url": img["url"]} for img in data.get("images", [])]


class LeonardoProvider(BaseImageProvider):
    """Leonardo.ai provider"""

    @property
    def name(self) -> str:
        return "leonardo"

    @property
    def cost_per_image(self) -> int:
        return 2  # $0.02

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://cloud.leonardo.ai/api/rest/v1"

    async def generate(
        self,
        prompt: str,
        size: str = "1024x1024",
        n: int = 1,
        **kwargs
    ) -> List[Dict[str, Any]]:
        width, height = map(int, size.split("x"))

        async with httpx.AsyncClient() as client:
            # Create generation
            response = await client.post(
                f"{self.base_url}/generations",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "prompt": prompt,
                    "width": width,
                    "height": height,
                    "num_images": n,
                },
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            generation_id = data["sdGenerationJob"]["generationId"]

            # Poll for completion
            import asyncio
            for _ in range(30):
                await asyncio.sleep(3)
                status_response = await client.get(
                    f"{self.base_url}/generations/{generation_id}",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                )
                status_data = status_response.json()

                if status_data["generations_by_pk"]["status"] == "COMPLETE":
                    images = status_data["generations_by_pk"]["generated_images"]
                    return [{"url": img["url"]} for img in images]

            raise Exception("Generation timeout")


class ImageService:
    """Unified image generation service"""

    def __init__(self, default_provider: str = None):
        self.default_provider = default_provider or settings.DEFAULT_IMAGE_PROVIDER
        self._providers: Dict[str, BaseImageProvider] = {}
        self._init_providers()

    def _init_providers(self):
        """Initialize available providers"""
        if settings.OPENAI_API_KEY:
            self._providers["dalle"] = DalleProvider(settings.OPENAI_API_KEY)
        if settings.REPLICATE_API_TOKEN:
            self._providers["replicate"] = ReplicateProvider(settings.REPLICATE_API_TOKEN)
            self._providers["flux"] = self._providers["replicate"]
            self._providers["sdxl"] = self._providers["replicate"]
        if settings.FAL_KEY:
            self._providers["fal"] = FALProvider(settings.FAL_KEY)
        if settings.LEONARDO_API_KEY:
            self._providers["leonardo"] = LeonardoProvider(settings.LEONARDO_API_KEY)

    def get_provider(self, name: str = None) -> BaseImageProvider:
        """Get a specific provider or the default one"""
        provider_name = name or self.default_provider
        if provider_name not in self._providers:
            available = list(self._providers.keys())
            if not available:
                raise ValueError("No image providers configured")
            provider_name = available[0]
        return self._providers[provider_name]

    async def generate(
        self,
        prompt: str,
        provider: str = None,
        size: str = "1024x1024",
        n: int = 1,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Generate images"""
        p = self.get_provider(provider)
        images = await p.generate(prompt, size, n, **kwargs)

        # Add metadata
        for img in images:
            img["provider"] = p.name
            img["prompt"] = prompt
            img["cost_cents"] = p.cost_per_image

        return images

    async def download_image(self, url: str, save_path: Path) -> Path:
        """Download image from URL to local path"""
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=60.0)
            response.raise_for_status()

            save_path.parent.mkdir(parents=True, exist_ok=True)
            save_path.write_bytes(response.content)
            return save_path

    def available_providers(self) -> List[str]:
        """List available providers"""
        return list(self._providers.keys())


# Import asyncio for polling
import asyncio

# Singleton
image_service = ImageService()
