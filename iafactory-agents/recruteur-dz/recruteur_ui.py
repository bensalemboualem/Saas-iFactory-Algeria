"""
Recruteur DZ - Interface Streamlit
AI Recruitment & Candidate Evaluation pour le Marché Algérien
"""
import streamlit as st
import asyncio
import sys
import os

# Add parent path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from recruteur_agent import (
    RecruteurAgent,
    InterviewState,
    InterviewMode,
    InterviewPhase,
    JOB_CATEGORIES
)

# ========== TRADUCTIONS ==========
TRANSLATIONS = {
    "fr": {
        "title": "Recruteur DZ",
        "subtitle": "Entretiens de Recrutement IA - Méthodologie STAR",
        "description": "Agent de recrutement intelligent adapté au marché de l'emploi algérien",
        "start_interview": "Démarrer l'Entretien",
        "mode_label": "Mode d'entretien",
        "mode_evaluation": "Évaluation (pour recruteurs)",
        "mode_simulation": "Simulation (pour candidats)",
        "mode_screening": "Screening rapide",
        "position_label": "Poste recherché",
        "position_placeholder": "Ex: Développeur Full Stack Senior",
        "category_label": "Catégorie",
        "select_category": "Sélectionner une catégorie",
        "candidate_name": "Nom du candidat",
        "candidate_placeholder": "Ex: Ahmed Benali",
        "input_placeholder": "Répondez à la question...",
        "generate_report": "Générer le Rapport",
        "new_interview": "Nouvel Entretien",
        "phase": "Phase",
        "exchanges": "Échanges",
        "evaluations": "Évaluations",
        "red_flags": "Red Flags",
        "strengths": "Points forts",
        "welcome": "Bienvenue sur Recruteur DZ !",
        "welcome_desc": "Configurez votre entretien de recrutement ci-dessous.",
        "methodology": "Méthodologie STAR",
        "methodology_tips": [
            "Situation : Contexte de l'expérience",
            "Tâche : Responsabilité du candidat",
            "Action : Ce qu'il a concrètement fait",
            "Résultat : Impact mesurable"
        ],
        "processing": "Analyse en cours...",
        "error": "Une erreur est survenue",
        "score": "Score global",
        "recommendation": "Recommandation"
    },
    "en": {
        "title": "Recruiter DZ",
        "subtitle": "AI Recruitment Interviews - STAR Methodology",
        "description": "Intelligent recruitment agent adapted to the Algerian job market",
        "start_interview": "Start Interview",
        "mode_label": "Interview mode",
        "mode_evaluation": "Evaluation (for recruiters)",
        "mode_simulation": "Simulation (for candidates)",
        "mode_screening": "Quick screening",
        "position_label": "Position sought",
        "position_placeholder": "Ex: Senior Full Stack Developer",
        "category_label": "Category",
        "select_category": "Select a category",
        "candidate_name": "Candidate name",
        "candidate_placeholder": "Ex: Ahmed Benali",
        "input_placeholder": "Answer the question...",
        "generate_report": "Generate Report",
        "new_interview": "New Interview",
        "phase": "Phase",
        "exchanges": "Exchanges",
        "evaluations": "Evaluations",
        "red_flags": "Red Flags",
        "strengths": "Strengths",
        "welcome": "Welcome to Recruiter DZ!",
        "welcome_desc": "Configure your recruitment interview below.",
        "methodology": "STAR Methodology",
        "methodology_tips": [
            "Situation: Context of the experience",
            "Task: Candidate's responsibility",
            "Action: What they concretely did",
            "Result: Measurable impact"
        ],
        "processing": "Analyzing...",
        "error": "An error occurred",
        "score": "Overall score",
        "recommendation": "Recommendation"
    },
    "ar": {
        "title": "المجند DZ",
        "subtitle": "مقابلات التوظيف بالذكاء الاصطناعي - منهجية STAR",
        "description": "وكيل توظيف ذكي متكيف مع سوق العمل الجزائري",
        "start_interview": "بدء المقابلة",
        "mode_label": "نمط المقابلة",
        "mode_evaluation": "تقييم (للمجندين)",
        "mode_simulation": "محاكاة (للمرشحين)",
        "mode_screening": "فرز سريع",
        "position_label": "الوظيفة المطلوبة",
        "position_placeholder": "مثال: مطور Full Stack أول",
        "category_label": "الفئة",
        "select_category": "اختر فئة",
        "candidate_name": "اسم المرشح",
        "candidate_placeholder": "مثال: أحمد بن علي",
        "input_placeholder": "أجب على السؤال...",
        "generate_report": "إنشاء التقرير",
        "new_interview": "مقابلة جديدة",
        "phase": "المرحلة",
        "exchanges": "التبادلات",
        "evaluations": "التقييمات",
        "red_flags": "علامات تحذير",
        "strengths": "نقاط القوة",
        "welcome": "مرحبًا بك في المجند DZ!",
        "welcome_desc": "قم بتكوين مقابلة التوظيف أدناه.",
        "methodology": "منهجية STAR",
        "methodology_tips": [
            "الموقف: سياق التجربة",
            "المهمة: مسؤولية المرشح",
            "الإجراء: ما فعله بالفعل",
            "النتيجة: التأثير القابل للقياس"
        ],
        "processing": "جاري التحليل...",
        "error": "حدث خطأ",
        "score": "النتيجة الإجمالية",
        "recommendation": "التوصية"
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

        .phase-badge {
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            background: linear-gradient(135deg, var(--primary), var(--primary-light));
            color: white;
            margin: 4px;
        }

        .red-flag-badge {
            background: #ef444420;
            color: #ef4444;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.85rem;
            margin: 2px;
            display: inline-block;
        }

        .strength-badge {
            background: #22c55e20;
            color: #22c55e;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.85rem;
            margin: 2px;
            display: inline-block;
        }

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

        .score-display {
            font-size: 2.5rem;
            font-weight: 700;
            text-align: center;
            padding: 1rem;
        }

        .score-excellent { color: #22c55e; }
        .score-good { color: #84cc16; }
        .score-average { color: #eab308; }
        .score-poor { color: #ef4444; }

        [data-testid="stSidebar"] {
            background: var(--bg-dark) !important;
        }

        .mode-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .mode-card:hover {
            border-color: var(--primary);
            transform: translateY(-2px);
        }

        .mode-card.selected {
            border-color: var(--primary);
            background: rgba(0, 166, 81, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render the header with language selector"""
    col1, col2 = st.columns([4, 1])

    with col1:
        st.markdown(f"""
        <div class="iaf-header">
            <span class="iaf-logo">👔</span>
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
        st.markdown(f"### 📊 Tableau de bord")

        if 'agent' in st.session_state and st.session_state.agent:
            state = st.session_state.agent.interview_state

            # Phase indicator
            phase_names = {
                'introduction': 'Introduction',
                'experience': 'Expérience',
                'technical': 'Technique',
                'soft_skills': 'Soft Skills',
                'motivation': 'Motivation',
                'closing': 'Closing'
            }

            st.markdown(f"**{t('phase')}:** {phase_names.get(state.current_phase.value, state.current_phase.value)}")
            st.markdown(f"**{t('exchanges')}:** {state.total_exchanges}")

            # Progress bar
            total_phases = 6
            current_idx = list(InterviewPhase).index(state.current_phase) + 1
            progress = current_idx / total_phases
            st.progress(progress, text=f"Phase {current_idx}/{total_phases}")

            st.markdown("---")

            # Evaluations
            if state.evaluations:
                st.markdown(f"### 📈 {t('evaluations')}")
                avg_score = sum(e.score for e in state.evaluations) / len(state.evaluations)
                score_class = "excellent" if avg_score >= 4 else "good" if avg_score >= 3 else "average" if avg_score >= 2 else "poor"
                st.markdown(f'<div class="score-display score-{score_class}">{avg_score:.1f}/5</div>', unsafe_allow_html=True)

            # Red flags
            if state.red_flags:
                st.markdown(f"### ⚠️ {t('red_flags')}")
                for flag in state.red_flags[:5]:
                    st.markdown(f'<span class="red-flag-badge">🚩 {flag}</span>', unsafe_allow_html=True)

            # Strengths
            if state.strengths:
                st.markdown(f"### ✅ {t('strengths')}")
                for strength in state.strengths[:5]:
                    st.markdown(f'<span class="strength-badge">💪 {strength}</span>', unsafe_allow_html=True)

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
        # Mode selection
        mode_options = {
            'evaluation': t('mode_evaluation'),
            'simulation': t('mode_simulation'),
            'screening': t('mode_screening')
        }
        mode = st.radio(
            t('mode_label'),
            options=list(mode_options.keys()),
            format_func=lambda x: mode_options[x],
            horizontal=True
        )

        col1, col2 = st.columns(2)

        with col1:
            position = st.text_input(
                t('position_label'),
                placeholder=t('position_placeholder')
            )

        with col2:
            category_options = {k: v['name'] for k, v in JOB_CATEGORIES.items()}
            category = st.selectbox(
                t('category_label'),
                options=[''] + list(category_options.keys()),
                format_func=lambda x: t('select_category') if x == '' else category_options.get(x, x)
            )

        candidate_name = st.text_input(
            t('candidate_name'),
            placeholder=t('candidate_placeholder')
        )

        submitted = st.form_submit_button(t('start_interview'), use_container_width=True)

        if submitted and position:
            return {
                'mode': mode,
                'position': position,
                'category': category or 'tech',
                'candidate_name': candidate_name
            }

    return None

async def run_agent_action(agent, action_data):
    """Run agent action asynchronously"""
    return await agent.execute(action_data)

def main():
    # Page config
    st.set_page_config(
        page_title="Recruteur DZ | IAFactory Algeria",
        page_icon="👔",
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
            st.session_state.agent = RecruteurAgent()

            # Start interview
            with st.spinner(t('processing')):
                result = asyncio.run(run_agent_action(
                    st.session_state.agent,
                    {
                        'action': 'start',
                        'mode': setup_data['mode'],
                        'position': setup_data['position'],
                        'category': setup_data['category'],
                        'candidate_name': setup_data['candidate_name']
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
