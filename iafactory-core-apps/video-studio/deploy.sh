#!/bin/bash
set -e

# ============================================
# 🚀 SCRIPT D'INSTALLATION AUTOMATIQUE
# IAFactory Video Studio Pro - VPS Hetzner
# ============================================

echo "🎬 Démarrage de l'installation Video Studio Pro..."
echo ""

# Vérifier qu'on est root
if [ "$EUID" -ne 0 ]; then
   echo "❌ Ce script doit être exécuté en tant que root (sudo)"
   exit 1
fi

# ============================================
# ÉTAPE 1: MISE À JOUR SYSTÈME
# ============================================
echo "📦 [1/8] Mise à jour du système..."
apt update -qq
apt upgrade -y -qq
apt install -y git curl wget vim htop build-essential

# ============================================
# ÉTAPE 2: INSTALLATION DOCKER
# ============================================
echo "🐳 [2/8] Installation de Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com | sh
    systemctl enable docker
    systemctl start docker
    echo "✅ Docker installé"
else
    echo "✅ Docker déjà installé"
fi

# ============================================
# ÉTAPE 3: INSTALLATION DOCKER COMPOSE
# ============================================
echo "🔧 [3/8] Installation de Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    echo "✅ Docker Compose installé"
else
    echo "✅ Docker Compose déjà installé"
fi

# ============================================
# ÉTAPE 4: INSTALLATION FFMPEG
# ============================================
echo "🎥 [4/8] Installation de FFmpeg..."
if ! command -v ffmpeg &> /dev/null; then
    apt install -y ffmpeg
    echo "✅ FFmpeg installé"
else
    echo "✅ FFmpeg déjà installé"
fi

# ============================================
# ÉTAPE 5: INSTALLATION NGINX
# ============================================
echo "🌐 [5/8] Installation de Nginx..."
if ! command -v nginx &> /dev/null; then
    apt install -y nginx
    systemctl enable nginx
    systemctl start nginx
    echo "✅ Nginx installé"
else
    echo "✅ Nginx déjà installé"
fi

# ============================================
# ÉTAPE 6: CLONER LE REPOSITORY
# ============================================
echo "📥 [6/8] Clone du repository..."

# Créer le dossier
mkdir -p /opt/iafactory

# Demander l'URL du repo
read -p "URL du repository Git (ou 'skip' pour passer): " REPO_URL

if [ "$REPO_URL" != "skip" ]; then
    cd /opt/iafactory

    # Supprimer si existe déjà
    if [ -d "rag-dz" ]; then
        echo "⚠️  Le dossier rag-dz existe déjà"
        read -p "Voulez-vous le supprimer et re-cloner? (y/n): " RECLONE
        if [ "$RECLONE" = "y" ]; then
            rm -rf rag-dz
            git clone "$REPO_URL" rag-dz
        fi
    else
        git clone "$REPO_URL" rag-dz
    fi

    echo "✅ Repository cloné"
else
    echo "⏭️  Clone du repository ignoré"
    echo "⚠️  Vous devrez copier manuellement les fichiers dans /opt/iafactory/rag-dz/"
fi

# ============================================
# ÉTAPE 7: CONFIGURATION .ENV
# ============================================
echo "🔑 [7/8] Configuration des variables d'environnement..."

VIDEO_STUDIO_PATH="/opt/iafactory/rag-dz/apps/video-studio"

if [ -d "$VIDEO_STUDIO_PATH" ]; then
    cd "$VIDEO_STUDIO_PATH"

    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            cp .env.example .env
            echo "✅ Fichier .env créé depuis .env.example"
        else
            # Créer un .env minimal
            cat > .env << 'EOF'
# ============================================
# IAFACTORY VIDEO STUDIO - PRODUCTION ENV
# ============================================

# === APIs IA ===
FAL_KEY=REMPLACER_PAR_VOTRE_CLE_FAL
REPLICATE_API_TOKEN=REMPLACER_PAR_VOTRE_TOKEN_REPLICATE
ELEVENLABS_API_KEY=REMPLACER_PAR_VOTRE_CLE_ELEVENLABS

# === Database ===
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/iafactory_video

# === Redis ===
REDIS_URL=redis://redis:6379

# === Auth ===
JWT_SECRET=GENERER_UN_SECRET_FORT_ICI
NEXTAUTH_SECRET=GENERER_UN_AUTRE_SECRET_ICI

