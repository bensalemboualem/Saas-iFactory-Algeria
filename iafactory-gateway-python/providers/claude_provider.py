import anthropic
import time
from typing import List
from .base import BaseProvider, Message, LLMResponse

class ClaudeProvider(BaseProvider):
    """Provider for Anthropic Claude models"""
    
    # Pricing per 1M tokens (input/output average for simplicity)
    PRICING = {
        "claude-haiku-4-5-20251001": 0.80,
        "claude-sonnet-4-5-20250929": 3.00,
        "claude-opus-4-1-20250805": 15.00
    }
    
    def __init__(self, api_key: str, model_name: str):
        super().__init__(api_key, model_name)
        self.client = anthropic.Anthropic(api_key=api_key)
    
    async def generate(
        self, 
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> LLMResponse:
        """Generate completion using Claude"""
        start_time = time.time()
        
        # Format messages for Claude API
        formatted_messages = self.format_messages(messages)
        
        # Call Claude API
        response = self.client.messages.create(
            model=self.model_name,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=formatted_messages
        )
        
        latency_ms = int((time.time() - start_time) * 1000)
        
        # Extract response content
        content = response.content[0].text
        
        # Calculate tokens (approximate from response)
        tokens_used = response.usage.input_tokens + response.usage.output_tokens
        
        # Calculate cost
        cost = self.calculate_cost(tokens_used)
        
        return LLMResponse(
            content=content,
            model=self.model_name,
            provider="claude",
            tokens_used=tokens_used,
            cost=cost,
            latency_ms=latency_ms
        )
    
    def calculate_cost(self, tokens_used: int) -> float:
        """Calculate cost for Claude based on pricing"""
        cost_per_1m = self.PRICING.get(self.model_name, 3.00)
        return (tokens_used / 1_000_000) * cost_per_1m
