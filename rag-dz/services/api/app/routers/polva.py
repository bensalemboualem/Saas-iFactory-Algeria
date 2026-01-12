"""
POLVA SuperAgent API Router
============================
API endpoints for the Polyvalent Omniscient Learning Virtual Assistant

POLVA is the ultimate orchestrator that can:
- Route to any agent in the system
- Execute multi-agent workflows
- Make executive decisions
- Learn from all interactions
"""
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field

from app.dependencies import get_current_user, optional_user
from app.services.super_agent_polva import (
    get_polva,
    SuperAgentPOLVA,
    POLVAMode,
    TaskPriority,
    POLVAResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/polva", tags=["POLVA SuperAgent"])


# ============================================
# REQUEST/RESPONSE MODELS
# ============================================

class POLVAQueryRequest(BaseModel):
    """Request for POLVA processing"""
    query: str = Field(..., min_length=1, max_length=5000, description="User query")
    mode: Optional[str] = Field("auto", description="Mode: auto, executive, orchestrator, assistant, analyst, developer, support, creative")
    priority: Optional[str] = Field("medium", description="Priority: critical, high, medium, low")
    session_id: Optional[str] = Field(None, description="Session ID for context continuity")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")
    language: Optional[str] = Field("fr", description="Response language: fr, ar, en")


class POLVAQueryResponse(BaseModel):
    """Response from POLVA"""
    answer: str = Field(..., description="POLVA's response")
    confidence: float = Field(..., description="Confidence score 0-1")
    agents_used: List[str] = Field(default_factory=list, description="Agents involved")
    mode: str = Field(..., description="Operating mode used")
    suggestions: List[str] = Field(default_factory=list, description="Follow-up suggestions")
    actions_taken: List[Dict[str, Any]] = Field(default_factory=list, description="Actions performed")
    memory_updated: bool = Field(False, description="Whether memory was updated")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class AgentListResponse(BaseModel):
    """List of available agents"""
    agents: Dict[str, List[str]] = Field(..., description="Agents grouped by category")
    total: int = Field(..., description="Total number of agents")


class StatsResponse(BaseModel):
    """POLVA statistics"""
    version: str
    name: str
    total_agents: int
    memory_enabled: bool
    voice_enabled: bool
    active_tasks: int
    completed_tasks: int


# ============================================
# MAIN ENDPOINTS
# ============================================

@router.post("/query", response_model=POLVAQueryResponse)
async def process_query(
    request: POLVAQueryRequest,
    current_user: dict = Depends(optional_user),
):
    """
    Process a query with POLVA SuperAgent.

    POLVA will:
    1. Analyze your query
    2. Route to the best agent(s)
    3. Execute the task
    4. Return a comprehensive response

    Modes:
    - auto: Automatic mode detection
    - executive: High-level decision making
    - orchestrator: Multi-agent coordination
    - assistant: Personal assistant
    - analyst: Data analysis
    - developer: Code generation
    - support: Customer support
    - creative: Creative tasks
    """
    polva = get_polva()

    # Map mode string to enum
    mode_map = {
        "auto": POLVAMode.AUTO,
        "executive": POLVAMode.EXECUTIVE,
        "orchestrator": POLVAMode.ORCHESTRATOR,
        "assistant": POLVAMode.ASSISTANT,
        "analyst": POLVAMode.ANALYST,
        "developer": POLVAMode.DEVELOPER,
        "support": POLVAMode.SUPPORT,
        "creative": POLVAMode.CREATIVE,
    }
    mode = mode_map.get(request.mode, POLVAMode.AUTO)

    # Map priority
    priority_map = {
        "critical": TaskPriority.CRITICAL,
        "high": TaskPriority.HIGH,
        "medium": TaskPriority.MEDIUM,
        "low": TaskPriority.LOW,
    }
    priority = priority_map.get(request.priority, TaskPriority.MEDIUM)

    # Get user ID if authenticated
    user_id = None
    if current_user:
        user_id = current_user.get("id") or current_user.get("email")

    try:
        response = await polva.process(
            query=request.query,
            user_id=user_id,
            session_id=request.session_id,
            mode=mode,
            context=request.context,
            priority=priority,
        )

        return POLVAQueryResponse(
            answer=response.answer,
            confidence=response.confidence,
            agents_used=response.agents_used,
            mode=response.mode.value if hasattr(response.mode, 'value') else str(response.mode),
            suggestions=response.suggestions,
            actions_taken=response.actions_taken,
            memory_updated=response.memory_updated,
            metadata=response.metadata,
        )

    except Exception as e:
        logger.error(f"POLVA query error: {e}")
        raise HTTPException(status_code=500, detail=f"POLVA processing failed: {str(e)}")


@router.post("/chat")
async def chat(
    message: str = Query(..., description="Chat message"),
    session_id: Optional[str] = Query(None, description="Session ID"),
    current_user: dict = Depends(optional_user),
):
    """
    Simple chat interface with POLVA.
    Shortcut for /query with auto mode.
    """
    polva = get_polva()

    user_id = None
    if current_user:
        user_id = current_user.get("id") or current_user.get("email")

    response = await polva.process(
        query=message,
        user_id=user_id,
        session_id=session_id,
        mode=POLVAMode.AUTO,
    )

    return {
        "response": response.answer,
        "agents": response.agents_used,
        "suggestions": response.suggestions,
    }


@router.post("/executive")
async def executive_decision(
    query: str = Query(..., description="Decision query"),
    priority: str = Query("high", description="Priority level"),
    current_user: dict = Depends(get_current_user),
):
    """
    Make an executive-level decision.
    Requires authentication.
    """
    polva = get_polva()

    user_id = current_user.get("id") or current_user.get("email")

    priority_map = {
        "critical": TaskPriority.CRITICAL,
        "high": TaskPriority.HIGH,
        "medium": TaskPriority.MEDIUM,
        "low": TaskPriority.LOW,
    }

    response = await polva.process(
        query=query,
        user_id=user_id,
        mode=POLVAMode.EXECUTIVE,
        priority=priority_map.get(priority, TaskPriority.HIGH),
    )

    return {
        "decision": response.answer,
        "confidence": response.confidence,
        "agents_consulted": response.agents_used,
        "suggestions": response.suggestions,
    }


@router.post("/orchestrate")
async def orchestrate_task(
    request: POLVAQueryRequest,
    current_user: dict = Depends(get_current_user),
):
    """
    Orchestrate multiple agents for a complex task.
    Requires authentication.
    """
    polva = get_polva()

    user_id = current_user.get("id") or current_user.get("email")

    response = await polva.process(
        query=request.query,
        user_id=user_id,
        session_id=request.session_id,
        mode=POLVAMode.ORCHESTRATOR,
        context=request.context,
    )

    return {
        "result": response.answer,
        "agents_orchestrated": response.agents_used,
        "actions": response.actions_taken,
        "confidence": response.confidence,
    }


# ============================================
# AGENT DISCOVERY
# ============================================

@router.get("/agents", response_model=AgentListResponse)
async def list_agents():
    """
    List all agents available through POLVA.
    """
    polva = get_polva()
    agents = polva.get_available_agents()

    return AgentListResponse(
        agents=agents,
        total=sum(len(v) for v in agents.values())
    )


@router.get("/agents/{category}")
async def list_agents_by_category(category: str):
    """
    List agents in a specific category.

    Categories: bmad, voice, rag, legal, finance, medical, business, education, saas, productivity
    """
    polva = get_polva()
    agents = polva.get_available_agents()

    if category not in agents:
        raise HTTPException(status_code=404, detail=f"Category '{category}' not found")

    return {
        "category": category,
        "agents": agents[category],
        "count": len(agents[category])
    }


@router.get("/route")
async def route_query(
    query: str = Query(..., description="Query to route"),
):
    """
    Preview which agent(s) would handle a query without executing.
    """
    polva = get_polva()
    routes = polva.router.route(query)

    return {
        "query": query,
        "routes": [
            {"agent": agent_id, "confidence": conf}
            for agent_id, conf in routes
        ],
        "primary_agent": routes[0][0] if routes else None,
    }


# ============================================
# MODES
# ============================================

@router.get("/modes")
async def list_modes():
    """
    List available POLVA operating modes.
    """
    return {
        "modes": [
            {
                "id": "auto",
                "name": "Automatique",
                "description": "POLVA détecte automatiquement le meilleur mode",
            },
            {
                "id": "executive",
                "name": "Exécutif",
                "description": "Prise de décisions de haut niveau",
            },
            {
                "id": "orchestrator",
                "name": "Orchestrateur",
                "description": "Coordination multi-agents",
            },
            {
                "id": "assistant",
                "name": "Assistant",
                "description": "Assistant personnel",
            },
            {
                "id": "analyst",
                "name": "Analyste",
                "description": "Analyse de données",
            },
            {
                "id": "developer",
                "name": "Développeur",
                "description": "Génération de code",
            },
            {
                "id": "support",
                "name": "Support",
                "description": "Support client",
            },
            {
                "id": "creative",
                "name": "Créatif",
                "description": "Tâches créatives",
            },
        ]
    }


# ============================================
# HEALTH & STATS
# ============================================

@router.get("/health")
async def health_check():
    """
    Check POLVA health status.
    """
    polva = get_polva()
    return await polva.health_check()


@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    """
    Get POLVA statistics.
    """
    polva = get_polva()
    stats = polva.get_stats()
    return StatsResponse(**stats)


@router.get("/")
async def polva_info():
    """
    POLVA SuperAgent information.
    """
    polva = get_polva()
    stats = polva.get_stats()

    return {
        "name": "POLVA",
        "full_name": "Polyvalent Omniscient Learning Virtual Assistant",
        "version": stats["version"],
        "description": "SuperAgent orchestrateur avec accès à tous les agents IAFactory",
        "capabilities": [
            "Routing intelligent vers 70+ agents",
            "Mémoire persistante multi-session",
            "Orchestration multi-agents",
            "Prise de décision executive",
            "Support multilingue (AR/FR/EN/Darija)",
            "Intégration vocale (STT/TTS/NLP)",
        ],
        "endpoints": {
            "/query": "Traitement principal des requêtes",
            "/chat": "Interface chat simplifiée",
            "/executive": "Décisions de haut niveau",
            "/orchestrate": "Coordination multi-agents",
            "/agents": "Liste des agents disponibles",
            "/route": "Preview du routing",
        },
        "stats": stats,
    }
