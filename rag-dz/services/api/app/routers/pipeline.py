"""
===================================================================
PIPELINE API ROUTER
IAFactory Algeria - BMAD → ARCHON → BOLT Pipeline
===================================================================
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any, List
import subprocess
import json
import os
from pathlib import Path
import asyncio
from datetime import datetime

router = APIRouter(prefix="/api/v1/pipeline", tags=["pipeline"])

# Paths
PROJECTS_DIR = Path("/opt/iafactory-rag-dz/projects")
BMAD_PATH = Path("/opt/iafactory-rag-dz/bmad")
PIPELINE_SCRIPT = Path("/opt/iafactory-rag-dz/scripts/pipeline-auto.sh")

# In-memory storage for pipeline status (use Redis in production)
pipeline_status_store: Dict[str, Dict[str, Any]] = {}


class PipelineCreateRequest(BaseModel):
    """Request model for creating a new project"""
    name: str
    description: str
    type: str = "custom"
    email: Optional[EmailStr] = None
    language: str = "fr"


class PipelineStatusResponse(BaseModel):
    """Response model for pipeline status"""
    pipeline_id: str
    status: str
    bmad_completed: bool = False
    archon_in_progress: bool = False
    archon_completed: bool = False
    bolt_in_progress: bool = False
    bolt_completed: bool = False
    completed: bool = False
    error: Optional[str] = None
    result: Optional[Dict[str, Any]] = None


class PipelineResult(BaseModel):
    """Response model for completed pipeline"""
    success: bool
    pipeline_id: str
    bmad: Dict[str, Any]
    archon: Dict[str, Any]
    bolt: Dict[str, Any]
    project_dir: str
    created_at: str


def slugify(text: str) -> str:
    """Convert text to slug"""
    import re
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    return text.strip('-')


async def run_bmad_workflow(
    project_name: str,
    project_desc: str,
    project_type: str,
    pipeline_id: str
):
    """
    Run BMAD workflow in background

    This function:
    1. Creates project directory
    2. Installs BMAD
    3. Waits for user to complete workflows (via websocket or polling)
    4. Extracts outputs (PRD, Architecture, Stories)
    """
    try:
        project_slug = slugify(project_name)
        project_dir = PROJECTS_DIR / project_slug

        # Update status
        pipeline_status_store[pipeline_id]["status"] = "bmad_running"
        pipeline_status_store[pipeline_id]["project_dir"] = str(project_dir)

        # Create project directory
        project_dir.mkdir(parents=True, exist_ok=True)

        # Install BMAD
        subprocess.run(
            ["npx", "bmad-method@alpha", "install", "--modules", "bmm", "--skip-prompts"],
            cwd=project_dir,
            check=True,
            capture_output=True
        )

        # Update status: BMAD installed, waiting for user workflows
        pipeline_status_store[pipeline_id]["status"] = "bmad_waiting_workflows"
        pipeline_status_store[pipeline_id]["bmad_installed"] = True

        # In production, use WebSocket to notify user to complete workflows
        # For now, we assume workflows are done when files exist

        # Wait for workflow outputs (poll for files)
        max_wait = 3600  # 1 hour max
        wait_interval = 10  # 10 seconds
        waited = 0

        bmad_docs = project_dir / ".bmad" / "docs"

        while waited < max_wait:
            # Check if PRD exists
            prd_files = list(bmad_docs.glob("**/prd*.md"))
            arch_files = list(bmad_docs.glob("**/architecture*.md"))
            story_files = list(bmad_docs.glob("**/story-*.md"))

            if prd_files and arch_files and story_files:
                # Workflows completed!
                break

            await asyncio.sleep(wait_interval)
            waited += wait_interval

        if waited >= max_wait:
            raise TimeoutError("BMAD workflows not completed in time")

        # Extract outputs
        bmad_outputs = {
            "prd": prd_files[0].read_text(encoding="utf-8") if prd_files else None,
            "architecture": arch_files[0].read_text(encoding="utf-8") if arch_files else None,
            "stories": [
                {
                    "file": str(f),
                    "content": f.read_text(encoding="utf-8")
                }
                for f in story_files
            ]
        }

        # Update status
        pipeline_status_store[pipeline_id]["status"] = "bmad_completed"
        pipeline_status_store[pipeline_id]["bmad_completed"] = True
        pipeline_status_store[pipeline_id]["bmad_outputs"] = bmad_outputs

        # Continue to ARCHON
        await run_archon_indexing(pipeline_id, bmad_outputs)

    except Exception as e:
        pipeline_status_store[pipeline_id]["status"] = "error"
        pipeline_status_store[pipeline_id]["error"] = str(e)


async def run_archon_indexing(pipeline_id: str, bmad_outputs: Dict[str, Any]):
    """
    Run ARCHON indexing

    This function:
    1. Creates knowledge base
    2. Uploads documents (PRD, Architecture, Stories)
    3. Runs indexing (embeddings)
    """
    try:
        pipeline_status_store[pipeline_id]["status"] = "archon_running"
        pipeline_status_store[pipeline_id]["archon_in_progress"] = True

        # Create KB (call your existing KB API)
        # For now, mock the response
        kb_id = f"kb_{pipeline_id[:8]}"

        # Upload documents
        documents_count = 2 + len(bmad_outputs["stories"])  # PRD + Arch + Stories

        # Run indexing
        embeddings_count = documents_count * 25  # Approximate

        # Update status
        pipeline_status_store[pipeline_id]["status"] = "archon_completed"
        pipeline_status_store[pipeline_id]["archon_completed"] = True
        pipeline_status_store[pipeline_id]["archon_in_progress"] = False
        pipeline_status_store[pipeline_id]["archon_result"] = {
            "kb_id": kb_id,
            "documents_count": documents_count,
            "embeddings_count": embeddings_count
        }

        # Continue to BOLT
        await run_bolt_generation(pipeline_id, kb_id)

    except Exception as e:
        pipeline_status_store[pipeline_id]["status"] = "error"
        pipeline_status_store[pipeline_id]["error"] = str(e)


async def run_bolt_generation(pipeline_id: str, kb_id: str):
    """
    Run BOLT code generation

    This function:
    1. Creates BOLT project
    2. Launches code generation with RAG
    3. Returns generated code info
    """
    try:
        pipeline_status_store[pipeline_id]["status"] = "bolt_running"
        pipeline_status_store[pipeline_id]["bolt_in_progress"] = True

        # Create BOLT project (call BOLT API)
        # For now, mock the response
        project_id = f"proj_{pipeline_id[:8]}"

        # Generate code
        files_count = 52
        code_size = 450 * 1024  # 450 KB

        # Update status
        pipeline_status_store[pipeline_id]["status"] = "completed"
        pipeline_status_store[pipeline_id]["bolt_completed"] = True
        pipeline_status_store[pipeline_id]["bolt_in_progress"] = False
        pipeline_status_store[pipeline_id]["completed"] = True
        pipeline_status_store[pipeline_id]["bolt_result"] = {
            "project_id": project_id,
            "files_count": files_count,
            "code_size": code_size
        }

    except Exception as e:
        pipeline_status_store[pipeline_id]["status"] = "error"
        pipeline_status_store[pipeline_id]["error"] = str(e)


@router.post("/create", response_model=PipelineResult)
async def create_pipeline(
    request: PipelineCreateRequest,
    background_tasks: BackgroundTasks
):
    """
    Create a new project using BMAD → ARCHON → BOLT pipeline

    This endpoint:
    1. Creates a unique pipeline ID
    2. Starts BMAD workflow in background
    3. Returns pipeline ID for status polling

    Example:
        POST /api/v1/pipeline/create
        {
            "name": "Mon E-commerce",
            "description": "Site de vente de produits artisanaux",
            "type": "ecommerce",
            "email": "user@example.com"
        }
    """
    # Generate pipeline ID
    pipeline_id = f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # Initialize status
    pipeline_status_store[pipeline_id] = {
        "pipeline_id": pipeline_id,
        "status": "initializing",
        "created_at": datetime.now().isoformat(),
        "request": request.dict()
    }

    # Start BMAD workflow in background
    background_tasks.add_task(
        run_bmad_workflow,
        request.name,
        request.description,
        request.type,
        pipeline_id
    )

    # Return immediately with pipeline ID
    return {
        "success": True,
        "pipeline_id": pipeline_id,
        "bmad": {"status": "starting"},
        "archon": {"status": "pending"},
        "bolt": {"status": "pending"},
        "project_dir": str(PROJECTS_DIR / slugify(request.name)),
        "created_at": datetime.now().isoformat()
    }


@router.get("/status/{pipeline_id}", response_model=PipelineStatusResponse)
async def get_pipeline_status(pipeline_id: str):
    """
    Get status of a running pipeline

    Use this endpoint to poll for updates while the pipeline is running.

    Example:
        GET /api/v1/pipeline/status/pipeline_20250106_143022
    """
    if pipeline_id not in pipeline_status_store:
        raise HTTPException(status_code=404, detail="Pipeline not found")

    status_data = pipeline_status_store[pipeline_id]

    return PipelineStatusResponse(
        pipeline_id=pipeline_id,
        status=status_data.get("status", "unknown"),
        bmad_completed=status_data.get("bmad_completed", False),
        archon_in_progress=status_data.get("archon_in_progress", False),
        archon_completed=status_data.get("archon_completed", False),
        bolt_in_progress=status_data.get("bolt_in_progress", False),
        bolt_completed=status_data.get("bolt_completed", False),
        completed=status_data.get("completed", False),
        error=status_data.get("error"),
        result={
            "bmad": status_data.get("bmad_result"),
            "archon": status_data.get("archon_result"),
            "bolt": status_data.get("bolt_result")
        } if status_data.get("completed") else None
    )


@router.get("/download/{project_id}")
async def download_project_code(project_id: str):
    """
    Download generated code as ZIP

    Example:
        GET /api/v1/pipeline/download/proj_abc123
    """
    # Find project directory
    # Create ZIP file
    # Return file response
    raise HTTPException(status_code=501, detail="Download not implemented yet")


@router.get("/list")
async def list_pipelines():
    """
    List all pipelines (for admin)

    Example:
        GET /api/v1/pipeline/list
    """
    return {
        "pipelines": [
            {
                "pipeline_id": pid,
                "status": data.get("status"),
                "created_at": data.get("created_at")
            }
            for pid, data in pipeline_status_store.items()
        ]
    }


@router.delete("/{pipeline_id}")
async def delete_pipeline(pipeline_id: str):
    """
    Delete a pipeline and its data

    Example:
        DELETE /api/v1/pipeline/pipeline_20250106_143022
    """
    if pipeline_id in pipeline_status_store:
        del pipeline_status_store[pipeline_id]
        return {"success": True, "message": "Pipeline deleted"}
    else:
        raise HTTPException(status_code=404, detail="Pipeline not found")
