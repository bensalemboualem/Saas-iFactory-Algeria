"""
Service pour gérer les workflows Bolt SuperPower
"""
import logging
import uuid
import json
from datetime import datetime
from typing import Optional, Dict, Any, List
import asyncpg

from app.models.bolt_workflow import (
    WorkflowMode,
    WorkflowStatus,
    AgentStatus,
    BoltWorkflowDB,
    AgentExecutionDB,
    WorkflowStatusResponse,
    AgentExecutionSummary,
    AgentResult
)

logger = logging.getLogger(__name__)


class BoltWorkflowService:
    """Service pour gérer les workflows Bolt"""

    def __init__(self, db_pool: asyncpg.Pool):
        self.db_pool = db_pool

    async def create_workflow(
        self,
        mode: WorkflowMode,
        user_description: Optional[str] = None,
        tech_stack: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Crée un nouveau workflow

        Args:
            mode: Mode du workflow (direct ou bmad)
            user_description: Description fournie par l'utilisateur
            tech_stack: Liste des technologies
            metadata: Métadonnées additionnelles

        Returns:
            workflow_id (UUID string)
        """
        workflow_id = str(uuid.uuid4())

        import json
        async with self.db_pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO bolt_workflows (
                    workflow_id,
                    mode,
                    user_description,
                    status,
                    tech_stack,
                    metadata
                )
                VALUES ($1, $2, $3, $4, $5::jsonb, $6::jsonb)
                """,
                workflow_id,
                mode.value,
                user_description,
                WorkflowStatus.PENDING.value,
                json.dumps(tech_stack if tech_stack else []),
                json.dumps(metadata if metadata else {})
            )

        logger.info(f"Created workflow {workflow_id} in mode {mode.value}")
        return workflow_id

    async def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """
        Récupère un workflow par son ID

        Args:
            workflow_id: UUID du workflow

        Returns:
            Dictionnaire avec les données du workflow ou None
        """
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT
                    id,
                    workflow_id,
                    mode,
                    user_description,
                    status,
                    current_agent,
                    agents_completed,
                    tech_stack,
                    archon_project_id,
                    knowledge_source_id,
                    zip_file_path,
                    created_at,
                    completed_at,
                    metadata
                FROM bolt_workflows
                WHERE workflow_id = $1
                """,
                workflow_id
            )

            if row:
                return dict(row)
            return None

    async def update_workflow_status(
        self,
        workflow_id: str,
        status: WorkflowStatus,
        current_agent: Optional[str] = None
    ) -> bool:
        """
        Met à jour le statut du workflow

        Args:
            workflow_id: UUID du workflow
            status: Nouveau statut
            current_agent: Agent actuellement en cours

        Returns:
            True si mis à jour, False sinon
        """
        async with self.db_pool.acquire() as conn:
            result = await conn.execute(
                """
                UPDATE bolt_workflows
                SET status = $2,
                    current_agent = $3
                WHERE workflow_id = $1
                """,
                workflow_id,
                status.value,
                current_agent
            )

            return result == "UPDATE 1"

    async def add_completed_agent(
        self,
        workflow_id: str,
        agent_id: str
    ) -> bool:
        """
        Ajoute un agent à la liste des agents complétés

        Args:
            workflow_id: UUID du workflow
            agent_id: ID de l'agent complété

        Returns:
            True si ajouté, False sinon
        """
        async with self.db_pool.acquire() as conn:
            result = await conn.execute(
                """
                UPDATE bolt_workflows
                SET agents_completed = agents_completed || $2::jsonb
                WHERE workflow_id = $1
                """,
                workflow_id,
                f'["{agent_id}"]'
            )

            return result == "UPDATE 1"

    async def set_archon_project(
        self,
        workflow_id: str,
        archon_project_id: int,
        knowledge_source_id: str
    ) -> bool:
        """
        Lie le workflow à un projet Archon

        Args:
            workflow_id: UUID du workflow
            archon_project_id: ID du projet dans Archon
            knowledge_source_id: ID de la source de connaissance

        Returns:
            True si mis à jour, False sinon
        """
        async with self.db_pool.acquire() as conn:
            result = await conn.execute(
                """
                UPDATE bolt_workflows
                SET archon_project_id = $2,
                    knowledge_source_id = $3
                WHERE workflow_id = $1
                """,
                workflow_id,
                archon_project_id,
                knowledge_source_id
            )

            return result == "UPDATE 1"

    async def set_zip_file_path(
        self,
        workflow_id: str,
        zip_file_path: str
    ) -> bool:
        """
        Définit le chemin du fichier ZIP généré

        Args:
            workflow_id: UUID du workflow
            zip_file_path: Chemin du fichier ZIP

        Returns:
            True si mis à jour, False sinon
        """
        async with self.db_pool.acquire() as conn:
            result = await conn.execute(
                """
                UPDATE bolt_workflows
                SET zip_file_path = $2
                WHERE workflow_id = $1
                """,
                workflow_id,
                zip_file_path
            )

            return result == "UPDATE 1"

    # ==================== Agent Executions ====================

    async def create_agent_execution(
        self,
        workflow_id: str,
        agent_name: str,
        agent_id: str,
        input_context: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Crée une exécution d'agent

        Args:
            workflow_id: UUID du workflow
            agent_name: Nom de l'agent
            agent_id: ID de l'agent
            input_context: Contexte d'entrée

        Returns:
            ID de l'exécution créée
        """
        async with self.db_pool.acquire() as conn:
            execution_id = await conn.fetchval(
                """
                INSERT INTO agent_executions (
                    workflow_id,
                    agent_name,
                    agent_id,
                    status,
                    input_context
                )
                VALUES ($1, $2, $3, $4, $5)
                RETURNING id
                """,
                workflow_id,
                agent_name,
                agent_id,
                AgentStatus.PENDING.value,
                json.dumps(input_context) if input_context else "{}"
            )

            logger.info(f"Created agent execution {execution_id} for {agent_name}")
            return execution_id

    async def start_agent_execution(
        self,
        execution_id: int
    ) -> bool:
        """
        Marque une exécution d'agent comme démarrée

        Args:
            execution_id: ID de l'exécution

        Returns:
            True si mis à jour, False sinon
        """
        async with self.db_pool.acquire() as conn:
            result = await conn.execute(
                """
                UPDATE agent_executions
                SET status = $2,
                    started_at = NOW()
                WHERE id = $1
                """,
                execution_id,
                AgentStatus.RUNNING.value
            )

            return result == "UPDATE 1"

    async def complete_agent_execution(
        self,
        execution_id: int,
        output_result: str,
        output_summary: str,
        execution_time_seconds: int
    ) -> bool:
        """
        Marque une exécution d'agent comme complétée

        Args:
            execution_id: ID de l'exécution
            output_result: Résultat complet
            output_summary: Résumé
            execution_time_seconds: Temps d'exécution

        Returns:
            True si mis à jour, False sinon
        """
        async with self.db_pool.acquire() as conn:
            result = await conn.execute(
                """
                UPDATE agent_executions
                SET status = $2,
                    output_result = $3,
                    output_summary = $4,
                    execution_time_seconds = $5,
                    completed_at = NOW()
                WHERE id = $1
                """,
                execution_id,
                AgentStatus.COMPLETED.value,
                output_result,
                output_summary,
                execution_time_seconds
            )

            return result == "UPDATE 1"

    async def fail_agent_execution(
        self,
        execution_id: int,
        error_message: str
    ) -> bool:
        """
        Marque une exécution d'agent comme échouée

        Args:
            execution_id: ID de l'exécution
            error_message: Message d'erreur

        Returns:
            True si mis à jour, False sinon
        """
        async with self.db_pool.acquire() as conn:
            result = await conn.execute(
                """
                UPDATE agent_executions
                SET status = $2,
                    error_message = $3,
                    completed_at = NOW()
                WHERE id = $1
                """,
                execution_id,
                AgentStatus.FAILED.value,
                error_message
            )

            return result == "UPDATE 1"

    async def get_agent_executions(
        self,
        workflow_id: str
    ) -> List[Dict[str, Any]]:
        """
        Récupère toutes les exécutions d'agents pour un workflow

        Args:
            workflow_id: UUID du workflow

        Returns:
            Liste des exécutions d'agents
        """
        async with self.db_pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT
                    id,
                    workflow_id,
                    agent_name,
                    agent_id,
                    status,
                    input_context,
                    output_result,
                    output_summary,
                    execution_time_seconds,
                    started_at,
                    completed_at,
                    error_message
                FROM agent_executions
                WHERE workflow_id = $1
                ORDER BY started_at NULLS LAST, id
                """,
                workflow_id
            )

            return [dict(row) for row in rows]

    # ==================== Status & Progress ====================

    async def get_workflow_status(
        self,
        workflow_id: str
    ) -> Optional[WorkflowStatusResponse]:
        """
        Récupère le statut complet du workflow

        Args:
            workflow_id: UUID du workflow

        Returns:
            Objet WorkflowStatusResponse ou None
        """
        # Récupérer le workflow
        workflow = await self.get_workflow(workflow_id)
        if not workflow:
            return None

        # Récupérer les exécutions d'agents
        agent_executions = await self.get_agent_executions(workflow_id)

        # Construire les résumés des agents complétés
        agents_completed = []
        agents_pending = []

        for execution in agent_executions:
            if execution["status"] == AgentStatus.COMPLETED.value:
                agents_completed.append(
                    AgentExecutionSummary(
                        agent=execution["agent_name"],
                        completed_at=execution["completed_at"],
                        output_summary=execution["output_summary"],
                        status=AgentStatus.COMPLETED,
                        execution_time_seconds=execution["execution_time_seconds"]
                    )
                )
            elif execution["status"] in [AgentStatus.PENDING.value, AgentStatus.RUNNING.value]:
                agents_pending.append(execution["agent_name"])

        # Calculer la progression
        total_agents = len(agent_executions)
        completed_agents = len(agents_completed)
        progress_percent = int((completed_agents / total_agents * 100)) if total_agents > 0 else 0

        # Construire le statut actuel
        current_step = None
        if workflow["current_agent"]:
            current_step = f"Agent {workflow['current_agent']} en cours..."
        elif workflow["status"] == WorkflowStatus.GENERATING.value:
            current_step = "Génération du code final..."
        elif workflow["status"] == WorkflowStatus.COMPLETED.value:
            current_step = "Workflow terminé avec succès"
        elif workflow["status"] == WorkflowStatus.FAILED.value:
            current_step = "Workflow échoué"

        # URL Archon
        archon_url = None
        if workflow["archon_project_id"]:
            archon_url = f"http://localhost:3737/projects/{workflow['archon_project_id']}"

        # URL de téléchargement
        download_url = None
        if workflow["zip_file_path"]:
            download_url = f"/api/bolt/download/{workflow_id}"

        # Collecter les erreurs
        errors = [
            exec["error_message"]
            for exec in agent_executions
            if exec["status"] == AgentStatus.FAILED.value and exec["error_message"]
        ]

        return WorkflowStatusResponse(
            workflow_id=workflow_id,
            mode=WorkflowMode(workflow["mode"]),
            status=WorkflowStatus(workflow["status"]),
            progress_percent=progress_percent,
            current_step=current_step,
            agents_completed=agents_completed,
            agents_pending=agents_pending,
            archon_project_id=workflow["archon_project_id"],
            archon_url=archon_url,
            download_url=download_url,
            errors=errors,
            created_at=workflow["created_at"],
            completed_at=workflow["completed_at"]
        )

    async def calculate_progress(self, workflow_id: str) -> int:
        """
        Calcule la progression d'un workflow en pourcentage

        Args:
            workflow_id: UUID du workflow

        Returns:
            Pourcentage de progression (0-100)
        """
        async with self.db_pool.acquire() as conn:
            progress = await conn.fetchval(
                "SELECT calculate_workflow_progress($1)",
                workflow_id
            )
            return progress if progress is not None else 0

    # ==================== Cleanup ====================

    async def cleanup_old_workflows(self, days: int = 30) -> int:
        """
        Nettoie les anciens workflows terminés

        Args:
            days: Nombre de jours avant suppression

        Returns:
            Nombre de workflows supprimés
        """
        async with self.db_pool.acquire() as conn:
            count = await conn.fetchval(
                "SELECT cleanup_old_workflows()"
            )
            logger.info(f"Cleaned up {count} old workflows")
            return count if count else 0
