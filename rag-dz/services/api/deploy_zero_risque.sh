#!/bin/bash
# Deploy Zero Risque Architecture - IA Factory Algeria
# IMPORTANT: Run this AFTER rotating the 18 exposed API keys

set -e  # Exit on error

echo "========================================"
echo "  DEPLOY ZERO RISQUE - IA FACTORY DZ"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check environment variables
echo -e "${YELLOW}[1/6] Vérification des variables d'environnement...${NC}"
required_vars=(
    "POSTGRES_URL"
    "REDIS_URL"
    "GROQ_API_KEY"
    "OPENROUTER_API_KEY"
    "GOOGLE_API_KEY"
    "CHARGILY_SECRET_KEY"
    "CHARGILY_PUBLIC_KEY"
)

missing_vars=()
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        missing_vars+=("$var")
    fi
done

if [ ${#missing_vars[@]} -ne 0 ]; then
    echo -e "${RED}❌ Variables manquantes: ${missing_vars[*]}${NC}"
    echo "Veuillez configurer ces variables dans .env"
    exit 1
fi
echo -e "${GREEN}✅ Toutes les variables requises sont présentes${NC}"
echo ""

# Step 2: Test database connection
echo -e "${YELLOW}[2/6] Test de connexion PostgreSQL...${NC}"
if psql "$POSTGRES_URL" -c "SELECT 1" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ PostgreSQL accessible${NC}"
else
    echo -e "${RED}❌ Impossible de se connecter à PostgreSQL${NC}"
    exit 1
fi
echo ""

# Step 3: Test Redis connection
echo -e "${YELLOW}[3/6] Test de connexion Redis...${NC}"
if redis-cli -u "$REDIS_URL" PING > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Redis accessible${NC}"
else
    echo -e "${RED}❌ Impossible de se connecter à Redis${NC}"
    exit 1
fi
echo ""

# Step 4: Apply SQL migrations
echo -e "${YELLOW}[4/6] Application des migrations SQL...${NC}"
MIGRATION_FILE="services/api/migrations/005_billing_tiers.sql"

if [ ! -f "$MIGRATION_FILE" ]; then
    echo -e "${RED}❌ Fichier de migration introuvable: $MIGRATION_FILE${NC}"
    exit 1
fi

echo "Executing migration: $MIGRATION_FILE"
psql "$POSTGRES_URL" -f "$MIGRATION_FILE"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Migration appliquée avec succès${NC}"
else
    echo -e "${RED}❌ Erreur lors de l'application de la migration${NC}"
    exit 1
fi
echo ""

# Step 5: Verify tables created
echo -e "${YELLOW}[5/6] Vérification des tables créées...${NC}"
tables=("user_tiers" "llm_usage_logs" "payment_transactions")

for table in "${tables[@]}"; do
    if psql "$POSTGRES_URL" -c "\d $table" > /dev/null 2>&1; then
        echo -e "${GREEN}  ✅ Table $table créée${NC}"
    else
        echo -e "${RED}  ❌ Table $table manquante${NC}"
        exit 1
    fi
done
echo ""

# Step 6: Start FastAPI server (or reload if already running)
echo -e "${YELLOW}[6/6] Démarrage/Reload du serveur FastAPI...${NC}"
echo "Si vous utilisez Docker, exécutez:"
echo "  docker-compose restart iafactory-api"
echo ""
echo "Si vous lancez en local, exécutez:"
echo "  cd services/api && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  DÉPLOIEMENT TERMINÉ AVEC SUCCÈS ✅${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Prochaines étapes:"
echo "1. Tester les endpoints avec le script de test:"
echo "   python services/api/test_zero_risque.py"
echo ""
echo "2. Accéder au dashboard admin:"
echo "   http://localhost:8000/api/admin/dashboard"
echo ""
echo "3. Tester le chat avec routing:"
echo "   curl -X POST http://localhost:8000/api/v2/chat \\"
echo "     -H 'Authorization: Bearer YOUR_TOKEN' \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"messages\": [{\"role\": \"user\", \"content\": \"Test\"}]}'"
echo ""
