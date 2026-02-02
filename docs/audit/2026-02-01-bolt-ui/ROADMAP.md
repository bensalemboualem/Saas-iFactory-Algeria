# ROADMAP - Bolt UI Security & Quality
## IA Factory Algeria - Q1 2026

**Date**: 2026-02-01
**Scope**: apps/bolt-ui
**Durée totale**: 4 semaines (42h effort)

---

## 🎯 Objectif

Sécuriser et optimiser l'application Bolt UI avant mise en production pour IA Factory Algeria.

---

## 📅 Timeline

```
Semaine 1-2 │ SÉCURITÉ CRITIQUE      │ 23h │ 4 PRs
Semaine 3   │ QUALITÉ & TESTS        │ 19h │ 3 PRs
Semaine 4   │ PERFORMANCE & A11Y     │ 16h │ 4 PRs
───────────┼────────────────────────┼─────┼───────
Total       │ 3 Milestones           │ 58h │ 11 PRs
```

---

## 🚨 MILESTONE 1: Sécurité Critique (Semaines 1-2)

**Objectif**: Corriger les 4 vulnérabilités critiques
**Durée**: 10 jours ouvrés
**Effort**: 23 heures
**Risque**: MOYEN (patches isolés, tests de régression complets)

### Sprint 1.1: Command Injection (Jours 1-2)

**PR #1**: `security(bolt-ui): prevent command injection in E2B API`

- [ ] **Jour 1 Matin**: Appliquer patch `0001-fix-e2b-command-injection.patch`
- [ ] **Jour 1 AM**: Créer tests sécurité E2B
- [ ] **Jour 2 Matin**: Code review + corrections
- [ ] **Jour 2 AM**: Merge → staging

**Fichiers**:
- `apps/bolt-ui/app/routes/api.e2b.ts` (+24 lignes)
- `apps/bolt-ui/tests/api-e2b-security.spec.ts` (nouveau, 85 lignes)

**Tests**:
```bash
pnpm --filter bolt-ui vitest run tests/api-e2b-security.spec.ts
pnpm --filter bolt-ui test # Régression
```

**Validation**:
- ✅ Tous tests passent
- ✅ Code coverage >80% sur api.e2b.ts
- ✅ Pentest manuel injection réussie

**Rollback**: `git revert <commit>`

---

### Sprint 1.2: API Key Exposure (Jours 3-4)

**PR #2**: `security(bolt-ui): move API keys to server-only context`

⚠️ **BREAKING CHANGE**

- [ ] **Jour 3 Matin**: Appliquer patch `0002-fix-api-key-exposure.patch`
- [ ] **Jour 3 AM**: Créer route `/api/config/public`
- [ ] **Jour 4 Matin**: Migration code client vers proxies serveur
- [ ] **Jour 4 AM**: Build production + scan bundle

**Fichiers**:
- `apps/bolt-ui/vite.config.ts` (-6 lignes)
- `apps/bolt-ui/app/routes/api.config.public.ts` (nouveau)
- `apps/bolt-ui/tests/security/api-key-exposure.spec.ts` (nouveau)

**Migration Notes**:
```typescript
// Avant (CLIENT - VULNÉRABLE)
const key = process.env.OPENAI_API_KEY;

// Après (SERVER - SÉCURISÉ)
export const loader = async () => {
  const key = process.env.OPENAI_API_KEY;
  // Utiliser la clé dans le loader
};
```

**Tests**:
```bash
pnpm --filter bolt-ui build
grep -r "sk-\|ANTHROPIC" apps/bolt-ui/build/client/ || echo "✓ Safe"
pnpm --filter bolt-ui vitest run tests/security/api-key-exposure.spec.ts
```

**Validation**:
- ✅ Aucune clé dans bundle client
- ✅ Tests bundle scan passent
- ✅ API calls fonctionnent via proxies

---

### Sprint 1.3: CSP Headers (Jour 5)

**PR #3**: `security(bolt-ui): add Content Security Policy headers`

- [ ] **Jour 5 Matin**: Appliquer patch `0003-add-csp-headers.patch`
- [ ] **Jour 5 14h**: Créer utils/nonce.ts
- [ ] **Jour 5 16h**: Tests CSP headers
- [ ] **Jour 5 17h**: Merge

**Fichiers**:
- `apps/bolt-ui/app/root.tsx` (+30 lignes)
- `apps/bolt-ui/app/utils/nonce.ts` (nouveau)
- `apps/bolt-ui/tests/security/csp-headers.spec.ts` (nouveau)

**Tests**:
```bash
pnpm --filter bolt-ui dev
curl -I http://localhost:5192/ | grep -i csp
pnpm --filter bolt-ui vitest run tests/security/csp-headers.spec.ts
```

