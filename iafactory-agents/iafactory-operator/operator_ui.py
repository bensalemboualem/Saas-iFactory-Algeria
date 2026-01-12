"""
IAFactory Operator - Interface Streamlit
Agent central pour orchestration des agents
"""
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TRANSLATIONS = {
    "fr": {
        "title": "IAFactory Operator",
        "subtitle": "Orchestration & Monitoring des Agents",
        "welcome": "Bienvenue dans l'opérateur central IAFactory. Gérez et orchestrez tous vos agents IA.",
        "input_placeholder": "Commande ou question...",
        "dashboard": "Dashboard",
        "agents": "Agents",
        "tasks": "Tâches",
        "logs": "Logs",
        "settings": "Paramètres",
        "new_session": "Nouvelle session",
        "processing": "Exécution...",
        "active_agents": "Agents actifs",
        "pending_tasks": "Tâches en attente",
        "completed": "Complétées",
        "errors": "Erreurs"
    },
    "en": {
        "title": "IAFactory Operator",
        "subtitle": "Agent Orchestration & Monitoring",
        "welcome": "Welcome to IAFactory central operator. Manage and orchestrate all your AI agents.",
        "input_placeholder": "Command or question...",
        "dashboard": "Dashboard",
        "agents": "Agents",
        "tasks": "Tasks",
        "logs": "Logs",
        "settings": "Settings",
        "new_session": "New session",
        "processing": "Executing...",
        "active_agents": "Active agents",
        "pending_tasks": "Pending tasks",
        "completed": "Completed",
        "errors": "Errors"
    },
    "ar": {
        "title": "مشغل IAFactory",
        "subtitle": "تنسيق ومراقبة الوكلاء",
        "welcome": "مرحبًا في المشغل المركزي لـ IAFactory. إدارة وتنسيق جميع وكلاء الذكاء الاصطناعي.",
        "input_placeholder": "أمر أو سؤال...",
        "dashboard": "لوحة القيادة",
        "agents": "الوكلاء",
        "tasks": "المهام",
        "logs": "السجلات",
        "settings": "الإعدادات",
        "new_session": "جلسة جديدة",
        "processing": "جاري التنفيذ...",
        "active_agents": "الوكلاء النشطون",
        "pending_tasks": "المهام المعلقة",
        "completed": "مكتملة",
        "errors": "أخطاء"
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
        .metric-card { background: rgba(0,166,81,0.1); padding: 1.5rem; border-radius: 12px;
            border: 1px solid rgba(0,166,81,0.2); text-align: center; }
        .metric-value { font-size: 2.5rem; font-weight: 700; color: #00a651; }
        .metric-label { font-size: 0.9rem; color: #666; margin-top: 0.5rem; }
        .agent-status { display: flex; align-items: center; gap: 8px; padding: 8px 0; }
        .status-dot { width: 10px; height: 10px; border-radius: 50%; }
        .status-active { background: #22c55e; }
        .status-idle { background: #eab308; }
        .status-error { background: #ef4444; }
        .iaf-header { display: flex; align-items: center; gap: 12px;
            padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.12); }
        .iaf-title { font-size: 1.8rem; font-weight: 700;
            background: linear-gradient(135deg, #00a651, #00d66a);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="IAFactory Operator", page_icon="⚙️", layout="wide")

    if 'language' not in st.session_state:
        st.session_state.language = 'fr'

    inject_css()

    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f'<div class="iaf-header"><span style="font-size:2rem">⚙️</span><span class="iaf-title">{t("title")}</span></div>', unsafe_allow_html=True)
        st.markdown(f"*{t('subtitle')}*")
    with col2:
        lang = st.selectbox("", ['fr', 'en', 'ar'], format_func=lambda x: {'fr': '🇫🇷 FR', 'en': '🇬🇧 EN', 'ar': '🇩🇿 AR'}[x],
                           index=['fr', 'en', 'ar'].index(st.session_state.language), label_visibility="collapsed")
        if lang != st.session_state.language:
            st.session_state.language = lang
            st.rerun()

    # Sidebar
    with st.sidebar:
        menu = st.radio("", [f"📊 {t('dashboard')}", f"🤖 {t('agents')}", f"📋 {t('tasks')}", f"📜 {t('logs')}", f"⚙️ {t('settings')}"], label_visibility="collapsed")

    # Dashboard Metrics
    st.markdown(f"### 📊 {t('dashboard')}")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">19</div><div class="metric-label">{t("active_agents")}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">7</div><div class="metric-label">{t("pending_tasks")}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-value">342</div><div class="metric-label">{t("completed")}</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><div class="metric-value">2</div><div class="metric-label">{t("errors")}</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    # Agents Status
    st.markdown(f"### 🤖 {t('agents')}")
    agents_data = [
        ("Discovery DZ", "active", 8501), ("Recruteur DZ", "active", 8502),
        ("UX Research", "active", 8503), ("Business Consultant", "active", 8504),
        ("Chat PDF", "active", 8505), ("Customer Support", "idle", 8506),
        ("Data Analysis", "active", 8507), ("Financial Coach", "active", 8508),
        ("Legal Assistant", "active", 8509), ("Real Estate", "idle", 8512)
    ]

    col1, col2 = st.columns(2)
    for i, (name, status, port) in enumerate(agents_data):
        with col1 if i % 2 == 0 else col2:
            status_class = f"status-{status}"
            status_icon = "🟢" if status == "active" else "🟡" if status == "idle" else "🔴"
            st.markdown(f'{status_icon} **{name}** - Port {port}')

    st.markdown("---")

    # Command input
    if prompt := st.chat_input(t('input_placeholder')):
        st.markdown(f"**Commande:** `{prompt}`")
        with st.spinner(t('processing')):
            st.success(f"Commande exécutée: {prompt}")

if __name__ == "__main__":
    main()
