#!/bin/bash

echo "════════════════════════════════════════"
echo "🔍 DIAGNOSTIC ULTRA-COMPLET IAFACTORY"
echo "════════════════════════════════════════"

VPS="root@46.224.3.125"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

ERRORS=0
WARNINGS=0

check() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ $1${NC}"
    else
        echo -e "${RED}❌ $1${NC}"
        ((ERRORS++))
    fi
}

warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
    ((WARNINGS++))
}

info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1️⃣  VÉRIFICATION BACKEND"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Backend running?
ssh $VPS "docker ps | grep iaf-backend-prod" > /dev/null 2>&1
check "Backend container actif"

# Backend healthy?
HEALTH=$(ssh $VPS "curl -s http://localhost:8180/health | grep -o 'healthy'")
if [ "$HEALTH" = "healthy" ]; then
    check "Backend health OK"
else
    echo -e "${RED}❌ Backend health FAILED${NC}"
    ((ERRORS++))
    info "Redémarrage du backend..."
    ssh $VPS "docker restart iaf-backend-prod"
    sleep 10
fi

# Backend logs errors?
ERROR_COUNT=$(ssh $VPS "docker logs iaf-backend-prod --tail 100 | grep -i 'error\|exception\|failed' | grep -v 'Database error, falling back' | wc -l")
if [ "$ERROR_COUNT" -gt 0 ]; then
    warn "Backend a $ERROR_COUNT erreurs dans les logs"
    ssh $VPS "docker logs iaf-backend-prod --tail 50 | grep -i 'error\|exception' | tail -5"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2️⃣  VÉRIFICATION CLÉS API"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check each provider
PROVIDERS=("openai" "anthropic" "google" "groq" "deepseek" "mistral" "cohere")
for provider in "${PROVIDERS[@]}"; do
    HAS_KEY=$(ssh $VPS "curl -s http://localhost:8180/api/credentials/ | grep -A 3 '\"provider\": \"$provider\"' | grep -o '\"has_key\": true'")
    if [ ! -z "$HAS_KEY" ]; then
        check "Provider $provider configuré"
    else
        echo -e "${RED}❌ Provider $provider NON configuré${NC}"
        ((ERRORS++))
    fi
done

# Check env vars loaded
info "Vérification variables d'environnement dans container..."
for provider in "OPENAI" "ANTHROPIC" "GOOGLE_GENERATIVE"; do
    ENV_CHECK=$(ssh $VPS "docker exec iaf-backend-prod env | grep ${provider}_API_KEY")
    if [ ! -z "$ENV_CHECK" ]; then
        check "Env var ${provider}_API_KEY chargée"
    else
        echo -e "${RED}❌ Env var ${provider}_API_KEY ABSENTE${NC}"
        ((ERRORS++))
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3️⃣  VÉRIFICATION NGINX"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Nginx running?
ssh $VPS "systemctl is-active nginx" > /dev/null 2>&1
check "Nginx actif"

# Nginx config valid?
ssh $VPS "nginx -t" > /dev/null 2>&1
check "Nginx config valide"

# API proxy working?
API_TEST=$(ssh $VPS "curl -s http://localhost/api/health | grep -o 'healthy'")
if [ "$API_TEST" = "healthy" ]; then
    check "Nginx proxy /api/ fonctionne"
else
    echo -e "${RED}❌ Nginx proxy /api/ FAILED${NC}"
    ((ERRORS++))
fi

# Landing page accessible?
LANDING_CODE=$(ssh $VPS "curl -s -o /dev/null -w '%{http_code}' http://localhost/landing/")
if [ "$LANDING_CODE" = "200" ]; then
    check "Landing page accessible (HTTP $LANDING_CODE)"
else
    echo -e "${RED}❌ Landing page erreur HTTP $LANDING_CODE${NC}"
    ((ERRORS++))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4️⃣  VÉRIFICATION FICHIERS LANDING"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# index.html exists and correct size?
FILE_SIZE=$(ssh $VPS "stat -c%s /opt/iafactory-rag-dz/apps/landing/index.html")
if [ "$FILE_SIZE" -gt 200000 ]; then
    check "index.html taille correcte ($FILE_SIZE bytes)"
else
    echo -e "${RED}❌ index.html trop petit ($FILE_SIZE bytes)${NC}"
    ((ERRORS++))
fi

# Check JavaScript syntax
info "Vérification syntaxe JavaScript..."
JS_ERRORS=$(ssh $VPS "cat /opt/iafactory-rag-dz/apps/landing/index.html | grep -o 'function\|const\|let\|var' | wc -l")
if [ "$JS_ERRORS" -gt 50 ]; then
    check "JavaScript présent ($JS_ERRORS déclarations)"
else
    warn "Peu de JavaScript trouvé ($JS_ERRORS déclarations)"
fi

# Check for providerModels
HAS_MODELS=$(ssh $VPS "grep -c 'providerModels' /opt/iafactory-rag-dz/apps/landing/index.html")
if [ "$HAS_MODELS" -gt 0 ]; then
    check "providerModels défini dans index.html"
