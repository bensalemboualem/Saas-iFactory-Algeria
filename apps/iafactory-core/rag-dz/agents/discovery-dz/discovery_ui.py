"""
Discovery DZ - Interface Streamlit
Customer Discovery & Market Validation pour Startups Algériennes
"""
import streamlit as st
import asyncio
import sys
import os

# Add parent path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from discovery_agent import (
    DiscoveryAgent,
    InterviewState,
    InterviewPhase,
    ALGERIAN_SECTORS,
    PHASE_QUESTIONS
)

# ========== TRADUCTIONS ==========
TRANSLATIONS = {
    "fr": {
        "title": "Discovery DZ",
        "subtitle": "Validation Marché - Méthodologie Mom Test",
        "description": "Agent de customer discovery pour valider vos hypothèses business sur le marché algérien",
        "start_interview": "Démarrer l'Interview",
        "problem_label": "Problème à valider",
        "problem_placeholder": "Ex: Les PME algériennes perdent du temps à gérer leur comptabilité manuellement",
        "target_label": "Profil cible",
        "target_placeholder": "Ex: Gérant de PME, 30-50 ans, secteur commerce",
        "sector_label": "Secteur",
        "select_sector": "Sélectionner un secteur",
        "input_placeholder": "Répondez à la question de l'agent...",
        "generate_report": "Générer le Rapport",
        "new_interview": "Nouvelle Interview",
        "phase": "Phase",
        "exchanges": "Échanges",
        "signals": "Signaux détectés",
        "strong": "Forts",
        "medium": "Moyens",
        "weak": "Faibles",
        "welcome": "Bienvenue sur Discovery DZ !",
        "welcome_desc": "Configurez votre interview de validation marché ci-dessous.",
        "methodology": "Méthodologie Mom Test",
        "methodology_tips": [
            "Parler du problème, pas de votre solution",
            "Questions sur le passé concret",
            "Chercher les faits, pas les opinions",
            "Quantifier : fréquence, coût, temps"
        ],
        "processing": "Analyse en cours...",
        "error": "Une erreur est survenue"
    },
    "en": {
        "title": "Discovery DZ",
        "subtitle": "Market Validation - Mom Test Methodology",
        "description": "Customer discovery agent to validate your business hypotheses in the Algerian market",
        "start_interview": "Start Interview",
        "problem_label": "Problem to validate",
        "problem_placeholder": "Ex: Algerian SMEs waste time managing their accounting manually",
        "target_label": "Target profile",
        "target_placeholder": "Ex: SME Manager, 30-50 years old, retail sector",
        "sector_label": "Sector",
        "select_sector": "Select a sector",
        "input_placeholder": "Respond to the agent's question...",
        "generate_report": "Generate Report",
        "new_interview": "New Interview",
        "phase": "Phase",
        "exchanges": "Exchanges",
        "signals": "Detected signals",
        "strong": "Strong",
        "medium": "Medium",
        "weak": "Weak",
        "welcome": "Welcome to Discovery DZ!",
        "welcome_desc": "Configure your market validation interview below.",
        "methodology": "Mom Test Methodology",
        "methodology_tips": [
            "Talk about the problem, not your solution",
            "Questions about concrete past events",
            "Look for facts, not opinions",
            "Quantify: frequency, cost, time"
        ],
        "processing": "Analyzing...",
        "error": "An error occurred"
    },
    "ar": {
        "title": "Discovery DZ",
        "subtitle": "التحقق من السوق - منهجية Mom Test",
        "description": "وكيل اكتشاف العملاء للتحقق من فرضيات عملك في السوق الجزائرية",
        "start_interview": "بدء المقابلة",
        "problem_label": "المشكلة للتحقق منها",
        "problem_placeholder": "مثال: الشركات الجزائرية تضيع الوقت في إدارة محاسبتها يدويًا",
        "target_label": "الملف الشخصي المستهدف",
        "target_placeholder": "مثال: مدير شركة، 30-50 سنة، قطاع التجارة",
        "sector_label": "القطاع",
        "select_sector": "اختر قطاعًا",
        "input_placeholder": "أجب على سؤال الوكيل...",
        "generate_report": "إنشاء التقرير",
        "new_interview": "مقابلة جديدة",
        "phase": "المرحلة",
        "exchanges": "التبادلات",
        "signals": "الإشارات المكتشفة",
        "strong": "قوية",
        "medium": "متوسطة",
        "weak": "ضعيفة",
        "welcome": "مرحبًا بك في Discovery DZ!",
        "welcome_desc": "قم بتكوين مقابلة التحقق من السوق أدناه.",
        "methodology": "منهجية Mom Test",
        "methodology_tips": [
            "تحدث عن المشكلة وليس الحل",
            "أسئلة عن الماضي الملموس",
            "ابحث عن الحقائق وليس الآراء",
            "حدد الكمية: التكرار، التكلفة، الوقت"
        ],
        "processing": "جاري التحليل...",
        "error": "حدث خطأ"
    }
}

