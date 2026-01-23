/**
 * IAFactory i18n System - Trilingual Support (FR/AR/EN)
 * Shared module for all docs pages
 * Version: 1.0.0
 */

const IAFactoryI18n = {
    currentLang: localStorage.getItem('iafactory_lang') || 'fr',

    translations: {
        // ===== COMMON NAVIGATION =====
        "home": { fr: "Accueil", ar: "الرئيسية", en: "Home" },
        "features": { fr: "Fonctionnalités", ar: "المميزات", en: "Features" },
        "apps": { fr: "Applications", ar: "التطبيقات", en: "Applications" },
        "pricing": { fr: "Tarifs", ar: "الأسعار", en: "Pricing" },
        "docs": { fr: "Documentation", ar: "التوثيق", en: "Documentation" },
        "contact": { fr: "Contact", ar: "اتصل بنا", en: "Contact" },
        "about": { fr: "À propos", ar: "من نحن", en: "About" },
        "blog": { fr: "Blog", ar: "مدونة", en: "Blog" },
        "api": { fr: "API", ar: "واجهة برمجة التطبيقات", en: "API" },

        // ===== AUTH =====
        "login": { fr: "Se connecter", ar: "تسجيل الدخول", en: "Log in" },
        "logout": { fr: "Se déconnecter", ar: "تسجيل الخروج", en: "Log out" },
        "register": { fr: "S'inscrire", ar: "إنشاء حساب", en: "Register" },
        "get_started": { fr: "Commencer", ar: "ابدأ الآن", en: "Get Started" },
        "try_free": { fr: "Essayer gratuitement", ar: "جرب مجاناً", en: "Try for free" },

        // ===== COMMON ACTIONS =====
        "back": { fr: "Retour", ar: "رجوع", en: "Back" },
        "next": { fr: "Suivant", ar: "التالي", en: "Next" },
        "previous": { fr: "Précédent", ar: "السابق", en: "Previous" },
        "submit": { fr: "Envoyer", ar: "إرسال", en: "Submit" },
        "cancel": { fr: "Annuler", ar: "إلغاء", en: "Cancel" },
        "save": { fr: "Enregistrer", ar: "حفظ", en: "Save" },
        "delete": { fr: "Supprimer", ar: "حذف", en: "Delete" },
        "edit": { fr: "Modifier", ar: "تعديل", en: "Edit" },
        "close": { fr: "Fermer", ar: "إغلاق", en: "Close" },
        "open": { fr: "Ouvrir", ar: "فتح", en: "Open" },
        "download": { fr: "Télécharger", ar: "تحميل", en: "Download" },
        "upload": { fr: "Uploader", ar: "رفع", en: "Upload" },
        "search": { fr: "Rechercher", ar: "بحث", en: "Search" },
        "filter": { fr: "Filtrer", ar: "تصفية", en: "Filter" },
        "copy": { fr: "Copier", ar: "نسخ", en: "Copy" },
        "share": { fr: "Partager", ar: "مشاركة", en: "Share" },

        // ===== PAGE TITLES =====
        "page_about": { fr: "À Propos", ar: "من نحن", en: "About Us" },
        "page_pricing": { fr: "Tarifs", ar: "الأسعار", en: "Pricing" },
        "page_contact": { fr: "Contact", ar: "اتصل بنا", en: "Contact" },
        "page_blog": { fr: "Blog", ar: "المدونة", en: "Blog" },
        "page_docs": { fr: "Documentation", ar: "التوثيق", en: "Documentation" },
        "page_api": { fr: "API Setup", ar: "إعداد API", en: "API Setup" },
        "page_agents": { fr: "Agents IA", ar: "وكلاء الذكاء الاصطناعي", en: "AI Agents" },
        "page_workflows": { fr: "Workflows", ar: "سير العمل", en: "Workflows" },
        "page_tools": { fr: "Outils IA", ar: "أدوات الذكاء الاصطناعي", en: "AI Tools" },
        "page_news": { fr: "Actualités", ar: "الأخبار", en: "News" },
        "page_newsletter": { fr: "Newsletter", ar: "النشرة الإخبارية", en: "Newsletter" },
        "page_getstarted": { fr: "Démarrage Rapide", ar: "البدء السريع", en: "Quick Start" },
        "page_rag": { fr: "RAG Assistants", ar: "مساعدو RAG", en: "RAG Assistants" },
        "page_developer": { fr: "Outils Développeur", ar: "أدوات المطور", en: "Developer Tools" },
        "page_login": { fr: "Connexion", ar: "تسجيل الدخول", en: "Login" },
        "page_privacy": { fr: "Confidentialité", ar: "الخصوصية", en: "Privacy" },
        "page_terms": { fr: "Conditions d'utilisation", ar: "شروط الاستخدام", en: "Terms of Use" },
        "page_legal": { fr: "Mentions légales", ar: "الإشعارات القانونية", en: "Legal Mentions" },

        // ===== ABOUT PAGE =====
        "about_mission": { fr: "Notre Mission", ar: "مهمتنا", en: "Our Mission" },
        "about_mission_text": {
            fr: "IAFactory Algeria est la première plateforme SaaS d'intelligence artificielle souveraine dédiée aux institutions et entreprises algériennes. Notre mission est de démocratiser l'accès à l'IA en offrant des solutions adaptées au contexte local.",
            ar: "IAFactory Algeria هي أول منصة SaaS للذكاء الاصطناعي السيادي المخصصة للمؤسسات والشركات الجزائرية. مهمتنا هي إضفاء الطابع الديمقراطي على الوصول إلى الذكاء الاصطناعي من خلال تقديم حلول تتكيف مع السياق المحلي.",
            en: "IAFactory Algeria is the first sovereign artificial intelligence SaaS platform dedicated to Algerian institutions and companies. Our mission is to democratize access to AI by offering solutions adapted to the local context."
        },
        "about_values": { fr: "Nos Valeurs", ar: "قيمنا", en: "Our Values" },
        "about_sovereignty": { fr: "Souveraineté", ar: "السيادة", en: "Sovereignty" },
        "about_innovation": { fr: "Innovation", ar: "الابتكار", en: "Innovation" },
        "about_accessibility": { fr: "Accessibilité", ar: "إمكانية الوصول", en: "Accessibility" },
        "about_excellence": { fr: "Excellence", ar: "التميز", en: "Excellence" },
        "about_company": { fr: "L'Entreprise", ar: "الشركة", en: "The Company" },
        "about_partners": { fr: "Nos Partenaires", ar: "شركاؤنا", en: "Our Partners" },

        // ===== PRICING PAGE =====
        "pricing_title": { fr: "Tarifs Transparents", ar: "أسعار شفافة", en: "Transparent Pricing" },
        "pricing_subtitle": {
            fr: "Payables en Dinars Algériens via Chargily",
            ar: "قابلة للدفع بالدينار الجزائري عبر Chargily",
            en: "Payable in Algerian Dinars via Chargily"
        },
        "pricing_free": { fr: "Gratuit", ar: "مجاني", en: "Free" },
        "pricing_starter": { fr: "Starter", ar: "المبتدئ", en: "Starter" },
        "pricing_pro": { fr: "Pro", ar: "احترافي", en: "Pro" },
        "pricing_enterprise": { fr: "Enterprise", ar: "المؤسسات", en: "Enterprise" },
        "pricing_month": { fr: "/mois", ar: "/شهر", en: "/month" },
        "pricing_year": { fr: "/an", ar: "/سنة", en: "/year" },
        "pricing_dzd": { fr: "DZD", ar: "دج", en: "DZD" },
        "pricing_contact_us": { fr: "Contactez-nous", ar: "اتصل بنا", en: "Contact us" },
        "pricing_choose_plan": { fr: "Choisir ce plan", ar: "اختر هذه الخطة", en: "Choose this plan" },

        // ===== CONTACT PAGE =====
        "contact_title": { fr: "Contactez-nous", ar: "اتصل بنا", en: "Contact Us" },
        "contact_name": { fr: "Nom", ar: "الاسم", en: "Name" },
        "contact_email": { fr: "Email", ar: "البريد الإلكتروني", en: "Email" },
        "contact_subject": { fr: "Sujet", ar: "الموضوع", en: "Subject" },
        "contact_message": { fr: "Message", ar: "الرسالة", en: "Message" },
        "contact_send": { fr: "Envoyer", ar: "إرسال", en: "Send" },
        "contact_address": { fr: "Adresse", ar: "العنوان", en: "Address" },
        "contact_phone": { fr: "Téléphone", ar: "الهاتف", en: "Phone" },

        // ===== NEWSLETTER =====
        "newsletter_title": { fr: "Newsletter", ar: "النشرة الإخبارية", en: "Newsletter" },
        "newsletter_subtitle": {
            fr: "Restez informé des dernières actualités IA",
            ar: "ابق على اطلاع بآخر أخبار الذكاء الاصطناعي",
            en: "Stay informed about the latest AI news"
        },
        "newsletter_subscribe": { fr: "S'abonner", ar: "اشترك", en: "Subscribe" },
        "newsletter_email_placeholder": { fr: "Votre email", ar: "بريدك الإلكتروني", en: "Your email" },

        // ===== FOOTER =====
        "footer_description": {
            fr: "Plateforme IA souveraine pour institutions algériennes, public et privé.",
            ar: "منصة ذكاء اصطناعي سيادية للمؤسسات الجزائرية، العامة والخاصة.",
            en: "Sovereign AI platform for Algerian institutions, public and private."
        },
        "footer_products": { fr: "Produits", ar: "المنتجات", en: "Products" },
        "footer_resources": { fr: "Ressources", ar: "الموارد", en: "Resources" },
        "footer_company": { fr: "Entreprise", ar: "الشركة", en: "Company" },
        "footer_legal": { fr: "Légal", ar: "قانوني", en: "Legal" },
        "footer_rights": { fr: "Tous droits réservés", ar: "جميع الحقوق محفوظة", en: "All rights reserved" },
        "footer_made_with_love": { fr: "Fait avec ❤️ pour l'Algérie", ar: "صُنع بـ ❤️ للجزائر", en: "Made with ❤️ for Algeria" },
        "footer_location": { fr: "Alger, Algérie", ar: "الجزائر العاصمة، الجزائر", en: "Algiers, Algeria" },

        // ===== STATS =====
        "stat_apps": { fr: "Applications", ar: "التطبيقات", en: "Applications" },
        "stat_agents": { fr: "Agents IA", ar: "وكلاء الذكاء الاصطناعي", en: "AI Agents" },
        "stat_sectors": { fr: "Secteurs", ar: "القطاعات", en: "Sectors" },
        "stat_languages": { fr: "Langues", ar: "اللغات", en: "Languages" },
        "stat_uptime": { fr: "Uptime", ar: "وقت التشغيل", en: "Uptime" },
        "stat_sovereign": { fr: "Souverain", ar: "سيادي", en: "Sovereign" },

        // ===== DOCS =====
        "docs_quickstart": { fr: "Démarrage Rapide", ar: "البدء السريع", en: "Quick Start" },
        "docs_installation": { fr: "Installation", ar: "التثبيت", en: "Installation" },
        "docs_configuration": { fr: "Configuration", ar: "التكوين", en: "Configuration" },
        "docs_api_reference": { fr: "Référence API", ar: "مرجع API", en: "API Reference" },
        "docs_examples": { fr: "Exemples", ar: "أمثلة", en: "Examples" },
        "docs_faq": { fr: "FAQ", ar: "الأسئلة الشائعة", en: "FAQ" },
        "docs_support": { fr: "Support", ar: "الدعم", en: "Support" },

        // ===== API SETUP =====
        "api_get_key": { fr: "Obtenir une clé API", ar: "الحصول على مفتاح API", en: "Get API Key" },
        "api_documentation": { fr: "Documentation API", ar: "توثيق API", en: "API Documentation" },
        "api_endpoints": { fr: "Endpoints", ar: "نقاط النهاية", en: "Endpoints" },
        "api_authentication": { fr: "Authentification", ar: "المصادقة", en: "Authentication" },
        "api_rate_limits": { fr: "Limites de requêtes", ar: "حدود الطلبات", en: "Rate Limits" },
        "api_errors": { fr: "Gestion des erreurs", ar: "إدارة الأخطاء", en: "Error Handling" },

        // ===== AGENTS =====
        "agents_title": { fr: "Agents IA", ar: "وكلاء الذكاء الاصطناعي", en: "AI Agents" },
        "agents_subtitle": {
            fr: "Découvrez nos agents IA spécialisés",
            ar: "اكتشف وكلاء الذكاء الاصطناعي المتخصصين لدينا",
            en: "Discover our specialized AI agents"
        },
        "agent_consultant": { fr: "AI Consultant", ar: "مستشار الذكاء الاصطناعي", en: "AI Consultant" },
        "agent_customer_support": { fr: "Support Client", ar: "دعم العملاء", en: "Customer Support" },
        "agent_data_analyst": { fr: "Analyste de Données", ar: "محلل البيانات", en: "Data Analyst" },
        "agent_financial_coach": { fr: "Coach Financier", ar: "مدرب مالي", en: "Financial Coach" },
        "agent_legal": { fr: "Assistant Juridique", ar: "مساعد قانوني", en: "Legal Assistant" },
        "agent_recruitment": { fr: "Recrutement", ar: "التوظيف", en: "Recruitment" },
        "agent_real_estate": { fr: "Immobilier", ar: "العقارات", en: "Real Estate" },
        "agent_travel": { fr: "Voyages", ar: "السفر", en: "Travel" },
        "agent_teaching": { fr: "Enseignement", ar: "التعليم", en: "Teaching" },

        // ===== MISC =====
        "loading": { fr: "Chargement...", ar: "جاري التحميل...", en: "Loading..." },
        "error": { fr: "Erreur", ar: "خطأ", en: "Error" },
        "success": { fr: "Succès", ar: "نجاح", en: "Success" },
        "warning": { fr: "Attention", ar: "تحذير", en: "Warning" },
        "info": { fr: "Information", ar: "معلومات", en: "Info" },
        "yes": { fr: "Oui", ar: "نعم", en: "Yes" },
        "no": { fr: "Non", ar: "لا", en: "No" },
        "or": { fr: "ou", ar: "أو", en: "or" },
        "and": { fr: "et", ar: "و", en: "and" },
        "all": { fr: "Tout", ar: "الكل", en: "All" },
        "none": { fr: "Aucun", ar: "لا شيء", en: "None" },
        "more": { fr: "Plus", ar: "المزيد", en: "More" },
        "less": { fr: "Moins", ar: "أقل", en: "Less" },
        "show_more": { fr: "Voir plus", ar: "عرض المزيد", en: "Show more" },
        "show_less": { fr: "Voir moins", ar: "عرض أقل", en: "Show less" },
        "view_all": { fr: "Voir tout", ar: "عرض الكل", en: "View all" },

        // ===== ABOUT PAGE EXTENDED =====
        "about_title": {
            fr: "À Propos d'IAFactory Algeria",
            ar: "حول IAFactory الجزائر",
            en: "About IAFactory Algeria"
        },
        "about_subtitle": {
            fr: "La première plateforme SaaS d'intelligence artificielle souveraine pour l'Algérie",
            ar: "أول منصة SaaS للذكاء الاصطناعي السيادي للجزائر",
            en: "The first sovereign AI SaaS platform for Algeria"
        },
        "about_sovereignty_desc": {
            fr: "Données hébergées en Algérie, respect de la législation locale",
            ar: "البيانات مستضافة في الجزائر، احترام التشريعات المحلية",
            en: "Data hosted in Algeria, compliance with local legislation"
        },
        "about_innovation_desc": {
            fr: "Technologies IA de pointe adaptées au marché algérien",
            ar: "تقنيات ذكاء اصطناعي متطورة مكيفة للسوق الجزائري",
            en: "Cutting-edge AI technologies adapted to the Algerian market"
        },
        "about_accessibility_desc": {
            fr: "Solutions abordables pour toutes les tailles d'entreprises",
            ar: "حلول ميسورة التكلفة لجميع أحجام الشركات",
            en: "Affordable solutions for all business sizes"
        },
        "about_excellence_desc": {
            fr: "Support premium et qualité de service garantie",
            ar: "دعم متميز وجودة خدمة مضمونة",
            en: "Premium support and guaranteed quality of service"
        },
        "about_company_text": {
            fr: "Fondée en 2024, IAFactory Algeria réunit une équipe d'experts en intelligence artificielle, développement logiciel et connaissance du marché algérien. Nous travaillons avec des partenaires locaux et internationaux pour offrir les meilleures solutions.",
            ar: "تأسست في 2024، تجمع IAFactory الجزائر فريقًا من الخبراء في الذكاء الاصطناعي وتطوير البرمجيات ومعرفة السوق الجزائري. نعمل مع شركاء محليين ودوليين لتقديم أفضل الحلول.",
            en: "Founded in 2024, IAFactory Algeria brings together a team of experts in artificial intelligence, software development and knowledge of the Algerian market. We work with local and international partners to offer the best solutions."
        },
        "about_location": { fr: "Alger, Algérie", ar: "الجزائر العاصمة، الجزائر", en: "Algiers, Algeria" },
        "about_partner1": { fr: "Institutions gouvernementales algériennes", ar: "المؤسسات الحكومية الجزائرية", en: "Algerian government institutions" },
        "about_partner2": { fr: "Universités et centres de recherche", ar: "الجامعات ومراكز البحث", en: "Universities and research centers" },
        "about_partner3": { fr: "Fournisseurs cloud souverains", ar: "مزودو السحابة السيادية", en: "Sovereign cloud providers" },
        "about_partner4": { fr: "Écosystème startup algérien", ar: "منظومة الشركات الناشئة الجزائرية", en: "Algerian startup ecosystem" },

        // ===== STATS =====
        "stat_apps": { fr: "Applications", ar: "التطبيقات", en: "Applications" },
        "stat_agents": { fr: "Agents IA", ar: "وكلاء الذكاء الاصطناعي", en: "AI Agents" },
        "stat_sectors": { fr: "Secteurs", ar: "القطاعات", en: "Sectors" },
        "stat_languages": { fr: "Langues", ar: "اللغات", en: "Languages" },

        // ===== BLOG PAGE =====
        "blog_title": { fr: "Blog IAFactory", ar: "مدونة IAFactory", en: "IAFactory Blog" },
        "blog_subtitle": { fr: "Actualités, tutoriels et insights sur l'IA en Algérie", ar: "أخبار ودروس ورؤى حول الذكاء الاصطناعي في الجزائر", en: "News, tutorials and insights about AI in Algeria" },
        "blog_read_more": { fr: "Lire la suite", ar: "اقرأ المزيد", en: "Read more" },
        "blog_category": { fr: "Catégorie", ar: "الفئة", en: "Category" },
        "blog_date": { fr: "Date", ar: "التاريخ", en: "Date" },
        "blog_author": { fr: "Auteur", ar: "الكاتب", en: "Author" },
        "blog_no_posts": { fr: "Aucun article pour le moment", ar: "لا توجد مقالات حالياً", en: "No posts yet" },

        // ===== CONTACT PAGE EXTENDED =====
        "contact_subtitle": { fr: "Une question ? Nous sommes là pour vous aider", ar: "لديك سؤال؟ نحن هنا لمساعدتك", en: "Have a question? We're here to help" },
        "contact_form_title": { fr: "Envoyez-nous un message", ar: "أرسل لنا رسالة", en: "Send us a message" },
        "contact_info_title": { fr: "Informations de contact", ar: "معلومات الاتصال", en: "Contact Information" },
        "contact_name": { fr: "Nom complet", ar: "الاسم الكامل", en: "Full Name" },
        "contact_email": { fr: "Email", ar: "البريد الإلكتروني", en: "Email" },
        "contact_subject": { fr: "Sujet", ar: "الموضوع", en: "Subject" },
        "contact_message": { fr: "Votre message", ar: "رسالتك", en: "Your message" },
        "contact_send": { fr: "Envoyer le message", ar: "إرسال الرسالة", en: "Send message" },
        "contact_success": { fr: "Message envoyé avec succès!", ar: "تم إرسال الرسالة بنجاح!", en: "Message sent successfully!" },
        "contact_phone": { fr: "Téléphone", ar: "الهاتف", en: "Phone" },
        "contact_address": { fr: "Adresse", ar: "العنوان", en: "Address" },
        "contact_hours": { fr: "Horaires", ar: "ساعات العمل", en: "Business Hours" },
        "contact_hours_value": { fr: "Dim - Jeu: 9h - 17h", ar: "الأحد - الخميس: 9 صباحاً - 5 مساءً", en: "Sun - Thu: 9am - 5pm" },

        // ===== LEGAL PAGES =====
        "legal_title": { fr: "Mentions Légales", ar: "الإشعارات القانونية", en: "Legal Mentions" },
        "legal_subtitle": { fr: "Informations légales sur IAFactory Algeria", ar: "المعلومات القانونية حول IAFactory الجزائر", en: "Legal information about IAFactory Algeria" },
        "legal_company_name": { fr: "Raison sociale", ar: "الاسم التجاري", en: "Company Name" },
        "legal_headquarters": { fr: "Siège social", ar: "المقر الرئيسي", en: "Headquarters" },
        "legal_rc": { fr: "Registre du Commerce", ar: "السجل التجاري", en: "Business Registration" },
        "legal_nif": { fr: "NIF", ar: "رقم التعريف الجبائي", en: "Tax ID" },
        "legal_director": { fr: "Directeur de publication", ar: "مدير النشر", en: "Publishing Director" },
        "legal_host": { fr: "Hébergeur", ar: "المستضيف", en: "Host" },

        "privacy_title": { fr: "Politique de Confidentialité", ar: "سياسة الخصوصية", en: "Privacy Policy" },
        "privacy_subtitle": { fr: "Comment nous protégeons vos données", ar: "كيف نحمي بياناتك", en: "How we protect your data" },
        "privacy_collect": { fr: "Données collectées", ar: "البيانات المجمعة", en: "Data Collected" },
        "privacy_use": { fr: "Utilisation des données", ar: "استخدام البيانات", en: "Data Use" },
        "privacy_storage": { fr: "Stockage des données", ar: "تخزين البيانات", en: "Data Storage" },
        "privacy_rights": { fr: "Vos droits", ar: "حقوقك", en: "Your Rights" },
        "privacy_cookies": { fr: "Cookies", ar: "ملفات تعريف الارتباط", en: "Cookies" },
        "privacy_contact": { fr: "Contact DPO", ar: "اتصل بمسؤول حماية البيانات", en: "Contact DPO" },

        "terms_title": { fr: "Conditions Générales d'Utilisation", ar: "الشروط والأحكام العامة", en: "Terms of Use" },
        "terms_subtitle": { fr: "Règles d'utilisation de nos services", ar: "قواعد استخدام خدماتنا", en: "Rules for using our services" },
        "terms_acceptance": { fr: "Acceptation des CGU", ar: "قبول الشروط", en: "Acceptance of Terms" },
        "terms_services": { fr: "Description des services", ar: "وصف الخدمات", en: "Service Description" },
        "terms_account": { fr: "Compte utilisateur", ar: "حساب المستخدم", en: "User Account" },
        "terms_obligations": { fr: "Obligations de l'utilisateur", ar: "التزامات المستخدم", en: "User Obligations" },
        "terms_ip": { fr: "Propriété intellectuelle", ar: "الملكية الفكرية", en: "Intellectual Property" },
        "terms_liability": { fr: "Responsabilité", ar: "المسؤولية", en: "Liability" },
        "terms_modification": { fr: "Modification des CGU", ar: "تعديل الشروط", en: "Modification of Terms" },
        "terms_law": { fr: "Droit applicable", ar: "القانون المعمول به", en: "Applicable Law" },

        // ===== WORKFLOWS PAGE =====
        "workflows_title": { fr: "Workflows IA", ar: "سير العمل بالذكاء الاصطناعي", en: "AI Workflows" },
        "workflows_subtitle": { fr: "Automatisez vos processus métier avec l'IA", ar: "أتمتة عملياتك التجارية بالذكاء الاصطناعي", en: "Automate your business processes with AI" },
        "workflows_create": { fr: "Créer un workflow", ar: "إنشاء سير عمل", en: "Create workflow" },
        "workflows_templates": { fr: "Templates", ar: "القوالب", en: "Templates" },
        "workflows_my_workflows": { fr: "Mes workflows", ar: "سير عملي", en: "My workflows" },

        // ===== IA TOOLS PAGE =====
        "tools_title": { fr: "Outils IA", ar: "أدوات الذكاء الاصطناعي", en: "AI Tools" },
        "tools_subtitle": { fr: "Suite complète d'outils d'intelligence artificielle", ar: "مجموعة كاملة من أدوات الذكاء الاصطناعي", en: "Complete suite of AI tools" },
        "tools_category_text": { fr: "Texte", ar: "النص", en: "Text" },
        "tools_category_image": { fr: "Image", ar: "الصورة", en: "Image" },
        "tools_category_audio": { fr: "Audio", ar: "الصوت", en: "Audio" },
        "tools_category_video": { fr: "Vidéo", ar: "الفيديو", en: "Video" },
        "tools_category_code": { fr: "Code", ar: "الكود", en: "Code" },

        // ===== DAILY NEWS PAGE =====
        "news_title": { fr: "Actualités IA", ar: "أخبار الذكاء الاصطناعي", en: "AI News" },
        "news_subtitle": { fr: "Les dernières nouvelles du monde de l'IA", ar: "آخر أخبار عالم الذكاء الاصطناعي", en: "Latest news from the AI world" },
        "news_today": { fr: "Aujourd'hui", ar: "اليوم", en: "Today" },
        "news_yesterday": { fr: "Hier", ar: "أمس", en: "Yesterday" },
        "news_this_week": { fr: "Cette semaine", ar: "هذا الأسبوع", en: "This week" },

        // ===== AGENTS PAGE =====
        "agents_title": { fr: "Agents IA", ar: "وكلاء الذكاء الاصطناعي", en: "AI Agents" },
        "agents_subtitle": { fr: "Découvrez nos agents IA spécialisés pour chaque domaine", ar: "اكتشف وكلاء الذكاء الاصطناعي المتخصصين لكل مجال", en: "Discover our specialized AI agents for each domain" },
        "agents_available": { fr: "Disponible", ar: "متاح", en: "Available" },
        "agents_coming_soon": { fr: "Bientôt", ar: "قريباً", en: "Coming Soon" },
        "agents_try": { fr: "Essayer", ar: "جرب", en: "Try" },
        "agents_learn_more": { fr: "En savoir plus", ar: "اعرف المزيد", en: "Learn more" }
    },

    /**
     * Get translation for a key
     * @param {string} key - Translation key
     * @returns {string} - Translated text
     */
    t: function(key) {
        const translation = this.translations[key];
        if (!translation) {
            console.warn(`IAFactoryI18n: Translation not found for key "${key}"`);
            return key;
        }
        return translation[this.currentLang] || translation['fr'] || key;
    },

    /**
     * Set current language and update all elements with data-i18n attribute
     * @param {string} lang - Language code (fr, ar, en)
     * @param {boolean} save - Whether to save to localStorage (default: true)
     */
    setLanguage: function(lang, save = true) {
        if (!['fr', 'ar', 'en'].includes(lang)) {
            console.warn(`IAFactoryI18n: Invalid language "${lang}". Using "fr".`);
            lang = 'fr';
        }

        this.currentLang = lang;

        if (save) {
            localStorage.setItem('iafactory_lang', lang);
        }

        // Set RTL for Arabic
        if (lang === 'ar') {
            document.documentElement.dir = 'rtl';
            document.documentElement.lang = 'ar';
            document.body.classList.add('rtl');
        } else {
            document.documentElement.dir = 'ltr';
            document.documentElement.lang = lang;
            document.body.classList.remove('rtl');
        }

        // Update all elements with data-i18n attribute
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            const translation = this.t(key);

            // Check if element should use innerHTML (for HTML content)
            if (el.getAttribute('data-i18n-html') === 'true') {
                el.innerHTML = translation;
            } else {
                el.textContent = translation;
            }
        });

        // Update placeholders
        document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
            const key = el.getAttribute('data-i18n-placeholder');
            el.placeholder = this.t(key);
        });

        // Update titles
        document.querySelectorAll('[data-i18n-title]').forEach(el => {
            const key = el.getAttribute('data-i18n-title');
            el.title = this.t(key);
        });

        // Update aria-labels
        document.querySelectorAll('[data-i18n-aria]').forEach(el => {
            const key = el.getAttribute('data-i18n-aria');
            el.setAttribute('aria-label', this.t(key));
        });

        // Update select options
        document.querySelectorAll('[data-i18n-option]').forEach(el => {
            const key = el.getAttribute('data-i18n-option');
            const originalText = el.textContent;
            // Preserve emojis at the beginning
            const emojiMatch = originalText.match(/^[\u{1F300}-\u{1F9FF}][\u{FE0F}]?\s*/u);
            const emoji = emojiMatch ? emojiMatch[0] : '';
            el.textContent = emoji + this.t(key);
        });

        // Update lang button display
        const langLabels = { fr: '🌐 FR', en: '🌐 EN', ar: '🌐 AR' };
        const langBtn = document.querySelector('.lang-btn');
        if (langBtn) {
            langBtn.textContent = langLabels[lang] || '🌐 FR';
        }

        // Dispatch event for custom handlers
        window.dispatchEvent(new CustomEvent('languageChanged', { detail: { lang } }));
    },

    /**
     * Initialize i18n system
     */
    init: function() {
        const savedLang = localStorage.getItem('iafactory_lang') || 'fr';
        this.setLanguage(savedLang, false);
    }
};

// Initialize on DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => IAFactoryI18n.init());
} else {
    IAFactoryI18n.init();
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = IAFactoryI18n;
}
