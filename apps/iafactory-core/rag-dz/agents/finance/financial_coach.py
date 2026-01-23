"""
Financial Coach Agent - Personal finance for PMEs and individuals (CH + DZ)
"""
from typing import Dict, Any
from ..core.base_agent import BaseAgent, AgentConfig, AgentResponse
import logging

logger = logging.getLogger(__name__)

FINANCIAL_KNOWLEDGE = {
    "algeria": {"currency": "DZD", "avg_salary": 40000, "inflation_rate": 9.3, "savings_rate_recommended": 20},
    "switzerland": {"currency": "CHF", "avg_salary": 6500, "inflation_rate": 1.7, "savings_rate_recommended": 15, "pillar_3a_max": 7056}
}

class FinancialCoachAgent(BaseAgent):
    def __init__(self, config: AgentConfig = None):
        if config is None:
            config = AgentConfig(name="FinancialCoach", model="deepseek-chat", temperature=0.6, language="fr")
        super().__init__(config)
    
    async def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        country = input_data.get("country", "algeria")
        income = input_data.get("monthly_income")
        expenses = input_data.get("monthly_expenses")
        savings_goal = input_data.get("savings_goal")
        debt = input_data.get("debt", 0)
        goals = input_data.get("goals", [])
        
        financial_data = FINANCIAL_KNOWLEDGE.get(country, FINANCIAL_KNOWLEDGE["algeria"])
        
        system_prompt = f"""Tu es un coach financier expert.

CONTEXTE: {country.upper()}
Données: {financial_data}

SITUATION CLIENT:
- Revenu: {income} {financial_data['currency']}
- Dépenses: {expenses} {financial_data['currency']}
- Épargne cible: {savings_goal}
- Dettes: {debt}
- Objectifs: {goals}

ANALYSE:
1. 📊 Diagnostic budget
2. 💡 Plan d'optimisation
3. 🎯 Stratégie épargne
4. 💳 Gestion dettes
5. 📈 Investissement
6. 📋 Optimisation fiscale
7. ✅ Plan d'action 90 jours

⚠️ DISCLAIMER: Ceci n'est pas un conseil financier certifié.
"""
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": "Analyse ma situation et crée un plan financier"}]
        response = await self._call_llm(messages)
        
        savings_capacity = (income or 0) - (expenses or 0)
        return AgentResponse(content=response['content'], metadata={"country": country, "savings_capacity": savings_capacity})

class BudgetPlannerAgent(BaseAgent):
    def __init__(self, config: AgentConfig = None):
        if config is None:
            config = AgentConfig(name="BudgetPlanner", model="deepseek-chat", temperature=0.5, language="fr")
        super().__init__(config)
    
    async def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        income = input_data.get("income")
        categories = input_data.get("expense_categories", {})
        
        system_prompt = f"""Crée un plan budgétaire selon la règle 50/30/20:

REVENU: {income}
CATÉGORIES ACTUELLES: {categories}

RÉPARTITION:
- 50% Besoins essentiels
- 30% Envies
- 20% Épargne

Génère:
1. Budget détaillé par catégorie
2. Comparaison avec situation actuelle
3. Ajustements nécessaires
"""
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": "Crée mon plan budgétaire"}]
        response = await self._call_llm(messages)
        return AgentResponse(content=response['content'])

__all__ = ['FinancialCoachAgent', 'BudgetPlannerAgent', 'FINANCIAL_KNOWLEDGE']
