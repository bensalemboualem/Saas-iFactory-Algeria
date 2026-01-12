"""
MCP Health Check Router - Test all MCP components
Provides health endpoints for apps, agents, workflows, and tools
"""
import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import httpx

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel

from app.dependencies import get_current_user
from app.mcp import mcp_registry
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/api/mcp/health", tags=["MCP Health Check"])


class HealthResult(BaseModel):
    """Health check result"""
    component_id: str
    component_type: str
    name: str
    status: str  # online, offline, degraded, unknown
    latency_ms: Optional[float] = None
    endpoint: Optional[str] = None
    error: Optional[str] = None
    last_checked: str


class HealthSummary(BaseModel):
    """Summary of all health checks"""
    total: int
    online: int
    offline: int
    degraded: int
    unknown: int
    timestamp: str


# Store health results
health_cache: Dict[str, HealthResult] = {}


async def check_http_endpoint(url: str, timeout: float = 5.0) -> tuple[bool, float, Optional[str]]:
    """Check HTTP endpoint health"""
    try:
        async with httpx.AsyncClient() as client:
            start = asyncio.get_event_loop().time()
            response = await client.get(url, timeout=timeout)
            latency = (asyncio.get_event_loop().time() - start) * 1000

            if response.status_code == 200:
                return True, latency, None
            else:
                return False, latency, f"HTTP {response.status_code}"

    except httpx.TimeoutException:
        return False, timeout * 1000, "Timeout"
    except httpx.ConnectError:
        return False, 0, "Connection refused"
    except Exception as e:
        return False, 0, str(e)


async def check_app_health(app_id: str) -> HealthResult:
    """Check health of a specific app"""
    mcp_registry.initialize()

    app = mcp_registry.get_app(app_id)
    if not app:
        return HealthResult(
            component_id=app_id,
            component_type="app",
            name="Unknown",
            status="unknown",
            error="App not found",
            last_checked=datetime.utcnow().isoformat()
        )

    # Determine endpoint
    port = app.port or 3000
    endpoint = f"http://localhost:{port}/health"

    # Check health
    is_healthy, latency, error = await check_http_endpoint(endpoint)

    result = HealthResult(
        component_id=app_id,
        component_type="app",
        name=app.name,
        status="online" if is_healthy else "offline",
        latency_ms=round(latency, 2) if is_healthy else None,
        endpoint=endpoint,
        error=error,
        last_checked=datetime.utcnow().isoformat()
    )

    health_cache[f"app_{app_id}"] = result
    return result


async def check_agent_health(agent_id: str) -> HealthResult:
    """Check health of a specific agent"""
    mcp_registry.initialize()

    agent = mcp_registry.get_agent(agent_id)
    if not agent:
        return HealthResult(
            component_id=agent_id,
            component_type="agent",
            name="Unknown",
            status="unknown",
            error="Agent not found",
            last_checked=datetime.utcnow().isoformat()
        )

    # Agents are checked via MCP server
    # Test by sending a simple ping message
    try:
        from app.mcp import mcp_server, MCPAgent, MCPMessage, MCPMessageType
        import uuid

        # Map agent_id to MCPAgent
        agent_mapping = {
            "bolt": MCPAgent.BOLT,
            "archon": MCPAgent.ARCHON,
            "bmad-pm": MCPAgent.BMAD_PM,
            "bmad-architect": MCPAgent.BMAD_ARCHITECT,
            "bmad-developer": MCPAgent.BMAD_DEVELOPER,
            "bmad-analyst": MCPAgent.BMAD_ANALYST,
            "bmad-tester": MCPAgent.BMAD_TESTER,
            "orchestrator": MCPAgent.ORCHESTRATOR,
        }

        mcp_agent = agent_mapping.get(agent_id)

        if mcp_agent and mcp_agent in mcp_server._handlers:
            status = "online"
            error = None
        else:
            status = "offline"
            error = "No handler registered"

        result = HealthResult(
            component_id=agent_id,
            component_type="agent",
            name=agent.name,
            status=status,
            endpoint=f"mcp://{agent_id}",
            error=error,
            last_checked=datetime.utcnow().isoformat()
        )

    except Exception as e:
        result = HealthResult(
            component_id=agent_id,
            component_type="agent",
            name=agent.name if agent else "Unknown",
            status="offline",
            error=str(e),
            last_checked=datetime.utcnow().isoformat()
        )

    health_cache[f"agent_{agent_id}"] = result
    return result


