"""
Ithy Router - Mixture-of-Agents Research Assistant
Inspired by https://github.com/winsonluk/ithy
"""
import asyncio
import logging
from typing import List, Dict, Optional, AsyncGenerator
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from ..config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/api/ithy", tags=["ithy"])


# Models
class IthyQueryRequest(BaseModel):
    """Request model for ithy query"""
    query: str
    reference_models: Optional[List[str]] = None
    aggregator_model: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2048
    stream: bool = True


class IthyQueryResponse(BaseModel):
    """Response model for ithy query"""
    query: str
    reference_responses: List[Dict[str, str]]
    final_response: str
    models_used: Dict[str, List[str]]


# Aggregator prompt from ithy
AGGREGATOR_PROMPT = """You have been provided with a set of responses from various AI models to the latest user query.
Your task is to synthesize these responses into a single, high-quality response.
It is crucial to critically evaluate the information provided in these responses, recognizing that some of it may be biased or incorrect.
Your response should not simply replicate the given answers but should offer a refined, accurate, and comprehensive reply to the instruction.
Ensure your response is well-structured, coherent, and adheres to the highest standards of accuracy and reliability.

Your knowledge cutoff is today's date, {date}.
Determine the prevalent points of agreement (consensus) among the provided sources.
Your strongest points should be concepts directly related to the user's query.
Prioritize consensus ideas found in multiple sources or models.
Combine similar concepts into single, comprehensive points, presenting each unique point only once in your response.
Do not speculate. Do not use hypotheticals. Do not make assumptions. Do not include placeholders.

Responses from models:"""


