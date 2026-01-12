#!/bin/bash
###############################################################################
# PIPELINE AUTOMATISÉ: BMAD → ARCHON → BOLT
# IAFactory Algeria - One-Click Project Creation
###############################################################################

set -e  # Exit on error

PROJECT_NAME="$1"

if [ -z "$PROJECT_NAME" ]; then
    echo "❌ Usage: ./pipeline-auto.sh \"Mon Projet\""
    exit 1
fi

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}============================================================${NC}"
echo -e "${GREEN}🚀 PIPELINE AUTOMATISÉ: BMAD → ARCHON → BOLT${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""
echo -e "📦 Projet: ${YELLOW}$PROJECT_NAME${NC}"
echo ""

# Slugify project name
PROJECT_SLUG=$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
PROJECT_DIR="/opt/iafactory-rag-dz/projects/$PROJECT_SLUG"

echo -e "📁 Dossier: ${PROJECT_DIR}"
echo ""

# Vérifier que les services sont démarrés
echo -e "${BLUE}[1/5] Vérification des services...${NC}"

# Backend RAG
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${RED}❌ Backend RAG non accessible${NC}"
    echo "   Démarrer avec: docker-compose up -d iaf-rag-backend-prod"
    exit 1
fi
echo -e "${GREEN}✅ Backend RAG OK${NC}"

# ARCHON (peut ne pas avoir de endpoint /health, vérifier le port)
if ! nc -z localhost 3737 2>/dev/null; then
    echo -e "${RED}❌ ARCHON non accessible${NC}"
    echo "   Démarrer avec: cd /opt/iafactory-rag-dz/frontend/archon-ui && npm run dev"
    exit 1
fi
echo -e "${GREEN}✅ ARCHON OK${NC}"

# BOLT
if ! nc -z localhost 5173 2>/dev/null; then
    echo -e "${RED}❌ BOLT non accessible${NC}"
    echo "   Démarrer avec: cd /opt/iafactory-rag-dz/bolt-diy && pnpm run dev"
    exit 1
fi
echo -e "${GREEN}✅ BOLT OK${NC}"

echo ""

# Créer le dossier projet
echo -e "${BLUE}[2/5] Création du projet BMAD...${NC}"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Installer BMAD
echo "📥 Installation BMAD..."
npx bmad-method@alpha install --modules bmm --skip-prompts

echo -e "${GREEN}✅ BMAD installé${NC}"
echo ""

# Instructions pour l'utilisateur
echo -e "${YELLOW}============================================================${NC}"
echo -e "${YELLOW}⚠️  ÉTAPE INTERACTIVE REQUISE${NC}"
echo -e "${YELLOW}============================================================${NC}"
echo ""
echo "Vous devez maintenant exécuter les workflows BMAD dans votre IDE:"
echo ""
echo -e "${GREEN}1. Ouvrir le projet:${NC}"
echo "   cd $PROJECT_DIR"
echo ""
echo -e "${GREEN}2. Charger l'agent Mary (Analyst) dans votre IDE${NC}"
echo "   Fichier: $PROJECT_DIR/.bmad/src/modules/bmm/agents/analyst.agent.yaml"
echo ""
echo -e "${GREEN}3. Exécuter les workflows:${NC}"
echo "   *workflow-init              # Initialisation"
echo "   *brainstorm-project         # Brainstorming"
echo "   /bmad:bmm:workflows:prd     # PRD"
echo "   /bmad:bmm:workflows:architecture   # Architecture"
echo "   /bmad:bmm:workflows:create-stories # User Stories"
echo ""
echo -e "${YELLOW}============================================================${NC}"
echo ""

read -p "✋ Appuyez sur ENTER quand les workflows BMAD sont terminés..."

echo ""
echo -e "${BLUE}[3/5] Collecte des outputs BMAD...${NC}"

# Trouver les documents BMAD
BMAD_DOCS="$PROJECT_DIR/.bmad/docs"
PRD_FILE=$(find "$BMAD_DOCS" -name "*prd*.md" -type f | head -1)
ARCH_FILE=$(find "$BMAD_DOCS" -name "*architecture*.md" -type f | head -1)
STORY_FILES=$(find "$BMAD_DOCS" -name "story-*.md" -type f)

if [ -z "$PRD_FILE" ]; then
    echo -e "${RED}❌ PRD non trouvé${NC}"
    exit 1
fi
echo -e "${GREEN}✅ PRD: $PRD_FILE${NC}"

if [ -z "$ARCH_FILE" ]; then
    echo -e "${RED}❌ Architecture non trouvée${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Architecture: $ARCH_FILE${NC}"

STORY_COUNT=$(echo "$STORY_FILES" | wc -l)
echo -e "${GREEN}✅ Stories: $STORY_COUNT${NC}"

echo ""

# Créer la Knowledge Base ARCHON
echo -e "${BLUE}[4/5] Création de la Knowledge Base ARCHON...${NC}"

KB_NAME="$PROJECT_NAME - Knowledge Base"
KB_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/knowledge \
    -H "Content-Type: application/json" \
    -d "{
        \"name\": \"$KB_NAME\",
        \"description\": \"KB générée depuis BMAD pour $PROJECT_NAME\",
        \"type\": \"project_specs\"
    }")

KB_ID=$(echo "$KB_RESPONSE" | jq -r '.id')

if [ -z "$KB_ID" ] || [ "$KB_ID" == "null" ]; then
    echo -e "${RED}❌ Échec création KB${NC}"
    echo "$KB_RESPONSE"
    exit 1
