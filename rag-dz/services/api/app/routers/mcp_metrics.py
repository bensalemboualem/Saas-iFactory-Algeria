"""
MCP Metrics Router - Real-time monitoring and analytics API
Exposes inter-agent communication metrics, workflow performance, and alerts
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel

from app.dependencies import get_current_user
from app.mcp import mcp_metrics, MetricType

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/mcp/metrics", tags=["MCP Metrics"])


class MetricRecordRequest(BaseModel):
    """Request to record a metric"""
    source: str
    target: Optional[str] = None
    metric_type: str
    value: float = 1.0
    metadata: Optional[Dict[str, Any]] = None


class AlertThreshold(BaseModel):
    """Alert threshold configuration"""
    error_rate_percent: Optional[float] = None
    latency_ms: Optional[float] = None
    queue_depth: Optional[int] = None
    memory_percent: Optional[float] = None


# ================================================
# PUBLIC ENDPOINTS (No auth required)
# ================================================

@router.get("/")
async def metrics_root():
    """Root endpoint - shows available metrics endpoints"""
    return {
        "service": "MCP Metrics",
        "endpoints": {
            "/dashboard": "Complete dashboard summary",
            "/agents": "Agent-level metrics",
            "/agents/{agent_id}": "Single agent metrics",
            "/workflows": "Workflow metrics",
            "/flow": "Message flow graph",
            "/timeseries": "Time series data",
            "/alerts": "Recent alerts"
        }
    }


@router.get("/dashboard")
async def get_dashboard(
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get comprehensive dashboard summary

    Returns:
    - Summary statistics (total agents, messages, errors, tokens)
    - Top 10 most active agents
    - Message flow graph between agents
    - Recent alerts
    - Hourly trend data
    """
    return mcp_metrics.get_dashboard_summary()


# ================================================
# AGENT METRICS
# ================================================

