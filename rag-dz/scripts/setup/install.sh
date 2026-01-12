#!/bin/bash

# =============================================================================
# 🚀 Script d'installation Claude Code Optimisé pour IA Factory
# =============================================================================

set -e

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║     🚀 Installation Claude Code Config - IA Factory             ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Vérifier qu'on est dans un projet
if [ ! -f "package.json" ]; then
    echo -e "${RED}❌ Erreur: package.json non trouvé.${NC}"
    echo "   Exécute ce script depuis la racine de ton projet."
    exit 1
fi

# Créer les dossiers
echo -e "${YELLOW}📁 Création des dossiers...${NC}"
mkdir -p .claude/commands

# Copier CLAUDE.md
echo -e "${YELLOW}📝 Installation de CLAUDE.md...${NC}"
if [ -f "CLAUDE.md" ]; then
    echo -e "${YELLOW}   ⚠️  CLAUDE.md existe déjà. Sauvegarde en CLAUDE.md.backup${NC}"
    mv CLAUDE.md CLAUDE.md.backup
fi

cat > CLAUDE.md << 'HEREDOC'
# IA Factory - Configuration Claude Code

## Commandes Bash Essentielles
- `npm run dev` : Serveur de développement
- `npm run build` : Build production
- `npm run lint` : Vérification ESLint
- `npm run typecheck` : Vérification TypeScript
- `npm test` : Lancer les tests

## Stack Technique
- **Framework**: Next.js 14+ App Router
- **UI**: shadcn/ui + Tailwind CSS
- **État**: Zustand / React Query
- **Langue**: TypeScript strict uniquement

## Style de Code - IMPORTANT
- ES Modules (import/export), JAMAIS CommonJS
- Composants React fonctionnels avec hooks
- Pas de `any` TypeScript - types stricts obligatoires
- camelCase variables, PascalCase composants

## Conventions UI - IA Factory
- Thème sombre: `bg-slate-900`, `text-slate-100`
- Thème clair: `bg-white`, `text-slate-900`
- Accent: `blue-600`, `emerald-500` (succès), `red-500` (erreur)
- Toujours supporter dark mode avec `dark:`

## Gestion des Tokens - OPTIMISATION
- Utilise `/clear` entre chaque tâche distincte
- Préfère lire des fichiers spécifiques
- Évite de relire les fichiers déjà en contexte

## NE JAMAIS FAIRE
- Modifier des fichiers non mentionnés
- Créer des abstractions inutiles
- Ignorer les erreurs TypeScript
HEREDOC

echo -e "${GREEN}   ✅ CLAUDE.md installé${NC}"

# Installer les commandes
echo -e "${YELLOW}📦 Installation des commandes personnalisées...${NC}"

# Commande: new-agent
cat > .claude/commands/new-agent.md << 'HEREDOC'
# Créer un nouvel agent IA Factory

Crée un nouvel agent nommé "$ARGUMENTS" pour IA Factory.

Structure: app/, components/, hooks/, lib/, types/, stores/
UI: shadcn/ui + Tailwind, dark/light mode
Features: Chat interface, historique, export, streaming

1. Crée la structure
2. Implémente les composants de base
3. Configure le prompt système
4. Vérifie typecheck + lint
5. Attends validation avant commit
HEREDOC

# Commande: fix-bug
cat > .claude/commands/fix-bug.md << 'HEREDOC'
# Analyser et corriger un bug

Bug: $ARGUMENTS

1. Lis les fichiers concernés (NE code PAS)
2. Think hard: diagnostique la cause
3. Propose 1-3 solutions, attends validation
4. Implémente la correction minimale
5. Ajoute test de non-régression
6. Vérifie typecheck + lint
HEREDOC

# Commande: review
cat > .claude/commands/review.md << 'HEREDOC'
# Review de code

Cible: $ARGUMENTS

Checklist:
- TypeScript strict (pas de any)
- React: hooks corrects, pas de re-renders
- Performance: pas de calculs dans render
- Sécurité: inputs validés
- Accessibilité: labels, alt, structure

Output: ✅ Positif | ⚠️ Suggestions | ❌ Bloquants
HEREDOC

# Commande: refactor
cat > .claude/commands/refactor.md << 'HEREDOC'
# Refactorer

Cible: $ARGUMENTS

Contraintes: NE casse PAS l'API, tests doivent passer

1. Analyse sans coder
2. Propose plan, attends validation
3. Implémente par étapes
4. Vérifie après chaque étape
5. typecheck + lint + test
HEREDOC

# Commande: quick
cat > .claude/commands/quick.md << 'HEREDOC'
# Quick Fix

Tâche: $ARGUMENTS

Pour modifications < 50 lignes, 1 seul fichier.
Fais la modif, vérifie typecheck + lint, montre le diff.
Si plus complexe, suggère /project:add-feature ou /project:refactor
HEREDOC

# Commande: commit
cat > .claude/commands/commit.md << 'HEREDOC'
# Git Commit

1. git status && git diff --stat
2. npm run typecheck && npm run lint
3. Message format: type(scope): description
   Types: feat, fix, refactor, style, docs, test, chore
4. git add -A && git commit -m "[message]"
HEREDOC

# Commande: explore
cat > .claude/commands/explore.md << 'HEREDOC'
# Explorer la codebase

Question: $ARGUMENTS

RÈGLE: NE modifie AUCUN fichier

1. tree -L 3 pour structure
2. Cherche avec grep -r "mot-clé" src/
3. Lis les fichiers pertinents
4. Réponds avec: Résumé + Détails + Fichiers clés
HEREDOC

# Commande: test
cat > .claude/commands/test.md << 'HEREDOC'
# Écrire des tests

Cible: $ARGUMENTS

Couvrir: cas nominal, limites, erreurs, edge cases
Structure AAA: Arrange, Act, Assert
Nommage: should [action] when [condition]
Frameworks: Vitest/Jest, React Testing Library, MSW

Éviter: tester l'implémentation, mocks excessifs
HEREDOC

echo -e "${GREEN}   ✅ 7 commandes installées${NC}"

# Installer .mcp.json
echo -e "${YELLOW}🔧 Installation de .mcp.json...${NC}"
cat > .mcp.json << 'HEREDOC'
{
  "mcpServers": {
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-puppeteer"]
    }
  }
}
HEREDOC
echo -e "${GREEN}   ✅ .mcp.json installé${NC}"

# Résumé
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     ✅ Installation terminée !                                   ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📋 Fichiers créés:${NC}"
echo "   • CLAUDE.md (configuration principale)"
echo "   • .claude/commands/ (7 commandes)"
echo "   • .mcp.json (serveurs MCP)"
echo ""
echo -e "${BLUE}🚀 Commandes disponibles:${NC}"
echo "   /project:new-agent [nom]    - Créer un nouvel agent"
echo "   /project:fix-bug [desc]     - Corriger un bug"
echo "   /project:review [fichier]   - Review de code"
echo "   /project:refactor [cible]   - Refactorer"
echo "   /project:quick [tâche]      - Fix rapide"
echo "   /project:commit             - Commit guidé"
echo "   /project:explore [question] - Explorer le code"
echo "   /project:test [cible]       - Écrire des tests"
echo ""
echo -e "${YELLOW}💡 Conseils:${NC}"
echo "   • Utilise /clear entre chaque tâche"
echo "   • Utilise 'think hard' pour les tâches complexes"
echo "   • Personnalise CLAUDE.md selon ton projet"
echo ""
