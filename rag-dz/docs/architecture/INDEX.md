# 📚 Index de la Documentation RAG.dz

Guide complet pour naviguer dans toute la documentation du projet.

## 🎯 Par Besoin

### Je débute sur le projet
1. **[README.md](README.md)** - Commencer ici
2. **[QUICKSTART.md](QUICKSTART.md)** - Installation en 60 secondes
3. **[CHEAT_SHEET.md](CHEAT_SHEET.md)** - Toutes les commandes essentielles

### Je veux tester le projet
1. **[HOW_TO_TEST.md](HOW_TO_TEST.md)** - Instructions rapides
2. **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Guide complet de test
3. **[test_all_interfaces.py](test_all_interfaces.py)** - Script de test automatique

### Je veux comprendre les améliorations
1. **[IMPROVEMENTS.md](IMPROVEMENTS.md)** - Détails de toutes les améliorations
2. **[SUMMARY.md](SUMMARY.md)** - Résumé visuel et métriques

### Je veux déployer en production
1. **[README.md](README.md)** - Section Déploiement
2. **[.env.example](.env.example)** - Configuration requise
3. **[docker-compose.yml](docker-compose.yml)** - Infrastructure

### Je cherche une commande spécifique
1. **[CHEAT_SHEET.md](CHEAT_SHEET.md)** - Toutes les commandes
2. **[Makefile](Makefile)** - Liste des commandes make

---

## 📖 Documentation par Fichier

### 📄 Fichiers Principaux

#### [README.md](README.md)
**Documentation principale du projet**
- Vue d'ensemble
- Architecture
- Installation
- Configuration
- API Documentation
- Monitoring
- Sécurité
- Déploiement

**Quand le lire :** Première fois sur le projet

---

#### [QUICKSTART.md](QUICKSTART.md)
**Guide de démarrage ultra-rapide**
- Installation en 3 étapes
- URLs essentielles
- Test rapide de l'API
- Dépannage express
- Prochaines étapes

**Quand le lire :** Besoin de démarrer vite

---

#### [IMPROVEMENTS.md](IMPROVEMENTS.md)
**Détails de toutes les améliorations**
- Sécurité (API keys, CORS, Rate limiting)
- Infrastructure (Docker Compose, Config)
- Tests (Backend pytest, Frontend Vitest)
- Performance (Cache Redis, Pagination)
- Monitoring (Prometheus, Grafana)
- Checklist de déploiement
- Métriques disponibles

**Quand le lire :** Comprendre ce qui a été fait

---

#### [SUMMARY.md](SUMMARY.md)
**Résumé visuel des améliorations**
- Objectifs atteints (tableaux)
- Métriques (fichiers créés, lignes de code)
- Améliorations détaillées
- Avant/Après comparaison
- ROI estimé
- Checklist production

**Quand le lire :** Vue d'ensemble rapide

---

#### [TESTING_GUIDE.md](TESTING_GUIDE.md)
**Guide complet de test**
- Test Backend API (10 sections)
- Test Frontend UI
- Test Base de Données
- Test Cache Redis
- Test Qdrant Vector DB
- Test Monitoring
- Tests Automatisés
- Test de Charge
- Checklist complète

**Quand le lire :** Tests approfondis

---

#### [HOW_TO_TEST.md](HOW_TO_TEST.md)
**Instructions rapides de test**
- Méthode ultra-rapide (script Python)
- Méthode manuelle (navigateur)
- Tests rapides par interface
- Tests de performance
- Checklist rapide
- Dépannage

**Quand le lire :** Tester rapidement

---

#### [CHEAT_SHEET.md](CHEAT_SHEET.md)
**Toutes les commandes en un seul endroit**
- URLs essentielles
- Commandes Make
- Commandes Docker Compose
- Tests API (curl)
- Commandes PostgreSQL, Redis, Qdrant
- Requêtes Prometheus
- Variables d'environnement
- Dépannage

**Quand le lire :** Chercher une commande

---

### ⚙️ Fichiers de Configuration

#### [.env.example](.env.example)
**Template de configuration**
- Variables backend
- Variables frontend
- Variables monitoring
- Secrets à configurer

**Action :** `cp .env.example .env` puis éditer

---

#### [docker-compose.yml](docker-compose.yml)
**Orchestration des services**
- 7 services configurés
- Healthchecks
- Volumes persistants
- Networks

**Action :** `docker-compose up -d`

---