async def check_workflow_health(workflow_id: str) -> HealthResult:
    """Check health of a specific workflow"""
    mcp_registry.initialize()

    workflow = mcp_registry.get_workflow(workflow_id)
    if not workflow:
        return HealthResult(
            component_id=workflow_id,
            component_type="workflow",
            name="Unknown",
            status="unknown",
            error="Workflow not found",
            last_checked=datetime.utcnow().isoformat()
        )

    # Check if all required agents are available
    missing_agents = []
    for agent_id in workflow.agents_involved:
        agent_health = health_cache.get(f"agent_{agent_id}")
        if not agent_health or agent_health.status != "online":
            missing_agents.append(agent_id)

    if missing_agents:
        status = "degraded"
        error = f"Missing agents: {', '.join(missing_agents)}"
    else:
        status = "online"
        error = None

    result = HealthResult(
        component_id=workflow_id,
        component_type="workflow",
        name=workflow.name,
        status=status,
        endpoint=f"workflow://{workflow_id}",
        error=error,
        last_checked=datetime.utcnow().isoformat()
    )

    health_cache[f"workflow_{workflow_id}"] = result
    return result


# ================================================
# API Endpoints
# ================================================

@router.get("/all")
async def check_all_health(
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Check health of ALL MCP components

    Returns health status for all apps, agents, and workflows
    """
    mcp_registry.initialize()

    results = {
        "apps": [],
        "agents": [],
        "workflows": [],
        "summary": None
    }

    # Check all apps
    for app_id in mcp_registry.apps.keys():
        result = await check_app_health(app_id)
        results["apps"].append(result.model_dump())

    # Check all agents
    for agent_id in mcp_registry.agents.keys():
        result = await check_agent_health(agent_id)
        results["agents"].append(result.model_dump())

    # Check all workflows
    for workflow_id in mcp_registry.workflows.keys():
        result = await check_workflow_health(workflow_id)
        results["workflows"].append(result.model_dump())

    # Calculate summary
    all_results = results["apps"] + results["agents"] + results["workflows"]
    results["summary"] = HealthSummary(
        total=len(all_results),
        online=len([r for r in all_results if r["status"] == "online"]),
        offline=len([r for r in all_results if r["status"] == "offline"]),
        degraded=len([r for r in all_results if r["status"] == "degraded"]),
        unknown=len([r for r in all_results if r["status"] == "unknown"]),
        timestamp=datetime.utcnow().isoformat()
    ).model_dump()

    return results


@router.get("/apps")
async def check_apps_health(
    current_user: dict = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """Check health of all applications"""
    mcp_registry.initialize()

    results = []
    for app_id in mcp_registry.apps.keys():
        result = await check_app_health(app_id)
        results.append(result.model_dump())

    return results


@router.get("/apps/{app_id}")
async def check_single_app_health(
    app_id: str,
    current_user: dict = Depends(get_current_user)
) -> HealthResult:
    """Check health of a specific application"""
    return await check_app_health(app_id)


@router.get("/agents")
async def check_agents_health(
    current_user: dict = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """Check health of all agents"""
    mcp_registry.initialize()

    results = []
    for agent_id in mcp_registry.agents.keys():
        result = await check_agent_health(agent_id)
        results.append(result.model_dump())

    return results


@router.get("/agents/{agent_id}")
async def check_single_agent_health(
    agent_id: str,
    current_user: dict = Depends(get_current_user)
) -> HealthResult:
    """Check health of a specific agent"""
    return await check_agent_health(agent_id)


@router.get("/workflows")
async def check_workflows_health(
    current_user: dict = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """Check health of all workflows"""
    mcp_registry.initialize()

    results = []
    for workflow_id in mcp_registry.workflows.keys():
        result = await check_workflow_health(workflow_id)
        results.append(result.model_dump())

    return results


@router.get("/workflows/{workflow_id}")
async def check_single_workflow_health(
    workflow_id: str,
    current_user: dict = Depends(get_current_user)
) -> HealthResult:
    """Check health of a specific workflow"""
    return await check_workflow_health(workflow_id)


@router.get("/summary")
async def get_health_summary(
    current_user: dict = Depends(get_current_user)
) -> HealthSummary:
    """Get summary of health status from cache"""
    all_results = list(health_cache.values())

    return HealthSummary(
        total=len(all_results),
        online=len([r for r in all_results if r.status == "online"]),
        offline=len([r for r in all_results if r.status == "offline"]),
        degraded=len([r for r in all_results if r.status == "degraded"]),
        unknown=len([r for r in all_results if r.status == "unknown"]),
        timestamp=datetime.utcnow().isoformat()
    )


@router.post("/test/{component_type}/{component_id}")
async def test_component(
    component_type: str,
    component_id: str,
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Run a test on a specific component

    component_type: app, agent, or workflow
    """
    mcp_registry.initialize()

    if component_type == "app":
        health = await check_app_health(component_id)

        # Try to call a tool from this app
        app = mcp_registry.get_app(component_id)
        tool_test = None

        if app and app.tools:
            try:
                from app.mcp import mcp_server, MCPAgent

                result = await mcp_server.call_tool(
                    tool_name=app.tools[0],
                    parameters={"test": True},
                    source=MCPAgent.ORCHESTRATOR
                )
                tool_test = {"success": True, "tool": app.tools[0], "result": result}
            except Exception as e:
                tool_test = {"success": False, "tool": app.tools[0], "error": str(e)}

        return {
            "health": health.model_dump(),
            "tool_test": tool_test,
            "timestamp": datetime.utcnow().isoformat()
        }

    elif component_type == "agent":
        health = await check_agent_health(component_id)

        # Try to send a test message
        message_test = None
        try:
            from app.mcp import mcp_server, MCPAgent, MCPMessage, MCPMessageType

            agent_mapping = {
                "bolt": MCPAgent.BOLT,
                "archon": MCPAgent.ARCHON,
                "bmad-pm": MCPAgent.BMAD_PM,
                "bmad-architect": MCPAgent.BMAD_ARCHITECT,
                "orchestrator": MCPAgent.ORCHESTRATOR,
            }

            mcp_agent = agent_mapping.get(component_id)
            if mcp_agent:
                message = MCPMessage(
                    id=None,
                    type=MCPMessageType.TOOL_CALL,
                    source=MCPAgent.ORCHESTRATOR,
                    target=mcp_agent,
                    payload={"message": "ping", "test": True}
                )
                response = await mcp_server.send_message(message)
                message_test = {
                    "success": response is not None,
                    "response": response.payload if response else None
                }
        except Exception as e:
            message_test = {"success": False, "error": str(e)}

        return {
            "health": health.model_dump(),
            "message_test": message_test,
            "timestamp": datetime.utcnow().isoformat()
        }

    elif component_type == "workflow":
        health = await check_workflow_health(component_id)

        # Check all agents in workflow
        workflow = mcp_registry.get_workflow(component_id)
        agent_status = {}

        if workflow:
            for agent_id in workflow.agents_involved:
                agent_health = await check_agent_health(agent_id)
                agent_status[agent_id] = agent_health.status

        return {
            "health": health.model_dump(),
            "agent_status": agent_status,
            "timestamp": datetime.utcnow().isoformat()
        }

    else:
        raise HTTPException(status_code=400, detail=f"Invalid component type: {component_type}")


@router.get("/")
async def health_check_root():
    """Root health check endpoint"""
    mcp_registry.initialize()

    return {
        "status": "healthy",
        "service": "MCP Health Check",
        "registry": {
            "apps": len(mcp_registry.apps),
            "agents": len(mcp_registry.agents),
            "workflows": len(mcp_registry.workflows)
        },
        "timestamp": datetime.utcnow().isoformat()
    }
