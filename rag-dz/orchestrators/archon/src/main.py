"""
Archon Orchestrator - Source de vérité KB + Tasks
Port: 8051
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .bridge import ArchonBridge, Document, Project, Task, SearchResult
from .supabase_bridge import SupabaseBridge
from .pg_bridge import PostgresBridge
from .sync import BMadSync, BoltSync, SyncResult, install_git_hook

# Configuration
ARCHON_URL = os.getenv("ARCHON_URL", "http://localhost:8181")
META_URL = os.getenv("META_URL", "http://localhost:8100")
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")
POSTGRES_URL = os.getenv("POSTGRES_URL", "")
USE_SUPABASE = os.getenv("USE_SUPABASE", "true").lower() == "true"
USE_POSTGRES = os.getenv("USE_POSTGRES", "true").lower() == "true"

# Clients globaux
archon_bridge: ArchonBridge | SupabaseBridge | PostgresBridge | None = None
bmad_sync: BMadSync | None = None
bolt_sync: BoltSync | None = None


def _is_valid_supabase_url(url: str) -> bool:
    """Check if URL is a real Supabase URL (not placeholder)"""
    return url and "supabase.co" in url and "your-project" not in url


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management"""
    global archon_bridge, bmad_sync, bolt_sync

    # Ordre de priorité:
    # 1. Supabase (cloud) si configuré avec vraies credentials
    # 2. PostgreSQL local si configuré
    # 3. Archon externe (fallback)

    if USE_SUPABASE and _is_valid_supabase_url(SUPABASE_URL) and SUPABASE_KEY:
        print(f"☁️ Connecting to Supabase: {SUPABASE_URL[:40]}...")
        archon_bridge = SupabaseBridge(SUPABASE_URL, SUPABASE_KEY)
    elif USE_POSTGRES and POSTGRES_URL:
        print(f"🐘 Connecting to PostgreSQL: {POSTGRES_URL[:40]}...")
        archon_bridge = PostgresBridge(POSTGRES_URL)
    else:
        print(f"🔗 Connecting to external Archon: {ARCHON_URL}")
        archon_bridge = ArchonBridge(ARCHON_URL)

    bmad_sync = BMadSync(ARCHON_URL)
    bolt_sync = BoltSync(ARCHON_URL)
    yield
    if archon_bridge:
        await archon_bridge.close()


app = FastAPI(
    title="Nexus Archon Orchestrator",
    description="Source de vérité pour Knowledge Base et Task Management",
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

class SearchRequest(BaseModel):
    query: str
    filters: dict | None = None
    limit: int = 10


class IngestRequest(BaseModel):
    content: str
    type: str
    metadata: dict | None = None


class SyncBmadRequest(BaseModel):
    path: str
    force: bool = False


class SyncBoltRequest(BaseModel):
    repo_path: str
    commit_sha: str | None = None


class InstallHookRequest(BaseModel):
    repo_path: str


# ============ HEALTH ============

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Nexus Archon Orchestrator",
        "version": "1.0.0",
        "archon_url": ARCHON_URL,
        "endpoints": {
            "health": "/health",
            "search": "/search",
            "ingest": "/ingest",
            "sync": "/sync"
        }
    }


@app.get("/health")
async def health():
    """Health check avec statut Archon"""
    archon_status = "disconnected"
    if archon_bridge:
        health_result = await archon_bridge.health()
        archon_status = health_result.get("status", "unknown")

    return {
        "status": "healthy" if archon_status == "healthy" else "degraded",
        "service": "archon-orchestrator",
        "version": "1.0.0",
        "archon": archon_status
    }


# ============ KNOWLEDGE BASE ============

@app.post("/search", response_model=list[SearchResult])
async def search(req: SearchRequest):
    """Recherche dans la Knowledge Base"""
    if not archon_bridge:
        raise HTTPException(503, "Archon bridge not initialized")

    return await archon_bridge.search(req.query, req.filters, req.limit)


@app.post("/ingest", response_model=Document)
async def ingest(req: IngestRequest):
    """Ingère un document dans la KB"""
    if not archon_bridge:
        raise HTTPException(503, "Archon bridge not initialized")

    return await archon_bridge.ingest(req.content, req.type, req.metadata)


