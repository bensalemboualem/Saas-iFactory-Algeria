"""
Pipeline API routes for long video production
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
import uuid
import asyncio

router = APIRouter()

# In-memory storage for pipelines (use Redis in production)
pipelines_db: dict = {}


class PipelineStatus(str, Enum):
    IDLE = "idle"
    SCRIPTING = "scripting"
    GENERATING = "generating"
    AUDIO = "audio"
    MONTAGE = "montage"
    COMPLETED = "completed"
    ERROR = "error"


class SegmentStatus(str, Enum):
    PENDING = "pending"
    GENERATING = "generating"
    COMPLETED = "completed"
    ERROR = "error"


class FreeModel(BaseModel):
    id: str
    name: str
    vram: str
    duration: int
    credits: int
    quality: int
    available: bool


class MusicPreset(BaseModel):
    id: str
    name: str
    genre: str
    duration: int
    url: Optional[str] = None


class SoundEffect(BaseModel):
    id: str
    name: str
    category: str
    duration: float
    url: Optional[str] = None


class PipelineSegment(BaseModel):
    id: int
    prompt: str
    status: SegmentStatus = SegmentStatus.PENDING
    progress: float = 0
    video_url: Optional[str] = None
    error: Optional[str] = None


class CreatePipelineRequest(BaseModel):
    prompt: str = Field(..., min_length=10, description="Main prompt for the video")
    target_duration: int = Field(30, ge=15, le=120, description="Target duration in seconds")
    model_id: str = Field("wan-2.1", description="Model ID to use")
    music_preset_id: Optional[str] = None
    narration_lang: Optional[str] = None
    enable_subtitles: bool = True


class PipelineResponse(BaseModel):
    id: str
    status: PipelineStatus
    current_step: int
    total_steps: int = 5
    segments: List[PipelineSegment]
    script: Optional[str] = None
    audio_url: Optional[str] = None
    final_video_url: Optional[str] = None
    error: Optional[str] = None
    progress: float = 0


# Free models data
FREE_MODELS = [
    FreeModel(id="wan-2.1", name="Wan 2.1", vram="8GB", duration=5, credits=0, quality=4, available=True),
    FreeModel(id="cogvideox-2b", name="CogVideoX 2B", vram="8GB", duration=6, credits=0, quality=3, available=True),
    FreeModel(id="cogvideox-5b", name="CogVideoX 5B", vram="12GB", duration=6, credits=2, quality=4, available=False),
    FreeModel(id="ltx-video-2", name="LTX Video 2", vram="12GB", duration=5, credits=2, quality=4, available=False),
    FreeModel(id="hunyuan-video", name="HunyuanVideo", vram="16GB", duration=5, credits=3, quality=5, available=False),
]

# Music presets
MUSIC_PRESETS = [
    MusicPreset(id="epic-cinematic", name="Epic Cinematic", genre="Cinematic", duration=60),
    MusicPreset(id="upbeat-corporate", name="Upbeat Corporate", genre="Corporate", duration=45),
    MusicPreset(id="ambient-chill", name="Ambient Chill", genre="Ambient", duration=90),
    MusicPreset(id="arabic-traditional", name="Arabic Traditional", genre="World", duration=60),
    MusicPreset(id="electronic-modern", name="Electronic Modern", genre="Electronic", duration=45),
    MusicPreset(id="motivational", name="Motivational", genre="Inspirational", duration=60),
]

# Sound effects
SOUND_EFFECTS = [
    SoundEffect(id="whoosh-1", name="Whoosh", category="Transition", duration=0.5),
    SoundEffect(id="swoosh-1", name="Swoosh", category="Transition", duration=0.3),
    SoundEffect(id="impact-1", name="Impact Hit", category="Impact", duration=0.4),
    SoundEffect(id="click-1", name="UI Click", category="UI", duration=0.1),
    SoundEffect(id="success-1", name="Success Chime", category="Notification", duration=1.0),
    SoundEffect(id="ambient-city", name="City Ambience", category="Ambient", duration=30.0),
    SoundEffect(id="ambient-nature", name="Nature Sounds", category="Ambient", duration=30.0),
]


def generate_segment_prompts(main_prompt: str, count: int) -> List[str]:
    """Generate segment-specific prompts from main prompt"""
    templates = [
        f"Opening shot: {main_prompt} - establishing wide angle view, cinematic lighting",
        f"Detail shot: {main_prompt} - focusing on key elements, shallow depth of field",
        f"Movement: {main_prompt} - dynamic camera motion, smooth tracking",
        f"Close-up: {main_prompt} - intimate details, macro perspective",
        f"Transition: {main_prompt} - shifting perspective, creative angle",
        f"Atmosphere: {main_prompt} - environmental mood, ambient scene",
        f"Action: {main_prompt} - dynamic movement, energetic pace",
        f"Climax: {main_prompt} - dramatic moment, peak intensity",
        f"Resolution: {main_prompt} - concluding scene, final statement",
    ]
    return templates[:count]


async def process_pipeline(pipeline_id: str):
    """Background task to process the pipeline"""
    pipeline = pipelines_db.get(pipeline_id)
    if not pipeline:
        return

    try:
        # Step 1: Script generation
        pipeline["status"] = PipelineStatus.SCRIPTING
        pipeline["current_step"] = 1
        await asyncio.sleep(2)  # Simulate script generation
        
        # Generate segment prompts
        prompts = generate_segment_prompts(pipeline["prompt"], len(pipeline["segments"]))
        for i, prompt in enumerate(prompts):
            if i < len(pipeline["segments"]):
                pipeline["segments"][i]["prompt"] = prompt
        
        pipeline["script"] = "\n\n".join(prompts)
        
        # Step 2: Generate segments
        pipeline["status"] = PipelineStatus.GENERATING
        pipeline["current_step"] = 2
        
        # Process in batches of 3
        batch_size = 3
        segments = pipeline["segments"]
        
        for i in range(0, len(segments), batch_size):
            batch = segments[i:i + batch_size]
            
            # Mark batch as generating
            for seg in batch:
                seg["status"] = SegmentStatus.GENERATING
            
            # Simulate generation
            for progress in range(0, 101, 10):
                await asyncio.sleep(0.3)
                for seg in batch:
                    seg["progress"] = progress
            
            # Mark batch as completed
            for j, seg in enumerate(batch):
                seg["status"] = SegmentStatus.COMPLETED
                seg["progress"] = 100
                seg["video_url"] = f"/outputs/segment-{i + j + 1}.mp4"
        
        # Step 3: Audio
        pipeline["status"] = PipelineStatus.AUDIO
        pipeline["current_step"] = 3
        await asyncio.sleep(2)
        pipeline["audio_url"] = "/outputs/narration.mp3"
        
        # Step 4: Montage
        pipeline["status"] = PipelineStatus.MONTAGE
        pipeline["current_step"] = 4
        await asyncio.sleep(3)
        
        # Step 5: Completed
        pipeline["status"] = PipelineStatus.COMPLETED
        pipeline["current_step"] = 5
        pipeline["final_video_url"] = f"/outputs/final-{pipeline_id}.mp4"
        pipeline["progress"] = 100
        
    except Exception as e:
        pipeline["status"] = PipelineStatus.ERROR
        pipeline["error"] = str(e)


@router.get("/free-models", response_model=List[FreeModel])
async def get_free_models():
    """Get list of available free models for local GPU"""
    return FREE_MODELS


@router.get("/music/presets", response_model=List[MusicPreset])
async def get_music_presets():
    """Get list of music presets"""
    return MUSIC_PRESETS


@router.get("/sound-effects", response_model=List[SoundEffect])
async def get_sound_effects():
    """Get list of sound effects"""
    return SOUND_EFFECTS


@router.post("/create", response_model=PipelineResponse)
async def create_pipeline(request: CreatePipelineRequest, background_tasks: BackgroundTasks):
    """Create a new video production pipeline"""
    
    # Calculate segments
    segments_count = max(1, request.target_duration // 5)
    
    # Create segments
    segments = [
        PipelineSegment(id=i + 1, prompt="")
        for i in range(segments_count)
    ]
    
    # Create pipeline
    pipeline_id = str(uuid.uuid4())[:8]
    pipeline = {
        "id": pipeline_id,
        "status": PipelineStatus.IDLE,
        "current_step": 0,
        "total_steps": 5,
        "segments": [seg.model_dump() for seg in segments],
        "prompt": request.prompt,
        "model_id": request.model_id,
        "music_preset_id": request.music_preset_id,
        "narration_lang": request.narration_lang,
        "enable_subtitles": request.enable_subtitles,
        "script": None,
        "audio_url": None,
        "final_video_url": None,
        "error": None,
        "progress": 0,
    }
    
    pipelines_db[pipeline_id] = pipeline
    
    # Start processing in background
    background_tasks.add_task(process_pipeline, pipeline_id)
    
    return PipelineResponse(
        id=pipeline_id,
        status=PipelineStatus.IDLE,
        current_step=0,
        total_steps=5,
        segments=segments,
    )


@router.get("/status/{pipeline_id}", response_model=PipelineResponse)
async def get_pipeline_status(pipeline_id: str):
    """Get pipeline status and progress"""
    
    pipeline = pipelines_db.get(pipeline_id)
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    
    # Calculate overall progress
    if pipeline["status"] == PipelineStatus.COMPLETED:
        progress = 100
    elif pipeline["status"] == PipelineStatus.ERROR:
        progress = 0
    else:
        completed_segments = sum(
            1 for seg in pipeline["segments"] 
            if seg["status"] == SegmentStatus.COMPLETED
        )
        segment_progress = (completed_segments / len(pipeline["segments"])) * 60  # 60% for segments
        step_progress = (pipeline["current_step"] / 5) * 40  # 40% for other steps
        progress = min(99, segment_progress + step_progress)
    
    return PipelineResponse(
        id=pipeline["id"],
        status=pipeline["status"],
        current_step=pipeline["current_step"],
        total_steps=pipeline["total_steps"],
        segments=[PipelineSegment(**seg) for seg in pipeline["segments"]],
        script=pipeline.get("script"),
        audio_url=pipeline.get("audio_url"),
        final_video_url=pipeline.get("final_video_url"),
        error=pipeline.get("error"),
        progress=progress,
    )


@router.delete("/{pipeline_id}")
async def cancel_pipeline(pipeline_id: str):
    """Cancel and delete a pipeline"""
    
    if pipeline_id in pipelines_db:
        del pipelines_db[pipeline_id]
        return {"success": True, "message": "Pipeline cancelled"}
    
    raise HTTPException(status_code=404, detail="Pipeline not found")


@router.post("/music/generate")
async def generate_music(
    genre: str = "cinematic",
    duration: int = 30,
    mood: str = "uplifting"
):
    """Generate AI music (placeholder - integrate with Suno/MusicGen)"""
    return {
        "success": True,
        "message": "Music generation started",
        "job_id": str(uuid.uuid4())[:8],
        "estimated_time": duration * 0.5,
    }
