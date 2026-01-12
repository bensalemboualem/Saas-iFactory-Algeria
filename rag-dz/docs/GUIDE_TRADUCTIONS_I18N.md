# 🌍 Guide des Traductions i18n IAFactory

## Vue d'ensemble

Ce guide explique comment implémenter le système de traduction trilingue (FR/EN/AR) dans les applications IAFactory.

## 📋 Système IAFactoryI18n

### 1. Structure du système

```javascript
const IAFactoryI18n = {
    currentLang: localStorage.getItem('iafactory_lang') || 'fr',
    
    translations: {
        // Clé: { fr: "texte français", en: "english text", ar: "النص العربي" }
        "key_name": { 
            fr: "Texte en français", 
            ar: "النص بالعربية", 
            en: "Text in English" 
        }
    },
    
    setLanguage(lang) {
        this.currentLang = lang;
        document.documentElement.lang = lang;
        // RTL pour l'arabe
        if (lang === 'ar') {
            document.documentElement.setAttribute('dir', 'rtl');
        } else {
            document.documentElement.setAttribute('dir', 'ltr');
        }
        this.updatePage();
    },
    
    updatePage() {
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (this.translations[key] && this.translations[key][this.currentLang]) {
                el.textContent = this.translations[key][this.currentLang];
            }
        });
    }
};
```

## 🔧 Implémentation pas à pas

### Étape 1: Ajouter le script i18n dans `<head>`

```html
<head>
    <!-- ... autres balises ... -->
    
    <!-- Système i18n IAFactory -->
    <script>
    const IAFactoryI18n = {
        currentLang: localStorage.getItem('iafactory_lang') || 'fr',
        
        translations: {
            // VOS TRADUCTIONS ICI
            "home": { fr: "Accueil", ar: "الرئيسية", en: "Home" },
            "apps": { fr: "Applications", ar: "التطبيقات", en: "Applications" }
            // ... etc
        },
        
        setLanguage(lang) {
            this.currentLang = lang;
            document.documentElement.lang = lang;
            if (lang === 'ar') {
                document.documentElement.setAttribute('dir', 'rtl');
            } else {
                document.documentElement.setAttribute('dir', 'ltr');
            }
            this.updatePage();
        },
        
        updatePage() {
            document.querySelectorAll('[data-i18n]').forEach(el => {
                const key = el.getAttribute('data-i18n');
                if (this.translations[key] && this.translations[key][this.currentLang]) {
                    el.textContent = this.translations[key][this.currentLang];
                }
            });
        }
    };
    </script>
</head>
```

### Étape 2: Ajouter les attributs data-i18n au HTML

```html
<!-- AVANT (texte en dur) -->
<h2>Accueil</h2>
<p>Bienvenue sur notre plateforme</p>

<!-- APRÈS (avec data-i18n) -->
<h2 data-i18n="home">Accueil</h2>
<p data-i18n="welcome">Bienvenue sur notre plateforme</p>
```

### Étape 3: Modifier la fonction changeLanguage

```javascript
function changeLanguage(lang) {
    const labels = { fr: 'FR', en: 'EN', ar: 'AR' };
    const langLabel = document.getElementById('langLabel');
    if (langLabel) langLabel.textContent = labels[lang] || 'FR';
    
    // Update active option
    document.querySelectorAll('.iaf-lang-option').forEach(option => {
        option.classList.remove('active');
        if (option.onclick.toString().includes(`'${lang}'`)) {
            option.classList.add('active');
        }
    });
    
    const menu = document.getElementById('langMenu');
    if (menu) menu.classList.remove('show');
    
    localStorage.setItem('iafactory_lang', lang);
    
    // ✅ IMPORTANT: Appeler IAFactoryI18n.setLanguage()
    IAFactoryI18n.setLanguage(lang);
}
```

### Étape 4: Initialiser au chargement de la page