#### [Makefile](Makefile)
**Commandes make**
- 40+ commandes disponibles
- Gestion services, logs, tests, DB, cache
- Monitoring, dev, production

**Usage :** `make help`

---

### 🧪 Fichiers de Test

#### [test_all_interfaces.py](test_all_interfaces.py)
**Script de test automatique Python**
- Teste toutes les interfaces
- Rapport coloré
- Exit code (0 = success)

**Usage :** `python test_all_interfaces.py`

---

#### [rag-compat/pytest.ini](rag-compat/pytest.ini)
**Configuration pytest**
- Coverage settings
- Markers (unit, integration, security)

**Usage :** `cd rag-compat && pytest`

---

#### [rag-compat/tests/](rag-compat/tests/)
**Tests backend**
- `conftest.py` - Fixtures
- `test_security.py` - Tests sécurité (12 tests)
- `test_api.py` - Tests API (10+ tests)

**Usage :** `pytest tests/test_security.py -v`

---

#### [rag-ui/src/**/__tests__/](rag-ui/src/)
**Tests frontend**
- `api.test.ts` - Tests API client
- `App.test.tsx` - Tests composants
- `security.test.ts` - Tests sécurité

**Usage :** `cd rag-ui && npm test`

---

### 🔧 Fichiers Backend

#### [rag-compat/app/config.py](rag-compat/app/config.py)
**Configuration centralisée**
- Classe Settings (Pydantic)
- Variables d'environnement
- Méthodes utilitaires

**Usage :** `from app.config import get_settings`

---

#### [rag-compat/app/security.py](rag-compat/app/security.py)
**Sécurité & Rate Limiting**
- RateLimiter class
- Middlewares (Auth, RateLimit)
- Validation API keys

**Features :** Rate limiting, CORS, headers sécurité

---

#### [rag-compat/app/cache.py](rag-compat/app/cache.py)
**Cache Redis**
- RedisCache class
- EmbeddingCache (24h TTL)
- QueryCache (5min TTL)

**Gains :** ~9.5x plus rapide

---

#### [rag-compat/app/pagination.py](rag-compat/app/pagination.py)
**Pagination**
- PaginationParams
- PaginatedResponse[T]
- Cursor-based pagination

**Usage :** Dans routers query.py

---

### 📊 Fichiers Monitoring

#### [monitoring/prometheus.yml](monitoring/prometheus.yml)
**Configuration Prometheus**
- 5 jobs configurés
- Scrape intervals
- Targets

**Port :** 9090

---

#### [monitoring/alerts.yml](monitoring/alerts.yml)
**Règles d'alertes**
- 9 alertes configurées
- Sévérités (critical, warning, info)
- Conditions & seuils

**Alertes :** ServiceDown, HighErrorRate, etc.

---

#### [monitoring/grafana/](monitoring/grafana/)
**Configuration Grafana**
- Datasources auto-provisionées
- Dashboards skeleton

**Port :** 3001 (admin/admin)

---

### 🚀 Scripts Utilitaires

#### [start.sh](start.sh)
**Script de démarrage automatique**
- Vérifie .env
- Démarre services en ordre
- Healthchecks
- Affiche URLs

**Usage :** `bash start.sh`

---

## 🗺️ Parcours Recommandés

### 🎓 Nouveau Développeur

```
1. README.md (vue d'ensemble)
   ↓
2. QUICKSTART.md (installation)
   ↓
3. HOW_TO_TEST.md (vérifier que ça marche)
   ↓
4. CHEAT_SHEET.md (commandes utiles)
   ↓
5. Backend: rag-compat/app/
   Frontend: rag-ui/src/
```

### 🧪 QA / Testeur

```
1. HOW_TO_TEST.md (instructions)
   ↓
2. python test_all_interfaces.py (auto)
   ↓
3. TESTING_GUIDE.md (manuel détaillé)
   ↓
4. CHEAT_SHEET.md (commandes test)
```

### 🔧 DevOps

```
1. docker-compose.yml (infrastructure)
   ↓
2. .env.example (configuration)
   ↓
3. Makefile (commandes)
   ↓
4. monitoring/ (Prometheus + Grafana)
   ↓
5. IMPROVEMENTS.md (architecture)
```

### 📊 Product Manager

```
1. SUMMARY.md (métriques & résultats)
   ↓
2. README.md (features)
   ↓
3. IMPROVEMENTS.md (améliorations)
```

---

## 🔍 Recherche par Mot-Clé

