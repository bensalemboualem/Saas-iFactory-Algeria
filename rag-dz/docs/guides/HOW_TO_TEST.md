# 🧪 Comment Tester Toutes les Interfaces

## 🚀 Méthode Ultra-Rapide (Recommandée)

### 1. Démarrer les Services

```bash
# Avec Make (recommandé)
make start

# OU avec Docker Compose
docker-compose up -d
```

### 2. Test Automatique Python

```bash
# Installer requests si nécessaire
pip install requests

# Lancer le script de test
python test_all_interfaces.py
```

**Ce script teste automatiquement :**
- ✅ Backend API (health, endpoints, sécurité)
- ✅ Frontend (accessibilité)
- ✅ PostgreSQL (via backend)
- ✅ Redis Cache (performance)
- ✅ Qdrant Vector DB
- ✅ Prometheus (monitoring)
- ✅ Grafana (dashboards)

**Résultat attendu :**
```
╔═══════════════════════════════════════════════════════════╗
║        RAG.dz - Test Automatique des Interfaces          ║
╚═══════════════════════════════════════════════════════════╝

🔧 TESTS BACKEND API
============================================================
✓ Backend Health Check                                [PASS]
✓ Prometheus Metrics                                  [PASS]
✓ Swagger Documentation                               [PASS]
✓ Embed Endpoint (with API key)                       [PASS]
✓ API Key Required (security)                         [PASS]
✓ Query Endpoint                                      [PASS]
...

📋 RÉSUMÉ DES TESTS
============================================================
Total tests:     25
Passed:          25
Failed:          0
Success rate:    100.0%

✓ ALL TESTS PASSED!
```

---

## 🌐 Méthode Manuelle (Navigateur)

### Ouvrir Toutes les Interfaces

**Dans votre navigateur, ouvrir ces onglets :**

1. **Frontend** → http://localhost:5173
   - Interface utilisateur React
   - Tester la recherche, navigation

2. **API Documentation** → http://localhost:8180/docs
   - Swagger UI interactif
   - Tester les endpoints directement

3. **Prometheus** → http://localhost:9090
   - Métriques système
   - Aller dans Graph, taper: `http_requests_total`

4. **Grafana** → http://localhost:3001
   - Login: admin/admin
   - Dashboards de monitoring

5. **Qdrant Dashboard** → http://localhost:6333/dashboard
   - Collections de vecteurs
   - Statistiques

---

## 📱 Tests Rapides par Interface

### 🔧 Backend API

```bash
# 1. Health check
curl http://localhost:8180/health

# 2. Tester avec API key
curl -X POST http://localhost:8180/api/query \
  -H "X-API-Key: test-api-key-ragdz-2024" \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "max_results": 5}'

# 3. Voir les métriques
curl http://localhost:8180/metrics | head -20
```

### 🎨 Frontend

```bash
# Ouvrir dans le navigateur
open http://localhost:5173  # macOS
xdg-open http://localhost:5173  # Linux
start http://localhost:5173  # Windows
```

**Vérifications:**
- [ ] Page charge sans erreur
- [ ] Ouvrir DevTools (F12)
- [ ] Onglet Console: pas d'erreurs rouges
- [ ] Onglet Network: requêtes vers API fonctionnent

### 🗄️ PostgreSQL

```bash
# Connexion via Make
make db-shell

# OU Docker exec
docker-compose exec postgres psql -U postgres -d archon

# Dans psql:
\dt                    # Lister tables
SELECT COUNT(*) FROM tenants;
SELECT COUNT(*) FROM api_keys;
\q                     # Quitter
```

### 💾 Redis

```bash
# Connexion via Make
make redis-cli

# OU Docker exec
docker-compose exec redis redis-cli

# Dans redis-cli:
PING                   # Doit retourner PONG
KEYS *                 # Voir toutes les clés
INFO stats             # Statistiques
exit                   # Quitter
```

### 🔍 Qdrant

