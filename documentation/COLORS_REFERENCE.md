# 🎨 RÉFÉRENCE COULEURS - IA FACTORY ALGERIA

## VARIABLES CSS PRINCIPALES

```css
:root {
    /* ===== MODE LIGHT (par défaut) ===== */
    --bg-page: #ffffff;           /* Fond page */
    --bg-section: #ffffff;        /* Fond sections */
    --bg-card: #f8f9fa;           /* Fond cartes (blanc cassé) */
    --bg-secondary: #faf9f7;      /* Fond alternatif */
    --bg-input: #ffffff;          /* Fond inputs */
    
    --text-primary: #1a1a1a;      /* Texte principal */
    --text-secondary: #666666;    /* Texte secondaire */
    --text-muted: #999999;        /* Texte discret */
    
    --border-color: #e5e5e5;      /* Bordures */
    --border-hover: #006233;      /* Bordure hover */
    
    /* Couleurs Algérie */
    --green-primary: #006233;     /* Vert principal */
    --green-hover: #00873E;       /* Vert hover */
    --green-light: #4CB963;       /* Vert clair */
    --green-bg: #0d1f12;          /* Fond vert foncé */
    --green-accent: #008000;      /* Vert icônes */
    --red-algeria: #D52B1E;       /* Rouge algérien */
    
    /* Autres */
    --linkedin: #0077b5;
    --shadow: rgba(0, 0, 0, 0.1);
    --shadow-green: rgba(0, 98, 51, 0.15);
}

[data-theme="dark"] {
    /* ===== MODE DARK ===== */
    --bg-page: #0a0a0f;           /* Fond page */
    --bg-section: #0a0a0f;        /* Fond sections */
    --bg-card: #1a1a24;           /* Fond cartes */
    --bg-secondary: #12121a;      /* Fond alternatif */
    --bg-input: #0a0a0f;          /* Fond inputs */
    
    --text-primary: #ffffff;      /* Texte principal */
    --text-secondary: #a0a0a0;    /* Texte secondaire */
    --text-muted: #666666;        /* Texte discret */
    
    --border-color: #2a2a3a;      /* Bordures */
    --border-hover: #00873E;      /* Bordure hover */
    
    /* Couleurs Algérie (ajustées pour dark) */
    --green-primary: #00873E;     /* Vert principal */
    --green-hover: #4CB963;       /* Vert hover */
    --green-light: #4CB963;       /* Vert clair */
    
    --shadow: rgba(0, 0, 0, 0.3);
    --shadow-green: rgba(0, 135, 62, 0.3);
}
```

---

## 📋 TABLEAU RÉCAPITULATIF

| Élément | Light Mode | Dark Mode |
|---------|------------|-----------|
| **FONDS** |||
| Page / Body | `#ffffff` | `#0a0a0f` |
| Sections | `#ffffff` | `#0a0a0f` |
| Cartes | `#f8f9fa` | `#1a1a24` |
| Fond secondaire | `#faf9f7` | `#12121a` |
| Inputs | `#ffffff` | `#0a0a0f` |
| **TEXTES** |||
| Principal | `#1a1a1a` | `#ffffff` |
| Secondaire | `#666666` | `#a0a0a0` |
| Muted/Discret | `#999999` | `#666666` |
| **BORDURES** |||
| Normale | `#e5e5e5` | `#2a2a3a` |
| Hover | `#006233` | `#00873E` |
| **VERTS ALGÉRIE** |||
| Primaire | `#006233` | `#00873E` |
| Hover | `#00873E` | `#4CB963` |
| Icônes | `#008000` | `#008000` |
| Clair | `#4CB963` | `#4CB963` |
| **AUTRES** |||
| Rouge Algérie | `#D52B1E` | `#D52B1E` |
| LinkedIn | `#0077b5` | `#0077b5` |

---

## 🏗️ STRUCTURE PAR SECTION

```
┌─────────────────────────────────────────────────────────────┐
│                        HEADER                                │
│  Light: transparent → scroll: rgba(255,255,255,0.8)          │
│  Dark: transparent → scroll: rgba(10,10,15,0.8)              │
├─────────────────────────────────────────────────────────────┤
│                         HERO                                 │
│  Light: #ffffff                                              │
│  Dark: #0a0a0f                                               │
├─────────────────────────────────────────────────────────────┤
│                       SECTIONS                               │
│  Light: #ffffff (toutes)                                     │
│  Dark: #0a0a0f (toutes)                                      │
│                                                              │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐                     │
│   │  CARTE  │  │  CARTE  │  │  CARTE  │                     │
│   │ #f8f9fa │  │ #f8f9fa │  │ #f8f9fa │  ← Light            │
│   │ #1a1a24 │  │ #1a1a24 │  │ #1a1a24 │  ← Dark             │
│   └─────────┘  └─────────┘  └─────────┘                     │
├─────────────────────────────────────────────────────────────┤
│                        FOOTER                                │
│  Light: #faf9f7                                              │
│  Dark: #0a0a0f                                               │
└─────────────────────────────────────────────────────────────┘
```

