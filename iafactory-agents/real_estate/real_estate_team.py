"""
Real Estate Agent Team - Specialized for Algerian market
"""
from typing import Dict, Any
from ..core.base_agent import BaseAgent, AgentConfig, AgentResponse, MultiAgentTeam
import logging

logger = logging.getLogger(__name__)

ALGERIAN_PROPERTIES = {
    "wilayas": {
        "Alger": {"communes": ["Hydra", "El Biar", "Dély Ibrahim", "Ben Aknoun"], "price_range_m2": {"low": 150000, "medium": 250000, "high": 400000}},
        "Oran": {"communes": ["Sidi El Houari", "El Hamri", "Bir El Djir"], "price_range_m2": {"low": 100000, "medium": 180000, "high": 300000}},
        "Constantine": {"communes": ["Ziadia", "Belle Vue", "El Khroub"], "price_range_m2": {"low": 80000, "medium": 150000, "high": 250000}},
        "Annaba": {"communes": ["Seraïdi", "Sidi Amar"], "price_range_m2": {"low": 70000, "medium": 120000, "high": 200000}},
        "Tizi-Ouzou": {"communes": ["Nouvelle ville", "Boukhalfa"], "price_range_m2": {"low": 90000, "medium": 160000, "high": 280000}}
    },
    "property_types": ["appartement", "villa", "studio", "duplex", "terrain"]
}

class PropertySearchAgent(BaseAgent):
    def __init__(self, config: AgentConfig = None):
        if config is None:
            config = AgentConfig(name="PropertySearchAgent", model="deepseek-chat", temperature=0.6, language="fr")
        super().__init__(config)
    
    async def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        wilaya = input_data.get("wilaya")
        property_type = input_data.get("property_type", "appartement")
        max_price = input_data.get("max_price")
        min_surface = input_data.get("min_surface")
        rooms = input_data.get("rooms")
        
        system_prompt = f"""Tu es un expert immobilier algérien.

CRITÈRES:
- Wilaya: {wilaya}
- Type: {property_type}
- Budget max: {max_price} DZD
- Surface min: {min_surface} m²
- Chambres: {rooms}

BASE DONNÉES: {ALGERIAN_PROPERTIES}

Propose 3-5 biens avec:
📍 Localisation
🏠 Type et surface
💰 Prix estimé
📋 Caractéristiques
✨ Points forts
"""
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": "Recherche les biens correspondants"}]
        response = await self._call_llm(messages)
        return AgentResponse(content=response['content'], metadata={"wilaya": wilaya, "property_type": property_type})

class MarketAnalysisAgent(BaseAgent):
    def __init__(self, config: AgentConfig = None):
        if config is None:
            config = AgentConfig(name="MarketAnalysisAgent", model="deepseek-chat", temperature=0.5, language="fr")
        super().__init__(config)
    
    async def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        wilaya = input_data.get("wilaya")
        property_type = input_data.get("property_type")
        
        system_prompt = f"""Tu es un analyste du marché immobilier algérien.

ZONE: {wilaya}
TYPE: {property_type}
DONNÉES: {ALGERIAN_PROPERTIES}

Analyse:
📊 Prix moyen au m²
📈 Tendances (hausse/baisse)
🔥 Quartiers en demande
💡 Recommandations achat/vente
⚠️ Risques
"""
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": f"Analyse le marché de {wilaya}"}]
        response = await self._call_llm(messages)
        return AgentResponse(content=response['content'], metadata={"wilaya": wilaya})

class RealEstateTeam(MultiAgentTeam):
    def __init__(self):
        agents = [PropertySearchAgent(), MarketAnalysisAgent()]
        super().__init__(agents, orchestrator="sequential")
    
    async def complete_search(self, criteria: Dict[str, Any]) -> Dict[str, Any]:
        properties = await self.agents[0].execute(criteria)
        analysis = await self.agents[1].execute({"wilaya": criteria.get("wilaya"), "property_type": criteria.get("property_type")})
        return {"properties": properties.content, "market_analysis": analysis.content}

__all__ = ['RealEstateTeam', 'PropertySearchAgent', 'MarketAnalysisAgent', 'ALGERIAN_PROPERTIES']
