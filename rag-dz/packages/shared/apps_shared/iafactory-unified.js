/**
 * IAFactory Algeria - Unified Components JS
 * Header, Footer, Chatbot Help, i18n
 * Trilingue: FR / AR / EN avec RTL
 * Version: 2.0 - Synchronized with Landing Page (Dec 2025)
 */

(function() {
    'use strict';

    // ========== TRANSLATIONS (Complete) ==========
    const IAF_TRANSLATIONS = {
        fr: {
            // Header Navigation
            home: "Accueil",
            pricing: "Tarifs",
            apps: "Applications",
            ai_agents: "Agents IA",
            workflows: "Workflows",
            docs: "Documentation",

            // Profile Toggle
            user: "Utilisateur",
            developer: "Développeur",

            // Auth
            login: "Log in",
            get_started: "Get Started",

            // Footer
            desc: "Plateforme IA souveraine pour l'Algérie. Applications intelligentes, agents IA, RAG Assistants et workflows automatisés pour institutions algériennes, public et privé.",
            location: "Alger, Algérie",
            products: "Produits",
            agents: "Agents IA",
            api: "API",
            rag: "RAG Assistants",
            dev_tools: "Developer Tools",
            directory: "Directory IA",
            ia_tools: "Outils IA",
            daily_news: "Daily News",
            resources: "Ressources",
            getstarted: "Démarrage rapide",
            blog: "Blog",
            support: "Support",
            company: "Entreprise",
            about: "À propos",
            contact: "Contact",
            newsletter: "Newsletter",
            legal: "Légal",
            mentions: "Mentions légales",
            privacy: "Confidentialité",
            terms: "CGU",
            rights: "Tous droits réservés.",
            made: "Fait avec",
            for: "pour l'Algérie",

            // Chatbot
            help_label: "Dzir IA - Aide",
            help_title: "Dzir IA",
            help_chat_ai: "Chat IA",
            help_rag_search: "Recherche RAG",
            help_support: "Support",
            help_welcome: "Bonjour ! Je suis <strong>Dzir IA</strong>, votre assistant IAFactory Algeria. Comment puis-je vous aider ?",
            help_placeholder: "Tapez votre message...",
            help_thinking: "Réflexion...",
            help_error: "Erreur de connexion",
            help_business_dz: "Business DZ (Algérie)",
            help_school_ch: "École (Suisse)",
            help_islam: "Islam (Global)",
            help_all_rags: "Tous les RAG",
            help_support_banner: "Mode support humain activé",
            help_back_to_ai: "Revenir au mode IA",

            // Language
            langFr: "Français",
            langEn: "English",
            langAr: "العربية"
        },
        en: {
            // Header Navigation
            home: "Home",
            pricing: "Pricing",
            apps: "Applications",
            ai_agents: "AI Agents",
            workflows: "Workflows",
            docs: "Documentation",

            // Profile Toggle
            user: "User",
            developer: "Developer",

            // Auth
            login: "Log in",
            get_started: "Get Started",

            // Footer
            desc: "Sovereign AI platform for Algeria. Smart applications, AI agents, RAG Assistants and automated workflows for Algerian institutions, public and private.",
            location: "Algiers, Algeria",
            products: "Products",
            agents: "AI Agents",
            api: "API",
            rag: "RAG Assistants",
            dev_tools: "Developer Tools",
            directory: "AI Directory",
            ia_tools: "AI Tools",
            daily_news: "Daily News",
            resources: "Resources",
            getstarted: "Quick Start",
            blog: "Blog",
            support: "Support",
            company: "Company",
            about: "About",
            contact: "Contact",
            newsletter: "Newsletter",
            legal: "Legal",
            mentions: "Legal Notice",
            privacy: "Privacy",
            terms: "Terms",
            rights: "All rights reserved.",
            made: "Made with",
            for: "for Algeria",

            // Chatbot
            help_label: "Dzir AI - Help",
            help_title: "Dzir AI",
            help_chat_ai: "AI Chat",
            help_rag_search: "RAG Search",
            help_support: "Support",
            help_welcome: "Hello! I'm <strong>Dzir AI</strong>, your IAFactory Algeria assistant. How can I help you?",
            help_placeholder: "Type your message...",
            help_thinking: "Thinking...",
            help_error: "Connection error",
            help_business_dz: "Business DZ (Algeria)",
            help_school_ch: "School (Switzerland)",
            help_islam: "Islam (Global)",
            help_all_rags: "All RAGs",
            help_support_banner: "Human support mode activated",
            help_back_to_ai: "Back to AI mode",

            // Language
            langFr: "Français",
            langEn: "English",
            langAr: "العربية"
        },
        ar: {
            // Header Navigation
            home: "الرئيسية",
            pricing: "الأسعار",
            apps: "التطبيقات",
            ai_agents: "وكلاء الذكاء",
            workflows: "سير العمل",
            docs: "التوثيق",

            // Profile Toggle
            user: "مستخدم",
            developer: "مطور",

            // Auth
            login: "تسجيل الدخول",
            get_started: "ابدأ الآن",

            // Footer
            desc: "منصة ذكاء اصطناعي سيادية للجزائر. تطبيقات ذكية، وكلاء ذكاء اصطناعي، مساعدات RAG وسير عمل آلي للمؤسسات الجزائرية العامة والخاصة.",
            location: "الجزائر العاصمة، الجزائر",
            products: "المنتجات",
            agents: "وكلاء الذكاء",
            api: "واجهة البرمجة",
            rag: "مساعدات RAG",
            dev_tools: "أدوات المطورين",
            directory: "دليل الذكاء",
            ia_tools: "أدوات الذكاء",
            daily_news: "أخبار يومية",
            resources: "الموارد",
            getstarted: "البدء السريع",
            blog: "المدونة",
            support: "الدعم",
            company: "الشركة",
            about: "حولنا",
            contact: "اتصل بنا",
            newsletter: "النشرة الإخبارية",
            legal: "قانوني",
            mentions: "إشعارات قانونية",
            privacy: "الخصوصية",
            terms: "الشروط",
            rights: "جميع الحقوق محفوظة.",
            made: "صنع بـ",
            for: "للجزائر",

            // Chatbot
            help_label: "ذزير ذكاء - مساعدة",
            help_title: "ذزير ذكاء",
            help_chat_ai: "دردشة ذكية",
            help_rag_search: "بحث RAG",
            help_support: "دعم",
            help_welcome: "مرحباً! أنا <strong>ذزير ذكاء</strong>، مساعدك من IAFactory الجزائر. كيف يمكنني مساعدتك؟",
            help_placeholder: "اكتب رسالتك...",
            help_thinking: "جاري التفكير...",
            help_error: "خطأ في الاتصال",
            help_business_dz: "أعمال الجزائر",
            help_school_ch: "مدرسة (سويسرا)",
            help_islam: "إسلام (عالمي)",
            help_all_rags: "جميع RAG",
            help_support_banner: "تم تفعيل وضع الدعم البشري",
            help_back_to_ai: "العودة لوضع الذكاء",

            // Language
            langFr: "Français",
            langEn: "English",
            langAr: "العربية"
        }
    };

    // ========== i18n CLASS ==========
    class IAFactoryI18n {
        constructor() {
            this.currentLang = localStorage.getItem('iafactory_lang') || 'fr';
            this.translations = IAF_TRANSLATIONS;
        }

        setLanguage(lang) {
            if (!this.translations[lang]) return;
            this.currentLang = lang;
            localStorage.setItem('iafactory_lang', lang);

            // Set RTL for Arabic
            document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
            document.documentElement.lang = lang;

            // Update all translatable elements
            this.updateDOM();

            // Dispatch event
            window.dispatchEvent(new CustomEvent('languageChanged', { detail: { lang } }));
        }

        t(key) {
            return this.translations[this.currentLang]?.[key] || this.translations['fr']?.[key] || key;
        }

        updateDOM() {
            document.querySelectorAll('[data-i18n]').forEach(el => {
                const key = el.getAttribute('data-i18n');
                const translation = this.t(key);
                if (el.hasAttribute('data-i18n-html') || el.getAttribute('data-i18n-html') === 'true') {
                    el.innerHTML = translation;
                } else {
                    el.textContent = translation;
                }
            });

            document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
                el.placeholder = this.t(el.getAttribute('data-i18n-placeholder'));
            });

            // Update select options
            document.querySelectorAll('[data-i18n-option]').forEach(el => {
                const key = el.getAttribute('data-i18n-option');
                el.textContent = this.t(key);
            });
        }

        getLang() {
            return this.currentLang;
        }
    }

    // ========== SOCIAL ICONS SVG ==========
    const SOCIAL_ICONS = {
        tiktok: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5 20.1a6.34 6.34 0 0 0 10.86-4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1-.1z"/></svg>',
        youtube: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>',
        instagram: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>',
        facebook: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>',
        linkedin: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>',
        twitter: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>',
        discord: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028c.462-.63.874-1.295 1.226-1.994.021-.041.001-.09-.041-.106a13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"/></svg>',
        reddit: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0zm5.01 4.744c.688 0 1.25.561 1.25 1.249a1.25 1.25 0 0 1-2.498.056l-2.597-.547-.8 3.747c1.824.07 3.48.632 4.674 1.488.308-.309.73-.491 1.207-.491.968 0 1.754.786 1.754 1.754 0 .716-.435 1.333-1.01 1.614a3.111 3.111 0 0 1 .042.52c0 2.694-3.13 4.87-7.004 4.87-3.874 0-7.004-2.176-7.004-4.87 0-.183.015-.366.043-.534A1.748 1.748 0 0 1 4.028 12c0-.968.786-1.754 1.754-1.754.463 0 .898.196 1.207.49 1.207-.883 2.878-1.43 4.744-1.487l.885-4.182a.342.342 0 0 1 .14-.197.35.35 0 0 1 .238-.042l2.906.617a1.214 1.214 0 0 1 1.108-.701zM9.25 12C8.561 12 8 12.562 8 13.25c0 .687.561 1.248 1.25 1.248.687 0 1.248-.561 1.248-1.249 0-.688-.561-1.249-1.249-1.249zm5.5 0c-.687 0-1.248.561-1.248 1.25 0 .687.561 1.248 1.249 1.248.688 0 1.249-.561 1.249-1.249 0-.687-.562-1.249-1.25-1.249zm-5.466 3.99a.327.327 0 0 0-.231.094.33.33 0 0 0 0 .463c.842.842 2.484.913 2.961.913.477 0 2.105-.056 2.961-.913a.361.361 0 0 0 .029-.463.33.33 0 0 0-.464 0c-.547.533-1.684.73-2.512.73-.828 0-1.979-.196-2.512-.73a.326.326 0 0 0-.232-.095z"/></svg>',
        telegram: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/></svg>',
        whatsapp: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>',
        github: '<i class="fa-brands fa-github"></i>',
        huggingface: '<span class="hf-icon">🤗</span>'
    };

    // ========== UNIFIED COMPONENTS CLASS ==========
    class IAFactoryComponents {
        constructor() {
            this.i18n = new IAFactoryI18n();
            this.chatMode = 'chat';
            this.chatOpen = false;
            this.avatarUrl = '/assets/images/lala-fatma.png';
        }

        // ========== HEADER GENERATOR ==========
        generateHeader(options = {}) {
            const currentPage = options.currentPage || '';
            const showNav = options.showNav !== false;
            const showProfileToggle = options.showProfileToggle !== false;
            const showSocialLinks = options.showSocialLinks !== false;
            const showAuthButtons = options.showAuthButtons !== false;

            return `
                <header class="iaf-header" role="banner">
                    <div class="iaf-header-container">
                        <!-- Logo -->
                        <a href="/" class="iaf-header-logo" dir="ltr">
                            <img src="https://flagcdn.com/w40/dz.png" alt="Algérie" class="iaf-logo-flag">
                            <span class="iaf-logo-text"><span class="letter i-drop" style="color: #00a651;"><span class="i-stem">ı</span><span class="i-dot">•</span></span><span class="letter" style="color: #00a651;">A</span><span class="letter" style="color: var(--iaf-text);">F</span><span class="letter" style="color: var(--iaf-text);">a</span><span class="letter" style="color: var(--iaf-text);">c</span><span class="letter" style="color: var(--iaf-text);">t</span><span class="letter" style="color: var(--iaf-text);">o</span><span class="letter" style="color: #ef4444;">r</span><span class="letter" style="color: #ef4444;">y</span> <span class="letter" style="color: var(--iaf-text);">A</span><span class="letter" style="color: var(--iaf-text);">l</span><span class="letter" style="color: var(--iaf-text);">g</span><span class="letter" style="color: var(--iaf-text);">e</span><span class="letter" style="color: var(--iaf-text);">r</span><span class="letter i-drop" style="color: #00a651;"><span class="i-stem">ı</span><span class="i-dot">•</span></span><span class="letter" style="color: #00a651;">a</span></span>
                        </a>

                        ${showNav ? `
                        <!-- Navigation -->
                        <nav class="iaf-nav" role="navigation">
                            <a href="/docs/tarifs.html" class="iaf-nav-link ${currentPage === 'pricing' ? 'active' : ''}">
                                <i class="fa-solid fa-tags iaf-nav-icon"></i>
                                <span data-i18n="pricing">${this.i18n.t('pricing')}</span>
                            </a>
                            <a href="/apps.html" class="iaf-nav-link ${currentPage === 'apps' ? 'active' : ''}">
                                <i class="fa-solid fa-th iaf-nav-icon"></i>
                                <span data-i18n="apps">${this.i18n.t('apps')}</span>
                            </a>
                            <a href="/docs/directory/agents.html" class="iaf-nav-link ${currentPage === 'agents' ? 'active' : ''}">
                                <i class="fa-solid fa-robot iaf-nav-icon"></i>
                                <span data-i18n="ai_agents">${this.i18n.t('ai_agents')}</span>
                            </a>
                            <a href="/docs/directory/workflows.html" class="iaf-nav-link ${currentPage === 'workflows' ? 'active' : ''}">
                                <i class="fa-solid fa-diagram-project iaf-nav-icon"></i>
                                <span data-i18n="workflows">${this.i18n.t('workflows')}</span>
                            </a>
                        </nav>
                        ` : ''}

                        <!-- Header Actions -->
                        <div class="iaf-header-actions">
                            ${showProfileToggle ? `
                            <!-- Profile Toggle -->
                            <div class="iaf-profile-toggle" role="tablist">
                                <button class="iaf-profile-btn active" data-profile="user" onclick="IAFactory.switchProfile('user')">
                                    <i class="fa-solid fa-user iaf-profile-icon"></i>
                                    <span data-i18n="user">${this.i18n.t('user')}</span>
                                </button>
                                <button class="iaf-profile-btn" data-profile="dev" onclick="IAFactory.switchProfile('dev')">
                                    <i class="fa-solid fa-code iaf-profile-icon"></i>
                                    <span data-i18n="developer">${this.i18n.t('developer')}</span>
                                </button>
                            </div>
                            ` : ''}

                            <!-- Language Selector -->
                            <div class="iaf-language-selector">
                                <button class="iaf-lang-btn" onclick="IAFactory.toggleLangMenu(event)" aria-expanded="false">
                                    <i class="fa-solid fa-globe iaf-lang-icon"></i>
                                    <span class="iaf-lang-label">${this.i18n.getLang().toUpperCase()}</span>
                                    <i class="fa-solid fa-chevron-down iaf-lang-chevron"></i>
                                </button>
                                <div class="iaf-lang-menu" id="iaf-lang-menu" role="menu">
                                    <button class="iaf-lang-option ${this.i18n.getLang() === 'fr' ? 'active' : ''}" onclick="IAFactory.setLanguage('fr')">
                                        <span class="iaf-lang-flag">🇫🇷</span>
                                        <span>Français</span>
                                        <i class="fa-solid fa-check iaf-lang-check"></i>
                                    </button>
                                    <button class="iaf-lang-option ${this.i18n.getLang() === 'en' ? 'active' : ''}" onclick="IAFactory.setLanguage('en')">
                                        <span class="iaf-lang-flag">🇬🇧</span>
                                        <span>English</span>
                                        <i class="fa-solid fa-check iaf-lang-check"></i>
                                    </button>
                                    <button class="iaf-lang-option ${this.i18n.getLang() === 'ar' ? 'active' : ''}" onclick="IAFactory.setLanguage('ar')" dir="rtl">
                                        <span class="iaf-lang-flag">🇩🇿</span>
                                        <span>العربية</span>
                                        <i class="fa-solid fa-check iaf-lang-check"></i>
                                    </button>
                                </div>
                            </div>

                            ${showSocialLinks ? `
                            <!-- Social Links -->
                            <div class="iaf-social-links">
                                <a href="https://github.com/IAFactory-Algeria" class="iaf-social-link" target="_blank" rel="noopener noreferrer" title="GitHub">
                                    <i class="fa-brands fa-github"></i>
                                </a>
                                <a href="https://huggingface.co/IAFactory-Algeria" class="iaf-social-link" target="_blank" rel="noopener noreferrer" title="Hugging Face">
                                    <span class="hf-icon">🤗</span>
                                </a>
                            </div>
                            ` : ''}

                            ${showAuthButtons ? `
                            <!-- Auth Buttons -->
                            <div class="iaf-auth-buttons">
                                <a href="/docs/login.html" class="iaf-btn iaf-btn-secondary">
                                    <i class="fa-solid fa-arrow-right-to-bracket iaf-btn-icon"></i>
                                    <span data-i18n="login">${this.i18n.t('login')}</span>
                                </a>
                                <a href="/docs/getstarted.html" class="iaf-btn iaf-btn-primary">
                                    <i class="fa-solid fa-rocket iaf-btn-icon"></i>
                                    <span data-i18n="get_started">${this.i18n.t('get_started')}</span>
                                </a>
                            </div>
                            ` : ''}

                            <!-- Mobile Menu Button -->
                            <button class="iaf-mobile-menu-btn" onclick="IAFactory.toggleMobileMenu()" aria-label="Menu">
                                <span class="iaf-burger-line"></span>
                                <span class="iaf-burger-line"></span>
                                <span class="iaf-burger-line"></span>
                            </button>
                        </div>
                    </div>

                    <!-- Mobile Menu -->
                    <div class="iaf-mobile-menu" id="iaf-mobile-menu">
                        <div class="iaf-mobile-menu-header">
                            <div class="iaf-mobile-logo">
                                <img src="https://flagcdn.com/w40/dz.png" alt="Algeria" width="28" height="21">
                                <span>IAFactory DZ</span>
                            </div>
                            <button class="iaf-mobile-close" onclick="IAFactory.toggleMobileMenu()">✕</button>
                        </div>
                        <nav class="iaf-mobile-nav">
                            <a href="/docs/tarifs.html" class="iaf-mobile-link"><span class="iaf-mobile-icon">💰</span><span data-i18n="pricing">${this.i18n.t('pricing')}</span></a>
                            <a href="/apps.html" class="iaf-mobile-link"><span class="iaf-mobile-icon">📱</span><span data-i18n="apps">${this.i18n.t('apps')}</span></a>
                            <a href="/docs/directory/agents.html" class="iaf-mobile-link"><span class="iaf-mobile-icon">🤖</span><span data-i18n="ai_agents">${this.i18n.t('ai_agents')}</span></a>
                            <a href="/docs/directory/workflows.html" class="iaf-mobile-link"><span class="iaf-mobile-icon">⚡</span><span data-i18n="workflows">${this.i18n.t('workflows')}</span></a>
                            <div class="iaf-mobile-divider"></div>
                            <a href="/docs/login.html" class="iaf-mobile-link"><span class="iaf-mobile-icon">🔑</span><span data-i18n="login">${this.i18n.t('login')}</span></a>
                            <a href="/docs/getstarted.html" class="iaf-mobile-link iaf-mobile-link-primary"><span class="iaf-mobile-icon">🚀</span><span data-i18n="get_started">${this.i18n.t('get_started')}</span></a>
                        </nav>
                    </div>
                </header>
            `;
        }

        // ========== FOOTER GENERATOR ==========
        generateFooter() {
            const socialLinks = [
                { name: 'tiktok', icon: SOCIAL_ICONS.tiktok, url: '#' },
                { name: 'youtube', icon: SOCIAL_ICONS.youtube, url: '#' },
                { name: 'instagram', icon: SOCIAL_ICONS.instagram, url: '#' },
                { name: 'facebook', icon: SOCIAL_ICONS.facebook, url: '#' },
                { name: 'linkedin', icon: SOCIAL_ICONS.linkedin, url: '#' },
                { name: 'twitter', icon: SOCIAL_ICONS.twitter, url: '#' },
                { name: 'discord', icon: SOCIAL_ICONS.discord, url: '#' },
                { name: 'reddit', icon: SOCIAL_ICONS.reddit, url: '#' },
                { name: 'telegram', icon: SOCIAL_ICONS.telegram, url: '#' },
                { name: 'whatsapp', icon: SOCIAL_ICONS.whatsapp, url: '#' }
            ];

            return `
                <footer class="iaf-footer">
                    <div class="iaf-footer-container">
                        <div class="iaf-footer-top">
                            <!-- Brand Column -->
                            <div class="iaf-footer-col iaf-footer-brand-col">
                                <div class="iaf-footer-logo">
                                    <img src="https://flagcdn.com/w40/dz.png" alt="Algeria" class="iaf-footer-flag">
                                    <span class="iaf-footer-brand">IAFactory <span style="color: var(--iaf-green)">Algeria</span></span>
                                </div>
                                <p class="iaf-footer-desc" data-i18n="desc">${this.i18n.t('desc')}</p>
                                <p class="iaf-footer-location">
                                    <i class="fa-solid fa-location-dot" style="color: var(--iaf-green); margin-right: 8px;"></i>
                                    <span data-i18n="location">${this.i18n.t('location')}</span>
                                </p>
                                <div class="iaf-footer-social">
                                    ${socialLinks.map(link => `<a href="${link.url}" class="iaf-footer-social-link" title="${link.name}">${link.icon}</a>`).join('')}
                                </div>
                            </div>

                            <!-- Products -->
                            <div class="iaf-footer-col">
                                <h4 class="iaf-footer-title" data-i18n="products">${this.i18n.t('products')}</h4>
                                <ul class="iaf-footer-links">
                                    <li><a href="/apps.html" data-i18n="apps">${this.i18n.t('apps')}</a></li>
                                    <li><a href="/docs/directory/agents.html" data-i18n="agents">${this.i18n.t('agents')}</a></li>
                                    <li><a href="/docs/directory/workflows.html" data-i18n="workflows">${this.i18n.t('workflows')}</a></li>
                                    <li><a href="/docs/api-setup.html" data-i18n="api">${this.i18n.t('api')}</a></li>
                                    <li><a href="/docs/rag-assistants.html" data-i18n="rag">${this.i18n.t('rag')}</a></li>
                                </ul>
                            </div>

                            <!-- Directory -->
                            <div class="iaf-footer-col">
                                <h4 class="iaf-footer-title" data-i18n="directory">${this.i18n.t('directory')}</h4>
                                <ul class="iaf-footer-links">
                                    <li><a href="/docs/directory/ia-tools.html" data-i18n="ia_tools">${this.i18n.t('ia_tools')}</a></li>
                                    <li><a href="/docs/directory/agents.html" data-i18n="agents">${this.i18n.t('agents')}</a></li>
                                    <li><a href="/docs/directory/workflows.html" data-i18n="workflows">${this.i18n.t('workflows')}</a></li>
                                    <li><a href="/docs/directory/daily-news.html" data-i18n="daily_news">${this.i18n.t('daily_news')}</a></li>
                                </ul>
                            </div>

                            <!-- Resources -->
                            <div class="iaf-footer-col">
                                <h4 class="iaf-footer-title" data-i18n="resources">${this.i18n.t('resources')}</h4>
                                <ul class="iaf-footer-links">
                                    <li><a href="/docs/documentation.html" data-i18n="docs">${this.i18n.t('docs')}</a></li>
                                    <li><a href="/docs/getstarted.html" data-i18n="getstarted">${this.i18n.t('getstarted')}</a></li>
                                    <li><a href="/docs/blog.html" data-i18n="blog">${this.i18n.t('blog')}</a></li>
                                    <li><a href="/docs/contact.html" data-i18n="support">${this.i18n.t('support')}</a></li>
                                </ul>
                            </div>

                            <!-- Company -->
                            <div class="iaf-footer-col">
                                <h4 class="iaf-footer-title" data-i18n="company">${this.i18n.t('company')}</h4>
                                <ul class="iaf-footer-links">
                                    <li><a href="/docs/a-propos.html" data-i18n="about">${this.i18n.t('about')}</a></li>
                                    <li><a href="/docs/tarifs.html" data-i18n="pricing">${this.i18n.t('pricing')}</a></li>
                                    <li><a href="/docs/contact.html" data-i18n="contact">${this.i18n.t('contact')}</a></li>
                                    <li><a href="/docs/newsletter.html" data-i18n="newsletter">${this.i18n.t('newsletter')}</a></li>
                                </ul>
                            </div>

                            <!-- Legal -->
                            <div class="iaf-footer-col">
                                <h4 class="iaf-footer-title" data-i18n="legal">${this.i18n.t('legal')}</h4>
                                <ul class="iaf-footer-links">
                                    <li><a href="/docs/mentions.html" data-i18n="mentions">${this.i18n.t('mentions')}</a></li>
                                    <li><a href="/docs/confidentialite.html" data-i18n="privacy">${this.i18n.t('privacy')}</a></li>
                                    <li><a href="/docs/conditions.html" data-i18n="terms">${this.i18n.t('terms')}</a></li>
                                </ul>
                            </div>
                        </div>

                        <div class="iaf-footer-bottom">
                            <p class="iaf-footer-copyright">
                                © <span id="iaf-current-year">${new Date().getFullYear()}</span> IAFactory Algeria. <span data-i18n="rights">${this.i18n.t('rights')}</span>
                            </p>
                            <p class="iaf-footer-made">
                                <span data-i18n="made">${this.i18n.t('made')}</span> ❤️ <span data-i18n="for">${this.i18n.t('for')}</span>
                            </p>
                        </div>
                    </div>
                </footer>
            `;
        }

        // ========== CHATBOT GENERATOR ==========
        generateChatbot() {
            return `
                <div class="iaf-chatbot">
                    <div class="iaf-help-bubble">
                        <span class="iaf-help-label" data-i18n="help_label">${this.i18n.t('help_label')}</span>
                        <button class="iaf-chatbot-btn" onclick="IAFactory.toggleChatbot()">
                            <img src="${this.avatarUrl}" alt="Dzir IA" onerror="this.style.display='none'; this.parentElement.innerHTML='💬';">
                        </button>
                    </div>
                </div>
                <div class="iaf-chatbot-window" id="iaf-chatbot-window">
                    <div class="iaf-chatbot-header">
                        <h3>
                            <img src="${this.avatarUrl}" alt="Dzir IA" onerror="this.style.display='none';">
                            <span data-i18n="help_title">${this.i18n.t('help_title')}</span>
                        </h3>
                        <button class="iaf-chatbot-close" onclick="IAFactory.toggleChatbot()">×</button>
                    </div>
                    <div class="iaf-chatbot-modes">
                        <button class="iaf-chatbot-mode active" id="iaf-mode-chat" onclick="IAFactory.setChatMode('chat')">
                            💬 <span data-i18n="help_chat_ai">${this.i18n.t('help_chat_ai')}</span>
                        </button>
                        <button class="iaf-chatbot-mode" id="iaf-mode-rag" onclick="IAFactory.setChatMode('rag')">
                            🔍 <span data-i18n="help_rag_search">${this.i18n.t('help_rag_search')}</span>
                        </button>
                        <button class="iaf-chatbot-mode" id="iaf-mode-support" onclick="IAFactory.setChatMode('support')">
                            📞 <span data-i18n="help_support">${this.i18n.t('help_support')}</span>
                        </button>
                    </div>
                    <div class="iaf-rag-selector" id="iaf-rag-selector">
                        <select id="iaf-rag-select">
                            <option value="DZ" data-i18n-option="help_business_dz">🇩🇿 ${this.i18n.t('help_business_dz')}</option>
                            <option value="CH" data-i18n-option="help_school_ch">🎓 ${this.i18n.t('help_school_ch')}</option>
                            <option value="GLOBAL" data-i18n-option="help_islam">🕌 ${this.i18n.t('help_islam')}</option>
                            <option value="ALL" data-i18n-option="help_all_rags">🌍 ${this.i18n.t('help_all_rags')}</option>
                        </select>
                    </div>
                    <div class="iaf-chatbot-messages" id="iaf-chatbot-messages">
                        <div class="iaf-chatbot-msg bot">
                            <div class="iaf-chatbot-avatar">
                                <img src="${this.avatarUrl}" alt="Dzir IA" onerror="this.parentElement.innerHTML='DZ';">
                            </div>
                            <div class="iaf-chatbot-bubble" data-i18n="help_welcome" data-i18n-html="true">${this.i18n.t('help_welcome')}</div>
                        </div>
                    </div>
                    <div class="iaf-chatbot-input">
                        <input type="text" id="iaf-chatbot-input" data-i18n-placeholder="help_placeholder" placeholder="${this.i18n.t('help_placeholder')}" onkeypress="if(event.key==='Enter')IAFactory.sendChatMessage()">
                        <button class="iaf-chatbot-send" onclick="IAFactory.sendChatMessage()">➤</button>
                    </div>
                </div>
            `;
        }

        // ========== EVENT HANDLERS ==========
        toggleLangMenu(event) {
            event.stopPropagation();
            const menu = document.getElementById('iaf-lang-menu');
            const btn = event.currentTarget;
            const isOpen = menu.classList.toggle('show');
            btn.setAttribute('aria-expanded', isOpen);
        }

        setLanguage(lang) {
            this.i18n.setLanguage(lang);
            const langLabel = document.querySelector('.iaf-lang-label');
            if (langLabel) langLabel.textContent = lang.toUpperCase();

            // Update active state
            document.querySelectorAll('.iaf-lang-option').forEach(opt => {
                opt.classList.remove('active');
            });
            const activeOpt = document.querySelector(`.iaf-lang-option[onclick="IAFactory.setLanguage('${lang}')"]`);
            if (activeOpt) activeOpt.classList.add('active');

            // Close menu
            const menu = document.getElementById('iaf-lang-menu');
            if (menu) menu.classList.remove('show');
        }

        toggleTheme() {
            const html = document.documentElement;
            const current = html.getAttribute('data-theme') || 'dark';
            const newTheme = current === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('iaf_theme', newTheme);
        }

        switchProfile(profile) {
            document.querySelectorAll('.iaf-profile-btn').forEach(btn => {
                btn.classList.toggle('active', btn.dataset.profile === profile);
            });
            window.dispatchEvent(new CustomEvent('profileChanged', { detail: { profile } }));
        }

        toggleMobileMenu() {
            const menu = document.getElementById('iaf-mobile-menu');
            const btn = document.querySelector('.iaf-mobile-menu-btn');
            if (menu && btn) {
                const isOpen = menu.classList.toggle('open');
                btn.classList.toggle('active', isOpen);
                document.body.style.overflow = isOpen ? 'hidden' : '';
            }
        }

        toggleChatbot() {
            const win = document.getElementById('iaf-chatbot-window');
            if (win) {
                this.chatOpen = !this.chatOpen;
                win.classList.toggle('open', this.chatOpen);
            }
        }

        setChatMode(mode) {
            this.chatMode = mode;
            document.querySelectorAll('.iaf-chatbot-mode').forEach(btn => btn.classList.remove('active'));
            const activeBtn = document.getElementById('iaf-mode-' + mode);
            if (activeBtn) activeBtn.classList.add('active');

            // Show/hide RAG selector
            const ragSelector = document.getElementById('iaf-rag-selector');
            if (ragSelector) {
                ragSelector.classList.toggle('show', mode === 'rag');
            }
        }

        async sendChatMessage() {
            const input = document.getElementById('iaf-chatbot-input');
            const messages = document.getElementById('iaf-chatbot-messages');
            if (!input || !messages) return;

            const msg = input.value.trim();
            if (!msg) return;

            // Add user message
            messages.innerHTML += `
                <div class="iaf-chatbot-msg user">
                    <div class="iaf-chatbot-bubble">${this.escapeHtml(msg)}</div>
                </div>
            `;
            input.value = '';

            // Add loading
            const loadingId = 'loading-' + Date.now();
            messages.innerHTML += `
                <div class="iaf-chatbot-msg bot" id="${loadingId}">
                    <div class="iaf-chatbot-avatar">
                        <img src="${this.avatarUrl}" alt="Dzir IA" onerror="this.parentElement.innerHTML='DZ';">
                    </div>
                    <div class="iaf-chatbot-bubble">⏳ ${this.i18n.t('help_thinking')}</div>
                </div>
            `;
            messages.scrollTop = messages.scrollHeight;

            try {
                const ragSelect = document.getElementById('iaf-rag-select');
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        message: msg,
                        mode: this.chatMode,
                        rag: ragSelect?.value || 'DZ',
                        lang: this.i18n.getLang()
                    })
                });
                const data = await response.json();
                const loadingEl = document.getElementById(loadingId);
                if (loadingEl) {
                    loadingEl.querySelector('.iaf-chatbot-bubble').innerHTML = data.response || 'OK';
                }
            } catch (e) {
                const loadingEl = document.getElementById(loadingId);
                if (loadingEl) {
                    loadingEl.querySelector('.iaf-chatbot-bubble').textContent = '❌ ' + this.i18n.t('help_error');
                }
            }
            messages.scrollTop = messages.scrollHeight;
        }

        escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        // ========== INITIALIZATION ==========
        init(options = {}) {
            // Load saved theme
            const savedTheme = localStorage.getItem('iaf_theme') || 'dark';
            document.documentElement.setAttribute('data-theme', savedTheme);

            // Load saved language
            const savedLang = localStorage.getItem('iafactory_lang') || 'fr';
            this.i18n.setLanguage(savedLang);

            // Inject Header
            const headerContainer = document.getElementById('iaf-header') || document.querySelector('[data-iaf-header]');
            if (headerContainer) {
                headerContainer.outerHTML = this.generateHeader(options);
            }

            // Inject Footer
            const footerContainer = document.getElementById('iaf-footer') || document.querySelector('[data-iaf-footer]');
            if (footerContainer) {
                footerContainer.outerHTML = this.generateFooter();
            }

            // Inject Chatbot
            const chatbotContainer = document.getElementById('iaf-chatbot') || document.querySelector('[data-iaf-chatbot]');
            if (chatbotContainer) {
                chatbotContainer.outerHTML = this.generateChatbot();
            } else if (options.autoChatbot !== false) {
                document.body.insertAdjacentHTML('beforeend', this.generateChatbot());
            }

            // Close menus on outside click
            document.addEventListener('click', (e) => {
                if (!e.target.closest('.iaf-language-selector')) {
                    const menu = document.getElementById('iaf-lang-menu');
                    if (menu) {
                        menu.classList.remove('show');
                        document.querySelector('.iaf-lang-btn')?.setAttribute('aria-expanded', 'false');
                    }
                }
            });

            // Close mobile menu on escape
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    const menu = document.getElementById('iaf-mobile-menu');
                    if (menu?.classList.contains('open')) {
                        this.toggleMobileMenu();
                    }
                }
            });

            // Header scroll effect
            window.addEventListener('scroll', () => {
                const header = document.querySelector('.iaf-header');
                if (header) {
                    header.classList.toggle('scrolled', window.scrollY > 10);
                }
            });

            console.log('✅ IAFactory Unified Components v2.0 initialized');
        }
    }

    // ========== GLOBAL INSTANCE ==========
    window.IAFactory = new IAFactoryComponents();
    window.IAFactoryI18n = IAFactoryI18n;

    // Auto-init on DOMContentLoaded
    document.addEventListener('DOMContentLoaded', function() {
        if (document.querySelector('[data-iaf-auto-init]')) {
            window.IAFactory.init();
        }
    });

})();
