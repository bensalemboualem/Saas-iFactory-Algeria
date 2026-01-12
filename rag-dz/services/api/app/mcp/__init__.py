"""
IAFactory MCP (Model Context Protocol) Module
Connects ALL applications, agents, and workflows via standardized protocol

Components:
- server: Central MCP server for message routing and tool management
- registry: Complete registry of all apps, agents, and workflows
- handlers: Message handlers for each agent type
- metrics: Real-time monitoring and analytics
"""
from .server import mcp_server, MCPAgent, MCPMessage, MCPMessageType, MCPTool, MCPContext
from .handlers import register_handlers
from .registry import mcp_registry
from .metrics import mcp_metrics, MCPMetricsCollector, MetricType

__all__ = [
    # Server
    "mcp_server",
    "MCPAgent",
    "MCPMessage",
    "MCPMessageType",
    "MCPTool",
    "MCPContext",
    # Registry
    "mcp_registry",
    # Handlers
    "register_handlers",
    # Metrics
    "mcp_metrics",
    "MCPMetricsCollector",
    "MetricType"
]
