"""
IA Factory Algeria - Branding & Personnalisation

Configuration centralisée pour l'identité de l'écosystème.
Multilingue: Français, English, العربية, Darija, ⵜⴰⵎⴰⵣⵉⵖⵜ (Tamazight)
"""

# ============ COMPANY IDENTITY ============

COMPANY = {
    "name": "IA Factory Algeria",
    "short_name": "IAF",
    "tagline": {
        "fr": "L'IA au service de l'Algérie",
        "en": "AI Serving Algeria",
        "ar": "الذكاء الاصطناعي في خدمة الجزائر",
        "dz": "L'IA fel khedma ta3 Dzayer",
        "ber": "ⵜⴰⵎⵓⵙⵏⵉ ⵜⴰⵎⴰⴽⵍⴰⵍⵜ ⵉ ⵍⴷⵣⴰⵢⵔ",  # Tamazight
    },
    "logo_emoji": "🇩🇿",
    "colors": {
        "primary": "#006233",      # Vert algérien
        "secondary": "#D52B1E",    # Rouge algérien
        "accent": "#FFFFFF",       # Blanc
        "gold": "#FFD700",         # Or (accent premium)
    },
    "website": "https://iafactory.dz",
    "support_email": "support@iafactory.dz",
}

# ============ NEXUS ORCHESTRATOR BRANDING ============

NEXUS_BRANDING = {
    "name": "Nexus",
    "full_name": {
        "fr": "Nexus - Orchestrateur IA Factory",
        "en": "Nexus - IA Factory Orchestrator",
        "ar": "نيكسوس - منسق IA Factory",
        "dz": "Nexus - Orchestrateur ta3 IA Factory",  # Darija
        "ber": "Nexus - ⴰⵎⵙⵓⴷⴷⵓ IA Factory",  # Tamazight
    },
    "avatar": "🧭",
    "description": {
        "fr": "Ton assistant IA pour créer des applications. Parle-moi de ton projet!",
        "en": "Your AI assistant for building apps. Tell me about your project!",
        "ar": "مساعدك الذكي لبناء التطبيقات. أخبرني عن مشروعك!",
        "dz": "L'assistant ta3ek bach tcréé des applications. Goul-li 3la projet ta3ek!",
        "ber": "ⴰⵎⴰⵡⴰⵙ ⵏⵏⴽ ⵉ ⵓⵙⴽⴰⵔ ⵏ ⵉⵙⵏⴼⴰⵔⵏ. ⵉⵏⵉ-ⴰⵢⵉ ⵖⴼ ⵓⵙⴽⴰⵔ ⵏⵏⴽ!",  # Tamazight
    },
}

# ============ WELCOME MESSAGES ============

