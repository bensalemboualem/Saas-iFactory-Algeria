#!/bin/bash
# ============================================================================
# IA Factory Manager - Script d'Installation
# ============================================================================
# Ce script installe le skill dans ton environnement Claude Code/Cowork
# ============================================================================

set -e

echo "============================================"
echo "   IA Factory Manager - Installation"
echo "============================================"
echo ""

# Déterminer le chemin d'installation
if [ -d "$HOME/.claude/skills" ]; then
    SKILL_PATH="$HOME/.claude/skills/ia-factory-manager"
    echo "📁 Installation dans: $SKILL_PATH"
elif [ -d "/mnt/skills/user" ]; then
    SKILL_PATH="/mnt/skills/user/ia-factory-manager"
    echo "📁 Installation dans: $SKILL_PATH (Claude.ai)"
else
    SKILL_PATH="$HOME/ia-factory-manager"
    echo "📁 Installation dans: $SKILL_PATH (local)"
fi

# Créer le répertoire
mkdir -p "$SKILL_PATH"

# Copier les fichiers
echo ""
echo "📋 Copie des fichiers..."

# Cette partie sera remplacée par le contenu réel lors du téléchargement
# Pour l'instant, afficher les instructions manuelles

echo ""
echo "============================================"
echo "   INSTRUCTIONS D'INSTALLATION"
echo "============================================"
echo ""
echo "1. Télécharge le dossier ia-factory-manager"
echo ""
echo "2. Pour Claude Code:"
echo "   cp -r ia-factory-manager ~/.claude/skills/"
echo ""
echo "3. Pour Claude Cowork (macOS):"
echo "   Glisse le dossier dans le dossier autorisé"
echo ""
echo "4. Mets à jour projects.json avec les VRAIS chemins de tes repos"
echo ""
echo "5. Lance le script de vérification:"
echo "   cd /ton/projet && ./ia-factory-manager/scripts/check-contamination.sh"
echo ""
echo "============================================"
echo ""
echo "✅ Installation terminée!"
echo ""
echo "🔥 PROCHAINES ÉTAPES:"
echo "   1. Ouvre references/projects.json"
echo "   2. Remplace /path/to/ par les vrais chemins"
echo "   3. Vérifie api-keys-inventory.md"
echo "   4. Lance check-contamination.sh sur chaque projet"
echo ""
