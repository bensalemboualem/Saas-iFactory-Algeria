# -*- coding: utf-8 -*-
import httpx

GATEWAY_URL = "http://localhost:3001/api/llm/chat/completions"

def chat(message: str):
    response = httpx.post(
        GATEWAY_URL,
        json={"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": message}], "max_tokens": 500},
        timeout=60.0
    )
    return response.json()

if __name__ == "__main__":
    result = chat("Bonjour")
    print(result)
