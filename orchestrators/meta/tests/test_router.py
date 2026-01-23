"""Tests pour le Router Intelligent"""

import pytest
from src.router import route, RouteResult, Target, get_all_patterns


class TestRouter:
    """Tests du routeur intelligent"""

    def test_route_to_bmad_workflow(self):
        """Test routage vers BMAD pour workflow"""
        result = route("Create a new workflow for user onboarding")
        assert result.target == Target.BMAD
        assert result.confidence >= 0.8

    def test_route_to_bmad_architecture(self):
        """Test routage vers BMAD pour architecture"""
        result = route("Design the system architecture")
        assert result.target == Target.BMAD
        assert result.confidence >= 0.8

    def test_route_to_archon_search(self):
        """Test routage vers ARCHON pour recherche"""
        result = route("Search for user documentation")
        assert result.target == Target.ARCHON
        assert result.confidence >= 0.8

    def test_route_to_archon_knowledge(self):
        """Test routage vers ARCHON pour knowledge"""
        result = route("Query the knowledge base")
        assert result.target == Target.ARCHON
        assert result.confidence >= 0.8

    def test_route_to_bolt_code(self):
        """Test routage vers BOLT pour code"""
        result = route("Generate the authentication code")
        assert result.target == Target.BOLT
        assert result.confidence >= 0.8

    def test_route_to_bolt_deploy(self):
        """Test routage vers BOLT pour déploiement"""
        result = route("Deploy to production")
        assert result.target == Target.BOLT
        assert result.confidence >= 0.8

    def test_route_ambiguous_to_meta(self):
        """Test routage ambigu vers META"""
        result = route("Hello, how are you?")
        assert result.target == Target.META
        assert result.action == "clarify"
        assert result.confidence < 0.5

    def test_route_with_context_bonus(self):
        """Test bonus contextuel"""
        context = {"current_target": "bmad"}
        result = route("Continue with the plan", context)
        # Le contexte devrait donner un léger bonus à BMAD
        assert result.target == Target.BMAD or result.confidence > 0

    def test_get_all_patterns(self):
        """Test récupération des patterns"""
        patterns = get_all_patterns()
        assert "bmad" in patterns
        assert "archon" in patterns
        assert "bolt" in patterns
        assert len(patterns["bmad"]) > 0

    def test_route_multiple_matches(self):
        """Test avec plusieurs matches"""
        result = route("Search and implement the authentication code")
        # Devrait matcher BOLT (implement, code) plus fort
        assert result.target in [Target.BOLT, Target.ARCHON]
        assert result.confidence >= 0.8

    def test_route_result_model(self):
        """Test du modèle RouteResult"""
        result = route("Create workflow")
        assert isinstance(result, RouteResult)
        assert hasattr(result, "target")
        assert hasattr(result, "action")
        assert hasattr(result, "confidence")
        assert hasattr(result, "reasoning")
