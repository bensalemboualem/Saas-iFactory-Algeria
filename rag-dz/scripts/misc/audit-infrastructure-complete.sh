#!/bin/bash
# ================================================================
# AUDIT COMPLET INFRASTRUCTURE - IAFactory Algeria SaaS Platform
# Audit professionnel de tous les services, agents et applications
# ================================================================

set -e

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# Fichier de sortie
REPORT_FILE="/tmp/iafactory-audit-$(date +%Y%m%d-%H%M%S).txt"

# Fonction pour logger
log() {
    echo -e "$1" | tee -a "$REPORT_FILE"
}

log_section() {
    log ""
    log "================================================================"
    log "$1"
    log "================================================================"
}

log ""
log "╔════════════════════════════════════════════════════════════════╗"
log "║     AUDIT INFRASTRUCTURE - IAFactory Algeria SaaS Platform      ║"
log "║                  Rapport Professionnel Complet                  ║"
log "╚════════════════════════════════════════════════════════════════╝"
log ""
log "Date: $(date '+%Y-%m-%d %H:%M:%S %Z')"
log "Hostname: $(hostname)"
log "Utilisateur: $(whoami)"
log ""

# ================================================================
# 1. INFORMATIONS SYSTÈME
# ================================================================
log_section "1. INFORMATIONS SYSTÈME"

log "${CYAN}[1.1] Système d'exploitation${NC}"
cat /etc/os-release | grep -E "PRETTY_NAME|VERSION" | tee -a "$REPORT_FILE"

log ""
log "${CYAN}[1.2] Ressources système${NC}"
log "CPU:"
lscpu | grep -E "^CPU\(s\)|^Model name|^Thread" | tee -a "$REPORT_FILE"

log ""
log "Mémoire:"
free -h | tee -a "$REPORT_FILE"

log ""
log "Disque:"
df -h / | tee -a "$REPORT_FILE"

log ""
log "${CYAN}[1.3] Uptime et charge${NC}"
uptime | tee -a "$REPORT_FILE"

log ""
log "${CYAN}[1.4] Processus les plus consommateurs${NC}"
ps aux --sort=-%mem | head -10 | tee -a "$REPORT_FILE"

# ================================================================
# 2. DOCKER - ÉTAT DES CONTENEURS
# ================================================================
log_section "2. DOCKER - ÉTAT DES CONTENEURS"

log "${CYAN}[2.1] Version Docker${NC}"
docker --version | tee -a "$REPORT_FILE"
docker-compose --version | tee -a "$REPORT_FILE"

log ""
log "${CYAN}[2.2] Conteneurs en cours d'exécution${NC}"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | tee -a "$REPORT_FILE"

log ""
log "${CYAN}[2.3] Tous les conteneurs (y compris arrêtés)${NC}"
docker ps -a --format "table {{.Names}}\t{{.Status}}" | tee -a "$REPORT_FILE"

log ""
log "${CYAN}[2.4] Utilisation des ressources Docker${NC}"
docker stats --no-stream | tee -a "$REPORT_FILE"

log ""
log "${CYAN}[2.5] Images Docker${NC}"
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | tee -a "$REPORT_FILE"

log ""
log "${CYAN}[2.6] Volumes Docker${NC}"
docker volume ls | tee -a "$REPORT_FILE"

log ""
log "${CYAN}[2.7] Réseaux Docker${NC}"
docker network ls | tee -a "$REPORT_FILE"

# ================================================================
# 3. SERVICES PRINCIPAUX - VÉRIFICATION DÉTAILLÉE
# ================================================================
log_section "3. SERVICES PRINCIPAUX - VÉRIFICATION DÉTAILLÉE"

