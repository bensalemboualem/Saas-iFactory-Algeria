"""
Integration tests for orchestrator API endpoints
"""
import pytest
from fastapi.testclient import TestClient


class TestOrchestratorAPI:
    """Test suite for /api/orchestrator endpoints"""

    def test_health_check(self, client: TestClient):
        """Test orchestrator health endpoint"""
        response = client.get("/api/orchestrator/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["agent"] == "Orchestrator #20"

    def test_analyze_readiness_empty(self, client: TestClient):
        """Test project readiness analysis with empty messages"""
        response = client.post("/api/orchestrator/analyze-readiness", json={
            "messages": [],
            "agents_used": []
        })

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["analysis"]["project_ready"] is False
        assert data["analysis"]["confidence_score"] == 0

    def test_analyze_readiness_with_data(self, client: TestClient):
        """Test project readiness analysis with real messages"""
        response = client.post("/api/orchestrator/analyze-readiness", json={
            "messages": [
                {"role": "user", "content": "Build a React app with FastAPI backend"},
                {"role": "assistant", "content": "Let me design the architecture", "agent": "bmm-architect"}
            ],
            "agents_used": ["bmm-architect"]
        })

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "analysis" in data
        assert data["analysis"]["confidence_score"] > 0

    def test_synthesize_knowledge(self, client: TestClient):
        """Test knowledge synthesis endpoint"""
        response = client.post("/api/orchestrator/synthesize-knowledge", json={
            "messages": [
                {"role": "user", "content": "Create a todo application"},
                {"role": "assistant", "content": "I'll create the requirements", "agent": "bmm-pm"}
            ],
            "agents_used": ["bmm-pm"]
        })

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "knowledge_document" in data
        assert len(data["knowledge_document"]) > 0

    def test_order_production(self, client: TestClient):
        """Test production order endpoint"""
        response = client.post("/api/orchestrator/order-production", json={
            "project_id": "test-project-1",
            "project_name": "Test App",
            "tech_stack": ["React", "FastAPI"],
            "knowledge_base_id": "kb-123"
        })

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "production_command" in data
        assert data["production_command"]["command"] == "PRODUCE_PROJECT"
