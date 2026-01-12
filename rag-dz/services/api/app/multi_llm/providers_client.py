"""
Providers Client
================
Wrappers pour appeler les différents providers IA (OpenAI, Anthropic, Groq, Google, etc.)
Les clés API sont TOUJOURS côté serveur, JAMAIS exposées au client.
"""

import os
import time
import logging
from typing import Optional, Tuple, List, Dict, Any
from decimal import Decimal

logger = logging.getLogger(__name__)


# ============================================
# Base Response Type
# ============================================

class LLMResponse:
    """Réponse standardisée d'un appel LLM"""
    def __init__(
        self,
        content: str,
        tokens_input: int,
        tokens_output: int,
        model: str,
        finish_reason: str = "stop",
        latency_ms: int = 0,
        raw_response: Optional[Dict] = None,
    ):
        self.content = content
        self.tokens_input = tokens_input
        self.tokens_output = tokens_output
        self.tokens_total = tokens_input + tokens_output
        self.model = model
        self.finish_reason = finish_reason
        self.latency_ms = latency_ms
        self.raw_response = raw_response


# ============================================
# OpenAI Client
# ============================================

async def call_openai_chat(
    model_code: str,
    messages: List[Dict[str, str]],
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
) -> LLMResponse:
    """
    Appeler l'API OpenAI Chat
    
    Args:
        model_code: Code du modèle (ex: "gpt-4o", "gpt-4o-mini")
        messages: Liste de messages [{role, content}]
        temperature: Créativité (0-2)
        max_tokens: Limite de tokens en sortie
    
    Returns:
        LLMResponse avec le contenu et les métriques
    """
    try:
        from openai import AsyncOpenAI
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not configured")
        
        client = AsyncOpenAI(api_key=api_key)
        
        # Extraire le nom du modèle sans le préfixe provider
        model_name = model_code.replace("openai.", "")
        
        start_time = time.time()
        
        response = await client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            max_completion_tokens=max_tokens,
        )
        
        latency_ms = int((time.time() - start_time) * 1000)
        
        content = response.choices[0].message.content or ""
        usage = response.usage
        
        return LLMResponse(
            content=content,
            tokens_input=usage.prompt_tokens if usage else 0,
            tokens_output=usage.completion_tokens if usage else 0,
            model=response.model,
            finish_reason=response.choices[0].finish_reason or "stop",
            latency_ms=latency_ms,
            raw_response=response.model_dump() if hasattr(response, 'model_dump') else None,
        )
        
    except ImportError:
        logger.error("openai package not installed")
        raise ValueError("OpenAI client not available")
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        raise


# ============================================
# Anthropic Client
# ============================================

async def call_anthropic_chat(
    model_code: str,
    messages: List[Dict[str, str]],
    temperature: float = 0.7,
    max_tokens: Optional[int] = 4096,
) -> LLMResponse:
    """
    Appeler l'API Anthropic Claude
    
    Args:
        model_code: Code du modèle (ex: "claude-3-5-sonnet", "claude-3-opus")
        messages: Liste de messages [{role, content}]
        temperature: Créativité (0-1)
        max_tokens: Limite de tokens en sortie
    
    Returns:
        LLMResponse avec le contenu et les métriques
    """
    try:
        from anthropic import AsyncAnthropic
        
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not configured")
        
        client = AsyncAnthropic(api_key=api_key)
        
        # Extraire le nom du modèle
        model_name = model_code.replace("anthropic.", "")
        
        # Map vers les vrais noms de modèles Anthropic
        model_map = {
            "claude-3-5-sonnet": "claude-sonnet-4-20250514",
            "claude-3-sonnet": "claude-3-sonnet-20240229",
            "claude-3-haiku": "claude-3-haiku-20240307",
            "claude-3-opus": "claude-3-opus-20240229",
        }
        actual_model = model_map.get(model_name, model_name)
        
        # Séparer le system message
        system_msg = None
        chat_messages = []
        
        for msg in messages:
            if msg["role"] == "system":
                system_msg = msg["content"]
            else:
                chat_messages.append(msg)
        
        start_time = time.time()
        
        kwargs = {
            "model": actual_model,
            "messages": chat_messages,
            "max_tokens": max_tokens or 4096,
            "temperature": min(temperature, 1.0),  # Anthropic max 1.0
        }
        
        if system_msg:
            kwargs["system"] = system_msg
        
        response = await client.messages.create(**kwargs)
        
        latency_ms = int((time.time() - start_time) * 1000)
        
        content = response.content[0].text if response.content else ""
        
        return LLMResponse(
            content=content,
            tokens_input=response.usage.input_tokens,
            tokens_output=response.usage.output_tokens,
            model=response.model,
            finish_reason=response.stop_reason or "stop",
            latency_ms=latency_ms,
            raw_response=response.model_dump() if hasattr(response, 'model_dump') else None,
        )
        
    except ImportError:
        logger.error("anthropic package not installed")
        raise ValueError("Anthropic client not available")
    except Exception as e:
        logger.error(f"Anthropic API error: {e}")
        raise


