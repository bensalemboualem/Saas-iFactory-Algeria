# Quick Start - API

An OpenAI-compatible LLM API to easily integrate AI into your applications.

➡️ **[Get your API key and credits](https://dashboard.iafactory-algeria.com/api)**

## Included Credits

All IAFactory Algeria subscribers have included credits.

| Plan | Starter | Standard | Expert |
|------|---------|----------|--------|
| **Monthly Credits** | $2 | $4 | $10 |

You can also subscribe on a pay-as-you-go basis directly from the API settings.

## With IAFactory API Directly

Generates a chat completion response based on your prompt.

### Python

```python
import requests

url = "https://api.iafactory-algeria.com/v1/chat/completions"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}
data = {
    "model": "gpt-4.1",
    "messages": [
        {
            "role": "user",
            "content": "Explain the basics of machine learning"
        }
    ]
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

### JavaScript

```javascript
const url = "https://api.iafactory-algeria.com/v1/chat/completions";
const headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
};
const data = {
    model: "gpt-4.1",
    messages: [
        {
            role: "user",
            content: "Explain the basics of machine learning"
        }
    ]
};

fetch(url, {
    method: "POST",
    headers: headers,
    body: JSON.stringify(data)
})
.then(response => response.json())
.then(data => console.log(data));
```

### cURL

```bash
curl https://api.iafactory-algeria.com/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4.1",
    "messages": [
      {
        "role": "user",
        "content": "Explain the basics of machine learning"
      }
    ]
  }'
```

## With OpenAI Library

```python
import openai

# Configure the client to use IAFactory Algeria
openai.api_base = "https://api.iafactory-algeria.com/v1"
openai.api_key = "YOUR_API_KEY"

response = openai.ChatCompletion.create(
    model="gpt-4.1",
    messages=[
        {"role": "user", "content": "What are the benefits of renewable energy?"}
    ]
)

print(response.choices[0].message.content)
```

## Response Format

### Successful Response

```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "gpt-4.1",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! I'm doing great, thanks for asking. How can I help you today?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 12,
    "completion_tokens": 19,
    "total_tokens": 31
  }
}
```

### Streaming Response

When `stream: true` is set, responses are returned as Server-Sent Events:

```
data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"gpt-4.1","choices":[{"index":0,"delta":{"content":"Hello"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"gpt-4.1","choices":[{"index":0,"delta":{"content":"!"},"finish_reason":null}]}

data: [DONE]
```

## Next Steps

- [Models and Pricing](./models-pricing.md)
- [Error Codes](./error-codes.md)
- [Advanced Parameters](./parameters.md)
- [Migration from OpenAI](./migration-openai.md)

---

➡️ **[Get your API key and credits](https://dashboard.iafactory-algeria.com/api)**
