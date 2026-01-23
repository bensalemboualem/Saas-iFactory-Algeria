"""
IAFactory Video Studio Pro - Orchestrateur de Montage Vidéo
Wrapper pour FFmpeg pour les opérations de montage asynchrones.
"""

import asyncio
import logging
from pathlib import Path
from typing import List, Literal, Optional

import ffmpeg
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


# === MODÈLES ===

class VideoSegment(BaseModel):
    """Représente un segment vidéo à utiliser dans le montage."""
    file_path: str
    start_time: float = 0.0
    end_time: Optional[float] = None


class AudioTrack(BaseModel):
    """Représente une piste audio (voix, musique)."""
    file_path: str
    volume: float = 1.0
    start_at: float = 0.0 # Début de la piste dans la timeline


class SubtitleTrack(BaseModel):
    """Représente une piste de sous-titres."""
    file_path: str
    language: str # ex: "fra", "ara"
    encoding: str = "utf-8"
    # Style pour les sous-titres gravés (format FFmpeg)
    style: str = "FontName=Arial,FontSize=24,PrimaryColour=&H00FFFFFF,BorderStyle=3"


class MontageProject(BaseModel):
    """Définit un projet de montage complet."""
    segments: List[VideoSegment]
    voiceover: Optional[AudioTrack] = None
    music: Optional[AudioTrack] = None
    output_path: str
    resolution: tuple[int, int] = (1920, 1080)
    fps: int = 24


# === ORCHESTRATEUR DE MONTAGE ===

class MontageOrchestrator:
    """
    Orchestre les opérations de montage vidéo avec FFmpeg.
    Exécute les opérations FFmpeg bloquantes dans un thread séparé.
    """

    def _run_ffmpeg_blocking(self, stream: ffmpeg.Stream, output_path: str):
        """Fonction interne bloquante pour exécuter FFmpeg."""
        try:
            logger.info(f"[FFmpeg] Début de l'opération de rendu pour: {output_path}")
            # .overwrite_output() permet de remplacer le fichier s'il existe
            stream.run(overwrite_output=True, quiet=True)
            logger.info(f"[FFmpeg] Opération de rendu terminée pour: {output_path}")
        except ffmpeg.Error as e:
            logger.error(f"[FFmpeg] Erreur FFmpeg: {e.stderr.decode('utf8')}")
            # Relancer l'exception pour que le thread parent la capture
            raise

    async def _execute_stream(self, stream: ffmpeg.Stream, output_path: str) -> bool:
        """Exécute un stream FFmpeg dans un thread séparé."""
        try:
            # Utilise asyncio.to_thread pour ne pas bloquer l'event loop
            await asyncio.to_thread(self._run_ffmpeg_blocking, stream, output_path)
            return True
        except Exception as e:
            logger.error(f"Erreur durant l'exécution du thread FFmpeg: {e}")
            return False

    async def assemble_video(self, project: MontageProject) -> Optional[str]:
        """
        Assemble des clips vidéo, une voix off et de la musique.
        (Implémentation de base)
        """
        logger.info(f"Début de l'assemblage pour le projet: {project.output_path}")
        
        # Valider les entrées
        if not project.segments:
            logger.error("Aucun segment vidéo fourni pour l'assemblage.")
            return None

        video_inputs = [ffmpeg.input(seg.file_path) for seg in project.segments]
        # Concaténer tous les segments vidéo
        video_stream = ffmpeg.concat(*video_inputs, v=1, a=0) # v=1: video, a=0: no audio from source

        audio_streams = []
        if project.voiceover:
            voice_stream = ffmpeg.input(project.voiceover.file_path).filter('volume', project.voiceover.volume)
            audio_streams.append(voice_stream)

        if project.music:
            music_stream = ffmpeg.input(project.music.file_path).filter('volume', project.music.volume)
            audio_streams.append(music_stream)

        if len(audio_streams) > 0:
            # Mixer les pistes audio s'il y en a plusieurs
            mixed_audio = ffmpeg.filter(audio_streams, 'amix', inputs=len(audio_streams))
            # Combiner le flux vidéo et le flux audio mixé
            final_stream = ffmpeg.concat(video_stream, mixed_audio, v=1, a=1).output(
                project.output_path,
                r=project.fps,
                s=f"{project.resolution[0]}x{project.resolution[1]}"
            )
        else:
            # Pas d'audio, juste le flux vidéo
            final_stream = ffmpeg.output(
                video_stream,
                project.output_path,
                r=project.fps,
                s=f"{project.resolution[0]}x{project.resolution[1]}"
            )

        success = await self._execute_stream(final_stream, project.output_path)
        return project.output_path if success else None

    async def add_subtitles(self, video_path: str, subtitle: SubtitleTrack) -> Optional[str]:
        """
        Grave (burn) des sous-titres sur une vidéo.
        """
        output_path = f"{Path(video_path).stem}_subtitled.mp4"
        logger.info(f"Ajout de sous-titres à '{video_path}' -> '{output_path}'")
        
        video_input = ffmpeg.input(video_path)
        stream = video_input.filter(
            'subtitles',
            filename=subtitle.file_path,
            force_style=subtitle.style
        ).output(output_path)
        
        success = await self._execute_stream(stream, output_path)
        return output_path if success else None

    async def convert_format(
        self,
        video_path: str,
        target_resolution: tuple[int, int] = (1080, 1920), # ex: 9:16
        target_fps: int = 30
    ) -> Optional[str]:
        """
        Convertit une vidéo à une nouvelle résolution et/ou framerate.
        """
        output_path = f"{Path(video_path).stem}_{target_resolution[0]}x{target_resolution[1]}.mp4"
        logger.info(f"Conversion de '{video_path}' -> '{output_path}'")
        
        stream = ffmpeg.input(video_path).output(
            output_path,
            s=f"{target_resolution[0]}x{target_resolution[1]}",
            r=target_fps
        )
        
        success = await self._execute_stream(stream, output_path)
        return output_path if success else None

    async def extract_segment(
        self,
        video_path: str,
        start_seconds: float,
        end_seconds: float
    ) -> Optional[str]:
        """
        Extrait un segment d'une vidéo.
        """
        output_path = f"{Path(video_path).stem}_segment_{start_seconds:.0f}s_{end_seconds:.0f}s.mp4"
        logger.info(f"Extraction du segment [{start_seconds}s - {end_seconds}s] de '{video_path}'")
        
        stream = ffmpeg.input(video_path).trim(
            start=start_seconds,
            end=end_seconds
        ).output(output_path)
        
        success = await self._execute_stream(stream, output_path)
        return output_path if success else None


# === FACTORY FUNCTION ===

_montage_orchestrator: Optional[MontageOrchestrator] = None

def get_montage_orchestrator() -> MontageOrchestrator:
    """Retourne l'instance singleton de l'orchestrateur de montage."""
    global _montage_orchestrator
    if _montage_orchestrator is None:
        _montage_orchestrator = MontageOrchestrator()
    return _montage_orchestrator
