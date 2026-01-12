# ============================================================================
# INSTALLATION AUTOMATIQUE CLAUDE CODE - RAG-DZ
# ============================================================================
# Usage: Ouvre PowerShell, va dans D:\iafactory\rag-dz et execute:
#   .\install-claude-code.ps1
# ============================================================================

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     🚀 INSTALLATION CLAUDE CODE CONFIG - IA FACTORY              ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Vérifier qu'on est dans rag-dz
$currentDir = Split-Path -Leaf (Get-Location)
if ($currentDir -ne "rag-dz") {
    Write-Host "⚠️  Tu n'es pas dans le dossier rag-dz" -ForegroundColor Yellow
    Write-Host "   Dossier actuel: $(Get-Location)" -ForegroundColor Gray
    $confirm = Read-Host "Continuer quand même? (o/n)"
    if ($confirm -ne "o") {
        Write-Host "Annulé. Va dans D:\iafactory\rag-dz et relance le script." -ForegroundColor Red
        exit 1
    }
}

# ============================================================================
# ÉTAPE 1: Créer les dossiers
# ============================================================================
Write-Host "[1/4] Création des dossiers..." -ForegroundColor Yellow

if (-not (Test-Path ".claude")) {
    New-Item -ItemType Directory -Path ".claude" | Out-Null
}
if (-not (Test-Path ".claude\commands")) {
    New-Item -ItemType Directory -Path ".claude\commands" | Out-Null
}
Write-Host "      ✅ .claude\commands\ créé" -ForegroundColor Green

# ============================================================================
# ÉTAPE 2: Backup ancien CLAUDE.md
# ============================================================================
Write-Host "[2/4] Backup des fichiers existants..." -ForegroundColor Yellow

if (Test-Path "CLAUDE.md") {
    $backupName = "CLAUDE.md.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Copy-Item "CLAUDE.md" $backupName
    Write-Host "      ✅ Ancien CLAUDE.md sauvegardé: $backupName" -ForegroundColor Green
} else {
    Write-Host "      ℹ️  Pas de CLAUDE.md existant" -ForegroundColor Gray
}

# ============================================================================
# ÉTAPE 3: Créer CLAUDE.md
# ============================================================================
Write-Host "[3/4] Création de CLAUDE.md..." -ForegroundColor Yellow

$claudeMd = @'
# IA Factory - rag-dz Configuration

## Commandes Bash
- `docker-compose up -d` : Démarrer les services
- `docker-compose logs -f [service]` : Voir les logs
- `docker-compose restart [service]` : Redémarrer un service
- `./deploy-to-vps.sh` : Déployer sur production
- `python -m http.server 8080` : Serveur local rapide

## Structure du Projet
```
rag-dz/
├── apps/              # Applications déployées (HTML/JS)
├── agents/            # Agents IA spécialisés
├── api/               # Backend Python/FastAPI
├── frontend/          # Frontend principal
├── shared/            # Code partagé
├── scripts/           # Scripts utilitaires
├── infra/             # Infrastructure Docker/Nginx
├── bolt-diy/          # Clone bolt.new
└── docs/              # Documentation
```

## Stack Technique
- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **Backend**: Python, FastAPI
- **Base de données**: Supabase, PostgreSQL
- **Conteneurs**: Docker, Docker Compose
- **Reverse Proxy**: Nginx
- **IA**: OpenAI, Anthropic, Groq, DeepSeek, Qwen

## Style de Code

### JavaScript
- ES6+ (const/let, arrow functions, async/await)
- Pas de jQuery - vanilla JS uniquement
- Gestion erreurs avec try/catch

### Python
- Type hints obligatoires
- Docstrings pour fonctions publiques
- Pas de print() en production

## Thème UI - IA Factory
```css
/* Mode sombre */
--bg-primary: #0f172a;      /* slate-900 */
--bg-secondary: #1e293b;    /* slate-800 */
--text-primary: #f1f5f9;    /* slate-100 */
--accent: #3b82f6;          /* blue-500 */
--success: #10b981;         /* emerald-500 */
--error: #ef4444;           /* red-500 */
```

## Internationalisation (i18n)
| Code | Langue | Direction |
|------|--------|-----------|
| `fr` | Français | LTR |
| `ar` | العربية | RTL |
| `en` | English | LTR |

## Gestion des Tokens - CRITIQUE
1. **`/clear` entre chaque tâche**
2. Lire des fichiers SPÉCIFIQUES seulement
3. Utiliser `grep` pour chercher
4. Ne pas relire les fichiers déjà en contexte

## URLs Production
- https://iafactoryalgeria.com
- https://iafactoryalgeria.com/apps/[nom]
- https://iafactoryalgeria.com/api/v1/

## NE JAMAIS FAIRE
- Modifier des fichiers non mentionnés
- Supprimer du code sans demander
- Hardcoder des credentials
- Committer du code non testé
'@

$claudeMd | Out-File -FilePath "CLAUDE.md" -Encoding UTF8
Write-Host "      ✅ CLAUDE.md créé" -ForegroundColor Green

