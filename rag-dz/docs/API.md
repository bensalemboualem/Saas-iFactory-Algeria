# API Reference - RAG-DZ / Nexus AI Platform

**Version:** 2.0.0
**Base URL:** `http://localhost:8000/api/v1`
**Dernière mise à jour:** Décembre 2024

---

## Vue d'ensemble

L'API principale de RAG-DZ expose plus de 90 endpoints organisés par domaine fonctionnel. Elle utilise FastAPI et fournit une documentation interactive via Swagger UI.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              API ENDPOINTS                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  /auth      - Authentification (login, register, tokens)                    │
│  /users     - Gestion des utilisateurs                                      │
│  /projects  - Projets et workspaces                                         │
│  /agents    - Agents IA (invoke, list, configure)                           │
│  /rag       - RAG endpoints (query, upload, index)                          │
│  /llm       - LLM endpoints (chat, complete, models)                        │
│  /video     - Génération vidéo                                              │
│  /voice     - STT/TTS endpoints                                             │
│  /billing   - Facturation Chargily                                          │
│  /keys      - Gestion des clés API                                          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Authentification

### Login

```http
POST /api/v1/auth/login
Content-Type: application/json

{
    "email": "user@example.dz",
    "password": "password123"
}
```

**Réponse:**
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer",
    "expires_in": 3600,
    "user": {
        "id": "uuid",
        "email": "user@example.dz",
        "name": "User Name",
        "role": "user"
    }
}
```

### Register

```http
POST /api/v1/auth/register
Content-Type: application/json

{
    "email": "newuser@example.dz",
    "password": "securepassword",
    "name": "New User"
}
```

### Refresh Token

```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
    "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

### API Key Authentication

Pour les appels machine-to-machine:

```http
GET /api/v1/resource
Authorization: Bearer sk-nexus-xxxxxxxxxxxxx
```

---

## Agents

### Invoquer un Agent

```http
POST /api/v1/agents/{agent_type}/invoke
Authorization: Bearer <token>
Content-Type: application/json

{
    "input": "Analyse le marché e-commerce en Algérie",
    "context": {
        "language": "fr",
        "format": "detailed"
    },
    "options": {
        "model": "gpt-4",
        "temperature": 0.7,
        "max_tokens": 4000
    }
}
```

**Types d'agents disponibles:**
- `consultant` - AI Consultant
- `customer_support` - Support client
- `data_analyst` - Analyse de données
- `financial_coach` - Coach financier
- `legal` - Conseils juridiques
- `recruitment` - Recrutement
- `real_estate` - Immobilier
- `travel` - Voyages
- `teaching` - Enseignement

**Réponse:**
```json
{
    "agent_type": "consultant",
    "response": "Selon mon analyse du marché...",
    "metadata": {
        "model": "gpt-4",
        "tokens_used": 1523,
        "latency_ms": 2340,
        "cost_usd": 0.0456
    }
}
```

### Lister les Agents

```http
GET /api/v1/agents
Authorization: Bearer <token>
```

**Réponse:**
```json
{
    "agents": [
        {
            "type": "consultant",
            "name": "AI Consultant",
            "description": "Agent conseil stratégique",
            "status": "available",
            "capabilities": ["market_analysis", "strategy", "competition"]
        }
    ]
}
```

### Conversation avec Agent

```http
POST /api/v1/agents/{agent_type}/chat
Authorization: Bearer <token>
Content-Type: application/json

{
    "message": "Continue l'analyse précédente",
    "session_id": "sess-123456",
    "stream": false
}
```

---

## RAG (Retrieval Augmented Generation)

### Upload de Document

```http
POST /api/v1/rag/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <binary>
collection: "my-documents"
metadata: {"source": "annual_report", "year": 2024}
```

**Réponse:**
```json
{
    "document_id": "doc-uuid",
    "filename": "rapport.pdf",
    "pages": 42,
    "chunks": 156,
    "collection": "my-documents",
    "status": "indexed"
}
```

### Query RAG

```http
POST /api/v1/rag/query
Authorization: Bearer <token>
Content-Type: application/json

{
    "query": "Quel est le chiffre d'affaires 2024?",
    "collection": "my-documents",
    "options": {
        "top_k": 5,
        "threshold": 0.7,
        "rerank": true
    }
}
```

