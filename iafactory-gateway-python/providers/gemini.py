# -*- coding: utf-8 -*-
import httpx
import os
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
class GeminiProvider:
    async def chat_completion(self, model: str, messages: list, temperature: float = 0.7, max_tokens: int = 1000, stream: bool = False):
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={GEMINI_API_KEY}",
                json={"contents": [{"parts": [{"text": m["content"]} for m in messages]}]})
            response.raise_for_status()
            return response.json()
gemini_provider = GeminiProvider()
