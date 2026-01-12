"""
Storyboard API Routes - Découpage et création de storyboards
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
import uuid
import structlog

from app.agents import AgentTask, AgentRole, AgentStatus, StoryboarderAgent

router = APIRouter()
logger = structlog.get_logger()

# In-memory storage
storyboards_db: dict = {}
scripts_db: dict = {}  # Reference to scripts


class ShotType(str, Enum):
    WIDE = "wide"
    MEDIUM = "medium"
    CLOSE_UP = "close-up"
    EXTREME_CLOSE_UP = "extreme_close_up"
    OVERHEAD = "overhead"
    LOW_ANGLE = "low_angle"
    POV = "pov"
    TRACKING = "tracking"


class TransitionType(str, Enum):
    CUT = "cut"
    FADE = "fade"
    DISSOLVE = "dissolve"
    WIPE = "wipe"
    ZOOM = "zoom"
    SLIDE = "slide"


class GenerateStoryboardRequest(BaseModel):
    script_id: Optional[str] = None
    script_data: Optional[dict] = None
    style: str = Field("cinematic", description="Style visuel")
    aspect_ratio: str = Field("16:9", description="Ratio d'aspect")


class Shot(BaseModel):
    id: int
    segment_id: int
    duration: float
    shot_type: str
    description: str
    visual_prompt: str
    camera_movement: str
    transition: str
    audio_cue: Optional[str] = None


class StoryboardResponse(BaseModel):
    id: str
    status: str
    shots: List[Shot] = []
    total_duration: float = 0
    metadata: Optional[dict] = None
    tokens_used: int = 0
    error: Optional[str] = None


# ===== STATIC ROUTES FIRST =====

@router.get("/")
async def list_storyboards(limit: int = 20, offset: int = 0):
    """Liste tous les storyboards."""
    storyboards = list(storyboards_db.values())
    
    return {
        "total": len(storyboards),
        "storyboards": storyboards[offset:offset + limit]
    }


@router.get("/shot-types")
async def get_shot_types():
    """Liste tous les types de plans disponibles."""
    return {
        "shot_types": [
            {"id": "wide", "name": "Plan Large", "description": "Vue d'ensemble de la scène"},
            {"id": "medium", "name": "Plan Moyen", "description": "Cadrage à mi-corps"},
            {"id": "close-up", "name": "Gros Plan", "description": "Focus sur le visage ou détail"},
            {"id": "extreme_close_up", "name": "Très Gros Plan", "description": "Détail extrême"},
            {"id": "overhead", "name": "Vue Aérienne", "description": "Vue du dessus"},
            {"id": "low_angle", "name": "Contre-Plongée", "description": "Vue du bas vers le haut"},
            {"id": "pov", "name": "POV", "description": "Point de vue subjectif"},
            {"id": "tracking", "name": "Travelling", "description": "Mouvement de caméra"}
        ]
    }


@router.get("/transitions")
async def get_transitions():
    """Liste toutes les transitions disponibles."""
    return {
        "transitions": [
            {"id": "cut", "name": "Coupe Franche", "duration": 0},
            {"id": "fade", "name": "Fondu", "duration": 0.5},
            {"id": "dissolve", "name": "Fondu Enchaîné", "duration": 1.0},
            {"id": "wipe", "name": "Volet", "duration": 0.5},
            {"id": "zoom", "name": "Zoom Transition", "duration": 0.3},
            {"id": "slide", "name": "Glissement", "duration": 0.5}
        ]
    }


# ===== HELPER FUNCTIONS =====

async def generate_storyboard_task(storyboard_id: str, script_data: dict, style: str, aspect_ratio: str):
    """Background task pour générer un storyboard."""
    try:
        storyboarder = StoryboarderAgent()
        
        task = AgentTask(
            task_id=storyboard_id,
            role=AgentRole.STORYBOARDER,
            input_data={
                "script": script_data,
                "style": style,
                "aspect_ratio": aspect_ratio
            }
        )
        
        result = await storyboarder.execute(task)
        
        if result.status == AgentStatus.COMPLETED:
            storyboards_db[storyboard_id] = {
                "id": storyboard_id,
                "status": "completed",
                "data": result.output,
                "tokens_used": result.tokens_used
            }
        else:
            storyboards_db[storyboard_id] = {
                "id": storyboard_id,
                "status": "error",
                "error": result.error
            }
            
    except Exception as e:
        logger.error("Storyboard generation error", storyboard_id=storyboard_id, error=str(e))
        storyboards_db[storyboard_id] = {
            "id": storyboard_id,
            "status": "error",
            "error": str(e)
        }


@router.post("/generate", response_model=StoryboardResponse)
async def generate_storyboard(
    request: GenerateStoryboardRequest,
    background_tasks: BackgroundTasks
):
    """
    Génère un storyboard à partir d'un script.
    
    Peut recevoir soit:
    - script_id: ID d'un script existant
    - script_data: Données du script directement
    """
    storyboard_id = str(uuid.uuid4())[:8]
    
    # Récupérer les données du script
    if request.script_id:
        script = scripts_db.get(request.script_id)
        if not script:
            raise HTTPException(status_code=404, detail="Script not found")
        script_data = script.get("data", {})
    elif request.script_data:
        script_data = request.script_data
    else:
        raise HTTPException(status_code=400, detail="Provide script_id or script_data")
    
    # Initialiser dans la DB
    storyboards_db[storyboard_id] = {
        "id": storyboard_id,
        "status": "generating",
        "script_id": request.script_id
    }
    
    # Lancer en background
    background_tasks.add_task(
        generate_storyboard_task,
        storyboard_id,
        script_data,
        request.style,
        request.aspect_ratio
    )
    
    logger.info(
        "Storyboard generation started",
        storyboard_id=storyboard_id,
        script_id=request.script_id
    )
    
    return StoryboardResponse(
        id=storyboard_id,
        status="generating"
    )


@router.get("/{storyboard_id}", response_model=StoryboardResponse)
async def get_storyboard(storyboard_id: str):
    """Récupère un storyboard par son ID."""
    storyboard = storyboards_db.get(storyboard_id)
    
    if not storyboard:
        raise HTTPException(status_code=404, detail="Storyboard not found")
    
    if storyboard["status"] == "completed":
        data = storyboard.get("data", {})
        shots = [Shot(**shot) for shot in data.get("shots", [])]
        
        return StoryboardResponse(
            id=storyboard_id,
            status="completed",
            shots=shots,
            total_duration=data.get("total_duration", 0),
            metadata=data.get("metadata"),
            tokens_used=storyboard.get("tokens_used", 0)
        )
    elif storyboard["status"] == "error":
        return StoryboardResponse(
            id=storyboard_id,
            status="error",
            error=storyboard.get("error")
        )
    else:
        return StoryboardResponse(
            id=storyboard_id,
            status=storyboard["status"]
        )


@router.put("/{storyboard_id}/shots/{shot_id}")
async def update_shot(storyboard_id: str, shot_id: int, shot: dict):
    """Met à jour un plan spécifique."""
    storyboard = storyboards_db.get(storyboard_id)
    
    if not storyboard:
        raise HTTPException(status_code=404, detail="Storyboard not found")
    
    data = storyboard.get("data", {})
    shots = data.get("shots", [])
    
    for i, s in enumerate(shots):
        if s.get("id") == shot_id:
            shots[i] = {**s, **shot}
            break
    else:
        raise HTTPException(status_code=404, detail="Shot not found")
    
    data["shots"] = shots
    storyboard["data"] = data
    storyboards_db[storyboard_id] = storyboard
    
    return {"success": True, "message": f"Shot {shot_id} updated"}


@router.post("/{storyboard_id}/approve")
async def approve_storyboard(storyboard_id: str):
    """Approuve un storyboard pour la production."""
    storyboard = storyboards_db.get(storyboard_id)
    
    if not storyboard:
        raise HTTPException(status_code=404, detail="Storyboard not found")
    
    storyboard["approved"] = True
    storyboard["status"] = "approved"
    storyboards_db[storyboard_id] = storyboard
    
    return {
        "success": True,
        "message": "Storyboard approved for production",
        "next_step": f"/api/v1/production/assemble?storyboard_id={storyboard_id}"
    }
