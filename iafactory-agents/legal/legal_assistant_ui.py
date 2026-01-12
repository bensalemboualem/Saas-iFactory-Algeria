"""
Legal Assistant DZ - Interface Streamlit
Assistant juridique spécialisé droit algérien
"""
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TRANSLATIONS = {
    "fr": {
        "title": "Assistant Juridique DZ",
        "subtitle": "Droit Algérien & Conseils Légaux",
        "welcome": "Bienvenue ! Je suis votre assistant juridique spécialisé dans le droit algérien. Comment puis-je vous aider ?",
        "input_placeholder": "Posez votre question juridique...",
        "domains": "Domaines",
        "commercial": "Droit Commercial",
        "fiscal": "Droit Fiscal",
        "travail": "Droit du Travail",
        "immobilier": "Droit Immobilier",
        "famille": "Droit de la Famille",
        "cnrc": "CNRC & Création",
        "new_chat": "Nouvelle consultation",
        "processing": "Analyse juridique...",
        "disclaimer": "⚠️ Ces informations sont fournies à titre indicatif et ne constituent pas un avis juridique officiel."
    },
    "en": {
        "title": "Legal Assistant DZ",
        "subtitle": "Algerian Law & Legal Advice",
        "welcome": "Welcome! I'm your legal assistant specialized in Algerian law. How can I help you?",
        "input_placeholder": "Ask your legal question...",
        "domains": "Domains",
        "commercial": "Commercial Law",
        "fiscal": "Tax Law",
        "travail": "Labor Law",
        "immobilier": "Real Estate Law",
        "famille": "Family Law",
        "cnrc": "CNRC & Registration",
        "new_chat": "New consultation",
        "processing": "Legal analysis...",
        "disclaimer": "⚠️ This information is for guidance only and does not constitute official legal advice."
    },
    "ar": {
        "title": "المساعد القانوني DZ",
        "subtitle": "القانون الجزائري والاستشارات القانونية",
        "welcome": "مرحبًا! أنا مساعدك القانوني المتخصص في القانون الجزائري. كيف يمكنني مساعدتك؟",
        "input_placeholder": "اطرح سؤالك القانوني...",
        "domains": "المجالات",
        "commercial": "القانون التجاري",
        "fiscal": "قانون الضرائب",
        "travail": "قانون العمل",
        "immobilier": "قانون العقارات",
        "famille": "قانون الأسرة",
        "cnrc": "CNRC والتسجيل",
        "new_chat": "استشارة جديدة",
        "processing": "التحليل القانوني...",
        "disclaimer": "⚠️ هذه المعلومات للإرشاد فقط ولا تشكل استشارة قانونية رسمية."
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
        .disclaimer { background: #fff3cd; padding: 1rem; border-radius: 8px;
            border-left: 4px solid #ffc107; color: #856404; margin: 1rem 0; }
        .iaf-header { display: flex; align-items: center; gap: 12px;
            padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.12); }
        .iaf-title { font-size: 1.8rem; font-weight: 700;
            background: linear-gradient(135deg, #00a651, #00d66a);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    </style>
    """, unsafe_allow_html=True)

def get_legal_response(question, domain=None):
    responses = {
        "commercial": """⚖️ **Droit Commercial Algérien**

**Création d'entreprise (SARL):**
- Capital minimum: 100 000 DZD
- Associés: 2 à 50 personnes
- Documents: Statuts, CNI, Casier judiciaire

**Procédure CNRC:**
1. Réservation de nom commercial
2. Rédaction des statuts notariés
3. Ouverture compte bancaire bloqué
4. Dépôt dossier CNRC
5. Obtention RC (3-5 jours)

📍 Délai moyen: 2-3 semaines""",
        "fiscal": """🏛️ **Fiscalité Algérienne**

**Impôts principaux entreprises:**
- **IBS** (Impôt sur Bénéfices Sociétés): 19-26%
- **TAP** (Taxe sur Activité Pro): 1-2%
- **TVA**: 9% ou 19%
- **IRG** (Revenus): Barème progressif

**Avantages fiscaux:**
- ANDI pour investissements
- Zones franches
- Startups labellisées""",
        "travail": """👷 **Droit du Travail Algérien**

**Contrat de travail:**
- CDI/CDD obligatoirement écrit
- Période d'essai: 6 mois max
- Préavis: 1-3 mois selon ancienneté

**SMIG 2024:** 20 000 DZD
**Durée légale:** 40h/semaine
**Congés:** 2.5 jours/mois travaillé

**Licenciement:**
- Motif légitime obligatoire
- Indemnité: 15 jours/année d'ancienneté""",
        "default": "Je peux vous aider avec vos questions sur le droit algérien. Précisez votre domaine: commercial, fiscal, travail, immobilier ou famille."
    }
    return responses.get(domain, responses["default"])

def main():
    st.set_page_config(page_title="Legal Assistant | IAFactory", page_icon="⚖️", layout="wide")

    if 'language' not in st.session_state:
        st.session_state.language = 'fr'
    if 'messages' not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": t('welcome')}]
    if 'domain' not in st.session_state:
        st.session_state.domain = None

    inject_css()

    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f'<div class="iaf-header"><span style="font-size:2rem">⚖️</span><span class="iaf-title">{t("title")}</span></div>', unsafe_allow_html=True)
        st.markdown(f"*{t('subtitle')}*")
    with col2:
        lang = st.selectbox("", ['fr', 'en', 'ar'], format_func=lambda x: {'fr': '🇫🇷 FR', 'en': '🇬🇧 EN', 'ar': '🇩🇿 AR'}[x],
                           index=['fr', 'en', 'ar'].index(st.session_state.language), label_visibility="collapsed")
        if lang != st.session_state.language:
            st.session_state.language = lang
            st.rerun()

    # Sidebar
    with st.sidebar:
        st.markdown(f"### {t('domains')}")
        domains = [('commercial', t('commercial'), '🏢'), ('fiscal', t('fiscal'), '🏛️'),
                  ('travail', t('travail'), '👷'), ('immobilier', t('immobilier'), '🏠'),
                  ('famille', t('famille'), '👨‍👩‍👧'), ('cnrc', t('cnrc'), '📋')]
        for dom_id, dom_name, icon in domains:
            if st.button(f"{icon} {dom_name}", key=dom_id, use_container_width=True):
                st.session_state.domain = dom_id
                response = get_legal_response("", dom_id)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

        st.markdown("---")
        if st.button(f"🔄 {t('new_chat')}", use_container_width=True):
            st.session_state.messages = [{"role": "assistant", "content": t('welcome')}]
            st.rerun()

    # Disclaimer
    st.markdown(f'<div class="disclaimer">{t("disclaimer")}</div>', unsafe_allow_html=True)

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
                response = get_legal_response(prompt, st.session_state.domain)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

if __name__ == "__main__":
    main()
