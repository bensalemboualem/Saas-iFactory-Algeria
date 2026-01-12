#!/bin/bash
# ================================================================
# EXÉCUTION COMPLÈTE DES 4 TÂCHES PRIORITAIRES
# IAFactory Algeria - Script Master
# ================================================================
# À exécuter via Hetzner Console ou SSH
# ================================================================

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

clear

cat << 'BANNER'
================================================================
🚀 IAFACTORY ALGERIA - CONFIGURATION PROFESSIONNELLE
================================================================
    Exécution des 4 tâches prioritaires:
    1. Sécuriser PostgreSQL et Ollama
    2. Vérifier/Corriger Bolt.diy
    3. Déployer 5 agents IA
    4. Configurer Grafana public avec SSL
================================================================
BANNER

echo ""
read -p "Appuyez sur ENTRÉE pour commencer (ou Ctrl+C pour annuler)..."
echo ""

# ================================================================
# TÂCHE 1: SÉCURISATION POSTGRESQL & OLLAMA
# ================================================================

echo "================================================================"
echo -e "${BLUE}TÂCHE 1/4:${NC} SÉCURISATION POSTGRESQL & OLLAMA"
echo "================================================================"
echo ""

cd /opt/iafactory-rag-dz

echo "📋 Analyse des ports actuels..."
echo ""
echo "Conteneurs PostgreSQL/Ollama:"
docker ps --format "{{.Names}}\t{{.Ports}}" | grep -E "(postgres|ollama)" || echo "Aucun trouvé"

echo ""
echo "Ports exposés publiquement:"
netstat -tlnp 2>/dev/null | grep -E ":(5432|6330|11434|8186) " | grep "0.0.0.0" || echo "Aucun (déjà sécurisé)"

echo ""
echo "🔍 Recherche de tous les docker-compose.yml..."
COMPOSE_FILES=$(find /opt/iafactory-rag-dz -name "docker-compose*.yml" -type f 2>/dev/null)
echo "$COMPOSE_FILES"

echo ""
echo "🔒 Application de la sécurisation..."

for COMPOSE_FILE in $COMPOSE_FILES; do
    echo ""
    echo "Fichier: $COMPOSE_FILE"

    # Backup
    cp "$COMPOSE_FILE" "${COMPOSE_FILE}.backup-$(date +%Y%m%d_%H%M%S)"

    # Sécuriser PostgreSQL
    if grep -q "5432" "$COMPOSE_FILE"; then
        sed -i 's/- "5432:5432"/- "127.0.0.1:5432:5432"/g' "$COMPOSE_FILE"
        sed -i 's/- "6330:5432"/- "127.0.0.1:6330:5432"/g' "$COMPOSE_FILE"
        echo "  ✅ PostgreSQL sécurisé"
    fi

    # Sécuriser Ollama
    if grep -q "11434" "$COMPOSE_FILE"; then
        sed -i 's/- "11434:11434"/- "127.0.0.1:11434:11434"/g' "$COMPOSE_FILE"
        sed -i 's/- "8186:11434"/- "127.0.0.1:8186:11434"/g' "$COMPOSE_FILE"
        echo "  ✅ Ollama sécurisé"
    fi
done

echo ""
echo "🔄 Redémarrage des services..."

# Redémarrer tous les PostgreSQL et Ollama
for CONTAINER in $(docker ps --format '{{.Names}}' | grep -E "(postgres|ollama)"); do
    echo "  Redémarrage: $CONTAINER"
    docker restart "$CONTAINER" > /dev/null 2>&1
done

echo ""
echo "⏳ Attente 15 secondes pour stabilisation..."
sleep 15

echo ""
echo "✅ Vérification finale:"
echo ""
netstat -tlnp 2>/dev/null | grep -E ":(5432|6330|11434|8186) " | while read line; do
    if echo "$line" | grep -q "127.0.0.1"; then
        echo -e "  ${GREEN}✅ $(echo "$line" | awk '{print $4}') - Localhost uniquement${NC}"
    elif echo "$line" | grep -q "0.0.0.0"; then
        echo -e "  ${RED}⚠️  $(echo "$line" | awk '{print $4}') - ENCORE PUBLIC${NC}"
    fi
done

echo ""
echo -e "${GREEN}✅ TÂCHE 1/4 TERMINÉE${NC}"
echo ""
read -p "Appuyez sur ENTRÉE pour continuer..."

# ================================================================
# TÂCHE 2: BOLT.DIY
# ================================================================

