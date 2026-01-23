"""Tests pour les Agents DZ (Algérie)"""

import pytest
from unittest.mock import MagicMock

from src.agents_dz import (
    CUSTOM_AGENTS,
    CUSTOM_AGENTS_INFO,
    register_dz_agents,
    get_dz_agent_info,
    list_dz_agents,
)
from src.runner import BMADRunner


class TestCustomAgents:
    """Tests des agents custom Algérie"""

    def test_conformity_dz_agent_defined(self):
        """Test que l'agent conformité est défini"""
        assert "conformity-dz" in CUSTOM_AGENTS
        assert "CNAS" in CUSTOM_AGENTS["conformity-dz"]
        assert "Chargily" in CUSTOM_AGENTS["conformity-dz"]

    def test_darija_content_agent_defined(self):
        """Test que l'agent Darija est défini"""
        assert "darija-content" in CUSTOM_AGENTS
        assert "Darija" in CUSTOM_AGENTS["darija-content"]
        assert "Wesh" in CUSTOM_AGENTS["darija-content"]

    def test_gov_integration_agent_defined(self):
        """Test que l'agent GOV est défini"""
        assert "gov-integration" in CUSTOM_AGENTS
        assert "CNAS" in CUSTOM_AGENTS["gov-integration"]
        assert "CNRC" in CUSTOM_AGENTS["gov-integration"]
        assert "Sonelgaz" in CUSTOM_AGENTS["gov-integration"]

    def test_chargily_payment_agent_defined(self):
        """Test que l'agent Chargily est défini"""
        assert "chargily-payment" in CUSTOM_AGENTS
        assert "CIB" in CUSTOM_AGENTS["chargily-payment"]
        assert "EDAHABIA" in CUSTOM_AGENTS["chargily-payment"]

    def test_all_agents_have_info(self):
        """Test que tous les agents ont des infos"""
        for agent_name in CUSTOM_AGENTS:
            assert agent_name in CUSTOM_AGENTS_INFO
            info = CUSTOM_AGENTS_INFO[agent_name]
            assert info.name
            assert info.description
            assert info.category
            assert info.tags

    def test_register_dz_agents(self):
        """Test enregistrement dans le runner"""
        runner = MagicMock(spec=BMADRunner)
        runner.register_custom_agent = MagicMock()

        register_dz_agents(runner)

        # Vérifier que tous les agents sont enregistrés
        assert runner.register_custom_agent.call_count == len(CUSTOM_AGENTS)

    def test_get_dz_agent_info(self):
        """Test récupération info agent"""
        info = get_dz_agent_info("conformity-dz")
        assert info is not None
        assert info.name == "Conformity DZ Agent"
        assert "algérie" in info.tags

    def test_get_dz_agent_info_not_found(self):
        """Test agent non trouvé"""
        info = get_dz_agent_info("nonexistent")
        assert info is None

    def test_list_dz_agents(self):
        """Test liste des agents"""
        agents = list_dz_agents()
        assert len(agents) == 4
        assert all(hasattr(a, "name") for a in agents)


class TestAgentContent:
    """Tests du contenu des agents"""

    def test_conformity_covers_payment(self):
        """Test que la conformité couvre le paiement"""
        prompt = CUSTOM_AGENTS["conformity-dz"]
        assert "Chargily" in prompt
        assert "Stripe" in prompt  # Mentionné comme interdit

    def test_conformity_covers_data_protection(self):
        """Test que la conformité couvre la protection des données"""
        prompt = CUSTOM_AGENTS["conformity-dz"]
        assert "données personnelles" in prompt.lower() or "protection" in prompt.lower()

    def test_darija_has_examples(self):
        """Test que l'agent Darija a des exemples"""
        prompt = CUSTOM_AGENTS["darija-content"]
        assert "Wesh" in prompt
        assert "Kayen" in prompt
        assert "Bezaf" in prompt

    def test_gov_covers_main_systems(self):
        """Test que l'agent GOV couvre les systèmes principaux"""
        prompt = CUSTOM_AGENTS["gov-integration"]
        systems = ["CNAS", "CASNOS", "CNRC", "DGI", "Sonelgaz"]
        for system in systems:
            assert system in prompt

    def test_chargily_has_api_info(self):
        """Test que l'agent Chargily a les infos API"""
        prompt = CUSTOM_AGENTS["chargily-payment"]
        assert "API" in prompt
        assert "checkouts" in prompt
        assert "webhooks" in prompt.lower()
