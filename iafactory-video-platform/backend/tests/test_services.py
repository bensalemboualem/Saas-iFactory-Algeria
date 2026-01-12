# -*- coding: utf-8 -*-
import httpx

GATEWAY_URL = "http://localhost:3001/api/llm/chat/completions"

async def call_ai(model: str, prompt: str, max_tokens: int = 500):
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(GATEWAY_URL, json={"model": model, "messages": [{"role": "user", "content": prompt}], "max_tokens": max_tokens})
        response.raise_for_status()
        return response.json()