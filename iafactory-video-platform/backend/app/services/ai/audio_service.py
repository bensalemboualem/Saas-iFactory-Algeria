"""
Audio Service - TTS, STT, and Music generation
"""
from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
import httpx
import asyncio
from pathlib import Path
from app.core.config import settings


class BaseTTSProvider(ABC):
    """Base class for TTS providers"""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    async def generate(
        self,
        text: str,
        voice_id: str = None,
        **kwargs
    ) -> bytes:
        """Generate audio, returns raw bytes"""
        pass

    @abstractmethod
    async def list_voices(self) -> List[Dict[str, Any]]:
        pass


class ElevenLabsProvider(BaseTTSProvider):
    """ElevenLabs TTS provider"""

    @property
    def name(self) -> str:
        return "elevenlabs"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.elevenlabs.io/v1"

    async def generate(
        self,
        text: str,
        voice_id: str = "21m00Tcm4TlvDq8ikWAM",  # Rachel
        model_id: str = "eleven_multilingual_v2",
        **kwargs
    ) -> bytes:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/text-to-speech/{voice_id}",
                headers={"xi-api-key": self.api_key},
                json={
                    "text": text,
                    "model_id": model_id,
                    "voice_settings": {
                        "stability": kwargs.get("stability", 0.5),
                        "similarity_boost": kwargs.get("similarity_boost", 0.75),
                    }
                },
                timeout=120.0
            )
            response.raise_for_status()
            return response.content

    async def list_voices(self) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/voices",
                headers={"xi-api-key": self.api_key},
            )
            response.raise_for_status()
            data = response.json()
            return [
                {
                    "id": v["voice_id"],
                    "name": v["name"],
                    "category": v.get("category", "generated"),
                    "labels": v.get("labels", {}),
                }
                for v in data["voices"]
            ]


class OpenAITTSProvider(BaseTTSProvider):
    """OpenAI TTS provider"""

    @property
    def name(self) -> str:
        return "openai"

    VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1"

    async def generate(
        self,
        text: str,
        voice_id: str = "nova",
        model: str = "tts-1",  # Use tts-1 (faster) instead of tts-1-hd
        speed: float = 1.0,
        **kwargs
    ) -> bytes:
        # Clean and validate text
        clean_text = text.strip()
        if not clean_text:
            raise ValueError("Text cannot be empty")

        # Truncate if too long (OpenAI limit is ~4096 chars)
        if len(clean_text) > 4000:
            clean_text = clean_text[:4000]

        # Ensure voice is valid
        if voice_id not in self.VOICES:
            voice_id = "nova"

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/audio/speech",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "input": clean_text,
                    "voice": voice_id,
                },
                timeout=120.0
            )
            response.raise_for_status()
            return response.content

    async def list_voices(self) -> List[Dict[str, Any]]:
        return [{"id": v, "name": v.title()} for v in self.VOICES]


class BaseSTTProvider(ABC):
    """Base class for STT providers"""

    @abstractmethod
    async def transcribe(
        self,
        audio_path: str,
        language: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        pass


class WhisperProvider(BaseSTTProvider):
    """OpenAI Whisper STT provider"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1"

    async def transcribe(
        self,
        audio_path: str,
        language: str = None,
        response_format: str = "verbose_json",
        **kwargs
    ) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            with open(audio_path, "rb") as f:
                files = {"file": (Path(audio_path).name, f, "audio/mpeg")}
                data = {"model": "whisper-1", "response_format": response_format}
                if language:
                    data["language"] = language

                response = await client.post(
                    f"{self.base_url}/audio/transcriptions",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    files=files,
                    data=data,
                    timeout=300.0
                )
                response.raise_for_status()
                return response.json()


class BaseMusicProvider(ABC):
    """Base class for music generation"""

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        duration: int = 30,
        **kwargs
    ) -> Dict[str, Any]:
        pass


class SunoProvider(BaseMusicProvider):
    """Suno AI music provider (unofficial API)"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        # Note: Suno doesn't have official API, using proxy
        self.base_url = "https://api.sunoai.io/v1"

    async def generate(
        self,
        prompt: str,
        duration: int = 30,
        instrumental: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        # Placeholder - implement with actual Suno API when available
        return {
            "status": "not_implemented",
            "message": "Suno API integration pending",
            "prompt": prompt,
        }


class AudioService:
    """Unified audio service for TTS, STT, and Music"""

    def __init__(self):
        self._tts_providers: Dict[str, BaseTTSProvider] = {}
        self._stt_providers: Dict[str, BaseSTTProvider] = {}
        self._music_providers: Dict[str, BaseMusicProvider] = {}
        self._init_providers()

    def _init_providers(self):
        # TTS
        if settings.ELEVENLABS_API_KEY:
            self._tts_providers["elevenlabs"] = ElevenLabsProvider(settings.ELEVENLABS_API_KEY)
        if settings.OPENAI_API_KEY:
            self._tts_providers["openai"] = OpenAITTSProvider(settings.OPENAI_API_KEY)

        # STT
        if settings.OPENAI_API_KEY:
            self._stt_providers["whisper"] = WhisperProvider(settings.OPENAI_API_KEY)

        # Music
        if settings.SUNO_API_KEY:
            self._music_providers["suno"] = SunoProvider(settings.SUNO_API_KEY)

    # TTS methods
    async def text_to_speech(
        self,
        text: str,
        provider: str = None,
        voice_id: str = None,
        output_path: Path = None,
        **kwargs
    ) -> Dict[str, Any]:
        provider_name = provider or settings.DEFAULT_TTS_PROVIDER
        if provider_name not in self._tts_providers:
            available = list(self._tts_providers.keys())
            if not available:
                raise ValueError("No TTS providers configured")
            provider_name = available[0]

        p = self._tts_providers[provider_name]
        audio_bytes = await p.generate(text, voice_id, **kwargs)

        result = {
            "provider": p.name,
            "text_length": len(text),
            "format": "mp3",
        }

        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(audio_bytes)
            result["path"] = str(output_path)
        else:
            result["audio_bytes"] = audio_bytes

        return result

    async def list_voices(self, provider: str = None) -> List[Dict[str, Any]]:
        provider_name = provider or settings.DEFAULT_TTS_PROVIDER
        if provider_name in self._tts_providers:
            return await self._tts_providers[provider_name].list_voices()
        return []

    # STT methods
    async def speech_to_text(
        self,
        audio_path: str,
        provider: str = None,
        language: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        provider_name = provider or settings.DEFAULT_STT_PROVIDER
        if provider_name not in self._stt_providers:
            available = list(self._stt_providers.keys())
            if not available:
                raise ValueError("No STT providers configured")
            provider_name = available[0]

        return await self._stt_providers[provider_name].transcribe(
            audio_path, language, **kwargs
        )

    # Music methods
    async def generate_music(
        self,
        prompt: str,
        provider: str = None,
        duration: int = 30,
        **kwargs
    ) -> Dict[str, Any]:
        provider_name = provider or "suno"
        if provider_name not in self._music_providers:
            available = list(self._music_providers.keys())
            if not available:
                raise ValueError("No music providers configured")
            provider_name = available[0]

        return await self._music_providers[provider_name].generate(
            prompt, duration, **kwargs
        )

    def available_tts_providers(self) -> List[str]:
        return list(self._tts_providers.keys())

    def available_stt_providers(self) -> List[str]:
        return list(self._stt_providers.keys())


# Singleton
audio_service = AudioService()
