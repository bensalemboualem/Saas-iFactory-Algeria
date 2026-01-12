"""
IAFactory MCP Metrics - Inter-Agent Communication Monitoring
Tracks message flows, latencies, errors, and performance across the MCP ecosystem
"""
import asyncio
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict
import json
from enum import Enum

logger = logging.getLogger(__name__)


class MetricType(str, Enum):
    """Types of metrics collected"""
    MESSAGE_SENT = "message_sent"
    MESSAGE_RECEIVED = "message_received"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    HANDOFF = "handoff"
    ERROR = "error"
    LATENCY = "latency"
    TOKEN_USAGE = "token_usage"
    WORKFLOW_STAGE = "workflow_stage"


@dataclass
class MetricPoint:
    """Single metric data point"""
    timestamp: datetime
    metric_type: MetricType
    source: str
    target: Optional[str]
    value: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentMetrics:
    """Aggregated metrics for a single agent"""
    agent_id: str
    messages_sent: int = 0
    messages_received: int = 0
    tools_called: int = 0
    errors: int = 0
    avg_latency_ms: float = 0.0
    total_tokens: int = 0
    success_rate: float = 100.0
    last_activity: Optional[datetime] = None

    # Per-target metrics
    messages_by_target: Dict[str, int] = field(default_factory=dict)
    latency_by_target: Dict[str, List[float]] = field(default_factory=dict)


@dataclass
class WorkflowMetrics:
    """Metrics for a workflow execution"""
    workflow_id: str
    session_id: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    current_stage: str = ""
    stages_completed: List[str] = field(default_factory=list)
    stage_durations: Dict[str, float] = field(default_factory=dict)
    agent_calls: Dict[str, int] = field(default_factory=dict)
    total_tokens: int = 0
    status: str = "running"  # running, completed, failed


