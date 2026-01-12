#!/bin/bash
# Déploiement rapide direct
set -e

VPS_IP="46.224.3.125"
DOMAIN="www.iafactoryalgeria.com"
EMAIL="admin@iafactoryalgeria.com"

echo "================================================================================"
echo "🚀 DÉPLOIEMENT IAFactory RAG-DZ"
echo "================================================================================"
echo "VPS: ${VPS_IP}"
echo "Domaine: ${DOMAIN}"
echo "================================================================================"
echo ""

echo "[1/4] Copie du projet sur le VPS..."
rsync -avz --progress \
    --exclude 'node_modules' \
    --exclude '.git' \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    --exclude '.env.local' \
    --exclude 'dist' \
    --exclude 'build' \
    ./ root@${VPS_IP}:/opt/iafactory-rag-dz/

echo ""
echo "[2/4] Création du fichier .env..."
ssh root@${VPS_IP} "cd /opt/iafactory-rag-dz && cat > .env << 'ENVEOF'
SOVEREIGNTY_REGION=DZ
SOVEREIGNTY_LABEL=Algérie
TZ=Africa/Algiers
POSTGRES_USER=postgres
POSTGRES_PASSWORD=\$(openssl rand -base64 32)
POSTGRES_DB=iafactory_dz
DATABASE_URL=postgresql://postgres:\$(openssl rand -base64 32)@iafactory-postgres:5432/iafactory_dz
REDIS_URL=redis://iafactory-redis:6379/0
QDRANT_URL=http://iafactory-qdrant:6333
SECRET_KEY=\$(openssl rand -base64 64)
JWT_SECRET=\$(openssl rand -base64 64)
PORT=8180
HOST=0.0.0.0
ENVIRONMENT=production
DEBUG=false
DOMAIN=${DOMAIN}
ENVEOF
"

echo ""
echo "[3/4] Lancement du script de déploiement sur VPS..."
ssh root@${VPS_IP} "cd /opt/iafactory-rag-dz && chmod +x deploy-vps-master.sh && export DOMAIN='${DOMAIN}' && export EMAIL='${EMAIL}' && ./deploy-vps-master.sh"

echo ""
echo "[4/4] Vérifications finales..."
sleep 10

echo ""
echo "================================================================================"
echo "✅ DÉPLOIEMENT TERMINÉ !"
echo "================================================================================"
echo ""
echo "🌐 Site: https://${DOMAIN}"
echo "📡 API: http://${VPS_IP}:8180/health"
echo ""
echo "================================================================================"
