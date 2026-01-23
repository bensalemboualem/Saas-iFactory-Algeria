"""
Real Estate Agent - Interface Streamlit
Agent immobilier IA pour le marché algérien
"""
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TRANSLATIONS = {
    "fr": {
        "title": "Agent Immobilier IA",
        "subtitle": "Recherche & Estimation - Marché Algérien",
        "welcome": "Bienvenue ! Je suis votre agent immobilier IA. Comment puis-je vous aider dans votre projet immobilier ?",
        "input_placeholder": "Décrivez votre recherche immobilière...",
        "services": "Services",
        "search": "Recherche bien",
        "estimate": "Estimation prix",
        "compare": "Comparatif",
        "advice": "Conseils achat",
        "new_chat": "Nouvelle recherche",
        "processing": "Analyse du marché...",
        "cities": "Villes",
        "property_type": "Type de bien",
        "apartment": "Appartement",
        "house": "Maison/Villa",
        "land": "Terrain",
        "commercial": "Local commercial",
        "budget": "Budget (DZD)"
    },
    "en": {
        "title": "AI Real Estate Agent",
        "subtitle": "Search & Estimation - Algerian Market",
        "welcome": "Welcome! I'm your AI real estate agent. How can I help with your property project?",
        "input_placeholder": "Describe your property search...",
        "services": "Services",
        "search": "Property search",
        "estimate": "Price estimation",
        "compare": "Comparison",
        "advice": "Buying advice",
        "new_chat": "New search",
        "processing": "Market analysis...",
        "cities": "Cities",
        "property_type": "Property type",
        "apartment": "Apartment",
        "house": "House/Villa",
        "land": "Land",
        "commercial": "Commercial",
        "budget": "Budget (DZD)"
    },
    "ar": {
        "title": "وكيل العقارات بالذكاء الاصطناعي",
        "subtitle": "بحث وتقدير - السوق الجزائرية",
        "welcome": "مرحبًا! أنا وكيلك العقاري. كيف يمكنني مساعدتك في مشروعك العقاري؟",
        "input_placeholder": "صف بحثك العقاري...",
        "services": "الخدمات",
        "search": "البحث عن عقار",
        "estimate": "تقدير السعر",
        "compare": "مقارنة",
        "advice": "نصائح الشراء",
        "new_chat": "بحث جديد",
        "processing": "تحليل السوق...",
        "cities": "المدن",
        "property_type": "نوع العقار",
        "apartment": "شقة",
        "house": "منزل/فيلا",
        "land": "أرض",
        "commercial": "تجاري",
        "budget": "الميزانية (DZD)"
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
        .property-card { background: rgba(0,166,81,0.05); padding: 1rem; border-radius: 12px;
            border: 1px solid rgba(0,166,81,0.2); margin: 0.5rem 0; }
        .price-tag { font-size: 1.5rem; font-weight: 700; color: #00a651; }
        .iaf-header { display: flex; align-items: center; gap: 12px;
            padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.12); }
        .iaf-title { font-size: 1.8rem; font-weight: 700;
            background: linear-gradient(135deg, #00a651, #00d66a);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    </style>
    """, unsafe_allow_html=True)

def get_real_estate_response(query, city=None, prop_type=None):
    if "estimation" in query.lower() or "prix" in query.lower():
        return """🏠 **Estimation Immobilière - Alger Centre**

Basé sur les données du marché actuel:

| Type | Prix/m² moyen | Tendance |
|------|---------------|----------|
| Appartement F3 | 350 000 DZD | 📈 +5% |
| Appartement F4 | 320 000 DZD | 📊 Stable |
| Villa | 280 000 DZD | 📈 +3% |

**Facteurs de valorisation:**
- Proximité transports: +15%
- Étage élevé avec vue: +10%
- Parking: +8%
- État neuf/rénové: +20%

📍 Prix moyen F3 (80m²): **28 000 000 DZD**"""

    elif "recherche" in query.lower() or "cherche" in query.lower():
        return """🔍 **Résultats de recherche - Alger**

**1. Appartement F3 - Hydra**
- Surface: 85 m²
- Prix: 32 000 000 DZD
- ✅ Parking, Ascenseur

**2. Appartement F3 - El Biar**
- Surface: 78 m²
- Prix: 28 500 000 DZD
- ✅ Rénové, Vue mer

**3. Appartement F4 - Bab Ezzouar**
- Surface: 110 m²
- Prix: 25 000 000 DZD
- ✅ Proche métro

Voulez-vous plus de détails sur l'un de ces biens ?"""

    return "Je peux vous aider à rechercher un bien, estimer un prix, ou vous conseiller sur le marché immobilier algérien. Précisez votre besoin !"

def main():
    st.set_page_config(page_title="Real Estate | IAFactory", page_icon="🏠", layout="wide")

    if 'language' not in st.session_state:
        st.session_state.language = 'fr'
    if 'messages' not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": t('welcome')}]

    inject_css()

    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f'<div class="iaf-header"><span style="font-size:2rem">🏠</span><span class="iaf-title">{t("title")}</span></div>', unsafe_allow_html=True)
        st.markdown(f"*{t('subtitle')}*")
    with col2:
        lang = st.selectbox("", ['fr', 'en', 'ar'], format_func=lambda x: {'fr': '🇫🇷 FR', 'en': '🇬🇧 EN', 'ar': '🇩🇿 AR'}[x],
                           index=['fr', 'en', 'ar'].index(st.session_state.language), label_visibility="collapsed")
        if lang != st.session_state.language:
            st.session_state.language = lang
            st.rerun()

    # Sidebar
    with st.sidebar:
        st.markdown(f"### {t('cities')}")
        city = st.selectbox("", ["Alger", "Oran", "Constantine", "Annaba", "Sétif", "Blida"], label_visibility="collapsed")

        st.markdown(f"### {t('property_type')}")
        prop_type = st.radio("", [t('apartment'), t('house'), t('land'), t('commercial')], label_visibility="collapsed")

        st.markdown(f"### {t('budget')}")
        budget = st.slider("", 5000000, 100000000, (15000000, 40000000), format="%d DZD", label_visibility="collapsed")

        st.markdown("---")
        st.markdown(f"### {t('services')}")
        services = [('search', t('search'), '🔍'), ('estimate', t('estimate'), '💰'),
                   ('compare', t('compare'), '📊'), ('advice', t('advice'), '💡')]
        for s_id, s_name, icon in services:
            if st.button(f"{icon} {s_name}", key=s_id, use_container_width=True):
                response = get_real_estate_response(s_id)
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
                response = get_real_estate_response(prompt)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

if __name__ == "__main__":
    main()
