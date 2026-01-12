"""
Nexus Meta-Orchestrator
Gouvernance globale, routage, sessions, conflits
"""

import os
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .router import route, RouteResult, get_all_patterns, Target
from .sessions import SessionManager, Session
from .locks import LockManager, Lock, LockError
from .conflicts import (
    ConflictResolver, ConflictType, Resolution,
    VetoError, PRIORITY_RULES
)
from .conversation_manager import (
    conversation_manager,
    ConversationPhase as CMPhase,
    AgentRole,
    AGENT_PERSONAS,
    detect_language,
    get_full_welcome_message
)
from .branding import (
    COMPANY, NEXUS_BRANDING, WELCOME_MESSAGES, SUCCESS_MESSAGES,
    get_text, get_welcome_message
)

# Configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
SESSION_TTL = int(os.getenv("SESSION_TTL", "3600"))
LOCK_TTL = int(os.getenv("LOCK_TTL", "300"))

# Managers globaux
session_manager: SessionManager | None = None
lock_manager: LockManager | None = None
conflict_resolver = ConflictResolver()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management"""
    global session_manager, lock_manager
    session_manager = SessionManager(REDIS_URL, ttl=SESSION_TTL)
    lock_manager = LockManager(REDIS_URL, default_ttl=LOCK_TTL)
    yield
    if session_manager:
        await session_manager.close()
    if lock_manager:
        await lock_manager.close()


app = FastAPI(
    title="Nexus Meta-Orchestrator",
    description="Gouvernance globale pour BMAD + Archon + Bolt.diy",
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

class RouteRequest(BaseModel):
    request: str
    context: dict[str, Any] | None = None


class SessionCreateRequest(BaseModel):
    user_id: str
    initial_context: dict[str, Any] | None = None


class SessionUpdateRequest(BaseModel):
    current_project: str | None = None
    current_task: str | None = None
    current_target: str | None = None
    context: dict[str, Any] | None = None


class LockRequest(BaseModel):
    resource: str
    holder: str
    ttl: int | None = None


class ConflictRequest(BaseModel):
    conflict_type: ConflictType
    contestants: list[str]
    context: dict[str, Any] | None = None


class WritePermissionRequest(BaseModel):
    agent: str
    path: str


class PipelineRequest(BaseModel):
    """Full pipeline request: BMAD → Archon → Bolt"""
    task: str
    workflow: str = "feature-flow"
    context: dict[str, Any] | None = None


class BoltJob(BaseModel):
    """Instructions for Bolt writer"""
    mode: str = "writer"
    project_id: str
    project_name: str
    prompt: str
    stack: list[str]
    file_plan: list[dict]


class PipelineResult(BaseModel):
    """Result from the full pipeline"""
    status: str  # success, rejected, error
    decision: str  # GO, NO_GO
    project_id: str | None = None
    bolt_job: BoltJob | None = None
    reasoning: str


# ============ HEALTH & STATUS ============

@app.get("/")
async def root():
    """Root endpoint - IA Factory Algeria Nexus"""
    return {
        "service": f"{NEXUS_BRANDING['name']} Meta-Orchestrator",
        "company": COMPANY["name"],
        "tagline": get_text(COMPANY["tagline"], "fr"),
        "version": "1.0.0",
        "logo": COMPANY["logo_emoji"],
        "colors": COMPANY["colors"],
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "status": "/status",
            "chat": "/chat",
            "route": "/route",
            "sessions": "/sessions",
            "locks": "/locks",
            "conflicts": "/conflicts"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    redis_ok = False
    try:
        if session_manager:
            await session_manager.redis.ping()
            redis_ok = True
    except Exception:
        pass

    return {
        "status": "healthy" if redis_ok else "degraded",
        "service": "meta-orchestrator",
        "version": "1.0.0",
        "redis": "connected" if redis_ok else "disconnected"
    }


@app.get("/status")
async def status():
    """Status des services orchestrés"""
    active_locks = []
    if lock_manager:
        locks = await lock_manager.list_locks()
        active_locks = [{"resource": l.resource, "holder": l.holder} for l in locks]

    return {
        "meta": "online",
        "services": {
            "bmad": "pending",
            "archon": "pending",
            "bolt": "pending"
        },
        "active_locks": active_locks,
        "config": {
            "session_ttl": SESSION_TTL,
            "lock_ttl": LOCK_TTL
        }
    }


# ============ ROUTING ============

@app.post("/route", response_model=RouteResult)
async def route_request(req: RouteRequest):
    """Route une requête vers l'orchestrateur approprié"""
    return route(req.request, req.context)


