---
name: ia-factory-manager
description: Système de gestion centralisé pour l'écosystème IA Factory (Algérie & Suisse). Utiliser quand il faut: (1) Identifier quel projet on édite, (2) Vérifier les clés API à utiliser, (3) Détecter la contamination de code entre projets, (4) Lister les apps/agents/features par marché, (5) Éviter les mélanges Algérie/Suisse. Triggers: "quel projet", "quelle clé", "contamination", "mélange", "bordel", "perdu", "organisation".
---

# IA Factory Manager

Système de gestion pour ne plus jamais mélanger les projets Algérie et Suisse.

## Règle d'Or

**AVANT toute modification de code, TOUJOURS vérifier:**
1. Quel projet? → `references/projects.json`
2. Quel marché? → 🇩🇿 Algérie OU 🇨🇭 Suisse (JAMAIS les deux)
3. Quelles clés? → `references/api-keys-inventory.md`

## Identification Rapide du Contexte

### Markers Algérie 🇩🇿
```
- domaine: iafactoryalgeria.com
- paiement: Chargily Pay
- devise: DZD
- langues: FR, AR, Darija
- .env: .env.algeria ou .env.local.dz
```

### Markers Suisse 🇨🇭
```
- domaine: iafactory.ch
- paiement: Stripe
- devise: CHF
- langues: FR, DE, EN
- .env: .env.suisse ou .env.local.ch
```

## Commandes Utiles

### Vérifier contamination dans un repo
```bash
# Depuis le dossier du projet
./scripts/check-contamination.sh
```

### Identifier le marché d'un fichier
```bash
grep -r "chargily\|DZD\|algeri" .  # Si match = Algérie
grep -r "stripe\|CHF\|suisse\|swiss" .  # Si match = Suisse
```

## Workflow Obligatoire

1. **Nouveau fichier/feature:**
   - [ ] Consulter `references/projects.json` pour le projet cible
   - [ ] Vérifier le marché (🇩🇿 ou 🇨🇭)
   - [ ] Utiliser le bon fichier .env
   - [ ] Ajouter commentaire header: `// Market: ALGERIA` ou `// Market: SWITZERLAND`

2. **Debugging API:**
   - [ ] Consulter `references/api-keys-inventory.md`
   - [ ] Vérifier que la clé correspond au bon projet
   - [ ] NE JAMAIS copier une clé d'un projet à l'autre

3. **Pull Request / Commit:**
   - [ ] Lancer `scripts/check-contamination.sh`
   - [ ] Vérifier 0 contamination avant commit

## Structure des Projets

Consulter `references/projects.json` pour la liste complète avec:
- Nom et domaine
- Marché (DZ/CH)
- Features activées
- Fichier env associé
- Repo path

## Inventaire Clés API

Consulter `references/api-keys-inventory.md` pour:
- Liste des services utilisés
- Quel projet utilise quelle clé
- Où trouver chaque clé (PAS les valeurs, juste les emplacements)

## Architecture Globale

Consulter `references/architecture.md` pour:
- Schéma de l'écosystème
- Relations entre apps
- Flow de données
