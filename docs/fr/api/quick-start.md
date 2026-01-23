# Démarrage Rapide - API

Une API LLM compatible OpenAI pour intégrer facilement l'IA dans vos applications.

➡️ **[Obtenez votre clé API et vos crédits](https://dashboard.iafactory-algeria.com/api)**

## Crédits Inclus

Tous les abonnés à IAFactory Algeria ont des crédits inclus.

| Formule | Starter | Standard | Expert |
|---------|---------|----------|--------|
| **Crédits mensuels** | 2$ | 4$ | 10$ |

Vous pouvez également vous abonner sur la base d'un paiement à l'usage directement depuis les paramètres de l'API.

## Avec l'API IAFactory Directement

Génère une réponse de complétion de chat basée sur votre prompt.

### Python

```python
import requests

url = "https://api.iafactory-algeria.com/v1/chat/completions"
headers = {
    "Authorization": "Bearer VOTRE_CLE_API",
    "Content-Type": "application/json"
}
data = {
    "model": "gpt-4.1",
    "messages": [
        {
            "role": "user",
            "content": "Explique les bases de l'apprentissage automatique"
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
    "Authorization": "Bearer VOTRE_CLE_API",
    "Content-Type": "application/json"
};
const data = {
    model: "gpt-4.1",
    messages: [
        {
            role: "user",
            content: "Explique les bases de l'apprentissage automatique"
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
  -H "Authorization: Bearer VOTRE_CLE_API" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4.1",
    "messages": [
      {
        "role": "user",
        "content": "Explique les bases de l'\''apprentissage automatique"
      }
    ]
  }'
```

## Avec la Bibliothèque OpenAI

```python
import openai

# Configurer le client pour utiliser IAFactory Algeria
openai.api_base = "https://api.iafactory-algeria.com/v1"
openai.api_key = "VOTRE_CLE_API"

response = openai.ChatCompletion.create(
    model="gpt-4.1",
    messages=[
        {"role": "user", "content": "Quels sont les avantages des énergies renouvelables ?"}
    ]
)

print(response.choices[0].message.content)
```

## Format de Réponse

### Réponse Réussie

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
        "content": "Bonjour ! Je vais très bien, merci de demander. Comment puis-je vous aider aujourd'hui ?"
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

### Réponse en Streaming

Quand `stream: true` est défini, les réponses sont retournées sous forme de Server-Sent Events :

```
data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"gpt-4.1","choices":[{"index":0,"delta":{"content":"Bonjour"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"gpt-4.1","choices":[{"index":0,"delta":{"content":"!"},"finish_reason":null}]}

data: [DONE]
```

## Prochaines Étapes

- [Modèles et Tarifs](./models-pricing.md)
- [Codes d'Erreur](./error-codes.md)
- [Paramètres Avancés](./parameters.md)
- [Migration depuis OpenAI](./migration-openai.md)

---

➡️ **[Obtenez votre clé API et vos crédits](https://dashboard.iafactory-algeria.com/api)**
