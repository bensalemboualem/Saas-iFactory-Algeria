# 🎴 EFFET CARTES - BORDURE VERTE ALGÉRIE + 3D

## 📋 Documentation Effet Cartes IAFactory Algeria

Cet effet s'applique sur **TOUTES les cartes** de toutes les pages de la documentation.

---

## 🎨 CSS - EFFET CARTES UNIVERSEL

### Style de Base

```css
/* ============================================
   CARTES - EFFET BORDURE VERTE + 3D
   ============================================ */

/* Style de base - Toutes les cartes */
.card,
.feature-card,
.privacy-card,
.testimonial-card,
.pricing-card,
.model-card,
.agent-card,
.app-card,
.workflow-card,
.faq-item,
.category-card,
[class*="-card"] {
    position: relative;
    background: #f8f9fa;
    border: 1px solid #e5e5e5;
    border-radius: 16px;
    padding: 24px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    overflow: hidden;
}

/* Bordure verte en haut (barre) */
.card::before,
.feature-card::before,
.privacy-card::before,
.testimonial-card::before,
.pricing-card::before,
.model-card::before,
.agent-card::before,
.app-card::before,
.workflow-card::before,
[class*="-card"]::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #006233 0%, #00873E 50%, #4CB963 100%);
    opacity: 0;
    transition: opacity 0.3s ease;
}

/* ===== HOVER EFFECT - LIGHT MODE ===== */
.card:hover,
.feature-card:hover,
.privacy-card:hover,
.testimonial-card:hover,
.pricing-card:hover,
.model-card:hover,
.agent-card:hover,
.app-card:hover,
.workflow-card:hover,
[class*="-card"]:hover {
    border-color: #006233;
    transform: translateY(-8px);
    box-shadow: 
        0 4px 6px rgba(0, 98, 51, 0.1),
        0 10px 20px rgba(0, 98, 51, 0.15),
        0 20px 40px rgba(0, 98, 51, 0.1);
}

/* Barre verte visible au hover */
.card:hover::before,
.feature-card:hover::before,
.privacy-card:hover::before,
.testimonial-card:hover::before,
.pricing-card:hover::before,
.model-card:hover::before,
.agent-card:hover::before,
.app-card:hover::before,
.workflow-card:hover::before,
[class*="-card"]:hover::before {
    opacity: 1;
}


/* ===== DARK MODE ===== */
[data-theme="dark"] .card,
[data-theme="dark"] .feature-card,
[data-theme="dark"] .privacy-card,
[data-theme="dark"] .testimonial-card,
[data-theme="dark"] .pricing-card,
[data-theme="dark"] .model-card,
[data-theme="dark"] .agent-card,
[data-theme="dark"] .app-card,
[data-theme="dark"] .workflow-card,
[data-theme="dark"] [class*="-card"] {
    background: #1a1a24;
    border-color: #2a2a3a;
}

/* Hover Dark Mode - Glow vert intense */
[data-theme="dark"] .card:hover,
[data-theme="dark"] .feature-card:hover,
[data-theme="dark"] .privacy-card:hover,
[data-theme="dark"] .testimonial-card:hover,
[data-theme="dark"] .pricing-card:hover,
[data-theme="dark"] .model-card:hover,
[data-theme="dark"] .agent-card:hover,
[data-theme="dark"] .app-card:hover,
[data-theme="dark"] .workflow-card:hover,
[data-theme="dark"] [class*="-card"]:hover {
    border-color: #00873E;
    transform: translateY(-8px);
    box-shadow: 
        0 4px 6px rgba(0, 135, 62, 0.2),
        0 10px 20px rgba(0, 135, 62, 0.25),
        0 20px 40px rgba(0, 135, 62, 0.15),
        0 0 30px rgba(76, 185, 99, 0.2);  /* Glow vert */
}

/* Bordure verte gradient en dark */
[data-theme="dark"] .card::before,
[data-theme="dark"] .feature-card::before,
[data-theme="dark"] .privacy-card::before,
[data-theme="dark"] .testimonial-card::before,
[data-theme="dark"] .pricing-card::before,
[data-theme="dark"] .model-card::before,
[data-theme="dark"] .agent-card::before,
[data-theme="dark"] .app-card::before,
[data-theme="dark"] .workflow-card::before,
[data-theme="dark"] [class*="-card"]::before {
    background: linear-gradient(90deg, #00873E 0%, #4CB963 50%, #00873E 100%);
}


/* ===== VARIANTE : CARTE FEATURED (mise en avant) ===== */
.card.featured,
.pricing-card.featured,
.agent-card.featured,
[class*="-card"].featured {
    border: 2px solid #006233;
    box-shadow: 
        0 4px 6px rgba(0, 98, 51, 0.1),
        0 10px 20px rgba(0, 98, 51, 0.1);
}

.card.featured::before,
.pricing-card.featured::before,
[class*="-card"].featured::before {
    opacity: 1;
    height: 5px;
}

[data-theme="dark"] .card.featured,
[data-theme="dark"] .pricing-card.featured,
[data-theme="dark"] [class*="-card"].featured {
    border-color: #00873E;
    box-shadow: 
        0 0 20px rgba(0, 135, 62, 0.3),
        0 10px 30px rgba(0, 135, 62, 0.2);
}


/* ===== EFFET 3D AVANCÉ (optionnel) ===== */
.card-3d,
.agent-card,
.app-card {
    transform-style: preserve-3d;
    perspective: 1000px;
}

.card-3d:hover,
.agent-card:hover,
.app-card:hover {
    transform: translateY(-8px) rotateX(2deg);
}

/* Ombre portée 3D */
.card-3d::after,
.agent-card::after,
.app-card::after {
    content: '';
    position: absolute;
    bottom: -10px;
    left: 5%;
    right: 5%;
    height: 20px;
    background: radial-gradient(ellipse at center, rgba(0, 98, 51, 0.2) 0%, transparent 70%);
    opacity: 0;
    transition: opacity 0.3s ease;
    z-index: -1;
    filter: blur(10px);
}

.card-3d:hover::after,
.agent-card:hover::after,
.app-card:hover::after {
    opacity: 1;
}

[data-theme="dark"] .card-3d::after,
[data-theme="dark"] .agent-card::after,
[data-theme="dark"] .app-card::after {
    background: radial-gradient(ellipse at center, rgba(76, 185, 99, 0.3) 0%, transparent 70%);
}
```

