
# ============= NOUVEAU ENDPOINT: MULTI-LLM ROUTER =============

class LLMRequest(BaseModel):
    """Request model pour génération via LLM Router"""
    messages: List[Dict[str, str]]
    use_case: str  # "analysis", "code_generation", "summarization", etc.
    complexity: Optional[str] = None  # "simple", "moderate", "complex", "expert"
    budget_tier: str = "standard"  # "economy", "standard", "premium"
    temperature: float = 0.7
    max_tokens: int = 2000


@router.post("/llm/generate")
async def generate_with_router(request: LLMRequest):
    """
    Génère une réponse en utilisant le Multi-LLM Router intelligent

    Le router sélectionne automatiquement le meilleur LLM (Claude, OpenAI, Mistral)
    selon le cas d'usage, la complexité et le budget.

    Args:
        messages: Liste de messages [{"role": "user", "content": "..."}]
        use_case: Type de tâche (analysis, code_generation, summarization, etc.)
        complexity: Niveau de complexité (simple, moderate, complex, expert)
        budget_tier: Tier de budget (economy, standard, premium)
        temperature: Temperature pour génération (0.0-1.0)
        max_tokens: Nombre maximum de tokens

    Returns:
        {
            "success": true,
            "content": "La réponse générée...",
            "provider": "claude",
            "model": "claude-sonnet-4-5-20250929",
            "tokens_used": 1234,
            "cost": 0.00370,
            "latency_ms": 1250
        }
    """
    try:
        from app.llm_router import LLMRouter, UseCaseType, TaskComplexity

        # Initialiser le router
        router_instance = LLMRouter()

        # Convertir use_case string en enum
        try:
            use_case_enum = UseCaseType[request.use_case.upper()]
        except KeyError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid use_case. Valid options: {[e.value for e in UseCaseType]}"
            )

        # Convertir complexity string en enum si fourni
        complexity_enum = None
        if request.complexity:
            try:
                complexity_enum = TaskComplexity[request.complexity.upper()]
            except KeyError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid complexity. Valid options: {[e.value for e in TaskComplexity]}"
                )

        # Générer avec le router
        result = await router_instance.generate(
            messages=request.messages,
            use_case=use_case_enum,
            complexity=complexity_enum,
            budget_tier=request.budget_tier,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )

        return result

    except ImportError as e:
        logger.error(f"LLM Router import error: {e}")
        raise HTTPException(
            status_code=500,
            detail="LLM Router not properly installed. Please check dependencies."
        )
    except Exception as e:
        logger.error(f"Error generating with LLM router: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/llm/providers")
async def list_providers():
    """
    Liste tous les providers LLM disponibles et leurs modèles
    """
    try:
        from app.llm_router.config import MODELS_CONFIG, Provider

        providers = {}
        for provider in Provider:
            if provider.value in MODELS_CONFIG:
                models = MODELS_CONFIG[provider.value]
                providers[provider.value] = {
                    "available": True,
                    "models": {
                        key: {
                            "name": config["name"],
                            "cost_per_1m_tokens": config["cost_per_1m_tokens"],
                            "context_window": config["context_window"]
                        }
                        for key, config in models.items()
                    }
                }

        return {
            "success": True,
            "providers": providers
        }

    except Exception as e:
        logger.error(f"Error listing providers: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/llm/use-cases")
async def list_use_cases():
    """
    Liste tous les cas d'usage disponibles avec leurs règles de routing
    """
    try:
        from app.llm_router.config import ROUTING_RULES, UseCaseType

        use_cases = {}
        for use_case in UseCaseType:
            if use_case in ROUTING_RULES:
                rule = ROUTING_RULES[use_case]
                primary_provider, primary_model = rule["primary"]
                fallback_provider, fallback_model = rule["fallback"]

                use_cases[use_case.value] = {
                    "complexity": rule["complexity"].value,
                    "primary": {
                        "provider": primary_provider.value,
                        "model": primary_model
                    },
                    "fallback": {
                        "provider": fallback_provider.value,
                        "model": fallback_model
                    }
                }

        return {
            "success": True,
            "use_cases": use_cases
        }

    except Exception as e:
        logger.error(f"Error listing use cases: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============= FIN MULTI-LLM ROUTER ENDPOINTS =============
