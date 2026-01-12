"""
BBC School - Démo Ministre (Version BBC Spécifique)
Interface Streamlit Premium - Version OFF par défaut (activer si deal confirmé)

USAGE:
    Pour activer cette version, modifiez config.py:
    - Mettez VERSIONS["bbc"]["enabled"] = True
    - Mettez VERSIONS["generic"]["enabled"] = False
"""

import streamlit as st
import time
from datetime import datetime
import json
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Import configuration - Force BBC config
from config import get_config_by_name, VERSIONS

# Force BBC configuration
BBC_CONFIG = get_config_by_name("bbc")

# ============================================
# TRANSLATOR CLASS
# ============================================
class Translator:
    def __init__(self, lang='fr'):
        self.lang = lang
        self.translations = self._load_translations()

    def _load_translations(self) -> dict:
        locale_path = os.path.join(os.path.dirname(__file__), 'locales', f'{self.lang}.json')
        try:
            with open(locale_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            fallback_path = os.path.join(os.path.dirname(__file__), 'locales', 'fr.json')
            try:
                with open(fallback_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}

    def t(self, key: str, default: str = None) -> str:
        keys = key.split('.')
        value = self.translations
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default if default else key

    def is_rtl(self) -> bool:
        return self.lang == 'ar'


# ============================================
# BBC PREMIUM DESIGN - ALGERIA GREEN THEME
# ============================================
def get_bbc_css(theme: str, is_rtl: bool = False) -> str:
    """Generate BBC-specific CSS with Algeria Green theme"""

    # BBC uses Algeria Green as primary color
    primary_color = "#006233"  # Algeria Green
    secondary_color = "#D52B1E"  # Algeria Red (accent)

    if theme == 'dark':
        bg_primary = '#09090B'
        bg_secondary = '#18181B'
        bg_tertiary = '#27272A'
        bg_elevated = '#1F1F23'
        bg_hover = '#2D2D33'
        text_primary = '#FAFAFA'
        text_secondary = '#A1A1AA'
        text_tertiary = '#71717A'
        accent_primary = '#34D399'  # Lighter green for dark mode
        accent_light = '#064E3B'
        success = '#34D399'
        success_bg = '#064E3B'
        success_text = '#A7F3D0'
        warning = '#FBBF24'
        border_light = '#27272A'
        border_medium = '#3F3F46'
        shadow_color = 'rgba(0,0,0,0.5)'
    else:
        bg_primary = '#FFFFFF'
        bg_secondary = '#FAFAFA'
        bg_tertiary = '#F4F4F5'
        bg_elevated = '#FFFFFF'
        bg_hover = '#F4F4F5'
        text_primary = '#18181B'
        text_secondary = '#52525B'
        text_tertiary = '#A1A1AA'
        accent_primary = primary_color
        accent_light = '#D1FAE5'
        success = '#10B981'
        success_bg = '#D1FAE5'
        success_text = '#065F46'
        warning = '#F59E0B'
        border_light = '#E4E4E7'
        border_medium = '#D4D4D8'
        shadow_color = 'rgba(0,0,0,0.08)'

    direction = 'rtl' if is_rtl else 'ltr'
    text_align = 'right' if is_rtl else 'left'
    border_side = 'right' if is_rtl else 'left'
    opposite_side = 'left' if is_rtl else 'right'

    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        :root {{
            --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            --radius-sm: 6px;
            --radius-md: 8px;
            --radius-lg: 12px;
            --radius-xl: 16px;
            --radius-full: 9999px;
            --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
            --transition-base: 200ms cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .stApp {{
            background-color: {bg_primary} !important;
            font-family: var(--font-sans) !important;
            direction: {direction};
        }}

        #MainMenu, footer, header[data-testid="stHeader"] {{ visibility: hidden; }}

        h1, h2, h3, h4, h5, h6 {{
            font-family: var(--font-sans) !important;
            font-weight: 600 !important;
            color: {text_primary} !important;
            letter-spacing: -0.02em;
            direction: {direction};
            text-align: {text_align};
        }}

        p, span, div, li {{
            font-family: var(--font-sans) !important;
            color: {text_secondary};
            direction: {direction};
            text-align: {text_align};
        }}

        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {primary_color} 0%, #004d26 100%) !important;
            border-{opposite_side}: none !important;
        }}

        section[data-testid="stSidebar"] * {{
            color: white !important;
        }}

        section[data-testid="stSidebar"] [data-testid="stMetricValue"] {{
            color: #FFD700 !important;
        }}

        section[data-testid="stSidebar"] [data-testid="stMetricDelta"] {{
            color: #90EE90 !important;
        }}

        [data-testid="stMetric"] {{
            background: {bg_elevated} !important;
            border: 1px solid {border_light} !important;
            border-radius: var(--radius-lg) !important;
            padding: 1rem 1.25rem !important;
        }}

        [data-testid="stMetricLabel"] {{
            font-size: 0.75rem !important;
            font-weight: 500 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            color: {text_tertiary} !important;
        }}

        [data-testid="stMetricValue"] {{
            font-size: 1.75rem !important;
            font-weight: 700 !important;
            color: {text_primary} !important;
        }}

        .stTabs [data-baseweb="tab-list"] {{
            background: {bg_tertiary} !important;
            border-radius: var(--radius-lg) !important;
            padding: 4px !important;
            border: 1px solid {border_light} !important;
        }}

        .stTabs [data-baseweb="tab"] {{
            background: transparent !important;
            border-radius: var(--radius-md) !important;
            padding: 0.5rem 1rem !important;
            font-size: 0.875rem !important;
            font-weight: 500 !important;
            color: {text_secondary} !important;
        }}

        .stTabs [aria-selected="true"] {{
            background: {primary_color} !important;
            color: white !important;
        }}

        .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {{ display: none !important; }}

        .stButton > button {{
            background: linear-gradient(180deg, {primary_color} 0%, #004d26 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: var(--radius-md) !important;
            padding: 0.625rem 1rem !important;
            font-weight: 500 !important;
        }}

        .stButton > button:hover {{
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px {primary_color}60 !important;
        }}

        /* BBC-specific hero with Algeria flag pattern */
        .hero-header {{
            background: linear-gradient(135deg, {primary_color} 0%, #004d26 50%, {secondary_color} 100%);
            border-radius: var(--radius-xl);
            padding: 2rem;
            margin-bottom: 1.5rem;
            position: relative;
            overflow: hidden;
        }}

        .hero-header::before {{
            content: '🇩🇿';
            position: absolute;
            right: 20px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 4rem;
            opacity: 0.3;
        }}

        .hero-header h2 {{ color: white !important; text-align: center; position: relative; }}
        .hero-header p {{ color: rgba(255,255,255,0.9) !important; text-align: center; position: relative; }}

        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin-bottom: 1.5rem;
        }}

        .kpi-card {{
            background: {bg_elevated};
            border: 1px solid {border_light};
            border-radius: var(--radius-xl);
            padding: 1.5rem;
            position: relative;
            overflow: hidden;
            transition: var(--transition-base);
        }}

        .kpi-card:hover {{
            border-color: {primary_color};
            box-shadow: 0 8px 24px {primary_color}20;
            transform: translateY(-2px);
        }}

        .kpi-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
        }}

        .kpi-card.green::before {{ background: linear-gradient(90deg, {primary_color}, #00a86b); }}
        .kpi-card.blue::before {{ background: linear-gradient(90deg, #3B82F6, #60A5FA); }}
        .kpi-card.orange::before {{ background: linear-gradient(90deg, #F59E0B, #FBBF24); }}

        .kpi-label {{ font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: {text_tertiary}; margin-bottom: 0.5rem; }}
        .kpi-value {{ font-size: 2rem; font-weight: 700; color: {text_primary}; letter-spacing: -0.02em; }}
        .kpi-value.green {{ color: {primary_color}; }}
        .kpi-value.blue {{ color: #3B82F6; }}
        .kpi-value.orange {{ color: {warning}; }}
        .kpi-desc {{ font-size: 0.8125rem; color: {text_secondary}; margin-top: 0.5rem; }}

        .phase-card {{
            background: {bg_elevated};
            border: 1px solid {border_light};
            border-radius: var(--radius-lg);
            padding: 1.25rem 1.5rem;
            margin-bottom: 1rem;
            border-{border_side}: 4px solid;
        }}

        .phase-card.phase-1 {{ border-{border_side}-color: {primary_color}; }}
        .phase-card.phase-2 {{ border-{border_side}-color: #3B82F6; }}
        .phase-card.phase-3 {{ border-{border_side}-color: {warning}; }}

        .timeline-container {{ position: relative; padding-{border_side}: 2rem; }}
        .timeline-container::before {{
            content: '';
            position: absolute;
            {border_side}: 0.75rem;
            top: 0;
            bottom: 0;
            width: 2px;
            background: linear-gradient(180deg, {primary_color}, {warning});
        }}

        .timeline-item {{
            position: relative;
            background: {bg_elevated};
            border: 1px solid {border_light};
            border-radius: var(--radius-lg);
            padding: 1rem 1.25rem;
            margin-bottom: 0.75rem;
        }}

        .timeline-item::before {{
            content: '';
            position: absolute;
            {border_side}: -2rem;
            top: 1.25rem;
            width: 12px;
            height: 12px;
            background: {bg_primary};
            border: 2px solid {primary_color};
            border-radius: 50%;
        }}

        .timeline-item.milestone::before {{ background: {warning}; border-color: {warning}; }}
        .timeline-item.done::before {{ background: {primary_color}; border-color: {primary_color}; }}

        .timeline-date {{ font-size: 0.75rem; font-weight: 600; color: {primary_color}; text-transform: uppercase; }}
        .timeline-title {{ font-size: 0.9375rem; font-weight: 500; color: {text_primary}; margin: 0.25rem 0; }}
        .timeline-badge {{ display: inline-block; font-size: 0.6875rem; font-weight: 600; text-transform: uppercase; padding: 0.25rem 0.625rem; border-radius: var(--radius-full); background: {primary_color}20; color: {primary_color}; }}

        .testimonial-card {{
            background: {bg_elevated};
            border: 1px solid {border_light};
            border-radius: var(--radius-xl);
            padding: 1.5rem;
            margin-bottom: 1rem;
        }}

        .testimonial-quote {{ font-size: 1rem; font-style: italic; color: {text_primary}; line-height: 1.6; margin-bottom: 1rem; padding-{border_side}: 1rem; border-{border_side}: 3px solid {primary_color}; }}
        .testimonial-author {{ font-size: 0.875rem; font-weight: 600; color: {primary_color}; }}
        .testimonial-role {{ font-size: 0.8125rem; color: {text_secondary}; }}

        .partner-card {{ background: {bg_elevated}; border: 1px solid {border_light}; border-radius: var(--radius-lg); padding: 1.5rem; text-align: center; }}
        .partner-logo {{ font-size: 2.5rem; margin-bottom: 0.75rem; }}
        .partner-name {{ font-size: 0.875rem; font-weight: 500; color: {text_primary}; }}

        table {{ width: 100%; border-collapse: separate; border-spacing: 0; }}
        th {{ background: {primary_color} !important; font-size: 0.75rem !important; font-weight: 600 !important; text-transform: uppercase !important; color: white !important; padding: 0.75rem 1rem !important; text-align: {text_align} !important; }}
        td {{ background: {bg_elevated} !important; font-size: 0.875rem !important; color: {text_primary} !important; padding: 0.875rem 1rem !important; text-align: {text_align} !important; border-bottom: 1px solid {border_light} !important; }}
        tr:hover td {{ background: {primary_color}10 !important; }}

        hr {{ border: none !important; border-top: 1px solid {border_light} !important; margin: 1.5rem 0 !important; }}

        .footer {{ text-align: center; padding: 2rem 0; margin-top: 2rem; border-top: 2px solid {primary_color}; }}
        .footer-brand {{ font-size: 1rem; font-weight: 700; color: {primary_color}; }}
        .footer-partners {{ font-size: 0.8125rem; color: {text_secondary}; }}
        .footer-stats {{ display: inline-block; background: linear-gradient(135deg, {primary_color}15, {warning}15); border: 2px solid {primary_color}; border-radius: var(--radius-full); padding: 0.5rem 1.5rem; margin-top: 0.75rem; font-size: 0.875rem; font-weight: 600; color: {primary_color}; }}

        .comparison-header {{ background: linear-gradient(135deg, #DC2626 0%, #EF4444 100%); border-radius: var(--radius-xl); padding: 1.5rem 2rem; margin-bottom: 1.5rem; }}
        .comparison-header h2, .comparison-header p {{ color: white !important; text-align: center; }}

        .conclusion-box {{ background: {primary_color}10; border: 2px solid {primary_color}; border-radius: var(--radius-xl); padding: 1.25rem 1.5rem; text-align: center; }}
        .conclusion-box h3 {{ color: {primary_color} !important; font-size: 1rem !important; margin: 0 !important; }}

        /* BBC Strategic Partner Badge */
        .strategic-badge {{
            display: inline-block;
            background: linear-gradient(135deg, {primary_color}, {secondary_color});
            color: white;
            font-size: 0.75rem;
            font-weight: 700;
            padding: 0.5rem 1rem;
            border-radius: var(--radius-full);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            box-shadow: 0 4px 12px {primary_color}40;
        }}

        @media (max-width: 768px) {{
            .kpi-grid {{ grid-template-columns: 1fr; }}
            .hero-header::before {{ display: none; }}
        }}
    </style>
    """


# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="BBC School × IAFactory - Programme National IA",
    page_icon="🇩🇿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# SESSION STATE INIT
# ============================================
if "lang" not in st.session_state:
    st.session_state.lang = "fr"
if "theme" not in st.session_state:
    st.session_state.theme = "light"
if "current_response" not in st.session_state:
    st.session_state.current_response = None

# Use BBC config
CONFIG = BBC_CONFIG
T = Translator(st.session_state.lang)

# ============================================
# DATA
# ============================================
COMPETITORS = {
    "IAFactory": {"prix_ecole": 1.1, "color": "#006233"},
    "EduTech Pro": {"prix_ecole": 3.5, "color": "#EF4444"},
    "SmartEdu AI": {"prix_ecole": 4.2, "color": "#3B82F6"},
    "Microsoft EDU": {"prix_ecole": 5.0, "color": "#8B5CF6"}
}

PARTNERS = [
    {"name": "UNESCO", "logo": "🇺🇳"},
    {"name": "Ministère Éducation", "logo": "🇩🇿"},
    {"name": "Devrabic", "logo": "💻"},
    {"name": "HES-SO Suisse", "logo": "🇨🇭"}
]


def get_timeline_events(t: Translator) -> list:
    return [
        {"date": "Déc 2025", "event": "Sélection BBC School", "phase": "Préparation", "status": "done"},
        {"date": "Jan 2026", "event": "Formation enseignants BBC", "phase": "Formation", "status": "upcoming"},
        {"date": "3 Fév 2026", "event": "🚀 LANCEMENT OFFICIEL BBC", "phase": "Lancement", "status": "milestone"},
        {"date": "Fév-Juin 2026", "event": "Formation 1,600 élèves BBC", "phase": "Pilote", "status": "upcoming"},
        {"date": "28 Juin 2026", "event": "🏆 BBC School AI Summit", "phase": "Événement", "status": "milestone"},
        {"date": "Juil-Déc 2026", "event": "Démarchage 50 écoles privées", "phase": "Expansion", "status": "future"},
        {"date": "Jan 2027", "event": "Phase 2: 50 écoles", "phase": "Scale", "status": "future"},
        {"date": "Q3 2027", "event": "Pitch Ministère Éducation", "phase": "Stratégie", "status": "future"},
        {"date": "Jan 2028", "event": "🎰 Contrat National 500 écoles", "phase": "JACKPOT", "status": "milestone"}
    ]


def get_testimonials(t: Translator) -> list:
    return [
        {"quote": t.t("testimonials.quote1"), "author": t.t("testimonials.author1"), "role": t.t("testimonials.role1"), "program": t.t("testimonials.program1"), "icon": "🏆"},
        {"quote": t.t("testimonials.quote2"), "author": t.t("testimonials.author2"), "role": t.t("testimonials.role2"), "program": t.t("testimonials.program2"), "icon": "📈"},
        {"quote": t.t("testimonials.quote3"), "author": t.t("testimonials.author3"), "role": t.t("testimonials.role3"), "program": t.t("testimonials.program3"), "icon": "🎓"}
    ]


# ============================================
# MAIN APP
# ============================================
def main():
    T = Translator(st.session_state.lang)
    is_rtl = T.is_rtl()

    # Apply BBC-specific CSS
    st.markdown(get_bbc_css(st.session_state.theme, is_rtl), unsafe_allow_html=True)

    # ===== HEADER =====
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem 0;'>
            <p style='font-size: 0.875rem; font-weight: 500; color: #006233; margin: 0 0 0.5rem 0;'>
                البرنامج الوطني للذكاء الاصطناعي
            </p>
            <h1 style='font-size: 2rem; font-weight: 700; margin: 0; letter-spacing: -0.02em; color: #006233;'>
                🇩🇿 BBC School × IAFactory
            </h1>
            <p style='font-size: 0.9375rem; margin: 0.5rem 0 0 0;'>
                Partenariat Stratégique - Programme National IA
            </p>
            <div style='margin-top: 0.75rem;'>
                <span class='strategic-badge'>Partenaire Stratégique</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ===== SIDEBAR =====
    with st.sidebar:
        st.markdown("## 📊 KPIs BBC School")

        st.metric("ROI Potentiel", CONFIG["metrics"]["roi_range"], CONFIG["metrics"]["revenue_range"])
        st.metric("Coût BBC School", "0 DA", "100% offert par IAFactory")
        st.metric("Élèves Phase 1", f"{CONFIG['students']:,}", "BBC School")

        st.markdown("---")

        st.markdown("### 🎯 Statut Partenariat")
        st.markdown("""
        <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
            <p style='margin: 0; font-size: 0.875rem;'>
                <strong>Type:</strong> Stratégique<br>
                <strong>Investissement IAF:</strong> 4.8M DA<br>
                <strong>BBC paye:</strong> 0 DA
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Language selector
        st.markdown("### 🌐 Langue")
        lang_options = {"Français": "fr", "العربية": "ar", "English": "en"}
        current_lang_name = [k for k, v in lang_options.items() if v == st.session_state.lang][0]
        selected_lang = st.selectbox("Language", options=list(lang_options.keys()), index=list(lang_options.keys()).index(current_lang_name), label_visibility="collapsed")
        if lang_options[selected_lang] != st.session_state.lang:
            st.session_state.lang = lang_options[selected_lang]
            st.rerun()

        # Theme selector
        st.markdown("### 🎨 Thème")
        theme_options = {"Clair": "light", "Sombre": "dark"}
        current_theme_name = [k for k, v in theme_options.items() if v == st.session_state.theme][0]
        selected_theme = st.selectbox("Theme", options=list(theme_options.keys()), index=list(theme_options.keys()).index(current_theme_name), label_visibility="collapsed")
        if theme_options[selected_theme] != st.session_state.theme:
            st.session_state.theme = theme_options[selected_theme]
            st.rerun()

    # ===== MAIN TABS =====
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "🎯 Résumé",
        "💰 Budget BBC",
        "⚔️ Concurrence",
        "🚀 Stratégie",
        "📅 Timeline",
        "💬 Témoignages",
        "📊 Graphiques",
        "🤖 Assistant IA"
    ])

    # ============================================
    # TAB 1: RÉSUMÉ
    # ============================================
    with tab1:
        st.markdown("""
        <div class='hero-header'>
            <h2>🎯 Proposition de Valeur IAFactory</h2>
            <p>BBC School = Partenaire Stratégique | Investissement 100% IAFactory</p>
        </div>
        """, unsafe_allow_html=True)

        roi = CONFIG["roi"]["realistic"]

        st.markdown(f"""
        <div class='kpi-grid'>
            <div class='kpi-card green'>
                <div class='kpi-label'>1️⃣ BBC School</div>
                <div class='kpi-value green'>0 DA</div>
                <div class='kpi-desc'>Partenaire stratégique<br>100% offert par IAFactory</div>
            </div>
            <div class='kpi-card blue'>
                <div class='kpi-label'>2️⃣ 50 Écoles</div>
                <div class='kpi-value blue'>55M DA</div>
                <div class='kpi-desc'>Écoles privées<br>Profit direct</div>
            </div>
            <div class='kpi-card orange'>
                <div class='kpi-label'>3️⃣ Ministère</div>
                <div class='kpi-value orange'>500M DA</div>
                <div class='kpi-desc'>500 écoles publiques<br>JACKPOT 🎰</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🔘 Actions Rapides")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📋 Résumé Exécutif", use_container_width=True, type="primary"):
                st.session_state.current_response = "executive_summary"
        with col2:
            if st.button("🤖 Module L2 LLM", use_container_width=True):
                st.session_state.current_response = "module_l2"
        with col3:
            if st.button("📝 Quiz Éthique", use_container_width=True):
                st.session_state.current_response = "quiz"

        if st.session_state.current_response:
            st.markdown("---")
            with st.spinner("Chargement..."):
                time.sleep(0.3)
            st.markdown(T.t(f'responses.{st.session_state.current_response}', T.t('responses.executive_summary')))

    # ============================================
    # TAB 2: BUDGET BBC
    # ============================================
    with tab2:
        st.markdown("""
        <div class='hero-header'>
            <h2>💰 Coût BBC School = 0 DA</h2>
            <p>Partenaire stratégique - Investissement 100% IAFactory</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Coût BBC", "0 DA", "100% offert", delta_color="off")
        with col2: st.metric("Élèves", "1,600", "BBC School")
        with col3: st.metric("Invest. IAF", "4.8M DA", "stratégique")
        with col4: st.metric("ROI", "×47-×104", "250-555M DA")

        st.markdown("---")
        st.markdown("### ✅ Infrastructure EXISTANTE BBC (Coût = 0 DA)")

        col1, col2 = st.columns(2)
        with col1:
            st.success("**🖥️ IA Locale**: Ollama, LM Studio, Groq (gratuit)")
            st.success("**🏗️ Tech**: 40 PC, WiFi 500 Mbps, 2 serveurs")
        with col2:
            st.success("**☁️ IA Cloud**: DeepSeek, Qwen, Kimi (gratuit)")
            st.success("**👥 Personnel**: 20 enseignants, IT support")

        st.markdown("---")
        st.markdown("### 📊 Budget Détaillé")

        st.markdown("""
| Poste | IAFactory paye | BBC paye |
|:------|---------------:|----------:|
| Formation 20 enseignants | 500,000 DA | **0 DA** ✅ |
| 38 leçons + manuels | 2,000,000 DA | **0 DA** ✅ |
| Plateforme RAG | 1,500,000 DA | **0 DA** ✅ |
| Support 6 mois | 800,000 DA | **0 DA** ✅ |
| **TOTAL** | **4,800,000 DA** | **0 DA** |
        """)

    # ============================================
    # TAB 3-7: (Similar to generic but with BBC branding)
    # ============================================
    with tab3:
        st.markdown("""
        <div class='comparison-header'>
            <h2>⚔️ IAFactory vs Concurrents</h2>
            <p>3× moins cher avec PLUS de valeur!</p>
        </div>
        """, unsafe_allow_html=True)

        price_df = pd.DataFrame({"Fournisseur": list(COMPETITORS.keys()), "Prix (M DA)": [c["prix_ecole"] for c in COMPETITORS.values()]})
        fig = go.Figure(go.Bar(x=price_df["Prix (M DA)"], y=price_df["Fournisseur"], orientation='h', marker_color=[c["color"] for c in COMPETITORS.values()], text=price_df["Prix (M DA)"].apply(lambda x: f"{x}M DA"), textposition='outside'))
        fig.update_layout(height=280, margin=dict(l=0, r=40, t=20, b=20), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(family="Inter"))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.markdown("""
| Critère | IAFactory | EduTech Pro | SmartEdu AI | Microsoft |
|:------|:----------:|:------------:|:------------:|:----------:|
| **Prix/école** | **1.1M** ✅ | 3.5M | 4.2M | 5M |
| **IA utilisées** | **Gratuites** ✅ | Payant | Payant | Payant |
| **Formation** | **40h** ✅ | 8h | Payant | Non |
| **Support 1 an** | **Inclus** ✅ | Payant | Payant | Payant |
| **Contenu algérien** | **100%** ✅ | 0% | 0% | 30% |
| **Fonctionne offline** | ✅ **OUI** | ❌ | ❌ | ❌ |
        """)

        st.markdown("""
        <div class='conclusion-box'>
            <h3>🏆 CONCLUSION: IAFactory = 3× moins cher avec PLUS de valeur!</h3>
        </div>
        """, unsafe_allow_html=True)

    with tab4:
        st.markdown("""
        <div class='hero-header' style='background: linear-gradient(135deg, #006233 0%, #004d26 50%, #D52B1E 100%);'>
            <h2>🚀 Stratégie 3 Phases → JACKPOT</h2>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='phase-card phase-1'><h3>📍 PHASE 1: BBC School (Fév-Juin 2026)</h3></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown("**Actions:** 1,600 élèves, 38 leçons, 20 profs")
        with col2: st.metric("Investissement", "4.8M DA", "100% IAFactory")
        with col3: st.metric("Revenu", "0 DA", "Phase investissement", delta_color="off")

        st.markdown("---")
        st.markdown("<div class='phase-card phase-2'><h3>🎪 PHASE 2: 50 Écoles Privées (2027)</h3></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown("**Actions:** AI Summit BBC, démarchage, contrats")
        with col2: st.metric("Écoles", "50", "+49")
        with col3: st.metric("Revenu", "55M DA", "Profit!")

        st.markdown("---")
        st.markdown("<div class='phase-card phase-3'><h3>🏆 PHASE 3: Contrat Ministère (2028)</h3></div>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.markdown("**Actions:** Appel d'offres gagné!")
        with col2: st.metric("Écoles", "500", "+450")
        with col3: st.metric("Élèves", "50,000", "+45,000")
        with col4: st.metric("Revenu", "500M DA", "JACKPOT 🎰")

    with tab5:
        st.markdown("""
        <div class='hero-header' style='background: linear-gradient(135deg, #006233 0%, #10B981 100%);'>
            <h2>📅 Timeline de Déploiement BBC School</h2>
        </div>
        """, unsafe_allow_html=True)

        timeline_events = get_timeline_events(T)
        st.markdown("<div class='timeline-container'>", unsafe_allow_html=True)
        for event in timeline_events:
            st.markdown(f"""
            <div class='timeline-item {event["status"]}'>
                <div class='timeline-date'>{event['date']}</div>
                <div class='timeline-title'>{event['event']}</div>
                <span class='timeline-badge'>{event['phase']}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab6:
        st.markdown("""
        <div class='hero-header' style='background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);'>
            <h2>💬 Témoignages & Social Proof</h2>
        </div>
        """, unsafe_allow_html=True)

        testimonials = get_testimonials(T)
        for t_item in testimonials:
            st.markdown(f"""
            <div class='testimonial-card'>
                <div style='font-size: 2rem; margin-bottom: 1rem;'>{t_item['icon']}</div>
                <div class='testimonial-quote'>"{t_item['quote']}"</div>
                <div class='testimonial-author'>— {t_item['author']}</div>
                <div class='testimonial-role'>{t_item['role']} • {t_item['program']}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🤝 Partenaires Officiels")
        cols = st.columns(4)
        for i, p in enumerate(PARTNERS):
            with cols[i]:
                st.markdown(f"<div class='partner-card'><div class='partner-logo'>{p['logo']}</div><div class='partner-name'>{p['name']}</div></div>", unsafe_allow_html=True)

    with tab7:
        st.markdown("### 📈 Croissance Revenus IAFactory")

        revenue_df = pd.DataFrame({"Année": ["2026", "2027", "2028"], "Revenus": [0, 55, 500], "Profit": [-4.8, 49.7, 549.7]})
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(x=revenue_df["Année"], y=revenue_df["Revenus"], name="Revenus Annuels", marker_color="#006233", text=["0M", "55M", "500M"], textposition='outside'))
        fig1.add_trace(go.Scatter(x=revenue_df["Année"], y=revenue_df["Profit"], name="Profit Cumulé", line=dict(color="#F59E0B", width=3), mode='lines+markers'))
        fig1.update_layout(title="Projection Revenus 2026-2028", height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(family="Inter"))
        st.plotly_chart(fig1, use_container_width=True)

    # ============================================
    # TAB 8: ASSISTANT IA (ANYTHINGLLM)
    # ============================================
    with tab8:
        st.markdown("""
        <div class='hero-header'>
            <h2>🤖 Assistant IA - BBC School</h2>
            <p>Posez vos questions sur le programme en Francais, Arabe ou Anglais</p>
        </div>
        """, unsafe_allow_html=True)

        # Info cards
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class='metric-card'>
                <div class='metric-value' style='color: #006233'>🌍</div>
                <div class='metric-label'>Trilingue</div>
                <div class='metric-desc'>Francais, Arabe, Anglais</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class='metric-card'>
                <div class='metric-value' style='color: #006233'>⚡</div>
                <div class='metric-label'>Rapide</div>
                <div class='metric-desc'>Reponses en < 3 secondes</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class='metric-card'>
                <div class='metric-value' style='color: #006233'>🔒</div>
                <div class='metric-label'>Securise</div>
                <div class='metric-desc'>Donnees locales</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Chatbot access
        st.markdown("### 💬 Acceder au Chatbot")

        chatbot_col1, chatbot_col2 = st.columns([2, 1])

        with chatbot_col1:
            st.info("""
            **AnythingLLM** est notre assistant IA intelligent qui peut repondre a toutes vos questions sur:
            - Le partenariat BBC School × IAFactory
            - Les tarifs et le modele economique
            - Les specifications techniques
            - La strategie de deploiement
            """)

            # Button to open chatbot
            st.markdown("""
            <a href="http://localhost:3001" target="_blank" style="text-decoration: none;">
                <button style="
                    background: linear-gradient(135deg, #006233 0%, #004d26 100%);
                    color: white;
                    border: none;
                    padding: 1rem 2rem;
                    font-size: 1.1rem;
                    font-weight: 600;
                    border-radius: 12px;
                    cursor: pointer;
                    width: 100%;
                    margin: 1rem 0;
                    box-shadow: 0 4px 15px rgba(0, 98, 51, 0.3);
                ">
                    🚀 Ouvrir le Chatbot AnythingLLM
                </button>
            </a>
            """, unsafe_allow_html=True)

            # Alternative: Streamlit chatbot
            st.markdown("""
            <a href="http://localhost:8504" target="_blank" style="text-decoration: none;">
                <button style="
                    background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
                    color: white;
                    border: none;
                    padding: 0.75rem 1.5rem;
                    font-size: 1rem;
                    font-weight: 500;
                    border-radius: 8px;
                    cursor: pointer;
                    width: 100%;
                    box-shadow: 0 2px 10px rgba(59, 130, 246, 0.2);
                ">
                    💬 Chatbot Streamlit (Alternative)
                </button>
            </a>
            """, unsafe_allow_html=True)

        with chatbot_col2:
            st.markdown("### 📝 Questions Exemples")
            examples = [
                "Quel est le cout pour BBC School?",
                "Quel est le ROI sur 3 ans?",
                "Quelles technologies utilisez-vous?",
                "ما هو سعر كل طالب؟",
                "What is the investment cost?",
            ]
            for example in examples:
                st.code(example, language=None)

    # ===== FOOTER =====
    st.markdown("""
    <div class='footer'>
        <p class='footer-brand'>🇩🇿 BBC School × IAFactory - Partenariat Stratégique</p>
        <p class='footer-partners'>UNESCO • IAFactory Academy • Devrabic • HES-SO</p>
        <div class='footer-stats'>Investissement: 5.3M DA → Revenus: 555M DA → Profit: 550M DA (ROI ×104)</div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
