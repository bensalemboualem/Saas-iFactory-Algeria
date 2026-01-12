"""
Projects API endpoints - Real implementation with full pipeline
"""
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
import logging
import asyncio

from app.services.project_manager import project_manager, ProjectStatus

router = APIRouter()
logger = logging.getLogger(__name__)


# === Schemas ===

class ProjectCreate(BaseModel):
    """Schéma pour créer un projet"""
    title: str = Field(..., min_length=1, max_length=255)
    user_prompt: str = Field(..., min_length=10, description="Le prompt NLP décrivant la vidéo souhaitée")
    target_duration: str = Field(default="60s", description="Durée cible: 15s, 30s, 60s, 3min, 10min")
    aspect_ratio: str = Field(default="16:9", description="Format: 16:9, 9:16, 1:1, 4:5")
    style: Optional[str] = Field(default="professional", description="Style visuel")
    language: str = Field(default="fr", description="Langue du contenu")
    target_platforms: List[str] = Field(default=["youtube"], description="Plateformes cibles")


class ProjectResponse(BaseModel):
    """Schéma de réponse pour un projet"""
    id: str
    title: str
    user_prompt: str
    target_duration: str
    aspect_ratio: str
    style: Optional[str]
    language: str
    target_platforms: List[str]
    status: str
    progress: dict
    video_url: Optional[str] = None
    error_message: Optional[str] = None


class ProjectPipelineStart(BaseModel):
    """Schéma pour démarrer le pipeline"""
    auto_publish: bool = Field(default=False, description="Publier automatiquement à la fin")
    priority: str = Field(default="normal", description="Priorité: low, normal, high")


class ProjectStatusResponse(BaseModel):
    """Schéma de réponse pour le statut d'un projet"""
    project_id: str
    status: str
    current_phase: str
    progress: dict


# === Endpoints ===

@router.post("/", response_model=ProjectResponse, status_code=201)
async def create_project(project: ProjectCreate):
    """
    Crée un nouveau projet vidéo.

    Le projet est créé en status 'draft'. Utilisez POST /projects/{id}/start
    pour lancer le pipeline de création.
    """
    try:
        created = project_manager.create_project(
            title=project.title,
            user_prompt=project.user_prompt,
            target_duration=project.target_duration,
            aspect_ratio=project.aspect_ratio,
            style=project.style,
            language=project.language,
            target_platforms=project.target_platforms,
        )

        logger.info(f"Project created: {created.id}")

        return ProjectResponse(
            id=str(created.id),
            title=created.title,
            user_prompt=created.user_prompt,
            target_duration=created.target_duration,
            aspect_ratio=created.aspect_ratio,
            style=created.style,
            language=created.language,
            target_platforms=created.target_platforms,
            status=created.status.value,
            progress={"overall": 0, "phases": {}},
        )

    except Exception as e:
        logger.error(f"Error creating project: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    status: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
):
    """Liste tous les projets avec pagination"""
    try:
        projects = project_manager.list_projects(status=status, limit=limit, offset=offset)

        return [
            ProjectResponse(
                id=str(p.id),
                title=p.title,
                user_prompt=p.user_prompt,
                target_duration=p.target_duration,
                aspect_ratio=p.aspect_ratio,
                style=p.style,
                language=p.language,
                target_platforms=p.target_platforms,
                status=p.status.value if isinstance(p.status, ProjectStatus) else p.status,
                progress={"overall": p.progress},
                video_url=p.video_url,
            )
            for p in projects
        ]

    except Exception as e:
        logger.error(f"Error listing projects: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str):
    """Récupère un projet par son ID"""
    project = project_manager.get_project(project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return ProjectResponse(
        id=str(project.id),
        title=project.title,
        user_prompt=project.user_prompt,
        target_duration=project.target_duration,
        aspect_ratio=project.aspect_ratio,
        style=project.style,
        language=project.language,
        target_platforms=project.target_platforms,
        status=project.status.value if isinstance(project.status, ProjectStatus) else project.status,
        progress={"overall": project.progress},
        video_url=project.video_url,
        error_message=project.error_message,
    )


@router.post("/{project_id}/start")
async def start_project_pipeline(
    project_id: str,
    options: ProjectPipelineStart,
    background_tasks: BackgroundTasks
):
    """
    Lance le pipeline de création vidéo pour un projet.

    Cette action démarre le processus asynchrone:
    1. Analyse du prompt
    2. Génération du script
    3. Génération des assets (images, voix, musique)
    4. Montage vidéo
    5. Publication (si auto_publish=true)
    """
    project = project_manager.get_project(project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.status not in [ProjectStatus.DRAFT, ProjectStatus.FAILED]:
        raise HTTPException(
            status_code=400,
            detail=f"Project cannot be started (current status: {project.status.value})"
        )

    try:
        # Start pipeline in background
        background_tasks.add_task(
            run_pipeline_async,
            project_id,
            options.auto_publish
        )

        return {
            "project_id": project_id,
            "status": "pipeline_started",
            "message": "Le pipeline de création a démarré",
            "options": options.model_dump()
        }

    except Exception as e:
        logger.error(f"Error starting pipeline for project {project_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def run_pipeline_async(project_id: str, auto_publish: bool):
    """Helper to run pipeline from background task"""
    try:
        await project_manager.start_pipeline(
            project_id=project_id,
            auto_publish=auto_publish
        )
    except Exception as e:
        logger.error(f"Pipeline execution error for {project_id}: {e}")


@router.get("/{project_id}/status", response_model=ProjectStatusResponse)
async def get_project_status(project_id: str):
    """
    Récupère le statut détaillé du projet et de son pipeline.
    """
    project = project_manager.get_project(project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project.get_status_dict()


@router.post("/{project_id}/pause")
async def pause_project(project_id: str):
    """Met en pause le pipeline du projet"""
    project = project_manager.get_project(project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Pause not fully implemented yet
    return {"project_id": project_id, "status": "pause_not_supported"}


@router.post("/{project_id}/resume")
async def resume_project(project_id: str):
    """Reprend le pipeline d'un projet en pause"""
    project = project_manager.get_project(project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return {"project_id": project_id, "status": "resume_not_supported"}


@router.post("/{project_id}/cancel")
async def cancel_project(project_id: str):
    """Annule le pipeline du projet"""
    project = project_manager.get_project(project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    success = project_manager.cancel_pipeline(project_id)

    return {
        "project_id": project_id,
        "status": "cancelled" if success else "cancel_failed"
    }


@router.delete("/{project_id}")
async def delete_project(project_id: str):
    """Supprime un projet et tous ses assets"""
    success = project_manager.delete_project(project_id)

    if not success:
        raise HTTPException(status_code=404, detail="Project not found")

    return {"deleted": True, "project_id": project_id}
