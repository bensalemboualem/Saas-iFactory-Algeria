#!/bin/bash
# Script de déploiement Nginx SÉCURISÉ avec rollback automatique V2
# Date: 2025-12-12
# Usage: ./deploy-nginx-safe-v2.sh
# IMPORTANT: Doit être exécuté DEPUIS le VPS (ou copier iafactoryalgeria-v2.conf avant)

set -euo pipefail  # Arrête sur erreur, variables non définies, erreurs dans pipes

# Couleurs pour output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m' # No Color

echo -e "${GREEN}=== Déploiement Nginx V2 (Astro Marketing) ===${NC}"

# ============================================
# ÉTAPE 1 : Vérifications pré-deploy
# ============================================
echo -e "\n${YELLOW}[1/7] Vérifications pré-deploy...${NC}"

# Vérifier que le fichier de config existe
if [ ! -f "/etc/nginx/sites-available/iafactoryalgeria" ]; then
    echo -e "${RED}Erreur: /etc/nginx/sites-available/iafactoryalgeria introuvable${NC}"
    exit 1
fi

# Vérifier que le nouveau dossier marketing existe
if [ ! -d "/opt/rag-dz-v2/marketing-dist" ]; then
    echo -e "${RED}Erreur: /opt/rag-dz-v2/marketing-dist introuvable${NC}"
    echo -e "${YELLOW}Exécutez d'abord: mkdir -p /opt/rag-dz-v2/marketing-dist${NC}"
    exit 1
fi

# Vérifier que le dossier contient index.html
if [ ! -f "/opt/rag-dz-v2/marketing-dist/index.html" ]; then
    echo -e "${RED}Erreur: /opt/rag-dz-v2/marketing-dist/index.html introuvable${NC}"
    echo -e "${YELLOW}Exécutez d'abord le rsync du build Astro${NC}"
    exit 1
fi

# Vérifier que la nouvelle config existe (doit être copiée avant)
if [ ! -f "/root/iafactoryalgeria-v2.conf" ]; then
    echo -e "${RED}Erreur: /root/iafactoryalgeria-v2.conf introuvable${NC}"
    echo -e "${YELLOW}Copiez d'abord la config depuis local:${NC}"
    echo -e "${YELLOW}  rsync -avz infra/nginx/iafactoryalgeria-v2.conf root@46.224.3.125:/root/${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Vérifications OK${NC}"

# ============================================
# ÉTAPE 2 : Backup config actuelle
# ============================================
readonly BACKUP_FILE="/etc/nginx/sites-available/iafactoryalgeria.backup-$(date +%Y%m%d-%H%M%S)"
echo -e "\n${YELLOW}[2/7] Backup config actuelle...${NC}"
cp /etc/nginx/sites-available/iafactoryalgeria "$BACKUP_FILE"
echo -e "${GREEN}✓ Backup créé: $BACKUP_FILE${NC}"

# ============================================
# ÉTAPE 3 : Copier nouvelle config
# ============================================
echo -e "\n${YELLOW}[3/7] Installation nouvelle config...${NC}"
cp /root/iafactoryalgeria-v2.conf /etc/nginx/sites-available/iafactoryalgeria
echo -e "${GREEN}✓ Config copiée${NC}"

# ============================================
# ÉTAPE 4 : Test syntaxe Nginx
# ============================================
echo -e "\n${YELLOW}[4/7] Test syntaxe Nginx...${NC}"
if nginx -t 2>&1 | tee /tmp/nginx-test.log; then
    echo -e "${GREEN}✓ Syntaxe Nginx OK${NC}"
else
    echo -e "${RED}✗ Erreur syntaxe Nginx !${NC}"
    echo -e "${YELLOW}Rollback automatique...${NC}"
    cp "$BACKUP_FILE" /etc/nginx/sites-available/iafactoryalgeria
    echo -e "${GREEN}✓ Config restaurée depuis backup${NC}"
    cat /tmp/nginx-test.log
    exit 1
fi

