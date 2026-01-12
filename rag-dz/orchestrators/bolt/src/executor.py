"""
Bolt Executor - Exécuteur de tâches avec gestion des locks
Implémente le Single-Writer Rule
"""

import os
from typing import Any
from datetime import datetime
from enum import Enum

import httpx
from pydantic import BaseModel, Field

from .bridge import BoltBridge, GenerationResult, CommandResult, Provider


class TaskStatus(str, Enum):
    """Statut d'une tâche"""
    PENDING = "pending"
    LOCKED = "locked"
    RUNNING = "running"
    TESTING = "testing"
    VALIDATING = "validating"
    COMPLETED = "completed"
    FAILED = "failed"
    REJECTED = "rejected"


class TaskType(str, Enum):
    """Type de tâche"""
    GENERATE = "generate"
    EDIT = "edit"
    FIX = "fix"
    REFACTOR = "refactor"
    TEST = "test"


class Task(BaseModel):
    """Tâche à exécuter"""
    id: str
    project_id: str
    title: str
    description: str
    type: TaskType = TaskType.GENERATE
    affected_files: list[str] = Field(default_factory=list)
    specs: dict = Field(default_factory=dict)
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ExecutionResult(BaseModel):
    """Résultat d'exécution d'une tâche"""
    task_id: str
    status: TaskStatus
    generation: GenerationResult | None = None
    tests: CommandResult | None = None
    locks_acquired: list[str] = Field(default_factory=list)
    locks_released: list[str] = Field(default_factory=list)
    validation_pending: bool = False
    error: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None


class LockInfo(BaseModel):
    """Information sur un lock"""
    resource: str
    holder: str
    acquired_at: datetime


