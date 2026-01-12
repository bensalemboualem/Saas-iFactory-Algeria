"""
Streaming Router - Server-Sent Events for Real-Time LLM Responses
Provides streaming endpoints for all LLM operations
Token tracking integre.
"""
import asyncio
import json
import logging
from typing import AsyncGenerator, Optional, Dict, Any
from datetime import datetime

from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.config import get_settings
from app.dependencies import get_current_user
from app.clients.llm_client import get_llm_client

# Token tracking
try:
    from app.tokens.llm_proxy import check_token_balance, deduct_after_llm_call, InsufficientTokensError
    TOKENS_ENABLED = True
except ImportError:
    TOKENS_ENABLED = False

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/api/stream", tags=["Streaming"])


def _get_optional_tenant_id(request: Request) -> Optional[str]:
    """Recupere tenant_id si disponible (backward compatible)."""
    return getattr(request.state, "tenant_id", None)


class StreamRequest(BaseModel):
    """Request for streaming LLM response"""
    prompt: str
    system_prompt: Optional[str] = None
    model: str = "gpt-4o-mini"
    provider: str = "openai"  # openai, anthropic, groq, ollama
    temperature: float = 0.7
    max_tokens: int = 4096
    conversation_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class StreamEvent:
    """SSE Event formatter"""

    @staticmethod
    def data(content: str, event_type: str = "message") -> str:
        """Format SSE data event"""
        return f"event: {event_type}\ndata: {json.dumps({'content': content, 'timestamp': datetime.utcnow().isoformat()})}\n\n"

    @staticmethod
    def error(message: str) -> str:
        """Format SSE error event"""
        return f"event: error\ndata: {json.dumps({'error': message})}\n\n"

    @staticmethod
    def done(metadata: Dict[str, Any] = None) -> str:
        """Format SSE done event"""
        return f"event: done\ndata: {json.dumps({'done': True, 'metadata': metadata or {}})}\n\n"

    @staticmethod
    def thinking(content: str) -> str:
        """Format thinking/reasoning event"""
        return f"event: thinking\ndata: {json.dumps({'thinking': content})}\n\n"


async def stream_openai_response(
    prompt: str,
    system_prompt: str,
    model: str,
    temperature: float,
    max_tokens: int,
    tenant_id: Optional[str] = None
) -> AsyncGenerator[str, None]:
    """Stream response from OpenAI with token tracking"""
    try:
        import openai
        client = openai.AsyncOpenAI(api_key=settings.openai_api_key)

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        stream = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True
        )

        full_response = ""
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                full_response += content
                yield StreamEvent.data(content)

        # Token tracking: deduire tokens APRES le stream (estimation)
        if TOKENS_ENABLED and tenant_id:
            try:
                input_tokens = len((prompt + (system_prompt or "")).split())
                output_tokens = int(len(full_response.split()) * 1.3)
                deduct_after_llm_call(
                    tenant_id=tenant_id,
                    provider="openai",
                    model=model,
                    tokens_input=input_tokens,
                    tokens_output=output_tokens
                )
            except Exception as e:
                logger.warning(f"Token deduction failed (stream_openai): {e}")

        yield StreamEvent.done({"total_tokens": len(full_response.split())})

    except Exception as e:
        logger.error(f"OpenAI streaming error: {e}")
        yield StreamEvent.error(str(e))


async def stream_anthropic_response(
    prompt: str,
    system_prompt: str,
    model: str,
    temperature: float,
    max_tokens: int,
    tenant_id: Optional[str] = None
) -> AsyncGenerator[str, None]:
    """Stream response from Anthropic Claude with token tracking"""
    try:
        import anthropic
        client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

        async with client.messages.stream(
            model=model or "claude-3-5-sonnet-20241022",
            max_tokens=max_tokens,
            system=system_prompt or "",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        ) as stream:
            full_response = ""
            async for text in stream.text_stream:
                full_response += text
                yield StreamEvent.data(text)

            # Get final message for metadata
            message = await stream.get_final_message()

            # Token tracking: deduire tokens APRES le stream
            if TOKENS_ENABLED and tenant_id and message.usage:
                try:
                    deduct_after_llm_call(
                        tenant_id=tenant_id,
                        provider="anthropic",
                        model=model or "claude-3-5-sonnet-20241022",
                        tokens_input=message.usage.input_tokens,
                        tokens_output=message.usage.output_tokens
                    )
                except Exception as e:
                    logger.warning(f"Token deduction failed (stream_anthropic): {e}")

            yield StreamEvent.done({
                "input_tokens": message.usage.input_tokens,
                "output_tokens": message.usage.output_tokens,
                "model": message.model
            })

    except Exception as e:
        logger.error(f"Anthropic streaming error: {e}")
        yield StreamEvent.error(str(e))


