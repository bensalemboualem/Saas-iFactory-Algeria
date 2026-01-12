import os
from typing import List, Dict, Any, Optional, Tuple
from .config import Provider, TaskComplexity, UseCaseType, MODELS_CONFIG, ROUTING_RULES, COST_TIERS
from .providers import BaseProvider, ClaudeProvider, OpenAIProvider, MistralProvider
from .providers.base import Message, LLMResponse

class LLMRouter:
    """
    Intelligent router qui sélectionne le meilleur LLM pour chaque tâche
    """

    def __init__(self):
        # Charger les API keys depuis l'environnement
        self.api_keys = {
            Provider.CLAUDE: os.getenv("ANTHROPIC_API_KEY"),
            Provider.OPENAI: os.getenv("OPENAI_API_KEY"),
            Provider.MISTRAL: os.getenv("MISTRAL_API_KEY"),
        }

        # Provider cache pour réutiliser les instances
        self.provider_cache: Dict[Tuple[Provider, str], BaseProvider] = {}

        # Cost tracking
        self.total_cost = 0.0

    def select_model(
        self,
        use_case: UseCaseType,
        complexity: Optional[TaskComplexity] = None,
        budget_tier: str = "standard"
    ) -> Tuple[Provider, str]:
        """
        Sélectionne le meilleur modèle basé sur le cas d'usage et la complexité

        Args:
            use_case: Type de tâche (ANALYSIS, CODE_GEN, etc.)
            complexity: Complexité de la tâche (SIMPLE, MODERATE, COMPLEX, EXPERT)
            budget_tier: Tier de budget client (economy, standard, premium)

        Returns:
            Tuple (Provider, model_name)
        """
        # Récupérer la règle de routing
        rule = ROUTING_RULES.get(use_case)
        if not rule:
            # Default: Claude Sonnet
            return (Provider.CLAUDE, "sonnet")

        # Si pas de complexité fournie, utiliser celle de la règle
        if complexity is None:
            complexity = rule["complexity"]

        # Récupérer le tier de budget
        tier_config = COST_TIERS.get(budget_tier, COST_TIERS["standard"])

        # Sélectionner primary ou fallback selon budget
        primary_provider, primary_model_key = rule["primary"]

        # Vérifier si le modèle primary est dans le budget
        model_config = MODELS_CONFIG[primary_provider][primary_model_key]
        max_cost = tier_config["max_cost_per_request"]

        # Estimation tokens pour calcul coût (assume 1000 tokens average)
        estimated_cost = (1000 / 1_000_000) * model_config["cost_per_1m_tokens"]

        if estimated_cost > max_cost:
            # Utiliser fallback si primary trop cher
            fallback_provider, fallback_model_key = rule["fallback"]
            return (fallback_provider, fallback_model_key)

        return (primary_provider, primary_model_key)

    def get_provider(self, provider: Provider, model_key: str) -> BaseProvider:
        """
        Récupère ou crée une instance du provider
        """
        cache_key = (provider, model_key)

        if cache_key in self.provider_cache:
            return self.provider_cache[cache_key]

        # Récupérer l'API key
        api_key = self.api_keys.get(provider)
        if not api_key:
            raise ValueError(f"API key non trouvée pour {provider}")

        # Récupérer le nom complet du modèle
        model_config = MODELS_CONFIG[provider][model_key]
        model_name = model_config["name"]

        # Créer l'instance du provider
        if provider == Provider.CLAUDE:
            instance = ClaudeProvider(api_key, model_name)
        elif provider == Provider.OPENAI:
            instance = OpenAIProvider(api_key, model_name)
        elif provider == Provider.MISTRAL:
            instance = MistralProvider(api_key, model_name)
        else:
            raise ValueError(f"Provider non supporté: {provider}")

        # Cacher l'instance
        self.provider_cache[cache_key] = instance

        return instance

    async def generate(
        self,
        messages: List[Dict[str, str]],
        use_case: UseCaseType,
        complexity: Optional[TaskComplexity] = None,
        budget_tier: str = "standard",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Génère une réponse en routant vers le meilleur LLM

        Args:
            messages: Liste de messages [{"role": "user", "content": "..."}]
            use_case: Type de tâche
            complexity: Complexité de la tâche
            budget_tier: Tier de budget
            temperature: Temperature pour génération
            max_tokens: Nombre max de tokens

        Returns:
            Dict avec response, metadata, cost, etc.
        """
        # Sélectionner le meilleur modèle
        provider, model_key = self.select_model(use_case, complexity, budget_tier)

        # Convertir messages en format Message
        formatted_messages = [Message(role=m["role"], content=m["content"]) for m in messages]

        try:
            # Obtenir le provider
            llm_provider = self.get_provider(provider, model_key)

            # Générer la réponse
            response = await llm_provider.generate(
                messages=formatted_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )

            # Tracker le coût
            self.total_cost += response.cost

            return {
                "success": True,
                "content": response.content,
                "provider": response.provider,
                "model": response.model,
                "tokens_used": response.tokens_used,
                "cost": response.cost,
                "latency_ms": response.latency_ms,
                "total_session_cost": self.total_cost
            }

        except Exception as e:
            # En cas d'erreur, essayer le fallback
            rule = ROUTING_RULES.get(use_case)
            if rule and "fallback" in rule:
                fallback_provider, fallback_model_key = rule["fallback"]

                try:
                    llm_provider = self.get_provider(fallback_provider, fallback_model_key)
                    response = await llm_provider.generate(
                        messages=formatted_messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        **kwargs
                    )

                    self.total_cost += response.cost

                    return {
                        "success": True,
                        "content": response.content,
                        "provider": response.provider,
                        "model": response.model,
                        "tokens_used": response.tokens_used,
                        "cost": response.cost,
                        "latency_ms": response.latency_ms,
                        "total_session_cost": self.total_cost,
                        "fallback_used": True,
                        "primary_error": str(e)
                    }
                except Exception as fallback_error:
                    return {
                        "success": False,
                        "error": str(fallback_error),
                        "primary_error": str(e)
                    }

            return {
                "success": False,
                "error": str(e)
            }

    def get_cost_summary(self) -> Dict[str, Any]:
        """Retourne un résumé des coûts de la session"""
        return {
            "total_cost": self.total_cost,
            "providers_used": list(self.provider_cache.keys())
        }