---

## 📊 RÉSUMÉ EFFETS

| État | Light Mode | Dark Mode |
|------|------------|-----------|
| **Normal** | Bordure `#e5e5e5`, fond `#f8f9fa` | Bordure `#2a2a3a`, fond `#1a1a24` |
| **Hover** | Bordure `#006233`, lift -8px, shadow vert | Bordure `#00873E`, lift -8px, glow vert |
| **Barre top** | Gradient vert (opacity 0→1 on hover) | Gradient vert clair |
| **Featured** | Bordure 2px `#006233`, barre visible | Bordure `#00873E` + glow |

---

## 🎯 CLASSES APPLICABLES

### Cartes Standard
- `.card` - Carte générique
- `.feature-card` - Carte de fonctionnalité
- `.privacy-card` - Carte confidentialité
- `.testimonial-card` - Carte témoignage
- `.pricing-card` - Carte tarif
- `.model-card` - Carte modèle IA
- `.faq-item` - Item FAQ

### Cartes Spécifiques Documentation
- `.agent-card` - Carte agent IA
- `.app-card` - Carte application
- `.workflow-card` - Carte workflow
- `.category-card` - Carte catégorie
- `[class*="-card"]` - Toute classe se terminant par "-card"

### Variantes
- `.featured` - Carte mise en avant (bordure visible permanente)
- `.card-3d` - Effet 3D avancé avec rotation

---

## 🎨 RÉSULTAT VISUEL

```
NORMAL :                          HOVER :
┌─────────────────────┐           ┌─────────────────────┐ ← barre verte
│                     │           │▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀│
│                     │           │                     │
│       CARTE         │    →      │       CARTE         │  ↑ lift -8px
│                     │           │                     │
│                     │           │                     │
└─────────────────────┘           └─────────────────────┘
                                  ░░░░░░░░░░░░░░░░░░░░░░░ ← shadow 3D
```

---

## 📝 PAGES CONCERNÉES

Cet effet s'applique automatiquement sur toutes les pages de la documentation:

### API Documentation (24 pages)
- ✅ FR: quick-start, response-format, models-pricing, error-codes, parameters, optimization, migration-openai, webhooks
- ✅ EN: Toutes les pages traduites
- ✅ AR: Toutes les pages traduites (RTL)

### Pages Principales
- ✅ index.html
- ✅ introduction.html
- ✅ installation.html
- ✅ tips-tricks.html
- ✅ best-practices/*
- ✅ integrations/*

### Future Pages
- apps.html (applications)
- agents.html (agents IA)
- workflows.html (workflows)
- tarifs.html (pricing)

---

## 💡 UTILISATION

### HTML Basique
```html
<div class="card">
    <h3>Titre de la carte</h3>
    <p>Contenu de la carte</p>
</div>
```

### Carte Featured (mise en avant)
```html
<div class="card featured">
    <h3>Plan Recommandé</h3>
    <p>Cette carte est mise en avant</p>
</div>
```

### Carte 3D
```html
<div class="card card-3d">
    <h3>Effet 3D</h3>
    <p>Rotation au hover</p>
</div>
```

---

## 🔧 PERSONNALISATION

### Modifier l'élévation au hover
```css
.card:hover {
    transform: translateY(-12px);  /* -8px par défaut */
}
```

### Modifier la couleur de la barre
```css
.card::before {
    background: linear-gradient(90deg, #006233 0%, #D52B1E 100%);
}
```

### Modifier le glow dark mode
```css
[data-theme="dark"] .card:hover {
    box-shadow: 0 0 50px rgba(76, 185, 99, 0.4);  /* Glow plus intense */
}
```

---

**📌 NOTE:** Ce CSS est déjà intégré dans `docs-theme.css`. Toutes les cartes utilisent automatiquement l'identité visuelle IAFactory Algeria 🇩🇿
