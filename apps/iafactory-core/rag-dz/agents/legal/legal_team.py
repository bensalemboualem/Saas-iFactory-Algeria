"""
Legal Agent Team - Specialized in Algerian legal systems
"""
from typing import Dict, Any
from ..core.base_agent import BaseAgent, AgentConfig, AgentResponse, MultiAgentTeam
import logging

logger = logging.getLogger(__name__)

LEGAL_SYSTEMS = {
    "algeria": {
        "main_codes": ["Code Civil", "Code du Commerce", "Code du Travail", "Code de la Famille"],
        "business_types": ["SARL", "SPA", "EURL", "SNC", "EI"],
        "labor_law": {"min_wage": 20000, "work_hours": "40h/week", "paid_leave": "30 jours/an"}
    }
}

class ContractAnalystAgent(BaseAgent):
    def __init__(self, config: AgentConfig = None):
        if config is None:
            config = AgentConfig(name="ContractAnalyst", model="deepseek-chat", temperature=0.3, language="fr")
        super().__init__(config)
    
    async def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        contract_text = input_data.get("contract_text")
        contract_type = input_data.get("contract_type")
        country = input_data.get("country", "algeria")
        
        legal_system = LEGAL_SYSTEMS.get(country)
        
        system_prompt = f"""Tu es un expert juridique en droit {country.upper()}.

SYSTÈME: {legal_system}
TYPE CONTRAT: {contract_type}

ANALYSE:
1. 📋 Synthèse exécutive
2. 📄 Clauses principales
3. ⚠️ Points d'attention
4. ✅ Recommandations
5. 📊 Conformité légale
6. 🚨 Risques identifiés

⚠️ DISCLAIMER: Consultation avocat recommandée.
"""
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": f"Analyse ce contrat:\n\n{contract_text}"}]
        response = await self._call_llm(messages)
        return AgentResponse(content=response['content'], metadata={"contract_type": contract_type, "country": country})

class DocumentGeneratorAgent(BaseAgent):
    def __init__(self, config: AgentConfig = None):
        if config is None:
            config = AgentConfig(name="DocumentGenerator", model="deepseek-chat", temperature=0.4, language="fr")
        super().__init__(config)
    
    async def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        document_type = input_data.get("document_type")
        parties = input_data.get("parties", {})
        country = input_data.get("country", "algeria")
        specifications = input_data.get("specifications", {})
        
        system_prompt = f"""Tu es un expert en rédaction juridique.

TYPE DOCUMENT: {document_type}
PAYS: {country}
PARTIES: {parties}
SPÉCIFICATIONS: {specifications}

Génère un document légal complet avec:
- En-tête formel
- Articles numérotés
- Clauses standard
- Signatures
- Mentions légales obligatoires

⚠️ DISCLAIMER: Document à valider par un avocat.
"""
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": f"Génère un {document_type}"}]
        response = await self._call_llm(messages)
        return AgentResponse(content=response['content'], metadata={"document_type": document_type, "country": country})

class LegalTeam(MultiAgentTeam):
    def __init__(self):
        agents = [ContractAnalystAgent(), DocumentGeneratorAgent()]
        super().__init__(agents, orchestrator="sequential")

__all__ = ['LegalTeam', 'ContractAnalystAgent', 'DocumentGeneratorAgent', 'LEGAL_SYSTEMS']
