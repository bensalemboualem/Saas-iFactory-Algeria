# 🎯 RAG.dz - Guide Multi-Interfaces

## ✅ Attribution des Ports - Résumé

Vous aviez raison ! Chaque interface a maintenant **son propre port** pour faciliter le testing simultané.

---

## 📊 Plan d'Attribution Final

### 🎨 Interfaces Frontend

| Interface | Port | Tech Stack | Status | Commande de Démarrage |
|-----------|------|------------|--------|----------------------|
| **Archon UI** | `3737` | React 18 + Vite + TanStack Query | ✅ Production | `make start-archon` |
| **RAG-UI Simple** | `5173` | React 19 + Create React App | ⚙️ Dev | `make start-ragui` |
| **Bolt.diy** | `5174` | Remix + WebContainer | 🤖 AI Editor | `make start-bolt` |

### ⚡ Backend & API

| Service | Port | Description |
|---------|------|-------------|
| **FastAPI Backend** | `8180` | API + RAG Engine + Metrics |

### 🗄️ Bases de Données

| Service | Port | Type |
|---------|------|------|
| **PostgreSQL** | `5432` | Base principale (pgvector) |
| **Redis** | `6379` | Cache & Queue |
| **Qdrant** | `6333` | Vector Database (HTTP) |
| **Qdrant gRPC** | `6334` | Vector Database (gRPC) |

### 📊 Monitoring

| Service | Port | Interface |
|---------|------|-----------|
| **Grafana** | `3001` | Dashboards (admin/admin) |
| **Prometheus** | `9090` | Metrics Collection |
| **Postgres Exporter** | `9187` | PostgreSQL Metrics |
| **Redis Exporter** | `9121` | Redis Metrics |

---

## 🚀 Démarrage des Interfaces

### Option 1: Tout démarrer (sauf Bolt)
```bash
make start
# ou
docker-compose up -d
```

**Services démarrés:**
- ✅ Archon UI (3737)
- ✅ RAG-UI Simple (5173)
- ✅ Backend (8180)
- ✅ Toutes les DBs
- ✅ Monitoring complet

### Option 2: TOUT démarrer (inclus Bolt)
```bash
make start-all
# ou
docker-compose --profile bolt up -d
```

**Services supplémentaires:**
- ✅ Bolt.diy (5174)

### Option 3: Démarrage Sélectif

#### Une seule interface
```bash
# Archon UI uniquement
make start-archon
# ou: docker-compose up -d frontend

# RAG-UI uniquement
make start-ragui
# ou: docker-compose up -d rag-ui

# Bolt.diy uniquement
make start-bolt
# ou: docker-compose --profile bolt up -d bolt-diy
```

---

## 🧪 Testing Simultané

### 1. Démarrer tous les services
```bash
make start-all
```

### 2. Tester tous les ports
```bash
make ports
# ou
python test_all_ports.py
```

### 3. Ouvrir toutes les interfaces

**Frontends:**
- http://localhost:3737 - Archon UI (principale)
- http://localhost:5173 - RAG-UI Simple
- http://localhost:5174 - Bolt.diy

**API & Docs:**
- http://localhost:8180/docs - Swagger UI
- http://localhost:8180/health - Health Check

**Monitoring:**
- http://localhost:3001 - Grafana (admin/admin)
- http://localhost:9090 - Prometheus
- http://localhost:6333/dashboard - Qdrant

---

## 📋 Commandes Utiles

### Gestion Globale
```bash
make help              # Liste toutes les commandes
make status            # Status de tous les services
make ports             # Test tous les ports
make urls              # Affiche toutes les URLs
make logs              # Tous les logs en temps réel
```

### Gestion par Interface
```bash
# Logs spécifiques
make logs-archon       # Logs Archon UI
make logs-ragui        # Logs RAG-UI
make logs-bolt         # Logs Bolt.diy
make logs-backend      # Logs Backend

# Redémarrage
docker-compose restart frontend    # Redémarre Archon
docker-compose restart rag-ui      # Redémarre RAG-UI
docker-compose restart bolt-diy    # Redémarre Bolt
```

### Tests
```bash
make test              # Tous les tests (ports + backend + frontend)
make test-ports        # Test uniquement les ports
make test-backend      # Tests backend Python
make test-frontend     # Tests frontend React
```

---

## 🔍 Vérification Post-Démarrage

