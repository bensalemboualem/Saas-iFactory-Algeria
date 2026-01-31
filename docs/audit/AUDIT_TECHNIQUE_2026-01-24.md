# AUDIT TECHNIQUE COMPLET - IAFACTORY ALGERIA

**Date** : 24 Janvier 2026
**Projet** : IAFactory Algeria (Fork LobeChat v2.0.0-next.179)
**Auditeur** : Claude Opus 4.5
**Marché cible** : Algérie uniquement

---

## RÉSUMÉ EXÉCUTIF

| Catégorie | CRITIQUE | MAJEUR | MINEUR | OK |
|-----------|----------|--------|--------|-----|
| Références Suisse | 0 | 3 | 2 | - |
| Sécurité | 1 | 1 | 0 | - |
| Docker | 0 | 0 | 0 | OK |
| Branding | 0 | 0 | 0 | OK |
| Dépendances | 0 | 1 | 0 | - |

**Score global** : 78/100 (Quelques correctifs nécessaires)

---

## 1. RÉFÉRENCES INVALIDES (Suisse/Swiss/CHF)

### 1.1 Problèmes MAJEURS

| # | Fichier | Ligne | Problème | Fix suggéré |
|---|---------|-------|----------|-------------|
| 1 | `apps/b2b/video-studio/README.md` | 9 | Mentionne "Français/Allemand/Italien" (langues suisses) | Remplacer par "Français/Arabe/Darija" |
| 2 | `docs/architecture/ARCHITECTURE_OPTIMALE.md` | 529, 673, 714 | Références "SWITZERLAND", "SUISSE" | Supprimer les sections Suisse ou déplacer vers D:\suisse_saas |
| 3 | `docs/migration/PLAN_MIGRATION_DETAILLE.md` | 678, 728, 779 | Références Switzerland et Stripe CH | Supprimer les sections Suisse |

### 1.2 Problèmes MINEURS

| # | Fichier | Ligne | Problème | Fix suggéré |
|---|---------|-------|----------|-------------|
| 4 | `apps/b2b/video-studio/README.md` | 220 | `LUMA_API_KEY_SUISSE` legacy | Supprimer la mention |
| 5 | `docker-compose/local/searxng-settings.yml` | 37 | Mention "swisscows" dans commentaire | Supprimer le commentaire |

### 1.3 Références SUPPRIMÉES (OK)

- `docker-compose/docker-compose.switzerland.yml` - **SUPPRIMÉ**
- `docker-compose/docker-compose.switzerland.prod.yml` - **SUPPRIMÉ**
- `packages/const/src/branding.ts` - **CORRIGÉ** (IAFactory Algeria)
- `apps/landing/src/pages/Pricing.tsx` - **CORRIGÉ** (DZD, Chargily)
- `src/app/[variants]/(landing)/verticals/LegalLanding.tsx` - **CORRIGÉ** (Droit algérien)
- `apps/iafactory-core/rag-dz/agents/legal/legal_team.py` - **CORRIGÉ** (Algérie uniquement)

---

## 2. AUDIT SÉCURITÉ

### 2.1 CRITIQUE - API Keys exposées

| # | Fichier | Problème | Gravité | Action |
|---|---------|----------|---------|--------|
| 1 | `apps/gateway/.env` | **API KEYS RÉELLES PRÉSENTES** | **CRITIQUE** | Révoquer et régénérer toutes les clés |

**Détails** :
```
apps/gateway/.env contient :
- GROQ_API_KEY=gsk_7kbTP... (RÉELLE)
- OPENROUTER_API_KEY=sk-or-v1-b343b... (RÉELLE)
- DEEPSEEK_API_KEY=sk-14487... (RÉELLE)
- OPENAI_API_KEY=sk-proj-TXy6r... (RÉELLE)
```

**Actions requises** :
1. Révoquer immédiatement ces clés dans les dashboards des providers
2. Régénérer de nouvelles clés
3. Stocker dans un gestionnaire de secrets (Vault, AWS Secrets Manager)
4. Ne JAMAIS commiter ce fichier

### 2.2 MAJEUR - Fichiers .env versionnables

| # | Fichier | Statut | Risque |
|---|---------|--------|--------|
| 1 | `.env` | Dans .gitignore | OK |
| 2 | `.env.local` | Dans .gitignore | OK |
| 3 | `apps/**/.env` | Dans .gitignore | OK |
| 4 | `apps/b2b/school/.env` | Présent mais vide | ATTENTION |

### 2.3 Configuration .gitignore

```
# Environment files ✓
.env
.env.local
.env*.local
.env.development
apps/**/.env
apps/**/.env.local
```

**Verdict** : Les règles .gitignore sont correctes.

---

## 3. AUDIT DOCKER

### 3.1 Fichiers Docker-Compose présents

| Fichier | Région | Statut |
|---------|--------|--------|
| `docker-compose.algeria.yml` | DZ | OK |
| `docker-compose.algeria.prod.yml` | DZ | OK |
| `docker-compose.switzerland.yml` | CH | **SUPPRIMÉ** |
| `docker-compose.switzerland.prod.yml` | CH | **SUPPRIMÉ** |

