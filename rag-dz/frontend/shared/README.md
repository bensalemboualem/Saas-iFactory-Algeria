# IAFactory Design System - Guide d'Intégration

## Vue d'ensemble

Ce design system unifie l'identité visuelle de toutes les applications IAFactory (Algeria + Suisse).

**Source de vérité**: Landing Page iafactoryalgeria.com

## Fichiers Disponibles

| Fichier | Usage | Format |
|---------|-------|--------|
| `iafactory-design-system.css` | CSS Variables + Composants | CSS pur |
| `tailwind.iafactory.config.js` | Preset Tailwind CSS | JavaScript |
| `theme.config.ts` | Configuration TypeScript | TypeScript |
| `theme-toggle.js` | Utilitaire toggle Dark/Light | JavaScript |

## Installation Rapide

### Option 1: CSS Pur (HTML/Vanilla JS)

```html
<head>
  <!-- 1. Importer le design system -->
  <link rel="stylesheet" href="/shared/iafactory-design-system.css">

  <!-- 2. Ajouter le toggle theme -->
  <script src="/shared/theme-toggle.js"></script>
</head>
```

### Option 2: React/Vue avec Tailwind

```javascript
// tailwind.config.js
const iafactoryPreset = require('./shared/tailwind.iafactory.config.js');

module.exports = {
  presets: [iafactoryPreset],
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  // vos customisations...
};
```

### Option 3: Import TypeScript

```typescript
import { theme, colors, getThemeColors } from './shared/theme.config';

// Utilisation
const primaryColor = colors.primary.DEFAULT; // '#00a651'
const darkBg = colors.dark.bg; // '#020617'
```

## Palette de Couleurs

### Brand Colors (Drapeau Algérien)

| Couleur | Hex | Usage |
|---------|-----|-------|
| **Vert Primary** | `#00a651` | Boutons, liens, accents |
| **Vert Light** | `#00c761` | Hover states |
| **Vert Dark** | `#008c45` | Active states |
| **Rouge Danger** | `#ef4444` | Erreurs, suppressions |

### Dark Mode (Défaut)

| Variable | Valeur | Usage |
|----------|--------|-------|
| `--iaf-bg` | `#020617` | Background principal |
| `--iaf-text` | `#f8fafc` | Texte principal |
| `--iaf-border` | `rgba(255,255,255,0.12)` | Bordures |
| `--iaf-glass` | `rgba(255,255,255,0.08)` | Glassmorphism |

### Light Mode

| Variable | Valeur | Usage |
|----------|--------|-------|
| `--iaf-bg` | `#f7f5f0` | Background crème chaud |
| `--iaf-text` | `#0f172a` | Texte navy foncé |
| `--iaf-border` | `rgba(0,0,0,0.08)` | Bordures subtiles |

## Composants CSS

### Boutons

```html
<!-- Primary (Vert gradient) -->
<button class="iaf-btn iaf-btn-primary">Commencer</button>

<!-- Secondary (Outline) -->
<button class="iaf-btn iaf-btn-secondary">Annuler</button>

<!-- Ghost (Transparent) -->
<button class="iaf-btn iaf-btn-ghost">Options</button>

<!-- Danger (Rouge) -->
<button class="iaf-btn iaf-btn-danger">Supprimer</button>

<!-- Sizes -->
<button class="iaf-btn iaf-btn-primary iaf-btn-sm">Petit</button>
<button class="iaf-btn iaf-btn-primary iaf-btn-lg">Grand</button>
```

### Cards

```html
<div class="iaf-card">
  <div class="iaf-card-header">Titre</div>
  <div class="iaf-card-body">Contenu</div>
  <div class="iaf-card-footer">Actions</div>
</div>

<!-- Glass variant -->
<div class="iaf-card iaf-card-glass">
  Carte avec effet glassmorphism
</div>
```

### Inputs

```html
<input type="text" class="iaf-input" placeholder="Email">
<textarea class="iaf-input iaf-textarea" placeholder="Message"></textarea>
<select class="iaf-input iaf-select">
  <option>Option 1</option>
</select>
```

### Badges

```html
<span class="iaf-badge iaf-badge-primary">Nouveau</span>
<span class="iaf-badge iaf-badge-success">Actif</span>
<span class="iaf-badge iaf-badge-danger">Erreur</span>
<span class="iaf-badge iaf-badge-warning">Attention</span>
```

## Toggle Dark/Light Mode

### HTML

```html
<button onclick="IAFTheme.toggle()" data-theme-toggle>
  <i class="fas fa-sun theme-icon-sun"></i>
  <i class="fas fa-moon theme-icon-moon"></i>
</button>
```

