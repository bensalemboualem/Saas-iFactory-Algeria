#!/bin/bash
# =====================================================
# DÉPLOIEMENT ARCHON SUR VPS - IAFactory Algeria
# =====================================================
set -e

echo "=========================================="
echo "🚀 DÉPLOIEMENT ARCHON"
echo "=========================================="
echo ""

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. Aller dans le répertoire projet
echo -e "${BLUE}[1/6]${NC} Navigation vers le répertoire..."
cd /opt/iafactory-rag-dz
echo -e "${GREEN}✅ Répertoire: $(pwd)${NC}"

# 2. Créer et nettoyer le dossier Archon
echo ""
echo -e "${BLUE}[2/6]${NC} Préparation du dossier Archon..."
rm -rf frontend/archon-ui-stable
mkdir -p frontend/archon-ui-stable
cd frontend/archon-ui-stable
echo -e "${GREEN}✅ Dossier créé et nettoyé${NC}"

# 3. Cloner Archon depuis GitHub
echo ""
echo -e "${BLUE}[3/6]${NC} Clonage d'Archon depuis GitHub..."
git clone https://github.com/coleam00/Archon.git .
echo -e "${GREEN}✅ Archon cloné${NC}"

# 4. Créer le fichier .env avec Supabase
echo ""
echo -e "${BLUE}[4/6]${NC} Configuration de l'environnement..."
cat > .env << 'EOF'
# Configuration Archon - IAFactory Algeria
# Generated: $(date)

# Supabase Connection (REQUIRED)
SUPABASE_URL=https://cxzcmmolfgijhjbevtzi.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN4emNtbW9sZmdpamhqYmV2dHppIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NDg3MjY1NSwiZXhwIjoyMDgwNDQ4NjU1fQ.MMfoTv4RRcbUSuuQDEDWlUZM9bzoK-t0cCQ7jcCISh0

# Optional: Logging
LOGFIRE_TOKEN=
LOG_LEVEL=INFO

# Service Ports Configuration
HOST=localhost
ARCHON_SERVER_PORT=8181
ARCHON_MCP_PORT=8051
ARCHON_AGENTS_PORT=8052
ARCHON_UI_PORT=3737
ARCHON_DOCS_PORT=3838

# Frontend Configuration
VITE_ALLOWED_HOSTS=www.iafactoryalgeria.com,iafactoryalgeria.com,localhost
VITE_SHOW_DEVTOOLS=false

# Production mode
PROD=false
EOF
echo -e "${GREEN}✅ Fichier .env créé${NC}"

# 5. Lancer Docker Compose
echo ""
echo -e "${BLUE}[5/6]${NC} Démarrage des services Docker (cela peut prendre 2-5 minutes)..."
echo -e "${YELLOW}⏳ Building images...${NC}"
docker compose up -d --build

# Attendre que les services démarrent
echo ""
echo -e "${YELLOW}⏳ Attente du démarrage des services (30 secondes)...${NC}"
sleep 30

# 6. Vérifier le statut
echo ""
echo -e "${BLUE}[6/6]${NC} Vérification des services..."
docker compose ps

echo ""
echo "=========================================="
echo -e "${GREEN}✅ DÉPLOIEMENT TERMINÉ${NC}"
echo "=========================================="
echo ""
echo "📊 Services Archon déployés:"
echo "  • Backend API:  http://localhost:8181"
echo "  • MCP Server:   http://localhost:8051"
echo "  • Frontend UI:  http://localhost:3737"
echo ""
echo "🔧 Commandes utiles:"
echo "  • Logs:         docker compose logs -f"
echo "  • Status:       docker compose ps"
echo "  • Restart:      docker compose restart"
echo "  • Stop:         docker compose down"
echo ""
echo "⚠️  PROCHAINE ÉTAPE:"
echo "  Configurer Nginx pour router /archon-ui/ vers port 3737"
echo ""
