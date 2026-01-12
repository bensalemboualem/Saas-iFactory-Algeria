"""
Multi-LLM Router
================
Endpoints FastAPI pour accès multi-providers IA avec gestion crédits
"""

import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Header

from .multi_llm_models import (
    ChatRequest, ChatResponse, ModelsListResponse,
    UsageHistoryResponse, UsageSummaryResponse,
    LLMModelTier, LLMProviderType, LLMModelType,
)
from .multi_llm_service import multi_llm_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/llm", tags=["Multi-LLM"])


# ============================================
# Models Endpoints
# ============================================

@router.get("/health")
async def llm_health():
    """Health check du module Multi-LLM"""
    models = multi_llm_service.list_models()
    return {
        "status": "healthy",
        "module": "multi_llm",
        "version": "1.0.0",
        "models_available": models.total,
        "default_model": models.default_model,
    }


@router.get("/models", response_model=ModelsListResponse)
async def list_models(
    tier: Optional[LLMModelTier] = Query(None, description="Filtrer par tier (free, basic, standard, premium, ultra)"),
    provider: Optional[LLMProviderType] = Query(None, description="Filtrer par provider (openai, anthropic, groq, google, mistral)"),
    model_type: Optional[LLMModelType] = Query(None, alias="type", description="Filtrer par type (chat, image_gen, video_gen, tts, stt, music_gen, presentation, code_gen)"),
):
    """
    Lister tous les modèles IA disponibles
    
    Retourne la liste des modèles avec leurs prix en crédits IAFactory.
    
    **Types disponibles:**
    - `chat`: Modèles de conversation (GPT-4o, Claude, etc.)
    - `image_gen`: Génération d'images (DALL-E, Stable Diffusion, Flux)
    - `video_gen`: Génération de vidéos (Runway, Pika, Kling)
    - `tts`: Text-to-Speech (ElevenLabs, OpenAI TTS)
    - `stt`: Speech-to-Text (Whisper)
    - `music_gen`: Génération musicale (Suno, Udio)
    - `presentation`: Présentations IA (Gamma, Beautiful.ai)
    - `code_gen`: Assistants code (Copilot, Cursor)
    
    **Tiers disponibles:**
    - `free`: Modèles gratuits (Groq Llama, etc.)
    - `basic`: Économiques (GPT-4o-mini, Claude Haiku)
    - `standard`: Équilibrés (GPT-4o, Claude Sonnet)
    - `premium`: Puissants (Claude Opus, Runway Gen-3)
    - `ultra`: Spécialisés (O1, modèles avancés)
    """
    try:
        return multi_llm_service.list_models(tier=tier, provider=provider, model_type=model_type)
    except Exception as e:
        logger.error(f"Error listing models: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models/{model_code}")
async def get_model(model_code: str):
    """
    Obtenir les détails d'un modèle spécifique
    
    Args:
        model_code: Code du modèle (ex: "openai.gpt-4o", "groq.llama-3.1-70b")
    
    Returns:
        Détails du modèle avec pricing
    """
    model = multi_llm_service.get_model(model_code)
    if not model:
        raise HTTPException(status_code=404, detail=f"Model not found: {model_code}")
    
    return {
        "success": True,
        "model": {
            "code": model.code,
            "display_name": model.display_name,
            "tier": model.tier.value,
            "type": model.type.value,
            "cost_credits_per_1k": model.cost_credits_per_1k,
            "cost_usd_input_per_1k": float(model.cost_usd_input_per_1k),
            "cost_usd_output_per_1k": float(model.cost_usd_output_per_1k),
            "max_tokens": model.max_tokens,
            "context_window": model.context_window,
            "supports_vision": model.supports_vision,
            "supports_tools": model.supports_tools,
            "description": model.description,
            "is_active": model.is_active,
            "is_default": model.is_default,
        }
    }


@router.get("/pricing")
async def get_pricing():
    """
    Obtenir la grille tarifaire complète
    
    Retourne les prix en crédits IAFactory et équivalent DZD.
    """
    return multi_llm_service.get_pricing_table()


# ============================================
# Chat Endpoint
# ============================================