def t(key: str) -> str:
    """Get translation for current language"""
    lang = st.session_state.get('language', 'fr')
    return TRANSLATIONS.get(lang, TRANSLATIONS['fr']).get(key, key)

def inject_css():
    """Inject IAFactory theme CSS"""
    st.markdown("""
    <style>
        :root {
            --primary: #00a651;
            --primary-light: #00d66a;
            --bg-dark: #020617;
            --bg-card: #0a0e1f;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --border: rgba(255, 255, 255, 0.12);
        }

        .main .block-container {
            padding-top: 2rem;
            max-width: 1200px;
        }

        .stButton > button {
            background: linear-gradient(135deg, var(--primary), var(--primary-light)) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.6rem 1.5rem !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(0, 166, 81, 0.4) !important;
        }

        .phase-indicator {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1rem;
            margin: 1rem 0;
        }

        .signal-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin: 2px;
        }

        .signal-strong { background: #22c55e20; color: #22c55e; }
        .signal-medium { background: #eab30820; color: #eab308; }
        .signal-weak { background: #ef444420; color: #ef4444; }

        .iaf-header {
            display: flex;
            align-items: center;
            gap: 12px;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border);
            margin-bottom: 1.5rem;
        }

        .iaf-logo {
            font-size: 2rem;
        }

        .iaf-title {
            font-size: 1.8rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary), var(--primary-light));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .stChatMessage {
            background: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            border-radius: 12px !important;
        }

        .methodology-card {
            background: linear-gradient(135deg, rgba(0, 166, 81, 0.1), rgba(0, 166, 81, 0.05));
            border: 1px solid rgba(0, 166, 81, 0.3);
            border-radius: 12px;
            padding: 1rem;
        }

        [data-testid="stSidebar"] {
            background: var(--bg-dark) !important;
        }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render the header with language selector"""
    col1, col2 = st.columns([4, 1])

    with col1:
        st.markdown(f"""
        <div class="iaf-header">
            <span class="iaf-logo">🇩🇿</span>
            <span class="iaf-title">{t('title')}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"*{t('subtitle')}*")

    with col2:
        lang_options = {'fr': '🇫🇷 FR', 'en': '🇬🇧 EN', 'ar': '🇩🇿 AR'}
        current_lang = st.session_state.get('language', 'fr')
        selected = st.selectbox(
            "Language",
            options=list(lang_options.keys()),
            format_func=lambda x: lang_options[x],
            index=list(lang_options.keys()).index(current_lang),
            key='lang_select',
            label_visibility="collapsed"
        )
        if selected != current_lang:
            st.session_state.language = selected
            st.rerun()

def render_sidebar():
    """Render sidebar with interview stats"""
    with st.sidebar:
        st.markdown(f"### 📊 {t('signals')}")

        if 'agent' in st.session_state and st.session_state.agent:
            state = st.session_state.agent.interview_state

            # Phase indicator
            phase_names = {
                'qualification': 'Qualification',
                'problem_exploration': 'Exploration Problème',
                'current_solutions': 'Solutions Actuelles',
                'value_validation': 'Validation Valeur',
                'closing': 'Closing'
            }

            st.markdown(f"**{t('phase')}:** {phase_names.get(state.current_phase.value, state.current_phase.value)}")
            st.markdown(f"**{t('exchanges')}:** {state.total_exchanges}")

            st.markdown("---")

            # Signal counts
            strong = len([s for s in state.signals if s.type.value == 'strong'])
            medium = len([s for s in state.signals if s.type.value == 'medium'])
            weak = len([s for s in state.signals if s.type.value == 'weak'])

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(f"🟢 {t('strong')}", strong)
            with col2:
                st.metric(f"🟡 {t('medium')}", medium)
            with col3:
                st.metric(f"🔴 {t('weak')}", weak)

            # Progress bar
            total_phases = 5
            current_idx = list(InterviewPhase).index(state.current_phase) + 1
            progress = current_idx / total_phases
            st.progress(progress, text=f"Phase {current_idx}/{total_phases}")

        st.markdown("---")

        # Methodology tips
        st.markdown(f"### 💡 {t('methodology')}")
        for tip in t('methodology_tips'):
            st.markdown(f"• {tip}")

def render_setup_form():
    """Render the interview setup form"""
    st.markdown(f"### {t('welcome')}")
    st.markdown(t('welcome_desc'))

    with st.form("interview_setup"):
        problem = st.text_area(
            t('problem_label'),
            placeholder=t('problem_placeholder'),
            height=100
        )

        target = st.text_input(
            t('target_label'),
            placeholder=t('target_placeholder')
        )

        sector_options = {k: v['name'] for k, v in ALGERIAN_SECTORS.items()}
        sector = st.selectbox(
            t('sector_label'),
            options=[''] + list(sector_options.keys()),
            format_func=lambda x: t('select_sector') if x == '' else sector_options.get(x, x)
        )

        submitted = st.form_submit_button(t('start_interview'), use_container_width=True)

        if submitted and problem and target:
            return {'problem': problem, 'target': target, 'sector': sector or None}

    return None

async def run_agent_action(agent, action_data):
    """Run agent action asynchronously"""
    return await agent.execute(action_data)

def main():
    # Page config
    st.set_page_config(
        page_title="Discovery DZ | IAFactory Algeria",
        page_icon="🇩🇿",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize session state
    if 'language' not in st.session_state:
        st.session_state.language = 'fr'
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'agent' not in st.session_state:
        st.session_state.agent = None
    if 'interview_started' not in st.session_state:
        st.session_state.interview_started = False

    # Inject CSS
    inject_css()

    # Render header
    render_header()

    # Render sidebar
    render_sidebar()

    # Main content
    if not st.session_state.interview_started:
        # Setup form
        setup_data = render_setup_form()

        if setup_data:
            # Initialize agent
            st.session_state.agent = DiscoveryAgent()

            # Start interview
            with st.spinner(t('processing')):
                result = asyncio.run(run_agent_action(
                    st.session_state.agent,
                    {
                        'action': 'start',
                        'problem': setup_data['problem'],
                        'target': setup_data['target'],
                        'sector': setup_data['sector']
                    }
                ))

            st.session_state.messages.append({
                'role': 'assistant',
                'content': result.content
            })
            st.session_state.interview_started = True
            st.rerun()

    else:
        # Display chat messages
        for msg in st.session_state.messages:
            with st.chat_message(msg['role']):
                st.markdown(msg['content'])

        # Action buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button(f"📊 {t('generate_report')}", use_container_width=True):
                with st.spinner(t('processing')):
                    result = asyncio.run(run_agent_action(
                        st.session_state.agent,
                        {'action': 'report'}
                    ))
                st.session_state.messages.append({
                    'role': 'assistant',
                    'content': result.content
                })
                st.rerun()

        with col2:
            if st.button(f"🔄 {t('new_interview')}", use_container_width=True):
                st.session_state.messages = []
                st.session_state.agent = None
                st.session_state.interview_started = False
                st.rerun()

        # Chat input
        if prompt := st.chat_input(t('input_placeholder')):
            # Add user message
            st.session_state.messages.append({
                'role': 'user',
                'content': prompt
            })

            # Get agent response
            with st.spinner(t('processing')):
                try:
                    result = asyncio.run(run_agent_action(
                        st.session_state.agent,
                        {'action': 'continue', 'message': prompt}
                    ))
                    st.session_state.messages.append({
                        'role': 'assistant',
                        'content': result.content
                    })
                except Exception as e:
                    st.error(f"{t('error')}: {str(e)}")

            st.rerun()


if __name__ == "__main__":
    main()
