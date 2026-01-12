# -*- coding: utf-8 -*-
import httpx
import os

class GeminiProvider:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")

    async def chat_completion(
        self,
        model: str,
        messages: list,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        stream: bool = False,
    ):
        contents = []
        for m in messages:
            role = "user" if m.get("role") in ["user", "system"] else "model"
            contents.append({
                "role": role,
                "parts": [{"text": m.get("content", "")}],
            })

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
            },
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent",
                params={"key": self.api_key},
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

            return {
                "choices": [{
                    "message": {
                        "role": "assistant",
                        "content": data["candidates"][0]["content"]["parts"][0]["text"],
                    },
                    "finish_reason": "stop",
                }],
                "usage": data.get("usageMetadata", {}),
            }

gemini_provider = GeminiProvider()
