#!/bin/bash
# ================================================================
# VÉRIFICATION NGINX & SSL - IAFactory Algeria
# ================================================================
set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "================================================================"
echo "🔒 VÉRIFICATION NGINX & SSL CERTIFICATES"
echo "================================================================"
echo ""

# ================================================================
# 1. NGINX STATUS
# ================================================================
echo -e "${BLUE}[1/6]${NC} Vérification Nginx..."
echo ""

if systemctl is-active --quiet nginx; then
    echo -e "${GREEN}✅ Nginx: Running${NC}"
    NGINX_VERSION=$(nginx -v 2>&1 | cut -d'/' -f2)
    echo "   Version: $NGINX_VERSION"
else
    echo -e "${RED}❌ Nginx: NOT RUNNING${NC}"
    exit 1
fi

# ================================================================
# 2. NGINX CONFIGURATION TEST
# ================================================================
echo ""
echo -e "${BLUE}[2/6]${NC} Test configuration Nginx..."
echo ""

if nginx -t 2>&1 | grep -q "successful"; then
    echo -e "${GREEN}✅ Configuration: Valid${NC}"
else
    echo -e "${RED}❌ Configuration: ERRORS${NC}"
    nginx -t
    exit 1
fi

# ================================================================
# 3. SITES ACTIVÉS
# ================================================================
echo ""
echo -e "${BLUE}[3/6]${NC} Sites activés..."
echo ""

SITES=$(ls /etc/nginx/sites-enabled/ 2>/dev/null | grep -v default || echo "aucun")
if [ "$SITES" != "aucun" ]; then
    echo -e "${GREEN}Sites configurés:${NC}"
    for site in $SITES; do
        echo "  • $site"
    done
else
    echo -e "${YELLOW}⚠️  Aucun site activé${NC}"
fi

# ================================================================
# 4. CERTIFICATS SSL
# ================================================================
echo ""
echo -e "${BLUE}[4/6]${NC} Certificats SSL (Let's Encrypt)..."
echo ""

if command -v certbot &> /dev/null; then
    echo -e "${GREEN}✅ Certbot installé${NC}"
    echo ""
    echo "📜 Certificats actifs:"
    certbot certificates 2>/dev/null || echo "   Aucun certificat trouvé"
else
    echo -e "${RED}❌ Certbot non installé${NC}"
fi

# ================================================================
# 5. VÉRIFICATION DOMAINES
# ================================================================
echo ""
echo -e "${BLUE}[5/6]${NC} Test des domaines principaux..."
echo ""

DOMAINS=(
    "www.iafactoryalgeria.com"
    "archon.iafactoryalgeria.com"
    "bolt.iafactoryalgeria.com"
    "api.iafactoryalgeria.com"
)

for domain in "${DOMAINS[@]}"; do
    echo -n "Testing $domain... "

    # Test DNS
    if host "$domain" &> /dev/null; then
        IP=$(host "$domain" | grep "has address" | head -1 | awk '{print $4}')
        echo -e "${GREEN}DNS: $IP${NC}"

        # Test HTTPS
        if timeout 5 curl -Is "https://$domain" &> /dev/null; then
            STATUS=$(timeout 5 curl -Is "https://$domain" | head -1 | cut -d' ' -f2)
            echo "   HTTPS Status: $STATUS"
        else
            echo -e "   ${YELLOW}HTTPS: Timeout/Error${NC}"
        fi
    else
        echo -e "${YELLOW}DNS: Not configured${NC}"
    fi
done

# ================================================================
# 6. PORTS EN ÉCOUTE
# ================================================================
echo ""
echo -e "${BLUE}[6/6]${NC} Ports Nginx en écoute..."
echo ""

echo "Port 80 (HTTP):"
if netstat -tlnp 2>/dev/null | grep -q ":80 "; then
    echo -e "${GREEN}✅ En écoute${NC}"
else
    echo -e "${RED}❌ NON en écoute${NC}"
fi

echo ""
echo "Port 443 (HTTPS):"
if netstat -tlnp 2>/dev/null | grep -q ":443 "; then
    echo -e "${GREEN}✅ En écoute${NC}"
else
    echo -e "${RED}❌ NON en écoute${NC}"
fi

# ================================================================
# RÉSUMÉ
# ================================================================
echo ""
echo "================================================================"
echo -e "${GREEN}✅ VÉRIFICATION NGINX/SSL TERMINÉE${NC}"
echo "================================================================"
echo ""
echo "📋 RÉSUMÉ:"
echo "  • Nginx: $(systemctl is-active nginx)"
echo "  • Configuration: $(nginx -t 2>&1 | grep -o 'successful' || echo 'avec erreurs')"
echo "  • Certbot: $(command -v certbot &> /dev/null && echo 'installé' || echo 'non installé')"
echo ""
echo "🔧 Commandes utiles:"
echo "  • Recharger Nginx:  systemctl reload nginx"
echo "  • Logs erreurs:     tail -f /var/log/nginx/error.log"
echo "  • Renouveler SSL:   certbot renew"
echo ""
