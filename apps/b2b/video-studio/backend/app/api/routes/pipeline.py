"""
Pipeline API routes for long video production
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
import uuid
import math
import asyncio
import os
import structlog

from app.core.config import settings
from app.agents import LLMProvider
from app.services.replicate_service import ReplicateService
from app.services.elevenlabs_service import ElevenLabsService
from app.services.fal_service import FalService
from app.services.minimax_service import MiniMaxService
from app.services.suno_service import SunoService, MusicStyle
from app.services.ffmpeg_service import FFmpegService, VideoSegment, AudioTrack, Subtitle, AssemblyConfig

router = APIRouter()
logger = structlog.get_logger()

# In-memory storage for pipelines (use Redis in production)
pipelines_db: dict = {}
projects_db: dict = {}


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


class ProjectStatus(str, Enum):
    DRAFT = "draft"
    STORYBOARDING = "storyboarding"
    STORYBOARDED = "storyboarded"
    ASSEMBLING = "assembling"
    ASSEMBLED = "assembled"
    RENDERING = "rendering"
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


class ProjectScene(BaseModel):
    id: int
    order: int
    duration: int = 5
    script: Optional[str] = None
    visual_prompt: Optional[str] = None
    status: SegmentStatus = SegmentStatus.PENDING
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


class CreateProjectRequest(BaseModel):
    prompt: str = Field(..., min_length=10, description="Main prompt for the video")
    target_duration: int = Field(30, ge=15, le=120, description="Target duration in seconds")
    model_id: str = Field("wan-2.1", description="Model ID to use")
    music_preset_id: Optional[str] = None
    narration_lang: Optional[str] = None
    enable_subtitles: bool = True


class ProjectResponse(BaseModel):
    id: str
    status: ProjectStatus
    prompt: str
    target_duration: int
    model_id: str
    music_preset_id: Optional[str]
    narration_lang: Optional[str]
    enable_subtitles: bool
    scenes: List[ProjectScene]
    final_video_url: Optional[str] = None
    error: Optional[str] = None


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


REPLICATE_MODELS = {
    "wan-2.1": "alibaba-pai/wan2.1-t2v-1.3b:c9c78a45f1848e7d1b89c5e8b028b98c89189c42fc6e386c8eb4ccb7478c1fd3",
    "cogvideox-2b": os.getenv("REPLICATE_COGVIDEOX_2B_MODEL", ""),
    "cogvideox-5b": "fofr/cogvideox-5b:8c5e35dddfed7efe4d0e4b11a9c23467ab44aa0c401a4835b96451d031417b72",
}

FAL_MODEL_IDS = {
    "kling-1.6",
    "kling-i2v",
    "minimax-fal",
    "luma",
}

MINIMAX_MODEL_ID = "minimax"


def _extract_json(content: str) -> dict:
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0]
    elif "```" in content:
        parts = content.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith("{") or part.startswith("["):
                content = part
                break
    content = content.strip()
    start = content.find("{")
    end = content.rfind("}") + 1
    if start >= 0 and end > start:
        content = content[start:end]
    return __import__("json").loads(content)


def _has_llm_keys() -> bool:
    return any(
        key and len(key) > 10
        for key in [
            os.getenv("GROQ_API_KEY"),
            os.getenv("DEEPSEEK_API_KEY"),
            os.getenv("OPENROUTER_API_KEY"),
        ]
    )


async def _run_replicate_text_to_video(prompt: str, model_id: str) -> str:
    replicate_model = REPLICATE_MODELS.get(model_id)
    if not replicate_model:
        raise Exception(f"Unsupported model_id: {model_id}")
    if not settings.REPLICATE_API_TOKEN:
        raise Exception("REPLICATE_API_TOKEN is not configured")

    service = ReplicateService()

    def _run():
        return service.client.run(
            replicate_model,
            input={
                "prompt": prompt,
                "num_frames": 81,
                "fps": 16,
                "guidance_scale": 5.0,
            },
        )

    output = await asyncio.to_thread(_run)
    if isinstance(output, list):
        return output[0]
    if isinstance(output, str):
        return output
    if isinstance(output, dict) and "video" in output:
        return output["video"]
    raise Exception("Unexpected Replicate output format")


async def _run_fal_text_to_video(prompt: str, model_id: str, duration: int = 5) -> str:
    if not settings.FAL_KEY:
        raise Exception("FAL_KEY is not configured")
    service = FalService()
    fal_model = model_id
    if model_id == "minimax-fal":
        fal_model = "minimax"
    result = await service.text_to_video(
        prompt=prompt,
        duration=str(duration),
        model=fal_model,
    )
    video_url = result.get("video_url")
    if not video_url:
        raise Exception("Fal did not return a video_url")
    return video_url


async def _run_minimax_text_to_video(prompt: str, duration: int = 5) -> str:
    if not settings.MINIMAX_API_KEY or not settings.MINIMAX_GROUP_ID:
        raise Exception("MINIMAX_API_KEY or MINIMAX_GROUP_ID is not configured")
    service = MiniMaxService(api_key=settings.MINIMAX_API_KEY, group_id=settings.MINIMAX_GROUP_ID)
    start = await service.text_to_video(prompt=prompt, duration=duration)
    if start.status.value == "failed":
        raise Exception(start.error or "MiniMax generation failed")
    for _ in range(60):
        status = await service.get_status(start.job_id)
        if status.status.value == "completed" and status.video_url:
            return status.video_url
        if status.status.value == "failed":
            raise Exception(status.error or "MiniMax generation failed")
        await asyncio.sleep(5)
    raise Exception("MiniMax generation timed out")


async def _generate_storyboard(prompt: str, scenes_count: int) -> List[dict]:
    if not _has_llm_keys():
        raise Exception("No LLM provider key configured (GROQ/DEEPSEEK/OPENROUTER)")

    system_prompt = (
        "Tu es un storyboarder pro. Tu dois retourner un JSON valide uniquement."
    )
    user_prompt = f"""
