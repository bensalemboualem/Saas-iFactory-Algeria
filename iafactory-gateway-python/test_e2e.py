import httpx

# Test DeepSeek via gateway
print(" Test Gateway  DeepSeek...")

# Crédits avant
r = httpx.get("http://localhost:3001/api/credits/test-user")
before = r.json()["credits"]
print(f"Crédits avant : {before}")

# Appel DeepSeek
body = {
    "model": "deepseek-chat",
    "messages": [{"role": "user", "content": "Réponds OK"}],
    "max_tokens": 5
}
r = httpx.post("http://localhost:3001/api/llm/chat/completions", json=body, timeout=30)
print(f"\nStatus : {r.status_code}")
if r.status_code == 200:
    data = r.json()
    print(f"Réponse : {data['choices'][0]['message']['content']}")
    print(f"Provider : {data.get('_gateway', {}).get('provider')}")
    print(f"Tokens : {data.get('_gateway', {}).get('tokens_debited')}")

# Crédits après
r = httpx.get("http://localhost:3001/api/credits/test-user")
after = r.json()["credits"]
print(f"\nCrédits après : {after}")
print(f"Débités : {before - after} tokens")
