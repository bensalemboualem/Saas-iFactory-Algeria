"""
IAFactory MCP Server - Model Context Protocol Hub
Connects Bolt.diy, Archon, and BMAD agents via standardized protocol

MCP enables:
- Tool sharing between agents
- Context passing across systems
- Standardized agent communication
"""
import asyncio
import json
import logging
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class MCPMessageType(str, Enum):
    """MCP message types"""
    # Requests
    TOOL_CALL = "tool_call"
    CONTEXT_REQUEST = "context_request"
    AGENT_HANDOFF = "agent_handoff"

    # Responses
    TOOL_RESULT = "tool_result"
    CONTEXT_RESPONSE = "context_response"
    HANDOFF_ACK = "handoff_ack"

    # Events
    PROGRESS = "progress"
    ERROR = "error"
    NOTIFICATION = "notification"


class MCPAgent(str, Enum):
    """Registered MCP agents"""
    BOLT = "bolt"
    ARCHON = "archon"
    BMAD_PM = "bmad_pm"
    BMAD_ARCHITECT = "bmad_architect"
    BMAD_DEVELOPER = "bmad_developer"
    BMAD_ANALYST = "bmad_analyst"
    BMAD_TESTER = "bmad_tester"
    ORCHESTRATOR = "orchestrator"
    RAG = "rag"


@dataclass
class MCPTool:
    """MCP Tool definition"""
    name: str
    description: str
    agent: MCPAgent
    parameters: Dict[str, Any]
    handler: Optional[Callable] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "agent": self.agent.value,
            "parameters": self.parameters
        }


@dataclass
class MCPMessage:
    """MCP Protocol message"""
    id: str
    type: MCPMessageType
    source: MCPAgent
    target: Optional[MCPAgent]
    payload: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    correlation_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type.value,
            "source": self.source.value,
            "target": self.target.value if self.target else None,
            "payload": self.payload,
            "timestamp": self.timestamp,
            "correlation_id": self.correlation_id
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MCPMessage":
        return cls(
            id=data["id"],
            type=MCPMessageType(data["type"]),
            source=MCPAgent(data["source"]),
            target=MCPAgent(data["target"]) if data.get("target") else None,
            payload=data["payload"],
            timestamp=data.get("timestamp", datetime.utcnow().isoformat()),
            correlation_id=data.get("correlation_id")
        )


class MCPContext(BaseModel):
    """Shared context between agents"""
    session_id: str
    project_name: Optional[str] = None
    project_description: Optional[str] = None

    # BMAD outputs
    brainstorm_result: Optional[str] = None
    project_plan: Optional[str] = None
    architecture: Optional[Dict[str, Any]] = None
    requirements: List[str] = []

    # Archon outputs
    knowledge_base_id: Optional[str] = None
    rag_context: Optional[str] = None
    relevant_docs: List[Dict[str, Any]] = []

    # Bolt outputs
    generated_prompt: Optional[str] = None
    project_files: List[str] = []
    bolt_session_id: Optional[str] = None

    # Metadata
    current_stage: str = "init"
    created_at: str = ""
    updated_at: str = ""