Génère un storyboard en {scenes_count} scènes de 5 secondes chacune.
Sujet principal: {prompt}
Contraintes:
- Chaque scène doit avoir: id, duration, script, visual_prompt, camera, transition.
- Le script doit être court et naturel.
- Le visual_prompt doit être détaillé et exploitable par une IA vidéo.
Réponds UNIQUEMENT avec un JSON au format:
{{
  "scenes": [
    {{
      "id": 1,
      "duration": 5,
      "script": "...",
      "visual_prompt": "...",
      "camera": "static|pan|zoom|tracking",
      "transition": "cut|fade|dissolve"
    }}
  ]
}}
"""
    content, _ = await LLMProvider.call(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=0.6,
        max_tokens=2000,
    )
    data = _extract_json(content)
    scenes = data.get("scenes", [])
    if not isinstance(scenes, list) or len(scenes) == 0:
        raise Exception("Invalid storyboard response")
    return scenes[:scenes_count]


async def process_pipeline(pipeline_id: str):
    """Background task to process the pipeline"""
    pipeline = pipelines_db.get(pipeline_id)
    if not pipeline:
        return

    try:
        # Step 1: Script generation
        pipeline["status"] = PipelineStatus.SCRIPTING
        pipeline["current_step"] = 1
        
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
            async def _gen(seg):
                try:
                    url = await _run_replicate_text_to_video(
                        seg.get("prompt") or pipeline["prompt"],
                        pipeline["model_id"],
                    )
                    seg["status"] = SegmentStatus.COMPLETED
                    seg["progress"] = 100
                    seg["video_url"] = url
                except Exception as e:
                    seg["status"] = SegmentStatus.ERROR
                    seg["error"] = str(e)

            await asyncio.gather(*[_gen(seg) for seg in batch])

            completed = sum(1 for s in segments if s["status"] == SegmentStatus.COMPLETED)
            pipeline["progress"] = min(90, (completed / len(segments)) * 60)
        
        # Step 3: Audio
        pipeline["status"] = PipelineStatus.AUDIO
        pipeline["current_step"] = 3
        if pipeline.get("narration_lang") and settings.ELEVENLABS_API_KEY:
            tts = ElevenLabsService()
            tts_result = await tts.generate_speech(
                text=pipeline["script"] or pipeline["prompt"],
                voice_id="darija_female_1" if pipeline["narration_lang"] == "darija" else "french_female_1",
                language=pipeline["narration_lang"],
            )
            pipeline["audio_url"] = tts_result.get("audio_url")
        
        # Step 4: Montage
        pipeline["status"] = PipelineStatus.MONTAGE
        pipeline["current_step"] = 4
        os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
        work_dir = os.path.join(settings.OUTPUT_DIR, f"work-{pipeline_id}")
        ffmpeg = FFmpegService(work_dir=work_dir)

        video_segments: List[VideoSegment] = []
        current_time = 0
        for seg in segments:
            if seg.get("status") == SegmentStatus.COMPLETED and seg.get("video_url"):
                video_segments.append(
                    VideoSegment(
                        url=seg["video_url"],
                        start_time=current_time,
                        duration=5,
                        shot_id=seg["id"],
                    )
                )
                current_time += 5

        audio_tracks: List[AudioTrack] = []
        if pipeline.get("audio_url"):
            audio_tracks.append(AudioTrack(url=pipeline["audio_url"], volume=1.0, is_music=False))

        subtitles: List[Subtitle] = []
        if pipeline.get("enable_subtitles"):
            current_time = 0
            for seg in segments:
                text = seg.get("prompt") or ""
                if text:
                    subtitles.append(
                        Subtitle(
                            text=text[:120],
                            start_time=current_time,
                            end_time=current_time + 5,
                        )
                    )
                current_time += 5

        output_path = os.path.join(settings.OUTPUT_DIR, f"final-{pipeline_id}.mp4")
        assembly_config = AssemblyConfig(
            output_path=output_path,
            resolution="1280x720",
            fps=24,
            crf=23,
            preset="medium",
        )

        if not video_segments:
            raise Exception("No completed video segments to assemble")

        result = await ffmpeg.full_assembly(
            segments=video_segments,
            audio_tracks=audio_tracks,
            subtitles=subtitles,
            output_path=output_path,
            config=assembly_config,
        )
        if not result.get("success"):
            raise Exception(result.get("error", "FFmpeg assembly failed"))
        
        # Step 5: Completed
        pipeline["status"] = PipelineStatus.COMPLETED
        pipeline["current_step"] = 5
        pipeline["final_video_url"] = f"/outputs/final-{pipeline_id}.mp4"
        pipeline["progress"] = 100
        
    except Exception as e:
        logger.error("Pipeline failed", pipeline_id=pipeline_id, error=str(e))
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


def _project_to_response(project: dict) -> ProjectResponse:
    return ProjectResponse(
        id=project["id"],
        status=project["status"],
        prompt=project["prompt"],
        target_duration=project["target_duration"],
        model_id=project["model_id"],
        music_preset_id=project.get("music_preset_id"),
        narration_lang=project.get("narration_lang"),
        enable_subtitles=project.get("enable_subtitles", True),
        scenes=[ProjectScene(**scene) for scene in project.get("scenes", [])],
        final_video_url=project.get("final_video_url"),
        error=project.get("error"),
    )


@router.post("/projects", response_model=ProjectResponse)
async def create_project(request: CreateProjectRequest):
    """Create a new pipeline project (manual steps)"""
    scenes_count = max(1, math.ceil(request.target_duration / 5))
    scenes = [
        ProjectScene(id=i + 1, order=i + 1, duration=5).model_dump()
        for i in range(scenes_count)
    ]
    project_id = str(uuid.uuid4())[:8]
    project = {
        "id": project_id,
        "status": ProjectStatus.DRAFT,
        "prompt": request.prompt,
        "target_duration": request.target_duration,
        "model_id": request.model_id,
        "music_preset_id": request.music_preset_id,
        "narration_lang": request.narration_lang,
        "enable_subtitles": request.enable_subtitles,
        "scenes": scenes,
        "final_video_url": None,
        "error": None,
    }
    projects_db[project_id] = project
    return _project_to_response(project)


@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str):
    project = projects_db.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return _project_to_response(project)


@router.post("/projects/{project_id}/storyboard", response_model=ProjectResponse)
async def storyboard_project(project_id: str):
    project = projects_db.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project["status"] = ProjectStatus.STORYBOARDING
    try:
        scenes_count = len(project.get("scenes", [])) or max(1, math.ceil(project["target_duration"] / 5))
        scenes = await _generate_storyboard(project["prompt"], scenes_count)
        normalized = []
        for i, scene in enumerate(scenes, 1):
            normalized.append(
                ProjectScene(
                    id=i,
                    order=i,
                    duration=int(scene.get("duration", 5)),
                    script=scene.get("script"),
                    visual_prompt=scene.get("visual_prompt"),
                    status=SegmentStatus.PENDING,
                ).model_dump()
            )
        project["scenes"] = normalized
        project["status"] = ProjectStatus.STORYBOARDED
        project["error"] = None
    except Exception as e:
        project["status"] = ProjectStatus.ERROR
        project["error"] = str(e)
    return _project_to_response(project)


@router.post("/projects/{project_id}/assemble", response_model=ProjectResponse)
async def assemble_project(project_id: str):
    project = projects_db.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if not project.get("scenes"):
        raise HTTPException(status_code=400, detail="Storyboard missing")

    project["status"] = ProjectStatus.ASSEMBLING
    model_id = project["model_id"]
    scenes = project["scenes"]

    async def _gen(scene: dict):
        scene["status"] = SegmentStatus.GENERATING
        try:
            prompt = scene.get("visual_prompt") or scene.get("script") or project["prompt"]
            if model_id in REPLICATE_MODELS:
                url = await _run_replicate_text_to_video(prompt, model_id)
            elif model_id in FAL_MODEL_IDS:
                url = await _run_fal_text_to_video(prompt, model_id, duration=int(scene.get("duration", 5)))
            elif model_id == MINIMAX_MODEL_ID:
                url = await _run_minimax_text_to_video(prompt, duration=int(scene.get("duration", 5)))
            else:
                raise Exception(f"Unsupported model_id: {model_id}")
            scene["video_url"] = url
            scene["status"] = SegmentStatus.COMPLETED
        except Exception as e:
            scene["status"] = SegmentStatus.ERROR
            scene["error"] = str(e)

    batch_size = 3
    for i in range(0, len(scenes), batch_size):
        await asyncio.gather(*[_gen(scene) for scene in scenes[i:i + batch_size]])

    if any(scene["status"] == SegmentStatus.ERROR for scene in scenes):
        project["status"] = ProjectStatus.ERROR
        project["error"] = "One or more scenes failed to generate"
    else:
        project["status"] = ProjectStatus.ASSEMBLED
        project["error"] = None

    return _project_to_response(project)


@router.post("/projects/{project_id}/render", response_model=ProjectResponse)
async def render_project(project_id: str):
    project = projects_db.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    scenes = project.get("scenes", [])
    if not scenes or any(not s.get("video_url") for s in scenes):
        raise HTTPException(status_code=400, detail="Scenes missing or not assembled")

    project["status"] = ProjectStatus.RENDERING
    project["error"] = None

    try:
        os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
        work_dir = os.path.join(settings.OUTPUT_DIR, f"project-{project_id}")
        ffmpeg = FFmpegService(work_dir=work_dir)

        video_segments: List[VideoSegment] = []
        current_time = 0
        for scene in scenes:
            video_segments.append(
                VideoSegment(
                    url=scene["video_url"],
                    start_time=current_time,
                    duration=int(scene.get("duration", 5)),
                    shot_id=scene.get("id"),
                )
            )
            current_time += int(scene.get("duration", 5))

        audio_tracks: List[AudioTrack] = []
        if project.get("narration_lang"):
            if not settings.ELEVENLABS_API_KEY:
                raise Exception("ELEVENLABS_API_KEY is not configured")
            tts = ElevenLabsService()
            script_text = "\n".join([s.get("script") or "" for s in scenes]).strip()
            tts_result = await tts.generate_speech(text=script_text or project["prompt"])
            audio_url = tts_result.get("audio_url")
            if not audio_url:
                raise Exception("Narration generation failed")
            audio_tracks.append(AudioTrack(url=audio_url, volume=1.0, is_music=False))

        if project.get("music_preset_id"):
            if not settings.SUNO_API_KEY:
                raise Exception("SUNO_API_KEY is not configured")
            music_style_map = {
                "epic-cinematic": MusicStyle.CINEMATIC,
                "upbeat-corporate": MusicStyle.CORPORATE,
                "ambient-chill": MusicStyle.AMBIENT,
                "arabic-traditional": MusicStyle.ARABIC,
                "electronic-modern": MusicStyle.ELECTRONIC,
                "motivational": MusicStyle.MOTIVATIONAL,
            }
            style = music_style_map.get(project["music_preset_id"], MusicStyle.CINEMATIC)
            suno = SunoService(api_key=settings.SUNO_API_KEY)
            start = await suno.generate_music(
                prompt=project["prompt"],
                style=style,
                duration=int(project["target_duration"]),
                instrumental=True,
            )
            if start.status.value == "failed":
                raise Exception(start.error or "Suno generation failed")
            music_url = None
            for _ in range(60):
                status = await suno.get_status(start.job_id)
                if status.status.value == "completed" and status.audio_url:
                    music_url = status.audio_url
                    break
                if status.status.value == "failed":
                    raise Exception(status.error or "Suno generation failed")
                await asyncio.sleep(5)
            if not music_url:
                raise Exception("Suno generation timed out")
            audio_tracks.append(AudioTrack(url=music_url, volume=0.6, is_music=True))

        subtitles: List[Subtitle] = []
        if project.get("enable_subtitles"):
            current_time = 0
            for scene in scenes:
                text = (scene.get("script") or "").strip()
                if text:
                    subtitles.append(
                        Subtitle(
                            text=text[:120],
                            start_time=current_time,
                            end_time=current_time + int(scene.get("duration", 5)),
                        )
                    )
                current_time += int(scene.get("duration", 5))

        output_path = os.path.join(settings.OUTPUT_DIR, f"project-{project_id}.mp4")
        assembly_config = AssemblyConfig(
            output_path=output_path,
            resolution="1280x720",
            fps=24,
            crf=23,
            preset="medium",
        )

        result = await ffmpeg.full_assembly(
            segments=video_segments,
            audio_tracks=audio_tracks,
            subtitles=subtitles,
            output_path=output_path,
            config=assembly_config,
        )
        if not result.get("success"):
            raise Exception(result.get("error", "FFmpeg assembly failed"))

        project["status"] = ProjectStatus.COMPLETED
        project["final_video_url"] = f"/outputs/project-{project_id}.mp4"
    except Exception as e:
        project["status"] = ProjectStatus.ERROR
        project["error"] = str(e)

    return _project_to_response(project)


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
