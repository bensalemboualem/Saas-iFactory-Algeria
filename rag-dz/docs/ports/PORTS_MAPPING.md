# 🌐 RAG.dz - Plan d'Attribution des Ports

## 📊 Vue d'ensemble

Chaque interface a maintenant son **port dédié** pour permettre le testing simultané de toutes les interfaces.

---

## 🎯 Interfaces Frontend

| Interface | Port | Container | Technologie | Commande |
|-----------|------|-----------|-------------|----------|
| **Archon UI** | **3737** | ragdz-frontend | React 18 + Vite + TanStack Query | `docker-compose up -d frontend` |
| **RAG-UI Simple** | **5173** | ragdz-rag-ui | React 19 + CRA | `docker-compose up -d rag-ui` |
| **Bolt.diy** | **5174** | ragdz-bolt-diy | Remix + WebContainer | `docker-compose --profile bolt up -d` |

---

## ⚙️ Backend & API

| Service | Port | Container | Description | URL |
|---------|------|-----------|-------------|-----|
| **Backend API** | **8180** | ragdz-backend | FastAPI + RAG Engine | http://localhost:8180/docs |
| **Metrics** | **8180** | ragdz-backend | Prometheus metrics endpoint | http://localhost:8180/metrics |

---

## 🗄️ Bases de Données

| Service | Port | Container | Description | Accès |
|---------|------|-----------|-------------|-------|
| **PostgreSQL** | **5432** | ragdz-postgres | Base principale (pgvector) | `psql -h localhost -U postgres -d archon` |
| **Redis** | **6379** | ragdz-redis | Cache & Queue | `redis-cli -h localhost` |
| **Qdrant** | **6333** | ragdz-qdrant | Vector Database | http://localhost:6333/dashboard |
| **Qdrant gRPC** | **6334** | ragdz-qdrant | gRPC endpoint | - |

---

## 📊 Monitoring & Observability

| Service | Port | Container | Description | Credentials |
|---------|------|-----------|-------------|-------------|
| **Grafana** | **3001** | ragdz-grafana | Dashboards & Viz | admin / admin |
| **Prometheus** | **9090** | ragdz-prometheus | Metrics Collection | - |
| **Postgres Exporter** | **9187** | ragdz-postgres-exporter | PG Metrics | - |
| **Redis Exporter** | **9121** | ragdz-redis-exporter | Redis Metrics | - |

---

## 🚀 Commandes de Démarrage

### Toutes les interfaces principales
```bash
docker-compose up -d
```

### Avec Bolt.diy (AI Code Editor)
```bash
docker-compose --profile bolt up -d
```

### Interface par interface
```bash
# Archon UI uniquement
docker-compose up -d frontend

# RAG-UI Simple uniquement
docker-compose up -d rag-ui

# Bolt.diy uniquement
docker-compose --profile bolt up -d bolt-diy
```

---

## 🧪 Testing Simultané

Ouvrir ces URLs dans différents onglets :

### Interfaces Utilisateur
1. **Archon UI** → http://localhost:3737
2. **RAG-UI** → http://localhost:5173
3. **Bolt.diy** → http://localhost:5174

### API & Docs
4. **Swagger UI** → http://localhost:8180/docs
5. **API Health** → http://localhost:8180/health

### Monitoring
6. **Grafana** → http://localhost:3001 (admin/admin)
7. **Prometheus** → http://localhost:9090
8. **Qdrant** → http://localhost:6333/dashboard

---

## 📝 Configuration des Ports

### Modifier un port (si conflit)

Éditer `docker-compose.yml` :

```yaml
services:
  rag-ui:
    ports:
      - "5173:5173"  # HOST:CONTAINER
      #  ^^^^  ^^^^
      #  |     └─ Port interne du container (ne pas changer)
      #  └─ Port externe (modifiable)
```

### Ports Réservés par le Système

