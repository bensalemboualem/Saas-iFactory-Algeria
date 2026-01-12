#!/bin/bash

# ============================================
# 🧪 SCRIPT DE TEST APRÈS DÉPLOIEMENT
# IAFactory Video Studio Pro
# ============================================

echo "🧪 Test de l'installation Video Studio Pro..."
echo ""

FAILED=0

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction de test
test_check() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ $1${NC}"
    else
        echo -e "${RED}❌ $1${NC}"
        FAILED=$((FAILED + 1))
    fi
}

# ============================================
# TESTS SYSTEME
# ============================================
echo "🔧 Tests système..."

docker --version > /dev/null 2>&1
test_check "Docker installé"

docker-compose --version > /dev/null 2>&1
test_check "Docker Compose installé"

nginx -v > /dev/null 2>&1
test_check "Nginx installé"

ffmpeg -version > /dev/null 2>&1
test_check "FFmpeg installé"

echo ""

# ============================================
# TESTS CONTAINERS
# ============================================
echo "🐳 Tests containers Docker..."

docker ps | grep -q video-studio-backend
test_check "Container backend en cours"

docker ps | grep -q video-studio-frontend
test_check "Container frontend en cours"

docker ps | grep -q video-studio-db
test_check "Container PostgreSQL en cours"

docker ps | grep -q video-studio-redis
test_check "Container Redis en cours"

echo ""

# ============================================
# TESTS SERVICES
# ============================================
echo "🌐 Tests des services..."

