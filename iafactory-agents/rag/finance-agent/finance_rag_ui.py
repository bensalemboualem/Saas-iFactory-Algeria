"""
Finance RAG Agent - Interface Streamlit
Agent RAG spécialisé documents financiers
"""
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TRANSLATIONS = {
    "fr": {
        "title": "Finance RAG Agent",
        "subtitle": "Analyse de Documents Financiers",
        "welcome": "Importez vos documents financiers (bilans, états financiers, rapports) et posez vos questions.",
        "upload": "Importer documents",
        "upload_desc": "PDF, Excel, Word",
        "input_placeholder": "Posez une question sur vos documents financiers...",
        "analyze": "Analyser",
        "new_session": "Nouvelle session",
        "processing": "Analyse RAG en cours...",
        "docs_loaded": "Documents chargés",
        "features": "Fonctionnalités",
        "feat_balance": "Analyse bilans",
        "feat_ratios": "Calcul ratios",
        "feat_compare": "Comparaison périodes",
        "feat_forecast": "Prévisions"
    },
    "en": {
        "title": "Finance RAG Agent",
        "subtitle": "Financial Document Analysis",
        "welcome": "Upload your financial documents (balance sheets, financial statements, reports) and ask your questions.",
        "upload": "Upload documents",
        "upload_desc": "PDF, Excel, Word",
        "input_placeholder": "Ask a question about your financial documents...",
        "analyze": "Analyze",
        "new_session": "New session",
        "processing": "RAG analysis in progress...",
        "docs_loaded": "Documents loaded",
        "features": "Features",
        "feat_balance": "Balance analysis",
        "feat_ratios": "Ratio calculation",
        "feat_compare": "Period comparison",
        "feat_forecast": "Forecasts"
    },
    "ar": {
        "title": "وكيل Finance RAG",
        "subtitle": "تحليل المستندات المالية",
        "welcome": "ارفع مستنداتك المالية واطرح أسئلتك.",
        "upload": "رفع المستندات",
        "upload_desc": "PDF، Excel، Word",
        "input_placeholder": "اطرح سؤالاً عن مستنداتك المالية...",
        "analyze": "تحليل",
        "new_session": "جلسة جديدة",
        "processing": "جاري تحليل RAG...",
        "docs_loaded": "المستندات المحملة",
        "features": "الميزات",
        "feat_balance": "تحليل الميزانية",
        "feat_ratios": "حساب النسب",
        "feat_compare": "مقارنة الفترات",
        "feat_forecast": "التوقعات"
    }
}

def t(key):
    lang = st.session_state.get('language', 'fr')
    return TRANSLATIONS.get(lang, TRANSLATIONS['fr']).get(key, key)

def inject_css():
    st.markdown("""
    <style>
        .main .block-container { padding-top: 2rem; max-width: 1000px; }
        .stButton > button { background: linear-gradient(135deg, #00a651, #00d66a) !important;
            color: white !important; border: none !important; border-radius: 10px !important; }
        .doc-badge { background: rgba(0,166,81,0.1); padding: 8px 16px; border-radius: 8px;
            margin: 4px; display: inline-block; border: 1px solid rgba(0,166,81,0.2); }
        .iaf-header { display: flex; align-items: center; gap: 12px;
            padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.12); }
        .iaf-title { font-size: 1.8rem; font-weight: 700;
            background: linear-gradient(135deg, #00a651, #00d66a);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    </style>
    """, unsafe_allow_html=True)

def analyze_financial_query(query, docs):
    """Simulate RAG financial analysis"""
    if "ratio" in query.lower() or "rentabilité" in query.lower():
        return """📊 **Analyse des Ratios Financiers**

Basé sur les documents fournis:

| Ratio | Valeur | Interprétation |
|-------|--------|----------------|
| ROE | 15.2% | ✅ Bon |
| ROA | 8.7% | ✅ Acceptable |
| Liquidité générale | 1.8 | ✅ Sain |
| Endettement | 45% | ⚠️ À surveiller |

**Recommandation:** La rentabilité est satisfaisante mais l'endettement mérite attention."""

    elif "bilan" in query.lower():
        return """📋 **Synthèse du Bilan**

**Actif:**
- Immobilisations: 45 000 000 DZD
- Stocks: 12 000 000 DZD
- Créances clients: 8 500 000 DZD
- Trésorerie: 3 200 000 DZD

**Passif:**
- Capitaux propres: 35 000 000 DZD
- Dettes financières: 25 000 000 DZD
- Dettes fournisseurs: 8 700 000 DZD

**Total Bilan:** 68 700 000 DZD"""

    return "Pour analyser vos documents financiers, veuillez d'abord les importer puis poser une question spécifique sur les ratios, le bilan, ou les performances."

def main():
    st.set_page_config(page_title="Finance RAG | IAFactory", page_icon="📈", layout="wide")

    if 'language' not in st.session_state:
        st.session_state.language = 'fr'
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'documents' not in st.session_state:
        st.session_state.documents = []

    inject_css()

    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f'<div class="iaf-header"><span style="font-size:2rem">📈</span><span class="iaf-title">{t("title")}</span></div>', unsafe_allow_html=True)
        st.markdown(f"*{t('subtitle')}*")
    with col2:
        lang = st.selectbox("", ['fr', 'en', 'ar'], format_func=lambda x: {'fr': '🇫🇷 FR', 'en': '🇬🇧 EN', 'ar': '🇩🇿 AR'}[x],
                           index=['fr', 'en', 'ar'].index(st.session_state.language), label_visibility="collapsed")
        if lang != st.session_state.language:
            st.session_state.language = lang
            st.rerun()

    # Sidebar
    with st.sidebar:
        st.markdown(f"### {t('upload')}")
        st.caption(t('upload_desc'))
        uploaded = st.file_uploader("", type=['pdf', 'xlsx', 'docx', 'csv'], accept_multiple_files=True, label_visibility="collapsed")

        if uploaded:
            for f in uploaded:
                if f.name not in [d['name'] for d in st.session_state.documents]:
                    st.session_state.documents.append({'name': f.name, 'size': f.size})

        if st.session_state.documents:
            st.markdown(f"### {t('docs_loaded')}")
            for doc in st.session_state.documents:
                st.markdown(f'<span class="doc-badge">📄 {doc["name"]}</span>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(f"### {t('features')}")
        features = [('balance', t('feat_balance'), '📋'), ('ratios', t('feat_ratios'), '📊'),
                   ('compare', t('feat_compare'), '🔄'), ('forecast', t('feat_forecast'), '🔮')]
        for f_id, f_name, icon in features:
            st.markdown(f"{icon} {f_name}")

        st.markdown("---")
        if st.button(f"🔄 {t('new_session')}", use_container_width=True):
            st.session_state.messages = []
            st.session_state.documents = []
            st.rerun()

    # Main
    if not st.session_state.documents:
        st.info(t('welcome'))
    else:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    if prompt := st.chat_input(t('input_placeholder')):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner(t('processing')):
                response = analyze_financial_query(prompt, st.session_state.documents)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

if __name__ == "__main__":
    main()
