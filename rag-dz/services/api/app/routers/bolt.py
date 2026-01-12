"""
Router pour l'API Bolt SuperPower
Endpoints pour gérer les workflows de génération de projets
"""
import logging
import asyncio
from typing import Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, Header
from fastapi.responses import FileResponse
import os

from app.models.bolt_workflow import (
    DirectModeRequest,
    BMADWorkflowRequest,
    ExportZipRequest,
    DirectWorkflowResponse,
    BMADWorkflowResponse,
    WorkflowStatusResponse,
    WorkflowMode,
    WorkflowStatus
)
from app.services.bolt_workflow_service import BoltWorkflowService
from app.services.bolt_orchestration_service import BoltOrchestrationService
from app.services.bolt_zip_service import BoltZipService
from app.dependencies import get_db_pool, verify_api_key

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/bolt", tags=["Bolt SuperPower"])


# ==================== Endpoints ====================

@router.post("/direct", response_model=DirectWorkflowResponse)
async def create_direct_workflow(
    request: DirectModeRequest,
    background_tasks: BackgroundTasks,
    db_pool = Depends(get_db_pool),
    api_key: str = Depends(verify_api_key)
):
    """
    Mode Direct: Génération immédiate à partir d'un prompt

    Le workflow:
    1. Crée le workflow en DB
    2. Lance la génération en arrière-plan
    3. Sauvegarde optionnelle dans Archon
    4. Génère le ZIP
    5. Retourne l'ID du workflow

    L'utilisateur peut ensuite poller /status/{workflow_id} pour suivre la progression.
    """
    try:
        workflow_service = BoltWorkflowService(db_pool)
        orchestration_service = BoltOrchestrationService(db_pool)

        # Créer le workflow
        workflow_id = await workflow_service.create_workflow(
            mode=WorkflowMode.DIRECT,
            user_description=request.prompt,
            tech_stack=request.tech_stack,
            metadata={
                "save_to_archon": request.save_to_archon,
                "export_format": request.export_format.value
            }
        )

        # Lancer la génération en arrière-plan
        background_tasks.add_task(
            orchestration_service.run_direct_mode,
            workflow_id,
            request.prompt,
            request.tech_stack,
            request.save_to_archon
        )

        logger.info(f"Created direct workflow {workflow_id}")

        return DirectWorkflowResponse(
            workflow_id=workflow_id,
            status=WorkflowStatus.GENERATING,
            mode=WorkflowMode.DIRECT,
            estimated_time_seconds=120,  # ~2 minutes estimés
            message="Génération du projet en cours...",
            download_url=f"/api/bolt/download/{workflow_id}"
        )

    except Exception as e:
        logger.error(f"Error creating direct workflow: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bmad-workflow", response_model=BMADWorkflowResponse)
async def create_bmad_workflow(
    request: BMADWorkflowRequest,
    background_tasks: BackgroundTasks,
    db_pool = Depends(get_db_pool),
    api_key: str = Depends(verify_api_key)
):
    """
    Mode BMAD: Orchestration par agents spécialisés

    Le workflow:
    1. Crée le workflow en DB
    2. Crée les exécutions d'agents (architect, pm, backend, etc.)
    3. Lance l'orchestration séquentielle en arrière-plan
    4. Chaque agent enrichit le contexte pour le suivant
    5. SuperPower Orchestrator synthétise tout
    6. Crée le projet dans Archon
    7. Génère le code final
    8. Crée le ZIP

    Durée estimée: 5-10 minutes selon le nombre d'agents.
    """
    try:
        workflow_service = BoltWorkflowService(db_pool)
        orchestration_service = BoltOrchestrationService(db_pool)

        # Créer le workflow
        workflow_id = await workflow_service.create_workflow(
            mode=WorkflowMode.BMAD,
            user_description=request.user_description,
            metadata={
                "constraints": request.constraints.dict(),
                "preferences": request.preferences.dict(),
                "agents_to_use": request.agents_to_use
            }
        )

        # Créer les exécutions d'agents
        for agent_id in request.agents_to_use:
            await workflow_service.create_agent_execution(
                workflow_id=workflow_id,
                agent_name=get_agent_name(agent_id),
                agent_id=agent_id
            )

        # Lancer l'orchestration en arrière-plan
        background_tasks.add_task(
            orchestration_service.run_bmad_orchestration,
            workflow_id,
            request
        )

        logger.info(f"Created BMAD workflow {workflow_id} with {len(request.agents_to_use)} agents")

        # Estimer le temps (1-2 min par agent)
        estimated_time = len(request.agents_to_use) * 90

        return BMADWorkflowResponse(
            workflow_id=workflow_id,
            status=WorkflowStatus.ORCHESTRATING,
            mode=WorkflowMode.BMAD,
            current_agent=request.agents_to_use[0] if request.agents_to_use else None,
            agents_completed=[],
            agents_pending=request.agents_to_use,
            estimated_time_seconds=estimated_time,
            live_updates_url=f"/api/bolt/status/{workflow_id}",
            message="Orchestration BMAD démarrée..."
        )

    except Exception as e:
        logger.error(f"Error creating BMAD workflow: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{workflow_id}", response_model=WorkflowStatusResponse)
