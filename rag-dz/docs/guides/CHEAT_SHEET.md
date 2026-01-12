# 🎯 Cheat Sheet RAG.dz

Toutes les commandes et URLs essentielles en un seul endroit.

## 🚀 Démarrage Rapide

```bash
# Première fois
cp .env.example .env
nano .env              # Configurer secrets
make start             # Démarrer

# Tests
python test_all_interfaces.py
make health
```

---

## 🌐 URLs Essentielles

| Service | URL | Login |
|---------|-----|-------|
| 🎨 **Frontend** | http://localhost:5173 | - |
| ⚡ **API** | http://localhost:8180 | API Key |
| 📚 **API Docs** | http://localhost:8180/docs | - |
| 📊 **Grafana** | http://localhost:3001 | admin/admin |
| 🔥 **Prometheus** | http://localhost:9090 | - |
| 🔍 **Qdrant** | http://localhost:6333/dashboard | - |

---

## 🔧 Commandes Make

### Gestion Services
```bash
make start          # ▶️  Démarrer
make stop           # ⏹️  Arrêter
make restart        # 🔄 Redémarrer
make status         # 📊 Status
make clean          # 🧹 Nettoyer
```

### Logs
```bash
make logs           # Tous les logs
make logs-backend   # Backend
make logs-frontend  # Frontend
make logs-db        # PostgreSQL
```

### Tests
```bash
make test           # Tous les tests
make test-backend   # Tests backend
make test-frontend  # Tests frontend
make test-security  # Tests sécurité
```

### Base de Données
```bash
make db-shell       # Shell PostgreSQL
make backup-db      # Backup DB
make restore-db     # Restore (FILE=backup.sql)
```

### Cache
```bash
make redis-cli      # Redis CLI
make cache-stats    # Stats cache
make clean-cache    # Vider cache
```

### Monitoring
```bash
make health         # Health check
make metrics        # Voir métriques
make grafana-open   # Ouvrir Grafana
make prometheus-open # Ouvrir Prometheus
```

### Dev
```bash
make dev-backend    # Dev backend (hot reload)
make dev-frontend   # Dev frontend (hot reload)
```

---

## 🐳 Commandes Docker Compose

```bash
# Démarrage
docker-compose up -d                    # Tout démarrer
docker-compose up -d backend frontend   # Services spécifiques

# Status
docker-compose ps                       # Status
docker-compose logs                     # Logs
docker-compose logs -f backend          # Logs suivi

# Gestion
docker-compose restart backend          # Redémarrer service
docker-compose stop                     # Arrêter
docker-compose down                     # Arrêter + supprimer
docker-compose down -v                  # + supprimer volumes
```

---

## 🔑 Tests API (curl)

### Health Check
```bash
curl http://localhost:8180/health
```

### Query (avec cache)
```bash
curl -X POST http://localhost:8180/api/query \
  -H "X-API-Key: test-api-key-ragdz-2024" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Comment fonctionne le RAG?",
    "max_results": 5,
    "use_cache": true
  }'
```

### Recherche Paginée
```bash
curl -X GET "http://localhost:8180/api/search?query=test&page=1&page_size=10" \
  -H "X-API-Key: test-api-key-ragdz-2024"
```

### Métriques
```bash
curl http://localhost:8180/metrics | head -20
```

---

## 💾 Commandes PostgreSQL

```bash
# Connexion
docker-compose exec postgres psql -U postgres -d archon

# Dans psql:
\dt                              # Lister tables
\d tenants                       # Structure table
SELECT COUNT(*) FROM tenants;    # Compter
SELECT * FROM api_keys LIMIT 5;  # Voir données
\q                               # Quitter
```

### Backup/Restore
```bash
# Backup
docker-compose exec postgres pg_dump -U postgres archon > backup.sql

# Restore
docker-compose exec -T postgres psql -U postgres archon < backup.sql
```

---

## 🔴 Commandes Redis

```bash
# Connexion
docker-compose exec redis redis-cli

# Dans redis-cli:
PING                    # Test
KEYS *                  # Toutes les clés
KEYS emb:*              # Clés embeddings
KEYS query:*            # Clés queries
GET emb:abc123          # Voir valeur
DBSIZE                  # Nombre de clés
INFO stats              # Statistiques
FLUSHALL                # ⚠️ Vider tout
exit                    # Quitter
```

---

## 🔍 Commandes Qdrant

