#!/usr/bin/env python3
"""
Script pour ajouter les traductions AR/EN aux cartes d'applications
"""

# Traductions des badges communs
badge_translations = {
    "IA & Agents": {"fr": "IA & Agents", "ar": "الذكاء الاصطناعي والوكلاء", "en": "AI & Agents"},
    "Business": {"fr": "Business", "ar": "الأعمال", "en": "Business"},
    "Finance": {"fr": "Finance", "ar": "المالية", "en": "Finance"},
    "Juridique": {"fr": "Juridique", "ar": "قانوني", "en": "Legal"},
    "Agriculture": {"fr": "Agriculture", "ar": "الزراعة", "en": "Agriculture"},
    "Santé": {"fr": "Santé", "ar": "الصحة", "en": "Health"},
    "Industrie": {"fr": "Industrie", "ar": "الصناعة", "en": "Industry"},
    "BTP": {"fr": "BTP", "ar": "البناء والأشغال العمومية", "en": "Construction"},
    "Logistique": {"fr": "Logistique", "ar": "اللوجستيات", "en": "Logistics"},
    "Commerce": {"fr": "Commerce", "ar": "التجارة", "en": "Commerce"},
    "Éducation": {"fr": "Éducation", "ar": "التعليم", "en": "Education"},
    "Religion": {"fr": "Religion", "ar": "الدين", "en": "Religion"},
    "Développeur": {"fr": "Développeur", "ar": "المطور", "en": "Developer"},
    "Monitoring": {"fr": "Monitoring", "ar": "المراقبة", "en": "Monitoring"},
    "Infrastructure": {"fr": "Infrastructure", "ar": "البنية التحتية", "en": "Infrastructure"},
}

# Traductions des apps principales (échantillon)
app_translations = {
    "archon_ui_title": {"fr": "🎛️ Archon UI", "ar": "🎛️ أركون واجهة", "en": "🎛️ Archon UI"},
    "archon_ui_desc": {"fr": "Interface multi-agents complète.", "ar": "واجهة متعددة الوكلاء الكاملة.", "en": "Complete multi-agent interface."},

    "pme_copilot_title": {"fr": "🚀 PME Copilot", "ar": "🚀 مساعد المؤسسات الصغيرة", "en": "🚀 SME Copilot"},
    "pme_copilot_desc": {"fr": "Assistant IA pour PME.", "ar": "مساعد ذكاء اصطناعي للمؤسسات الصغيرة.", "en": "AI assistant for SMEs."},

    "crm_ia_title": {"fr": "🤝 CRM IA", "ar": "🤝 إدارة العملاء بالذكاء الاصطناعي", "en": "🤝 AI CRM"},
    "crm_ia_desc": {"fr": "CRM intelligent avec IA.", "ar": "إدارة علاقات العملاء الذكية بالذكاء الاصطناعي.", "en": "Intelligent CRM with AI."},

    "data_dz_title": {"fr": "📊 Data-DZ Dashboard", "ar": "📊 لوحة بيانات الجزائر", "en": "📊 Data-DZ Dashboard"},
    "data_dz_desc": {"fr": "Tableaux de bord analytiques.", "ar": "لوحات المعلومات التحليلية.", "en": "Analytical dashboards."},

    "fiscal_assistant_title": {"fr": "💰 Fiscal Assistant", "ar": "💰 مساعد ضريبي", "en": "💰 Fiscal Assistant"},
    "fiscal_assistant_desc": {"fr": "Assistant fiscal algérien.", "ar": "مساعد ضريبي جزائري.", "en": "Algerian tax assistant."},

    "legal_assistant_title": {"fr": "⚖️ Legal Assistant", "ar": "⚖️ مساعد قانوني", "en": "⚖️ Legal Assistant"},
    "legal_assistant_desc": {"fr": "Assistant juridique IA.", "ar": "مساعد قانوني بالذكاء الاصطناعي.", "en": "AI legal assistant."},

    "agri_dz_title": {"fr": "🌾 Agri-DZ", "ar": "🌾 الزراعة الجزائرية", "en": "🌾 Agri-DZ"},
    "agri_dz_desc": {"fr": "Solutions agricoles IA.", "ar": "حلول زراعية بالذكاء الاصطناعي.", "en": "AI agricultural solutions."},

    "med_dz_title": {"fr": "🏥 Med-DZ", "ar": "🏥 الطب الجزائري", "en": "🏥 Med-DZ"},
    "med_dz_desc": {"fr": "Assistant médical IA.", "ar": "مساعد طبي بالذكاء الاصطناعي.", "en": "AI medical assistant."},

    "industrie_dz_title": {"fr": "🏭 Industrie-DZ", "ar": "🏭 الصناعة الجزائرية", "en": "🏭 Industry-DZ"},
    "industrie_dz_desc": {"fr": "Solutions industrie 4.0.", "ar": "حلول الصناعة 4.0.", "en": "Industry 4.0 solutions."},

    "btp_dz_title": {"fr": "🏗️ BTP-DZ", "ar": "🏗️ البناء الجزائري", "en": "🏗️ Construction-DZ"},
    "btp_dz_desc": {"fr": "Gestion projets BTP.", "ar": "إدارة مشاريع البناء.", "en": "Construction project management."},

    "islam_dz_title": {"fr": "☪️ Islam-DZ", "ar": "☪️ الإسلام الجزائري", "en": "☪️ Islam-DZ"},
    "islam_dz_desc": {"fr": "Assistant religieux islamique.", "ar": "مساعد ديني إسلامي.", "en": "Islamic religious assistant."},

    "prof_dz_title": {"fr": "👨‍🏫 Prof-DZ", "ar": "👨‍🏫 الأستاذ الجزائري", "en": "👨‍🏫 Prof-DZ"},
    "prof_dz_desc": {"fr": "Assistant pédagogique IA.", "ar": "مساعد تعليمي بالذكاء الاصطناعي.", "en": "AI educational assistant."},

    "bolt_diy_title": {"fr": "⚡ Bolt.DIY", "ar": "⚡ بولت افعلها بنفسك", "en": "⚡ Bolt.DIY"},
    "bolt_diy_desc": {"fr": "Backend IA personnalisable.", "ar": "خلفية ذكاء اصطناعي قابلة للتخصيص.", "en": "Customizable AI backend."},

    "bmad_title": {"fr": "🧠 BMAD", "ar": "🧠 بماد", "en": "🧠 BMAD"},
    "bmad_desc": {"fr": "Multi-agents development.", "ar": "تطوير متعدد الوكلاء.", "en": "Multi-agent development."},
}

