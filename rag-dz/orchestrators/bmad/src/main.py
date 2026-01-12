"""
BMAD Orchestrator - Moteur de workflows agile
Port: 8052
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .runner import BMADRunner, Workflow, Scope, Complexity, AgentResult
from .workflow import WorkflowEngine, WorkflowExecution, WorkflowStatus
from .agents_dz import register_dz_agents, list_dz_agents, CustomAgentInfo
from .mcp_tools import BMADMCPServer

# Configuration
BMAD_PATH = os.getenv("BMAD_PATH", "./bmad")
LLM_URL = os.getenv("LLM_URL", "http://localhost:8100/llm")

# Instances globales
runner: BMADRunner | None = None
engine: WorkflowEngine | None = None
mcp_server: BMADMCPServer | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management"""
    global runner, engine, mcp_server

    runner = BMADRunner(BMAD_PATH, LLM_URL)
    register_dz_agents(runner)
    engine = WorkflowEngine(runner)
    mcp_server = BMADMCPServer(runner, engine)

    yield


app = FastAPI(
    title="Nexus BMAD Orchestrator",
    description="Moteur de workflows agile BMAD Method",
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


# ============ MODELS ============

class RecommendRequest(BaseModel):
    scope: str
    complexity: str = "moderate"


class RunAgentRequest(BaseModel):
    agent: str
    task: str
    context: dict | None = None


class ExecuteWorkflowRequest(BaseModel):
    workflow: str
    requirements: str
    context: dict | None = None


class ExecuteProRequest(BaseModel):
    """Request for pro workflow execution with structured JSON output"""
    requirements: str
    workflow: str = "feature-flow"  # Default to feature-flow
    context: dict | None = None


class ProjectDecision(BaseModel):
    """Structured project decision from BMAD"""
    decision: str  # GO, NO_GO, NEEDS_CLARIFICATION
    project: dict  # name, type, stack, constraints
    artifacts: dict  # prd_md, architecture_md, backlog
    reasoning: str


class GeneratePRDRequest(BaseModel):
    requirements: str


class GenerateArchitectureRequest(BaseModel):
    prd: str


class LocalizeDarijaRequest(BaseModel):
    content: str
    context: str | None = None


class CheckConformityRequest(BaseModel):
    solution: str


# ============ HEALTH ============

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Nexus BMAD Orchestrator",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "workflows": "/workflows",
            "agents": "/agents",
            "execute": "/execute"
        }
    }


@app.get("/health")
async def health():
    """Health check"""
    agents_loaded = len(runner.agents) if runner else 0
    custom_agents = len(runner.custom_agents) if runner else 0

    return {
        "status": "healthy",
        "service": "bmad-orchestrator",
        "version": "1.0.0",
        "agents_loaded": agents_loaded,
        "custom_agents": custom_agents
    }


# ============ WORKFLOWS ============

@app.get("/workflows")
async def list_workflows():
    """Liste tous les workflows disponibles"""
    if not engine:
        raise HTTPException(503, "Engine not initialized")

    return {
        "workflows": [
            engine.get_workflow_info(w)
            for w in Workflow
        ]
    }


@app.post("/workflows/recommend")
async def recommend_workflow(req: RecommendRequest):
    """Recommande un workflow basé sur la portée et complexité"""
    if not engine:
        raise HTTPException(503, "Engine not initialized")

    return engine.recommend_and_explain(req.scope, req.complexity)


@app.post("/workflows/execute")
async def execute_workflow(
    req: ExecuteWorkflowRequest,
    background_tasks: BackgroundTasks
):
    """Lance l'exécution d'un workflow"""
    if not engine:
        raise HTTPException(503, "Engine not initialized")

    try:
        workflow = Workflow(req.workflow)
    except ValueError:
        raise HTTPException(400, f"Invalid workflow: {req.workflow}")

    input_data = {
        "requirements": req.requirements,
        **(req.context or {})
    }

    # Lancer en background pour ne pas bloquer
    import uuid
    execution_id = str(uuid.uuid4())

    async def run_workflow():
        await engine.execute(workflow, input_data, execution_id)

    background_tasks.add_task(run_workflow)

    return {
        "execution_id": execution_id,
        "workflow": workflow.value,
        "status": "started"
    }


