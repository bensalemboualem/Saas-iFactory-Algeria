#!/bin/bash
# ================================================================
# VÉRIFICATION BOLT.DIY - IAFactory Algeria
# ================================================================
set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "================================================================"
echo "⚡ VÉRIFICATION BOLT.DIY"
echo "================================================================"
echo ""

# ================================================================
# 1. LOCALISATION BOLT
# ================================================================
echo -e "${BLUE}[1/5]${NC} Recherche de Bolt.diy..."
echo ""

BOLT_DIRS=(
    "/opt/iafactory-rag-dz/bolt-diy"
    "/opt/iafactory-rag-dz/frontend/bolt-diy"
    "/opt/bolt-diy"
    "/var/www/bolt"
)

BOLT_PATH=""
for dir in "${BOLT_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✅ Trouvé: $dir${NC}"
        BOLT_PATH="$dir"
        break
    fi
done

if [ -z "$BOLT_PATH" ]; then
    echo -e "${RED}❌ Bolt.diy non trouvé${NC}"
    echo "Recherche globale..."
    find /opt -name "*bolt*" -type d 2>/dev/null | head -5
    exit 1
fi

cd "$BOLT_PATH" || exit 1
echo "📂 Working directory: $(pwd)"

# ================================================================
# 2. VÉRIFICATION DOCKER
# ================================================================
echo ""
echo -e "${BLUE}[2/5]${NC} Vérification Docker..."
echo ""

if docker ps | grep -q bolt; then
    echo -e "${GREEN}✅ Conteneur Bolt détecté:${NC}"
    docker ps | grep bolt | awk '{print "   "$1, $2, $7}'
    BOLT_CONTAINER=$(docker ps | grep bolt | awk '{print $1}' | head -1)

    echo ""
    echo "Health status:"
    docker inspect --format='{{.State.Health.Status}}' "$BOLT_CONTAINER" 2>/dev/null || echo "   No healthcheck configured"
else
    echo -e "${YELLOW}⚠️  Aucun conteneur Bolt en cours${NC}"
fi

# ================================================================
# 3. VÉRIFICATION PROCESSUS
# ================================================================
echo ""
echo -e "${BLUE}[3/5]${NC} Vérification processus npm/node..."
echo ""

if ps aux | grep -v grep | grep -q "[b]olt.*npm"; then
    echo -e "${GREEN}✅ Processus Bolt détecté:${NC}"
    ps aux | grep -v grep | grep "[b]olt" | head -3
else
    echo -e "${YELLOW}⚠️  Aucun processus npm Bolt${NC}"
fi

# ================================================================
# 4. VÉRIFICATION PORT 5173
# ================================================================
echo ""
echo -e "${BLUE}[4/5]${NC} Vérification port 5173..."
echo ""

if netstat -tlnp 2>/dev/null | grep -q ":5173 "; then
    echo -e "${GREEN}✅ Port 5173: En écoute${NC}"
    netstat -tlnp 2>/dev/null | grep ":5173 " | awk '{print "   "$4, $7}'

    echo ""
    echo "Test HTTP local:"
    if timeout 3 curl -s http://localhost:5173 > /dev/null; then
        echo -e "${GREEN}✅ Bolt répond sur http://localhost:5173${NC}"
    else
        echo -e "${RED}❌ Bolt ne répond pas${NC}"
    fi
else
    echo -e "${RED}❌ Port 5173: NON en écoute${NC}"
fi

# ================================================================
# 5. VÉRIFICATION NGINX PROXY
# ================================================================
echo ""
echo -e "${BLUE}[5/5]${NC} Vérification configuration Nginx..."
echo ""

if grep -q "location /bolt" /etc/nginx/sites-enabled/* 2>/dev/null; then
    echo -e "${GREEN}✅ Configuration Nginx /bolt/ trouvée${NC}"
    grep -A 3 "location /bolt" /etc/nginx/sites-enabled/* | head -10
else
    echo -e "${YELLOW}⚠️  Configuration Nginx /bolt/ NON trouvée${NC}"
fi

echo ""
echo "Test via Nginx:"
if timeout 3 curl -s http://localhost/bolt/ > /dev/null; then
    echo -e "${GREEN}✅ Bolt accessible via Nginx${NC}"
else
    echo -e "${RED}❌ Bolt NON accessible via Nginx${NC}"
fi

# ================================================================
# 6. VÉRIFICATION DNS & HTTPS
# ================================================================
echo ""
echo -e "${BLUE}[6/6]${NC} Vérification domaine public..."
echo ""

BOLT_DOMAIN="bolt.iafactoryalgeria.com"

echo "DNS $BOLT_DOMAIN:"
if host "$BOLT_DOMAIN" &> /dev/null; then
    IP=$(host "$BOLT_DOMAIN" | grep "has address" | awk '{print $4}')
    echo -e "${GREEN}✅ DNS configuré: $IP${NC}"
else
    echo -e "${YELLOW}⚠️  DNS non configuré${NC}"
fi

echo ""
echo "HTTPS $BOLT_DOMAIN:"
if timeout 5 curl -Is "https://$BOLT_DOMAIN" &> /dev/null; then
    STATUS=$(timeout 5 curl -Is "https://$BOLT_DOMAIN" | head -1)
    echo -e "${GREEN}✅ HTTPS accessible${NC}"
    echo "   $STATUS"
else
    echo -e "${YELLOW}⚠️  HTTPS timeout/erreur${NC}"
fi

# ================================================================
# DIAGNOSTIC FINAL
# ================================================================
echo ""
echo "================================================================"
echo -e "${BLUE}📊 DIAGNOSTIC BOLT.DIY${NC}"
echo "================================================================"
echo ""

# Compter les ✅
CHECKS=0
TOTAL=6

[ -d "$BOLT_PATH" ] && ((CHECKS++))
docker ps | grep -q bolt && ((CHECKS++))
netstat -tlnp 2>/dev/null | grep -q ":5173 " && ((CHECKS++))
timeout 3 curl -s http://localhost:5173 > /dev/null && ((CHECKS++))
grep -q "location /bolt" /etc/nginx/sites-enabled/* 2>/dev/null && ((CHECKS++))
timeout 3 curl -s http://localhost/bolt/ > /dev/null && ((CHECKS++))

SCORE=$((CHECKS * 100 / TOTAL))

echo "Score: $CHECKS/$TOTAL ($SCORE%)"
echo ""

if [ $SCORE -ge 80 ]; then
    echo -e "${GREEN}✅ Bolt.diy: OPÉRATIONNEL${NC}"
elif [ $SCORE -ge 50 ]; then
    echo -e "${YELLOW}⚠️  Bolt.diy: PARTIELLEMENT FONCTIONNEL${NC}"
    echo "   → Exécuter fix-bolt-complete.sh"
else
    echo -e "${RED}❌ Bolt.diy: NON OPÉRATIONNEL${NC}"
    echo "   → Exécuter fix-bolt-complete.sh"
fi

echo ""
echo "🔧 Actions disponibles:"
echo "  • Corriger Bolt:        bash fix-bolt-complete.sh"
echo "  • Logs Docker:          docker logs \$(docker ps | grep bolt | awk '{print \$1}')"
echo "  • Redémarrer Docker:    cd $BOLT_PATH && docker-compose restart"
echo "  • Redémarrer npm:       cd $BOLT_PATH && npm run dev"
echo ""
