#!/bin/bash
# ============================================================
# AUDIT COMPLET IA FACTORY ALGERIA - ZÉRO TOLÉRANCE
# Script de vérification exhaustif avant production
# ============================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PASS=0
FAIL=0
WARN=0

log_pass() { echo -e "${GREEN}✅ PASS${NC}: $1"; ((PASS++)); }
log_fail() { echo -e "${RED}❌ FAIL${NC}: $1"; ((FAIL++)); }
log_warn() { echo -e "${YELLOW}⚠️  WARN${NC}: $1"; ((WARN++)); }
log_info() { echo -e "${BLUE}ℹ️  INFO${NC}: $1"; }
log_section() { echo -e "\n${BLUE}═══════════════════════════════════════════════════════════${NC}"; echo -e "${BLUE}  $1${NC}"; echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}\n"; }

PROJECT_ROOT="d:/IAFactory/rag-dz"
cd "$PROJECT_ROOT"

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     AUDIT COMPLET IA FACTORY ALGERIA - ZÉRO TOLÉRANCE         ║"
echo "║                    $(date '+%Y-%m-%d %H:%M:%S')                       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# ============================================================
# SECTION 1: SÉCURITÉ CRITIQUE
# ============================================================
log_section "1. SÉCURITÉ CRITIQUE"

# 1.1 Clés API hardcodées dans le frontend
log_info "Vérification des clés API hardcodées..."
HARDCODED_KEYS=$(grep -rn "test-api-key-123\|test-api-key\|api-key-123" frontend/ --include="*.tsx" --include="*.ts" --include="*.js" 2>/dev/null | grep -v node_modules | grep -v ".next" || true)
if [ -z "$HARDCODED_KEYS" ]; then
    log_pass "Aucune clé API hardcodée dans le frontend"
else
    log_fail "Clés API hardcodées trouvées:"
    echo "$HARDCODED_KEYS"
fi

# 1.2 Tenant IDs hardcodés
log_info "Vérification des Tenant IDs hardcodés..."
HARDCODED_TENANTS=$(grep -rn "00000000-0000-0000-0000-000000000001" frontend/ --include="*.tsx" --include="*.ts" 2>/dev/null | grep -v node_modules || true)
if [ -z "$HARDCODED_TENANTS" ]; then
    log_pass "Aucun Tenant ID de test hardcodé"
else
    log_fail "Tenant IDs hardcodés trouvés:"
    echo "$HARDCODED_TENANTS"
fi

# 1.3 Fichiers .env exposés
log_info "Vérification des fichiers .env..."
if [ -f "services/api/.env" ]; then
    # Vérifier qu'il n'y a pas de secrets en clair évidents
    if grep -q "test-api-key-123\|password123\|secret123" "services/api/.env" 2>/dev/null; then
        log_fail ".env contient des secrets de test faibles"
    else
        log_pass ".env ne contient pas de secrets de test évidents"
    fi
else
    log_warn "Fichier .env non trouvé"
fi

# 1.4 Vérifier que .env n'est pas dans git
if git ls-files --error-unmatch "services/api/.env" 2>/dev/null; then
    log_fail ".env est suivi par git!"
else
    log_pass ".env n'est pas suivi par git"
fi

# 1.5 Vérifier .gitignore
if grep -q "\.env" ".gitignore" 2>/dev/null; then
    log_pass ".gitignore exclut les fichiers .env"
else
    log_warn ".gitignore ne mentionne pas .env"
fi

# 1.6 Secrets dans le code
log_info "Recherche de secrets potentiels..."
SECRETS=$(grep -rn "password\s*=\s*['\"][^'\"]*['\"]" services/ --include="*.py" 2>/dev/null | grep -v "password:" | grep -v "# " | head -5 || true)
if [ -z "$SECRETS" ]; then
    log_pass "Pas de mots de passe hardcodés détectés"
else
    log_warn "Mots de passe potentiellement hardcodés:"
    echo "$SECRETS"
fi

# ============================================================
# SECTION 2: BASE DE DONNÉES
# ============================================================
log_section "2. BASE DE DONNÉES"

# 2.1 Connexion PostgreSQL
log_info "Test de connexion PostgreSQL..."
if docker exec iaf-dz-postgres-local pg_isready -U postgres -d iafactory_dz >/dev/null 2>&1; then
    log_pass "PostgreSQL répond"
else
    log_fail "PostgreSQL ne répond pas"
fi