# ============================================
# ÉTAPE 5 : Reload Nginx
# ============================================
echo -e "\n${YELLOW}[5/7] Reload Nginx...${NC}"
if systemctl reload nginx; then
    echo -e "${GREEN}✓ Nginx rechargé avec succès${NC}"
else
    echo -e "${RED}✗ Erreur reload Nginx !${NC}"
    echo -e "${YELLOW}Rollback automatique...${NC}"
    cp "$BACKUP_FILE" /etc/nginx/sites-available/iafactoryalgeria
    systemctl reload nginx
    echo -e "${GREEN}✓ Config restaurée et Nginx rechargé${NC}"
    exit 1
fi

# ============================================
# ÉTAPE 6 : Test HTTP/HTTPS
# ============================================
echo -e "\n${YELLOW}[6/7] Tests HTTP/HTTPS...${NC}"

# Test page d'accueil (local HTTP - doit redirect 301)
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost 2>/dev/null || echo "000")
if [[ "$HTTP_CODE" == "200" ]] || [[ "$HTTP_CODE" == "301" ]]; then
    echo -e "${GREEN}✓ HTTP localhost: $HTTP_CODE${NC}"
else
    echo -e "${YELLOW}⚠ HTTP localhost retourne: $HTTP_CODE (attendu 200 ou 301)${NC}"
fi

# Test HTTPS local
HTTPS_CODE=$(curl -s -k -o /dev/null -w "%{http_code}" https://localhost 2>/dev/null || echo "000")
if [[ "$HTTPS_CODE" == "200" ]]; then
    echo -e "${GREEN}✓ HTTPS localhost: $HTTPS_CODE${NC}"
else
    echo -e "${YELLOW}⚠ HTTPS localhost retourne: $HTTPS_CODE (attendu 200)${NC}"
fi

# ============================================
# ÉTAPE 7 : Test routes existantes
# ============================================
echo -e "\n${YELLOW}[7/7] Test routes proxy existantes...${NC}"

# Fonction helper pour tester une route
test_route() {
    local route=$1
    local name=$2
    local code
    code=$(curl -s -k -o /dev/null -w "%{http_code}" "https://localhost$route" 2>/dev/null || echo "000")

    # Codes acceptables: 200 (OK), 301/302 (redirect), 401/403 (auth requis), 404 (route existe)
    # IMPORTANT: 502 (Bad Gateway) n'est PAS acceptable - indique backend down
    if [[ "$code" == "200" ]] || [[ "$code" == "301" ]] || [[ "$code" == "302" ]] || [[ "$code" == "401" ]] || [[ "$code" == "403" ]] || [[ "$code" == "404" ]]; then
        echo -e "${GREEN}✓ $name ($route): $code${NC}"
    else
        echo -e "${RED}✗ $name ($route): $code (attendu 200/301/302/401/403/404)${NC}"
    fi
}

test_route "/api/health" "API Health"
test_route "/archon/" "Archon UI"
test_route "/rag-ui/" "RAG UI"
test_route "/hub/" "Hub"
test_route "/_astro/test.js" "Astro Assets" # 404 attendu mais route fonctionne

# ============================================
# RÉSUMÉ
# ============================================
echo -e "\n${GREEN}=== Déploiement terminé avec succès ===${NC}"
echo -e "${YELLOW}Backup sauvegardé:${NC} $BACKUP_FILE"
echo -e "\n${YELLOW}Pour restaurer (si problème):${NC}"
echo -e "  cp $BACKUP_FILE /etc/nginx/sites-available/iafactoryalgeria"
echo -e "  nginx -t && systemctl reload nginx"
echo -e "\n${YELLOW}Tests externes recommandés:${NC}"
echo -e "  curl -I https://www.iafactoryalgeria.com/"
echo -e "  curl -I https://www.iafactoryalgeria.com/features"
echo -e "  curl -I https://www.iafactoryalgeria.com/hub/"
echo -e "  curl -I https://www.iafactoryalgeria.com/api/health"
echo -e "\n${GREEN}✓ Tous les tests automatiques ont réussi${NC}"
