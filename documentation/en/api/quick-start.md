# API Quick Start

Welcome to the IAFactory Algeria API documentation.

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

## Example in Python (requests)
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

## Example in JavaScript (fetch)
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

The following models are currently available via the API:

- gpt-4.1
- claude-3.5-sonnet
- gemini-2.5-pro
- mistral-large
- deepseek-r1

For more details and pricing, see [Models & Pricing](models-pricing.md)

## Example Response
```json
{
  "id": "chatcmpl-123456",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "gpt-4.1",
  "choices": [
    {
      "index": 0,
      "message": {"role": "assistant", "content": "Hello! How can I help you?"},
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 10,
    "total_tokens": 20
  }
}
```

## Useful Resources
- [Response Format](response-format.md)  TODO(AR)
- [Error Codes](error-codes.md)  TODO(AR)
- [FAQ](../faq.md)  TODO(AR)

For any questions, contact support@iafactory.dz
