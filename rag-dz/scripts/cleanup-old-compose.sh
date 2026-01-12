#!/bin/bash
# =============================================================================
# SCRIPT: cleanup-old-compose.sh
# Description: Archive les anciens fichiers docker-compose fragmentés
# Usage: ./scripts/cleanup-old-compose.sh [--dry-run]
# =============================================================================

set -e

# Couleurs
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

DRY_RUN=false
if [[ "$1" == "--dry-run" ]]; then
    DRY_RUN=true
fi

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ARCHIVE_DIR="$PROJECT_ROOT/infrastructure/docker/_archive_compose"

# Fichiers à archiver
FILES_TO_ARCHIVE=(
    "infrastructure/docker/docker-compose.essential.yml"
    "infrastructure/docker/docker-compose.simple.yml"
    "infrastructure/docker/docker-compose.prod.yml"
    "infrastructure/docker/docker-compose.production.yml"
    "infrastructure/docker/docker-compose.frontend.yml"
    "infrastructure/docker/docker-compose.apps.yml"
    "infrastructure/docker/docker-compose.extras.yml"
    "infrastructure/docker/docker-compose-local.yml"
    "infrastructure/docker/docker-compose-ai-agents.yml"
    "infrastructure/docker/docker-compose-ai-agents-phase2.yml"
    "infrastructure/docker/docker-compose-ai-agents-phase3.yml"
    "infrastructure/docker/docker-compose-ai-agents-phase4.yml"
)

echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  CLEANUP OLD DOCKER-COMPOSE FILES${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

echo -e "[INFO] Project root: $PROJECT_ROOT"
echo -e "[INFO] Archive dir: $ARCHIVE_DIR"

if $DRY_RUN; then
    echo -e "${YELLOW}[WARN] Mode DRY-RUN: aucune modification ne sera effectuée${NC}"
fi

# Créer le dossier d'archive
if ! $DRY_RUN; then
    mkdir -p "$ARCHIVE_DIR"
    echo -e "${GREEN}[OK] Dossier d'archive créé${NC}"
fi

# Compteurs
FILES_FOUND=0
FILES_MOVED=0
FILES_NOT_FOUND=0

echo ""
echo -e "[INFO] Fichiers à archiver:"
echo ""

for relative_path in "${FILES_TO_ARCHIVE[@]}"; do
    full_path="$PROJECT_ROOT/$relative_path"
    filename=$(basename "$relative_path")

    if [[ -f "$full_path" ]]; then
        ((FILES_FOUND++))
        echo -e "  ${YELLOW}[X] $relative_path${NC}"

        if ! $DRY_RUN; then
            dest_path="$ARCHIVE_DIR/$filename"

            # Gérer les doublons
            if [[ -f "$dest_path" ]]; then
                timestamp=$(date +%Y%m%d-%H%M%S)
                dest_path="$ARCHIVE_DIR/${filename%.yml}-$timestamp.yml"
            fi

            mv "$full_path" "$dest_path"
            ((FILES_MOVED++))
        fi
    else
        ((FILES_NOT_FOUND++))
        echo -e "  [ ] $relative_path (non trouvé)"
    fi
done

echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  RÉSUMÉ${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""
echo "  Fichiers trouvés:   $FILES_FOUND"
echo -e "  ${GREEN}Fichiers archivés:  $FILES_MOVED${NC}"
echo "  Non trouvés:        $FILES_NOT_FOUND"
echo ""

# Fichiers conservés
echo -e "[INFO] Fichiers Docker Compose actifs (conservés):"
echo ""
for keep_file in "docker-compose.yml" "docker-compose.minimal.yml"; do
    if [[ -f "$PROJECT_ROOT/$keep_file" ]]; then
        echo -e "  ${GREEN}[*] $keep_file${NC}"
    fi
done
echo ""

if $DRY_RUN; then
    echo -e "${YELLOW}[WARN] Mode DRY-RUN terminé. Relancer sans --dry-run pour effectuer les modifications.${NC}"
elif [[ $FILES_MOVED -gt 0 ]]; then
    echo -e "${GREEN}[OK] Cleanup terminé! $FILES_MOVED fichiers archivés dans:${NC}"
    echo -e "  ${CYAN}$ARCHIVE_DIR${NC}"

    # Créer un fichier README dans l'archive
    cat > "$ARCHIVE_DIR/README.md" << EOF
# Archive Docker-Compose

Ces fichiers ont été archivés le $(date "+%Y-%m-%d %H:%M:%S").

Ils ont été remplacés par les fichiers consolidés à la racine du projet:
- \`docker-compose.yml\` - Stack complète
- \`docker-compose.minimal.yml\` - Stack RAG minimale

Pour restaurer un fichier, déplacez-le vers son emplacement original.
EOF

else
    echo "[INFO] Aucun fichier à archiver."
fi

echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  PROCHAINES ÉTAPES${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""
echo "  1. Copier .env.docker.example vers .env"
echo "     cp .env.docker.example .env"
echo ""
echo "  2. Configurer les clés API dans .env"
echo ""
echo "  3. Démarrer la stack minimale:"
echo "     docker compose -f docker-compose.minimal.yml up -d"
echo ""
echo "  4. Ou démarrer la stack complète:"
echo "     docker compose up -d"
echo ""
