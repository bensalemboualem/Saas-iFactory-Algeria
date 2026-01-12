#!/bin/bash

# ============================================
# IAFACTORY VIDEO STUDIO PRO - SETUP SCRIPT
# ============================================

set -e

echo "🎬 IAFactory Video Studio Pro - Installation"
echo "============================================="

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Vérification des prérequis
check_prerequisites() {
    echo -e "\n${YELLOW}📋 Vérification des prérequis...${NC}"
    
    # Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        echo -e "${GREEN}✓ Python: $PYTHON_VERSION${NC}"
    else
        echo -e "${RED}✗ Python 3 non installé${NC}"
        exit 1
    fi
    
    # Node.js
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        echo -e "${GREEN}✓ Node.js: $NODE_VERSION${NC}"
    else
        echo -e "${RED}✗ Node.js non installé${NC}"
        exit 1
    fi
    
    # Docker
    if command -v docker &> /dev/null; then
        DOCKER_VERSION=$(docker --version)
        echo -e "${GREEN}✓ Docker: $DOCKER_VERSION${NC}"
    else
        echo -e "${YELLOW}⚠ Docker non installé (optionnel pour le dev local)${NC}"
    fi
    
    # FFmpeg
    if command -v ffmpeg &> /dev/null; then
        echo -e "${GREEN}✓ FFmpeg installé${NC}"
    else
        echo -e "${YELLOW}⚠ FFmpeg non installé - Installation recommandée${NC}"
        echo "   sudo apt-get install ffmpeg"
    fi
}

# Configuration de l'environnement Python
setup_python_env() {
    echo -e "\n${YELLOW}🐍 Configuration de l'environnement Python...${NC}"
    
    cd backend
    
    # Créer le virtualenv
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        echo -e "${GREEN}✓ Virtualenv créé${NC}"
    fi
    
    # Activer et installer les dépendances
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    
    echo -e "${GREEN}✓ Dépendances Python installées${NC}"
    
    cd ..
}

# Configuration de l'environnement Node.js
setup_node_env() {
    echo -e "\n${YELLOW}📦 Configuration de l'environnement Node.js...${NC}"
    
    cd frontend
    
    # Installer les dépendances
    if [ -f "package.json" ]; then
        npm install
        echo -e "${GREEN}✓ Dépendances Node.js installées${NC}"
    else
        echo -e "${YELLOW}⚠ package.json non trouvé - Initialisation...${NC}"
        npm init -y
        npm install next@14 react react-dom typescript @types/react @types/node tailwindcss postcss autoprefixer
    fi
    
    cd ..
}

# Configuration des fichiers d'environnement
setup_env_files() {
    echo -e "\n${YELLOW}🔐 Configuration des fichiers d'environnement...${NC}"
    
    # Backend .env
    if [ ! -f "backend/.env" ]; then
        if [ -f "infrastructure/.env.example" ]; then
            cp infrastructure/.env.example backend/.env
            echo -e "${GREEN}✓ backend/.env créé (à configurer)${NC}"
        fi
    else
        echo -e "${GREEN}✓ backend/.env existe déjà${NC}"
    fi
    
    # Frontend .env.local
    if [ ! -f "frontend/.env.local" ]; then
        cat > frontend/.env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
EOF
        echo -e "${GREEN}✓ frontend/.env.local créé${NC}"
    fi
}

# Création des dossiers manquants
create_directories() {
    echo -e "\n${YELLOW}📁 Création des dossiers...${NC}"
    
    mkdir -p backend/api/routes
    mkdir -p backend/api/schemas
    mkdir -p backend/video
    mkdir -p backend/audio
    mkdir -p frontend/components/VideoStudio
    mkdir -p frontend/components/PodcastCreator
    mkdir -p frontend/components/ShortsGenerator
    mkdir -p frontend/pages/video-studio
    mkdir -p frontend/hooks
    mkdir -p tests
    mkdir -p media/uploads
    mkdir -p media/outputs
    mkdir -p logs
    
    # Fichiers __init__.py
    touch backend/services/__init__.py
    touch backend/video/__init__.py
    touch backend/audio/__init__.py
    touch backend/api/__init__.py
    touch backend/api/routes/__init__.py
    touch backend/api/schemas/__init__.py
    
    echo -e "${GREEN}✓ Dossiers créés${NC}"
}

# Initialisation de la base de données
init_database() {
    echo -e "\n${YELLOW}🗄️ Initialisation de la base de données...${NC}"
    
    if command -v docker &> /dev/null; then
        # Démarrer PostgreSQL avec Docker
        docker run -d \
            --name iafactory-postgres \
            -e POSTGRES_USER=iafactory \
            -e POSTGRES_PASSWORD=dev_password \
            -e POSTGRES_DB=video_studio \
            -p 5432:5432 \
            postgres:16-alpine 2>/dev/null || true
        
        echo -e "${GREEN}✓ PostgreSQL démarré (Docker)${NC}"
    else
        echo -e "${YELLOW}⚠ Docker non disponible - Configurez PostgreSQL manuellement${NC}"
    fi
}

# Instructions finales
print_instructions() {
    echo -e "\n${GREEN}=============================================${NC}"
    echo -e "${GREEN}✅ Installation terminée !${NC}"
    echo -e "${GREEN}=============================================${NC}"
    
    echo -e "\n${YELLOW}📝 Prochaines étapes :${NC}"
    echo ""
    echo "1. Configurez vos clés API dans backend/.env :"
    echo "   - ANTHROPIC_API_KEY (requis)"
    echo "   - ELEVENLABS_API_KEY (requis pour TTS)"
    echo "   - MINIMAX_API_KEY (requis pour vidéo)"
    echo ""
    echo "2. Démarrez le backend :"
    echo "   cd backend"
    echo "   source venv/bin/activate"
    echo "   uvicorn main:app --reload"
    echo ""
    echo "3. Démarrez le frontend :"
    echo "   cd frontend"
    echo "   npm run dev"
    echo ""
    echo "4. Ou utilisez Docker Compose :"
    echo "   cd infrastructure"
    echo "   docker-compose up -d"
    echo ""
    echo -e "${YELLOW}📚 Documentation :${NC}"
    echo "   - README.md : Vue d'ensemble du projet"
    echo "   - docs/ARCHITECTURE.md : Architecture technique"
    echo "   - docs/AGENTS_SPECS.md : Spécifications des agents IA"
    echo "   - CLAUDE_CODE_INSTRUCTIONS.md : Guide pour Claude Code"
    echo ""
    echo -e "${GREEN}🚀 Bon développement !${NC}"
}

# Exécution principale
main() {
    check_prerequisites
    create_directories
    setup_env_files
    setup_python_env
    # setup_node_env  # Décommenter quand package.json existe
    # init_database   # Décommenter si Docker disponible
    print_instructions
}

# Lancer le script
main "$@"