async def stream_groq_response(
    prompt: str,
    system_prompt: str,
    model: str,
    temperature: float,
    max_tokens: int,
    tenant_id: Optional[str] = None
) -> AsyncGenerator[str, None]:
    """Stream response from Groq with token tracking"""
    try:
        from groq import AsyncGroq
        client = AsyncGroq(api_key=settings.groq_api_key)

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        stream = await client.chat.completions.create(
            model=model or "llama-3.3-70b-versatile",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True
        )

        full_response = ""
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                full_response += content
                yield StreamEvent.data(content)

        # Token tracking: deduire tokens APRES le stream (estimation)
        if TOKENS_ENABLED and tenant_id:
            try:
                input_tokens = len((prompt + (system_prompt or "")).split())
                output_tokens = int(len(full_response.split()) * 1.3)
                deduct_after_llm_call(
                    tenant_id=tenant_id,
                    provider="groq",
                    model=model or "llama-3.3-70b-versatile",
                    tokens_input=input_tokens,
                    tokens_output=output_tokens
                )
            except Exception as e:
                logger.warning(f"Token deduction failed (stream_groq): {e}")

        yield StreamEvent.done({"model": model})

    except Exception as e:
        logger.error(f"Groq streaming error: {e}")
        yield StreamEvent.error(str(e))


async def stream_ollama_response(
    prompt: str,
    system_prompt: str,
    model: str,
    temperature: float,
    max_tokens: int,
    tenant_id: Optional[str] = None  # Ollama is local/free, no deduction needed
) -> AsyncGenerator[str, None]:
    """Stream response from local Ollama (no token deduction - local model)"""
    try:
        import httpx

        ollama_url = settings.ollama_url or "http://localhost:11434"

        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{ollama_url}/api/generate",
                json={
                    "model": model or "llama3.2",
                    "prompt": prompt,
                    "system": system_prompt or "",
                    "stream": True,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                },
                timeout=300.0
            ) as response:
                full_response = ""
                async for line in response.aiter_lines():
                    if line:
                        data = json.loads(line)
                        if "response" in data:
                            content = data["response"]
                            full_response += content
                            yield StreamEvent.data(content)
                        if data.get("done"):
                            yield StreamEvent.done({
                                "total_duration": data.get("total_duration"),
                                "eval_count": data.get("eval_count")
                            })

    except Exception as e:
        logger.error(f"Ollama streaming error: {e}")
        yield StreamEvent.error(str(e))


@router.post("/chat")
async def stream_chat(
    request: StreamRequest,
    http_request: Request,
    current_user: dict = Depends(get_current_user)
):
    """
    Stream LLM response via Server-Sent Events

    Supports: OpenAI, Anthropic, Groq, Ollama

    Usage:
    ```javascript
    const eventSource = new EventSource('/api/stream/chat', {
        method: 'POST',
        body: JSON.stringify({ prompt: 'Hello', provider: 'openai' })
    });
    eventSource.onmessage = (e) => console.log(JSON.parse(e.data));
    ```
    """
    # Token tracking: recuperer tenant_id si disponible
    tenant_id = _get_optional_tenant_id(http_request) if TOKENS_ENABLED else None

    # Token tracking: verifier solde AVANT l'appel (sauf Ollama qui est local)
    if TOKENS_ENABLED and tenant_id and request.provider != "ollama":
        estimated_tokens = len(request.prompt.split()) * 2 + len((request.system_prompt or "").split()) + 500
        try:
            check_token_balance(tenant_id, estimated_tokens)
        except InsufficientTokensError as e:
            raise HTTPException(status_code=402, detail=str(e))

    provider_streams = {
        "openai": stream_openai_response,
        "anthropic": stream_anthropic_response,
        "groq": stream_groq_response,
        "ollama": stream_ollama_response,
    }

    stream_func = provider_streams.get(request.provider)
    if not stream_func:
        raise HTTPException(status_code=400, detail=f"Unknown provider: {request.provider}")

    async def event_generator():
        # Start event
        yield StreamEvent.data("", "start")

        # Stream response with tenant_id for token tracking
        async for event in stream_func(
            prompt=request.prompt,
            system_prompt=request.system_prompt,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            tenant_id=tenant_id
        ):
            yield event

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )


@router.post("/bmad")
async def stream_bmad_chat(
    request: StreamRequest,
    http_request: Request,
    agent: str = "architect",
    current_user: dict = Depends(get_current_user)
):
    """
    Stream BMAD agent response

    Agents: architect, pm, developer, analyst, tester
    """
    from app.services.bmad_orchestrator import bmad_orchestrator

    # Token tracking: recuperer tenant_id si disponible
    tenant_id = _get_optional_tenant_id(http_request) if TOKENS_ENABLED else None

    # Token tracking: verifier solde AVANT l'appel
    if TOKENS_ENABLED and tenant_id:
        estimated_tokens = len(request.prompt.split()) * 2 + 1000  # BMAD uses more context
        try:
            check_token_balance(tenant_id, estimated_tokens)
        except InsufficientTokensError as e:
            raise HTTPException(status_code=402, detail=str(e))

    async def bmad_stream():
        yield StreamEvent.data("", "start")

        try:
            # Get agent persona
            persona = bmad_orchestrator.get_agent_persona(agent)
            system_prompt = f"""Tu es {persona.get('name', agent)}, {persona.get('role', 'un expert')}.

{persona.get('system_prompt', '')}

Contexte projet BMAD:
{request.system_prompt or 'Projet IAFactory Algérie'}
"""

            # Stream via preferred provider with tenant_id for token tracking
            async for event in stream_anthropic_response(
                prompt=request.prompt,
                system_prompt=system_prompt,
                model="claude-3-5-sonnet-20241022",
                temperature=0.7,
                max_tokens=request.max_tokens,
                tenant_id=tenant_id
            ):
                yield event

        except Exception as e:
            yield StreamEvent.error(str(e))

    return StreamingResponse(
        bmad_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@router.post("/rag")
async def stream_rag_response(
    request: StreamRequest,
    http_request: Request,
    region: str = "dz",
    current_user: dict = Depends(get_current_user)
):
    """
    Stream RAG-augmented response with context retrieval
    """
    from app.bigrag import bigrag_service

    # Token tracking: recuperer tenant_id si disponible
    tenant_id = _get_optional_tenant_id(http_request) if TOKENS_ENABLED else None

    # Token tracking: verifier solde AVANT l'appel (RAG uses more context)
    if TOKENS_ENABLED and tenant_id:
        estimated_tokens = len(request.prompt.split()) * 3 + 2000  # RAG adds context
        try:
            check_token_balance(tenant_id, estimated_tokens)
        except InsufficientTokensError as e:
            raise HTTPException(status_code=402, detail=str(e))

    async def rag_stream():
        yield StreamEvent.data("", "start")

        try:
            # Retrieve context
            yield StreamEvent.thinking("Recherche du contexte pertinent...")

            context_results = await bigrag_service.search(
                query=request.prompt,
                region=region,
                limit=5
            )

            # Build augmented prompt
            context_text = "\n\n".join([
                f"[Source: {r.get('source', 'unknown')}]\n{r.get('content', '')}"
                for r in context_results.get("results", [])
            ])

            augmented_prompt = f"""Contexte récupéré:
{context_text}

Question: {request.prompt}

Réponds en te basant sur le contexte ci-dessus. Cite tes sources."""

            yield StreamEvent.thinking(f"Contexte trouvé: {len(context_results.get('results', []))} documents")

            # Stream response with tenant_id for token tracking
            async for event in stream_openai_response(
                prompt=augmented_prompt,
                system_prompt=request.system_prompt or "Tu es un assistant RAG expert pour l'Algérie.",
                model=request.model,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                tenant_id=tenant_id
            ):
                yield event

        except Exception as e:
            yield StreamEvent.error(str(e))

    return StreamingResponse(
        rag_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@router.get("/health")
async def streaming_health():
    """Check streaming service health"""
    return {
        "status": "healthy",
        "providers": ["openai", "anthropic", "groq", "ollama"],
        "timestamp": datetime.utcnow().isoformat()
    }
