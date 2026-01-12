"""
BMAD Orchestration Router - Endpoints pour le vrai bmad-method
"""

import logging
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.bmad_orchestrator import bmad_orchestrator

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/bmad", tags=["bmad-orchestration"])


class TaskRequest(BaseModel):
    agent_id: str
    task: str
    context: Optional[Dict[str, Any]] = None


class WorkflowRequest(BaseModel):
    name: str
    agents: List[str]
    steps: List[Dict[str, Any]]


@router.get("/orchestration/status")
async def get_orchestration_status():
    """Obtient le statut du système d'orchestration BMAD"""
    try:
        status = bmad_orchestrator.get_status()
        return status
    except Exception as e:
        logger.error(f"Error getting BMAD status: {e}")
        return {
            "status": "error",
            "error": str(e)
        }


@router.get("/orchestration/agents")
async def list_orchestration_agents():
    """Liste tous les agents BMAD disponibles via le système d'orchestration"""
    try:
        agents = bmad_orchestrator.list_agents()
        return {
            "agents": agents,
            "count": len(agents)
        }
    except Exception as e:
        logger.error(f"Error listing BMAD agents: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list agents: {str(e)}"
        )


@router.post("/orchestration/execute")
async def execute_agent_task(request: TaskRequest):
    """
    Exécute une tâche avec un agent BMAD via le système d'orchestration complet

    NOTE: Pour l'instant, utilise /api/bmad/chat pour les conversations.
    L'orchestration complète sera implémentée dans une version future.
    """
    try:
        result = bmad_orchestrator.execute_agent_task(
            agent_id=request.agent_id,
            task=request.task,
            context=request.context
        )

        if not result.get("success"):
            raise HTTPException(
                status_code=501,  # Not Implemented
                detail=result.get("error", "Orchestration not fully implemented")
            )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error executing agent task: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to execute task: {str(e)}"
        )


@router.post("/orchestration/workflow")
async def create_workflow(request: WorkflowRequest):
    """
    Crée un workflow BMAD multi-agents

    NOTE: Feature en développement
    """
    try:
        result = bmad_orchestrator.create_workflow(
            workflow_name=request.name,
            agents=request.agents,
            steps=request.steps
        )

        if not result.get("success"):
            raise HTTPException(
                status_code=501,
                detail=result.get("error", "Workflow creation not implemented")
            )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating workflow: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create workflow: {str(e)}"
        )
