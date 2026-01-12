# -*- coding: utf-8 -*-
"""
LLM Service via IAFactory Gateway
"""
import httpx

GATEWAY_URL = "http://localhost:3001/api/llm/chat/completions"

async def chat_completion(model: str, messages: list, temperature: float = 0.7, max_tokens: int = 1000):
    """Appel LLM via gateway"""
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            GATEWAY_URL,
            json={
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
        )
        response.raise_for_status()
        return response.json()

def chat_completion_sync(model: str, messages: list, temperature: float = 0.7, max_tokens: int = 1000):
    """Version synchrone"""
    response = httpx.post(
        GATEWAY_URL,
        json={"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens},
        timeout=60.0
    )
    response.raise_for_status()
    return response.json()
