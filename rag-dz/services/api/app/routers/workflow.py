"""
Workflow Router - API endpoints for orchestrated project creation
BMAD → Orchestrator → Archon → Prompt Creator → Bolt
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging

from app.services.workflow_orchestrator import (
    workflow_orchestrator,
    WorkflowContext,
    WorkflowStage
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/workflow", tags=["Workflow Orchestrator"])


class WorkflowStartRequest(BaseModel):
    """Request to start a new workflow"""
    project_name: str
    project_description: str
    user_id: Optional[str] = None
    auto_execute: bool = True  # Run full pipeline automatically


class WorkflowStageRequest(BaseModel):
    """Request to execute a specific stage"""
    workflow_id: str
    stage: str  # bmad_brainstorm, bmad_planning, etc.


class WorkflowResponse(BaseModel):
    """Response with workflow status"""
    workflow_id: str
    project_name: str
    current_stage: str
    stage_history: List[Dict[str, Any]]
    has_errors: bool
    errors: List[str]

    # Optional outputs based on stage
    brainstorm_result: Optional[Dict[str, Any]] = None
    project_plan: Optional[Dict[str, Any]] = None
    knowledge_base_id: Optional[str] = None
    final_prompt: Optional[str] = None
    bolt_session_id: Optional[str] = None


def _context_to_response(context: WorkflowContext) -> WorkflowResponse:
    """Convert WorkflowContext to API response"""
    return WorkflowResponse(
        workflow_id=context.workflow_id,
        project_name=context.project_name,
        current_stage=context.current_stage.value,
        stage_history=context.stage_history,
        has_errors=len(context.errors) > 0,
        errors=context.errors,
        brainstorm_result=context.brainstorm_result,
        project_plan=context.project_plan,
        knowledge_base_id=context.knowledge_base_id,
        final_prompt=context.final_prompt[:500] if context.final_prompt else None,  # Truncate
        bolt_session_id=context.bolt_session_id
    )


@router.post("/start", response_model=WorkflowResponse)
async def start_workflow(
    request: WorkflowStartRequest,
    background_tasks: BackgroundTasks
):
    """
    Start a new project creation workflow

    Pipeline:
    1. BMAD Agents brainstorm the project
    2. BMAD Agents create detailed plan
    3. Orchestrator processes and structures
    4. Archon creates knowledge base
    5. Prompt Creator prepares Bolt prompt
    6. Bolt.diy generates the code

    Args:
        request: Project details to start workflow

    Returns:
        WorkflowResponse with workflow ID and initial status
    """
    try:
        logger.info(f"Starting workflow for: {request.project_name}")

        if request.auto_execute:
            # Run full pipeline in background
            context = await workflow_orchestrator.start_workflow(
                project_name=request.project_name,
                project_description=request.project_description,
                user_id=request.user_id,
                auto_execute=False  # We'll execute manually
            )

            # Execute pipeline in background
            background_tasks.add_task(
                workflow_orchestrator.execute_pipeline,
                context
            )

            return _context_to_response(context)
        else:
            # Just create workflow, don't execute
            context = await workflow_orchestrator.start_workflow(
                project_name=request.project_name,
                project_description=request.project_description,
                user_id=request.user_id,
                auto_execute=False
            )

            return _context_to_response(context)

    except Exception as e:
        logger.error(f"Workflow start error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow_status(workflow_id: str):
    """
    Get workflow status and outputs

    Returns current stage, history, and any available outputs
    """
    context = workflow_orchestrator.get_workflow(workflow_id)

    if not context:
        raise HTTPException(status_code=404, detail="Workflow not found")

    return _context_to_response(context)


@router.get("/", response_model=List[WorkflowResponse])
async def list_workflows():
    """List all workflows"""
    workflows = workflow_orchestrator.get_all_workflows()
    return [_context_to_response(w) for w in workflows]


@router.post("/{workflow_id}/execute-stage")
async def execute_stage(workflow_id: str, request: WorkflowStageRequest):
    """
    Execute a specific workflow stage manually

    Useful for step-by-step execution or retrying failed stages
    """
    context = workflow_orchestrator.get_workflow(workflow_id)

    if not context:
        raise HTTPException(status_code=404, detail="Workflow not found")

    try:
        stage = WorkflowStage(request.stage)

        if stage == WorkflowStage.BMAD_BRAINSTORM:
            context.brainstorm_result = await workflow_orchestrator.bmad.brainstorm(context)
        elif stage == WorkflowStage.BMAD_PLANNING:
            context.project_plan = await workflow_orchestrator.bmad.create_project_plan(context)
        elif stage == WorkflowStage.ARCHON_KNOWLEDGE:
            context.knowledge_base_id = await workflow_orchestrator.archon.create_knowledge_base(context)
        elif stage == WorkflowStage.PROMPT_CREATION:
            result = await workflow_orchestrator.prompt_creator.create_prompt(context)
            context.final_prompt = result["prompt"]
            context.prompt_metadata = result["metadata"]
        elif stage == WorkflowStage.BOLT_EXECUTION:
            result = await workflow_orchestrator.bolt.execute(context)
            context.generated_code = result
            context.bolt_session_id = result.get("session_id")
        else:
            raise HTTPException(status_code=400, detail=f"Cannot execute stage: {stage}")

        return _context_to_response(context)

    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid stage: {request.stage}")
    except Exception as e:
        logger.error(f"Stage execution error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{workflow_id}/prompt")
async def get_workflow_prompt(workflow_id: str):
    """
    Get the full generated prompt for Bolt

    Returns the complete prompt that will be/was sent to Bolt
    """
    context = workflow_orchestrator.get_workflow(workflow_id)

    if not context:
        raise HTTPException(status_code=404, detail="Workflow not found")

    if not context.final_prompt:
        raise HTTPException(status_code=400, detail="Prompt not yet generated")

    return {
        "workflow_id": workflow_id,
        "prompt": context.final_prompt,
        "metadata": context.prompt_metadata,
        "ready_for_bolt": True
    }


@router.post("/{workflow_id}/send-to-bolt")
async def send_to_bolt(workflow_id: str):
    """
    Send the prepared prompt to Bolt for execution

    Triggers code generation in Bolt.diy with the optimized prompt
    """
    context = workflow_orchestrator.get_workflow(workflow_id)

    if not context:
        raise HTTPException(status_code=404, detail="Workflow not found")

    if not context.final_prompt:
        raise HTTPException(status_code=400, detail="Prompt not yet generated. Run prompt_creation stage first.")

    try:
        result = await workflow_orchestrator.bolt.execute(context)
        context.generated_code = result
        context.bolt_session_id = result.get("session_id")
        context.current_stage = WorkflowStage.COMPLETED

        return {
            "workflow_id": workflow_id,
            "bolt_session_id": context.bolt_session_id,
            "status": "sent_to_bolt",
            "message": "Prompt sent to Bolt for code generation"
        }

    except Exception as e:
        logger.error(f"Bolt execution error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==============================================
# QUICK START ENDPOINTS
# ==============================================

@router.post("/quick-start")
async def quick_start_project(
    project_name: str,
    project_idea: str,
    background_tasks: BackgroundTasks
):
    """
    Quick start a project with minimal input

    Just provide a name and idea, the workflow handles everything:
    1. BMAD brainstorms and plans
    2. Archon creates knowledge base
    3. Prompt is prepared
    4. Code is generated in Bolt

    Example:
        POST /api/workflow/quick-start?project_name=TodoApp&project_idea=A task management app with real-time sync
    """
    return await start_workflow(
        WorkflowStartRequest(
            project_name=project_name,
            project_description=project_idea,
            auto_execute=True
        ),
        background_tasks
    )


@router.get("/stages/available")
async def get_available_stages():
    """Get list of available workflow stages"""
    return {
        "stages": [
            {"id": "bmad_brainstorm", "name": "BMAD Brainstorm", "description": "Initial project ideation with PM and Architect"},
            {"id": "bmad_planning", "name": "BMAD Planning", "description": "Detailed project planning with full BMAD team"},
            {"id": "orchestrator_process", "name": "Orchestrator", "description": "Process and structure project"},
            {"id": "archon_knowledge", "name": "Archon Knowledge", "description": "Create knowledge base"},
            {"id": "prompt_creation", "name": "Prompt Creator", "description": "Prepare optimized Bolt prompt"},
            {"id": "bolt_execution", "name": "Bolt Execution", "description": "Generate code with Bolt.diy"},
        ]
    }
