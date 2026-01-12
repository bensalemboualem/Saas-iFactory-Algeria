# 🔧 Plan de Refactoring IAFactory – 11 janvier 2025

## 📊 Situation actuelle (diagnostic 04h00)

**Bon** :
- Backup complet fait (1.1 GB, 23776 fichiers) ✅
- Aucun projet en production = liberté totale pour refactorer ✅
- Architecture cible claire dans `CLAUDE.md` ✅

**Problèmes critiques détectés** :
- 🔴 3 systèmes de facturation dans `rag-dz` au lieu de 0
- 🔴 5 services de paiement dupliqués (Chargily, Stripe, PayPal)
- 🔴 14+ fichiers de providers IA qui bypassent le gateway
- 🔴 14 fichiers `.env` avec clés API exposées
- 🟠 Conflits de ports Docker (impossible de lancer 2 projets en même temps)
- 🟠 `rag-dz` = monorepo chaotique (60+ apps, 50+ agents, 2 backends)

## 🎯 Décision prise (05h00)

**Stratégie** : Éclater `rag-dz` en gardant TOUTES les apps (pas de suppression), mais les réorganiser proprement autour du gateway central.

**Timing** : Démarrage demain matin à tête reposée.

---

## 📋 PHASE 1 – Sécurité & Architecture (Semaine 1)

### Jour 1 : Audit et gel

**Matin (2h)**
1. Relire ce document
2. Créer `D:\IAFactory\.claude\refactor-tracking.md` pour suivre la progression
3. Lister TOUTES les clés API actuellement dans les 14 fichiers `.env` :
   ```bash
   # Dans Git Bash ou PowerShell
   cd D:\IAFactory
   grep -r "API_KEY\|SECRET_KEY\|OPENAI\|ANTHROPIC\|GROQ" --include="*.env*" . > keys-audit.txt
