"""
MCP Router - Model Context Protocol API Endpoints
Exposes MCP functionality for Bolt, Archon, BMAD, and all IAFactory apps

Endpoints:
- Tool discovery and execution
- Agent communication
- Workflow orchestration
- Context management
- Real-time events (SSE)
"""
import asyncio
import json
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, Query, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.dependencies import get_current_user
from app.mcp import mcp_server, mcp_registry, MCPAgent, MCPMessage, MCPMessageType

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/mcp", tags=["MCP - Model Context Protocol"])


# ================================================
# REQUEST/RESPONSE MODELS
# ================================================

class ToolCallRequest(BaseModel):
    """Request to call an MCP tool"""
    tool: str
    parameters: Dict[str, Any] = {}
    session_id: Optional[str] = None


class AgentMessageRequest(BaseModel):
    """Request to send message to an agent"""
    agent: str
    message: str
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class WorkflowStartRequest(BaseModel):
    """Request to start a workflow"""
    workflow: str
    project_name: str
    description: str
    agents: Optional[List[str]] = None
    config: Optional[Dict[str, Any]] = None


class HandoffRequest(BaseModel):
    """Request to handoff between agents"""
    from_agent: str
    to_agent: str
    session_id: str
    data: Dict[str, Any] = {}


# ================================================
# DISCOVERY ENDPOINTS
# ================================================

@router.get("/registry")
async def get_registry(current_user: dict = Depends(get_current_user)):
    """
    Get complete MCP registry

    Returns all registered apps, agents, and workflows
    """
    mcp_registry.initialize()
    return mcp_registry.to_dict()


