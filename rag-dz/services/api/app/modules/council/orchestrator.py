"""
Council Orchestrator - Gestionnaire principal du LLM Council
Coordonne les 3 étapes: Opinions → Review → Synthesis
"""
import asyncio
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from .providers import get_provider
from .config import council_config

logger = logging.getLogger(__name__)


class CouncilOrchestrator:
    """
    Orchestrateur principal du LLM Council

    Pipeline en 3 étapes:
    1. Stage 1: Chaque LLM donne son opinion indépendante
    2. Stage 2 (optionnel): Review croisée des opinions
    3. Stage 3: Chairman synthétise la réponse finale
    """

    def __init__(
        self,
        council_members: Optional[List[str]] = None,
        enable_review: bool = True,
        chairman: Optional[str] = None
    ):
        self.members = council_members or council_config.DEFAULT_COUNCIL
        self.chairman = chairman or council_config.CHAIRMAN
        self.enable_review = enable_review

        # Filtrer les membres disponibles
        available_providers = council_config.get_available_providers()
        self.members = [m for m in self.members if m in available_providers]

        if not self.members:
            raise ValueError("No available providers configured")

        if self.chairman not in available_providers:
            # Fallback au premier membre disponible
            self.chairman = self.members[0]

        logger.info(f"Council initialized with members: {self.members}, chairman: {self.chairman}")

    async def process_query(
        self,
        user_query: str,
        context: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Pipeline complet du Council

        Args:
            user_query: Question de l'utilisateur
            context: Contexte additionnel (optionnel)
            metadata: Métadonnées additionnelles

        Returns:
            Dict contenant la réponse finale, opinions, rankings et metadata
        """
        start_time = datetime.now()

        try:
            # Stage 1: Opinions initiales
            logger.info("Stage 1: Gathering opinions from council members")
            opinions = await self._stage1_opinions(user_query, context)

            # Stage 2: Review (optionnel)
            rankings = None
            if self.enable_review and len(opinions) > 1:
                logger.info("Stage 2: Cross-review of opinions")
                rankings = await self._stage2_review(opinions, user_query)

            # Stage 3: Synthèse finale
            logger.info("Stage 3: Chairman synthesis")
            final_response = await self._stage3_synthesis(
                opinions,
                rankings,
                user_query
            )

            execution_time = (datetime.now() - start_time).total_seconds()

            result = {
                "final_response": final_response,
                "opinions": opinions,
                "rankings": rankings,
                "metadata": {
                    "execution_time": execution_time,
                    "council_members": self.members,
                    "chairman": self.chairman,
                    "review_enabled": self.enable_review,
                    "timestamp": datetime.now().isoformat(),
                    **(metadata or {})
                }
            }

            logger.info(f"Council processing completed in {execution_time:.2f}s")
            return result

        except Exception as e:
            logger.error(f"Council processing error: {str(e)}", exc_info=True)
            raise

    async def _stage1_opinions(
        self,
        query: str,
        context: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Stage 1: Chaque LLM donne son opinion indépendante

        Returns:
            Dict[model_name, opinion]
        """
        # Construire le prompt complet
        prompt = query
        if context:
            prompt = f"Contexte:\n{context}\n\nQuestion:\n{query}"

        system_prompt = """Tu es un expert consultant. Réponds de manière précise, structurée et factuelle.
Si tu mentionnes des informations spécifiques, cite tes sources quand c'est applicable.
Sois concis mais complet."""

        # Appels parallèles pour rapidité
        tasks = []
        for member in self.members:
            try:
                provider = get_provider(member)
                if provider.is_available():
                    task = provider.generate(prompt, system_prompt)
                    tasks.append((member, task))
                else:
                    logger.warning(f"Provider {member} not available, skipping")
            except Exception as e:
                logger.error(f"Error initializing provider {member}: {e}")

        # Exécution parallèle avec gestion des erreurs
        opinions = {}
        results = await asyncio.gather(
            *[task for _, task in tasks],
            return_exceptions=True
        )

        for (member, _), result in zip(tasks, results):
            if isinstance(result, Exception):
                error_msg = f"Erreur lors de la génération: {str(result)}"
                opinions[member] = error_msg
                logger.error(f"Provider {member} failed: {error_msg}")
            else:
                opinions[member] = result

        if not opinions:
            raise Exception("No opinions could be generated from any provider")

        return opinions

    async def _stage2_review(
        self,
        opinions: Dict[str, str],
        original_query: str
    ) -> Dict[str, Dict]:
        """
        Stage 2: Chaque LLM évalue les autres (optionnel)

        Returns:
            Dict[reviewer_name, rankings]
        """
        # Anonymiser les réponses si configuré
        anonymized = self._anonymize_opinions(opinions) if council_config.ANONYMIZE_MODELS else opinions

        rankings = {}

        # Chaque membre évalue les autres
        for reviewer in self.members:
            try:
                # Créer prompt de review
                review_prompt = self._create_review_prompt(
                    anonymized,
                    original_query,
                    reviewer
                )

                provider = get_provider(reviewer)
                if not provider.is_available():
                    continue

                review = await provider.generate(review_prompt)
                rankings[reviewer] = self._parse_ranking(review)

            except Exception as e:
                rankings[reviewer] = {"error": str(e)}
                logger.error(f"Review error for {reviewer}: {e}")

        return rankings

    async def _stage3_synthesis(
        self,
        opinions: Dict[str, str],
        rankings: Optional[Dict] = None,
        original_query: str = ""
    ) -> str:
        """
        Stage 3: Chairman synthétise toutes les opinions

        Returns:
            Réponse finale synthétisée
        """
        # Construire prompt de synthèse
        synthesis_prompt = f"""Tu es le Chairman d'un conseil d'experts IA.

Question originale: {original_query}

Voici les réponses des différents experts:

"""

        # Ajouter chaque opinion
        for model, opinion in opinions.items():
            model_name = council_config.PROVIDERS.get(model, {}).get("name", model)
            synthesis_prompt += f"\n=== Expert {model_name} ===\n{opinion}\n"

        # Ajouter les rankings si disponibles
        if rankings:
            synthesis_prompt += f"\n\n=== Évaluations croisées ===\n"
            for reviewer, ranking in rankings.items():
                synthesis_prompt += f"\n{reviewer}: {json.dumps(ranking, indent=2)}\n"

        synthesis_prompt += """

Ta mission: Synthétiser ces réponses en UNE réponse finale optimale qui:

1. Intègre les meilleures idées et arguments de chaque expert
2. Résout les contradictions éventuelles en expliquant les différences de perspective
3. Fournit une réponse claire, structurée et actionnelle
4. Mentionne les points de consensus et les divergences importantes si nécessaire
5. Conclut avec une recommandation claire

Fournis UNIQUEMENT la synthèse finale, sans préambule du type "Voici ma synthèse..."."""

        try:
            chairman_provider = get_provider(self.chairman)
            final = await chairman_provider.generate(synthesis_prompt)
            return final
        except Exception as e:
            logger.error(f"Synthesis error: {e}")
            # Fallback: retourner la meilleure opinion disponible
            if opinions:
                return f"Synthèse automatique:\n\n{list(opinions.values())[0]}"
            raise

    def _anonymize_opinions(self, opinions: Dict[str, str]) -> Dict[str, str]:
        """Anonymise les noms des modèles pour éviter les biais"""
        anonymized = {}
        for i, (model, opinion) in enumerate(opinions.items(), 1):
            anonymized[f"Response_{i}"] = opinion
        return anonymized

    def _create_review_prompt(
        self,
        anonymized: Dict[str, str],
        query: str,
        reviewer: str
    ) -> str:
        """Crée le prompt de review pour un membre"""

        prompt = f"""Tu dois évaluer plusieurs réponses à cette question:

Question: {query}

Voici les réponses à évaluer:

"""
        for key, opinion in anonymized.items():
            prompt += f"\n{key}:\n{opinion}\n\n---\n"

        prompt += """
Évalue chaque réponse selon ces critères (note de 1 à 10):
- Précision factuelle: exactitude des informations
- Pertinence: adéquation à la question posée
- Clarté: facilité de compréhension
- Complétude: couverture du sujet

Réponds au format JSON strict:
{
  "Response_1": {"precision": X, "pertinence": Y, "clarte": Z, "completude": W},
  "Response_2": {...},
  ...
}

Fournis uniquement le JSON, sans texte additionnel.
"""
        return prompt

    def _parse_ranking(self, review: str) -> Dict:
        """Parse le ranking JSON de la review"""
        try:
            # Extraire JSON du texte
            start = review.find('{')
            end = review.rfind('}') + 1

            if start == -1 or end == 0:
                return {"raw": review, "parsed": False}

            json_str = review[start:end]
            parsed = json.loads(json_str)
            return {"rankings": parsed, "parsed": True}

        except json.JSONDecodeError:
            logger.warning("Failed to parse ranking JSON")
            return {"raw": review, "parsed": False}
        except Exception as e:
            logger.error(f"Ranking parse error: {e}")
            return {"error": str(e), "raw": review}