# Fonction pour vérifier un service
check_service() {
    SERVICE_NAME=$1
    CONTAINER_NAME=$2
    PORT=$3
    URL=$4

    log ""
    log "${MAGENTA}──────────────────────────────────────${NC}"
    log "${CYAN}Service: ${SERVICE_NAME}${NC}"
    log "${MAGENTA}──────────────────────────────────────${NC}"

    # Vérifier conteneur
    if docker ps | grep -q "$CONTAINER_NAME"; then
        HEALTH=$(docker inspect --format='{{.State.Health.Status}}' "$CONTAINER_NAME" 2>/dev/null || echo "no-healthcheck")
        log "${GREEN}✅ Conteneur: Running${NC}"
        log "   Health: $HEALTH"
        log "   Uptime: $(docker inspect --format='{{.State.StartedAt}}' "$CONTAINER_NAME")"
    else
        log "${RED}❌ Conteneur: NOT RUNNING${NC}"
    fi

    # Vérifier port
    if netstat -tlnp 2>/dev/null | grep -q ":$PORT "; then
        log "${GREEN}✅ Port $PORT: En écoute${NC}"
        netstat -tlnp | grep ":$PORT " | tee -a "$REPORT_FILE"
    else
        log "${RED}❌ Port $PORT: NON en écoute${NC}"
    fi

    # Test HTTP
    if [ -n "$URL" ]; then
        HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$URL" 2>/dev/null || echo "000")
        if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "301" ] || [ "$HTTP_CODE" = "302" ]; then
            log "${GREEN}✅ HTTP Test: $HTTP_CODE${NC}"
        else
            log "${RED}❌ HTTP Test: $HTTP_CODE (Failed)${NC}"
        fi
    fi

    # Logs récents (5 dernières lignes)
    if docker ps | grep -q "$CONTAINER_NAME"; then
        log "   Derniers logs:"
        docker logs "$CONTAINER_NAME" --tail 5 2>&1 | sed 's/^/   /' | tee -a "$REPORT_FILE"
    fi
}

# Archon Services
check_service "Archon Server (Backend)" "archon-server" "8181" "http://localhost:8181/health"
check_service "Archon MCP Server" "archon-mcp" "8051" "http://localhost:8051"
check_service "Archon Frontend UI" "archon-ui" "3737" "http://localhost:3737"

# Bolt.diy
if docker ps | grep -q bolt; then
    check_service "Bolt.diy" "bolt" "5173" "http://localhost:5173"
fi

# School OneST (MySQL)
if docker ps | grep -q school; then
    check_service "School OneST" "school" "3306" ""
fi

# RAG Backend
if netstat -tlnp | grep -q ":8000 "; then
    check_service "RAG Backend FastAPI" "rag-backend" "8000" "http://localhost:8000/docs"
fi

# ================================================================
# 4. NGINX - CONFIGURATION ET SANTÉ
# ================================================================
log_section "4. NGINX - CONFIGURATION ET SANTÉ"

log "${CYAN}[4.1] Version et status Nginx${NC}"
nginx -v 2>&1 | tee -a "$REPORT_FILE"
systemctl status nginx --no-pager | head -15 | tee -a "$REPORT_FILE"

log ""
log "${CYAN}[4.2] Test de configuration${NC}"
if nginx -t 2>&1 | tee -a "$REPORT_FILE"; then
    log "${GREEN}✅ Configuration Nginx valide${NC}"
else
    log "${RED}❌ Configuration Nginx INVALIDE${NC}"
fi

log ""
log "${CYAN}[4.3] Sites disponibles${NC}"
ls -la /etc/nginx/sites-available/ | tee -a "$REPORT_FILE"

log ""
log "${CYAN}[4.4] Sites activés${NC}"
ls -la /etc/nginx/sites-enabled/ | tee -a "$REPORT_FILE"

log ""
log "${CYAN}[4.5] Vérification des configurations${NC}"

