"""
Video Operator - Interface Streamlit
Agent pour création et montage vidéo automatisé
"""
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TRANSLATIONS = {
    "fr": {
        "title": "Video Operator",
        "subtitle": "Création & Montage Vidéo IA",
        "welcome": "Bienvenue ! Je peux créer des vidéos, générer des voix-off et ajouter des sous-titres automatiquement.",
        "input_placeholder": "Décrivez la vidéo à créer...",
        "tools": "Outils",
        "create_video": "Créer vidéo",
        "tts": "Voix-off TTS",
        "subtitles": "Sous-titres",
        "edit": "Montage",
        "new_project": "Nouveau projet",
        "processing": "Génération en cours...",
        "format": "Format",
        "duration": "Durée (sec)",
        "voice": "Voix",
        "style": "Style"
    },
    "en": {
        "title": "Video Operator",
        "subtitle": "AI Video Creation & Editing",
        "welcome": "Welcome! I can create videos, generate voiceovers and add subtitles automatically.",
        "input_placeholder": "Describe the video to create...",
        "tools": "Tools",
        "create_video": "Create video",
        "tts": "TTS Voiceover",
        "subtitles": "Subtitles",
        "edit": "Editing",
        "new_project": "New project",
        "processing": "Generating...",
        "format": "Format",
        "duration": "Duration (sec)",
        "voice": "Voice",
        "style": "Style"
    },
    "ar": {
        "title": "مشغل الفيديو",
        "subtitle": "إنشاء وتحرير الفيديو بالذكاء الاصطناعي",
        "welcome": "مرحبًا! يمكنني إنشاء مقاطع فيديو وإنشاء تعليقات صوتية وإضافة ترجمات تلقائيًا.",
        "input_placeholder": "صف الفيديو المراد إنشاؤه...",
        "tools": "الأدوات",
        "create_video": "إنشاء فيديو",
        "tts": "صوت TTS",
        "subtitles": "الترجمات",
        "edit": "التحرير",
        "new_project": "مشروع جديد",
        "processing": "جاري التوليد...",
        "format": "الصيغة",
        "duration": "المدة (ثانية)",
        "voice": "الصوت",
        "style": "النمط"
    }
}

def t(key):
    lang = st.session_state.get('language', 'fr')
    return TRANSLATIONS.get(lang, TRANSLATIONS['fr']).get(key, key)

def inject_css():
    st.markdown("""
    <style>
        .main .block-container { padding-top: 2rem; max-width: 1100px; }
        .stButton > button { background: linear-gradient(135deg, #00a651, #00d66a) !important;
            color: white !important; border: none !important; border-radius: 10px !important; }
        .video-preview { background: #1a1a24; padding: 2rem; border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.1); text-align: center; min-height: 300px;
            display: flex; align-items: center; justify-content: center; }
        .iaf-header { display: flex; align-items: center; gap: 12px;
            padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.12); }
        .iaf-title { font-size: 1.8rem; font-weight: 700;
            background: linear-gradient(135deg, #00a651, #00d66a);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    </style>
    """, unsafe_allow_html=True)

def get_video_response(query, tool=None):
    if tool == "create_video" or "vidéo" in query.lower():
        return """🎬 **Projet Vidéo Créé**

**Configuration:**
- Format: 1080x1920 (Vertical/Reels)
- Durée: 60 secondes
- Style: Corporate moderne

**Éléments générés:**
1. ✅ Script voix-off (150 mots)
2. ✅ 12 scènes avec transitions
3. ✅ Musique de fond sélectionnée
4. ✅ Sous-titres FR/AR

**Prochaines étapes:**
- [ ] Valider le script
- [ ] Choisir les visuels
- [ ] Lancer le rendu

⏱️ Temps estimé: 5 minutes"""

    elif tool == "tts":
        return """🎙️ **Voix-off TTS Générée**

**Paramètres:**
- Langue: Français (Algérie)
- Voix: Masculine naturelle
- Vitesse: 1.0x
- Durée: 45 secondes

**Script converti:**
> "Bienvenue chez IAFactory Algeria, votre partenaire en intelligence artificielle..."

🔊 [Écouter la prévisualisation]
📥 [Télécharger MP3]"""

    return "Je peux créer des vidéos, générer des voix-off, ou ajouter des sous-titres. Décrivez votre projet !"

def main():
    st.set_page_config(page_title="Video Operator | IAFactory", page_icon="🎬", layout="wide")

    if 'language' not in st.session_state:
        st.session_state.language = 'fr'
    if 'messages' not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": t('welcome')}]

    inject_css()

    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f'<div class="iaf-header"><span style="font-size:2rem">🎬</span><span class="iaf-title">{t("title")}</span></div>', unsafe_allow_html=True)
        st.markdown(f"*{t('subtitle')}*")
    with col2:
        lang = st.selectbox("", ['fr', 'en', 'ar'], format_func=lambda x: {'fr': '🇫🇷 FR', 'en': '🇬🇧 EN', 'ar': '🇩🇿 AR'}[x],
                           index=['fr', 'en', 'ar'].index(st.session_state.language), label_visibility="collapsed")
        if lang != st.session_state.language:
            st.session_state.language = lang
            st.rerun()

    # Sidebar
    with st.sidebar:
        st.markdown(f"### {t('format')}")
        format_opt = st.selectbox("", ["16:9 (YouTube)", "9:16 (Reels/TikTok)", "1:1 (Instagram)", "4:5 (Feed)"], label_visibility="collapsed")

        st.markdown(f"### {t('duration')}")
        duration = st.slider("", 15, 180, 60, 15, label_visibility="collapsed")

        st.markdown(f"### {t('voice')}")
        voice = st.selectbox("", ["Français - Homme", "Français - Femme", "Arabe - Homme", "Arabe - Femme", "Anglais"], label_visibility="collapsed")

        st.markdown(f"### {t('style')}")
        style = st.selectbox("", ["Corporate", "Dynamique", "Minimaliste", "Cinématique"], label_visibility="collapsed")

        st.markdown("---")
        st.markdown(f"### {t('tools')}")
        tools = [('create_video', t('create_video'), '🎥'), ('tts', t('tts'), '🎙️'),
                ('subtitles', t('subtitles'), '📝'), ('edit', t('edit'), '✂️')]
        for tool_id, tool_name, icon in tools:
            if st.button(f"{icon} {tool_name}", key=tool_id, use_container_width=True):
                response = get_video_response("", tool_id)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

        st.markdown("---")
        if st.button(f"🔄 {t('new_project')}", use_container_width=True):
            st.session_state.messages = [{"role": "assistant", "content": t('welcome')}]
            st.rerun()

    # Main content
    col1, col2 = st.columns([2, 1])
    with col1:
        # Chat
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
    with col2:
        st.markdown("### 📺 Prévisualisation")
        st.markdown('<div class="video-preview">🎬 Aperçu vidéo</div>', unsafe_allow_html=True)

    if prompt := st.chat_input(t('input_placeholder')):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner(t('processing')):
            response = get_video_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

if __name__ == "__main__":
    main()
