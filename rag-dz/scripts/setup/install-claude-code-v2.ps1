<# 
INSTALLATION CLAUDE CODE - RAG-DZ
Copie-colle ce script ENTIER dans PowerShell
#>

Write-Host "Installation Claude Code..." -ForegroundColor Cyan

# Creer dossiers
New-Item -ItemType Directory -Force -Path ".claude\commands" | Out-Null
Write-Host "[OK] Dossiers crees" -ForegroundColor Green

# Backup
if (Test-Path "CLAUDE.md") {
    Copy-Item "CLAUDE.md" "CLAUDE.md.backup"
    Write-Host "[OK] Backup CLAUDE.md" -ForegroundColor Green
}

# CLAUDE.md
Set-Content -Path "CLAUDE.md" -Value @"
# IA Factory - rag-dz

## Commandes
docker-compose up -d : Demarrer
docker-compose logs -f : Logs
./deploy-to-vps.sh : Deployer

## Structure
apps/ agents/ api/ frontend/ shared/ bolt-diy/

## Style Code
- JavaScript ES6+, pas jQuery
- Python avec type hints
- Gestion erreurs try/catch

## Theme UI
Mode sombre: bg slate-900, text slate-100
Accent: blue-500, success emerald-500, error red-500

## i18n
fr (LTR), ar (RTL), en (LTR)

## Tokens - IMPORTANT
1. /clear entre chaque tache
2. Lire fichiers specifiques seulement
3. grep pour chercher

## NE JAMAIS FAIRE
- Modifier fichiers non mentionnes
- Supprimer code sans demander
- Hardcoder credentials
"@
Write-Host "[OK] CLAUDE.md cree" -ForegroundColor Green

# Commande: new-agent
Set-Content -Path ".claude\commands\new-agent.md" -Value @"
# Creer un nouvel agent

Agent: `$ARGUMENTS

1. Structure: index.html, styles.css, app.js, i18n.js
2. Theme IA Factory + dark/light mode
3. Chat interface + streaming
4. i18n FR/AR/EN
5. Test avant commit
"@

# Commande: fix-bug
Set-Content -Path ".claude\commands\fix-bug.md" -Value @"
# Corriger un bug

Bug: `$ARGUMENTS

1. Lis les fichiers (NE CODE PAS)
2. Diagnostique (think hard)
3. Propose solutions - ATTENDS VALIDATION
4. Corrige minimalement
5. Verifie + message commit
"@

# Commande: review
Set-Content -Path ".claude\commands\review.md" -Value @"
# Review de code

Cible: `$ARGUMENTS

Checklist:
- Nommage clair, pas de code duplique
- ES6+, gestion erreurs
- Theme IA Factory, responsive
- i18n FR/AR/EN, RTL arabe

Output: Positif / Suggestions / Bloquants
"@

# Commande: refactor
Set-Content -Path ".claude\commands\refactor.md" -Value @"
# Refactorer

Cible: `$ARGUMENTS

1. Analyse (NE CODE PAS)
2. Propose plan - ATTENDS VALIDATION
3. Implemente par etapes
4. Teste + message commit

Contrainte: NE casse PAS l'API existante
"@

# Commande: add-feature
Set-Content -Path ".claude\commands\add-feature.md" -Value @"
# Ajouter feature

Feature: `$ARGUMENTS

1. Clarifie (pose questions si besoin)
2. Design avec ultrathink - ATTENDS VALIDATION
3. Implemente (HTML/CSS/JS/i18n)
4. Teste mobile + 3 langues + dark mode
"@

# Commande: quick
Set-Content -Path ".claude\commands\quick.md" -Value @"
# Quick fix

Tache: `$ARGUMENTS

Pour modifs < 50 lignes, 1 fichier.
Fais la modif, verifie, montre diff.

Si plus complexe: /project:add-feature ou /project:fix-bug
"@

# Commande: commit
Set-Content -Path ".claude\commands\commit.md" -Value @"
# Git commit

1. git status + git diff
2. Message: type(scope): description
   Types: feat fix refactor style docs i18n chore
   Scopes: apps agents api frontend infra bolt
3. git add -A + git commit
"@

# Commande: explore
Set-Content -Path ".claude\commands\explore.md" -Value @"
# Explorer code

Question: `$ARGUMENTS

REGLE: NE modifie RIEN

Commandes: tree, ls, grep, head
Output: Resume + Fichiers cles + Details
"@

# Commande: test
Set-Content -Path ".claude\commands\test.md" -Value @"
# Tester

Cible: `$ARGUMENTS

UI: page charge, responsive, dark/light, FR/AR/EN
Fonctionnel: boutons, chat, streaming, erreurs
Console F12: pas erreurs JS, pas 404/500

Output: Passes / Echoues / Warnings
"@

# Commande: deploy
Set-Content -Path ".claude\commands\deploy.md" -Value @"
# Deployer

Cible: `$ARGUMENTS

Pre: tout commit, pas console.log, teste local

Statique: rsync apps/[nom]/ user@vps:/var/www/iafactory/apps/[nom]/
Docker: git pull + docker-compose up -d --build

Verifier: docker-compose ps, curl URL
"@

Write-Host "[OK] 10 commandes creees" -ForegroundColor Green

# Resume
Write-Host ""
Write-Host "========== INSTALLATION TERMINEE ==========" -ForegroundColor Green
Write-Host ""
Write-Host "Commandes disponibles:" -ForegroundColor Cyan
Write-Host "  /project:new-agent [nom]"
Write-Host "  /project:fix-bug [desc]"
Write-Host "  /project:review [fichier]"
Write-Host "  /project:refactor [cible]"
Write-Host "  /project:add-feature [feat]"
Write-Host "  /project:quick [tache]"
Write-Host "  /project:commit"
Write-Host "  /project:explore [question]"
Write-Host "  /project:test [cible]"
Write-Host "  /project:deploy [cible]"
Write-Host ""
Write-Host "Lance 'claude' pour commencer!" -ForegroundColor Yellow
