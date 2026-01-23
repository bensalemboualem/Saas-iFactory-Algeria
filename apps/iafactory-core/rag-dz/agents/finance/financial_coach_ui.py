"""
Financial Coach - Interface Streamlit
Coach financier personnel pour gestion budget et investissements
"""
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TRANSLATIONS = {
    "fr": {
        "title": "Coach Financier IA",
        "subtitle": "Gestion Budget & Investissements - Algérie",
        "welcome": "Bienvenue ! Je suis votre coach financier personnel. Comment puis-je vous aider à mieux gérer vos finances ?",
        "input_placeholder": "Posez votre question financière...",
        "topics": "Sujets",
        "budget": "Budget mensuel",
        "savings": "Épargne",
        "investment": "Investissement",
        "taxes": "Fiscalité DZ",
        "retirement": "Retraite",
        "new_chat": "Nouvelle conversation",
        "processing": "Analyse financière...",
        "tip_title": "Conseil du jour",
        "tip": "Épargnez au moins 20% de vos revenus mensuels pour constituer un fonds d'urgence."
    },
    "en": {
        "title": "AI Financial Coach",
        "subtitle": "Budget Management & Investments - Algeria",
        "welcome": "Welcome! I'm your personal financial coach. How can I help you manage your finances better?",
        "input_placeholder": "Ask your financial question...",
        "topics": "Topics",
        "budget": "Monthly budget",
        "savings": "Savings",
        "investment": "Investment",
        "taxes": "DZ Taxes",
        "retirement": "Retirement",
        "new_chat": "New conversation",
        "processing": "Financial analysis...",
        "tip_title": "Tip of the day",
        "tip": "Save at least 20% of your monthly income to build an emergency fund."
    },
    "ar": {
        "title": "المدرب المالي بالذكاء الاصطناعي",
        "subtitle": "إدارة الميزانية والاستثمارات - الجزائر",
        "welcome": "مرحبًا! أنا مدربك المالي الشخصي. كيف يمكنني مساعدتك في إدارة أموالك بشكل أفضل؟",
        "input_placeholder": "اطرح سؤالك المالي...",
        "topics": "المواضيع",
        "budget": "الميزانية الشهرية",
        "savings": "الادخار",
        "investment": "الاستثمار",
        "taxes": "الضرائب DZ",
        "retirement": "التقاعد",
        "new_chat": "محادثة جديدة",
        "processing": "التحليل المالي...",
        "tip_title": "نصيحة اليوم",
        "tip": "وفر 20٪ على الأقل من دخلك الشهري لبناء صندوق طوارئ."
    }
}

def t(key):
    lang = st.session_state.get('language', 'fr')
    return TRANSLATIONS.get(lang, TRANSLATIONS['fr']).get(key, key)

def inject_css():
    st.markdown("""
    <style>
        .main .block-container { padding-top: 2rem; max-width: 900px; }
        .stButton > button { background: linear-gradient(135deg, #00a651, #00d66a) !important;
            color: white !important; border: none !important; border-radius: 10px !important; }
        .tip-card { background: linear-gradient(135deg, rgba(0,166,81,0.1), rgba(0,166,81,0.05));
            padding: 1rem; border-radius: 12px; border-left: 4px solid #00a651; margin: 1rem 0; }
        .iaf-header { display: flex; align-items: center; gap: 12px;
            padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.12); }
        .iaf-title { font-size: 1.8rem; font-weight: 700;
            background: linear-gradient(135deg, #00a651, #00d66a);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    </style>
    """, unsafe_allow_html=True)

def get_financial_response(question, topic=None):
    """Simulate financial coach response"""
    responses = {
        "budget": """📊 **Conseil Budget Mensuel**

Pour un budget efficace en Algérie, je recommande la règle 50/30/20:
- **50%** pour les besoins essentiels (loyer, nourriture, transport)
- **30%** pour les envies (loisirs, sorties)
- **20%** pour l'épargne et remboursement de dettes

💡 Utilisez des applications comme Excel ou des apps mobiles pour suivre vos dépenses quotidiennes.""",
        "savings": """💰 **Stratégie d'Épargne**

Options d'épargne en Algérie:
1. **Compte épargne CCP** - Sécurisé, taux faible
2. **Livret d'épargne bancaire** - Meilleur rendement
3. **Bons du Trésor** - Pour épargne long terme

🎯 Objectif: 3-6 mois de dépenses en fonds d'urgence.""",
        "investment": """📈 **Options d'Investissement en Algérie**

1. **Immobilier** - Investissement traditionnel, bonne protection inflation
2. **Or** - Valeur refuge, disponible chez bijoutiers agréés
3. **Actions Bourse d'Alger** - Marché en développement
4. **Commerce** - Import/export, petit commerce local

⚠️ Diversifiez vos investissements pour réduire les risques.""",
        "default": "Je suis là pour vous aider avec vos questions financières. Pouvez-vous préciser votre question sur le budget, l'épargne, ou l'investissement ?"
    }
    return responses.get(topic, responses["default"])

def main():
    st.set_page_config(page_title="Coach Financier | IAFactory", page_icon="💰", layout="wide")

    if 'language' not in st.session_state:
        st.session_state.language = 'fr'
    if 'messages' not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": t('welcome')}]
    if 'topic' not in st.session_state:
        st.session_state.topic = None

    inject_css()

    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f'<div class="iaf-header"><span style="font-size:2rem">💰</span><span class="iaf-title">{t("title")}</span></div>', unsafe_allow_html=True)
        st.markdown(f"*{t('subtitle')}*")
    with col2:
        lang = st.selectbox("", ['fr', 'en', 'ar'], format_func=lambda x: {'fr': '🇫🇷 FR', 'en': '🇬🇧 EN', 'ar': '🇩🇿 AR'}[x],
                           index=['fr', 'en', 'ar'].index(st.session_state.language), label_visibility="collapsed")
        if lang != st.session_state.language:
            st.session_state.language = lang
            st.rerun()

    # Sidebar
    with st.sidebar:
        st.markdown(f"### {t('topics')}")
        topics = [('budget', t('budget'), '📊'), ('savings', t('savings'), '💵'),
                 ('investment', t('investment'), '📈'), ('taxes', t('taxes'), '🏛️'),
                 ('retirement', t('retirement'), '🏖️')]
        for topic_id, topic_name, icon in topics:
            if st.button(f"{icon} {topic_name}", key=topic_id, use_container_width=True):
                st.session_state.topic = topic_id
                response = get_financial_response("", topic_id)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

        st.markdown("---")
        st.markdown(f'<div class="tip-card"><strong>💡 {t("tip_title")}</strong><br>{t("tip")}</div>', unsafe_allow_html=True)

        st.markdown("---")
        if st.button(f"🔄 {t('new_chat')}", use_container_width=True):
            st.session_state.messages = [{"role": "assistant", "content": t('welcome')}]
            st.rerun()

    # Chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input(t('input_placeholder')):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner(t('processing')):
                response = get_financial_response(prompt, st.session_state.topic)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

if __name__ == "__main__":
    main()