@router.post("/chat", response_model=ChatResponse)
async def chat_completion(
    request: ChatRequest,
    x_user_id: str = Header(default="anonymous", alias="X-User-Id"),
):
    """
    Envoyer une requête chat à un modèle IA
    
    **Corps de la requête:**
    ```json
    {
        "model": "openai.gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Tu es un assistant expert..."},
            {"role": "user", "content": "Explique moi la CNAS en Algérie"}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    ```
    
    **Modèles recommandés:**
    - `groq.llama-3.1-70b`: Gratuit, rapide, bon pour tests
    - `openai.gpt-4o-mini`: Économique, polyvalent
    - `anthropic.claude-3-5-sonnet`: Excellent pour le français
    - `google.gemini-1.5-flash`: Ultra économique
    
    **Crédits:**
    - Les crédits sont déduits automatiquement via Billing V2
    - Le coût dépend du modèle et du nombre de tokens
    - Erreur 402 si crédits insuffisants
    
    Returns:
        Réponse du modèle avec tokens utilisés et crédits consommés
    """
    try:
        response = await multi_llm_service.chat(
            user_id=x_user_id,
            request=request,
            check_credits=True,
        )
        return response
        
    except ValueError as e:
        error_msg = str(e)
        
        # Crédits insuffisants
        if "insuffisants" in error_msg.lower() or "insufficient" in error_msg.lower():
            raise HTTPException(
                status_code=402,
                detail={
                    "error": "insufficient_credits",
                    "message": error_msg,
                    "upgrade_url": "/api/v2/billing/plans",
                }
            )
        
        # Modèle inconnu
        if "unknown model" in error_msg.lower():
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "model_not_found",
                    "message": error_msg,
                    "available_models": "/api/llm/models",
                }
            )
        
        # Erreur API provider
        if "api error" in error_msg.lower() or "call failed" in error_msg.lower():
            raise HTTPException(
                status_code=503,
                detail={
                    "error": "provider_error",
                    "message": error_msg,
                }
            )
        
        raise HTTPException(status_code=400, detail=error_msg)
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/free")
async def chat_completion_free(
    request: ChatRequest,
    x_user_id: str = Header(default="anonymous", alias="X-User-Id"),
):
    """
    Chat SANS vérification de crédits (pour tests/démo)
    
    ⚠️ À utiliser uniquement pour les démos et tests.
    En production, utiliser `/api/llm/chat`.
    """
    try:
        # Forcer un modèle gratuit
        if not request.model.startswith("groq."):
            request.model = "groq.llama-3.1-8b"
        
        response = await multi_llm_service.chat(
            user_id=x_user_id,
            request=request,
            check_credits=False,  # Pas de vérification
        )
        return response
        
    except Exception as e:
        logger.error(f"Chat free error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# Usage Endpoints
# ============================================

@router.get("/usage", response_model=UsageSummaryResponse)
async def get_usage_summary(
    period: str = Query(default="7d", regex="^(7d|30d|all)$"),
    x_user_id: str = Header(default="anonymous", alias="X-User-Id"),
):
    """
    Obtenir le résumé d'usage LLM
    
    Args:
        period: Période ("7d", "30d", "all")
    
    Returns:
        Résumé avec totaux et répartition par modèle/jour
    """
    try:
        return multi_llm_service.get_usage_summary(
            user_id=x_user_id,
            period=period,
        )
    except Exception as e:
        logger.error(f"Usage summary error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/usage/history", response_model=UsageHistoryResponse)
async def get_usage_history(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    x_user_id: str = Header(default="anonymous", alias="X-User-Id"),
):
    """
    Obtenir l'historique détaillé d'usage LLM
    
    Args:
        limit: Nombre max de résultats (1-100)
        offset: Pagination
    
    Returns:
        Liste des appels LLM avec détails
    """
    try:
        return multi_llm_service.get_usage_history(
            user_id=x_user_id,
            limit=limit,
            offset=offset,
        )
    except Exception as e:
        logger.error(f"Usage history error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# Quick Chat Helpers
# ============================================

@router.post("/quick")
async def quick_chat(
    prompt: str = Query(..., description="Question à poser"),
    model: str = Query(default="groq.llama-3.1-70b", description="Modèle à utiliser"),
    x_user_id: str = Header(default="anonymous", alias="X-User-Id"),
):
    """
    Chat rapide en un seul appel (GET-style)
    
    Idéal pour tests rapides et intégrations simples.
    
    Example:
        /api/llm/quick?prompt=Explique la CNAS&model=groq.llama-3.1-70b
    """
    from .multi_llm_models import ChatMessage
    
    request = ChatRequest(
        model=model,
        messages=[ChatMessage(role="user", content=prompt)],
    )
    
    try:
        response = await multi_llm_service.chat(
            user_id=x_user_id,
            request=request,
            check_credits=True,
        )
        return {
            "success": True,
            "answer": response.answer,
            "model": response.model,
            "tokens": response.tokens_total,
            "credits_used": response.credits_used,
        }
    except ValueError as e:
        if "insuffisants" in str(e).lower():
            raise HTTPException(status_code=402, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))
