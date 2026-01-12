"""
Scripts API endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID

router = APIRouter()


class SceneSchema(BaseModel):
    """Schéma d'une scène"""
    scene_id: str
    order: int
    duration: float
    type: str  # intro, content, transition, outro
    narration: str
    visual_prompt: str
    music_mood: str
    text_overlay: Optional[str] = None
    speaker: str = "narrator"
    camera_movement: str = "static"


class ScriptCreate(BaseModel):
    """Créer un script manuellement"""
    project_id: UUID
    title: str
    synopsis: Optional[str] = None
    scenes: List[SceneSchema]


class ScriptResponse(BaseModel):
    """Réponse script"""
    id: UUID
    project_id: UUID
    title: str
    synopsis: Optional[str]
    scenes: List[SceneSchema]
    total_duration: int
    version: int
    is_approved: bool


class ScriptGenerateRequest(BaseModel):
    """Demande de génération automatique"""
    topic: str = Field(..., description="Sujet de la vidéo")
    duration: int = Field(default=60, description="Durée cible en secondes")
    style: str = Field(default="professional")
    tone: str = Field(default="educational")
    key_messages: List[str] = Field(default=[])
    language: str = Field(default="fr")


class ScriptEditRequest(BaseModel):
    """Demande d'édition de script"""
    instructions: str = Field(..., description="Instructions d'édition en langage naturel")


@router.post("/generate", response_model=ScriptResponse)
async def generate_script(request: ScriptGenerateRequest):
    """
    Génère un script automatiquement à partir des paramètres.

    L'agent Script analyse les paramètres et génère:
    - Structure complète avec scènes
    - Narration pour chaque scène
    - Prompts visuels optimisés
    - Timeline calculée
    """
    from app.agents.script_agent import ScriptAgent
    from app.agents.base import AgentTask
    import uuid

    agent = ScriptAgent()
    task = AgentTask(
        task_type="generate_script",
        input_data=request.model_dump()
    )

    result = await agent.execute(task)

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error_message)

    script_data = result.output_data.get("script", {})

    return ScriptResponse(
        id=uuid.uuid4(),
        project_id=uuid.uuid4(),
        title=script_data.get("title", "Generated Script"),
        synopsis=script_data.get("synopsis"),
        scenes=[SceneSchema(**s) for s in script_data.get("scenes", [])],
        total_duration=script_data.get("total_duration", 0),
        version=1,
        is_approved=False
    )


@router.get("/{script_id}", response_model=ScriptResponse)
async def get_script(script_id: UUID):
    """Récupère un script par ID"""
    raise HTTPException(status_code=404, detail="Script not found")


@router.put("/{script_id}")
async def update_script(script_id: UUID, script: ScriptCreate):
    """Met à jour un script"""
    return {"updated": True, "script_id": str(script_id)}


@router.post("/{script_id}/edit")
async def edit_script_with_ai(script_id: UUID, request: ScriptEditRequest):
    """
    Édite le script avec l'aide de l'IA.

    Exemples d'instructions:
    - "Rends l'intro plus dynamique"
    - "Ajoute une scène sur les avantages"
    - "Raccourcis les scènes de transition"
    """
    # TODO: Récupérer le script, appeler l'agent, sauvegarder
    return {
        "script_id": str(script_id),
        "status": "edited",
        "instructions": request.instructions
    }


@router.post("/{script_id}/approve")
async def approve_script(script_id: UUID):
    """Approuve le script pour passer à la génération"""
    return {"script_id": str(script_id), "approved": True}


@router.post("/{script_id}/regenerate")
async def regenerate_script(script_id: UUID, keep_scenes: List[str] = None):
    """
    Régénère le script en gardant optionnellement certaines scènes.
    """
    return {
        "script_id": str(script_id),
        "status": "regenerating",
        "kept_scenes": keep_scenes or []
    }


@router.get("/{script_id}/visual-prompts")
async def get_visual_prompts(script_id: UUID, provider: str = "dalle"):
    """
    Génère des prompts visuels optimisés pour le provider d'images choisi.
    """
    from app.agents.script_agent import ScriptAgent
    from app.agents.base import AgentTask

    # TODO: Récupérer les scènes du script depuis DB
    scenes = []

    agent = ScriptAgent()
    task = AgentTask(
        task_type="generate_visual_prompts",
        input_data={
            "scenes": scenes,
            "image_provider": provider
        }
    )

    result = await agent.execute(task)

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error_message)

    return result.output_data


@router.post("/{script_id}/translate")
async def translate_script(script_id: UUID, target_language: str = "en"):
    """Traduit le script dans une autre langue"""
    return {
        "script_id": str(script_id),
        "target_language": target_language,
        "status": "translating"
    }
