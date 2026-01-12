"""
Base Agent - Classe de base pour tous les agents IA
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from pydantic import BaseModel
import logging
from datetime import datetime
import uuid


class AgentTask(BaseModel):
    """Tâche assignée à un agent"""
    task_id: str = None
    task_type: str
    input_data: Dict[str, Any]
    priority: int = 5  # 1-10, 1 = highest
    created_at: datetime = None
    metadata: Dict[str, Any] = {}

    def __init__(self, **data):
        super().__init__(**data)
        if self.task_id is None:
            self.task_id = str(uuid.uuid4())
        if self.created_at is None:
            self.created_at = datetime.utcnow()


class AgentResult(BaseModel):
    """Résultat d'une tâche d'agent"""
    task_id: str
    success: bool
    output_data: Dict[str, Any] = {}
    error_message: Optional[str] = None
    execution_time_ms: int = 0
    cost_cents: int = 0  # Coût en centimes
    metadata: Dict[str, Any] = {}


class AgentState(BaseModel):
    """État interne d'un agent"""
    agent_id: str
    agent_type: str
    status: str = "idle"  # idle, processing, waiting, error
    current_task: Optional[str] = None
    tasks_completed: int = 0
    total_cost_cents: int = 0
    last_activity: datetime = None


class BaseAgent(ABC):
    """
    Classe de base pour tous les agents IA de la plateforme.

    Chaque agent est spécialisé dans une tâche spécifique du pipeline vidéo.
    """

    def __init__(self, agent_id: str = None):
        self.agent_id = agent_id or str(uuid.uuid4())
        self.logger = logging.getLogger(f"agent.{self.agent_type}")
        self._state = AgentState(
            agent_id=self.agent_id,
            agent_type=self.agent_type,
            last_activity=datetime.utcnow()
        )

    @property
    @abstractmethod
    def agent_type(self) -> str:
        """Type de l'agent (ex: 'script', 'image', 'video')"""
        pass

    @property
    @abstractmethod
    def capabilities(self) -> List[str]:
        """Liste des capacités de l'agent"""
        pass

    @property
    def state(self) -> AgentState:
        """État actuel de l'agent"""
        return self._state

    async def execute(self, task: AgentTask) -> AgentResult:
        """
        Exécute une tâche et retourne le résultat.
        Gère le cycle de vie de la tâche.
        """
        start_time = datetime.utcnow()
        self._state.status = "processing"
        self._state.current_task = task.task_id
        self._state.last_activity = start_time

        self.logger.info(f"Starting task {task.task_id}: {task.task_type}")

        try:
            # Validation
            self._validate_task(task)

            # Exécution spécifique à l'agent
            result = await self._execute_task(task)

            # Mise à jour de l'état
            self._state.tasks_completed += 1
            self._state.total_cost_cents += result.cost_cents

            execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            result.execution_time_ms = int(execution_time)

            self.logger.info(f"Task {task.task_id} completed in {execution_time:.0f}ms")

            return result

        except Exception as e:
            self.logger.error(f"Task {task.task_id} failed: {str(e)}")
            execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000

            return AgentResult(
                task_id=task.task_id,
                success=False,
                error_message=str(e),
                execution_time_ms=int(execution_time)
            )

        finally:
            self._state.status = "idle"
            self._state.current_task = None
            self._state.last_activity = datetime.utcnow()

    @abstractmethod
    async def _execute_task(self, task: AgentTask) -> AgentResult:
        """
        Implémentation spécifique de l'exécution de la tâche.
        À implémenter par chaque agent.
        """
        pass

    def _validate_task(self, task: AgentTask):
        """Validation de base de la tâche"""
        if task.task_type not in self.capabilities:
            raise ValueError(
                f"Task type '{task.task_type}' not supported. "
                f"Available: {self.capabilities}"
            )

    async def health_check(self) -> Dict[str, Any]:
        """Vérifie la santé de l'agent"""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "status": self._state.status,
            "tasks_completed": self._state.tasks_completed,
            "healthy": True
        }

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.agent_id[:8]}>"
