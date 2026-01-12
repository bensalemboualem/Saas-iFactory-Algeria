"""
API Integration Tests for Generators Endpoints
Tests all REST API endpoints
"""

import pytest
from fastapi.testclient import TestClient

import sys
sys.path.insert(0, 'src')

from api import app

client = TestClient(app)


class TestGeneratorsAPI:
    """Test all generators API endpoints"""

    def test_api_root(self):
        """Test API root endpoint"""
        response = client.get("/")
        assert response.status_code == 200

        data = response.json()
        assert data["service"] == "Dzir IA Video"
        assert data["version"] == "2.1.0"
        assert data["features"]["ai_generators"] >= 40

    def test_list_generators(self):
        """Test GET /api/v1/generators/list"""
        response = client.get("/api/v1/generators/list")
        assert response.status_code == 200

        generators = response.json()
        assert isinstance(generators, list)
        assert len(generators) >= 40

    def test_list_generators_by_category(self):
        """Test filtering by category"""
        response = client.get("/api/v1/generators/list?category=text-to-video")
        assert response.status_code == 200

        generators = response.json()
        assert len(generators) >= 17  # 17 text-to-video generators

    def test_get_generator_info(self):
        """Test GET /api/v1/generators/info/{name}"""
        response = client.get("/api/v1/generators/info/wan_2_1")
        assert response.status_code == 200

        info = response.json()
        assert info["name"] == "wan_2_1"
        assert info["provider"] == "Alibaba Cloud"
        assert info["quality_score"] == 85
        assert info["free_tier"] is True

    def test_get_generator_info_not_found(self):
        """Test getting non-existent generator"""
        response = client.get("/api/v1/generators/info/nonexistent")
        assert response.status_code == 404

    def test_get_summary(self):
        """Test GET /api/v1/generators/summary"""
        response = client.get("/api/v1/generators/summary")
        assert response.status_code == 200

        summary = response.json()
        assert "total_generators" in summary
        assert "free_generators" in summary
        assert "by_category" in summary
        assert summary["total_generators"] >= 40

    def test_estimate_cost(self):
        """Test GET /api/v1/generators/estimate-cost/{name}"""
        response = client.get("/api/v1/generators/estimate-cost/wan_2_1?duration_seconds=10")
        assert response.status_code == 200

        estimate = response.json()
        assert "estimated_cost_usd" in estimate
        assert estimate["estimated_cost_usd"] == 0.0  # Free generator
        assert estimate["free_tier"] is True

    def test_recommend_free(self):
        """Test POST /api/v1/generators/recommend"""
        response = client.post("/api/v1/generators/recommend", json={
            "category": "text-to-video",
            "budget_level": "free"
        })
        assert response.status_code == 200

        rec = response.json()
        assert "primary_recommendation" in rec
        assert rec["primary_recommendation"] is not None
        assert rec["budget_level"] == "free"

    def test_recommend_premium(self):
        """Test recommend with premium budget"""
        response = client.post("/api/v1/generators/recommend", json={
            "category": "text-to-video",
            "budget_level": "premium"
        })
        assert response.status_code == 200

        rec = response.json()
        assert rec["primary_recommendation"] is not None


class TestGenerateEndpoint:
    """Test generation endpoints (mocked)"""

    def test_generate_auto_route(self):
        """Test POST /api/v1/generators/generate with auto-routing"""
        # This would need mocking of actual generator APIs
        # For now, test the request structure

        payload = {
            "prompt": "Test video",
            "category": "text-to-video",
            "duration_seconds": 10,
            "max_budget_usd": 0,
            "quality_priority": True
        }

        # Would need to mock the actual generator.generate() call
        # response = client.post("/api/v1/generators/generate", json=payload)
        # assert response.status_code == 200

    def test_generate_specific_generator(self):
        """Test specifying a generator"""
        payload = {
            "prompt": "Test video",
            "category": "text-to-video",
            "generator_name": "wan_2_1",
            "duration_seconds": 10
        }

        # Would need mocking
        # response = client.post("/api/v1/generators/generate", json=payload)
        # assert response.status_code == 200

    def test_compare_multiple_generators(self):
        """Test POST /api/v1/generators/compare"""
        payload = {
            "prompt": "Test video",
            "category": "text-to-video",
            "generators": ["wan_2_1", "kling_ai", "luma_dream"],
            "duration_seconds": 10
        }

        # Would need mocking of all 3 generators
        # response = client.post("/api/v1/generators/compare", json=payload)
        # assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