## 🔘 BOUTONS

| Type | Light Mode | Dark Mode |
|------|------------|-----------|
| Primaire (vert) | bg: `#006233`, text: `#ffffff` | bg: `#00873E`, text: `#ffffff` |
| Primaire hover | bg: `#00873E` | bg: `#4CB963` |
| Secondaire | bg: transparent, border: `#e5e5e5`, text: `#1a1a1a` | bg: transparent, border: `#2a2a3a`, text: `#ffffff` |
| Ghost | bg: transparent, text: `#006233` | bg: transparent, text: `#4CB963` |

---

## 📝 CSS COPIER-COLLER

```css
/* ===== SECTIONS - FOND ===== */
.section,
.hero-section,
.features-section,
.privacy-section,
.testimonials-section,
.faq-section,
.cta-section,
.contact-section,
.models-section,
.pricing-section {
    background: #ffffff;
}

[data-theme="dark"] .section,
[data-theme="dark"] .hero-section,
[data-theme="dark"] .features-section,
[data-theme="dark"] .privacy-section,
[data-theme="dark"] .testimonials-section,
[data-theme="dark"] .faq-section,
[data-theme="dark"] .cta-section,
[data-theme="dark"] .contact-section,
[data-theme="dark"] .models-section,
[data-theme="dark"] .pricing-section {
    background: #0a0a0f;
}

/* ===== CARTES ===== */
.card,
.feature-card,
.privacy-card,
.testimonial-card,
.pricing-card,
.model-card,
.faq-item {
    background: #f8f9fa;
    border: 1px solid #e5e5e5;
    border-radius: 12px;
}

[data-theme="dark"] .card,
[data-theme="dark"] .feature-card,
[data-theme="dark"] .privacy-card,
[data-theme="dark"] .testimonial-card,
[data-theme="dark"] .pricing-card,
[data-theme="dark"] .model-card,
[data-theme="dark"] .faq-item {
    background: #1a1a24;
    border-color: #2a2a3a;
}

/* ===== TEXTES ===== */
h1, h2, h3, h4, h5, h6 {
    color: #1a1a1a;
}

[data-theme="dark"] h1,
[data-theme="dark"] h2,
[data-theme="dark"] h3,
[data-theme="dark"] h4,
[data-theme="dark"] h5,
[data-theme="dark"] h6 {
    color: #ffffff;
}

p, span, li {
    color: #666666;
}

[data-theme="dark"] p,
[data-theme="dark"] span,
[data-theme="dark"] li {
    color: #a0a0a0;
}

/* ===== BOUTON PRIMAIRE ===== */
.btn-primary {
    background: #006233;
    color: #ffffff;
    border: none;
}

.btn-primary:hover {
    background: #00873E;
}

[data-theme="dark"] .btn-primary {
    background: #00873E;
}

[data-theme="dark"] .btn-primary:hover {
    background: #4CB963;
}

/* ===== BOUTON SECONDAIRE ===== */
.btn-secondary {
    background: transparent;
    color: #1a1a1a;
    border: 1px solid #e5e5e5;
}

[data-theme="dark"] .btn-secondary {
    color: #ffffff;
    border-color: #2a2a3a;
}

/* ===== ICÔNES ALGÉRIE ===== */
.icon-algeria {
    background: #008000;
    color: #ffffff;
}

/* ===== LIENS ===== */
a {
    color: #006233;
}

a:hover {
    color: #00873E;
}

[data-theme="dark"] a {
    color: #4CB963;
}

[data-theme="dark"] a:hover {
    color: #4CB963;
}
```

---

## 🇩🇿 COULEURS DRAPEAU ALGÉRIEN

| Couleur | Code Hex | Usage |
|---------|----------|-------|
| 🟢 Vert | `#006233` | Boutons, liens, accents |
| ⚪ Blanc | `#ffffff` | Texte sur vert, fonds |
| 🔴 Rouge | `#D52B1E` | Badges, alertes, highlights |

---

**📌 NOTE:** Utiliser ces couleurs de manière cohérente sur toutes les pages de la documentation IAFactory Algeria pour maintenir une identité visuelle forte et professionnelle.