@router.get("/apps")
async def list_apps(
    category: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    List all registered applications

    Filter by category: media, business, legal, finance, productivity, etc.
    """
    mcp_registry.initialize()

    from app.mcp.registry import AppCategory

    if category:
        try:
            cat = AppCategory(category)
            apps = mcp_registry.list_apps(cat)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
    else:
        apps = mcp_registry.list_apps()

    return {
        "apps": [
            {
                "id": k,
                "name": v.name,
                "category": v.category.value,
                "description": v.description,
                "tools": v.tools,
                "port": v.port,
                "active": v.active
            }
            for k, v in mcp_registry.apps.items()
            if not category or v.category.value == category
        ],
        "total": len(apps),
        "categories": [c.value for c in AppCategory]
    }


@router.get("/agents")
async def list_agents(
    agent_type: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    List all registered agents

    Filter by type: bmad, rag, business, finance, legal, productivity, etc.
    """
    mcp_registry.initialize()

    from app.mcp.registry import AgentType

    if agent_type:
        try:
            at = AgentType(agent_type)
            agents = mcp_registry.list_agents(at)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid agent type: {agent_type}")
    else:
        agents = mcp_registry.list_agents()

    return {
        "agents": [
            {
                "id": k,
                "name": v.name,
                "type": v.agent_type.value,
                "description": v.description,
                "model": v.model,
                "capabilities": v.capabilities,
                "tools": v.tools
            }
            for k, v in mcp_registry.agents.items()
            if not agent_type or v.agent_type.value == agent_type
        ],
        "total": len(agents),
        "types": [t.value for t in AgentType]
    }


@router.get("/workflows")
async def list_workflows(current_user: dict = Depends(get_current_user)):
    """
    List all registered workflows
    """
    mcp_registry.initialize()

    return {
        "workflows": [
            {
                "id": k,
                "name": v.name,
                "description": v.description,
                "stages": v.stages,
                "agents_involved": v.agents_involved
            }
            for k, v in mcp_registry.workflows.items()
        ],
        "total": len(mcp_registry.workflows)
    }


@router.get("/tools")
async def list_tools(
    agent: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    List all available MCP tools

    Filter by agent: bolt, archon, bmad_pm, bmad_architect, etc.
    """
    mcp_registry.initialize()

    if agent:
        try:
            mcp_agent = MCPAgent(agent)
            tools = mcp_server.get_tools(mcp_agent)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid agent: {agent}")
    else:
        tools = mcp_server.get_tools()

    return {
        "tools": [t.to_dict() for t in tools],
        "total": len(tools),
        "agents": [a.value for a in MCPAgent]
    }


# ================================================
# TOOL EXECUTION
# ================================================

@router.post("/tools/call")
async def call_tool(
    request: ToolCallRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Call an MCP tool

    Example:
    ```json
    {
        "tool": "bmad_brainstorm",
        "parameters": {
            "project_name": "E-commerce DZ",
            "description": "Plateforme e-commerce pour l'Algérie"
        }
    }
    ```
    """
    mcp_registry.initialize()

    tool = mcp_server.get_tool(request.tool)
    if not tool:
        raise HTTPException(status_code=404, detail=f"Tool not found: {request.tool}")

    try:
        result = await mcp_server.call_tool(
            tool_name=request.tool,
            parameters=request.parameters,
            source=MCPAgent.ORCHESTRATOR,
            session_id=request.session_id
        )

        return {
            "tool": request.tool,
            "result": result,
            "session_id": request.session_id,
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"Tool call error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ================================================
# AGENT COMMUNICATION
# ================================================

@router.post("/agents/message")
async def send_agent_message(
    request: AgentMessageRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Send a message to an MCP agent

    Available agents:
    - bolt: Code generation
    - archon: Knowledge base
    - bmad_pm, bmad_architect, bmad_developer, bmad_analyst, bmad_tester: BMAD team
    - orchestrator: Workflow coordination
    """
    mcp_registry.initialize()

    # Map agent string to MCPAgent
    agent_mapping = {
        "bolt": MCPAgent.BOLT,
        "archon": MCPAgent.ARCHON,
        "bmad_pm": MCPAgent.BMAD_PM,
        "bmad_architect": MCPAgent.BMAD_ARCHITECT,
        "bmad_developer": MCPAgent.BMAD_DEVELOPER,
        "bmad_analyst": MCPAgent.BMAD_ANALYST,
        "bmad_tester": MCPAgent.BMAD_TESTER,
        "orchestrator": MCPAgent.ORCHESTRATOR,
        "rag": MCPAgent.RAG,
    }

    target_agent = agent_mapping.get(request.agent)
    if not target_agent:
        raise HTTPException(status_code=400, detail=f"Unknown agent: {request.agent}")

    try:
        message = MCPMessage(
            id=None,
            type=MCPMessageType.TOOL_CALL,
            source=MCPAgent.ORCHESTRATOR,
            target=target_agent,
            payload={
                "message": request.message,
                "context": request.context or {},
                "session_id": request.session_id
            }
        )

        response = await mcp_server.send_message(message)

        return {
            "agent": request.agent,
            "response": response.payload if response else None,
            "session_id": request.session_id,
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"Agent message error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agents/handoff")
async def agent_handoff(
    request: HandoffRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Handoff context from one agent to another

    Used in workflows to pass context between BMAD → Archon → Bolt
    """
    mcp_registry.initialize()

    agent_mapping = {
        "bolt": MCPAgent.BOLT,
        "archon": MCPAgent.ARCHON,
        "bmad_pm": MCPAgent.BMAD_PM,
        "bmad_architect": MCPAgent.BMAD_ARCHITECT,
        "bmad_developer": MCPAgent.BMAD_DEVELOPER,
        "orchestrator": MCPAgent.ORCHESTRATOR,
    }

    from_agent = agent_mapping.get(request.from_agent)
    to_agent = agent_mapping.get(request.to_agent)

    if not from_agent or not to_agent:
        raise HTTPException(status_code=400, detail="Invalid agent specified")

    try:
        response = await mcp_server.handoff(
            from_agent=from_agent,
            to_agent=to_agent,
            session_id=request.session_id,
            data=request.data
        )

        return {
            "handoff": f"{request.from_agent} → {request.to_agent}",
            "response": response.payload if response else None,
            "session_id": request.session_id,
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"Handoff error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ================================================
# WORKFLOW EXECUTION
# ================================================

@router.post("/workflows/start")
async def start_workflow(
    request: WorkflowStartRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Start a workflow pipeline

    Available workflows:
    - bmad-to-bolt: Complete BMAD → Archon → Bolt pipeline
    - media-reels: Automated media reels generation
    - sales-pipeline: Sales automation
    - rag-pipeline: Advanced RAG processing
    - conversational: Multi-modal conversation processing
    """
    mcp_registry.initialize()

    workflow = mcp_registry.get_workflow(request.workflow)
    if not workflow:
        raise HTTPException(status_code=404, detail=f"Workflow not found: {request.workflow}")

    try:
        # Start the main workflow
        result = await mcp_server.call_tool(
            tool_name="workflow_start",
            parameters={
                "project_name": request.project_name,
                "description": request.description,
                "agents": request.agents or workflow.agents_involved,
                "config": request.config or {}
            },
            source=MCPAgent.ORCHESTRATOR
        )

        return {
            "workflow": request.workflow,
            "stages": workflow.stages,
            "agents": workflow.agents_involved,
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"Workflow start error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/workflows/{workflow_id}/status")
async def get_workflow_status(
    workflow_id: str,
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get workflow execution status
    """
    context = mcp_server.get_context(session_id)

    if not context:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "workflow_id": workflow_id,
        "session_id": session_id,
        "current_stage": context.current_stage,
        "project_name": context.project_name,
        "brainstorm_complete": bool(context.brainstorm_result),
        "plan_complete": bool(context.project_plan),
        "kb_created": bool(context.knowledge_base_id),
        "prompt_generated": bool(context.generated_prompt),
        "updated_at": context.updated_at
    }


# ================================================
# CONTEXT MANAGEMENT
# ================================================

@router.post("/context/create")
async def create_context(
    session_id: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new MCP context session
    """
    context = mcp_server.create_context(session_id)

    return {
        "session_id": context.session_id,
        "created_at": context.created_at,
        "message": "Context created successfully"
    }


@router.get("/context/{session_id}")
async def get_context(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get context by session ID
    """
    context = mcp_server.get_context(session_id)

    if not context:
        raise HTTPException(status_code=404, detail="Context not found")

    return context.model_dump()


@router.put("/context/{session_id}")
async def update_context(
    session_id: str,
    updates: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """
    Update context with new data
    """
    context = mcp_server.update_context(session_id, updates)

    return {
        "session_id": session_id,
        "updated_at": context.updated_at,
        "message": "Context updated successfully"
    }


# ================================================
# REAL-TIME EVENTS (SSE)
# ================================================

@router.get("/events/{session_id}")
async def stream_events(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Stream MCP events via Server-Sent Events

    Subscribe to real-time updates for a session
    """

    async def event_generator():
        queue = await mcp_server.subscribe(session_id)

        try:
            yield f"event: connected\ndata: {json.dumps({'session_id': session_id})}\n\n"

            while True:
                try:
                    message = await asyncio.wait_for(queue.get(), timeout=30)
                    yield f"event: {message.type.value}\ndata: {json.dumps(message.to_dict())}\n\n"
                except asyncio.TimeoutError:
                    # Send keepalive
                    yield f"event: ping\ndata: {json.dumps({'timestamp': datetime.utcnow().isoformat()})}\n\n"

        except asyncio.CancelledError:
            pass
        finally:
            mcp_server.unsubscribe(session_id, queue)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


# ================================================
# WEBSOCKET FOR REAL-TIME
# ================================================

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for real-time MCP communication
    """
    await websocket.accept()

    queue = await mcp_server.subscribe(session_id)

    try:
        # Send welcome message
        await websocket.send_json({
            "type": "connected",
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat()
        })

        # Listen for messages from queue
        while True:
            try:
                message = await asyncio.wait_for(queue.get(), timeout=30)
                await websocket.send_json(message.to_dict())
            except asyncio.TimeoutError:
                # Send ping
                await websocket.send_json({"type": "ping"})

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {session_id}")
    finally:
        mcp_server.unsubscribe(session_id, queue)


# ================================================
# HEALTH & INFO
# ================================================

@router.get("/health")
async def mcp_health():
    """
    MCP service health check
    """
    mcp_registry.initialize()

    return {
        "status": "healthy",
        "apps_registered": len(mcp_registry.apps),
        "agents_registered": len(mcp_registry.agents),
        "workflows_registered": len(mcp_registry.workflows),
        "tools_available": len(mcp_server._tools),
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/info")
async def mcp_info():
    """
    Get MCP server information
    """
    mcp_registry.initialize()

    return {
        "name": "IAFactory MCP Server",
        "version": "1.0.0",
        "description": "Model Context Protocol hub connecting Bolt, Archon, BMAD, and all IAFactory apps",
        "capabilities": {
            "tools": True,
            "agents": True,
            "workflows": True,
            "context": True,
            "streaming": True,
            "websocket": True
        },
        "registry": {
            "apps": len(mcp_registry.apps),
            "agents": len(mcp_registry.agents),
            "workflows": len(mcp_registry.workflows),
            "tools": len(mcp_server._tools)
        }
    }
