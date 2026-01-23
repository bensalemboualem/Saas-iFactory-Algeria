"""
Production API Routes - Assemblage vidéo et génération
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
import uuid
import asyncio
import os
import structlog

from app.agents import AgentTask, AgentRole, AgentStatus, DirectorAgent
from app.services.minimax_service import MiniMaxService, MiniMaxVideoRequest
from app.services.suno_service import SunoService, SunoMusicRequest, MusicStyle
from app.services.ffmpeg_service import FFmpegService, VideoSegment, AudioTrack, Subtitle, AssemblyConfig

router = APIRouter()
logger = structlog.get_logger()

# In-memory storage
productions_db: dict = {}
storyboards_db: dict = {}  # Reference


class ProductionQuality(str, Enum):
    DRAFT = "draft"  # 480p, fast
    STANDARD = "standard"  # 720p
    HIGH = "high"  # 1080p
    ULTRA = "ultra"  # 4K


class ProductionStatus(str, Enum):
    PENDING = "pending"
    GENERATING_ASSETS = "generating_assets"
    GENERATING_VIDEO = "generating_video"
    GENERATING_AUDIO = "generating_audio"
    ASSEMBLING = "assembling"
    COMPLETED = "completed"
    ERROR = "error"


class AssembleRequest(BaseModel):
    storyboard_id: Optional[str] = None
    storyboard_data: Optional[dict] = None
    quality: ProductionQuality = ProductionQuality.STANDARD
    add_music: bool = True
    music_style: MusicStyle = MusicStyle.CINEMATIC
    add_narration: bool = True
    narration_voice: str = "alloy"
    add_subtitles: bool = True
    output_format: str = "mp4"


class AssetStatus(BaseModel):
    id: str
    type: str  # video, audio, music
    status: str
    url: Optional[str] = None
    error: Optional[str] = None


class ProductionResponse(BaseModel):
    id: str
    status: str
    progress: float = 0
    current_step: Optional[str] = None
    assets: List[AssetStatus] = []
    output_url: Optional[str] = None
    timeline: Optional[dict] = None
    tokens_used: int = 0
    error: Optional[str] = None


# ===== STATIC ROUTES FIRST =====

@router.get("/")
async def list_productions(
    status: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
):
    """Liste toutes les productions."""
    productions = list(productions_db.values())
    
    if status:
        productions = [p for p in productions if p.get("status") == status]
    
    return {
        "total": len(productions),
        "productions": productions[offset:offset + limit]
    }


@router.get("/quality-presets")
async def get_quality_presets():
    """Retourne les préréglages de qualité."""
    return {
        "presets": [
            {
                "id": "draft",
                "name": "Brouillon",
                "resolution": "480p",
                "fps": 24,
                "bitrate": "1M",
                "estimated_time_multiplier": 0.5
            },
            {
                "id": "standard",
                "name": "Standard",
                "resolution": "720p",
                "fps": 30,
                "bitrate": "5M",
                "estimated_time_multiplier": 1.0
            },
            {
                "id": "high",
                "name": "Haute Qualité",
                "resolution": "1080p",
                "fps": 30,
                "bitrate": "10M",
                "estimated_time_multiplier": 2.0
            },
            {
                "id": "ultra",
                "name": "Ultra HD",
                "resolution": "4K",
                "fps": 60,
                "bitrate": "20M",
                "estimated_time_multiplier": 4.0
            }
        ]
    }


@router.get("/output-formats")
async def get_output_formats():
    """Retourne les formats de sortie disponibles."""
    return {
        "formats": [
            {"id": "mp4", "name": "MP4", "codec": "H.264", "compatible": ["youtube", "instagram", "tiktok"]},
            {"id": "webm", "name": "WebM", "codec": "VP9", "compatible": ["web"]},
            {"id": "mov", "name": "MOV", "codec": "ProRes", "compatible": ["professional"]},
            {"id": "gif", "name": "GIF", "codec": "GIF", "compatible": ["social_preview"]}
        ]
    }


# ===== HELPER FUNCTIONS =====

async def generate_video_segment(shot: dict, index: int) -> dict:
    """Génère un segment vidéo pour un plan."""
    try:
        service = MiniMaxService()
        request = MiniMaxVideoRequest(
            prompt=shot.get("visual_prompt", shot.get("description", "")),
            duration=int(shot.get("duration", 5)),
            resolution="1280x720",
            style="cinematic"
        )
        
        result = await service.text_to_video(request)
        
        # Attendre la completion (simplified)
        for _ in range(60):  # 5 min max
            status = await service.get_status(result.task_id)
            if status.status == "completed":
                return {
                    "id": f"seg_{index}",
                    "type": "video",
                    "status": "completed",
                    "url": status.video_url,
                    "shot_id": shot.get("id")
                }
            elif status.status == "error":
                return {
                    "id": f"seg_{index}",
                    "type": "video",
                    "status": "error",
                    "error": status.error,
                    "shot_id": shot.get("id")
                }
            await asyncio.sleep(5)
        
        return {
            "id": f"seg_{index}",
            "type": "video",
            "status": "timeout",
            "shot_id": shot.get("id")
        }
        
    except Exception as e:
        return {
            "id": f"seg_{index}",
            "type": "video",
            "status": "error",
            "error": str(e),
            "shot_id": shot.get("id")
        }


async def generate_music(style: MusicStyle, duration: int) -> dict:
    """Génère la musique de fond."""
    try:
        service = SunoService()
        request = SunoMusicRequest(
            style=style,
            duration=duration,
            instrumental=True
        )
        
        result = await service.generate_music(request)
        
        return {
            "id": "music_0",
            "type": "music",
            "status": "completed",
            "url": result.get("audio_url"),
            "task_id": result.get("task_id")
        }
        
    except Exception as e:
        return {
            "id": "music_0",
            "type": "music",
            "status": "error",
            "error": str(e)
        }


async def production_task(
    production_id: str,
    storyboard_data: dict,
    config: AssembleRequest
):
    """Background task pour la production complète avec FFmpeg."""
    try:
        shots = storyboard_data.get("shots", [])
        total_duration = storyboard_data.get("total_duration", 60)
        
        assets = []
        ffmpeg = FFmpegService(work_dir=f"/tmp/video-studio/{production_id}")
        
        # Étape 1: Générer les segments vidéo
        productions_db[production_id]["status"] = ProductionStatus.GENERATING_VIDEO.value
        productions_db[production_id]["current_step"] = "Génération des segments vidéo"
        
        video_tasks = [
            generate_video_segment(shot, i)
            for i, shot in enumerate(shots[:10])  # Limit to 10 shots
        ]
        video_results = await asyncio.gather(*video_tasks)
        assets.extend(video_results)
        
        productions_db[production_id]["progress"] = 0.4
        productions_db[production_id]["assets"] = assets
        
        # Étape 2: Générer la musique
        music_url = None
        if config.add_music:
            productions_db[production_id]["status"] = ProductionStatus.GENERATING_AUDIO.value
            productions_db[production_id]["current_step"] = "Génération de la musique"
            
            music_result = await generate_music(config.music_style, total_duration)
            assets.append(music_result)
            if music_result.get("status") == "completed":
                music_url = music_result.get("url")
            
            productions_db[production_id]["progress"] = 0.6
            productions_db[production_id]["assets"] = assets
        
        # Étape 3: Assembler avec FFmpeg
        productions_db[production_id]["status"] = ProductionStatus.ASSEMBLING.value
        productions_db[production_id]["current_step"] = "Assemblage FFmpeg en cours"
        
        # Préparer les segments vidéo
        video_segments = []
        current_time = 0
        for asset in video_results:
            if asset.get("status") == "completed" and asset.get("url"):
                duration = 5  # Default duration per segment
                video_segments.append(VideoSegment(
                    url=asset["url"],
                    start_time=current_time,
                    duration=duration,
                    shot_id=asset.get("shot_id")
                ))
                current_time += duration
        
        # Préparer les pistes audio
        audio_tracks = []
        if music_url:
            audio_tracks.append(AudioTrack(
                url=music_url,
                volume=0.3,  # Musique en fond
                is_music=True
            ))
        
        # Préparer les sous-titres depuis le storyboard
        subtitles = []
        if config.add_subtitles:
            current_time = 0
            for shot in shots:
                text = shot.get("description", "") or shot.get("visual_prompt", "")
                duration = shot.get("duration", 5)
                if text:
                    subtitles.append(Subtitle(
                        text=text[:100],  # Limiter la longueur
                        start_time=current_time,
                        end_time=current_time + duration
                    ))
                current_time += duration
        
        # Définir la qualité
        quality_settings = {
            "draft": {"resolution": "854x480", "crf": 28, "preset": "ultrafast"},
            "standard": {"resolution": "1280x720", "crf": 23, "preset": "medium"},
            "high": {"resolution": "1920x1080", "crf": 20, "preset": "slow"},
            "ultra": {"resolution": "3840x2160", "crf": 18, "preset": "slow"}
        }
        settings = quality_settings.get(config.quality.value, quality_settings["standard"])
        
        output_path = f"/tmp/video-studio/output/{production_id}.{config.output_format}"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        assembly_config = AssemblyConfig(
            output_path=output_path,
            resolution=settings["resolution"],
            crf=settings["crf"],
            preset=settings["preset"]
        )
        
        # Lancer l'assemblage FFmpeg
        if video_segments:
            result = await ffmpeg.full_assembly(
                segments=video_segments,
                audio_tracks=audio_tracks,
                subtitles=subtitles,
                output_path=output_path,
                config=assembly_config
            )
            
            if result.get("success"):
                productions_db[production_id] = {
                    "id": production_id,
                    "status": ProductionStatus.COMPLETED.value,
                    "progress": 1.0,
                    "current_step": "Terminé",
                    "assets": assets,
                    "output_url": f"/videos/{production_id}.{config.output_format}",
                    "timeline": {
                        "duration": result.get("duration"),
                        "file_size_mb": result.get("file_size_mb"),
                        "resolution": settings["resolution"]
                    },
                    "tokens_used": 0
                }
                logger.info("Production completed with FFmpeg", 
                           production_id=production_id,
                           duration=result.get("duration"),
                           size_mb=result.get("file_size_mb"))
            else:
                raise Exception(result.get("error", "FFmpeg assembly failed"))
        else:
            # Fallback: utiliser DirectorAgent si pas de vidéos
            director = DirectorAgent()
            task = AgentTask(
                task_id=production_id,
                role=AgentRole.DIRECTOR,
                input_data={
                    "storyboard": storyboard_data,
                    "assets": assets,
                    "output_format": config.output_format,
                    "quality": config.quality.value,
                    "add_subtitles": config.add_subtitles
                }
            )
            
            result = await director.execute(task)
            
            if result.status == AgentStatus.COMPLETED:
                productions_db[production_id] = {
                    "id": production_id,
                    "status": ProductionStatus.COMPLETED.value,
                    "progress": 1.0,
                    "current_step": "Terminé",
                    "assets": assets,
                    "timeline": result.output,
                    "tokens_used": result.tokens_used
                }
            else:
                productions_db[production_id]["status"] = ProductionStatus.ERROR.value
                productions_db[production_id]["error"] = result.error
            
    except Exception as e:
        logger.error("Production error", production_id=production_id, error=str(e))
        productions_db[production_id] = {
            "id": production_id,
            "status": ProductionStatus.ERROR.value,
            "error": str(e)
        }


@router.post("/assemble", response_model=ProductionResponse)
async def assemble_production(
    request: AssembleRequest,
    background_tasks: BackgroundTasks
):
    """
    Lance l'assemblage d'une production vidéo complète.
    
    Workflow:
    1. Génération des segments vidéo (MiniMax/Hailuo)
    2. Génération de la musique (Suno)
    3. Génération de la narration (ElevenLabs)
    4. Assemblage final avec DirectorAgent
    """
    production_id = str(uuid.uuid4())[:8]
    
    # Récupérer le storyboard
    if request.storyboard_id:
        storyboard = storyboards_db.get(request.storyboard_id)
        if not storyboard:
            raise HTTPException(status_code=404, detail="Storyboard not found")
        storyboard_data = storyboard.get("data", {})
    elif request.storyboard_data:
        storyboard_data = request.storyboard_data
    else:
        raise HTTPException(status_code=400, detail="Provide storyboard_id or storyboard_data")
    
    # Initialiser
    productions_db[production_id] = {
        "id": production_id,
        "status": ProductionStatus.PENDING.value,
        "progress": 0,
        "current_step": "Initialisation",
        "storyboard_id": request.storyboard_id,
        "config": request.model_dump()
    }
    
    # Lancer en background
    background_tasks.add_task(
        production_task,
        production_id,
        storyboard_data,
        request
    )
    
    logger.info(
        "Production started",
        production_id=production_id,
        quality=request.quality.value
    )
    
    return ProductionResponse(
        id=production_id,
        status=ProductionStatus.PENDING.value,
        progress=0,
        current_step="Initialisation"
    )


@router.get("/{production_id}", response_model=ProductionResponse)
async def get_production(production_id: str):
    """Récupère le statut d'une production."""
    production = productions_db.get(production_id)
    
    if not production:
        raise HTTPException(status_code=404, detail="Production not found")
    
    return ProductionResponse(
        id=production_id,
        status=production.get("status", "unknown"),
        progress=production.get("progress", 0),
        current_step=production.get("current_step"),
        assets=[AssetStatus(**a) for a in production.get("assets", [])],
        output_url=production.get("output_url"),
        timeline=production.get("timeline"),
        tokens_used=production.get("tokens_used", 0),
        error=production.get("error")
    )


@router.post("/{production_id}/cancel")
async def cancel_production(production_id: str):
    """Annule une production en cours."""
    production = productions_db.get(production_id)
    
    if not production:
        raise HTTPException(status_code=404, detail="Production not found")
    
    if production.get("status") == ProductionStatus.COMPLETED.value:
        raise HTTPException(status_code=400, detail="Production already completed")
    
    production["status"] = "cancelled"
    production["current_step"] = "Annulé par l'utilisateur"
    productions_db[production_id] = production
    
    return {"success": True, "message": "Production cancelled"}


@router.get("/{production_id}/download")
async def download_production(production_id: str, format: str = "mp4"):
    """Génère un lien de téléchargement pour la production."""
    production = productions_db.get(production_id)
    
    if not production:
        raise HTTPException(status_code=404, detail="Production not found")
    
    if production.get("status") != ProductionStatus.COMPLETED.value:
        raise HTTPException(status_code=400, detail="Production not ready")
    
    output_url = production.get("output_url")
    
    if not output_url:
        raise HTTPException(status_code=400, detail="Output not available")
    
    return {
        "download_url": output_url,
        "format": format,
        "expires_in": 3600
    }
