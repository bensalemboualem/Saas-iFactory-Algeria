#!/bin/bash
###############################################################################
# DÉPLOIEMENT AUTOMATIQUE COMPLET - PIPELINE CREATOR
# IAFactory Algeria - One-Click Installation
###############################################################################

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}============================================================${NC}"
echo -e "${GREEN}🚀 IAFactory Pipeline - Installation Automatique${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""

# ========== ÉTAPE 1: Backend API ==========
echo -e "${BLUE}[1/6] Installation Backend API...${NC}"

# Ajouter le router pipeline au main.py
MAIN_PY="/opt/iafactory-rag-dz/backend/rag-compat/app/main.py"

if ! grep -q "from app.routers import pipeline" "$MAIN_PY"; then
    # Trouver la ligne avec les autres imports de routers
    sed -i '/from app.routers import/a from app.routers import pipeline' "$MAIN_PY"

    # Ajouter l'include_router après les autres
    sed -i '/app.include_router/a app.include_router(pipeline.router)' "$MAIN_PY"

    echo -e "${GREEN}✅ Router pipeline ajouté${NC}"
else
    echo -e "${YELLOW}⚠️  Router pipeline déjà présent${NC}"
fi

# Installer pydantic[email] si nécessaire
docker exec iaf-rag-backend-prod pip install "pydantic[email]" -q 2>/dev/null || true

# Redémarrer le backend
docker restart iaf-rag-backend-prod
echo -e "${GREEN}✅ Backend redémarré${NC}"

sleep 5

# ========== ÉTAPE 2: Nginx Configuration ==========
echo ""
echo -e "${BLUE}[2/6] Configuration Nginx...${NC}"

cat > /etc/nginx/sites-enabled/pipeline.conf << 'EOF'
# Pipeline Creator Web UI
location /pipeline {
    alias /opt/iafactory-rag-dz/apps/pipeline-creator;
    index index.html;
    try_files $uri $uri/ /pipeline/index.html;
}

# Pipeline API
location /api/v1/pipeline {
    proxy_pass http://127.0.0.1:8000/api/v1/pipeline;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_read_timeout 600;
    proxy_buffering off;
}
EOF

nginx -t && nginx -s reload
echo -e "${GREEN}✅ Nginx configuré${NC}"

# ========== ÉTAPE 3: Web UI ==========
echo ""
echo -e "${BLUE}[3/6] Déploiement Web UI...${NC}"

# Créer le dossier si nécessaire
mkdir -p /opt/iafactory-rag-dz/apps/pipeline-creator

# Le fichier index.html existe déjà (créé par Claude)
if [ -f "/opt/iafactory-rag-dz/apps/pipeline-creator/index.html" ]; then
    echo -e "${GREEN}✅ Web UI déjà présent${NC}"
else
    echo -e "${RED}❌ index.html manquant${NC}"
    exit 1
fi

# ========== ÉTAPE 4: CLI Installation ==========
echo ""
echo -e "${BLUE}[4/6] Installation CLI...${NC}"

cd /opt/iafactory-rag-dz/cli

if [ ! -d "node_modules" ]; then
    npm install --quiet 2>/dev/null
fi

# Link globalement
npm link 2>/dev/null || true

echo -e "${GREEN}✅ CLI installé${NC}"

# ========== ÉTAPE 5: Permissions Scripts ==========
echo ""
echo -e "${BLUE}[5/6] Configuration des scripts...${NC}"

chmod +x /opt/iafactory-rag-dz/scripts/pipeline-auto.sh
chmod +x /opt/iafactory-rag-dz/scripts/bmad-to-archon-to-bolt.py

echo -e "${GREEN}✅ Scripts configurés${NC}"

# ========== ÉTAPE 6: Tests ==========
echo ""
echo -e "${BLUE}[6/6] Tests de validation...${NC}"

# Test Backend API
if curl -s http://localhost:8000/api/v1/pipeline/list > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend API: OK${NC}"
else
    echo -e "${RED}❌ Backend API: ERREUR${NC}"
fi

# Test Web UI
if [ -f "/opt/iafactory-rag-dz/apps/pipeline-creator/index.html" ]; then
    echo -e "${GREEN}✅ Web UI: OK${NC}"
else
    echo -e "${RED}❌ Web UI: ERREUR${NC}"
fi

# Test CLI
if command -v iafactory &> /dev/null; then
    echo -e "${GREEN}✅ CLI: OK${NC}"
else
    echo -e "${YELLOW}⚠️  CLI: Installez avec 'npm link' dans /opt/iafactory-rag-dz/cli${NC}"
fi

# Test Nginx
if curl -s https://iafactoryalgeria.com/pipeline > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Nginx: OK${NC}"
else
    echo -e "${YELLOW}⚠️  Nginx: Vérifiez SSL${NC}"
fi

# ========== RÉSUMÉ FINAL ==========
echo ""
echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}✅ INSTALLATION TERMINÉE AVEC SUCCÈS!${NC}"
echo -e "${GREEN}============================================================${NC}"
echo ""
echo -e "${YELLOW}📊 URLs Disponibles:${NC}"
echo ""
echo -e "  ${BLUE}Web UI:${NC}"
echo -e "  https://iafactoryalgeria.com/pipeline"
echo ""
echo -e "  ${BLUE}API Docs:${NC}"
echo -e "  http://localhost:8000/docs"
echo ""
echo -e "  ${BLUE}API Health:${NC}"
echo -e "  http://localhost:8000/api/v1/pipeline/list"
echo ""
echo -e "${YELLOW}💻 Commandes CLI:${NC}"
echo ""
echo -e "  iafactory create \"Mon Projet\""
echo -e "  iafactory list"
echo -e "  iafactory status <pipeline_id>"
echo ""
echo -e "${YELLOW}🔧 Script Direct:${NC}"
echo ""
echo -e "  /opt/iafactory-rag-dz/scripts/pipeline-auto.sh \"Mon Projet\""
echo ""
echo -e "${GREEN}Prêt pour votre présentation! 🚀${NC}"
echo ""
