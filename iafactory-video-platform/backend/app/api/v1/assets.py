"""
Assets API endpoints - Images, Audio, Video clips
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID

router = APIRouter()


class ImageGenerateRequest(BaseModel):
    """Demande de génération d'image"""
    prompt: str = Field(..., min_length=5)
    provider: str = Field(default="dalle", description="dalle, flux, sdxl, leonardo, ideogram")
    size: str = Field(default="1024x1024")
    style: Optional[str] = None
    num_images: int = Field(default=1, ge=1, le=4)


class VoiceGenerateRequest(BaseModel):
    """Demande de génération voix"""
    text: str = Field(..., min_length=1)
    provider: str = Field(default="elevenlabs")
    voice_id: Optional[str] = None
    language: str = Field(default="fr")
    speed: float = Field(default=1.0, ge=0.5, le=2.0)
    emotion: str = Field(default="neutral")


class MusicGenerateRequest(BaseModel):
    """Demande de génération de musique"""
    prompt: str = Field(..., min_length=5)
    provider: str = Field(default="suno")
    duration: int = Field(default=30, ge=5, le=300)
    genre: str = Field(default="background")
    mood: str = Field(default="neutral")
    instrumental: bool = Field(default=True)


class VideoClipGenerateRequest(BaseModel):
    """Demande de génération de clip vidéo"""
    prompt: str = Field(default="")
    image_path: Optional[str] = Field(default=None, description="Chemin de l'image source pour image-to-video")
    provider: str = Field(default="runway")
    duration: int = Field(default=5, ge=2, le=16)
    motion_prompt: str = Field(default="subtle movement")


class AssetResponse(BaseModel):
    """Réponse générique pour un asset"""
    id: str
    type: str
    provider: str
    url: Optional[str]
    local_path: Optional[str]
    metadata: dict


# === Image Endpoints ===

@router.post("/images/generate", response_model=List[AssetResponse])
async def generate_images(request: ImageGenerateRequest):
    """
    Génère des images avec l'IA.

    Providers disponibles:
    - dalle: DALL-E 3 (OpenAI) - Haute qualité, bon pour corporate
    - flux: Flux (Replicate) - Photoréaliste
    - sdxl: Stable Diffusion XL - Économique
    - leonardo: Leonardo AI - Cinématique
    - ideogram: Ideogram - Bon pour le texte dans les images
    """
    from app.agents.image_agent import ImageAgent
    from app.agents.base import AgentTask

    agent = ImageAgent(default_provider=request.provider)

    if request.num_images == 1:
        task = AgentTask(
            task_type="generate_image",
            input_data={
                "prompt": request.prompt,
                "provider": request.provider,
                "size": request.size,
                "style": request.style
            }
        )
        result = await agent.execute(task)

        if not result.success:
            raise HTTPException(status_code=500, detail=result.error_message)

        image = result.output_data.get("image", {})
        return [AssetResponse(
            id=image.get("image_id"),
            type="image",
            provider=request.provider,
            url=image.get("url"),
            local_path=image.get("local_path"),
            metadata=image.get("generation_params", {})
        )]
    else:
        task = AgentTask(
            task_type="generate_batch",
            input_data={
                "prompts": [request.prompt] * request.num_images,
                "provider": request.provider,
                "size": request.size
            }
        )
        result = await agent.execute(task)

        if not result.success:
            raise HTTPException(status_code=500, detail=result.error_message)

        images = result.output_data.get("images", [])
        return [AssetResponse(
            id=img.get("image_id"),
            type="image",
            provider=request.provider,
            url=img.get("url"),
            local_path=img.get("local_path"),
            metadata=img.get("generation_params", {})
        ) for img in images]


@router.post("/images/upscale")
async def upscale_image(image_path: str, scale: int = 2):
    """Upscale une image (2x ou 4x)"""
    from app.agents.image_agent import ImageAgent
    from app.agents.base import AgentTask

    agent = ImageAgent()
    task = AgentTask(
        task_type="upscale_image",
        input_data={"image_path": image_path, "scale": scale}
    )
    result = await agent.execute(task)

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error_message)

    return result.output_data


@router.post("/images/remove-background")
async def remove_background(image_path: str):
    """Supprime le fond d'une image"""
    from app.agents.image_agent import ImageAgent
    from app.agents.base import AgentTask

    agent = ImageAgent()
    task = AgentTask(
        task_type="remove_background",
        input_data={"image_path": image_path}
    )
    result = await agent.execute(task)

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error_message)

    return result.output_data


# === Voice/Audio Endpoints ===

