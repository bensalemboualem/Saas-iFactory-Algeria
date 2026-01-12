# Démarrage rapide API

Bienvenue dans la documentation de l’API IAFactory Algeria.

## Prérequis
- Créez un compte sur la plateforme IAFactory
- Générez une clé API depuis votre espace utilisateur
- Installez un outil HTTP (curl, Postman, etc.)

## Exemple de requête cURL
```bash
curl -X POST https://api.iafactory.dz/v1/chat/completions \
  -H "Authorization: Bearer VOTRE_CLE_API" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4.1",
    "messages": [{"role": "user", "content": "Bonjour IA!"}],
    "max_tokens": 50
  }'
```

## Exemple en Python (requests)
```python
import requests

url = "https://api.iafactory.dz/v1/chat/completions"
headers = {
    "Authorization": "Bearer VOTRE_CLE_API",
    "Content-Type": "application/json"
}
data = {
    "model": "gpt-4.1",
    "messages": [{"role": "user", "content": "Bonjour IA!"}],
    "max_tokens": 50
}
response = requests.post(url, headers=headers, json=data)
print(response.json())
```

## Exemple en JavaScript (fetch)
```js
fetch("https://api.iafactory.dz/v1/chat/completions", {
  method: "POST",
  headers: {
    "Authorization": "Bearer VOTRE_CLE_API",
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    model: "gpt-4.1",
    messages: [{ role: "user", content: "Bonjour IA!" }],
    max_tokens: 50
  })
})
  .then(res => res.json())
  .then(console.log);
```

## Utiliser la bibliothèque OpenAI (compatible)
Vous pouvez utiliser la librairie openai-python en configurant l’URL de base :
```python
import openai
openai.api_key = "VOTRE_CLE_API"
openai.api_base = "https://api.iafactory.dz/v1"
response = openai.ChatCompletion.create(
    model="gpt-4.1",
    messages=[{"role": "user", "content": "Bonjour IA!"}]
)
print(response)
```

## Modèles disponibles (V1)

Les modèles actuellement exposés via l’API :

- gpt-4.1
- claude-3.5-sonnet
- gemini-2.5-pro
- mistral-large
- deepseek-r1

Pour plus de détails et la tarification, voir [Modèles & Tarification](models-pricing.md)

## Réponse attendue
```json
{
  "id": "chatcmpl-123456",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "gpt-4.1",
  "choices": [
    {
      "index": 0,
      "message": {"role": "assistant", "content": "Bonjour! Comment puis-je vous aider?"},
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

## Ressources utiles
- [Format de réponse](response-format.md)  TODO(EN) TODO(AR)
- [Codes d’erreur](error-codes.md)  TODO(EN) TODO(AR)
- [FAQ](../faq.md)  TODO(EN) TODO(AR)

Pour toute question, contactez support@iafactory.dz