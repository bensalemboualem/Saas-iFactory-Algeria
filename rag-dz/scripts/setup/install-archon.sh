#!/bin/bash
# ================================================================
# INSTALLATION AUTOMATIQUE ARCHON - IAFactory Algeria
# ================================================================
set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "================================================================"
echo "🚀 INSTALLATION ARCHON SUR VPS"
echo "================================================================"
echo ""

# Aller dans le répertoire
echo -e "${BLUE}[1/5]${NC} Navigation..."
cd /opt/iafactory-rag-dz || { echo "❌ Erreur: /opt/iafactory-rag-dz n'existe pas"; exit 1; }
echo -e "${GREEN}✅ Dans: $(pwd)${NC}"

# Nettoyer et créer le dossier
echo ""
echo -e "${BLUE}[2/5]${NC} Préparation..."
rm -rf frontend/archon-ui-stable
mkdir -p frontend/archon-ui-stable
cd frontend/archon-ui-stable
echo -e "${GREEN}✅ Dossier prêt${NC}"

# Cloner Archon
echo ""
echo -e "${BLUE}[3/5]${NC} Clonage Archon depuis GitHub..."
git clone https://github.com/coleam00/Archon.git . || { echo "❌ Erreur git clone"; exit 1; }
echo -e "${GREEN}✅ Archon cloné${NC}"

# Créer .env
echo ""
echo -e "${BLUE}[4/5]${NC} Configuration Supabase..."
cat > .env << 'EOF'
SUPABASE_URL=https://cxzcmmolfgijhjbevtzi.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN4emNtbW9sZmdpamhqYmV2dHppIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NDg3MjY1NSwiZXhwIjoyMDgwNDQ4NjU1fQ.MMfoTv4RRcbUSuuQDEDWlUZM9bzoK-t0cCQ7jcCISh0
LOG_LEVEL=INFO
HOST=localhost
ARCHON_SERVER_PORT=8181
ARCHON_MCP_PORT=8051
ARCHON_AGENTS_PORT=8052
ARCHON_UI_PORT=3737
VITE_ALLOWED_HOSTS=www.iafactoryalgeria.com,iafactoryalgeria.com
VITE_SHOW_DEVTOOLS=false
PROD=false
EOF
echo -e "${GREEN}✅ Configuration créée${NC}"

# Lancer Docker
echo ""
echo -e "${BLUE}[5/5]${NC} Lancement Docker (2-5 minutes)..."
echo -e "${YELLOW}⏳ Building images...${NC}"
docker compose up -d --build

echo ""
echo -e "${YELLOW}⏳ Attente 30 secondes pour le démarrage...${NC}"
sleep 30

echo ""
echo "================================================================"
echo -e "${GREEN}✅ ✅ ✅ ARCHON INSTALLÉ! ✅ ✅ ✅${NC}"
echo "================================================================"
echo ""
echo "📊 STATUS DES SERVICES:"
docker compose ps
echo ""
echo "🌐 SERVICES:"
echo "  • Backend API:  http://localhost:8181"
echo "  • MCP Server:   http://localhost:8051"
echo "  • Frontend UI:  http://localhost:3737"
echo ""
echo "🔧 COMMANDES:"
echo "  • Logs:    docker compose logs -f"
echo "  • Status:  docker compose ps"
echo "  • Restart: docker compose restart"
echo ""
echo "✅ Installation terminée!"
echo ""
