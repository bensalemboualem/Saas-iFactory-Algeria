# PLAN DE MIGRATION DETAILLE - IAFACTORY MONOREPO

**PROMPT 5** - Plan executif avec commandes exactes
**Date**: 2025-12-29
**Duree estimee**: 5-7 jours
**Prerequis**: ARCHITECTURE_OPTIMALE.md + RAG_DZ_COMPLET.md

---

## TABLE DES MATIERES

1. [Prerequis & Verification](#1-prerequis--verification)
2. [Phase 1: Backup & Securisation](#phase-1-backup--securisation)
3. [Phase 2: Creation Structure Monorepo](#phase-2-creation-structure-monorepo)
4. [Phase 3: Migration du Code Core](#phase-3-migration-du-code-core)
5. [Phase 4: Configuration Regions](#phase-4-configuration-regions)
6. [Phase 5: Adaptation du Code](#phase-5-adaptation-du-code)
7. [Phase 6: Tests & Validation](#phase-6-tests--validation)
8. [Phase 7: Deploiement Production](#phase-7-deploiement-production)
9. [Procedures de Rollback](#procedures-de-rollback)
10. [Checklist Finale](#checklist-finale)

---

## 1. PREREQUIS & VERIFICATION

### Outils Requis

```bash
# Verifier les versions installees
node --version      # >= 18.0.0
npm --version       # >= 9.0.0
pnpm --version      # >= 8.0.0 (ou installer: npm install -g pnpm)
python --version    # >= 3.11.0
docker --version    # >= 24.0.0
git --version       # >= 2.40.0
```

### Structure Actuelle Verifiee

```
D:\IAFactory\
├── rag-dz/                    # SOURCE PRINCIPALE (500+ fichiers)
├── iafactory-academy/         # CONSERVE (separe)
├── onestschooled/             # CONSERVE (separe)
├── BACKUPS/                   # Sauvegardes existantes
├── _archive/                  # 5 projets vides archives
├── ANALYSE_EXHAUSTIVE_IAFACTORY.md
├── RAG_DZ_COMPLET.md
├── ARCHITECTURE_OPTIMALE.md
└── NETTOYAGE_DONE.md
```

---

## PHASE 1: BACKUP & SECURISATION

**Duree: 30 minutes**
**Criticite: HAUTE**

### 1.1 Backup Complet de rag-dz

```bash
# Creer dossier backup avec timestamp
set TIMESTAMP=%date:~6,4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%
mkdir "D:\IAFactory\BACKUPS\pre-migration_%TIMESTAMP%"

# Copier l'integralite de rag-dz
xcopy /E /I /H "D:\IAFactory\rag-dz" "D:\IAFactory\BACKUPS\pre-migration_%TIMESTAMP%\rag-dz-backup"

# Verifier la copie
dir "D:\IAFactory\BACKUPS\pre-migration_%TIMESTAMP%\rag-dz-backup" /s | find "File(s)"
```

### 1.2 Backup des Bases de Donnees (si en cours d'utilisation)

```bash
# Si PostgreSQL local est actif
cd D:\IAFactory\rag-dz
docker-compose exec iafactory-postgres pg_dump -U postgres iafactory_dz > "D:\IAFactory\BACKUPS\pre-migration\db_backup.sql"

# Si Qdrant local est actif
docker-compose exec iafactory-qdrant curl -X POST "http://localhost:6333/collections/documents/snapshots"
```

### 1.3 Verification du Backup

```bash
# Verifier que le backup est complet
echo === VERIFICATION BACKUP ===
dir /s /b "D:\IAFactory\BACKUPS\pre-migration_%TIMESTAMP%\rag-dz-backup\*" | find /c /v ""
# Doit afficher 500+ fichiers
```

### TEST PHASE 1

```bash
# Le backup existe et contient les fichiers critiques
if exist "D:\IAFactory\BACKUPS\pre-migration_*\rag-dz-backup\services\api\app\main.py" (
    echo [OK] Backup valide
) else (
    echo [ERREUR] Backup incomplet - ARRETER LA MIGRATION
)
```

---

## PHASE 2: CREATION STRUCTURE MONOREPO

**Duree: 15 minutes**
**Criticite: MOYENNE**

### 2.1 Creer le Nouveau Repository

```bash
# Naviguer vers le workspace
cd D:\IAFactory

# Creer le dossier du monorepo
mkdir iafactory-platform
cd iafactory-platform

# Initialiser Git
git init
git branch -M main
```

### 2.2 Creer l'Arborescence Complete

```bash
# Structure core/
mkdir core
mkdir core\apps
mkdir core\agents
mkdir core\services
mkdir core\frontend
mkdir core\workflows
mkdir core\infrastructure

# Structure deployments/
mkdir deployments
mkdir deployments\algeria
mkdir deployments\algeria\nginx
mkdir deployments\algeria\nginx\ssl
mkdir deployments\algeria\messages
mkdir deployments\algeria\legal
mkdir deployments\algeria\branding
mkdir deployments\algeria\scripts
mkdir deployments\switzerland
mkdir deployments\switzerland\nginx
mkdir deployments\switzerland\nginx\ssl
mkdir deployments\switzerland\messages
mkdir deployments\switzerland\legal
mkdir deployments\switzerland\branding
mkdir deployments\switzerland\scripts

# Structure shared/
mkdir shared
mkdir shared\scripts
mkdir shared\templates

# Structure docs/
mkdir docs
mkdir docs\api
mkdir docs\guides

# Structure CI/CD
mkdir .github
mkdir .github\workflows
```

### 2.3 Creer les Fichiers Root

```bash
# package.json root (pnpm workspace)
echo {> package.json
echo   "name": "iafactory-platform",>> package.json
echo   "version": "1.0.0",>> package.json
echo   "private": true,>> package.json
echo   "workspaces": [>> package.json
echo     "core/apps/*",>> package.json
echo     "core/frontend/*">> package.json
echo   ],>> package.json
echo   "scripts": {>> package.json
echo     "dev:algeria": "cd deployments/algeria && docker-compose up",>> package.json
echo     "dev:switzerland": "cd deployments/switzerland && docker-compose up",>> package.json
echo     "build": "turbo run build",>> package.json
echo     "test": "turbo run test",>> package.json
echo     "lint": "turbo run lint",>> package.json
echo     "deploy:algeria": "./shared/scripts/deploy.sh algeria production",>> package.json
echo     "deploy:switzerland": "./shared/scripts/deploy.sh switzerland production">> package.json
echo   },>> package.json
echo   "devDependencies": {>> package.json
echo     "turbo": "^2.0.0">> package.json
echo   }>> package.json
echo }>> package.json

# pnpm-workspace.yaml
echo packages:> pnpm-workspace.yaml
echo   - "core/apps/*">> pnpm-workspace.yaml
echo   - "core/frontend/*">> pnpm-workspace.yaml

# turbo.json
echo {> turbo.json
echo   "$schema": "https://turbo.build/schema.json",>> turbo.json
echo   "tasks": {>> turbo.json
echo     "build": { "outputs": ["dist/**", ".next/**"] },>> turbo.json
echo     "test": { "dependsOn": ["build"] },>> turbo.json
echo     "lint": {}>> turbo.json
echo   }>> turbo.json
echo }>> turbo.json

# .gitignore
echo node_modules/> .gitignore
echo .env>> .gitignore
echo .env.local>> .gitignore
echo .env.production>> .gitignore
echo __pycache__/>> .gitignore
echo *.pyc>> .gitignore
echo .venv/>> .gitignore
echo venv/>> .gitignore
echo dist/>> .gitignore
echo .next/>> .gitignore
echo *.log>> .gitignore
echo .DS_Store>> .gitignore

# .dockerignore
echo node_modules> .dockerignore
echo .git>> .dockerignore
echo .env*>> .dockerignore
echo __pycache__>> .dockerignore
echo *.md>> .dockerignore
```

### TEST PHASE 2

```bash
# Verifier la structure creee
cd D:\IAFactory\iafactory-platform
dir /s /ad /b | find /c /v ""
# Doit afficher environ 25 dossiers

# Verifier les fichiers root
if exist "package.json" if exist "pnpm-workspace.yaml" if exist "turbo.json" (
    echo [OK] Structure monorepo creee
) else (
    echo [ERREUR] Fichiers root manquants
)
```

---

## PHASE 3: MIGRATION DU CODE CORE

**Duree: 2-3 heures**
**Criticite: HAUTE**

### 3.1 Migrer les Applications (28 apps)

```bash
cd D:\IAFactory

# Copier toutes les apps
xcopy /E /I "rag-dz\apps\*" "iafactory-platform\core\apps\"

# Renommer les dossiers specifiques DZ -> generiques
cd iafactory-platform\core\apps
if exist "pme-dz" ren "pme-dz" "pme"
if exist "seo-dz-boost" ren "seo-dz-boost" "seo-boost"
if exist "crm-ia" ren "crm-ia" "crm"
if exist "ia-chatbot" ren "ia-chatbot" "chatbot"
if exist "ia-notebook" ren "ia-notebook" "notebook"
if exist "ia-searcher" ren "ia-searcher" "searcher"
if exist "ia-voice" ren "ia-voice" "voice"
if exist "ia-agents" ren "ia-agents" "agents-marketplace"
if exist "dzirvideo" ren "dzirvideo" "video-gen"

cd D:\IAFactory
```

### 3.2 Migrer les Agents (15+ agents)

```bash
# Copier tous les agents
xcopy /E /I "rag-dz\agents\*" "iafactory-platform\core\agents\"

# Renommer les dossiers specifiques DZ
cd iafactory-platform\core\agents
if exist "discovery-dz" ren "discovery-dz" "discovery"
if exist "recruteur-dz" ren "recruteur-dz" "recruiter"

cd D:\IAFactory
```

### 3.3 Migrer les Services Backend

```bash
# Copier le backend API complet
xcopy /E /I "rag-dz\services\*" "iafactory-platform\core\services\"

# Verifier les fichiers critiques
dir "iafactory-platform\core\services\api\app\main.py"
dir "iafactory-platform\core\services\api\app\config.py"
dir "iafactory-platform\core\services\api\requirements.txt"
```

### 3.4 Migrer les Frontends (4 UI)

```bash
# Frontend principal Next.js
xcopy /E /I "rag-dz\frontend\ia-factory-ui\*" "iafactory-platform\core\frontend\main-ui\"

# Frontend RAG Vite
xcopy /E /I "rag-dz\frontend\rag-ui\*" "iafactory-platform\core\frontend\rag-ui\"

# Frontend Archon (si existe)
if exist "rag-dz\frontend\archon-ui" xcopy /E /I "rag-dz\frontend\archon-ui\*" "iafactory-platform\core\frontend\archon-ui\"

# Frontend Video Studio (si existe)
if exist "rag-dz\frontend\video-studio" xcopy /E /I "rag-dz\frontend\video-studio\*" "iafactory-platform\core\frontend\video-studio\"
```

### 3.5 Migrer les Workflows n8n

```bash
# Copier les workflows
if exist "rag-dz\workflows" xcopy /E /I "rag-dz\workflows\*" "iafactory-platform\core\workflows\"
```

### 3.6 Migrer l'Infrastructure

```bash
# Copier les scripts SQL et configs
if exist "rag-dz\infrastructure" xcopy /E /I "rag-dz\infrastructure\*" "iafactory-platform\core\infrastructure\"

# Copier les migrations Alembic
if exist "rag-dz\services\api\alembic" xcopy /E /I "rag-dz\services\api\alembic\*" "iafactory-platform\core\services\api\alembic\"
```

### TEST PHASE 3

```bash
cd D:\IAFactory\iafactory-platform

# Compter les fichiers migres
echo === VERIFICATION MIGRATION ===
dir /s /b "core\apps\*" | find /c /v ""
echo fichiers dans core/apps (attendu: 200+)

dir /s /b "core\agents\*" | find /c /v ""
echo fichiers dans core/agents (attendu: 50+)

dir /s /b "core\services\*" | find /c /v ""
echo fichiers dans core/services (attendu: 150+)

dir /s /b "core\frontend\*" | find /c /v ""
echo fichiers dans core/frontend (attendu: 100+)

# Verifier fichiers critiques
if exist "core\services\api\app\main.py" (
    echo [OK] Backend API migre
) else (
    echo [ERREUR] Backend manquant
)

if exist "core\frontend\main-ui\package.json" (
    echo [OK] Frontend main-ui migre
) else (
    echo [ERREUR] Frontend manquant
)
```

---

## PHASE 4: CONFIGURATION REGIONS

**Duree: 1-2 heures**
**Criticite: HAUTE**

### 4.1 Configuration Algerie

#### Fichier .env.example

```bash
cd D:\IAFactory\iafactory-platform\deployments\algeria

# Creer .env.example
type nul > .env.example
```

Contenu de `deployments/algeria/.env.example`:

```env
# ═══════════════════════════════════════════════════════════
# IAFACTORY ALGERIA - CONFIGURATION
# ═══════════════════════════════════════════════════════════

# ── REGION ──
REGION=algeria
REGION_CODE=DZ
TIMEZONE=Africa/Algiers
DEFAULT_LANGUAGE=fr
SUPPORTED_LANGUAGES=fr,ar,en,dz

# ── DOMAIN ──
DOMAIN=iafactory-algeria.com
API_URL=https://api.iafactory-algeria.com
APP_URL=https://app.iafactory-algeria.com

# ── DATABASE ──
POSTGRES_HOST=iaf-postgres
POSTGRES_PORT=5432
POSTGRES_USER=iafactory_dz
POSTGRES_PASSWORD=CHANGE_ME_SECURE_PASSWORD
POSTGRES_DB=iafactory_dz
POSTGRES_URL=postgresql://iafactory_dz:CHANGE_ME@iaf-postgres:5432/iafactory_dz

# ── REDIS ──
REDIS_URL=redis://iaf-redis:6379/0
REDIS_PASSWORD=

# ── QDRANT ──
QDRANT_HOST=iaf-qdrant
QDRANT_PORT=6333
QDRANT_API_KEY=

# ── LLM PROVIDERS ──
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-5-sonnet-20241022
ENABLE_LLM=true
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-ant-xxx
GROQ_API_KEY=gsk_xxx
GOOGLE_GENERATIVE_AI_API_KEY=AIzaSy-xxx
DEEPSEEK_API_KEY=sk-xxx

# ── OLLAMA (LOCAL/SOUVERAIN) ──
OLLAMA_BASE_URL=http://iaf-ollama:11434
OLLAMA_MODEL=llama3.2

# ── EMBEDDINGS ──
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-mpnet-base-v2
EMBEDDING_DEVICE=cpu
EMBEDDING_BATCH_SIZE=32

# ── PAIEMENTS (ALGERIE = CHARGILY) ──
PAYMENT_PROVIDER=chargily
CHARGILY_API_KEY=xxx
CHARGILY_SECRET_KEY=xxx
CHARGILY_WEBHOOK_SECRET=xxx
CHARGILY_MODE=test
CHARGILY_API_URL=https://pay.chargily.net/test/api/v2
PAYMENT_CURRENCY=DZD
DEFAULT_CREDITS=100
CREDITS_PER_DZD=1.0

# ── MEILISEARCH ──
MEILI_URL=http://iaf-meilisearch:7700
MEILI_MASTER_KEY=

# ── SECURITY ──
API_SECRET_KEY=CHANGE_ME_MIN_32_CHARS_SECURE
JWT_SECRET_KEY=CHANGE_ME_MIN_32_CHARS_JWT
HASH_ALGORITHM=sha256
ALLOWED_ORIGINS=https://app.iafactory-algeria.com,https://iafactory-algeria.com

# ── RATE LIMITING ──
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
RATE_LIMIT_BURST=10
ENABLE_RATE_LIMITING=true

# ── FEATURES ──
ENABLE_DARIJA=true
ENABLE_ARABIC_RTL=true
ENABLE_CORS=true
ENABLE_METRICS=true
ENABLE_API_KEY_AUTH=true
LEGAL_FRAMEWORK=algeria
USE_RERANKING=true
RERANKING_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2
RERANKING_TOP_K=10
USE_PGVECTOR=true

# ── SERVICE ──
SERVICE_NAME=iafactory-dz-api
SERVICE_VERSION=1.0.0
LOG_LEVEL=INFO
ENVIRONMENT=development
DEFAULT_TENANT_ID=550e8400-e29b-41d4-a716-446655440000
PORT=8000
HOST=0.0.0.0
METRICS_PORT=9090
```

#### Docker Compose Algerie

Creer `deployments/algeria/docker-compose.yml`:

```yaml
# IAFACTORY ALGERIA - Docker Compose
version: '3.8'

services:
  iaf-postgres:
    image: pgvector/pgvector:pg16
    container_name: iaf-dz-postgres
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
      TZ: ${TIMEZONE}
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ../../core/infrastructure/sql:/docker-entrypoint-initdb.d:ro
    ports:
      - "5432:5432"
    networks:
      - iaf-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5

  iaf-redis:
    image: redis:7-alpine
    container_name: iaf-dz-redis
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
    ports:
      - "6379:6379"
    networks:
      - iaf-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  iaf-qdrant:
    image: qdrant/qdrant:latest
    container_name: iaf-dz-qdrant
    volumes:
      - qdrant-data:/qdrant/storage
    ports:
      - "6333:6333"
      - "6334:6334"
    networks:
      - iaf-network

  iaf-meilisearch:
    image: getmeili/meilisearch:latest
    container_name: iaf-dz-meilisearch
    environment:
      MEILI_MASTER_KEY: ${MEILI_MASTER_KEY}
    volumes:
      - meili-data:/meili_data
    ports:
      - "7700:7700"
    networks:
      - iaf-network

  iaf-backend:
    build:
      context: ../../core/services/api
      dockerfile: Dockerfile
    container_name: iaf-dz-backend
    env_file:
      - .env
    environment:
      - REGION=algeria
      - PYTHONUNBUFFERED=1
    volumes:
      - ../../core/services/api:/app
      - ../../core/agents:/agents:ro
    ports:
      - "8000:8000"
    depends_on:
      iaf-postgres:
        condition: service_healthy
      iaf-redis:
        condition: service_healthy
      iaf-qdrant:
        condition: service_started
    networks:
      - iaf-network
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  iaf-frontend:
    build:
      context: ../../core/frontend/main-ui
      dockerfile: Dockerfile
      args:
        - NEXT_PUBLIC_API_URL=${API_URL}
        - NEXT_PUBLIC_REGION=${REGION}
    container_name: iaf-dz-frontend
    environment:
      - NEXT_PUBLIC_API_URL=${API_URL}
      - NEXT_PUBLIC_REGION=algeria
    volumes:
      - ./messages:/app/messages:ro
      - ./branding:/app/public/branding:ro
    ports:
      - "3000:3000"
    depends_on:
      - iaf-backend
    networks:
      - iaf-network

  iaf-rag-ui:
    build:
      context: ../../core/frontend/rag-ui
      dockerfile: Dockerfile
    container_name: iaf-dz-rag-ui
    environment:
      - VITE_API_URL=${API_URL}
    ports:
      - "5173:5173"
    depends_on:
      - iaf-backend
    networks:
      - iaf-network

  iaf-ollama:
    image: ollama/ollama:latest
    container_name: iaf-dz-ollama
    volumes:
      - ollama-data:/root/.ollama
    ports:
      - "11434:11434"
    networks:
      - iaf-network
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]

  iaf-nginx:
    image: nginx:alpine
    container_name: iaf-dz-nginx
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - iaf-backend
      - iaf-frontend
    networks:
      - iaf-network

volumes:
  postgres-data:
  redis-data:
  qdrant-data:
  meili-data:
  ollama-data:

networks:
  iaf-network:
    driver: bridge
```

### 4.2 Configuration Suisse

#### Fichier .env.example

Creer `deployments/switzerland/.env.example`:

```env
# ═══════════════════════════════════════════════════════════
# IAFACTORY SWITZERLAND - CONFIGURATION
# ═══════════════════════════════════════════════════════════

# ── REGION ──
REGION=switzerland
REGION_CODE=CH
TIMEZONE=Europe/Zurich
DEFAULT_LANGUAGE=fr
SUPPORTED_LANGUAGES=fr,de,it,en

# ── DOMAIN ──
DOMAIN=iafactory.ch
API_URL=https://api.iafactory.ch
APP_URL=https://app.iafactory.ch

# ── DATABASE ──
POSTGRES_HOST=iaf-postgres
POSTGRES_PORT=5432
POSTGRES_USER=iafactory_ch
POSTGRES_PASSWORD=CHANGE_ME_SECURE_PASSWORD
POSTGRES_DB=iafactory_ch
POSTGRES_URL=postgresql://iafactory_ch:CHANGE_ME@iaf-postgres:5432/iafactory_ch

# ── REDIS ──
REDIS_URL=redis://iaf-redis:6379/0
REDIS_PASSWORD=

# ── QDRANT ──
QDRANT_HOST=iaf-qdrant
QDRANT_PORT=6333
QDRANT_API_KEY=

# ── LLM PROVIDERS ──
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-5-sonnet-20241022
ENABLE_LLM=true
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-ant-xxx
GROQ_API_KEY=gsk_xxx
GOOGLE_GENERATIVE_AI_API_KEY=AIzaSy-xxx

# ── OLLAMA (LOCAL/SOUVERAIN) ──
OLLAMA_BASE_URL=http://iaf-ollama:11434
OLLAMA_MODEL=llama3.2

# ── EMBEDDINGS ──
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-mpnet-base-v2
EMBEDDING_DEVICE=cpu
EMBEDDING_BATCH_SIZE=32

# ── PAIEMENTS (SUISSE = STRIPE) ──
PAYMENT_PROVIDER=stripe
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_PUBLIC_KEY=pk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
PAYMENT_CURRENCY=CHF

# ── MEILISEARCH ──
MEILI_URL=http://iaf-meilisearch:7700
MEILI_MASTER_KEY=

# ── SECURITY ──
API_SECRET_KEY=CHANGE_ME_MIN_32_CHARS_SECURE
JWT_SECRET_KEY=CHANGE_ME_MIN_32_CHARS_JWT
HASH_ALGORITHM=sha256
ALLOWED_ORIGINS=https://app.iafactory.ch,https://iafactory.ch

# ── RATE LIMITING ──
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
RATE_LIMIT_BURST=10
ENABLE_RATE_LIMITING=true

# ── FEATURES ──
ENABLE_DARIJA=false
ENABLE_ARABIC_RTL=false
ENABLE_CORS=true
ENABLE_METRICS=true
ENABLE_API_KEY_AUTH=true
LEGAL_FRAMEWORK=switzerland
USE_RERANKING=true
RERANKING_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2
RERANKING_TOP_K=10
USE_PGVECTOR=true

# ── SERVICE ──
SERVICE_NAME=iafactory-ch-api
SERVICE_VERSION=1.0.0
LOG_LEVEL=INFO
ENVIRONMENT=development
DEFAULT_TENANT_ID=660e8400-e29b-41d4-a716-446655440001
PORT=8000
HOST=0.0.0.0
METRICS_PORT=9090
```

#### Docker Compose Suisse

Creer `deployments/switzerland/docker-compose.yml` (similaire a Algerie mais ports differents):

```yaml
# IAFACTORY SWITZERLAND - Docker Compose
version: '3.8'

services:
  iaf-postgres:
    image: pgvector/pgvector:pg16
    container_name: iaf-ch-postgres
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
      TZ: ${TIMEZONE}
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ../../core/infrastructure/sql:/docker-entrypoint-initdb.d:ro
    ports:
      - "5433:5432"
    networks:
      - iaf-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5

  iaf-redis:
    image: redis:7-alpine
    container_name: iaf-ch-redis
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
    ports:
      - "6380:6379"
    networks:
      - iaf-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  iaf-qdrant:
    image: qdrant/qdrant:latest
    container_name: iaf-ch-qdrant
    volumes:
      - qdrant-data:/qdrant/storage
    ports:
      - "6335:6333"
      - "6336:6334"
    networks:
      - iaf-network

  iaf-meilisearch:
    image: getmeili/meilisearch:latest
    container_name: iaf-ch-meilisearch
    environment:
      MEILI_MASTER_KEY: ${MEILI_MASTER_KEY}
    volumes:
      - meili-data:/meili_data
    ports:
      - "7701:7700"
    networks:
      - iaf-network

  iaf-backend:
    build:
      context: ../../core/services/api
      dockerfile: Dockerfile
    container_name: iaf-ch-backend
    env_file:
      - .env
    environment:
      - REGION=switzerland
      - PYTHONUNBUFFERED=1
    volumes:
      - ../../core/services/api:/app
      - ../../core/agents:/agents:ro
    ports:
      - "8001:8000"
    depends_on:
      iaf-postgres:
        condition: service_healthy
      iaf-redis:
        condition: service_healthy
      iaf-qdrant:
        condition: service_started
    networks:
      - iaf-network
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  iaf-frontend:
    build:
      context: ../../core/frontend/main-ui
      dockerfile: Dockerfile
      args:
        - NEXT_PUBLIC_API_URL=${API_URL}
        - NEXT_PUBLIC_REGION=${REGION}
    container_name: iaf-ch-frontend
    environment:
      - NEXT_PUBLIC_API_URL=${API_URL}
      - NEXT_PUBLIC_REGION=switzerland
    volumes:
      - ./messages:/app/messages:ro
      - ./branding:/app/public/branding:ro
    ports:
      - "3001:3000"
    depends_on:
      - iaf-backend
    networks:
      - iaf-network

  iaf-rag-ui:
    build:
      context: ../../core/frontend/rag-ui
      dockerfile: Dockerfile
    container_name: iaf-ch-rag-ui
    environment:
      - VITE_API_URL=${API_URL}
    ports:
      - "5174:5173"
    depends_on:
      - iaf-backend
    networks:
      - iaf-network

  iaf-ollama:
    image: ollama/ollama:latest
    container_name: iaf-ch-ollama
    volumes:
      - ollama-data:/root/.ollama
    ports:
      - "11435:11434"
    networks:
      - iaf-network

  iaf-nginx:
    image: nginx:alpine
    container_name: iaf-ch-nginx
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    ports:
      - "81:80"
      - "444:443"
    depends_on:
      - iaf-backend
      - iaf-frontend
    networks:
      - iaf-network

volumes:
  postgres-data:
  redis-data:
  qdrant-data:
  meili-data:
  ollama-data:

networks:
  iaf-network:
    driver: bridge
```

### 4.3 Creer les Traductions i18n

#### Algerie (fr, ar, en, dz)

```bash
cd D:\IAFactory\iafactory-platform\deployments\algeria\messages

# Francais
echo {> fr.json
echo   "app": {>> fr.json
echo     "name": "IAFactory Algerie",>> fr.json
echo     "tagline": "Intelligence Artificielle pour l'Algerie",>> fr.json
echo     "currency": "DZD",>> fr.json
echo     "currencySymbol": "DA">> fr.json
echo   },>> fr.json
echo   "nav": {>> fr.json
echo     "home": "Accueil",>> fr.json
echo     "dashboard": "Tableau de bord",>> fr.json
echo     "agents": "Agents IA",>> fr.json
echo     "documents": "Documents",>> fr.json
echo     "settings": "Parametres">> fr.json
echo   },>> fr.json
echo   "auth": {>> fr.json
echo     "login": "Connexion",>> fr.json
echo     "register": "Inscription",>> fr.json
echo     "logout": "Deconnexion">> fr.json
echo   }>> fr.json
echo }>> fr.json

# Arabe
echo {> ar.json
echo   "app": {>> ar.json
echo     "name": "IAFactory الجزائر",>> ar.json
echo     "tagline": "الذكاء الاصطناعي للجزائر",>> ar.json
echo     "currency": "DZD",>> ar.json
echo     "currencySymbol": "دج">> ar.json
echo   },>> ar.json
echo   "nav": {>> ar.json
echo     "home": "الرئيسية",>> ar.json
echo     "dashboard": "لوحة القيادة",>> ar.json
echo     "agents": "وكلاء الذكاء",>> ar.json
echo     "documents": "الوثائق",>> ar.json
echo     "settings": "الإعدادات">> ar.json
echo   },>> ar.json
echo   "auth": {>> ar.json
echo     "login": "تسجيل الدخول",>> ar.json
echo     "register": "إنشاء حساب",>> ar.json
echo     "logout": "تسجيل الخروج">> ar.json
echo   }>> ar.json
echo }>> ar.json

# Anglais
echo {> en.json
echo   "app": {>> en.json
echo     "name": "IAFactory Algeria",>> en.json
echo     "tagline": "AI for Algeria",>> en.json
echo     "currency": "DZD",>> en.json
echo     "currencySymbol": "DA">> en.json
echo   },>> en.json
echo   "nav": {>> en.json
echo     "home": "Home",>> en.json
echo     "dashboard": "Dashboard",>> en.json
echo     "agents": "AI Agents",>> en.json
echo     "documents": "Documents",>> en.json
echo     "settings": "Settings">> en.json
echo   },>> en.json
echo   "auth": {>> en.json
echo     "login": "Login",>> en.json
echo     "register": "Sign up",>> en.json
echo     "logout": "Logout">> en.json
echo   }>> en.json
echo }>> en.json

# Darija (dialecte algerien)
echo {> dz.json
echo   "app": {>> dz.json
echo     "name": "IAFactory Dzair",>> dz.json
echo     "tagline": "الذكاء الاصطناعي للدزيريين",>> dz.json
echo     "currency": "DZD",>> dz.json
echo     "currencySymbol": "دج">> dz.json
echo   },>> dz.json
echo   "nav": {>> dz.json
echo     "home": "الدار",>> dz.json
echo     "dashboard": "التابلو",>> dz.json
echo     "agents": "الوكلاء",>> dz.json
echo     "documents": "الوراق",>> dz.json
echo     "settings": "الإعدادات">> dz.json
echo   },>> dz.json
echo   "auth": {>> dz.json
echo     "login": "دخول",>> dz.json
echo     "register": "التسجيل",>> dz.json
echo     "logout": "خروج">> dz.json
echo   }>> dz.json
echo }>> dz.json
```

#### Suisse (fr, de, it, en)

```bash
cd D:\IAFactory\iafactory-platform\deployments\switzerland\messages

# Francais (Suisse)
echo {> fr.json
echo   "app": {>> fr.json
echo     "name": "IAFactory Suisse",>> fr.json
echo     "tagline": "Intelligence Artificielle pour la Suisse",>> fr.json
echo     "currency": "CHF",>> fr.json
echo     "currencySymbol": "CHF">> fr.json
echo   },>> fr.json
echo   "nav": {>> fr.json
echo     "home": "Accueil",>> fr.json
echo     "dashboard": "Tableau de bord",>> fr.json
echo     "agents": "Agents IA",>> fr.json
echo     "documents": "Documents",>> fr.json
echo     "settings": "Parametres">> fr.json
echo   },>> fr.json
echo   "auth": {>> fr.json
echo     "login": "Connexion",>> fr.json
echo     "register": "S'inscrire",>> fr.json
echo     "logout": "Deconnexion">> fr.json
echo   }>> fr.json
echo }>> fr.json

# Allemand
echo {> de.json
echo   "app": {>> de.json
echo     "name": "IAFactory Schweiz",>> de.json
echo     "tagline": "Kunstliche Intelligenz fur die Schweiz",>> de.json
echo     "currency": "CHF",>> de.json
echo     "currencySymbol": "CHF">> de.json
echo   },>> de.json
echo   "nav": {>> de.json
echo     "home": "Startseite",>> de.json
echo     "dashboard": "Dashboard",>> de.json
echo     "agents": "KI-Agenten",>> de.json
echo     "documents": "Dokumente",>> de.json
echo     "settings": "Einstellungen">> de.json
echo   },>> de.json
echo   "auth": {>> de.json
echo     "login": "Anmelden",>> de.json
echo     "register": "Registrieren",>> de.json
echo     "logout": "Abmelden">> de.json
echo   }>> de.json
echo }>> de.json

# Italien
echo {> it.json
echo   "app": {>> it.json
echo     "name": "IAFactory Svizzera",>> it.json
echo     "tagline": "Intelligenza Artificiale per la Svizzera",>> it.json
echo     "currency": "CHF",>> it.json
echo     "currencySymbol": "CHF">> it.json
echo   },>> it.json
echo   "nav": {>> it.json
echo     "home": "Home",>> it.json
echo     "dashboard": "Dashboard",>> it.json
echo     "agents": "Agenti IA",>> it.json
echo     "documents": "Documenti",>> it.json
echo     "settings": "Impostazioni">> it.json
echo   },>> it.json
echo   "auth": {>> it.json
echo     "login": "Accedi",>> it.json
echo     "register": "Registrati",>> it.json
echo     "logout": "Esci">> it.json
echo   }>> it.json
echo }>> it.json

# Anglais
echo {> en.json
echo   "app": {>> en.json
echo     "name": "IAFactory Switzerland",>> en.json
echo     "tagline": "AI for Switzerland",>> en.json
echo     "currency": "CHF",>> en.json
echo     "currencySymbol": "CHF">> en.json
echo   },>> en.json
echo   "nav": {>> en.json
echo     "home": "Home",>> en.json
echo     "dashboard": "Dashboard",>> en.json
echo     "agents": "AI Agents",>> en.json
echo     "documents": "Documents",>> en.json
echo     "settings": "Settings">> en.json
echo   },>> en.json
echo   "auth": {>> en.json
echo     "login": "Login",>> en.json
echo     "register": "Sign up",>> en.json
echo     "logout": "Logout">> en.json
echo   }>> en.json
echo }>> en.json
```

### TEST PHASE 4

```bash
cd D:\IAFactory\iafactory-platform

# Verifier les fichiers de configuration
echo === VERIFICATION CONFIGS ===

if exist "deployments\algeria\.env.example" (
    echo [OK] Config Algerie presente
) else (
    echo [ERREUR] Config Algerie manquante
)

if exist "deployments\switzerland\.env.example" (
    echo [OK] Config Suisse presente
) else (
    echo [ERREUR] Config Suisse manquante
)

if exist "deployments\algeria\docker-compose.yml" (
    echo [OK] Docker Algerie present
) else (
    echo [ERREUR] Docker Algerie manquant
)

if exist "deployments\switzerland\docker-compose.yml" (
    echo [OK] Docker Suisse present
) else (
    echo [ERREUR] Docker Suisse manquant
)

# Verifier les traductions
dir deployments\algeria\messages\*.json
dir deployments\switzerland\messages\*.json
```

---

## PHASE 5: ADAPTATION DU CODE

**Duree: 2-4 heures**
**Criticite: HAUTE**

### 5.1 Modifier config.py pour Multi-Region

Fichier: `core/services/api/app/config.py`

Modifications a effectuer:

```python
# AJOUTER ces nouvelles variables:

# Region Configuration
region: str = "algeria"  # algeria | switzerland
region_code: str = "DZ"  # DZ | CH

# Payment Provider (abstraction)
payment_provider: str = "chargily"  # chargily | stripe

# Stripe (pour Suisse)
stripe_secret_key: str = ""
stripe_public_key: str = ""
stripe_webhook_secret: str = ""

# Features par region
enable_darija: bool = True
enable_arabic_rtl: bool = True
legal_framework: str = "algeria"  # algeria | switzerland

# MODIFIER la methode get_allowed_origins:
def get_payment_config(self) -> dict:
    """Get payment configuration based on region"""
    if self.payment_provider == "chargily":
        return {
            "provider": "chargily",
            "api_key": self.chargily_api_key,
            "secret_key": self.chargily_secret_key,
            "webhook_secret": self.chargily_webhook_secret,
            "mode": self.chargily_mode,
            "currency": "DZD"
        }
    elif self.payment_provider == "stripe":
        return {
            "provider": "stripe",
            "secret_key": self.stripe_secret_key,
            "public_key": self.stripe_public_key,
            "webhook_secret": self.stripe_webhook_secret,
            "currency": "CHF"
        }
    return {}
```

### 5.2 Creer un Service de Paiement Abstrait

Creer: `core/services/api/app/services/payment_service.py`

```python
"""
Payment Service - Abstraction for multi-region payments
Supports: Chargily (Algeria) and Stripe (Switzerland)
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from app.config import get_settings

settings = get_settings()


class PaymentProvider(ABC):
    """Abstract base class for payment providers"""

    @abstractmethod
    async def create_checkout(self, amount: float, currency: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def verify_webhook(self, payload: bytes, signature: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        pass


class ChargilyProvider(PaymentProvider):
    """Chargily payment provider for Algeria"""

    def __init__(self):
        self.api_key = settings.chargily_api_key
        self.secret_key = settings.chargily_secret_key
        self.api_url = settings.chargily_api_url

    async def create_checkout(self, amount: float, currency: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation for Chargily
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/checkouts",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "amount": int(amount * 100),
                    "currency": currency or "DZD",
                    "metadata": metadata
                }
            )
            return response.json()

    async def verify_webhook(self, payload: bytes, signature: str) -> Dict[str, Any]:
        # Chargily webhook verification
        import hmac
        import hashlib
        expected = hmac.new(
            self.secret_key.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        if hmac.compare_digest(expected, signature):
            import json
            return json.loads(payload)
        raise ValueError("Invalid webhook signature")

    async def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/checkouts/{payment_id}",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            return response.json()


class StripeProvider(PaymentProvider):
    """Stripe payment provider for Switzerland"""

    def __init__(self):
        import stripe
        stripe.api_key = settings.stripe_secret_key
        self.stripe = stripe

    async def create_checkout(self, amount: float, currency: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        session = self.stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": currency or "chf",
                    "unit_amount": int(amount * 100),
                    "product_data": {"name": metadata.get("product_name", "IAFactory Credits")}
                },
                "quantity": 1
            }],
            mode="payment",
            metadata=metadata
        )
        return {"checkout_url": session.url, "session_id": session.id}

    async def verify_webhook(self, payload: bytes, signature: str) -> Dict[str, Any]:
        event = self.stripe.Webhook.construct_event(
            payload, signature, settings.stripe_webhook_secret
        )
        return event

    async def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        session = self.stripe.checkout.Session.retrieve(payment_id)
        return {"status": session.payment_status, "amount": session.amount_total}


def get_payment_provider() -> PaymentProvider:
    """Factory function to get the appropriate payment provider"""
    if settings.payment_provider == "stripe":
        return StripeProvider()
    return ChargilyProvider()
```

### 5.3 Creer Scripts de Deploiement

Creer: `shared/scripts/deploy.sh`

```bash
#!/bin/bash
# ═══════════════════════════════════════════════════════════
# IAFACTORY PLATFORM - DEPLOYMENT SCRIPT
# ═══════════════════════════════════════════════════════════

set -e

REGION=$1
ENVIRONMENT=${2:-development}

if [ -z "$REGION" ]; then
    echo "Usage: ./deploy.sh <algeria|switzerland> [development|production]"
    exit 1
fi

if [ "$REGION" != "algeria" ] && [ "$REGION" != "switzerland" ]; then
    echo "Error: Invalid region. Use 'algeria' or 'switzerland'"
    exit 1
fi

echo "═══════════════════════════════════════════════════════════"
echo "  DEPLOYING IAFACTORY PLATFORM"
echo "  Region: $REGION"
echo "  Environment: $ENVIRONMENT"
echo "═══════════════════════════════════════════════════════════"

# Navigate to deployment directory
DEPLOY_DIR="deployments/$REGION"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"

cd "$ROOT_DIR/$DEPLOY_DIR"

# Select environment file
if [ "$ENVIRONMENT" == "production" ]; then
    if [ ! -f ".env.production" ]; then
        echo "Error: .env.production not found"
        exit 1
    fi
    ENV_FILE=".env.production"
    COMPOSE_FILE="docker-compose.prod.yml"
else
    if [ ! -f ".env" ]; then
        echo "Copying .env.example to .env..."
        cp .env.example .env
    fi
    ENV_FILE=".env"
    COMPOSE_FILE="docker-compose.yml"
fi

# Load environment
export $(cat $ENV_FILE | grep -v '^#' | xargs)

echo ""
echo "Step 1: Pulling latest Docker images..."
docker-compose -f $COMPOSE_FILE pull

echo ""
echo "Step 2: Building custom images..."
docker-compose -f $COMPOSE_FILE build

echo ""
echo "Step 3: Stopping existing containers..."
docker-compose -f $COMPOSE_FILE down --remove-orphans

echo ""
echo "Step 4: Starting new containers..."
docker-compose -f $COMPOSE_FILE up -d

echo ""
echo "Step 5: Waiting for services to be healthy..."
sleep 15

echo ""
echo "Step 6: Running database migrations..."
docker-compose -f $COMPOSE_FILE exec -T iaf-backend alembic upgrade head || echo "No migrations to run"

echo ""
echo "Step 7: Health check..."
HEALTH_URL="http://localhost:8000/health"
if [ "$REGION" == "switzerland" ]; then
    HEALTH_URL="http://localhost:8001/health"
fi

HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_URL)
if [ "$HTTP_STATUS" == "200" ]; then
    echo "[OK] API is healthy!"
else
    echo "[WARNING] API health check returned: $HTTP_STATUS"
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  DEPLOYMENT COMPLETE!"
echo "═══════════════════════════════════════════════════════════"
echo "  Region: $REGION"
echo "  Environment: $ENVIRONMENT"
echo ""
echo "  Services running:"
docker-compose -f $COMPOSE_FILE ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"
echo ""
echo "═══════════════════════════════════════════════════════════"
```

### 5.4 Creer Script de Backup

Creer: `deployments/algeria/scripts/backup.sh` et `deployments/switzerland/scripts/backup.sh`

```bash
#!/bin/bash
# ═══════════════════════════════════════════════════════════
# IAFACTORY - BACKUP SCRIPT
# ═══════════════════════════════════════════════════════════

set -e

REGION=${1:-algeria}
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="./backups/$TIMESTAMP"

echo "═══════════════════════════════════════════════════════════"
echo "  BACKUP IAFACTORY - $REGION"
echo "  Timestamp: $TIMESTAMP"
echo "═══════════════════════════════════════════════════════════"

mkdir -p $BACKUP_DIR

echo ""
echo "Step 1: Backing up PostgreSQL..."
docker-compose exec -T iaf-postgres pg_dump -U $POSTGRES_USER $POSTGRES_DB > "$BACKUP_DIR/database.sql"
echo "[OK] Database backup created"

echo ""
echo "Step 2: Backing up Qdrant..."
docker-compose exec -T iaf-qdrant curl -X POST "http://localhost:6333/collections/documents/snapshots" > "$BACKUP_DIR/qdrant_snapshot.json"
echo "[OK] Qdrant snapshot created"

echo ""
echo "Step 3: Backing up Redis..."
docker-compose exec -T iaf-redis redis-cli BGSAVE
sleep 5
docker cp $(docker-compose ps -q iaf-redis):/data/dump.rdb "$BACKUP_DIR/redis.rdb"
echo "[OK] Redis backup created"

echo ""
echo "Step 4: Backing up configuration..."
cp .env "$BACKUP_DIR/.env.backup"
cp docker-compose.yml "$BACKUP_DIR/docker-compose.yml.backup"
echo "[OK] Configuration backup created"

echo ""
echo "Step 5: Compressing backup..."
tar -czf "backups/backup_${REGION}_${TIMESTAMP}.tar.gz" -C backups $TIMESTAMP
rm -rf $BACKUP_DIR
echo "[OK] Backup compressed"

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  BACKUP COMPLETE!"
echo "  File: backups/backup_${REGION}_${TIMESTAMP}.tar.gz"
echo "═══════════════════════════════════════════════════════════"
```

### TEST PHASE 5

```bash
cd D:\IAFactory\iafactory-platform

# Verifier les scripts
if exist "shared\scripts\deploy.sh" (
    echo [OK] Script deploy present
) else (
    echo [ERREUR] Script deploy manquant
)

# Verifier le service de paiement
if exist "core\services\api\app\services\payment_service.py" (
    echo [OK] Service paiement present
) else (
    echo [ERREUR] Service paiement manquant
)

# Syntaxe Python
python -m py_compile core\services\api\app\services\payment_service.py
if %errorlevel% == 0 (
    echo [OK] Syntaxe Python valide
) else (
    echo [ERREUR] Erreur de syntaxe Python
)
```

---

## PHASE 6: TESTS & VALIDATION

**Duree: 2-4 heures**
**Criticite: HAUTE**

### 6.1 Test Local Algerie

```bash
cd D:\IAFactory\iafactory-platform\deployments\algeria

# Copier le fichier env
copy .env.example .env

# Lancer les services
docker-compose up -d

# Attendre que les services demarrent
timeout /t 30

# Verifier les services
docker-compose ps

# Test API health
curl http://localhost:8000/health

# Test Frontend
start http://localhost:3000
```

### 6.2 Test Local Suisse

```bash
cd D:\IAFactory\iafactory-platform\deployments\switzerland

# Copier le fichier env
copy .env.example .env

# Lancer les services (ports differents)
docker-compose up -d

# Attendre
timeout /t 30

# Verifier les services
docker-compose ps

# Test API health
curl http://localhost:8001/health

# Test Frontend
start http://localhost:3001
```

### 6.3 Tests Automatises

Creer: `shared/scripts/test.sh`

```bash
#!/bin/bash
# ═══════════════════════════════════════════════════════════
# IAFACTORY - TEST SUITE
# ═══════════════════════════════════════════════════════════

set -e

echo "═══════════════════════════════════════════════════════════"
echo "  RUNNING IAFACTORY TEST SUITE"
echo "═══════════════════════════════════════════════════════════"

# Test 1: Backend API Tests
echo ""
echo "Test 1: Running Backend API Tests..."
cd core/services/api
python -m pytest tests/ -v --tb=short || echo "Warning: Some tests failed"
cd ../../..

# Test 2: Frontend Type Check
echo ""
echo "Test 2: Running Frontend Type Check..."
cd core/frontend/main-ui
npm run type-check || echo "Warning: Type errors found"
cd ../../..

# Test 3: Linting
echo ""
echo "Test 3: Running Linters..."
cd core/services/api
python -m flake8 app/ --max-line-length=120 || echo "Warning: Linting issues found"
cd ../../..

# Test 4: Docker Build Test
echo ""
echo "Test 4: Testing Docker Builds..."
docker build -t iaf-backend-test core/services/api/
docker build -t iaf-frontend-test core/frontend/main-ui/
echo "[OK] Docker builds successful"

# Test 5: Configuration Validation
echo ""
echo "Test 5: Validating Configurations..."
for region in algeria switzerland; do
    if [ -f "deployments/$region/.env.example" ]; then
        echo "[OK] $region .env.example exists"
    else
        echo "[FAIL] $region .env.example missing"
    fi
    if [ -f "deployments/$region/docker-compose.yml" ]; then
        docker-compose -f deployments/$region/docker-compose.yml config > /dev/null
        echo "[OK] $region docker-compose.yml is valid"
    else
        echo "[FAIL] $region docker-compose.yml missing"
    fi
done

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  TEST SUITE COMPLETE"
echo "═══════════════════════════════════════════════════════════"
```

### 6.4 Checklist de Validation Manuelle

```
[ ] API Algerie repond sur http://localhost:8000/health
[ ] API Suisse repond sur http://localhost:8001/health
[ ] Frontend Algerie accessible sur http://localhost:3000
[ ] Frontend Suisse accessible sur http://localhost:3001
[ ] Login/Register fonctionne (les 2 regions)
[ ] Chat avec agent fonctionne
[ ] Upload document fonctionne
[ ] Recherche RAG fonctionne
[ ] Traductions s'affichent correctement (FR/AR/EN/DZ pour Algerie)
[ ] Traductions s'affichent correctement (FR/DE/IT/EN pour Suisse)
```

---

## PHASE 7: DEPLOIEMENT PRODUCTION

**Duree: 1-2 heures**
**Criticite: CRITIQUE**

### 7.1 Preparation Production

```bash
# Sur le VPS Algerie (Alger)
ssh user@vps-algeria.iafactory-algeria.com

# Cloner le monorepo
git clone https://github.com/iafactory/iafactory-platform.git
cd iafactory-platform

# Creer les fichiers production
cd deployments/algeria
cp .env.example .env.production
# EDITER .env.production avec les vraies valeurs

# Sur le VPS Suisse (Geneve)
ssh user@vps-switzerland.iafactory.ch

# Cloner le monorepo
git clone https://github.com/iafactory/iafactory-platform.git
cd iafactory-platform

# Creer les fichiers production
cd deployments/switzerland
cp .env.example .env.production
# EDITER .env.production avec les vraies valeurs
```

### 7.2 Deploiement Algerie

```bash
# Sur VPS Algerie
cd /home/user/iafactory-platform
./shared/scripts/deploy.sh algeria production

# Verifier
curl https://api.iafactory-algeria.com/health
```

### 7.3 Deploiement Suisse

```bash
# Sur VPS Suisse
cd /home/user/iafactory-platform
./shared/scripts/deploy.sh switzerland production

# Verifier
curl https://api.iafactory.ch/health
```

### 7.4 Configuration DNS

```
# Algerie (registrar DZ ou international)
api.iafactory-algeria.com    A    <IP_VPS_ALGER>
app.iafactory-algeria.com    A    <IP_VPS_ALGER>

# Suisse (registrar CH)
api.iafactory.ch             A    <IP_VPS_GENEVE>
app.iafactory.ch             A    <IP_VPS_GENEVE>
```

### 7.5 Configuration SSL (Let's Encrypt)

```bash
# Algerie
certbot --nginx -d api.iafactory-algeria.com -d app.iafactory-algeria.com

# Suisse
certbot --nginx -d api.iafactory.ch -d app.iafactory.ch
```

---

## PROCEDURES DE ROLLBACK

### Rollback Complet

```bash
# Si la migration echoue completement

# 1. Arreter tous les nouveaux services
cd D:\IAFactory\iafactory-platform\deployments\algeria
docker-compose down

cd D:\IAFactory\iafactory-platform\deployments\switzerland
docker-compose down

# 2. Restaurer l'ancien rag-dz depuis le backup
cd D:\IAFactory
xcopy /E /I "BACKUPS\pre-migration_*\rag-dz-backup" "rag-dz-restored"

# 3. Relancer l'ancien systeme
cd rag-dz-restored
docker-compose up -d

# 4. Verifier
curl http://localhost:8000/health
```

### Rollback Base de Donnees

```bash
# Si les donnees sont corrompues

# 1. Arreter le backend
docker-compose stop iaf-backend

# 2. Restaurer la base
docker-compose exec -T iaf-postgres psql -U postgres -c "DROP DATABASE IF EXISTS iafactory_dz"
docker-compose exec -T iaf-postgres psql -U postgres -c "CREATE DATABASE iafactory_dz"
docker-compose exec -T iaf-postgres psql -U postgres -d iafactory_dz < "D:\IAFactory\BACKUPS\pre-migration\db_backup.sql"

# 3. Relancer
docker-compose start iaf-backend
```

### Rollback d'un Service Specifique

```bash
# Si un seul service pose probleme

# 1. Identifier le service
docker-compose logs iaf-backend --tail=100

# 2. Rollback vers l'image precedente
docker-compose stop iaf-backend
docker-compose rm iaf-backend
# Modifier docker-compose.yml pour utiliser l'ancienne image/version
docker-compose up -d iaf-backend
```

---

## CHECKLIST FINALE

### Pre-Migration

- [ ] Backup complet de rag-dz effectue
- [ ] Backup base de donnees effectue
- [ ] Tous les services rag-dz actuels arretes
- [ ] Acces VPS Algerie confirme
- [ ] Acces VPS Suisse confirme
- [ ] API keys LLM disponibles

### Structure Monorepo

- [ ] Dossier iafactory-platform cree
- [ ] Structure core/ complete
- [ ] Structure deployments/ complete
- [ ] Structure shared/ complete
- [ ] Fichiers root (package.json, turbo.json) crees

### Migration Code

- [ ] 28 apps migrees dans core/apps/
- [ ] 15+ agents migres dans core/agents/
- [ ] Backend API migre dans core/services/
- [ ] 4 frontends migres dans core/frontend/
- [ ] Workflows migres dans core/workflows/
- [ ] Infrastructure migree

### Configuration Regions

- [ ] .env.example Algerie cree
- [ ] .env.example Suisse cree
- [ ] docker-compose.yml Algerie cree
- [ ] docker-compose.yml Suisse cree
- [ ] Traductions FR/AR/EN/DZ creees
- [ ] Traductions FR/DE/IT/EN creees

### Adaptation Code

- [ ] config.py modifie pour multi-region
- [ ] payment_service.py cree
- [ ] Scripts deploy.sh crees
- [ ] Scripts backup.sh crees

### Tests

- [ ] Tests backend passes
- [ ] Tests frontend passes
- [ ] Docker builds reussis
- [ ] Test local Algerie OK
- [ ] Test local Suisse OK
- [ ] Validation manuelle complete

### Production

- [ ] Git push vers GitHub
- [ ] Deploy VPS Algerie reussi
- [ ] Deploy VPS Suisse reussi
- [ ] DNS configure
- [ ] SSL configure
- [ ] Health checks OK
- [ ] Monitoring active

### Post-Migration

- [ ] Ancien rag-dz archive
- [ ] Documentation mise a jour
- [ ] Equipe informee
- [ ] Procedures rollback testees

---

## RESUME EXECUTIF

| Phase | Duree | Actions Principales |
|-------|-------|---------------------|
| **1. Backup** | 30 min | Backup complet rag-dz + BDD |
| **2. Structure** | 15 min | Creer arborescence monorepo |
| **3. Migration** | 2-3h | Copier code core depuis rag-dz |
| **4. Config** | 1-2h | Creer .env et docker-compose par region |
| **5. Adaptation** | 2-4h | Modifier code pour multi-region |
| **6. Tests** | 2-4h | Tests locaux et automatises |
| **7. Production** | 1-2h | Deploy VPS + DNS + SSL |

**TOTAL: 5-7 jours**

---

*Document genere par Claude Code - PROMPT 5*
*Date: 29 Decembre 2025*
*Basé sur: ARCHITECTURE_OPTIMALE.md + RAG_DZ_COMPLET.md*
