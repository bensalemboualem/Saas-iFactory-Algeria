# IAFactory-School - Spécifications Techniques

## Architecture Globale

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND                                │
│  React 18 + TypeScript + Tailwind CSS + Shadcn/UI           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      API GATEWAY                             │
│  FastAPI + Uvicorn + JWT Authentication                     │
└─────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   PostgreSQL    │ │   ChromaDB      │ │   Redis         │
│   (Supabase)    │ │   (Vectors)     │ │   (Cache)       │
└─────────────────┘ └─────────────────┘ └─────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      LLM ENGINE                              │
│  Ollama (Qwen 2.5) / OpenAI API (fallback)                  │
└─────────────────────────────────────────────────────────────┘
```

## Stack Technologique

### Frontend
| Technologie | Version | Usage |
|-------------|---------|-------|
| React | 18.2 | Framework UI |
| TypeScript | 5.3 | Typage statique |
| Tailwind CSS | 3.4 | Styling |
| Shadcn/UI | Latest | Composants |
| Vite | 5.0 | Build tool |
| React Query | 5.0 | State management |
| React Router | 6.0 | Navigation |

### Backend
| Technologie | Version | Usage |
|-------------|---------|-------|
| Python | 3.11+ | Runtime |
| FastAPI | 0.109 | API REST |
| Uvicorn | 0.27 | Serveur ASGI |
| Pydantic | 2.6 | Validation |
| SQLAlchemy | 2.0 | ORM |
| Alembic | 1.13 | Migrations |

### Base de Données
| Technologie | Version | Usage |
|-------------|---------|-------|
| PostgreSQL | 15 | Base principale |
| Supabase | Cloud | BaaS |
| ChromaDB | 0.4 | Vector store |
| Redis | 7.2 | Cache/Sessions |

### Intelligence Artificielle
| Technologie | Version | Usage |
|-------------|---------|-------|
| LangChain | 0.1 | Orchestration LLM |
| Ollama | 0.1 | LLM local |
| Qwen 2.5 | 7B | Modèle principal |
| HuggingFace | Embeddings | Vectorisation |
| sentence-transformers | 2.2 | Embeddings multilingues |

### Infrastructure
| Technologie | Version | Usage |
|-------------|---------|-------|
| Docker | 24 | Conteneurisation |
| Docker Compose | 2.24 | Orchestration |
| Nginx | 1.25 | Reverse proxy |
| Certbot | Latest | SSL/TLS |

## API Endpoints

### Authentification
```
POST /api/auth/login          # Connexion
POST /api/auth/register       # Inscription
POST /api/auth/refresh        # Rafraîchir token
POST /api/auth/logout         # Déconnexion
```

### Utilisateurs
```
GET  /api/users/me            # Profil courant
PUT  /api/users/me            # Modifier profil
GET  /api/users/{id}          # Profil utilisateur
GET  /api/users               # Liste (admin)
```

### Cours et Leçons
```
GET  /api/courses             # Liste des cours
GET  /api/courses/{id}        # Détail cours
GET  /api/lessons/{id}        # Détail leçon
POST /api/lessons/{id}/complete  # Marquer comme complété
```

### Assistant IA (RAG)
```
POST /api/chat                # Question au chatbot
GET  /api/chat/history        # Historique conversation
POST /api/chat/feedback       # Feedback sur réponse
```

### Analytics
```
GET  /api/analytics/student/{id}   # Stats élève
GET  /api/analytics/class/{id}     # Stats classe
GET  /api/analytics/school/{id}    # Stats école
```

## Système RAG (Retrieval Augmented Generation)

### Architecture RAG
```
Question Utilisateur
        │
        ▼
┌─────────────────┐
│   Embedding     │  ← HuggingFace multilingual
│   (Question)    │
└─────────────────┘
        │
        ▼
┌─────────────────┐
│   ChromaDB      │  ← Recherche similarité
│   (Retrieval)   │
└─────────────────┘
        │
        ▼
┌─────────────────┐
│   Context       │  ← Top K documents
│   Assembly      │
└─────────────────┘
        │
        ▼
┌─────────────────┐
│   LLM           │  ← Qwen 2.5 / OpenAI
│   (Generation)  │
└─────────────────┘
        │
        ▼
    Réponse + Sources
```

### Configuration ChromaDB
```python
# Paramètres vectorstore
COLLECTION_NAME = "iafactory_docs"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 5
```

### Modèle LLM (Qwen 2.5)
```python
# Configuration Ollama
OLLAMA_BASE_URL = "http://localhost:11434"
MODEL_NAME = "qwen2.5:7b"
TEMPERATURE = 0.3
MAX_TOKENS = 2048
CONTEXT_WINDOW = 8192
```

## Sécurité

### Authentification
- JWT tokens (access + refresh)
- Expiration: 15 min (access), 7 jours (refresh)
- Hachage passwords: bcrypt
- Rate limiting: 100 req/min

### Autorisation
- RBAC (Role-Based Access Control)
- Rôles: admin, teacher, student, parent
- Permissions granulaires par ressource

### Protection des Données
- Chiffrement TLS 1.3 en transit
- Chiffrement AES-256 au repos
- Anonymisation des logs
- Conformité RGPD

### Validation Inputs
- Pydantic pour toutes les entrées
- Sanitization HTML/SQL
- CORS configuré strictement
- CSP headers

## Performance

### Cibles
| Métrique | Cible | Actuel |
|----------|-------|--------|
| Time to First Byte | < 200ms | 150ms |
| LCP (Largest Contentful Paint) | < 2.5s | 2.1s |
| API Response (P95) | < 500ms | 350ms |
| RAG Response | < 3s | 2.5s |

### Optimisations
- Mise en cache Redis (TTL: 5 min)
- Lazy loading composants React
- Code splitting automatique
- Images optimisées (WebP)
- Gzip compression

## Déploiement

### Environnements
| Env | URL | Usage |
|-----|-----|-------|
| Dev | localhost:3000 | Développement |
| Staging | staging.iafactory.ai | Tests |
| Production | app.iafactory.ai | Live |

### Docker Compose (Production)
```yaml
services:
  frontend:
    image: iafactory/frontend:latest
    ports: ["3000:80"]

  backend:
    image: iafactory/backend:latest
    ports: ["8000:8000"]
    environment:
      - DATABASE_URL=postgresql://...

  chromadb:
    image: chromadb/chroma:latest
    volumes: ["./chroma_data:/chroma/chroma"]

  ollama:
    image: ollama/ollama:latest
    volumes: ["./ollama_data:/root/.ollama"]
```

### Monitoring
- **Logs**: Loki + Grafana
- **Metrics**: Prometheus + Grafana
- **APM**: Sentry
- **Uptime**: Uptime Robot

## Prérequis Serveur

### Minimum (Production)
- CPU: 4 cores
- RAM: 16 GB
- SSD: 100 GB
- GPU: Non requis (CPU inference)

### Recommandé (Scale)
- CPU: 8 cores
- RAM: 32 GB
- SSD: 500 GB
- GPU: NVIDIA RTX 3060+ (optionnel)

## Support Multilingue

### Langues Supportées
| Code | Langue | Direction | Status |
|------|--------|-----------|--------|
| ar | Arabe | RTL | ✅ |
| fr | Français | LTR | ✅ |
| en | Anglais | LTR | ✅ |

### Implémentation i18n
- Frontend: react-i18next
- Backend: Babel
- Base de données: Colonnes multilingues
- RAG: Embeddings multilingues

---

*Documentation technique v1.0 - Décembre 2025*