### JavaScript

```javascript
// Toggle
IAFTheme.toggle();

// Set specific
IAFTheme.setTheme('dark');
IAFTheme.setTheme('light');

// Get current
const current = IAFTheme.getTheme(); // 'dark' ou 'light'

// Check
if (IAFTheme.isDark()) { /* ... */ }

// Listen for changes
window.addEventListener('themeChanged', (e) => {
  console.log('Theme changed to:', e.detail.theme);
});
```

## RTL Support (Arabe)

Le design system supporte automatiquement le mode RTL:

```html
<html dir="rtl" lang="ar">
```

Les classes s'adaptent automatiquement pour:
- Direction du texte
- Position des icônes
- Alignement des inputs

## Animations

```html
<div class="iaf-animate-fade-in">Fade in</div>
<div class="iaf-animate-slide-up">Slide up</div>
<div class="iaf-animate-scale-in">Scale in</div>
<div class="iaf-animate-pulse">Pulse (loading)</div>
<div class="iaf-animate-spin">Spin (spinner)</div>
```

## Variables CSS Disponibles

### Espacements
- `--iaf-spacing-xs`: 4px
- `--iaf-spacing-sm`: 8px
- `--iaf-spacing-md`: 12px
- `--iaf-spacing-lg`: 16px
- `--iaf-spacing-xl`: 24px

### Border Radius
- `--iaf-radius-sm`: 6px
- `--iaf-radius-md`: 8px
- `--iaf-radius-lg`: 10px
- `--iaf-radius-xl`: 12px
- `--iaf-radius-full`: 999px

### Shadows
- `--iaf-shadow-sm`: Légère
- `--iaf-shadow-md`: Moyenne
- `--iaf-shadow-lg`: Forte
- `--iaf-shadow-xl`: Très forte
- `--iaf-shadow-glow`: Effet glow vert

### Transitions
- `--iaf-transition-fast`: 150ms
- `--iaf-transition-base`: 250ms
- `--iaf-transition-slow`: 350ms

## Header Universel (IAFactoryHeader)

### Installation

```tsx
// Dans votre App.tsx ou Layout.tsx
import { IAFactoryHeader } from '@/shared/components/IAFactoryHeader';

function App() {
  return (
    <>
      <IAFactoryHeader />
      {/* Votre contenu */}
    </>
  );
}
```

### Props Disponibles

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `region` | `'dz' \| 'ch'` | Auto-détecté | Force la région (Algérie ou Suisse) |
| `showProfileToggle` | `boolean` | `true` | Affiche le toggle User/Dev |
| `showSocialLinks` | `boolean` | `true` | Affiche GitHub/HuggingFace |
| `navItems` | `NavItem[]` | Default | Custom navigation items |
| `loginUrl` | `string` | `/docs/login.html` | URL de connexion |
| `getStartedUrl` | `string` | `/docs/getstarted.html` | URL Get Started |
| `onProfileChange` | `(profile) => void` | - | Callback profil |
| `onLanguageChange` | `(lang) => void` | - | Callback langue |
| `onThemeChange` | `(theme) => void` | - | Callback thème |

### Détection Automatique de Région

Le header détecte automatiquement la région basée sur le hostname:
- `*.iafactory.ch` → Suisse (drapeau suisse)
- Autres → Algérie (drapeau algérien)

### Fonctionnalités Incluses

- **Sticky Header** - Reste en haut au scroll
- **Dark/Light Toggle** - Switch de thème intégré
- **i18n** - Support FR/EN/AR avec RTL automatique
- **Responsive** - Mobile menu hamburger inclus
- **Profile Toggle** - User/Developer mode
- **Social Links** - GitHub et Hugging Face

### Dossiers où copier le Header

Pour remplacer les headers existants:

```
frontend/rag-ui/src/components/layout/
frontend/archon-ui-new/src/components/layout/
frontend/archon-ui-stable/archon-ui-main/src/components/layout/
frontend/ia-factory-ui/components/
apps/*/components/ (pour les apps HTML)
```

### Version HTML (pour apps non-React)

```html
<!-- Copier depuis apps/landing/components/header-component.html -->
<link rel="stylesheet" href="/shared/components/header-styles.css">
<div id="header-container"></div>
<script>
  fetch('/shared/components/header-component.html')
    .then(r => r.text())
    .then(html => document.getElementById('header-container').innerHTML = html);
</script>
```

## Support

- GitHub: https://github.com/iafactory
- Email: support@iafactory.ch
