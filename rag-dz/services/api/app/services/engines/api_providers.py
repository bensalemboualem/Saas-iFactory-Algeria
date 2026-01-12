"""
API Providers for Dzir IA Video
Use external APIs for video generation (no GPU required)

Providers:
- Stability AI (text-to-image, text-to-video)
- Replicate (Stable Diffusion Video)
- ElevenLabs (TTS)
- Google Cloud TTS (Arabic/French)
"""
import os
import logging
import requests
from pathlib import Path
from typing import Optional, Dict
import time

logger = logging.getLogger(__name__)

class StabilityAPIProvider:
    """
    Stability AI API for video generation
    https://stability.ai/

    Pricing: $0.04 per image, ~$0.80 per 4s video
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("STABILITY_API_KEY")
        self.base_url = "https://api.stability.ai/v2beta"

        if not self.api_key:
            logger.warning("No Stability AI API key found")

    def generate_image(
        self,
        prompt: str,
        width: int = 1024,
        height: int = 576,
        output_path: Optional[Path] = None
    ) -> Path:
        """Generate image from text"""
        try:
            if not self.api_key:
                raise ValueError("Stability AI API key required")

            logger.info(f"Generating image via Stability AI: {prompt[:50]}...")

            response = requests.post(
                f"{self.base_url}/stable-image/generate/core",
                headers={
                    "authorization": f"Bearer {self.api_key}",
                    "accept": "image/*"
                },
                files={"none": ''},
                data={
                    "prompt": prompt,
                    "output_format": "png",
                    "aspect_ratio": f"{width}:{height}"
                }
            )

            if response.status_code == 200:
                if output_path is None:
                    output_path = Path(f"/tmp/stability_{int(time.time())}.png")

                output_path.write_bytes(response.content)
                logger.info(f"✅ Image generated: {output_path}")
                return output_path
            else:
                raise Exception(f"Stability AI error: {response.status_code} - {response.text}")

        except Exception as e:
            logger.error(f"Stability AI generation failed: {str(e)}")
            raise


class ReplicateAPIProvider:
    """
    Replicate API for Stable Diffusion Video
    https://replicate.com/

    Pricing: ~$0.0023 per second of video
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("REPLICATE_API_KEY")
        self.base_url = "https://api.replicate.com/v1"

        if not self.api_key:
            logger.warning("No Replicate API key found")

    def generate_video(
        self,
        prompt: str,
        duration: float = 3.0,
        fps: int = 8,
        output_path: Optional[Path] = None
    ) -> Path:
        """Generate video from text via Replicate"""
        try:
            if not self.api_key:
                raise ValueError("Replicate API key required")

            logger.info(f"Generating video via Replicate: {prompt[:50]}...")

            # Start prediction
            response = requests.post(
                f"{self.base_url}/predictions",
                headers={
                    "Authorization": f"Token {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "version": "9f747673945c62801b13b84701c783929c0ee784e4748ec062204894dda1a351",  # Zeroscope
                    "input": {
                        "prompt": prompt,
                        "num_frames": int(duration * fps),
                        "fps": fps
                    }
                }
            )

            if response.status_code not in [200, 201]:
                raise Exception(f"Replicate error: {response.status_code} - {response.text}")

            prediction_id = response.json()["id"]
            logger.info(f"Prediction started: {prediction_id}")

            # Poll for completion
            while True:
                status_response = requests.get(
                    f"{self.base_url}/predictions/{prediction_id}",
                    headers={"Authorization": f"Token {self.api_key}"}
                )

                result = status_response.json()
                status = result["status"]

                if status == "succeeded":
                    video_url = result["output"]

                    # Download video
                    if output_path is None:
                        output_path = Path(f"/tmp/replicate_{int(time.time())}.mp4")

                    video_data = requests.get(video_url).content
                    output_path.write_bytes(video_data)

                    logger.info(f"✅ Video generated: {output_path}")
                    return output_path

                elif status == "failed":
                    raise Exception(f"Replicate generation failed: {result.get('error')}")

                time.sleep(2)

        except Exception as e:
            logger.error(f"Replicate generation failed: {str(e)}")
            raise


