"""
Scripts API Routes - Génération et gestion des scripts
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from enum import Enum
import uuid
import structlog

from app.agents import (
    AgentTask, AgentRole, AgentStatus,
    ScriptwriterAgent, GrowthHackerAgent, create_agent
)

router = APIRouter()
logger = structlog.get_logger()

# In-memory storage (use Redis in production)
scripts_db: dict = {}


class ScriptLanguage(str, Enum):
    FR = "fr"
    AR = "ar"
    DARIJA = "darija"
    EN = "en"


class ScriptPlatform(str, Enum):
    YOUTUBE = "youtube"
    YOUTUBE_SHORTS = "youtube_shorts"
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    LINKEDIN = "linkedin"


class ScriptStyle(str, Enum):
    INFORMATIVE = "informative"
    ENTERTAINING = "entertaining"
    EDUCATIONAL = "educational"
    PROMOTIONAL = "promotional"
    STORYTELLING = "storytelling"


class GenerateScriptRequest(BaseModel):
    topic: str = Field(..., min_length=10, description="Sujet du script")
    platform: ScriptPlatform = ScriptPlatform.YOUTUBE
    language: ScriptLanguage = ScriptLanguage.FR
    duration: int = Field(60, ge=15, le=900, description="Durée en secondes")
    style: ScriptStyle = ScriptStyle.INFORMATIVE
    target_audience: Optional[str] = "18-35 ans"
    keywords: Optional[List[str]] = []
    include_optimization: bool = True


class ScriptSegment(BaseModel):
    id: int
    type: str
    duration: int
    script: str
    visual_prompt: str
    emotion: str


class ScriptResponse(BaseModel):
    id: str
    status: str
    title: Optional[str] = None
    hook: Optional[str] = None
    segments: List[ScriptSegment] = []
    metadata: Optional[dict] = None
    optimization: Optional[dict] = None
    tokens_used: int = 0
    error: Optional[str] = None


class UpdateScriptRequest(BaseModel):
    title: Optional[str] = None
    segments: Optional[List[dict]] = None
    metadata: Optional[dict] = None


class ExtractShortsRequest(BaseModel):
    count: int = Field(3, ge=1, le=10, description="Nombre de shorts à extraire")
    duration: int = Field(30, ge=15, le=60, description="Durée max par short")


async def generate_script_task(script_id: str, request: GenerateScriptRequest):
    """Background task pour générer un script."""
    try:
        # Créer l'agent scénariste
        scriptwriter = ScriptwriterAgent()
        
        task = AgentTask(
            task_id=script_id,
            role=AgentRole.SCRIPTWRITER,
            input_data={
                "topic": request.topic,
                "platform": request.platform.value,
                "language": request.language.value,
                "duration": request.duration,
                "style": request.style.value,
                "target_audience": request.target_audience,
                "keywords": request.keywords
            }
        )
        
        # Générer le script
        result = await scriptwriter.execute(task)
        
        if result.status == AgentStatus.COMPLETED:
            script_data = result.output
            
            # Optimisation si demandée
            optimization = None
            if request.include_optimization:
                growth_hacker = GrowthHackerAgent()
                opt_task = AgentTask(
                    task_id=f"{script_id}_opt",
                    role=AgentRole.GROWTH_HACKER,
                    input_data={
                        "script": script_data,
                        "topic": request.topic,
                        "platforms": [request.platform.value],
                        "target_audience": request.target_audience
                    }
                )
                opt_result = await growth_hacker.execute(opt_task)
                if opt_result.status == AgentStatus.COMPLETED:
                    optimization = opt_result.output
            
            # Sauvegarder
            scripts_db[script_id] = {
                "id": script_id,
                "status": "completed",
                "data": script_data,
                "optimization": optimization,
                "tokens_used": result.tokens_used,
                "request": request.model_dump()
            }
        else:
            scripts_db[script_id] = {
                "id": script_id,
                "status": "error",
                "error": result.error
            }
            
    except Exception as e:
        logger.error("Script generation error", script_id=script_id, error=str(e))
        scripts_db[script_id] = {
            "id": script_id,
            "status": "error",
            "error": str(e)
        }


@router.post("/generate", response_model=ScriptResponse)
async def generate_script(request: GenerateScriptRequest, background_tasks: BackgroundTasks):
    """
    Génère un script viral avec l'agent Scénariste.
    
    - **topic**: Sujet du script
    - **platform**: Plateforme cible (youtube, tiktok, instagram)
    - **language**: Langue (fr, ar, darija, en)
    - **duration**: Durée cible en secondes
    - **style**: Style du contenu
    """
    script_id = str(uuid.uuid4())[:8]
    
    # Initialiser dans la DB
    scripts_db[script_id] = {
        "id": script_id,
        "status": "generating",
        "request": request.model_dump()
    }
    
    # Lancer en background
    background_tasks.add_task(generate_script_task, script_id, request)
    
    logger.info(
        "Script generation started",
        script_id=script_id,
        topic=request.topic[:50],
        platform=request.platform.value
    )
    
    return ScriptResponse(
        id=script_id,
        status="generating"
    )


@router.get("/{script_id}", response_model=ScriptResponse)
async def get_script(script_id: str):
    """Récupère un script par son ID."""
    script = scripts_db.get(script_id)
    
    if not script:
        raise HTTPException(status_code=404, detail="Script not found")
    
    if script["status"] == "completed":
        data = script.get("data", {})
        segments = [
            ScriptSegment(**seg) for seg in data.get("segments", [])
        ]
        
        return ScriptResponse(
            id=script_id,
            status="completed",
            title=data.get("title"),
            hook=data.get("hook"),
            segments=segments,
            metadata=data.get("metadata"),
            optimization=script.get("optimization"),
            tokens_used=script.get("tokens_used", 0)
        )
    elif script["status"] == "error":
        return ScriptResponse(
            id=script_id,
            status="error",
            error=script.get("error")
        )
    else:
        return ScriptResponse(
            id=script_id,
            status=script["status"]
        )


@router.put("/{script_id}")
async def update_script(script_id: str, update: UpdateScriptRequest):
    """Met à jour un script existant."""
    script = scripts_db.get(script_id)
    
    if not script:
        raise HTTPException(status_code=404, detail="Script not found")
    
    if script["status"] != "completed":
        raise HTTPException(status_code=400, detail="Script not ready for editing")
    
    data = script.get("data", {})
    
    if update.title:
        data["title"] = update.title
    if update.segments:
        data["segments"] = update.segments
    if update.metadata:
        data["metadata"] = {**data.get("metadata", {}), **update.metadata}
    
    script["data"] = data
    scripts_db[script_id] = script
    
    return {"success": True, "message": "Script updated"}


@router.post("/{script_id}/approve")
async def approve_script(script_id: str):
    """Approuve un script pour la production."""
    script = scripts_db.get(script_id)
    
    if not script:
        raise HTTPException(status_code=404, detail="Script not found")
    
    script["approved"] = True
    script["status"] = "approved"
    scripts_db[script_id] = script
    
    return {
        "success": True,
        "message": "Script approved for production",
        "next_step": f"/api/v1/storyboard/generate?script_id={script_id}"
    }


@router.post("/{script_id}/extract-shorts")
async def extract_shorts(script_id: str, request: ExtractShortsRequest):
    """Extrait des Shorts à partir d'un script long."""
    script = scripts_db.get(script_id)
    
    if not script:
        raise HTTPException(status_code=404, detail="Script not found")
    
    data = script.get("data", {})
    segments = data.get("segments", [])
    
    if not segments:
        raise HTTPException(status_code=400, detail="No segments in script")
    
    # Identifier les meilleurs segments pour Shorts
    shorts = []
    current_short = []
    current_duration = 0
    
    for seg in segments:
        seg_duration = seg.get("duration", 5)
        
        if current_duration + seg_duration <= request.duration:
            current_short.append(seg)
            current_duration += seg_duration
        else:
            if current_short:
                shorts.append({
                    "segments": current_short,
                    "duration": current_duration,
                    "hook": current_short[0].get("script", "")[:50]
                })
            current_short = [seg]
            current_duration = seg_duration
        
        if len(shorts) >= request.count:
            break
    
    # Ajouter le dernier short
    if current_short and len(shorts) < request.count:
        shorts.append({
            "segments": current_short,
            "duration": current_duration,
            "hook": current_short[0].get("script", "")[:50]
        })
    
    return {
        "script_id": script_id,
        "shorts_count": len(shorts),
        "shorts": shorts[:request.count]
    }


@router.get("/")
async def list_scripts(
    status: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
):
    """Liste tous les scripts."""
    scripts = list(scripts_db.values())
    
    if status:
        scripts = [s for s in scripts if s.get("status") == status]
    
    return {
        "total": len(scripts),
        "scripts": scripts[offset:offset + limit]
    }