### Checklist Rapide
```bash
# 1. Status des containers
docker-compose ps

# 2. Test automatique de tous les ports
python test_all_ports.py

# 3. Vérifier chaque interface
curl http://localhost:3737  # Archon UI
curl http://localhost:5173  # RAG-UI
curl http://localhost:5174  # Bolt.diy
curl http://localhost:8180/health  # Backend API
```

### Résultat Attendu
```
Total services:     12
✅ En ligne:        12 (100%)
❌ Hors ligne:       0 (0%)
```

---

## 🎯 Pourquoi des Ports Séparés ?

### ✅ Avantages

1. **Testing Simultané**
   - Tester toutes les interfaces en parallèle
   - Comparer les fonctionnalités côte à côte
   - Détecter les bugs spécifiques à une interface

2. **Développement Flexible**
   - Démarrer uniquement ce dont vous avez besoin
   - Pas de conflits de ports
   - Isolation des services

3. **Production Ready**
   - Configuration claire et prévisible
   - Facile à monitorer
   - Scalabilité simplifiée

4. **Debugging Facilité**
   - Logs séparés par interface
   - Redémarrage individuel sans impact
   - Identification rapide des problèmes

### 📊 Ancien vs Nouveau

**Ancien Système:**
```
❌ Port 5173 - Conflit entre RAG-UI et Bolt
❌ Démarrage manuel nécessaire
❌ Testing séquentiel uniquement
```

**Nouveau Système:**
```
✅ Port 3737 - Archon UI
✅ Port 5173 - RAG-UI
✅ Port 5174 - Bolt.diy
✅ Démarrage automatique avec Docker Compose
✅ Testing simultané de toutes les interfaces
```

---

## 🔧 Configuration Avancée

### Modifier un Port (si besoin)

Éditer `docker-compose.yml`:

```yaml
services:
  rag-ui:
    ports:
      - "5175:5173"  # Change le port externe vers 5175
      #  ^^^^  ^^^^
      #  |     └─ Port interne (ne pas changer)
      #  └─ Port externe (modifiable)
```

### Variables d'Environnement

Les ports sont configurables via `.env`:

```bash
# .env
ARCHON_PORT=3737
RAGUI_PORT=5173
BOLT_PORT=5174
BACKEND_PORT=8180
```

---

## 🐛 Résolution de Problèmes

### Port déjà utilisé

**Symptôme:**
```
Error: bind: address already in use
```

**Solution:**
```bash
# 1. Identifier le processus
netstat -ano | findstr ":5173"  # Windows
lsof -i :5173                   # Linux/Mac

# 2. Arrêter le processus ou changer le port
```

### Service ne démarre pas

**Vérification:**
```bash
# Logs détaillés
docker-compose logs rag-ui

# Status du container
docker-compose ps rag-ui

# Rebuild si nécessaire
docker-compose up -d --build rag-ui
```

### Interface inaccessible

**Checklist:**
1. ✅ Container running? `docker-compose ps`
2. ✅ Port ouvert? `python test_all_ports.py`
3. ✅ Logs propres? `docker-compose logs rag-ui`
4. ✅ Backend accessible? `curl http://localhost:8180/health`

---

## 📚 Documentation Associée

- **`PORTS_MAPPING.md`** - Plan détaillé d'attribution des ports
- **`docker-compose.yml`** - Configuration des services
- **`test_all_ports.py`** - Script de test automatique
- **`Makefile`** - Commandes de gestion
- **`START_HERE.md`** - Guide de démarrage rapide

---

## 🎉 Résumé Visuel

```
┌──────────────────────────────────────────────────────┐
│                  TESTING SIMULTANÉ                   │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Browser Tab 1: http://localhost:3737 (Archon UI)   │
│  Browser Tab 2: http://localhost:5173 (RAG-UI)      │
│  Browser Tab 3: http://localhost:5174 (Bolt.diy)    │
│  Browser Tab 4: http://localhost:8180/docs (API)    │
│  Browser Tab 5: http://localhost:3001 (Grafana)     │
│  Browser Tab 6: http://localhost:9090 (Prometheus)  │
│                                                      │
│  ✅ Toutes les interfaces accessibles EN MÊME TEMPS │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## 🎯 Prochaines Étapes

### 1. Démarrer tout
```bash
make start-all
```

### 2. Vérifier
```bash
make ports
```

### 3. Tester
Ouvrir toutes les URLs dans votre navigateur et tester !

---

**Made with ❤️ for Algeria 🇩🇿**

*Question répondue: Pourquoi pas un port séparé pour chaque interface ?*
**Réponse: C'est fait ! Chaque interface a maintenant son port dédié. 🎉**