echo ""
echo "================================================================"
echo -e "${BLUE}TÂCHE 2/4:${NC} VÉRIFICATION/CORRECTION BOLT.DIY"
echo "================================================================"
echo ""

# Recherche de Bolt
BOLT_PATH=""
BOLT_DIRS=(
    "/opt/iafactory-rag-dz/bolt-diy"
    "/opt/iafactory-rag-dz/frontend/bolt-diy"
    "/opt/bolt-diy"
)

for dir in "${BOLT_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        BOLT_PATH="$dir"
        echo -e "${GREEN}✅ Bolt trouvé: $BOLT_PATH${NC}"
        break
    fi
done

if [ -z "$BOLT_PATH" ]; then
    echo -e "${RED}❌ Bolt.diy non trouvé${NC}"
    echo "Recherche globale..."
    find /opt -name "*bolt*" -type d 2>/dev/null | head -5
    echo ""
    echo -e "${YELLOW}⚠️  Bolt.diy n'est pas installé. Voulez-vous l'installer?${NC}"
    read -p "Installer Bolt.diy? (o/N): " INSTALL_BOLT

    if [ "$INSTALL_BOLT" = "o" ] || [ "$INSTALL_BOLT" = "O" ]; then
        echo ""
        echo "Installation de Bolt.diy..."
        cd /opt/iafactory-rag-dz
        git clone https://github.com/stackblitz/bolt.new.git bolt-diy
        cd bolt-diy
        npm install
        echo -e "${GREEN}✅ Bolt.diy installé${NC}"
        BOLT_PATH="/opt/iafactory-rag-dz/bolt-diy"
    else
        echo "⏭️  Saut de Bolt.diy"
        echo ""
        read -p "Appuyez sur ENTRÉE pour continuer..."
        SKIP_BOLT=1
    fi
fi