class IthyService:
    """Service for Mixture-of-Agents orchestration"""

    def __init__(self):
        # Default reference models - mix of providers
        self.default_reference_models = [
            {"provider": "openai", "model": "gpt-4o-mini"},
            {"provider": "openai", "model": "gpt-3.5-turbo"},
            {"provider": "anthropic", "model": "claude-3-haiku-20240307"},
            {"provider": "anthropic", "model": "claude-3-sonnet-20240229"}
        ]

        # Default aggregator model - use strongest model
        self.default_aggregator = {"provider": "anthropic", "model": "claude-3-5-sonnet-20241022"}

        # Initialize LLM clients
        self._init_clients()

    def _init_clients(self):
        """Initialize LLM clients for different providers"""
        self.openai_client = None
        self.anthropic_client = None

        # Initialize OpenAI
        if settings.openai_api_key:
            try:
                from openai import AsyncOpenAI
                self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
                logger.info("✅ OpenAI async client initialized for ithy")
            except (ImportError, TypeError) as e:
                logger.warning(f"OpenAI client initialization failed: {e}")

        # Initialize Anthropic
        if settings.anthropic_api_key:
            try:
                from anthropic import AsyncAnthropic
                self.anthropic_client = AsyncAnthropic(api_key=settings.anthropic_api_key)
                logger.info("✅ Anthropic async client initialized for ithy")
            except (ImportError, TypeError) as e:
                logger.warning(f"Anthropic client initialization failed: {e}")

    async def _call_openai(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> str:
        """Call OpenAI API"""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        # Retry logic with exponential backoff
        for sleep_time in [1, 2, 4]:
            try:
                response = await self.openai_client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content
            except Exception as e:
                if "rate_limit" in str(e).lower():
                    logger.warning(f"OpenAI rate limit, waiting {sleep_time}s...")
                    await asyncio.sleep(sleep_time)
                else:
                    raise

        raise Exception("OpenAI rate limit exceeded after retries")

    async def _call_anthropic(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> str:
        """Call Anthropic API"""
        if not self.anthropic_client:
            raise ValueError("Anthropic client not initialized")

        # Retry logic with exponential backoff
        for sleep_time in [1, 2, 4]:
            try:
                response = await self.anthropic_client.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    system=system or "You are a helpful AI assistant.",
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            except Exception as e:
                if "rate_limit" in str(e).lower():
                    logger.warning(f"Anthropic rate limit, waiting {sleep_time}s...")
                    await asyncio.sleep(sleep_time)
                else:
                    raise

        raise Exception("Anthropic rate limit exceeded after retries")

    async def _call_model(
        self,
        provider: str,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> str:
        """Universal model caller"""
        try:
            if provider == "openai":
                return await self._call_openai(model, prompt, system, temperature, max_tokens)
            elif provider == "anthropic":
                return await self._call_anthropic(model, prompt, system, temperature, max_tokens)
            else:
                raise ValueError(f"Unsupported provider: {provider}")
        except Exception as e:
            logger.error(f"Error calling {provider}/{model}: {e}")
            return f"[Error from {provider}/{model}: {str(e)}]"

    async def mixture_of_agents_query(
        self,
        query: str,
        reference_models: Optional[List[Dict]] = None,
        aggregator_model: Optional[Dict] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> Dict:
        """
        Execute Mixture-of-Agents query pattern

        Args:
            query: User query
            reference_models: List of reference models to query in parallel
            aggregator_model: Aggregator model to synthesize responses
            temperature: Sampling temperature
            max_tokens: Max tokens per response

        Returns:
            Dict with reference responses and final aggregated response
        """
        # Use defaults if not provided
        if not reference_models:
            reference_models = self.default_reference_models
        if not aggregator_model:
            aggregator_model = self.default_aggregator

        logger.info(f"🔍 Ithy query: {query[:100]}...")
        logger.info(f"📊 Using {len(reference_models)} reference models")

        # Step 1: Query all reference models in parallel
        tasks = [
            self._call_model(
                provider=model["provider"],
                model=model["model"],
                prompt=query,
                temperature=temperature,
                max_tokens=max_tokens
            )
            for model in reference_models
        ]

        reference_responses = await asyncio.gather(*tasks)

        # Build reference responses list
        responses_data = []
        for i, (model_config, response) in enumerate(zip(reference_models, reference_responses), 1):
            responses_data.append({
                "model": f"{model_config['provider']}/{model_config['model']}",
                "response": response
            })

        # Step 2: Build aggregator prompt
        today = datetime.now().strftime("%A, %Y-%m-%d")
        aggregator_system = AGGREGATOR_PROMPT.format(date=today)

        # Add reference responses
        for i, resp_data in enumerate(responses_data, 1):
            aggregator_system += f"\n\n{i}. [{resp_data['model']}]\n{resp_data['response']}"

        # Step 3: Call aggregator model
        logger.info(f"🤖 Aggregating with {aggregator_model['provider']}/{aggregator_model['model']}")

        final_response = await self._call_model(
            provider=aggregator_model["provider"],
            model=aggregator_model["model"],
            prompt=query,
            system=aggregator_system,
            temperature=0.5,  # Lower temperature for synthesis
            max_tokens=max_tokens
        )

        return {
            "query": query,
            "reference_responses": responses_data,
            "final_response": final_response,
            "models_used": {
                "reference": [f"{m['provider']}/{m['model']}" for m in reference_models],
                "aggregator": f"{aggregator_model['provider']}/{aggregator_model['model']}"
            }
        }

    async def mixture_of_agents_stream(
        self,
        query: str,
        reference_models: Optional[List[Dict]] = None,
        aggregator_model: Optional[Dict] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> AsyncGenerator[str, None]:
        """
        Execute Mixture-of-Agents with streaming response
        """
        # Use defaults if not provided
        if not reference_models:
            reference_models = self.default_reference_models
        if not aggregator_model:
            aggregator_model = self.default_aggregator

        logger.info(f"🔍 Ithy streaming query: {query[:100]}...")

        # Step 1: Query all reference models in parallel
        yield f"data: {{'status': 'querying', 'message': 'Querying {len(reference_models)} reference models...'}}\n\n"

        tasks = [
            self._call_model(
                provider=model["provider"],
                model=model["model"],
                prompt=query,
                temperature=temperature,
                max_tokens=max_tokens
            )
            for model in reference_models
        ]

        reference_responses = await asyncio.gather(*tasks)

        # Build reference responses
        responses_data = []
        for i, (model_config, response) in enumerate(zip(reference_models, reference_responses), 1):
            responses_data.append({
                "model": f"{model_config['provider']}/{model_config['model']}",
                "response": response
            })
            yield f"data: {{'status': 'reference_complete', 'model': '{model_config['provider']}/{model_config['model']}', 'index': {i}}}\n\n"

        # Step 2: Build aggregator prompt
        yield f"data: {{'status': 'aggregating', 'message': 'Synthesizing responses...'}}\n\n"

        today = datetime.now().strftime("%A, %Y-%m-%d")
        aggregator_system = AGGREGATOR_PROMPT.format(date=today)

        for i, resp_data in enumerate(responses_data, 1):
            aggregator_system += f"\n\n{i}. [{resp_data['model']}]\n{resp_data['response']}"

        # Step 3: Stream aggregator response
        if aggregator_model["provider"] == "openai":
            async for chunk in self._stream_openai(
                model=aggregator_model["model"],
                prompt=query,
                system=aggregator_system,
                temperature=0.5,
                max_tokens=max_tokens
            ):
                yield f"data: {{'status': 'streaming', 'content': '{chunk}'}}\n\n"
        elif aggregator_model["provider"] == "anthropic":
            async for chunk in self._stream_anthropic(
                model=aggregator_model["model"],
                prompt=query,
                system=aggregator_system,
                temperature=0.5,
                max_tokens=max_tokens
            ):
                yield f"data: {{'status': 'streaming', 'content': '{chunk}'}}\n\n"

        yield f"data: {{'status': 'complete'}}\n\n"

    async def _stream_openai(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> AsyncGenerator[str, None]:
        """Stream OpenAI response"""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        stream = await self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                # Escape for SSE format
                content = chunk.choices[0].delta.content.replace('"', '\\"').replace('\n', '\\n')
                yield content

    async def _stream_anthropic(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> AsyncGenerator[str, None]:
        """Stream Anthropic response"""
        if not self.anthropic_client:
            raise ValueError("Anthropic client not initialized")

        async with self.anthropic_client.messages.stream(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system or "You are a helpful AI assistant.",
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            async for text in stream.text_stream:
                # Escape for SSE format
                content = text.replace('"', '\\"').replace('\n', '\\n')
                yield content


# Initialize service
ithy_service = IthyService()


# Routes
@router.post("/query", response_model=IthyQueryResponse)
async def ithy_query(request: IthyQueryRequest):
    """
    Execute Mixture-of-Agents query (non-streaming)

    This endpoint queries multiple AI models in parallel,
    then synthesizes their responses into a single high-quality answer.
    """
    try:
        # Parse reference models if provided
        reference_models = None
        if request.reference_models:
            reference_models = []
            for model_str in request.reference_models:
                provider, model = model_str.split("/", 1)
                reference_models.append({"provider": provider, "model": model})

        # Parse aggregator model if provided
        aggregator_model = None
        if request.aggregator_model:
            provider, model = request.aggregator_model.split("/", 1)
            aggregator_model = {"provider": provider, "model": model}

        # Execute MoA query
        result = await ithy_service.mixture_of_agents_query(
            query=request.query,
            reference_models=reference_models,
            aggregator_model=aggregator_model,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )

        return result

    except Exception as e:
        logger.error(f"Ithy query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query/stream")
async def ithy_query_stream(request: IthyQueryRequest):
    """
    Execute Mixture-of-Agents query with streaming response

    This endpoint queries multiple AI models in parallel,
    then streams the synthesized response using Server-Sent Events (SSE).
    """
    try:
        # Parse models
        reference_models = None
        if request.reference_models:
            reference_models = []
            for model_str in request.reference_models:
                provider, model = model_str.split("/", 1)
                reference_models.append({"provider": provider, "model": model})

        aggregator_model = None
        if request.aggregator_model:
            provider, model = request.aggregator_model.split("/", 1)
            aggregator_model = {"provider": provider, "model": model}

        # Stream response
        return StreamingResponse(
            ithy_service.mixture_of_agents_stream(
                query=request.query,
                reference_models=reference_models,
                aggregator_model=aggregator_model,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            ),
            media_type="text/event-stream"
        )

    except Exception as e:
        logger.error(f"Ithy streaming error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models")
async def list_available_models():
    """List available models for ithy"""
    models = {
        "reference_models": [
            {"id": "openai/gpt-4o-mini", "name": "GPT-4o Mini", "provider": "OpenAI"},
            {"id": "openai/gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "provider": "OpenAI"},
            {"id": "anthropic/claude-3-haiku-20240307", "name": "Claude 3 Haiku", "provider": "Anthropic"},
            {"id": "anthropic/claude-3-sonnet-20240229", "name": "Claude 3 Sonnet", "provider": "Anthropic"},
        ],
        "aggregator_models": [
            {"id": "anthropic/claude-3-5-sonnet-20241022", "name": "Claude 3.5 Sonnet", "provider": "Anthropic"},
            {"id": "openai/gpt-4o", "name": "GPT-4o", "provider": "OpenAI"},
            {"id": "anthropic/claude-3-opus-20240229", "name": "Claude 3 Opus", "provider": "Anthropic"},
        ]
    }
    return models


@router.get("/status")
async def ithy_status():
    """Get ithy service status"""
    return {
        "status": "operational",
        "service": "ithy-moa",
        "version": "1.0.0",
        "openai_available": ithy_service.openai_client is not None,
        "anthropic_available": ithy_service.anthropic_client is not None,
        "description": "Mixture-of-Agents research assistant"
    }