class MCPServer:
    """
    Central MCP Server for IAFactory ecosystem

    Manages:
    - Tool registration and discovery
    - Message routing between agents
    - Shared context management
    - Event broadcasting
    """

    def __init__(self):
        self._tools: Dict[str, MCPTool] = {}
        self._handlers: Dict[MCPAgent, Callable] = {}
        self._contexts: Dict[str, MCPContext] = {}
        self._message_queue: asyncio.Queue = asyncio.Queue()
        self._subscribers: Dict[str, List[asyncio.Queue]] = {}
        self._running = False

    # ================================================
    # Tool Management
    # ================================================

    def register_tool(self, tool: MCPTool):
        """Register a tool with the MCP server"""
        self._tools[tool.name] = tool
        logger.info(f"MCP Tool registered: {tool.name} from {tool.agent.value}")

    def get_tools(self, agent: MCPAgent = None) -> List[MCPTool]:
        """Get available tools, optionally filtered by agent"""
        if agent:
            return [t for t in self._tools.values() if t.agent == agent]
        return list(self._tools.values())

    def get_tool(self, name: str) -> Optional[MCPTool]:
        """Get a specific tool by name"""
        return self._tools.get(name)

    # ================================================
    # Agent Registration
    # ================================================

    def register_agent_handler(self, agent: MCPAgent, handler: Callable):
        """Register a message handler for an agent"""
        self._handlers[agent] = handler
        logger.info(f"MCP Agent handler registered: {agent.value}")

    # ================================================
    # Message Handling
    # ================================================

    async def send_message(self, message: MCPMessage) -> Optional[MCPMessage]:
        """Send a message and optionally wait for response"""
        message.id = message.id or str(uuid.uuid4())

        logger.debug(f"MCP Message: {message.source.value} -> {message.target.value if message.target else 'broadcast'}: {message.type.value}")

        # Route to target agent
        if message.target and message.target in self._handlers:
            handler = self._handlers[message.target]
            try:
                response = await handler(message)
                return response
            except Exception as e:
                logger.error(f"MCP handler error: {e}")
                return MCPMessage(
                    id=str(uuid.uuid4()),
                    type=MCPMessageType.ERROR,
                    source=MCPAgent.ORCHESTRATOR,
                    target=message.source,
                    payload={"error": str(e)},
                    correlation_id=message.id
                )

        # Broadcast if no target
        if not message.target:
            await self._broadcast(message)

        return None

    async def _broadcast(self, message: MCPMessage):
        """Broadcast message to all subscribers"""
        session_id = message.payload.get("session_id", "global")
        if session_id in self._subscribers:
            for queue in self._subscribers[session_id]:
                await queue.put(message)

    async def call_tool(
        self,
        tool_name: str,
        parameters: Dict[str, Any],
        source: MCPAgent,
        session_id: str = None
    ) -> Dict[str, Any]:
        """Call a registered tool"""
        tool = self.get_tool(tool_name)
        if not tool:
            raise ValueError(f"Tool not found: {tool_name}")

        # Create tool call message
        message = MCPMessage(
            id=str(uuid.uuid4()),
            type=MCPMessageType.TOOL_CALL,
            source=source,
            target=tool.agent,
            payload={
                "tool": tool_name,
                "parameters": parameters,
                "session_id": session_id
            }
        )

        # Execute tool
        if tool.handler:
            try:
                result = await tool.handler(**parameters)
                return {"success": True, "result": result}
            except Exception as e:
                logger.error(f"Tool execution error: {e}")
                return {"success": False, "error": str(e)}

        # Send to agent handler
        response = await self.send_message(message)
        if response:
            return response.payload

        return {"success": False, "error": "No response from agent"}

    # ================================================
    # Context Management
    # ================================================

    def create_context(self, session_id: str = None) -> MCPContext:
        """Create a new shared context"""
        session_id = session_id or str(uuid.uuid4())[:8]
        context = MCPContext(
            session_id=session_id,
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat()
        )
        self._contexts[session_id] = context
        return context

    def get_context(self, session_id: str) -> Optional[MCPContext]:
        """Get context by session ID"""
        return self._contexts.get(session_id)

    def update_context(self, session_id: str, updates: Dict[str, Any]) -> MCPContext:
        """Update context with new data"""
        context = self._contexts.get(session_id)
        if not context:
            context = self.create_context(session_id)

        for key, value in updates.items():
            if hasattr(context, key):
                setattr(context, key, value)

        context.updated_at = datetime.utcnow().isoformat()
        return context

    # ================================================
    # Subscription (Real-time events)
    # ================================================

    async def subscribe(self, session_id: str) -> asyncio.Queue:
        """Subscribe to session events"""
        if session_id not in self._subscribers:
            self._subscribers[session_id] = []

        queue = asyncio.Queue()
        self._subscribers[session_id].append(queue)
        return queue

    def unsubscribe(self, session_id: str, queue: asyncio.Queue):
        """Unsubscribe from session events"""
        if session_id in self._subscribers:
            self._subscribers[session_id].remove(queue)

    # ================================================
    # Agent Handoff
    # ================================================

    async def handoff(
        self,
        from_agent: MCPAgent,
        to_agent: MCPAgent,
        session_id: str,
        data: Dict[str, Any]
    ) -> MCPMessage:
        """Handoff context from one agent to another"""
        # Update context
        context = self.get_context(session_id)
        if context:
            context.current_stage = f"handoff_{from_agent.value}_to_{to_agent.value}"

        # Create handoff message
        message = MCPMessage(
            id=str(uuid.uuid4()),
            type=MCPMessageType.AGENT_HANDOFF,
            source=from_agent,
            target=to_agent,
            payload={
                "session_id": session_id,
                "context": context.model_dump() if context else {},
                "data": data
            }
        )

        # Send and get acknowledgment
        response = await self.send_message(message)

        # Broadcast progress
        await self._broadcast(MCPMessage(
            id=str(uuid.uuid4()),
            type=MCPMessageType.PROGRESS,
            source=MCPAgent.ORCHESTRATOR,
            target=None,
            payload={
                "session_id": session_id,
                "event": "handoff",
                "from": from_agent.value,
                "to": to_agent.value
            }
        ))

        return response


