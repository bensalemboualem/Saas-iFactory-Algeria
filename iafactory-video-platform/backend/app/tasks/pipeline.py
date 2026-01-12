"""
Pipeline Tasks - Main video creation workflow
"""
from celery import shared_task, chain, group
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def run_full_pipeline(self, project_id: str, options: Dict[str, Any] = None):
    """
    Execute the complete video creation pipeline.

    Pipeline steps:
    1. Analyze prompt -> 2. Generate script -> 3. Generate assets (parallel)
    4. Montage video -> 5. Quality check -> 6. Publish (optional)
    """
    options = options or {}
    logger.info(f"Starting pipeline for project {project_id}")

    try:
        # Build pipeline chain
        pipeline = chain(
            analyze_prompt.s(project_id),
            generate_script.s(),
            generate_assets_parallel.s(),
            montage_video.s(),
            quality_check.s(),
        )

        # Add publishing if auto_publish is enabled
        if options.get("auto_publish"):
            pipeline = pipeline | publish_video.s()

        # Execute pipeline
        result = pipeline.apply_async()

        return {
            "project_id": project_id,
            "pipeline_id": result.id,
            "status": "started"
        }

    except Exception as e:
        logger.error(f"Pipeline failed for project {project_id}: {e}")
        self.retry(exc=e, countdown=60)


@shared_task(bind=True)
def analyze_prompt(self, project_id: str) -> Dict[str, Any]:
    """Analyze user prompt and extract video requirements."""
    from app.agents.orchestrator import OrchestratorAgent
    from app.agents.base import AgentTask
    import asyncio

    logger.info(f"Analyzing prompt for project {project_id}")

    # TODO: Get project from database
    user_prompt = "Sample prompt"  # Replace with actual DB fetch

    agent = OrchestratorAgent()
    task = AgentTask(
        task_type="analyze_prompt",
        input_data={"prompt": user_prompt, "language": "fr"}
    )

    result = asyncio.run(agent.execute(task))

    return {
        "project_id": project_id,
        "analysis": result.output_data.get("analysis", {}),
        "status": "analyzed"
    }


@shared_task(bind=True)
def generate_script(self, previous_result: Dict[str, Any]) -> Dict[str, Any]:
    """Generate video script based on analysis."""
    from app.agents.script_agent import ScriptAgent
    from app.agents.base import AgentTask
    import asyncio

    project_id = previous_result.get("project_id")
    analysis = previous_result.get("analysis", {})

    logger.info(f"Generating script for project {project_id}")

    agent = ScriptAgent()
    task = AgentTask(
        task_type="generate_script",
        input_data={
            "topic": analysis.get("topic", ""),
            "duration": analysis.get("duration", 60),
            "style": analysis.get("style", "professional"),
            "tone": analysis.get("tone", "educational"),
            "key_messages": analysis.get("key_messages", []),
            "language": "fr"
        }
    )

    result = asyncio.run(agent.execute(task))

    return {
        "project_id": project_id,
        "analysis": analysis,
        "script": result.output_data.get("script", {}),
        "status": "script_generated"
    }


@shared_task(bind=True)
def generate_assets_parallel(self, previous_result: Dict[str, Any]) -> Dict[str, Any]:
    """Generate all assets in parallel (images, voice, music)."""
    project_id = previous_result.get("project_id")
    script = previous_result.get("script", {})

    logger.info(f"Generating assets for project {project_id}")

    # Create parallel tasks for asset generation
    scenes = script.get("scenes", [])

    asset_tasks = group(
        generate_images.s(project_id, scenes),
        generate_voiceover.s(project_id, scenes),
        generate_music.s(project_id, script),
    )

    # Execute in parallel
    result = asset_tasks.apply_async()
    assets_results = result.get(timeout=600)  # 10 min timeout

    return {
        "project_id": project_id,
        "script": script,
        "assets": {
            "images": assets_results[0],
            "voiceover": assets_results[1],
            "music": assets_results[2],
        },
        "status": "assets_generated"
    }


@shared_task(bind=True)
def generate_images(self, project_id: str, scenes: list) -> list:
    """Generate images for all scenes."""
    from app.agents.image_agent import ImageAgent
    from app.agents.base import AgentTask
    import asyncio

    logger.info(f"Generating {len(scenes)} images for project {project_id}")

    agent = ImageAgent()
    prompts = [scene.get("visual_prompt", "") for scene in scenes]

    task = AgentTask(
        task_type="generate_batch",
        input_data={"prompts": prompts, "provider": "dalle", "size": "1024x1024"}
    )

    result = asyncio.run(agent.execute(task))
    return result.output_data.get("images", [])


@shared_task(bind=True)
def generate_voiceover(self, project_id: str, scenes: list) -> list:
    """Generate voiceover for all scenes."""
    from app.agents.voice_agent import VoiceAgent
    from app.agents.base import AgentTask
    import asyncio

    logger.info(f"Generating voiceover for project {project_id}")

    agent = VoiceAgent()
    audio_files = []

    for scene in scenes:
        narration = scene.get("narration", "")
        if narration:
            task = AgentTask(
                task_type="text_to_speech",
                input_data={
                    "text": narration,
                    "provider": "elevenlabs",
                    "language": "fr"
                }
            )
            result = asyncio.run(agent.execute(task))
            audio_files.append(result.output_data.get("audio", {}))

    return audio_files


