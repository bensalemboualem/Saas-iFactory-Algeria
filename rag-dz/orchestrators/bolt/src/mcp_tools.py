"""
MCP Tools Bolt - Exposition des capacités Bolt via MCP
"""

from typing import Any
from pydantic import BaseModel

from .bridge import BoltBridge, Template, Provider
from .executor import BoltExecutor, Task, TaskType
from .templates import list_templates, get_template, get_template_files


class MCPToolDefinition(BaseModel):
    """Définition d'un tool MCP"""
    name: str
    description: str
    input_schema: dict


# ============ TOOL DEFINITIONS ============

BOLT_TOOLS: list[MCPToolDefinition] = [
    MCPToolDefinition(
        name="bolt_create_project",
        description="Crée un nouveau projet avec un template",
        input_schema={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Nom du projet"},
                "template": {
                    "type": "string",
                    "description": "Template à utiliser (react, nextjs, fastapi, iafactory-fastapi, etc.)"
                },
                "description": {"type": "string", "description": "Description du projet"}
            },
            "required": ["name", "template"]
        }
    ),
    MCPToolDefinition(
        name="bolt_generate_code",
        description="Génère du code avec un LLM",
        input_schema={
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "Description de ce qu'il faut générer"},
                "project_id": {"type": "string", "description": "ID du projet cible"},
                "provider": {
                    "type": "string",
                    "enum": ["anthropic", "openai", "deepseek", "groq"],
                    "description": "Provider LLM"
                },
                "context": {"type": "object", "description": "Contexte additionnel"}
            },
            "required": ["prompt"]
        }
    ),
    MCPToolDefinition(
        name="bolt_edit_file",
        description="Édite un fichier existant avec des instructions",
        input_schema={
            "type": "object",
            "properties": {
                "project_id": {"type": "string", "description": "ID du projet"},
                "file_path": {"type": "string", "description": "Chemin du fichier"},
                "instructions": {"type": "string", "description": "Instructions d'édition"}
            },
            "required": ["project_id", "file_path", "instructions"]
        }
    ),
    MCPToolDefinition(
        name="bolt_execute_command",
        description="Exécute une commande dans un projet",
        input_schema={
            "type": "object",
            "properties": {
                "project_id": {"type": "string", "description": "ID du projet"},
                "command": {"type": "string", "description": "Commande à exécuter"}
            },
            "required": ["project_id", "command"]
        }
    ),
    MCPToolDefinition(
        name="bolt_run_tests",
        description="Exécute les tests d'un projet",
        input_schema={
            "type": "object",
            "properties": {
                "project_id": {"type": "string", "description": "ID du projet"},
                "test_command": {"type": "string", "description": "Commande de test (optionnel)"}
            },
            "required": ["project_id"]
        }
    ),
    MCPToolDefinition(
        name="bolt_deploy",
        description="Déploie un projet",
        input_schema={
            "type": "object",
            "properties": {
                "project_id": {"type": "string", "description": "ID du projet"},
                "target": {
                    "type": "string",
                    "enum": ["preview", "production"],
                    "description": "Cible de déploiement"
                }
            },
            "required": ["project_id"]
        }
    ),
    MCPToolDefinition(
        name="bolt_list_templates",
        description="Liste les templates disponibles (standard et IA Factory)",
        input_schema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    MCPToolDefinition(
        name="bolt_get_template",
        description="Récupère les détails et fichiers d'un template",
        input_schema={
            "type": "object",
            "properties": {
                "template_id": {"type": "string", "description": "ID du template"}
            },
            "required": ["template_id"]
        }
    ),
    MCPToolDefinition(
        name="bolt_execute_task",
        description="Exécute une tâche complète avec locks et validation",
        input_schema={
            "type": "object",
            "properties": {
                "project_id": {"type": "string", "description": "ID du projet"},
                "title": {"type": "string", "description": "Titre de la tâche"},
                "description": {"type": "string", "description": "Description/instructions"},
                "affected_files": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Fichiers affectés"
                },
                "skip_tests": {"type": "boolean", "description": "Sauter les tests"},
                "skip_validation": {"type": "boolean", "description": "Sauter la validation"}
            },
            "required": ["project_id", "title", "description"]
        }
    ),
    MCPToolDefinition(
        name="bolt_quick_fix",
        description="Applique un quick fix sur un fichier",
        input_schema={
            "type": "object",
            "properties": {
                "project_id": {"type": "string", "description": "ID du projet"},
                "file_path": {"type": "string", "description": "Fichier à corriger"},
                "fix_description": {"type": "string", "description": "Description de la correction"}
            },
            "required": ["project_id", "file_path", "fix_description"]
        }
    ),
    MCPToolDefinition(
        name="bolt_git_commit",
        description="Effectue un git commit",
        input_schema={
            "type": "object",
            "properties": {
                "project_id": {"type": "string", "description": "ID du projet"},
                "message": {"type": "string", "description": "Message de commit"}
            },
            "required": ["project_id", "message"]
        }
    ),
]


