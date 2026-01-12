"""
Bolt Executor - SEUL WRITER de code dans l'architecture Nexus
Port: 8053
"""

import os
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .bridge import BoltBridge, Provider, Template, Project, GenerationResult, CommandResult
from .executor import BoltExecutor, Task, TaskType, TaskStatus, ExecutionResult
from .templates import list_templates, get_template, get_template_files, TemplateInfo
from .mcp_tools import BoltMCPServer, BOLT_TOOLS

# Import UI Rules from shared
import sys
# Add shared directory to path (for Docker container with copied shared folder)
shared_paths = [
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'shared'),  # /app/shared
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'shared'),  # ../shared
]
for p in shared_paths:
    if os.path.exists(p) and p not in sys.path:
        sys.path.insert(0, p)

try:
    from ui_rules import (
        validate_ui,
        validate_ui_strict,
        get_tailwind_config,
        get_css_variables,
        get_i18n_config,
        UI_RULES,
        UIValidationResult
    )
    UI_RULES_AVAILABLE = True
    print("UI Rules loaded successfully")
except ImportError as e:
    UI_RULES_AVAILABLE = False
    print(f"Warning: UI Rules not available - {e}")


# ============ CONFIGURATION ============

BOLT_URL = os.getenv("BOLT_URL", "http://localhost:5173")
LOCK_URL = os.getenv("META_ORCHESTRATOR_URL", "http://localhost:8100")
VALIDATOR_URL = os.getenv("VALIDATOR_URL", "http://localhost:8054")
DEFAULT_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", "anthropic")


# ============ GLOBAL INSTANCES ============

bolt_bridge: BoltBridge | None = None
bolt_executor: BoltExecutor | None = None
mcp_server: BoltMCPServer | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle du serveur"""
    global bolt_bridge, bolt_executor, mcp_server

    # Startup
    bolt_bridge = BoltBridge(
        base_url=BOLT_URL,
        default_provider=Provider(DEFAULT_PROVIDER)
    )
    bolt_executor = BoltExecutor(
        bolt=bolt_bridge,
        lock_url=LOCK_URL,
        validator_url=VALIDATOR_URL
    )
    mcp_server = BoltMCPServer(bolt_bridge, bolt_executor)

    print(f"Bolt Executor started - Bolt URL: {BOLT_URL}")

    yield

    # Shutdown
    if bolt_bridge:
        await bolt_bridge.close()


app = FastAPI(
    title="Bolt Executor",
    description="SEUL WRITER de code - Exécute la génération et modification de code",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============ REQUEST MODELS ============

class CreateProjectRequest(BaseModel):
    """Requête de création de projet"""
    name: str
    template: str
    description: str | None = None


class GenerateCodeRequest(BaseModel):
    """Requête de génération de code"""
    prompt: str
    project_id: str | None = None
    provider: str | None = None
    model: str | None = None
    context: dict = Field(default_factory=dict)


class EditFileRequest(BaseModel):
    """Requête d'édition de fichier"""
    project_id: str
    file_path: str
    instructions: str
    provider: str | None = None


class ExecuteCommandRequest(BaseModel):
    """Requête d'exécution de commande"""
    project_id: str
    command: str
    timeout: int = 60


class ExecuteTaskRequest(BaseModel):
    """Requête d'exécution de tâche"""
    project_id: str
    title: str
    description: str
    type: str = "generate"
    affected_files: list[str] = Field(default_factory=list)
    specs: dict = Field(default_factory=dict)
    provider: str | None = None
    skip_tests: bool = False
    skip_validation: bool = False


class QuickFixRequest(BaseModel):
    """Requête de quick fix"""
    project_id: str
    file_path: str
    fix_description: str


class DeployRequest(BaseModel):
    """Requête de déploiement"""
    project_id: str
    target: str = "preview"
    options: dict = Field(default_factory=dict)


class MCPToolRequest(BaseModel):
    """Requête MCP tool"""
    tool_name: str
    arguments: dict = Field(default_factory=dict)


class UIValidateRequest(BaseModel):
    """Requête de validation UI"""
    code: str
    file_type: str = "auto"
    strict: bool = False


# ============ HEALTH ENDPOINTS ============

