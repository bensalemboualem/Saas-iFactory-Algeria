"""
IAFactory-School - Démo Ministre (Version Générique)
Interface Streamlit Premium - Version ON par défaut pour prospects
"""

import streamlit as st
import time
from datetime import datetime
import json
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Import configuration
from config import get_active_config, get_config_by_name, list_versions, enable_version, calculate_pricing

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
# PREMIUM DESIGN SYSTEM
# ============================================
def get_premium_css(theme: str, is_rtl: bool = False, primary_color: str = "#3B82F6") -> str:
    """Generate premium CSS with dynamic primary color"""

    if theme == 'dark':
        bg_primary = '#09090B'
        bg_secondary = '#18181B'
        bg_tertiary = '#27272A'
        bg_elevated = '#1F1F23'
        bg_hover = '#2D2D33'
        text_primary = '#FAFAFA'
        text_secondary = '#A1A1AA'
        text_tertiary = '#71717A'
        accent_primary = '#60A5FA'
        accent_hover = '#3B82F6'
        accent_light = '#1E3A8A'
        success = '#34D399'
        success_bg = '#064E3B'
        success_text = '#A7F3D0'
        warning = '#FBBF24'
        warning_bg = '#78350F'
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
        accent_hover = primary_color
        accent_light = '#DBEAFE'
        success = '#10B981'
        success_bg = '#D1FAE5'
        success_text = '#065F46'
        warning = '#F59E0B'
        warning_bg = '#FEF3C7'
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
            --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
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
            background: {bg_secondary} !important;
            border-{opposite_side}: 1px solid {border_light} !important;
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
            background: {bg_elevated} !important;
            color: {text_primary} !important;
            box-shadow: 0 1px 3px {shadow_color} !important;
        }}

        .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {{ display: none !important; }}

        .stButton > button {{
            background: linear-gradient(180deg, {accent_primary} 0%, {accent_hover} 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: var(--radius-md) !important;
            padding: 0.625rem 1rem !important;
            font-weight: 500 !important;
        }}

        .stButton > button:hover {{
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px {accent_primary}40 !important;
        }}

        .hero-header {{
            background: linear-gradient(135deg, {accent_primary} 0%, #8B5CF6 100%);
            border-radius: var(--radius-xl);
            padding: 2rem;
            margin-bottom: 1.5rem;
            position: relative;
            overflow: hidden;
        }}

        .hero-header h2 {{ color: white !important; text-align: center; position: relative; }}
        .hero-header p {{ color: rgba(255,255,255,0.8) !important; text-align: center; position: relative; }}

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
            border-color: {border_medium};
            box-shadow: 0 8px 24px {shadow_color};
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

        .kpi-card.green::before {{ background: linear-gradient(90deg, #10B981, #34D399); }}
        .kpi-card.blue::before {{ background: linear-gradient(90deg, #3B82F6, #60A5FA); }}
        .kpi-card.orange::before {{ background: linear-gradient(90deg, #F59E0B, #FBBF24); }}

        .kpi-label {{ font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: {text_tertiary}; margin-bottom: 0.5rem; }}
        .kpi-value {{ font-size: 2rem; font-weight: 700; color: {text_primary}; letter-spacing: -0.02em; }}
        .kpi-value.green {{ color: {success}; }}
        .kpi-value.blue {{ color: {accent_primary}; }}
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

        .phase-card.phase-1 {{ border-{border_side}-color: {success}; }}
        .phase-card.phase-2 {{ border-{border_side}-color: {accent_primary}; }}
        .phase-card.phase-3 {{ border-{border_side}-color: {warning}; }}

        .timeline-container {{ position: relative; padding-{border_side}: 2rem; }}
        .timeline-container::before {{
            content: '';
            position: absolute;
            {border_side}: 0.75rem;
            top: 0;
            bottom: 0;
            width: 2px;
            background: linear-gradient(180deg, {accent_primary}, {success});
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
            border: 2px solid {accent_primary};
            border-radius: 50%;
        }}

        .timeline-item.milestone::before {{ background: {warning}; border-color: {warning}; }}
        .timeline-item.done::before {{ background: {success}; border-color: {success}; }}

        .timeline-date {{ font-size: 0.75rem; font-weight: 600; color: {accent_primary}; text-transform: uppercase; }}
        .timeline-title {{ font-size: 0.9375rem; font-weight: 500; color: {text_primary}; margin: 0.25rem 0; }}
        .timeline-badge {{ display: inline-block; font-size: 0.6875rem; font-weight: 600; text-transform: uppercase; padding: 0.25rem 0.625rem; border-radius: var(--radius-full); background: {accent_light}; color: {accent_primary}; }}

        .testimonial-card {{
            background: {bg_elevated};
            border: 1px solid {border_light};
            border-radius: var(--radius-xl);
            padding: 1.5rem;
            margin-bottom: 1rem;
        }}

        .testimonial-quote {{ font-size: 1rem; font-style: italic; color: {text_primary}; line-height: 1.6; margin-bottom: 1rem; padding-{border_side}: 1rem; border-{border_side}: 3px solid {accent_primary}; }}
        .testimonial-author {{ font-size: 0.875rem; font-weight: 600; color: {text_primary}; }}
        .testimonial-role {{ font-size: 0.8125rem; color: {text_secondary}; }}

        .partner-card {{ background: {bg_elevated}; border: 1px solid {border_light}; border-radius: var(--radius-lg); padding: 1.5rem; text-align: center; }}
        .partner-logo {{ font-size: 2.5rem; margin-bottom: 0.75rem; }}
        .partner-name {{ font-size: 0.875rem; font-weight: 500; color: {text_primary}; }}

        table {{ width: 100%; border-collapse: separate; border-spacing: 0; }}
        th {{ background: {bg_tertiary} !important; font-size: 0.75rem !important; font-weight: 600 !important; text-transform: uppercase !important; color: {text_tertiary} !important; padding: 0.75rem 1rem !important; text-align: {text_align} !important; }}
        td {{ background: {bg_elevated} !important; font-size: 0.875rem !important; color: {text_primary} !important; padding: 0.875rem 1rem !important; text-align: {text_align} !important; border-bottom: 1px solid {border_light} !important; }}
        tr:hover td {{ background: {bg_hover} !important; }}

        hr {{ border: none !important; border-top: 1px solid {border_light} !important; margin: 1.5rem 0 !important; }}

        .footer {{ text-align: center; padding: 2rem 0; margin-top: 2rem; border-top: 1px solid {border_light}; }}
        .footer-brand {{ font-size: 0.875rem; font-weight: 600; color: {text_primary}; }}
        .footer-partners {{ font-size: 0.8125rem; color: {text_secondary}; }}
        .footer-stats {{ display: inline-block; background: linear-gradient(135deg, {accent_primary}15, #8B5CF615); border: 1px solid {accent_primary}30; border-radius: var(--radius-full); padding: 0.5rem 1rem; margin-top: 0.75rem; font-size: 0.8125rem; font-weight: 500; color: {accent_primary}; }}

        .comparison-header {{ background: linear-gradient(135deg, #DC2626 0%, #EF4444 100%); border-radius: var(--radius-xl); padding: 1.5rem 2rem; margin-bottom: 1.5rem; }}
        .comparison-header h2, .comparison-header p {{ color: white !important; text-align: center; }}

        .conclusion-box {{ background: {success_bg}; border: 2px solid {success}; border-radius: var(--radius-xl); padding: 1.25rem 1.5rem; text-align: center; }}
        .conclusion-box h3 {{ color: {'#065F46' if theme == 'light' else success} !important; font-size: 1rem !important; margin: 0 !important; }}

        .demo-config {{ background: {bg_tertiary}; border: 1px solid {border_light}; border-radius: var(--radius-lg); padding: 1rem; margin-bottom: 1rem; }}
        .demo-badge {{ display: inline-block; background: {warning}; color: #000; font-size: 0.6875rem; font-weight: 700; padding: 0.25rem 0.5rem; border-radius: var(--radius-sm); text-transform: uppercase; }}

        @media (max-width: 768px) {{
            .kpi-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
    """


# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Programme National IA - IAFactory",
    page_icon="🎓",
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
if "demo_students" not in st.session_state:
    st.session_state.demo_students = 1600

# Load configuration
CONFIG = get_active_config()
T = Translator(st.session_state.lang)

# ============================================
# DATA
# ============================================
COMPETITORS = {
    "IAFactory": {"prix_ecole": 1.1, "color": "#10B981"},
    "EduTech Pro": {"prix_ecole": 3.5, "color": "#EF4444"},
    "SmartEdu AI": {"prix_ecole": 4.2, "color": "#3B82F6"},
    "Microsoft EDU": {"prix_ecole": 5.0, "color": "#8B5CF6"}
}

PARTNERS = [
    {"name": "UNESCO", "logo": "🇺🇳"},
    {"name": "Ministère", "logo": "🇩🇿"},
    {"name": "Devrabic", "logo": "💻"},
    {"name": "HES-SO", "logo": "🇨🇭"}
]


def get_timeline_events(t: Translator, config: dict) -> list:
    launch_date = config.get("launch_date", "2026-02-03")
    return [
        {"date": t.t("timeline.dec_2025"), "event": f"Sélection {config['display_name']}", "phase": t.t("timeline.phase_prep"), "status": "done"},
        {"date": t.t("timeline.jan_2026"), "event": t.t("timeline.event_training"), "phase": t.t("timeline.phase_training"), "status": "upcoming"},
        {"date": t.t("timeline.feb_2026"), "event": t.t("timeline.event_launch"), "phase": t.t("timeline.phase_launch"), "status": "milestone"},
        {"date": t.t("timeline.feb_jun_2026"), "event": f"Formation {config['students']:,} élèves", "phase": t.t("timeline.phase_pilot"), "status": "upcoming"},
        {"date": t.t("timeline.jun_2026"), "event": f"{config['display_name']} AI Summit", "phase": t.t("timeline.phase_event"), "status": "milestone"},
        {"date": t.t("timeline.jul_dec_2026"), "event": t.t("timeline.event_expansion"), "phase": t.t("timeline.phase_expansion"), "status": "future"},
        {"date": t.t("timeline.jan_2027"), "event": t.t("timeline.event_phase2"), "phase": t.t("timeline.phase_scale"), "status": "future"},
        {"date": t.t("timeline.q3_2027"), "event": t.t("timeline.event_pitch"), "phase": t.t("timeline.phase_strategy"), "status": "future"},
        {"date": t.t("timeline.jan_2028"), "event": t.t("timeline.event_contract"), "phase": t.t("timeline.phase_jackpot"), "status": "milestone"}
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
    global CONFIG

    T = Translator(st.session_state.lang)
    is_rtl = T.is_rtl()

    # Recalculate config if demo mode with custom students
    if CONFIG.get("demo_mode") and st.session_state.demo_students != CONFIG["students"]:
        CONFIG["students"] = st.session_state.demo_students
        CONFIG["pricing"] = calculate_pricing(st.session_state.demo_students)
        from config import calculate_iafactory_investment, calculate_roi
        CONFIG["investment"] = calculate_iafactory_investment(st.session_state.demo_students)
        CONFIG["roi"] = calculate_roi(st.session_state.demo_students)

    # Apply premium CSS
    st.markdown(get_premium_css(st.session_state.theme, is_rtl, CONFIG.get("primary_color", "#3B82F6")), unsafe_allow_html=True)

    # ===== HEADER =====
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem 0;'>
            <p style='font-size: 0.875rem; font-weight: 500; color: {CONFIG.get("primary_color", "#3B82F6")}; margin: 0 0 0.5rem 0;'>
                {CONFIG.get('display_name_ar', 'البرنامج الوطني للذكاء الاصطناعي') if is_rtl else 'PROGRAMME NATIONAL IA'}
            </p>
            <h1 style='font-size: 2rem; font-weight: 700; margin: 0; letter-spacing: -0.02em;'>
                {CONFIG.get("logo_emoji", "🎓")} {CONFIG.get("display_name", "IAFactory-School")}
            </h1>
            <p style='font-size: 0.9375rem; margin: 0.5rem 0 0 0;'>
                {CONFIG.get("tagline", T.t('app.subtitle'))}
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ===== SIDEBAR =====
    with st.sidebar:
        st.markdown(f"## {T.t('sidebar.title')}")

        # Dynamic metrics from config
        st.metric(T.t('sidebar.roi_label'), CONFIG["metrics"]["roi_range"], CONFIG["metrics"]["revenue_range"])
        st.metric(T.t('sidebar.cost_label'), CONFIG["metrics"]["cost_for_school"], "Pour l'école" if CONFIG.get("partner_type") != "strategic" else "100% offert")
        st.metric(T.t('sidebar.students_label'), f"{CONFIG['students']:,}", CONFIG["display_name"])

        st.markdown("---")

        # Demo mode configuration
        if CONFIG.get("demo_mode"):
            st.markdown("### ⚙️ Configuration Démo")
            st.markdown("<span class='demo-badge'>Mode Démo</span>", unsafe_allow_html=True)

            new_students = st.slider(
                "Nombre d'élèves",
                min_value=100,
                max_value=5000,
                value=st.session_state.demo_students,
                step=100,
                help="Ajustez pour voir les calculs dynamiques"
            )
            if new_students != st.session_state.demo_students:
                st.session_state.demo_students = new_students
                st.rerun()

            # Show calculated values
            st.markdown(f"""
            <div class='demo-config'>
                <p style='margin: 0; font-size: 0.8125rem;'>
                    <strong>Prix/élève:</strong> {CONFIG['pricing']['price_per_student_month']} DA/mois<br>
                    <strong>Tier:</strong> {CONFIG['pricing']['tier_label']}<br>
                    <strong>Invest. IAF:</strong> {CONFIG['investment']['total_millions']}M DA
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")

        # Language selector
        st.markdown(f"### {T.t('sidebar.language')}")
        lang_options = {"Français": "fr", "العربية": "ar", "English": "en"}
        current_lang_name = [k for k, v in lang_options.items() if v == st.session_state.lang][0]
        selected_lang = st.selectbox("Language", options=list(lang_options.keys()), index=list(lang_options.keys()).index(current_lang_name), label_visibility="collapsed")
        if lang_options[selected_lang] != st.session_state.lang:
            st.session_state.lang = lang_options[selected_lang]
            st.rerun()

        # Theme selector
        st.markdown(f"### {T.t('sidebar.theme')}")
        theme_options = {T.t('sidebar.light'): "light", T.t('sidebar.dark'): "dark"}
        current_theme_name = [k for k, v in theme_options.items() if v == st.session_state.theme][0]
        selected_theme = st.selectbox("Theme", options=list(theme_options.keys()), index=list(theme_options.keys()).index(current_theme_name), label_visibility="collapsed")
        if theme_options[selected_theme] != st.session_state.theme:
            st.session_state.theme = theme_options[selected_theme]
            st.rerun()

    # ===== MAIN TABS =====
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        f"🎯 {T.t('tabs.summary')}",
        f"💰 {T.t('tabs.budget')}",
        f"⚔️ {T.t('tabs.competition')}",
        f"🚀 {T.t('tabs.strategy')}",
        f"📅 {T.t('tabs.timeline')}",
        f"💬 {T.t('tabs.testimonials')}",
        f"📊 {T.t('tabs.charts')}",
        f"🤖 Assistant IA"
    ])

    # ============================================
    # TAB 1: RÉSUMÉ
    # ============================================
    with tab1:
        st.markdown(f"""
        <div class='hero-header'>
            <h2>🎯 {T.t('summary.title')}</h2>
        </div>
        """, unsafe_allow_html=True)

        # Dynamic KPI Cards based on config
        roi_data = CONFIG["roi"]
        phase2_revenue = roi_data["realistic"]["phase2"]["revenue"] / 1_000_000
        phase3_revenue = roi_data["realistic"]["phase3"]["revenue"] / 1_000_000

        st.markdown(f"""
        <div class='kpi-grid'>
            <div class='kpi-card green'>
                <div class='kpi-label'>1️⃣ {CONFIG['display_name']}</div>
                <div class='kpi-value green'>{CONFIG['metrics']['cost_for_school']}</div>
                <div class='kpi-desc'>{'Partenaire stratégique' if CONFIG.get('partner_type') == 'strategic' else 'Preuve de concept'}<br>{CONFIG['students']:,} élèves</div>
            </div>
            <div class='kpi-card blue'>
                <div class='kpi-label'>2️⃣ {roi_data['realistic']['phase2']['schools']} Écoles</div>
                <div class='kpi-value blue'>{phase2_revenue:.0f}M DA</div>
                <div class='kpi-desc'>Écoles privées<br>Profit direct</div>
            </div>
            <div class='kpi-card orange'>
                <div class='kpi-label'>3️⃣ Ministère</div>
                <div class='kpi-value orange'>{phase3_revenue:.0f}M DA</div>
                <div class='kpi-desc'>{roi_data['realistic']['phase3']['schools']} écoles publiques<br>JACKPOT 🎰</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(f"### {T.t('summary.quick_actions')}")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(f"📋 {T.t('summary.executive_summary')}", use_container_width=True, type="primary"):
                st.session_state.current_response = "executive_summary"
        with col2:
            if st.button(f"🤖 {T.t('summary.module_l2')}", use_container_width=True):
                st.session_state.current_response = "module_l2"
        with col3:
            if st.button(f"📝 {T.t('summary.ethics_quiz')}", use_container_width=True):
                st.session_state.current_response = "quiz"

        if st.session_state.current_response:
            st.markdown("---")
            with st.spinner(T.t('common.loading')):
                time.sleep(0.3)
            st.markdown(T.t(f'responses.{st.session_state.current_response}', T.t('responses.executive_summary')))

    # ============================================
    # TAB 2: BUDGET
    # ============================================
    with tab2:
        cost_display = CONFIG['metrics']['cost_for_school']
        st.markdown(f"""
        <div class='hero-header'>
            <h2>💰 Coût {CONFIG['display_name']} = {cost_display}</h2>
            <p>{'Partenaire stratégique, pas client' if CONFIG.get('partner_type') == 'strategic' else 'Investissement partagé'}</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Coût École", cost_display, "100% offert" if CONFIG.get('partner_type') == 'strategic' else CONFIG['pricing']['tier_label'], delta_color="off")
        with col2: st.metric("Élèves", f"{CONFIG['students']:,}", CONFIG['display_name'])
        with col3: st.metric("Invest. IAF", f"{CONFIG['investment']['total_millions']}M DA", "stratégique")
        with col4: st.metric("ROI", CONFIG['metrics']['roi_range'], CONFIG['metrics']['revenue_range'])

        st.markdown("---")
        st.markdown(f"### ✅ {T.t('budget.infrastructure_title')}")

        col1, col2 = st.columns(2)
        with col1:
            st.success(f"**🖥️ {T.t('budget.ia_local')}**: {T.t('budget.ia_local_desc')}")
            st.success(f"**🏗️ {T.t('budget.tech')}**: {T.t('budget.tech_desc')}")
        with col2:
            st.success(f"**☁️ {T.t('budget.ia_cloud')}**: {T.t('budget.ia_cloud_desc')}")
            st.success(f"**👥 {T.t('budget.personnel')}**: {CONFIG['teachers']} enseignants, IT support")

        st.markdown("---")
        st.markdown(f"### 📊 {T.t('budget.budget_detail')}")

        inv = CONFIG['investment']
        st.markdown(f"""
| {T.t('budget.item')} | {T.t('budget.iaf_pays')} | {CONFIG['display_name']} paye |
|:------|---------------:|----------:|
| {T.t('budget.training')} ({CONFIG['students']} élèves) | {inv['formation']:,} DA | **0 DA** ✅ |
| {T.t('budget.content')} | {inv['content']:,} DA | **0 DA** ✅ |
| {T.t('budget.platform')} | {inv['platform']:,} DA | **0 DA** ✅ |
| {T.t('budget.support')} | {inv['support']:,} DA | **0 DA** ✅ |
| **{T.t('budget.total')}** | **{inv['total']:,} DA** | **0 DA** |
        """)

    # ============================================
    # TAB 3: CONCURRENCE
    # ============================================
    with tab3:
        st.markdown(f"""
        <div class='comparison-header'>
            <h2>⚔️ {T.t('competition.title')}</h2>
            <p>{T.t('competition.subtitle')}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"### 💰 {T.t('competition.price_comparison')}")

        price_df = pd.DataFrame({
            "Fournisseur": list(COMPETITORS.keys()),
            "Prix (M DA)": [c["prix_ecole"] for c in COMPETITORS.values()]
        })

        fig = go.Figure(go.Bar(
            x=price_df["Prix (M DA)"],
            y=price_df["Fournisseur"],
            orientation='h',
            marker_color=[c["color"] for c in COMPETITORS.values()],
            text=price_df["Prix (M DA)"].apply(lambda x: f"{x}M DA"),
            textposition='outside'
        ))
        fig.update_layout(height=280, margin=dict(l=0, r=40, t=20, b=20), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(family="Inter"))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.markdown(f"### 📊 {T.t('competition.detailed_comparison')}")

        st.markdown(f"""
| {T.t('competition.criteria')} | IAFactory | EduTech Pro | SmartEdu AI | Microsoft |
|:------|:----------:|:------------:|:------------:|:----------:|
| **{T.t('competition.price_school')}** | **1.1M** ✅ | 3.5M | 4.2M | 5M |
| **{T.t('competition.ai_used')}** | **{T.t('competition.free')}** ✅ | Payant | Payant | Payant |
| **{T.t('competition.training')}** | **40h** ✅ | 8h | Payant | Non |
| **{T.t('competition.support')}** | **{T.t('competition.included')}** ✅ | Payant | Payant | Payant |
| **{T.t('competition.algerian_content')}** | **100%** ✅ | 0% | 0% | 30% |
| **{T.t('competition.offline')}** | ✅ **{T.t('competition.yes')}** | ❌ | ❌ | ❌ |
        """)

        st.markdown(f"""
        <div class='conclusion-box'>
            <h3>🏆 {T.t('competition.conclusion')}</h3>
        </div>
        """, unsafe_allow_html=True)

    # ============================================
    # TAB 4: STRATÉGIE
    # ============================================
    with tab4:
        st.markdown(f"""
        <div class='hero-header' style='background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);'>
            <h2>🚀 {T.t('strategy.title')}</h2>
        </div>
        """, unsafe_allow_html=True)

        roi = CONFIG["roi"]["realistic"]

        # Phase 1
        st.markdown(f"""
        <div class='phase-card phase-1'>
            <h3>📍 PHASE 1: {CONFIG['display_name']} (Fév-Juin 2026)</h3>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f"**Actions:** {CONFIG['students']:,} élèves, 38 leçons, {CONFIG['teachers']} profs")
        with col2: st.metric("Investissement", f"{CONFIG['investment']['total_millions']}M DA", "offert" if CONFIG.get('partner_type') == 'strategic' else "partagé")
        with col3: st.metric("Revenu", "0 DA", "Phase investissement", delta_color="off")

        st.markdown("---")

        # Phase 2
        st.markdown(f"""
        <div class='phase-card phase-2'>
            <h3>🎪 PHASE 2: {roi['phase2']['schools']} Écoles Privées (2027)</h3>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown("**Actions:** AI Summit, démarchage, contrats")
        with col2: st.metric("Écoles", str(roi['phase2']['schools']), f"+{roi['phase2']['schools']-1}")
        with col3: st.metric("Revenu", f"{roi['phase2']['revenue']/1_000_000:.0f}M DA", "Profit!")

        st.markdown("---")

        # Phase 3
        st.markdown(f"""
        <div class='phase-card phase-3'>
            <h3>🏆 PHASE 3: Contrat Ministère (2028)</h3>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.markdown("**Actions:** Appel d'offres gagné!")
        with col2: st.metric("Écoles", str(roi['phase3']['schools']), f"+{roi['phase3']['schools']-roi['phase2']['schools']}")
        with col3: st.metric("Élèves", "50,000", "+45,000")
        with col4: st.metric("Revenu", f"{roi['phase3']['revenue']/1_000_000:.0f}M DA", "JACKPOT 🎰")

        st.markdown("---")
        st.markdown(f"### 📈 {T.t('strategy.roi_summary')}")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
| Phase | Investissement | Revenu |
|:------|---------------:|----------:|
| Phase 1 | {CONFIG['investment']['total_millions']}M DA | 0 DA |
| Phase 2 | 0.5M DA | {roi['phase2']['revenue']/1_000_000:.0f}M DA |
| Phase 3 | Variable | {roi['phase3']['revenue']/1_000_000:.0f}M DA |
| **TOTAL** | **{CONFIG['investment']['total_millions']+0.5}M DA** | **{roi['total_revenue_millions']}M DA** |
            """)
        with col2:
            st.markdown(f"""
| Scénario | Revenu | ROI |
|:----------|--------:|------:|
| 🔴 Pessimiste | {CONFIG['roi']['pessimistic']['total_revenue_millions']}M DA | **×{CONFIG['roi']['pessimistic']['roi_multiplier']}** |
| 🟡 Réaliste | {CONFIG['roi']['realistic']['total_revenue_millions']}M DA | **×{CONFIG['roi']['realistic']['roi_multiplier']}** |
| 🟢 Optimiste | {CONFIG['roi']['optimistic']['total_revenue_millions']}M DA | **×{CONFIG['roi']['optimistic']['roi_multiplier']}** |
            """)

    # ============================================
    # TAB 5: TIMELINE
    # ============================================
    with tab5:
        st.markdown(f"""
        <div class='hero-header' style='background: linear-gradient(135deg, #059669 0%, #10B981 100%);'>
            <h2>📅 {T.t('timeline.title')}</h2>
        </div>
        """, unsafe_allow_html=True)

        timeline_events = get_timeline_events(T, CONFIG)

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

    # ============================================
    # TAB 6: TÉMOIGNAGES
    # ============================================
    with tab6:
        st.markdown(f"""
        <div class='hero-header' style='background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);'>
            <h2>💬 {T.t('testimonials.title')}</h2>
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
        st.markdown(f"### 🤝 {T.t('testimonials.partners_title')}")

        cols = st.columns(4)
        for i, p in enumerate(PARTNERS):
            with cols[i]:
                st.markdown(f"""
                <div class='partner-card'>
                    <div class='partner-logo'>{p['logo']}</div>
                    <div class='partner-name'>{p['name']}</div>
                </div>
                """, unsafe_allow_html=True)

    # ============================================
    # TAB 7: GRAPHIQUES
    # ============================================
    with tab7:
        st.markdown(f"### 📈 {T.t('charts.revenue_title')}")

        roi = CONFIG["roi"]["realistic"]
        revenue_df = pd.DataFrame({
            "Année": ["2026", "2027", "2028"],
            "Revenus": [0, roi['phase2']['revenue']/1_000_000, roi['phase3']['revenue']/1_000_000],
            "Profit": [
                -CONFIG['investment']['total_millions'],
                -CONFIG['investment']['total_millions'] - 0.5 + roi['phase2']['revenue']/1_000_000,
                roi['total_revenue_millions'] - CONFIG['investment']['total_millions'] - 0.5
            ]
        })

        fig1 = go.Figure()
        fig1.add_trace(go.Bar(x=revenue_df["Année"], y=revenue_df["Revenus"], name=T.t('charts.revenue_annual'), marker_color="#10B981", text=revenue_df["Revenus"].apply(lambda x: f"{x:.0f}M"), textposition='outside'))
        fig1.add_trace(go.Scatter(x=revenue_df["Année"], y=revenue_df["Profit"], name=T.t('charts.profit_cumulative'), line=dict(color="#F59E0B", width=3), mode='lines+markers+text', text=revenue_df["Profit"].apply(lambda x: f"{x:.1f}M"), textposition='top center'))
        fig1.update_layout(title=T.t('charts.projection_title'), height=400, yaxis_title=T.t('charts.amount'), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(family="Inter"), legend=dict(orientation="h", yanchor="bottom", y=1.02))
        st.plotly_chart(fig1, use_container_width=True)

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"### 💰 {T.t('charts.price_comparison')}")
            fig2 = go.Figure(go.Bar(x=[1.1, 3.5, 4.2, 5.0], y=["IAFactory", "EduTech", "SmartEdu", "Microsoft"], orientation='h', marker_color=["#10B981", "#EF4444", "#3B82F6", "#8B5CF6"], text=["1.1M", "3.5M", "4.2M", "5M"], textposition='outside'))
            fig2.update_layout(height=280, xaxis_title=T.t('charts.price_school'), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(family="Inter"), margin=dict(l=0, r=40, t=20, b=40))
            st.plotly_chart(fig2, use_container_width=True)

        with col2:
            st.markdown(f"### 🎯 {T.t('charts.investment_breakdown')}")
            inv = CONFIG['investment']
            fig3 = go.Figure(go.Pie(labels=["Formation", "Contenu", "Plateforme", "Support"], values=[inv['formation'], inv['content'], inv['platform'], inv['support']], hole=0.4, marker_colors=["#10B981", "#3B82F6", "#F59E0B", "#8B5CF6"]))
            fig3.update_layout(height=280, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(family="Inter"), legend=dict(orientation="h", yanchor="bottom", y=-0.2))
            st.plotly_chart(fig3, use_container_width=True)

        st.markdown("---")
        st.markdown(f"### 🗺️ {T.t('charts.national_impact')}")

        roi = CONFIG["roi"]["realistic"]
        expansion_df = pd.DataFrame({
            "Phase": ["2026", "2027", "2028"],
            "Écoles": [1, roi['phase2']['schools'], roi['phase3']['schools']],
            "Élèves": [CONFIG['students'], roi['phase2']['schools']*100, 50000]
        })

        fig4 = go.Figure()
        fig4.add_trace(go.Bar(x=expansion_df["Phase"], y=expansion_df["Écoles"], name=T.t('charts.schools_count'), marker_color="#3B82F6"))
        fig4.add_trace(go.Scatter(x=expansion_df["Phase"], y=expansion_df["Élèves"], name=T.t('charts.students_count'), line=dict(color="#F59E0B", width=3), mode='lines+markers', yaxis='y2'))
        fig4.update_layout(title=T.t('charts.expansion_title'), yaxis=dict(title=T.t('charts.schools_count'), side='left'), yaxis2=dict(title=T.t('charts.students_count'), overlaying='y', side='right'), height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(family="Inter"), legend=dict(orientation="h", yanchor="bottom", y=1.02))
        st.plotly_chart(fig4, use_container_width=True)

    # ============================================
    # TAB 8: ASSISTANT IA (ANYTHINGLLM)
    # ============================================
    with tab8:
        st.markdown("""
        <div class='hero-header'>
            <h2>🤖 Assistant IA - IAFactory-School</h2>
            <p>Posez vos questions sur le programme en Francais, Arabe ou Anglais</p>
        </div>
        """, unsafe_allow_html=True)

        # Info cards
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class='metric-card'>
                <div class='metric-value' style='color: #10B981'>🌍</div>
                <div class='metric-label'>Trilingue</div>
                <div class='metric-desc'>Francais, Arabe, Anglais</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class='metric-card'>
                <div class='metric-value' style='color: #3B82F6'>⚡</div>
                <div class='metric-label'>Rapide</div>
                <div class='metric-desc'>Reponses en < 3 secondes</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class='metric-card'>
                <div class='metric-value' style='color: #8B5CF6'>🔒</div>
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
            - Le programme IAFactory-School
            - Les tarifs et le modele economique
            - Les specifications techniques
            - La strategie de deploiement
            """)

            # Button to open chatbot
            st.markdown("""
            <a href="http://localhost:3001" target="_blank" style="text-decoration: none;">
                <button style="
                    background: linear-gradient(135deg, #10B981 0%, #059669 100%);
                    color: white;
                    border: none;
                    padding: 1rem 2rem;
                    font-size: 1.1rem;
                    font-weight: 600;
                    border-radius: 12px;
                    cursor: pointer;
                    width: 100%;
                    margin: 1rem 0;
                    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
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
                "Quel est le prix par eleve?",
                "Quel est le ROI sur 3 ans?",
                "Quelles technologies utilisez-vous?",
                "ما هو سعر كل طالب؟",
                "What is the investment cost?",
            ]
            for example in examples:
                st.code(example, language=None)

        st.markdown("---")

        # Iframe integration (optional)
        st.markdown("### 🖥️ Chat Integre")
        show_iframe = st.checkbox("Afficher le chat integre (requiert AnythingLLM actif)", value=False)

        if show_iframe:
            st.markdown("""
            <iframe
                src="http://localhost:3001"
                width="100%"
                height="600"
                style="border: 1px solid #e5e7eb; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);"
            ></iframe>
            """, unsafe_allow_html=True)
        else:
            st.warning("Cochez la case ci-dessus pour afficher le chat integre. Assurez-vous que AnythingLLM est lance.")

    # ===== FOOTER =====
    st.markdown(f"""
    <div class='footer'>
        <p class='footer-brand'>{CONFIG.get('logo_emoji', '🎓')} {CONFIG.get('display_name', 'IAFactory-School')} × IAFactory</p>
        <p class='footer-partners'>{T.t('app.partners')}</p>
        <div class='footer-stats'>Investissement: {CONFIG['investment']['total_millions']}M DA → Revenus: {CONFIG['roi']['realistic']['total_revenue_millions']}M DA → ROI {CONFIG['metrics']['roi_range']}</div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
