import os
from typing import List, Dict, Any, Optional, Tuple
from .config import Provider, TaskComplexity, UseCaseType, MODELS_CONFIG, ROUTING_RULES, COST_TIERS
from .providers import BaseProvider, ClaudeProvider, OpenAIProvider, MistralProvider, GeminiProvider
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
        elif provider == Provider.GEMINI:
            instance = GeminiProvider(api_key, model_name)
        else:
            raise ValueError(f"Provider non supporté: {provider}")

        # Cacher l'instance
        self.provider_cache[cache_key] = instance

        return instance
