#!/bin/bash
# ================================================================
# CONFIGURATION GRAFANA PUBLIC - IAFactory Algeria
# ================================================================
# Crée un sous-domaine grafana.iafactoryalgeria.com avec SSL
# ================================================================

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "================================================================"
echo "📊 CONFIGURATION GRAFANA PUBLIC"
echo "================================================================"
echo ""

DOMAIN="grafana.iafactoryalgeria.com"
GRAFANA_PORT="3033"

echo -e "${BLUE}[1/5]${NC} Vérification que Grafana tourne..."
if docker ps | grep -q grafana; then
    echo -e "${GREEN}✅ Grafana container trouvé${NC}"
    GRAFANA_CONTAINER=$(docker ps | grep grafana | awk '{print $1}')
    echo "   Container ID: $GRAFANA_CONTAINER"
else
    echo -e "${RED}❌ Grafana ne tourne pas${NC}"
    echo "Démarrez Grafana avec: docker-compose up -d grafana"
    exit 1
fi
echo ""

echo -e "${BLUE}[2/5]${NC} Test de Grafana sur localhost:$GRAFANA_PORT..."
if timeout 5 curl -s http://localhost:$GRAFANA_PORT/api/health > /dev/null; then
    echo -e "${GREEN}✅ Grafana répond${NC}"
else
    echo -e "${YELLOW}⚠️  Grafana ne répond pas sur port $GRAFANA_PORT${NC}"
    echo "Vérifiez le port avec: docker ps | grep grafana"
fi
echo ""

echo -e "${BLUE}[3/5]${NC} Création de la configuration Nginx..."

cat > /etc/nginx/sites-available/$DOMAIN << 'NGINXEOF'
# ================================================================
# GRAFANA PUBLIC - IAFactory Algeria
# ================================================================

# HTTP → HTTPS Redirect
server {
    listen 80;
    listen [::]:80;
    server_name grafana.iafactoryalgeria.com;

    return 301 https://$host$request_uri;
}

# HTTPS Server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name grafana.iafactoryalgeria.com;

    # SSL certificates (will be added by certbot)
    # ssl_certificate /etc/letsencrypt/live/grafana.iafactoryalgeria.com/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/grafana.iafactoryalgeria.com/privkey.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Grafana proxy
    location / {
        proxy_pass http://127.0.0.1:3033;
        proxy_http_version 1.1;

        # WebSocket support (for live updates)
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;

        # Timeouts (for long-running queries)
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
        proxy_read_timeout 300;

        # Buffering
        proxy_buffering off;
    }

    # API endpoints
    location /api/ {
        proxy_pass http://127.0.0.1:3033;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Live updates
    location /api/live/ {
        proxy_pass http://127.0.0.1:3033;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }

    # Access logs
    access_log /var/log/nginx/grafana-access.log;
    error_log /var/log/nginx/grafana-error.log;
}
NGINXEOF

echo -e "${GREEN}✅ Configuration Nginx créée${NC}"
echo ""

echo -e "${BLUE}[4/5]${NC} Activation de la configuration..."

# Créer le lien symbolique
ln -sf /etc/nginx/sites-available/$DOMAIN /etc/nginx/sites-enabled/$DOMAIN

# Tester la configuration
if nginx -t 2>&1 | grep -q "successful"; then
    echo -e "${GREEN}✅ Configuration Nginx valide${NC}"
else
    echo -e "${RED}❌ Erreur dans la configuration Nginx${NC}"
    nginx -t
    exit 1
fi

# Recharger Nginx
systemctl reload nginx
echo -e "${GREEN}✅ Nginx rechargé${NC}"
echo ""

echo -e "${BLUE}[5/5]${NC} Configuration SSL avec Let's Encrypt..."
echo ""

echo -e "${YELLOW}⚠️  IMPORTANT: DNS REQUIS${NC}"
echo ""
echo "Avant de continuer, assurez-vous que le DNS est configuré:"
echo ""
echo "  Type: A"
echo "  Name: grafana"
echo "  Value: 46.224.3.125"
echo "  TTL: Auto/300"
echo ""

# Vérifier le DNS
echo "Vérification DNS..."
if host $DOMAIN &> /dev/null; then
    IP=$(host $DOMAIN | grep "has address" | awk '{print $4}')
    echo -e "${GREEN}✅ DNS configuré: $DOMAIN → $IP${NC}"

    echo ""
    echo "Configuration SSL automatique..."

    # Certbot
    if certbot --nginx -d $DOMAIN \
        --non-interactive \
        --agree-tos \
        --email admin@iafactoryalgeria.com \
        --redirect; then

        echo -e "${GREEN}✅ SSL configuré avec succès${NC}"
    else
        echo -e "${YELLOW}⚠️  SSL échoué - Configuration manuelle requise${NC}"
        echo ""
        echo "Commande manuelle:"
        echo "  certbot --nginx -d $DOMAIN"
    fi
else
    echo -e "${YELLOW}⚠️  DNS non configuré ou pas encore propagé${NC}"
    echo ""
    echo "Configuration SSL manuelle après propagation DNS:"
    echo "  certbot --nginx -d $DOMAIN --email admin@iafactoryalgeria.com"
fi

echo ""
echo "================================================================"
echo -e "${GREEN}✅ CONFIGURATION GRAFANA TERMINÉE${NC}"
echo "================================================================"
echo ""

echo "📊 RÉSUMÉ:"
echo "  • Nginx configuré: ✅"
echo "  • Site activé: ✅"
echo "  • DNS: $(host $DOMAIN &> /dev/null && echo '✅' || echo '⚠️  À vérifier')"
echo "  • SSL: $([ -f /etc/letsencrypt/live/$DOMAIN/fullchain.pem ] && echo '✅' || echo '⚠️  À configurer')"
echo ""

echo "🌐 ACCÈS:"
echo "  • HTTP:  http://$DOMAIN (redirige vers HTTPS)"
echo "  • HTTPS: https://$DOMAIN"
echo ""

echo "🔐 CREDENTIALS PAR DÉFAUT GRAFANA:"
echo "  • Username: admin"
echo "  • Password: admin (à changer au premier login!)"
echo ""

echo "🔧 COMMANDES UTILES:"
echo "  • Logs Grafana:  docker logs $GRAFANA_CONTAINER -f"
echo "  • Restart:       docker restart $GRAFANA_CONTAINER"
echo "  • Nginx logs:    tail -f /var/log/nginx/grafana-*.log"
echo ""

echo "⚠️  SÉCURITÉ RECOMMANDÉE:"
echo "  1. Changez le mot de passe admin immédiatement"
echo "  2. Configurez l'authentification (OAuth, LDAP, etc.)"
echo "  3. Limitez l'accès par IP si nécessaire"
echo ""

echo "✅ Configuration terminée!"
echo ""
