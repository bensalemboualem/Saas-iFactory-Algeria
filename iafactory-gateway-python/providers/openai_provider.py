import openai
import time
from typing import List
from .base import BaseProvider, Message, LLMResponse

class OpenAIProvider(BaseProvider):
    """Provider for OpenAI models"""
    
    # Pricing per 1M tokens
    PRICING = {
        "gpt-4o": 2.50,
        "gpt-4o-mini": 0.15,
        "gpt-4-turbo": 10.00,
        "gpt-3.5-turbo": 0.50
    }
    
    def __init__(self, api_key: str, model_name: str):
        super().__init__(api_key, model_name)
        self.client = openai.OpenAI(api_key=api_key)
    
    async def generate(
        self, 
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> LLMResponse:
        """Generate completion using OpenAI"""
        start_time = time.time()
        
        # Format messages for OpenAI API
        formatted_messages = self.format_messages(messages)
        
        # Call OpenAI API
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
            provider="openai",
            tokens_used=tokens_used,
            cost=cost,
            latency_ms=latency_ms
        )
    
    def calculate_cost(self, tokens_used: int) -> float:
        """Calculate cost for OpenAI based on pricing"""
        cost_per_1m = self.PRICING.get(self.model_name, 2.50)
        return (tokens_used / 1_000_000) * cost_per_1m