@app.get("/documents/{doc_id}", response_model=Document)
async def get_document(doc_id: str):
    """Récupère un document"""
    if not archon_bridge:
        raise HTTPException(503, "Archon bridge not initialized")

    doc = await archon_bridge.get_document(doc_id)
    if not doc:
        raise HTTPException(404, "Document not found")
    return doc


@app.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    """Supprime un document"""
    if not archon_bridge:
        raise HTTPException(503, "Archon bridge not initialized")

    deleted = await archon_bridge.delete_document(doc_id)
    if not deleted:
        raise HTTPException(404, "Document not found")
    return {"status": "deleted"}


# ============ PROJECTS ============

@app.get("/projects", response_model=list[Project])
async def list_projects(status: str | None = None):
    """Liste les projets"""
    if not archon_bridge:
        raise HTTPException(503, "Archon bridge not initialized")

    return await archon_bridge.list_projects(status)


@app.post("/projects", response_model=Project)
async def create_project(name: str, description: str):
    """Crée un projet"""
    if not archon_bridge:
        raise HTTPException(503, "Archon bridge not initialized")

    return await archon_bridge.create_project(name, description)


@app.get("/projects/{project_id}", response_model=Project)
async def get_project(project_id: str):
    """Récupère un projet"""
    if not archon_bridge:
        raise HTTPException(503, "Archon bridge not initialized")

    project = await archon_bridge.get_project(project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    return project


# ============ TASKS ============

@app.get("/projects/{project_id}/tasks", response_model=list[Task])
async def list_tasks(project_id: str, status: str | None = None):
    """Liste les tâches d'un projet"""
    if not archon_bridge:
        raise HTTPException(503, "Archon bridge not initialized")

    return await archon_bridge.list_tasks(project_id, status)


@app.post("/projects/{project_id}/tasks", response_model=Task)
async def create_task(
    project_id: str,
    title: str,
    description: str,
    assignee: str | None = None,
    priority: int = 0
):
    """Crée une tâche"""
    if not archon_bridge:
        raise HTTPException(503, "Archon bridge not initialized")

    return await archon_bridge.create_task(
        project_id, title, description, assignee, priority
    )


@app.patch("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, status: str | None = None, assignee: str | None = None):
    """Met à jour une tâche (Archon = source de vérité)"""
    if not archon_bridge:
        raise HTTPException(503, "Archon bridge not initialized")

    updates = {}
    if status:
        updates["status"] = status
    if assignee:
        updates["assignee"] = assignee

    task = await archon_bridge.update_task(task_id, **updates)
    if not task:
        raise HTTPException(404, "Task not found")
    return task


# ============ SYNC ============

@app.post("/sync/bmad", response_model=dict)
async def sync_bmad(req: SyncBmadRequest, background_tasks: BackgroundTasks):
    """Synchronise les artefacts BMAD vers la KB"""
    if not bmad_sync:
        raise HTTPException(503, "BMAD sync not initialized")

    # Exécuter en background pour ne pas bloquer
    async def do_sync():
        return await bmad_sync.sync_artifacts(req.path, req.force)

    background_tasks.add_task(do_sync)
    return {"status": "sync_started", "path": req.path}


@app.post("/sync/bolt", response_model=SyncResult)
async def sync_bolt(req: SyncBoltRequest):
    """Synchronise les fichiers modifiés d'un commit"""
    if not bolt_sync:
        raise HTTPException(503, "Bolt sync not initialized")

    return await bolt_sync.sync_commit(req.repo_path, req.commit_sha)


@app.post("/sync/install-hook")
async def install_hook(req: InstallHookRequest):
    """Installe le hook post-commit Git"""
    success = install_git_hook(req.repo_path)
    if not success:
        raise HTTPException(500, "Failed to install hook")
    return {"status": "installed", "repo": req.repo_path}


@app.post("/sync/directory")
async def sync_directory(
    directory: str,
    patterns: list[str] | None = None,
    source: str = "manual"
):
    """Synchronise un répertoire complet vers la KB"""
    if not archon_bridge:
        raise HTTPException(503, "Archon bridge not initialized")

    count = await archon_bridge.sync_directory(directory, patterns, source)
    return {"synced": count, "directory": directory}
