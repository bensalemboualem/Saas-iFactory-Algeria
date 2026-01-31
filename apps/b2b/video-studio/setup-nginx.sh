#!/bin/bash
set -e

# ============================================
# 🌐 CONFIGURATION AUTOMATIQUE NGINX + SSL
# IAFactory Video Studio Pro
# ============================================

echo "🌐 Configuration de Nginx pour Video Studio Pro..."
echo ""

# Vérifier qu'on est root
if [ "$EUID" -ne 0 ]; then
   echo "❌ Ce script doit être exécuté en tant que root"
   exit 1
fi

# Demander les domaines
read -p "Domaine frontend (ex: video-studio.iafactoryalgeria.com): " FRONTEND_DOMAIN
read -p "Domaine API (ex: api.iafactoryalgeria.com): " API_DOMAIN
read -p "Email pour Let's Encrypt: " LETSENCRYPT_EMAIL

# Vérifier que Nginx est installé
if ! command -v nginx &> /dev/null; then
    echo "📦 Installation de Nginx..."
    apt update
    apt install -y nginx
fi

# ============================================
# CRÉER LA CONFIGURATION NGINX
# ============================================
echo "📝 Création de la configuration Nginx..."

cat > /etc/nginx/sites-available/video-studio << EOF
# ============================================
# IAFACTORY VIDEO STUDIO PRO - NGINX CONFIG
# ============================================

# Frontend Next.js
server {
    listen 80;
    listen [::]:80;
    server_name $FRONTEND_DOMAIN;

    # Redirection HTTPS (sera ajoutée par Certbot)
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Next.js specific
    location /_next/static/ {
        proxy_pass http://localhost:3000/_next/static/;
        proxy_cache_valid 60m;
        add_header Cache-Control "public, max-age=3600, immutable";
    }

    # Logs
    access_log /var/log/nginx/video-studio-frontend-access.log;
    error_log /var/log/nginx/video-studio-frontend-error.log;
}

# Backend FastAPI
server {
    listen 80;
    listen [::]:80;
    server_name $API_DOMAIN;

    # Limite de taille des uploads (important pour vidéos)
    client_max_body_size 500M;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        # Timeouts pour génération vidéo (peut être long)
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }

    # Webhooks Stripe
    location /webhooks/stripe {
        proxy_pass http://localhost:8000/webhooks/stripe;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }

    # Documentation API
    location /docs {
        proxy_pass http://localhost:8000/docs;
        proxy_set_header Host \$host;
    }

    location /redoc {
        proxy_pass http://localhost:8000/redoc;
        proxy_set_header Host \$host;
    }

    # Logs
    access_log /var/log/nginx/video-studio-api-access.log;
    error_log /var/log/nginx/video-studio-api-error.log;
}
EOF

# ============================================
# ACTIVER LA CONFIGURATION
# ============================================
echo "🔗 Activation de la configuration..."

# Supprimer le lien symbolique s'il existe
rm -f /etc/nginx/sites-enabled/video-studio

# Créer le lien symbolique
ln -s /etc/nginx/sites-available/video-studio /etc/nginx/sites-enabled/

# Supprimer la config par défaut si elle existe
rm -f /etc/nginx/sites-enabled/default

# Tester la configuration
echo "🧪 Test de la configuration Nginx..."
if nginx -t; then
    echo "✅ Configuration Nginx valide"
else
    echo "❌ Erreur dans la configuration Nginx"
    exit 1
fi

# Redémarrer Nginx
echo "🔄 Redémarrage de Nginx..."
systemctl reload nginx

echo "✅ Nginx configuré avec succès!"
echo ""

# ============================================
# INSTALLER CERTBOT SI NÉCESSAIRE
# ============================================
if ! command -v certbot &> /dev/null; then
    echo "🔒 Installation de Certbot..."
    apt install -y certbot python3-certbot-nginx
fi

# ============================================
# OBTENIR LES CERTIFICATS SSL
# ============================================
echo ""
echo "🔒 Obtention des certificats SSL Let's Encrypt..."
echo ""
read -p "Voulez-vous obtenir les certificats SSL maintenant? (y/n): " GET_SSL

if [ "$GET_SSL" = "y" ]; then
    echo ""
    echo "⚠️  IMPORTANT: Assurez-vous que:"
    echo "   1. Les DNS sont configurés ($FRONTEND_DOMAIN → IP du serveur)"
    echo "   2. Les DNS sont configurés ($API_DOMAIN → IP du serveur)"
    echo "   3. Les ports 80 et 443 sont ouverts"
    echo ""
    read -p "Les DNS sont-ils configurés? (y/n): " DNS_READY

    if [ "$DNS_READY" = "y" ]; then
        certbot --nginx \
            -d "$FRONTEND_DOMAIN" \
            -d "$API_DOMAIN" \
            --email "$LETSENCRYPT_EMAIL" \
            --agree-tos \
            --redirect \
            --non-interactive

        if [ $? -eq 0 ]; then
            echo "✅ Certificats SSL obtenus et configurés!"
            echo ""
            echo "🎉 HTTPS activé sur:"
            echo "   - https://$FRONTEND_DOMAIN"
            echo "   - https://$API_DOMAIN"
        else
            echo "⚠️  Échec de l'obtention des certificats SSL"
            echo "   Vérifiez que les DNS pointent vers ce serveur"
            echo "   Vous pouvez réessayer avec:"
            echo "   certbot --nginx -d $FRONTEND_DOMAIN -d $API_DOMAIN"
        fi
    else
        echo "⏭️  Configuration DNS à faire d'abord"
        echo ""
        echo "📝 Configurez vos DNS:"
        echo "   Type A: $FRONTEND_DOMAIN → $(curl -s ifconfig.me)"
        echo "   Type A: $API_DOMAIN → $(curl -s ifconfig.me)"
        echo ""
        echo "Puis lancez:"
        echo "   certbot --nginx -d $FRONTEND_DOMAIN -d $API_DOMAIN"
    fi
else
    echo "⏭️  Configuration SSL à faire plus tard"
    echo ""
    echo "📝 Quand vous serez prêt, lancez:"
    echo "   certbot --nginx -d $FRONTEND_DOMAIN -d $API_DOMAIN"
fi

# ============================================
# RÉSUMÉ
# ============================================
echo ""
echo "============================================"
echo "✅ CONFIGURATION NGINX TERMINÉE"
echo "============================================"
echo ""
echo "📍 Fichier de config: /etc/nginx/sites-available/video-studio"
echo ""
echo "🌐 Domaines configurés:"
echo "   Frontend: http://$FRONTEND_DOMAIN → localhost:3000"
echo "   API:      http://$API_DOMAIN → localhost:8000"
echo ""
echo "🧪 Tester la configuration:"
echo "   curl http://$FRONTEND_DOMAIN"
echo "   curl http://$API_DOMAIN/health"
echo ""
echo "📊 Voir les logs:"
echo "   tail -f /var/log/nginx/video-studio-frontend-access.log"
echo "   tail -f /var/log/nginx/video-studio-api-access.log"
echo ""
echo "🔧 Commandes utiles:"
echo "   nginx -t                    # Tester la config"
echo "   systemctl reload nginx      # Recharger Nginx"
echo "   systemctl status nginx      # État de Nginx"
echo "   certbot renew --dry-run     # Tester le renouvellement SSL"
echo ""
echo "============================================"
