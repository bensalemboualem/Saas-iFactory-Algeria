"""
Travel Agent - Specialized for Algerian tourism
"""
from typing import Dict, Any
from ..core.base_agent import BaseAgent, AgentConfig, AgentResponse
import logging

logger = logging.getLogger(__name__)

ALGERIAN_DESTINATIONS = {
    "sahara": {
        "tamanrasset": {"type": "desert", "best_season": "Oct-Mar", "budget_dzd": 50000},
        "djanet": {"type": "desert", "best_season": "Oct-Mar", "budget_dzd": 60000},
        "timimoun": {"type": "oasis", "best_season": "Oct-Apr", "budget_dzd": 40000},
        "ghardaia": {"type": "oasis", "best_season": "Sep-May", "budget_dzd": 35000}
    },
    "cote": {
        "tipaza": {"type": "plage", "best_season": "Jun-Sep", "budget_dzd": 25000},
        "jijel": {"type": "plage", "best_season": "Jun-Sep", "budget_dzd": 30000},
        "bejaia": {"type": "plage", "best_season": "Jun-Sep", "budget_dzd": 28000},
        "oran": {"type": "ville_cotiere", "best_season": "May-Oct", "budget_dzd": 35000}
    },
    "culture": {
        "alger": {"type": "capitale", "best_season": "All year", "budget_dzd": 40000},
        "constantine": {"type": "historique", "best_season": "Mar-Jun, Sep-Nov", "budget_dzd": 30000},
        "tlemcen": {"type": "historique", "best_season": "Mar-Jun, Sep-Nov", "budget_dzd": 28000}
    }
}

class TravelAgent(BaseAgent):
    def __init__(self, config: AgentConfig = None):
        if config is None:
            config = AgentConfig(name="TravelAgent", model="deepseek-chat", temperature=0.7, language="fr")
        super().__init__(config)
    
    async def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        query = input_data.get("query", "")
        preferences = input_data.get("preferences", {})
        
        system_prompt = f"""Tu es un expert en voyage spécialisé dans le tourisme algérien.

DESTINATIONS DISPONIBLES:
{ALGERIAN_DESTINATIONS}

PRÉFÉRENCES UTILISATEUR:
- Budget: {preferences.get('budget', 'moyen')}
- Durée: {preferences.get('duration_days', 5)} jours
- Intérêts: {preferences.get('interests', ['découverte'])}
- Saison: {preferences.get('season', 'actuelle')}

MISSION:
1. Recommander les meilleures destinations
2. Proposer un itinéraire détaillé jour par jour
3. Estimer le budget total en DZD
4. Donner des conseils pratiques (transport, hébergement, cuisine)
5. Mentionner les points d'intérêt culturels

FORMAT:
🎯 RECOMMANDATION PRINCIPALE
📍 ITINÉRAIRE DÉTAILLÉ (jour par jour)
💰 BUDGET ESTIMÉ
🚗 TRANSPORT
🏨 HÉBERGEMENT
🍽️ GASTRONOMIE LOCALE
💡 CONSEILS PRATIQUES
"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
        
        response = await self._call_llm(messages)
        
        return AgentResponse(
            content=response['content'],
            tokens_used=response.get('tokens'),
            metadata={"destinations": list(ALGERIAN_DESTINATIONS.keys()), "preferences": preferences}
        )

__all__ = ['TravelAgent', 'ALGERIAN_DESTINATIONS']
