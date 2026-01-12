"""
Lip-sync Service
Synchronisation automatique des lèvres avec audio
Support multilingue: FR, AR, Darija
"""

from typing import Optional, Literal
from pydantic import BaseModel
import httpx
import os
import asyncio


Language = Literal["fr", "ar", "darija", "en"]


class LipsyncResult(BaseModel):
    """Résultat de synchronisation lip-sync"""
    video_url: str
    duration_seconds: float
    language: str
    quality: str = "high"  # low, medium, high
    service_used: str  # fal-sync-1, wav2lip, d-id


class LipsyncService:
    """
    Service de synchronisation lip-sync

    Supporte plusieurs providers:
    - Fal.ai Sync-1 (meilleure qualité, payant)
    - Wav2Lip (gratuit, qualité moyenne)
    - D-ID (talking heads, payant)

    Spécialité: Support natif arabe et darija
    """

    def __init__(
        self,
        fal_api_key: Optional[str] = None,
        did_api_key: Optional[str] = None,
        provider: str = "fal"  # fal, wav2lip, did
    ):
        self.fal_api_key = fal_api_key or os.getenv("FAL_KEY")
        self.did_api_key = did_api_key or os.getenv("DID_API_KEY")
        self.provider = provider

    async def apply_lipsync(
        self,
        video_path: str,
        audio_path: str,
        language: Language = "fr"
    ) -> LipsyncResult:
        """
        Applique lip-sync sur une vidéo existante

        Args:
            video_path: URL ou chemin de la vidéo source
            audio_path: URL ou chemin de l'audio
            language: Langue de l'audio (fr, ar, darija, en)

        Returns:
            LipsyncResult avec URL de la vidéo synchronisée
        """

        if self.provider == "fal":
            return await self._apply_fal_sync(video_path, audio_path, language)
        elif self.provider == "wav2lip":
            return await self._apply_wav2lip(video_path, audio_path, language)
        elif self.provider == "did":
            return await self._apply_did(video_path, audio_path, language)
        else:
            raise ValueError(f"Provider non supporté: {self.provider}")

    async def _apply_fal_sync(
        self,
        video_path: str,
        audio_path: str,
        language: Language
    ) -> LipsyncResult:
        """Utilise Fal.ai Sync-1 pour lip-sync haute qualité"""

        url = "https://queue.fal.run/fal-ai/sync-1"

        # Mapper language codes
        lang_map = {
            "fr": "french",
            "ar": "arabic",
            "darija": "arabic",  # Traiter darija comme arabe
            "en": "english"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers={
                    "Authorization": f"Key {self.fal_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "video_url": video_path,
                    "audio_url": audio_path,
                    "language": lang_map.get(language, "french"),
                    "quality": "high"
                },
                timeout=120.0
            )

            result = response.json()

            return LipsyncResult(
                video_url=result["video"]["url"],
                duration_seconds=result.get("duration", 0),
                language=language,
                quality="high",
                service_used="fal-sync-1"
            )

    async def _apply_wav2lip(
        self,
        video_path: str,
        audio_path: str,
        language: Language
    ) -> LipsyncResult:
        """
        Utilise Wav2Lip (open-source)
        Qualité moyenne mais gratuit
        """

        # TODO: Implémenter appel à Wav2Lip
        # Peut être hébergé localement ou via Replicate

        raise NotImplementedError("Wav2Lip pas encore implémenté")

    async def _apply_did(
        self,
        video_path: str,
        audio_path: str,
        language: Language
    ) -> LipsyncResult:
        """Utilise D-ID pour talking heads"""

        url = "https://api.d-id.com/talks"

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers={
                    "Authorization": f"Basic {self.did_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "source_url": video_path,
                    "script": {
                        "type": "audio",
                        "audio_url": audio_path
                    },
                    "config": {
                        "stitch": True
                    }
                },
                timeout=120.0
            )

            talk_data = response.json()
            talk_id = talk_data["id"]

            # Attendre la génération (polling)
            video_url = await self._poll_did_result(talk_id)

            return LipsyncResult(
                video_url=video_url,
                duration_seconds=0,  # D-ID ne retourne pas la durée
                language=language,
                quality="high",
                service_used="d-id"
            )

    async def _poll_did_result(self, talk_id: str, max_wait: int = 300) -> str:
        """
        Polling du résultat D-ID

        Args:
            talk_id: ID de la génération
            max_wait: Temps max d'attente en secondes

        Returns:
            URL de la vidéo finale
        """

        url = f"https://api.d-id.com/talks/{talk_id}"

        async with httpx.AsyncClient() as client:
            for _ in range(max_wait // 5):
                response = await client.get(
                    url,
                    headers={"Authorization": f"Basic {self.did_api_key}"}
                )

                data = response.json()
                status = data.get("status")

                if status == "done":
                    return data["result_url"]
                elif status == "error":
                    raise Exception(f"D-ID error: {data.get('error')}")

                await asyncio.sleep(5)

        raise TimeoutError("D-ID génération timeout")

    async def generate_talking_head(
        self,
        character_image_url: str,
        script_text: str,
        voice_id: str,
        language: Language = "fr",
        voice_service: str = "elevenlabs"
    ) -> LipsyncResult:
        """
        Crée une vidéo talking head depuis:
        - Image de personnage
        - Texte à dire
        - Voix ElevenLabs ou autre

        Args:
            character_image_url: URL de l'image du personnage
            script_text: Texte à faire dire
            voice_id: ID de la voix (ElevenLabs)
            language: Langue du texte
            voice_service: Service TTS (elevenlabs, google, azure)

        Returns:
            LipsyncResult avec vidéo du personnage parlant
        """

        # 1. Générer l'audio avec service TTS
        if voice_service == "elevenlabs":
            audio_url = await self._generate_elevenlabs_audio(
                text=script_text,
                voice_id=voice_id,
                language=language
            )
        else:
            raise NotImplementedError(f"Service TTS {voice_service} pas supporté")

        # 2. Appliquer lip-sync sur l'image
        result = await self.apply_lipsync(
            video_path=character_image_url,
            audio_path=audio_url,
            language=language
        )

        return result

    async def _generate_elevenlabs_audio(
        self,
        text: str,
        voice_id: str,
        language: Language
    ) -> str:
        """
        Génère audio avec ElevenLabs

        Args:
            text: Texte à convertir
            voice_id: ID de la voix ElevenLabs
            language: Langue

        Returns:
            URL de l'audio généré
        """

        # Importer service ElevenLabs existant
        from .elevenlabs_service import ElevenLabsService

        elevenlabs = ElevenLabsService()

        # Mapper language
        lang_code = {
            "fr": "fr",
            "ar": "ar",
            "darija": "ar",  # Darija = arabe dialectal
            "en": "en"
        }.get(language, "fr")

        audio_url = await elevenlabs.text_to_speech(
            text=text,
            voice_id=voice_id,
            language_code=lang_code
        )

        return audio_url

    async def batch_lipsync(
        self,
        scenes: list[dict]
    ) -> list[LipsyncResult]:
        """
        Traite plusieurs scènes en parallèle

        Args:
            scenes: Liste de {video_path, audio_path, language}

        Returns:
            Liste de LipsyncResult
        """

        tasks = []
        for scene in scenes:
            task = self.apply_lipsync(
                video_path=scene["video_path"],
                audio_path=scene["audio_path"],
                language=scene.get("language", "fr")
            )
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        return results


# Exemple d'utilisation
if __name__ == "__main__":
    import asyncio

    async def demo():
        service = LipsyncService(provider="fal")

        # Exemple 1: Lip-sync sur vidéo existante
        print("=== LIP-SYNC SUR VIDÉO ===\n")

        result = await service.apply_lipsync(
            video_path="https://example.com/video.mp4",
            audio_path="https://example.com/audio.mp3",
            language="darija"
        )

        print(f"✓ Vidéo synchronisée: {result.video_url}")
        print(f"  Durée: {result.duration_seconds}s")
        print(f"  Service: {result.service_used}")

        # Exemple 2: Talking head
        print("\n=== TALKING HEAD ===\n")

        talking_head = await service.generate_talking_head(
            character_image_url="https://example.com/karim.jpg",
            script_text="Saha rakom! Ana Karim, entrepreneur fi Alger.",
            voice_id="21m00Tcm4TlvDq8ikWAM",  # ElevenLabs voice
            language="darija"
        )

        print(f"✓ Talking head créé: {talking_head.video_url}")

        # Exemple 3: Batch processing
        print("\n=== BATCH PROCESSING ===\n")

        scenes = [
            {
                "video_path": "https://example.com/scene1.mp4",
                "audio_path": "https://example.com/audio1.mp3",
                "language": "fr"
            },
            {
                "video_path": "https://example.com/scene2.mp4",
                "audio_path": "https://example.com/audio2.mp3",
                "language": "darija"
            }
        ]

        results = await service.batch_lipsync(scenes)
        print(f"✓ {len(results)} scènes traitées")

    # asyncio.run(demo())
    print("Demo LipsyncService - Décommenter asyncio.run(demo()) pour tester")