# 2.2 Tables requises
log_info "Vérification des tables..."
REQUIRED_TABLES=("tenants" "user_credits" "billing_tenants" "subscription_plans" "service_pricing" "credit_transactions" "api_keys" "app_catalog" "agent_catalog")
for table in "${REQUIRED_TABLES[@]}"; do
    if docker exec iaf-dz-postgres-local psql -U postgres -d iafactory_dz -tAc "SELECT 1 FROM pg_tables WHERE tablename='$table'" 2>/dev/null | grep -q 1; then
        log_pass "Table '$table' existe"
    else
        log_fail "Table '$table' MANQUANTE"
    fi
done

# 2.3 Données seed
log_info "Vérification des données seed..."
TENANT_COUNT=$(docker exec iaf-dz-postgres-local psql -U postgres -d iafactory_dz -tAc "SELECT COUNT(*) FROM tenants" 2>/dev/null || echo "0")
if [ "$TENANT_COUNT" -gt 0 ]; then
    log_pass "Table tenants: $TENANT_COUNT enregistrement(s)"
else
    log_fail "Table tenants VIDE"
fi

CREDITS_COUNT=$(docker exec iaf-dz-postgres-local psql -U postgres -d iafactory_dz -tAc "SELECT COUNT(*) FROM user_credits" 2>/dev/null || echo "0")
if [ "$CREDITS_COUNT" -gt 0 ]; then
    log_pass "Table user_credits: $CREDITS_COUNT enregistrement(s)"
else
    log_fail "Table user_credits VIDE"
fi

BILLING_COUNT=$(docker exec iaf-dz-postgres-local psql -U postgres -d iafactory_dz -tAc "SELECT COUNT(*) FROM billing_tenants" 2>/dev/null || echo "0")
if [ "$BILLING_COUNT" -gt 0 ]; then
    log_pass "Table billing_tenants: $BILLING_COUNT enregistrement(s)"
else
    log_fail "Table billing_tenants VIDE"
fi

# 2.4 Plans de subscription
PLANS_COUNT=$(docker exec iaf-dz-postgres-local psql -U postgres -d iafactory_dz -tAc "SELECT COUNT(*) FROM subscription_plans" 2>/dev/null || echo "0")
if [ "$PLANS_COUNT" -ge 4 ]; then
    log_pass "subscription_plans: $PLANS_COUNT plans configurés"
else
    log_warn "subscription_plans: seulement $PLANS_COUNT plans (attendu: 4+)"
fi

# 2.5 Catalog apps
APPS_COUNT=$(docker exec iaf-dz-postgres-local psql -U postgres -d iafactory_dz -tAc "SELECT COUNT(*) FROM app_catalog WHERE is_published=true" 2>/dev/null || echo "0")
if [ "$APPS_COUNT" -gt 0 ]; then
    log_pass "app_catalog: $APPS_COUNT apps publiées"
else
    log_warn "app_catalog: aucune app publiée"
fi

# ============================================================
# SECTION 3: CONFIGURATION
# ============================================================
log_section "3. CONFIGURATION"

# 3.1 DATABASE_URL unique
log_info "Vérification DATABASE_URL..."
DB_URL_COUNT=$(grep -c "DATABASE_URL" services/api/.env 2>/dev/null || echo "0")
if [ "$DB_URL_COUNT" -eq 1 ]; then
    log_pass "Un seul DATABASE_URL dans .env"
else
    log_fail "DATABASE_URL dupliqué ou manquant ($DB_URL_COUNT occurrences)"
fi

# 3.2 Port cohérent
log_info "Vérification cohérence des ports..."
PORT_8002=$(grep -rn "localhost:8002\|:8002" frontend/ia-factory-ui --include="*.ts" --include="*.tsx" --include="*.js" 2>/dev/null | grep -v node_modules | wc -l || echo "0")
PORT_8000=$(grep -rn "localhost:8000\|:8000" frontend/ia-factory-ui --include="*.ts" --include="*.tsx" --include="*.js" 2>/dev/null | grep -v node_modules | wc -l || echo "0")
if [ "$PORT_8002" -eq 0 ]; then
    log_pass "Pas de référence au port 8002 (obsolète)"
else
    log_warn "$PORT_8002 références au port 8002 trouvées"
fi

