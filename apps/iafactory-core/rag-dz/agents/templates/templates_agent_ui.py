"""
Templates Agent - Interface Streamlit
Gestionnaire de templates et modèles pour agents
"""
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TRANSLATIONS = {
    "fr": {
        "title": "Templates Agent",
        "subtitle": "Gestionnaire de Templates & Prompts",
        "welcome": "Bienvenue ! Explorez et utilisez les templates pour vos agents IA.",
        "input_placeholder": "Rechercher ou créer un template...",
        "categories": "Catégories",
        "prompts": "Prompts système",
        "configs": "Configurations",
        "docs": "Modèles docs",
        "workflows": "Workflows",
        "new_template": "Nouveau template",
        "processing": "Génération...",
        "search": "Rechercher",
        "popular": "Populaires",
        "recent": "Récents"
    },
    "en": {
        "title": "Templates Agent",
        "subtitle": "Templates & Prompts Manager",
        "welcome": "Welcome! Explore and use templates for your AI agents.",
        "input_placeholder": "Search or create a template...",
        "categories": "Categories",
        "prompts": "System prompts",
        "configs": "Configurations",
        "docs": "Doc templates",
        "workflows": "Workflows",
        "new_template": "New template",
        "processing": "Generating...",
        "search": "Search",
        "popular": "Popular",
        "recent": "Recent"
    },
    "ar": {
        "title": "وكيل القوالب",
        "subtitle": "مدير القوالب والبرومبت",
        "welcome": "مرحبًا! استكشف واستخدم القوالب لوكلاء الذكاء الاصطناعي.",
        "input_placeholder": "البحث أو إنشاء قالب...",
        "categories": "الفئات",
        "prompts": "برومبت النظام",
        "configs": "التكوينات",
        "docs": "قوالب المستندات",
        "workflows": "سير العمل",
        "new_template": "قالب جديد",
        "processing": "جاري التوليد...",
        "search": "بحث",
        "popular": "شائعة",
        "recent": "حديثة"
    }
}

def t(key):
    lang = st.session_state.get('language', 'fr')
    return TRANSLATIONS.get(lang, TRANSLATIONS['fr']).get(key, key)

def inject_css():
    st.markdown("""
    <style>
        .main .block-container { padding-top: 2rem; max-width: 1100px; }
        .stButton > button { background: linear-gradient(135deg, #00a651, #00d66a) !important;
            color: white !important; border: none !important; border-radius: 10px !important; }
        .template-card { background: rgba(0,166,81,0.05); padding: 1rem; border-radius: 12px;
            border: 1px solid rgba(0,166,81,0.2); margin: 0.5rem 0; cursor: pointer;
            transition: all 0.3s; }
        .template-card:hover { border-color: #00a651; transform: translateY(-2px); }
        .iaf-header { display: flex; align-items: center; gap: 12px;
            padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.12); }
        .iaf-title { font-size: 1.8rem; font-weight: 700;
            background: linear-gradient(135deg, #00a651, #00d66a);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .code-block { background: #1a1a24; padding: 1rem; border-radius: 8px;
            font-family: monospace; font-size: 0.9rem; overflow-x: auto; }
    </style>
    """, unsafe_allow_html=True)

TEMPLATES = {
    "prompts": [
        {"name": "Customer Support Agent", "desc": "Template pour agent support client", "uses": 1234},
        {"name": "Legal Advisor", "desc": "Prompt pour conseils juridiques", "uses": 856},
        {"name": "Sales Assistant", "desc": "Agent commercial B2B", "uses": 723},
    ],
    "configs": [
        {"name": "Multi-Agent Setup", "desc": "Configuration multi-agents", "uses": 445},
        {"name": "RAG Pipeline", "desc": "Pipeline RAG standard", "uses": 612},
    ],
    "docs": [
        {"name": "Business Report", "desc": "Modèle rapport business", "uses": 389},
        {"name": "Invoice Template", "desc": "Template facture DZD", "uses": 567},
    ]
}

def main():
    st.set_page_config(page_title="Templates Agent | IAFactory", page_icon="📄", layout="wide")

    if 'language' not in st.session_state:
        st.session_state.language = 'fr'
    if 'selected_template' not in st.session_state:
        st.session_state.selected_template = None

    inject_css()

    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f'<div class="iaf-header"><span style="font-size:2rem">📄</span><span class="iaf-title">{t("title")}</span></div>', unsafe_allow_html=True)
        st.markdown(f"*{t('subtitle')}*")
    with col2:
        lang = st.selectbox("", ['fr', 'en', 'ar'], format_func=lambda x: {'fr': '🇫🇷 FR', 'en': '🇬🇧 EN', 'ar': '🇩🇿 AR'}[x],
                           index=['fr', 'en', 'ar'].index(st.session_state.language), label_visibility="collapsed")
        if lang != st.session_state.language:
            st.session_state.language = lang
            st.rerun()

    # Sidebar
    with st.sidebar:
        st.markdown(f"### {t('search')}")
        search = st.text_input("", placeholder="🔍 Rechercher...", label_visibility="collapsed")

        st.markdown("---")
        st.markdown(f"### {t('categories')}")
        categories = [('prompts', t('prompts'), '💬'), ('configs', t('configs'), '⚙️'),
                     ('docs', t('docs'), '📋'), ('workflows', t('workflows'), '🔄')]
        selected_cat = st.radio("", [f"{icon} {name}" for _, name, icon in categories], label_visibility="collapsed")

        st.markdown("---")
        if st.button(f"➕ {t('new_template')}", use_container_width=True):
            st.session_state.selected_template = "new"

    # Main content
    tabs = st.tabs([f"⭐ {t('popular')}", f"🕐 {t('recent')}"])

    with tabs[0]:
        st.markdown("### Templates Populaires")
        for cat, templates in TEMPLATES.items():
            st.markdown(f"**{cat.title()}**")
            cols = st.columns(3)
            for i, tpl in enumerate(templates):
                with cols[i % 3]:
                    if st.button(f"📄 {tpl['name']}\n_{tpl['desc']}_\n`{tpl['uses']} utilisations`", key=f"tpl_{cat}_{i}", use_container_width=True):
                        st.session_state.selected_template = tpl['name']

    with tabs[1]:
        st.markdown("### Templates Récents")
        st.info("Vos templates récemment utilisés apparaîtront ici.")

    # Template detail
    if st.session_state.selected_template and st.session_state.selected_template != "new":
        st.markdown("---")
        st.markdown(f"### 📄 {st.session_state.selected_template}")
        st.markdown('<div class="code-block">Tu es un assistant IA spécialisé...\n\nRègles:\n1. Répondre en français\n2. Être concis\n3. Citer les sources</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.button("📋 Copier", use_container_width=True)
        with col2:
            st.button("✏️ Modifier", use_container_width=True)

if __name__ == "__main__":
    main()
