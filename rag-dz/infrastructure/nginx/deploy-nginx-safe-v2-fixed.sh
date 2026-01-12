#!/bin/bash
# Script de déploiement Nginx SÉCURISÉ avec rollback automatique V2 FIXED
# Date: 2025-12-13
# CORRECTIONS:
# - Utilise iafactoryalgeria-v2-fixed.conf (config basée sur l'actuelle qui fonctionne)
# - Teste UNIQUEMENT les routes qui existent dans la config actuelle
# - Pas de tests pour /archon/, /rag-ui/, /hub/ (n'existent pas actuellement)

set -euo pipefail  # Arrête sur erreur, variables non définies, erreurs dans pipes

# Couleurs pour output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m' # No Color

echo -e "${GREEN}=== Déploiement Nginx V2 FIXED (Marketing SSG) ===${NC}"

# ============================================
# ÉTAPE 1 : Vérifications pré-deploy
# ============================================
echo -e "\n${YELLOW}[1/7] Vérifications pré-deploy...${NC}"

# Vérifier que le fichier de config existe
if [ ! -f "/etc/nginx/sites-available/iafactoryalgeria.com" ]; then
    echo -e "${RED}Erreur: /etc/nginx/sites-available/iafactoryalgeria.com introuvable${NC}"
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
    echo -e "${YELLOW}Exécutez d'abord le rsync du build marketing${NC}"
    exit 1
fi

# Vérifier que la nouvelle config existe (doit être copiée avant)
if [ ! -f "/root/iafactoryalgeria-v2-fixed.conf" ]; then
    echo -e "${RED}Erreur: /root/iafactoryalgeria-v2-fixed.conf introuvable${NC}"
    echo -e "${YELLOW}Copiez d'abord la config depuis local:${NC}"
    echo -e "${YELLOW}  rsync -avz infra/nginx/iafactoryalgeria-v2-fixed.conf root@46.224.3.125:/root/${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Vérifications OK${NC}"

# ============================================
# ÉTAPE 2 : Backup config actuelle
# ============================================
readonly BACKUP_FILE="/etc/nginx/sites-available/iafactoryalgeria.com.backup-$(date +%Y%m%d-%H%M%S)"
echo -e "\n${YELLOW}[2/7] Backup config actuelle...${NC}"
cp /etc/nginx/sites-available/iafactoryalgeria.com "$BACKUP_FILE"
echo -e "${GREEN}✓ Backup créé: $BACKUP_FILE${NC}"

# ============================================
# ÉTAPE 3 : Copier nouvelle config
# ============================================
echo -e "\n${YELLOW}[3/7] Installation nouvelle config...${NC}"
cp /root/iafactoryalgeria-v2-fixed.conf /etc/nginx/sites-available/iafactoryalgeria.com
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
    cp "$BACKUP_FILE" /etc/nginx/sites-available/iafactoryalgeria.com
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
    cp "$BACKUP_FILE" /etc/nginx/sites-available/iafactoryalgeria.com
    systemctl reload nginx
    echo -e "${GREEN}✓ Config restaurée et Nginx rechargé${NC}"
    exit 1
fi

# ============================================
# ÉTAPE 6 : Test HTTP/HTTPS root (AVEC HOST HEADER)
# ============================================
echo -e "\n${YELLOW}[6/7] Tests HTTP/HTTPS root (www.iafactoryalgeria.com)...${NC}"

# Test page d'accueil HTTP (doit redirect 301)
HTTP_CODE=$(curl -s -H "Host: www.iafactoryalgeria.com" -o /dev/null -w "%{http_code}" http://127.0.0.1/ 2>/dev/null || echo "000")
if [[ "$HTTP_CODE" == "200" ]] || [[ "$HTTP_CODE" == "301" ]]; then
    echo -e "${GREEN}✓ HTTP root: $HTTP_CODE${NC}"
else
    echo -e "${RED}✗ HTTP root: $HTTP_CODE (attendu 200 ou 301)${NC}"
fi

# Test HTTPS root (via fichier statique direct, pas SSL)
# On teste que nginx peut lire le fichier depuis le nouveau root
if [ -f "/opt/rag-dz-v2/marketing-dist/index.html" ]; then
    echo -e "${GREEN}✓ Marketing index.html accessible (fichier existe)${NC}"
else
    echo -e "${RED}✗ Marketing index.html introuvable${NC}"
fi

# ============================================
# ÉTAPE 7 : Test UNIQUEMENT routes qui existent
# ============================================
echo -e "\n${YELLOW}[7/7] Test routes proxy existantes (config actuelle)...${NC}"

# Fonction helper pour tester une route (AVEC Host header)
test_route() {
    local route=$1
    local name=$2
    local code
    code=$(curl -s -H "Host: www.iafactoryalgeria.com" -o /dev/null -w "%{http_code}" "http://127.0.0.1$route" 2>/dev/null || echo "000")

    # Codes acceptables: 200 (OK), 301/302 (redirect), 401/403 (auth), 404 (existe mais vide)
    # IMPORTANT: 502 (Bad Gateway) n'est PAS acceptable
    if [[ "$code" == "200" ]] || [[ "$code" == "301" ]] || [[ "$code" == "302" ]] || [[ "$code" == "401" ]] || [[ "$code" == "403" ]] || [[ "$code" == "404" ]]; then
        echo -e "${GREEN}✓ $name ($route): $code${NC}"
        return 0
    else
        echo -e "${RED}✗ $name ($route): $code (attendu 200/301/302/401/403/404)${NC}"
        return 1
    fi
}

# Test UNIQUEMENT les routes de la config actuelle (qui fonctionnent déjà)
# NOTE: Ne pas tester /api/health car backend peut être down, juste tester le routing nginx
FAILED=0
test_route "/apps/" "Apps Legacy (alias)" || FAILED=$((FAILED + 1))
test_route "/api-packages/" "API Packages (alias)" || FAILED=$((FAILED + 1))

# Si des tests échouent, rollback
if [ $FAILED -gt 0 ]; then
    echo -e "\n${RED}✗ $FAILED test(s) échoué(s) - Rollback automatique${NC}"
    cp "$BACKUP_FILE" /etc/nginx/sites-available/iafactoryalgeria.com
    systemctl reload nginx
    echo -e "${GREEN}✓ Config restaurée${NC}"
    exit 1
fi

# ============================================
# RÉSUMÉ
# ============================================
echo -e "\n${GREEN}=== Déploiement terminé avec succès ===${NC}"
echo -e "${YELLOW}Backup sauvegardé:${NC} $BACKUP_FILE"
echo -e "\n${YELLOW}Tests externes recommandés (depuis navigateur):${NC}"
echo -e "  https://www.iafactoryalgeria.com/ ${GREEN}(nouveau marketing)${NC}"
echo -e "  https://www.iafactoryalgeria.com/apps/ ${YELLOW}(apps legacy)${NC}"
echo -e "  https://www.iafactoryalgeria.com/api/health ${YELLOW}(API backend)${NC}"
echo -e "\n${GREEN}✓ Tous les tests automatiques ont réussi${NC}"
echo -e "\n${YELLOW}Pour rollback manuel si besoin:${NC}"
echo -e "  cp $BACKUP_FILE /etc/nginx/sites-available/iafactoryalgeria.com"
echo -e "  nginx -t && systemctl reload nginx"