# Fonction pour analyser une config Nginx
analyze_nginx_config() {
    CONFIG_FILE=$1
    CONFIG_NAME=$(basename "$CONFIG_FILE")

    log ""
    log "${MAGENTA}   Config: ${CONFIG_NAME}${NC}"

    if [ -f "$CONFIG_FILE" ]; then
        # Compter les locations
        LOCATIONS=$(grep -c "location" "$CONFIG_FILE" 2>/dev/null || echo "0")
        log "   • Locations: $LOCATIONS"

        # Extraire server_names
        SERVERS=$(grep "server_name" "$CONFIG_FILE" | sed 's/.*server_name //' | sed 's/;.*//' | tr '\n' ' ')
        log "   • Domains: $SERVERS"

        # Vérifier SSL
        if grep -q "ssl_certificate" "$CONFIG_FILE"; then
            CERT_PATH=$(grep "ssl_certificate " "$CONFIG_FILE" | head -1 | sed 's/.*ssl_certificate //' | sed 's/;.*//' | tr -d ' ')
            if [ -f "$CERT_PATH" ]; then
                CERT_EXPIRY=$(openssl x509 -enddate -noout -in "$CERT_PATH" 2>/dev/null | cut -d= -f2)
                log "${GREEN}   • SSL: Configuré (Expire: $CERT_EXPIRY)${NC}"
            else
                log "${RED}   • SSL: Certificat introuvable${NC}"
            fi
        else
            log "${YELLOW}   • SSL: Non configuré${NC}"
        fi

        # Vérifier proxy_pass
        PROXIES=$(grep -o "proxy_pass.*;" "$CONFIG_FILE" | wc -l)
        log "   • Proxies configurés: $PROXIES"
    else
        log "${RED}   • Fichier non trouvé${NC}"
    fi
}

