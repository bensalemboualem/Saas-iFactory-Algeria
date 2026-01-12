"""
BMAD OpenAI-Compatible Router - Endpoint compatible avec Vercel AI SDK pour Bolt.diy
Expose les agents BMAD via une API OpenAI-compatible avec streaming SSE
Token tracking integre.
"""

import os
import json
import logging
import time
import uuid
from typing import List, Optional, AsyncGenerator
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI

from .bmad_chat import (
    load_agent_personality,
    get_iafactory_context,
    get_llm_client,
    RAG_ENABLED,
    _get_provider_from_env,
    _get_optional_tenant_id,
    TOKENS_ENABLED
)

# Token tracking
try:
    from app.tokens.llm_proxy import check_token_balance, deduct_after_llm_call, InsufficientTokensError
    _TOKENS_AVAILABLE = True
except ImportError:
    _TOKENS_AVAILABLE = False

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/bmad/v1", tags=["bmad-openai"])


# Mapping des modèles BMAD vers les agent_id
BMAD_MODELS = {
    "bmm-architect": {"name": "Winston", "title": "Architect", "icon": "🏗️"},
    "bmm-pm": {"name": "John", "title": "Product Manager", "icon": "📋"},
    "bmm-developer": {"name": "Amelia", "title": "Developer", "icon": "💻"},
    "bmm-analyst": {"name": "Mary", "title": "Business Analyst", "icon": "📊"},
    "bmm-tester": {"name": "Murat", "title": "Test Architect", "icon": "🧪"},
    "bmm-sm": {"name": "Scrum Master", "title": "Scrum Master", "icon": "🏃"},
    "bmm-tech-writer": {"name": "Paige", "title": "Technical Writer", "icon": "📝"},
    "bmm-ux-designer": {"name": "UX Designer", "title": "UX Designer", "icon": "🎨"},
    "cis-ideator": {"name": "Ideator", "title": "Creative Ideator", "icon": "💡"},
    "cis-strategist": {"name": "Strategist", "title": "Strategy Expert", "icon": "🎯"},
    "bmb-agent-builder": {"name": "Agent Builder", "title": "Agent Builder", "icon": "🤖"},
    "bmb-workflow-builder": {"name": "Workflow Builder", "title": "Workflow Builder", "icon": "🔧"},
}


class OpenAIMessage(BaseModel):
    role: str
    content: str


class OpenAIChatRequest(BaseModel):
    model: str
    messages: List[OpenAIMessage]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 4096
    stream: Optional[bool] = False
    # Extension BMAD
    region: Optional[str] = "DZ"


class OpenAIChoice(BaseModel):
    index: int
    message: OpenAIMessage
    finish_reason: str


class OpenAIUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class OpenAIChatResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[OpenAIChoice]
    usage: OpenAIUsage


@router.get("/models")
async def list_models():
    """Liste les modèles BMAD disponibles au format OpenAI"""
    models = []
    for model_id, info in BMAD_MODELS.items():
        models.append({
            "id": model_id,
            "object": "model",
            "created": 1700000000,
            "owned_by": "bmad",
            "permission": [],
            "root": model_id,
            "parent": None,
            "name": f"{info['icon']} {info['name']} ({info['title']})",
        })
    return {"object": "list", "data": models}


async def stream_bmad_response(
    agent_id: str,
    messages: List[OpenAIMessage],
    temperature: float,
    max_tokens: int,
    region: str,
    tenant_id: Optional[str] = None
) -> AsyncGenerator[str, None]:
    """Génère une réponse streaming au format SSE OpenAI avec token tracking."""

    request_id = f"chatcmpl-{uuid.uuid4().hex[:24]}"
    created = int(time.time())
    provider = _get_provider_from_env()

    try:
        # Charger la personnalité de l'agent
        system_prompt = load_agent_personality(agent_id)

        # Récupérer le contexte RAG si activé
        user_messages = [msg for msg in messages if msg.role == "user"]
        last_user_message = user_messages[-1].content if user_messages else ""

        if last_user_message and RAG_ENABLED:
            rag_context = await get_iafactory_context(last_user_message, region)
            if rag_context:
                system_prompt += rag_context

        # Token tracking: verifier solde AVANT l'appel
        if _TOKENS_AVAILABLE and TOKENS_ENABLED and tenant_id:
            total_content = system_prompt + " ".join(msg.content for msg in messages)
            estimated_tokens = len(total_content.split()) * 2 + 500
            try:
                check_token_balance(tenant_id, estimated_tokens)
            except InsufficientTokensError as e:
                error_chunk = {
                    "id": request_id, "object": "chat.completion.chunk", "created": created,
                    "model": agent_id, "choices": [{"index": 0, "delta": {"content": f"Erreur: {e}"}, "finish_reason": "error"}]
                }
                yield f"data: {json.dumps(error_chunk)}\n\n"
                yield "data: [DONE]\n\n"
                return

        # Préparer les messages OpenAI
        client, model = get_llm_client()
        openai_messages = [{"role": "system", "content": system_prompt}]
        for msg in messages:
            openai_messages.append({"role": msg.role, "content": msg.content})

        # Appel streaming
        stream = client.chat.completions.create(
            model=model,
            messages=openai_messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True
        )

        # Émettre les chunks au format SSE et compter tokens
        total_output_words = 0
        for chunk in stream:
            if chunk.choices and len(chunk.choices) > 0:
                delta = chunk.choices[0].delta
                content = delta.content if delta.content else ""
                finish_reason = chunk.choices[0].finish_reason

                if content:
                    total_output_words += len(content.split())

                chunk_data = {
                    "id": request_id,
                    "object": "chat.completion.chunk",
                    "created": created,
                    "model": agent_id,
                    "choices": [{
                        "index": 0,
                        "delta": {"content": content} if content else {},
                        "finish_reason": finish_reason
                    }]
                }

                yield f"data: {json.dumps(chunk_data)}\n\n"

        # Token tracking: deduire tokens APRES le stream (estimation)
        if _TOKENS_AVAILABLE and TOKENS_ENABLED and tenant_id:
            try:
                input_tokens = len((system_prompt + " ".join(msg.content for msg in messages)).split())
                output_tokens = int(total_output_words * 1.3)
                deduct_after_llm_call(
                    tenant_id=tenant_id,
                    provider=provider,
                    model=model,
                    tokens_input=input_tokens,
                    tokens_output=output_tokens
                )
            except Exception as e:
                logger.warning(f"Token deduction failed (stream): {e}")

        # Signal de fin
        yield "data: [DONE]\n\n"

    except Exception as e:
        logger.error(f"BMAD streaming error: {e}")
        error_chunk = {
            "id": request_id,
            "object": "chat.completion.chunk",
            "created": created,
            "model": agent_id,
            "choices": [{
                "index": 0,
                "delta": {"content": f"\n\n[Erreur: {str(e)}]"},
                "finish_reason": "error"
            }]
        }
        yield f"data: {json.dumps(error_chunk)}\n\n"
        yield "data: [DONE]\n\n"


