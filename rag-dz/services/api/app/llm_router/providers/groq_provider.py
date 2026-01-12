from groq import Groq
import time
from typing import List
from .base import BaseProvider, Message, LLMResponse

class GroqProvider(BaseProvider):
    """Provider for Groq ultra-fast inference"""

    # Pricing per 1M tokens (UPDATED - removed deprecated models)
    PRICING = {
        "llama-3.3-70b-versatile": 0.59,  # NEW - tested working!
        "llama-guard-3-8b": 0.20,
        "llama3-70b-8192": 0.59,
        "llama3-8b-8192": 0.05,
        "gemma-7b-it": 0.07,
        "gemma2-9b-it": 0.20
    }

    def __init__(self, api_key: str, model_name: str):
        super().__init__(api_key, model_name)
        self.client = Groq(api_key=api_key)

    def generate(  # FIXED: removed async
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> LLMResponse:
        """Generate completion using Groq (ultra-fast)"""
        start_time = time.time()

        # Format messages for Groq API
        formatted_messages = self.format_messages(messages)

        # Call Groq API (synchronous - Groq is so fast async not needed)
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=formatted_messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

        latency_ms = int((time.time() - start_time) * 1000)

        # Extract response
        content = response.choices[0].message.content
        tokens_used = response.usage.total_tokens

        # Calculate cost
        cost = self.calculate_cost(tokens_used)

        return LLMResponse(
            content=content,
            model=self.model_name,
            provider="groq",
            tokens_used=tokens_used,
            cost=cost,
            latency_ms=latency_ms
        )

    def calculate_cost(self, tokens_used: int) -> float:
        """Calculate cost for Groq based on pricing"""
        cost_per_1m = self.PRICING.get(self.model_name, 0.59)
        return (tokens_used / 1_000_000) * cost_per_1m