@shared_task(bind=True)
def generate_music(self, project_id: str, script: dict) -> dict:
    """Generate background music."""
    from app.agents.voice_agent import VoiceAgent
    from app.agents.base import AgentTask
    import asyncio

    logger.info(f"Generating music for project {project_id}")

    agent = VoiceAgent()
    duration = script.get("total_duration", 60)

    task = AgentTask(
        task_type="generate_music",
        input_data={
            "prompt": "background music for video",
            "duration": min(duration, 120),
            "provider": "suno",
            "instrumental": True
        }
    )

    result = asyncio.run(agent.execute(task))
    return result.output_data.get("music", {})


@shared_task(bind=True)
def montage_video(self, previous_result: Dict[str, Any]) -> Dict[str, Any]:
    """Assemble all assets into final video."""
    from app.agents.montage_agent import MontageAgent
    from app.agents.base import AgentTask
    import asyncio

    project_id = previous_result.get("project_id")
    assets = previous_result.get("assets", {})
    script = previous_result.get("script", {})

    logger.info(f"Creating montage for project {project_id}")

    agent = MontageAgent()

    # Create timeline
    clips = []
    for i, scene in enumerate(script.get("scenes", [])):
        if i < len(assets.get("images", [])):
            clips.append({
                "id": f"clip_{i}",
                "path": assets["images"][i].get("local_path"),
                "duration": scene.get("duration", 5)
            })

    timeline_task = AgentTask(
        task_type="assemble_timeline",
        input_data={
            "clips": clips,
            "audio_tracks": assets.get("voiceover", []),
            "music_track": assets.get("music"),
            "format": "youtube"
        }
    )

    timeline_result = asyncio.run(agent.execute(timeline_task))
    timeline = timeline_result.output_data.get("timeline", {})

    # Add transitions
    transitions_task = AgentTask(
        task_type="add_transitions",
        input_data={"timeline": timeline, "default_transition": "crossfade"}
    )
    asyncio.run(agent.execute(transitions_task))

    # Render
    render_task = AgentTask(
        task_type="render_video",
        input_data={"timeline": timeline, "format": "youtube", "quality": "high"}
    )

    render_result = asyncio.run(agent.execute(render_task))

    return {
        "project_id": project_id,
        "video": render_result.output_data.get("video", {}),
        "status": "video_rendered"
    }


@shared_task(bind=True)
def quality_check(self, previous_result: Dict[str, Any]) -> Dict[str, Any]:
    """Perform quality check on rendered video."""
    from app.agents.orchestrator import OrchestratorAgent
    from app.agents.base import AgentTask
    import asyncio

    project_id = previous_result.get("project_id")
    video = previous_result.get("video", {})

    logger.info(f"Quality check for project {project_id}")

    agent = OrchestratorAgent()
    task = AgentTask(
        task_type="quality_check",
        input_data={"video_id": video.get("video_id")}
    )

    result = asyncio.run(agent.execute(task))
    quality_report = result.output_data.get("quality_report", {})

    return {
        "project_id": project_id,
        "video": video,
        "quality_report": quality_report,
        "status": "quality_checked"
    }


@shared_task(bind=True)
def publish_video(self, previous_result: Dict[str, Any]) -> Dict[str, Any]:
    """Publish video to configured platforms."""
    from app.agents.publish_agent import PublishAgent
    from app.agents.base import AgentTask
    import asyncio

    project_id = previous_result.get("project_id")
    video = previous_result.get("video", {})

    logger.info(f"Publishing video for project {project_id}")

    # TODO: Get target platforms from project config
    platforms = ["youtube"]

    agent = PublishAgent()
    task = AgentTask(
        task_type="batch_publish",
        input_data={
            "video_path": video.get("output_path"),
            "platforms": platforms,
            "auto_optimize": True,
            "metadata": {
                "title": f"Video {project_id}",
                "description": "Generated with IAFactory Video Platform"
            }
        }
    )

    result = asyncio.run(agent.execute(task))

    return {
        "project_id": project_id,
        "video": video,
        "publish_results": result.output_data,
        "status": "published"
    }


@shared_task
def cleanup_old_files():
    """Periodic task to clean up old temporary files."""
    import os
    import time
    from pathlib import Path

    storage_path = Path("/app/storage/tmp")
    if not storage_path.exists():
        return {"cleaned": 0}

    max_age = 86400 * 7  # 7 days
    current_time = time.time()
    cleaned = 0

    for file_path in storage_path.glob("**/*"):
        if file_path.is_file():
            file_age = current_time - file_path.stat().st_mtime
            if file_age > max_age:
                file_path.unlink()
                cleaned += 1

    logger.info(f"Cleaned {cleaned} old files")
    return {"cleaned": cleaned}
