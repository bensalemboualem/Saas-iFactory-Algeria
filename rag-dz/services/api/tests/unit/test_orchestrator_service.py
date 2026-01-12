"""
Unit tests for OrchestratorService
"""
import pytest
from app.services.orchestrator_service import orchestrator_service


class TestOrchestratorService:
    """Test suite for orchestrator service"""

    def test_analyze_project_readiness_empty(self):
        """Test project readiness analysis with empty data"""
        messages = []
        agents_used = []

        result = orchestrator_service.analyze_project_readiness(messages, agents_used)

        assert result["project_ready"] is False
        assert result["confidence_score"] == 0
        assert len(result["missing_elements"]) > 0

    def test_analyze_project_readiness_with_architect(self):
        """Test project readiness with architect agent"""
        messages = [
            {"role": "user", "content": "I need a microservices architecture with React frontend"},
            {"role": "assistant", "content": "Let me design a microservices architecture for you", "agent": "bmm-architect"}
        ]
        agents_used = ["bmm-architect"]

        result = orchestrator_service.analyze_project_readiness(messages, agents_used)

        assert result["signals"]["architecture_defined"] is True
        assert result["confidence_score"] > 0

    def test_detect_project_signals_tech_stack(self):
        """Test tech stack detection from messages"""
        messages = [
            {"role": "user", "content": "Build with React, FastAPI, and PostgreSQL"}
        ]
        agents_used = []

        signals = orchestrator_service._detect_project_signals(messages, agents_used)

        assert signals["tech_stack_chosen"] is True

    def test_synthesize_knowledge_basic(self):
        """Test knowledge synthesis"""
        messages = [
            {"role": "user", "content": "Create a todo app"},
            {"role": "assistant", "content": "I'll help you create a todo application", "agent": "bmm-pm"}
        ]
        agents_used = ["bmm-pm"]

        knowledge_doc = orchestrator_service.synthesize_knowledge(messages, agents_used)

        assert isinstance(knowledge_doc, str)
        assert len(knowledge_doc) > 0
        assert "Knowledge Base" in knowledge_doc
        assert "bmm-pm" in knowledge_doc or "Product Manager" in knowledge_doc

    def test_order_bolt_production(self):
        """Test Bolt production order creation"""
        result = orchestrator_service.order_bolt_production(
            project_id="test-123",
            project_name="Test Project",
            tech_stack=["React", "FastAPI"],
            knowledge_base_id="kb-456"
        )

        assert result["command"] == "PRODUCE_PROJECT"
        assert result["project_id"] == "test-123"
        assert result["project_name"] == "Test Project"
        assert "React" in result["tech_stack"]
        assert "bolt_url" in result
        assert "kb-456" in result["bolt_url"]
