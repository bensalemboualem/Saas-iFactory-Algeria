# -*- coding: utf-8 -*-
import httpx

GATEWAY_URL = "http://localhost:3001/api/llm/chat/completions"

def chat(message: str, model: str = "deepseek-chat"):
    response = httpx.post(
        GATEWAY_URL,
        json={"model": model, "messages": [{"role": "user", "content": message}], "max_tokens": 50},
        timeout=60.0
    )
    return response.json()

if __name__ == "__main__":
    result = chat("Dis bonjour en français", model="deepseek-chat")
    print(result)
