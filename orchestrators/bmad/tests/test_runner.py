"""Tests pour le BMAD Runner"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import tempfile
from pathlib import Path

from src.runner import BMADRunner, Workflow, Scope, Complexity, AgentResult


class TestBMADRunner:
    """Tests du BMAD Runner"""

    @pytest.fixture
    def runner(self):
        """Runner sans fichiers BMAD"""
        return BMADRunner(bmad_path=None)

    @pytest.fixture
    def runner_with_agents(self):
        """Runner avec agents mockés"""
        with tempfile.TemporaryDirectory() as tmpdir:
            agents_dir = Path(tmpdir) / "agents"
            agents_dir.mkdir()

            # Créer quelques agents mock
            (agents_dir / "pm-agent.md").write_text("# PM Agent\nYou are a PM...")
            (agents_dir / "architect-agent.md").write_text("# Architect Agent\nYou are an architect...")
            (agents_dir / "developer.md").write_text("# Developer Agent\nYou are a developer...")

            runner = BMADRunner(bmad_path=tmpdir)
            yield runner

    def test_recommend_workflow_bugfix(self, runner):
        """Test recommandation pour bugfix"""
        workflow = runner.recommend_workflow(Scope.BUGFIX)
        assert workflow == Workflow.QUICK

    def test_recommend_workflow_hotfix(self, runner):
        """Test recommandation pour hotfix"""
        workflow = runner.recommend_workflow(Scope.HOTFIX)
        assert workflow == Workflow.QUICK

    def test_recommend_workflow_feature_simple(self, runner):
        """Test recommandation pour feature simple"""
        workflow = runner.recommend_workflow(Scope.FEATURE, Complexity.SIMPLE)
        assert workflow == Workflow.QUICK

    def test_recommend_workflow_feature_moderate(self, runner):
        """Test recommandation pour feature modérée"""
        workflow = runner.recommend_workflow(Scope.FEATURE, Complexity.MODERATE)
        assert workflow == Workflow.FEATURE

    def test_recommend_workflow_feature_enterprise(self, runner):
        """Test recommandation pour feature enterprise"""
        workflow = runner.recommend_workflow(Scope.FEATURE, Complexity.ENTERPRISE)
        assert workflow == Workflow.ENTERPRISE

    def test_recommend_workflow_greenfield(self, runner):
        """Test recommandation pour greenfield"""
        workflow = runner.recommend_workflow(Scope.GREENFIELD, Complexity.COMPLEX)
        assert workflow == Workflow.METHOD

    def test_recommend_workflow_greenfield_enterprise(self, runner):
        """Test recommandation pour greenfield enterprise"""
        workflow = runner.recommend_workflow(Scope.GREENFIELD, Complexity.ENTERPRISE)
        assert workflow == Workflow.ENTERPRISE

    def test_register_custom_agent(self, runner):
        """Test enregistrement agent custom"""
        runner.register_custom_agent("test-agent", "Test prompt")
        assert "test-agent" in runner.custom_agents
        assert runner.get_agent_prompt("test-agent") == "Test prompt"

    def test_get_agent_prompt_not_found(self, runner):
        """Test agent non trouvé"""
        prompt = runner.get_agent_prompt("nonexistent")
        assert prompt is None

    def test_list_agents_empty(self, runner):
        """Test liste agents vide"""
        agents = runner.list_agents()
        assert agents == {}

    def test_load_agents(self, runner_with_agents):
        """Test chargement des agents"""
        assert len(runner_with_agents.agents) == 3
        assert "pm" in runner_with_agents.agents
        assert "architect" in runner_with_agents.agents
        assert "developer" in runner_with_agents.agents

    def test_build_prompt(self, runner):
        """Test construction du prompt"""
        agent_prompt = "You are an agent"
        task = "Do something"
        context = {"previous": "Some result"}

        result = runner._build_prompt(agent_prompt, task, context)

        assert "Agent Instructions" in result
        assert "You are an agent" in result
        assert "Current Task" in result
        assert "Do something" in result
        assert "previous" in result

    @pytest.mark.asyncio
    async def test_run_agent_not_found(self, runner):
        """Test exécution agent non trouvé"""
        result = await runner.run_agent("nonexistent", "task")
        assert result.status == "error"
        assert "not found" in result.output


class TestAgentResult:
    """Tests du modèle AgentResult"""

    def test_agent_result_creation(self):
        """Test création d'un résultat"""
        result = AgentResult(
            agent="test",
            status="success",
            output="Test output",
            duration_ms=100
        )
        assert result.agent == "test"
        assert result.status == "success"
        assert result.duration_ms == 100

    def test_agent_result_with_metadata(self):
        """Test résultat avec métadonnées"""
        result = AgentResult(
            agent="test",
            status="success",
            output="output",
            duration_ms=50,
            metadata={"model": "gpt-4", "tokens": 100}
        )
        assert result.metadata["model"] == "gpt-4"