**Verdict** : Seules les configurations Algérie sont présentes.

### 3.2 Configuration Algérie validée

```yaml
# docker-compose.algeria.yml
REGION: algeria
REGION_CODE: DZ
TZ: Africa/Algiers
PAYMENT_PROVIDER: chargily
PAYMENT_CURRENCY: DZD
ENABLE_DARIJA: true
ENABLE_ARABIC_RTL: true
LEGAL_FRAMEWORK: algeria
```

---

## 4. AUDIT BRANDING

### 4.1 packages/const/src/branding.ts

```typescript
// IAFactory Algeria - Plateforme IA tout-en-un
export const ORG_NAME = 'IAFactory Algeria';
export const BRANDING_EMAIL = {
  business: 'contact@iafactoryalgeria.com',
  support: 'support@iafactoryalgeria.com',
};
export const SOCIAL_URL = {
  linkedin: 'https://linkedin.com/company/iafactory-algeria',
  x: 'https://x.com/iafactorydz',
};
```

**Verdict** : OK - Branding correctement configuré pour Algérie.

### 4.2 Pricing (apps/landing/src/pages/Pricing.tsx)

| Élément | Valeur | Statut |
|---------|--------|--------|
| Devise | DZD | OK |
| Méthodes paiement | Chargily, CIB, BaridiMob, Dahabia | OK |
| Plan IDs | dz_starter, dz_pro, dz_business | OK |
| Langues | FR, EN, AR | OK |

---

## 5. AUDIT DÉPENDANCES

### 5.1 Dépendances Stripe

| Package | Présence | Commentaire |
|---------|----------|-------------|
| `stripe` | v17.7.0 | Présent dans package.json |
| `stripe_id` | DB schema | Colonne dans tables |

**Recommandation** : Stripe reste dans le code pour compatibilité LobeChat upstream. Pour Algérie, utiliser Chargily via l'API Gateway.

### 5.2 Packages à vérifier

```
packages/chargily-pay - Package Chargily personnalisé ✓
packages/credits-system - Système de crédits ✓
```

---

## 6. RÉFÉRENCES LOBEHUB

### 6.1 URLs externes

| URL | Fichier | Usage |
|-----|---------|-------|
| `chat-agents.lobehub.com` | .env.example | Market agents |
| `chat-plugins.lobehub.com` | .env.example | Market plugins |

**Verdict** : Normal pour un fork LobeChat. Peut être personnalisé si nécessaire.

---

## 7. ACTIONS CORRECTIVES

### 7.1 URGENTES (Sécurité)

```bash
# 1. Révoquer les API keys exposées
# Dans chaque dashboard provider, révoquer les clés actuelles

# 2. Ajouter apps/gateway/.env au .gitignore spécifique
echo "apps/gateway/.env" >> .gitignore

# 3. Vérifier que le fichier n'est pas déjà commité
git ls-files apps/gateway/.env
# Si résultat non vide, supprimer du tracking:
git rm --cached apps/gateway/.env
```

### 7.2 MAJEURES (Contenu)

```bash
# 1. Corriger video-studio README
# Fichier: apps/b2b/video-studio/README.md
# Ligne 9: Remplacer "Français/Allemand/Italien" par "Français/Arabe/Darija"

# 2. Nettoyer les docs
# Supprimer les sections Switzerland de:
# - docs/architecture/ARCHITECTURE_OPTIMALE.md
# - docs/migration/PLAN_MIGRATION_DETAILLE.md
```

### 7.3 MINEURES

```bash
# 1. Supprimer mention legacy Suisse
# Fichier: apps/b2b/video-studio/README.md
# Ligne 220: Supprimer "Legacy support: LUMA_API_KEY_SUISSE"

# 2. Nettoyer commentaire searxng
# Fichier: docker-compose/local/searxng-settings.yml
# Ligne 37: Supprimer "swisscows" de la liste
```

---

## 8. RÉSUMÉ FINAL

### Ce qui est OK

- Branding `packages/const/src/branding.ts` : IAFactory Algeria
- Pricing `apps/landing/` : DZD, Chargily
- Legal Landing : Droit algérien
- Legal Agents : Algérie uniquement
- Docker : Seules les configs Algeria présentes
- .gitignore : Règles .env correctes

### Ce qui doit être corrigé

| Priorité | Action | Fichier(s) |
|----------|--------|------------|
| **P0** | Révoquer API keys | apps/gateway/.env |
| **P1** | Supprimer refs Suisse | docs/architecture/, docs/migration/ |
| **P2** | Corriger langues | apps/b2b/video-studio/README.md |
| **P3** | Nettoyer commentaires | docker-compose/local/searxng-settings.yml |

---

## 9. VALIDATION POST-AUDIT

Après corrections, exécuter :

```bash
# Vérifier aucune référence Suisse dans le code source
grep -ri "suisse\|swiss\|switzerland" src/ apps/ packages/ --include="*.ts" --include="*.tsx"

# Vérifier branding
cat packages/const/src/branding.ts | grep ORG_NAME

# Vérifier aucun .env versionné
git ls-files "*.env"
```

---

**Fin du rapport d'audit**

*Document généré le 24/01/2026 par Claude Opus 4.5*
