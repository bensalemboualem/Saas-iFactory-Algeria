import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

from providers.gemini import gemini_provider
from providers.deepseek import deepseek_provider

async def main():
    print("Env DEEPSEEK_API_KEY prefix:", os.getenv("DEEPSEEK_API_KEY", "")[:10])
    print("Env GEMINI_API_KEY prefix:", os.getenv("GEMINI_API_KEY", "")[:10])

    print("\nTest DeepSeek...")
    try:
        resp = await deepseek_provider.chat_completion(
            model="deepseek-chat",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10,
        )
        print("DeepSeek OK")
        print(resp.get("choices", [{}])[0].get("message", {}).get("content"))
    except Exception as e:
        print(f"DeepSeek FAIL: {str(e)[:200]}")

    print("\nTest Gemini...")
    try:
        resp = await gemini_provider.chat_completion(
            model="gemini-1.5-flash",
            messages=[{"role": "user", "content": "Bonjour"}],
            max_tokens=10,
        )
        print("Gemini OK")
        print(resp.get("choices", [{}])[0].get("message", {}).get("content"))
    except Exception as e:
        print(f"Gemini FAIL: {str(e)[:200]}")

asyncio.run(main())
