"""
Flexible Council Orchestrator - Accepte n'importe quelle combinaison de LLMs
"""
from typing import List, Dict, Any, Optional
import asyncio
from datetime import datetime
import logging

from .universal_provider import UniversalProvider
from .models_config import AvailableModels

logger = logging.getLogger(__name__)


class FlexibleCouncilOrchestrator:
    """Orchestrateur qui accepte n'importe quelle combinaison de LLMs"""

    def __init__(
        self,
        expert1: str,
        expert2: str,
        expert3: str,
        chairman: str,
        enable_review: bool = False
    ):
        self.experts = [expert1, expert2, expert3]
        self.chairman = chairman
        self.enable_review = enable_review

        # Validation
        all_models = self.experts + [self.chairman]
        for model in all_models:
            if model not in AvailableModels.MODELS:
                raise ValueError(f"Modèle inconnu: {model}")

        logger.info(f"Council créé avec experts: {self.experts}, chairman: {self.chairman}")

    async def process_query(
        self,
        user_query: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Pipeline complet personnalisable"""

        start_time = datetime.now()

        # Estimation coûts
        estimated_cost = AvailableModels.estimate_cost(
            self.experts + [self.chairman]
        )
        estimated_time = AvailableModels.estimate_time(
            self.experts + [self.chairman]
        )

        logger.info(f"Début traitement query. Coût estimé: ${estimated_cost:.4f}")

        # Stage 1: Opinions des experts
        opinions = await self._gather_opinions(user_query, context)

        # Stage 2: Review croisée (optionnel)
        rankings = None
        if self.enable_review:
            logger.info("Stage 2: Review croisée activée")
            rankings = await self._cross_review(opinions, user_query)

        # Stage 3: Synthèse par chairman
        logger.info("Stage 3: Synthèse finale par chairman")
        final_response = await self._chairman_synthesis(
            opinions,
            rankings,
            user_query
        )

        execution_time = (datetime.now() - start_time).total_seconds()

        # Calcul coût réel (approximatif)
        actual_cost = self._calculate_actual_cost(opinions, final_response)

        logger.info(f"Traitement terminé en {execution_time:.2f}s, coût: ${actual_cost:.4f}")

        return {
            "final_response": final_response,
            "opinions": opinions,
            "rankings": rankings,
            "metadata": {
                "experts": [
                    {
                        "id": exp,
                        "name": AvailableModels.MODELS[exp]["name"],
                        "icon": AvailableModels.MODELS[exp]["icon"]
                    }
                    for exp in self.experts
                ],
                "chairman": {
                    "id": self.chairman,
                    "name": AvailableModels.MODELS[self.chairman]["name"],
                    "icon": AvailableModels.MODELS[self.chairman]["icon"]
                },
                "execution_time": execution_time,
                "estimated_cost": estimated_cost,
                "actual_cost": actual_cost,
                "estimated_time_range": estimated_time,
                "review_enabled": self.enable_review
            }
        }

    async def _gather_opinions(
        self,
        query: str,
        context: Optional[str]
    ) -> Dict[str, str]:
        """Collecte opinions en parallèle"""

        logger.info("Stage 1: Collecte opinions des experts")

        prompt = query
        if context:
            prompt = f"Contexte:\n{context}\n\nQuestion:\n{query}"

        system = """Tu es un expert consultant. Fournis une réponse
        précise, structurée et factuelle."""

        # Créer tasks parallèles
        tasks = []
        for expert in self.experts:
            provider = UniversalProvider.get_provider(expert)
            task = provider.generate(prompt, system)
            tasks.append((expert, task))

        # Exécution parallèle
        opinions = {}
        results = await asyncio.gather(
            *[task for _, task in tasks],
            return_exceptions=True
        )

        for (expert, _), result in zip(tasks, results):
            expert_name = AvailableModels.MODELS[expert]["name"]
            if isinstance(result, Exception):
                logger.error(f"Erreur {expert_name}: {result}")
                opinions[expert] = f"❌ Erreur: {str(result)}"
            else:
                logger.info(f"✓ Opinion reçue de {expert_name}")
                opinions[expert] = result

        return opinions

    async def _cross_review(
        self,
        opinions: Dict[str, str],
        query: str
    ) -> Dict[str, Any]:
        """Review croisée des opinions"""

        # Anonymiser
        anonymized = {}
        reverse_map = {}
        for i, (model_id, opinion) in enumerate(opinions.items(), 1):
            anon_key = f"Response_{i}"
            anonymized[anon_key] = opinion
            reverse_map[anon_key] = model_id

        rankings = {}

        for expert in self.experts:
            review_prompt = f"""Question: {query}

Voici plusieurs réponses à évaluer:

"""
            for key, opinion in anonymized.items():
                review_prompt += f"\n{key}:\n{opinion}\n\n---\n"

            review_prompt += """
Note chaque réponse sur:
- Précision (1-10)
- Pertinence (1-10)
- Clarté (1-10)

Format JSON:
{
  "Response_1": {"precision": X, "pertinence": Y, "clarte": Z},
  "Response_2": {...}
}
"""

            provider = UniversalProvider.get_provider(expert)
            try:
                review = await provider.generate(review_prompt)
                rankings[expert] = review
            except Exception as e:
                logger.error(f"Erreur review {expert}: {e}")
                rankings[expert] = f"Erreur review: {e}"

        return rankings

    async def _chairman_synthesis(
        self,
        opinions: Dict[str, str],
        rankings: Optional[Dict],
        query: str
    ) -> str:
        """Synthèse finale par le chairman"""

        synthesis_prompt = f"""Tu es le Chairman d'un conseil d'experts IA.

Question: {query}

Réponses des experts:

"""
        for model_id, opinion in opinions.items():
            model_name = AvailableModels.MODELS[model_id]["name"]
            synthesis_prompt += f"\n=== {model_name} ===\n{opinion}\n\n"

        if rankings:
            synthesis_prompt += f"\nÉvaluations croisées:\n{rankings}\n"

        synthesis_prompt += """

Synthétise ces réponses en UNE réponse finale optimale qui:
1. Intègre les meilleures contributions
2. Résout les contradictions
3. Fournit une réponse claire et actionnelle

Réponds UNIQUEMENT avec la synthèse, sans préambule."""

        chairman_provider = UniversalProvider.get_provider(self.chairman)
        final = await chairman_provider.generate(synthesis_prompt)

        return final

    def _calculate_actual_cost(
        self,
        opinions: Dict[str, str],
        final: str
    ) -> float:
        """Calcule coût réel approximatif"""

        # Approximation: 1 mot ≈ 1.3 tokens
        total_cost = 0.0

        for model_id, opinion in opinions.items():
            tokens = len(opinion.split()) * 1.3
            cost_per_1k = AvailableModels.MODELS[model_id]["cost_per_1k_tokens"]
            total_cost += (tokens / 1000) * cost_per_1k

        # Chairman
        chairman_tokens = len(final.split()) * 1.3
        chairman_cost = AvailableModels.MODELS[self.chairman]["cost_per_1k_tokens"]
        total_cost += (chairman_tokens / 1000) * chairman_cost

        return round(total_cost, 4)