WELCOME_MESSAGES = {
    "first_visit": {
        "fr": """🇩🇿 **Bienvenue sur IA Factory Algeria!**

Je suis **Nexus**, ton chef de projet IA. Mon équipe et moi allons t'aider à créer ton application.

**Comment ça marche:**
1. 💬 Tu me décris ton idée
2. 🔍 Amine (l'analyste) va explorer avec toi
3. ✅ On valide ensemble
4. 🚀 Bolt génère ton code!

**Exemples de projets:**
• "Je veux créer une app de livraison pour Alger"
• "Fais-moi un site e-commerce avec Chargily"
• "Une app de gestion de stock pour mon restaurant"

Alors, c'est quoi ton projet? 🎯""",

        "en": """🇩🇿 **Welcome to IA Factory Algeria!**

I'm **Nexus**, your AI project manager. My team and I will help you build your app.

**How it works:**
1. 💬 Tell me your idea
2. 🔍 Amine (analyst) will explore with you
3. ✅ We validate together
4. 🚀 Bolt generates your code!

**Project examples:**
• "I want a delivery app for Algiers"
• "Build me an e-commerce site with Chargily"
• "A stock management app for my restaurant"

So, what's your project? 🎯""",

        "ar": """🇩🇿 **مرحبا بك في IA Factory الجزائر!**

أنا **Nexus**، مدير مشروعك الذكي. فريقي وأنا سنساعدك في بناء تطبيقك.

**كيف يعمل:**
1. 💬 أخبرني بفكرتك
2. 🔍 أمين (المحلل) سيستكشف معك
3. ✅ نتحقق معًا
4. 🚀 Bolt يولّد الكود!

**أمثلة على المشاريع:**
• "أريد تطبيق توصيل للجزائر العاصمة"
• "أنشئ لي موقع تجارة إلكترونية مع Chargily"
• "تطبيق إدارة المخزون لمطعمي"

إذن، ما هو مشروعك؟ 🎯""",

        "dz": """🇩🇿 **Marhba bik f'IA Factory Algeria!**

Ana **Nexus**, chef de projet ta3ek. Ana w l'équipe ta3i rah nsawnok tbni l'app ta3ek.

**Kifach tkhedm:**
1. 💬 Goul-li l'idée ta3ek
2. 🔍 Amine (l'analyste) rah yexplori m3ak
3. ✅ Nvalidaw ensemble
4. 🚀 Bolt rah ygénéri le code!

**Exemples de projets:**
• "Nheb ncréé app de livraison l'Alger"
• "Dir-li site e-commerce b'Chargily"
• "App de gestion de stock l'restaurant ta3i"

Yalla, wach howa projet ta3ek? 🎯""",

        "ber": """🇩🇿 **ⴰⵏⵙⵓⴼ ⵖⵔ IA Factory ⵍⴷⵣⴰⵢⵔ!**

ⵏⴽⴽ ⴷ **Nexus**, ⴰⵏⴱⴷⴰⴷ ⵏ ⵓⵙⴽⴰⵔ ⵏⵏⴽ. ⵏⴽⴽ ⴷ ⵜⵔⴰⴱⴱⵓⵜ ⵉⵏⵓ ⴰⴷ ⴽ-ⵏⵄⴰⵡⵏ ⴰⴷ ⵜⴱⵏⵉⴷ ⴰⵙⵏⴼⴰⵔ ⵏⵏⴽ.

**ⵎⴰⵎⴽ ⵉⵜⵜⵅⴷⴷⴰⵎ:**
1. 💬 ⵉⵏⵉ-ⴰⵢⵉ ⵜⴰⵡⵏⴳⵉⵎⵜ ⵏⵏⴽ
2. 🔍 Amine (ⴰⵎⵙⴼⵔⵓ) ⴰⴷ ⵉⵙⵙⵏⴽⴷ ⵉⴷⵎⴽ
3. ✅ ⴰⴷ ⵏⵙⴼⵇⴷ ⵉⵎⴰⵏ ⵏⵏⵖ
4. 🚀 Bolt ⴰⴷ ⵉⵙⵙⴽⵔ ⵜⴰⵏⴳⴰⵍⵜ!

**ⵉⵎⴷⵢⴰⵜⵏ ⵏ ⵉⵙⴽⴰⵔⵏ:**
• "ⴱⵖⵉⵖ ⴰⴷ ⵙⴽⵔⵖ app ⵏ ⵓⵙⵙⵉⵡⴹ ⵉ ⵍⵣⵣⴰⵢⵔ"
• "ⵙⴽⵔ-ⴰⵢⵉ ⴰⵙⵉⵜ ⵏ e-commerce ⵙ Chargily"
• "App ⵏ ⵓⵙⵡⵓⴷⴷⵓ ⵏ ⵓⴽⵜⵜⵓⵔ ⵉ ⵓⵙⴰⴽⵉ ⵉⵏⵓ"

ⵉⵀⵉ, ⵎⴰⵜⵜⴰ ⴷ ⴰⵙⴽⴰⵔ ⵏⵏⴽ? 🎯""",
    },

    "returning_user": {
        "fr": "Ravi de te revoir! 👋 On continue sur quoi aujourd'hui?",
        "en": "Good to see you again! 👋 What are we working on today?",
        "ar": "سعيد برؤيتك مجددًا! 👋 على ماذا نعمل اليوم؟",
        "dz": "Marhba bik mara okhra! 👋 Wach rah nkhedmo lyoum?",
        "ber": "ⵄⴰⴷⴷⵏⵖ ⴰⴷ ⴽ-ⵥⵕⵖ ⴷⴰⵖ! 👋 ⵎⴰⵜⵜⴰ ⴰⴷ ⵏⵅⴷⵎ ⴰⵙⵙⴰ?",
    },
}

# ============ ALGERIAN CONTEXT ============

ALGERIA_CONTEXT = {
    "payment_providers": ["Chargily", "Baridimob", "CCP", "SATIM"],
    "delivery_services": ["Yassir Express", "Jumia Food", "Glovo"],
    "popular_cities": ["Alger", "Oran", "Constantine", "Annaba", "Blida", "Sétif"],
    "wilayas_count": 58,
    "languages": ["Arabe", "Français", "Tamazight", "Darija"],
    "currency": "DZD",
    "phone_prefix": "+213",
    "timezone": "Africa/Algiers",
}

# ============ TECH STACK PREFERENCES ============

PREFERRED_STACK = {
    "frontend": {
        "framework": "React",
        "bundler": "Vite",
        "styling": "Tailwind CSS",
        "ui_library": "shadcn/ui",
        "icons": "Lucide React",
    },
    "backend": {
        "framework": "FastAPI",
        "database": "PostgreSQL",
        "cache": "Redis",
        "orm": "SQLAlchemy",
    },
    "mobile": {
        "framework": "React Native",
        "expo": True,
    },
    "ai": {
        "llm_provider": "OpenAI / Anthropic",
        "embedding": "OpenAI Ada",
        "vector_db": "Qdrant",
    },
    "deployment": {
        "container": "Docker",
        "orchestration": "Docker Compose",
        "cloud": "VPS Algérie (Webhost.dz) / DigitalOcean",
    },
}

# ============ AGENT NAMES (Algerian flavor) ============

