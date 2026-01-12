"""
===================================================================
SYSTÈME I18N POUR STREAMLIT - IAFactory Algeria
Traductions trilingues pour tous les agents IA
Français | English | العربية
===================================================================
"""

import streamlit as st
from typing import Dict, Any

# ========== TRADUCTIONS AGENTS IA ==========
TRANSLATIONS = {
    # Interface commune
    "common": {
        "title": {
            "fr": "Assistant IA",
            "en": "AI Assistant",
            "ar": "مساعد الذكاء الاصطناعي"
        },
        "subtitle": {
            "fr": "Propulsé par IAFactory Algeria",
            "en": "Powered by IAFactory Algeria",
            "ar": "مدعوم من IAFactory الجزائر"
        },
        "input_placeholder": {
            "fr": "Posez votre question en français, arabe ou anglais...",
            "en": "Ask your question in French, Arabic or English...",
            "ar": "اطرح سؤالك بالفرنسية أو العربية أو الإنجليزية..."
        },
        "send": {
            "fr": "Envoyer",
            "en": "Send",
            "ar": "إرسال"
        },
        "clear": {
            "fr": "Effacer",
            "en": "Clear",
            "ar": "مسح"
        },
        "thinking": {
            "fr": "Réflexion en cours...",
            "en": "Thinking...",
            "ar": "جاري التفكير..."
        },
        "error": {
            "fr": "Une erreur est survenue",
            "en": "An error occurred",
            "ar": "حدث خطأ"
        },
        "settings": {
            "fr": "Paramètres",
            "en": "Settings",
            "ar": "الإعدادات"
        },
        "about": {
            "fr": "À propos",
            "en": "About",
            "ar": "حول"
        },
        "new_chat": {
            "fr": "Nouvelle conversation",
            "en": "New Chat",
            "ar": "محادثة جديدة"
        }
    },

    # AI Consultant
    "consultant": {
        "title": {
            "fr": "Consultant IA Business",
            "en": "AI Business Consultant",
            "ar": "مستشار الأعمال بالذكاء الاصطناعي"
        },
        "description": {
            "fr": "Conseils stratégiques pour votre entreprise",
            "en": "Strategic advice for your business",
            "ar": "نصائح استراتيجية لأعمالك"
        }
    },

    # Customer Support
    "support": {
        "title": {
            "fr": "Support Client IA",
            "en": "AI Customer Support",
            "ar": "دعم العملاء بالذكاء الاصطناعي"
        },
        "description": {
            "fr": "Assistance client 24/7",
            "en": "24/7 Customer Assistance",
            "ar": "مساعدة العملاء على مدار الساعة"
        }
    },

    # Data Analysis
    "data_analysis": {
        "title": {
            "fr": "Analyse de Données IA",
            "en": "AI Data Analysis",
            "ar": "تحليل البيانات بالذكاء الاصطناعي"
        },
        "description": {
            "fr": "Insights puissants de vos données",
            "en": "Powerful insights from your data",
            "ar": "رؤى قوية من بياناتك"
        },
        "upload_data": {
            "fr": "Importer des données",
            "en": "Upload Data",
            "ar": "رفع البيانات"
        }
    },

    # RAG Agents
    "rag": {
        "title": {
            "fr": "Assistant RAG",
            "en": "RAG Assistant",
            "ar": "مساعد RAG"
        },
        "upload_doc": {
            "fr": "Importer document",
            "en": "Upload Document",
            "ar": "رفع مستند"
        },
        "search": {
            "fr": "Rechercher dans documents",
            "en": "Search in documents",
            "ar": "البحث في المستندات"
        }
    },

    # Financial Coach
    "finance": {
        "title": {
            "fr": "Coach Financier IA",
            "en": "AI Financial Coach",
            "ar": "مدرب مالي بالذكاء الاصطناعي"
        },
        "description": {
            "fr": "Conseils financiers personnalisés",
            "en": "Personalized financial advice",
            "ar": "نصائح مالية مخصصة"
        }
    },

    # Investment AI
    "investment": {
        "title": {
            "fr": "IA Investissement",
            "en": "Investment AI",
            "ar": "الذكاء الاصطناعي للاستثمار"
        },
        "stock_search": {
            "fr": "Rechercher action",
            "en": "Search Stock",
            "ar": "البحث عن الأسهم"
        }
    },

    # Sidebar
    "sidebar": {
        "language": {
            "fr": "Langue",
            "en": "Language",
            "ar": "اللغة"
        },
        "choose_lang": {
            "fr": "Choisir la langue",
            "en": "Choose Language",
            "ar": "اختر اللغة"
        },
        "api_key": {
            "fr": "Clé API OpenAI",
            "en": "OpenAI API Key",
            "ar": "مفتاح API OpenAI"
        },
        "model": {
            "fr": "Modèle",
            "en": "Model",
            "ar": "النموذج"
        },
        "temperature": {
            "fr": "Température",
            "en": "Temperature",
            "ar": "درجة الحرارة"
        }
    }
}


