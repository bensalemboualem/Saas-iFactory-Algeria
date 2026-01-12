"""
Customer Support Agent - Interface Streamlit
Support Client Intelligent 24/7 avec contexte algérien
"""
import streamlit as st
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Translations
TRANSLATIONS = {
    "fr": {
        "title": "Support Client IA",
        "subtitle": "Assistance 24/7 - Multilingue",
        "description": "Support client intelligent avec compréhension du contexte algérien",
        "input_placeholder": "Décrivez votre problème ou question...",
        "send": "Envoyer",
        "new_chat": "Nouvelle conversation",
        "welcome": "Bienvenue ! Comment puis-je vous aider aujourd'hui ?",
        "processing": "Traitement en cours...",
        "categories": "Catégories",
        "cat_billing": "Facturation",
        "cat_technical": "Technique",
        "cat_account": "Mon compte",
        "cat_general": "Général",
        "satisfaction": "Cette réponse vous a-t-elle aidé ?",
        "yes": "Oui",
        "no": "Non"
    },
    "en": {
        "title": "AI Customer Support",
        "subtitle": "24/7 Assistance - Multilingual",
        "description": "Intelligent customer support with Algerian context understanding",
        "input_placeholder": "Describe your problem or question...",
        "send": "Send",
        "new_chat": "New conversation",
        "welcome": "Welcome! How can I help you today?",
        "processing": "Processing...",
        "categories": "Categories",
        "cat_billing": "Billing",
        "cat_technical": "Technical",
        "cat_account": "My account",
        "cat_general": "General",
        "satisfaction": "Was this answer helpful?",
        "yes": "Yes",
        "no": "No"
    },
    "ar": {
        "title": "دعم العملاء بالذكاء الاصطناعي",
        "subtitle": "مساعدة 24/7 - متعدد اللغات",
        "description": "دعم عملاء ذكي مع فهم السياق الجزائري",
        "input_placeholder": "صف مشكلتك أو سؤالك...",
        "send": "إرسال",
        "new_chat": "محادثة جديدة",
        "welcome": "مرحبًا! كيف يمكنني مساعدتك اليوم؟",
        "processing": "جاري المعالجة...",
        "categories": "الفئات",
        "cat_billing": "الفواتير",
        "cat_technical": "تقني",
        "cat_account": "حسابي",
        "cat_general": "عام",
        "satisfaction": "هل ساعدتك هذه الإجابة؟",
        "yes": "نعم",
        "no": "لا"
    }
}

def t(key):
    lang = st.session_state.get('language', 'fr')
    return TRANSLATIONS.get(lang, TRANSLATIONS['fr']).get(key, key)

def inject_css():
    st.markdown("""
    <style>
        .main .block-container { padding-top: 2rem; max-width: 900px; }
        .stButton > button {
            background: linear-gradient(135deg, #00a651, #00d66a) !important;
            color: white !important; border: none !important;
            border-radius: 10px !important; font-weight: 600 !important;
        }
        .iaf-header { display: flex; align-items: center; gap: 12px;
            padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.12); margin-bottom: 1.5rem; }
        .iaf-title { font-size: 1.8rem; font-weight: 700;
            background: linear-gradient(135deg, #00a651, #00d66a);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .category-btn { padding: 8px 16px; border-radius: 20px; margin: 4px;
            background: rgba(0,166,81,0.1); border: 1px solid rgba(0,166,81,0.3);
            cursor: pointer; transition: all 0.3s; }
        .category-btn:hover { background: rgba(0,166,81,0.2); }
    </style>
    """, unsafe_allow_html=True)

def get_ai_response(message, category=None):
    """Simulate AI response - replace with actual agent call"""
    responses = {
        "facturation": "Je comprends votre question sur la facturation. En Algérie, nous acceptons les paiements par CCP, Baridimob, et virement bancaire. Votre facture sera disponible dans les 24h.",
        "technique": "Je vais vous aider avec ce problème technique. Pouvez-vous me donner plus de détails sur l'erreur que vous rencontrez ?",
        "compte": "Pour les questions relatives à votre compte, je peux vous aider à vérifier votre solde, modifier vos informations ou réinitialiser votre mot de passe.",
        "default": "Merci pour votre message. Je suis là pour vous aider. Pouvez-vous me donner plus de détails ?"
    }
    if category:
        return responses.get(category, responses["default"])
    return responses["default"]

def main():
    st.set_page_config(page_title="Support Client | IAFactory", page_icon="🎧", layout="wide")

    if 'language' not in st.session_state:
        st.session_state.language = 'fr'
    if 'messages' not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": t('welcome')}]
    if 'category' not in st.session_state:
        st.session_state.category = None

    inject_css()

    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f'<div class="iaf-header"><span style="font-size:2rem">🎧</span><span class="iaf-title">{t("title")}</span></div>', unsafe_allow_html=True)
        st.markdown(f"*{t('subtitle')}*")
    with col2:
        lang = st.selectbox("", ['fr', 'en', 'ar'], format_func=lambda x: {'fr': '🇫🇷 FR', 'en': '🇬🇧 EN', 'ar': '🇩🇿 AR'}[x],
                           index=['fr', 'en', 'ar'].index(st.session_state.language), label_visibility="collapsed")
        if lang != st.session_state.language:
            st.session_state.language = lang
            st.rerun()

    # Sidebar categories
    with st.sidebar:
        st.markdown(f"### {t('categories')}")
        categories = [('billing', t('cat_billing'), '💳'), ('technical', t('cat_technical'), '🔧'),
                     ('account', t('cat_account'), '👤'), ('general', t('cat_general'), '💬')]
        for cat_id, cat_name, icon in categories:
            if st.button(f"{icon} {cat_name}", key=cat_id, use_container_width=True):
                st.session_state.category = cat_id

        st.markdown("---")
        if st.button(f"🔄 {t('new_chat')}", use_container_width=True):
            st.session_state.messages = [{"role": "assistant", "content": t('welcome')}]
            st.rerun()

    # Chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input
    if prompt := st.chat_input(t('input_placeholder')):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner(t('processing')):
                response = get_ai_response(prompt, st.session_state.category)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

if __name__ == "__main__":
    main()