AGENT_NAMES = {
    "orchestrator": {
        "name": "Nexus",
        "personality": "Le chef d'équipe organisé",
    },
    "analyst": {
        "name": "Amine",
        "personality": "Le curieux qui veut tout comprendre",
    },
    "pm": {
        "name": "Sarah",
        "personality": "La pragmatique qui priorise",
    },
    "architect": {
        "name": "Karim",
        "personality": "Le tech accessible",
    },
    "ux": {
        "name": "Lina",
        "personality": "La créative qui pense utilisateur",
    },
    "developer": {
        "name": "Yacine",
        "personality": "L'efficace qui code",
    },
    "po": {
        "name": "Nadia",
        "personality": "L'organisée qui découpe",
    },
    "qa": {
        "name": "Mehdi",
        "personality": "Le rigoureux qui teste",
    },
}

# ============ ERROR MESSAGES ============

ERROR_MESSAGES = {
    "connection_failed": {
        "fr": "❌ Impossible de se connecter à Nexus. Vérifie que le serveur est lancé.",
        "en": "❌ Unable to connect to Nexus. Make sure the server is running.",
        "ar": "❌ تعذر الاتصال بـ Nexus. تأكد من تشغيل الخادم.",
        "dz": "❌ Ma ymkenche nconnectiw l'Nexus. Vérifi que le serveur lancé.",
        "ber": "❌ ⵓⵔ ⵏⵣⵎⵔ ⴰⴷ ⵏⵣⴷⵉ ⵖⵔ Nexus. ⵙⴼⵇⴷ ⵎⴰⵍⴰ ⵉⵜⵜⵓⵙⵏⴽⵔ ⵓⵇⴷⴷⴰⵛ.",
    },
    "timeout": {
        "fr": "⏳ La requête a pris trop de temps. Réessaye dans un instant.",
        "en": "⏳ Request took too long. Try again in a moment.",
        "ar": "⏳ استغرق الطلب وقتًا طويلاً. حاول مرة أخرى بعد قليل.",
        "dz": "⏳ La requête khdmet bezaf wqet. 3awd jarreb.",
        "ber": "⏳ ⵜⵓⵜⵔⴰ ⵜⴽⴽⴰ ⴰⵟⴰⵙ ⵏ ⵡⴰⴽⵓⴷ. ⵄⴰⵡⴷ ⴰⵔⵎ.",
    },
    "generic": {
        "fr": "❌ Une erreur s'est produite. Notre équipe est notifiée.",
        "en": "❌ An error occurred. Our team has been notified.",
        "ar": "❌ حدث خطأ. تم إخطار فريقنا.",
        "dz": "❌ Kayn erreur. L'équipe ta3na 3almet.",
        "ber": "❌ ⵜⵍⵍⴰ ⵜⵓⵛⴷⴰ. ⵜⵔⴰⴱⴱⵓⵜ ⵏⵏⵖ ⵜⵜⵡⴰⵙⵙⵏ.",
    },
}

# ============ SUCCESS MESSAGES ============

SUCCESS_MESSAGES = {
    "project_created": {
        "fr": "✅ Projet créé avec succès! Prêt pour la génération.",
        "en": "✅ Project created successfully! Ready for generation.",
        "ar": "✅ تم إنشاء المشروع بنجاح! جاهز للتوليد.",
        "dz": "✅ Projet tcréa b'succès! Prêt l'génération.",
        "ber": "✅ ⴰⵙⴽⴰⵔ ⵉⵜⵜⵓⵙⴽⵔ! ⵢⵓⵊⴰⴷ ⵉ ⵓⵙⵙⴽⵔ.",
    },
    "code_generated": {
        "fr": "🚀 Code généré! Tu peux maintenant explorer ton projet.",
        "en": "🚀 Code generated! You can now explore your project.",
        "ar": "🚀 تم توليد الكود! يمكنك الآن استكشاف مشروعك.",
        "dz": "🚀 Code tgénéra! Dork tzid tchouf projet ta3ek.",
        "ber": "🚀 ⵜⴰⵏⴳⴰⵍⵜ ⵜⵜⵡⴰⵙⴽⵔ! ⵜⵣⵎⵔⴷ ⴰⴷ ⵜⵙⵙⵏⴽⴷⴷ ⴰⵙⴽⴰⵔ ⵏⵏⴽ.",
    },
}

# ============ HELPER FUNCTIONS ============

def get_text(messages: dict, lang: str = "fr") -> str:
    """Get text in the specified language with fallback to French"""
    if lang in messages:
        return messages[lang]
    return messages.get("fr", list(messages.values())[0])


def get_company_tagline(lang: str = "fr") -> str:
    """Get company tagline in specified language"""
    return get_text(COMPANY["tagline"], lang)


def get_welcome_message(lang: str = "fr", returning: bool = False) -> str:
    """Get appropriate welcome message"""
    if returning:
        return get_text(WELCOME_MESSAGES["returning_user"], lang)
    return get_text(WELCOME_MESSAGES["first_visit"], lang)


def get_error_message(error_type: str, lang: str = "fr") -> str:
    """Get error message in specified language"""
    if error_type in ERROR_MESSAGES:
        return get_text(ERROR_MESSAGES[error_type], lang)
    return get_text(ERROR_MESSAGES["generic"], lang)
