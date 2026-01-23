"""
Recruitment Agent - Interface Streamlit
Agent de recrutement IA pour sourcing et matching
"""
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TRANSLATIONS = {
    "fr": {
        "title": "Recruitment Agent",
        "subtitle": "Sourcing & Matching de Talents",
        "welcome": "Bienvenue ! Je suis votre assistant de recrutement IA. Comment puis-je vous aider ?",
        "input_placeholder": "Décrivez le profil recherché...",
        "services": "Services",
        "sourcing": "Sourcing CV",
        "matching": "Matching IA",
        "screening": "Pré-screening",
        "interview": "Questions entretien",
        "new_chat": "Nouvelle recherche",
        "processing": "Analyse des profils...",
        "job_title": "Poste recherché",
        "experience": "Expérience requise",
        "skills": "Compétences clés",
        "location": "Localisation",
        "junior": "Junior (0-2 ans)",
        "mid": "Confirmé (2-5 ans)",
        "senior": "Senior (5+ ans)"
    },
    "en": {
        "title": "Recruitment Agent",
        "subtitle": "Talent Sourcing & Matching",
        "welcome": "Welcome! I'm your AI recruitment assistant. How can I help you?",
        "input_placeholder": "Describe the profile you're looking for...",
        "services": "Services",
        "sourcing": "CV Sourcing",
        "matching": "AI Matching",
        "screening": "Pre-screening",
        "interview": "Interview questions",
        "new_chat": "New search",
        "processing": "Analyzing profiles...",
        "job_title": "Job title",
        "experience": "Required experience",
        "skills": "Key skills",
        "location": "Location",
        "junior": "Junior (0-2 years)",
        "mid": "Mid-level (2-5 years)",
        "senior": "Senior (5+ years)"
    },
    "ar": {
        "title": "وكيل التوظيف",
        "subtitle": "البحث عن المواهب ومطابقتها",
        "welcome": "مرحبًا! أنا مساعدك في التوظيف. كيف يمكنني مساعدتك؟",
        "input_placeholder": "صف الملف الشخصي المطلوب...",
        "services": "الخدمات",
        "sourcing": "البحث عن CV",
        "matching": "مطابقة IA",
        "screening": "الفرز المسبق",
        "interview": "أسئلة المقابلة",
        "new_chat": "بحث جديد",
        "processing": "تحليل الملفات...",
        "job_title": "الوظيفة المطلوبة",
        "experience": "الخبرة المطلوبة",
        "skills": "المهارات الأساسية",
        "location": "الموقع",
        "junior": "مبتدئ (0-2 سنة)",
        "mid": "متمرس (2-5 سنوات)",
        "senior": "كبير (5+ سنوات)"
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
        .candidate-card { background: rgba(0,166,81,0.05); padding: 1rem; border-radius: 12px;
            border: 1px solid rgba(0,166,81,0.2); margin: 0.5rem 0; }
        .match-score { font-size: 1.2rem; font-weight: 700; color: #00a651; }
        .iaf-header { display: flex; align-items: center; gap: 12px;
            padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.12); }
        .iaf-title { font-size: 1.8rem; font-weight: 700;
            background: linear-gradient(135deg, #00a651, #00d66a);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    </style>
    """, unsafe_allow_html=True)

def get_recruitment_response(query, job_title=None):
    if "sourcing" in query.lower() or "candidat" in query.lower():
        return """🔍 **Résultats Sourcing - Développeur Full Stack**

**1. Ahmed B. - Match 95%**
- 4 ans d'expérience React/Node.js
- Alger | Disponible immédiatement
- Prétention: 120 000 DZD/mois
- ✅ Portfolio solide

**2. Yasmine K. - Match 88%**
- 3 ans d'expérience Vue.js/Python
- Oran | Préavis 1 mois
- Prétention: 100 000 DZD/mois
- ✅ Certifications AWS

**3. Mohamed L. - Match 82%**
- 5 ans d'expérience PHP/Laravel
- Constantine | Disponible
- Prétention: 90 000 DZD/mois
- ⚠️ En reconversion vers React

Voulez-vous voir les CV détaillés ?"""

    elif "interview" in query.lower() or "entretien" in query.lower():
        return """📝 **Questions d'entretien suggérées - Dev Full Stack**

**Technique:**
1. Décrivez l'architecture d'un projet React récent
2. Comment gérez-vous l'état dans une application complexe ?
3. Expliquez le concept de CI/CD

**Comportemental (STAR):**
4. Racontez un conflit technique avec un collègue
5. Décrivez un projet livré sous pression
6. Comment gérez-vous les priorités multiples ?

**Culture fit:**
7. Pourquoi l'Algérie et pas l'étranger ?
8. Comment vous formez-vous aux nouvelles technologies ?"""

    return "Je peux vous aider à sourcer des candidats, créer des questions d'entretien, ou évaluer des profils. Précisez votre besoin !"

def main():
    st.set_page_config(page_title="Recruitment | IAFactory", page_icon="👥", layout="wide")

    if 'language' not in st.session_state:
        st.session_state.language = 'fr'
    if 'messages' not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": t('welcome')}]

    inject_css()

    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f'<div class="iaf-header"><span style="font-size:2rem">👥</span><span class="iaf-title">{t("title")}</span></div>', unsafe_allow_html=True)
        st.markdown(f"*{t('subtitle')}*")
    with col2:
        lang = st.selectbox("", ['fr', 'en', 'ar'], format_func=lambda x: {'fr': '🇫🇷 FR', 'en': '🇬🇧 EN', 'ar': '🇩🇿 AR'}[x],
                           index=['fr', 'en', 'ar'].index(st.session_state.language), label_visibility="collapsed")
        if lang != st.session_state.language:
            st.session_state.language = lang
            st.rerun()

    # Sidebar
    with st.sidebar:
        st.markdown(f"### {t('job_title')}")
        job = st.text_input("", placeholder="Ex: Développeur Full Stack", label_visibility="collapsed")

        st.markdown(f"### {t('experience')}")
        exp = st.radio("", [t('junior'), t('mid'), t('senior')], label_visibility="collapsed")

        st.markdown(f"### {t('skills')}")
        skills = st.text_input("", placeholder="React, Node.js, Python...", label_visibility="collapsed", key="skills")

        st.markdown(f"### {t('location')}")
        location = st.selectbox("", ["Toute l'Algérie", "Alger", "Oran", "Constantine", "Remote"], label_visibility="collapsed")

        st.markdown("---")
        st.markdown(f"### {t('services')}")
        services = [('sourcing', t('sourcing'), '🔍'), ('matching', t('matching'), '🎯'),
                   ('screening', t('screening'), '📋'), ('interview', t('interview'), '💬')]
        for s_id, s_name, icon in services:
            if st.button(f"{icon} {s_name}", key=s_id, use_container_width=True):
                response = get_recruitment_response(s_id)
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
                response = get_recruitment_response(prompt)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

if __name__ == "__main__":
    main()
