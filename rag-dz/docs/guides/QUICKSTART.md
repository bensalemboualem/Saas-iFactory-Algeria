# 🚀 Guide de Démarrage Ultra-Rapide

## Installation en 60 secondes

```bash
# 1. Configuration
cp .env.example .env
nano .env  # Éditer API_SECRET_KEY et POSTGRES_PASSWORD

# 2. Démarrer
docker-compose up -d

# 3. Vérifier
curl http://localhost:8180/health
```

## URLs Essentielles

| Service | URL | Credentials |
|---------|-----|-------------|
| 🎨 Frontend | http://localhost:5173 | - |
| ⚡ API Backend | http://localhost:8180 | X-API-Key header |
| 📚 API Docs | http://localhost:8180/docs | - |
| 📊 Grafana | http://localhost:3001 | admin/admin |
| 🔥 Prometheus | http://localhost:9090 | - |

## Commandes Make les Plus Utiles

```bash
make help           # 📋 Liste toutes les commandes
make start          # ▶️  Démarrer
make stop           # ⏹️  Arrêter
make restart        # 🔄 Redémarrer
make logs           # 📝 Voir logs
make test           # 🧪 Tests
make health         # ❤️  Santé
make clean          # 🧹 Nettoyer
```

## Test Rapide de l'API

### 1. Health Check
```bash
curl http://localhost:8180/health
```

### 2. Recherche (avec API key)
```bash
curl -X POST http://localhost:8180/api/query \
  -H "X-API-Key: test-api-key-ragdz-2024" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Comment fonctionne le RAG?",
    "max_results": 5
  }'
```

### 3. Métriques
```bash
curl http://localhost:8180/metrics | head -20
```

## Dépannage Express

### Backend ne démarre pas
```bash
docker-compose logs backend
# Vérifier POSTGRES_URL dans .env
```

### Frontend erreur 502
```bash
docker-compose restart frontend
# Vérifier VITE_API_URL dans .env
```

### DB connection failed
```bash
docker-compose up -d postgres
# Attendre 30s pour healthcheck
docker-compose restart backend
```

### Cache Redis non disponible
```bash
docker-compose up -d redis
docker-compose exec redis redis-cli ping
# Doit retourner: PONG
```

## Configuration Minimale .env

```env
# Secrets (OBLIGATOIRE)
API_SECRET_KEY=<généré-avec-openssl-rand-hex-32>
POSTGRES_PASSWORD=<mot-de-passe-fort>

# Reste: valeurs par défaut OK pour dev
ENVIRONMENT=development
```

## Prochaines Étapes

1. ✅ Services démarrés → Configurer API key
2. ✅ API key configurée → Tester upload de documents
3. ✅ Documents uploadés → Tester recherche sémantique
4. ✅ Recherche OK → Explorer Grafana dashboards
5. ✅ Monitoring OK → Passer en production

## Aide Rapide

```bash
# Logs en temps réel
make logs-backend

# Stats Redis
make cache-stats

# Status services
make status

# Shell PostgreSQL
make db-shell

# Vider cache
make clean-cache
```

---

**En cas de problème**: Voir [README.md](README.md) ou [IMPROVEMENTS.md](IMPROVEMENTS.md)
