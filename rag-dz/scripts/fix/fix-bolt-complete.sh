#!/bin/bash
# ================================================================
# DIAGNOSTIC ET CORRECTION BOLT.DIY - IAFactory Algeria
# ================================================================
set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "================================================================"
echo "🔧 DIAGNOSTIC ET CORRECTION BOLT.DIY"
echo "================================================================"
echo ""

# ================================================================
# PHASE 1: DIAGNOSTIC
# ================================================================
echo -e "${BLUE}[1/6]${NC} Diagnostic du système..."
echo ""

# Vérifier si Bolt existe
if [ -d "/opt/iafactory-rag-dz/bolt-diy" ]; then
    echo -e "${GREEN}✅ Bolt.diy trouvé dans /opt/iafactory-rag-dz/bolt-diy${NC}"
    BOLT_DIR="/opt/iafactory-rag-dz/bolt-diy"
elif [ -d "/opt/iafactory-rag-dz/frontend/bolt-diy" ]; then
    echo -e "${GREEN}✅ Bolt.diy trouvé dans /opt/iafactory-rag-dz/frontend/bolt-diy${NC}"
    BOLT_DIR="/opt/iafactory-rag-dz/frontend/bolt-diy"
else
    echo -e "${RED}❌ Bolt.diy non trouvé!${NC}"
    echo "Recherche dans tous les emplacements..."
    find /opt -name "*bolt*" -type d 2>/dev/null | head -10
    exit 1
fi

cd "$BOLT_DIR"
echo "📂 Répertoire Bolt: $(pwd)"
echo ""

# Vérifier Docker
echo -e "${BLUE}[2/6]${NC} Vérification Docker..."
if docker ps | grep -q bolt; then
    echo -e "${GREEN}✅ Conteneur Bolt en cours d'exécution${NC}"
    docker ps | grep bolt
else
    echo -e "${YELLOW}⚠️  Aucun conteneur Bolt en cours${NC}"
fi
echo ""

# Vérifier Nginx
echo -e "${BLUE}[3/6]${NC} Vérification Nginx..."
if [ -f "/etc/nginx/sites-available/iafactoryalgeria.com" ]; then
    echo -e "${GREEN}✅ Config Nginx trouvée${NC}"

    # Chercher la config Bolt
    if grep -q "/bolt" /etc/nginx/sites-available/iafactoryalgeria.com; then
        echo -e "${GREEN}✅ Route /bolt/ configurée${NC}"
        echo "Configuration actuelle:"
        grep -A 10 "location /bolt" /etc/nginx/sites-available/iafactoryalgeria.com
    else
        echo -e "${RED}❌ Route /bolt/ NON configurée${NC}"
    fi
else
    echo -e "${RED}❌ Fichier Nginx non trouvé${NC}"
fi
echo ""

# Vérifier le port Bolt
echo -e "${BLUE}[4/6]${NC} Vérification du port Bolt..."
BOLT_PORT=$(grep -r "VITE_PORT\|PORT" "$BOLT_DIR/.env" 2>/dev/null | head -1 || echo "5173")
echo "Port Bolt détecté: $BOLT_PORT"

if netstat -tlnp 2>/dev/null | grep -q ":$BOLT_PORT"; then
    echo -e "${GREEN}✅ Port $BOLT_PORT en écoute${NC}"
    netstat -tlnp | grep ":$BOLT_PORT"
else
    echo -e "${YELLOW}⚠️  Port $BOLT_PORT NON en écoute${NC}"
fi
echo ""

# ================================================================
# PHASE 2: VÉRIFIER DNS
# ================================================================
echo -e "${BLUE}[5/6]${NC} Vérification DNS..."
echo ""

# Tester www.bolt.iafactoryalgeria.com
if host www.bolt.iafactoryalgeria.com > /dev/null 2>&1; then
    echo -e "${GREEN}✅ www.bolt.iafactoryalgeria.com résolu${NC}"
    host www.bolt.iafactoryalgeria.com
    DNS_EXISTS=true
else
    echo -e "${YELLOW}⚠️  www.bolt.iafactoryalgeria.com NON résolu${NC}"
    echo "   Bolt sera accessible via: https://www.iafactoryalgeria.com/bolt/"
    DNS_EXISTS=false
fi
echo ""

# ================================================================
# PHASE 3: CORRECTION
# ================================================================
echo -e "${BLUE}[6/6]${NC} Application des corrections..."
echo ""

# Correction 1: Redémarrer Bolt si nécessaire
if ! docker ps | grep -q bolt; then
    echo "🔄 Démarrage de Bolt..."

    # Chercher docker-compose.yml
    if [ -f "$BOLT_DIR/docker-compose.yml" ]; then
        cd "$BOLT_DIR"
        docker-compose up -d
        echo -e "${GREEN}✅ Bolt démarré via docker-compose${NC}"
    elif [ -f "/opt/iafactory-rag-dz/docker-compose.yml" ]; then
        cd /opt/iafactory-rag-dz
        docker-compose up -d bolt
        echo -e "${GREEN}✅ Bolt démarré${NC}"
    else
        echo -e "${YELLOW}⚠️  docker-compose.yml non trouvé, tentative npm...${NC}"
        cd "$BOLT_DIR"
        npm install
        nohup npm run dev > bolt.log 2>&1 &
        echo -e "${GREEN}✅ Bolt démarré en mode npm${NC}"
    fi
