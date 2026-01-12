"""
API Router pour LLM Council
Endpoints pour interroger le conseil d'IA et gérer les providers
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import logging

from ..modules.council.orchestrator import CouncilOrchestrator
from ..modules.council.providers import test_provider, get_provider
from ..modules.council.config import council_config

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/council", tags=["Council"])


# ==================== Models ====================

class CouncilRequest(BaseModel):
    """Requête vers le Council"""
    query: str = Field(..., description="Question à poser au conseil d'IA")
    context: Optional[str] = Field(None, description="Contexte additionnel")
    council_members: Optional[List[str]] = Field(
        None,
        description="Liste des membres (claude, gemini, ollama). Par défaut: tous disponibles"
    )
    enable_review: Optional[bool] = Field(
        False,
        description="Activer la revue croisée (plus lent mais plus précis)"
    )
    chairman: Optional[str] = Field(
        None,
        description="Modèle chairman pour la synthèse. Par défaut: claude"
    )


class CouncilResponse(BaseModel):
    """Réponse du Council"""
    final_response: str = Field(..., description="Réponse finale synthétisée")
    opinions: Dict[str, str] = Field(..., description="Opinions individuelles de chaque membre")
    rankings: Optional[Dict[str, Dict]] = Field(None, description="Évaluations croisées (si activé)")
    metadata: Dict[str, Any] = Field(..., description="Métadonnées de traitement")


class ProviderStatus(BaseModel):
    """Status d'un provider"""
    name: str
    display_name: str
    available: bool
    model: str
    role: str
    cost_per_1k: float


# ==================== Endpoints ====================

@router.post("/query", response_model=CouncilResponse)
async def council_query(request: CouncilRequest):
    """
    Interroge le conseil d'IA

    Le Council consulte plusieurs modèles d'IA en parallèle,
    optionnellement fait une revue croisée, puis synthétise
    une réponse finale optimale.

    **Étapes:**
    1. Stage 1: Chaque IA donne son opinion
    2. Stage 2 (optionnel): Revue croisée des opinions
    3. Stage 3: Synthèse finale par le chairman
    """
    try:
        logger.info(f"Council query received: {request.query[:100]}...")

        # Créer orchestrateur
        orchestrator = CouncilOrchestrator(
            council_members=request.council_members,
            enable_review=request.enable_review,
            chairman=request.chairman
        )

        # Traiter la requête
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
        logger.error(f"Council query error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du traitement par le Council: {str(e)}"
        )


@router.get("/providers", response_model=List[ProviderStatus])
async def list_providers():
    """
    Liste tous les providers disponibles avec leur statut

    Retourne la liste des modèles d'IA configurés et
    indique lesquels sont actuellement disponibles.
    """
    try:
        providers_status = []

        for provider_name, provider_info in council_config.PROVIDERS.items():
            try:
                provider = get_provider(provider_name)
                available = provider.is_available()

                providers_status.append(
                    ProviderStatus(
                        name=provider_name,
                        display_name=provider_info["name"],
                        available=available,
                        model=provider_info["model"],
                        role=provider_info["role"],
                        cost_per_1k=provider_info["cost_per_1k"]
                    )
                )
            except Exception as e:
                logger.error(f"Error checking provider {provider_name}: {e}")
                providers_status.append(
                    ProviderStatus(
                        name=provider_name,
                        display_name=provider_info["name"],
                        available=False,
                        model=provider_info["model"],
                        role=provider_info["role"],
                        cost_per_1k=provider_info["cost_per_1k"]
                    )
                )

        return providers_status

    except Exception as e:
        logger.error(f"Error listing providers: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/test")
async def test_providers():
    """
    Test de connectivité de tous les providers

    Envoie un message de test à chaque provider pour
    vérifier la connectivité et la configuration.
    """
    try:
        results = {}

        for provider_name in council_config.PROVIDERS.keys():
            result = await test_provider(provider_name)
            results[provider_name] = result

        return {
            "status": "completed",
            "results": results,
            "available_providers": council_config.get_available_providers()
        }

    except Exception as e:
        logger.error(f"Provider test error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/config")
async def get_council_config():
    """
    Récupère la configuration actuelle du Council

    Retourne les paramètres de configuration sans
    exposer les clés API.
    """
    return {
        "default_council": council_config.DEFAULT_COUNCIL,
        "chairman": council_config.CHAIRMAN,
        "enable_review": council_config.ENABLE_REVIEW,
        "anonymize_models": council_config.ANONYMIZE_MODELS,
        "timeouts": {
            "stage1": council_config.STAGE1_TIMEOUT,
            "stage2": council_config.STAGE2_TIMEOUT,
            "stage3": council_config.STAGE3_TIMEOUT,
            "total": council_config.TOTAL_TIMEOUT
        },
        "available_providers": council_config.get_available_providers(),
        "providers_info": {
            name: {
                "name": info["name"],
                "model": info["model"],
                "role": info["role"],
                "cost_per_1k": info["cost_per_1k"]
            }
            for name, info in council_config.PROVIDERS.items()
        }
    }


@router.get("/health")
async def council_health():
    """
    Vérifie la santé du service Council

    Retourne le nombre de providers disponibles
    et l'état général du service.
    """
    available = council_config.get_available_providers()

    return {
        "status": "healthy" if len(available) > 0 else "degraded",
        "available_providers": len(available),
        "providers": available,
        "chairman_available": council_config.CHAIRMAN in available
    }
