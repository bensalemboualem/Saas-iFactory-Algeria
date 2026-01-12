import requests
import time
from typing import List
from .base import BaseProvider, Message, LLMResponse

class DeepSeekProvider(BaseProvider):
    """Provider for DeepSeek models (excellent for code)"""

    # Pricing per 1M tokens
    PRICING = {
        "deepseek-chat": 0.14,
        "deepseek-coder": 0.14
    }

    def __init__(self, api_key: str, model_name: str):
        super().__init__(api_key, model_name)
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def generate(  # FIXED: removed async, using requests HTTP
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> LLMResponse:
        """Generate completion using DeepSeek"""
        start_time = time.time()

        # Format messages for DeepSeek API
        formatted_messages = self.format_messages(messages)

        # Prepare request payload
        payload = {
            "model": self.model_name,
            "messages": formatted_messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        # Call DeepSeek API via HTTP (avoids OpenAI SDK 'proxies' issue)
        response = requests.post(
            self.api_url,
            headers=self.headers,
            json=payload,
            timeout=30
        )

        latency_ms = int((time.time() - start_time) * 1000)

        # Check response
        if response.status_code != 200:
            raise Exception(f"DeepSeek API error {response.status_code}: {response.text}")

        data = response.json()

        # Extract response
        content = data["choices"][0]["message"]["content"]
        tokens_used = data["usage"]["total_tokens"]

        # Calculate cost
        cost = self.calculate_cost(tokens_used)

        return LLMResponse(
            content=content,
            model=self.model_name,
            provider="deepseek",
            tokens_used=tokens_used,
            cost=cost,
            latency_ms=latency_ms
        )

    def calculate_cost(self, tokens_used: int) -> float:
        """Calculate cost for DeepSeek based on pricing"""
        cost_per_1m = self.PRICING.get(self.model_name, 0.14)
        return (tokens_used / 1_000_000) * cost_per_1m