@app.get("/route/patterns")
async def get_patterns():
    """Retourne tous les patterns de routage"""
    return get_all_patterns()


# ============ SESSIONS ============

@app.post("/sessions", response_model=Session)
async def create_session(req: SessionCreateRequest):
    """Crée une nouvelle session"""
    if not session_manager:
        raise HTTPException(503, "Session manager not initialized")
    return await session_manager.create(req.user_id, req.initial_context)


@app.get("/sessions/{session_id}", response_model=Session)
async def get_session(session_id: str):
    """Récupère une session"""
    if not session_manager:
        raise HTTPException(503, "Session manager not initialized")

    session = await session_manager.get(session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    return session


@app.patch("/sessions/{session_id}", response_model=Session)
async def update_session(session_id: str, req: SessionUpdateRequest):
    """Met à jour une session"""
    if not session_manager:
        raise HTTPException(503, "Session manager not initialized")

    updates = {k: v for k, v in req.model_dump().items() if v is not None}
    session = await session_manager.update(session_id, **updates)
    if not session:
        raise HTTPException(404, "Session not found")
    return session


@app.post("/sessions/{session_id}/history")
async def add_history(session_id: str, entry: dict):
    """Ajoute une entrée à l'historique"""
    if not session_manager:
        raise HTTPException(503, "Session manager not initialized")

    session = await session_manager.add_to_history(session_id, entry)
    if not session:
        raise HTTPException(404, "Session not found")
    return {"status": "added", "history_length": len(session.history)}


@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Supprime une session"""
    if not session_manager:
        raise HTTPException(503, "Session manager not initialized")

    deleted = await session_manager.delete(session_id)
    if not deleted:
        raise HTTPException(404, "Session not found")
    return {"status": "deleted"}


# ============ LOCKS ============

@app.post("/locks", response_model=Lock)
async def acquire_lock(req: LockRequest):
    """Acquiert un verrou"""
    if not lock_manager:
        raise HTTPException(503, "Lock manager not initialized")

    try:
        return await lock_manager.acquire(req.resource, req.holder, req.ttl)
    except LockError as e:
        raise HTTPException(409, f"Resource locked by {e.holder}")


@app.delete("/locks/{resource}")
async def release_lock(resource: str, holder: str = Header(..., alias="X-Lock-Holder")):
    """Libère un verrou"""
    if not lock_manager:
        raise HTTPException(503, "Lock manager not initialized")

    released = await lock_manager.release(resource, holder)
    if not released:
        raise HTTPException(403, "Not authorized to release this lock")
    return {"status": "released", "resource": resource}


@app.get("/locks/{resource}")
async def get_lock(resource: str):
    """Vérifie le statut d'un verrou"""
    if not lock_manager:
        raise HTTPException(503, "Lock manager not initialized")

    locked, holder = await lock_manager.is_locked(resource)
    return {"locked": locked, "holder": holder}


@app.get("/locks")
async def list_locks(pattern: str = "*"):
    """Liste tous les verrous actifs"""
    if not lock_manager:
        raise HTTPException(503, "Lock manager not initialized")

    locks = await lock_manager.list_locks(pattern)
    return {
        "count": len(locks),
        "locks": [
            {
                "resource": l.resource,
                "holder": l.holder,
                "remaining_seconds": l.remaining_seconds
            }
            for l in locks
        ]
    }


# ============ CONFLICTS ============

@app.post("/conflicts/resolve", response_model=Resolution)
async def resolve_conflict(req: ConflictRequest):
    """Résout un conflit entre agents"""
    return conflict_resolver.resolve(req.conflict_type, req.contestants, req.context)


@app.get("/conflicts/rules")
async def get_conflict_rules():
    """Retourne les règles de priorité"""
    return {
        conflict_type.value: agents
        for conflict_type, agents in PRIORITY_RULES.items()
    }


@app.post("/conflicts/check-write")
async def check_write_permission(req: WritePermissionRequest):
    """Vérifie les permissions d'écriture"""
    return conflict_resolver.get_write_permission(req.agent, req.path)


@app.get("/conflicts/single-writer")
async def check_single_writer(agent: str, operation: str):
    """Vérifie la règle Single-Writer"""
    allowed = conflict_resolver.check_single_writer(agent, operation)
    return {
        "agent": agent,
        "operation": operation,
        "allowed": allowed,
        "reason": "Only bolt-executor can write code" if not allowed else "Authorized"
    }


# ============ PIPELINE PRO ============

BMAD_URL = os.getenv("BMAD_URL", "http://localhost:8052")
ARCHON_URL = os.getenv("ARCHON_URL", "http://localhost:8051")
BOLT_URL = os.getenv("BOLT_URL", "http://localhost:5173")

# LLM for orchestrator responses
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")


@app.post("/pipeline/execute", response_model=PipelineResult)
async def execute_pipeline(req: PipelineRequest):
    """
    PRO Pipeline: BMAD → Archon → Bolt

    This is the main entry point for the full orchestration pipeline.

    Flow:
    1. Call BMAD /workflows/execute-pro to get structured decision
    2. GATE A: If decision != GO, return rejection
    3. Call Archon to create project workspace
    4. GATE B: If Archon fails, return error
    5. Build bolt_job for Bolt writer
    6. Return bolt_job for execution

    Note: Bolt execution is NOT triggered here - caller must send bolt_job to Bolt.
    """
    import httpx
    import uuid

    # === STEP 1: Call BMAD ===
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            bmad_response = await client.post(
                f"{BMAD_URL}/workflows/execute-pro",
                json={
                    "requirements": req.task,
                    "workflow": req.workflow,
                    "context": req.context
                }
            )
            bmad_response.raise_for_status()
            bmad_result = bmad_response.json()
    except httpx.HTTPError as e:
        return PipelineResult(
            status="error",
            decision="ERROR",
            reasoning=f"BMAD call failed: {str(e)}"
        )

    # === GATE A: Check BMAD decision ===
    decision = bmad_result.get("decision", "NO_GO")
    if decision != "GO":
        return PipelineResult(
            status="rejected",
            decision=decision,
            reasoning=bmad_result.get("reasoning", "BMAD rejected the task")
        )

    # Extract project info
    project = bmad_result.get("project", {})
    artifacts = bmad_result.get("artifacts", {})

    # === STEP 2: Create Archon project (optional - if Archon /projects exists) ===
    project_id = str(uuid.uuid4())[:8]  # Short project ID

    # TODO: When Archon /projects endpoint is ready, call it here
    # For now, we just generate a project_id

    # === STEP 3: Build Bolt Job ===
    stack = project.get("stack", [])
    project_name = project.get("name", "new-project")
    project_type = project.get("type", "fullstack")
    constraints = project.get("constraints", [])
    backlog = artifacts.get("backlog", [])

    # Build prompt for Bolt
    prompt_parts = [
        f"Create a {project_type} project: {project_name}",
        f"\nStack: {', '.join(stack)}",
        f"\nTask: {req.task}",
    ]

    if constraints:
        prompt_parts.append(f"\nConstraints: {', '.join(constraints)}")

    if backlog:
        prompt_parts.append("\n\nBacklog:")
        for task in backlog[:5]:  # Max 5 tasks in prompt
            prompt_parts.append(f"- [{task.get('priority', 'P1')}] {task.get('title', '')}")

    # Build file plan based on stack
    file_plan = []
    if "react" in stack or "vite" in stack:
        file_plan.extend([
            {"path": "package.json", "action": "create"},
            {"path": "vite.config.ts", "action": "create"},
            {"path": "src/App.tsx", "action": "create"},
            {"path": "src/main.tsx", "action": "create"},
            {"path": "src/index.css", "action": "create"},
        ])
        if "tailwind" in stack:
            file_plan.append({"path": "tailwind.config.js", "action": "create"})

    if "fastapi" in stack:
        file_plan.extend([
            {"path": "requirements.txt", "action": "create"},
            {"path": "app/main.py", "action": "create"},
            {"path": "app/models.py", "action": "create"},
            {"path": "app/routes.py", "action": "create"},
        ])

    bolt_job = BoltJob(
        mode="writer",
        project_id=f"archon_{project_id}",
        project_name=project_name,
        prompt="".join(prompt_parts),
        stack=stack,
        file_plan=file_plan
    )

    return PipelineResult(
        status="success",
        decision="GO",
        project_id=f"archon_{project_id}",
        bolt_job=bolt_job,
        reasoning=bmad_result.get("reasoning", "Pipeline completed successfully")
    )


# ============ CONVERSATION ORCHESTRATOR ============
# This is the GUIDED conversation flow where orchestrator talks to user

class ConversationPhase(str):
    """Phases of the guided conversation"""
    BRAINSTORM = "brainstorm"      # BMAD agents help define the project
    CLARIFY = "clarify"            # Ask user clarifying questions
    PROPOSE = "propose"            # Propose options to user
    CONFIRM = "confirm"            # User confirms choices
    CREATE_PROJECT = "create"      # Archon creates DB/workspace
    READY_FOR_BOLT = "ready"       # Ready to generate code
    GENERATING = "generating"      # Bolt is generating


class ConversationMessage(BaseModel):
    """A message in the conversation"""
    role: str  # "user" | "orchestrator" | "system"
    content: str
    metadata: dict[str, Any] | None = None


class ConversationRequest(BaseModel):
    """Request to continue the conversation"""
    session_id: str | None = None  # None = create new session
    message: str
    context: dict[str, Any] | None = None


class ConversationResponse(BaseModel):
    """Response from the orchestrator"""
    session_id: str
    phase: str
    message: str  # The orchestrator's response to display
    options: list[str] | None = None  # Options for user to choose
    project_summary: dict[str, Any] | None = None  # Current project state
    bolt_prompt: str | None = None  # Final prompt for Bolt (when phase=ready)
    can_proceed: bool = False  # True when user can say "GO"


# In-memory conversation state (use Redis in production)
conversation_states: dict[str, dict] = {}


def get_orchestrator_prompt(phase: str, context: dict) -> str:
    """Generate system prompt for the orchestrator based on phase"""
    base = """Tu es un coach produit expert de IA Factory Algeria. Tu guides les utilisateurs dans la création de leur projet.

RÈGLES:
- Parle en français, tu peux utiliser du darija algérien si l'utilisateur le fait
- Sois concis mais chaleureux
- Pose UNE question à la fois
- Propose des OPTIONS claires (A, B, C)
- Ne génère JAMAIS de code toi-même
- Quand le projet est clair, demande confirmation avec "GO"

CONTRAINTES IA FACTORY:
- Paiement: Chargily uniquement (pas Stripe)
- Monnaie: DZD
- Langues: fr, ar, darija
- Stack par défaut: React + Vite + Tailwind + FastAPI
"""

    if phase == "brainstorm":
        return base + """
PHASE: BRAINSTORM
Tu viens de recevoir l'idée initiale. Analyse-la et pose des questions pour clarifier:
- Type de projet (frontend/backend/fullstack)
- Fonctionnalités principales
- Utilisateurs cibles
"""
    elif phase == "clarify":
        return base + f"""
PHASE: CLARIFICATION
Contexte actuel: {context.get('project_summary', {})}
Continue à poser des questions pour affiner le projet.
"""
    elif phase == "propose":
        return base + f"""
PHASE: PROPOSITION
Contexte: {context.get('project_summary', {})}
Propose 2-3 options d'architecture ou d'approche.
Termine par "Quelle option préfères-tu? (A/B/C)"
"""
    elif phase == "confirm":
        return base + f"""
PHASE: CONFIRMATION
Projet défini: {context.get('project_summary', {})}
Résume le projet et demande: "On lance la création? (GO/Modifier)"
"""

    return base


async def call_bmad_for_analysis(task: str, context: dict) -> dict:
    """Call BMAD agents to analyze the task (invisible to user)"""
    import httpx

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Quick analysis via analyst agent
            response = await client.post(
                f"{BMAD_URL}/agents/run",
                json={
                    "agent": "analyst",
                    "task": task,
                    "context": context
                }
            )
            if response.status_code == 200:
                return response.json()
    except Exception as e:
        print(f"[BMAD Analysis] Error: {e}")

    return {"output": "", "success": False}


async def call_archon_create_project(project: dict) -> dict:
    """Call Archon to create project workspace"""
    import httpx
    import uuid

    # For now, just generate project ID
    # TODO: Implement actual Archon project creation
    project_id = f"iaf-{uuid.uuid4().hex[:8]}"

    return {
        "project_id": project_id,
        "status": "created",
        "workspace": f"/projects/{project_id}"
    }


async def generate_orchestrator_response(
    messages: list[dict],
    system_prompt: str
) -> str:
    """Generate orchestrator response using LLM"""
    import httpx

    # Try OpenAI first, then Anthropic
    if OPENAI_API_KEY:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            *messages
                        ],
                        "max_tokens": 500,
                        "temperature": 0.7
                    }
                )
                if response.status_code == 200:
                    return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"[OpenAI] Error: {e}")

    if ANTHROPIC_API_KEY:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": ANTHROPIC_API_KEY,
                        "anthropic-version": "2023-06-01"
                    },
                    json={
                        "model": "claude-3-haiku-20240307",
                        "max_tokens": 500,
                        "system": system_prompt,
                        "messages": messages
                    }
                )
                if response.status_code == 200:
                    return response.json()["content"][0]["text"]
        except Exception as e:
            print(f"[Anthropic] Error: {e}")

    # Fallback: simple response
    return "Je suis prêt à t'aider! Dis-moi ce que tu veux créer."


