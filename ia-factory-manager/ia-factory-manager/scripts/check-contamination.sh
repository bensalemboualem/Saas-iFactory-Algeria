#!/bin/bash
# ============================================================================
# IA Factory - Script de Détection de Contamination
# ============================================================================
# Usage: ./check-contamination.sh [chemin_projet]
# Si pas de chemin fourni, utilise le répertoire courant
# ============================================================================

set -e

# Couleurs pour output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PROJECT_PATH="${1:-.}"
CONTAMINATION_FOUND=0

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}   IA Factory - Détection Contamination    ${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""
echo -e "Scanning: ${YELLOW}$PROJECT_PATH${NC}"
echo ""

# ----------------------------------------------------------------------------
# Fonction: Chercher pattern et reporter
# ----------------------------------------------------------------------------
search_pattern() {
    local pattern="$1"
    local description="$2"
    local severity="$3"
    
    results=$(grep -r --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" --include="*.json" --include="*.env*" -l "$pattern" "$PROJECT_PATH" 2>/dev/null | grep -v node_modules | grep -v ".next" | grep -v "dist" | grep -v "build" || true)
    
    if [ -n "$results" ]; then
        if [ "$severity" == "ERROR" ]; then
            echo -e "${RED}❌ $severity: $description${NC}"
            CONTAMINATION_FOUND=1
        else
            echo -e "${YELLOW}⚠️  $severity: $description${NC}"
        fi
        echo "   Fichiers concernés:"
        echo "$results" | while read file; do
            echo -e "   - ${file}"
        done
        echo ""
    fi
}

# ----------------------------------------------------------------------------
# PHASE 1: Détecter le marché du projet
# ----------------------------------------------------------------------------
echo -e "${BLUE}[PHASE 1] Détection du marché...${NC}"
echo ""

MARKET="UNKNOWN"

# Check pour Algérie
if grep -rq "chargily\|iafactoryalgeria\|DZD" "$PROJECT_PATH" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.json" --include="*.env*" 2>/dev/null | grep -v node_modules > /dev/null; then
    MARKET="ALGERIA"
    echo -e "Marché détecté: ${GREEN}🇩🇿 ALGÉRIE${NC}"
fi

# Check pour Suisse
if grep -rq "stripe\|iafactory\.ch\|CHF\|suisse\|swiss" "$PROJECT_PATH" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.json" --include="*.env*" 2>/dev/null | grep -v node_modules > /dev/null; then
    if [ "$MARKET" == "ALGERIA" ]; then
        MARKET="MIXED"
        echo -e "${RED}⚠️ ATTENTION: Références aux DEUX marchés détectées!${NC}"
    else
        MARKET="SWITZERLAND"
        echo -e "Marché détecté: ${GREEN}🇨🇭 SUISSE${NC}"
    fi
fi

if [ "$MARKET" == "UNKNOWN" ]; then
    echo -e "${YELLOW}Marché: Non déterminé (pas de markers spécifiques)${NC}"
fi
echo ""

# ----------------------------------------------------------------------------
# PHASE 2: Contamination Cross-Market
# ----------------------------------------------------------------------------
echo -e "${BLUE}[PHASE 2] Vérification contamination cross-market...${NC}"
echo ""

if [ "$MARKET" == "ALGERIA" ]; then
    # Projet Algérien ne doit PAS contenir de refs Suisse
    search_pattern "stripe" "Stripe trouvé dans projet Algérien" "ERROR"
    search_pattern "CHF" "Devise CHF trouvée dans projet Algérien" "ERROR"
    search_pattern "iafactory\.ch" "Domaine Suisse trouvé dans projet Algérien" "ERROR"
    search_pattern "\.env\.suisse" "Référence à .env.suisse dans projet Algérien" "ERROR"
elif [ "$MARKET" == "SWITZERLAND" ]; then
    # Projet Suisse ne doit PAS contenir de refs Algérie
    search_pattern "chargily" "Chargily trouvé dans projet Suisse" "ERROR"
    search_pattern "DZD" "Devise DZD trouvée dans projet Suisse" "ERROR"
    search_pattern "iafactoryalgeria" "Domaine Algérien trouvé dans projet Suisse" "ERROR"
    search_pattern "\.env\.algeria" "Référence à .env.algeria dans projet Suisse" "ERROR"
    search_pattern "darija" "Référence Darija dans projet Suisse" "WARNING"
fi

# ----------------------------------------------------------------------------
# PHASE 3: Contamination entre projets satellites
# ----------------------------------------------------------------------------
echo -e "${BLUE}[PHASE 3] Vérification contamination inter-projets...${NC}"
echo ""

# Patterns spécifiques à BOLT-PLUS
search_pattern "bolt-plus\|BOLT_PLUS\|BoltPlus" "Références BOLT-PLUS" "INFO"

# Patterns spécifiques à RAG
search_pattern "rag-system\|RAG_SYSTEM\|pinecone\|qdrant\|vector.*db" "Références RAG System" "INFO"

# Patterns spécifiques à Video Studio
search_pattern "video-studio\|replicate\|cogvideo\|wan.*2\.1" "Références Video Studio" "INFO"

# ----------------------------------------------------------------------------
# PHASE 4: Fichiers .env suspects
# ----------------------------------------------------------------------------
echo -e "${BLUE}[PHASE 4] Vérification fichiers .env...${NC}"
echo ""

# Lister tous les fichiers .env
env_files=$(find "$PROJECT_PATH" -name ".env*" -type f 2>/dev/null | grep -v node_modules || true)

if [ -n "$env_files" ]; then
    echo "Fichiers .env trouvés:"
    echo "$env_files" | while read file; do
        echo -e "   - ${YELLOW}$file${NC}"
        
        # Vérifier contenu suspect
        if grep -q "CHARGILY\|chargily" "$file" 2>/dev/null && grep -q "STRIPE\|stripe" "$file" 2>/dev/null; then
            echo -e "     ${RED}⚠️ DANGER: Ce fichier contient CHARGILY ET STRIPE!${NC}"
            CONTAMINATION_FOUND=1
        fi
    done
    echo ""
else
    echo -e "${YELLOW}Aucun fichier .env trouvé${NC}"
    echo ""
fi

# ----------------------------------------------------------------------------
# PHASE 5: Vérification TypeScript/React errors patterns
# ----------------------------------------------------------------------------
echo -e "${BLUE}[PHASE 5] Patterns d'erreurs courants...${NC}"
echo ""

# Imports dupliqués ou conflictuels
search_pattern "from ['\"].*bolt.*['\"]" "Imports depuis bolt" "INFO"
search_pattern "from ['\"].*rag.*['\"]" "Imports depuis rag" "INFO"
search_pattern "from ['\"].*video.*studio.*['\"]" "Imports depuis video-studio" "INFO"

# ----------------------------------------------------------------------------
# RÉSUMÉ
# ----------------------------------------------------------------------------
echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}                 RÉSUMÉ                     ${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

if [ $CONTAMINATION_FOUND -eq 1 ]; then
    echo -e "${RED}❌ CONTAMINATION DÉTECTÉE${NC}"
    echo ""
    echo "Actions recommandées:"
    echo "  1. Identifier les fichiers listés ci-dessus"
    echo "  2. Supprimer/corriger les références incorrectes"
    echo "  3. Relancer ce script jusqu'à 0 erreurs"
    echo ""
    exit 1
else
    echo -e "${GREEN}✅ AUCUNE CONTAMINATION CRITIQUE DÉTECTÉE${NC}"
    echo ""
    echo "Le projet semble propre. Vérifiez quand même les infos ci-dessus."
    echo ""
    exit 0
fi
