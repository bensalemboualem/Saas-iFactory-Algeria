"""
UX Research Agent - Interface Streamlit
Collecte de Feedback Utilisateur pour les Produits IAFactory
"""
import streamlit as st
import asyncio
import sys
import os

# Add parent path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ux_research_agent import (
    UXResearchAgent,
    InterviewState,
    InterviewPhase,
    FeedbackType,
    IAFACTORY_PRODUCTS
)

# ========== TRADUCTIONS ==========
TRANSLATIONS = {
    "fr": {
        "title": "UX Research",
        "subtitle": "Collecte de Feedback Utilisateur - IAFactory",
        "description": "Agent de recherche UX pour améliorer l'expérience utilisateur des produits IAFactory",
        "start_session": "Démarrer la Session",
        "product_label": "Produit à évaluer",
        "select_product": "Sélectionner un produit",
        "user_type_label": "Type d'utilisateur",
        "user_new": "Nouvel utilisateur",
        "user_regular": "Utilisateur régulier",
        "user_power": "Power user",
        "user_beta": "Beta testeur",
        "context_label": "Contexte d'utilisation",
        "context_placeholder": "Ex: J'utilise le produit pour gérer ma comptabilité...",
        "input_placeholder": "Partagez votre expérience...",
        "generate_report": "Générer le Rapport",
        "new_session": "Nouvelle Session",
        "phase": "Phase",
        "exchanges": "Échanges",
        "feedback_collected": "Feedback collecté",
        "satisfaction": "Satisfaction",
        "bugs": "Bugs",
        "features": "Features",
        "ux_issues": "UX",
        "performance": "Performance",
        "welcome": "Bienvenue sur UX Research !",
        "welcome_desc": "Partagez votre expérience pour nous aider à améliorer nos produits.",
        "methodology": "Notre Approche",
        "methodology_tips": [
            "Vos retours sont anonymes et confidentiels",
            "Soyez honnête - les critiques nous aident",
            "Décrivez des situations concrètes",
            "Chaque feedback compte !"
        ],
        "processing": "Analyse en cours...",
        "error": "Une erreur est survenue",
        "action_items": "Actions à prendre",
        "insights": "Insights clés"
    },
    "en": {
        "title": "UX Research",
        "subtitle": "User Feedback Collection - IAFactory",
        "description": "UX research agent to improve IAFactory product user experience",
        "start_session": "Start Session",
        "product_label": "Product to evaluate",
        "select_product": "Select a product",
        "user_type_label": "User type",
        "user_new": "New user",
        "user_regular": "Regular user",
        "user_power": "Power user",
        "user_beta": "Beta tester",
        "context_label": "Usage context",
        "context_placeholder": "Ex: I use the product to manage my accounting...",
        "input_placeholder": "Share your experience...",
        "generate_report": "Generate Report",
        "new_session": "New Session",
        "phase": "Phase",
        "exchanges": "Exchanges",
        "feedback_collected": "Feedback collected",
        "satisfaction": "Satisfaction",
        "bugs": "Bugs",
        "features": "Features",
        "ux_issues": "UX",
        "performance": "Performance",
        "welcome": "Welcome to UX Research!",
        "welcome_desc": "Share your experience to help us improve our products.",
        "methodology": "Our Approach",
        "methodology_tips": [
            "Your feedback is anonymous and confidential",
            "Be honest - criticism helps us",
            "Describe concrete situations",
            "Every feedback counts!"
        ],
        "processing": "Analyzing...",
        "error": "An error occurred",
        "action_items": "Action items",
        "insights": "Key insights"
    },
    "ar": {
        "title": "بحث UX",
        "subtitle": "جمع آراء المستخدمين - IAFactory",
        "description": "وكيل بحث UX لتحسين تجربة المستخدم لمنتجات IAFactory",
        "start_session": "بدء الجلسة",
        "product_label": "المنتج للتقييم",
        "select_product": "اختر منتجًا",
        "user_type_label": "نوع المستخدم",
        "user_new": "مستخدم جديد",
        "user_regular": "مستخدم عادي",
        "user_power": "مستخدم متقدم",
        "user_beta": "مختبر بيتا",
        "context_label": "سياق الاستخدام",
        "context_placeholder": "مثال: أستخدم المنتج لإدارة محاسبتي...",
        "input_placeholder": "شارك تجربتك...",
        "generate_report": "إنشاء التقرير",
        "new_session": "جلسة جديدة",
        "phase": "المرحلة",
        "exchanges": "التبادلات",
        "feedback_collected": "الملاحظات المجمعة",
        "satisfaction": "الرضا",
        "bugs": "الأخطاء",
        "features": "الميزات",
        "ux_issues": "UX",
        "performance": "الأداء",
        "welcome": "مرحبًا بك في بحث UX!",
        "welcome_desc": "شارك تجربتك لمساعدتنا في تحسين منتجاتنا.",
        "methodology": "نهجنا",
        "methodology_tips": [
            "ملاحظاتك مجهولة وسرية",
            "كن صادقًا - النقد يساعدنا",
            "صف مواقف ملموسة",
            "كل ملاحظة مهمة!"
        ],
        "processing": "جاري التحليل...",
        "error": "حدث خطأ",
        "action_items": "إجراءات للقيام بها",
        "insights": "رؤى رئيسية"
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

        .feedback-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin: 2px;
        }

        .badge-bug { background: #ef444420; color: #ef4444; }
        .badge-feature { background: #3b82f620; color: #3b82f6; }
        .badge-ux { background: #a855f720; color: #a855f7; }
        .badge-performance { background: #f9731620; color: #f97316; }
        .badge-positive { background: #22c55e20; color: #22c55e; }

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

        .satisfaction-meter {
            height: 20px;
            border-radius: 10px;
            background: linear-gradient(90deg, #ef4444, #f97316, #eab308, #84cc16, #22c55e);
            position: relative;
            margin: 1rem 0;
        }

        .satisfaction-indicator {
            position: absolute;
            top: -5px;
            width: 30px;
            height: 30px;
            background: white;
            border-radius: 50%;
            border: 3px solid var(--primary);
            transform: translateX(-50%);
        }

        .product-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
            transition: all 0.3s ease;
        }

        .product-card:hover {
            border-color: var(--primary);
            transform: translateY(-2px);
        }

        [data-testid="stSidebar"] {
            background: var(--bg-dark) !important;
        }

        .metric-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
        }

        .metric-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--primary);
        }

        .metric-label {
            font-size: 0.85rem;
            color: var(--text-secondary);
        }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render the header with language selector"""
    col1, col2 = st.columns([4, 1])

    with col1:
        st.markdown(f"""
        <div class="iaf-header">
            <span class="iaf-logo">🔬</span>
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
    """Render sidebar with session stats"""
    with st.sidebar:
        st.markdown(f"### 📊 {t('feedback_collected')}")

        if 'agent' in st.session_state and st.session_state.agent:
            state = st.session_state.agent.interview_state

            # Phase indicator
            phase_names = {
                'introduction': 'Introduction',
                'general_usage': 'Usage Général',
                'pain_points': 'Points de Friction',
                'feature_requests': 'Suggestions',
                'closing': 'Closing'
            }

            st.markdown(f"**{t('phase')}:** {phase_names.get(state.current_phase.value, state.current_phase.value)}")
            st.markdown(f"**{t('exchanges')}:** {state.total_exchanges}")

            # Progress bar
            total_phases = 5
            current_idx = list(InterviewPhase).index(state.current_phase) + 1
            progress = current_idx / total_phases
            st.progress(progress, text=f"Phase {current_idx}/{total_phases}")

            st.markdown("---")

            # Feedback metrics
            if state.feedback_items:
                st.markdown(f"### 📋 Types de feedback")

                bugs = len([f for f in state.feedback_items if f.type == FeedbackType.BUG])
                features = len([f for f in state.feedback_items if f.type == FeedbackType.FEATURE_REQUEST])
                ux = len([f for f in state.feedback_items if f.type == FeedbackType.UX_ISSUE])
                perf = len([f for f in state.feedback_items if f.type == FeedbackType.PERFORMANCE])
                positive = len([f for f in state.feedback_items if f.type == FeedbackType.POSITIVE])

                col1, col2 = st.columns(2)
                with col1:
                    if bugs > 0:
                        st.markdown(f'<span class="feedback-badge badge-bug">🐛 {bugs} {t("bugs")}</span>', unsafe_allow_html=True)
                    if features > 0:
                        st.markdown(f'<span class="feedback-badge badge-feature">✨ {features} {t("features")}</span>', unsafe_allow_html=True)
                with col2:
                    if ux > 0:
                        st.markdown(f'<span class="feedback-badge badge-ux">🎨 {ux} {t("ux_issues")}</span>', unsafe_allow_html=True)
                    if perf > 0:
                        st.markdown(f'<span class="feedback-badge badge-performance">⚡ {perf} {t("performance")}</span>', unsafe_allow_html=True)

                if positive > 0:
                    st.markdown(f'<span class="feedback-badge badge-positive">👍 {positive} Positifs</span>', unsafe_allow_html=True)

            # Satisfaction score
            if state.satisfaction_score:
                st.markdown("---")
                st.markdown(f"### {t('satisfaction')}")
                satisfaction_percent = state.satisfaction_score * 10
                st.progress(satisfaction_percent / 100, text=f"{state.satisfaction_score}/10")

        st.markdown("---")

        # Methodology tips
        st.markdown(f"### 💡 {t('methodology')}")
        for tip in t('methodology_tips'):
            st.markdown(f"• {tip}")

def render_setup_form():
    """Render the session setup form"""
    st.markdown(f"### {t('welcome')}")
    st.markdown(t('welcome_desc'))

    with st.form("session_setup"):
        # Product selection
        product_options = {k: v['name'] for k, v in IAFACTORY_PRODUCTS.items()}
        product = st.selectbox(
            t('product_label'),
            options=[''] + list(product_options.keys()),
            format_func=lambda x: t('select_product') if x == '' else product_options.get(x, x)
        )

        col1, col2 = st.columns(2)

        with col1:
            user_types = {
                'new': t('user_new'),
                'regular': t('user_regular'),
                'power': t('user_power'),
                'beta': t('user_beta')
            }
            user_type = st.selectbox(
                t('user_type_label'),
                options=list(user_types.keys()),
                format_func=lambda x: user_types[x]
            )

        with col2:
            context = st.text_area(
                t('context_label'),
                placeholder=t('context_placeholder'),
                height=100
            )

        submitted = st.form_submit_button(t('start_session'), use_container_width=True)

        if submitted and product:
            return {
                'product': product,
                'user_type': user_type,
                'context': context
            }

    # Product showcase
    st.markdown("---")
    st.markdown("### 🎯 Nos Produits")

    cols = st.columns(3)
    for idx, (key, product) in enumerate(list(IAFACTORY_PRODUCTS.items())[:6]):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="product-card">
                <h4>{product['name']}</h4>
                <p style="font-size: 0.85rem; color: var(--text-secondary);">{product.get('category', 'Agent IA')}</p>
            </div>
            """, unsafe_allow_html=True)

    return None

async def run_agent_action(agent, action_data):
    """Run agent action asynchronously"""
    return await agent.execute(action_data)

def main():
    # Page config
    st.set_page_config(
        page_title="UX Research | IAFactory Algeria",
        page_icon="🔬",
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
    if 'session_started' not in st.session_state:
        st.session_state.session_started = False

    # Inject CSS
    inject_css()

    # Render header
    render_header()

    # Render sidebar
    render_sidebar()

    # Main content
    if not st.session_state.session_started:
        # Setup form
        setup_data = render_setup_form()

        if setup_data:
            # Initialize agent
            st.session_state.agent = UXResearchAgent()

            # Start session
            with st.spinner(t('processing')):
                result = asyncio.run(run_agent_action(
                    st.session_state.agent,
                    {
                        'action': 'start',
                        'product': setup_data['product'],
                        'user_type': setup_data['user_type'],
                        'context': setup_data['context']
                    }
                ))

            st.session_state.messages.append({
                'role': 'assistant',
                'content': result.content
            })
            st.session_state.session_started = True
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
            if st.button(f"🔄 {t('new_session')}", use_container_width=True):
                st.session_state.messages = []
                st.session_state.agent = None
                st.session_state.session_started = False
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