for config in /etc/nginx/sites-available/*; do
    if [ -f "$config" ] && [ "$(basename "$config")" != "default" ]; then
        analyze_nginx_config "$config"
    fi
done

log ""
log "${CYAN}[4.6] Connexions actives Nginx${NC}"
ss -tn | grep ":80\|:443" | wc -l | xargs -I {} log "   Connexions HTTPS actives: {}"

# ================================================================
# 5. CERTIFICATS SSL
# ================================================================
log_section "5. CERTIFICATS SSL - LET'S ENCRYPT"

log "${CYAN}[5.1] Certificats actifs${NC}"
if command -v certbot > /dev/null; then
    certbot certificates 2>&1 | tee -a "$REPORT_FILE"
else
    log "${RED}❌ Certbot non installé${NC}"
fi

log ""
log "${CYAN}[5.2] Vérification des domaines principaux${NC}"

check_ssl_cert() {
    DOMAIN=$1
    log ""
    log "${MAGENTA}   Domain: ${DOMAIN}${NC}"

    # Vérifier si certificat existe
    CERT_PATH="/etc/letsencrypt/live/$DOMAIN/fullchain.pem"
    if [ -f "$CERT_PATH" ]; then
        EXPIRY=$(openssl x509 -enddate -noout -in "$CERT_PATH" 2>/dev/null | cut -d= -f2)
        DAYS_LEFT=$(( ($(date -d "$EXPIRY" +%s) - $(date +%s)) / 86400 ))

        if [ $DAYS_LEFT -gt 30 ]; then
            log "${GREEN}   ✅ Valide - Expire dans $DAYS_LEFT jours${NC}"
        elif [ $DAYS_LEFT -gt 7 ]; then
            log "${YELLOW}   ⚠️  Expire bientôt - $DAYS_LEFT jours restants${NC}"
        else
            log "${RED}   ❌ URGENT - Expire dans $DAYS_LEFT jours!${NC}"
        fi

        log "   Expiration: $EXPIRY"
    else
        log "${RED}   ❌ Certificat non trouvé${NC}"
    fi
}

check_ssl_cert "iafactoryalgeria.com"
check_ssl_cert "archon.iafactoryalgeria.com"
check_ssl_cert "school.iafactoryalgeria.com"

# ================================================================
# 6. DNS ET RÉSEAU
# ================================================================
log_section "6. DNS ET RÉSEAU"

log "${CYAN}[6.1] Résolution DNS des domaines${NC}"

check_dns() {
    DOMAIN=$1
    log ""
    log "${MAGENTA}   Domain: ${DOMAIN}${NC}"

    if host "$DOMAIN" > /dev/null 2>&1; then
        IP=$(host "$DOMAIN" | grep "has address" | awk '{print $4}')
        log "${GREEN}   ✅ Résolu: $IP${NC}"
    else
        log "${RED}   ❌ Non résolu${NC}"
    fi
}

check_dns "www.iafactoryalgeria.com"
check_dns "archon.iafactoryalgeria.com"
check_dns "school.iafactoryalgeria.com"
check_dns "bolt.iafactoryalgeria.com"

log ""
log "${CYAN}[6.2] Ports ouverts publiquement${NC}"
netstat -tlnp | grep -E ":80 |:443 |:22 " | tee -a "$REPORT_FILE"

log ""
log "${CYAN}[6.3] Firewall (UFW)${NC}"
if command -v ufw > /dev/null; then
    ufw status verbose 2>&1 | tee -a "$REPORT_FILE"
else
    log "   UFW non installé"
fi

# ================================================================
# 7. BASE DE DONNÉES
# ================================================================
log_section "7. BASES DE DONNÉES"

log "${CYAN}[7.1] Supabase (PostgreSQL distant)${NC}"
SUPABASE_URL="https://cxzcmmolfgijhjbevtzi.supabase.co"
if curl -s -o /dev/null -w "%{http_code}" "$SUPABASE_URL" 2>/dev/null | grep -q "200"; then
    log "${GREEN}✅ Supabase accessible${NC}"
    log "   URL: $SUPABASE_URL"
else
    log "${RED}❌ Supabase non accessible${NC}"
fi

log ""
log "${CYAN}[7.2] MySQL (School OneST)${NC}"
if docker ps | grep -q school.*mysql; then
    log "${GREEN}✅ MySQL en cours d'exécution${NC}"
    MYSQL_CONTAINER=$(docker ps --filter "name=school" --format "{{.Names}}" | grep mysql | head -1)
    if [ -n "$MYSQL_CONTAINER" ]; then
        docker exec "$MYSQL_CONTAINER" mysql -uroot -e "SHOW DATABASES;" 2>&1 | tee -a "$REPORT_FILE"
    fi
else
    log "${YELLOW}⚠️  MySQL non trouvé${NC}"
fi

log ""
log "${CYAN}[7.3] Qdrant (Vector DB pour IA Agents)${NC}"
if netstat -tlnp | grep -q ":6333 "; then
    log "${GREEN}✅ Qdrant en écoute sur port 6333${NC}"
    if curl -s http://localhost:6333 > /dev/null 2>&1; then
        log "${GREEN}✅ Qdrant accessible${NC}"
    fi
else
    log "${YELLOW}⚠️  Qdrant non trouvé (normal si agents IA pas encore déployés)${NC}"
fi

# ================================================================
# 8. APPLICATIONS ET AGENTS
# ================================================================
log_section "8. APPLICATIONS ET AGENTS IA"

log "${CYAN}[8.1] Structure des applications${NC}"
APPS_DIR="/opt/iafactory-rag-dz/apps"
if [ -d "$APPS_DIR" ]; then
    APP_COUNT=$(find "$APPS_DIR" -maxdepth 1 -type d | wc -l)
    log "   Applications trouvées: $((APP_COUNT - 1))"  # -1 pour exclure le dossier parent
    log ""
    log "   Liste des apps:"
    ls -1 "$APPS_DIR" | grep -v "^shared" | sed 's/^/   • /' | tee -a "$REPORT_FILE"
else
    log "${YELLOW}⚠️  Dossier apps non trouvé${NC}"
fi

log ""
log "${CYAN}[8.2] Agents IA installés${NC}"
IA_AGENTS_DIR="/opt/iafactory-rag-dz/ia-agents"
if [ -d "$IA_AGENTS_DIR" ]; then
    log "${GREEN}✅ Structure IA-Agents présente${NC}"
    ls -1 "$IA_AGENTS_DIR" | sed 's/^/   • /' | tee -a "$REPORT_FILE"
else
    log "${YELLOW}⚠️  Agents IA non encore déployés (normal)${NC}"
fi

log ""
log "${CYAN}[8.3] Bolt.diy${NC}"
BOLT_DIR=$(find /opt -name "*bolt*" -type d 2>/dev/null | grep -v node_modules | head -1)
if [ -n "$BOLT_DIR" ]; then
    log "${GREEN}✅ Bolt trouvé: $BOLT_DIR${NC}"
    if [ -f "$BOLT_DIR/package.json" ]; then
        BOLT_VERSION=$(grep '"version"' "$BOLT_DIR/package.json" | head -1 | sed 's/.*: "//;s/".*//')
        log "   Version: $BOLT_VERSION"
    fi
