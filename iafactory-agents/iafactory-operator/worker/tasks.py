"""
IA Factory Operator - Worker Tasks
Background tasks for video processing
"""

import os
import tempfile
import traceback
from datetime import datetime
from typing import Dict, Any

import structlog
import httpx

from core.config import settings
from core.state import VideoEditorState
from core.models import JobStatusEnum, VideoOutput, PlatformEnum
from services import (
    get_queue_service,
    get_storage_client,
    get_llm_client,
    get_whisper_client,
)
from pipeline.analyzer import analyze_video
from pipeline.planner import plan_edits
from pipeline.executor import execute_edits

logger = structlog.get_logger(__name__)


async def process_video_job(state_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main video processing task.
    Runs the full pipeline: download -> analyze -> plan -> execute -> upload
    """
    job_id = state_dict.get("job_id", "unknown")
    logger.info(f"Processing job: {job_id}")
    
    queue = get_queue_service()
    storage = get_storage_client()
    
    # Reconstruct state
    state = VideoEditorState(
        job_id=job_id,
        source_video_url=state_dict.get("source_video_url", ""),
        template=state_dict.get("template", "algerian_minimal"),
        target_duration=state_dict.get("target_duration", 15),
        platforms=state_dict.get("platforms", ["instagram_reels"]),
        style=state_dict.get("style", "default"),
        language=state_dict.get("language", "fr"),
        add_captions=state_dict.get("add_captions", True),
        add_music=state_dict.get("add_music", False),
        voiceover_text=state_dict.get("voiceover_text"),
        webhook_url=state_dict.get("webhook_url"),
    )
    
    state.started_at = datetime.utcnow()
    state.status = JobStatusEnum.downloading.value
    
    try:
        # Create work directory
        work_dir = tempfile.mkdtemp(prefix=f"iafactory_{job_id}_")
        state.work_dir = work_dir
        
        # 1. DOWNLOAD
        state.add_log("📥 Downloading source video...")
        state.set_status("downloading", progress=5, stage="download")
        _update_job_result(queue, state)
        
        state.source_video_path = await storage.download_video(
            state.source_video_url,
            work_dir=work_dir,
        )
        state.add_log(f"✅ Downloaded: {state.source_video_path}")
        
        # 2. ANALYZE
        whisper_client = get_whisper_client() if state.add_captions else None
        state = await analyze_video(state, whisper_client=whisper_client)
        _update_job_result(queue, state)
        
        # 3. PLAN
        llm_client = get_llm_client()
        state = await plan_edits(state, llm_client=llm_client)
        _update_job_result(queue, state)
        
        # 4. EXECUTE
        state = await execute_edits(state, storage_client=storage)
        _update_job_result(queue, state)
        
        # 5. UPLOAD
        state.add_log("☁️ Uploading outputs...")
        state.set_status("uploading", progress=96, stage="upload")
        _update_job_result(queue, state)
        
        for platform, local_path in state.output_files.items():
            if os.path.exists(local_path):
                url = await storage.upload_video(
                    local_path,
                    key=f"outputs/{job_id}/{platform}.mp4",
                )
                state.output_urls[platform] = url
                state.add_log(f"✅ Uploaded {platform}: {url}")
        
        # 6. COMPLETE
        state.completed_at = datetime.utcnow()
        state.processing_time = (state.completed_at - state.started_at).total_seconds()
        state.set_status("completed", progress=100, stage="done")
        state.add_log(f"🎉 Job complete! Processing time: {state.processing_time:.1f}s")
        
        # Build final result
        result = _build_result(state)
        queue.store_result(job_id, result)
        
        # Send webhook if configured
        if state.webhook_url:
            await _send_webhook(state, result)
        
        # Cleanup
        _cleanup_work_dir(work_dir)
        
        return result
        
    except Exception as e:
        logger.exception(f"Job {job_id} failed", error=str(e))
        
        state.error = str(e)
        state.set_status("failed", progress=0)
        state.add_log(f"❌ Error: {str(e)}")
        
        result = _build_result(state)
        result["error"] = str(e)
        result["traceback"] = traceback.format_exc()
        queue.store_result(job_id, result)
        
        # Send failure webhook
        if state.webhook_url:
            await _send_webhook(state, result)
        
        raise


def _update_job_result(queue, state: VideoEditorState):
    """Update job result in Redis"""
    queue.update_progress(
        state.job_id,
        progress=state.progress,
        stage=state.current_stage,
        message=state.logs[-1] if state.logs else "",
    )
    
    result = _build_result(state)
    queue.store_result(state.job_id, result)


def _build_result(state: VideoEditorState) -> Dict[str, Any]:
    """Build result dictionary from state"""
    outputs = []
    for platform, url in state.output_urls.items():
        outputs.append({
            "platform": platform,
            "duration": state.target_duration,
            "aspect_ratio": "9:16" if platform != "square" else "1:1",
            "width": 1080,
            "height": 1920 if platform != "square" else 1080,
            "video_url": url,
            "thumbnail_url": state.thumbnail_urls.get(platform),
        })
    
    return {
        "job_id": state.job_id,
        "status": state.status,
        "progress": state.progress,
        "created_at": state.created_at.isoformat() if state.created_at else None,
        "updated_at": datetime.utcnow().isoformat(),
        "started_at": state.started_at.isoformat() if state.started_at else None,
        "completed_at": state.completed_at.isoformat() if state.completed_at else None,
        "input": {
            "source_video_url": state.source_video_url,
            "template": state.template,
            "target_duration": state.target_duration,
            "platforms": state.platforms,
            "style": state.style,
            "language": state.language,
            "add_captions": state.add_captions,
            "add_music": state.add_music,
        },
        "outputs": outputs,
        "transcript": state.analysis.full_transcript if state.analysis else None,
        "scenes_detected": state.analysis.total_scenes if state.analysis else 0,
        "logs": state.logs,
        "error": state.error,
        "processing_time_seconds": state.processing_time,
    }


async def _send_webhook(state: VideoEditorState, result: Dict[str, Any]):
    """Send webhook notification"""
    if not state.webhook_url:
        return
    
    try:
        payload = {
            "event": "video.job.completed" if state.status == "completed" else "video.job.failed",
            "job_id": state.job_id,
            "status": state.status,
            "outputs": result.get("outputs", []),
            "error": state.error,
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                state.webhook_url,
                json=payload,
                timeout=30.0,
            )
            logger.info(f"Webhook sent: {response.status_code}")
            
    except Exception as e:
        logger.warning(f"Webhook failed: {e}")


def _cleanup_work_dir(work_dir: str):
    """Clean up temporary work directory"""
    import shutil
    
    try:
        if work_dir and os.path.exists(work_dir):
            shutil.rmtree(work_dir)
            logger.debug(f"Cleaned up work dir: {work_dir}")
    except Exception as e:
        logger.warning(f"Cleanup failed: {e}")
