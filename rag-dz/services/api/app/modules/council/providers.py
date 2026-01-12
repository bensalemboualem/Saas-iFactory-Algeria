"""
LLM Providers pour Council
Implémentation des interfaces pour Claude, Gemini et Ollama
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import httpx
import os
import logging

logger = logging.getLogger(__name__)


class LLMProvider(ABC):
    """Interface abstraite pour tous les providers LLM"""

    @abstractmethod
    async def generate(self, prompt: str, system: Optional[str] = None) -> str:
        """Génère une réponse à partir d'un prompt"""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Vérifie si le provider est disponible"""
        pass


class ClaudeProvider(LLMProvider):
    """Provider pour Claude (Anthropic)"""

    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.base_url = "https://api.anthropic.com/v1"
        self.model = "claude-sonnet-4-20250514"

    def is_available(self) -> bool:
        return bool(self.api_key)

    async def generate(self, prompt: str, system: Optional[str] = None) -> str:
        if not self.is_available():
            raise ValueError("ANTHROPIC_API_KEY not configured")

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                headers = {
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                }

                payload = {
                    "model": self.model,
                    "max_tokens": 2048,
                    "messages": [{"role": "user", "content": prompt}]
                }

                if system:
                    payload["system"] = system

                response = await client.post(
                    f"{self.base_url}/messages",
                    headers=headers,
                    json=payload
                )

                response.raise_for_status()
                data = response.json()
                return data["content"][0]["text"]

        except httpx.HTTPStatusError as e:
            logger.error(f"Claude API error: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Claude API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Claude provider error: {str(e)}")
            raise


class GeminiProvider(LLMProvider):
    """Provider pour Gemini (Google)"""

    def __init__(self):
        self.api_key = os.getenv("GOOGLE_GENERATIVE_AI_API_KEY", "")
        self.base_url = "https://generativelanguage.googleapis.com/v1"
        self.model = "gemini-2.5-flash"

    def is_available(self) -> bool:
        return bool(self.api_key)

    async def generate(self, prompt: str, system: Optional[str] = None) -> str:
        if not self.is_available():
            raise ValueError("GOOGLE_GENERATIVE_AI_API_KEY not configured")

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Gemini API v1 endpoint (not v1beta)
                url = f"https://generativelanguage.googleapis.com/v1/models/{self.model}:generateContent"

                # Combine system and user prompt
                full_prompt = prompt
                if system:
                    full_prompt = f"{system}\n\n{prompt}"

                payload = {
                    "contents": [{
                        "parts": [{"text": full_prompt}]
                    }],
                    "generationConfig": {
                        "maxOutputTokens": 2048,
                        "temperature": 0.7
                    }
                }

                response = await client.post(
                    url,
                    params={"key": self.api_key},
                    json=payload
                )

                response.raise_for_status()
                data = response.json()

                if "candidates" in data and len(data["candidates"]) > 0:
                    return data["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    raise Exception("No response from Gemini")

        except httpx.HTTPStatusError as e:
            logger.error(f"Gemini API error: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Gemini API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Gemini provider error: {str(e)}")
            raise


class OllamaProvider(LLMProvider):
    """Provider pour Ollama (modèles locaux)"""

    def __init__(self, model: str = "llama3.2:3b"):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://iaf-ollama:11434")
        self.model = model

    def is_available(self) -> bool:
        """Vérifie si Ollama est accessible"""
        try:
            import httpx
            with httpx.Client(timeout=5.0) as client:
                response = client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except:
            return False

    async def generate(self, prompt: str, system: Optional[str] = None) -> str:
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                payload = {
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 1024,
                        "num_ctx": 2048
                    }
                }

                if system:
                    payload["system"] = system

                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=payload
                )

                response.raise_for_status()
                data = response.json()
                return data.get("response", "")

        except httpx.HTTPStatusError as e:
            logger.error(f"Ollama API error: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Ollama API error: {e.response.status_code}")
        except httpx.ConnectError:
            logger.error(f"Cannot connect to Ollama at {self.base_url}")
            raise Exception("Ollama service not available")
        except Exception as e:
            logger.error(f"Ollama provider error: {str(e)}")
            raise


