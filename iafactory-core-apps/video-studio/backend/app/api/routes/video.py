from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
import uuid
from datetime import datetime
import structlog

from app.schemas import (
    VideoGenerateRequest,
    VideoGenerateResponse,
    VideoStatusResponse,
    ProjectResponse,
)
from app.services.fal_service import FalService

router = APIRouter()
logger = structlog.get_logger()

# In-memory storage for demo (use Redis/DB in production)
video_tasks = {}

fal_service = FalService()


@router.post("/generate", response_model=VideoGenerateResponse)
async def generate_video(
    request: VideoGenerateRequest,
    background_tasks: BackgroundTasks,
):
    """Start video generation task"""
    task_id = str(uuid.uuid4())
    
    # Estimate credits
    credits = 10 if request.duration == 5 else 20
    if request.aspect_ratio != "16:9":
        credits = int(credits * 1.2)
    
    # Create task
    video_tasks[task_id] = {
        "id": task_id,
        "status": "pending",
        "progress": 0,
        "prompt": request.prompt,
        "mode": request.mode,
        "duration": request.duration,
        "aspect_ratio": request.aspect_ratio,
        "created_at": datetime.utcnow(),
        "video_url": None,
        "error": None,
    }
    
    # Start background generation
    background_tasks.add_task(
        process_video_generation,
        task_id,
        request,
    )
    
    logger.info("Video generation started", task_id=task_id, mode=request.mode)
    
    return VideoGenerateResponse(
        task_id=task_id,
        estimated_time=120 if request.duration == 5 else 240,
        credits=credits,
    )


async def process_video_generation(task_id: str, request: VideoGenerateRequest):
    """Process video generation in background"""
    try:
        video_tasks[task_id]["status"] = "processing"
        video_tasks[task_id]["progress"] = 10
        
        # Call Fal.ai
        if request.mode == "text-to-video":
            result = await fal_service.text_to_video(
                prompt=request.prompt,
                duration=str(request.duration),
                aspect_ratio=request.aspect_ratio,
                model=request.model,
            )
        else:
            result = await fal_service.image_to_video(
                image_url=request.image_url,
                prompt=request.prompt,
                duration=str(request.duration),
                aspect_ratio=request.aspect_ratio,
            )
        
        video_tasks[task_id]["status"] = "completed"
        video_tasks[task_id]["progress"] = 100
        video_tasks[task_id]["video_url"] = result["video_url"]
        video_tasks[task_id]["completed_at"] = datetime.utcnow()
        
        logger.info("Video generation completed", task_id=task_id)
        
    except Exception as e:
        logger.error("Video generation failed", task_id=task_id, error=str(e))
        video_tasks[task_id]["status"] = "failed"
        video_tasks[task_id]["error"] = str(e)


@router.get("/status/{task_id}", response_model=VideoStatusResponse)
async def get_video_status(task_id: str):
    """Get video generation status"""
    if task_id not in video_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = video_tasks[task_id]
    return VideoStatusResponse(
        task_id=task_id,
        status=task["status"],
        progress=task["progress"],
        video_url=task.get("video_url"),
        error=task.get("error"),
        created_at=task["created_at"],
        completed_at=task.get("completed_at"),
    )


@router.get("/projects", response_model=List[ProjectResponse])
async def list_projects():
    """List all video projects for the user"""
    projects = []
    for task_id, task in video_tasks.items():
        projects.append(ProjectResponse(
            id=task_id,
            name=task["prompt"][:50] + "..." if len(task["prompt"]) > 50 else task["prompt"],
            prompt=task["prompt"],
            mode=task["mode"],
            status=task["status"],
            video_url=task.get("video_url"),
            thumbnail_url=None,
            duration=task["duration"],
            aspect_ratio=task["aspect_ratio"],
            credits_used=10,
            created_at=task["created_at"],
        ))
    return projects


@router.delete("/projects/{project_id}")
async def delete_project(project_id: str):
    """Delete a video project"""
    if project_id not in video_tasks:
        raise HTTPException(status_code=404, detail="Project not found")
    
    del video_tasks[project_id]
    return {"message": "Project deleted"}
