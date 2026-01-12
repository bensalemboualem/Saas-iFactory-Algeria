# -*- coding: utf-8 -*-
"""Helper pour appeler gateway depuis n'importe quelle app"""
import httpx

GATEWAY_URL = "http://localhost:3001"

async def call_llm(model: str, messages: list, temperature: float = 0.7, max_tokens: int = 1000):
    """Appel LLM via gateway"""
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{GATEWAY_URL}/api/llm/chat/completions",
            json={
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
        )
        response.raise_for_status()
        return response.json()

def call_llm_sync(model: str, messages: list, temperature: float = 0.7, max_tokens: int = 1000):
    """Version synchrone"""
    import httpx
    response = httpx.post(
        f"{GATEWAY_URL}/api/llm/chat/completions",
        json={"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens},
        timeout=60.0
    )
    response.raise_for_status()
    return response.json()
