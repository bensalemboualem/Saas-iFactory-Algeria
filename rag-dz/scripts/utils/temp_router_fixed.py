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