fi

echo -e "${GREEN}✅ Knowledge Base créée: $KB_ID${NC}"

# Uploader les documents
echo "📤 Upload des documents..."

# PRD
curl -s -X POST "http://localhost:8000/api/v1/knowledge/$KB_ID/documents" \
    -H "Content-Type: application/json" \
    -d "{
        \"name\": \"Product Requirements Document\",
        \"type\": \"prd\",
        \"content\": $(cat "$PRD_FILE" | jq -Rs .),
        \"metadata\": {\"phase\": \"planning\"}
    }" > /dev/null
echo -e "${GREEN}  ✅ PRD uploaded${NC}"

# Architecture
curl -s -X POST "http://localhost:8000/api/v1/knowledge/$KB_ID/documents" \
    -H "Content-Type: application/json" \
    -d "{
        \"name\": \"Architecture Document\",
        \"type\": \"architecture\",
        \"content\": $(cat "$ARCH_FILE" | jq -Rs .),
        \"metadata\": {\"phase\": \"design\"}
    }" > /dev/null
echo -e "${GREEN}  ✅ Architecture uploaded${NC}"

# Stories
STORY_NUM=1
for STORY_FILE in $STORY_FILES; do
    curl -s -X POST "http://localhost:8000/api/v1/knowledge/$KB_ID/documents" \
        -H "Content-Type: application/json" \
        -d "{
            \"name\": \"User Story $STORY_NUM\",
            \"type\": \"user_story\",
            \"content\": $(cat "$STORY_FILE" | jq -Rs .),
            \"metadata\": {\"phase\": \"implementation\", \"story_number\": $STORY_NUM}
        }" > /dev/null
    echo -e "${GREEN}  ✅ Story $STORY_NUM uploaded${NC}"
    STORY_NUM=$((STORY_NUM + 1))
done

# Indexer
echo "🔄 Indexation..."
curl -s -X POST "http://localhost:8000/api/v1/knowledge/$KB_ID/index" > /dev/null
echo -e "${GREEN}✅ Indexation terminée${NC}"

echo ""

# Lancer BOLT
echo -e "${BLUE}[5/5] Lancement de BOLT...${NC}"

BOLT_RESPONSE=$(curl -s -X POST http://localhost:5173/api/projects \
    -H "Content-Type: application/json" \
    -d "{
        \"name\": \"$PROJECT_NAME\",
        \"description\": \"Projet généré depuis BMAD\",
        \"knowledge_base_id\": \"$KB_ID\",
        \"template\": \"auto\"
    }")

BOLT_PROJECT_ID=$(echo "$BOLT_RESPONSE" | jq -r '.id')

if [ -z "$BOLT_PROJECT_ID" ] || [ "$BOLT_PROJECT_ID" == "null" ]; then
    echo -e "${RED}❌ Échec création projet BOLT${NC}"
    echo "$BOLT_RESPONSE"
    exit 1
fi

echo -e "${GREEN}✅ Projet BOLT créé: $BOLT_PROJECT_ID${NC}"

# Lancer la génération
echo "⚡ Génération du code..."
curl -s -X POST "http://localhost:5173/api/projects/$BOLT_PROJECT_ID/generate" \
    -H "Content-Type: application/json" \
    -d "{
        \"mode\": \"auto\",
        \"use_rag\": true,
        \"knowledge_base_id\": \"$KB_ID\"
    }" > /dev/null

echo -e "${GREEN}✅ Génération terminée!${NC}"

echo ""
echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}✅ PIPELINE TERMINÉ AVEC SUCCÈS!${NC}"
echo -e "${GREEN}============================================================${NC}"
echo ""
echo -e "${BLUE}📊 Résumé:${NC}"
echo "   1. BMAD: Specs créées"
echo "      - PRD: ✅"
echo "      - Architecture: ✅"
echo "      - Stories: $STORY_COUNT"
echo ""
echo "   2. ARCHON: Knowledge Base créée"
echo "      - KB ID: $KB_ID"
echo "      - URL: http://localhost:3737/knowledge/$KB_ID"
echo ""
echo "   3. BOLT: Projet créé et code généré"
echo "      - Project ID: $BOLT_PROJECT_ID"
echo "      - URL: http://localhost:5173/projects/$BOLT_PROJECT_ID"
echo ""
echo -e "${YELLOW}🎯 Prochaines étapes:${NC}"
echo "   1. Ouvrir BOLT: http://localhost:5173/projects/$BOLT_PROJECT_ID"
echo "   2. Vérifier le code généré"
echo "   3. Tester l'application"
echo "   4. Déployer!"
echo ""

# Sauvegarder le résumé
cat > "$PROJECT_DIR/pipeline-summary.json" <<EOF
{
  "project_name": "$PROJECT_NAME",
  "project_slug": "$PROJECT_SLUG",
  "project_dir": "$PROJECT_DIR",
  "bmad": {
    "prd_file": "$PRD_FILE",
    "architecture_file": "$ARCH_FILE",
    "stories_count": $STORY_COUNT
  },
  "archon": {
    "kb_id": "$KB_ID",
    "url": "http://localhost:3737/knowledge/$KB_ID"
  },
  "bolt": {
    "project_id": "$BOLT_PROJECT_ID",
    "url": "http://localhost:5173/projects/$BOLT_PROJECT_ID"
  },
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

echo -e "💾 Résumé sauvegardé: ${PROJECT_DIR}/pipeline-summary.json"
echo ""
