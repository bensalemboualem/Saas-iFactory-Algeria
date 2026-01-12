"""
Proxy LLM avec compteur de tokens et déduction automatique
Intercepte les appels vers OpenAI, Groq, Anthropic, Google
"""
import logging
import time
import os
from typing import Dict, Any, Optional, Callable
from functools import wraps

from . import repository as tokens_repo

logger = logging.getLogger(__name__)


class InsufficientTokensError(Exception):
    """Levée quand le solde tokens est insuffisant"""
    def __init__(self, required: int, balance: int):
        self.required = required
        self.balance = balance
        super().__init__(
            f"Solde insuffisant: {balance} tokens disponibles, {required} requis. "
            "Rechargez votre compte avec un code licence."
        )


def get_api_keys_from_env() -> Dict[str, Optional[str]]:
    """
    Récupère les clés API depuis les variables d'environnement

    Returns:
        Dict avec openai_key, groq_key, anthropic_key, google_key

    Sécurité: Les clés ne sont jamais stockées en dur dans le code
    """
    return {
        "openai_key": os.getenv("OPENAI_API_KEY"),
        "groq_key": os.getenv("GROQ_API_KEY"),
        "anthropic_key": os.getenv("ANTHROPIC_API_KEY"),
        "google_key": os.getenv("GOOGLE_AI_KEY"),
    }


def check_token_balance(tenant_id: str, estimated_tokens: int = 500) -> bool:
    """
    Vérifie si le tenant a assez de tokens AVANT l'appel LLM

    Args:
        tenant_id: UUID du tenant
        estimated_tokens: Estimation tokens requis (sécurité)

    Returns:
        True si solde suffisant

    Raises:
        InsufficientTokensError si solde insuffisant
    """
    balance = tokens_repo.get_balance(tenant_id)

    if balance["balance_tokens"] < estimated_tokens:
        raise InsufficientTokensError(
            required=estimated_tokens,
            balance=balance["balance_tokens"]
        )

    return True


def deduct_after_llm_call(
    tenant_id: str,
    provider: str,
    model: str,
    tokens_input: int,
    tokens_output: int,
    latency_ms: Optional[int] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Déduire tokens APRÈS un appel LLM réussi

    Args:
        tenant_id: UUID du tenant
        provider: Provider (openai, groq, anthropic, google)
        model: Modèle utilisé (gpt-4o, llama-3.3-70b, claude-3.5-sonnet)
        tokens_input: Tokens consommés input (prompt)
        tokens_output: Tokens générés output (completion)
        latency_ms: Latence de l'appel (ms)
        metadata: Métadonnées additionnelles

    Returns:
        Résultat de la déduction avec new_balance

    Raises:
        InsufficientTokensError si solde insuffisant (rare cas race condition)
    """
    meta = metadata or {}
    if latency_ms:
        meta["latency_ms"] = latency_ms

    result = tokens_repo.deduct_tokens_for_llm(
        tenant_id=tenant_id,
        provider=provider,
        model=model,
        tokens_input=tokens_input,
        tokens_output=tokens_output,
        metadata=meta
    )

    if not result.get("success"):
        raise InsufficientTokensError(
            required=tokens_input + tokens_output,
            balance=result.get("balance", 0)
        )

    return result


def with_token_tracking(provider: str, model: str):
    """
    Décorateur pour tracker automatiquement la consommation tokens

    Usage:
        @with_token_tracking(provider="openai", model="gpt-4o")
        def call_openai(tenant_id: str, prompt: str) -> dict:
            # Votre appel LLM ici
            response = client.chat.completions.create(...)
            return {
                "text": response.choices[0].message.content,
                "tokens_input": response.usage.prompt_tokens,
                "tokens_output": response.usage.completion_tokens,
            }

    Le décorateur:
    1. Vérifie le solde AVANT l'appel
    2. Exécute la fonction
    3. Déduit les tokens APRÈS basé sur response["tokens_input/output"]
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, tenant_id: str, **kwargs):
            # 1. Vérifier solde avant (estimation 500 tokens)
            check_token_balance(tenant_id, estimated_tokens=500)

            # 2. Exécuter appel LLM
            start_time = time.time()
            response = func(*args, tenant_id=tenant_id, **kwargs)
            latency_ms = int((time.time() - start_time) * 1000)

            # 3. Déduire tokens après
            if isinstance(response, dict) and "tokens_input" in response:
                deduct_after_llm_call(
                    tenant_id=tenant_id,
                    provider=provider,
                    model=model,
                    tokens_input=response.get("tokens_input", 0),
                    tokens_output=response.get("tokens_output", 0),
                    latency_ms=latency_ms,
                    metadata={"function": func.__name__}
                )

            return response

        return wrapper
    return decorator


