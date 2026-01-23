# Endpoints API

## Vue d'Ensemble

Liste complète des endpoints disponibles dans l'API IAFactory Algeria.

## Chat Completions

### POST /v1/chat/completions

Créer une réponse de chat pour une conversation.

**Requête :**

```json
{
  "model": "gpt-4",
  "messages": [
    {"role": "system", "content": "Tu es un assistant utile."},
    {"role": "user", "content": "Bonjour!"}
  ],
  "temperature": 0.7,
  "max_tokens": 150,
  "stream": false
}
```

**Paramètres :**

| Paramètre | Type | Requis | Description |
|-----------|------|--------|-------------|
| `model` | string | ✅ | Identifiant du modèle |
| `messages` | array | ✅ | Liste des messages |
| `temperature` | number | ❌ | 0-2, défaut: 1 |
| `max_tokens` | integer | ❌ | Nombre max de tokens |
| `stream` | boolean | ❌ | Streaming activé |
| `top_p` | number | ❌ | 0-1, défaut: 1 |
| `frequency_penalty` | number | ❌ | -2 à 2, défaut: 0 |
| `presence_penalty` | number | ❌ | -2 à 2, défaut: 0 |

**Réponse :**

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
      "content": "Bonjour! Comment puis-je vous aider?"
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 13,
    "completion_tokens": 10,
    "total_tokens": 23
  }
}
```

## Completions (Legacy)

### POST /v1/completions

Créer une complétion de texte.

**Requête :**

```json
{
  "model": "gpt-3.5-turbo-instruct",
  "prompt": "Écris une histoire sur",
  "max_tokens": 100,
  "temperature": 0.7
}
```

## Embeddings

### POST /v1/embeddings

Créer des vecteurs d'embedding pour du texte.

**Requête :**

```json
{
  "model": "text-embedding-ada-002",
  "input": "Votre texte ici"
}
```

**Réponse :**

```json
{
  "object": "list",
  "data": [{
    "object": "embedding",
    "embedding": [0.0023, -0.009, ...],
    "index": 0
  }],
  "model": "text-embedding-ada-002",
  "usage": {
    "prompt_tokens": 8,
    "total_tokens": 8
  }
}
```

## Modèles

### GET /v1/models

Lister tous les modèles disponibles.

**Réponse :**

```json
{
  "object": "list",
  "data": [
    {
      "id": "gpt-4",
      "object": "model",
      "created": 1687882410,
      "owned_by": "openai"
    },
    {
      "id": "gpt-3.5-turbo",
      "object": "model",
      "created": 1677610602,
      "owned_by": "openai"
    }
  ]
}
```

### GET /v1/models/{model_id}

Récupérer les détails d'un modèle spécifique.

**Réponse :**

```json
{
  "id": "gpt-4",
  "object": "model",
  "created": 1687882410,
  "owned_by": "openai",
  "permission": [...],
  "root": "gpt-4",
  "parent": null
}
```

## Modération

### POST /v1/moderations

Classifier si du texte viole la politique de contenu.

**Requête :**

```json
{
  "input": "Texte à modérer"
}
```

**Réponse :**

```json
{
  "id": "modr-123",
  "model": "text-moderation-latest",
  "results": [{
    "flagged": false,
    "categories": {
      "hate": false,
      "violence": false,
      "sexual": false,
      "self-harm": false
    },
    "category_scores": {
      "hate": 0.0001,
      "violence": 0.0002,
      "sexual": 0.0003,
      "self-harm": 0.0001
    }
  }]
}
```

## Images (DALL-E)

### POST /v1/images/generations

Générer une image à partir d'un prompt.

**Requête :**

```json
{
  "prompt": "Un chat astronaute",
  "n": 1,
  "size": "1024x1024"
}
```

## Audio

### POST /v1/audio/transcriptions

Transcrire un fichier audio en texte.

**Requête (multipart/form-data) :**

```
file: audio.mp3
model: whisper-1
```

### POST /v1/audio/translations

Traduire un fichier audio en anglais.

## Files

### POST /v1/files

Upload un fichier pour fine-tuning.

### GET /v1/files

Lister tous les fichiers uploadés.

### GET /v1/files/{file_id}

Récupérer les infos d'un fichier.

### DELETE /v1/files/{file_id}

Supprimer un fichier.

## Fine-tuning

### POST /v1/fine-tuning/jobs

Créer un job de fine-tuning.

### GET /v1/fine-tuning/jobs

Lister les jobs de fine-tuning.

### GET /v1/fine-tuning/jobs/{job_id}

Récupérer le statut d'un job.

### POST /v1/fine-tuning/jobs/{job_id}/cancel

Annuler un job de fine-tuning.

## Utilisation

### GET /v1/usage

Récupérer les statistiques d'utilisation.

**Réponse :**

```json
{
  "object": "usage",
  "data": {
    "date": "2024-01-15",
    "tokens_used": 150000,
    "requests": 1500,
    "cost": 4.50
  }
}
```

## Codes de Statut

| Code | Signification |
|------|--------------|
| 200 | Succès |
| 400 | Requête invalide |
| 401 | Non autorisé |
| 403 | Interdit |
| 404 | Non trouvé |
| 429 | Trop de requêtes |
| 500 | Erreur serveur |
| 503 | Service indisponible |

## Rate Limiting

Les en-têtes de réponse incluent :

```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1234567890
```
