"""
Workflow Orchestrator - Multi-Agent Pipeline
BMAD → Orchestrator → Archon → Prompt Creator → Bolt

Pipeline:
1. BMAD Agents: Brainstorming & Project Planning
2. Orchestrator: Coordination & Knowledge Base Creation
3. Archon: Store knowledge in vector DB
4. Prompt Creator: Prepare optimized prompt
5. Bolt.diy: Execute code generation
"""
import asyncio
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
from pydantic import BaseModel
import httpx

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class WorkflowStage(str, Enum):
    """Workflow pipeline stages"""
    INIT = "init"
    BMAD_BRAINSTORM = "bmad_brainstorm"
    BMAD_PLANNING = "bmad_planning"
    ORCHESTRATOR_PROCESS = "orchestrator_process"
    ARCHON_KNOWLEDGE = "archon_knowledge"
    PROMPT_CREATION = "prompt_creation"
    BOLT_EXECUTION = "bolt_execution"
    COMPLETED = "completed"
    FAILED = "failed"


class WorkflowContext(BaseModel):
    """Context passed through the workflow"""
    workflow_id: str
    project_name: str
    project_description: str
    user_id: Optional[str] = None

    # BMAD outputs
    brainstorm_result: Optional[Dict[str, Any]] = None
    project_plan: Optional[Dict[str, Any]] = None
    selected_agents: List[str] = []

    # Orchestrator outputs
    knowledge_base_id: Optional[str] = None
    project_structure: Optional[Dict[str, Any]] = None

    # Prompt Creator output
    final_prompt: Optional[str] = None
    prompt_metadata: Optional[Dict[str, Any]] = None

    # Bolt output
    generated_code: Optional[Dict[str, Any]] = None
    bolt_session_id: Optional[str] = None

    # Workflow state
    current_stage: WorkflowStage = WorkflowStage.INIT
    stage_history: List[Dict[str, Any]] = []
    errors: List[str] = []
    created_at: str = ""
    updated_at: str = ""


class BMADAgentService:
    """Service to interact with BMAD agents for brainstorming"""

    AGENTS = {
        "pm": {"name": "John", "role": "Product Manager", "focus": "requirements"},
        "architect": {"name": "Winston", "role": "Architect", "focus": "system_design"},
        "developer": {"name": "Amelia", "role": "Developer", "focus": "implementation"},
        "analyst": {"name": "Mary", "role": "Business Analyst", "focus": "user_research"},
        "tester": {"name": "Murat", "role": "Test Architect", "focus": "testing_strategy"},
    }

    def __init__(self, api_url: str = None):
        self.api_url = api_url or f"http://localhost:{settings.port}"

    async def brainstorm(self, context: WorkflowContext) -> Dict[str, Any]:
        """Run BMAD brainstorming session"""
        logger.info(f"[BMAD] Starting brainstorm for: {context.project_name}")

        # Use PM and Architect for initial brainstorming
        brainstorm_prompt = f"""
        Tu es une équipe BMAD composée de John (PM) et Winston (Architect).

        PROJET: {context.project_name}
        DESCRIPTION: {context.project_description}

        Ensemble, analysez ce projet et fournissez:
        1. **Vision Produit** (John): Objectifs, utilisateurs cibles, problèmes résolus
        2. **Architecture Technique** (Winston): Stack recommandé, composants principaux
        3. **MVP Scope**: Features essentielles pour v1
        4. **Risques**: Défis techniques et business identifiés
        5. **Questions**: Points à clarifier avant de continuer

        Répondez en JSON structuré.
        """

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/api/bmad/chat",
                json={
                    "message": brainstorm_prompt,
                    "agent_id": "bmm-pm",
                    "include_architect": True,
                    "output_format": "json"
                },
                timeout=60.0
            )

            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"BMAD brainstorm failed: {response.status_code}")

    async def create_project_plan(self, context: WorkflowContext) -> Dict[str, Any]:
        """Create detailed project plan with BMAD agents"""
        logger.info(f"[BMAD] Creating project plan for: {context.project_name}")

        plan_prompt = f"""
        CONTEXTE BRAINSTORM:
        {context.brainstorm_result}

        En tant qu'équipe BMAD complète, créez un plan de projet détaillé:

        1. **PRD** (John - PM):
           - User Stories avec critères d'acceptation
           - Priorités MoSCoW
           - KPIs de succès

        2. **Architecture** (Winston):
           - Diagramme composants (en texte)
           - APIs et interfaces
           - Modèle de données

        3. **Plan Technique** (Amelia - Developer):
           - Tasks de développement
           - Dépendances
           - Estimations

        4. **Test Strategy** (Murat):
           - Types de tests
           - Coverage cibles
           - Outils recommandés

        Répondez en JSON structuré avec sections: prd, architecture, dev_plan, test_plan
        """

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/api/bmad/chat",
                json={
                    "message": plan_prompt,
                    "agent_id": "bmm-architect",
                    "multi_agent": True,
                    "output_format": "json"
                },
                timeout=120.0
            )

            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"BMAD planning failed: {response.status_code}")


