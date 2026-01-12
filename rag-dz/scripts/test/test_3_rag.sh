#!/usr/bin/env bash
# ==============================================
# Test Rapide des 3 RAG - iaFactory Algeria
# ==============================================

set -e

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configuration
API_URL="${1:-http://localhost:8180}"
TIMEOUT=10

echo -e "${CYAN}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║     🧪 Test des 3 RAG - iaFactory Algeria                     ║"
echo "║     API: ${API_URL}                    "
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Fonction de test
test_rag() {
    local NAME="$1"
    local EMOJI="$2"
    local COUNTRY="$3"
    local QUERY="$4"

    echo -e "\n${BLUE}═══ ${EMOJI} ${NAME} ═══${NC}"
    echo -e "${YELLOW}Question:${NC} ${QUERY}"
    echo -e "${YELLOW}Pays/RAG:${NC} ${COUNTRY}"
    echo ""

    START_TIME=$(date +%s%3N)

    RESPONSE=$(curl -s -X POST "${API_URL}/api/rag/multi/query" \
        -H "Content-Type: application/json" \
        -d "{
            \"query\": \"${QUERY}\",
            \"country\": \"${COUNTRY}\",
            \"top_k\": 5,
            \"threshold\": 0.3
        }" \
        --max-time ${TIMEOUT} 2>&1)

    END_TIME=$(date +%s%3N)
    DURATION=$((END_TIME - START_TIME))

    # Vérifier succès
    if echo "$RESPONSE" | grep -q '"answer"'; then
        ANSWER=$(echo "$RESPONSE" | grep -o '"answer":"[^"]*"' | head -1 | sed 's/"answer":"//;s/"$//')

        # Limiter à 200 caractères
        if [ ${#ANSWER} -gt 200 ]; then
            ANSWER="${ANSWER:0:200}..."
        fi

        echo -e "${GREEN}✓ Succès${NC} (${DURATION}ms)"
        echo -e "${CYAN}Réponse:${NC} ${ANSWER}"

        # Extraire infos supplémentaires
        DETECTED_COUNTRY=$(echo "$RESPONSE" | grep -o '"country_detected":"[^"]*"' | head -1 | sed 's/"country_detected":"//;s/"$//')
        TOTAL_RESULTS=$(echo "$RESPONSE" | grep -o '"total":[0-9]*' | head -1 | sed 's/"total"://')

        if [ -n "$DETECTED_COUNTRY" ]; then
            echo -e "${CYAN}Pays détecté:${NC} ${DETECTED_COUNTRY}"
        fi

        if [ -n "$TOTAL_RESULTS" ]; then
            echo -e "${CYAN}Sources trouvées:${NC} ${TOTAL_RESULTS}"
        fi

        return 0
    else
        echo -e "${RED}✗ Échec${NC}"
        echo -e "${RED}Erreur:${NC} $(echo "$RESPONSE" | head -c 200)"
        return 1
    fi
}

# ==============================================
# TESTS
# ==============================================

TOTAL=0
PASSED=0
FAILED=0

# Test 1: RAG Business DZ
TOTAL=$((TOTAL + 1))
if test_rag "RAG Business DZ" "💼" "DZ" "Quel est le taux de TVA en Algérie?"; then
    PASSED=$((PASSED + 1))
else
    FAILED=$((FAILED + 1))
fi

sleep 1

# Test 2: RAG Business DZ (juridique)
TOTAL=$((TOTAL + 1))
if test_rag "RAG Business DZ" "💼" "DZ" "Comment créer une SARL en Algérie?"; then
    PASSED=$((PASSED + 1))
else
    FAILED=$((FAILED + 1))
fi

sleep 1

# Test 3: RAG École
TOTAL=$((TOTAL + 1))
if test_rag "RAG École" "🎓" "CH" "Comment gérer les absences des étudiants?"; then
    PASSED=$((PASSED + 1))
else
    FAILED=$((FAILED + 1))
fi

sleep 1

# Test 4: RAG École (notes)
TOTAL=$((TOTAL + 1))
if test_rag "RAG École" "🎓" "CH" "Système de notation dans les écoles?"; then
    PASSED=$((PASSED + 1))
else
    FAILED=$((FAILED + 1))
fi

sleep 1

# Test 5: RAG Islam
TOTAL=$((TOTAL + 1))
if test_rag "RAG Islam" "☪️" "GLOBAL" "Quels sont les piliers de l'Islam?"; then
    PASSED=$((PASSED + 1))
else
    FAILED=$((FAILED + 1))
fi

sleep 1

# Test 6: RAG Islam (arabe)
TOTAL=$((TOTAL + 1))
if test_rag "RAG Islam" "☪️" "GLOBAL" "ما هي أركان الإسلام؟"; then
    PASSED=$((PASSED + 1))
else
    FAILED=$((FAILED + 1))
fi

# ==============================================
# RÉSULTAT FINAL
# ==============================================

echo ""
echo -e "${PURPLE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║                    RÉSULTAT FINAL                              ║${NC}"
echo -e "${PURPLE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "Total tests:   ${TOTAL}"
echo -e "${GREEN}✓ Réussis:${NC}    ${PASSED}"
echo -e "${RED}✗ Échecs:${NC}     ${FAILED}"

PERCENT=$((PASSED * 100 / TOTAL))
echo -e "Taux succès:  ${PERCENT}%"

echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  🎉 TOUS LES TESTS PASSENT - PRÊT POUR LA DÉMO! 🚀           ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    exit 0
else
    echo -e "${RED}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║  ⚠️  CERTAINS TESTS ONT ÉCHOUÉ - À CORRIGER!                  ║${NC}"
    echo -e "${RED}╚═══════════════════════════════════════════════════════════════╝${NC}"
    exit 1
fi
