#!/bin/bash
# ================================================================
# SÉCURISATION POSTGRESQL & OLLAMA - IAFactory Algeria
# ================================================================
# Restreint les ports 5432 et 11434 à localhost uniquement
# ================================================================

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "================================================================"
echo "🔒 SÉCURISATION POSTGRESQL & OLLAMA"
echo "================================================================"
echo ""

# Vérifier qu'on est dans le bon répertoire
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}❌ Erreur: docker-compose.yml non trouvé${NC}"
    echo "Assurez-vous d'être dans /opt/iafactory-rag-dz"
    exit 1
fi

echo -e "${BLUE}[1/5]${NC} Sauvegarde du docker-compose.yml actuel..."
cp docker-compose.yml docker-compose.yml.backup-$(date +%Y%m%d_%H%M%S)
echo -e "${GREEN}✅ Backup créé${NC}"
echo ""

echo -e "${BLUE}[2/5]${NC} Vérification des ports actuels..."
echo ""

# Vérifier PostgreSQL
if grep -q '"5432:5432"' docker-compose.yml || grep -q "'5432:5432'" docker-compose.yml || grep -q "- 5432:5432" docker-compose.yml; then
    echo -e "${RED}⚠️  PostgreSQL: Port 5432 EXPOSÉ PUBLIQUEMENT${NC}"
    POSTGRES_EXPOSED=1
else
    echo -e "${GREEN}✅ PostgreSQL: Déjà sécurisé${NC}"
    POSTGRES_EXPOSED=0
fi

# Vérifier Ollama
if grep -q '"11434:11434"' docker-compose.yml || grep -q "'11434:11434'" docker-compose.yml || grep -q "- 11434:11434" docker-compose.yml; then
    echo -e "${RED}⚠️  Ollama: Port 11434 EXPOSÉ PUBLIQUEMENT${NC}"
    OLLAMA_EXPOSED=1
else
    echo -e "${GREEN}✅ Ollama: Déjà sécurisé${NC}"
    OLLAMA_EXPOSED=0
fi

echo ""

if [ $POSTGRES_EXPOSED -eq 0 ] && [ $OLLAMA_EXPOSED -eq 0 ]; then
    echo -e "${GREEN}✅ Tous les ports sont déjà sécurisés!${NC}"
    exit 0
fi

echo -e "${BLUE}[3/5]${NC} Application des corrections de sécurité..."
echo ""

# Fonction pour remplacer les ports
secure_port() {
    local PORT=$1
    local FILE="docker-compose.yml"

    # Différents formats possibles
    sed -i "s/\"$PORT:$PORT\"/\"127.0.0.1:$PORT:$PORT\"/g" "$FILE"
    sed -i "s/'$PORT:$PORT'/'127.0.0.1:$PORT:$PORT'/g" "$FILE"
    sed -i "s/- $PORT:$PORT/- 127.0.0.1:$PORT:$PORT/g" "$FILE"
    sed -i "s/  $PORT:$PORT/  127.0.0.1:$PORT:$PORT/g" "$FILE"
}

if [ $POSTGRES_EXPOSED -eq 1 ]; then
    echo "Sécurisation PostgreSQL (port 5432)..."
    secure_port "5432"
    echo -e "${GREEN}✅ PostgreSQL sécurisé${NC}"
fi

if [ $OLLAMA_EXPOSED -eq 1 ]; then
    echo "Sécurisation Ollama (port 11434)..."
    secure_port "11434"
    echo -e "${GREEN}✅ Ollama sécurisé${NC}"
fi

echo ""
echo -e "${BLUE}[4/5]${NC} Vérification des modifications..."
echo ""

# Afficher les ports modifiés
echo "Ports PostgreSQL:"
grep -A 2 "postgres" docker-compose.yml | grep "5432" || echo "  (non trouvé dans config)"

echo ""
echo "Ports Ollama:"
grep -A 2 "ollama" docker-compose.yml | grep "11434" || echo "  (non trouvé dans config)"

echo ""
echo -e "${BLUE}[5/5]${NC} Redémarrage des services..."
echo ""

# Trouver les noms de conteneurs
POSTGRES_CONTAINER=$(docker ps --format '{{.Names}}' | grep -i postgres | head -1)
OLLAMA_CONTAINER=$(docker ps --format '{{.Names}}' | grep -i ollama | head -1)

echo "PostgreSQL container: ${POSTGRES_CONTAINER:-non trouvé}"
echo "Ollama container: ${OLLAMA_CONTAINER:-non trouvé}"
echo ""

# Redémarrer
if [ $POSTGRES_EXPOSED -eq 1 ] && [ -n "$POSTGRES_CONTAINER" ]; then
    echo "Redémarrage PostgreSQL..."
    docker-compose restart $(echo $POSTGRES_CONTAINER | sed 's/.*-//')
    echo -e "${GREEN}✅ PostgreSQL redémarré${NC}"
fi

if [ $OLLAMA_EXPOSED -eq 1 ] && [ -n "$OLLAMA_CONTAINER" ]; then
    echo "Redémarrage Ollama..."
    docker-compose restart $(echo $OLLAMA_CONTAINER | sed 's/.*-//')
    echo -e "${GREEN}✅ Ollama redémarré${NC}"
fi

echo ""
echo "⏳ Attente 10 secondes pour stabilisation..."
sleep 10

echo ""
echo "================================================================"
echo -e "${GREEN}✅ SÉCURISATION TERMINÉE${NC}"
echo "================================================================"
echo ""

# Vérification finale
echo "📊 VÉRIFICATION FINALE:"
echo ""

echo "Ports en écoute sur 0.0.0.0 (PUBLICS):"
netstat -tlnp 2>/dev/null | grep -E ":(5432|11434) " | grep "0.0.0.0" || echo "  Aucun (bon!)"

echo ""
echo "Ports en écoute sur 127.0.0.1 (LOCAUX):"
netstat -tlnp 2>/dev/null | grep -E ":(5432|11434) " | grep "127.0.0.1" || echo "  Aucun"

echo ""
echo "📋 RÉSUMÉ:"
echo "  • PostgreSQL: Accessible uniquement depuis localhost"
echo "  • Ollama: Accessible uniquement depuis localhost"
echo "  • Applications internes: Peuvent toujours accéder via Docker network"
echo "  • Accès externe: BLOQUÉ (sécurité renforcée)"
echo ""

echo "🔧 Backup disponible:"
ls -lh docker-compose.yml.backup-* | tail -1

echo ""
echo "✅ Sécurité renforcée avec succès!"
echo ""