@app.get("/health")
async def health():
    """Health check"""
    bolt_status = await bolt_bridge.health() if bolt_bridge else {"status": "not initialized"}

    return {
        "status": "healthy",
        "service": "bolt-executor",
        "port": 8053,
        "role": "SEUL WRITER - Code Generation & Execution",
        "bolt_connection": bolt_status,
        "active_locks": len(bolt_executor.active_locks) if bolt_executor else 0,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/providers")
async def get_providers():
    """Liste les providers LLM disponibles"""
    providers = await bolt_bridge.get_providers() if bolt_bridge else []
    return {
        "providers": providers,
        "default": DEFAULT_PROVIDER
    }


# ============ PROJECT ENDPOINTS ============

@app.post("/projects", response_model=dict)
async def create_project(request: CreateProjectRequest):
    """Crée un nouveau projet"""
    if not bolt_bridge:
        raise HTTPException(status_code=503, detail="Bolt bridge not initialized")

    try:
        project = await bolt_bridge.create_project(
            request.name,
            request.template,
            request.description
        )
        return project.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/projects")
async def list_projects():
    """Liste tous les projets"""
    if not bolt_bridge:
        raise HTTPException(status_code=503, detail="Bolt bridge not initialized")

    projects = await bolt_bridge.list_projects()
    return {"projects": [p.model_dump() for p in projects]}


@app.get("/projects/{project_id}")
async def get_project(project_id: str):
    """Récupère un projet"""
    if not bolt_bridge:
        raise HTTPException(status_code=503, detail="Bolt bridge not initialized")

    project = await bolt_bridge.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project.model_dump()


@app.delete("/projects/{project_id}")
async def delete_project(project_id: str):
    """Supprime un projet"""
    if not bolt_bridge:
        raise HTTPException(status_code=503, detail="Bolt bridge not initialized")

    success = await bolt_bridge.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete project")

    return {"success": True, "project_id": project_id}


# ============ CODE GENERATION ENDPOINTS ============

@app.post("/generate")
async def generate_code(request: GenerateCodeRequest):
    """Génère du code avec un LLM"""
    if not bolt_bridge:
        raise HTTPException(status_code=503, detail="Bolt bridge not initialized")

    provider = Provider(request.provider) if request.provider else None

    result = await bolt_bridge.generate_code(
        prompt=request.prompt,
        context=request.context,
        provider=provider,
        model=request.model,
        project_id=request.project_id
    )

    return result.model_dump()


@app.post("/edit")
async def edit_file(request: EditFileRequest):
    """Édite un fichier existant"""
    if not bolt_bridge:
        raise HTTPException(status_code=503, detail="Bolt bridge not initialized")

    provider = Provider(request.provider) if request.provider else None

    result = await bolt_bridge.edit_file(
        request.project_id,
        request.file_path,
        request.instructions,
        provider
    )

    return result.model_dump()


@app.post("/execute")
async def execute_command(request: ExecuteCommandRequest):
    """Exécute une commande"""
    if not bolt_bridge:
        raise HTTPException(status_code=503, detail="Bolt bridge not initialized")

    result = await bolt_bridge.execute_command(
        request.project_id,
        request.command,
        request.timeout
    )

    return result.model_dump()


# ============ TASK EXECUTION ENDPOINTS ============

@app.post("/tasks/execute")
async def execute_task(request: ExecuteTaskRequest):
    """
    Exécute une tâche complète avec gestion des locks.
    C'est le point d'entrée principal pour l'exécution de code.
    """
    if not bolt_executor:
        raise HTTPException(status_code=503, detail="Bolt executor not initialized")

    import uuid

    task = Task(
        id=str(uuid.uuid4()),
        project_id=request.project_id,
        title=request.title,
        description=request.description,
        type=TaskType(request.type),
        affected_files=request.affected_files,
        specs=request.specs
    )

    provider = Provider(request.provider) if request.provider else None

    result = await bolt_executor.execute_task(
        task,
        provider=provider,
        skip_tests=request.skip_tests,
        skip_validation=request.skip_validation
    )

    return result.model_dump()


@app.post("/tasks/quick-fix")
async def quick_fix(request: QuickFixRequest):
    """Applique un quick fix sur un fichier"""
    if not bolt_executor:
        raise HTTPException(status_code=503, detail="Bolt executor not initialized")

    result = await bolt_executor.execute_quick_fix(
        request.project_id,
        request.file_path,
        request.fix_description
    )

    return result.model_dump()


@app.get("/tasks/locks")
async def get_active_locks():
    """Retourne les locks actifs"""
    if not bolt_executor:
        raise HTTPException(status_code=503, detail="Bolt executor not initialized")

    locks = bolt_executor.get_active_locks()
    return {"locks": [l.model_dump() for l in locks]}


# ============ TEMPLATE ENDPOINTS ============

@app.get("/templates")
async def list_all_templates():
    """Liste tous les templates disponibles"""
    standard = [t.value for t in Template]
    custom = [t.model_dump() for t in list_templates()]

    return {
        "standard_templates": standard,
        "iafactory_templates": custom
    }


@app.get("/templates/{template_id}")
async def get_template_details(template_id: str):
    """Récupère les détails d'un template"""
    template = get_template(template_id)
    if not template:
        # Vérifier si c'est un template standard
        try:
            Template(template_id)
            return {
                "id": template_id,
                "type": "standard",
                "files": []
            }
        except ValueError:
            raise HTTPException(status_code=404, detail="Template not found")

    return {
        "template": template.model_dump(),
        "files": list(template.files.keys())
    }


@app.get("/templates/{template_id}/files")
async def get_template_files_endpoint(template_id: str):
    """Récupère les fichiers d'un template"""
    files = get_template_files(template_id)
    if not files:
        raise HTTPException(status_code=404, detail="Template not found")

    return {"files": files}


# ============ DEPLOYMENT ENDPOINTS ============

@app.post("/deploy")
async def deploy(request: DeployRequest):
    """Déploie un projet"""
    if not bolt_bridge:
        raise HTTPException(status_code=503, detail="Bolt bridge not initialized")

    result = await bolt_bridge.deploy(
        request.project_id,
        request.target,
        request.options
    )

    return result


# ============ GIT ENDPOINTS ============

@app.post("/projects/{project_id}/git/commit")
async def git_commit(project_id: str, message: str):
    """Effectue un git commit"""
    if not bolt_bridge:
        raise HTTPException(status_code=503, detail="Bolt bridge not initialized")

    result = await bolt_bridge.git_commit(project_id, message)
    return result.model_dump()


@app.post("/projects/{project_id}/git/push")
async def git_push(project_id: str):
    """Effectue un git push"""
    if not bolt_bridge:
        raise HTTPException(status_code=503, detail="Bolt bridge not initialized")

    result = await bolt_bridge.git_push(project_id)
    return result.model_dump()


# ============ UI VALIDATION ENDPOINTS ============

@app.post("/ui/validate")
async def validate_ui_code(request: UIValidateRequest):
    """
    Valide le code UI selon les règles IA Factory Algérie.

    Règles vérifiées:
    - Responsive mobile-first
    - i18n (FR/AR/Darija/EN)
    - Support RTL pour l'arabe
    - Dark/Light mode
    - Couleur primaire #00a651
    - Paiement Chargily uniquement
    """
    if not UI_RULES_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="UI Rules module not available"
        )

    if request.strict:
        result = validate_ui_strict(request.code)
    else:
        result = validate_ui(request.code, request.file_type)

    return result.to_dict()