fi

# Correction 2: Vérifier/Créer config Nginx
echo ""
echo "🔧 Configuration Nginx..."

NGINX_CONFIG_BOLT='
    # Bolt.diy - AI Code Generator
    location /bolt/ {
        proxy_pass http://127.0.0.1:5173/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
    }

    # Bolt.diy - HMR (Hot Module Replacement)
    location /bolt/@vite/ {
        proxy_pass http://127.0.0.1:5173/@vite/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
'

if ! grep -q "location /bolt/" /etc/nginx/sites-available/iafactoryalgeria.com; then
    echo "Ajout de la configuration Bolt dans Nginx..."

    # Backup
    cp /etc/nginx/sites-available/iafactoryalgeria.com /etc/nginx/sites-available/iafactoryalgeria.com.backup-$(date +%Y%m%d-%H%M%S)

    # Ajouter la config avant la dernière accolade fermante
    sed -i '/^}$/i\'"$NGINX_CONFIG_BOLT" /etc/nginx/sites-available/iafactoryalgeria.com

    echo -e "${GREEN}✅ Configuration Nginx ajoutée${NC}"
else
    echo -e "${GREEN}✅ Configuration Nginx déjà présente${NC}"
fi

# Test et reload Nginx
echo ""
echo "🧪 Test de la configuration Nginx..."
if nginx -t; then
    echo -e "${GREEN}✅ Configuration Nginx valide${NC}"
    echo "🔄 Rechargement de Nginx..."
    systemctl reload nginx
    echo -e "${GREEN}✅ Nginx rechargé${NC}"
else
    echo -e "${RED}❌ Erreur dans la configuration Nginx${NC}"
    echo "Restauration du backup..."
    cp /etc/nginx/sites-available/iafactoryalgeria.com.backup-$(date +%Y%m%d)* /etc/nginx/sites-available/iafactoryalgeria.com
fi

# Correction 3: Créer sous-domaine si DNS existe
if [ "$DNS_EXISTS" = true ]; then
    echo ""
    echo "🌐 Configuration sous-domaine bolt.iafactoryalgeria.com..."

    SUBDOMAIN_CONFIG="/etc/nginx/sites-available/bolt.iafactoryalgeria.com"

    cat > "$SUBDOMAIN_CONFIG" << 'NGINXEOF'
# HTTP → HTTPS Redirect
server {
    listen 80;
    listen [::]:80;
    server_name bolt.iafactoryalgeria.com www.bolt.iafactoryalgeria.com;
    return 301 https://$host$request_uri;
}

# HTTPS Server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name bolt.iafactoryalgeria.com www.bolt.iafactoryalgeria.com;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    client_max_body_size 100M;

    # Bolt.diy Frontend
    location / {
        proxy_pass http://127.0.0.1:5173;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
    }

    # HMR WebSocket
    location /@vite/ {
        proxy_pass http://127.0.0.1:5173/@vite/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
NGINXEOF

    # Activer le site
    ln -sf "$SUBDOMAIN_CONFIG" /etc/nginx/sites-enabled/

    # Test Nginx
    if nginx -t; then
        systemctl reload nginx

        # Obtenir certificat SSL
        echo "🔐 Obtention certificat SSL pour bolt.iafactoryalgeria.com..."
        certbot --nginx -d bolt.iafactoryalgeria.com -d www.bolt.iafactoryalgeria.com \
            --non-interactive --agree-tos --email admin@iafactoryalgeria.com --redirect

        echo -e "${GREEN}✅ Sous-domaine bolt.iafactoryalgeria.com configuré${NC}"
    else
        echo -e "${RED}❌ Erreur config Nginx pour sous-domaine${NC}"
    fi
fi

# ================================================================
# PHASE 4: VÉRIFICATION FINALE
# ================================================================
echo ""
echo "================================================================"
echo "📊 VÉRIFICATION FINALE"
echo "================================================================"
echo ""

echo "🐳 Conteneurs Docker:"
docker ps | grep -E "bolt|CONTAINER" || echo "Aucun conteneur Bolt"

echo ""
echo "🌐 Ports en écoute:"
netstat -tlnp | grep ":5173" || echo "Port 5173 non en écoute"

echo ""
echo "📡 Services Nginx:"
systemctl status nginx --no-pager | head -10

echo ""
echo "================================================================"
echo -e "${GREEN}✅ ✅ ✅ DIAGNOSTIC ET CORRECTIONS TERMINÉS! ✅ ✅ ✅${NC}"
echo "================================================================"
echo ""

if [ "$DNS_EXISTS" = true ]; then
    echo "🌐 ACCÈS BOLT:"
    echo "   • https://bolt.iafactoryalgeria.com"
    echo "   • https://www.bolt.iafactoryalgeria.com"
else
    echo "🌐 ACCÈS BOLT:"
    echo "   • https://www.iafactoryalgeria.com/bolt/"
fi

echo ""
echo "🔧 COMMANDES UTILES:"
echo "   • Logs Bolt:      docker logs bolt -f  (si Docker)"
echo "   • Logs Bolt:      tail -f $BOLT_DIR/bolt.log  (si npm)"
echo "   • Restart Bolt:   docker-compose restart bolt"
echo "   • Status Nginx:   systemctl status nginx"
echo ""
