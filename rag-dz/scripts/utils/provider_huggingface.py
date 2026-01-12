import requests
import time
from typing import List
from .base import BaseProvider, Message, LLMResponse

class HuggingFaceProvider(BaseProvider):
    """Provider for HuggingFace Inference API - 400K+ open-source models"""

    # Pricing per 1M tokens (approximations for popular models)
    PRICING = {
        "meta-llama/Meta-Llama-3-70B-Instruct": 0.50,
        "meta-llama/Meta-Llama-3-8B-Instruct": 0.10,
        "mistralai/Mixtral-8x7B-Instruct-v0.1": 0.40,
        "mistralai/Mistral-7B-Instruct-v0.2": 0.15,
        "google/gemma-7b-it": 0.10,
        "bigscience/bloom": 0.20,
        "tiiuae/falcon-40b-instruct": 0.35,
        "HuggingFaceH4/zephyr-7b-beta": 0.08
    }

    def __init__(self, api_key: str, model_name: str):
        super().__init__(api_key, model_name)
        self.api_url = f"https://api-inference.huggingface.co/models/{model_name}"

    async def generate(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> LLMResponse:
        """Generate completion using HuggingFace Inference API"""
        start_time = time.time()

        # Convert messages to prompt format
        # Most HF chat models expect a specific format
        if messages[0].role == "system":
            prompt = f"{messages[0].content}\n\n"
            chat_messages = messages[1:]
        else:
            prompt = ""
            chat_messages = messages

        for msg in chat_messages:
            if msg.role == "user":
                prompt += f"User: {msg.content}\n"
            elif msg.role == "assistant":
                prompt += f"Assistant: {msg.content}\n"

        prompt += "Assistant:"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "inputs": prompt,
            "parameters": {
                "temperature": temperature,
                "max_new_tokens": max_tokens,
                "return_full_text": False
            }
        }

        # Call HuggingFace Inference API
        response = requests.post(
            self.api_url,
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            raise Exception(f"HuggingFace API error: {response.status_code} - {response.text}")

        data = response.json()

        latency_ms = int((time.time() - start_time) * 1000)

        # Extract response
        if isinstance(data, list) and len(data) > 0:
            content = data[0].get("generated_text", "")
        else:
            content = data.get("generated_text", "")

        # HF doesn't always return token counts, estimate
        tokens_used = len(prompt.split()) + len(content.split())

        cost = self.calculate_cost(tokens_used)

        return LLMResponse(
            content=content.strip(),
            model=self.model_name,
            provider="huggingface",
            tokens_used=tokens_used,
            cost=cost,
            latency_ms=latency_ms
        )

    def calculate_cost(self, tokens_used: int) -> float:
        # Get base model name (without organization)
        model_key = self.model_name
        cost_per_1m = self.PRICING.get(model_key, 0.15)  # Default $0.15
        return (tokens_used / 1_000_000) * cost_per_1m