# ============================================================
# Helpers pour intégration facile
# ============================================================

def proxy_openai_call(
    tenant_id: str,
    model: str,
    messages: list,
    **kwargs
) -> Dict[str, Any]:
    """
    Appel OpenAI avec déduction automatique tokens

    Args:
        tenant_id: UUID du tenant
        model: Modèle OpenAI (gpt-4o, gpt-4o-mini, etc.)
        messages: Messages chat
        **kwargs: Paramètres additionnels (temperature, max_tokens, etc.)

    Returns:
        Dict avec text, tokens_input, tokens_output

    Raises:
        InsufficientTokensError si solde insuffisant
    """
    from openai import OpenAI

    # 1. Vérifier solde
    check_token_balance(tenant_id)

    # 2. Appel OpenAI
    api_key = get_api_keys_from_env()["openai_key"]
    if not api_key:
        raise ValueError("OPENAI_API_KEY non configurée dans .env")

    client = OpenAI(api_key=api_key)

    start_time = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        **kwargs
    )
    latency_ms = int((time.time() - start_time) * 1000)

    # 3. Déduire tokens
    deduct_after_llm_call(
        tenant_id=tenant_id,
        provider="openai",
        model=model,
        tokens_input=response.usage.prompt_tokens,
        tokens_output=response.usage.completion_tokens,
        latency_ms=latency_ms
    )

    return {
        "text": response.choices[0].message.content,
        "tokens_input": response.usage.prompt_tokens,
        "tokens_output": response.usage.completion_tokens,
        "model": model,
        "latency_ms": latency_ms,
    }


def proxy_groq_call(
    tenant_id: str,
    model: str,
    messages: list,
    **kwargs
) -> Dict[str, Any]:
    """
    Appel Groq avec déduction automatique tokens

    Args:
        tenant_id: UUID du tenant
        model: Modèle Groq (llama-3.3-70b-versatile, mixtral-8x7b-32768, etc.)
        messages: Messages chat
        **kwargs: Paramètres additionnels

    Returns:
        Dict avec text, tokens_input, tokens_output

    Raises:
        InsufficientTokensError si solde insuffisant
    """
    from groq import Groq

    # 1. Vérifier solde
    check_token_balance(tenant_id)

    # 2. Appel Groq
    api_key = get_api_keys_from_env()["groq_key"]
    if not api_key:
        raise ValueError("GROQ_API_KEY non configurée dans .env")

    client = Groq(api_key=api_key)

    start_time = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        **kwargs
    )
    latency_ms = int((time.time() - start_time) * 1000)

    # 3. Déduire tokens
    deduct_after_llm_call(
        tenant_id=tenant_id,
        provider="groq",
        model=model,
        tokens_input=response.usage.prompt_tokens,
        tokens_output=response.usage.completion_tokens,
        latency_ms=latency_ms
    )

    return {
        "text": response.choices[0].message.content,
        "tokens_input": response.usage.prompt_tokens,
        "tokens_output": response.usage.completion_tokens,
        "model": model,
        "latency_ms": latency_ms,
    }


logger.info("🔥 LLM Proxy avec Token Tracking initialisé")
logger.info("   Providers: OpenAI, Groq (Anthropic/Google à venir)")
logger.info("   Isolation: Multi-tenant via RLS")
