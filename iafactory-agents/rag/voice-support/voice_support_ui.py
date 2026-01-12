"""
Voice Support Agent - Interface Streamlit
Agent vocal intelligent avec STT/TTS multilingue
"""
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TRANSLATIONS = {
    "fr": {
        "title": "Voice Support Agent",
        "subtitle": "Support Vocal Intelligent - STT/TTS",
        "welcome": "Bienvenue ! Cliquez sur le micro pour parler ou tapez votre message.",
        "input_placeholder": "Tapez ou utilisez le micro...",
        "record": "Enregistrer",
        "stop": "Arrêter",
        "play": "Écouter la réponse",
        "new_chat": "Nouvelle conversation",
        "processing": "Traitement vocal...",
        "languages": "Langues vocales",
        "french": "Français",
        "arabic": "Arabe / Darija",
        "english": "Anglais",
        "voice_settings": "Paramètres voix",
        "speed": "Vitesse",
        "pitch": "Tonalité"
    },
    "en": {
        "title": "Voice Support Agent",
        "subtitle": "Intelligent Voice Support - STT/TTS",
        "welcome": "Welcome! Click the microphone to speak or type your message.",
        "input_placeholder": "Type or use the microphone...",
        "record": "Record",
        "stop": "Stop",
        "play": "Play response",
        "new_chat": "New conversation",
        "processing": "Voice processing...",
        "languages": "Voice languages",
        "french": "French",
        "arabic": "Arabic / Darija",
        "english": "English",
        "voice_settings": "Voice settings",
        "speed": "Speed",
        "pitch": "Pitch"
    },
    "ar": {
        "title": "وكيل الدعم الصوتي",
        "subtitle": "دعم صوتي ذكي - STT/TTS",
        "welcome": "مرحبًا! انقر على الميكروفون للتحدث أو اكتب رسالتك.",
        "input_placeholder": "اكتب أو استخدم الميكروفون...",
        "record": "تسجيل",
        "stop": "إيقاف",
        "play": "تشغيل الرد",
        "new_chat": "محادثة جديدة",
        "processing": "معالجة صوتية...",
        "languages": "اللغات الصوتية",
        "french": "فرنسية",
        "arabic": "عربية / دارجة",
        "english": "إنجليزية",
        "voice_settings": "إعدادات الصوت",
        "speed": "السرعة",
        "pitch": "النبرة"
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
        .mic-btn { width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, #00a651, #00d66a);
            display: flex; align-items: center; justify-content: center; cursor: pointer;
            box-shadow: 0 4px 20px rgba(0,166,81,0.3); transition: all 0.3s; margin: 2rem auto; }
        .mic-btn:hover { transform: scale(1.1); box-shadow: 0 8px 30px rgba(0,166,81,0.5); }
        .iaf-header { display: flex; align-items: center; gap: 12px;
            padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.12); }
        .iaf-title { font-size: 1.8rem; font-weight: 700;
            background: linear-gradient(135deg, #00a651, #00d66a);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .voice-wave { text-align: center; padding: 2rem; }
    </style>
    """, unsafe_allow_html=True)

def get_voice_response(text):
    """Simulate voice agent response"""
    return f"J'ai bien compris votre demande: '{text}'. Je suis là pour vous aider avec le support vocal. Cette fonctionnalité utilise la reconnaissance vocale et la synthèse vocale pour une expérience naturelle."

def main():
    st.set_page_config(page_title="Voice Support | IAFactory", page_icon="🎙️", layout="wide")

    if 'language' not in st.session_state:
        st.session_state.language = 'fr'
    if 'messages' not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": t('welcome')}]
    if 'recording' not in st.session_state:
        st.session_state.recording = False

    inject_css()

    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f'<div class="iaf-header"><span style="font-size:2rem">🎙️</span><span class="iaf-title">{t("title")}</span></div>', unsafe_allow_html=True)
        st.markdown(f"*{t('subtitle')}*")
    with col2:
        lang = st.selectbox("", ['fr', 'en', 'ar'], format_func=lambda x: {'fr': '🇫🇷 FR', 'en': '🇬🇧 EN', 'ar': '🇩🇿 AR'}[x],
                           index=['fr', 'en', 'ar'].index(st.session_state.language), label_visibility="collapsed")
        if lang != st.session_state.language:
            st.session_state.language = lang
            st.rerun()

    # Sidebar
    with st.sidebar:
        st.markdown(f"### {t('languages')}")
        voice_lang = st.radio("", [t('french'), t('arabic'), t('english')], label_visibility="collapsed")

        st.markdown("---")
        st.markdown(f"### {t('voice_settings')}")
        speed = st.slider(t('speed'), 0.5, 2.0, 1.0, 0.1)
        pitch = st.slider(t('pitch'), 0.5, 2.0, 1.0, 0.1)

        st.markdown("---")
        if st.button(f"🔄 {t('new_chat')}", use_container_width=True):
            st.session_state.messages = [{"role": "assistant", "content": t('welcome')}]
            st.rerun()

    # Mic button
    st.markdown('<div class="voice-wave">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎤 " + (t('stop') if st.session_state.recording else t('record')), use_container_width=True):
            st.session_state.recording = not st.session_state.recording
            if not st.session_state.recording:
                st.info("Transcription: 'Bonjour, j'ai besoin d'aide'")
    st.markdown('</div>', unsafe_allow_html=True)

    # Chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and len(st.session_state.messages) > 1:
                st.button(f"🔊 {t('play')}", key=f"play_{len(st.session_state.messages)}")

    if prompt := st.chat_input(t('input_placeholder')):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner(t('processing')):
                response = get_voice_response(prompt)
                st.markdown(response)
                st.button(f"🔊 {t('play')}", key="play_last")
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

if __name__ == "__main__":
    main()
