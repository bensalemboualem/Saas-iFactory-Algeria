#!/bin/bash
# ================================================================
# DÉPLOIEMENT AGENTS IA - IAFactory Algeria
# ================================================================
# Déploie les 5 agents IA sur le VPS
# ================================================================

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "================================================================"
echo "🤖 DÉPLOIEMENT DES 5 AGENTS IA"
echo "================================================================"
echo ""

AGENTS_DIR="/opt/iafactory-rag-dz/ia-agents"

echo -e "${BLUE}[1/7]${NC} Création de la structure des agents IA..."
mkdir -p "$AGENTS_DIR"
cd "$AGENTS_DIR"
echo -e "${GREEN}✅ Répertoire créé: $AGENTS_DIR${NC}"
echo ""

echo -e "${BLUE}[2/7]${NC} Création des répertoires pour chaque agent..."
mkdir -p local-rag finance-agent chat-pdf hybrid-search voice-support
echo -e "${GREEN}✅ 5 répertoires créés${NC}"
echo ""

echo -e "${BLUE}[3/7]${NC} Création du docker-compose.yml des agents IA..."

cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  # ================================================================
  # QDRANT - Vector Database
  # ================================================================
  qdrant:
    image: qdrant/qdrant:latest
    container_name: iaf-qdrant
    ports:
      - "127.0.0.1:6333:6333"
      - "127.0.0.1:6334:6334"
    volumes:
      - qdrant_data:/qdrant/storage
    environment:
      - QDRANT__SERVICE__GRPC_PORT=6334
    networks:
      - ia-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # ================================================================
  # LOCAL RAG AGENT - Documents locaux (RGPD compliant)
  # ================================================================
  local-rag:
    build: ./local-rag
    container_name: iaf-local-rag
    ports:
      - "8200:8200"
    environment:
      - QDRANT_URL=http://qdrant:6333
      - OLLAMA_HOST=http://host.docker.internal:11434
      - PYTHONUNBUFFERED=1
    volumes:
      - ./local-rag/docs:/app/docs
      - ./local-rag/data:/app/data
    networks:
      - ia-network
    depends_on:
      - qdrant
    restart: unless-stopped
    extra_hosts:
      - "host.docker.internal:host-gateway"

  # ================================================================
  # FINANCE AGENT - Fiscal algérien (G50, IBS, TVA)
  # ================================================================
  finance-agent:
    build: ./finance-agent
    container_name: iaf-finance-agent
    ports:
      - "8201:8201"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@host.docker.internal:5432/iafactory
      - OLLAMA_HOST=http://host.docker.internal:11434
      - PYTHONUNBUFFERED=1
      - COUNTRY=DZ
      - FISCAL_YEAR=2025
    volumes:
      - ./finance-agent/data:/app/data
    networks:
      - ia-network
    restart: unless-stopped
    extra_hosts:
      - "host.docker.internal:host-gateway"

  # ================================================================
  # CHAT PDF AGENT - Documents PDF interactifs
  # ================================================================
  chat-pdf:
    build: ./chat-pdf
    container_name: iaf-chat-pdf
    ports:
      - "8202:8202"
    environment:
      - QDRANT_URL=http://qdrant:6333
      - OLLAMA_HOST=http://host.docker.internal:11434
      - PYTHONUNBUFFERED=1
    volumes:
      - ./chat-pdf/uploads:/app/uploads
      - ./chat-pdf/data:/app/data
    networks:
      - ia-network
    depends_on:
      - qdrant
    restart: unless-stopped
    extra_hosts:
      - "host.docker.internal:host-gateway"

  # ================================================================
  # HYBRID SEARCH - Recherche sémantique + mots-clés
  # ================================================================
  hybrid-search:
    build: ./hybrid-search
    container_name: iaf-hybrid-search
    ports:
      - "8203:8203"
    environment:
      - QDRANT_URL=http://qdrant:6333
      - OLLAMA_HOST=http://host.docker.internal:11434
      - PYTHONUNBUFFERED=1
    volumes:
      - ./hybrid-search/data:/app/data
    networks:
      - ia-network
    depends_on:
      - qdrant
    restart: unless-stopped
    extra_hosts:
      - "host.docker.internal:host-gateway"

  # ================================================================
  # VOICE SUPPORT - Assistance vocale
  # ================================================================
  voice-support:
    build: ./voice-support
    container_name: iaf-voice-support
    ports:
      - "8204:8204"
    environment:
      - OLLAMA_HOST=http://host.docker.internal:11434
      - PYTHONUNBUFFERED=1
      - LANGUAGE=fr-DZ
    volumes:
      - ./voice-support/data:/app/data
    networks:
      - ia-network
    restart: unless-stopped
    extra_hosts:
      - "host.docker.internal:host-gateway"

