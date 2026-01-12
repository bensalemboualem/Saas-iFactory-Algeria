"""
Agents API endpoints - Direct access to AI agents
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from uuid import UUID

router = APIRouter()


class AgentTaskRequest(BaseModel):
    """Demande d'exécution de tâche par un agent"""
    agent_type: str = Field(..., description="orchestrator, script, image, video, avatar, voice, montage, publish")
    task_type: str = Field(..., description="Type de tâche spécifique à l'agent")
    input_data: Dict[str, Any] = Field(default={})
    priority: int = Field(default=5, ge=1, le=10)


class AgentResponse(BaseModel):
    """Réponse d'une tâche d'agent"""
    task_id: str
    agent_type: str
    success: bool
    output_data: Dict[str, Any] = {}
    error_message: Optional[str] = None
    execution_time_ms: int
    cost_cents: int


@router.post("/execute", response_model=AgentResponse)
async def execute_agent_task(request: AgentTaskRequest):
    """
    Exécute une tâche directement sur un agent.

    Agents disponibles:
    - orchestrator: Chef d'orchestre du pipeline
    - script: Génération de scripts
    - image: Génération d'images
    - video: Génération de clips vidéo
    - avatar: Avatars parlants
    - voice: TTS, STT, musique
    - montage: Édition vidéo
    - publish: Publication multi-plateforme
    """
    from app.agents import (
        OrchestratorAgent, ScriptAgent, ImageAgent, VideoAgent,
        AvatarAgent, VoiceAgent, MontageAgent, PublishAgent
    )
    from app.agents.base import AgentTask

    # Mapping des agents
    agent_classes = {
        "orchestrator": OrchestratorAgent,
        "script": ScriptAgent,
        "image": ImageAgent,
        "video": VideoAgent,
        "avatar": AvatarAgent,
        "voice": VoiceAgent,
        "montage": MontageAgent,
        "publish": PublishAgent
    }

    agent_class = agent_classes.get(request.agent_type)
    if not agent_class:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown agent type: {request.agent_type}. Available: {list(agent_classes.keys())}"
        )

    agent = agent_class()

    # Vérifier que la tâche est supportée
    if request.task_type not in agent.capabilities:
        raise HTTPException(
            status_code=400,
            detail=f"Task '{request.task_type}' not supported by {request.agent_type} agent. Available: {agent.capabilities}"
        )

    task = AgentTask(
        task_type=request.task_type,
        input_data=request.input_data,
        priority=request.priority
    )

    result = await agent.execute(task)

    return AgentResponse(
        task_id=result.task_id,
        agent_type=request.agent_type,
        success=result.success,
        output_data=result.output_data,
        error_message=result.error_message,
        execution_time_ms=result.execution_time_ms,
        cost_cents=result.cost_cents
    )


@router.get("/")
async def list_agents():
    """Liste tous les agents et leurs capacités"""
    from app.agents import (
        OrchestratorAgent, ScriptAgent, ImageAgent, VideoAgent,
        AvatarAgent, VoiceAgent, MontageAgent, PublishAgent
    )

    agents = []
    for agent_class in [OrchestratorAgent, ScriptAgent, ImageAgent, VideoAgent,
                        AvatarAgent, VoiceAgent, MontageAgent, PublishAgent]:
        agent = agent_class()
        agents.append({
            "type": agent.agent_type,
            "capabilities": agent.capabilities,
            "status": agent.state.status
        })

    return {"agents": agents}