```bash
# Health
curl http://localhost:6333/health

# Collections
curl http://localhost:6333/collections

# Stats d'une collection
curl http://localhost:6333/collections/docs_tenant-id
```

---

## 📊 Requêtes Prometheus (PromQL)

Dans Prometheus UI (http://localhost:9090/graph) :

```promql
# Services actifs
up

# Total requêtes HTTP
http_requests_total

# Taux de requêtes/sec
rate(http_requests_total[5m])

# Latence P95
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Taux d'erreurs
rate(http_requests_total{status=~"5.."}[5m])

# Cache hit rate
rate(cache_hits_total[5m]) / (rate(cache_hits_total[5m]) + rate(cache_misses_total[5m]))

# Rate limiting
rate(rate_limit_exceeded_total[5m])
```

---

## 🧪 Tests Python

```bash
# Script automatique
python test_all_interfaces.py

# Tests backend
cd rag-compat
pytest -v
pytest --cov=app
pytest -m security

# Tests frontend
cd rag-ui
npm test
npm run test:coverage
```

---

## ⚙️ Variables d'Environnement

### Backend (.env)
```env
# Sécurité (OBLIGATOIRE)
API_SECRET_KEY=<généré-avec-openssl-rand-hex-32>
POSTGRES_PASSWORD=<mot-de-passe-fort>
ALLOWED_ORIGINS=http://localhost:5173

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000

# Environment
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### Frontend (rag-ui/.env)
```env
VITE_API_URL=http://localhost:8180
VITE_API_KEY=
```

---

## 🔒 Sécurité

### Générer Secret
```bash
openssl rand -hex 32
```

### Vérifier Rate Limiting
```bash
for i in {1..70}; do
  curl -s -o /dev/null -w "%{http_code}\n" \
    -H "X-API-Key: test-api-key-ragdz-2024" \
    http://localhost:8180/health
  sleep 0.5
done
```

### Tester CORS
```bash
curl -H "Origin: http://localhost:5173" \
  -H "Access-Control-Request-Method: POST" \
  -X OPTIONS \
  http://localhost:8180/api/query
```

---

## 📈 Performance

### Benchmark avec ab
```bash
ab -n 100 -c 10 \
  -H "X-API-Key: test-api-key-ragdz-2024" \
  http://localhost:8180/health
```

### Tester Cache
```bash
# 1ère requête (sans cache)
time curl -X POST http://localhost:8180/api/query \
  -H "X-API-Key: test-api-key-ragdz-2024" \
  -d '{"query":"test","use_cache":true}'

# 2ème requête (avec cache)
time curl -X POST http://localhost:8180/api/query \
  -H "X-API-Key: test-api-key-ragdz-2024" \
  -d '{"query":"test","use_cache":true}'
```

---

## 🚨 Dépannage

### Vérifier tout
```bash
make status
make health
docker-compose ps
docker-compose logs
```

### Redémarrer service
```bash
docker-compose restart backend
docker-compose restart frontend
docker-compose restart postgres
```

### Cleanup complet
```bash
docker-compose down -v
docker-compose up -d
```

### Rebuild
```bash
docker-compose up -d --build
```

---

## 📝 Logs Utiles

### Filtrer logs
```bash
# Erreurs uniquement
docker-compose logs backend | grep -i error

# Dernier 100 lignes
docker-compose logs --tail=100 backend

# Suivre en temps réel
docker-compose logs -f backend
```

---

## 🎯 Checklist Rapide

```bash
# 1. Tout démarrer
make start

# 2. Vérifier status
make status

# 3. Tester
python test_all_interfaces.py

# 4. Ouvrir interfaces
# - Frontend: http://localhost:5173
# - API Docs: http://localhost:8180/docs
# - Grafana: http://localhost:3001
```

---

## 📚 Documentation

| Fichier | Description |
|---------|-------------|
| README.md | Documentation principale |
| QUICKSTART.md | Démarrage rapide |
| IMPROVEMENTS.md | Détails améliorations |
| TESTING_GUIDE.md | Guide de test complet |
| HOW_TO_TEST.md | Instructions test |
| CHEAT_SHEET.md | Ce fichier |

---

## 🆘 Aide Rapide

```bash
# Aide Make
make help

# Status services
docker-compose ps

# Logs d'un service
docker-compose logs backend

# Shell PostgreSQL
make db-shell

# Redis CLI
make redis-cli

# Vider cache
make clean-cache

# Health check
make health
```

---

**Imprimez cette page et gardez-la à portée de main ! 📄**
