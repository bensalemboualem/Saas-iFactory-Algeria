# API Quick Start

## Prerequisites
- Create an account on the IAFactory platform
- Generate an API key from your user dashboard
- Install an HTTP tool (curl, Postman, etc.)

## Example cURL Request
```bash
curl -X POST https://api.iafactory.dz/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4.1",
    "messages": [{"role": "user", "content": "Hello AI!"}],
    "max_tokens": 50
  }'
```

## Python Example (requests)
```python
import requests

url = "https://api.iafactory.dz/v1/chat/completions"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}
data = {
    "model": "gpt-4.1",
    "messages": [{"role": "user", "content": "Hello AI!"}],
    "max_tokens": 50
}
response = requests.post(url, headers=headers, json=data)
print(response.json())
```

## JavaScript Example (fetch)
```js
fetch("https://api.iafactory.dz/v1/chat/completions", {
  method: "POST",
  headers: {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    model: "gpt-4.1",
    messages: [{ role: "user", content: "Hello AI!" }],
    max_tokens: 50
  })
})
  .then(res => res.json())
  .then(console.log);
```

## Using the OpenAI Library (compatible)
You can use the openai-python library by configuring the base URL:
```python
import openai
openai.api_key = "YOUR_API_KEY"
openai.api_base = "https://api.iafactory.dz/v1"
response = openai.ChatCompletion.create(
    model="gpt-4.1",
    messages=[{"role": "user", "content": "Hello AI!"}]
)
print(response)
```

## Available Models (V1)
- gpt-4.1
- claude-3.5-sonnet
- gemini-2.5-pro
- mistral-large
- deepseek-r1

TODO(AR): Traduction en arabe à faire.