@router.get("/{agent_type}")
async def get_agent_info(agent_type: str):
    """Récupère les informations détaillées d'un agent"""
    from app.agents import (
        OrchestratorAgent, ScriptAgent, ImageAgent, VideoAgent,
        AvatarAgent, VoiceAgent, MontageAgent, PublishAgent
    )

    agent_classes = {
        "orchestrator": OrchestratorAgent,
        "script": ScriptAgent,
        "image": ImageAgent,
        "video": VideoAgent,
        "avatar": AvatarAgent,
        "voice": VoiceAgent,
        "montage": MontageAgent,
        "publish": PublishAgent
    }

    agent_class = agent_classes.get(agent_type)
    if not agent_class:
        raise HTTPException(status_code=404, detail="Agent not found")

    agent = agent_class()

    return {
        "type": agent.agent_type,
        "capabilities": agent.capabilities,
        "state": agent.state.model_dump()
    }


@router.get("/{agent_type}/health")
async def agent_health_check(agent_type: str):
    """Vérifie la santé d'un agent"""
    from app.agents import (
        OrchestratorAgent, ScriptAgent, ImageAgent, VideoAgent,
        AvatarAgent, VoiceAgent, MontageAgent, PublishAgent
    )

    agent_classes = {
        "orchestrator": OrchestratorAgent,
        "script": ScriptAgent,
        "image": ImageAgent,
        "video": VideoAgent,
        "avatar": AvatarAgent,
        "voice": VoiceAgent,
        "montage": MontageAgent,
        "publish": PublishAgent
    }

    agent_class = agent_classes.get(agent_type)
    if not agent_class:
        raise HTTPException(status_code=404, detail="Agent not found")

    agent = agent_class()
    return await agent.health_check()


# === Orchestrator specific endpoints ===

@router.post("/orchestrator/pipeline")
async def run_full_pipeline(
    user_prompt: str,
    project_id: Optional[str] = None,
    language: str = "fr",
    auto_publish: bool = False
):
    """
    Lance le pipeline complet de création vidéo.

    Étapes:
    1. Analyse du prompt NLP
    2. Création du plan de projet
    3. Génération du script
    4. Génération des assets
    5. Montage vidéo
    6. Publication (si auto_publish=true)
    """
    from app.agents.orchestrator import OrchestratorAgent
    import uuid

    agent = OrchestratorAgent()
    result = await agent.run_full_pipeline(
        user_prompt=user_prompt,
        project_id=project_id or str(uuid.uuid4()),
        options={
            "language": language,
            "auto_publish": auto_publish
        }
    )

    return result


# === Provider-specific endpoints ===

@router.get("/image/providers")
async def list_image_providers():
    """Liste les providers d'images disponibles"""
    from app.agents.image_agent import ImageAgent

    return {
        "providers": list(ImageAgent.PROVIDER_COSTS.keys()),
        "costs": ImageAgent.PROVIDER_COSTS,
        "default": "dalle"
    }


@router.get("/video/providers")
async def list_video_providers():
    """Liste les providers de vidéos disponibles"""
    from app.agents.video_agent import VideoAgent

    return {
        "providers": list(VideoAgent.PROVIDER_COSTS.keys()),
        "costs": VideoAgent.PROVIDER_COSTS,
        "default": "runway"
    }


@router.get("/avatar/providers")
async def list_avatar_providers():
    """Liste les providers d'avatars disponibles"""
    from app.agents.avatar_agent import AvatarAgent

    return {
        "providers": list(AvatarAgent.PROVIDER_COSTS.keys()),
        "costs": AvatarAgent.PROVIDER_COSTS,
        "default_avatars": AvatarAgent.DEFAULT_AVATARS,
        "default": "heygen"
    }


@router.get("/voice/providers")
async def list_voice_providers():
    """Liste les providers de voix disponibles"""
    from app.agents.voice_agent import VoiceAgent

    return {
        "tts_providers": list(VoiceAgent.TTS_COSTS.keys()),
        "tts_costs": VoiceAgent.TTS_COSTS,
        "stt_providers": list(VoiceAgent.STT_COSTS.keys()),
        "stt_costs": VoiceAgent.STT_COSTS,
        "voices": VoiceAgent.VOICES,
        "default_tts": "elevenlabs",
        "default_stt": "whisper"
    }