# Singleton instance
mcp_server = MCPServer()


# ================================================
# Tool Definitions
# ================================================

def register_default_tools():
    """Register default MCP tools"""

    # BMAD Tools
    mcp_server.register_tool(MCPTool(
        name="bmad_brainstorm",
        description="Start brainstorming session with BMAD PM and Architect",
        agent=MCPAgent.BMAD_PM,
        parameters={
            "project_name": {"type": "string", "required": True},
            "description": {"type": "string", "required": True},
            "language": {"type": "string", "default": "fr"}
        }
    ))

    mcp_server.register_tool(MCPTool(
        name="bmad_plan",
        description="Create detailed project plan with BMAD team",
        agent=MCPAgent.BMAD_ARCHITECT,
        parameters={
            "session_id": {"type": "string", "required": True},
            "brainstorm_result": {"type": "string", "required": True}
        }
    ))

    mcp_server.register_tool(MCPTool(
        name="bmad_review",
        description="Review code or plan with BMAD analyst",
        agent=MCPAgent.BMAD_ANALYST,
        parameters={
            "content": {"type": "string", "required": True},
            "review_type": {"type": "string", "enum": ["code", "plan", "architecture"]}
        }
    ))

    # Archon Tools
    mcp_server.register_tool(MCPTool(
        name="archon_create_kb",
        description="Create knowledge base in Archon",
        agent=MCPAgent.ARCHON,
        parameters={
            "session_id": {"type": "string", "required": True},
            "project_name": {"type": "string", "required": True},
            "documents": {"type": "array", "items": {"type": "string"}}
        }
    ))

    mcp_server.register_tool(MCPTool(
        name="archon_query",
        description="Query Archon knowledge base",
        agent=MCPAgent.ARCHON,
        parameters={
            "query": {"type": "string", "required": True},
            "kb_id": {"type": "string"},
            "limit": {"type": "integer", "default": 5}
        }
    ))

    mcp_server.register_tool(MCPTool(
        name="archon_index",
        description="Index new content in Archon",
        agent=MCPAgent.ARCHON,
        parameters={
            "content": {"type": "string", "required": True},
            "metadata": {"type": "object"},
            "kb_id": {"type": "string"}
        }
    ))

    # Bolt Tools
    mcp_server.register_tool(MCPTool(
        name="bolt_generate",
        description="Generate code with Bolt.diy",
        agent=MCPAgent.BOLT,
        parameters={
            "prompt": {"type": "string", "required": True},
            "template": {"type": "string"},
            "model": {"type": "string", "default": "claude-3-5-sonnet"}
        }
    ))

    mcp_server.register_tool(MCPTool(
        name="bolt_preview",
        description="Preview generated project in Bolt",
        agent=MCPAgent.BOLT,
        parameters={
            "session_id": {"type": "string", "required": True}
        }
    ))

    mcp_server.register_tool(MCPTool(
        name="bolt_deploy",
        description="Deploy project from Bolt",
        agent=MCPAgent.BOLT,
        parameters={
            "session_id": {"type": "string", "required": True},
            "target": {"type": "string", "enum": ["vercel", "netlify", "docker"]}
        }
    ))

    # RAG Tools
    mcp_server.register_tool(MCPTool(
        name="rag_search",
        description="Search RAG knowledge base",
        agent=MCPAgent.RAG,
        parameters={
            "query": {"type": "string", "required": True},
            "region": {"type": "string", "default": "dz"},
            "limit": {"type": "integer", "default": 5}
        }
    ))

    # Orchestrator Tools
    mcp_server.register_tool(MCPTool(
        name="workflow_start",
        description="Start complete BMAD → Archon → Bolt workflow",
        agent=MCPAgent.ORCHESTRATOR,
        parameters={
            "project_name": {"type": "string", "required": True},
            "description": {"type": "string", "required": True},
            "agents": {"type": "array", "items": {"type": "string"}}
        }
    ))


# Initialize default tools
register_default_tools()