class StreamlitI18n:
    """Classe de gestion i18n pour Streamlit"""

    def __init__(self):
        # Initialiser la langue dans session_state
        if 'language' not in st.session_state:
            st.session_state.language = 'fr'

        self.current_lang = st.session_state.language

    def t(self, key: str, default: str = "") -> str:
        """
        Traduire une clé

        Args:
            key: Clé de traduction (ex: "common.title")
            default: Valeur par défaut si traduction non trouvée

        Returns:
            Texte traduit
        """
        keys = key.split('.')
        value = TRANSLATIONS

        try:
            for k in keys:
                value = value[k]

            if isinstance(value, dict):
                return value.get(self.current_lang, value.get('fr', default or key))
            return str(value)
        except (KeyError, TypeError):
            return default or key

    def set_language(self, lang: str):
        """Changer la langue"""
        if lang in ['fr', 'en', 'ar']:
            st.session_state.language = lang
            self.current_lang = lang
            st.rerun()

    def get_language(self) -> str:
        """Obtenir la langue actuelle"""
        return self.current_lang

    def language_selector(self):
        """
        Afficher le sélecteur de langue dans la sidebar
        Retourne True si la langue a changé
        """
        with st.sidebar:
            st.markdown("---")
            st.markdown(f"### {self.t('sidebar.language')}")

            lang_options = {
                'fr': '🇫🇷 Français',
                'en': '🇬🇧 English',
                'ar': '🇩🇿 العربية'
            }

            current_idx = list(lang_options.keys()).index(self.current_lang)

            selected_lang = st.selectbox(
                self.t('sidebar.choose_lang'),
                options=list(lang_options.keys()),
                format_func=lambda x: lang_options[x],
                index=current_idx,
                key='lang_selector'
            )

            if selected_lang != self.current_lang:
                self.set_language(selected_lang)
                return True

            return False


# Instance globale
def get_i18n() -> StreamlitI18n:
    """Obtenir l'instance i18n"""
    if 'i18n' not in st.session_state:
        st.session_state.i18n = StreamlitI18n()
    return st.session_state.i18n


