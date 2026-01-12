import openai
import time
from typing import List
from .base import BaseProvider, Message, LLMResponse

class GitHubModelsProvider(BaseProvider):
    """Provider for GitHub Models Marketplace - Developer ecosystem"""

    # Pricing per 1M tokens (GitHub Models pricing)
    PRICING = {
        "gpt-4o": 2.50,
        "gpt-4o-mini": 0.15,
        "gpt-4-turbo": 10.00,
        "o1-preview": 15.00,
        "o1-mini": 3.00,
        "phi-3-medium-128k": 0.10,
        "phi-3-mini-128k": 0.05,
        "llama-3.1-70b": 0.60,
        "llama-3.1-8b": 0.15,
        "mistral-large-2407": 2.00,
        "mistral-small": 0.20,
        "cohere-command-r-plus": 3.00
    }

    def __init__(self, api_key: str, model_name: str):
        super().__init__(api_key, model_name)
        # GitHub Models uses OpenAI-compatible API
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url="https://models.inference.ai.azure.com"
        )

    async def generate(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> LLMResponse:
        """Generate completion using GitHub Models"""
        start_time = time.time()

        formatted_messages = self.format_messages(messages)

        # Call GitHub Models API (OpenAI-compatible)
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
            provider="github",
            tokens_used=tokens_used,
            cost=cost,
            latency_ms=latency_ms
        )

    def calculate_cost(self, tokens_used: int) -> float:
        cost_per_1m = self.PRICING.get(self.model_name, 0.50)
        return (tokens_used / 1_000_000) * cost_per_1m
