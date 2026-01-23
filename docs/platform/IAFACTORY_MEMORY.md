# IAFactory Memory System

**Version:** 1.0.0
**Date:** 30 Decembre 2025
**Stack:** PostgreSQL + Redis + Qdrant + OpenAI Embeddings

---

## Vue d'Ensemble

Systeme de memoire persistante pour IAFactory comprenant:
- **Conversations**: Stockage sessions + messages
- **User Memory**: Profil, preferences, business, faits, objectifs
- **Semantic Search**: Recherche par similarite vectorielle
- **Auto-extraction**: Extraction memoire via LLM

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend/Apps                          │
│            (Chat, PME Audit, CRM, Bolt, etc.)              │
└─────────────────┬───────────────────────────────┬──────────┘
                  │                               │
                  ▼                               ▼
┌─────────────────────────────┐   ┌─────────────────────────────┐
│   /api/conversations/*      │   │     /api/memory/*           │
│   - Sessions CRUD           │   │     - Memories CRUD         │
│   - Messages                │   │     - Context injection     │
│   - Quick send              │   │     - Semantic search       │
└─────────────────┬───────────┘   └─────────────┬───────────────┘
                  │                               │
                  └───────────────┬───────────────┘
                                  ▼
                  ┌───────────────────────────────┐
                  │       MemoryService           │
                  │   - Session management        │
                  │   - Message storage           │
                  │   - Memory extraction (LLM)   │
                  │   - Context building          │
                  └───────────────┬───────────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PostgreSQL    │    │     Redis       │    │     Qdrant      │
│   - Sessions    │    │   - Session     │    │   - Message     │
│   - Messages    │    │     cache       │    │     embeddings  │
│   - Memories    │    │   - Rate limit  │    │   - Memory      │
│   - Corrections │    │                 │    │     embeddings  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## Fichiers Crees

| Fichier | Description | Lignes |
|---------|-------------|--------|
| `migrations/014_iafactory_memory.sql` | Schema PostgreSQL complet | ~400 |
| `app/models/memory_models.py` | Modeles Pydantic | ~450 |
| `app/services/memory_service.py` | Service principal | ~750 |
| `app/routers/memory.py` | API memoires | ~320 |
| `app/routers/conversations.py` | API conversations | ~450 |

---

## Schema Base de Donnees

### Tables Principales

```sql
-- Sessions de conversation
chat_sessions (
    id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL,
    user_id UUID NOT NULL,
    title VARCHAR(255),
    app_context VARCHAR(50),  -- 'chat', 'pme', 'rag', 'crm', 'bolt', 'council'
    language VARCHAR(10),
    agent_id VARCHAR(100),
    model VARCHAR(50),
    message_count INTEGER,
    total_tokens INTEGER,
    is_archived BOOLEAN,
    is_starred BOOLEAN,
    metadata JSONB,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ,
    last_message_at TIMESTAMPTZ
)

-- Messages
chat_messages (
    id UUID PRIMARY KEY,
    session_id UUID NOT NULL,
    role VARCHAR(20),  -- 'user', 'assistant', 'system', 'tool'
    content TEXT NOT NULL,
    parent_message_id UUID,
    tokens_input INTEGER,
    tokens_output INTEGER,
    model_used VARCHAR(50),
    latency_ms INTEGER,
    tool_calls JSONB,
    tool_results JSONB,
    metadata JSONB,
    created_at TIMESTAMPTZ
)

-- Memoires utilisateur
user_memories (
    id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL,
    user_id UUID NOT NULL,
    category VARCHAR(20),  -- 'profile', 'preference', 'business', 'fact', 'goal'
    key VARCHAR(100) NOT NULL,
    value TEXT NOT NULL,
    confidence DECIMAL(3,2),
    source VARCHAR(20),  -- 'extracted', 'explicit', 'system'
    source_message_id UUID,
    is_active BOOLEAN,
    access_count INTEGER,
    metadata JSONB,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ,
    last_accessed_at TIMESTAMPTZ,
    UNIQUE(user_id, category, key)
)

-- Corrections de memoire
memory_corrections (
    id UUID PRIMARY KEY,
    memory_id UUID NOT NULL,
    old_value TEXT NOT NULL,
    new_value TEXT NOT NULL,
    corrected_by UUID NOT NULL,
    reason TEXT,
    created_at TIMESTAMPTZ
)
```

### Categories de Memoire

| Categorie | Description | Exemples |
|-----------|-------------|----------|
| `profile` | Informations personnelles | nom, metier, localisation |
| `preference` | Preferences utilisateur | langue, style_communication |
| `business` | Informations entreprise | secteur, taille, CA |
| `fact` | Faits importants | "utilise Laravel", "client depuis 2024" |
| `goal` | Objectifs | "automatiser la comptabilite" |

---

## API Endpoints

### Conversations API (`/api/conversations`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Liste sessions (pagination) |
| POST | `/` | Creer session |
| GET | `/{id}` | Detail session + messages |
| PUT | `/{id}` | Modifier session |
| DELETE | `/{id}` | Supprimer session |
| GET | `/{id}/messages` | Messages (pagination cursor) |
| POST | `/{id}/messages` | Ajouter message |
| POST | `/send` | Envoi rapide (auto-create session) |
| POST | `/{id}/star` | Toggle favori |
| POST | `/{id}/archive` | Archiver |
| POST | `/{id}/unarchive` | Desarchiver |
| POST | `/bulk/archive` | Archivage multiple |

### Memory API (`/api/memory`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Liste memoires (filtre categorie) |
| GET | `/context` | Contexte pour IA |
| GET | `/stats` | Statistiques memoire |
| GET | `/{id}` | Detail memoire |
| POST | `/` | Creer memoire explicite |
| PUT | `/{id}` | Modifier memoire |
| DELETE | `/{id}` | Supprimer memoire |
| POST | `/search` | Recherche semantique |
| POST | `/bulk` | Creation multiple |
| GET | `/export` | Exporter memoires JSON |

---

## Utilisation

### 1. Creer une Conversation

```python
# POST /api/conversations/
{
    "title": "Audit PME - Boulangerie Oran",
    "app_context": "pme",
    "language": "fr",
    "model": "groq"
}
```

### 2. Envoyer un Message

```python
# POST /api/conversations/{session_id}/messages
{
    "content": "Je suis Ahmed, je gere une boulangerie a Oran avec 5 employes",
    "role": "user"
}

# Response inclut: memories_extracted: 3
# -> profile/nom: Ahmed
# -> business/secteur: boulangerie
# -> business/localisation: Oran
```

### 3. Envoi Rapide (Auto-Session)

```python
# POST /api/conversations/send
{
    "content": "Bonjour, j'ai besoin d'aide pour ma comptabilite",
    "app_context": "pme",
    "include_memory": true,
    "extract_memories": true
}

# Response
{
    "success": true,
    "session_id": "uuid-auto-generated",
    "message": {...},
    "memories_extracted": 1
}
```

### 4. Recuperer Contexte Memoire pour IA

```python
# GET /api/memory/context

# Response
{
    "user_profile": {
        "nom": "Ahmed",
        "metier": "gerant"
    },
    "preferences": {
        "langue": "fr",
        "style": "professionnel"
    },
    "business_info": {
        "secteur": "boulangerie",
        "localisation": "Oran",
        "employes": "5"
    },
    "relevant_facts": [
        "utilise_logiciel: Excel pour la comptabilite"
    ],
    "goals": [
        "Automatiser la facturation"
    ],
    "recent_topics": [
        "Audit PME",
        "Comptabilite"
    ]
}
```

### 5. Injecter dans Prompt IA

```python
from app.services.memory_service import get_memory_service

service = get_memory_service()
context = await service.get_memory_context(tenant_id, user_id)

system_prompt = f"""Tu es un assistant IA pour les PME algeriennes.

Contexte utilisateur:
{context.to_system_prompt()}

Instructions:
- Reponds en francais
- Sois concis et pratique
"""
```

### 6. Creer Memoire Explicite

```python
# POST /api/memory/
{
    "category": "business",
    "key": "budget_annuel",
    "value": "50 millions DA",
    "confidence": 1.0
}
```

### 7. Recherche Semantique

```python
# POST /api/memory/search
{
    "query": "problemes de facturation",
    "search_type": "all",  # "messages", "memories", "all"
    "limit": 10,
    "min_similarity": 0.7
}

# Response
{
    "query": "problemes de facturation",
    "results": [
        {
            "id": "...",
            "type": "message",
            "content": "J'ai des difficultés avec mes factures...",
            "similarity": 0.89
        },
        {
            "id": "...",
            "type": "memory",
            "content": "goal: automatiser la facturation",
            "similarity": 0.82
        }
    ],
    "search_time_ms": 45
}
```

---

## Integration Frontend

### React/TypeScript

```typescript
// hooks/useConversations.ts
import { useQuery, useMutation } from '@tanstack/react-query';

export function useConversations(appContext?: string) {
  return useQuery({
    queryKey: ['conversations', appContext],
    queryFn: () => api.get('/api/conversations/', { params: { app_context: appContext } })
  });
}

export function useSendMessage() {
  return useMutation({
    mutationFn: (data: { content: string; session_id?: string }) =>
      api.post('/api/conversations/send', data)
  });
}
```

```typescript
// hooks/useMemory.ts
export function useMemoryContext() {
  return useQuery({
    queryKey: ['memory', 'context'],
    queryFn: () => api.get('/api/memory/context')
  });
}

export function useMemories(category?: string) {
  return useQuery({
    queryKey: ['memories', category],
    queryFn: () => api.get('/api/memory/', { params: { category } })
  });
}
```

---

## Flow Extraction Memoire

```
┌─────────────────┐
│  User Message   │
│  "Je suis       │
│   Ahmed..."     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Save Message   │
│  PostgreSQL     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  LLM Extraction │
│  GPT-4o-mini    │
│  "Extrait les   │
│   informations" │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Parse JSON     │
│  {memories: [   │
│    {category,   │
│     key, value} │
│  ]}             │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Upsert Memory  │
│  PostgreSQL     │
│  (ON CONFLICT)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Index Vector   │
│  Qdrant         │
│  (async)        │
└─────────────────┘
```

---

## Configuration

### Variables d'Environnement

```env
# PostgreSQL
POSTGRES_URL=postgresql://user:pass@host:5432/iafactory_dz

# Redis
REDIS_URL=redis://host:6379/0
REDIS_PASSWORD=

# Qdrant
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_API_KEY=

# OpenAI (pour embeddings et extraction)
OPENAI_API_KEY=sk-...
```

### Qdrant Collections

Creer les collections au demarrage:

```python
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

client = QdrantClient(host="localhost", port=6333)

# Collection messages
client.create_collection(
    collection_name="chat_messages",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
)

# Collection memories
client.create_collection(
    collection_name="user_memories",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
)
```

---

## Migration

Executer la migration SQL:

```bash
psql -U postgres -d iafactory_dz -f migrations/014_iafactory_memory.sql
```

Ou via Python:

```python
from app.db import get_db_connection

with open('migrations/014_iafactory_memory.sql') as f:
    sql = f.read()

with get_db_connection() as conn:
    with conn.cursor() as cur:
        cur.execute(sql)
```

---

## Tests

```python
import pytest
from app.services.memory_service import MemoryService

@pytest.mark.asyncio
async def test_create_session():
    service = MemoryService()
    session = await service.create_session(
        tenant_id="test-tenant",
        user_id="test-user",
        session_data=ChatSessionCreate(title="Test")
    )
    assert session.id is not None
    assert session.title == "Test"

@pytest.mark.asyncio
async def test_memory_context():
    service = MemoryService()
    context = await service.get_memory_context(
        tenant_id="test-tenant",
        user_id="test-user"
    )
    assert isinstance(context, MemoryContext)
```

---

## Performance

| Operation | Latence Typique |
|-----------|-----------------|
| Create session | 5-10ms |
| Add message | 5-10ms |
| Get messages (50) | 10-20ms |
| Get memory context | 15-30ms |
| Memory extraction (LLM) | 500-1500ms |
| Semantic search | 50-100ms |

### Optimisations

1. **Redis Cache**: Sessions actives cachees 1h
2. **Async Indexing**: Embeddings indexes en background
3. **Batch Operations**: Bulk create pour imports
4. **Pagination Cursor**: Pas d'OFFSET pour messages

---

## Securite

### Row-Level Security (RLS)

```sql
-- Chaque table a des policies RLS
ALTER TABLE chat_sessions ENABLE ROW LEVEL SECURITY;

CREATE POLICY sessions_tenant_isolation ON chat_sessions
    USING (tenant_id = current_setting('app.current_tenant')::UUID);
```

### Validation

- Tous les IDs valides comme UUID
- Ownership verifie avant modification
- Soft delete pour memories (is_active)
- Corrections trackees pour audit

---

## Roadmap

- [ ] Export/Import conversations (JSON/ZIP)
- [ ] Partage de conversations (read-only links)
- [ ] Memories auto-cleanup (TTL configurable)
- [ ] Analytics dashboard conversations
- [ ] Webhooks sur events memoire
- [ ] Multi-model embeddings support

---

## Support

Pour questions ou bugs:
- GitHub Issues: https://github.com/iafactory/rag-dz/issues
- Email: support@iafactory.dz

---

*Documentation generee le 30 Decembre 2025*