### API
- README.md - API Documentation
- TESTING_GUIDE.md - Test Backend API
- CHEAT_SHEET.md - Tests API (curl)

### Cache
- cache.py - Implémentation
- IMPROVEMENTS.md - Cache Redis
- TESTING_GUIDE.md - Test Cache Redis

### Docker
- docker-compose.yml - Configuration
- README.md - Architecture
- IMPROVEMENTS.md - Infrastructure

### Monitoring
- monitoring/ - Configuration
- README.md - Monitoring
- TESTING_GUIDE.md - Test Monitoring

### Performance
- cache.py - Cache Redis
- pagination.py - Pagination
- IMPROVEMENTS.md - Performance
- SUMMARY.md - Gains

### Sécurité
- security.py - Implémentation
- IMPROVEMENTS.md - Sécurité
- TESTING_GUIDE.md - Tests de Sécurité
- tests/test_security.py - Tests

### Tests
- TESTING_GUIDE.md - Guide complet
- HOW_TO_TEST.md - Instructions rapides
- test_all_interfaces.py - Script auto
- tests/ - Tests backend
- src/**/__tests__/ - Tests frontend

---

## 📐 Structure Complète du Projet

```
rag-dz/
├── 📚 Documentation
│   ├── README.md                    # Principal
│   ├── QUICKSTART.md                # Démarrage rapide
│   ├── IMPROVEMENTS.md              # Améliorations
│   ├── SUMMARY.md                   # Résumé
│   ├── TESTING_GUIDE.md             # Guide test complet
│   ├── HOW_TO_TEST.md               # Instructions test
│   ├── CHEAT_SHEET.md               # Commandes
│   └── INDEX.md                     # Ce fichier
│
├── ⚙️ Configuration
│   ├── .env.example                 # Template config
│   ├── .gitignore                   # Secrets protection
│   ├── docker-compose.yml           # Orchestration
│   ├── Makefile                     # Commandes make
│   └── start.sh                     # Script démarrage
│
├── 🧪 Tests
│   └── test_all_interfaces.py       # Tests auto
│
├── 🔧 Backend
│   └── rag-compat/
│       ├── app/
│       │   ├── main.py              # FastAPI app
│       │   ├── config.py            # Configuration
│       │   ├── security.py          # Sécurité
│       │   ├── cache.py             # Cache Redis
│       │   ├── pagination.py        # Pagination
│       │   ├── db.py                # Database
│       │   ├── middleware.py        # Middlewares
│       │   ├── monitoring.py        # Métriques
│       │   ├── routers/             # Endpoints
│       │   └── clients/             # Embeddings, Qdrant
│       ├── tests/
│       │   ├── conftest.py          # Fixtures
│       │   ├── test_security.py     # Tests sécurité
│       │   └── test_api.py          # Tests API
│       ├── requirements.txt
│       ├── pytest.ini
│       ├── .env.example
│       └── Dockerfile
│
├── 🎨 Frontend
│   └── rag-ui/
│       ├── src/
│       │   ├── App.tsx
│       │   ├── components/
│       │   ├── services/
│       │   ├── hooks/
│       │   └── **/__tests__/        # Tests Vitest
│       ├── .env.example
│       ├── package.json
│       ├── vite.config.ts
│       ├── vitest.config.ts
│       └── Dockerfile
│
├── 📊 Monitoring
│   └── monitoring/
│       ├── prometheus.yml           # Config Prometheus
│       ├── alerts.yml               # Alertes
│       └── grafana/
│           ├── datasources/
│           └── dashboards/
│
└── 🗄️ Database
    └── sql/
        └── init.sql                 # Schema initial
```

---

## 🎯 Quick Links

| Besoin | Fichier |
|--------|---------|
| 🚀 Démarrer | [QUICKSTART.md](QUICKSTART.md) |
| 📖 Comprendre | [README.md](README.md) |
| 🧪 Tester | [HOW_TO_TEST.md](HOW_TO_TEST.md) |
| 🔍 Chercher commande | [CHEAT_SHEET.md](CHEAT_SHEET.md) |
| 📊 Voir résultats | [SUMMARY.md](SUMMARY.md) |
| 🔧 Détails techniques | [IMPROVEMENTS.md](IMPROVEMENTS.md) |
| 🧪 Tests complets | [TESTING_GUIDE.md](TESTING_GUIDE.md) |

---

**Navigation Rapide :** Ctrl+F pour rechercher dans ce fichier ! 🔍
