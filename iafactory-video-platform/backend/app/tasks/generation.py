"""
Generation Tasks - Individual asset generation tasks
"""
from celery import shared_task
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def generate_single_image(
    self,
    prompt: str,
    provider: str = "dalle",
    size: str = "1024x1024",
    style: str = None
) -> Dict[str, Any]:
    """Generate a single image."""
    from app.agents.image_agent import ImageAgent
    from app.agents.base import AgentTask
    import asyncio

    try:
        agent = ImageAgent(default_provider=provider)
        task = AgentTask(
            task_type="generate_image",
            input_data={
                "prompt": prompt,
                "provider": provider,
                "size": size,
                "style": style
            }
        )

        result = asyncio.run(agent.execute(task))

        if not result.success:
            raise Exception(result.error_message)

        return result.output_data.get("image", {})

    except Exception as e:
        logger.error(f"Image generation failed: {e}")
        self.retry(exc=e)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def generate_video_clip(
    self,
    prompt: str = None,
    image_path: str = None,
    provider: str = "runway",
    duration: int = 5
) -> Dict[str, Any]:
    """Generate a video clip from text or image."""
    from app.agents.video_agent import VideoAgent
    from app.agents.base import AgentTask
    import asyncio

    try:
        agent = VideoAgent(default_provider=provider)

        if image_path:
            task = AgentTask(
                task_type="image_to_video",
                input_data={
                    "image_path": image_path,
                    "motion_prompt": prompt or "subtle cinematic movement",
                    "duration": duration,
                    "provider": provider
                }
            )
        else:
            task = AgentTask(
                task_type="text_to_video",
                input_data={
                    "prompt": prompt,
                    "duration": duration,
                    "provider": provider
                }
            )

        result = asyncio.run(agent.execute(task))

        if not result.success:
            raise Exception(result.error_message)

        return result.output_data.get("video", {})

    except Exception as e:
        logger.error(f"Video generation failed: {e}")
        self.retry(exc=e)


@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def generate_avatar_video(
    self,
    script: str,
    avatar_id: str = None,
    voice_id: str = None,
    provider: str = "heygen",
    language: str = "fr"
) -> Dict[str, Any]:
    """Generate avatar talking head video."""
    from app.agents.avatar_agent import AvatarAgent
    from app.agents.base import AgentTask
    import asyncio

    try:
        agent = AvatarAgent(default_provider=provider)
        task = AgentTask(
            task_type="generate_avatar_video",
            input_data={
                "script": script,
                "avatar_id": avatar_id,
                "voice_id": voice_id,
                "provider": provider,
                "language": language
            }
        )

        result = asyncio.run(agent.execute(task))

        if not result.success:
            raise Exception(result.error_message)

        return result.output_data.get("video", {})

    except Exception as e:
        logger.error(f"Avatar generation failed: {e}")
        self.retry(exc=e)


@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def generate_tts(
    self,
    text: str,
    voice_id: str = None,
    provider: str = "elevenlabs",
    language: str = "fr",
    speed: float = 1.0
) -> Dict[str, Any]:
    """Generate text-to-speech audio."""
    from app.agents.voice_agent import VoiceAgent
    from app.agents.base import AgentTask
    import asyncio

    try:
        agent = VoiceAgent(default_tts_provider=provider)
        task = AgentTask(
            task_type="text_to_speech",
            input_data={
                "text": text,
                "voice_id": voice_id,
                "provider": provider,
                "language": language,
                "speed": speed
            }
        )

        result = asyncio.run(agent.execute(task))

        if not result.success:
            raise Exception(result.error_message)

        return result.output_data.get("audio", {})

    except Exception as e:
        logger.error(f"TTS generation failed: {e}")
        self.retry(exc=e)


@shared_task(bind=True, max_retries=2, default_retry_delay=60)
def generate_music_track(
    self,
    prompt: str,
    duration: int = 60,
    provider: str = "suno",
    genre: str = "background",
    mood: str = "neutral",
    instrumental: bool = True
) -> Dict[str, Any]:
    """Generate music track."""
    from app.agents.voice_agent import VoiceAgent
    from app.agents.base import AgentTask
    import asyncio

    try:
        agent = VoiceAgent()
        task = AgentTask(
            task_type="generate_music",
            input_data={
                "prompt": prompt,
                "duration": duration,
                "provider": provider,
                "genre": genre,
                "mood": mood,
                "instrumental": instrumental
            }
        )

        result = asyncio.run(agent.execute(task))

        if not result.success:
            raise Exception(result.error_message)

        return result.output_data.get("music", {})

    except Exception as e:
        logger.error(f"Music generation failed: {e}")
        self.retry(exc=e)


@shared_task(bind=True, max_retries=2)
def transcribe_audio(
    self,
    audio_path: str,
    provider: str = "whisper",
    language: str = "fr"
) -> Dict[str, Any]:
    """Transcribe audio to text."""
    from app.agents.voice_agent import VoiceAgent
    from app.agents.base import AgentTask
    import asyncio

    try:
        agent = VoiceAgent(default_stt_provider=provider)
        task = AgentTask(
            task_type="speech_to_text",
            input_data={
                "audio_path": audio_path,
                "provider": provider,
                "language": language,
                "timestamps": True
            }
        )

        result = asyncio.run(agent.execute(task))

        if not result.success:
            raise Exception(result.error_message)

        return result.output_data.get("transcription", {})

    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        self.retry(exc=e)


@shared_task(bind=True)
def render_video(
    self,
    timeline: Dict[str, Any],
    output_format: str = "youtube",
    quality: str = "high"
) -> Dict[str, Any]:
    """Render final video from timeline."""
    from app.agents.montage_agent import MontageAgent
    from app.agents.base import AgentTask
    import asyncio

    try:
        agent = MontageAgent()
        task = AgentTask(
            task_type="render_video",
            input_data={
                "timeline": timeline,
                "format": output_format,
                "quality": quality
            }
        )

        result = asyncio.run(agent.execute(task))

        if not result.success:
            raise Exception(result.error_message)

        return result.output_data.get("video", {})

    except Exception as e:
        logger.error(f"Video rendering failed: {e}")
        raise