**Validation**:
- ✅ CSP header présent
- ✅ Nonce généré dynamiquement
- ✅ Pas de violations console browser

---

### Sprint 1.4: Rate Limiting (Jours 6-7)

**PR #4**: `feat(bolt-ui): add rate limiting to API routes`

- [ ] **Jour 6 Matin**: Installer `limiter` package
- [ ] **Jour 6 AM**: Créer `utils/rateLimit.ts`
- [ ] **Jour 7 Matin**: Appliquer à toutes routes API
- [ ] **Jour 7 AM**: Tests rate limiting

**Dépendance**:
```bash
pnpm --filter bolt-ui add limiter
```

**Fichiers**:
- `apps/bolt-ui/app/utils/rateLimit.ts` (nouveau)
- `apps/bolt-ui/app/routes/api.chat.ts` (+5 lignes)
- `apps/bolt-ui/app/routes/api.e2b.ts` (+5 lignes)
- `apps/bolt-ui/tests/api/rate-limiting.spec.ts` (nouveau)

**Configuration**:
```typescript
// 20 requêtes/minute par IP
rateLimit(ip, 20, 60000)
```

**Tests**:
```bash
# Spam test
for i in {1..25}; do curl -X POST http://localhost:5192/api/chat & done
# Doit retourner 429 après 20 requêtes
```

**Validation**:
- ✅ 429 Too Many Requests après limite
- ✅ Reset après fenêtre temporelle
- ✅ Par IP tracking fonctionne

---

### Sprint 1.5: Revue & Déploiement Staging (Jours 8-10)

- [ ] **Jour 8**: Tests d'intégration complets
- [ ] **Jour 9**: QA manuel + pentest
- [ ] **Jour 10**: Déploiement staging + monitoring

**Checklist Déploiement**:
- ✅ Toutes 4 PRs merged
- ✅ Suite de tests complète passe
- ✅ `pnpm audit` clean (ou moderate seulement)
- ✅ Build production réussit
- ✅ Sentry configuré (monitoring errors)

---

## ✅ MILESTONE 2: Qualité & Tests (Semaine 3)

**Objectif**: Améliorer couverture tests et qualité code
**Durée**: 5 jours ouvrés
**Effort**: 19 heures

### Sprint 2.1: Tests E2E (Jours 11-13)

**PR #5**: `test(bolt-ui): add E2E test suites with Playwright`

- [ ] **Jour 11**: Setup Playwright + config
- [ ] **Jour 12**: Créer 3 suites E2E (chat, deploy, editor)
- [ ] **Jour 13**: Tests error handling + CI integration

**Suites à créer**:
1. `tests/e2e/chat-flow.spec.ts` - Chat conversationnel
2. `tests/e2e/deployment.spec.ts` - GitHub/Netlify deploy
3. `tests/e2e/editor.spec.ts` - File editing, preview
4. `tests/e2e/error-handling.spec.ts` - Toasts, network errors
5. `tests/e2e/auth.spec.ts` - Login/logout flows

**Effort**: 12h

---

### Sprint 2.2: Sanitization HTML (Jour 14)

**PR #6**: `security(bolt-ui): sanitize HTML with DOMPurify`

- [ ] Installer `dompurify` + types
- [ ] Wrapper tous `dangerouslySetInnerHTML` (6 fichiers)
- [ ] Tests sanitization

**Effort**: 3h

---

### Sprint 2.3: Chiffrement localStorage (Jour 15)

**PR #7**: `security(bolt-ui): encrypt sensitive data in localStorage`

- [ ] Installer `crypto-js`
- [ ] Créer `utils/secureStorage.ts`
- [ ] Migrer GitHub/Netlify tokens

**Effort**: 4h

⚠️ **Note**: Users devront re-connecter leurs comptes

---

## 🚀 MILESTONE 3: Performance & Accessibilité (Semaine 4)

**Objectif**: Optimiser performance et conformité WCAG
**Durée**: 5 jours ouvrés
**Effort**: 16 heures

### Sprint 3.1: Self-Host Fonts (Jour 16)

**PR #8**: `perf(bolt-ui): self-host fonts to improve FCP`

**Effort**: 2h

**Objectif**: FCP < 1.8s, LCP < 2.5s

---

### Sprint 3.2: Lazy Loading (Jours 17-18)

**PR #9**: `perf(bolt-ui): lazy load heavy components`

- [ ] React.lazy() pour CodeMirror, xterm, Workbench
- [ ] Suspense boundaries
- [ ] Bundle analysis

**Effort**: 4h

**Objectif**: Initial bundle < 300KB

---

### Sprint 3.3: Accessibilité (Jour 19)

