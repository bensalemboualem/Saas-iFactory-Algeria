"""Tests pour le Bolt Executor"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

from src.executor import (
    BoltExecutor,
    Task,
    TaskType,
    TaskStatus,
    ExecutionResult,
    LockInfo,
)
from src.bridge import BoltBridge, GenerationResult, CommandResult, Provider


class TestBoltExecutor:
    """Tests du BoltExecutor"""

    @pytest.fixture
    def mock_bridge(self):
        """Mock du BoltBridge"""
        bridge = MagicMock(spec=BoltBridge)
        bridge.generate_code = AsyncMock()
        bridge.edit_file = AsyncMock()
        bridge.run_tests = AsyncMock()
        return bridge

    @pytest.fixture
    def executor(self, mock_bridge):
        """Fixture executor"""
        return BoltExecutor(
            bolt=mock_bridge,
            lock_url="http://localhost:8100",
            validator_url="http://localhost:8054"
        )

    def test_init(self, executor):
        """Test initialisation"""
        assert executor.lock_url == "http://localhost:8100"
        assert executor.validator_url == "http://localhost:8054"
        assert executor.HOLDER_ID == "bolt-executor"
        assert executor.active_locks == {}

    @pytest.mark.asyncio
    async def test_acquire_lock_success(self, executor):
        """Test acquisition de lock réussie"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            mock_instance.post.return_value = MagicMock(status_code=200)

            result = await executor.acquire_lock("src/main.py")

            assert result is True
            assert "src/main.py" in executor.active_locks

    @pytest.mark.asyncio
    async def test_acquire_lock_failure(self, executor):
        """Test acquisition de lock échouée"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            mock_instance.post.return_value = MagicMock(status_code=409)

            result = await executor.acquire_lock("src/main.py")

            assert result is False
            assert "src/main.py" not in executor.active_locks

    @pytest.mark.asyncio
    async def test_release_lock_success(self, executor):
        """Test libération de lock réussie"""
        # Ajouter un lock d'abord
        executor.active_locks["src/main.py"] = LockInfo(
            resource="src/main.py",
            holder="bolt-executor",
            acquired_at=datetime.utcnow()
        )

        with patch('httpx.AsyncClient') as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            mock_instance.delete.return_value = MagicMock(status_code=200)

            result = await executor.release_lock("src/main.py")

            assert result is True
            assert "src/main.py" not in executor.active_locks

    @pytest.mark.asyncio
    async def test_acquire_locks_for_task(self, executor):
        """Test acquisition de locks pour une tâche"""
        task = Task(
            id="task-123",
            project_id="proj-123",
            title="Test task",
            description="Test",
            affected_files=["src/a.py", "src/b.py"]
        )

        with patch.object(executor, 'acquire_lock', new_callable=AsyncMock) as mock_acquire:
            mock_acquire.return_value = True

            locked = await executor.acquire_locks_for_task(task)

            assert len(locked) == 2
            assert "src/a.py" in locked
            assert "src/b.py" in locked

    @pytest.mark.asyncio
    async def test_acquire_locks_rollback_on_failure(self, executor):
        """Test rollback des locks si un échoue"""
        task = Task(
            id="task-123",
            project_id="proj-123",
            title="Test task",
            description="Test",
            affected_files=["src/a.py", "src/b.py", "src/c.py"]
        )

        with patch.object(executor, 'acquire_lock', new_callable=AsyncMock) as mock_acquire:
            # Premier OK, deuxième OK, troisième échoue
            mock_acquire.side_effect = [True, True, False]

            with patch.object(executor, 'release_lock', new_callable=AsyncMock) as mock_release:
                locked = await executor.acquire_locks_for_task(task)

                # Doit retourner vide et avoir libéré les locks acquis
                assert locked == []
                assert mock_release.call_count == 2

    @pytest.mark.asyncio
    async def test_execute_task_generate_success(self, executor, mock_bridge):
        """Test exécution de tâche generate réussie"""
        task = Task(
            id="task-123",
            project_id="proj-123",
            title="Generate feature",
            description="Create a new feature",
            type=TaskType.GENERATE,
            affected_files=[]
        )

        mock_bridge.generate_code.return_value = GenerationResult(
            success=True,
            files={"src/feature.py": "code"}
        )
        mock_bridge.run_tests.return_value = CommandResult(
            success=True,
            exit_code=0,
            stdout="Tests passed",
            stderr="",
            duration_ms=1000
        )

        with patch.object(executor, 'request_validation', new_callable=AsyncMock) as mock_val:
            mock_val.return_value = {"status": "approved"}

            result = await executor.execute_task(task)

            assert result.status == TaskStatus.COMPLETED
            assert result.generation is not None
            assert result.generation.success is True

    @pytest.mark.asyncio
    async def test_execute_task_edit_success(self, executor, mock_bridge):
        """Test exécution de tâche edit réussie"""
        task = Task(
            id="task-123",
            project_id="proj-123",
            title="Edit file",
            description="Update the file",
            type=TaskType.EDIT,
            affected_files=["src/main.py"]
        )

        mock_bridge.edit_file.return_value = GenerationResult(
            success=True,
            files={"src/main.py": "updated code"}
        )
        mock_bridge.run_tests.return_value = CommandResult(
            success=True,
            exit_code=0,
            stdout="Tests passed",
            stderr="",
            duration_ms=1000
        )

        with patch.object(executor, 'acquire_locks_for_task', new_callable=AsyncMock) as mock_lock:
            mock_lock.return_value = ["src/main.py"]

            with patch.object(executor, 'release_locks_for_task', new_callable=AsyncMock):
                with patch.object(executor, 'request_validation', new_callable=AsyncMock) as mock_val:
                    mock_val.return_value = {"status": "approved"}

                    result = await executor.execute_task(task)

                    assert result.status == TaskStatus.COMPLETED
                    mock_bridge.edit_file.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_task_generation_failed(self, executor, mock_bridge):
        """Test échec de génération"""
        task = Task(
            id="task-123",
            project_id="proj-123",
            title="Generate feature",
            description="Create a new feature",
            affected_files=[]
        )

        mock_bridge.generate_code.return_value = GenerationResult(
            success=False,
            messages=["API Error"]
        )

        result = await executor.execute_task(task)

        assert result.status == TaskStatus.FAILED
        assert "API Error" in result.error

    @pytest.mark.asyncio
    async def test_execute_task_tests_failed(self, executor, mock_bridge):
        """Test échec des tests"""
        task = Task(
            id="task-123",
            project_id="proj-123",
            title="Generate feature",
            description="Create a new feature",
            affected_files=[]
        )

        mock_bridge.generate_code.return_value = GenerationResult(
            success=True,
            files={"src/main.py": "code"}
        )
        mock_bridge.run_tests.return_value = CommandResult(
            success=False,
            exit_code=1,
            stdout="",
            stderr="Test failed: assertion error",
            duration_ms=1000
        )

        result = await executor.execute_task(task)

        assert result.status == TaskStatus.FAILED
        assert "Tests failed" in result.error

    @pytest.mark.asyncio
    async def test_execute_task_validation_rejected(self, executor, mock_bridge):
        """Test validation rejetée"""
        task = Task(
            id="task-123",
            project_id="proj-123",
            title="Generate feature",
            description="Create a new feature",
            affected_files=[]
        )

        mock_bridge.generate_code.return_value = GenerationResult(
            success=True,
            files={"src/main.py": "code"}
        )
        mock_bridge.run_tests.return_value = CommandResult(
            success=True,
            exit_code=0,
            stdout="Tests passed",
            stderr="",
            duration_ms=1000
        )

        with patch.object(executor, 'request_validation', new_callable=AsyncMock) as mock_val:
            mock_val.return_value = {"status": "rejected", "reason": "Code quality issues"}

            result = await executor.execute_task(task)

            assert result.status == TaskStatus.REJECTED
            assert "Code quality issues" in result.error

    @pytest.mark.asyncio
    async def test_execute_task_skip_tests(self, executor, mock_bridge):
        """Test skip des tests"""
        task = Task(
            id="task-123",
            project_id="proj-123",
            title="Generate feature",
            description="Create a new feature",
            affected_files=[]
        )

        mock_bridge.generate_code.return_value = GenerationResult(
            success=True,
            files={"src/main.py": "code"}
        )

        with patch.object(executor, 'request_validation', new_callable=AsyncMock) as mock_val:
            mock_val.return_value = {"status": "approved"}

            result = await executor.execute_task(task, skip_tests=True)

            # Tests ne doivent pas être appelés
            mock_bridge.run_tests.assert_not_called()
            assert result.tests.stdout == "Tests skipped"

    @pytest.mark.asyncio
    async def test_execute_quick_fix(self, executor):
        """Test quick fix"""
        with patch.object(executor, 'execute_task', new_callable=AsyncMock) as mock_exec:
            mock_exec.return_value = ExecutionResult(
                task_id="fix-123",
                status=TaskStatus.COMPLETED
            )

            result = await executor.execute_quick_fix(
                "proj-123",
                "src/main.py",
                "Fix the bug"
            )

            assert mock_exec.called
            # Vérifier que c'est un task de type FIX
            call_args = mock_exec.call_args
            task = call_args[0][0]
            assert task.type == TaskType.FIX

    def test_get_active_locks(self, executor):
        """Test récupération des locks actifs"""
        executor.active_locks["a.py"] = LockInfo(
            resource="a.py",
            holder="bolt-executor",
            acquired_at=datetime.utcnow()
        )
        executor.active_locks["b.py"] = LockInfo(
            resource="b.py",
            holder="bolt-executor",
            acquired_at=datetime.utcnow()
        )

        locks = executor.get_active_locks()
        assert len(locks) == 2


class TestTask:
    """Tests du modèle Task"""

    def test_task_defaults(self):
        """Test valeurs par défaut"""
        task = Task(
            id="123",
            project_id="proj",
            title="Test",
            description="Description"
        )
        assert task.type == TaskType.GENERATE
        assert task.status == TaskStatus.PENDING
        assert task.affected_files == []
        assert task.specs == {}

    def test_task_types(self):
        """Test types de tâches"""
        assert TaskType.GENERATE.value == "generate"
        assert TaskType.EDIT.value == "edit"
        assert TaskType.FIX.value == "fix"
        assert TaskType.REFACTOR.value == "refactor"
        assert TaskType.TEST.value == "test"

    def test_task_status(self):
        """Test statuts de tâches"""
        assert TaskStatus.PENDING.value == "pending"
        assert TaskStatus.LOCKED.value == "locked"
        assert TaskStatus.RUNNING.value == "running"
        assert TaskStatus.COMPLETED.value == "completed"
        assert TaskStatus.FAILED.value == "failed"


class TestExecutionResult:
    """Tests du modèle ExecutionResult"""

    def test_execution_result(self):
        """Test création"""
        result = ExecutionResult(
            task_id="123",
            status=TaskStatus.COMPLETED
        )
        assert result.task_id == "123"
        assert result.status == TaskStatus.COMPLETED
        assert result.generation is None
        assert result.tests is None
        assert result.locks_acquired == []
        assert result.error is None
