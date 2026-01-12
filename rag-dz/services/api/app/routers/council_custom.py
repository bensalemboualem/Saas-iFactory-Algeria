"""
Council Custom API - Endpoints pour la personnalisation complète du Council
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import logging

from ..modules.council.flexible_orchestrator import FlexibleCouncilOrchestrator
from ..modules.council.models_config import AvailableModels, RECOMMENDED_COUNCILS
from ..modules.council.universal_provider import UniversalProvider

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/council", tags=["Council Custom"])


# ==================== Models ====================

class CustomCouncilRequest(BaseModel):
    """Requête Council personnalisée"""
    query: str = Field(..., description="Question à poser au Council")
    expert1: str = Field(..., description="Premier expert (model ID)")
    expert2: str = Field(..., description="Deuxième expert (model ID)")
    expert3: str = Field(..., description="Troisième expert (model ID)")
    chairman: str = Field(..., description="Chairman pour la synthèse (model ID)")
    enable_review: bool = Field(False, description="Activer la revue croisée")
    context: Optional[str] = Field(None, description="Contexte additionnel")


class CouncilResponse(BaseModel):
    """Réponse du Council"""
    final_response: str
    opinions: Dict[str, str]
    rankings: Optional[Dict]
    metadata: Dict[str, Any]


class ModelInfo(BaseModel):
    """Information sur un modèle"""
    id: str
    name: str
    provider: str
    tier: str
    cost_per_1k_tokens: float
    speed: str
    strengths: List[str]
    languages: List[str]
    icon: str
    available: bool


class EstimateRequest(BaseModel):
    """Requête d'estimation"""
    expert1: str
    expert2: str
    expert3: str
    chairman: str
    enable_review: bool = False


class EstimateResponse(BaseModel):
    """Réponse d'estimation"""
    estimated_cost_usd: float
    estimated_cost_dzd: float
    estimated_time_seconds: Dict[str, int]
    breakdown: Dict[str, Dict[str, Any]]


# ==================== Endpoints ====================

@router.get("/models/all")
async def get_all_models():
    """
    Liste TOUS les modèles disponibles avec leurs infos complètes
    """
    try:
        available_models = AvailableModels.get_available_models()

        models_list = []
        for model_id, model_info in AvailableModels.MODELS.items():
            models_list.append({
                "id": model_id,
                "name": model_info["name"],
                "provider": model_info["provider"],
                "tier": model_info["tier"],
                "cost_per_1k_tokens": model_info["cost_per_1k_tokens"],
                "speed": model_info["speed"],
                "strengths": model_info["strengths"],
                "languages": model_info["languages"],
                "icon": model_info["icon"],
                "available": model_id in available_models
            })

        return {
            "models": models_list,
            "by_tier": {
                "premium": [m for m in models_list if m["tier"] == "premium"],
                "standard": [m for m in models_list if m["tier"] == "standard"],
                "local": [m for m in models_list if m["tier"] == "local"],
                "specialized": [m for m in models_list if m["tier"] == "specialized"]
            },
            "by_provider": {
                "openai": [m for m in models_list if m["provider"] == "openai"],
                "anthropic": [m for m in models_list if m["provider"] == "anthropic"],
                "google": [m for m in models_list if m["provider"] == "google"],
                "mistral": [m for m in models_list if m["provider"] == "mistral"],
                "ollama": [m for m in models_list if m["provider"] == "ollama"]
            }
        }

    except Exception as e:
        logger.error(f"Error fetching models: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/presets")
async def get_recommended_presets():
    """
    Retourne les configurations recommandées
    """
    try:
        return {"presets": RECOMMENDED_COUNCILS}
    except Exception as e:
        logger.error(f"Error fetching presets: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/estimate", response_model=EstimateResponse)
async def estimate_cost_and_time(request: EstimateRequest):
    """
    Estime coût et temps AVANT l'exécution
    """
    try:
        all_models = [request.expert1, request.expert2, request.expert3, request.chairman]

        # Validation
        for model in all_models:
            if model not in AvailableModels.MODELS:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Modèle inconnu: {model}"
                )

        cost = AvailableModels.estimate_cost(all_models)
        time_range = AvailableModels.estimate_time(all_models)

        # Ajuster pour review
        if request.enable_review:
            cost *= 1.5
            time_range = (time_range[0], int(time_range[1] * 1.3))

        return EstimateResponse(
            estimated_cost_usd=round(cost, 4),
            estimated_cost_dzd=round(cost * 135, 2),  # 1 USD ≈ 135 DZD
            estimated_time_seconds={
                "min": int(time_range[0]),
                "max": int(time_range[1])
            },
            breakdown={
                model: {
                    "name": AvailableModels.MODELS[model]["name"],
                    "cost": AvailableModels.MODELS[model]["cost_per_1k_tokens"],
                    "tier": AvailableModels.MODELS[model]["tier"],
                    "icon": AvailableModels.MODELS[model]["icon"]
                }
                for model in all_models
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error estimating: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/custom-query", response_model=CouncilResponse)
async def execute_custom_council(request: CustomCouncilRequest):
    """
    Exécute le Council avec la config choisie par l'utilisateur
    """
    try:
        logger.info(f"Custom Council: experts=[{request.expert1}, {request.expert2}, {request.expert3}], chairman={request.chairman}")

        orchestrator = FlexibleCouncilOrchestrator(
            expert1=request.expert1,
            expert2=request.expert2,
            expert3=request.expert3,
            chairman=request.chairman,
            enable_review=request.enable_review
        )

        result = await orchestrator.process_query(
            user_query=request.query,
            context=request.context
        )

        return CouncilResponse(**result)

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Council execution error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur Council: {str(e)}"
        )


@router.post("/test-combination")
async def test_model_combination(
    expert1: str,
    expert2: str,
    expert3: str,
    chairman: str
):
    """
    Test rapide d'une combinaison (sans vraie requête)
    """
    try:
        all_models = [expert1, expert2, expert3, chairman]

        results = {}
        test_prompt = "Réponds 'OK' si tu me reçois."

        for model in all_models:
            try:
                provider = UniversalProvider.get_provider(model)
                response = await provider.generate(test_prompt)

                results[model] = {
                    "status": "✅ Opérationnel",
                    "response_preview": response[:50],
                    "name": AvailableModels.MODELS[model]["name"]
                }
            except Exception as e:
                results[model] = {
                    "status": "❌ Erreur",
                    "error": str(e),
                    "name": AvailableModels.MODELS[model].get("name", model)
                }

        return {
            "combination_valid": all(
                r["status"].startswith("✅") for r in results.values()
            ),
            "tests": results
        }

    except Exception as e:
        logger.error(f"Test combination error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