class GoogleCloudTTSProvider:
    """
    Google Cloud Text-to-Speech
    Support for Arabic and French

    Pricing: $4 per 1 million characters (very cheap)
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_CLOUD_TTS_KEY")
        self.base_url = "https://texttospeech.googleapis.com/v1"

        if not self.api_key:
            logger.warning("No Google Cloud TTS API key found")

    def synthesize(
        self,
        text: str,
        language: str = "ar",
        output_path: Optional[Path] = None
    ) -> Path:
        """Synthesize speech from text"""
        try:
            if not self.api_key:
                raise ValueError("Google Cloud TTS API key required")

            # Language mapping
            voice_map = {
                "ar": {"languageCode": "ar-XA", "name": "ar-XA-Wavenet-A"},
                "fr": {"languageCode": "fr-FR", "name": "fr-FR-Wavenet-A"},
                "en": {"languageCode": "en-US", "name": "en-US-Wavenet-D"}
            }

            voice_config = voice_map.get(language, voice_map["en"])

            logger.info(f"Synthesizing {language} speech via Google Cloud TTS...")

            response = requests.post(
                f"{self.base_url}/text:synthesize?key={self.api_key}",
                json={
                    "input": {"text": text},
                    "voice": {
                        "languageCode": voice_config["languageCode"],
                        "name": voice_config["name"]
                    },
                    "audioConfig": {
                        "audioEncoding": "MP3",
                        "speakingRate": 1.0,
                        "pitch": 0.0
                    }
                }
            )

            if response.status_code == 200:
                import base64

                audio_content = response.json()["audioContent"]
                audio_bytes = base64.b64decode(audio_content)

                if output_path is None:
                    output_path = Path(f"/tmp/tts_{language}_{int(time.time())}.mp3")

                output_path.write_bytes(audio_bytes)
                logger.info(f"✅ TTS audio generated: {output_path}")
                return output_path
            else:
                raise Exception(f"Google TTS error: {response.status_code} - {response.text}")

        except Exception as e:
            logger.error(f"Google TTS failed: {str(e)}")
            raise


class ElevenLabsTTSProvider:
    """
    ElevenLabs TTS (high quality, multiple voices)
    https://elevenlabs.io/

    Pricing: Free tier: 10,000 characters/month
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        self.base_url = "https://api.elevenlabs.io/v1"

        if not self.api_key:
            logger.warning("No ElevenLabs API key found")

    def synthesize(
        self,
        text: str,
        voice_id: str = "21m00Tcm4TlvDq8ikWAM",  # Rachel voice
        output_path: Optional[Path] = None
    ) -> Path:
        """Synthesize speech with ElevenLabs"""
        try:
            if not self.api_key:
                raise ValueError("ElevenLabs API key required")

            logger.info(f"Synthesizing speech via ElevenLabs...")

            response = requests.post(
                f"{self.base_url}/text-to-speech/{voice_id}",
                headers={
                    "xi-api-key": self.api_key,
                    "Content-Type": "application/json"
                },
                json={
                    "text": text,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.75
                    }
                }
            )

            if response.status_code == 200:
                if output_path is None:
                    output_path = Path(f"/tmp/elevenlabs_{int(time.time())}.mp3")

                output_path.write_bytes(response.content)
                logger.info(f"✅ ElevenLabs audio generated: {output_path}")
                return output_path
            else:
                raise Exception(f"ElevenLabs error: {response.status_code} - {response.text}")

        except Exception as e:
            logger.error(f"ElevenLabs TTS failed: {str(e)}")
            raise


# Factory functions
def get_video_api_provider(provider: str = "replicate", **kwargs):
    """Get video generation API provider"""
    if provider == "replicate":
        return ReplicateAPIProvider(**kwargs)
    elif provider == "stability":
        return StabilityAPIProvider(**kwargs)
    else:
        raise ValueError(f"Unknown video provider: {provider}")


def get_tts_api_provider(provider: str = "google", **kwargs):
    """Get TTS API provider"""
    if provider == "google":
        return GoogleCloudTTSProvider(**kwargs)
    elif provider == "elevenlabs":
        return ElevenLabsTTSProvider(**kwargs)
    else:
        raise ValueError(f"Unknown TTS provider: {provider}")