```javascript
document.addEventListener('DOMContentLoaded', function() {
    // ... autres initialisations ...
    
    // Initialiser la langue depuis localStorage
    const savedLang = localStorage.getItem('iafactory_lang') || 'fr';
    IAFactoryI18n.setLanguage(savedLang);
});
```

## 📚 Catégories de traductions courantes

### Navigation
```javascript
"home": { fr: "Accueil", ar: "الرئيسية", en: "Home" },
"apps": { fr: "Applications", ar: "التطبيقات", en: "Applications" },
"ai_agents": { fr: "Agents IA", ar: "وكلاء الذكاء الاصطناعي", en: "AI Agents" },
"workflows": { fr: "Workflows", ar: "مسارات العمل", en: "Workflows" },
"pricing": { fr: "Tarifs", ar: "الأسعار", en: "Pricing" },
"docs": { fr: "Documentation", ar: "التوثيق", en: "Documentation" },
"contact": { fr: "Contact", ar: "اتصل بنا", en: "Contact" }
```

### Actions & Boutons
```javascript
"login": { fr: "Connexion", ar: "تسجيل الدخول", en: "Login" },
"logout": { fr: "Déconnexion", ar: "تسجيل الخروج", en: "Logout" },
"get_started": { fr: "Commencer", ar: "ابدأ", en: "Get Started" },
"try_free": { fr: "Essayer gratuitement", ar: "جرب مجاناً", en: "Try for free" },
"learn_more": { fr: "En savoir plus", ar: "اعرف المزيد", en: "Learn more" },
"download": { fr: "Télécharger", ar: "تحميل", en: "Download" },
"save": { fr: "Enregistrer", ar: "حفظ", en: "Save" },
"cancel": { fr: "Annuler", ar: "إلغاء", en: "Cancel" },
"confirm": { fr: "Confirmer", ar: "تأكيد", en: "Confirm" },
"send": { fr: "Envoyer", ar: "إرسال", en: "Send" }
```

### Statuts
```javascript
"active": { fr: "Actif", ar: "نشط", en: "Active" },
"inactive": { fr: "Inactif", ar: "غير نشط", en: "Inactive" },
"loading": { fr: "Chargement...", ar: "جاري التحميل...", en: "Loading..." },
"success": { fr: "Succès", ar: "نجاح", en: "Success" },
"error": { fr: "Erreur", ar: "خطأ", en: "Error" },
"pending": { fr: "En attente", ar: "قيد الانتظار", en: "Pending" },
"completed": { fr: "Terminé", ar: "مكتمل", en: "Completed" }
```

### Métriques & Performance
```javascript
"performance": { fr: "Performances", ar: "الأداء", en: "Performance" },
"availability": { fr: "Disponibilité", ar: "التوفر", en: "Availability" },
"latency": { fr: "Latence", ar: "الكمون", en: "Latency" },
"uptime": { fr: "Uptime", ar: "وقت التشغيل", en: "Uptime" },
"support": { fr: "Support", ar: "الدعم", en: "Support" },
"response_time": { fr: "Temps de réponse", ar: "وقت الاستجابة", en: "Response time" }
```

### Footer
```javascript
"footer_description": { 
    fr: "Plateforme IA souveraine pour institutions algériennes.", 
    ar: "منصة ذكاء اصطناعي سيادية للمؤسسات الجزائرية.", 
    en: "Sovereign AI platform for Algerian institutions." 
},
"links": { fr: "Liens", ar: "الروابط", en: "Links" },
"legal": { fr: "Légal", ar: "القانونية", en: "Legal" },
"privacy": { fr: "Confidentialité", ar: "الخصوصية", en: "Privacy" },
"terms": { fr: "Conditions", ar: "الشروط", en: "Terms" },
"legal_mentions": { fr: "Mentions légales", ar: "الإشعارات القانونية", en: "Legal mentions" },
"all_rights_reserved": { fr: "Tous droits réservés", ar: "جميع الحقوق محفوظة", en: "All rights reserved" },
"made_with_love": { fr: "Fait avec ❤️ pour l'Algérie", ar: "صُنع بـ ❤️ للجزائر", en: "Made with ❤️ for Algeria" }
```

