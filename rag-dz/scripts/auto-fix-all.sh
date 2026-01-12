#!/bin/bash

echo "=========================================="
echo "🔧 AUTO-FIX COMPLET IAFACTORY"
echo "=========================================="

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

VPS_HOST="root@46.224.3.125"
VPS_PATH="/opt/iafactory-rag-dz"

echo ""
echo "1️⃣ Vérification Backend..."
BACKEND_STATUS=$(ssh $VPS_HOST "curl -s http://localhost:8180/health | grep -o 'healthy'")
if [ "$BACKEND_STATUS" = "healthy" ]; then
    echo -e "${GREEN}✅ Backend: OK${NC}"
else
    echo -e "${RED}❌ Backend: ERREUR${NC}"
    echo "   Redémarrage du backend..."
    ssh $VPS_HOST "docker restart iaf-backend-prod"
    sleep 10
fi

echo ""
echo "2️⃣ Vérification API Credentials..."
PROVIDERS_COUNT=$(ssh $VPS_HOST "curl -s http://localhost:8180/api/credentials/ | grep -o '\"has_key\": true' | wc -l")
echo "   Providers configurés: $PROVIDERS_COUNT/7"
if [ "$PROVIDERS_COUNT" -ge "7" ]; then
    echo -e "${GREEN}✅ API Credentials: OK${NC}"
else
    echo -e "${YELLOW}⚠️  Seulement $PROVIDERS_COUNT providers actifs${NC}"
fi

echo ""
echo "3️⃣ Nettoyage cache Nginx..."
ssh $VPS_HOST "nginx -s reload"
echo -e "${GREEN}✅ Nginx rechargé${NC}"

echo ""
echo "4️⃣ Ajout timestamps pour forcer refresh..."
TIMESTAMP=$(date +%s)
ssh $VPS_HOST "cd $VPS_PATH/apps/landing && sed -i 's/\?v=[0-9]*/\?v=$TIMESTAMP/g' index.html"
echo -e "${GREEN}✅ Timestamps ajoutés: v=$TIMESTAMP${NC}"

echo ""
echo "5️⃣ Vérification permissions fichiers..."
ssh $VPS_HOST "chown -R www-data:www-data $VPS_PATH/apps/"
ssh $VPS_HOST "chmod -R 755 $VPS_PATH/apps/"
echo -e "${GREEN}✅ Permissions corrigées${NC}"

echo ""
echo "6️⃣ Test endpoints publics..."
echo "   • /api/health"
HEALTH=$(ssh $VPS_HOST "curl -s http://localhost:8180/health | grep -o 'healthy'")
[ "$HEALTH" = "healthy" ] && echo -e "     ${GREEN}✅${NC}" || echo -e "     ${RED}❌${NC}"

echo "   • /api/credentials/"
CREDS=$(ssh $VPS_HOST "curl -s http://localhost:8180/api/credentials/ | grep -o '\"has_key\": true' | head -1")
[ ! -z "$CREDS" ] && echo -e "     ${GREEN}✅${NC}" || echo -e "     ${RED}❌${NC}"

echo "   • /api/agent-chat/sessions"
SESSION=$(ssh $VPS_HOST "curl -s -X POST http://localhost:8180/api/agent-chat/sessions -H 'Content-Type: application/json' -d '{\"title\":\"test\"}' | grep -o 'session_id'")
[ "$SESSION" = "session_id" ] && echo -e "     ${GREEN}✅${NC}" || echo -e "     ${RED}❌${NC}"

echo ""
echo "7️⃣ Génération rapport de vérification..."
ssh $VPS_HOST "cat > /tmp/iafactory-status.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>IAFactory - État du Système</title>
    <meta http-equiv='refresh' content='5'>
    <style>
        body { font-family: monospace; background: #0a0a0a; color: #0f0; padding: 20px; }
        .ok { color: #0f0; }
        .error { color: #f00; }
        .warning { color: #ff0; }
        h1 { color: #0ff; }
        pre { background: #1a1a1a; padding: 10px; border: 1px solid #0f0; }
    </style>
</head>
<body>
    <h1>🔧 IAFactory - État du Système</h1>
    <p>Dernière mise à jour: $(date)</p>
    <h2>Backend:</h2>
    <pre>$(curl -s http://localhost:8180/health | python3 -m json.tool 2>/dev/null)</pre>
    <h2>API Credentials:</h2>
    <pre>$(curl -s http://localhost:8180/api/credentials/ | python3 -m json.tool 2>/dev/null | grep -E '(provider|has_key)')</pre>
    <h2>Docker Containers:</h2>
    <pre>$(docker ps --format 'table {{.Names}}\t{{.Status}}' | grep iaf)</pre>
</body>
</html>
EOF
"

ssh $VPS_HOST "cp /tmp/iafactory-status.html $VPS_PATH/apps/landing/status.html"
echo -e "${GREEN}✅ Rapport disponible: https://www.iafactoryalgeria.com/landing/status.html${NC}"

echo ""
echo "=========================================="
echo -e "${GREEN}✅ AUTO-FIX TERMINÉ!${NC}"
echo "=========================================="
echo ""
echo "📋 URLS À TESTER:"
echo "   • Landing: https://www.iafactoryalgeria.com/landing/"
echo "   • Status:  https://www.iafactoryalgeria.com/landing/status.html"
echo "   • Test JS: https://www.iafactoryalgeria.com/landing/test-js.html"
echo "   • API:     https://www.iafactoryalgeria.com/api/credentials/"
echo ""
echo "🔄 Pour vider le cache: Ctrl+Shift+Delete ou Ctrl+F5"
echo ""