**PR #10**: `a11y(bolt-ui): fix WCAG violations`

- [ ] Labels ARIA pour boutons icon
- [ ] Tests axe-core
- [ ] Contraste couleurs

**Effort**: 8h

**Objectif**: 0 violations axe-core

---

### Sprint 3.4: i18n Validation (Jour 20)

**PR #11**: `feat(bolt-ui): add i18n translation validation`

- [ ] Schema Zod pour traductions
- [ ] Tests clés manquantes
- [ ] Fallback amélioration

**Effort**: 4h

---

## 📊 Métriques de Succès

### Sécurité
- ✅ 0 vulnérabilités CRITICAL/HIGH dans `pnpm audit`
- ✅ Pentest externe passé
- ✅ CSP configuré sans violations
- ✅ Rate limiting actif (logs confirmés)

### Qualité
- ✅ Code coverage > 70%
- ✅ E2E coverage sur flows critiques
- ✅ TypeScript strict mode activé

### Performance
- ✅ Lighthouse score > 90 (mobile)
- ✅ FCP < 1.8s
- ✅ Initial bundle < 300KB

### Accessibilité
- ✅ 0 violations axe-core
- ✅ Support clavier complet
- ✅ RTL support pour arabe

---

## 🛠️ Setup Développeur

### Environnement Requis
```bash
Node.js >= 18.18.0
pnpm 9.14.4
```

### Installation
```bash
# Clone repo
git clone <repo>
cd iafactorychatgpt_v2

# Install deps
pnpm install

# Setup env
cp apps/bolt-ui/.env.example apps/bolt-ui/.env.local
# Remplir les clés API

# Dev
pnpm --filter bolt-ui dev

# Tests
pnpm --filter bolt-ui test
pnpm --filter bolt-ui exec playwright test
```

---

## 📋 Checklist Pré-Production

### Sécurité
- [ ] Toutes PRs sécurité merged et testées
- [ ] Pentest externe effectué
- [ ] Secrets scan clean (`git-secrets`, `trufflehog`)
- [ ] CSP headers en production
- [ ] Rate limiting actif

### Tests
- [ ] Coverage > 70%
- [ ] E2E tests passent
- [ ] Tests de charge OK (100 concurrent users)

### Performance
- [ ] Lighthouse > 90
- [ ] Bundle size limites respectées
- [ ] CDN configuré (images, fonts)

### Monitoring
- [ ] Sentry configuré
- [ ] Logs structurés
- [ ] Alertes critiques setup

### Documentation
- [ ] README à jour
- [ ] API docs générées
- [ ] Runbook ops créé

---

## 🔄 Process de Release

```
develop → staging (auto deploy) → production (manual)
   ↓           ↓                      ↓
  PR       Auto tests            Smoke tests
          E2E suite              Rollback plan
```

### Stratégie Rollback
```bash
# Si problème en production
git revert <commit>
# OU
git reset --hard <previous-tag>
git push --force origin main

# Redéployer
pnpm build && deploy
```

---

## 👥 Responsabilités

| Rôle | Responsable | Tâches |
|------|-------------|--------|
| **Tech Lead** | TBD | Code review, architecture decisions |
| **Security** | TBD | Pentest, audit, CSP config |
| **QA** | TBD | Tests manuels, E2E scenarios |
| **DevOps** | TBD | CI/CD, déploiements, monitoring |

---

## 📞 Support & Questions

- **Audit Report**: `docs/audit/2026-02-01-bolt-ui/audit-report.md`
- **Patches**: `docs/audit/2026-02-01-bolt-ui/*.patch`
- **JSON Summary**: `docs/audit/2026-02-01-bolt-ui/summary.json`

---

**Dernière mise à jour**: 2026-02-01
**Prochaine revue**: Fin Milestone 1 (J+10)

---

## 🎯 Quick Start (Demain Matin)

```bash
# 1. Lire l'audit complet
code docs/audit/2026-02-01-bolt-ui/audit-report.md

# 2. Créer branch de travail
git checkout -b security/milestone-1

# 3. Appliquer premier patch
git apply docs/audit/2026-02-01-bolt-ui/0001-fix-e2b-command-injection.patch

# 4. Tester
pnpm --filter bolt-ui vitest run tests/api-e2b-security.spec.ts

# 5. Commit + Push
git add .
git commit -m "security(bolt-ui): prevent command injection in E2B API"
git push -u origin security/milestone-1

# 6. Créer PR sur GitHub
gh pr create --title "security(bolt-ui): prevent command injection in E2B API" \
             --body "Fixes F-001 from security audit. See docs/audit/2026-02-01-bolt-ui/"
```

**Bon courage ! 🚀**
