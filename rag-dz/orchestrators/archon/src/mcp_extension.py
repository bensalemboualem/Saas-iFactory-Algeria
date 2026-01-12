"""
MCP Server Extension - Tools supplémentaires pour Nexus
Étend le serveur MCP Archon avec des capacités spécifiques
"""

from typing import Any
from pydantic import BaseModel, Field


class MCPTool(BaseModel):
    """Définition d'un tool MCP"""
    name: str
    description: str
    input_schema: dict
    handler: str  # Nom de la fonction handler


class MCPToolResult(BaseModel):
    """Résultat d'exécution d'un tool"""
    success: bool
    data: Any = None
    error: str | None = None


# ============ NEXUS-SPECIFIC TOOLS ============

NEXUS_TOOLS: list[MCPTool] = [
    MCPTool(
        name="nexus_route",
        description="Route une requête vers l'orchestrateur approprié (BMAD, Archon, Bolt)",
        input_schema={
            "type": "object",
            "properties": {
                "request": {"type": "string", "description": "La requête à router"},
                "context": {"type": "object", "description": "Contexte optionnel"}
            },
            "required": ["request"]
        },
        handler="handle_route"
    ),
    MCPTool(
        name="nexus_lock",
        description="Acquiert un verrou sur une ressource (Single-Writer Rule)",
        input_schema={
            "type": "object",
            "properties": {
                "resource": {"type": "string", "description": "Chemin de la ressource"},
                "holder": {"type": "string", "description": "Agent demandeur"},
                "ttl": {"type": "integer", "description": "TTL en secondes", "default": 300}
            },
            "required": ["resource", "holder"]
        },
        handler="handle_lock"
    ),
    MCPTool(
        name="nexus_unlock",
        description="Libère un verrou sur une ressource",
        input_schema={
            "type": "object",
            "properties": {
                "resource": {"type": "string", "description": "Chemin de la ressource"},
                "holder": {"type": "string", "description": "Agent détenteur"}
            },
            "required": ["resource", "holder"]
        },
        handler="handle_unlock"
    ),
    MCPTool(
        name="nexus_sync_bmad",
        description="Synchronise les artefacts BMAD vers la Knowledge Base",
        input_schema={
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Chemin du dossier BMAD"},
                "force": {"type": "boolean", "description": "Force re-sync", "default": False}
            },
            "required": ["path"]
        },
        handler="handle_sync_bmad"
    ),
    MCPTool(
        name="nexus_task_status",
        description="Met à jour le statut d'une tâche (Archon only)",
        input_schema={
            "type": "object",
            "properties": {
                "task_id": {"type": "string", "description": "ID de la tâche"},
                "status": {
                    "type": "string",
                    "enum": ["todo", "doing", "done", "blocked"],
                    "description": "Nouveau statut"
                },
                "comment": {"type": "string", "description": "Commentaire optionnel"}
            },
            "required": ["task_id", "status"]
        },
        handler="handle_task_status"
    ),
    MCPTool(
        name="nexus_check_permission",
        description="Vérifie les permissions d'écriture pour un agent",
        input_schema={
            "type": "object",
            "properties": {
                "agent": {"type": "string", "description": "Nom de l'agent"},
                "path": {"type": "string", "description": "Chemin à vérifier"},
                "operation": {"type": "string", "description": "Opération (read, write, delete)"}
            },
            "required": ["agent", "path", "operation"]
        },
        handler="handle_check_permission"
    ),
]


class NexusMCPExtension:
    """
    Extension MCP pour Nexus.
    Ajoute des tools spécifiques à l'orchestration multi-agents.
    """

    def __init__(
        self,
        meta_url: str = "http://localhost:8100",
        archon_url: str = "http://localhost:8181"
    ):
        self.meta_url = meta_url
        self.archon_url = archon_url
        self.tools = {tool.name: tool for tool in NEXUS_TOOLS}

    def get_tools(self) -> list[dict]:
        """Retourne les définitions des tools pour MCP"""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.input_schema
            }
            for tool in NEXUS_TOOLS
        ]

    async def execute(self, tool_name: str, arguments: dict) -> MCPToolResult:
        """Exécute un tool MCP"""
        if tool_name not in self.tools:
            return MCPToolResult(
                success=False,
                error=f"Unknown tool: {tool_name}"
            )

        handler_name = self.tools[tool_name].handler
        handler = getattr(self, handler_name, None)

        if not handler:
            return MCPToolResult(
                success=False,
                error=f"Handler not implemented: {handler_name}"
            )

        try:
            result = await handler(arguments)
            return MCPToolResult(success=True, data=result)
        except Exception as e:
            return MCPToolResult(success=False, error=str(e))

    async def handle_route(self, args: dict) -> dict:
        """Handler pour nexus_route"""
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.meta_url}/route",
                json={"request": args["request"], "context": args.get("context")}
            )
            return response.json()

    async def handle_lock(self, args: dict) -> dict:
        """Handler pour nexus_lock"""
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.meta_url}/locks",
                json={
                    "resource": args["resource"],
                    "holder": args["holder"],
                    "ttl": args.get("ttl", 300)
                }
            )
            if response.status_code == 409:
                return {"locked": False, "error": "Resource already locked"}
            return {"locked": True, **response.json()}

    async def handle_unlock(self, args: dict) -> dict:
        """Handler pour nexus_unlock"""
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self.meta_url}/locks/{args['resource']}",
                headers={"X-Lock-Holder": args["holder"]}
            )
            return {"released": response.status_code == 200}

    async def handle_sync_bmad(self, args: dict) -> dict:
        """Handler pour nexus_sync_bmad"""
        from .sync import BMadSync
        syncer = BMadSync(archon_url=self.archon_url)
        count = await syncer.sync_artifacts(args["path"], force=args.get("force", False))
        return {"synced": count, "path": args["path"]}

    async def handle_task_status(self, args: dict) -> dict:
        """Handler pour nexus_task_status"""
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"{self.archon_url}/api/tasks/{args['task_id']}",
                json={
                    "status": args["status"],
                    "status_comment": args.get("comment")
                }
            )
            return response.json()

    async def handle_check_permission(self, args: dict) -> dict:
        """Handler pour nexus_check_permission"""
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.meta_url}/conflicts/check-write",
                json={"agent": args["agent"], "path": args["path"]}
            )
            result = response.json()
            result["operation"] = args["operation"]
            return result


def register_nexus_tools(mcp_server) -> None:
    """
    Enregistre les tools Nexus dans un serveur MCP existant.

    Usage:
        from mcp_server import server
        register_nexus_tools(server)
    """
    extension = NexusMCPExtension()

    for tool in extension.get_tools():
        mcp_server.register_tool(
            name=tool["name"],
            description=tool["description"],
            input_schema=tool["inputSchema"],
            handler=lambda name=tool["name"]: extension.execute(name, {})
        )
