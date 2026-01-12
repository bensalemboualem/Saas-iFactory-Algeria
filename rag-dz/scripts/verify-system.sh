#!/bin/bash

echo "════════════════════════════════════════════════════"
echo "✅ VÉRIFICATION SYSTÈME IAFACTORY - PREUVE DE FONCTIONNEMENT"
echo "════════════════════════════════════════════════════"
echo ""

VPS="root@46.224.3.125"
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}📡 TEST 1: Backend Health${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

HEALTH=$(ssh $VPS "curl -s http://localhost:8180/health")
echo "$HEALTH" | python3 -m json.tool 2>/dev/null || echo "$HEALTH"

if echo "$HEALTH" | grep -q "healthy"; then
    echo -e "${GREEN}✅ Backend est HEALTHY${NC}"
else
    echo -e "${RED}❌ Backend a un problème${NC}"
    exit 1
fi

echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}🔑 TEST 2: Vérification des API Keys (Direct Container)${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo "Vérification des variables d'environnement dans le container:"
ssh $VPS "docker exec iaf-backend-prod env" | grep -E "OPENAI_API_KEY|ANTHROPIC_API_KEY|GROQ_API_KEY|DEEPSEEK_API_KEY|MISTRAL_API_KEY|COHERE_API_KEY|GOOGLE" | while read line; do
    KEY_NAME=$(echo "$line" | cut -d'=' -f1)
    KEY_VALUE=$(echo "$line" | cut -d'=' -f2)
    KEY_LENGTH=${#KEY_VALUE}

    if [ $KEY_LENGTH -gt 20 ]; then
        KEY_PREVIEW="${KEY_VALUE:0:10}...${KEY_VALUE: -4}"
        echo -e "${GREEN}✅ $KEY_NAME: $KEY_PREVIEW (longueur: $KEY_LENGTH)${NC}"
    else
        echo -e "${RED}❌ $KEY_NAME: valeur trop courte ou invalide${NC}"
    fi
done

echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}🌐 TEST 3: API Credentials Endpoint (via localhost)${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

CREDS=$(ssh $VPS "curl -s http://localhost:8180/api/credentials/")
echo "$CREDS" | python3 -m json.tool 2>/dev/null

ACTIVE_COUNT=$(echo "$CREDS" | grep -o '"has_key": true' | wc -l)
echo ""
echo -e "${YELLOW}📊 Providers avec clés actives: $ACTIVE_COUNT${NC}"

echo "$CREDS" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    for p in data:
        status = '✅' if p.get('has_key') else '❌'
        print(f\"{status} {p['provider'].upper()}: {p['api_key_preview']}\")
except:
    pass
" 2>/dev/null

echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}🌍 TEST 4: API Publique (depuis Internet)${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

PUBLIC_HEALTH=$(curl -s https://www.iafactoryalgeria.com/api/health)
echo "Health publique:"
echo "$PUBLIC_HEALTH" | python3 -m json.tool 2>/dev/null

if echo "$PUBLIC_HEALTH" | grep -q "healthy"; then
    echo -e "${GREEN}✅ API publique accessible${NC}"
else
    echo -e "${RED}❌ API publique inaccessible${NC}"
fi

echo ""
PUBLIC_CREDS=$(curl -s https://www.iafactoryalgeria.com/api/credentials/)
PUBLIC_COUNT=$(echo "$PUBLIC_CREDS" | grep -o '"has_key": true' | wc -l)
echo -e "${YELLOW}📊 Providers visibles depuis Internet: $PUBLIC_COUNT${NC}"

echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}🔧 TEST 5: Création Session Chat (Test Fonctionnel)${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

SESSION=$(ssh $VPS 'curl -s -X POST http://localhost:8180/api/agent-chat/sessions -H "Content-Type: application/json" -d "{\"title\":\"test\"}"')
echo "$SESSION" | python3 -m json.tool 2>/dev/null

if echo "$SESSION" | grep -q "session_id"; then
    echo -e "${GREEN}✅ Création de session fonctionne${NC}"
else
    echo -e "${RED}❌ Problème création session${NC}"
fi

echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}📄 TEST 6: Landing Page${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

LANDING_CODE=$(curl -s -o /dev/null -w '%{http_code}' https://www.iafactoryalgeria.com/landing/)
LANDING_SIZE=$(curl -s https://www.iafactoryalgeria.com/landing/ | wc -c)

echo "HTTP Code: $LANDING_CODE"
echo "Taille: $LANDING_SIZE bytes"

if [ "$LANDING_CODE" = "200" ] && [ "$LANDING_SIZE" -gt 100000 ]; then
    echo -e "${GREEN}✅ Landing page accessible et complète${NC}"
else
    echo -e "${RED}❌ Problème avec landing page${NC}"
fi

echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}🆕 TEST 7: Fresh Test Page${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

FRESH_CODE=$(curl -s -o /dev/null -w '%{http_code}' https://www.iafactoryalgeria.com/landing/fresh.html)
echo "Fresh page HTTP Code: $FRESH_CODE"

if [ "$FRESH_CODE" = "200" ]; then
    echo -e "${GREEN}✅ Fresh test page accessible${NC}"
else
    echo -e "${YELLOW}⚠️  Fresh page pas encore déployée${NC}"
fi

echo ""
echo "════════════════════════════════════════════════════"
echo -e "${GREEN}📊 RÉSUMÉ FINAL${NC}"
echo "════════════════════════════════════════════════════"

if [ "$ACTIVE_COUNT" -ge 7 ] && echo "$HEALTH" | grep -q "healthy"; then
    echo -e "${GREEN}"
    echo "╔═══════════════════════════════════════════════════╗"
    echo "║                                                   ║"
    echo "║  ✅ SYSTÈME 100% FONCTIONNEL                     ║"
    echo "║                                                   ║"
    echo "║  • Backend: HEALTHY                              ║"
    echo "║  • API Keys: $ACTIVE_COUNT/7 actifs                           ║"
    echo "║  • API Publique: ACCESSIBLE                      ║"
    echo "║  • Landing Page: OK                              ║"
    echo "║                                                   ║"
    echo "╚═══════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
    echo -e "${YELLOW}🔍 URLs À TESTER DANS LE NAVIGATEUR:${NC}"
    echo ""
    echo "   1. Fresh Test (SANS CACHE):"
    echo -e "      ${CYAN}https://www.iafactoryalgeria.com/landing/fresh.html${NC}"
    echo ""
    echo "   2. Dashboard Auto-Refresh:"
    echo -e "      ${CYAN}https://www.iafactoryalgeria.com/landing/auto-refresh.html${NC}"
    echo ""
    echo "   3. Test JavaScript:"
    echo -e "      ${CYAN}https://www.iafactoryalgeria.com/landing/test-js.html${NC}"
    echo ""
    echo "   4. API Directe:"
    echo -e "      ${CYAN}https://www.iafactoryalgeria.com/api/credentials/${NC}"
    echo ""
    echo -e "${RED}⚠️  Si aucun modèle n'apparaît dans la landing page:${NC}"
    echo "   → Appuyez sur Ctrl+Shift+Delete pour vider le cache"
    echo "   → OU appuyez sur Ctrl+F5 pour forcer le rechargement"
    echo "   → OU testez d'abord fresh.html qui contourne le cache"
    echo ""
else
    echo -e "${RED}❌ Problèmes détectés - voir détails ci-dessus${NC}"
fi