**Réponse:**
```json
{
    "answer": "Le chiffre d'affaires 2024 est de 15M DZD...",
    "sources": [
        {
            "document_id": "doc-uuid",
            "chunk_id": "chunk-123",
            "content": "...",
            "score": 0.92,
            "page": 15
        }
    ],
    "metadata": {
        "tokens_used": 850,
        "latency_ms": 1200
    }
}
```

### Lister les Collections

```http
GET /api/v1/rag/collections
Authorization: Bearer <token>
```

### Supprimer un Document

```http
DELETE /api/v1/rag/documents/{document_id}
Authorization: Bearer <token>
```

---

## LLM

### Chat Completion

```http
POST /api/v1/llm/chat
Authorization: Bearer <token>
Content-Type: application/json

{
    "messages": [
        {"role": "system", "content": "Tu es un assistant utile."},
        {"role": "user", "content": "Explique l'IA en termes simples."}
    ],
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 1000,
    "stream": false
}
```

**Réponse:**
```json
{
    "id": "chat-uuid",
    "model": "gpt-4",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "L'intelligence artificielle..."
            },
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 25,
        "completion_tokens": 150,
        "total_tokens": 175
    }
}
```

### Streaming

```http
POST /api/v1/llm/chat
Content-Type: application/json

{
    "messages": [...],
    "stream": true
}
```

**Réponse (SSE):**
```
data: {"delta": "L'", "finish_reason": null}
data: {"delta": "intelligence", "finish_reason": null}
data: {"delta": " artificielle", "finish_reason": null}
...
data: {"delta": "", "finish_reason": "stop"}
```

### Lister les Modèles

```http
GET /api/v1/llm/models
Authorization: Bearer <token>
```

**Réponse:**
```json
{
    "models": [
        {
            "id": "gpt-4",
            "provider": "openai",
            "context_length": 128000,
            "cost_per_1k_input": 0.01,
            "cost_per_1k_output": 0.03
        },
        {
            "id": "claude-3-opus",
            "provider": "anthropic",
            "context_length": 200000,
            "cost_per_1k_input": 0.015,
            "cost_per_1k_output": 0.075
        }
    ]
}
```

---

## Vidéo

### Créer un Projet Vidéo

```http
POST /api/v1/video/projects
Authorization: Bearer <token>
Content-Type: application/json

{
    "title": "Introduction à l'IA",
    "prompt": "Créer une vidéo explicative de 2 minutes sur l'IA",
    "config": {
        "duration": 120,
        "language": "fr",
        "style": "professional"
    }
}
```

### Démarrer la Génération

```http
POST /api/v1/video/projects/{project_id}/start
Authorization: Bearer <token>
```

### Statut du Projet

```http
GET /api/v1/video/projects/{project_id}/status
Authorization: Bearer <token>
```

**Réponse:**
```json
{
    "project_id": "uuid",
    "status": "generating",
    "progress": 45,
    "current_step": "image_generation",
    "steps": {
        "script": {"status": "completed", "progress": 100},
        "images": {"status": "in_progress", "progress": 60},
        "voice": {"status": "pending", "progress": 0},
        "montage": {"status": "pending", "progress": 0}
    }
}
```

---

## Voice

### Speech-to-Text

```http
POST /api/v1/voice/transcribe
Authorization: Bearer <token>
Content-Type: multipart/form-data

audio: <binary>
language: "fr"
```

**Réponse:**
```json
{
    "text": "Bonjour, comment puis-je vous aider?",
    "language": "fr",
    "confidence": 0.95,
    "duration_seconds": 3.5
}
```

### Text-to-Speech

```http
POST /api/v1/voice/synthesize
Authorization: Bearer <token>
Content-Type: application/json

{
    "text": "Bienvenue sur notre plateforme.",
    "voice_id": "thomas",
    "provider": "elevenlabs",
    "format": "mp3"
}
```

**Réponse:**
Binary audio file avec header:
```
Content-Type: audio/mpeg
Content-Disposition: attachment; filename="speech.mp3"
```

### Lister les Voix

```http
GET /api/v1/voice/voices?provider=elevenlabs&language=fr
Authorization: Bearer <token>
```

---

## Billing (Chargily)

### Créer un Paiement

```http
POST /api/v1/billing/payments
Authorization: Bearer <token>
Content-Type: application/json

{
    "amount": 5000,
    "currency": "DZD",
    "description": "Abonnement Pro mensuel",
    "customer": {
        "name": "Client Name",
        "email": "client@example.dz"
    },
    "metadata": {
        "plan": "pro",
        "period": "monthly"
    }
}
```