**Ne PAS utiliser :**
- `80`, `443` - HTTP/HTTPS standard (souvent réservés)
- `3000` - Souvent utilisé par dev servers
- `5000` - Flask/Python dev servers

---

## 🔍 Vérification des Ports

### Windows
```powershell
# Voir tous les ports en écoute
netstat -ano | findstr "LISTENING"

# Vérifier un port spécifique
netstat -ano | findstr ":3737"
```

### Linux/Mac
```bash
# Voir tous les ports
netstat -tuln | grep LISTEN

# Vérifier un port spécifique
lsof -i :3737
```

### Docker
```bash
# Voir les ports mappés
docker-compose ps

# Ports d'un container spécifique
docker port ragdz-frontend
```

---

## 🎯 Plan de Résolution de Conflits

Si un port est déjà utilisé :

1. **Identifier le processus**
   ```bash
   # Windows
   netstat -ano | findstr ":PORT"

   # Linux/Mac
   lsof -i :PORT
   ```

2. **Options**
   - Arrêter l'application qui utilise le port
   - Changer le port dans `docker-compose.yml`
   - Utiliser un autre profil Docker

3. **Exemple de changement**
   ```yaml
   # Si 5173 est occupé, utiliser 5175
   rag-ui:
     ports:
       - "5175:5173"  # Nouveau port externe
   ```

---

## 📦 Profils Docker Compose

### Profil `default` (sans option)
- ✅ Archon UI (3737)
- ✅ RAG-UI Simple (5173)
- ✅ Backend (8180)
- ✅ Toutes les DBs
- ✅ Monitoring

### Profil `bolt`
```bash
docker-compose --profile bolt up -d
```
- ✅ Tout le profil default
- ✅ Bolt.diy (5174)

---

## 🔐 Ports & Sécurité

### En Production

**NE PAS exposer publiquement :**
- PostgreSQL (5432)
- Redis (6379)
- Prometheus (9090)
- Exporters (9121, 9187)

**Exposer via reverse proxy uniquement :**
- Interfaces Frontend (3737, 5173, 5174)
- API Backend (8180)
- Grafana (3001)

### Exemple Nginx
```nginx
# Exposer uniquement Archon UI
location / {
    proxy_pass http://localhost:3737;
}

# Exposer API
location /api {
    proxy_pass http://localhost:8180;
}
```

---

## 📊 Plan Complet d'Attribution

```
┌─────────────────────────────────────────────────┐
│           FRONTENDS (3000-5999)                 │
├─────────────────────────────────────────────────┤
│  3737  →  Archon UI (Principal)                │
│  3001  →  Grafana (Monitoring UI)              │
│  5173  →  RAG-UI Simple                        │
│  5174  →  Bolt.diy (AI Code Editor)            │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│           BACKENDS (8000-8999)                  │
├─────────────────────────────────────────────────┤
│  8180  →  FastAPI Backend + Metrics            │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│           DATABASES (5000-6999)                 │
├─────────────────────────────────────────────────┤
│  5432  →  PostgreSQL                           │
│  6333  →  Qdrant (HTTP)                        │
│  6334  →  Qdrant (gRPC)                        │
│  6379  →  Redis                                │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│           MONITORING (9000-9999)                │
├─────────────────────────────────────────────────┤
│  9090  →  Prometheus                           │
│  9121  →  Redis Exporter                       │
│  9187  →  Postgres Exporter                    │
└─────────────────────────────────────────────────┘
```

---

## 🎉 Avantages de cette Architecture

✅ **Testing Simultané** - Toutes les interfaces accessibles en même temps
✅ **Pas de Conflits** - Chaque service a son port dédié
✅ **Facile à Mémoriser** - Organisation logique par plage
✅ **Scalable** - Facile d'ajouter de nouveaux services
✅ **Production Ready** - Séparation claire frontend/backend/data

---

**Made with ❤️ for Algeria 🇩🇿**