# ============================================
# Groq Client (OpenAI-compatible)
# ============================================

async def call_groq_chat(
    model_code: str,
    messages: List[Dict[str, str]],
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
) -> LLMResponse:
    """
    Appeler l'API Groq (ultra-rapide, open-source models)
    
    Args:
        model_code: Code du modèle (ex: "llama-3.1-70b", "mixtral-8x7b")
        messages: Liste de messages [{role, content}]
        temperature: Créativité (0-2)
        max_tokens: Limite de tokens en sortie
    
    Returns:
        LLMResponse avec le contenu et les métriques
    """
    try:
        from groq import AsyncGroq
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not configured")
        
        client = AsyncGroq(api_key=api_key)
        
        # Extraire le nom du modèle
        model_name = model_code.replace("groq.", "")
        
        # Map vers les vrais noms Groq
        model_map = {
            "llama-3.1-70b": "llama-3.1-70b-versatile",
            "llama-3.1-8b": "llama-3.1-8b-instant",
            "mixtral-8x7b": "mixtral-8x7b-32768",
            "gemma2-9b": "gemma2-9b-it",
        }
        actual_model = model_map.get(model_name, model_name)
        
        start_time = time.time()
        
        response = await client.chat.completions.create(
            model=actual_model,
            messages=messages,
            temperature=temperature,
            max_completion_tokens=max_tokens,
        )
        
        latency_ms = int((time.time() - start_time) * 1000)
        
        content = response.choices[0].message.content or ""
        usage = response.usage
        
        return LLMResponse(
            content=content,
            tokens_input=usage.prompt_tokens if usage else 0,
            tokens_output=usage.completion_tokens if usage else 0,
            model=response.model,
            finish_reason=response.choices[0].finish_reason or "stop",
            latency_ms=latency_ms,
            raw_response=response.model_dump() if hasattr(response, 'model_dump') else None,
        )
        
    except ImportError:
        logger.error("groq package not installed")
        raise ValueError("Groq client not available")
    except Exception as e:
        logger.error(f"Groq API error: {e}")
        raise


# ============================================
# Google Gemini Client
# ============================================

