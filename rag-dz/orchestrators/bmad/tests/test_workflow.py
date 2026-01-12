"""Tests pour le Workflow Engine"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from src.runner import BMADRunner, Workflow, AgentResult
from src.workflow import WorkflowEngine, WorkflowStatus, WorkflowExecution


class TestWorkflowEngine:
    """Tests du Workflow Engine"""

    @pytest.fixture
    def mock_runner(self):
        """Runner mocké"""
        runner = MagicMock(spec=BMADRunner)
        runner.run_agent = AsyncMock(return_value=AgentResult(
            agent="test",
            status="success",
            output="Test output",
            duration_ms=100
        ))
        runner.recommend_workflow = MagicMock(return_value=Workflow.FEATURE)
        return runner

    @pytest.fixture
    def engine(self, mock_runner):
        """Engine avec runner mocké"""
        return WorkflowEngine(mock_runner)

    def test_get_workflow_agents_quick(self, engine):
        """Test agents workflow quick"""
        agents = engine.get_workflow_agents(Workflow.QUICK)
        assert agents == ["developer", "test"]

    def test_get_workflow_agents_feature(self, engine):
        """Test agents workflow feature"""
        agents = engine.get_workflow_agents(Workflow.FEATURE)
        assert agents == ["analyst", "developer", "test"]

    def test_get_workflow_agents_method(self, engine):
        """Test agents workflow method"""
        agents = engine.get_workflow_agents(Workflow.METHOD)
        assert "pm" in agents
        assert "architect" in agents
        assert "developer" in agents

    def test_get_workflow_agents_enterprise(self, engine):
        """Test agents workflow enterprise"""
        agents = engine.get_workflow_agents(Workflow.ENTERPRISE)
        assert "security" in agents
        assert "ux" in agents
        assert len(agents) == 8

    def test_get_workflow_info(self, engine):
        """Test infos workflow"""
        info = engine.get_workflow_info(Workflow.FEATURE)
        assert info["workflow"] == "feature-flow"
        assert "description" in info
        assert "agents" in info
        assert info["steps_count"] == 3

    def test_recommend_and_explain(self, engine):
        """Test recommandation avec explication"""
        result = engine.recommend_and_explain("feature", "moderate")
        assert "recommended_workflow" in result
        assert "description" in result
        assert "reasoning" in result
        assert "estimated_steps" in result

    @pytest.mark.asyncio
    async def test_execute_workflow(self, engine):
        """Test exécution workflow"""
        input_data = {"requirements": "Build a feature"}

        execution = await engine.execute(Workflow.QUICK, input_data)

        assert execution.status == WorkflowStatus.COMPLETED
        assert len(execution.steps) == 2
        assert all(s.status == WorkflowStatus.COMPLETED for s in execution.steps)

    @pytest.mark.asyncio
    async def test_execute_workflow_with_failure(self, engine, mock_runner):
        """Test exécution avec échec"""
        # Premier appel OK, deuxième en erreur
        mock_runner.run_agent.side_effect = [
            AgentResult(agent="dev", status="success", output="OK", duration_ms=100),
            AgentResult(agent="test", status="error", output="Failed", duration_ms=50),
        ]

        execution = await engine.execute(Workflow.QUICK, {"requirements": "test"})

        assert execution.status == WorkflowStatus.FAILED
        assert execution.error is not None

    def test_pause_execution(self, engine):
        """Test pause d'une exécution"""
        # Créer une exécution
        from src.workflow import WorkflowExecution, WorkflowStep
        execution = WorkflowExecution(
            id="test-123",
            workflow=Workflow.QUICK,
            steps=[WorkflowStep(agent="dev")]
        )
        engine.executions["test-123"] = execution

        result = engine.pause("test-123")
        assert result is True
        assert execution.status == WorkflowStatus.PAUSED

    def test_cancel_execution(self, engine):
        """Test annulation d'une exécution"""
        from src.workflow import WorkflowExecution, WorkflowStep
        execution = WorkflowExecution(
            id="test-456",
            workflow=Workflow.QUICK,
            steps=[WorkflowStep(agent="dev")]
        )
        engine.executions["test-456"] = execution

        result = engine.cancel("test-456")
        assert result is True
        assert execution.status == WorkflowStatus.CANCELLED

    def test_get_execution(self, engine):
        """Test récupération exécution"""
        from src.workflow import WorkflowExecution, WorkflowStep
        execution = WorkflowExecution(
            id="test-789",
            workflow=Workflow.QUICK,
            steps=[WorkflowStep(agent="dev")]
        )
        engine.executions["test-789"] = execution

        result = engine.get_execution("test-789")
        assert result is not None
        assert result.id == "test-789"

    def test_get_execution_not_found(self, engine):
        """Test exécution non trouvée"""
        result = engine.get_execution("nonexistent")
        assert result is None

    def test_list_executions(self, engine):
        """Test liste des exécutions"""
        from src.workflow import WorkflowExecution, WorkflowStep

        for i in range(3):
            execution = WorkflowExecution(
                id=f"exec-{i}",
                workflow=Workflow.QUICK,
                steps=[WorkflowStep(agent="dev")]
            )
            engine.executions[f"exec-{i}"] = execution

        results = engine.list_executions()
        assert len(results) == 3

    def test_register_hook(self, engine):
        """Test enregistrement hook"""
        def my_hook(exec, step):
            pass

        engine.register_hook("before_step", my_hook)
        assert my_hook in engine.hooks["before_step"]