# ============================================================================
# ÉTAPE 4: Créer les 10 commandes
# ============================================================================
Write-Host "[4/4] Création des 10 commandes..." -ForegroundColor Yellow

# --- new-agent.md ---
@'
# Créer un nouvel agent IA Factory

Crée un nouvel agent nommé "$ARGUMENTS" pour IA Factory.

## Structure à créer dans apps/ ou agents/
```
[nom-agent]/
├── index.html     # Page principale
├── styles.css     # Styles thème IA Factory
├── app.js         # Logique JavaScript
└── i18n.js        # Traductions FR/AR/EN
```

## Checklist
1. Structure HTML avec header/chat/footer
2. Styles: import iafactory-design-system.css
3. Support dark/light mode + responsive
4. Interface chat avec streaming
5. Historique localStorage
6. Sélecteur langue FR/AR/EN
7. Gestion erreurs API
8. Test local avant commit

NE commit PAS sans ma validation.
'@ | Out-File -FilePath ".claude\commands\new-agent.md" -Encoding UTF8

# --- fix-bug.md ---
@'
# Analyser et corriger un bug

Bug: $ARGUMENTS

## Workflow

### 1. Comprendre (NE CODE PAS)
- Lis les fichiers de l'erreur
- Identifie la stack trace
- Note les fichiers impliqués

### 2. Diagnostiquer (think hard)
- Problème de types?
- Problème de logique?
- Problème async?
- Problème CSS/i18n?

### 3. Proposer
Propose 1-3 solutions avec risques.
**ATTENDS VALIDATION** avant d'implémenter.

### 4. Corriger
- Correction MINIMALE
- Ne touche QUE les fichiers nécessaires

### 5. Vérifier
- Bug résolu?
- Pas de régression?
- Propose message commit
'@ | Out-File -FilePath ".claude\commands\fix-bug.md" -Encoding UTF8

# --- review.md ---
@'
# Review de code

Cible: $ARGUMENTS

## Checklist

### Code
- [ ] Nommage clair
- [ ] Pas de code dupliqué
- [ ] Fonctions < 50 lignes
- [ ] Pas de console.log

### JavaScript
- [ ] ES6+ syntax
- [ ] Gestion erreurs try/catch
- [ ] Pas de variables globales

### CSS
- [ ] Thème IA Factory respecté
- [ ] Dark/light mode OK
- [ ] Responsive OK

### i18n
- [ ] Textes traduits FR/AR/EN
- [ ] RTL pour arabe

## Output
✅ Positif | ⚠️ Suggestions | ❌ Bloquants
'@ | Out-File -FilePath ".claude\commands\review.md" -Encoding UTF8

# --- refactor.md ---
@'
# Refactorer

Cible: $ARGUMENTS

## Contraintes
- NE casse PAS l'API existante
- Comportements préservés
- Pas de nouvelles dépendances

## Workflow

### 1. Analyse (NE CODE PAS)
- Lis le fichier complet
- Identifie les problèmes
- Liste les dépendances

### 2. Plan
Propose plan détaillé.
**ATTENDS VALIDATION.**

### 3. Implémentation
- Changement minimal par étape
- Vérifie après chaque étape

### 4. Finalisation
- Teste toutes fonctionnalités
- Teste 3 langues si i18n
- Propose message commit
'@ | Out-File -FilePath ".claude\commands\refactor.md" -Encoding UTF8

# --- add-feature.md ---
@'
# Ajouter une fonctionnalité

Feature: $ARGUMENTS

## Workflow

### 1. Clarification
- Objectif utilisateur?
- Cas d'usage?
- Edge cases?
- Contraintes?

Si pas clair, POSE DES QUESTIONS.

### 2. Design (ultrathink)
- Architecture
- UI/UX
- Données
- Plan d'implémentation

**ATTENDS VALIDATION du plan.**

### 3. Implémentation
- HTML/CSS: thème IA Factory
- JS: gestion erreurs, loading
- i18n: FR/AR/EN obligatoires

### 4. Tests
- Mobile/desktop
- 3 langues
- Dark/light mode
- Cas d'erreur
'@ | Out-File -FilePath ".claude\commands\add-feature.md" -Encoding UTF8

# --- quick.md ---
@'
# Quick Fix

Tâche: $ARGUMENTS

## Critères
- < 50 lignes
- 1 seul fichier
- Pas de changement architecture

## Exécution
1. Fais la modification
2. Vérifie que ça marche
3. Montre le diff

## Exemples OK
✅ Corriger typo
✅ Changer couleur CSS
✅ Modifier texte/traduction

## Si plus complexe
Utilise plutôt:
- /project:add-feature
- /project:refactor
- /project:fix-bug
'@ | Out-File -FilePath ".claude\commands\quick.md" -Encoding UTF8

# --- commit.md ---
@'
# Git Commit

## Workflow

### 1. Vérifier
```bash
git status
git diff --stat
```

### 2. Format message
```
type(scope): description
```

Types: feat, fix, refactor, style, docs, i18n, chore

Scopes: apps, agents, api, frontend, infra, bolt

### 3. Exemples
```
feat(agents): ajouter IA Recruteur DZ
fix(apps): corriger scroll chat
i18n(agents): traductions arabes
```