# 3.3 Variables d'environnement requises
log_info "Vérification variables d'environnement..."
REQUIRED_VARS=("DATABASE_URL" "JWT_SECRET_KEY" "GROQ_API_KEY" "CHARGILY_API_KEY")
for var in "${REQUIRED_VARS[@]}"; do
    if grep -q "^$var=" services/api/.env 2>/dev/null; then
        log_pass "Variable $var définie"
    else
        log_fail "Variable $var MANQUANTE"
    fi
done

# ============================================================
# SECTION 4: FICHIERS CRITIQUES
# ============================================================
log_section "4. FICHIERS CRITIQUES"

# 4.1 Fichiers backend
CRITICAL_FILES=(
    "services/api/app/main.py"
    "services/api/app/routers/credits.py"
    "services/api/app/routers/payment.py"
    "services/api/app/routers/catalog.py"
    "apps/video-studio/backend/services/credits_proxy.py"
)
for file in "${CRITICAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        log_pass "Fichier $file existe"
    else
        log_fail "Fichier $file MANQUANT"
    fi
done

# 4.2 Fichiers frontend
FRONTEND_FILES=(
    "frontend/ia-factory-ui/app/pricing/page.tsx"
    "frontend/ia-factory-ui/app/apps/page.tsx"
    "frontend/ia-factory-ui/app/checkout/page.tsx"
    "frontend/ia-factory-ui/components/CreditBalance.tsx"
)
for file in "${FRONTEND_FILES[@]}"; do
    if [ -f "$file" ]; then
        log_pass "Fichier $file existe"
    else
        log_fail "Fichier $file MANQUANT"
    fi
done

# ============================================================
# SECTION 5: IMPORTS ET DÉPENDANCES
# ============================================================
log_section "5. IMPORTS ET DÉPENDANCES"

# 5.1 Vérifier les imports dans main.py
log_info "Vérification imports API..."
if grep -q "from .routers import.*catalog" services/api/app/main.py 2>/dev/null; then
    log_pass "Router catalog importé dans main.py"
else
    log_fail "Router catalog NON importé dans main.py"
fi

if grep -q "from .routers import.*credits" services/api/app/main.py 2>/dev/null; then
    log_pass "Router credits importé dans main.py"
else
    log_fail "Router credits NON importé dans main.py"
fi

# 5.2 Vérifier __init__.py
if grep -q "catalog" services/api/app/routers/__init__.py 2>/dev/null; then
    log_pass "catalog dans __init__.py des routers"
else
    log_fail "catalog ABSENT de __init__.py"
fi

# ============================================================
# SECTION 6: WEBHOOK CHARGILY
# ============================================================
log_section "6. WEBHOOK CHARGILY"

# 6.1 Vérifier la correction du webhook
log_info "Vérification webhook payment.py..."
if grep -q "billing_tenants" services/api/app/routers/payment.py 2>/dev/null; then
    if grep -q "ON CONFLICT (tenant_id)" services/api/app/routers/payment.py 2>/dev/null; then
        log_pass "Webhook utilise UPSERT pour billing_tenants"
    else
        log_warn "Webhook référence billing_tenants mais sans UPSERT"
    fi
else
    log_fail "Webhook ne met pas à jour billing_tenants"
fi

if grep -q "user_credits" services/api/app/routers/payment.py 2>/dev/null; then
    log_pass "Webhook met à jour user_credits"
else
    log_fail "Webhook ne met pas à jour user_credits"
fi

# ============================================================
# SECTION 7: DOCKER ET SERVICES
# ============================================================
log_section "7. DOCKER ET SERVICES"

# 7.1 Conteneurs en cours d'exécution
log_info "Vérification conteneurs Docker..."
POSTGRES_RUNNING=$(docker ps --filter "name=postgres" --filter "status=running" -q 2>/dev/null | wc -l)
if [ "$POSTGRES_RUNNING" -gt 0 ]; then
    log_pass "PostgreSQL en cours d'exécution"
else
    log_fail "PostgreSQL NON en cours d'exécution"
fi

REDIS_RUNNING=$(docker ps --filter "name=redis" --filter "status=running" -q 2>/dev/null | wc -l)
if [ "$REDIS_RUNNING" -gt 0 ]; then
    log_pass "Redis en cours d'exécution"
else
    log_warn "Redis non détecté (optionnel)"
fi

# ============================================================
# SECTION 8: SYNTAXE ET TYPES
# ============================================================
log_section "8. SYNTAXE ET TYPES"

# 8.1 Erreurs Python évidentes
log_info "Vérification syntaxe Python..."
PYTHON_ERRORS=$(python -m py_compile services/api/app/main.py 2>&1 || true)
if [ -z "$PYTHON_ERRORS" ]; then
    log_pass "main.py: syntaxe Python valide"