@router.get("/agents")
async def get_all_agent_metrics(
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get metrics for all agents"""
    return mcp_metrics.get_agent_metrics()


@router.get("/agents/{agent_id}")
async def get_agent_metrics(
    agent_id: str,
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get metrics for a specific agent"""
    metrics = mcp_metrics.get_agent_metrics(agent_id)
    if not metrics:
        raise HTTPException(status_code=404, detail=f"No metrics found for agent: {agent_id}")
    return metrics


@router.get("/agents/{agent_id}/latency")
async def get_agent_latency(
    agent_id: str,
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get latency breakdown for an agent by target"""
    metrics = mcp_metrics.get_agent_metrics(agent_id)
    if not metrics:
        raise HTTPException(status_code=404, detail=f"No metrics found for agent: {agent_id}")

    return {
        "agent_id": agent_id,
        "avg_latency_ms": metrics.get("avg_latency_ms", 0),
        "latency_by_target": {
            target: sum(lats) / len(lats) if lats else 0
            for target, lats in mcp_metrics._agent_metrics.get(agent_id, {}).latency_by_target.items()
        } if agent_id in mcp_metrics._agent_metrics else {}
    }


# ================================================
# WORKFLOW METRICS
# ================================================

@router.get("/workflows")
async def get_all_workflow_metrics(
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get metrics for all workflows"""
    return mcp_metrics.get_workflow_metrics()


@router.get("/workflows/{workflow_id}")
async def get_workflow_metrics(
    workflow_id: str,
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get metrics for a specific workflow"""
    return mcp_metrics.get_workflow_metrics(workflow_id)


@router.get("/workflows/{workflow_id}/executions")
async def get_workflow_executions(
    workflow_id: str,
    limit: int = Query(default=10, le=100),
    current_user: dict = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """Get recent executions of a workflow"""
    executions = [
        {
            "session_id": wf.session_id,
            "started_at": wf.started_at.isoformat(),
            "completed_at": wf.completed_at.isoformat() if wf.completed_at else None,
            "status": wf.status,
            "stages_completed": wf.stages_completed,
            "total_tokens": wf.total_tokens
        }
        for key, wf in mcp_metrics._workflow_metrics.items()
        if wf.workflow_id == workflow_id
    ]

    return sorted(executions, key=lambda x: x["started_at"], reverse=True)[:limit]


# ================================================
# MESSAGE FLOW
# ================================================

@router.get("/flow")
async def get_message_flow(
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get message flow graph between agents

    Returns a graph structure suitable for visualization:
    - nodes: List of agent IDs
    - edges: List of (source, target, count) tuples
    """
    flow = mcp_metrics.get_message_flow()

    # Convert to visualization-friendly format
    nodes = set()
    edges = []

    for source, targets in flow.items():
        nodes.add(source)
        for target, count in targets.items():
            nodes.add(target)
            edges.append({
                "source": source,
                "target": target,
                "count": count
            })

    return {
        "nodes": list(nodes),
        "edges": edges,
        "total_messages": sum(e["count"] for e in edges)
    }


@router.get("/flow/matrix")
async def get_flow_matrix(
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get message flow as a matrix (for heatmap visualization)
    """
    flow = mcp_metrics.get_message_flow()

    # Get all unique agents
    agents = set()
    for source, targets in flow.items():
        agents.add(source)
        agents.update(targets.keys())

    agents = sorted(agents)

    # Build matrix
    matrix = []
    for source in agents:
        row = []
        for target in agents:
            count = flow.get(source, {}).get(target, 0)
            row.append(count)
        matrix.append(row)

    return {
        "agents": agents,
        "matrix": matrix
    }


# ================================================
# TIME SERIES
# ================================================

@router.get("/timeseries")
async def get_time_series(
    metric_type: Optional[str] = Query(default=None),
    source: Optional[str] = Query(default=None),
    window_minutes: int = Query(default=60, le=1440),
    bucket_minutes: int = Query(default=5, le=60),
    current_user: dict = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    Get time series data for visualization

    Parameters:
    - metric_type: Filter by metric type (message_sent, tool_call, error, etc.)
    - source: Filter by source agent
    - window_minutes: Time window (default 60 minutes, max 24 hours)
    - bucket_minutes: Time bucket size (default 5 minutes)
    """
    mt = MetricType(metric_type) if metric_type else None
    return mcp_metrics.get_time_series(
        metric_type=mt,
        source=source,
        window_minutes=window_minutes,
        bucket_minutes=bucket_minutes
    )


@router.get("/timeseries/messages")
async def get_message_time_series(
    window_minutes: int = Query(default=60, le=1440),
    current_user: dict = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """Get message volume time series"""
    return mcp_metrics.get_time_series(
        metric_type=MetricType.MESSAGE_SENT,
        window_minutes=window_minutes
    )


@router.get("/timeseries/errors")
async def get_error_time_series(
    window_minutes: int = Query(default=60, le=1440),
    current_user: dict = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """Get error rate time series"""
    return mcp_metrics.get_time_series(
        metric_type=MetricType.ERROR,
        window_minutes=window_minutes
    )


# ================================================
# ALERTS
# ================================================

@router.get("/alerts")
async def get_alerts(
    level: Optional[str] = Query(default=None, description="Filter by level: info, warning, error, critical"),
    limit: int = Query(default=50, le=200),
    current_user: dict = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """Get recent alerts"""
    return mcp_metrics.get_alerts(level=level, limit=limit)


@router.get("/alerts/count")
async def get_alert_counts(
    current_user: dict = Depends(get_current_user)
) -> Dict[str, int]:
    """Get alert counts by level"""
    alerts = mcp_metrics.get_alerts(limit=1000)
    counts = {"info": 0, "warning": 0, "error": 0, "critical": 0}

    for alert in alerts:
        level = alert.get("level", "info")
        if level in counts:
            counts[level] += 1

    return counts


# ================================================
# CONFIGURATION
# ================================================

@router.get("/thresholds")
async def get_thresholds(
    current_user: dict = Depends(get_current_user)
) -> Dict[str, float]:
    """Get current alert thresholds"""
    return mcp_metrics.thresholds


@router.put("/thresholds")
async def update_thresholds(
    thresholds: AlertThreshold,
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """Update alert thresholds"""
    if thresholds.error_rate_percent is not None:
        mcp_metrics.thresholds["error_rate_percent"] = thresholds.error_rate_percent
    if thresholds.latency_ms is not None:
        mcp_metrics.thresholds["latency_ms"] = thresholds.latency_ms
    if thresholds.queue_depth is not None:
        mcp_metrics.thresholds["queue_depth"] = thresholds.queue_depth
    if thresholds.memory_percent is not None:
        mcp_metrics.thresholds["memory_percent"] = thresholds.memory_percent

    return {
        "status": "updated",
        "thresholds": mcp_metrics.thresholds
    }


# ================================================
# RECORDING (Internal use)
# ================================================

@router.post("/record")
async def record_metric(
    request: MetricRecordRequest,
    current_user: dict = Depends(get_current_user)
) -> Dict[str, str]:
    """
    Record a metric (for testing or manual recording)

    Normally metrics are recorded automatically by the MCP server
    """
    try:
        metric_type = request.metric_type

        if metric_type == "message":
            mcp_metrics.record_message(
                source=request.source,
                target=request.target or "",
                message_type="manual",
                metadata=request.metadata
            )
        elif metric_type == "error":
            mcp_metrics.record_error(
                source=request.source,
                error_type="manual",
                error_message=str(request.metadata or {}),
                target=request.target
            )
        elif metric_type == "tool_call":
            mcp_metrics.record_tool_call(
                agent=request.source,
                tool_name=request.target or "unknown",
                latency_ms=request.value,
                metadata=request.metadata
            )

        return {"status": "recorded"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ================================================
# EXPORT
# ================================================

@router.get("/export")
async def export_metrics(
    format: str = Query(default="json", description="Export format: json, csv"),
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """Export all metrics data"""
    summary = mcp_metrics.get_dashboard_summary()

    if format == "csv":
        # Return CSV-friendly format
        return {
            "agents": [
                {**m, "agent_id": aid}
                for aid, m in mcp_metrics.get_agent_metrics().items()
            ],
            "workflows": list(mcp_metrics.get_workflow_metrics().values()),
            "alerts": mcp_metrics.get_alerts(limit=1000)
        }

    return {
        "exported_at": datetime.utcnow().isoformat(),
        "summary": summary["summary"],
        "agents": summary["top_agents"],
        "flow": summary["message_flow"],
        "alerts": summary["recent_alerts"],
        "trend": summary["hourly_trend"]
    }
