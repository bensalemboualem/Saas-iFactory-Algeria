# PRP-001: Project Setup

> **Priorité**: P0  
> **Effort**: 2-3 heures  
> **Dépendances**: Aucune

---

## Objectif

Créer la structure de base du projet Nexus fusionnant BMAD, Archon et bolt.diy.

---

## Tâches

### T1: Vérification Environnement
**Effort**: 10 min

```bash
# Vérifier les prérequis
docker --version       # >= 24.0
docker compose version # >= 2.20
git --version          # >= 2.40
node --version         # >= 20.0
python --version       # >= 3.11

# Si un prérequis manque, l'installer avant de continuer
```

**Validation**: Toutes les commandes retournent une version valide.

---

### T2: Structure Monorepo
**Effort**: 15 min

```bash
# Créer la structure
mkdir -p orchestrators/{meta,bmad,archon,bolt}/src
mkdir -p orchestrators/shared
mkdir -p {scripts,docs,requirements}
mkdir -p .claude/{agents,commands}

# Créer les __init__.py
touch orchestrators/__init__.py
touch orchestrators/{meta,bmad,archon,bolt}/src/__init__.py
touch orchestrators/shared/__init__.py

# Vérifier
find . -type d | head -20
```

**Validation**: Structure créée selon l'arborescence définie dans CLAUDE.md.

---

### T3: Submodules Git
**Effort**: 20 min

```bash
# Ajouter les submodules (si pas déjà présents)
git submodule add https://github.com/BMadCode/bmad-method.git bmad 2>/dev/null || echo "BMAD existe"
git submodule add https://github.com/coleam00/archon.git archon 2>/dev/null || echo "Archon existe"
git submodule add https://github.com/stackblitz-labs/bolt.diy.git bolt-diy 2>/dev/null || echo "Bolt existe"

# Initialiser
git submodule update --init --recursive
```

**Validation**: Les 3 dossiers bmad/, archon/, bolt-diy/ contiennent du code.

---

### T4: Docker Compose
**Effort**: 30 min

Créer `docker-compose.yml`:

```yaml
version: '3.9'

services:
  # ============ ORCHESTRATORS ============
  meta-orchestrator:
    build: ./orchestrators/meta
    ports:
      - "${META_PORT:-8100}:8100"
    environment:
      - REDIS_URL=redis://redis:6379
      - BMAD_URL=http://bmad-orchestrator:8052
      - ARCHON_URL=http://archon-server:8181
      - BOLT_URL=http://bolt-app:5173
    depends_on:
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8100/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - nexus

  # ============ ARCHON ============
  archon-server:
    build: ./archon/python
    ports:
      - "${ARCHON_SERVER_PORT:-8181}:8181"
    environment:
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_SERVICE_KEY=${SUPABASE_SERVICE_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      redis:
        condition: service_healthy
    networks:
      - nexus

  archon-mcp:
    build:
      context: ./archon/python
      target: mcp
    ports:
      - "${ARCHON_MCP_PORT:-8051}:8051"
    depends_on:
      - archon-server
    networks:
      - nexus

  archon-ui:
    build: ./archon/archon-ui-main
    ports:
      - "${ARCHON_UI_PORT:-3737}:3737"
    depends_on:
      - archon-server
    networks:
      - nexus

  # ============ BOLT ============
  bolt-app:
    build: ./bolt-diy
    ports:
      - "${BOLT_PORT:-5173}:5173"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    networks:
      - nexus

  # ============ INFRASTRUCTURE ============
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3
    networks:
      - nexus

volumes:
  redis-data:

networks:
  nexus:
    driver: bridge
```

**Validation**: `docker compose config` ne retourne pas d'erreur.

---

### T5: Variables d'Environnement
**Effort**: 10 min

Créer `.env.example`:

```env
# ============ PORTS ============
META_PORT=8100
ARCHON_SERVER_PORT=8181
ARCHON_MCP_PORT=8051
ARCHON_UI_PORT=3737
BOLT_PORT=5173

# ============ DATABASE ============
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_KEY=your-service-key

# ============ LLM PROVIDERS ============
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-ant-xxx
DEEPSEEK_API_KEY=xxx
GROQ_API_KEY=gsk_xxx
GEMINI_API_KEY=xxx

# ============ ALGERIA ============
CHARGILY_API_KEY=xxx
CHARGILY_SECRET_KEY=xxx

# ============ OPTIONAL ============
NETLIFY_TOKEN=xxx
VERCEL_TOKEN=xxx
```

Créer `.gitignore`:
```
.env
.env.local
.env.production
__pycache__/
node_modules/
*.pyc
.DS_Store
```

**Validation**: `.env.example` existe et contient toutes les variables.

---

### T6: Scripts de Démarrage
**Effort**: 15 min

Créer `scripts/start.sh`:
```bash
#!/bin/bash
set -e

echo "🚀 Démarrage Nexus AI Platform..."

if [ ! -f .env ]; then
    echo "❌ .env manquant. Copiez .env.example → .env"
    exit 1
fi

docker compose up -d --build

echo "⏳ Attente des services (30s)..."
sleep 30

echo "🔍 Vérification..."
./scripts/health-check.sh

echo "✅ Nexus démarré!"
echo ""
echo "📍 Services:"
echo "   Meta-Orchestrator: http://localhost:8100"
echo "   Archon UI:         http://localhost:3737"
echo "   Archon API:        http://localhost:8181"
echo "   Bolt.diy:          http://localhost:5173"
```

Créer `scripts/stop.sh`:
```bash
#!/bin/bash
echo "🛑 Arrêt Nexus..."
docker compose down
echo "✅ Arrêté"
```

Créer `scripts/health-check.sh`:
```bash
#!/bin/bash
echo "🔍 Health Check..."

check_service() {
    if curl -sf "$1/health" > /dev/null 2>&1; then
        echo "  ✅ $2"
    else
        echo "  ❌ $2"
    fi
}

check_service "http://localhost:8100" "Meta-Orchestrator"
check_service "http://localhost:8181" "Archon Server"
check_service "http://localhost:3737" "Archon UI"
```

```bash
chmod +x scripts/*.sh
```

**Validation**: `./scripts/health-check.sh` s'exécute sans erreur.

---

### T7: Dockerfile Meta-Orchestrator
**Effort**: 20 min

Créer `orchestrators/meta/Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

EXPOSE 8100

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8100/health || exit 1

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8100"]
```

Créer `orchestrators/meta/requirements.txt`:
```
fastapi>=0.109.0
uvicorn>=0.27.0
redis>=5.0.0
httpx>=0.26.0
pydantic>=2.5.0
python-dotenv>=1.0.0
```

Créer `orchestrators/meta/src/main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Nexus Meta-Orchestrator", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "meta-orchestrator", "version": "1.0.0"}

@app.get("/status")
async def status():
    return {"meta": "online", "services": {"bmad": "pending", "archon": "pending", "bolt": "pending"}}
```

**Validation**: `docker build -t meta-test ./orchestrators/meta` réussit.

---

### T8: README.md
**Effort**: 15 min

Créer `README.md` avec documentation utilisateur.

**Validation**: README.md présent et lisible.

---

## Critères de Complétion

- [ ] T1: Environnement vérifié
- [ ] T2: Structure créée
- [ ] T3: Submodules clonés
- [ ] T4: docker-compose.yml valide
- [ ] T5: .env.example créé
- [ ] T6: Scripts fonctionnels
- [ ] T7: Dockerfile Meta OK
- [ ] T8: README.md présent

---

## Prochaine étape

→ **PRP-002**: Meta-Orchestrator complet
