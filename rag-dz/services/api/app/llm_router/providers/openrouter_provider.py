import openai
import time
from typing import List
from .base import BaseProvider, Message, LLMResponse

class OpenRouterProvider(BaseProvider):
    """Provider for OpenRouter - Universal gateway to 100+ models"""

    # Pricing varies by model routed to
    PRICING = {
        "auto": 1.00,  # Auto-routing
        "anthropic/claude-3-opus": 15.00,
        "openai/gpt-4-turbo": 10.00,
        "google/gemini-pro": 0.50,
        "meta-llama/llama-3-70b": 0.70
    }

    def __init__(self, api_key: str, model_name: str):
        super().__init__(api_key, model_name)
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )

    async def generate(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> LLMResponse:
        """Generate completion using OpenRouter"""
        start_time = time.time()

        formatted_messages = self.format_messages(messages)

        # Call OpenRouter API
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=formatted_messages,
            temperature=temperature,
            max_tokens=max_tokens,
            extra_headers={
                "HTTP-Referer": "https://iafactoryalgeria.com",
                "X-Title": "IAFactory BMAD Pipeline"
            }
        )

        latency_ms = int((time.time() - start_time) * 1000)

        content = response.choices[0].message.content
        tokens_used = response.usage.total_tokens

        cost = self.calculate_cost(tokens_used)

        return LLMResponse(
            content=content,
            model=self.model_name,
            provider="openrouter",
            tokens_used=tokens_used,
            cost=cost,
            latency_ms=latency_ms
        )

    def calculate_cost(self, tokens_used: int) -> float:
        cost_per_1m = self.PRICING.get(self.model_name, 1.00)
        return (tokens_used / 1_000_000) * cost_per_1m