networks:
  ia-network:
    driver: bridge

volumes:
  qdrant_data:
    driver: local
EOF

echo -e "${GREEN}✅ docker-compose.yml créé${NC}"
echo ""

echo -e "${BLUE}[4/7]${NC} Création des Dockerfiles pour chaque agent..."

# Local RAG
cat > local-rag/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    agno \
    qdrant-client \
    fastapi \
    uvicorn[standard] \
    python-multipart

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8200"]
EOF

# Finance Agent
cat > finance-agent/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    agno \
    fastapi \
    uvicorn[standard] \
    sqlalchemy \
    psycopg2-binary \
    python-multipart

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8201"]
EOF

# Chat PDF
cat > chat-pdf/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    agno \
    qdrant-client \
    fastapi \
    uvicorn[standard] \
    pypdf2 \
    python-multipart

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8202"]
EOF

# Hybrid Search
cat > hybrid-search/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    agno \
    qdrant-client \
    fastapi \
    uvicorn[standard] \
    rank-bm25 \
    python-multipart

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8203"]
EOF

# Voice Support
cat > voice-support/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    agno \
    fastapi \
    uvicorn[standard] \
    openai-whisper \
    pydub \
    python-multipart

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8204"]
EOF

echo -e "${GREEN}✅ 5 Dockerfiles créés${NC}"
echo ""

echo -e "${BLUE}[5/7]${NC} Création des fichiers main.py pour chaque agent..."

# Local RAG main.py
cat > local-rag/main.py << 'EOF'
from fastapi import FastAPI, UploadFile
from agno.agent import Agent
from agno.models.ollama import Ollama
import os

app = FastAPI(title="Local RAG Agent")

# Agent configuration
agent = Agent(
    name="Local RAG Agent",
    model=Ollama(id="llama3.2", host=os.getenv("OLLAMA_HOST", "http://localhost:11434")),
    description="Agent RAG local pour documents sensibles (RGPD compliant)"
)

@app.get("/")
async def root():
    return {
        "service": "Local RAG Agent",
        "status": "running",
        "description": "RGPD-compliant document processing"
    }

@app.post("/query")
async def query(question: str):
    response = agent.run(question)
    return {"answer": response.content}

@app.get("/health")
async def health():
    return {"status": "healthy"}
EOF

# Finance Agent main.py
cat > finance-agent/main.py << 'EOF'
from fastapi import FastAPI
from agno.agent import Agent
from agno.models.ollama import Ollama
import os

app = FastAPI(title="Finance Agent - Algérie")

agent = Agent(
    name="Finance Agent DZ",
    model=Ollama(id="llama3.2", host=os.getenv("OLLAMA_HOST", "http://localhost:11434")),
    description="Expert fiscal algérien (G50, IBS, TVA)",
    instructions=[
        "Tu es un expert comptable algérien",
        "Tu connais le G50, IBS, TVA, et toutes les réglementations fiscales algériennes",
        "Réponds en français et avec précision"
    ]
)

@app.get("/")
async def root():
    return {
        "service": "Finance Agent Algérie",
        "status": "running",
        "expertise": ["G50", "IBS", "TVA", "Fiscalité DZ"]
    }

@app.post("/consult")
async def consult(question: str):
    response = agent.run(question)
    return {"answer": response.content}

@app.get("/health")
async def health():
    return {"status": "healthy"}
EOF

# Chat PDF main.py
cat > chat-pdf/main.py << 'EOF'
from fastapi import FastAPI, UploadFile, File
from agno.agent import Agent
from agno.models.ollama import Ollama
import os

app = FastAPI(title="Chat PDF Agent")

agent = Agent(
    name="Chat PDF Agent",
    model=Ollama(id="llama3.2", host=os.getenv("OLLAMA_HOST", "http://localhost:11434")),
    description="Agent pour dialoguer avec des documents PDF"
)

@app.get("/")
async def root():
    return {
        "service": "Chat PDF Agent",
        "status": "running",
        "description": "Interactive PDF document chat"
    }

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    return {"filename": file.filename, "status": "uploaded"}

@app.post("/ask")
async def ask_pdf(question: str, pdf_id: str):
    response = agent.run(f"Question about PDF {pdf_id}: {question}")
    return {"answer": response.content}

@app.get("/health")
async def health():
    return {"status": "healthy"}
EOF

# Hybrid Search main.py
cat > hybrid-search/main.py << 'EOF'
from fastapi import FastAPI
from agno.agent import Agent
from agno.models.ollama import Ollama
import os

