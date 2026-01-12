# -*- coding: utf-8 -*-
import httpx
import os
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
class DeepSeekProvider:
    async def chat_completion(self, model: str, messages: list, temperature: float = 0.7, max_tokens: int = 1000, stream: bool = False):
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post("https://api.deepseek.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
                json={"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens})
            response.raise_for_status()
            return response.json()
deepseek_provider = DeepSeekProvider()
