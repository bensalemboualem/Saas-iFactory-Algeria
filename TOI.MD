# TOI.MD - REPRISE SESSION LANDING PAGE IAFACTORY
# Date: 25 Janvier 2026
# A lire en premier pour reprendre le travail

# NE PAS TOUCHER AUX ICONES - CONFIGURATION FINALE

---

## ETAT ACTUEL DU PROJET

### Pages Landing Auditees et Corrigees

| Page | Statut | i18n | Notes |
|------|--------|------|-------|
| Home.tsx | OK | FR/EN/AR | Reference couleurs |
| Pricing.tsx | OK | FR/EN/AR | Reecrit complet avec i18n |
| B2B.tsx | OK | FR/EN/AR | Couleurs synchronisees |
| Tools.tsx | OK | UI traduite | Couleurs + YT enleves |
| Apps.tsx | OK | UI traduite | Couleurs synchronisees |
| Agents.tsx | OK | UI traduite | Couleurs synchronisees |
| Workflows.tsx | OK | UI traduite | Couleurs synchronisees |

---

## COULEURS SYNCHRONISEES (SESSION 25 JAN)

### Palette finale - Mode Dark
```css
--bg: #0A0F1A;
--bg2: #111827;
--text: #F8FAFC;
--muted: rgba(248,250,252,0.65);
--card: rgba(255,255,255,0.06);
--border: rgba(255,255,255,0.10);
--accent: #22C55E;
```

### Palette finale - Mode Light
```css
--bg: #F6F3EE;
--bg2: #FBF8F3;
--text: #141414;
--muted: rgba(20,20,20,0.62);
--card: #EDE9E3;        /* Beige sombre, pas blanc */
--border: rgba(20,20,20,0.10);
--accent: #1C7A5F;
```

### Fichiers mis a jour pour couleurs
- global.css (variables CSS globales)
- useTheme.ts (hook theme)
- Home.tsx (CSS vars inline)
- Pricing.tsx, Tools.tsx, Apps.tsx, Agents.tsx, Workflows.tsx, B2B.tsx

### Corrections specifiques
1. **Cartes mode clair**: blanc -> beige #EDE9E3
2. **Champs recherche**: blanc -> beige #EDE9E3
3. **Sections Pricing**: meme couleur que body
4. **Footer**: herite de global.css (transparent)
5. **Icon badge**: transparent, pas de gradient

---

## CORRECTIONS HOME.TSX (TERMINEES)

1. **Emojis supprimes** - Remplaces par icones Lucide
2. **Badge icone premium** - Transparent (pas de gradient)
3. **Light mode beige chaud**: #F6F3EE
4. **Footer ajoute** en bas de page
5. **DashboardMockup internationalise**
6. **Algeria section** - Reduit de 6 a 4 cartes

---

## TOOLS.TSX - VIDEOS YT SUPPRIMEES

- videoUrl enleve de l'interface Tool
- VideoThumbnail et VideoModal supprimes
- Fonctions YouTube utilitaires supprimees
- A refaire avec nos propres videos plus tard

---

## FICHIERS CLES

```
apps/landing/src/
├── pages/
│   ├── Home.tsx        <- Reference couleurs
│   ├── Pricing.tsx     <- OK
│   ├── B2B.tsx         <- OK
│   ├── Tools.tsx       <- OK (videos enlevees)
│   ├── Apps.tsx        <- OK
│   ├── Agents.tsx      <- OK
│   └── Workflows.tsx   <- OK
├── components/
│   ├── Header.tsx
│   └── Footer.tsx      <- Transparent
├── hooks/
│   └── useTheme.ts     <- Couleurs centralisees
└── global.css          <- Variables CSS globales
```

---

## PROCHAINES TACHES POTENTIELLES

1. **Internationaliser les donnees** de Tools/Apps/Agents/Workflows
   - Actuellement: noms et descriptions hardcodes en francais
   - A faire: ajouter traductions EN/AR pour les items

2. **Ajouter nos videos** dans Tools.tsx (remplacer YT)

3. **Verifier visuellement** sur http://localhost:5175/
   - Tester les 3 langues (FR/EN/AR)
   - Verifier RTL en arabe
   - Tester responsive mobile

---

## COMMANDES UTILES

```bash
# Dev server landing
cd apps/landing && pnpm dev

# Build
pnpm build

# Type check
bun run type-check
```

---

## NOTES IMPORTANTES

- Ne JAMAIS lancer `pnpm test` (trop long ~10min)
- Ne JAMAIS lancer `pnpm i18n` (gere par CI)
- Utiliser pnpm pour les deps, bun pour les scripts
- Port dev landing: 5175
- NE PAS TOUCHER AUX ICONES

---

# FIN - BONNE REPRISE!
