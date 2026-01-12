"""
Workflow Engine - Moteur d'orchestration des workflows BMAD
"""

from enum import Enum
from typing import Any, Callable
from datetime import datetime

from pydantic import BaseModel, Field

from .runner import BMADRunner, Workflow, AgentResult, Scope, Complexity


class WorkflowStatus(str, Enum):
    """Statut d'un workflow"""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class WorkflowStep(BaseModel):
    """Étape d'un workflow"""
    agent: str
    status: WorkflowStatus = WorkflowStatus.PENDING
    result: AgentResult | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None


class WorkflowExecution(BaseModel):
    """Exécution d'un workflow"""
    id: str
    workflow: Workflow
    status: WorkflowStatus = WorkflowStatus.PENDING
    steps: list[WorkflowStep] = Field(default_factory=list)
    input_data: dict = Field(default_factory=dict)
    results: dict[str, Any] = Field(default_factory=dict)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error: str | None = None


class WorkflowEngine:
    """
    Moteur d'exécution des workflows BMAD.
    Orchestre l'exécution séquentielle des agents.
    """

    # Définition des workflows et leurs agents
    WORKFLOWS: dict[Workflow, list[str]] = {
        Workflow.QUICK: [
            "developer",
            "test"
        ],
        Workflow.FEATURE: [
            "analyst",
            "developer",
            "test"
        ],
        Workflow.METHOD: [
            "pm",
            "architect",
            "po",
            "developer",
            "test"
        ],
        Workflow.ENTERPRISE: [
            "pm",
            "architect",
            "ux",
            "po",
            "developer",
            "test",
            "security",
            "devops"
        ],
    }

    # Descriptions des workflows
    WORKFLOW_DESCRIPTIONS = {
        Workflow.QUICK: "Quick flow for bugfixes and hotfixes",
        Workflow.FEATURE: "Standard feature development flow",
        Workflow.METHOD: "Full BMAD method for complex features",
        Workflow.ENTERPRISE: "Enterprise flow with all validations",
    }

    def __init__(self, runner: BMADRunner):
        """
        Args:
            runner: Instance du BMAD Runner
        """
        self.runner = runner
        self.executions: dict[str, WorkflowExecution] = {}
        self.hooks: dict[str, list[Callable]] = {
            "before_step": [],
            "after_step": [],
            "on_error": [],
            "on_complete": [],
        }

    def get_workflow_agents(self, workflow: Workflow) -> list[str]:
        """Retourne la liste des agents pour un workflow"""
        return self.WORKFLOWS.get(workflow, [])

    def get_workflow_info(self, workflow: Workflow) -> dict:
        """Retourne les informations d'un workflow"""
        return {
            "workflow": workflow.value,
            "description": self.WORKFLOW_DESCRIPTIONS.get(workflow, ""),
            "agents": self.get_workflow_agents(workflow),
            "steps_count": len(self.get_workflow_agents(workflow))
        }

    def recommend_and_explain(
        self,
        scope: Scope | str,
        complexity: Complexity | str
    ) -> dict:
        """
        Recommande un workflow et explique pourquoi.

        Returns:
            Dict avec workflow recommandé et explication
        """
        workflow = self.runner.recommend_workflow(scope, complexity)
        agents = self.get_workflow_agents(workflow)

        return {
            "recommended_workflow": workflow.value,
            "description": self.WORKFLOW_DESCRIPTIONS.get(workflow),
            "agents": agents,
            "reasoning": self._get_recommendation_reasoning(scope, complexity, workflow),
            "estimated_steps": len(agents)
        }

    def _get_recommendation_reasoning(
        self,
        scope: Scope | str,
        complexity: Complexity | str,
        workflow: Workflow
    ) -> str:
        """Génère l'explication de la recommandation"""
        scope_str = scope.value if isinstance(scope, Scope) else scope
        complexity_str = complexity.value if isinstance(complexity, Complexity) else complexity

        if workflow == Workflow.QUICK:
            return f"Quick flow recommended for {scope_str} with {complexity_str} complexity. Minimal overhead for fast delivery."

        if workflow == Workflow.FEATURE:
            return f"Feature flow recommended for {scope_str}. Includes analysis phase for better requirements understanding."

        if workflow == Workflow.METHOD:
            return f"Full BMAD method recommended for {scope_str} with {complexity_str} complexity. Comprehensive design phase included."

        if workflow == Workflow.ENTERPRISE:
            return f"Enterprise flow recommended for {scope_str} with {complexity_str} complexity. Full validation including security and UX."

        return "Standard workflow selected."

    async def execute(
        self,
        workflow: Workflow,
        input_data: dict,
        execution_id: str | None = None
    ) -> WorkflowExecution:
        """
        Exécute un workflow complet.

        Args:
            workflow: Type de workflow
            input_data: Données d'entrée (requirements, context, etc.)
            execution_id: ID optionnel pour reprendre une exécution

        Returns:
            WorkflowExecution avec tous les résultats
        """
        import uuid

        # Créer ou récupérer l'exécution
        if execution_id and execution_id in self.executions:
            execution = self.executions[execution_id]
        else:
            execution_id = execution_id or str(uuid.uuid4())
            agents = self.get_workflow_agents(workflow)
            execution = WorkflowExecution(
                id=execution_id,
                workflow=workflow,
                steps=[WorkflowStep(agent=agent) for agent in agents],
                input_data=input_data
            )
            self.executions[execution_id] = execution

        execution.status = WorkflowStatus.RUNNING
        execution.started_at = datetime.utcnow()

        try:
            # Exécuter chaque étape
            for step in execution.steps:
                if step.status == WorkflowStatus.COMPLETED:
                    continue  # Skip les étapes déjà complétées

                # Hook before
                await self._run_hooks("before_step", execution, step)

                step.status = WorkflowStatus.RUNNING
                step.started_at = datetime.utcnow()

                # Construire le contexte avec les résultats précédents
                context = {**input_data, **execution.results}

                # Exécuter l'agent
                result = await self.runner.run_agent(
                    step.agent,
                    self._build_task_for_agent(step.agent, input_data),
                    context
                )

                step.result = result
                step.completed_at = datetime.utcnow()

                if result.status == "success":
                    step.status = WorkflowStatus.COMPLETED
                    execution.results[step.agent] = result.output
                else:
                    step.status = WorkflowStatus.FAILED
                    execution.status = WorkflowStatus.FAILED
                    execution.error = f"Agent {step.agent} failed: {result.output}"

                    # Hook on_error
                    await self._run_hooks("on_error", execution, step)
                    break

                # Hook after
                await self._run_hooks("after_step", execution, step)

            # Marquer comme complété si toutes les étapes sont OK
            if all(s.status == WorkflowStatus.COMPLETED for s in execution.steps):
                execution.status = WorkflowStatus.COMPLETED

                # Hook on_complete
                await self._run_hooks("on_complete", execution, None)

        except Exception as e:
            execution.status = WorkflowStatus.FAILED
            execution.error = str(e)

        execution.completed_at = datetime.utcnow()
        return execution

    def _build_task_for_agent(self, agent: str, input_data: dict) -> str:
        """Construit la description de tâche pour un agent"""
        base_task = input_data.get("task", input_data.get("requirements", ""))

        task_templates = {
            "analyst": f"Analyze and structure these requirements:\n\n{base_task}",
            "pm": f"Create a comprehensive PRD for:\n\n{base_task}",
            "architect": f"Design the technical architecture for:\n\n{base_task}",
            "ux": f"Design the user experience for:\n\n{base_task}",
            "po": f"Create user stories and acceptance criteria for:\n\n{base_task}",
            "developer": f"Implement the solution for:\n\n{base_task}",
            "test": f"Create test plan and test cases for:\n\n{base_task}",
            "security": f"Perform security review for:\n\n{base_task}",
            "devops": f"Create deployment plan for:\n\n{base_task}",
        }

        return task_templates.get(agent, base_task)

    async def _run_hooks(
        self,
        hook_type: str,
        execution: WorkflowExecution,
        step: WorkflowStep | None
    ) -> None:
        """Exécute les hooks enregistrés"""
        for hook in self.hooks.get(hook_type, []):
            try:
                if callable(hook):
                    result = hook(execution, step)
                    if hasattr(result, "__await__"):
                        await result
            except Exception:
                pass  # Les hooks ne doivent pas bloquer l'exécution

    def register_hook(self, hook_type: str, callback: Callable) -> None:
        """Enregistre un hook"""
        if hook_type in self.hooks:
            self.hooks[hook_type].append(callback)

    def pause(self, execution_id: str) -> bool:
        """Met en pause une exécution"""
        if execution_id in self.executions:
            self.executions[execution_id].status = WorkflowStatus.PAUSED
            return True
        return False

    def cancel(self, execution_id: str) -> bool:
        """Annule une exécution"""
        if execution_id in self.executions:
            self.executions[execution_id].status = WorkflowStatus.CANCELLED
            return True
        return False

    def get_execution(self, execution_id: str) -> WorkflowExecution | None:
        """Récupère une exécution par ID"""
        return self.executions.get(execution_id)

    def list_executions(
        self,
        status: WorkflowStatus | None = None
    ) -> list[WorkflowExecution]:
        """Liste les exécutions"""
        executions = list(self.executions.values())
        if status:
            executions = [e for e in executions if e.status == status]
        return executions
