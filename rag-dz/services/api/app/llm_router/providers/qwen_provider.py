import http.client
import json
import time
from typing import List
from .base import BaseProvider, Message, LLMResponse

class QwenProvider(BaseProvider):
    """Provider for Alibaba Qwen (通义千问) models via DashScope API"""

    # Pricing per 1M tokens
    PRICING = {
        "qwen-turbo": 0.08,      # Ultra économique
        "qwen-plus": 0.40,       # Standard
        "qwen-max": 1.20,        # Premium
        "qwen-max-longcontext": 1.20  # Long context
    }

    def __init__(self, api_key: str, model_name: str):
        super().__init__(api_key, model_name)
        self.api_host = "dashscope.aliyuncs.com"

    async def generate(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> LLMResponse:
        """Generate completion using Qwen"""
        start_time = time.time()

        # Format messages for Qwen API
        formatted_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

        # Prepare request
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model_name,
            "input": {
                "messages": formatted_messages
            },
            "parameters": {
                "temperature": temperature,
                "max_tokens": max_tokens,
                "result_format": "message"
            }
        }

        # Call Qwen API
        conn = http.client.HTTPSConnection(self.api_host)
        conn.request(
            "POST",
            "/api/v1/services/aigc/text-generation/generation",
            body=json.dumps(payload),
            headers=headers
        )

        response = conn.getresponse()
        data = json.loads(response.read().decode())
        conn.close()

        latency_ms = int((time.time() - start_time) * 1000)

        # Extract response
        if data.get("output"):
            content = data["output"]["choices"][0]["message"]["content"]
            usage = data.get("usage", {})
            tokens_used = usage.get("total_tokens", 1000)
        else:
            raise Exception(f"Qwen API error: {data.get('message', 'Unknown error')}")

        # Calculate cost
        cost = self.calculate_cost(tokens_used)

        return LLMResponse(
            content=content,
            model=self.model_name,
            provider="qwen",
            tokens_used=tokens_used,
            cost=cost,
            latency_ms=latency_ms
        )

    def calculate_cost(self, tokens_used: int) -> float:
        """Calculate cost for Qwen based on pricing"""
        cost_per_1m = self.PRICING.get(self.model_name, 0.40)
        return (tokens_used / 1_000_000) * cost_per_1m