# === Storage Cloudflare R2 ===
S3_BUCKET=iafactory-videos
S3_ACCESS_KEY=REMPLACER_PAR_VOTRE_ACCESS_KEY
S3_SECRET_KEY=REMPLACER_PAR_VOTRE_SECRET_KEY
S3_ENDPOINT=https://VOTRE_ACCOUNT.r2.cloudflarestorage.com
S3_REGION=auto

# === Stripe ===
STRIPE_PUBLISHABLE_KEY=REMPLACER_PAR_VOTRE_CLE_PUBLIQUE
STRIPE_SECRET_KEY=REMPLACER_PAR_VOTRE_CLE_SECRETE
STRIPE_WEBHOOK_SECRET=REMPLACER_PAR_VOTRE_WEBHOOK_SECRET

# === Frontend ===
FRONTEND_URL=https://video-studio.iafactory.ch
NEXT_PUBLIC_API_URL=https://api.iafactory.ch

# === Config ===
ENVIRONMENT=production
DEBUG=false
EOF
            echo "✅ Fichier .env créé avec template"
        fi

        echo ""
        echo "⚠️  IMPORTANT: Vous devez éditer le fichier .env avec vos vraies clés!"
        echo "📝 Commande: nano $VIDEO_STUDIO_PATH/.env"
        echo ""
        read -p "Voulez-vous éditer le .env maintenant? (y/n): " EDIT_ENV

        if [ "$EDIT_ENV" = "y" ]; then
            nano .env
        fi
    else
        echo "✅ Fichier .env déjà existant"
    fi
else
    echo "⚠️  Chemin $VIDEO_STUDIO_PATH non trouvé"
    echo "   Vous devrez créer le .env manuellement"
fi

# ============================================
# ÉTAPE 8: LANCEMENT DOCKER
# ============================================
echo "🐳 [8/8] Lancement des containers Docker..."

if [ -d "$VIDEO_STUDIO_PATH" ]; then
    cd "$VIDEO_STUDIO_PATH"

    echo "📦 Build des images Docker..."
    docker-compose build

    echo "🚀 Lancement des services..."
    docker-compose up -d

    echo ""
    echo "⏳ Attente du démarrage des services (30s)..."
    sleep 30

    echo ""
    echo "📊 État des containers:"
    docker-compose ps

    echo ""
    echo "🧪 Test du backend..."
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Backend opérationnel!"
    else
        echo "⚠️  Backend ne répond pas encore (normal si premier démarrage)"
        echo "   Vérifier les logs: docker-compose logs backend"
    fi

    echo ""
    echo "🧪 Test du frontend..."
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        echo "✅ Frontend opérationnel!"
    else
        echo "⚠️  Frontend ne répond pas encore"
        echo "   Vérifier les logs: docker-compose logs frontend"
    fi
else
    echo "⚠️  Impossible de lancer Docker - chemin non trouvé"
fi

# ============================================
# RÉSUMÉ FINAL
# ============================================
echo ""
echo "============================================"
echo "✅ INSTALLATION TERMINÉE!"
echo "============================================"
echo ""
echo "📍 Emplacement: $VIDEO_STUDIO_PATH"
echo ""
echo "🔧 Prochaines étapes:"
echo ""
echo "1. 📝 Éditer le .env avec vos vraies clés:"
echo "   nano $VIDEO_STUDIO_PATH/.env"
echo ""
echo "2. 🔄 Redémarrer les services:"
echo "   cd $VIDEO_STUDIO_PATH"
echo "   docker-compose restart"
echo ""
echo "3. 🌐 Configurer Nginx reverse proxy:"
echo "   nano /etc/nginx/sites-available/video-studio"
echo "   (Voir le fichier DEPLOY_VPS.md pour la config complète)"
echo ""
echo "4. 🔒 Obtenir les certificats SSL:"
echo "   apt install certbot python3-certbot-nginx"
echo "   certbot --nginx -d video-studio.iafactory.ch -d api.iafactory.ch"
echo ""
echo "5. 🧪 Tester l'API:"
echo "   curl http://localhost:8000/health"
echo "   curl http://localhost:8000/docs"
echo ""
echo "📊 Commandes utiles:"
echo "   docker-compose ps              # Voir l'état"
echo "   docker-compose logs -f         # Voir les logs"
echo "   docker-compose restart         # Redémarrer"
echo "   docker-compose down            # Arrêter"
echo "   docker-compose up -d --build   # Rebuild + redémarrer"
echo ""
echo "============================================"
