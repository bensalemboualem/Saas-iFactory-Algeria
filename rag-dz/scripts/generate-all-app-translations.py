#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générer toutes les traductions pour les apps et agents
"""

# Traductions complètes pour toutes les apps
app_translations = {
    # Business Apps
    "app_archon_ui_desc": {
        "fr": "Interface multi-agents complète.",
        "ar": "واجهة متعددة الوكلاء الكاملة.",
        "en": "Complete multi-agent interface."
    },
    "app_pme_copilot_desc": {
        "fr": "Assistant IA pour PME.",
        "ar": "مساعد ذكاء اصطناعي للمؤسسات الصغيرة.",
        "en": "AI assistant for SMEs."
    },
    "app_pme_copilot_ui_desc": {
        "fr": "Interface PME Copilot.",
        "ar": "واجهة مساعد المؤسسات الصغيرة.",
        "en": "SME Copilot Interface."
    },
    "app_pmedz_sales_desc": {
        "fr": "Gestion commerciale PME.",
        "ar": "إدارة المبيعات للمؤسسات الصغيرة.",
        "en": "SME sales management."
    },
    "app_pmedz_sales_ui_desc": {
        "fr": "Interface Sales PME.",
        "ar": "واجهة مبيعات المؤسسات الصغيرة.",
        "en": "SME Sales Interface."
    },
    "app_crm_ia_desc": {
        "fr": "CRM intelligent avec IA.",
        "ar": "إدارة علاقات العملاء بالذكاء الاصطناعي.",
        "en": "Intelligent CRM with AI."
    },
    "app_crm_ia_ui_desc": {
        "fr": "Interface CRM IA.",
        "ar": "واجهة إدارة العملاء بالذكاء الاصطناعي.",
        "en": "AI CRM Interface."
    },
    "app_growth_grid_desc": {
        "fr": "Analyse croissance startup.",
        "ar": "تحليل نمو الشركات الناشئة.",
        "en": "Startup growth analysis."
    },
    "app_startup_dz_desc": {
        "fr": "Écosystème startup algérien.",
        "ar": "النظام البيئي للشركات الناشئة الجزائرية.",
        "en": "Algerian startup ecosystem."
    },
    "app_startup_onboarding_desc": {
        "fr": "Intégration startup DZ.",
        "ar": "تأهيل الشركات الناشئة الجزائرية.",
        "en": "DZ startup onboarding."
    },
    "app_startup_onboarding_ui_desc": {
        "fr": "Interface onboarding startup.",
        "ar": "واجهة تأهيل الشركات الناشئة.",
        "en": "Startup onboarding interface."
    },
    "app_business_dz_desc": {
        "fr": "Solutions business Algérie.",
        "ar": "حلول الأعمال الجزائرية.",
        "en": "Algerian business solutions."
    },
    "app_creative_studio_desc": {
        "fr": "Studio création contenu IA.",
        "ar": "استوديو إنشاء المحتوى بالذكاء الاصطناعي.",
        "en": "AI content creation studio."
    },
    "app_ecommerce_dz_desc": {
        "fr": "E-commerce Algérie.",
        "ar": "التجارة الإلكترونية الجزائرية.",
        "en": "Algerian e-commerce."
    },
    "app_commerce_dz_desc": {
        "fr": "Solutions commerce local.",
        "ar": "حلول التجارة المحلية.",
        "en": "Local commerce solutions."
    },

    # Finance Apps
    "app_data_dz_desc": {
        "fr": "Tableaux de bord analytiques.",
        "ar": "لوحات المعلومات التحليلية.",
        "en": "Analytical dashboards."
    },
    "app_data_dz_dashboard_desc": {
        "fr": "Dashboard Data-DZ.",
        "ar": "لوحة بيانات الجزائر.",
        "en": "Data-DZ Dashboard."
    },
    "app_fiscal_assistant_desc": {
        "fr": "Assistant fiscal algérien.",
        "ar": "مساعد ضريبي جزائري.",
        "en": "Algerian tax assistant."
    },
    "app_expert_comptable_desc": {
        "fr": "Expert comptable IA.",
        "ar": "خبير محاسبة بالذكاء الاصطناعي.",
        "en": "AI accounting expert."
    },

    # Legal Apps
    "app_legal_assistant_desc": {
        "fr": "Assistant juridique IA.",
        "ar": "مساعد قانوني بالذكاء الاصطناعي.",
        "en": "AI legal assistant."
    },
    "app_douanes_dz_desc": {
        "fr": "Assistant douanes Algérie.",
        "ar": "مساعد الجمارك الجزائرية.",
        "en": "Algerian customs assistant."
    },

    # AI & Agents Apps
    "app_council_desc": {
        "fr": "Council multi-LLM.",
        "ar": "مجلس متعدد النماذج اللغوية.",
        "en": "Multi-LLM council."
    },
    "app_ithy_desc": {
        "fr": "Agent IA conversationnel.",
        "ar": "وكيل ذكاء اصطناعي محادثة.",
        "en": "Conversational AI agent."
    },
    "app_notebook_lm_desc": {
        "fr": "Notebook IA interactif.",
        "ar": "دفتر ذكاء اصطناعي تفاعلي.",
        "en": "Interactive AI notebook."
    },
    "app_ai_searcher_desc": {
        "fr": "Moteur recherche IA.",
        "ar": "محرك بحث بالذكاء الاصطناعي.",
        "en": "AI search engine."
    },
    "app_prompt_creator_desc": {
        "fr": "Créateur prompts IA.",
        "ar": "منشئ المطالبات بالذكاء الاصطناعي.",
        "en": "AI prompt creator."
    },
    "app_chatbot_ia_desc": {
        "fr": "Chatbot IA personnalisable.",
        "ar": "روبوت محادثة قابل للتخصيص.",
        "en": "Customizable AI chatbot."
    },
    "app_bolt_diy_desc": {
        "fr": "Backend IA personnalisable.",
        "ar": "خلفية ذكاء اصطناعي قابلة للتخصيص.",
        "en": "Customizable AI backend."
    },
    "app_bmad_desc": {
        "fr": "Multi-agents development.",
        "ar": "تطوير متعدد الوكلاء.",
        "en": "Multi-agent development."
    },
    "app_voice_assistant_desc": {
        "fr": "Assistant vocal IA.",
        "ar": "مساعد صوتي بالذكاء الاصطناعي.",
        "en": "AI voice assistant."
    },
    "app_dzirvideo_ai_desc": {
        "fr": "Création vidéo IA.",
        "ar": "إنشاء فيديو بالذكاء الاصطناعي.",
        "en": "AI video creation."
    },
    "app_seo_dz_desc": {
        "fr": "Optimisation SEO Algérie.",
        "ar": "تحسين محركات البحث الجزائر.",
        "en": "Algerian SEO optimization."
    },
    "app_seo_dz_boost_desc": {
        "fr": "Boost SEO avancé.",
        "ar": "تعزيز تحسين محركات البحث المتقدم.",
        "en": "Advanced SEO boost."
    },

    # Religion
    "app_islam_dz_desc": {
        "fr": "Assistant religieux islamique.",
        "ar": "مساعد ديني إسلامي.",
        "en": "Islamic religious assistant."
    },

    # Education Apps
    "app_prof_dz_desc": {
        "fr": "Assistant pédagogique IA.",
        "ar": "مساعد تعليمي بالذكاء الاصطناعي.",
        "en": "AI educational assistant."
    },
    "app_universite_dz_desc": {
        "fr": "Plateforme université IA.",
        "ar": "منصة جامعية بالذكاء الاصطناعي.",
        "en": "AI university platform."
    },
    "app_formation_pro_desc": {
        "fr": "Formation professionnelle IA.",
        "ar": "التدريب المهني بالذكاء الاصطناعي.",
        "en": "AI professional training."
    },

    # Agriculture Apps
    "app_agri_dz_desc": {
        "fr": "Solutions agricoles IA.",
        "ar": "حلول زراعية بالذكاء الاصطناعي.",
        "en": "AI agricultural solutions."
    },
    "app_irrigation_dz_desc": {
        "fr": "Gestion irrigation intelligente.",
        "ar": "إدارة الري الذكية.",
        "en": "Smart irrigation management."
    },
    "app_agroalimentaire_desc": {
        "fr": "Solutions agroalimentaires.",
        "ar": "حلول صناعة الأغذية الزراعية.",
        "en": "Agri-food solutions."
    },

    # Health Apps
    "app_med_dz_desc": {
        "fr": "Assistant médical IA.",
        "ar": "مساعد طبي بالذكاء الاصطناعي.",
        "en": "AI medical assistant."
    },
    "app_clinique_dz_desc": {
        "fr": "Gestion clinique IA.",
        "ar": "إدارة العيادات بالذكاء الاصطناعي.",
        "en": "AI clinic management."
    },
    "app_pharma_dz_desc": {
        "fr": "Pharmacie intelligente.",
        "ar": "صيدلية ذكية.",
        "en": "Smart pharmacy."
    },

    # Industry Apps
    "app_industrie_dz_desc": {
        "fr": "Solutions industrie 4.0.",
        "ar": "حلول الصناعة 4.0.",
        "en": "Industry 4.0 solutions."
    },

    # BTP Apps
    "app_btp_dz_desc": {
        "fr": "Gestion projets BTP.",
        "ar": "إدارة مشاريع البناء.",
        "en": "Construction project management."
    },

    # Logistics Apps
    "app_transport_dz_desc": {
        "fr": "Gestion transport IA.",
        "ar": "إدارة النقل بالذكاء الاصطناعي.",
        "en": "AI transport management."
    },

    # Developer Tools
    "app_dev_portal_desc": {
        "fr": "Portail développeurs.",
        "ar": "بوابة المطورين.",
        "en": "Developer portal."
    },
    "app_api_portal_desc": {
        "fr": "Portail API.",
        "ar": "بوابة واجهة برمجة التطبيقات.",
        "en": "API portal."
    },

    # Monitoring
    "app_dashboard_central_desc": {
        "fr": "Dashboard central monitoring.",
        "ar": "لوحة المراقبة المركزية.",
        "en": "Central monitoring dashboard."
    },
}

# Générer le code JavaScript
print("// ===== TRADUCTIONS APPS COMPLÈTES =====")
for key, trans in sorted(app_translations.items()):
    print(f'        "{key}": {{ fr: "{trans["fr"]}", ar: "{trans["ar"]}", en: "{trans["en"]}" }},')

print(f"\n// Total: {len(app_translations)} traductions d'apps générées")