class ChatGPTProvider(LLMProvider):
    """Provider pour ChatGPT (OpenAI) - Support multiple models"""

    def __init__(self, model: str = "gpt-4-turbo-preview"):
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.base_url = "https://api.openai.com/v1"
        self.model = model

    def is_available(self) -> bool:
        return bool(self.api_key)

    async def generate(self, prompt: str, system: Optional[str] = None) -> str:
        if not self.is_available():
            raise ValueError("OPENAI_API_KEY not configured")

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }

                messages = []
                if system:
                    messages.append({"role": "system", "content": system})
                messages.append({"role": "user", "content": prompt})

                payload = {
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": 2048,
                    "temperature": 0.7
                }

                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )

                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]

        except httpx.HTTPStatusError as e:
            logger.error(f"ChatGPT API error: {e.response.status_code} - {e.response.text}")
            raise Exception(f"ChatGPT API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"ChatGPT provider error: {str(e)}")
            raise


class MistralProvider(LLMProvider):
    """Provider pour Mistral AI"""

    def __init__(self, model: str = "mistral-large-latest"):
        self.api_key = os.getenv("MISTRAL_API_KEY", "")
        self.base_url = "https://api.mistral.ai/v1"
        self.model = model

    def is_available(self) -> bool:
        return bool(self.api_key)

    async def generate(self, prompt: str, system: Optional[str] = None) -> str:
        if not self.is_available():
            raise ValueError("MISTRAL_API_KEY not configured")

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }

                messages = []
                if system:
                    messages.append({"role": "system", "content": system})
                messages.append({"role": "user", "content": prompt})

                payload = {
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": 2048,
                    "temperature": 0.7
                }

                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )

                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]

        except httpx.HTTPStatusError as e:
            logger.error(f"Mistral API error: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Mistral API error: {e.response.status_code}")
        except httpx.TimeoutException as e:
            logger.error(f"Mistral timeout error: {str(e)}")
            raise Exception("Mistral API timeout - try again")
        except Exception as e:
            logger.error(f"Mistral provider error: {str(e)}")
            raise Exception(f"Mistral error: {str(e)}")


class PerplexityProvider(LLMProvider):
    """Provider pour Perplexity"""

    def __init__(self):
        self.api_key = os.getenv("PERPLEXITY_API_KEY", "")
        self.base_url = "https://api.perplexity.ai"
        self.model = "llama-3.1-sonar-large-128k-online"

    def is_available(self) -> bool:
        return bool(self.api_key)

    async def generate(self, prompt: str, system: Optional[str] = None) -> str:
        if not self.is_available():
            raise ValueError("PERPLEXITY_API_KEY not configured")

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }

                messages = []
                if system:
                    messages.append({"role": "system", "content": system})
                messages.append({"role": "user", "content": prompt})

                payload = {
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": 2048,
                    "temperature": 0.7
                }

                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )

                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]

        except httpx.HTTPStatusError as e:
            logger.error(f"Perplexity API error: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Perplexity API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Perplexity provider error: {str(e)}")
            raise


class GroqProvider(LLMProvider):
    """Provider pour Groq (ultra-rapide)"""

    def __init__(self, model: str = "llama-3.3-70b-versatile"):
        self.api_key = os.getenv("GROQ_API_KEY", "")
        self.base_url = "https://api.groq.com/openai/v1"
        self.model = model

    def is_available(self) -> bool:
        return bool(self.api_key)

    async def generate(self, prompt: str, system: Optional[str] = None) -> str:
        if not self.is_available():
            raise ValueError("GROQ_API_KEY not configured")

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }

                messages = []
                if system:
                    messages.append({"role": "system", "content": system})
                messages.append({"role": "user", "content": prompt})

                payload = {
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": 2048,
                    "temperature": 0.7
                }

                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )

                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]

        except httpx.HTTPStatusError as e:
            logger.error(f"Groq API error: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Groq API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Groq provider error: {str(e)}")
            raise Exception(f"Groq error: {str(e)}")


class OpenRouterProvider(LLMProvider):
    """Provider pour OpenRouter (accès à tous les modèles: GPT-4, Claude, DeepSeek, Qwen, Kimi, etc.)"""

    def __init__(self, model: str = "openai/gpt-4o"):
        self.api_key = os.getenv("OPEN_ROUTER_API_KEY", "")
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = model

    def is_available(self) -> bool:
        return bool(self.api_key)

    async def generate(self, prompt: str, system: Optional[str] = None) -> str:
        if not self.is_available():
            raise ValueError("OPEN_ROUTER_API_KEY not configured")

        try:
            async with httpx.AsyncClient(timeout=90.0) as client:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://www.iafactoryalgeria.com",
                    "X-Title": "IAFactory Council"
                }

                messages = []
                if system:
                    messages.append({"role": "system", "content": system})
                messages.append({"role": "user", "content": prompt})

                payload = {
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": 2048,
                    "temperature": 0.7
                }

                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )

                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]

        except httpx.HTTPStatusError as e:
            logger.error(f"OpenRouter API error: {e.response.status_code} - {e.response.text}")
            raise Exception(f"OpenRouter API error: {e.response.status_code}")
        except httpx.TimeoutException:
            logger.error("OpenRouter timeout")
            raise Exception("OpenRouter timeout - try again")
        except Exception as e:
            logger.error(f"OpenRouter provider error: {str(e)}")
            raise Exception(f"OpenRouter error: {str(e)}")


