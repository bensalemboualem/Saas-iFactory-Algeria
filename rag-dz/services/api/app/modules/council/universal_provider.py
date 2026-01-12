"""
Universal Provider Factory - Support pour tous les LLM providers
OpenAI, Anthropic, Google, Mistral, Ollama
"""
from abc import ABC, abstractmethod
import httpx
import os
from typing import Optional
import logging

from .models_config import AvailableModels

logger = logging.getLogger(__name__)


class UniversalProvider:
    """Factory pour tous les providers"""

    @staticmethod
    def get_provider(model_id: str):
        """Retourne le bon provider selon le model_id"""
        if model_id not in AvailableModels.MODELS:
            raise ValueError(f"Modèle inconnu: {model_id}")

        model_info = AvailableModels.MODELS[model_id]
        provider_name = model_info["provider"]

        providers = {
            "openai": OpenAIProvider,
            "anthropic": ClaudeProvider,
            "google": GeminiProvider,
            "mistral": MistralProvider,
            "xai": XAIProvider,
            "deepseek": DeepSeekProvider,
            "qwen": QwenProvider,
            "perplexity": PerplexityProvider,
            "moonshot": MoonshotProvider,
            "ollama": OllamaProvider
        }

        if provider_name not in providers:
            raise ValueError(f"Provider non supporté: {provider_name}")

        return providers[provider_name](model_id, model_info)


class BaseProvider(ABC):
    """Classe de base pour tous les providers"""

    def __init__(self, model_id: str, model_info: dict):
        self.model_id = model_id
        self.model_info = model_info
        self.model_name = model_info.get("name", model_id)

    @abstractmethod
    async def generate(self, prompt: str, system: str = None) -> str:
        """Génère une réponse"""
        pass

    def is_available(self) -> bool:
        """Vérifie si le provider est disponible"""
        return True


class OpenAIProvider(BaseProvider):
    """Provider pour OpenAI (GPT-4, GPT-3.5)"""

    async def generate(self, prompt: str, system: str = None) -> str:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY non configurée")

        async with httpx.AsyncClient(timeout=60.0) as client:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

            payload = {
                "model": self.model_id,
                "messages": messages,
                "max_tokens": 2048
            }

            try:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except Exception as e:
                logger.error(f"OpenAI API error: {e}")
                raise

    def is_available(self) -> bool:
        return bool(os.getenv("OPENAI_API_KEY"))


class ClaudeProvider(BaseProvider):
    """Provider pour Anthropic Claude"""

    async def generate(self, prompt: str, system: str = None) -> str:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY non configurée")

        async with httpx.AsyncClient(timeout=60.0) as client:
            headers = {
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }

            payload = {
                "model": self.model_id,
                "max_tokens": 2048,
                "messages": [{"role": "user", "content": prompt}]
            }

            if system:
                payload["system"] = system

            try:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                return data["content"][0]["text"]
            except Exception as e:
                logger.error(f"Anthropic API error: {e}")
                raise

    def is_available(self) -> bool:
        return bool(os.getenv("ANTHROPIC_API_KEY"))