def determine_next_phase(current_phase: str, user_message: str, context: dict) -> str:
    """Determine the next phase based on user input"""
    lower = user_message.lower()

    # User says GO
    if lower in ["go", "oui", "yes", "lance", "confirme", "ok let's go", "c'est bon"]:
        if current_phase == "confirm":
            return "create"
        elif current_phase == "brainstorm" or current_phase == "clarify":
            return "confirm"  # Skip to confirm if user is eager

    # User wants to modify
    if any(w in lower for w in ["modifier", "change", "non", "autre", "différent"]):
        return "clarify"

    # User selected an option
    if lower in ["a", "b", "c", "option a", "option b", "option c"]:
        return "confirm"

    # Natural progression
    phase_order = ["brainstorm", "clarify", "propose", "confirm", "create", "ready"]
    try:
        idx = phase_order.index(current_phase)
        # Stay in clarify/propose until enough info
        if current_phase in ["brainstorm", "clarify"]:
            # Check if we have enough info
            summary = context.get("project_summary", {})
            if summary.get("type") and summary.get("features"):
                return "propose"
            return "clarify"
        return phase_order[min(idx + 1, len(phase_order) - 1)]
    except ValueError:
        return "brainstorm"


def extract_project_info(messages: list[dict]) -> dict:
    """Extract project information from conversation"""
    project = {
        "name": "",
        "type": "fullstack",
        "features": [],
        "stack": [],
        "constraints": []
    }

    full_text = " ".join(m.get("content", "") for m in messages).lower()

    # Detect project type
    if "frontend" in full_text or "react" in full_text or "ui" in full_text:
        project["type"] = "frontend"
        project["stack"] = ["react", "vite", "tailwind"]
    if "backend" in full_text or "api" in full_text or "fastapi" in full_text:
        if project["type"] == "frontend":
            project["type"] = "fullstack"
        else:
            project["type"] = "backend"
        project["stack"].extend(["fastapi", "postgresql"])

    # Detect constraints
    if any(w in full_text for w in ["paiement", "payment", "chargily"]):
        project["constraints"].append("payment:chargily")
    if any(w in full_text for w in ["algérie", "algeria", "dz", "darija"]):
        project["constraints"].append("locale:dz")

    # Extract features (simple heuristic)
    feature_keywords = ["counter", "compteur", "login", "auth", "dashboard", "chat", "todo", "list"]
    for kw in feature_keywords:
        if kw in full_text:
            project["features"].append(kw)

    return project