class ArchonService:
    """Service to create knowledge bases in Archon"""

    def __init__(self, api_url: str = None):
        self.api_url = api_url or f"http://localhost:{settings.port}"

    async def create_knowledge_base(self, context: WorkflowContext) -> str:
        """Create a knowledge base from project plan"""
        logger.info(f"[Archon] Creating knowledge base for: {context.project_name}")

        # Prepare documents for ingestion
        documents = [
            {
                "title": f"{context.project_name} - Brainstorm",
                "content": str(context.brainstorm_result),
                "metadata": {"type": "brainstorm", "project": context.project_name}
            },
            {
                "title": f"{context.project_name} - Project Plan",
                "content": str(context.project_plan),
                "metadata": {"type": "project_plan", "project": context.project_name}
            }
        ]

        async with httpx.AsyncClient() as client:
            # Create collection
            collection_response = await client.post(
                f"{self.api_url}/api/knowledge/collections",
                json={
                    "name": f"project_{context.workflow_id}",
                    "description": f"Knowledge base for {context.project_name}",
                    "metadata": {"workflow_id": context.workflow_id}
                },
                timeout=30.0
            )

            if collection_response.status_code not in [200, 201]:
                raise Exception(f"Failed to create collection: {collection_response.status_code}")

            collection_id = collection_response.json().get("id", context.workflow_id)

            # Ingest documents
            for doc in documents:
                await client.post(
                    f"{self.api_url}/api/knowledge/ingest",
                    json={
                        "collection_id": collection_id,
                        "documents": [doc]
                    },
                    timeout=60.0
                )

            logger.info(f"[Archon] Knowledge base created: {collection_id}")
            return collection_id

    async def query_knowledge(self, collection_id: str, query: str) -> List[Dict[str, Any]]:
        """Query the knowledge base"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/api/knowledge/query",
                json={
                    "collection_id": collection_id,
                    "query": query,
                    "top_k": 5
                },
                timeout=30.0
            )

            if response.status_code == 200:
                return response.json().get("results", [])
            return []


class PromptCreatorService:
    """Service to create optimized prompts for Bolt"""

    BOLT_PROMPT_TEMPLATE = """
Tu es un expert en développement full-stack. Génère le code pour ce projet.

## PROJET: {project_name}

## CONTEXTE
{context}

## ARCHITECTURE
{architecture}

## PLAN DE DÉVELOPPEMENT
{dev_plan}

## INSTRUCTIONS
1. Crée la structure de fichiers complète
2. Implémente chaque composant selon l'architecture
3. Inclus les tests unitaires
4. Ajoute la documentation inline
5. Configure le build et le déploiement

## FORMAT DE SORTIE
Génère le code dans des blocs avec le chemin du fichier:
```filepath:src/example.ts
// code here
```