@app.get("/workflows/executions/{execution_id}")
async def get_execution(execution_id: str):
    """Récupère le statut d'une exécution"""
    if not engine:
        raise HTTPException(503, "Engine not initialized")

    execution = engine.get_execution(execution_id)
    if not execution:
        raise HTTPException(404, "Execution not found")

    return {
        "id": execution.id,
        "workflow": execution.workflow.value,
        "status": execution.status.value,
        "steps": [
            {
                "agent": s.agent,
                "status": s.status.value,
                "duration_ms": s.result.duration_ms if s.result else None
            }
            for s in execution.steps
        ],
        "results": execution.results,
        "error": execution.error
    }


@app.get("/workflows/executions")
async def list_executions(status: str | None = None):
    """Liste les exécutions"""
    if not engine:
        raise HTTPException(503, "Engine not initialized")

    status_filter = WorkflowStatus(status) if status else None
    executions = engine.list_executions(status_filter)

    return {
        "executions": [
            {
                "id": e.id,
                "workflow": e.workflow.value,
                "status": e.status.value,
                "started_at": e.started_at.isoformat() if e.started_at else None
            }
            for e in executions
        ]
    }


@app.post("/workflows/execute-pro", response_model=ProjectDecision)
async def execute_workflow_pro(req: ExecuteProRequest):
    """
    PRO Workflow Execution - Returns structured JSON contract.

    This is the CONTRACTUAL endpoint that returns machine-readable output.
    Used by Nexus meta-orchestrator to route to Archon and then Bolt.

    Output contract:
    - decision: GO | NO_GO | NEEDS_CLARIFICATION
    - project: {name, type, stack, repo_strategy, constraints}
    - artifacts: {prd_md, architecture_md, backlog}
    - reasoning: explanation
    """
    if not engine or not runner:
        raise HTTPException(503, "Engine not initialized")

    from .runner import extract_keywords, detect_domain, get_feature_name, is_billing_task
    import re

    task = req.requirements

    # === GATE: Check for forbidden/impossible tasks ===
    forbidden_patterns = [
        r"\b(hack|ddos|exploit|crack|steal|malware|ransomware)\b",
        r"\b(bypass\s+security|break\s+into|unauthorized\s+access)\b",
    ]
    for pattern in forbidden_patterns:
        if re.search(pattern, task.lower()):
            return ProjectDecision(
                decision="NO_GO",
                project={},
                artifacts={},
                reasoning=f"Task refused: contains forbidden intent matching pattern '{pattern}'"
            )

    # === ANALYSIS ===
    keywords = extract_keywords(task)
    domain = detect_domain(task)
    feature_name = get_feature_name(task)

    # Detect project type and stack
    project_type = "fullstack"  # default
    stack = []

    if domain["frontend"] and not domain["backend"]:
        project_type = "frontend"
        if "react" in task.lower():
            stack.extend(["react", "vite"])
        elif "vue" in task.lower():
            stack.extend(["vue", "vite"])
        elif "angular" in task.lower():
            stack.append("angular")
        else:
            stack.extend(["react", "vite"])  # default frontend
        if "tailwind" in task.lower():
            stack.append("tailwind")
        if "typescript" in task.lower() or "tsx" in task.lower():
            stack.append("typescript")

    elif domain["backend"] and not domain["frontend"]:
        project_type = "backend"
        if "fastapi" in task.lower():
            stack.extend(["fastapi", "python"])
        elif "django" in task.lower():
            stack.extend(["django", "python"])
        elif "express" in task.lower():
            stack.extend(["express", "nodejs"])
        else:
            stack.extend(["fastapi", "python"])  # default backend
        stack.append("postgresql")

    else:
        # Fullstack default
        stack.extend(["react", "vite", "tailwind", "fastapi", "postgresql"])

    # Constraints
    constraints = []
    if is_billing_task(task):
        constraints.append("payment:chargily")
        constraints.append("currency:DZD")
    if domain["dz"]:
        constraints.append("locale:dz")
        constraints.append("languages:fr,ar,darija")
    if domain["auth"]:
        constraints.append("auth:jwt")

    # === Execute workflow synchronously for structured output ===
    try:
        workflow = Workflow(req.workflow)
    except ValueError:
        workflow = Workflow.FEATURE  # default

    input_data = {
        "requirements": req.requirements,
        **(req.context or {})
    }

    # Execute synchronously
    import asyncio
    execution = await engine.execute(workflow, input_data)

    # === BUILD STRUCTURED OUTPUT ===
    if execution.status.value == "failed":
        return ProjectDecision(
            decision="NO_GO",
            project={},
            artifacts={},
            reasoning=f"Workflow execution failed: {execution.error}"
        )

    # Build backlog from developer output
    backlog = []
    dev_output = execution.results.get("developer", "")

    # Extract tasks from developer output
    task_patterns = [
        r"- \[[ x]\] (.+?)(?:\n|$)",
        r"(\d+)\. (.+?)(?:\n|$)",
    ]
    for pattern in task_patterns:
        matches = re.findall(pattern, dev_output)
        for i, match in enumerate(matches[:10]):  # max 10 tasks
            title = match[1] if isinstance(match, tuple) and len(match) > 1 else match
            if isinstance(title, str) and len(title) > 5:
                backlog.append({
                    "id": f"T{i+1}",
                    "title": title.strip()[:100],
                    "priority": "P0" if i < 3 else "P1"
                })

    # Default backlog if none extracted
    if not backlog:
        backlog = [
            {"id": "T1", "title": f"Setup {' + '.join(stack[:3])}", "priority": "P0"},
            {"id": "T2", "title": f"Implement {feature_name}", "priority": "P0"},
            {"id": "T3", "title": "Add tests", "priority": "P1"},
        ]

    # Build project name
    project_name = feature_name.lower().replace(" ", "-")
    if domain["frontend"]:
        project_name += "-frontend"
    elif domain["backend"]:
        project_name += "-api"

    return ProjectDecision(
        decision="GO",
        project={
            "name": project_name,
            "type": project_type,
            "stack": stack,
            "repo_strategy": "new",
            "constraints": constraints
        },
        artifacts={
            "prd_md": execution.results.get("pm", execution.results.get("analyst", "")),
            "architecture_md": execution.results.get("architect", ""),
            "test_strategy_md": execution.results.get("test", ""),
            "backlog": backlog
        },
        reasoning=f"Workflow {workflow.value} completed successfully with {len(execution.steps)} agents"
    )