def build_bolt_prompt(project: dict) -> str:
    """Build the final prompt for Bolt"""
    parts = [
        f"Crée un projet {project.get('type', 'fullstack')}: {project.get('name', 'mon-projet')}",
        f"\nStack: {', '.join(project.get('stack', ['react', 'vite', 'tailwind']))}",
    ]

    if project.get("features"):
        parts.append(f"\nFonctionnalités: {', '.join(project['features'])}")

    if project.get("constraints"):
        parts.append(f"\nContraintes: {', '.join(project['constraints'])}")

    parts.append("\n\nGénère le code complet avec tous les fichiers nécessaires.")

    return "".join(parts)


@app.post("/conversation", response_model=ConversationResponse)
async def conversation(req: ConversationRequest):
    """
    GUIDED CONVERSATION ENDPOINT

    This is the main entry point for the orchestrator-guided conversation.

    Flow:
    1. User sends message
    2. Orchestrator analyzes (calls BMAD internally if needed)
    3. Orchestrator responds with questions/options
    4. Repeat until user says GO
    5. Create project via Archon
    6. Return Bolt prompt for confirmation
    """
    import uuid

    # Get or create session
    session_id = req.session_id
    if not session_id or session_id not in conversation_states:
        session_id = str(uuid.uuid4())
        conversation_states[session_id] = {
            "phase": "brainstorm",
            "messages": [],
            "project_summary": {},
            "bmad_context": {}
        }

    state = conversation_states[session_id]

    # Add user message
    state["messages"].append({
        "role": "user",
        "content": req.message
    })

    # Determine next phase
    current_phase = state["phase"]
    next_phase = determine_next_phase(current_phase, req.message, state)
    state["phase"] = next_phase

    # Extract project info from conversation
    state["project_summary"] = extract_project_info(state["messages"])

    # Handle CREATE phase - call Archon
    if next_phase == "create":
        archon_result = await call_archon_create_project(state["project_summary"])
        state["project_summary"]["project_id"] = archon_result["project_id"]
        state["phase"] = "ready"

        bolt_prompt = build_bolt_prompt(state["project_summary"])

        return ConversationResponse(
            session_id=session_id,
            phase="ready",
            message=f"""✅ **Projet créé!**

**ID:** {archon_result['project_id']}
**Type:** {state['project_summary'].get('type', 'fullstack')}
**Stack:** {', '.join(state['project_summary'].get('stack', []))}

Voici le prompt pour Bolt. Confirme pour lancer la génération:

---
{bolt_prompt}
---

**Confirmer?** (Oui / Modifier)""",
            project_summary=state["project_summary"],
            bolt_prompt=bolt_prompt,
            can_proceed=True
        )

    # Call BMAD for background analysis (first message only)
    if len(state["messages"]) == 1:
        bmad_analysis = await call_bmad_for_analysis(req.message, {})
        state["bmad_context"] = bmad_analysis

    # Generate orchestrator response
    system_prompt = get_orchestrator_prompt(next_phase, state)
    orchestrator_message = await generate_orchestrator_response(
        state["messages"],
        system_prompt
    )

    # Add orchestrator response to history
    state["messages"].append({
        "role": "assistant",
        "content": orchestrator_message
    })

    # Detect options in response
    options = None
    if any(marker in orchestrator_message for marker in ["A)", "B)", "C)", "(A)", "(B)", "(C)"]):
        options = ["A", "B", "C"]

    return ConversationResponse(
        session_id=session_id,
        phase=next_phase,
        message=orchestrator_message,
        options=options,
        project_summary=state["project_summary"],
        can_proceed=(next_phase == "confirm")
    )


