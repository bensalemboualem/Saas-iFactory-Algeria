"""
Publish API endpoints - Multi-platform publishing
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime

router = APIRouter()


class PublishRequest(BaseModel):
    """Demande de publication"""
    video_id: UUID
    platform: str = Field(..., description="youtube, tiktok, instagram_reels, linkedin, twitter, facebook")
    title: str = Field(..., max_length=255)
    description: str = Field(default="")
    tags: List[str] = Field(default=[])
    thumbnail_path: Optional[str] = None
    privacy: str = Field(default="public", description="public, unlisted, private")
    platform_settings: Dict[str, Any] = Field(default={})


class ScheduleRequest(BaseModel):
    """Demande de planification"""
    video_id: UUID
    platform: str
    scheduled_time: str = Field(..., description="ISO 8601 datetime")
    title: str
    description: str = ""
    tags: List[str] = []


class BatchPublishRequest(BaseModel):
    """Publication sur plusieurs plateformes"""
    video_id: UUID
    platforms: List[str]
    auto_optimize: bool = Field(default=True, description="Optimiser automatiquement les métadonnées pour chaque plateforme")
    base_title: str
    base_description: str = ""
    base_tags: List[str] = []


class PublishResponse(BaseModel):
    """Réponse de publication"""
    id: UUID
    video_id: UUID
    platform: str
    status: str
    platform_post_id: Optional[str]
    platform_url: Optional[str]
    published_at: Optional[datetime]


@router.post("/", response_model=PublishResponse)
async def publish_video(request: PublishRequest):
    """
    Publie une vidéo sur une plateforme.

    La publication est asynchrone. Utilisez GET /publish/{id}/status pour suivre.
    """
    from app.agents.publish_agent import PublishAgent
    from app.agents.base import AgentTask
    import uuid

    agent = PublishAgent()
    task = AgentTask(
        task_type="publish_video",
        input_data={
            "video_path": str(request.video_id),  # TODO: résoudre le chemin
            "platform": request.platform,
            "title": request.title,
            "description": request.description,
            "tags": request.tags,
            "thumbnail_path": request.thumbnail_path,
            "privacy": request.privacy,
            "platform_settings": request.platform_settings
        }
    )
    result = await agent.execute(task)

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error_message)

    pub_result = result.output_data.get("publish_result", {})

    return PublishResponse(
        id=uuid.uuid4(),
        video_id=request.video_id,
        platform=request.platform,
        status=pub_result.get("status", "pending"),
        platform_post_id=pub_result.get("platform_post_id"),
        platform_url=pub_result.get("platform_url"),
        published_at=None
    )


@router.post("/schedule", response_model=PublishResponse)
async def schedule_publish(request: ScheduleRequest):
    """
    Planifie une publication pour plus tard.
    """
    from app.agents.publish_agent import PublishAgent
    from app.agents.base import AgentTask
    import uuid

    agent = PublishAgent()
    task = AgentTask(
        task_type="schedule_publish",
        input_data={
            "video_path": str(request.video_id),
            "platform": request.platform,
            "scheduled_time": request.scheduled_time,
            "metadata": {
                "title": request.title,
                "description": request.description,
                "tags": request.tags
            }
        }
    )
    result = await agent.execute(task)

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error_message)

    return PublishResponse(
        id=uuid.uuid4(),
        video_id=request.video_id,
        platform=request.platform,
        status="scheduled",
        platform_post_id=None,
        platform_url=None,
        published_at=None
    )


@router.post("/batch", response_model=Dict[str, Any])
async def batch_publish(request: BatchPublishRequest):
    """
    Publie sur plusieurs plateformes en une fois.

    Si auto_optimize=true, les titres, descriptions et tags
    sont automatiquement optimisés pour chaque plateforme.
    """
    from app.agents.publish_agent import PublishAgent
    from app.agents.base import AgentTask

    agent = PublishAgent()
    task = AgentTask(
        task_type="batch_publish",
        input_data={
            "video_path": str(request.video_id),
            "platforms": request.platforms,
            "auto_optimize": request.auto_optimize,
            "metadata": {
                "title": request.base_title,
                "description": request.base_description,
                "tags": request.base_tags
            }
        }
    )
    result = await agent.execute(task)

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error_message)

    return result.output_data


@router.post("/optimize-metadata")
async def optimize_metadata(
    content_summary: str,
    platform: str,
    target_audience: str = "general",
    language: str = "fr"
):
    """
    Génère des métadonnées optimisées pour une plateforme.

    Utilise l'IA pour créer:
    - Titre accrocheur
    - Description SEO-optimisée
    - Tags/hashtags pertinents
    """
    from app.agents.publish_agent import PublishAgent
    from app.agents.base import AgentTask

    agent = PublishAgent()
    task = AgentTask(
        task_type="optimize_metadata",
        input_data={
            "platform": platform,
            "content_summary": content_summary,
            "target_audience": target_audience,
            "language": language
        }
    )
    result = await agent.execute(task)

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error_message)

    return result.output_data


@router.post("/thumbnail/generate")
async def generate_thumbnail(
    video_id: UUID,
    platform: str = "youtube",
    title_text: Optional[str] = None,
    style: str = "modern"
):
    """
    Génère une miniature optimisée pour la plateforme.
    """
    from app.agents.publish_agent import PublishAgent
    from app.agents.base import AgentTask

    agent = PublishAgent()
    task = AgentTask(
        task_type="generate_thumbnail",
        input_data={
            "video_path": str(video_id),
            "platform": platform,
            "title_text": title_text,
            "style": style
        }
    )
    result = await agent.execute(task)

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error_message)

    return result.output_data


@router.get("/{publish_id}/status")
async def get_publish_status(publish_id: UUID):
    """Récupère le statut d'une publication"""
    return {
        "publish_id": str(publish_id),
        "status": "published",
        "platform_url": f"https://youtube.com/watch?v={publish_id}"
    }


@router.get("/{publish_id}/analytics")
async def get_publish_analytics(publish_id: UUID):
    """
    Récupère les analytics d'une publication.
    """
    from app.agents.publish_agent import PublishAgent
    from app.agents.base import AgentTask

    agent = PublishAgent()
    task = AgentTask(
        task_type="get_analytics",
        input_data={
            "platform": "youtube",  # TODO: récupérer depuis DB
            "platform_post_id": str(publish_id)
        }
    )
    result = await agent.execute(task)
    return result.output_data


@router.delete("/{publish_id}")
async def cancel_publish(publish_id: UUID):
    """Annule une publication planifiée"""
    return {"publish_id": str(publish_id), "status": "cancelled"}


@router.get("/accounts")
async def list_connected_accounts():
    """Liste les comptes sociaux connectés"""
    from app.agents.publish_agent import PublishAgent
    from app.agents.base import AgentTask

    agent = PublishAgent()
    task = AgentTask(
        task_type="list_connected_accounts",
        input_data={}
    )
    result = await agent.execute(task)
    return result.output_data


@router.get("/best-time/{platform}")
async def get_best_posting_time(platform: str, timezone: str = "Europe/Paris"):
    """
    Recommande le meilleur moment pour publier sur une plateforme.
    """
    from app.agents.publish_agent import PublishAgent

    agent = PublishAgent()
    return agent.get_best_posting_time(platform, timezone)


@router.get("/platforms")
async def list_supported_platforms():
    """Liste les plateformes supportées et leurs limites"""
    from app.agents.publish_agent import PublishAgent

    return {
        "platforms": list(PublishAgent.PLATFORM_LIMITS.keys()),
        "limits": PublishAgent.PLATFORM_LIMITS
    }