else
    log "${YELLOW}⚠️  Bolt.diy non trouvé${NC}"
fi

log ""
log "${CYAN}[8.4] Archon${NC}"
ARCHON_DIR="/opt/iafactory-rag-dz/frontend/archon-ui-stable"
if [ -d "$ARCHON_DIR" ]; then
    log "${GREEN}✅ Archon trouvé: $ARCHON_DIR${NC}"
    if [ -f "$ARCHON_DIR/.env" ]; then
        log "   Configuration .env présente"
        grep -E "VITE_ALLOWED_HOSTS|ARCHON.*PORT" "$ARCHON_DIR/.env" | sed 's/^/   /' | tee -a "$REPORT_FILE"
    fi
else
    log "${YELLOW}⚠️  Archon non trouvé${NC}"
fi

# ================================================================
# 9. LOGS SYSTÈME
# ================================================================
log_section "9. LOGS SYSTÈME - DERNIÈRES ERREURS"

log "${CYAN}[9.1] Erreurs Nginx (10 dernières)${NC}"
tail -n 10 /var/log/nginx/error.log 2>/dev/null | tee -a "$REPORT_FILE" || log "   Logs non accessibles"

log ""
log "${CYAN}[9.2] Erreurs système (journalctl)${NC}"
journalctl -p err -n 10 --no-pager 2>/dev/null | tee -a "$REPORT_FILE" || log "   Logs non accessibles"

log ""
log "${CYAN}[9.3] Docker logs (conteneurs en erreur)${NC}"
for container in $(docker ps -a --filter "status=exited" --format "{{.Names}}"); do
    log "   Container: $container"
    docker logs "$container" --tail 5 2>&1 | sed 's/^/      /' | tee -a "$REPORT_FILE"
done

# ================================================================
# 10. SÉCURITÉ
# ================================================================
log_section "10. SÉCURITÉ"

log "${CYAN}[10.1] Utilisateurs système${NC}"
cat /etc/passwd | grep -E "/bin/bash|/bin/sh" | cut -d: -f1 | tee -a "$REPORT_FILE"

log ""
log "${CYAN}[10.2] Connexions SSH actives${NC}"
who | tee -a "$REPORT_FILE"

log ""
log "${CYAN}[10.3] Dernières connexions${NC}"
last | head -10 | tee -a "$REPORT_FILE"

log ""
log "${CYAN}[10.4] Paquets à mettre à jour${NC}"
apt list --upgradable 2>/dev/null | wc -l | xargs -I {} log "   Mises à jour disponibles: {}"

# ================================================================
# 11. PERFORMANCE
# ================================================================
log_section "11. PERFORMANCE"

log "${CYAN}[11.1] I/O Disk${NC}"
iostat -x 1 2 | tee -a "$REPORT_FILE" 2>/dev/null || log "   iostat non disponible"

log ""
log "${CYAN}[11.2] Top processus CPU${NC}"
ps aux --sort=-%cpu | head -10 | tee -a "$REPORT_FILE"

log ""
log "${CYAN}[11.3] Top processus mémoire${NC}"
ps aux --sort=-%mem | head -10 | tee -a "$REPORT_FILE"