async def get_workflow_status(
    workflow_id: str,
    db_pool = Depends(get_db_pool),
    api_key: str = Depends(verify_api_key)
):
    """
    Récupère le statut temps réel d'un workflow

    Retourne:
    - Statut global (pending, orchestrating, generating, completed, failed)
    - Progression en pourcentage
    - Agents complétés avec leurs résumés
    - Agents en attente
    - Erreurs éventuelles
    - Liens vers Archon et téléchargement ZIP
    """
    try:
        workflow_service = BoltWorkflowService(db_pool)

        status = await workflow_service.get_workflow_status(workflow_id)

        if not status:
            raise HTTPException(status_code=404, detail=f"Workflow {workflow_id} not found")

        return status

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting workflow status: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/export-zip/{workflow_id}")
async def export_workflow_zip(
    workflow_id: str,
    request: ExportZipRequest,
    db_pool = Depends(get_db_pool),
    api_key: str = Depends(verify_api_key)
):
    """
    Génère et télécharge le ZIP du projet

    Options:
    - include_docs: Inclure la documentation (ARCHITECTURE.md, etc.)
    - include_tests: Inclure les tests
    - include_deployment: Inclure les configs de déploiement

    Le ZIP est créé à la volée et retourné immédiatement.
    """
    try:
        workflow_service = BoltWorkflowService(db_pool)
        zip_service = BoltZipService(db_pool)

        # Vérifier que le workflow existe et est complété
        workflow = await workflow_service.get_workflow(workflow_id)

        if not workflow:
            raise HTTPException(status_code=404, detail=f"Workflow {workflow_id} not found")

        if workflow["status"] != WorkflowStatus.COMPLETED.value:
            raise HTTPException(
                status_code=400,
                detail=f"Workflow is not completed yet. Current status: {workflow['status']}"
            )

        # Générer le ZIP si nécessaire
        if not workflow["zip_file_path"] or not os.path.exists(workflow["zip_file_path"]):
            logger.info(f"Generating ZIP for workflow {workflow_id}")
            zip_path = await zip_service.create_project_zip(
                workflow_id=workflow_id,
                include_docs=request.include_docs,
                include_tests=request.include_tests,
                include_deployment=request.include_deployment
            )

            # Mettre à jour le chemin dans la DB
            await workflow_service.set_zip_file_path(workflow_id, zip_path)
        else:
            zip_path = workflow["zip_file_path"]

        # Retourner le fichier
        if not os.path.exists(zip_path):
            raise HTTPException(status_code=404, detail="ZIP file not found")

        return FileResponse(
            path=zip_path,
            media_type="application/zip",
            filename=f"project-{workflow_id}.zip",
            headers={
                "Content-Disposition": f'attachment; filename="project-{workflow_id}.zip"'
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting ZIP: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{workflow_id}")
async def download_workflow_project(
    workflow_id: str,
    db_pool = Depends(get_db_pool),
    api_key: str = Depends(verify_api_key)
):
    """
    Endpoint simplifié pour télécharger le projet

    Équivalent à POST /export-zip avec options par défaut (tout inclus)
    """
    try:
        workflow_service = BoltWorkflowService(db_pool)

        workflow = await workflow_service.get_workflow(workflow_id)

        if not workflow:
            raise HTTPException(status_code=404, detail=f"Workflow {workflow_id} not found")

        if workflow["status"] != WorkflowStatus.COMPLETED.value:
            raise HTTPException(
                status_code=400,
                detail=f"Workflow is not completed yet. Current status: {workflow['status']}"
            )

        zip_path = workflow["zip_file_path"]

        if not zip_path or not os.path.exists(zip_path):
            raise HTTPException(
                status_code=404,
                detail="Project ZIP not found. Use POST /export-zip to generate it."
            )

        return FileResponse(
            path=zip_path,
            media_type="application/zip",
            filename=f"project-{workflow_id}.zip",
            headers={
                "Content-Disposition": f'attachment; filename="project-{workflow_id}.zip"'
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading project: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Endpoints de gestion ====================

@router.delete("/workflow/{workflow_id}")
async def delete_workflow(
    workflow_id: str,
    db_pool = Depends(get_db_pool),
    api_key: str = Depends(verify_api_key)
):
    """
    Supprime un workflow et tous ses artifacts

    Utiliser avec précaution : suppression définitive !
    """
    try:
        workflow_service = BoltWorkflowService(db_pool)
        zip_service = BoltZipService(db_pool)

        workflow = await workflow_service.get_workflow(workflow_id)

        if not workflow:
            raise HTTPException(status_code=404, detail=f"Workflow {workflow_id} not found")

        # Supprimer le ZIP si existe
        if workflow["zip_file_path"] and os.path.exists(workflow["zip_file_path"]):
            os.remove(workflow["zip_file_path"])
            logger.info(f"Deleted ZIP file: {workflow['zip_file_path']}")

        # Supprimer de la DB (cascade sur agent_executions et artifacts)
        async with db_pool.acquire() as conn:
            await conn.execute(
                "DELETE FROM bolt_workflows WHERE workflow_id = $1",
                workflow_id
            )

        logger.info(f"Deleted workflow {workflow_id}")

        return {"message": f"Workflow {workflow_id} deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting workflow: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check de l'API Bolt SuperPower"""
    return {
        "status": "healthy",
        "service": "Bolt SuperPower API",
        "version": "1.0.0"
    }


# ==================== Helper Functions ====================

def get_agent_name(agent_id: str) -> str:
    """Convertit un agent_id en nom complet"""
    agent_names = {
        "architect": "Winston - Architect Agent",
        "pm": "John - PM Agent",
        "backend": "Amelia - Backend Dev Agent",
        "frontend": "Sara - Frontend Dev Agent",
        "devops": "Carlos - DevOps Agent",
        "qa": "Murat - QA Agent"
    }
    return agent_names.get(agent_id, f"{agent_id.title()} Agent")
