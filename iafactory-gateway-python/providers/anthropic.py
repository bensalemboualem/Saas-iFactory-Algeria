# -*- coding: utf-8 -*-
"""
Provider Anthropic Claude
"""
import httpx
import os

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_BASE_URL = "https://api.anthropic.com/v1"

class AnthropicProvider:
    def __init__(self):
        self.api_key = ANTHROPIC_API_KEY
        self.base_url = ANTHROPIC_BASE_URL
    
    async def chat_completion(self, model: str, messages: list, temperature: float = 0.7, max_tokens: int = 1000, stream: bool = False):
        """Appel chat completion Anthropic"""
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
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
                f"{self.base_url}/messages",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()

anthropic_provider = AnthropicProvider()