async def call_google_chat(
    model_code: str,
    messages: List[Dict[str, str]],
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
) -> LLMResponse:
    """
    Appeler l'API Google Gemini
    
    Args:
        model_code: Code du modèle (ex: "gemini-1.5-pro", "gemini-1.5-flash")
        messages: Liste de messages [{role, content}]
        temperature: Créativité (0-2)
        max_tokens: Limite de tokens en sortie
    
    Returns:
        LLMResponse avec le contenu et les métriques
    """
    try:
        import google.generativeai as genai
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not configured")
        
        genai.configure(api_key=api_key)
        
        # Extraire le nom du modèle
        model_name = model_code.replace("google.", "")
        
        # Map vers les vrais noms Google
        model_map = {
            "gemini-1.5-pro": "gemini-1.5-pro",
            "gemini-1.5-flash": "gemini-1.5-flash",
            "gemini-pro": "gemini-pro",
        }
        actual_model = model_map.get(model_name, model_name)
        
        model = genai.GenerativeModel(actual_model)
        
        # Convertir les messages au format Gemini
        # Gemini utilise un format différent
        chat_history = []
        system_instruction = None
        
        for msg in messages:
            if msg["role"] == "system":
                system_instruction = msg["content"]
            elif msg["role"] == "user":
                chat_history.append({"role": "user", "parts": [msg["content"]]})
            elif msg["role"] == "assistant":
                chat_history.append({"role": "model", "parts": [msg["content"]]})
        
        start_time = time.time()
        
        # Démarrer le chat
        chat = model.start_chat(history=chat_history[:-1] if len(chat_history) > 1 else [])
        
        # Dernier message utilisateur
        last_user_msg = chat_history[-1]["parts"][0] if chat_history else ""
        if system_instruction:
            last_user_msg = f"{system_instruction}\n\n{last_user_msg}"
        
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        )
        
        response = await chat.send_message_async(
            last_user_msg,
            generation_config=generation_config,
        )
        
        latency_ms = int((time.time() - start_time) * 1000)
        
        content = response.text if response.text else ""
        
        # Estimation des tokens (Gemini ne donne pas toujours les métriques)
        tokens_input = len(last_user_msg.split()) * 1.3  # Approximation
        tokens_output = len(content.split()) * 1.3
        
        return LLMResponse(
            content=content,
            tokens_input=int(tokens_input),
            tokens_output=int(tokens_output),
            model=actual_model,
            finish_reason="stop",
            latency_ms=latency_ms,
        )
        
    except ImportError:
        logger.error("google-generativeai package not installed")
        raise ValueError("Google Gemini client not available")
    except Exception as e:
        logger.error(f"Google API error: {e}")
        raise


# ============================================
# Mistral Client
# ============================================

async def call_mistral_chat(
    model_code: str,
    messages: List[Dict[str, str]],
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
) -> LLMResponse:
    """
    Appeler l'API Mistral AI
    
    Args:
        model_code: Code du modèle (ex: "mistral-large", "mistral-small")
        messages: Liste de messages [{role, content}]
        temperature: Créativité (0-1)
        max_tokens: Limite de tokens en sortie
    
    Returns:
        LLMResponse avec le contenu et les métriques
    """
    try:
        from mistralai import Mistral
        
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY not configured")
        
        client = Mistral(api_key=api_key)
        
        # Extraire le nom du modèle
        model_name = model_code.replace("mistral.", "")
        
        # Map vers les vrais noms Mistral
        model_map = {
            "mistral-large": "mistral-large-latest",
            "mistral-small": "mistral-small-latest",
            "mistral-medium": "mistral-medium-latest",
            "codestral": "codestral-latest",
        }
        actual_model = model_map.get(model_name, model_name)
        
        start_time = time.time()
        
        response = await client.chat.complete_async(
            model=actual_model,
            messages=messages,
            temperature=min(temperature, 1.0),
            max_completion_tokens=max_tokens,
        )
        
        latency_ms = int((time.time() - start_time) * 1000)
        
        content = response.choices[0].message.content or ""
        usage = response.usage
        
        return LLMResponse(
            content=content,
            tokens_input=usage.prompt_tokens if usage else 0,
            tokens_output=usage.completion_tokens if usage else 0,
            model=response.model,
            finish_reason=response.choices[0].finish_reason or "stop",
            latency_ms=latency_ms,
        )
        
    except ImportError:
        logger.error("mistralai package not installed")
        raise ValueError("Mistral client not available")
    except Exception as e:
        logger.error(f"Mistral API error: {e}")
        raise


