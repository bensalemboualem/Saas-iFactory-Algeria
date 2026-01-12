"""
Teaching Assistant - Interface Streamlit
Assistant pédagogique IA pour enseignants
"""
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TRANSLATIONS = {
    "fr": {
        "title": "Teaching Assistant",
        "subtitle": "Assistant Pédagogique IA",
        "welcome": "Bienvenue ! Je suis votre assistant pédagogique. Comment puis-je vous aider à préparer vos cours ?",
        "input_placeholder": "Décrivez votre besoin pédagogique...",
        "tools": "Outils",
        "lesson_plan": "Plan de cours",
        "exercises": "Exercices",
        "evaluation": "Évaluation",
        "correction": "Correction auto",
        "new_chat": "Nouvelle session",
        "processing": "Génération en cours...",
        "subject": "Matière",
        "level": "Niveau",
        "duration": "Durée (min)",
        "primary": "Primaire",
        "middle": "Moyen",
        "secondary": "Secondaire",
        "university": "Universitaire"
    },
    "en": {
        "title": "Teaching Assistant",
        "subtitle": "AI Teaching Assistant",
        "welcome": "Welcome! I'm your teaching assistant. How can I help you prepare your lessons?",
        "input_placeholder": "Describe your teaching need...",
        "tools": "Tools",
        "lesson_plan": "Lesson plan",
        "exercises": "Exercises",
        "evaluation": "Evaluation",
        "correction": "Auto correction",
        "new_chat": "New session",
        "processing": "Generating...",
        "subject": "Subject",
        "level": "Level",
        "duration": "Duration (min)",
        "primary": "Primary",
        "middle": "Middle school",
        "secondary": "High school",
        "university": "University"
    },
    "ar": {
        "title": "المساعد التعليمي",
        "subtitle": "مساعد تعليمي بالذكاء الاصطناعي",
        "welcome": "مرحبًا! أنا مساعدك التعليمي. كيف يمكنني مساعدتك في تحضير دروسك؟",
        "input_placeholder": "صف احتياجك التعليمي...",
        "tools": "الأدوات",
        "lesson_plan": "خطة الدرس",
        "exercises": "التمارين",
        "evaluation": "التقييم",
        "correction": "تصحيح آلي",
        "new_chat": "جلسة جديدة",
        "processing": "جاري التوليد...",
        "subject": "المادة",
        "level": "المستوى",
        "duration": "المدة (دقيقة)",
        "primary": "ابتدائي",
        "middle": "متوسط",
        "secondary": "ثانوي",
        "university": "جامعي"
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
        .lesson-card { background: rgba(0,166,81,0.05); padding: 1rem; border-radius: 12px;
            border: 1px solid rgba(0,166,81,0.2); margin: 0.5rem 0; }
        .iaf-header { display: flex; align-items: center; gap: 12px;
            padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.12); }
        .iaf-title { font-size: 1.8rem; font-weight: 700;
            background: linear-gradient(135deg, #00a651, #00d66a);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    </style>
    """, unsafe_allow_html=True)

def get_teaching_response(query, tool=None):
    if tool == "lesson_plan" or "cours" in query.lower():
        return """📚 **Plan de Cours - Mathématiques 3ème AM**

**Thème:** Les équations du premier degré
**Durée:** 60 minutes
**Objectifs:** Résoudre une équation simple

---

**1. Introduction (10 min)**
- Rappel: qu'est-ce qu'une équation ?
- Exemples de la vie quotidienne

**2. Leçon (20 min)**
- Définition formelle
- Propriétés fondamentales
- Méthode de résolution pas à pas

**3. Exercices guidés (15 min)**
- 3 exercices au tableau
- Participation des élèves

**4. Exercices autonomes (10 min)**
- Feuille d'exercices individuels

**5. Conclusion (5 min)**
- Récapitulatif
- Devoirs pour la prochaine séance

📝 **Ressources:** Manuel p.45-48, Exercices supplémentaires"""

    elif tool == "exercises" or "exercice" in query.lower():
        return """✏️ **Fiche d'exercices - Équations 1er degré**

**Niveau:** 3ème AM | **Durée:** 30 min

---

**Exercice 1** ⭐
Résoudre: 2x + 5 = 13

**Exercice 2** ⭐
Résoudre: 3x - 7 = 2x + 4

**Exercice 3** ⭐⭐
Résoudre: 4(x + 2) = 3x + 10

**Exercice 4** ⭐⭐
Un nombre augmenté de 5 égale le double de ce nombre diminué de 3. Quel est ce nombre?

**Exercice 5** ⭐⭐⭐
Problème: Ahmed a 3 fois l'âge de son fils. Dans 10 ans, il aura le double. Quels sont leurs âges?

---
**Corrigé disponible sur demande**"""

    return "Je peux créer des plans de cours, générer des exercices, préparer des évaluations ou corriger des copies. Précisez votre besoin !"

def main():
    st.set_page_config(page_title="Teaching Assistant | IAFactory", page_icon="📚", layout="wide")

    if 'language' not in st.session_state:
        st.session_state.language = 'fr'
    if 'messages' not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": t('welcome')}]

    inject_css()

    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f'<div class="iaf-header"><span style="font-size:2rem">📚</span><span class="iaf-title">{t("title")}</span></div>', unsafe_allow_html=True)
        st.markdown(f"*{t('subtitle')}*")
    with col2:
        lang = st.selectbox("", ['fr', 'en', 'ar'], format_func=lambda x: {'fr': '🇫🇷 FR', 'en': '🇬🇧 EN', 'ar': '🇩🇿 AR'}[x],
                           index=['fr', 'en', 'ar'].index(st.session_state.language), label_visibility="collapsed")
        if lang != st.session_state.language:
            st.session_state.language = lang
            st.rerun()

    # Sidebar
    with st.sidebar:
        st.markdown(f"### {t('subject')}")
        subject = st.selectbox("", ["Mathématiques", "Physique", "Français", "Arabe", "Anglais", "Sciences", "Histoire-Géo"], label_visibility="collapsed")

        st.markdown(f"### {t('level')}")
        level = st.radio("", [t('primary'), t('middle'), t('secondary'), t('university')], label_visibility="collapsed")

        st.markdown(f"### {t('duration')}")
        duration = st.slider("", 15, 120, 60, 15, label_visibility="collapsed")

        st.markdown("---")
        st.markdown(f"### {t('tools')}")
        tools = [('lesson_plan', t('lesson_plan'), '📋'), ('exercises', t('exercises'), '✏️'),
                ('evaluation', t('evaluation'), '📝'), ('correction', t('correction'), '✅')]
        for t_id, t_name, icon in tools:
            if st.button(f"{icon} {t_name}", key=t_id, use_container_width=True):
                response = get_teaching_response("", t_id)
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
                response = get_teaching_response(prompt)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

if __name__ == "__main__":
    main()
