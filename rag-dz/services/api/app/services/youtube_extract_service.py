"""
YouTube Audio Extraction Service - Privacy-First
IAFactory 2025

Endpoint: POST /api/media/youtube-extract
- Extrait l'audio d'une video YouTube
- Stream direct, pas de stockage permanent (Privacy-First)
- Utilise yt-dlp (fork de youtube-dl)
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, HttpUrl
import subprocess
import tempfile
import os
import re
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/media", tags=["media"])


class YouTubeExtractRequest(BaseModel):
    url: str
    format: str = "audio"  # audio | video
    stream: bool = True    # Privacy-first: no permanent storage


class YouTubeExtractResponse(BaseModel):
    success: bool
    message: str
    duration: float = None
    title: str = None


def validate_youtube_url(url: str) -> bool:
    """Valide une URL YouTube"""
    patterns = [
        r'^(https?://)?(www\.)?youtube\.com/watch\?v=[\w-]+',
        r'^(https?://)?(www\.)?youtu\.be/[\w-]+',
        r'^(https?://)?(www\.)?youtube\.com/shorts/[\w-]+'
    ]
    return any(re.match(p, url) for p in patterns)


def extract_video_id(url: str) -> str:
    """Extrait l'ID de la video YouTube"""
    patterns = [
        r'(?:v=|youtu\.be/|shorts/)([a-zA-Z0-9_-]{11})',
    ]
    for p in patterns:
        match = re.search(p, url)
        if match:
            return match.group(1)
    return None


@router.post("/youtube-extract")
async def youtube_extract(request: YouTubeExtractRequest):
    """
    Extrait l'audio d'une video YouTube en mode streaming.
    Privacy-First: Le fichier est supprime apres envoi.
    """

    # Validation URL
    if not validate_youtube_url(request.url):
        raise HTTPException(status_code=400, detail="URL YouTube invalide")

    video_id = extract_video_id(request.url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Impossible d'extraire l'ID video")

    logger.info(f"YouTube extract: {video_id}")

    # Creer fichier temporaire (sera supprime apres streaming)
    temp_dir = tempfile.mkdtemp(prefix="yt_")
    output_path = os.path.join(temp_dir, f"{video_id}.mp3")

    try:
        # yt-dlp command pour extraire audio uniquement
        cmd = [
            "yt-dlp",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "128K",  # Qualite raisonnable pour transcription
            "--no-playlist",
            "--no-warnings",
            "--quiet",
            "--output", output_path,
            request.url
        ]

        # Executer yt-dlp
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120  # 2 minutes max
        )

        if result.returncode != 0:
            logger.error(f"yt-dlp error: {result.stderr}")
            raise HTTPException(
                status_code=500,
                detail=f"Extraction failed: {result.stderr[:200]}"
            )

        # Verifier que le fichier existe
        if not os.path.exists(output_path):
            raise HTTPException(status_code=500, detail="Audio file not created")

        file_size = os.path.getsize(output_path)
        logger.info(f"Audio extracted: {file_size} bytes")

        # Streaming response avec cleanup automatique
        def iterfile():
            try:
                with open(output_path, "rb") as f:
                    while chunk := f.read(8192):
                        yield chunk
            finally:
                # Privacy-First: Supprimer apres envoi
                try:
                    os.remove(output_path)
                    os.rmdir(temp_dir)
                    logger.info(f"Cleaned up temp files for {video_id}")
                except Exception as e:
                    logger.warning(f"Cleanup error: {e}")

        return StreamingResponse(
            iterfile(),
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f'attachment; filename="{video_id}.mp3"',
                "Content-Length": str(file_size),
                "X-Video-ID": video_id
            }
        )

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Extraction timeout (max 2 min)")
    except Exception as e:
        logger.error(f"YouTube extract error: {e}")
        # Cleanup en cas d'erreur
        try:
            if os.path.exists(output_path):
                os.remove(output_path)
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)
        except:
            pass
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/youtube-info/{video_id}")
async def youtube_info(video_id: str):
    """
    Recupere les metadonnees d'une video YouTube sans telecharger.
    """
    if not re.match(r'^[\w-]{11}$', video_id):
        raise HTTPException(status_code=400, detail="Video ID invalide")

    url = f"https://www.youtube.com/watch?v={video_id}"

    try:
        cmd = [
            "yt-dlp",
            "--dump-json",
            "--no-download",
            "--no-warnings",
            url
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            raise HTTPException(status_code=404, detail="Video not found")

        import json
        info = json.loads(result.stdout)

        return {
            "id": video_id,
            "title": info.get("title", ""),
            "duration": info.get("duration", 0),
            "channel": info.get("channel", ""),
            "view_count": info.get("view_count", 0),
            "thumbnail": info.get("thumbnail", "")
        }

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