@app.get("/ui/rules")
async def get_ui_rules():
    """Retourne les règles UI IA Factory"""
    if not UI_RULES_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="UI Rules module not available"
        )

    return {
        "rules": UI_RULES,
        "version": "1.0.0",
        "mandatory": [
            "responsive",
            "i18n",
            "rtl",
            "dark_light_theme",
            "primary_color",
            "chargily_only"
        ]
    }


@app.get("/ui/config/tailwind")
async def get_tailwind_configuration():
    """Génère la configuration Tailwind pour IA Factory"""
    if not UI_RULES_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="UI Rules module not available"
        )

    return {
        "config": get_tailwind_config(),
        "filename": "tailwind.config.js"
    }


@app.get("/ui/config/css")
async def get_css_configuration():
    """Génère les variables CSS pour les thèmes"""
    if not UI_RULES_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="UI Rules module not available"
        )

    return {
        "css": get_css_variables(),
        "filename": "iafactory-design-system.css"
    }


@app.get("/ui/config/i18n")
async def get_i18n_configuration():
    """Génère la configuration i18n"""
    if not UI_RULES_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="UI Rules module not available"
        )

    return {
        "config": get_i18n_config(),
        "filename": "i18n.config.ts"
    }


# ============ MCP ENDPOINTS ============

@app.get("/mcp/tools")
async def list_mcp_tools():
    """Liste les tools MCP disponibles"""
    return {
        "tools": [
            {
                "name": t.name,
                "description": t.description,
                "inputSchema": t.input_schema
            }
            for t in BOLT_TOOLS
        ]
    }


@app.post("/mcp/execute")
async def execute_mcp_tool(request: MCPToolRequest):
    """Exécute un tool MCP"""
    if not mcp_server:
        raise HTTPException(status_code=503, detail="MCP server not initialized")

    result = await mcp_server.execute(request.tool_name, request.arguments)
    return result


# ============ MAIN ============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8053)
