import httpx
import structlog
import os
import uuid
from typing import List
from app.core.config import settings

logger = structlog.get_logger()


class ElevenLabsService:
    """Service for interacting with ElevenLabs API"""
    
    BASE_URL = "https://api.elevenlabs.io/v1"
    
    # Predefined voice mappings for Darija/Arabic
    VOICE_MAPPING = {
        "darija_male_1": "pNInz6obpgDQGcFmaJgB",  # Replace with actual voice ID
        "darija_female_1": "EXAVITQu4vr4xnSDxMaL",  # Replace with actual voice ID
        "arabic_male_1": "VR6AewLTigWG4xSOukaG",
        "french_male_1": "pMsXgVXv3BLzUgSXRplE",
        "french_female_1": "jsCqWAovK2LkecY7zXl4",
    }
    
    def __init__(self):
        self.api_key = settings.ELEVENLABS_API_KEY
        
    async def generate_speech(
        self,
        text: str,
        voice_id: str,
        language: str = "darija",
    ) -> dict:
        """Generate speech from text"""
        # Map internal voice ID to ElevenLabs voice ID
        el_voice_id = self.VOICE_MAPPING.get(voice_id, voice_id)
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.BASE_URL}/text-to-speech/{el_voice_id}",
                headers={
                    "xi-api-key": self.api_key,
                    "Content-Type": "application/json",
                },
                json={
                    "text": text,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.75,
                    },
                },
            )
            response.raise_for_status()

            os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
            filename = f"tts-{uuid.uuid4().hex[:8]}.mp3"
            output_path = os.path.join(settings.OUTPUT_DIR, filename)
            with open(output_path, "wb") as f:
                f.write(response.content)

            logger.info("ElevenLabs TTS completed", voice_id=voice_id, language=language)
            
            return {
                "audio_url": f"/outputs/{filename}",
                "duration": len(text) * 0.05,  # Rough estimate
            }
    
    async def clone_voice(self, name: str, audio_files: List[str]) -> str:
        """Clone a voice from audio samples"""
        async with httpx.AsyncClient(timeout=120.0) as client:
            # Download audio files and prepare multipart form
            files = []
            for i, url in enumerate(audio_files):
                audio_response = await client.get(url)
                files.append(("files", (f"sample_{i}.mp3", audio_response.content)))
            
            response = await client.post(
                f"{self.BASE_URL}/voices/add",
                headers={"xi-api-key": self.api_key},
                data={"name": name, "description": f"Custom voice: {name}"},
                files=files,
            )
            response.raise_for_status()
            result = response.json()
            
            logger.info("Voice cloned", name=name, voice_id=result["voice_id"])
            
            return result["voice_id"]
    
    async def list_voices(self) -> List[dict]:
        """List all available voices"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.BASE_URL}/voices",
                headers={"xi-api-key": self.api_key},
            )
            response.raise_for_status()
            return response.json()["voices"]
