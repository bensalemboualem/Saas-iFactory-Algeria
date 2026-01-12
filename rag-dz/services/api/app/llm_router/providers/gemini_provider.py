import google.generativeai as genai
import time
from typing import List
from .base import BaseProvider, Message, LLMResponse

class GeminiProvider(BaseProvider):
    """Provider for Google Gemini models"""

    # Pricing per 1M tokens
    PRICING = {
        "gemini-2.0-flash": 0.10,
        "gemini-pro": 0.50,
        "gemini-ultra": 2.00
    }

    def __init__(self, api_key: str, model_name: str):
        super().__init__(api_key, model_name)
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    async def generate(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> LLMResponse:
        """Generate completion using Gemini"""
        start_time = time.time()

        # Gemini uses a chat format - convert messages
        chat = self.model.start_chat(history=[])

        # Build conversation from messages
        for msg in messages[:-1]:  # All but last
            if msg.role == "user":
                chat.send_message(msg.content)

        # Send final user message
        last_message = messages[-1].content
        response = chat.send_message(
            last_message,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens
            )
        )

        latency_ms = int((time.time() - start_time) * 1000)

        # Extract response
        content = response.text

        # Estimate tokens (Gemini doesn't always return token count)
        tokens_used = len(content.split()) * 1.3  # Rough estimate
        tokens_used = int(tokens_used)

        # Calculate cost
        cost = self.calculate_cost(tokens_used)

        return LLMResponse(
            content=content,
            model=self.model_name,
            provider="gemini",
            tokens_used=tokens_used,
            cost=cost,
            latency_ms=latency_ms
        )

    def calculate_cost(self, tokens_used: int) -> float:
        """Calculate cost for Gemini based on pricing"""
        cost_per_1m = self.PRICING.get(self.model_name, 0.50)
        return (tokens_used / 1_000_000) * cost_per_1m
