# Introduction à l'API

## Vue d'Ensemble

L'API IAFactory Algeria est une API REST compatible OpenAI qui vous permet d'intégrer des capacités d'intelligence artificielle dans vos applications.

## Caractéristiques Principales

### ✨ Modèles Puissants
- GPT-4, GPT-3.5-Turbo
- Claude 3 (Opus, Sonnet, Haiku)
- Mistral AI
- Llama 2 et 3
- Gemini Pro

### 🚀 Performance
- Latence faible
- Haute disponibilité (99.9% uptime)
- Scaling automatique
- Caching intelligent

### 🔒 Sécurité
- Chiffrement HTTPS
- Authentification par clé API
- Rotation des clés
- Logs d'audit

### 💰 Tarification Flexible
- Pay-as-you-go
- Plans mensuels
- Tarifs dégressifs
- Essai gratuit

## Protocole API

### Format des Requêtes

**Base URL :**
```
https://api.iafactory-algeria.com/v1
```

**Format :**
```
JSON (application/json)
```

**Méthodes HTTP :**
- `GET` : Récupération de données
- `POST` : Création/Exécution
- `PUT` : Mise à jour
- `DELETE` : Suppression

### Structure d'une Requête

```http
POST /v1/chat/completions HTTP/1.1
Host: api.iafactory-algeria.com
Content-Type: application/json
Authorization: Bearer VOTRE_CLE_API

{
  "model": "gpt-4",
  "messages": [
    {"role": "system", "content": "Tu es un assistant utile."},
    {"role": "user", "content": "Bonjour!"}
  ],
  "temperature": 0.7,
  "max_tokens": 150
}
```

### Structure d'une Réponse

```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "gpt-4",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Bonjour! Comment puis-je vous aider?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 20,
    "completion_tokens": 10,
    "total_tokens": 30
  }
}
```

## Limites

### Rate Limits

| Plan | Requêtes/minute | Tokens/minute |
|------|----------------|---------------|
| Gratuit | 3 | 40,000 |
| Pro | 60 | 200,000 |
| Enterprise | Illimité | Illimité |

### Limites de Taille

- **Requête** : 10 MB max
- **Contexte** : Variable selon le modèle
- **Timeout** : 60 secondes

## Compatibilité

L'API est compatible avec :
- ✅ OpenAI SDK
- ✅ LangChain
- ✅ LlamaIndex
- ✅ Semantic Kernel
- ✅ AutoGen

## Versions

**Version actuelle :** v1

**Changelog :**
- `v1.0.0` (2024-01-15) : Version initiale
- Support multimodèle
- Endpoints chat et completions
- Support streaming

## Support

- 📧 Email : support@iafactory-algeria.com
- 💬 Discord : [Rejoindre notre serveur](https://discord.gg/iafactory)
- 📚 Documentation : [docs.iafactory-algeria.com](https://docs.iafactory-algeria.com)
