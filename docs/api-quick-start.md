# Guide de Démarrage Rapide - API IAFactory Algeria

## Configuration de Base

### URL de Base
```
https://api.iafactory-algeria.com/v1
```

### Authentification
Utilisez votre clé API dans l'en-tête `Authorization` :
```
Authorization: Bearer VOTRE_CLE_API
```

## Exemples d'Intégration

### 1. cURL (Ligne de commande)

```bash
curl https://api.iafactory-algeria.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer VOTRE_CLE_API" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Bonjour!"}]
  }'
```

### 2. JavaScript/TypeScript (Node.js)

```typescript
const response = await fetch('https://api.iafactory-algeria.com/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer VOTRE_CLE_API'
  },
  body: JSON.stringify({
    model: 'gpt-4',
    messages: [{ role: 'user', content: 'Bonjour!' }]
  })
});

const data = await response.json();
console.log(data.choices[0].message.content);
```

### 3. Python

```python
import requests

response = requests.post(
    'https://api.iafactory-algeria.com/v1/chat/completions',
    headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer VOTRE_CLE_API'
    },
    json={
        'model': 'gpt-4',
        'messages': [{'role': 'user', 'content': 'Bonjour!'}]
    }
)

print(response.json()['choices'][0]['message']['content'])
```

### 4. n8n

1. Ajoutez un nœud **HTTP Request**
2. Configurez :
   - **Method** : POST
   - **URL** : `https://api.iafactory-algeria.com/v1/chat/completions`
   - **Authentication** : Header Auth
     - **Name** : Authorization
     - **Value** : `Bearer VOTRE_CLE_API`
   - **Body** :
   ```json
   {
     "model": "gpt-4",
     "messages": [{"role": "user", "content": "Bonjour!"}]
   }
   ```

### 5. VS Code / Cline

Créez un fichier `.env` :
```
IAFACTORY_API_KEY=votre_cle_api
IAFACTORY_API_URL=https://api.iafactory-algeria.com/v1
```

Configuration dans `settings.json` :
```json
{
  "cline.apiProvider": "openai-compatible",
  "cline.apiUrl": "https://api.iafactory-algeria.com/v1",
  "cline.apiKey": "VOTRE_CLE_API"
}
```

### 6. Make (Integromat)

1. Créez un nouveau scénario
2. Ajoutez un module **HTTP > Make a request**
3. Configurez :
   - **URL** : `https://api.iafactory-algeria.com/v1/chat/completions`
   - **Method** : POST
   - **Headers** :
     - `Content-Type`: `application/json`
     - `Authorization`: `Bearer VOTRE_CLE_API`
   - **Body** :
   ```json
   {
     "model": "gpt-4",
     "messages": [{"role": "user", "content": "{{1.message}}"}]
   }
   ```

## Endpoints Disponibles

### Chat Completions
```
POST /v1/chat/completions
```

### Models
```
GET /v1/models
```

### Embeddings
```
POST /v1/embeddings
```

## Codes de Réponse

- `200` : Succès
- `400` : Requête invalide
- `401` : Non autorisé (clé API invalide)
- `429` : Limite de taux dépassée
- `500` : Erreur serveur

## Support

Pour toute question : support@iafactory-algeria.com
