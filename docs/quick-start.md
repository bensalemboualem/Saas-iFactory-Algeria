# Guide de Démarrage Rapide

## Configuration Initiale

### 1. Obtenir votre Clé API

1. Connectez-vous à [IAFactory Algeria Dashboard](https://dashboard.iafactory-algeria.com)
2. Allez dans **Paramètres** → **Clés API**
3. Cliquez sur **Créer une nouvelle clé**
4. Copiez et sécurisez votre clé API

### 2. Configuration de Base

**URL de Base :**
```
https://api.iafactory-algeria.com/v1
```

**En-tête d'Authentification :**
```
Authorization: Bearer VOTRE_CLE_API
```

## Premier Appel API

### Exemple Simple (cURL)

```bash
curl https://api.iafactory-algeria.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer VOTRE_CLE_API" \
  -d '{
    "model": "gpt-4",
    "messages": [
      {
        "role": "user",
        "content": "Bonjour, comment vas-tu?"
      }
    ]
  }'
```

### Réponse

```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "gpt-4",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "Bonjour! Je vais bien, merci. Comment puis-je vous aider aujourd'hui?"
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 13,
    "completion_tokens": 17,
    "total_tokens": 30
  }
}
```

## Intégrations Rapides

### JavaScript/Node.js

```javascript
const fetch = require('node-fetch');

async function chat(message) {
  const response = await fetch('https://api.iafactory-algeria.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer VOTRE_CLE_API'
    },
    body: JSON.stringify({
      model: 'gpt-4',
      messages: [{ role: 'user', content: message }]
    })
  });
  
  const data = await response.json();
  return data.choices[0].message.content;
}

chat('Bonjour!').then(console.log);
```

### Python

```python
import requests

def chat(message):
    response = requests.post(
        'https://api.iafactory-algeria.com/v1/chat/completions',
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer VOTRE_CLE_API'
        },
        json={
            'model': 'gpt-4',
            'messages': [{'role': 'user', 'content': message}]
        }
    )
    return response.json()['choices'][0]['message']['content']

print(chat('Bonjour!'))
```

## Prochaines Étapes

- [Authentification détaillée](./api/authentication.md)
- [Explorer tous les endpoints](./api/endpoints.md)
- [Voir plus d'exemples](./examples/javascript.md)
- [Intégrer avec vos outils](./integrations/n8n.md)
