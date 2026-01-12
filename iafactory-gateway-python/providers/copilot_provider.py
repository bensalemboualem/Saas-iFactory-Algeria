import openai
import time
from typing import List
from .base import BaseProvider, Message, LLMResponse

class CopilotProvider(BaseProvider):
    """Provider for Microsoft Copilot via Azure OpenAI - Enterprise compliance"""

    # Pricing per 1M tokens (Azure OpenAI pricing)
    PRICING = {
        "gpt-4": 30.00,
        "gpt-4-32k": 60.00,
        "gpt-4-turbo": 10.00,
        "gpt-4o": 5.00,
        "gpt-4o-mini": 0.15,
        "gpt-35-turbo": 0.50,
        "gpt-35-turbo-16k": 1.00,
        "o1-preview": 15.00,
        "o1-mini": 3.00
    }

    def __init__(self, api_key: str, model_name: str, azure_endpoint: str = None):
        super().__init__(api_key, model_name)
        # Azure OpenAI requires endpoint URL
        # Format: https://<resource-name>.openai.azure.com/
        self.azure_endpoint = azure_endpoint or "https://iafactory.openai.azure.com/"

        # Azure OpenAI client
        self.client = openai.AzureOpenAI(
            api_key=api_key,
            azure_endpoint=self.azure_endpoint,
            api_version="2024-08-01-preview"
        )

    async def generate(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> LLMResponse:
        """Generate completion using Microsoft Copilot (Azure OpenAI)"""
        start_time = time.time()

        formatted_messages = self.format_messages(messages)

        # Call Azure OpenAI API
        response = self.client.chat.completions.create(
            model=self.model_name,  # This is the deployment name in Azure
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
            provider="copilot",
            tokens_used=tokens_used,
            cost=cost,
            latency_ms=latency_ms
        )

    def calculate_cost(self, tokens_used: int) -> float:
        cost_per_1m = self.PRICING.get(self.model_name, 5.00)
        return (tokens_used / 1_000_000) * cost_per_1m
