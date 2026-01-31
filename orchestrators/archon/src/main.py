"""
Archon Orchestrator - Source de vérité KB + Tasks
Port: 8051

Support multilingue: Arabe (ar), Français (fr), Anglais (en)
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks, Query, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .bridge import ArchonBridge, Document, Project, Task, SearchResult
from .supabase_bridge import SupabaseBridge
from .pg_bridge import PostgresBridge
from .sync import BMadSync, BoltSync, SyncResult, install_git_hook
from .branding import (
    ARCHON_BRANDING,
    get_text,
    get_agent_info,
    get_all_agents,
    get_status_label,
    get_error_message,
    get_success_message,
    get_ui_label,
    detect_language,
    get_theme,
    ARCHON_AGENTS,
)

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
        print(f"[CLOUD] Connecting to Supabase: {SUPABASE_URL[:40]}...")
        archon_bridge = SupabaseBridge(SUPABASE_URL, SUPABASE_KEY)
    elif USE_POSTGRES and POSTGRES_URL:
        print(f"[PG] Connecting to PostgreSQL: {POSTGRES_URL[:40]}...")
        archon_bridge = PostgresBridge(POSTGRES_URL)
    else:
        print(f"[LINK] Connecting to external Archon: {ARCHON_URL}")
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


# ============ LANGUAGE HELPERS ============

def get_lang(
    accept_language: str | None = None,
    lang_param: str | None = None
) -> str:
    """
    Détermine la langue à utiliser.
    Priorité: paramètre > header > défaut (fr)
    """
    if lang_param and lang_param in ["ar", "fr", "en", "dz", "ber"]:
        return lang_param
    if accept_language:
        # Parse Accept-Language header
        for part in accept_language.split(","):
            lang = part.split(";")[0].strip().lower()
            if lang.startswith("ar"):
                return "ar"
            if lang.startswith("fr"):
                return "fr"
            if lang.startswith("en"):
                return "en"
    return "fr"  # Défaut: français


# ============ HEALTH ============

@app.get("/")
async def root(
    lang: str | None = Query(None, description="Language: ar, fr, en"),
    accept_language: str | None = Header(None, alias="Accept-Language")
):
    """Root endpoint - Multilingue"""
    current_lang = get_lang(accept_language, lang)

    return {
        "service": get_text(ARCHON_BRANDING["title"], current_lang),
        "description": get_text(ARCHON_BRANDING["description"], current_lang),
        "version": ARCHON_BRANDING["version"],
        "language": current_lang,
        "archon_url": ARCHON_URL,
        "endpoints": {
            "health": "/health",
            "search": "/search",
            "ingest": "/ingest",
            "sync": "/sync",
            "agents": "/agents",
            "i18n": "/i18n/{key}",
        },
        "supported_languages": ["ar", "fr", "en", "dz", "ber"],
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


# ============ AGENTS (i18n) ============

@app.get("/agents")
async def list_agents(
    lang: str | None = Query(None, description="Language: ar, fr, en"),
    accept_language: str | None = Header(None, alias="Accept-Language")
):
    """
    Liste tous les agents Archon avec noms localisés.

    Returns:
        Liste des agents avec nom, titre, avatar en langue demandée
    """
    current_lang = get_lang(accept_language, lang)
    return {
        "agents": get_all_agents(current_lang),
        "language": current_lang,
        "count": len(ARCHON_AGENTS),
    }


@app.get("/agents/{agent_id}")
async def get_agent(
    agent_id: str,
    lang: str | None = Query(None, description="Language: ar, fr, en"),
    accept_language: str | None = Header(None, alias="Accept-Language")
):
    """
    Récupère un agent spécifique avec informations localisées.
    """
    current_lang = get_lang(accept_language, lang)
    agent = get_agent_info(agent_id, current_lang)

    if agent["name"] == agent_id and agent_id not in ARCHON_AGENTS:
        raise HTTPException(404, get_error_message("not_found", current_lang))

    return {
        "agent": agent,
        "language": current_lang,
    }


# ============ I18N ============

@app.get("/i18n/labels")
async def get_labels(
    lang: str | None = Query(None, description="Language: ar, fr, en"),
    accept_language: str | None = Header(None, alias="Accept-Language")
):
    """
    Récupère tous les labels UI dans la langue spécifiée.
    """
    from .branding import UI_LABELS
    current_lang = get_lang(accept_language, lang)

    return {
        "labels": {key: get_ui_label(key, current_lang) for key in UI_LABELS},
        "language": current_lang,
    }


@app.get("/i18n/statuses")
async def get_statuses(
    lang: str | None = Query(None, description="Language: ar, fr, en"),
    accept_language: str | None = Header(None, alias="Accept-Language")
):
    """
    Récupère les labels de statuts dans la langue spécifiée.
    """
    from .branding import TASK_STATUS_LABELS, PROJECT_STATUS_LABELS
    current_lang = get_lang(accept_language, lang)

    return {
        "task_statuses": {
            key: get_status_label(key, "task", current_lang)
            for key in TASK_STATUS_LABELS
        },
        "project_statuses": {
            key: get_status_label(key, "project", current_lang)
            for key in PROJECT_STATUS_LABELS
        },
        "language": current_lang,
    }


@app.get("/i18n/messages")
async def get_messages(
    lang: str | None = Query(None, description="Language: ar, fr, en"),
    accept_language: str | None = Header(None, alias="Accept-Language")
):
    """
    Récupère les messages (erreurs + succès) dans la langue spécifiée.
    """
    from .branding import ERROR_MESSAGES, SUCCESS_MESSAGES
    current_lang = get_lang(accept_language, lang)

    return {
        "errors": {
            key: get_error_message(key, current_lang)
            for key in ERROR_MESSAGES
        },
        "success": {
            key: get_success_message(key, current_lang)
            for key in SUCCESS_MESSAGES
        },
        "language": current_lang,
    }


# ============ THEME ============

@app.get("/theme/{mode}")
async def get_theme_config(mode: str = "light"):
    """
    Récupère la configuration du thème (light/dark).
    """
    if mode not in ["light", "dark"]:
        mode = "light"

    return {
        "mode": mode,
        "colors": get_theme(mode),
    }


@app.get("/theme")
async def list_themes():
    """
    Liste les thèmes disponibles.
    """
    return {
        "themes": ["light", "dark"],
        "default": "light",
        "light": get_theme("light"),
        "dark": get_theme("dark"),
    }
