#!/usr/bin/env bash
# ==============================================
# 🏥 IAFactory DZ/CH - Health Check Complet
# ==============================================
# Vérifie tous les endpoints de l'API
# Usage: ./health_check.sh [host] [port]
# ==============================================

set -e

# Configuration
HOST="${1:-localhost}"
PORT="${2:-8180}"
BASE_URL="http://${HOST}:${PORT}"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║     🏥 IAFactory DZ/CH - Health Check Complet                 ║"
echo "║     Target: ${BASE_URL}                              "
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Compteurs
TOTAL=0
PASSED=0
FAILED=0

# Fonction de test
check_endpoint() {
    local NAME="$1"
    local ENDPOINT="$2"
    local METHOD="${3:-GET}"
    local DATA="$4"
    
    TOTAL=$((TOTAL + 1))
    
    if [ "$METHOD" = "POST" ] && [ -n "$DATA" ]; then
        RESPONSE=$(curl -sf -X POST "${BASE_URL}${ENDPOINT}" \
            -H "Content-Type: application/json" \
            -d "$DATA" 2>&1) && STATUS=0 || STATUS=1
    else
        RESPONSE=$(curl -sf "${BASE_URL}${ENDPOINT}" 2>&1) && STATUS=0 || STATUS=1
    fi
    
    if [ $STATUS -eq 0 ]; then
        echo -e "${GREEN}✓${NC} ${NAME}"
        PASSED=$((PASSED + 1))
        return 0
    else
        echo -e "${RED}✗${NC} ${NAME} (${ENDPOINT})"
        FAILED=$((FAILED + 1))
        return 1
    fi
}

# ==============================================
# CORE HEALTH
# ==============================================
echo -e "\n${BLUE}═══ CORE SERVICES ═══${NC}"
check_endpoint "API Health" "/health"
check_endpoint "API Root" "/"
check_endpoint "API Metrics" "/metrics"

# ==============================================
# BILLING & CRM
# ==============================================
echo -e "\n${BLUE}═══ BILLING & CRM ═══${NC}"
check_endpoint "Billing V1" "/api/billing/health"
check_endpoint "Billing V2" "/api/billing/v2/health"
check_endpoint "CRM" "/api/crm/health"
check_endpoint "CRM PRO" "/api/crm-pro/health"
check_endpoint "PME Copilot" "/api/pme/health"
check_endpoint "PME V2" "/api/pme/v2/health"

# ==============================================
# BIG RAG MULTI-PAYS
# ==============================================
echo -e "\n${BLUE}═══ BIG RAG MULTI-PAYS 🌍 ═══${NC}"
check_endpoint "BIG RAG Status" "/api/rag/multi/status"
check_endpoint "BIG RAG Collections" "/api/rag/multi/collections"
check_endpoint "BIG RAG Ingest Status" "/api/rag/multi/ingest/status"

# Test de recherche (optionnel)
echo -e "${YELLOW}  Testing search...${NC}"
SEARCH_RESULT=$(curl -sf -X POST "${BASE_URL}/api/rag/multi/seed/search" \
    -H "Content-Type: application/json" \
    -d '{"query":"test fiscal", "collection":"rag_dz", "top_k":1}' 2>&1) && {
    echo -e "${GREEN}✓${NC} BIG RAG Search (DZ)"
    PASSED=$((PASSED + 1))
} || {
    echo -e "${YELLOW}⚠${NC} BIG RAG Search (collections vides?)"
}
TOTAL=$((TOTAL + 1))

# ==============================================
# VOICE AI (DZ)
# ==============================================
echo -e "\n${BLUE}═══ VOICE AI 🎙️ ═══${NC}"
check_endpoint "STT Status" "/api/voice/stt/status"
check_endpoint "TTS Status" "/api/voice/tts/status"
check_endpoint "Voice Agent Status" "/api/voice/agent/status"

# ==============================================
# NLP & OCR
# ==============================================
echo -e "\n${BLUE}═══ NLP & OCR 📄 ═══${NC}"
check_endpoint "Darija NLP Status" "/api/darija/status"
check_endpoint "OCR Status" "/api/ocr/status"

# Test Darija detection
echo -e "${YELLOW}  Testing Darija detection...${NC}"
DARIJA_RESULT=$(curl -sf -X POST "${BASE_URL}/api/darija/detect" \
    -H "Content-Type: application/json" \
    -d '{"text":"wach kayen chi haja jdida?"}' 2>&1) && {
    echo -e "${GREEN}✓${NC} Darija Detection"
    PASSED=$((PASSED + 1))
} || {
    echo -e "${RED}✗${NC} Darija Detection"
    FAILED=$((FAILED + 1))
}
TOTAL=$((TOTAL + 1))

# ==============================================
# OTHER SERVICES
# ==============================================
echo -e "\n${BLUE}═══ OTHER SERVICES ═══${NC}"
check_endpoint "Auth" "/api/auth/health" || true
check_endpoint "Knowledge Base" "/api/knowledge/health" || true
check_endpoint "Calendar" "/api/calendar/health" || true
check_endpoint "Email Agent" "/api/email-agent/health" || true
check_endpoint "Council (LLM)" "/api/council/health" || true
check_endpoint "Ithy MoA" "/api/ithy/health" || true

# ==============================================
# INFRASTRUCTURE
# ==============================================
echo -e "\n${BLUE}═══ INFRASTRUCTURE ═══${NC}"

# PostgreSQL (via backend)
echo -e "${YELLOW}  Checking PostgreSQL...${NC}"
curl -sf "${BASE_URL}/health" | grep -q "healthy" && {
    echo -e "${GREEN}✓${NC} PostgreSQL (via backend health)"
} || {
    echo -e "${YELLOW}⚠${NC} PostgreSQL (check manually)"
}

# Redis
echo -e "${YELLOW}  Checking Redis...${NC}"
docker exec iaf-dz-redis redis-cli ping 2>/dev/null | grep -q "PONG" && {
    echo -e "${GREEN}✓${NC} Redis"
} || {
    echo -e "${YELLOW}⚠${NC} Redis (container not accessible)"
}

# Qdrant
echo -e "${YELLOW}  Checking Qdrant...${NC}"
curl -sf "http://${HOST}:6332/collections" > /dev/null 2>&1 && {
    echo -e "${GREEN}✓${NC} Qdrant Vector DB"
} || {
    echo -e "${YELLOW}⚠${NC} Qdrant (port 6332)"
}

# ==============================================
# SUMMARY
# ==============================================
echo -e "\n${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "📊 ${BLUE}RÉSUMÉ${NC}"
echo -e "   Total tests:  ${TOTAL}"
echo -e "   ${GREEN}Passés:      ${PASSED}${NC}"
echo -e "   ${RED}Échoués:     ${FAILED}${NC}"

PERCENT=$((PASSED * 100 / TOTAL))

if [ $FAILED -eq 0 ]; then
    echo -e "\n${GREEN}✅ TOUS LES SERVICES SONT OPÉRATIONNELS (${PERCENT}%)${NC}"
    exit 0
elif [ $PERCENT -ge 80 ]; then
    echo -e "\n${YELLOW}⚠️ SYSTÈME PARTIELLEMENT OPÉRATIONNEL (${PERCENT}%)${NC}"
    exit 0
else
    echo -e "\n${RED}❌ SYSTÈME EN ERREUR (${PERCENT}%)${NC}"
    exit 1
fi