class MCPMetricsCollector:
    """
    Central metrics collector for MCP ecosystem

    Features:
    - Real-time metric collection
    - Time-series data storage
    - Aggregation by agent, workflow, and time window
    - Alert thresholds
    """

    def __init__(self, retention_hours: int = 24):
        self.retention_hours = retention_hours
        self._metrics: List[MetricPoint] = []
        self._agent_metrics: Dict[str, AgentMetrics] = {}
        self._workflow_metrics: Dict[str, WorkflowMetrics] = {}
        self._alerts: List[Dict[str, Any]] = []

        # Alert thresholds
        self.thresholds = {
            "error_rate_percent": 10.0,
            "latency_ms": 5000,
            "queue_depth": 100,
            "memory_percent": 80.0
        }

        # Message flow graph (for visualization)
        self._message_flow: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

    # ================================================
    # METRIC RECORDING
    # ================================================

    def record_message(
        self,
        source: str,
        target: str,
        message_type: str,
        latency_ms: Optional[float] = None,
        tokens: int = 0,
        success: bool = True,
        metadata: Dict[str, Any] = None
    ):
        """Record a message between agents"""
        now = datetime.utcnow()

        # Record metric point
        self._metrics.append(MetricPoint(
            timestamp=now,
            metric_type=MetricType.MESSAGE_SENT,
            source=source,
            target=target,
            value=1,
            metadata={
                "message_type": message_type,
                "latency_ms": latency_ms,
                "tokens": tokens,
                "success": success,
                **(metadata or {})
            }
        ))

        # Update agent metrics
        self._update_agent_metrics(source, target, latency_ms, tokens, success)

        # Update message flow
        self._message_flow[source][target] += 1

        # Check alerts
        self._check_alerts(source, latency_ms, success)

    def record_tool_call(
        self,
        agent: str,
        tool_name: str,
        latency_ms: float,
        success: bool = True,
        result_size: int = 0,
        metadata: Dict[str, Any] = None
    ):
        """Record a tool call"""
        now = datetime.utcnow()

        self._metrics.append(MetricPoint(
            timestamp=now,
            metric_type=MetricType.TOOL_CALL,
            source=agent,
            target=tool_name,
            value=latency_ms,
            metadata={
                "success": success,
                "result_size": result_size,
                **(metadata or {})
            }
        ))

        # Update agent tool count
        if agent in self._agent_metrics:
            self._agent_metrics[agent].tools_called += 1

    def record_workflow_stage(
        self,
        workflow_id: str,
        session_id: str,
        stage: str,
        duration_ms: float,
        agent: str,
        tokens: int = 0
    ):
        """Record a workflow stage completion"""
        key = f"{workflow_id}_{session_id}"

        if key not in self._workflow_metrics:
            self._workflow_metrics[key] = WorkflowMetrics(
                workflow_id=workflow_id,
                session_id=session_id,
                started_at=datetime.utcnow()
            )

        wf = self._workflow_metrics[key]
        wf.stages_completed.append(stage)
        wf.stage_durations[stage] = duration_ms
        wf.current_stage = stage
        wf.agent_calls[agent] = wf.agent_calls.get(agent, 0) + 1
        wf.total_tokens += tokens

    def record_error(
        self,
        source: str,
        error_type: str,
        error_message: str,
        target: Optional[str] = None
    ):
        """Record an error"""
        now = datetime.utcnow()

        self._metrics.append(MetricPoint(
            timestamp=now,
            metric_type=MetricType.ERROR,
            source=source,
            target=target,
            value=1,
            metadata={
                "error_type": error_type,
                "error_message": error_message
            }
        ))

        # Update agent error count
        if source in self._agent_metrics:
            self._agent_metrics[source].errors += 1
            self._recalculate_success_rate(source)

        # Create alert
        self._alerts.append({
            "timestamp": now.isoformat(),
            "level": "error",
            "source": source,
            "message": f"{error_type}: {error_message}"
        })

    # ================================================
    # HELPER METHODS
    # ================================================

    def _update_agent_metrics(
        self,
        source: str,
        target: str,
        latency_ms: Optional[float],
        tokens: int,
        success: bool
    ):
        """Update aggregated agent metrics"""
        # Initialize if needed
        if source not in self._agent_metrics:
            self._agent_metrics[source] = AgentMetrics(agent_id=source)
        if target and target not in self._agent_metrics:
            self._agent_metrics[target] = AgentMetrics(agent_id=target)

        src = self._agent_metrics[source]
        src.messages_sent += 1
        src.last_activity = datetime.utcnow()
        src.total_tokens += tokens

        if target:
            tgt = self._agent_metrics[target]
            tgt.messages_received += 1
            tgt.last_activity = datetime.utcnow()

            # Track per-target metrics
            src.messages_by_target[target] = src.messages_by_target.get(target, 0) + 1

            if latency_ms:
                if target not in src.latency_by_target:
                    src.latency_by_target[target] = []
                src.latency_by_target[target].append(latency_ms)

                # Update average
                all_latencies = []
                for lats in src.latency_by_target.values():
                    all_latencies.extend(lats)
                src.avg_latency_ms = sum(all_latencies) / len(all_latencies)

        if not success:
            src.errors += 1
            self._recalculate_success_rate(source)

    def _recalculate_success_rate(self, agent_id: str):
        """Recalculate success rate for an agent"""
        if agent_id not in self._agent_metrics:
            return

        agent = self._agent_metrics[agent_id]
        total = agent.messages_sent + agent.tools_called
        if total > 0:
            agent.success_rate = ((total - agent.errors) / total) * 100

    def _check_alerts(self, source: str, latency_ms: Optional[float], success: bool):
        """Check if any alert thresholds are exceeded"""
        if latency_ms and latency_ms > self.thresholds["latency_ms"]:
            self._alerts.append({
                "timestamp": datetime.utcnow().isoformat(),
                "level": "warning",
                "source": source,
                "message": f"High latency detected: {latency_ms:.0f}ms"
            })

        # Check error rate
        if source in self._agent_metrics:
            agent = self._agent_metrics[source]
            if agent.success_rate < (100 - self.thresholds["error_rate_percent"]):
                self._alerts.append({
                    "timestamp": datetime.utcnow().isoformat(),
                    "level": "critical",
                    "source": source,
                    "message": f"High error rate: {100 - agent.success_rate:.1f}%"
                })

    def _cleanup_old_metrics(self):
        """Remove metrics older than retention period"""
        cutoff = datetime.utcnow() - timedelta(hours=self.retention_hours)
        self._metrics = [m for m in self._metrics if m.timestamp > cutoff]
        self._alerts = [a for a in self._alerts
                       if datetime.fromisoformat(a["timestamp"]) > cutoff]

    # ================================================
    # QUERY METHODS
    # ================================================

    def get_agent_metrics(self, agent_id: str = None) -> Dict[str, Any]:
        """Get metrics for one or all agents"""
        if agent_id:
            agent = self._agent_metrics.get(agent_id)
            if not agent:
                return {}
            return {
                "agent_id": agent.agent_id,
                "messages_sent": agent.messages_sent,
                "messages_received": agent.messages_received,
                "tools_called": agent.tools_called,
                "errors": agent.errors,
                "avg_latency_ms": round(agent.avg_latency_ms, 2),
                "total_tokens": agent.total_tokens,
                "success_rate": round(agent.success_rate, 2),
                "last_activity": agent.last_activity.isoformat() if agent.last_activity else None,
                "top_targets": sorted(
                    agent.messages_by_target.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:5]
            }

        return {
            agent_id: self.get_agent_metrics(agent_id)
            for agent_id in self._agent_metrics.keys()
        }

    def get_workflow_metrics(self, workflow_id: str = None) -> Dict[str, Any]:
        """Get metrics for one or all workflows"""
        if workflow_id:
            # Find matching workflows
            matches = [wf for wf in self._workflow_metrics.values()
                      if wf.workflow_id == workflow_id]
            return {
                "workflow_id": workflow_id,
                "executions": len(matches),
                "avg_duration_ms": sum(
                    sum(wf.stage_durations.values()) for wf in matches
                ) / len(matches) if matches else 0,
                "avg_tokens": sum(wf.total_tokens for wf in matches) / len(matches) if matches else 0,
                "success_rate": len([wf for wf in matches if wf.status == "completed"]) / len(matches) * 100 if matches else 0
            }

        return {
            wf_id: self.get_workflow_metrics(wf_id)
            for wf_id in set(wf.workflow_id for wf in self._workflow_metrics.values())
        }

    def get_message_flow(self) -> Dict[str, Dict[str, int]]:
        """Get message flow graph between agents"""
        return dict(self._message_flow)

    def get_time_series(
        self,
        metric_type: MetricType = None,
        source: str = None,
        window_minutes: int = 60,
        bucket_minutes: int = 5
    ) -> List[Dict[str, Any]]:
        """Get time series data for visualization"""
        cutoff = datetime.utcnow() - timedelta(minutes=window_minutes)

        # Filter metrics
        filtered = [
            m for m in self._metrics
            if m.timestamp > cutoff
            and (metric_type is None or m.metric_type == metric_type)
            and (source is None or m.source == source)
        ]

        # Bucket by time
        buckets = defaultdict(lambda: {"count": 0, "value_sum": 0})

        for m in filtered:
            bucket_key = m.timestamp.replace(
                minute=(m.timestamp.minute // bucket_minutes) * bucket_minutes,
                second=0,
                microsecond=0
            )
            buckets[bucket_key]["count"] += 1
            buckets[bucket_key]["value_sum"] += m.value

        return [
            {
                "timestamp": ts.isoformat(),
                "count": data["count"],
                "avg_value": data["value_sum"] / data["count"] if data["count"] > 0 else 0
            }
            for ts, data in sorted(buckets.items())
        ]

    def get_alerts(self, level: str = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent alerts"""
        filtered = self._alerts
        if level:
            filtered = [a for a in filtered if a["level"] == level]
        return sorted(filtered, key=lambda x: x["timestamp"], reverse=True)[:limit]

    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get comprehensive dashboard summary"""
        self._cleanup_old_metrics()

        # Calculate totals
        total_messages = sum(a.messages_sent for a in self._agent_metrics.values())
        total_errors = sum(a.errors for a in self._agent_metrics.values())
        total_tokens = sum(a.total_tokens for a in self._agent_metrics.values())

        # Get recent metrics (last hour)
        hour_ago = datetime.utcnow() - timedelta(hours=1)
        recent = [m for m in self._metrics if m.timestamp > hour_ago]

        # Active agents (activity in last 5 minutes)
        five_min_ago = datetime.utcnow() - timedelta(minutes=5)
        active_agents = [
            a for a in self._agent_metrics.values()
            if a.last_activity and a.last_activity > five_min_ago
        ]

        return {
            "summary": {
                "total_agents": len(self._agent_metrics),
                "active_agents": len(active_agents),
                "total_messages_24h": total_messages,
                "total_errors_24h": total_errors,
                "total_tokens_24h": total_tokens,
                "messages_per_hour": len(recent),
                "overall_success_rate": round(
                    (total_messages - total_errors) / total_messages * 100
                    if total_messages > 0 else 100,
                    2
                )
            },
            "top_agents": sorted(
                [self.get_agent_metrics(a) for a in self._agent_metrics.keys()],
                key=lambda x: x.get("messages_sent", 0),
                reverse=True
            )[:10],
            "message_flow": self.get_message_flow(),
            "recent_alerts": self.get_alerts(limit=10),
            "hourly_trend": self.get_time_series(window_minutes=60, bucket_minutes=5)
        }


# Singleton instance
mcp_metrics = MCPMetricsCollector()
