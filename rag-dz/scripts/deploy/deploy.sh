#!/usr/bin/env bash
# ==============================================
# 🚀 IAFactory DZ/CH - Script de Déploiement
# ==============================================
# Usage: ./deploy.sh [options]
# Options:
#   --full      : Rebuild complet (tous les services)
#   --backend   : Backend uniquement
#   --frontend  : Frontend uniquement
#   --no-cache  : Build sans cache Docker
#   --logs      : Afficher les logs après déploiement
# ==============================================

set -e

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="${PROJECT_DIR:-$(pwd)}"
BRANCH="${BRANCH:-main}"
COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.yml}"

# Options par défaut
BUILD_BACKEND=true
BUILD_FRONTEND=false
NO_CACHE=""
SHOW_LOGS=false
FULL_BUILD=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --full)
            FULL_BUILD=true
            BUILD_FRONTEND=true
            shift
            ;;
        --backend)
            BUILD_BACKEND=true
            BUILD_FRONTEND=false
            shift
            ;;
        --frontend)
            BUILD_BACKEND=false
            BUILD_FRONTEND=true
            shift
            ;;
        --no-cache)
            NO_CACHE="--no-cache"
            shift
            ;;
        --logs)
            SHOW_LOGS=true
            shift
            ;;
        *)
            echo -e "${RED}Option inconnue: $1${NC}"
            exit 1
            ;;
    esac
done

echo -e "${PURPLE}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║     🚀 IAFactory DZ/CH - Déploiement Production               ║"
echo "║     Région: Algérie 🇩🇿 / Suisse 🇨🇭                            ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Vérification du répertoire
if [ ! -f "$PROJECT_DIR/$COMPOSE_FILE" ]; then
    echo -e "${RED}❌ Erreur: $COMPOSE_FILE non trouvé dans $PROJECT_DIR${NC}"
    exit 1
fi

cd "$PROJECT_DIR"

# ==============================================
# 1. Pull du code (si git)
# ==============================================
if [ -d ".git" ]; then
    echo -e "${CYAN}📥 Pull du dernier code depuis $BRANCH...${NC}"
    git fetch origin
    git pull origin $BRANCH || {
        echo -e "${YELLOW}⚠️ Conflits git détectés, tentative de stash...${NC}"
        git stash
        git pull origin $BRANCH
        git stash pop || true
    }
    echo -e "${GREEN}✓ Code mis à jour${NC}"
else
    echo -e "${YELLOW}⚠️ Pas de repo git, skip pull${NC}"
fi

# ==============================================
# 2. Vérification des prérequis
# ==============================================
echo -e "${CYAN}🔍 Vérification des prérequis...${NC}"

# Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker non installé${NC}"
    exit 1
fi

# Docker Compose
if ! docker compose version &> /dev/null; then
    echo -e "${RED}❌ Docker Compose non installé${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker et Docker Compose OK${NC}"

# ==============================================
# 3. Build des images
# ==============================================
echo -e "${CYAN}🐳 Build des images Docker...${NC}"

if [ "$FULL_BUILD" = true ]; then
    echo -e "${YELLOW}  → Build complet (tous les services)${NC}"
    docker compose -f $COMPOSE_FILE build $NO_CACHE
elif [ "$BUILD_BACKEND" = true ] && [ "$BUILD_FRONTEND" = true ]; then
    docker compose -f $COMPOSE_FILE build $NO_CACHE iafactory-backend iafactory-hub iafactory-docs
elif [ "$BUILD_BACKEND" = true ]; then
    echo -e "${YELLOW}  → Build backend uniquement${NC}"
    docker compose -f $COMPOSE_FILE build $NO_CACHE iafactory-backend
elif [ "$BUILD_FRONTEND" = true ]; then
    echo -e "${YELLOW}  → Build frontend uniquement${NC}"
    docker compose -f $COMPOSE_FILE build $NO_CACHE iafactory-hub iafactory-docs
fi

echo -e "${GREEN}✓ Build terminé${NC}"

# ==============================================
# 4. Arrêt des anciens conteneurs
# ==============================================
echo -e "${CYAN}⏹️ Arrêt des services...${NC}"
docker compose -f $COMPOSE_FILE down --remove-orphans || true
echo -e "${GREEN}✓ Services arrêtés${NC}"

# ==============================================
# 5. Démarrage des nouveaux conteneurs
# ==============================================
echo -e "${CYAN}⬆️ Démarrage des services...${NC}"
docker compose -f $COMPOSE_FILE up -d

# Attendre le démarrage
echo -e "${YELLOW}⏳ Attente du démarrage des services (15s)...${NC}"
sleep 15

# ==============================================
# 6. Vérification de la santé
# ==============================================
echo -e "${CYAN}🔍 Vérification de la santé des services...${NC}"

# Liste des services à vérifier
declare -A SERVICES=(
    ["Backend API"]="http://localhost:8180/health"
    ["Billing V2"]="http://localhost:8180/api/billing/v2/health"
    ["CRM PRO"]="http://localhost:8180/api/crm-pro/health"
    ["BIG RAG"]="http://localhost:8180/api/rag/multi/status"
    ["Darija NLP"]="http://localhost:8180/api/darija/status"
    ["Voice Agent"]="http://localhost:8180/api/voice/agent/status"
)

FAILED=0
for SERVICE in "${!SERVICES[@]}"; do
    URL="${SERVICES[$SERVICE]}"
    if curl -sf "$URL" > /dev/null 2>&1; then
        echo -e "${GREEN}  ✓ $SERVICE${NC}"
    else
        echo -e "${RED}  ✗ $SERVICE (${URL})${NC}"
        FAILED=$((FAILED + 1))
    fi
done

# ==============================================
# 7. État des conteneurs
# ==============================================
echo -e "${CYAN}📊 État des conteneurs:${NC}"
docker compose -f $COMPOSE_FILE ps

# ==============================================
# 8. Résumé
# ==============================================
echo ""
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║     ✅ DÉPLOIEMENT RÉUSSI                                      ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}🌐 URLs disponibles:${NC}"
    echo -e "   • API Docs:    http://localhost:8180/docs"
    echo -e "   • Hub:         http://localhost:8182"
    echo -e "   • Docs UI:     http://localhost:8183"
    echo -e "   • n8n:         http://localhost:8185"
    echo -e "   • Ollama:      http://localhost:8186"
else
    echo -e "${YELLOW}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║     ⚠️ DÉPLOIEMENT PARTIEL ($FAILED services en erreur)         ║${NC}"
    echo -e "${YELLOW}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo -e "${YELLOW}Vérifiez les logs: docker compose logs -f iafactory-backend${NC}"
fi

# ==============================================
# 9. Logs (optionnel)
# ==============================================
if [ "$SHOW_LOGS" = true ]; then
    echo -e "${CYAN}📋 Logs du backend:${NC}"
    docker compose -f $COMPOSE_FILE logs -f iafactory-backend
fi

exit $FAILED