Commence maintenant:
"""

    async def create_prompt(self, context: WorkflowContext) -> Dict[str, Any]:
        """Create optimized prompt for Bolt"""
        logger.info(f"[PromptCreator] Creating prompt for: {context.project_name}")

        # Extract relevant info from context
        architecture = ""
        dev_plan = ""

        if context.project_plan:
            architecture = context.project_plan.get("architecture", "")
            dev_plan = context.project_plan.get("dev_plan", "")

        # Build the prompt
        prompt = self.BOLT_PROMPT_TEMPLATE.format(
            project_name=context.project_name,
            context=context.project_description,
            architecture=architecture,
            dev_plan=dev_plan
        )

        # Add knowledge base context if available
        if context.brainstorm_result:
            prompt += f"\n\n## INSIGHTS DU BRAINSTORM\n{context.brainstorm_result}"

        metadata = {
            "prompt_length": len(prompt),
            "has_architecture": bool(architecture),
            "has_dev_plan": bool(dev_plan),
            "has_knowledge_base": bool(context.knowledge_base_id),
            "created_at": datetime.utcnow().isoformat()
        }

        return {
            "prompt": prompt,
            "metadata": metadata
        }


class BoltExecutionService:
    """Service to execute code generation in Bolt"""

    def __init__(self, bolt_url: str = None):
        self.bolt_url = bolt_url or "http://localhost:5173"

    async def execute(self, context: WorkflowContext) -> Dict[str, Any]:
        """Send prompt to Bolt for execution"""
        logger.info(f"[Bolt] Executing code generation for: {context.project_name}")

        if not context.final_prompt:
            raise ValueError("No prompt available for Bolt execution")

        async with httpx.AsyncClient() as client:
            # Create new Bolt session
            session_response = await client.post(
                f"{self.bolt_url}/api/chat",
                json={
                    "messages": [
                        {"role": "user", "content": context.final_prompt}
                    ],
                    "provider": "BMAD",
                    "model": "bmm-developer"
                },
                timeout=300.0  # 5 minutes for code generation
            )

            if session_response.status_code == 200:
                return {
                    "status": "success",
                    "response": session_response.json(),
                    "session_id": session_response.headers.get("x-session-id")
                }
            else:
                raise Exception(f"Bolt execution failed: {session_response.status_code}")


class WorkflowOrchestrator:
    """
    Main orchestrator that coordinates the entire workflow pipeline
    BMAD → Orchestrator → Archon → Prompt Creator → Bolt
    """

    def __init__(self):
        self.bmad = BMADAgentService()
        self.archon = ArchonService()
        self.prompt_creator = PromptCreatorService()
        self.bolt = BoltExecutionService()

        # Active workflows
        self._workflows: Dict[str, WorkflowContext] = {}

    def _update_stage(
        self,
        context: WorkflowContext,
        stage: WorkflowStage,
        details: Optional[Dict[str, Any]] = None
    ):
        """Update workflow stage and history"""
        context.current_stage = stage
        context.updated_at = datetime.utcnow().isoformat()
        context.stage_history.append({
            "stage": stage.value,
            "timestamp": context.updated_at,
            "details": details or {}
        })
        logger.info(f"[Workflow {context.workflow_id}] Stage: {stage.value}")

    async def start_workflow(
        self,
        project_name: str,
        project_description: str,
        user_id: Optional[str] = None,
        auto_execute: bool = True
    ) -> WorkflowContext:
        """Start a new workflow pipeline"""
        import uuid

        workflow_id = str(uuid.uuid4())[:8]

        context = WorkflowContext(
            workflow_id=workflow_id,
            project_name=project_name,
            project_description=project_description,
            user_id=user_id,
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat()
        )

        self._workflows[workflow_id] = context
        logger.info(f"[Workflow] Started new workflow: {workflow_id}")

        if auto_execute:
            await self.execute_pipeline(context)

        return context

    async def execute_pipeline(self, context: WorkflowContext) -> WorkflowContext:
        """Execute the full workflow pipeline"""
        try:
            # Stage 1: BMAD Brainstorming
            self._update_stage(context, WorkflowStage.BMAD_BRAINSTORM)
            context.brainstorm_result = await self.bmad.brainstorm(context)

            # Stage 2: BMAD Planning
            self._update_stage(context, WorkflowStage.BMAD_PLANNING)
            context.project_plan = await self.bmad.create_project_plan(context)

            # Stage 3: Orchestrator Processing
            self._update_stage(context, WorkflowStage.ORCHESTRATOR_PROCESS)
            context.project_structure = self._process_project_structure(context)

            # Stage 4: Archon Knowledge Base
            self._update_stage(context, WorkflowStage.ARCHON_KNOWLEDGE)
            context.knowledge_base_id = await self.archon.create_knowledge_base(context)

            # Stage 5: Prompt Creation
            self._update_stage(context, WorkflowStage.PROMPT_CREATION)
            prompt_result = await self.prompt_creator.create_prompt(context)
            context.final_prompt = prompt_result["prompt"]
            context.prompt_metadata = prompt_result["metadata"]

            # Stage 6: Bolt Execution
            self._update_stage(context, WorkflowStage.BOLT_EXECUTION)
            bolt_result = await self.bolt.execute(context)
            context.generated_code = bolt_result
            context.bolt_session_id = bolt_result.get("session_id")

            # Complete
            self._update_stage(context, WorkflowStage.COMPLETED)
            logger.info(f"[Workflow {context.workflow_id}] Completed successfully!")

        except Exception as e:
            context.errors.append(str(e))
            self._update_stage(context, WorkflowStage.FAILED, {"error": str(e)})
            logger.error(f"[Workflow {context.workflow_id}] Failed: {e}")

        return context

    def _process_project_structure(self, context: WorkflowContext) -> Dict[str, Any]:
        """Process and structure project from BMAD outputs"""
        structure = {
            "name": context.project_name,
            "type": "fullstack",  # Could be detected from architecture
            "directories": [
                "src/",
                "src/components/",
                "src/services/",
                "src/utils/",
                "tests/",
                "docs/"
            ],
            "config_files": [
                "package.json",
                "tsconfig.json",
                ".env.example"
            ]
        }

        # Extract from architecture if available
        if context.project_plan and "architecture" in context.project_plan:
            arch = context.project_plan["architecture"]
            if isinstance(arch, dict):
                structure["stack"] = arch.get("stack", [])
                structure["components"] = arch.get("components", [])

        return structure

    def get_workflow(self, workflow_id: str) -> Optional[WorkflowContext]:
        """Get workflow by ID"""
        return self._workflows.get(workflow_id)

    def get_all_workflows(self) -> List[WorkflowContext]:
        """Get all workflows"""
        return list(self._workflows.values())


# Singleton instance
workflow_orchestrator = WorkflowOrchestrator()
