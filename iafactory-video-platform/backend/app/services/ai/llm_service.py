"""
LLM Service - Unified interface for all LLM providers
"""
from typing import Optional, List, Dict, Any, AsyncGenerator
from abc import ABC, abstractmethod
import httpx
from app.core.config import settings


class BaseLLMProvider(ABC):
    """Base class for LLM providers"""

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        pass

    @abstractmethod
    async def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        pass


class OpenAIProvider(BaseLLMProvider):
    """OpenAI GPT provider"""

    def __init__(self, api_key: str, model: str = "gpt-4-turbo-preview"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.openai.com/v1"

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                },
                timeout=120.0
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": True,
                },
                timeout=120.0
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: ") and line != "data: [DONE]":
                        import json
                        data = json.loads(line[6:])
                        if data["choices"][0].get("delta", {}).get("content"):
                            yield data["choices"][0]["delta"]["content"]


class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude provider"""

    def __init__(self, api_key: str, model: str = "claude-3-opus-20240229"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.anthropic.com/v1"

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/messages",
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": self.model,
                    "max_tokens": max_tokens,
                    "system": system_prompt or "",
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=120.0
            )
            response.raise_for_status()
            data = response.json()
            return data["content"][0]["text"]

    async def generate_stream(self, prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        # Simplified - implement full streaming if needed
        result = await self.generate(prompt, **kwargs)
        yield result


class GroqProvider(BaseLLMProvider):
    """Groq provider (fast inference)"""

    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.groq.com/openai/v1"

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                },
                timeout=60.0
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def generate_stream(self, prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        result = await self.generate(prompt, **kwargs)
        yield result


class DeepSeekProvider(BaseLLMProvider):
    """DeepSeek provider"""

    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.deepseek.com/v1"

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                },
                timeout=120.0
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def generate_stream(self, prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        result = await self.generate(prompt, **kwargs)
        yield result


class LLMService:
    """Unified LLM service with multiple provider support"""

    PROVIDERS = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "groq": GroqProvider,
        "deepseek": DeepSeekProvider,
    }

    def __init__(self, default_provider: str = None):
        self.default_provider = default_provider or settings.DEFAULT_LLM_PROVIDER
        self._providers: Dict[str, BaseLLMProvider] = {}
        self._init_providers()

    def _init_providers(self):
        """Initialize available providers based on API keys"""
        if settings.OPENAI_API_KEY:
            self._providers["openai"] = OpenAIProvider(
                settings.OPENAI_API_KEY, settings.OPENAI_MODEL
            )
        if settings.ANTHROPIC_API_KEY:
            self._providers["anthropic"] = AnthropicProvider(
                settings.ANTHROPIC_API_KEY, settings.ANTHROPIC_MODEL
            )
        if settings.GROQ_API_KEY:
            self._providers["groq"] = GroqProvider(
                settings.GROQ_API_KEY, settings.GROQ_MODEL
            )
        if settings.DEEPSEEK_API_KEY:
            self._providers["deepseek"] = DeepSeekProvider(
                settings.DEEPSEEK_API_KEY, settings.DEEPSEEK_MODEL
            )

    def get_provider(self, name: str = None) -> BaseLLMProvider:
        """Get a specific provider or the default one"""
        provider_name = name or self.default_provider
        if provider_name not in self._providers:
            available = list(self._providers.keys())
            if not available:
                raise ValueError("No LLM providers configured. Add API keys to .env")
            provider_name = available[0]
        return self._providers[provider_name]

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        provider: str = None,
        **kwargs
    ) -> str:
        """Generate text using specified or default provider"""
        return await self.get_provider(provider).generate(
            prompt, system_prompt, **kwargs
        )

    async def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        provider: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate and parse JSON response"""
        import json

        json_system = (system_prompt or "") + "\n\nRespond ONLY with valid JSON."
        result = await self.generate(prompt, json_system, provider, **kwargs)

        # Clean response
        result = result.strip()
        if result.startswith("```json"):
            result = result[7:]
        if result.startswith("```"):
            result = result[3:]
        if result.endswith("```"):
            result = result[:-3]

        return json.loads(result.strip())

    def available_providers(self) -> List[str]:
        """List available providers"""
        return list(self._providers.keys())


# Singleton instance
llm_service = LLMService()
