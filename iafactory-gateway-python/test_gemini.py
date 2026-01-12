import asyncio
from dotenv import load_dotenv
load_dotenv()

from providers.gemini import gemini_provider

async def main():
    # Test gemini-pro (pas gemini-1.5-flash)
    resp = await gemini_provider.chat_completion(
        model="gemini-pro",
        messages=[{"role": "user", "content": "Dis bonjour en français"}],
        max_tokens=15
    )
    print(" Gemini OK")
    print(resp.get("choices", [{}])[0].get("message", {}).get("content"))

asyncio.run(main())
