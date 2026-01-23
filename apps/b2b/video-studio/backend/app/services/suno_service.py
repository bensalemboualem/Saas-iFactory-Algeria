"""
Suno AI Music Generation Service
Génération de musique IA pour les vidéos
"""

import httpx
import asyncio
from typing import Optional, List, Literal
from pydantic import BaseModel
from enum import Enum
import structlog

logger = structlog.get_logger()


class MusicStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class MusicStyle(str, Enum):
    CINEMATIC = "cinematic"
    CORPORATE = "corporate"
    AMBIENT = "ambient"
    ELECTRONIC = "electronic"
    ARABIC = "arabic"
    MOTIVATIONAL = "motivational"
    HIP_HOP = "hip_hop"
    POP = "pop"
    CLASSICAL = "classical"
    JAZZ = "jazz"


class SunoMusicRequest(BaseModel):
    prompt: str
    style: MusicStyle = MusicStyle.CINEMATIC
    duration: int = 30  # secondes
    instrumental: bool = True
    tempo: Literal["slow", "medium", "fast"] = "medium"
    mood: Literal["happy", "sad", "energetic", "calm", "dramatic"] = "energetic"


class SunoMusicResponse(BaseModel):
    job_id: str
    status: MusicStatus
    audio_url: Optional[str] = None
    title: Optional[str] = None
    duration: Optional[float] = None
    progress: float = 0
    error: Optional[str] = None


class SunoService:
    """Service de génération musicale avec Suno AI"""

    def __init__(self, api_key: str, base_url: str = "https://api.suno.ai/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.client = httpx.AsyncClient(
            timeout=120.0,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
        )

    async def generate_music(
        self,
        prompt: str,
        style: MusicStyle = MusicStyle.CINEMATIC,
        duration: int = 30,
        instrumental: bool = True,
        tempo: str = "medium",
        mood: str = "energetic"
    ) -> SunoMusicResponse:
        """
        Génère de la musique avec Suno AI.
        
        Args:
            prompt: Description de la musique
            style: Style musical
            duration: Durée en secondes
            instrumental: Sans paroles si True
            tempo: Vitesse
            mood: Ambiance
            
        Returns:
            SunoMusicResponse avec job_id
        """
        try:
            # Construire le prompt enrichi
            full_prompt = self._build_prompt(prompt, style, tempo, mood, instrumental)
            
            payload = {
                "prompt": full_prompt,
                "make_instrumental": instrumental,
                "duration": duration,
                "wait_audio": False  # Mode async
            }

            response = await self.client.post(
                f"{self.base_url}/generations",
                json=payload
            )
            response.raise_for_status()
            data = response.json()

            job_id = data.get("id") or data.get("task_id", "")
            
            logger.info(
                "Suno music generation started",
                job_id=job_id,
                style=style.value,
                duration=duration
            )

            return SunoMusicResponse(
                job_id=job_id,
                status=MusicStatus.PENDING,
                progress=0
            )

        except httpx.HTTPStatusError as e:
            logger.error("Suno API error", status=e.response.status_code)
            return SunoMusicResponse(
                job_id="",
                status=MusicStatus.FAILED,
                error=f"API Error: {e.response.status_code}"
            )
        except Exception as e:
            logger.error("Suno error", error=str(e))
            return SunoMusicResponse(
                job_id="",
                status=MusicStatus.FAILED,
                error=str(e)
            )

    def _build_prompt(
        self,
        prompt: str,
        style: MusicStyle,
        tempo: str,
        mood: str,
        instrumental: bool
    ) -> str:
        """Construit un prompt enrichi pour Suno."""
        style_descriptions = {
            MusicStyle.CINEMATIC: "epic cinematic orchestral soundtrack",
            MusicStyle.CORPORATE: "upbeat corporate background music",
            MusicStyle.AMBIENT: "relaxing ambient electronic soundscape",
            MusicStyle.ELECTRONIC: "modern electronic dance music",
            MusicStyle.ARABIC: "traditional arabic oud and percussion",
            MusicStyle.MOTIVATIONAL: "inspiring motivational background music",
            MusicStyle.HIP_HOP: "urban hip hop beat with bass",
            MusicStyle.POP: "catchy pop music melody",
            MusicStyle.CLASSICAL: "classical orchestral composition",
            MusicStyle.JAZZ: "smooth jazz with saxophone"
        }

        tempo_map = {
            "slow": "60-80 BPM",
            "medium": "100-120 BPM", 
            "fast": "140-160 BPM"
        }

        parts = [
            style_descriptions.get(style, ""),
            f"{tempo_map.get(tempo, '100 BPM')}",
            f"{mood} mood",
            prompt
        ]
        
        if instrumental:
            parts.append("instrumental only, no vocals")

        return ", ".join(filter(None, parts))

    async def get_status(self, job_id: str) -> SunoMusicResponse:
        """
        Récupère le statut d'une génération.
        
        Args:
            job_id: ID de la tâche
            
        Returns:
            SunoMusicResponse avec statut
        """
        try:
            response = await self.client.get(
                f"{self.base_url}/generations/{job_id}"
            )
            response.raise_for_status()
            data = response.json()

            status_raw = data.get("status", "").lower()
            
            if status_raw in ["completed", "complete", "done"]:
                return SunoMusicResponse(
                    job_id=job_id,
                    status=MusicStatus.COMPLETED,
                    audio_url=data.get("audio_url"),
                    title=data.get("title"),
                    duration=data.get("duration"),
                    progress=100
                )
            elif status_raw in ["failed", "error"]:
                return SunoMusicResponse(
                    job_id=job_id,
                    status=MusicStatus.FAILED,
                    error=data.get("error", "Generation failed")
                )
            else:
                return SunoMusicResponse(
                    job_id=job_id,
                    status=MusicStatus.PROCESSING,
                    progress=data.get("progress", 50)
                )

        except Exception as e:
            logger.error("Suno status check error", job_id=job_id, error=str(e))
            return SunoMusicResponse(
                job_id=job_id,
                status=MusicStatus.FAILED,
                error=str(e)
            )

    async def wait_for_completion(
        self,
        job_id: str,
        max_wait: int = 180,
        poll_interval: int = 5
    ) -> SunoMusicResponse:
        """Attend la fin de la génération."""
        elapsed = 0
        while elapsed < max_wait:
            result = await self.get_status(job_id)
            
            if result.status in [MusicStatus.COMPLETED, MusicStatus.FAILED]:
                return result
            
            await asyncio.sleep(poll_interval)
            elapsed += poll_interval

        return SunoMusicResponse(
            job_id=job_id,
            status=MusicStatus.FAILED,
            error="Timeout"
        )

    async def generate_variations(
        self,
        original_job_id: str,
        count: int = 3
    ) -> List[SunoMusicResponse]:
        """
        Génère des variations d'une musique existante.
        
        Args:
            original_job_id: ID de la musique originale
            count: Nombre de variations
            
        Returns:
            Liste de SunoMusicResponse
        """
        try:
            payload = {
                "original_id": original_job_id,
                "count": count
            }

            response = await self.client.post(
                f"{self.base_url}/generations/variations",
                json=payload
            )
            response.raise_for_status()
            data = response.json()

            variations = []
            for item in data.get("variations", []):
                variations.append(SunoMusicResponse(
                    job_id=item.get("id", ""),
                    status=MusicStatus.PENDING
                ))

            return variations

        except Exception as e:
            logger.error("Suno variations error", error=str(e))
            return []

    async def close(self):
        """Ferme le client HTTP."""
        await self.client.aclose()


