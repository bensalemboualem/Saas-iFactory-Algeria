"""
BMAD-METHOD Integration API
Orchestration d'agents AI pour workflows avancés
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel
import subprocess
import json
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/bmad", tags=["BMAD"])

# Store active workflows in memory (use Redis in production)
active_workflows: Dict[str, Dict[str, Any]] = {}


class WorkflowRequest(BaseModel):
    name: str
    description: Optional[str] = None
    agent: str = "bmm-architect"  # Default agent
    command: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = {}


class WorkflowResponse(BaseModel):
    id: str
    status: str
    created_at: str
    name: str
    agent: str
    output: Optional[str] = None
    error: Optional[str] = None


@router.get("/agents")
async def list_agents():
    """List available BMAD agents from real bmad-method YAML files"""
    from app.services.bmad_orchestrator import bmad_orchestrator

    try:
        # Charger les agents depuis les vrais fichiers YAML
        yaml_agents = bmad_orchestrator.list_agents()

        # Mapper vers format frontend avec icônes
        icon_map = {
            "architect": "🏗️",
            "pm": "📋",
            "dev": "💻",
            "tea": "🧪",
            "tech-writer": "📝",
            "analyst": "📊",
            "sm": "🎯",
            "ux-designer": "🎨",
            "frame-expert": "🖼️",
            "bmad-builder": "🔨",
            "brainstorming-coach": "💡",
            "creative-problem-solver": "🧩",
            "design-thinking-coach": "✨",
            "innovation-strategist": "🚀",
            "storyteller": "📖",
            "game-architect": "🎮",
            "game-designer": "🎲",
            "game-dev": "👾",
            "game-scrum-master": "🏃"
        }

        category_map = {
            "bmm": "development",
            "bmb": "builder",
            "cis": "creative",
            "bmgd": "game-dev"
        }

        agents = []
        for agent in yaml_agents:
            agent_id = f"{agent['module']}-{agent['id']}"
            agents.append({
                "id": agent_id,
                "name": agent['name'],
                "description": agent.get('description') or agent.get('title', ''),
                "category": category_map.get(agent['module'], "other"),
                "icon": icon_map.get(agent['id'], "🤖")
            })

    except Exception as e:
        logger.error(f"Error loading agents from YAML: {e}")
        # Fallback to minimal list
        agents = [
            {
                "id": "bmm-architect",
                "name": "Winston",
                "description": "Software architecture and design",
                "category": "development",
                "icon": "🏗️"
            }
        ]
    return {
        "agents": agents,
        "total": len(agents)
    }


@router.get("/workflows")
async def list_workflows():
    """List available BMAD workflows - Generated from all 19 agents"""
    workflows = [
        # BMM - Development
        {"id": "architecture", "name": "Architecture Design", "description": "Design system architecture", "agent": "bmm-architect", "icon": "🏗️"},
        {"id": "product-planning", "name": "Product Planning", "description": "Create product roadmap", "agent": "bmm-pm", "icon": "📋"},
        {"id": "development", "name": "Development", "description": "Implement features", "agent": "bmm-dev", "icon": "💻"},
        {"id": "testing", "name": "Testing", "description": "Create test suite", "agent": "bmm-tea", "icon": "🧪"},
        {"id": "documentation", "name": "Documentation", "description": "Write documentation", "agent": "bmm-tech-writer", "icon": "📝"},
        {"id": "analysis", "name": "Business Analysis", "description": "Analyze requirements", "agent": "bmm-analyst", "icon": "📊"},
        {"id": "scrum", "name": "Scrum Planning", "description": "Sprint planning", "agent": "bmm-sm", "icon": "🎯"},
        {"id": "ux-design", "name": "UX Design", "description": "Design user experience", "agent": "bmm-ux-designer", "icon": "🎨"},
        {"id": "visual-design", "name": "Visual Design", "description": "Create diagrams", "agent": "bmm-frame-expert", "icon": "🖼️"},

        # BMB - Builder
        {"id": "custom-agent", "name": "Build Custom Agent", "description": "Create custom BMAD agent", "agent": "bmb-bmad-builder", "icon": "🔨"},

        # CIS - Creative
        {"id": "brainstorming", "name": "Brainstorming", "description": "Generate creative ideas", "agent": "cis-brainstorming-coach", "icon": "💡"},
        {"id": "problem-solving", "name": "Problem Solving", "description": "Solve complex problems", "agent": "cis-creative-problem-solver", "icon": "🧩"},
        {"id": "design-thinking", "name": "Design Thinking", "description": "Apply design thinking", "agent": "cis-design-thinking-coach", "icon": "✨"},
        {"id": "innovation", "name": "Innovation Strategy", "description": "Develop innovation strategy", "agent": "cis-innovation-strategist", "icon": "🚀"},
        {"id": "storytelling", "name": "Storytelling", "description": "Craft compelling narratives", "agent": "cis-storyteller", "icon": "📖"},

        # BMGD - Game Development
        {"id": "game-architecture", "name": "Game Architecture", "description": "Design game systems", "agent": "bmgd-game-architect", "icon": "🎮"},
        {"id": "game-design", "name": "Game Design", "description": "Create game mechanics", "agent": "bmgd-game-designer", "icon": "🎲"},
        {"id": "game-development", "name": "Game Development", "description": "Implement game features", "agent": "bmgd-game-dev", "icon": "👾"},
        {"id": "game-scrum", "name": "Game Scrum", "description": "Manage game dev sprint", "agent": "bmgd-game-scrum-master", "icon": "🏃"},
    ]
    return {
        "workflows": workflows,
        "total": len(workflows)
    }


@router.get("/workflows/active")
async def get_active_workflows():
    """Get all active workflows"""
    return {
        "workflows": list(active_workflows.values()),
        "total": len(active_workflows)
    }


@router.post("/workflows/execute", response_model=WorkflowResponse)
async def execute_workflow(
    request: WorkflowRequest,
    background_tasks: BackgroundTasks
):
    """Execute a BMAD workflow"""
    workflow_id = str(uuid.uuid4())

    workflow_data = {
        "id": workflow_id,
        "name": request.name,
        "agent": request.agent,
        "status": "queued",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "output": "",
        "error": None
    }

    active_workflows[workflow_id] = workflow_data

    # Execute workflow in background
    background_tasks.add_task(
        run_bmad_workflow,
        workflow_id,
        request
    )

    return WorkflowResponse(**workflow_data)


@router.get("/workflows/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow_status(workflow_id: str):
    """Get workflow execution status"""
    if workflow_id not in active_workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")

    return WorkflowResponse(**active_workflows[workflow_id])


@router.delete("/workflows/{workflow_id}")
async def cancel_workflow(workflow_id: str):
    """Cancel a running workflow"""
    if workflow_id not in active_workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")

    # TODO: Actually kill the subprocess
    active_workflows[workflow_id]["status"] = "cancelled"
    active_workflows[workflow_id]["updated_at"] = datetime.utcnow().isoformat()

    return {"success": True, "workflow_id": workflow_id}


async def run_bmad_workflow(workflow_id: str, request: WorkflowRequest):
    """Execute BMAD workflow in subprocess"""
    try:
        active_workflows[workflow_id]["status"] = "running"
        active_workflows[workflow_id]["updated_at"] = datetime.utcnow().isoformat()

        # TODO: Execute actual BMAD command
        # For now, simulate execution
        import asyncio
        await asyncio.sleep(2)

        output = f"Workflow '{request.name}' completed successfully with agent {request.agent}"

        active_workflows[workflow_id]["status"] = "completed"
        active_workflows[workflow_id]["output"] = output
        active_workflows[workflow_id]["updated_at"] = datetime.utcnow().isoformat()

    except Exception as e:
        logger.error(f"Workflow {workflow_id} failed: {e}")
        active_workflows[workflow_id]["status"] = "failed"
        active_workflows[workflow_id]["error"] = str(e)
        active_workflows[workflow_id]["updated_at"] = datetime.utcnow().isoformat()


@router.get("/health")
async def bmad_health():
    """Check BMAD service health"""
    # TODO: Check if Node.js and BMAD are installed
    return {
        "status": "healthy",
        "bmad_installed": True,  # Check actual installation
        "node_version": "20.0.0",  # Get actual version
        "active_workflows": len(active_workflows)
    }