@app.get("/conversation/{session_id}")
async def get_conversation(session_id: str):
    """Get conversation state"""
    if session_id not in conversation_states:
        raise HTTPException(404, "Conversation not found")

    state = conversation_states[session_id]
    return {
        "session_id": session_id,
        "phase": state["phase"],
        "messages": state["messages"],
        "project_summary": state["project_summary"]
    }


@app.delete("/conversation/{session_id}")
async def delete_conversation(session_id: str):
    """Delete a conversation"""
    if session_id in conversation_states:
        del conversation_states[session_id]
    return {"status": "deleted"}


# ============ CHAT - CONVERSATIONAL MULTI-AGENT ============
# Le user PARLE avec les agents, c'est une vraie conversation

class ChatRequest(BaseModel):
    """Request for multi-agent chat"""
    session_id: str | None = None
    message: str
    user_id: str = "anonymous"


class AgentInfo(BaseModel):
    """Info sur l'agent qui parle"""
    role: str
    name: str
    title: str
    avatar: str


class ChatResponse(BaseModel):
    """Response from an agent"""
    session_id: str
    phase: str
    agent: AgentInfo
    message: str
    project_summary: dict[str, Any] | None = None
    options: list[str] | None = None  # Options proposées au user
    can_advance: bool = False  # User peut dire GO
    bolt_prompt: str | None = None  # Prompt final quand prêt