# Presets de musique prédéfinis
MUSIC_PRESETS = {
    "epic_trailer": {
        "prompt": "powerful epic trailer music with drums and brass",
        "style": MusicStyle.CINEMATIC,
        "tempo": "fast",
        "mood": "dramatic",
        "instrumental": True
    },
    "corporate_upbeat": {
        "prompt": "professional uplifting corporate background",
        "style": MusicStyle.CORPORATE,
        "tempo": "medium",
        "mood": "happy",
        "instrumental": True
    },
    "arabic_traditional": {
        "prompt": "traditional arabic music with oud and darbuka",
        "style": MusicStyle.ARABIC,
        "tempo": "medium",
        "mood": "calm",
        "instrumental": True
    },
    "tech_modern": {
        "prompt": "modern tech startup background music",
        "style": MusicStyle.ELECTRONIC,
        "tempo": "medium",
        "mood": "energetic",
        "instrumental": True
    },
    "motivational_speech": {
        "prompt": "inspiring background for motivational speech",
        "style": MusicStyle.MOTIVATIONAL,
        "tempo": "slow",
        "mood": "dramatic",
        "instrumental": True
    },
    "chill_ambient": {
        "prompt": "relaxing lo-fi ambient background",
        "style": MusicStyle.AMBIENT,
        "tempo": "slow",
        "mood": "calm",
        "instrumental": True
    }
}


def create_suno_service(api_key: str = None) -> SunoService:
    """Factory function pour créer le service Suno."""
    import os
    
    api_key = api_key or os.getenv("SUNO_API_KEY", "")
    
    if not api_key:
        logger.warning("Suno API key not configured")
    
    return SunoService(api_key=api_key)