**Réponse:**
```json
{
    "payment_id": "pay-uuid",
    "checkout_url": "https://pay.chargily.dz/checkout/...",
    "status": "pending",
    "amount": 5000,
    "currency": "DZD",
    "expires_at": "2024-12-01T12:00:00Z"
}
```

### Webhook Chargily

```http
POST /api/v1/billing/webhook
Content-Type: application/json
X-Chargily-Signature: sha256=...

{
    "event": "checkout.completed",
    "data": {
        "payment_id": "pay-uuid",
        "status": "paid",
        "amount": 5000
    }
}
```

### Lister les Factures

```http
GET /api/v1/billing/invoices?status=paid&limit=10
Authorization: Bearer <token>
```

---

## Keys (Gestion des Clés API)

### Créer une Clé API

```http
POST /api/v1/keys
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "Production API Key",
    "permissions": ["read", "write"],
    "rate_limit": 1000,
    "expires_at": "2025-12-31T23:59:59Z"
}
```

**Réponse:**
```json
{
    "key_id": "key-uuid",
    "api_key": "sk-nexus-xxxxxxxxxxxxxxxx",
    "name": "Production API Key",
    "created_at": "2024-12-01T10:00:00Z",
    "expires_at": "2025-12-31T23:59:59Z"
}
```

**Important:** La clé API n'est affichée qu'une seule fois. Conservez-la de manière sécurisée.

### Lister les Clés

```http
GET /api/v1/keys
Authorization: Bearer <token>
```

### Révoquer une Clé

```http
DELETE /api/v1/keys/{key_id}
Authorization: Bearer <token>
```

---

## Projets

### Créer un Projet

```http
POST /api/v1/projects
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "Mon Projet IA",
    "description": "Description du projet",
    "type": "rag"
}
```

### Lister les Projets

```http
GET /api/v1/projects?page=1&limit=10
Authorization: Bearer <token>
```

---

## Utilisateurs

### Profil Utilisateur

```http
GET /api/v1/users/me
Authorization: Bearer <token>
```

### Mettre à Jour le Profil

```http
PATCH /api/v1/users/me
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "New Name",
    "avatar_url": "https://..."
}
```

---

## Codes d'Erreur

| Code | Signification |
|------|---------------|
| 400 | Bad Request - Paramètres invalides |
| 401 | Unauthorized - Token manquant ou invalide |
| 403 | Forbidden - Permissions insuffisantes |
| 404 | Not Found - Ressource introuvable |
| 409 | Conflict - Conflit de données |
| 422 | Unprocessable Entity - Validation échouée |
| 429 | Too Many Requests - Rate limit dépassé |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

### Format des Erreurs

```json
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Le champ 'email' est invalide",
        "details": {
            "field": "email",
            "constraint": "email_format"
        }
    },
    "request_id": "req-uuid"
}
```

---

## Rate Limiting

| Endpoint | Limite | Fenêtre |
|----------|--------|---------|
| `/auth/*` | 10 req | 1 min |
| `/llm/chat` | 60 req | 1 min |
| `/rag/query` | 100 req | 1 min |
| `/agents/*/invoke` | 30 req | 1 min |
| `/video/*` | 10 req | 1 hour |

Headers de réponse:
```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 55
X-RateLimit-Reset: 1701432000
```

---

## WebSocket API

### Connexion

```javascript
const ws = new WebSocket('wss://api.nexus.iafactory.dz/ws');

ws.send(JSON.stringify({
    type: 'auth',
    token: 'Bearer <access_token>'
}));
```

### Channels

- `agent:{agent_type}` - Mises à jour d'un agent
- `project:{project_id}` - Progression d'un projet
- `chat:{session_id}` - Messages de chat en temps réel

---

## SDK

### Python

```python
from nexus_sdk import NexusClient

client = NexusClient(api_key="sk-nexus-xxx")

# Invoquer un agent
response = client.agents.invoke(
    agent_type="consultant",
    input="Analyse du marché"
)

# RAG Query
answer = client.rag.query(
    query="Quel est le CA?",
    collection="documents"
)
```

### JavaScript

```javascript
import { NexusClient } from '@nexus/sdk';

const client = new NexusClient({ apiKey: 'sk-nexus-xxx' });

// Chat streaming
const stream = await client.llm.chat({
    messages: [{ role: 'user', content: 'Hello' }],
    stream: true
});

for await (const chunk of stream) {
    console.log(chunk.delta);
}
```

---

## Documentation Interactive

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

---

*API Reference générée le 31 décembre 2024*