# ============ AGENTS ============

@app.get("/agents")
async def list_agents():
    """Liste tous les agents disponibles"""
    if not runner:
        raise HTTPException(503, "Runner not initialized")

    return {
        "standard_agents": runner.list_agents(),
        "custom_agents": [a.model_dump() for a in list_dz_agents()]
    }


@app.post("/agents/run", response_model=dict)
async def run_agent(req: RunAgentRequest):
    """Exécute un agent spécifique"""
    if not runner:
        raise HTTPException(503, "Runner not initialized")

    result = await runner.run_agent(req.agent, req.task, req.context)
    return result.model_dump()


# ============ CONVENIENCE ENDPOINTS ============

@app.post("/generate/prd")
async def generate_prd(req: GeneratePRDRequest):
    """Génère un PRD"""
    if not runner:
        raise HTTPException(503, "Runner not initialized")

    result = await runner.generate_prd(req.requirements)
    return result.model_dump()


@app.post("/generate/architecture")
async def generate_architecture(req: GenerateArchitectureRequest):
    """Génère l'architecture"""
    if not runner:
        raise HTTPException(503, "Runner not initialized")

    result = await runner.generate_architecture(req.prd)
    return result.model_dump()


# ============ ALGERIA-SPECIFIC ============

@app.post("/dz/conformity")
async def check_dz_conformity(req: CheckConformityRequest):
    """Vérifie la conformité pour l'Algérie"""
    if not runner:
        raise HTTPException(503, "Runner not initialized")

    result = await runner.run_agent(
        "conformity-dz",
        f"Vérifie la conformité:\n\n{req.solution}"
    )
    return result.model_dump()


@app.post("/dz/localize")
async def localize_darija(req: LocalizeDarijaRequest):
    """Localise en Darija algérien"""
    if not runner:
        raise HTTPException(503, "Runner not initialized")

    task = f"Localise en Darija:\n\n{req.content}"
    if req.context:
        task += f"\n\nContexte: {req.context}"

    result = await runner.run_agent("darija-content", task)
    return result.model_dump()


@app.get("/dz/agents")
async def list_dz_agents_endpoint():
    """Liste les agents spécifiques Algérie"""
    return {"agents": [a.model_dump() for a in list_dz_agents()]}


# ============ MCP ============

@app.get("/mcp/tools")
async def get_mcp_tools():
    """Liste les tools MCP disponibles"""
    if not mcp_server:
        raise HTTPException(503, "MCP server not initialized")

    return {"tools": mcp_server.get_tools()}


@app.post("/mcp/execute")
async def execute_mcp_tool(tool_name: str, arguments: dict):
    """Exécute un tool MCP"""
    if not mcp_server:
        raise HTTPException(503, "MCP server not initialized")

    return await mcp_server.execute(tool_name, arguments)