@router.post("/voice/generate", response_model=AssetResponse)
async def generate_voice(request: VoiceGenerateRequest):
    """
    Génère une voix off (Text-to-Speech).

    Providers:
    - elevenlabs: Voix naturelles de haute qualité
    - openai: OpenAI TTS
    - google: Google Cloud TTS
    """
    from app.agents.voice_agent import VoiceAgent
    from app.agents.base import AgentTask

    agent = VoiceAgent(default_tts_provider=request.provider)
    task = AgentTask(
        task_type="text_to_speech",
        input_data=request.model_dump()
    )
    result = await agent.execute(task)

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error_message)

    audio = result.output_data.get("audio", {})
    return AssetResponse(
        id=audio.get("audio_id"),
        type="voice",
        provider=request.provider,
        url=audio.get("url"),
        local_path=audio.get("local_path"),
        metadata={"duration": audio.get("duration")}
    )


@router.post("/voice/transcribe")
async def transcribe_audio(
    audio_path: Optional[str] = None,
    audio_url: Optional[str] = None,
    provider: str = "whisper",
    language: str = "fr"
):
    """
    Transcrit un fichier audio (Speech-to-Text).
    """
    from app.agents.voice_agent import VoiceAgent
    from app.agents.base import AgentTask

    agent = VoiceAgent(default_stt_provider=provider)
    task = AgentTask(
        task_type="speech_to_text",
        input_data={
            "audio_path": audio_path,
            "audio_url": audio_url,
            "provider": provider,
            "language": language,
            "timestamps": True
        }
    )
    result = await agent.execute(task)

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error_message)

    return result.output_data


@router.get("/voice/list")
async def list_voices(provider: str = "elevenlabs"):
    """Liste les voix disponibles pour un provider"""
    from app.agents.voice_agent import VoiceAgent
    from app.agents.base import AgentTask

    agent = VoiceAgent()
    task = AgentTask(
        task_type="list_voices",
        input_data={"provider": provider}
    )
    result = await agent.execute(task)
    return result.output_data


# === Music Endpoints ===

@router.post("/music/generate", response_model=AssetResponse)
async def generate_music(request: MusicGenerateRequest):
    """
    Génère de la musique avec l'IA.

    Providers:
    - suno: Suno AI - Musique complète avec/sans paroles
    - udio: Udio - Alternative à Suno
    - musicgen: MusicGen (Meta) - Open source
    """
    from app.agents.voice_agent import VoiceAgent
    from app.agents.base import AgentTask

    agent = VoiceAgent()
    task = AgentTask(
        task_type="generate_music",
        input_data=request.model_dump()
    )
    result = await agent.execute(task)

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error_message)

    music = result.output_data.get("music", {})
    return AssetResponse(
        id=music.get("music_id"),
        type="music",
        provider=request.provider,
        url=music.get("url"),
        local_path=music.get("local_path"),
        metadata={"duration": music.get("duration"), "genre": request.genre}
    )


# === Video Clip Endpoints ===

@router.post("/video-clips/generate", response_model=AssetResponse)
async def generate_video_clip(request: VideoClipGenerateRequest):
    """
    Génère un clip vidéo avec l'IA.

    Providers:
    - runway: Runway Gen-3 Alpha
    - pika: Pika Labs
    - luma: Luma Dream Machine
    - kling: Kling AI
    """
    from app.agents.video_agent import VideoAgent
    from app.agents.base import AgentTask

    agent = VideoAgent(default_provider=request.provider)

    if request.image_path:
        task = AgentTask(
            task_type="image_to_video",
            input_data={
                "image_path": request.image_path,
                "motion_prompt": request.motion_prompt,
                "duration": request.duration,
                "provider": request.provider
            }
        )
    else:
        task = AgentTask(
            task_type="text_to_video",
            input_data={
                "prompt": request.prompt,
                "duration": request.duration,
                "provider": request.provider
            }
        )

    result = await agent.execute(task)

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error_message)

    video = result.output_data.get("video", {})
    return AssetResponse(
        id=video.get("video_id"),
        type="video_clip",
        provider=request.provider,
        url=video.get("url"),
        local_path=video.get("local_path"),
        metadata={"duration": video.get("duration")}
    )


# === Upload Endpoint ===

@router.post("/upload")
async def upload_asset(
    file: UploadFile = File(...),
    asset_type: str = Form(...),
    project_id: Optional[str] = Form(None)
):
    """
    Upload un asset (image, audio, vidéo).
    """
    # TODO: Implémenter l'upload vers le storage
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "asset_type": asset_type,
        "project_id": project_id,
        "status": "uploaded"
    }
