"""
Voice Bridge - Connecte le Voice Agent a n8n
====================================================
Ce service ecoute les commandes vocales et declenche les workflows n8n.
"""

import os
import httpx
import redis.asyncio as redis
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
from datetime import datetime
import json

# Configuration
VOICE_AGENT_URL = os.getenv("VOICE_AGENT_URL", "http://localhost:8205")
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook")
N8N_API_KEY = os.getenv("N8N_API_KEY", "")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/3")
PORT = int(os.getenv("PORT", 8223))

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("voice-bridge")

# FastAPI App
app = FastAPI(
    title="IAFactory Voice Bridge",
    description="Connecte le Voice Agent aux workflows n8n",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis client
redis_client: Optional[redis.Redis] = None

# ==============================================
# MODELS
# ==============================================

class VoiceCommand(BaseModel):
    """Commande vocale recue du Voice Agent"""
    session_id: str
    user_id: Optional[str] = None
    command: str
    intent: str
    entities: Dict[str, Any] = {}
    confidence: float = 0.0
    language: str = "fr"
    timestamp: Optional[str] = None

class N8NTrigger(BaseModel):
    """Declencheur pour n8n workflow"""
    workflow_name: str
    data: Dict[str, Any] = {}
    session_id: Optional[str] = None

class ActionResult(BaseModel):
    """Resultat d'une action n8n"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

# ==============================================
# INTENT TO N8N WORKFLOW MAPPING
# ==============================================

INTENT_WORKFLOWS = {
    # Email
    "send_email": "voice-send-email",
    "check_email": "voice-check-email",
    "reply_email": "voice-reply-email",

    # Calendar
    "create_event": "voice-create-event",
    "check_calendar": "voice-check-calendar",
    "reschedule_event": "voice-reschedule-event",

    # Tasks
    "create_task": "voice-create-task",
    "list_tasks": "voice-list-tasks",
    "complete_task": "voice-complete-task",

    # Finance
    "check_budget": "voice-check-budget",
    "add_expense": "voice-add-expense",
    "financial_report": "voice-financial-report",

    # Legal
    "contract_review": "voice-contract-review",
    "legal_search": "voice-legal-search",

    # Travel
    "book_travel": "voice-book-travel",
    "check_flights": "voice-check-flights",

    # Web Search
    "web_search": "voice-web-search",
    "scrape_url": "voice-scrape-url",

    # General
    "help": "voice-help",
    "status": "voice-status"
}

# ==============================================
# STARTUP / SHUTDOWN
# ==============================================

@app.on_event("startup")
async def startup():
    """Connexion Redis au demarrage"""
    global redis_client
    try:
        redis_client = redis.from_url(REDIS_URL, decode_responses=True)
        await redis_client.ping()
        logger.info(f"Connected to Redis: {REDIS_URL}")
    except Exception as e:
        logger.warning(f"Redis connection failed: {e}. Continuing without cache.")
        redis_client = None

@app.on_event("shutdown")
async def shutdown():
    """Fermeture Redis"""
    global redis_client
    if redis_client:
        await redis_client.close()

# ==============================================
# ENDPOINTS
# ==============================================

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "service": "voice-bridge",
        "version": "1.0.0",
        "n8n_url": N8N_WEBHOOK_URL,
        "voice_agent_url": VOICE_AGENT_URL,
        "redis_connected": redis_client is not None
    }

@app.post("/voice/command", response_model=ActionResult)
async def handle_voice_command(
    command: VoiceCommand,
    background_tasks: BackgroundTasks
):
    """
    Recoit une commande vocale et declenche le workflow n8n correspondant
    """
    logger.info(f"Voice command received: {command.intent} - {command.command}")

    # Trouver le workflow correspondant
    workflow_name = INTENT_WORKFLOWS.get(command.intent)

    if not workflow_name:
        # Intent non reconnu - utiliser le workflow generique
        workflow_name = "voice-generic-command"
        logger.warning(f"Unknown intent: {command.intent}, using generic workflow")

    # Construire le payload pour n8n
    payload = {
        "session_id": command.session_id,
        "user_id": command.user_id,
        "command": command.command,
        "intent": command.intent,
        "entities": command.entities,
        "confidence": command.confidence,
        "language": command.language,
        "timestamp": command.timestamp or datetime.utcnow().isoformat()
    }

    # Sauvegarder en cache si Redis disponible
    if redis_client:
        try:
            cache_key = f"voice:session:{command.session_id}"
            await redis_client.setex(
                cache_key,
                3600,  # 1 heure TTL
                json.dumps(payload)
            )
        except Exception as e:
            logger.warning(f"Redis cache error: {e}")

    # Declencher le workflow n8n
    try:
        result = await trigger_n8n_workflow(workflow_name, payload)
        return ActionResult(
            success=True,
            message=f"Workflow '{workflow_name}' triggered",
            data=result
        )
    except Exception as e:
        logger.error(f"N8N trigger failed: {e}")
        return ActionResult(
            success=False,
            message=f"Failed to trigger workflow: {str(e)}"
        )

@app.post("/n8n/trigger", response_model=ActionResult)
async def trigger_workflow(trigger: N8NTrigger):
    """
    Declenche un workflow n8n specifique
    """
    try:
        result = await trigger_n8n_workflow(trigger.workflow_name, trigger.data)
        return ActionResult(
            success=True,
            message=f"Workflow '{trigger.workflow_name}' triggered",
            data=result
        )
    except Exception as e:
        return ActionResult(
            success=False,
            message=f"Failed: {str(e)}"
        )

@app.get("/workflows")
async def list_workflows():
    """Liste des workflows disponibles"""
    return {
        "workflows": INTENT_WORKFLOWS,
        "total": len(INTENT_WORKFLOWS)
    }

@app.get("/session/{session_id}")
async def get_session(session_id: str):
    """Recupere les infos de session"""
    if not redis_client:
        raise HTTPException(status_code=503, detail="Redis not available")

    cache_key = f"voice:session:{session_id}"
    data = await redis_client.get(cache_key)

    if not data:
        raise HTTPException(status_code=404, detail="Session not found")

    return json.loads(data)

# ==============================================
# N8N INTEGRATION
# ==============================================

async def trigger_n8n_workflow(
    workflow_name: str,
    data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Declenche un workflow n8n via webhook
    """
    webhook_url = f"{N8N_WEBHOOK_URL}/{workflow_name}"

    headers = {
        "Content-Type": "application/json"
    }

    if N8N_API_KEY:
        headers["Authorization"] = f"Bearer {N8N_API_KEY}"

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            webhook_url,
            json=data,
            headers=headers
        )

        if response.status_code >= 400:
            raise Exception(f"N8N error: {response.status_code} - {response.text}")

        try:
            return response.json()
        except:
            return {"raw_response": response.text}

# ==============================================
# FIRECRAWL INTEGRATION
# ==============================================

FIRECRAWL_URL = os.getenv("FIRECRAWL_URL", "http://iaf-firecrawl:3002")

@app.post("/scrape")
async def scrape_url(url: str, formats: list = ["markdown"]):
    """
    Utilise Firecrawl pour scrapper une URL
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{FIRECRAWL_URL}/v0/scrape",
            json={
                "url": url,
                "formats": formats
            }
        )

        if response.status_code >= 400:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Firecrawl error: {response.text}"
            )

        return response.json()

@app.post("/crawl")
async def crawl_site(url: str, max_pages: int = 10):
    """
    Crawle un site entier avec Firecrawl
    """
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{FIRECRAWL_URL}/v0/crawl",
            json={
                "url": url,
                "limit": max_pages,
                "scrapeOptions": {
                    "formats": ["markdown"]
                }
            }
        )

        if response.status_code >= 400:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Firecrawl error: {response.text}"
            )

        return response.json()

# ==============================================
# MAIN
# ==============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