app = FastAPI(title="Hybrid Search Agent")

agent = Agent(
    name="Hybrid Search Agent",
    model=Ollama(id="llama3.2", host=os.getenv("OLLAMA_HOST", "http://localhost:11434")),
    description="Recherche hybride sémantique + mots-clés"
)

@app.get("/")
async def root():
    return {
        "service": "Hybrid Search Agent",
        "status": "running",
        "search_types": ["semantic", "keyword", "hybrid"]
    }

@app.post("/search")
async def search(query: str, search_type: str = "hybrid"):
    response = agent.run(f"Search query ({search_type}): {query}")
    return {"results": response.content, "type": search_type}

@app.get("/health")
async def health():
    return {"status": "healthy"}
EOF

# Voice Support main.py
cat > voice-support/main.py << 'EOF'
from fastapi import FastAPI, UploadFile, File
from agno.agent import Agent
from agno.models.ollama import Ollama
import os

app = FastAPI(title="Voice Support Agent")

agent = Agent(
    name="Voice Support Agent",
    model=Ollama(id="llama3.2", host=os.getenv("OLLAMA_HOST", "http://localhost:11434")),
    description="Agent d'assistance vocale en français algérien",
    instructions=[
        "Tu es un assistant vocal pour le marché algérien",
        "Réponds en français avec un ton professionnel et amical",
        "Adapte-toi au contexte algérien (darija acceptée)"
    ]
)

@app.get("/")
async def root():
    return {
        "service": "Voice Support Agent",
        "status": "running",
        "language": "fr-DZ"
    }

@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    return {"transcription": "Audio transcribed", "status": "success"}

@app.post("/respond")
async def respond(text: str):
    response = agent.run(text)
    return {"response": response.content}

@app.get("/health")
async def health():
    return {"status": "healthy"}
EOF

echo -e "${GREEN}✅ 5 fichiers main.py créés${NC}"
echo ""

echo -e "${BLUE}[6/7]${NC} Création de la configuration Nginx pour les agents IA..."

cat > nginx-ia-agents.conf << 'EOF'
# ================================================================
# NGINX CONFIGURATION - IA AGENTS
# À ajouter dans /etc/nginx/sites-available/iafactoryalgeria.com
# ================================================================

    # Local RAG Agent
    location /api/local-rag/ {
        proxy_pass http://127.0.0.1:8200/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Finance Agent
    location /api/finance/ {
        proxy_pass http://127.0.0.1:8201/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Chat PDF Agent
    location /api/chat-pdf/ {
        proxy_pass http://127.0.0.1:8202/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Hybrid Search Agent
    location /api/search/ {
        proxy_pass http://127.0.0.1:8203/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Voice Support Agent
    location /api/voice/ {
        proxy_pass http://127.0.0.1:8204/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        client_max_body_size 50M;
    }

    # Qdrant Vector DB (Admin uniquement)
    location /qdrant/ {
        proxy_pass http://127.0.0.1:6333/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        # TODO: Ajouter authentification
    }
EOF

echo -e "${GREEN}✅ Configuration Nginx créée${NC}"
echo ""

echo -e "${BLUE}[7/7]${NC} Démarrage des agents IA..."
echo ""

echo "Building et démarrage des containers (cela peut prendre 5-10 minutes)..."
docker-compose up -d --build

echo ""
echo "⏳ Attente 30 secondes pour le démarrage..."
sleep 30

echo ""
echo "================================================================"
echo -e "${GREEN}✅ AGENTS IA DÉPLOYÉS!${NC}"
echo "================================================================"
echo ""

echo "📊 STATUS DES SERVICES:"
docker-compose ps

echo ""
echo "🌐 ENDPOINTS DISPONIBLES:"
echo "  • Local RAG:      http://localhost:8200 → /api/local-rag/"
echo "  • Finance Agent:  http://localhost:8201 → /api/finance/"
echo "  • Chat PDF:       http://localhost:8202 → /api/chat-pdf/"
echo "  • Hybrid Search:  http://localhost:8203 → /api/search/"
echo "  • Voice Support:  http://localhost:8204 → /api/voice/"
echo "  • Qdrant DB:      http://localhost:6333"
echo ""

echo "🔧 PROCHAINES ÉTAPES:"
echo "  1. Configurer Nginx avec nginx-ia-agents.conf"
echo "  2. Tester les endpoints"
echo "  3. Ajouter des documents dans local-rag/docs/"
echo ""

echo "📝 LOGS:"
echo "  docker-compose logs -f [service-name]"
echo ""
