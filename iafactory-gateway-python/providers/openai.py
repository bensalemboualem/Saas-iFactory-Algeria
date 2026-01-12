# -*- coding: utf-8 -*-
"""
Provider OpenAI
"""
import httpx
import os
from typing import AsyncGenerator

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = "https://api.openai.com/v1"

class OpenAIProvider:
    def __init__(self):
        self.api_key = OPENAI_API_KEY
        self.base_url = OPENAI_BASE_URL
    
    async def chat_completion(self, model: str, messages: list, temperature: float = 0.7, max_tokens: int = 1000, stream: bool = False):
        """Appel chat completion OpenAI"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()

openai_provider = OpenAIProvider()
