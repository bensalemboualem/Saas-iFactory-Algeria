"""
MCP Tools BMAD - Exposition des capacités BMAD via MCP
"""

from typing import Any
from pydantic import BaseModel

from .runner import BMADRunner, Workflow, Scope, Complexity
from .workflow import WorkflowEngine, WorkflowStatus
from .agents_dz import register_dz_agents, list_dz_agents


class MCPToolDefinition(BaseModel):
    """Définition d'un tool MCP"""
    name: str
    description: str
    input_schema: dict


# ============ TOOL DEFINITIONS ============

BMAD_TOOLS: list[MCPToolDefinition] = [
    MCPToolDefinition(
        name="bmad_recommend_workflow",
        description="Recommande le meilleur workflow BMAD basé sur la portée et complexité du projet",
        input_schema={
            "type": "object",
            "properties": {
                "scope": {
                    "type": "string",
                    "enum": ["bugfix", "hotfix", "feature", "refactor", "greenfield", "migration"],
                    "description": "Portée du projet"
                },
                "complexity": {
                    "type": "string",
                    "enum": ["simple", "moderate", "complex", "enterprise"],
                    "description": "Niveau de complexité"
                }
            },
            "required": ["scope"]
        }
    ),
    MCPToolDefinition(
        name="bmad_run_agent",
        description="Exécute un agent BMAD spécifique sur une tâche",
        input_schema={
            "type": "object",
            "properties": {
                "agent": {
                    "type": "string",
                    "description": "Nom de l'agent (pm, architect, developer, etc.)"
                },
                "task": {
                    "type": "string",
                    "description": "Description de la tâche"
                },
                "context": {
                    "type": "object",
                    "description": "Contexte additionnel"
                }
            },
            "required": ["agent", "task"]
        }
    ),
    MCPToolDefinition(
        name="bmad_execute_workflow",
        description="Exécute un workflow BMAD complet",
        input_schema={
            "type": "object",
            "properties": {
                "workflow": {
                    "type": "string",
                    "enum": ["quick-flow", "feature-flow", "method-flow", "enterprise-flow"],
                    "description": "Type de workflow"
                },
                "requirements": {
                    "type": "string",
                    "description": "Requirements du projet"
                },
                "context": {
                    "type": "object",
                    "description": "Contexte additionnel"
                }
            },
            "required": ["workflow", "requirements"]
        }
    ),
    MCPToolDefinition(
        name="bmad_generate_prd",
        description="Génère un PRD (Product Requirements Document) à partir des requirements",
        input_schema={
            "type": "object",
            "properties": {
                "requirements": {
                    "type": "string",
                    "description": "Requirements bruts"
                }
            },
            "required": ["requirements"]
        }
    ),
    MCPToolDefinition(
        name="bmad_generate_architecture",
        description="Génère l'architecture technique à partir d'un PRD",
        input_schema={
            "type": "object",
            "properties": {
                "prd": {
                    "type": "string",
                    "description": "PRD complet"
                }
            },
            "required": ["prd"]
        }
    ),
    MCPToolDefinition(
        name="bmad_generate_stories",
        description="Génère les user stories à partir de l'architecture",
        input_schema={
            "type": "object",
            "properties": {
                "architecture": {
                    "type": "string",
                    "description": "Document d'architecture"
                }
            },
            "required": ["architecture"]
        }
    ),
    MCPToolDefinition(
        name="bmad_list_agents",
        description="Liste tous les agents BMAD disponibles",
        input_schema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    MCPToolDefinition(
        name="bmad_check_dz_conformity",
        description="Vérifie la conformité d'une solution pour l'Algérie",
        input_schema={
            "type": "object",
            "properties": {
                "solution": {
                    "type": "string",
                    "description": "Description de la solution à vérifier"
                }
            },
            "required": ["solution"]
        }
    ),
    MCPToolDefinition(
        name="bmad_localize_darija",
        description="Localise du contenu en Darija algérien",
        input_schema={
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "Contenu à localiser"
                },
                "context": {
                    "type": "string",
                    "description": "Contexte (audience, ton, etc.)"
                }
            },
            "required": ["content"]
        }
    ),
    MCPToolDefinition(
        name="bmad_get_workflow_status",
        description="Récupère le statut d'une exécution de workflow",
        input_schema={
            "type": "object",
            "properties": {
                "execution_id": {
                    "type": "string",
                    "description": "ID de l'exécution"
                }
            },
            "required": ["execution_id"]
        }
    ),
]