class BoltExecutor:
    """
    Exécuteur de tâches Bolt avec gestion des locks.
    Seul composant autorisé à écrire du code (Single-Writer Rule).
    """

    HOLDER_ID = "bolt-executor"

    def __init__(
        self,
        bolt: BoltBridge,
        lock_url: str = "http://localhost:8100",
        validator_url: str = "http://localhost:8054"
    ):
        """
        Args:
            bolt: Instance du BoltBridge
            lock_url: URL du Meta-Orchestrator pour les locks
            validator_url: URL du Validator-QA
        """
        self.bolt = bolt
        self.lock_url = lock_url
        self.validator_url = validator_url
        self.active_locks: dict[str, LockInfo] = {}

    # ============ LOCK MANAGEMENT ============

    async def acquire_lock(self, resource: str, ttl: int = 300) -> bool:
        """
        Acquiert un verrou sur une ressource.

        Args:
            resource: Chemin de la ressource
            ttl: Time-to-live en secondes

        Returns:
            True si le lock est acquis
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.lock_url}/locks",
                    json={
                        "resource": resource,
                        "holder": self.HOLDER_ID,
                        "ttl": ttl
                    }
                )

                if response.status_code == 200:
                    self.active_locks[resource] = LockInfo(
                        resource=resource,
                        holder=self.HOLDER_ID,
                        acquired_at=datetime.utcnow()
                    )
                    return True

                return False

        except Exception:
            return False

    async def release_lock(self, resource: str) -> bool:
        """
        Libère un verrou.

        Args:
            resource: Chemin de la ressource

        Returns:
            True si libéré avec succès
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"{self.lock_url}/locks/{resource}",
                    headers={"X-Lock-Holder": self.HOLDER_ID}
                )

                if response.status_code == 200:
                    self.active_locks.pop(resource, None)
                    return True

                return False

        except Exception:
            return False

    async def acquire_locks_for_task(self, task: Task) -> list[str]:
        """
        Acquiert tous les locks nécessaires pour une tâche.

        Args:
            task: Tâche à exécuter

        Returns:
            Liste des ressources lockées
        """
        locked = []

        for file_path in task.affected_files:
            if await self.acquire_lock(file_path):
                locked.append(file_path)
            else:
                # Rollback les locks déjà acquis
                for path in locked:
                    await self.release_lock(path)
                return []

        return locked

    async def release_locks_for_task(self, task: Task) -> list[str]:
        """Libère tous les locks d'une tâche"""
        released = []
        for file_path in task.affected_files:
            if await self.release_lock(file_path):
                released.append(file_path)
        return released

    # ============ VALIDATION ============

    async def request_validation(
        self,
        task: Task,
        generation: GenerationResult,
        tests: CommandResult
    ) -> dict:
        """
        Demande la validation au Validator-QA.

        Args:
            task: Tâche exécutée
            generation: Résultat de la génération
            tests: Résultat des tests

        Returns:
            Réponse du validateur
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.validator_url}/validate",
                    json={
                        "task_id": task.id,
                        "project_id": task.project_id,
                        "files": generation.files,
                        "tests_passed": tests.success,
                        "test_output": tests.stdout
                    }
                )
                return response.json()

        except Exception as e:
            return {"status": "error", "error": str(e)}

    # ============ TASK EXECUTION ============

    async def execute_task(
        self,
        task: Task,
        provider: Provider | None = None,
        skip_tests: bool = False,
        skip_validation: bool = False
    ) -> ExecutionResult:
        """
        Exécute une tâche complète avec gestion des locks.

        Workflow:
        1. Acquérir les locks sur les fichiers affectés
        2. Générer/modifier le code
        3. Exécuter les tests
        4. Demander validation (optionnel)
        5. Libérer les locks (ou attendre validation)

        Args:
            task: Tâche à exécuter
            provider: Provider LLM à utiliser
            skip_tests: Sauter l'exécution des tests
            skip_validation: Sauter la demande de validation

        Returns:
            Résultat de l'exécution
        """
        result = ExecutionResult(
            task_id=task.id,
            status=TaskStatus.PENDING,
            started_at=datetime.utcnow()
        )

        # 1. Acquérir les locks
        task.status = TaskStatus.LOCKED
        locked = await self.acquire_locks_for_task(task)

        if not locked and task.affected_files:
            result.status = TaskStatus.FAILED
            result.error = "Failed to acquire locks on affected files"
            result.completed_at = datetime.utcnow()
            return result

        result.locks_acquired = locked

        try:
            # 2. Générer le code
            task.status = TaskStatus.RUNNING

            if task.type == TaskType.EDIT:
                # Édition de fichier existant
                if task.affected_files:
                    generation = await self.bolt.edit_file(
                        task.project_id,
                        task.affected_files[0],
                        task.description,
                        provider
                    )
                else:
                    generation = GenerationResult(
                        success=False,
                        messages=["No file specified for edit"]
                    )
            else:
                # Génération de code
                generation = await self.bolt.generate_code(
                    prompt=task.description,
                    context=task.specs,
                    provider=provider,
                    project_id=task.project_id
                )

            result.generation = generation

            if not generation.success:
                result.status = TaskStatus.FAILED
                result.error = generation.messages[0] if generation.messages else "Generation failed"
                await self.release_locks_for_task(task)
                result.locks_released = locked
                result.completed_at = datetime.utcnow()
                return result

            # 3. Exécuter les tests
            if not skip_tests:
                task.status = TaskStatus.TESTING
                tests = await self.bolt.run_tests(task.project_id)
                result.tests = tests

                if not tests.success:
                    result.status = TaskStatus.FAILED
                    result.error = f"Tests failed: {tests.stderr}"
                    await self.release_locks_for_task(task)
                    result.locks_released = locked
                    result.completed_at = datetime.utcnow()
                    return result
            else:
                result.tests = CommandResult(
                    success=True,
                    exit_code=0,
                    stdout="Tests skipped",
                    stderr="",
                    duration_ms=0
                )

            # 4. Demander validation
            if not skip_validation:
                task.status = TaskStatus.VALIDATING
                result.validation_pending = True

                validation = await self.request_validation(
                    task,
                    generation,
                    result.tests
                )

                if validation.get("status") == "approved":
                    result.status = TaskStatus.COMPLETED
                    result.validation_pending = False
                    await self.release_locks_for_task(task)
                    result.locks_released = locked
                elif validation.get("status") == "rejected":
                    result.status = TaskStatus.REJECTED
                    result.error = validation.get("reason", "Validation rejected")
                    await self.release_locks_for_task(task)
                    result.locks_released = locked
                # Si pending, les locks restent acquis
            else:
                result.status = TaskStatus.COMPLETED
                await self.release_locks_for_task(task)
                result.locks_released = locked

        except Exception as e:
            result.status = TaskStatus.FAILED
            result.error = str(e)
            await self.release_locks_for_task(task)
            result.locks_released = locked

        result.completed_at = datetime.utcnow()
        return result

    async def execute_quick_fix(
        self,
        project_id: str,
        file_path: str,
        fix_description: str
    ) -> ExecutionResult:
        """
        Exécute un quick fix sur un fichier.

        Args:
            project_id: ID du projet
            file_path: Fichier à corriger
            fix_description: Description de la correction

        Returns:
            Résultat
        """
        import uuid

        task = Task(
            id=str(uuid.uuid4()),
            project_id=project_id,
            title=f"Quick fix: {file_path}",
            description=fix_description,
            type=TaskType.FIX,
            affected_files=[file_path]
        )

        return await self.execute_task(task, skip_validation=True)

    def get_active_locks(self) -> list[LockInfo]:
        """Retourne les locks actifs"""
        return list(self.active_locks.values())