async def generate_agent_response(
    agent: AgentRole,
    phase: ConversationPhase,
    messages: list,
    project_context: str,
    system_prompt: str
) -> str:
    """Génère la réponse de l'agent via LLM"""
    import httpx

    # Format messages for LLM
    llm_messages = []
    for msg in messages[-10:]:  # Last 10 messages for context
        role = "user" if msg.role == "user" else "assistant"
        llm_messages.append({"role": role, "content": msg.content})

    # Try OpenAI
    if OPENAI_API_KEY:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            *llm_messages
                        ],
                        "max_tokens": 500,
                        "temperature": 0.8  # Plus créatif pour les conversations
                    }
                )
                if response.status_code == 200:
                    return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"[OpenAI] Error: {e}")

    # Try Anthropic
    if ANTHROPIC_API_KEY:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": ANTHROPIC_API_KEY,
                        "anthropic-version": "2023-06-01"
                    },
                    json={
                        "model": "claude-3-haiku-20240307",
                        "max_tokens": 500,
                        "system": system_prompt,
                        "messages": llm_messages
                    }
                )
                if response.status_code == 200:
                    return response.json()["content"][0]["text"]
        except Exception as e:
            print(f"[Anthropic] Error: {e}")

    # Fallback: greeting from agent
    persona = AGENT_PERSONAS.get(agent, {})
    return persona.get("greeting", f"Salut! Je suis {agent.value}. Comment puis-je t'aider?")


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    MULTI-AGENT CONVERSATIONAL CHAT

    Le user parle à UN agent à la fois.
    L'agent pose des questions, le user répond.
    On avance de phase en phase jusqu'à la génération.

    Flow:
    1. Orchestrator accueille
    2. Analyst brainstorme avec le user
    3. PM cadre le scope
    4. Architect propose la stack
    5. UX parle de l'expérience
    6. Orchestrator valide tout
    7. Archon crée le projet
    8. Orchestrator prépare Bolt
    9. Bolt génère après validation
    """

    # Detect language from user message
    lang = detect_language(req.message)

    # Get or create session
    session = None
    if req.session_id:
        session = conversation_manager.get_session(req.session_id)

    if not session:
        session = conversation_manager.create_session(req.user_id)
        session.language = lang  # Store detected language
        # Add FULL welcome message from IA Factory branding (in detected language)
        welcome = get_full_welcome_message(lang)
        session.add_message("agent", welcome, AgentRole.ORCHESTRATOR)

    # Add user message
    session.add_message("user", req.message)

    # Determine next phase and agent
    next_phase, next_agent = conversation_manager.determine_next_phase(session, req.message)

    # Check if we're transitioning to a new agent
    agent_changed = next_agent != session.active_agent
    phase_changed = next_phase != session.phase

    # Update session
    session.phase = next_phase
    session.active_agent = next_agent

    # Extract project info from conversation
    session.project = conversation_manager.extract_project_info_from_messages(session.messages)

    # Handle special phases
    if next_phase == CMPhase.CREATION:
        # Create project in Archon
        archon_result = await call_archon_create_project(session.project.__dict__)
        session.project.archon_project_id = archon_result["project_id"]
        session.phase = CMPhase.PREPARATION

        # Build bolt prompt
        session.project.bolt_prompt = conversation_manager.build_bolt_prompt(session.project)

        # Message de succès multilingue
        lang = session.language
        success_title = get_text(SUCCESS_MESSAGES["project_created"], lang)
        # Features text multilingue (5 langues)
        features_fallback = {
            'fr': 'À définir',
            'en': 'TBD',
            'ar': 'سيتم تحديدها',
            'dz': 'Rah ndéfiniwouha',
            'ber': 'ⴰⴷ ⵜⵜⵓⵙⵜⵉ'
        }
        features_text = ', '.join(session.project.features) if session.project.features else features_fallback.get(lang, 'À définir')

        response_message = f"""{success_title}