```bash
# Health check
curl http://localhost:6333/health

# Collections
curl http://localhost:6333/collections

# OU ouvrir dashboard
open http://localhost:6333/dashboard
```

### 📊 Prometheus

```bash
# Health check
curl http://localhost:9090/-/healthy

# OU navigateur
open http://localhost:9090
```

**Dans l'UI:**
1. Aller dans "Graph"
2. Requêtes à tester:
   - `up` (services actifs)
   - `http_requests_total`
   - `rate(http_requests_total[5m])`

### 📈 Grafana

```bash
# Ouvrir
open http://localhost:3001

# Login: admin / admin
```

**Vérifications:**
1. Configuration → Data Sources
2. Vérifier que Prometheus est connecté (vert)
3. Cliquer "Test" → "Data source is working"

---

## 🔥 Tests de Performance

### Test Cache Redis

```bash
# Faire 2 requêtes identiques
echo "Requête 1 (sans cache):"
time curl -X POST http://localhost:8180/api/query \
  -H "X-API-Key: test-api-key-ragdz-2024" \
  -H "Content-Type: application/json" \
  -d '{"query": "performance test", "use_cache": true}'

echo "\nRequête 2 (avec cache):"
time curl -X POST http://localhost:8180/api/query \
  -H "X-API-Key: test-api-key-ragdz-2024" \
  -H "Content-Type: application/json" \
  -d '{"query": "performance test", "use_cache": true}'
```

**Attendu:** 2ème requête ~10x plus rapide

### Test Rate Limiting

```bash
# Faire 70 requêtes rapidement
for i in {1..70}; do
  echo "Request $i"
  curl -s -o /dev/null -w "Status: %{http_code}\n" \
    -H "X-API-Key: test-api-key-ragdz-2024" \
    http://localhost:8180/health
  sleep 0.5
done
```

**Attendu:** Après ~60 requêtes → Status: 429

---

## 📊 Checklist Rapide

Cocher au fur et à mesure :

### Services Running
- [ ] `docker-compose ps` → tous les services "Up"
- [ ] Pas d'erreurs dans `docker-compose logs`

### Backend
- [ ] http://localhost:8180/health → 200 OK
- [ ] http://localhost:8180/docs → Swagger UI
- [ ] API key fonctionne
- [ ] Rate limiting actif

### Frontend
- [ ] http://localhost:5173 → Page charge
- [ ] Pas d'erreurs console (F12)
- [ ] Requêtes API fonctionnent

### Databases
- [ ] PostgreSQL accessible (`make db-shell`)
- [ ] Redis accessible (`make redis-cli`)
- [ ] Qdrant accessible (http://localhost:6333/health)

### Monitoring
- [ ] Prometheus http://localhost:9090 → Targets UP
- [ ] Grafana http://localhost:3001 → Login OK

---

## 🚨 Si Quelque Chose Ne Marche Pas

### 1. Vérifier les Logs

```bash
# Tous les services
make logs

# Service spécifique
docker-compose logs backend
docker-compose logs frontend
docker-compose logs postgres
```

### 2. Redémarrer

```bash
# Tout redémarrer
make restart

# Service spécifique
docker-compose restart backend
```

### 3. Status Services

```bash
make status
# Tous doivent être "Up (healthy)" ou "Up"
```

### 4. Cleanup Complet

```bash
# Arrêter et nettoyer
make clean

# Redémarrer from scratch
make start
```

---

## 📚 Documentation Complète

Pour des tests plus approfondis, voir :
- **TESTING_GUIDE.md** - Guide complet de test
- **README.md** - Documentation principale
- **QUICKSTART.md** - Démarrage rapide

---

## 💡 Résumé Ultra-Court

```bash
# 1. Démarrer
make start

# 2. Tester automatiquement
python test_all_interfaces.py

# 3. Ou tester manuellement
# - Frontend: http://localhost:5173
# - API: http://localhost:8180/docs
# - Grafana: http://localhost:3001
# - Prometheus: http://localhost:9090

# 4. Vérifier
make health
make status
```

**C'est tout ! 🎉**
