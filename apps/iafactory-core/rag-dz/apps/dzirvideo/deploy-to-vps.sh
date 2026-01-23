#!/bin/bash
# Deploy Dzir IA Video v2.1 to VPS (46.224.3.125)
# Usage: ./deploy-to-vps.sh [--build-only | --sync-only | --full]

set -e  # Exit on error

VPS_HOST="root@46.224.3.125"
VPS_PATH="/opt/rag-dz/apps/dzirvideo"
LOCAL_PATH="."

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'  # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Parse arguments
MODE="${1:-full}"

log_info "🚀 Déploiement Dzir IA Video v2.1 vers VPS"
log_info "Mode: $MODE"

# Step 1: Sync files to VPS
if [[ "$MODE" != "build-only" ]]; then
    log_info "📦 Synchronisation des fichiers vers VPS..."

    rsync -avz --progress \
        --exclude 'output/' \
        --exclude 'models/' \
        --exclude 'cache/' \
        --exclude '__pycache__/' \
        --exclude '*.pyc' \
        --exclude '.git/' \
        --exclude 'node_modules/' \
        --exclude '.env' \
        $LOCAL_PATH/ $VPS_HOST:$VPS_PATH/

    log_info "✅ Fichiers synchronisés"
fi

# Step 2: Build Docker image on VPS
if [[ "$MODE" != "sync-only" ]]; then
    log_info "🔨 Build de l'image Docker sur VPS..."

    ssh $VPS_HOST << 'EOF'
cd /opt/rag-dz/apps/dzirvideo

# Pull latest base images
docker compose pull || true

# Build with progress
docker compose build --progress=plain 2>&1 | tee build.log

# Check build success
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo "✅ Build réussi"
else
    echo "❌ Build échoué - voir build.log"
    exit 1
fi
EOF

    log_info "✅ Image Docker buildée"
fi

# Step 3: Deploy (restart containers)
if [[ "$MODE" == "full" ]]; then
    log_info "🔄 Redémarrage des containers..."

    ssh $VPS_HOST << 'EOF'
cd /opt/rag-dz/apps/dzirvideo

# Stop existing containers
docker compose down

# Start new containers
docker compose up -d

# Wait for health check
echo "⏳ Attente du démarrage (30s)..."
sleep 30

# Check health
if curl -f http://localhost:8200/health 2>/dev/null; then
    echo "✅ API Dzir IA Video démarrée et healthy"
    docker ps | grep dzir-ia-video
else
    echo "❌ Health check échoué"
    docker compose logs --tail=50 dzirvideo
    exit 1
fi
EOF

    log_info "✅ Déploiement terminé"
fi

# Final status
log_info ""
log_info "📊 Statut final:"
ssh $VPS_HOST "docker ps | grep dzir-ia-video && echo '---' && curl -s http://localhost:8200/health | jq ."

log_info ""
log_info "🎉 Déploiement réussi!"
log_info "🌐 API disponible sur: https://iafactory.pro/dzirvideo/"
log_info "📝 Logs: ssh $VPS_HOST 'cd $VPS_PATH && docker compose logs -f'"