### 4. Exécuter
```bash
git add -A
git commit -m "[message]"
```
'@ | Out-File -FilePath ".claude\commands\commit.md" -Encoding UTF8

# --- explore.md ---
@'
# Explorer la codebase

Question: $ARGUMENTS

## RÈGLE: NE modifie AUCUN fichier

## Commandes utiles
```bash
# Structure
tree -L 2 apps/
ls agents/

# Chercher
grep -r "mot" apps/ --include="*.html"
grep -r "mot" api/ --include="*.py"

# Voir partiellement
head -100 fichier.html
```

## Output attendu
```markdown
## Résumé
[réponse courte]

## Fichiers clés
- chemin/fichier: [rôle]

## Détails
[explication]
```
'@ | Out-File -FilePath ".claude\commands\explore.md" -Encoding UTF8

# --- test.md ---
@'
# Tester

Cible: $ARGUMENTS

## Tests manuels

### UI
- [ ] Page charge sans erreur
- [ ] Responsive OK
- [ ] Dark/light mode OK
- [ ] FR/AR/EN OK
- [ ] RTL arabe OK

### Fonctionnel
- [ ] Boutons cliquables
- [ ] Chat envoie/reçoit
- [ ] Streaming OK
- [ ] Erreurs affichées

### Console (F12)
- [ ] Pas d'erreurs JS
- [ ] Requêtes OK (Network)
- [ ] Pas de 404/500

## Output
✅ Passés | ❌ Échoués | ⚠️ Warnings
'@ | Out-File -FilePath ".claude\commands\test.md" -Encoding UTF8

# --- deploy.md ---
@'
# Déployer

Cible: $ARGUMENTS

## Pré-déploiement
- [ ] Tout commité
- [ ] Pas de console.log
- [ ] Testé localement

## Déploiement

### Fichiers statiques
```bash
rsync -avz apps/[nom]/ user@vps:/var/www/iafactory/apps/[nom]/
```

### Docker
```bash
# Sur VPS
cd /opt/rag-dz
git pull
docker-compose up -d --build
```

## Post-déploiement
```bash
# Vérifier
docker-compose ps
curl -I https://iafactoryalgeria.com/[path]
```

## Rollback si problème
```bash
git revert HEAD
docker-compose up -d --build
```
'@ | Out-File -FilePath ".claude\commands\deploy.md" -Encoding UTF8

Write-Host "      ✅ 10 commandes créées" -ForegroundColor Green

# ============================================================================
# RÉSUMÉ FINAL
# ============================================================================
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║     ✅ INSTALLATION TERMINÉE !                                   ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "📁 Fichiers créés:" -ForegroundColor Cyan
Write-Host "   CLAUDE.md" -ForegroundColor White
Write-Host "   .claude\commands\new-agent.md" -ForegroundColor Gray
Write-Host "   .claude\commands\fix-bug.md" -ForegroundColor Gray
Write-Host "   .claude\commands\review.md" -ForegroundColor Gray
Write-Host "   .claude\commands\refactor.md" -ForegroundColor Gray
Write-Host "   .claude\commands\add-feature.md" -ForegroundColor Gray
Write-Host "   .claude\commands\quick.md" -ForegroundColor Gray
Write-Host "   .claude\commands\commit.md" -ForegroundColor Gray
Write-Host "   .claude\commands\explore.md" -ForegroundColor Gray
Write-Host "   .claude\commands\test.md" -ForegroundColor Gray
Write-Host "   .claude\commands\deploy.md" -ForegroundColor Gray
Write-Host ""

Write-Host "🚀 Commandes disponibles dans Claude Code:" -ForegroundColor Cyan
Write-Host "   /project:new-agent [nom]     - Créer agent" -ForegroundColor White
Write-Host "   /project:fix-bug [desc]      - Corriger bug" -ForegroundColor White
Write-Host "   /project:review [fichier]    - Review code" -ForegroundColor White
Write-Host "   /project:refactor [cible]    - Refactorer" -ForegroundColor White
Write-Host "   /project:add-feature [feat]  - Nouvelle feature" -ForegroundColor White
Write-Host "   /project:quick [tâche]       - Fix rapide" -ForegroundColor White
Write-Host "   /project:commit              - Commit guidé" -ForegroundColor White
Write-Host "   /project:explore [question]  - Explorer code" -ForegroundColor White
Write-Host "   /project:test [cible]        - Tester" -ForegroundColor White
Write-Host "   /project:deploy [cible]      - Déployer" -ForegroundColor White
Write-Host ""

Write-Host "💡 Tips:" -ForegroundColor Yellow
Write-Host "   • /clear entre chaque tâche (économise tokens)" -ForegroundColor Gray
Write-Host "   • 'ultrathink' pour les décisions complexes" -ForegroundColor Gray
Write-Host "   • Tape '/' dans Claude Code pour voir les commandes" -ForegroundColor Gray
Write-Host ""

Write-Host "👉 Lance 'claude' dans ce dossier pour commencer!" -ForegroundColor Cyan
Write-Host ""