class BMADMCPServer:
    """
    Serveur MCP pour exposer les capacités BMAD.
    """

    def __init__(
        self,
        runner: BMADRunner,
        engine: WorkflowEngine | None = None
    ):
        self.runner = runner
        self.engine = engine or WorkflowEngine(runner)

        # Enregistrer les agents custom
        register_dz_agents(runner)

    def get_tools(self) -> list[dict]:
        """Retourne les définitions des tools pour MCP"""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.input_schema
            }
            for tool in BMAD_TOOLS
        ]

    async def execute(self, tool_name: str, arguments: dict) -> dict:
        """Exécute un tool MCP"""
        handlers = {
            "bmad_recommend_workflow": self._handle_recommend_workflow,
            "bmad_run_agent": self._handle_run_agent,
            "bmad_execute_workflow": self._handle_execute_workflow,
            "bmad_generate_prd": self._handle_generate_prd,
            "bmad_generate_architecture": self._handle_generate_architecture,
            "bmad_generate_stories": self._handle_generate_stories,
            "bmad_list_agents": self._handle_list_agents,
            "bmad_check_dz_conformity": self._handle_check_dz_conformity,
            "bmad_localize_darija": self._handle_localize_darija,
            "bmad_get_workflow_status": self._handle_get_workflow_status,
        }

        handler = handlers.get(tool_name)
        if not handler:
            return {"error": f"Unknown tool: {tool_name}"}

        try:
            return await handler(arguments)
        except Exception as e:
            return {"error": str(e)}

    async def _handle_recommend_workflow(self, args: dict) -> dict:
        """Handler pour bmad_recommend_workflow"""
        scope = args.get("scope", "feature")
        complexity = args.get("complexity", "moderate")

        return self.engine.recommend_and_explain(scope, complexity)

    async def _handle_run_agent(self, args: dict) -> dict:
        """Handler pour bmad_run_agent"""
        result = await self.runner.run_agent(
            args["agent"],
            args["task"],
            args.get("context")
        )
        return result.model_dump()

    async def _handle_execute_workflow(self, args: dict) -> dict:
        """Handler pour bmad_execute_workflow"""
        workflow = Workflow(args["workflow"])
        input_data = {
            "requirements": args["requirements"],
            **(args.get("context") or {})
        }

        execution = await self.engine.execute(workflow, input_data)
        return {
            "execution_id": execution.id,
            "status": execution.status.value,
            "steps_completed": sum(1 for s in execution.steps if s.status == WorkflowStatus.COMPLETED),
            "total_steps": len(execution.steps)
        }

    async def _handle_generate_prd(self, args: dict) -> dict:
        """Handler pour bmad_generate_prd"""
        result = await self.runner.generate_prd(args["requirements"])
        return result.model_dump()

    async def _handle_generate_architecture(self, args: dict) -> dict:
        """Handler pour bmad_generate_architecture"""
        result = await self.runner.generate_architecture(args["prd"])
        return result.model_dump()

    async def _handle_generate_stories(self, args: dict) -> dict:
        """Handler pour bmad_generate_stories"""
        result = await self.runner.generate_stories(args["architecture"])
        return result.model_dump()

    async def _handle_list_agents(self, args: dict) -> dict:
        """Handler pour bmad_list_agents"""
        standard_agents = self.runner.list_agents()
        custom_agents = [a.model_dump() for a in list_dz_agents()]

        return {
            "standard_agents": standard_agents,
            "custom_agents": custom_agents
        }

    async def _handle_check_dz_conformity(self, args: dict) -> dict:
        """Handler pour bmad_check_dz_conformity"""
        result = await self.runner.run_agent(
            "conformity-dz",
            f"Vérifie la conformité:\n\n{args['solution']}"
        )
        return result.model_dump()

    async def _handle_localize_darija(self, args: dict) -> dict:
        """Handler pour bmad_localize_darija"""
        task = f"Localise en Darija:\n\n{args['content']}"
        if args.get("context"):
            task += f"\n\nContexte: {args['context']}"

        result = await self.runner.run_agent("darija-content", task)
        return result.model_dump()

    async def _handle_get_workflow_status(self, args: dict) -> dict:
        """Handler pour bmad_get_workflow_status"""
        execution = self.engine.get_execution(args["execution_id"])
        if not execution:
            return {"error": "Execution not found"}

        return {
            "id": execution.id,
            "workflow": execution.workflow.value,
            "status": execution.status.value,
            "steps": [
                {
                    "agent": s.agent,
                    "status": s.status.value,
                    "duration_ms": s.result.duration_ms if s.result else None
                }
                for s in execution.steps
            ],
            "error": execution.error
        }