else
    log_fail "main.py: erreurs de syntaxe"
    echo "$PYTHON_ERRORS"
fi

# 8.2 Vérifier TypeScript (si disponible)
if command -v npx &> /dev/null; then
    log_info "Vérification TypeScript..."
    cd frontend/ia-factory-ui
    TS_ERRORS=$(npx tsc --noEmit 2>&1 | grep -c "error" || echo "0")
    cd "$PROJECT_ROOT"
    if [ "$TS_ERRORS" -eq 0 ]; then
        log_pass "Pas d'erreurs TypeScript"
    else
        log_warn "$TS_ERRORS erreurs TypeScript détectées"
    fi
fi

# ============================================================
# SECTION 9: API ENDPOINTS
# ============================================================
log_section "9. API ENDPOINTS (si API démarrée)"

# 9.1 Test health endpoint
log_info "Test endpoint /health..."
HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health 2>/dev/null || echo "000")
if [ "$HEALTH" = "200" ]; then
    log_pass "API /health répond 200"
else
    log_warn "API /health non accessible (code: $HEALTH)"
fi

# 9.2 Test pricing endpoint
log_info "Test endpoint /api/credits/pricing..."
PRICING=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/credits/pricing 2>/dev/null || echo "000")
if [ "$PRICING" = "200" ]; then
    log_pass "API /api/credits/pricing répond 200"
else
    log_warn "API /api/credits/pricing non accessible (code: $PRICING)"
fi

# ============================================================
# SECTION 10: i18n ET DARK MODE
# ============================================================
log_section "10. i18n ET DARK MODE"

# 10.1 Fichiers de traduction
log_info "Vérification fichiers i18n..."
I18N_FILES=("fr.json" "ar.json" "en.json")
for file in "${I18N_FILES[@]}"; do
    if [ -f "frontend/ia-factory-ui/messages/$file" ]; then
        log_pass "Traduction $file existe"
    else
        log_warn "Traduction $file MANQUANTE"
    fi
done

# 10.2 Dark mode classes
log_info "Vérification classes dark mode..."
DARK_CLASSES=$(grep -rn "dark:" frontend/ia-factory-ui --include="*.tsx" 2>/dev/null | grep -v node_modules | wc -l || echo "0")
if [ "$DARK_CLASSES" -gt 50 ]; then
    log_pass "Dark mode: $DARK_CLASSES classes dark: trouvées"
elif [ "$DARK_CLASSES" -gt 0 ]; then
    log_warn "Dark mode partiel: seulement $DARK_CLASSES classes"
else
    log_fail "Dark mode: AUCUNE classe dark: trouvée"
fi

# 10.3 ThemeProvider
if [ -f "frontend/ia-factory-ui/components/ThemeProvider.tsx" ]; then
    log_pass "ThemeProvider.tsx existe"
else
    log_warn "ThemeProvider.tsx MANQUANT"
fi

# ============================================================
# RAPPORT FINAL
# ============================================================
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                      RAPPORT FINAL                             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

TOTAL=$((PASS + FAIL + WARN))
SCORE=$((PASS * 100 / TOTAL))

echo -e "${GREEN}✅ PASS: $PASS${NC}"
echo -e "${RED}❌ FAIL: $FAIL${NC}"
echo -e "${YELLOW}⚠️  WARN: $WARN${NC}"
echo ""
echo -e "SCORE: ${BLUE}$SCORE%${NC} ($PASS/$TOTAL)"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}══════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  ✅ PROJET PRÊT POUR STAGING - AUCUNE ERREUR CRITIQUE       ${NC}"
    echo -e "${GREEN}══════════════════════════════════════════════════════════════${NC}"
    exit 0
elif [ $FAIL -le 2 ]; then
    echo -e "${YELLOW}══════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}  ⚠️  PROJET PARTIELLEMENT PRÊT - $FAIL ERREUR(S) À CORRIGER   ${NC}"
    echo -e "${YELLOW}══════════════════════════════════════════════════════════════${NC}"
    exit 1
else
    echo -e "${RED}══════════════════════════════════════════════════════════════${NC}"
    echo -e "${RED}  ❌ PROJET NON PRÊT - $FAIL ERREURS CRITIQUES                 ${NC}"
    echo -e "${RED}══════════════════════════════════════════════════════════════${NC}"
    exit 2
fi
