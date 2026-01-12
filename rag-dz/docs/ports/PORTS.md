# 🔌 Configuration des Ports RAG.dz

> **Dernière vérification:** 13 Novembre 2025
> **Statut:** ✅ Tous les ports sont LIBRES et FONCTIONNELS

## 📊 Vue d'Ensemble

| Service | Port | Protocole | Status | Description |
|---------|------|-----------|--------|-------------|
| **Frontend** | `5173` | HTTP | ✅ LIBRE | Interface utilisateur React |
| **Backend API** | `8180` | HTTP | ✅ LIBRE | API FastAPI principale |
| **PostgreSQL** | `5432` | TCP | ✅ LIBRE | Base de données |
| **Redis** | `6379` | TCP | ✅ LIBRE | Cache & Sessions |
| **Qdrant** | `6333` | HTTP | ✅ LIBRE | API Vector Database |
| **Qdrant gRPC** | `6334` | gRPC | ✅ LIBRE | Qdrant Protocol Buffers |
| **Prometheus** | `9090` | HTTP | ✅ LIBRE | Monitoring & Métriques |
| **Grafana** | `3001` | HTTP | ✅ LIBRE | Dashboards |
| **Postgres Exporter** | `9187` | HTTP | ✅ LIBRE | Métriques PostgreSQL |
| **Redis Exporter** | `9121` | HTTP | ✅ LIBRE | Métriques Redis |

---

## 🌐 Accès aux Services

### Services Utilisateur

```bash
# Frontend Interface
http://localhost:5173

# Backend API
http://localhost:8180
http://localhost:8180/docs  # Swagger UI
http://localhost:8180/redoc # ReDoc

# Grafana Dashboards
http://localhost:3001
# Login: admin / admin
```

### Services Données

```bash
# PostgreSQL
postgresql://postgres:ragdz2024secure@localhost:5432/archon

# Redis
redis://localhost:6379

# Qdrant Vector DB
http://localhost:6333
http://localhost:6333/dashboard
```

### Services Monitoring

```bash
# Prometheus
http://localhost:9090
http://localhost:9090/targets
http://localhost:9090/graph

# Metrics Endpoints
http://localhost:8180/metrics     # Backend
http://localhost:6333/metrics     # Qdrant
http://localhost:9187/metrics     # PostgreSQL
http://localhost:9121/metrics     # Redis
```

---

## 🔒 Sécurité des Ports

### Ports Publics (Accessibles depuis l'extérieur)
```
5173  - Frontend (Si production: nginx sur port 80/443)
8180  - Backend API (Nécessite API Key)
3001  - Grafana (Nécessite authentification)
```

### Ports Internes (Réseau Docker uniquement)
```
5432  - PostgreSQL (Accès base de données)
6379  - Redis (Cache interne)
6333  - Qdrant (Vector DB)
6334  - Qdrant gRPC
9090  - Prometheus (Monitoring)
9187  - Postgres Exporter
9121  - Redis Exporter
```

### Recommandations Production

```yaml
# Firewall Rules (UFW/iptables)
# Autoriser uniquement:
- 80/443 (HTTPS via reverse proxy)
- 22 (SSH admin)

# Bloquer l'accès direct à:
- 5432 (PostgreSQL)
- 6379 (Redis)
- Tous les autres ports internes
```

---

## 🔧 Configuration Docker Compose

```yaml
# Extrait de docker-compose.yml
ports:
  # Format: "HOST:CONTAINER"
  frontend:    "5173:5173"
  backend:     "8180:8180"
  postgres:    "5432:5432"
  redis:       "6379:6379"
  qdrant:      "6333:6333"
  qdrant:      "6334:6334"
  prometheus:  "9090:9090"
  grafana:     "3001:3000"    # 3001 externe, 3000 interne
  pg-exporter: "9187:9187"
  redis-exp:   "9121:9121"
```

---

## ⚠️ Conflits de Ports Potentiels

### Ports Communs à Vérifier

