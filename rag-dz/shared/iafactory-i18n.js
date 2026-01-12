/**
 * IAFactory i18n System - Système multilingue centralisé
 * Support: FR / AR / EN
 * Usage: Inclure ce fichier dans toutes les apps Streamlit/React/HTML
 */

const IAFactoryI18n = {
    currentLang: localStorage.getItem('iafactory_lang') || 'fr',

    // Traductions communes à toutes les apps
    translations: {
        // Navigation & UI Commun
        "home": { fr: "Accueil", ar: "الرئيسية", en: "Home" },
        "back": { fr: "Retour", ar: "رجوع", en: "Back" },
        "next": { fr: "Suivant", ar: "التالي", en: "Next" },
        "submit": { fr: "Soumettre", ar: "إرسال", en: "Submit" },
        "cancel": { fr: "Annuler", ar: "إلغاء", en: "Cancel" },
        "save": { fr: "Enregistrer", ar: "حفظ", en: "Save" },
        "delete": { fr: "Supprimer", ar: "حذف", en: "Delete" },
        "edit": { fr: "Modifier", ar: "تعديل", en: "Edit" },
        "search": { fr: "Rechercher", ar: "بحث", en: "Search" },
        "filter": { fr: "Filtrer", ar: "تصفية", en: "Filter" },
        "download": { fr: "Télécharger", ar: "تنزيل", en: "Download" },
        "upload": { fr: "Téléverser", ar: "رفع", en: "Upload" },
        "loading": { fr: "Chargement...", ar: "جار التحميل...", en: "Loading..." },
        "error": { fr: "Erreur", ar: "خطأ", en: "Error" },
        "success": { fr: "Succès", ar: "نجاح", en: "Success" },
        "warning": { fr: "Attention", ar: "تحذير", en: "Warning" },
        "info": { fr: "Information", ar: "معلومات", en: "Information" },

        // Formulaires
        "name": { fr: "Nom", ar: "الاسم", en: "Name" },
        "email": { fr: "Email", ar: "البريد الإلكتروني", en: "Email" },
        "password": { fr: "Mot de passe", ar: "كلمة المرور", en: "Password" },
        "phone": { fr: "Téléphone", ar: "الهاتف", en: "Phone" },
        "address": { fr: "Adresse", ar: "العنوان", en: "Address" },
        "city": { fr: "Ville", ar: "المدينة", en: "City" },
        "country": { fr: "Pays", ar: "البلد", en: "Country" },
        "date": { fr: "Date", ar: "التاريخ", en: "Date" },
        "time": { fr: "Heure", ar: "الوقت", en: "Time" },
        "description": { fr: "Description", ar: "الوصف", en: "Description" },

        // Messages
        "welcome": { fr: "Bienvenue", ar: "مرحبا", en: "Welcome" },
        "thank_you": { fr: "Merci", ar: "شكرا", en: "Thank you" },
        "please_wait": { fr: "Veuillez patienter", ar: "يرجى الانتظار", en: "Please wait" },
        "no_results": { fr: "Aucun résultat", ar: "لا توجد نتائج", en: "No results" },
        "confirm": { fr: "Confirmer", ar: "تأكيد", en: "Confirm" },

        // IAFactory spécifique
        "powered_by": { fr: "Propulsé par IAFactory", ar: "مدعوم من IAFactory", en: "Powered by IAFactory" },
        "algeria": { fr: "Algérie", ar: "الجزائر", en: "Algeria" },
        "contact_support": { fr: "Contacter le support", ar: "اتصل بالدعم", en: "Contact support" },
    },

    init() {
        // Appliquer la langue sauvegardée
        this.setLanguage(this.currentLang, false);

        // Écouter les événements de changement de langue
        document.addEventListener('DOMContentLoaded', () => {
            const langButtons = document.querySelectorAll('.lang-btn');
            langButtons.forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const lang = e.currentTarget.dataset.lang;
                    this.setLanguage(lang);
                });
            });

            // Appliquer les traductions initiales
            this.applyTranslations();
        });

        // Écouter les changements de langue depuis d'autres onglets
        window.addEventListener('storage', (e) => {
            if (e.key === 'iafactory_lang' && e.newValue) {
                this.setLanguage(e.newValue, false);
            }
        });
    },

    setLanguage(lang, save = true) {
        this.currentLang = lang;

        if (save) {
            localStorage.setItem('iafactory_lang', lang);
        }

        // Mettre à jour HTML lang et dir
        document.documentElement.lang = lang;
        document.documentElement.dir = (lang === 'ar') ? 'rtl' : 'ltr';

        // Ajouter/retirer classe RTL
        if (lang === 'ar') {
            document.body.classList.add('rtl');
        } else {
            document.body.classList.remove('rtl');
        }

        // Appliquer les traductions
        this.applyTranslations();

        // Mettre à jour boutons actifs
        document.querySelectorAll('.lang-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.lang === lang);
        });

        // Événement custom pour les apps
        window.dispatchEvent(new CustomEvent('languageChanged', {
            detail: { lang, direction: (lang === 'ar') ? 'rtl' : 'ltr' }
        }));

        // Streamlit compatibility (si dans Streamlit)
        if (window.parent && window.parent.postMessage) {
            window.parent.postMessage({
                type: 'streamlit:languageChanged',
                lang: lang
            }, '*');
        }
    },

    applyTranslations() {
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.dataset.i18n;
            const translation = this.t(key);

            if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                if (el.dataset.i18nPlaceholder) {
                    el.placeholder = translation;
                } else {
                    el.value = translation;
                }
            } else {
                el.textContent = translation;
            }
        });

        // Appliquer traductions pour les placeholders
        document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
            const key = el.dataset.i18nPlaceholder;
            el.placeholder = this.t(key);
        });

        // Appliquer traductions pour les titres
        document.querySelectorAll('[data-i18n-title]').forEach(el => {
            const key = el.dataset.i18nTitle;
            el.title = this.t(key);
        });
    },

    t(key) {
        const translation = this.translations[key];
        if (!translation) {
            console.warn(`[i18n] Translation missing for key: ${key}`);
            return key;
        }
        return translation[this.currentLang] || translation['fr'] || key;
    },

    getCurrentLang() {
        return this.currentLang;
    },

    getDirection() {
        return (this.currentLang === 'ar') ? 'rtl' : 'ltr';
    },

    // Ajouter des traductions dynamiquement
    addTranslations(newTranslations) {
        Object.keys(newTranslations).forEach(key => {
            this.translations[key] = newTranslations[key];
        });
        this.applyTranslations();
    }
};

// Auto-init si on n'est pas dans Streamlit
if (typeof Streamlit === 'undefined') {
    IAFactoryI18n.init();
}

// Export pour utilisation ES6
if (typeof module !== 'undefined' && module.exports) {
    module.exports = IAFactoryI18n;
}