else
    echo -e "${RED}❌ providerModels ABSENT de index.html${NC}"
    ((ERRORS++))
fi

# Check for DOMContentLoaded
HAS_DOM=$(ssh $VPS "grep -c 'DOMContentLoaded' /opt/iafactory-rag-dz/apps/landing/index.html")
if [ "$HAS_DOM" -gt 0 ]; then
    check "DOMContentLoaded présent"
else
    echo -e "${RED}❌ DOMContentLoaded ABSENT${NC}"
    ((ERRORS++))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5️⃣  VÉRIFICATION ENDPOINTS API"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Test each endpoint
ENDPOINTS=(
    "/api/health"
    "/api/credentials/"
    "/api/agent-chat/sessions"
    "/api/bmad"
    "/api/query"
)

for endpoint in "${ENDPOINTS[@]}"; do
    if [[ "$endpoint" == *"sessions"* ]]; then
        RESPONSE=$(ssh $VPS "curl -s -X POST http://localhost:8180$endpoint -H 'Content-Type: application/json' -d '{\"title\":\"test\"}' -w '%{http_code}' -o /dev/null")
    else
        RESPONSE=$(ssh $VPS "curl -s -o /dev/null -w '%{http_code}' http://localhost:8180$endpoint")
    fi

    if [ "$RESPONSE" = "200" ] || [ "$RESPONSE" = "201" ]; then
        check "Endpoint $endpoint (HTTP $RESPONSE)"
    else
        echo -e "${RED}❌ Endpoint $endpoint FAILED (HTTP $RESPONSE)${NC}"
        ((ERRORS++))
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "6️⃣  VÉRIFICATION CORS & HEADERS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check CORS headers
CORS_HEADER=$(ssh $VPS "curl -s -I http://localhost:8180/api/health | grep -i 'access-control-allow'")
if [ ! -z "$CORS_HEADER" ]; then
    check "Headers CORS présents"
else
    warn "Headers CORS absents"
fi

# Check Cache-Control
CACHE_HEADER=$(ssh $VPS "curl -s -I http://localhost/landing/ | grep -i 'cache-control'")
if [ ! -z "$CACHE_HEADER" ]; then
    info "Cache headers: $CACHE_HEADER"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "7️⃣  VÉRIFICATION PERMISSIONS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check file permissions
PERMS=$(ssh $VPS "stat -c '%a' /opt/iafactory-rag-dz/apps/landing/index.html")
if [ "$PERMS" = "755" ] || [ "$PERMS" = "644" ]; then
    check "Permissions fichiers OK ($PERMS)"
else
    warn "Permissions inhabituelles: $PERMS"
    info "Correction des permissions..."
    ssh $VPS "chmod 644 /opt/iafactory-rag-dz/apps/landing/index.html"
fi

# Check ownership
OWNER=$(ssh $VPS "stat -c '%U:%G' /opt/iafactory-rag-dz/apps/landing/index.html")
info "Propriétaire: $OWNER"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "8️⃣  TEST DEPUIS INTERNET"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Test public URL
PUBLIC_CODE=$(curl -s -o /dev/null -w '%{http_code}' https://www.iafactoryalgeria.com/landing/)
if [ "$PUBLIC_CODE" = "200" ]; then
    check "Landing publique accessible (HTTP $PUBLIC_CODE)"
else
    echo -e "${RED}❌ Landing publique erreur HTTP $PUBLIC_CODE${NC}"
    ((ERRORS++))
fi

# Test API publique
PUBLIC_API=$(curl -s https://www.iafactoryalgeria.com/api/health | grep -o 'healthy')
if [ "$PUBLIC_API" = "healthy" ]; then
    check "API publique accessible"
else
    echo -e "${RED}❌ API publique FAILED${NC}"
    ((ERRORS++))
fi

# Count providers via public API
PUBLIC_PROVIDERS=$(curl -s https://www.iafactoryalgeria.com/api/credentials/ | grep -c '"has_key": true')
info "Providers visibles via API publique: $PUBLIC_PROVIDERS/7"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "9️⃣  VÉRIFICATION JAVASCRIPT CONSOLE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check for console.log statements
CONSOLE_LOGS=$(ssh $VPS "grep -c 'console.log' /opt/iafactory-rag-dz/apps/landing/index.html")
info "Statements console.log trouvés: $CONSOLE_LOGS"

# Check for error handlers
ERROR_HANDLERS=$(ssh $VPS "grep -c 'catch\|error' /opt/iafactory-rag-dz/apps/landing/index.html")
info "Gestionnaires d'erreur trouvés: $ERROR_HANDLERS"

echo ""
echo "════════════════════════════════════════"
echo "📊 RÉSUMÉ"
echo "════════════════════════════════════════"
echo -e "${RED}Erreurs: $ERRORS${NC}"
echo -e "${YELLOW}Avertissements: $WARNINGS${NC}"

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ SYSTÈME OK - AUCUNE ERREUR CRITIQUE${NC}"
    exit 0
else
    echo -e "${RED}❌ ERREURS DÉTECTÉES - CORRECTION NÉCESSAIRE${NC}"
    exit 1
fi
