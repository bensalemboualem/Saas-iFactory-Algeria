import http.client
import json
import time
from typing import List
from .base import BaseProvider, Message, LLMResponse

class GLMProvider(BaseProvider):
    """Provider for GLM-4 (Zhipu AI / ChatGLM)"""

    # Pricing per 1M tokens
    PRICING = {
        "glm-4": 0.10,
        "glm-4-air": 0.001,  # Ultra cheap
        "glm-4-flash": 0.0001  # Nearly free
    }

    def __init__(self, api_key: str, model_name: str):
        super().__init__(api_key, model_name)
        self.api_host = "open.bigmodel.cn"

    async def generate(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> LLMResponse:
        """Generate completion using GLM-4"""
        start_time = time.time()

        # Format messages
        formatted_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model_name,
            "messages": formatted_messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        # Call GLM API
        conn = http.client.HTTPSConnection(self.api_host)
        conn.request(
            "POST",
            "/api/paas/v4/chat/completions",
            body=json.dumps(payload),
            headers=headers
        )

        response = conn.getresponse()
        data = json.loads(response.read().decode())
        conn.close()

        latency_ms = int((time.time() - start_time) * 1000)

        # Extract response
        content = data["choices"][0]["message"]["content"]
        tokens_used = data["usage"]["total_tokens"]

        cost = self.calculate_cost(tokens_used)

        return LLMResponse(
            content=content,
            model=self.model_name,
            provider="glm",
            tokens_used=tokens_used,
            cost=cost,
            latency_ms=latency_ms
        )

    def calculate_cost(self, tokens_used: int) -> float:
        cost_per_1m = self.PRICING.get(self.model_name, 0.10)
        return (tokens_used / 1_000_000) * cost_per_1m