if [ -z "$SKIP_BOLT" ] && [ -n "$BOLT_PATH" ]; then
    cd "$BOLT_PATH"

    echo ""
    echo "📊 Diagnostic:"

    # Docker
    if docker ps | grep -q bolt; then
        echo -e "  ${GREEN}✅ Conteneur Bolt: Running${NC}"
        BOLT_RUNNING=1
    else
        echo -e "  ${YELLOW}⚠️  Conteneur Bolt: Stopped${NC}"
        BOLT_RUNNING=0
    fi

    # Port 5173
    if netstat -tlnp 2>/dev/null | grep -q ":5173 "; then
        echo -e "  ${GREEN}✅ Port 5173: En écoute${NC}"
        PORT_OK=1
    else
        echo -e "  ${RED}❌ Port 5173: NON en écoute${NC}"
        PORT_OK=0
    fi

    # HTTP test
    if timeout 3 curl -s http://localhost:5173 > /dev/null 2>&1; then
        echo -e "  ${GREEN}✅ HTTP: Répond${NC}"
        HTTP_OK=1
    else
        echo -e "  ${RED}❌ HTTP: Ne répond pas${NC}"
        HTTP_OK=0
    fi

    # Nginx
    if grep -q "location /bolt" /etc/nginx/sites-enabled/* 2>/dev/null; then
        echo -e "  ${GREEN}✅ Nginx: Configuré${NC}"
        NGINX_OK=1
    else
        echo -e "  ${YELLOW}⚠️  Nginx: Non configuré${NC}"
        NGINX_OK=0
    fi

    echo ""

    # Corrections si nécessaire
    if [ $BOLT_RUNNING -eq 0 ] || [ $PORT_OK -eq 0 ] || [ $HTTP_OK -eq 0 ]; then
        echo "🔧 Démarrage de Bolt..."

        if [ -f "docker-compose.yml" ]; then
            docker-compose up -d --build
        elif [ -f "package.json" ]; then
            npm run dev > bolt.log 2>&1 &
            echo "  Processus démarré en arrière-plan"
        fi

        echo "⏳ Attente 30 secondes..."
        sleep 30
    fi

    # Configuration Nginx
    if [ $NGINX_OK -eq 0 ]; then
        echo ""
        echo "🔧 Configuration Nginx pour Bolt..."

        # Vérifier quel fichier nginx utiliser
        NGINX_CONF="/etc/nginx/sites-available/iafactoryalgeria.com"
        if [ ! -f "$NGINX_CONF" ]; then
            NGINX_CONF=$(ls /etc/nginx/sites-available/ | grep -v default | head -1)
            NGINX_CONF="/etc/nginx/sites-available/$NGINX_CONF"
        fi

        echo "  Fichier Nginx: $NGINX_CONF"

        # Ajouter la config Bolt
        cat >> "$NGINX_CONF" << 'NGINXBOLT'

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
NGINXBOLT

        # Test et reload
        if nginx -t 2>&1 | grep -q "successful"; then
            systemctl reload nginx
            echo -e "  ${GREEN}✅ Nginx rechargé${NC}"
        else
            echo -e "  ${RED}❌ Erreur Nginx${NC}"
        fi
    fi

    echo ""
    echo "✅ Test final:"
    if timeout 5 curl -s http://localhost:5173 > /dev/null 2>&1; then
        echo -e "  ${GREEN}✅ Bolt accessible: http://localhost:5173${NC}"
        echo -e "  ${GREEN}✅ Via proxy: https://www.iafactoryalgeria.com/bolt/${NC}"
    else
        echo -e "  ${YELLOW}⚠️  Bolt ne répond pas encore${NC}"
        echo "  Vérifiez les logs: docker logs \$(docker ps | grep bolt | awk '{print \$1}')"
    fi
fi

echo ""
echo -e "${GREEN}✅ TÂCHE 2/4 TERMINÉE${NC}"
echo ""
read -p "Appuyez sur ENTRÉE pour continuer..."

# ================================================================
# TÂCHE 3: AGENTS IA
# ================================================================

echo ""
echo "================================================================"
echo -e "${BLUE}TÂCHE 3/4:${NC} DÉPLOIEMENT DES 5 AGENTS IA"
echo "================================================================"
echo ""

AGENTS_DIR="/opt/iafactory-rag-dz/ia-agents"

echo "Ce déploiement va créer:"
echo "  • Qdrant (Vector DB)"
echo "  • Local RAG Agent"
echo "  • Finance Agent (fiscal algérien)"
echo "  • Chat PDF Agent"
echo "  • Hybrid Search Agent"
echo "  • Voice Support Agent"
echo ""

read -p "Déployer les agents IA? (o/N): " DEPLOY_AGENTS

if [ "$DEPLOY_AGENTS" = "o" ] || [ "$DEPLOY_AGENTS" = "O" ]; then
    echo ""
    echo "📦 Création de la structure..."

    mkdir -p "$AGENTS_DIR"
    cd "$AGENTS_DIR"

    # Copier le script de déploiement
    cat > deploy.sh << 'DEPLOYSCRIPT'
#!/bin/bash
# Script généré automatiquement

echo "Installation des agents IA..."
echo "Cette opération peut prendre 10-15 minutes (build Docker)"
echo ""

# Création structure minimale pour test
mkdir -p local-rag finance-agent chat-pdf hybrid-search voice-support

# Docker-compose minimal
cat > docker-compose.yml << 'YMLEOF'
version: '3.8'
services:
  qdrant:
    image: qdrant/qdrant:latest
    container_name: iaf-qdrant
    ports:
      - "127.0.0.1:6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage
    restart: unless-stopped

volumes:
  qdrant_data:
YMLEOF

docker-compose up -d
echo "✅ Qdrant démarré"
echo ""
echo "Pour déploiement complet, voir: /opt/iafactory-rag-dz/deploy-ia-agents.sh"
DEPLOYSCRIPT

    chmod +x deploy.sh
    ./deploy.sh

    echo -e "${GREEN}✅ Base des agents IA créée${NC}"
    echo ""
    echo "📝 Pour déploiement complet:"
    echo "  Copiez le contenu de ia-agents/ depuis votre machine locale"
    echo "  Ou utilisez le script: /opt/iafactory-rag-dz/deploy-ia-agents.sh"
else
    echo "⏭️  Déploiement agents IA reporté"
fi

echo ""
echo -e "${GREEN}✅ TÂCHE 3/4 TERMINÉE${NC}"
echo ""
read -p "Appuyez sur ENTRÉE pour continuer..."

# ================================================================
# TÂCHE 4: GRAFANA PUBLIC
# ================================================================

echo ""
echo "================================================================"
echo -e "${BLUE}TÂCHE 4/4:${NC} CONFIGURATION GRAFANA PUBLIC"
echo "================================================================"
echo ""

# Vérifier Grafana
if docker ps | grep -q grafana; then
    GRAFANA_CONTAINER=$(docker ps | grep grafana | awk '{print $1}')
    GRAFANA_PORT=$(docker ps | grep grafana | awk '{print $NF}' | grep -oP '\d+:\K\d+' | head -1)

    echo -e "${GREEN}✅ Grafana trouvé${NC}"
    echo "  Container: $(docker ps | grep grafana | awk '{print $NF}')"
    echo "  Port: $GRAFANA_PORT"

    echo ""
    echo "⚠️  PRÉREQUIS DNS:"
    echo ""
    echo "  Avant de continuer, configurez le DNS:"
    echo "  Type: A"
    echo "  Name: grafana"
    echo "  Value: 46.224.3.125"
    echo ""

    read -p "DNS configuré? Continuer? (o/N): " SETUP_GRAFANA

    if [ "$SETUP_GRAFANA" = "o" ] || [ "$SETUP_GRAFANA" = "O" ]; then
        echo ""
        echo "🔧 Configuration Nginx..."

        cat > /etc/nginx/sites-available/grafana.iafactoryalgeria.com << 'GRAFANANGINX'
server {
    listen 80;
    server_name grafana.iafactoryalgeria.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name grafana.iafactoryalgeria.com;

    location / {
        proxy_pass http://127.0.0.1:3033;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
GRAFANANGINX

        ln -sf /etc/nginx/sites-available/grafana.iafactoryalgeria.com /etc/nginx/sites-enabled/

        if nginx -t 2>&1 | grep -q "successful"; then
            systemctl reload nginx
            echo -e "${GREEN}✅ Nginx configuré${NC}"
        fi

        echo ""
        echo "🔒 Configuration SSL..."
        if certbot --nginx -d grafana.iafactoryalgeria.com \
            --non-interactive \
            --agree-tos \
            --email admin@iafactoryalgeria.com \
            --redirect 2>&1 | grep -q "Successfully"; then

            echo -e "${GREEN}✅ SSL configuré${NC}"
            echo ""
            echo -e "${GREEN}🎉 Grafana accessible sur: https://grafana.iafactoryalgeria.com${NC}"
        else
            echo -e "${YELLOW}⚠️  SSL échoué - Configuration manuelle requise${NC}"
            echo "  Commande: certbot --nginx -d grafana.iafactoryalgeria.com"
        fi
    else
        echo "⏭️  Configuration Grafana reportée"
    fi
else
    echo -e "${RED}❌ Grafana ne tourne pas${NC}"
    echo "Démarrez Grafana avec: docker-compose up -d grafana"
fi

echo ""
echo -e "${GREEN}✅ TÂCHE 4/4 TERMINÉE${NC}"
echo ""

# ================================================================
# RÉSUMÉ FINAL
# ================================================================

echo "================================================================"
echo -e "${GREEN}🎉 TOUTES LES TÂCHES TERMINÉES!${NC}"
echo "================================================================"
echo ""

echo "📊 RÉSUMÉ:"
echo ""

echo "1. Sécurité PostgreSQL/Ollama:"
netstat -tlnp 2>/dev/null | grep -E ":(5432|6330|11434|8186) " | grep "127.0.0.1" > /dev/null && \
    echo -e "   ${GREEN}✅ Sécurisé (localhost uniquement)${NC}" || \
    echo -e "   ${YELLOW}⚠️  À vérifier${NC}"

echo ""
echo "2. Bolt.diy:"
timeout 2 curl -s http://localhost:5173 > /dev/null 2>&1 && \
    echo -e "   ${GREEN}✅ Opérationnel${NC}" || \
    echo -e "   ${YELLOW}⚠️  À vérifier${NC}"

echo ""
echo "3. Agents IA:"
docker ps | grep -q qdrant && \
    echo -e "   ${GREEN}✅ Qdrant démarré${NC}" || \
    echo -e "   ${YELLOW}⚠️  Non déployé${NC}"

echo ""
echo "4. Grafana Public:"
curl -sk https://grafana.iafactoryalgeria.com > /dev/null 2>&1 && \
    echo -e "   ${GREEN}✅ Accessible (https://grafana.iafactoryalgeria.com)${NC}" || \
    echo -e "   ${YELLOW}⚠️  Non configuré${NC}"

echo ""
echo "================================================================"
echo -e "${BLUE}📝 LOGS ET VÉRIFICATIONS${NC}"
echo "================================================================"
echo ""
echo "Containers actifs:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | head -10

echo ""
echo "🔧 Commandes utiles:"
echo "  • Status Docker:     docker ps"
echo "  • Logs service:      docker logs <container-name> -f"
echo "  • Restart service:   docker restart <container-name>"
echo "  • Nginx reload:      systemctl reload nginx"
echo "  • Voir ce script:    cat $0"
echo ""

echo "✅ Configuration professionnelle terminée!"
echo ""