class BoltMCPServer:
    """
    Serveur MCP pour exposer les capacités Bolt.
    """

    def __init__(
        self,
        bolt: BoltBridge,
        executor: BoltExecutor | None = None
    ):
        self.bolt = bolt
        self.executor = executor or BoltExecutor(bolt)

    def get_tools(self) -> list[dict]:
        """Retourne les définitions des tools pour MCP"""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.input_schema
            }
            for tool in BOLT_TOOLS
        ]

    async def execute(self, tool_name: str, arguments: dict) -> dict:
        """Exécute un tool MCP"""
        handlers = {
            "bolt_create_project": self._handle_create_project,
            "bolt_generate_code": self._handle_generate_code,
            "bolt_edit_file": self._handle_edit_file,
            "bolt_execute_command": self._handle_execute_command,
            "bolt_run_tests": self._handle_run_tests,
            "bolt_deploy": self._handle_deploy,
            "bolt_list_templates": self._handle_list_templates,
            "bolt_get_template": self._handle_get_template,
            "bolt_execute_task": self._handle_execute_task,
            "bolt_quick_fix": self._handle_quick_fix,
            "bolt_git_commit": self._handle_git_commit,
        }

        handler = handlers.get(tool_name)
        if not handler:
            return {"error": f"Unknown tool: {tool_name}"}

        try:
            return await handler(arguments)
        except Exception as e:
            return {"error": str(e)}

    async def _handle_create_project(self, args: dict) -> dict:
        """Handler pour bolt_create_project"""
        project = await self.bolt.create_project(
            args["name"],
            args["template"],
            args.get("description")
        )
        return project.model_dump()

    async def _handle_generate_code(self, args: dict) -> dict:
        """Handler pour bolt_generate_code"""
        provider = Provider(args["provider"]) if args.get("provider") else None
        result = await self.bolt.generate_code(
            args["prompt"],
            args.get("context"),
            provider,
            project_id=args.get("project_id")
        )
        return result.model_dump()

    async def _handle_edit_file(self, args: dict) -> dict:
        """Handler pour bolt_edit_file"""
        result = await self.bolt.edit_file(
            args["project_id"],
            args["file_path"],
            args["instructions"]
        )
        return result.model_dump()

    async def _handle_execute_command(self, args: dict) -> dict:
        """Handler pour bolt_execute_command"""
        result = await self.bolt.execute_command(
            args["project_id"],
            args["command"]
        )
        return result.model_dump()

    async def _handle_run_tests(self, args: dict) -> dict:
        """Handler pour bolt_run_tests"""
        result = await self.bolt.run_tests(
            args["project_id"],
            args.get("test_command")
        )
        return result.model_dump()

    async def _handle_deploy(self, args: dict) -> dict:
        """Handler pour bolt_deploy"""
        return await self.bolt.deploy(
            args["project_id"],
            args.get("target", "preview")
        )

    async def _handle_list_templates(self, args: dict) -> dict:
        """Handler pour bolt_list_templates"""
        standard = [t.value for t in Template]
        custom = [t.model_dump() for t in list_templates()]

        return {
            "standard_templates": standard,
            "iafactory_templates": custom
        }

    async def _handle_get_template(self, args: dict) -> dict:
        """Handler pour bolt_get_template"""
        template = get_template(args["template_id"])
        if not template:
            return {"error": f"Template not found: {args['template_id']}"}

        return {
            "template": template.model_dump(),
            "files": list(template.files.keys())
        }

    async def _handle_execute_task(self, args: dict) -> dict:
        """Handler pour bolt_execute_task"""
        import uuid

        task = Task(
            id=str(uuid.uuid4()),
            project_id=args["project_id"],
            title=args["title"],
            description=args["description"],
            affected_files=args.get("affected_files", []),
            type=TaskType.GENERATE
        )

        result = await self.executor.execute_task(
            task,
            skip_tests=args.get("skip_tests", False),
            skip_validation=args.get("skip_validation", False)
        )

        return result.model_dump()

    async def _handle_quick_fix(self, args: dict) -> dict:
        """Handler pour bolt_quick_fix"""
        result = await self.executor.execute_quick_fix(
            args["project_id"],
            args["file_path"],
            args["fix_description"]
        )
        return result.model_dump()

    async def _handle_git_commit(self, args: dict) -> dict:
        """Handler pour bolt_git_commit"""
        result = await self.bolt.git_commit(
            args["project_id"],
            args["message"]
        )
        return result.model_dump()