# ============================================
# OpenRouter Client (Accès à tous les modèles)
# ============================================

async def call_openrouter_chat(
    model_code: str,
    messages: List[Dict[str, str]],
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
) -> LLMResponse:
    """
    Appeler l'API OpenRouter (gateway vers tous les modèles)
    
    Args:
        model_code: Code du modèle (ex: "openai/gpt-4", "anthropic/claude-3-opus")
        messages: Liste de messages [{role, content}]
        temperature: Créativité (0-2)
        max_tokens: Limite de tokens en sortie
    
    Returns:
        LLMResponse avec le contenu et les métriques
    """
    try:
        import httpx
        
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not configured")
        
        # Extraire le nom du modèle
        model_name = model_code.replace("openrouter.", "")
        
        start_time = time.time()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "HTTP-Referer": "https://iafactory.dz",
                    "X-Title": "IAFactory DZ",
                },
                json={
                    "model": model_name,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                },
                timeout=120.0,
            )
            
            response.raise_for_status()
            data = response.json()
        
        latency_ms = int((time.time() - start_time) * 1000)
        
        content = data["choices"][0]["message"]["content"] or ""
        usage = data.get("usage", {})
        
        return LLMResponse(
            content=content,
            tokens_input=usage.get("prompt_tokens", 0),
            tokens_output=usage.get("completion_tokens", 0),
            model=data.get("model", model_name),
            finish_reason=data["choices"][0].get("finish_reason", "stop"),
            latency_ms=latency_ms,
            raw_response=data,
        )
        
    except ImportError:
        logger.error("httpx package not installed")
        raise ValueError("HTTP client not available")
    except Exception as e:
        logger.error(f"OpenRouter API error: {e}")
        raise


# ============================================
# Provider Router
# ============================================

from .multi_llm_models import LLMProviderType

PROVIDER_HANDLERS = {
    LLMProviderType.OPENAI: call_openai_chat,
    LLMProviderType.ANTHROPIC: call_anthropic_chat,
    LLMProviderType.GROQ: call_groq_chat,
    LLMProviderType.GOOGLE: call_google_chat,
    LLMProviderType.MISTRAL: call_mistral_chat,
    LLMProviderType.OPENROUTER: call_openrouter_chat,
}


def get_provider_from_model_code(model_code: str) -> LLMProviderType:
    """Extraire le provider depuis le code modèle"""
    if "." in model_code:
        provider_name = model_code.split(".")[0]
        try:
            return LLMProviderType(provider_name)
        except ValueError:
            pass
    
    # Fallback: deviner le provider
    if "gpt" in model_code.lower() or "o1" in model_code.lower():
        return LLMProviderType.OPENAI
    elif "claude" in model_code.lower():
        return LLMProviderType.ANTHROPIC
    elif "llama" in model_code.lower() or "mixtral" in model_code.lower():
        return LLMProviderType.GROQ
    elif "gemini" in model_code.lower():
        return LLMProviderType.GOOGLE
    elif "mistral" in model_code.lower():
        return LLMProviderType.MISTRAL
    
    raise ValueError(f"Unknown provider for model: {model_code}")


async def call_llm(
    model_code: str,
    messages: List[Dict[str, str]],
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
) -> LLMResponse:
    """
    Appeler le bon provider selon le code modèle
    
    Args:
        model_code: Code complet (ex: "openai.gpt-4o", "groq.llama-3.1-70b")
        messages: Liste de messages
        temperature: Créativité
        max_tokens: Limite tokens
    
    Returns:
        LLMResponse standardisée
    """
    provider = get_provider_from_model_code(model_code)
    handler = PROVIDER_HANDLERS.get(provider)
    
    if not handler:
        raise ValueError(f"No handler for provider: {provider}")
    
    return await handler(
        model_code=model_code,
        messages=messages,
        temperature=temperature,
        max_completion_tokens=max_tokens,
    )