# ================================================================
# 12. RECOMMANDATIONS
# ================================================================
log_section "12. RECOMMANDATIONS ET ACTIONS"

# Analyse et recommandations
ISSUES_FOUND=0

log "${CYAN}[12.1] Analyse automatique${NC}"
log ""

# Vérifier mémoire
MEM_USED=$(free | grep Mem | awk '{print int($3/$2 * 100)}')
if [ $MEM_USED -gt 80 ]; then
    log "${RED}❌ CRITIQUE: Utilisation mémoire élevée ($MEM_USED%)${NC}"
    log "   → Recommandation: Redémarrer services non essentiels ou upgrader RAM"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
elif [ $MEM_USED -gt 60 ]; then
    log "${YELLOW}⚠️  ATTENTION: Utilisation mémoire modérée ($MEM_USED%)${NC}"
    log "   → Recommandation: Surveiller et planifier upgrade RAM"
else
    log "${GREEN}✅ Mémoire: OK ($MEM_USED%)${NC}"
fi

# Vérifier disque
DISK_USED=$(df / | tail -1 | awk '{print int($5)}')
if [ $DISK_USED -gt 85 ]; then
    log "${RED}❌ CRITIQUE: Disque presque plein ($DISK_USED%)${NC}"
    log "   → Recommandation: Nettoyer logs et images Docker"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
elif [ $DISK_USED -gt 70 ]; then
    log "${YELLOW}⚠️  ATTENTION: Espace disque limité ($DISK_USED%)${NC}"
    log "   → Recommandation: Planifier nettoyage"
else
    log "${GREEN}✅ Espace disque: OK ($DISK_USED%)${NC}"
fi

# Vérifier conteneurs arrêtés
STOPPED=$(docker ps -a --filter "status=exited" | wc -l)
if [ $STOPPED -gt 5 ]; then
    log "${YELLOW}⚠️  $STOPPED conteneurs arrêtés${NC}"
    log "   → Recommandation: docker container prune"
fi

# Vérifier certificats SSL
CERTS_EXPIRING=$(certbot certificates 2>/dev/null | grep -c "VALID: [0-9] days" || echo "0")
if [ $CERTS_EXPIRING -gt 0 ]; then
    log "${YELLOW}⚠️  Certificats SSL expirent bientôt${NC}"
    log "   → Recommandation: certbot renew"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

log ""
log "${CYAN}[12.2] Score de santé global${NC}"

TOTAL_CHECKS=10
HEALTH_SCORE=$(( (TOTAL_CHECKS - ISSUES_FOUND) * 10 ))

if [ $HEALTH_SCORE -ge 90 ]; then
    log "${GREEN}✅ EXCELLENT: $HEALTH_SCORE/100${NC}"
elif [ $HEALTH_SCORE -ge 70 ]; then
    log "${YELLOW}⚠️  BON: $HEALTH_SCORE/100${NC}"
else
    log "${RED}❌ ATTENTION REQUISE: $HEALTH_SCORE/100${NC}"
fi

# ================================================================
# RÉSUMÉ FINAL
# ================================================================
log ""
log "╔════════════════════════════════════════════════════════════════╗"
log "║                         RÉSUMÉ FINAL                            ║"
log "╚════════════════════════════════════════════════════════════════╝"
log ""
log "✅ Services opérationnels:"
docker ps --format "   • {{.Names}}" | tee -a "$REPORT_FILE"

log ""
log "📊 Problèmes détectés: $ISSUES_FOUND"

log ""
log "📁 Rapport complet sauvegardé: $REPORT_FILE"
log ""
log "================================================================"
log "Audit terminé: $(date '+%Y-%m-%d %H:%M:%S')"
log "================================================================"
log ""

# Afficher le chemin du rapport
echo ""
echo -e "${GREEN}✅ Rapport d'audit généré:${NC}"
echo -e "${CYAN}$REPORT_FILE${NC}"
echo ""
echo "Pour consulter:"
echo "  cat $REPORT_FILE"
echo "  less $REPORT_FILE"
echo ""
