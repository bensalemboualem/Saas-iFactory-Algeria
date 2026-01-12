"""
Travel Agent - Interface Streamlit
Agent voyage IA pour planification et conseils
"""
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TRANSLATIONS = {
    "fr": {
        "title": "Travel Agent IA",
        "subtitle": "Planification & Conseils Voyage",
        "welcome": "Bienvenue ! Je suis votre agent de voyage IA. Où souhaitez-vous partir ?",
        "input_placeholder": "Décrivez votre voyage idéal...",
        "services": "Services",
        "itinerary": "Créer itinéraire",
        "destinations": "Destinations DZ",
        "budget": "Estimation budget",
        "tips": "Conseils voyage",
        "new_chat": "Nouvelle recherche",
        "processing": "Planification...",
        "departure": "Départ de",
        "destination_label": "Destination",
        "travel_date": "Date de voyage",
        "travelers": "Voyageurs",
        "budget_range": "Budget (DZD)"
    },
    "en": {
        "title": "AI Travel Agent",
        "subtitle": "Travel Planning & Advice",
        "welcome": "Welcome! I'm your AI travel agent. Where would you like to go?",
        "input_placeholder": "Describe your ideal trip...",
        "services": "Services",
        "itinerary": "Create itinerary",
        "destinations": "DZ Destinations",
        "budget": "Budget estimate",
        "tips": "Travel tips",
        "new_chat": "New search",
        "processing": "Planning...",
        "departure": "Departure from",
        "destination_label": "Destination",
        "travel_date": "Travel date",
        "travelers": "Travelers",
        "budget_range": "Budget (DZD)"
    },
    "ar": {
        "title": "وكيل السفر بالذكاء الاصطناعي",
        "subtitle": "تخطيط السفر والنصائح",
        "welcome": "مرحبًا! أنا وكيل سفرك. إلى أين تريد الذهاب؟",
        "input_placeholder": "صف رحلتك المثالية...",
        "services": "الخدمات",
        "itinerary": "إنشاء برنامج",
        "destinations": "وجهات DZ",
        "budget": "تقدير الميزانية",
        "tips": "نصائح السفر",
        "new_chat": "بحث جديد",
        "processing": "جاري التخطيط...",
        "departure": "المغادرة من",
        "destination_label": "الوجهة",
        "travel_date": "تاريخ السفر",
        "travelers": "المسافرون",
        "budget_range": "الميزانية (DZD)"
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
        .destination-card { background: rgba(0,166,81,0.05); padding: 1rem; border-radius: 12px;
            border: 1px solid rgba(0,166,81,0.2); margin: 0.5rem 0; }
        .iaf-header { display: flex; align-items: center; gap: 12px;
            padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.12); }
        .iaf-title { font-size: 1.8rem; font-weight: 700;
            background: linear-gradient(135deg, #00a651, #00d66a);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    </style>
    """, unsafe_allow_html=True)

def get_travel_response(query, service=None):
    if service == "itinerary" or "itinéraire" in query.lower():
        return """✈️ **Itinéraire Proposé - Sahara Algérien**

**Durée:** 5 jours / 4 nuits
**Meilleure période:** Octobre - Mars

---

**Jour 1: Alger → Ghardaïa**
- 🚗 Vol Alger-Ghardaïa (1h)
- 🏨 Hôtel El Djanoub
- 🌆 Visite de la vallée du M'Zab

**Jour 2: Ghardaïa**
- 🕌 Visite des 5 villes fortifiées
- 🛍️ Marché traditionnel
- 🍽️ Déjeuner chez l'habitant

**Jour 3: Ghardaïa → Timimoun**
- 🚗 Route panoramique (4h)
- 🏜️ Découverte des ksour
- 🌅 Coucher de soleil sur les dunes

**Jour 4: Timimoun**
- 🐪 Excursion chameau
- 🎭 Soirée traditionnelle
- ⭐ Nuit sous les étoiles

**Jour 5: Retour Alger**
- 🛫 Vol retour

💰 **Budget estimé:** 85 000 DZD/personne"""

    elif service == "destinations" or "destination" in query.lower():
        return """🌍 **Top Destinations en Algérie**

**🏜️ Le Sahara**
- Timimoun, Ghardaïa, Djanet, Tamanrasset
- Meilleure période: Oct-Mars
- Budget: 60 000 - 150 000 DZD

**🏔️ Montagne - Kabylie**
- Tikjda, Djurdjura, Villages kabyles
- Meilleure période: Été
- Budget: 25 000 - 50 000 DZD

**🏖️ Côte Méditerranéenne**
- Béjaïa, Jijel, Tipaza, Oran
- Meilleure période: Juin-Sept
- Budget: 30 000 - 80 000 DZD

**🏛️ Patrimoine Historique**
- Tipaza, Timgad, Djémila, Constantine
- Toute l'année
- Budget: 20 000 - 40 000 DZD"""

    return "Je peux vous aider à planifier votre voyage, découvrir des destinations en Algérie, ou estimer votre budget. Où souhaitez-vous aller ?"

def main():
    st.set_page_config(page_title="Travel Agent | IAFactory", page_icon="✈️", layout="wide")

    if 'language' not in st.session_state:
        st.session_state.language = 'fr'
    if 'messages' not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": t('welcome')}]

    inject_css()

    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f'<div class="iaf-header"><span style="font-size:2rem">✈️</span><span class="iaf-title">{t("title")}</span></div>', unsafe_allow_html=True)
        st.markdown(f"*{t('subtitle')}*")
    with col2:
        lang = st.selectbox("", ['fr', 'en', 'ar'], format_func=lambda x: {'fr': '🇫🇷 FR', 'en': '🇬🇧 EN', 'ar': '🇩🇿 AR'}[x],
                           index=['fr', 'en', 'ar'].index(st.session_state.language), label_visibility="collapsed")
        if lang != st.session_state.language:
            st.session_state.language = lang
            st.rerun()

    # Sidebar
    with st.sidebar:
        st.markdown(f"### {t('departure')}")
        departure = st.selectbox("", ["Alger", "Oran", "Constantine", "Annaba"], label_visibility="collapsed")

        st.markdown(f"### {t('destination_label')}")
        destination = st.selectbox("", ["Sahara", "Kabylie", "Côte", "Patrimoine", "International"], label_visibility="collapsed", key="dest")

        st.markdown(f"### {t('travelers')}")
        travelers = st.number_input("", 1, 10, 2, label_visibility="collapsed")

        st.markdown(f"### {t('budget_range')}")
        budget = st.slider("", 20000, 300000, (50000, 100000), format="%d DZD", label_visibility="collapsed")

        st.markdown("---")
        st.markdown(f"### {t('services')}")
        services = [('itinerary', t('itinerary'), '🗺️'), ('destinations', t('destinations'), '🌍'),
                   ('budget', t('budget'), '💰'), ('tips', t('tips'), '💡')]
        for s_id, s_name, icon in services:
            if st.button(f"{icon} {s_name}", key=s_id, use_container_width=True):
                response = get_travel_response("", s_id)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

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
                response = get_travel_response(prompt)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

if __name__ == "__main__":
    main()