# ========== CSS POUR STREAMLIT ==========
def inject_custom_css():
    """Injecter le CSS IAFactory dans Streamlit"""
    st.markdown("""
    <style>
        /* IAFactory Theme pour Streamlit */
        :root {
            --primary-color: #00a651 !important;
            --background-color: #020617 !important;
            --secondary-background-color: #0a0e1f !important;
            --text-color: #f8fafc !important;
        }

        /* Header */
        .main .block-container {
            padding-top: 2rem !important;
        }

        /* Boutons */
        .stButton > button {
            background-color: #00a651 !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.5rem 1.5rem !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
        }

        .stButton > button:hover {
            background-color: #00c767 !important;
            box-shadow: 0 0 20px rgba(0, 166, 81, 0.4) !important;
            transform: translateY(-2px) !important;
        }

        /* Inputs */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            background-color: #0a0e1f !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 10px !important;
            color: #f8fafc !important;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #00a651 !important;
            box-shadow: 0 0 0 3px rgba(0, 166, 81, 0.1) !important;
        }

        /* Chat messages */
        .stChatMessage {
            background-color: #0a0e1f !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 10px !important;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #020617 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.12) !important;
        }

        /* RTL Support pour l'arabe */
        [lang="ar"] {
            direction: rtl !important;
            text-align: right !important;
            font-family: 'Noto Sans Arabic', 'Cairo', 'Amiri', Arial, sans-serif !important;
        }

        /* Titre de l'app */
        h1 {
            color: #f8fafc !important;
            font-weight: 700 !important;
        }

        /* Logo IAFactory */
        .iaf-logo {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 1rem 0;
            margin-bottom: 1rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.12);
        }

        .iaf-logo-text {
            font-size: 1.2rem;
            font-weight: 700;
            color: #00a651;
        }
    </style>
    """, unsafe_allow_html=True)


# ========== HEADER TRILINGUE ==========
def render_header(agent_type: str = "common"):
    """
    Afficher le header trilingue de l'agent

    Args:
        agent_type: Type d'agent (common, consultant, support, etc.)
    """
    i18n = get_i18n()

    # Injecter CSS
    inject_custom_css()

    # Logo et titre
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown(f"""
        <div class="iaf-logo">
            <span style="font-size: 2rem;">🇩🇿</span>
            <span class="iaf-logo-text">IAFactory Algeria</span>
        </div>
        """, unsafe_allow_html=True)

        st.title(i18n.t(f"{agent_type}.title", i18n.t("common.title")))

        description = i18n.t(f"{agent_type}.description", "")
        if description:
            st.markdown(f"*{description}*")

    with col2:
        # Sélecteur de langue compact
        lang_options = {
            'fr': '🇫🇷 FR',
            'en': '🇬🇧 EN',
            'ar': '🇩🇿 AR'
        }

        selected = st.selectbox(
            "",
            options=list(lang_options.keys()),
            format_func=lambda x: lang_options[x],
            index=list(lang_options.keys()).index(i18n.current_lang),
            key='header_lang_selector',
            label_visibility="collapsed"
        )

        if selected != i18n.current_lang:
            i18n.set_language(selected)

    st.markdown("---")


# ========== EXEMPLE D'UTILISATION ==========
if __name__ == "__main__":
    # Configuration Streamlit
    st.set_page_config(
        page_title="IAFactory Algeria",
        page_icon="🇩🇿",
        layout="wide"
    )

    # Obtenir l'instance i18n
    i18n = get_i18n()

    # Afficher le header
    render_header("consultant")

    # Exemple de contenu trilingue
    st.write(i18n.t("common.subtitle"))

    # Input trilingue
    user_input = st.text_input(
        i18n.t("common.input_placeholder"),
        key="user_input"
    )

    # Bouton trilingue
    if st.button(i18n.t("common.send")):
        st.success(f"Message envoyé: {user_input}")

    # Sélecteur de langue dans sidebar
    i18n.language_selector()

    # Chatbot Help Widget
    st.markdown("""
    <div style="position: fixed; bottom: 24px; right: 24px; z-index: 9999;">
        <button onclick="var f = document.getElementById('cb-fr'); f.style.display = (f.style.display === 'block' ? 'none' : 'block')" style="width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, #00a651, #00d66a); border: none; cursor: pointer; color: white; font-size: 24px; box-shadow: 0 4px 12px rgba(0, 166, 81, 0.3);">?</button>
        <div id="cb-fr" style="display: none; position: fixed; bottom: 100px; right: 24px; width: 380px; height: 600px; border-radius: 16px; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3); background: white; overflow: hidden;">
            <iframe src="https://iafactoryalgeria.com/chatbot-ia" style="width: 100%; height: 100%; border: none;"></iframe>
        </div>
    </div>
    """, unsafe_allow_html=True)

