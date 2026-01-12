# 🧪 Guide de Test Complet - RAG.dz

Guide étape par étape pour tester toutes les interfaces du projet.

## 📋 Table des Matières

1. [Préparation](#préparation)
2. [Test Backend API](#1-test-backend-api)
3. [Test Frontend UI](#2-test-frontend-ui)
4. [Test Base de Données](#3-test-base-de-données)
5. [Test Cache Redis](#4-test-cache-redis)
6. [Test Qdrant Vector DB](#5-test-qdrant-vector-db)
7. [Test Monitoring](#6-test-monitoring-prometheus--grafana)
8. [Tests Automatisés](#7-tests-automatisés)
9. [Test de Charge](#8-test-de-charge)
10. [Dépannage](#dépannage)

---

## Préparation

### 1. Démarrer tous les services

```bash
# Méthode 1: Avec Make
make start
make status

# Méthode 2: Docker Compose directement
docker-compose up -d
docker-compose ps
```

Vérifiez que tous les services sont `healthy` ou `running`.

### 2. Vérifier les logs

```bash
# Tous les services
make logs

# Backend uniquement
make logs-backend

# Frontend uniquement
make logs-frontend
```

---

## 1. Test Backend API

### A. Health Check

```bash
# Test simple
curl http://localhost:8180/health

# Ou avec Make
make health
```

**Résultat attendu:**
```json
{
  "status": "healthy",
  "timestamp": 1699876543.21,
  "service": "RAG.dz"
}
```

### B. Documentation API Interactive

**Ouvrir dans le navigateur:**
- Swagger UI: http://localhost:8180/docs
- ReDoc: http://localhost:8180/redoc

**Test via Swagger UI:**

1. Ouvrir http://localhost:8180/docs
2. Cliquer sur `GET /health`
3. Cliquer "Try it out"
4. Cliquer "Execute"
5. Vérifier la réponse 200

### C. Test des Endpoints avec curl

#### Test Embed (avec API key)

```bash
curl -X POST http://localhost:8180/api/test/embed \
  -H "X-API-Key: test-api-key-ragdz-2024" \
  -H "Content-Type: application/json"
```

**Résultat attendu:**
```json
{
  "tenant": "Test Tenant",
  "queries": ["Hello world", "Bonjour le monde", "مرحبا بالعالم"],
  "embeddings_count": 3,
  "vector_size": 768,
  "collection_created": "test_tenant-id"
}
```

#### Test Query (recherche sémantique)

```bash
curl -X POST http://localhost:8180/api/query \
  -H "X-API-Key: test-api-key-ragdz-2024" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Comment fonctionne le RAG?",
    "max_results": 5,
    "score_threshold": 0.3,
    "use_cache": true
  }'
```

#### Test Pagination

```bash
curl -X GET "http://localhost:8180/api/search?query=test&page=1&page_size=10" \
  -H "X-API-Key: test-api-key-ragdz-2024"
```

**Résultat attendu:**
```json
{
  "items": [...],
  "pagination": {
    "current_page": 1,
    "page_size": 10,
    "total_items": 0,
    "total_pages": 0,
    "has_previous": false,
    "has_next": false
  }
}
```

### D. Test Rate Limiting

```bash
# Script pour tester rate limiting
for i in {1..70}; do
  echo "Request $i"
  curl -s -w "\nStatus: %{http_code}\n" \
    -H "X-API-Key: test-api-key-ragdz-2024" \
    http://localhost:8180/health
  sleep 0.5
done
```

Après ~60 requêtes, vous devriez voir:
```
Status: 429
{"error":"Rate limit exceeded","retry_after":30}
```

### E. Test Métriques Prometheus

```bash
# Voir les métriques
curl http://localhost:8180/metrics

# Filtrer certaines métriques
curl -s http://localhost:8180/metrics | grep http_requests_total
curl -s http://localhost:8180/metrics | grep cache_hits
```

### F. Test Upload Document (si implémenté)

```bash
curl -X POST http://localhost:8180/api/upload \
  -H "X-API-Key: test-api-key-ragdz-2024" \
  -F "file=@test-document.pdf"
```

---

## 2. Test Frontend UI

### A. Accès Frontend

**Ouvrir dans le navigateur:**
```
http://localhost:5173
```

### B. Tests Manuels UI

#### 1. Page d'accueil
- [ ] La page charge sans erreur
- [ ] Pas d'erreurs dans la Console (F12)
- [ ] Navigation fonctionne

#### 2. Test de recherche (si disponible)
- [ ] Saisir une query dans le champ de recherche
- [ ] Cliquer "Search"
- [ ] Vérifier les résultats affichés
- [ ] Vérifier la pagination

#### 3. Configuration API Key
- [ ] Ouvrir les DevTools (F12)
- [ ] Aller dans Application > Session Storage
- [ ] Ajouter `apiKey` = `test-api-key-ragdz-2024`
- [ ] Rafraîchir la page
- [ ] Vérifier que l'API key est utilisée

#### 4. Test Network
- [ ] Ouvrir DevTools > Network
- [ ] Faire une recherche
- [ ] Vérifier les requêtes:
  - Headers contiennent `X-API-Key`
  - Status code 200 ou 429
  - Réponse JSON valide

### C. Test Responsive

**Tester différentes tailles:**
```
Desktop:  1920x1080
Tablet:   768x1024
Mobile:   375x667
```

Dans Chrome DevTools:
1. F12 > Toggle device toolbar (Ctrl+Shift+M)
2. Sélectionner différents devices
3. Vérifier que l'UI s'adapte

### D. Test Performance Frontend

**Lighthouse Audit:**
1. Ouvrir Chrome DevTools (F12)
2. Aller dans l'onglet "Lighthouse"
3. Sélectionner:
   - Performance
   - Accessibility
   - Best Practices
   - SEO
4. Cliquer "Analyze page load"
5. Vérifier les scores

**Objectifs:**
- Performance: >70
- Accessibility: >90
- Best Practices: >90

---

## 3. Test Base de Données

### A. Connexion PostgreSQL

```bash
# Méthode 1: Via Make
make db-shell

# Méthode 2: Docker exec
docker-compose exec postgres psql -U postgres -d archon
```

### B. Vérifier les Tables

```sql
-- Lister toutes les tables
\dt

-- Voir structure table tenants
\d tenants

-- Voir structure table api_keys
\d api_keys

-- Voir structure table usage_events
\d usage_events
```

**Tables attendues:**
- `tenants`
- `api_keys`
- `usage_events`

### C. Requêtes de Test

```sql
-- Compter les tenants
SELECT COUNT(*) FROM tenants;

-- Voir les tenants actifs
SELECT id, name, plan, status FROM tenants WHERE status = 'active';

-- Voir les API keys
SELECT id, name, plan, created_at, revoked
FROM api_keys
WHERE NOT revoked;

-- Voir les derniers événements d'usage
SELECT tenant_id, route, method, status_code, latency_ms, timestamp
FROM usage_events
ORDER BY timestamp DESC
LIMIT 10;
```

### D. Insérer Données de Test

```sql
-- Créer un tenant de test
INSERT INTO tenants (name, plan, status)
VALUES ('Test Company', 'pro', 'active');

-- Récupérer l'ID
SELECT id FROM tenants WHERE name = 'Test Company';

-- Créer une API key pour ce tenant
-- (Remplacer <tenant_id> par l'ID du tenant)
INSERT INTO api_keys (key_hash, tenant_id, name, plan)
VALUES (
  encode(sha256('test-api-key-123'), 'hex'),
  '<tenant_id>',
  'Test API Key',
  'pro'
);
```

### E. Vérifier Performance

```sql
-- Analyser une requête
EXPLAIN ANALYZE
SELECT * FROM usage_events
WHERE tenant_id = '<tenant_id>'
AND timestamp > NOW() - INTERVAL '1 day';

-- Vérifier les index
SELECT tablename, indexname, indexdef
FROM pg_indexes
WHERE schemaname = 'public';
```

### F. Backup & Restore

```bash
# Créer un backup
make backup-db
# Ou:
docker-compose exec postgres pg_dump -U postgres archon > backup.sql

# Restaurer (ATTENTION: écrase les données!)
make restore-db FILE=backup.sql
# Ou:
docker-compose exec -T postgres psql -U postgres archon < backup.sql
```

---

## 4. Test Cache Redis

### A. Connexion Redis CLI

```bash
# Méthode 1: Via Make
make redis-cli

# Méthode 2: Docker exec
docker-compose exec redis redis-cli
```

### B. Commandes Redis de Base

```bash
# Ping
PING
# Doit retourner: PONG

# Vérifier nombre de clés
DBSIZE

# Voir toutes les clés
KEYS *

# Voir les clés d'embeddings
KEYS emb:*

# Voir les clés de queries
KEYS query:*

# Voir une valeur
GET emb:abc123def456

# Voir infos serveur
INFO

# Voir stats
INFO stats
```

### C. Tester le Cache

**1. Faire une requête (génère cache):**
```bash
curl -X POST http://localhost:8180/api/query \
  -H "X-API-Key: test-api-key-ragdz-2024" \
  -H "Content-Type: application/json" \
  -d '{"query": "test cache", "use_cache": true}'
```

**2. Vérifier dans Redis:**
```bash
docker-compose exec redis redis-cli
> KEYS *
> GET query:<hash>
```

**3. Refaire la même requête:**
```bash
# Devrait être plus rapide (cache hit)
time curl -X POST http://localhost:8180/api/query \
  -H "X-API-Key: test-api-key-ragdz-2024" \
  -H "Content-Type: application/json" \
  -d '{"query": "test cache", "use_cache": true}'
```

Vérifier `"from_cache": true` dans la réponse.

### D. Statistiques Cache

```bash
# Via Make
make cache-stats

# Ou manuellement
docker-compose exec redis redis-cli INFO stats | grep keyspace
```

**Métriques importantes:**
- `keyspace_hits` - Cache hits
- `keyspace_misses` - Cache misses
- Hit rate = hits / (hits + misses)

### E. Vider le Cache

```bash
# Via Make
make clean-cache

# Ou manuellement
docker-compose exec redis redis-cli FLUSHALL
```

---

## 5. Test Qdrant Vector DB

### A. Vérifier Status Qdrant

```bash
# Health check
curl http://localhost:6333/health

# Collections
curl http://localhost:6333/collections
```

### B. Interface Web Qdrant

**Ouvrir dans le navigateur:**
```
http://localhost:6333/dashboard
```

### C. Créer une Collection de Test

```bash
curl -X PUT http://localhost:6333/collections/test_collection \
  -H "Content-Type: application/json" \
  -d '{
    "vectors": {
      "size": 768,
      "distance": "Cosine"
    }
  }'
```

### D. Insérer des Vecteurs

```bash
curl -X PUT http://localhost:6333/collections/test_collection/points \
  -H "Content-Type: application/json" \
  -d '{
    "points": [
      {
        "id": 1,
        "vector": [0.1, 0.2, 0.3, ...],
        "payload": {"text": "Test document 1"}
      }
    ]
  }'
```

### E. Recherche Vectorielle

```bash
curl -X POST http://localhost:6333/collections/test_collection/points/search \
  -H "Content-Type: application/json" \
  -d '{
    "vector": [0.1, 0.2, 0.3, ...],
    "limit": 5
  }'
```

### F. Statistiques Collection

```bash
curl http://localhost:6333/collections/test_collection
```

---

## 6. Test Monitoring (Prometheus & Grafana)

### A. Prometheus

**1. Ouvrir Prometheus:**
```
http://localhost:9090
```

**2. Tests de base:**
- [ ] Aller dans Status > Targets
- [ ] Vérifier que tous les targets sont UP
- [ ] Aller dans Graph

**3. Requêtes PromQL:**

```promql
# Total de requêtes HTTP
http_requests_total

# Taux de requêtes par seconde
rate(http_requests_total[5m])

# Latence P95
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Cache hit rate
rate(cache_hits_total[5m]) / (rate(cache_hits_total[5m]) + rate(cache_misses_total[5m]))

# Rate limit exceeded
rate(rate_limit_exceeded_total[5m])
```

**4. Tester les Alertes:**
```
http://localhost:9090/alerts
```

### B. Grafana

**1. Ouvrir Grafana:**
```
http://localhost:3001
```

**Login:** admin / admin

**2. Vérifier Datasource:**
- Configuration > Data Sources
- Vérifier que Prometheus est connecté (vert)
- Cliquer "Test" → Should see "Data source is working"

**3. Créer un Dashboard:**

1. Click "+" > Dashboard
2. Add new panel
3. Configurer une requête:
   - Datasource: Prometheus
   - Query: `rate(http_requests_total[5m])`
4. Cliquer "Apply"

**4. Importer Dashboard:**
1. Click "+" > Import
2. Enter dashboard ID ou upload JSON
3. Select Prometheus datasource

**Dashboards recommandés:**
- Node Exporter: 1860
- Redis: 11835
- PostgreSQL: 9628

---

## 7. Tests Automatisés

### A. Tests Backend (pytest)

```bash
# Tous les tests
cd rag-compat
pytest -v

# Avec coverage
pytest --cov=app --cov-report=html

# Tests spécifiques
pytest -m unit              # Tests unitaires
pytest -m integration       # Tests d'intégration
pytest -m security          # Tests de sécurité

# Un fichier spécifique
pytest tests/test_security.py -v

# Une fonction spécifique
pytest tests/test_security.py::TestRateLimiter::test_rate_limiter_allows_initial_requests -v

# Via Make
make test-backend
```

**Voir le rapport coverage:**
```bash
cd rag-compat
pytest --cov=app --cov-report=html
# Ouvrir: htmlcov/index.html
```

### B. Tests Frontend (Vitest)

```bash
# Tous les tests
cd rag-ui
npm run test

# Avec coverage
npm run test:coverage

# Watch mode
npm run test:watch

# UI mode
npm run test:ui

# Via Make
make test-frontend
```

**Voir le rapport coverage:**
```bash
cd rag-ui
npm run test:coverage
# Ouvrir: coverage/index.html
```

### C. Linting & Formatting

```bash
# Backend
cd rag-compat
ruff check .                # Linting
black . --check             # Format check

# Frontend
cd rag-ui
npm run lint                # ESLint
npm run lint:fix            # Auto-fix
```

---

## 8. Test de Charge

### A. Avec Apache Bench (ab)

```bash
# Installer ab
sudo apt-get install apache2-utils  # Ubuntu/Debian
brew install apache2                 # macOS

# Test simple (100 requêtes, 10 concurrent)
ab -n 100 -c 10 http://localhost:8180/health

# Test avec API key
ab -n 100 -c 10 \
  -H "X-API-Key: test-api-key-ragdz-2024" \
  http://localhost:8180/health
```

### B. Avec wrk

```bash
# Installer wrk
sudo apt-get install wrk  # Ubuntu
brew install wrk          # macOS

# Test 30 secondes, 10 threads, 100 connections
wrk -t10 -c100 -d30s http://localhost:8180/health

# Avec API key (créer script.lua)
echo '
wrk.headers["X-API-Key"] = "test-api-key-ragdz-2024"
' > script.lua

wrk -t10 -c100 -d30s -s script.lua http://localhost:8180/health
```

### C. Avec Locust

**1. Créer locustfile.py:**
```python
from locust import HttpUser, task, between

class RAGUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.client.headers = {
            "X-API-Key": "test-api-key-ragdz-2024"
        }

    @task(3)
    def health_check(self):
        self.client.get("/health")

    @task(1)
    def query(self):
        self.client.post("/api/query", json={
            "query": "test",
            "max_results": 5
        })
```

**2. Lancer Locust:**
```bash
pip install locust
locust -f locustfile.py --host=http://localhost:8180

# Ouvrir: http://localhost:8089
```

---

## 9. Tests de Sécurité

### A. Test Rate Limiting

```bash
# Script bash pour tester
for i in {1..100}; do
  response=$(curl -s -w "\n%{http_code}" \
    -H "X-API-Key: test-api-key-ragdz-2024" \
    http://localhost:8180/health)

  code=$(echo "$response" | tail -n1)

  if [ "$code" = "429" ]; then
    echo "Rate limited at request $i"
    echo "$response"
    break
  fi

  echo "Request $i: $code"
  sleep 0.1
done
```

### B. Test Sans API Key

```bash
# Devrait retourner 401
curl -v http://localhost:8180/api/query
```

### C. Test CORS

```bash
# From different origin
curl -H "Origin: http://evil.com" \
  -H "Access-Control-Request-Method: POST" \
  -X OPTIONS \
  http://localhost:8180/api/query
```

### D. Test Injection SQL

```bash
# Tester avec payload malicieux
curl -X POST http://localhost:8180/api/query \
  -H "X-API-Key: test-api-key-ragdz-2024" \
  -H "Content-Type: application/json" \
  -d '{"query": "test OR 1=1; DROP TABLE users--"}'

# Devrait être échappé/sanitisé
```

---

## 10. Checklist Complète

### Backend
- [ ] `/health` retourne 200
- [ ] `/metrics` retourne métriques Prometheus
- [ ] `/docs` charge Swagger UI
- [ ] API key requise sur endpoints protégés
- [ ] Rate limiting fonctionne (429 après limite)
- [ ] Cache Redis fonctionne (from_cache: true)
- [ ] Pagination retourne bon format
- [ ] Embeddings générés correctement
- [ ] Qdrant stocke/cherche vecteurs

### Frontend
- [ ] Page charge sans erreur
- [ ] Pas d'erreurs console
- [ ] API calls fonctionnent
- [ ] Headers X-API-Key envoyés
- [ ] Erreurs affichées proprement
- [ ] Responsive sur mobile/tablet
- [ ] Navigation fonctionne

### Base de Données
- [ ] PostgreSQL accessible
- [ ] Tables créées
- [ ] Index présents
- [ ] Queries performantes
- [ ] Backup/Restore fonctionne

### Cache
- [ ] Redis accessible
- [ ] Cache hit/miss trackés
- [ ] TTL respecté
- [ ] Invalidation fonctionne

### Monitoring
- [ ] Prometheus scrape targets UP
- [ ] Métriques visibles
- [ ] Alertes configurées
- [ ] Grafana accessible
- [ ] Dashboards fonctionnent

### Sécurité
- [ ] Pas de secrets exposés
- [ ] Rate limiting actif
- [ ] CORS configuré
- [ ] Headers sécurité présents
- [ ] Validation input

### Performance
- [ ] Latence API < 500ms (sans cache)
- [ ] Latence API < 50ms (avec cache)
- [ ] Cache hit rate > 30%
- [ ] 0 erreurs sous charge normale

---

## Dépannage

### Backend ne répond pas

```bash
# Vérifier logs
docker-compose logs backend

# Redémarrer
docker-compose restart backend

# Vérifier config
docker-compose exec backend env | grep -E "(POSTGRES|REDIS|QDRANT)"
```

### Frontend erreur 502

```bash
# Vérifier que backend est UP
curl http://localhost:8180/health

# Vérifier VITE_API_URL
docker-compose exec frontend env | grep VITE

# Rebuild
docker-compose up -d --build frontend
```

### PostgreSQL connection failed

```bash
# Vérifier status
docker-compose ps postgres

# Vérifier logs
docker-compose logs postgres

# Attendre healthcheck
sleep 30

# Redémarrer backend
docker-compose restart backend
```

### Redis not available

```bash
# Vérifier
docker-compose exec redis redis-cli ping

# Redémarrer
docker-compose restart redis

# L'app devrait continuer sans cache
```

### Qdrant not responding

```bash
# Vérifier
curl http://localhost:6333/health

# Logs
docker-compose logs qdrant

# Redémarrer
docker-compose restart qdrant
```

---

## 📊 Tableau de Bord de Test

| Service | URL | Test Commande | Status |
|---------|-----|---------------|--------|
| Backend | :8180 | `curl localhost:8180/health` | ⬜ |
| Frontend | :5173 | Ouvrir navigateur | ⬜ |
| PostgreSQL | :5432 | `make db-shell` | ⬜ |
| Redis | :6379 | `make redis-cli` | ⬜ |
| Qdrant | :6333 | `curl localhost:6333/health` | ⬜ |
| Prometheus | :9090 | Ouvrir navigateur | ⬜ |
| Grafana | :3001 | Ouvrir navigateur | ⬜ |

---

**Bon test ! 🧪**