@router.post("/chat/completions")
async def chat_completions(request: OpenAIChatRequest, http_request: Request):
    """
    Endpoint OpenAI-compatible pour BMAD chat
    Supporte streaming et non-streaming avec token tracking
    """
    # Token tracking: recuperer tenant_id si disponible
    tenant_id = _get_optional_tenant_id(http_request) if TOKENS_ENABLED else None
    provider = _get_provider_from_env()

    # Valider le modèle
    agent_id = request.model
    if agent_id not in BMAD_MODELS and not agent_id.startswith("bmm-") and not agent_id.startswith("cis-") and not agent_id.startswith("bmb-"):
        raise HTTPException(
            status_code=400,
            detail=f"Unknown model: {agent_id}. Available: {list(BMAD_MODELS.keys())}"
        )

    if request.stream:
        # Mode streaming SSE
        return StreamingResponse(
            stream_bmad_response(
                agent_id=agent_id,
                messages=request.messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                region=request.region,
                tenant_id=tenant_id
            ),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            }
        )

    # Mode non-streaming
    try:
        system_prompt = load_agent_personality(agent_id)

        # RAG context
        user_messages = [msg for msg in request.messages if msg.role == "user"]
        last_user_message = user_messages[-1].content if user_messages else ""

        if last_user_message and RAG_ENABLED:
            rag_context = await get_iafactory_context(last_user_message, request.region)
            if rag_context:
                system_prompt += rag_context

        # Token tracking: verifier solde AVANT l'appel
        if _TOKENS_AVAILABLE and TOKENS_ENABLED and tenant_id:
            total_content = system_prompt + " ".join(msg.content for msg in request.messages)
            estimated_tokens = len(total_content.split()) * 2 + 500
            try:
                check_token_balance(tenant_id, estimated_tokens)
            except InsufficientTokensError as e:
                raise HTTPException(status_code=402, detail=str(e))

        client, model = get_llm_client()
        openai_messages = [{"role": "system", "content": system_prompt}]
        for msg in request.messages:
            openai_messages.append({"role": msg.role, "content": msg.content})

        response = client.chat.completions.create(
            model=model,
            messages=openai_messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )

        # Token tracking: deduire tokens APRES l'appel
        if _TOKENS_AVAILABLE and TOKENS_ENABLED and tenant_id and hasattr(response, 'usage') and response.usage:
            try:
                deduct_after_llm_call(
                    tenant_id=tenant_id,
                    provider=provider,
                    model=model,
                    tokens_input=response.usage.prompt_tokens,
                    tokens_output=response.usage.completion_tokens
                )
            except Exception as e:
                logger.warning(f"Token deduction failed: {e}")

        # Formatter la réponse OpenAI
        return OpenAIChatResponse(
            id=f"chatcmpl-{uuid.uuid4().hex[:24]}",
            created=int(time.time()),
            model=agent_id,
            choices=[
                OpenAIChoice(
                    index=0,
                    message=OpenAIMessage(
                        role="assistant",
                        content=response.choices[0].message.content
                    ),
                    finish_reason="stop"
                )
            ],
            usage=OpenAIUsage(
                prompt_tokens=response.usage.prompt_tokens if response.usage else 0,
                completion_tokens=response.usage.completion_tokens if response.usage else 0,
                total_tokens=response.usage.total_tokens if response.usage else 0
            )
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"BMAD chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def openai_health():
    """Health check pour l'endpoint OpenAI-compatible"""
    try:
        client, model = get_llm_client()
        return {
            "status": "healthy",
            "endpoint": "/api/bmad/v1",
            "models_available": len(BMAD_MODELS),
            "backend_model": model,
            "streaming": True,
            "rag_enabled": RAG_ENABLED
        }
    except Exception as e:
        return {"status": "error", "detail": str(e)}