class GeminiProvider(BaseProvider):
    """Provider pour Google Gemini"""

    async def generate(self, prompt: str, system: str = None) -> str:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY non configurée")

        # Map model_id to Gemini API format
        model_mapping = {
            "gemini-1.5-pro": "gemini-1.5-pro",
            "gemini-1.5-flash": "gemini-1.5-flash"
        }
        gemini_model = model_mapping.get(self.model_id, "gemini-1.5-pro")

        async with httpx.AsyncClient(timeout=60.0) as client:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{gemini_model}:generateContent"

            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "maxOutputTokens": 2048
                }
            }

            if system:
                payload["systemInstruction"] = {"parts": [{"text": system}]}

            try:
                response = await client.post(
                    url,
                    params={"key": api_key},
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            except Exception as e:
                logger.error(f"Google Gemini API error: {e}")
                raise

    def is_available(self) -> bool:
        return bool(os.getenv("GOOGLE_API_KEY"))


class MistralProvider(BaseProvider):
    """Provider pour Mistral AI"""

    async def generate(self, prompt: str, system: str = None) -> str:
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY non configurée")

        async with httpx.AsyncClient(timeout=60.0) as client:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

            payload = {
                "model": self.model_id,
                "messages": messages,
                "max_tokens": 2048
            }

            try:
                response = await client.post(
                    "https://api.mistral.ai/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except Exception as e:
                logger.error(f"Mistral API error: {e}")
                raise

    def is_available(self) -> bool:
        return bool(os.getenv("MISTRAL_API_KEY"))


class OllamaProvider(BaseProvider):
    """Provider pour Ollama (modèles locaux)"""

    async def generate(self, prompt: str, system: str = None) -> str:
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

        # Get the actual Ollama model name
        ollama_model = self.model_info.get("ollama_model", self.model_id)

        async with httpx.AsyncClient(timeout=120.0) as client:
            payload = {
                "model": ollama_model,
                "prompt": prompt,
                "stream": False
            }

            if system:
                payload["system"] = system

            try:
                response = await client.post(
                    f"{base_url}/api/generate",
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                return data["response"]
            except Exception as e:
                logger.error(f"Ollama API error: {e}")
                raise

    def is_available(self) -> bool:
        base_url = os.getenv("OLLAMA_BASE_URL")
        return bool(base_url)


class XAIProvider(BaseProvider):
    """Provider pour xAI Grok"""

    async def generate(self, prompt: str, system: str = None) -> str:
        api_key = os.getenv("XAI_API_KEY")
        if not api_key:
            raise ValueError("XAI_API_KEY non configurée")

        async with httpx.AsyncClient(timeout=60.0) as client:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

            payload = {
                "model": self.model_id,
                "messages": messages,
                "max_tokens": 2048
            }

            try:
                response = await client.post(
                    "https://api.x.ai/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except Exception as e:
                logger.error(f"xAI API error: {e}")
                raise

    def is_available(self) -> bool:
        return bool(os.getenv("XAI_API_KEY"))


class DeepSeekProvider(BaseProvider):
    """Provider pour DeepSeek"""

    async def generate(self, prompt: str, system: str = None) -> str:
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY non configurée")

        async with httpx.AsyncClient(timeout=60.0) as client:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

            payload = {
                "model": self.model_id,
                "messages": messages,
                "max_tokens": 2048
            }

            try:
                response = await client.post(
                    "https://api.deepseek.com/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except Exception as e:
                logger.error(f"DeepSeek API error: {e}")
                raise

    def is_available(self) -> bool:
        return bool(os.getenv("DEEPSEEK_API_KEY"))


class QwenProvider(BaseProvider):
    """Provider pour Qwen (via DashScope API)"""

    async def generate(self, prompt: str, system: str = None) -> str:
        api_key = os.getenv("QWEN_API_KEY")
        if not api_key:
            raise ValueError("QWEN_API_KEY non configurée")

        async with httpx.AsyncClient(timeout=60.0) as client:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

            payload = {
                "model": self.model_id,
                "messages": messages,
                "max_tokens": 2048
            }

            try:
                response = await client.post(
                    "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except Exception as e:
                logger.error(f"Qwen API error: {e}")
                raise

    def is_available(self) -> bool:
        return bool(os.getenv("QWEN_API_KEY"))


class PerplexityProvider(BaseProvider):
    """Provider pour Perplexity"""

    async def generate(self, prompt: str, system: str = None) -> str:
        api_key = os.getenv("PERPLEXITY_API_KEY")
        if not api_key:
            raise ValueError("PERPLEXITY_API_KEY non configurée")

        async with httpx.AsyncClient(timeout=60.0) as client:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

            payload = {
                "model": self.model_id,
                "messages": messages,
                "max_tokens": 2048
            }

            try:
                response = await client.post(
                    "https://api.perplexity.ai/chat/completions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except Exception as e:
                logger.error(f"Perplexity API error: {e}")
                raise

    def is_available(self) -> bool:
        return bool(os.getenv("PERPLEXITY_API_KEY"))


class MoonshotProvider(BaseProvider):
    """Provider pour Moonshot (Kimi)"""

    async def generate(self, prompt: str, system: str = None) -> str:
        api_key = os.getenv("MOONSHOT_API_KEY")
        if not api_key:
            raise ValueError("MOONSHOT_API_KEY non configurée")

        async with httpx.AsyncClient(timeout=60.0) as client:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

            payload = {
                "model": "moonshot-v1-32k",
                "messages": messages,
                "max_tokens": 2048
            }

            try:
                response = await client.post(
                    "https://api.moonshot.cn/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except Exception as e:
                logger.error(f"Moonshot API error: {e}")
                raise

    def is_available(self) -> bool:
        return bool(os.getenv("MOONSHOT_API_KEY"))