# Factory function
def get_provider(name: str) -> LLMProvider:
    """Factory pour créer un provider par son nom"""
    
    # Mapping des noms aux providers et modèles
    provider_mapping = {
        # Anthropic (direct)
        "claude": (ClaudeProvider, {}),
        "claude-opus-4": (ClaudeProvider, {}),
        # OpenAI (direct)
        "chatgpt": (ChatGPTProvider, {"model": "gpt-3.5-turbo"}),
        "gpt-4-turbo": (ChatGPTProvider, {"model": "gpt-4-turbo-preview"}),
        # Google (direct)
        "gemini": (GeminiProvider, {}),
        "gemini-pro": (GeminiProvider, {}),
        # Mistral (direct)
        "mistral-large": (MistralProvider, {}),
        # Perplexity
        "perplexity": (PerplexityProvider, {}),
        
        # === GROQ (ultra-rapide) ===
        "groq-llama": (GroqProvider, {"model": "llama-3.3-70b-versatile"}),
        "groq-mixtral": (GroqProvider, {"model": "mixtral-8x7b-32768"}),
        "groq-gemma": (GroqProvider, {"model": "gemma2-9b-it"}),
        
        # === OPENROUTER (tous les modèles) ===
        # OpenAI via OpenRouter
        "or-gpt4o": (OpenRouterProvider, {"model": "openai/gpt-4o"}),
        "or-gpt4": (OpenRouterProvider, {"model": "openai/gpt-4-turbo"}),
        "or-gpt35": (OpenRouterProvider, {"model": "openai/gpt-3.5-turbo"}),
        # Claude via OpenRouter
        "or-claude": (OpenRouterProvider, {"model": "anthropic/claude-3.5-sonnet"}),
        "or-claude-opus": (OpenRouterProvider, {"model": "anthropic/claude-3-opus"}),
        # DeepSeek
        "deepseek": (OpenRouterProvider, {"model": "deepseek/deepseek-chat"}),
        "deepseek-coder": (OpenRouterProvider, {"model": "deepseek/deepseek-coder"}),
        # Qwen
        "qwen-72b": (OpenRouterProvider, {"model": "qwen/qwen-2.5-72b-instruct"}),
        "qwen-coder": (OpenRouterProvider, {"model": "qwen/qwen-2.5-coder-32b-instruct"}),
        # Kimi (Moonshot)
        "kimi": (OpenRouterProvider, {"model": "moonshotai/moonshot-v1-128k"}),
        # Llama via OpenRouter
        "or-llama": (OpenRouterProvider, {"model": "meta-llama/llama-3.1-70b-instruct"}),
        # Mistral via OpenRouter
        "or-mistral": (OpenRouterProvider, {"model": "mistralai/mistral-large"}),
        # Google via OpenRouter
        "or-gemini": (OpenRouterProvider, {"model": "google/gemini-pro-1.5"}),
        
        # Ollama local models
        "ollama": (OllamaProvider, {"model": "llama3.2:3b"}),
        "llama": (OllamaProvider, {"model": "llama3.2:3b"}),
        "mistral": (OllamaProvider, {"model": "mistral:7b"}),
        "qwen": (OllamaProvider, {"model": "qwen2.5:3b"}),
        "ollama-mistral": (OllamaProvider, {"model": "mistral:7b"}),
        "ollama-qwen": (OllamaProvider, {"model": "qwen2.5:3b"}),
    }

    if name not in provider_mapping:
        raise ValueError(f"Unknown provider: {name}")

    provider_class, kwargs = provider_mapping[name]
    return provider_class(**kwargs) if kwargs else provider_class()


async def test_provider(name: str) -> Dict[str, Any]:
    """Test de connectivité pour un provider"""
    try:
        provider = get_provider(name)

        if not provider.is_available():
            return {
                "provider": name,
                "status": "unavailable",
                "error": "API key not configured or service not accessible"
            }

        test_prompt = "Réponds simplement 'OK' si tu reçois ce message."
        response = await provider.generate(test_prompt)

        return {
            "provider": name,
            "status": "ok",
            "response_preview": response[:100]
        }

    except Exception as e:
        return {
            "provider": name,
            "status": "error",
            "error": str(e)
        }