**ID:** {archon_result['project_id']}
**Type:** {session.project.type}
**Features:** {features_text}

{get_text(NEXUS_BRANDING['description'], lang)}

---
{session.project.bolt_prompt[:500]}...
---

**{
            {'fr': 'Tu valides ces instructions?',
             'en': 'Do you validate these instructions?',
             'ar': 'هل توافق على هذه التعليمات؟',
             'dz': 'Rak tvalidi had les instructions?',
             'ber': 'ⵜⵙⴼⵇⴷⴷ ⵉⵙⵓⵎⴰⵔ ⴰⴷ?'}.get(lang, 'Tu valides ces instructions?')
        }** (Oui / Modifier)"""

        session.add_message("agent", response_message, AgentRole.ORCHESTRATOR)

        return ChatResponse(
            session_id=session.id,
            phase=session.phase.value,
            agent=AgentInfo(**conversation_manager.get_agent_info(AgentRole.ORCHESTRATOR, lang)),
            message=response_message,
            project_summary=session.project.__dict__,
            bolt_prompt=session.project.bolt_prompt,
            can_advance=True
        )

    # Handle GENERATION phase
    if next_phase == CMPhase.GENERATION:
        # Message de génération multilingue
        lang = session.language
        code_gen_msg = get_text(SUCCESS_MESSAGES["code_generated"], lang)

        if lang == "ar":
            response_message = f"""{code_gen_msg}

أرسل التعليمات إلى Bolt لتوليد مشروعك.

سترى تطبيقك يتشكل!

---
*تم تحضير الأوامر. عند النقر على توليد، سيقوم Bolt بإنشاء الكود.*
---"""
        elif lang == "en":
            response_message = f"""{code_gen_msg}

Sending instructions to Bolt to generate your project.

You'll see your app come to life!

---
*The prompt is ready. When you click Generate, Bolt will create the code.*
---"""
        elif lang == "dz":
            response_message = f"""{code_gen_msg}

Rah nsifti les instructions l'Bolt bach ygénéri le projet ta3ek.

Rah tchouf l'app ta3ek tetshakkel!