# Test Backend Health
BACKEND_HEALTH=$(curl -s http://localhost:8000/health)
if echo "$BACKEND_HEALTH" | grep -q "healthy"; then
    echo -e "${GREEN}✅ Backend API répond (health check OK)${NC}"
else
    echo -e "${RED}❌ Backend API ne répond pas${NC}"
    FAILED=$((FAILED + 1))
fi

# Test Backend Docs
curl -s http://localhost:8000/docs | grep -q "Swagger" > /dev/null 2>&1
test_check "Documentation API accessible (/docs)"

# Test Frontend
curl -s http://localhost:3000 > /dev/null 2>&1
test_check "Frontend Next.js répond"

# Test PostgreSQL
docker exec video-studio-db-1 pg_isready -U postgres > /dev/null 2>&1
test_check "PostgreSQL opérationnel"

# Test Redis
docker exec video-studio-redis-1 redis-cli ping | grep -q "PONG" > /dev/null 2>&1
test_check "Redis opérationnel"

echo ""

# ============================================
# TESTS CONFIGURATION
# ============================================
echo "⚙️  Tests configuration..."

# Vérifier que .env existe
if [ -f "/opt/iafactory/rag-dz/apps/video-studio/.env" ]; then
    echo -e "${GREEN}✅ Fichier .env existe${NC}"

    # Vérifier que les clés sont configurées
    ENV_FILE="/opt/iafactory/rag-dz/apps/video-studio/.env"

    if grep -q "REMPLACER" "$ENV_FILE"; then
        echo -e "${YELLOW}⚠️  Certaines clés API ne sont pas configurées${NC}"
        echo "   Éditer: nano $ENV_FILE"
        FAILED=$((FAILED + 1))
    else
        echo -e "${GREEN}✅ Clés API configurées${NC}"
    fi

    if grep -q "GENERER" "$ENV_FILE"; then
        echo -e "${YELLOW}⚠️  Les secrets JWT ne sont pas générés${NC}"
        echo "   Générer avec: openssl rand -base64 32"
        FAILED=$((FAILED + 1))
    else
        echo -e "${GREEN}✅ Secrets JWT configurés${NC}"
    fi
else
    echo -e "${RED}❌ Fichier .env manquant${NC}"
    FAILED=$((FAILED + 1))
fi

echo ""

# ============================================
# TESTS NGINX
# ============================================
echo "🌐 Tests Nginx..."

systemctl is-active --quiet nginx
test_check "Nginx en cours d'exécution"

nginx -t > /dev/null 2>&1
test_check "Configuration Nginx valide"

if [ -f "/etc/nginx/sites-enabled/video-studio" ]; then
    echo -e "${GREEN}✅ Configuration video-studio active${NC}"
else
    echo -e "${YELLOW}⚠️  Configuration Nginx pas encore activée${NC}"
    echo "   Lancer: ./setup-nginx.sh"
fi

echo ""

# ============================================
# TESTS RÉSEAU
# ============================================
echo "🌍 Tests réseau..."

# Vérifier l'IP publique
PUBLIC_IP=$(curl -s ifconfig.me)
echo "📍 IP publique du serveur: $PUBLIC_IP"

# Vérifier les ports ouverts
ss -tuln | grep -q ":80 " && echo -e "${GREEN}✅ Port 80 (HTTP) ouvert${NC}" || echo -e "${YELLOW}⚠️  Port 80 fermé${NC}"
ss -tuln | grep -q ":443 " && echo -e "${GREEN}✅ Port 443 (HTTPS) ouvert${NC}" || echo -e "${YELLOW}⚠️  Port 443 fermé${NC}"
ss -tuln | grep -q ":3000 " && echo -e "${GREEN}✅ Port 3000 (Frontend) ouvert${NC}" || echo -e "${RED}❌ Port 3000 fermé${NC}"
ss -tuln | grep -q ":8000 " && echo -e "${GREEN}✅ Port 8000 (Backend) ouvert${NC}" || echo -e "${RED}❌ Port 8000 fermé${NC}"

echo ""

# ============================================
# TESTS LOGS
# ============================================
echo "📊 Vérification des logs récents..."

# Logs Backend
BACKEND_ERRORS=$(docker logs video-studio-backend-1 2>&1 | grep -i "error" | tail -5)
if [ -z "$BACKEND_ERRORS" ]; then
    echo -e "${GREEN}✅ Aucune erreur dans les logs backend${NC}"
else
    echo -e "${YELLOW}⚠️  Erreurs détectées dans backend:${NC}"
    echo "$BACKEND_ERRORS"
fi

# Logs Frontend
FRONTEND_ERRORS=$(docker logs video-studio-frontend-1 2>&1 | grep -i "error" | tail -5)
if [ -z "$FRONTEND_ERRORS" ]; then
    echo -e "${GREEN}✅ Aucune erreur dans les logs frontend${NC}"
else
    echo -e "${YELLOW}⚠️  Erreurs détectées dans frontend:${NC}"
    echo "$FRONTEND_ERRORS"
fi

echo ""

# ============================================
# TESTS SSL
# ============================================
echo "🔒 Tests SSL..."

# Vérifier si Certbot est installé
if command -v certbot &> /dev/null; then
    echo -e "${GREEN}✅ Certbot installé${NC}"

    # Lister les certificats
    CERTS=$(certbot certificates 2>&1 | grep "Certificate Name" | wc -l)
    if [ "$CERTS" -gt 0 ]; then
        echo -e "${GREEN}✅ $CERTS certificat(s) SSL configuré(s)${NC}"
    else
        echo -e "${YELLOW}⚠️  Aucun certificat SSL configuré${NC}"
        echo "   Lancer: ./setup-nginx.sh"
    fi
else
    echo -e "${YELLOW}⚠️  Certbot pas installé${NC}"
fi

echo ""

# ============================================
# RÉSUMÉ
# ============================================
echo "============================================"
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ TOUS LES TESTS PASSENT!${NC}"
    echo ""
    echo "🎉 Votre installation est opérationnelle!"
    echo ""
    echo "🌐 Prochaines étapes:"
    echo "   1. Configurer Nginx: ./setup-nginx.sh"
    echo "   2. Tester l'API: curl http://localhost:8000/docs"
    echo "   3. Accéder au frontend: http://localhost:3000"
else
    echo -e "${RED}❌ $FAILED TEST(S) EN ÉCHEC${NC}"
    echo ""
    echo "🔧 Actions recommandées:"

    if docker ps | grep -q video-studio; then
        echo "   ✅ Les containers tournent"
    else
        echo "   ❌ Démarrer les containers: cd /opt/iafactory/rag-dz/apps/video-studio && docker-compose up -d"
    fi

    if [ -f "/opt/iafactory/rag-dz/apps/video-studio/.env" ]; then
        if grep -q "REMPLACER\|GENERER" "/opt/iafactory/rag-dz/apps/video-studio/.env"; then
            echo "   ❌ Configurer le .env: nano /opt/iafactory/rag-dz/apps/video-studio/.env"
        fi
    else
        echo "   ❌ Créer le .env: cd /opt/iafactory/rag-dz/apps/video-studio && cp .env.production .env"
    fi

    echo ""
    echo "📖 Voir les logs:"
    echo "   docker-compose logs -f"
fi
echo "============================================"
echo ""

# Afficher les URL utiles
echo "📚 URLs utiles:"
echo "   Backend Health: http://localhost:8000/health"
echo "   API Docs: http://localhost:8000/docs"
echo "   Frontend: http://localhost:3000"
echo ""
echo "📊 Commandes utiles:"
echo "   docker-compose ps                # État des containers"
echo "   docker-compose logs -f           # Voir les logs"
echo "   docker-compose restart backend   # Redémarrer un service"
echo "   ./test-deploy.sh                 # Re-lancer ce test"
echo ""

exit $FAILED
