import openai
import time
from typing import List
from .base import BaseProvider, Message, LLMResponse

class PerplexityProvider(BaseProvider):
    """Provider for Perplexity AI - Web-connected search + LLM"""

    # Pricing per 1M tokens
    PRICING = {
        "sonar-small-chat": 0.20,
        "sonar-small-online": 0.20,
        "sonar-medium-chat": 0.60,
        "sonar-medium-online": 0.60
    }

    def __init__(self, api_key: str, model_name: str):
        super().__init__(api_key, model_name)
        # Perplexity uses OpenAI-compatible API
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.perplexity.ai"
        )

    async def generate(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> LLMResponse:
        """Generate completion using Perplexity (with optional web search)"""
        start_time = time.time()

        formatted_messages = self.format_messages(messages)

        # Call Perplexity API
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=formatted_messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

        latency_ms = int((time.time() - start_time) * 1000)

        content = response.choices[0].message.content
        tokens_used = response.usage.total_tokens

        cost = self.calculate_cost(tokens_used)

        return LLMResponse(
            content=content,
            model=self.model_name,
            provider="perplexity",
            tokens_used=tokens_used,
            cost=cost,
            latency_ms=latency_ms
        )

    def calculate_cost(self, tokens_used: int) -> float:
        cost_per_1m = self.PRICING.get(self.model_name, 0.20)
        return (tokens_used / 1_000_000) * cost_per_1m