---
*Le prompt jah. Ki tappuyi 3la Générer, Bolt rah ycréé le code.*
---"""
        elif lang == "ber":
            response_message = f"""{code_gen_msg}

ⴰⴷ ⵙⵙⵉⴼⴹⵖ ⵉⵙⵓⵎⴰⵔ ⵉ Bolt ⴰⴷ ⵉⵙⵙⴽⵔ ⴰⵙⴽⴰⵔ ⵏⵏⴽ.

ⴰⴷ ⵜⵥⵕⴷ ⴰⵙⵏⴼⴰⵔ ⵏⵏⴽ ⵉⵜⵜⵓⵙⴽⴰⵔ!

---
*ⵢⵓⵊⴰⴷ ⵓⵙⵓⵎⵔ. ⵎⴽ ⵜⴽⵍⵉⴽⵉⴷ ⵖⴼ "Générer", Bolt ⴰⴷ ⵉⵙⵙⴽⵔ ⵜⴰⵏⴳⴰⵍⵜ.*
---"""
        else:  # French default
            response_message = f"""{code_gen_msg}

J'envoie les instructions à Bolt pour générer ton projet.

Tu vas voir ton app prendre forme!

---
*Le prompt a été préparé. Quand tu cliques sur Générer, Bolt va créer le code.*
---"""

        session.add_message("agent", response_message, AgentRole.ORCHESTRATOR)

        return ChatResponse(
            session_id=session.id,
            phase=session.phase.value,
            agent=AgentInfo(**conversation_manager.get_agent_info(AgentRole.ORCHESTRATOR, lang)),
            message=response_message,
            project_summary=session.project.__dict__,
            bolt_prompt=session.project.bolt_prompt,
            can_advance=True
        )

    # Generate agent response
    # Use session language for prompts
    lang = session.language
    system_prompt = conversation_manager.get_phase_prompt(next_phase, next_agent, session.project, lang)

    # If agent changed, add a transition message
    transition_intro = ""
    if agent_changed and next_agent != AgentRole.ORCHESTRATOR:
        persona = AGENT_PERSONAS.get(next_agent, {})
        transition_intro = f"*{persona.get('name', next_agent.value)} entre dans la conversation*\n\n"

    agent_response = await generate_agent_response(
        next_agent,
        next_phase,
        session.messages,
        conversation_manager._format_project_context(session.project),
        system_prompt
    )

    # Prepend transition if needed
    if transition_intro:
        agent_response = transition_intro + agent_response

    session.add_message("agent", agent_response, next_agent)

    # Detect options in response
    options = None
    if any(marker in agent_response for marker in ["A)", "B)", "C)", "(A)", "(B)", "(C)", "Option A", "Option B"]):
        options = ["A", "B", "C"]

    # Can advance to next phase?
    can_advance = next_phase in [
        CMPhase.VALIDATION,
        CMPhase.PREPARATION,
    ]

    return ChatResponse(
        session_id=session.id,
        phase=session.phase.value,
        agent=AgentInfo(**conversation_manager.get_agent_info(next_agent, lang)),
        message=agent_response,
        project_summary=session.project.__dict__ if session.project else None,
        options=options,
        can_advance=can_advance
    )


@app.get("/chat/{session_id}")
async def get_chat_session(session_id: str):
    """Get chat session state"""
    session = conversation_manager.get_session(session_id)
    if not session:
        raise HTTPException(404, "Session not found")

    lang = session.language  # Use session language for agent titles
    return {
        "session_id": session.id,
        "phase": session.phase.value,
        "active_agent": conversation_manager.get_agent_info(session.active_agent, lang),
        "messages": [
            {
                "id": m.id,
                "role": m.role,
                "agent": conversation_manager.get_agent_info(m.agent, lang) if m.agent else None,
                "content": m.content,
                "timestamp": m.timestamp.isoformat()
            }
            for m in session.messages
        ],
        "project": session.project.__dict__ if session.project else None
    }


@app.delete("/chat/{session_id}")
async def delete_chat_session(session_id: str):
    """Delete a chat session"""
    deleted = conversation_manager.delete_session(session_id)
    if not deleted:
        raise HTTPException(404, "Session not found")
    return {"status": "deleted"}


@app.get("/agents")
async def list_agents():
    """Liste tous les agents disponibles avec leurs personnalités"""
    return {
        agent.value: {
            "name": info["name"],
            "title": info["title"],
            "avatar": info["avatar"],
            "personality": info["personality"],
        }
        for agent, info in AGENT_PERSONAS.items()
    }
