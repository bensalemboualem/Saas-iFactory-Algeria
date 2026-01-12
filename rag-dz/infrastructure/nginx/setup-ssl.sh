#!/usr/bin/env bash
# ==============================================
# SSL/TLS Setup - Let's Encrypt avec Certbot
# ==============================================
# Configure les certificats SSL automatiques
# avec renouvellement automatique
# ==============================================

set -e

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
DOMAIN="${DOMAIN:-www.iafactoryalgeria.com}"
EMAIL="${EMAIL:-admin@iafactoryalgeria.com}"
STAGING="${STAGING:-0}"  # 1 pour staging (tests), 0 pour production

echo -e "${BLUE}==============================================\${NC}"
echo -e "${BLUE}🔒 SSL/TLS Setup - Let's Encrypt${NC}"
echo -e "${BLUE}==============================================\${NC}"

# Vérifier si on est root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}❌ Ce script doit être exécuté en tant que root${NC}"
    exit 1
fi

# Installer Certbot si nécessaire
echo -e "${YELLOW}📦 Installation de Certbot...${NC}"
if ! command -v certbot &> /dev/null; then
    if [ -f /etc/debian_version ]; then
        # Debian/Ubuntu
        apt-get update
        apt-get install -y certbot python3-certbot-nginx
    elif [ -f /etc/redhat-release ]; then
        # RHEL/CentOS/AlmaLinux
        yum install -y certbot python3-certbot-nginx
    else
        echo -e "${RED}❌ Distribution non supportée${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Certbot installé${NC}"
else
    echo -e "${GREEN}✅ Certbot déjà installé${NC}"
fi

# Créer le répertoire pour le challenge
mkdir -p /var/www/certbot
chown -R nginx:nginx /var/www/certbot || chown -R www-data:www-data /var/www/certbot

# Domaines à certifier
DOMAINS=(
    "$DOMAIN"
    "api.$DOMAIN"
    "hub.$DOMAIN"
    "studio.$DOMAIN"
    "n8n.$DOMAIN"
    "monitoring.$DOMAIN"
    "prometheus.$DOMAIN"
)

# Construire la liste de domaines pour Certbot
DOMAIN_ARGS=""
for domain in "${DOMAINS[@]}"; do
    DOMAIN_ARGS="$DOMAIN_ARGS -d $domain"
done

echo -e "${YELLOW}📋 Domaines à certifier:${NC}"
for domain in "${DOMAINS[@]}"; do
    echo -e "  - $domain"
done

# Arrêter Nginx temporairement
echo -e "${YELLOW}🛑 Arrêt temporaire de Nginx...${NC}"
systemctl stop nginx || docker-compose stop nginx || true

# Mode staging ou production
if [ "$STAGING" = "1" ]; then
    echo -e "${YELLOW}⚠️  Mode STAGING (test) activé${NC}"
    STAGING_ARG="--staging"
else
    echo -e "${GREEN}🚀 Mode PRODUCTION activé${NC}"
    STAGING_ARG=""
fi

# Obtenir les certificats
echo -e "${YELLOW}🔐 Obtention des certificats SSL...${NC}"
certbot certonly \
    --standalone \
    $STAGING_ARG \
    --non-interactive \
    --agree-tos \
    --email "$EMAIL" \
    $DOMAIN_ARGS \
    --rsa-key-size 4096 \
    --must-staple

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Certificats SSL obtenus avec succès !${NC}"
else
    echo -e "${RED}❌ Erreur lors de l'obtention des certificats${NC}"
    exit 1
fi

# Créer un lien symbolique pour le domaine principal
CERT_PATH="/etc/letsencrypt/live/$DOMAIN"
if [ -d "$CERT_PATH" ]; then
    echo -e "${GREEN}✅ Certificats disponibles dans: $CERT_PATH${NC}"
    ls -la "$CERT_PATH"
else
    echo -e "${RED}❌ Certificats non trouvés dans: $CERT_PATH${NC}"
    exit 1
fi

# Configuration du renouvellement automatique
echo -e "${YELLOW}🔄 Configuration du renouvellement automatique...${NC}"

# Créer un script de renouvellement
cat > /etc/cron.daily/certbot-renew << 'EOF'
#!/bin/bash
# Renouvellement automatique des certificats SSL

# Renouveler les certificats
certbot renew --quiet --deploy-hook "systemctl reload nginx || docker-compose restart nginx"

# Nettoyer les anciens certificats
certbot delete --cert-name expired 2>/dev/null || true

# Log
echo "[$(date)] Certificats SSL renouvelés" >> /var/log/certbot-renew.log
EOF

chmod +x /etc/cron.daily/certbot-renew
echo -e "${GREEN}✅ Renouvellement automatique configuré (quotidien)${NC}"

# Tester le renouvellement (dry-run)
echo -e "${YELLOW}🧪 Test du renouvellement...${NC}"
certbot renew --dry-run

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Test de renouvellement réussi !${NC}"
else
    echo -e "${YELLOW}⚠️  Test de renouvellement échoué (pas critique si nouveaux certificats)${NC}"
fi

# Permissions
echo -e "${YELLOW}🔐 Configuration des permissions...${NC}"
chmod -R 755 /etc/letsencrypt/live
chmod -R 755 /etc/letsencrypt/archive

# Redémarrer Nginx
echo -e "${YELLOW}🔄 Redémarrage de Nginx...${NC}"
if systemctl is-active --quiet nginx; then
    systemctl restart nginx
    echo -e "${GREEN}✅ Nginx redémarré (systemd)${NC}"
elif docker ps | grep -q nginx; then
    docker-compose restart nginx
    echo -e "${GREEN}✅ Nginx redémarré (Docker)${NC}"
else
    echo -e "${YELLOW}⚠️  Nginx non trouvé, démarrez-le manuellement${NC}"
fi

# Afficher les informations sur les certificats
echo -e "${BLUE}==============================================\${NC}"
echo -e "${GREEN}✅ Configuration SSL complète !${NC}"
echo -e "${BLUE}==============================================\${NC}"
echo -e "${GREEN}📜 Certificats:${NC}"
certbot certificates

echo -e "\n${GREEN}🔒 Vos certificats SSL sont configurés pour:${NC}"
for domain in "${DOMAINS[@]}"; do
    echo -e "  ✅ https://$domain"
done

echo -e "\n${GREEN}🔄 Renouvellement automatique:${NC}"
echo -e "  - Vérifié quotidiennement via cron"
echo -e "  - Renouvellement automatique 30 jours avant expiration"
echo -e "  - Nginx rechargé automatiquement après renouvellement"

echo -e "\n${YELLOW}📝 Prochaines étapes:${NC}"
echo -e "  1. Vérifier que tous les domaines pointent vers votre serveur"
echo -e "  2. Tester les domaines: curl -I https://$DOMAIN"
echo -e "  3. Vérifier les logs Nginx: tail -f /var/log/nginx/error.log"

echo -e "\n${GREEN}✅ Setup SSL terminé !${NC}"