## ✅ Checklist d'implémentation

- [ ] Script IAFactoryI18n ajouté dans `<head>`
- [ ] Dictionnaire de traductions complété
- [ ] Attributs `data-i18n` ajoutés sur tous les textes
- [ ] Fonction `changeLanguage()` modifiée pour appeler `IAFactoryI18n.setLanguage()`
- [ ] Initialisation au `DOMContentLoaded` avec `IAFactoryI18n.setLanguage(savedLang)`
- [ ] Support RTL pour l'arabe (direction automatique)
- [ ] Sélecteur de langue avec drapeaux 🇫🇷🇬🇧🇩🇿
- [ ] Sauvegarde dans localStorage
- [ ] Test de changement de langue en temps réel

## 🎯 Exemple complet: douanes-dz

Voir le fichier `apps/_archived/douanes-dz/index.html` pour un exemple complet d'implémentation.

### Navigation traduite
```html
<nav class="iaf-nav" role="navigation">
    <a href="../../iafactory-landing/index.html" class="iaf-nav-link">
        <i class="fa-solid fa-home iaf-nav-icon"></i>
        <span data-i18n="home">Accueil</span>
    </a>
    <a href="../../iafactory-landing/apps.html" class="iaf-nav-link">
        <i class="fa-solid fa-th iaf-nav-icon"></i>
        <span data-i18n="apps">Applications</span>
    </a>
</nav>
```

### Hero traduit
```html
<div class="hero">
    <h2 data-i18n="app_title">🛃 Douanes-DZ</h2>
    <p data-i18n="app_description">Application IAFactory Algeria</p>
    <div class="status-badge">
        <i class="fas fa-check-circle"></i>
        <span data-i18n="service_active">Service actif</span>
    </div>
</div>
```

## 🌐 Support RTL pour l'arabe

Le système gère automatiquement la direction RTL (right-to-left) pour l'arabe:

```javascript
if (lang === 'ar') {
    document.documentElement.setAttribute('dir', 'rtl');
} else {
    document.documentElement.setAttribute('dir', 'ltr');
}
```

Le CSS IAFactory Unified supporte déjà RTL avec:
```css
[dir="rtl"] .iaf-header-container { flex-direction: row-reverse; }
[dir="rtl"] .iaf-nav { margin-left: 0; margin-right: auto; }
```

## 🚀 Déploiement

1. **Test local**: Ouvrir la page dans le navigateur
2. **Vérifier les 3 langues**: Cliquer sur 🇫🇷, 🇬🇧, 🇩🇿
3. **Vérifier RTL**: Texte arabe aligné à droite
4. **Vérifier localStorage**: Langue conservée au rechargement
5. **Vérifier responsive**: Navigation mobile + sélecteur langue

## 📝 Notes importantes

- **Cohérence**: Utiliser les mêmes clés (`home`, `apps`, etc.) dans toutes les apps
- **Emojis**: Les emojis 🛃🎯⚡ ne changent pas, seulement le texte
- **Icônes FontAwesome**: Les icônes restent, seul le texte change
- **HTML dans traductions**: Éviter le HTML, utiliser `textContent` (sécurité)
- **Maintenance**: Centraliser les traductions communes dans un fichier partagé (futur)

## 🔄 Migration d'une app existante

1. Identifier tous les textes visibles
2. Créer les clés de traduction
3. Ajouter les traductions FR/EN/AR
4. Remplacer les textes par `<span data-i18n="key">Texte</span>`
5. Tester les 3 langues
6. Vérifier le mode sombre/clair avec chaque langue

---

**Documentation créée le**: 01/01/2026  
**Version**: 1.0  
**Auteur**: IAFactory Algeria Team  
**Contact**: support@iafactory-algeria.dz
