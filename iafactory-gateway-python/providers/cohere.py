# -*- coding: utf-8 -*-
import httpx
import os
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")
class CohereProvider:
    async def chat_completion(self, model: str, messages: list, temperature: float = 0.7, max_tokens: int = 1000, stream: bool = False):
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post("https://api.cohere.ai/v1/chat",
                headers={"Authorization": f"Bearer {COHERE_API_KEY}"},
                json={"model": model, "message": messages[-1]["content"], "temperature": temperature, "max_tokens": max_tokens})
            response.raise_for_status()
            return response.json()
cohere_provider = CohereProvider()