| Port | Service Alternatif Possible |
|------|----------------------------|
| `5173` | Autres apps Vite/React |
| `8180` | Serveurs web custom |
| `5432` | Autres instances PostgreSQL |
| `6379` | Autres instances Redis |
| `3001` | Autres dashboards |
| `9090` | Autres instances Prometheus |

### Commandes de Vérification

```bash
# Windows
netstat -ano | findstr ":<PORT>"

# Linux/Mac
lsof -i :<PORT>
netstat -tuln | grep <PORT>

# Docker
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

### En Cas de Conflit

Si un port est occupé, modifiez docker-compose.yml:

```yaml
# Exemple: Changer frontend de 5173 à 5174
frontend:
  ports:
    - "5174:5173"  # Nouveau port externe: 5174
```

---

## 🧪 Tests de Connectivité

### Script de Test Rapide

```bash
# Frontend
curl http://localhost:5173

# Backend Health
curl http://localhost:8180/health

# Qdrant Health
curl http://localhost:6333/healthz

# Prometheus
curl http://localhost:9090/-/healthy

# Grafana
curl http://localhost:3001/api/health
```

### Test Complet avec PowerShell

```powershell
# Exécuter le script de vérification
powershell -ExecutionPolicy Bypass -File find_free_ports.ps1
```

---

## 📝 Résolution de Problèmes

### Port Déjà Utilisé

**Symptôme:**
```
Error starting userland proxy: listen tcp 0.0.0.0:5173: bind: address already in use
```

**Solution:**
```bash
# 1. Identifier le processus
netstat -ano | findstr ":5173"

# 2. Tuer le processus (remplacer PID)
taskkill /PID <PID> /F

# 3. Ou changer le port dans docker-compose.yml
```

### Service Non Accessible

**Vérifications:**
```bash
# 1. Service running?
docker ps | grep ragdz

# 2. Port bien mappé?
docker port ragdz-backend

# 3. Logs du service
docker logs ragdz-backend
```

### Firewall Bloque l'Accès

**Windows:**
```powershell
# Ajouter règle firewall
New-NetFirewallRule -DisplayName "RAG.dz Frontend" -Direction Inbound -LocalPort 5173 -Protocol TCP -Action Allow
```

---

## 📊 Monitoring des Ports

### Dashboard Grafana

Accédez à http://localhost:3001 et consultez:
- **RAG.dz Overview** - Vue d'ensemble système
- **Network Metrics** - Trafic par port
- **Service Health** - Status de tous les services

### Prometheus Queries

```promql
# Requêtes par seconde sur chaque port
rate(http_requests_total[5m])

# Services up/down
up{job=~"ragdz-.*"}

# Latence par endpoint
http_request_duration_seconds{quantile="0.95"}
```

---

## 🚀 Mode Production

### Reverse Proxy (Nginx)

```nginx
# Exemple configuration
server {
    listen 80;
    server_name ragdz.example.com;

    # Frontend
    location / {
        proxy_pass http://localhost:5173;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8180;
    }
}
```

### Docker Compose Production

```yaml
# Exposer seulement via reverse proxy
services:
  backend:
    ports:
      - "127.0.0.1:8180:8180"  # Localhost uniquement

  frontend:
    ports:
      - "127.0.0.1:5173:5173"  # Localhost uniquement
```

---

## ✅ Checklist Pré-Déploiement

- [ ] Tous les ports sont libres (`find_free_ports.ps1`)
- [ ] Services accessibles via localhost
- [ ] Firewall configuré (production)
- [ ] Reverse proxy configuré (production)
- [ ] Monitoring Prometheus fonctionnel
- [ ] Grafana dashboards visibles
- [ ] Backup des données critiques
- [ ] Documentation mise à jour

---

## 📞 Support

En cas de problème de ports:

1. Exécuter `find_free_ports.ps1`
2. Vérifier les logs: `docker-compose logs`
3. Consulter la documentation: [README.md](README.md)

**Note:** Ce document est généré automatiquement et peut être mis à jour à tout moment.