# Traductions boutons communs
button_translations = {
    "btn_open": {"fr": "Ouvrir", "ar": "فتح", "en": "Open"},
    "btn_access": {"fr": "Accéder", "ar": "دخول", "en": "Access"},
    "btn_discover": {"fr": "Découvrir", "ar": "اكتشف", "en": "Discover"},
    "btn_launch": {"fr": "Lancer", "ar": "تشغيل", "en": "Launch"},
}

# Générer le dictionnaire de traductions complet pour JavaScript
all_translations = {}
all_translations.update(badge_translations)
all_translations.update(app_translations)
all_translations.update(button_translations)

# Générer le code JavaScript
js_translations = []
for key, translations in all_translations.items():
    key_safe = key.replace(" ", "_").replace("&", "and").lower()
    js_line = f'        "{key_safe}": {{ fr: "{translations["fr"]}", ar: "{translations["ar"]}", en: "{translations["en"]}" }},'
    js_translations.append(js_line)

print("=" * 80)
print("TRADUCTIONS À AJOUTER DANS IAFactoryI18n.translations")
print("=" * 80)
print("\n".join(js_translations))

print("\n" + "=" * 80)
print("EXEMPLE D'UTILISATION DANS HTML")
print("=" * 80)
print("""
<!-- Avant -->
<article class="app-card" data-category="business" data-audience="user">
    <h5>🚀 PME Copilot</h5>
    <div class="badge">Business</div>
    <p>Assistant IA pour PME.</p>
    <button type="button" class="btn-round btn-secondary" onclick="...">Ouvrir</button>
</article>

<!-- Après -->
<article class="app-card" data-category="business" data-audience="user">
    <h5 data-i18n="pme_copilot_title">🚀 PME Copilot</h5>
    <div class="badge" data-i18n="business">Business</div>
    <p data-i18n="pme_copilot_desc">Assistant IA pour PME.</p>
    <button type="button" class="btn-round btn-secondary" data-i18n="btn_open" onclick="...">Ouvrir</button>
</article>
""")

print("\n" + "=" * 80)
print(f"TOTAL TRADUCTIONS: {len(all_translations)}")
print("=" * 80)
