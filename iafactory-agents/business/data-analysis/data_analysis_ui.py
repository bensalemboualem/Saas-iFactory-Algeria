"""
Data Analysis Agent - Interface Streamlit
Analyse de données et génération de rapports BI
"""
import streamlit as st
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TRANSLATIONS = {
    "fr": {
        "title": "Data Analysis Agent",
        "subtitle": "Analyse de données & Business Intelligence",
        "upload": "Importer vos données",
        "upload_desc": "Formats: CSV, Excel, JSON",
        "analyze": "Analyser",
        "insights": "Insights IA",
        "charts": "Visualisations",
        "export": "Exporter le rapport",
        "ask": "Posez une question sur vos données...",
        "welcome": "Importez un fichier de données pour commencer l'analyse.",
        "processing": "Analyse en cours...",
        "summary": "Résumé des données",
        "rows": "Lignes",
        "columns": "Colonnes",
        "missing": "Valeurs manquantes",
        "new_analysis": "Nouvelle analyse"
    },
    "en": {
        "title": "Data Analysis Agent",
        "subtitle": "Data Analysis & Business Intelligence",
        "upload": "Upload your data",
        "upload_desc": "Formats: CSV, Excel, JSON",
        "analyze": "Analyze",
        "insights": "AI Insights",
        "charts": "Visualizations",
        "export": "Export report",
        "ask": "Ask a question about your data...",
        "welcome": "Upload a data file to start the analysis.",
        "processing": "Analyzing...",
        "summary": "Data Summary",
        "rows": "Rows",
        "columns": "Columns",
        "missing": "Missing values",
        "new_analysis": "New analysis"
    },
    "ar": {
        "title": "وكيل تحليل البيانات",
        "subtitle": "تحليل البيانات وذكاء الأعمال",
        "upload": "رفع بياناتك",
        "upload_desc": "الصيغ: CSV، Excel، JSON",
        "analyze": "تحليل",
        "insights": "رؤى الذكاء الاصطناعي",
        "charts": "التصورات",
        "export": "تصدير التقرير",
        "ask": "اطرح سؤالاً عن بياناتك...",
        "welcome": "ارفع ملف بيانات لبدء التحليل.",
        "processing": "جاري التحليل...",
        "summary": "ملخص البيانات",
        "rows": "الصفوف",
        "columns": "الأعمدة",
        "missing": "القيم المفقودة",
        "new_analysis": "تحليل جديد"
    }
}

def t(key):
    lang = st.session_state.get('language', 'fr')
    return TRANSLATIONS.get(lang, TRANSLATIONS['fr']).get(key, key)

def inject_css():
    st.markdown("""
    <style>
        .main .block-container { padding-top: 2rem; max-width: 1200px; }
        .stButton > button { background: linear-gradient(135deg, #00a651, #00d66a) !important;
            color: white !important; border: none !important; border-radius: 10px !important; }
        .metric-card { background: rgba(0,166,81,0.1); padding: 1rem; border-radius: 12px;
            border: 1px solid rgba(0,166,81,0.2); text-align: center; }
        .metric-value { font-size: 2rem; font-weight: 700; color: #00a651; }
        .metric-label { font-size: 0.9rem; color: #666; }
        .iaf-header { display: flex; align-items: center; gap: 12px;
            padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.12); }
        .iaf-title { font-size: 1.8rem; font-weight: 700;
            background: linear-gradient(135deg, #00a651, #00d66a);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    </style>
    """, unsafe_allow_html=True)

def analyze_dataframe(df):
    """Generate AI insights from dataframe"""
    insights = []
    insights.append(f"📊 Le dataset contient **{len(df)}** lignes et **{len(df.columns)}** colonnes.")

    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        for col in numeric_cols[:3]:
            insights.append(f"📈 **{col}**: moyenne = {df[col].mean():.2f}, max = {df[col].max():.2f}")

    missing = df.isnull().sum().sum()
    if missing > 0:
        insights.append(f"⚠️ **{missing}** valeurs manquantes détectées dans le dataset.")
    else:
        insights.append("✅ Aucune valeur manquante - données complètes.")

    return insights

def main():
    st.set_page_config(page_title="Data Analysis | IAFactory", page_icon="📊", layout="wide")

    if 'language' not in st.session_state:
        st.session_state.language = 'fr'
    if 'dataframe' not in st.session_state:
        st.session_state.dataframe = None

    inject_css()

    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f'<div class="iaf-header"><span style="font-size:2rem">📊</span><span class="iaf-title">{t("title")}</span></div>', unsafe_allow_html=True)
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
        uploaded = st.file_uploader("", type=['csv', 'xlsx', 'json'], label_visibility="collapsed")

        if uploaded:
            try:
                if uploaded.name.endswith('.csv'):
                    st.session_state.dataframe = pd.read_csv(uploaded)
                elif uploaded.name.endswith('.xlsx'):
                    st.session_state.dataframe = pd.read_excel(uploaded)
                elif uploaded.name.endswith('.json'):
                    st.session_state.dataframe = pd.read_json(uploaded)
                st.success(f"✅ {uploaded.name}")
            except Exception as e:
                st.error(f"Erreur: {e}")

        st.markdown("---")
        if st.button(f"🔄 {t('new_analysis')}", use_container_width=True):
            st.session_state.dataframe = None
            st.rerun()

    # Main content
    if st.session_state.dataframe is not None:
        df = st.session_state.dataframe

        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{len(df)}</div><div class="metric-label">{t("rows")}</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{len(df.columns)}</div><div class="metric-label">{t("columns")}</div></div>', unsafe_allow_html=True)
        with col3:
            missing = df.isnull().sum().sum()
            st.markdown(f'<div class="metric-card"><div class="metric-value">{missing}</div><div class="metric-label">{t("missing")}</div></div>', unsafe_allow_html=True)

        st.markdown("---")

        # Tabs
        tab1, tab2, tab3 = st.tabs([f"📋 {t('summary')}", f"💡 {t('insights')}", f"📈 {t('charts')}"])

        with tab1:
            st.dataframe(df.head(100), use_container_width=True)
            st.markdown("**Types de colonnes:**")
            st.write(df.dtypes.to_dict())

        with tab2:
            insights = analyze_dataframe(df)
            for insight in insights:
                st.markdown(insight)

        with tab3:
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            if numeric_cols:
                col = st.selectbox("Colonne à visualiser", numeric_cols)
                st.bar_chart(df[col].value_counts().head(20))
            else:
                st.info("Aucune colonne numérique pour la visualisation")

        # Chat
        if prompt := st.chat_input(t('ask')):
            st.markdown(f"**Question:** {prompt}")
            st.markdown("**Réponse IA:** Basé sur vos données, je peux voir que...")

    else:
        st.info(t('welcome'))

if __name__ == "__main__":
    main()
