"""
Conversation Manager - Gère les conversations multi-agents avec le user

🇩🇿 IA Factory Algeria - BMAD Multi-Agent Conversation System

Le user VOIT et PARLE avec chaque agent BMAD individuellement.
C'est une expérience interactive, pas un pipeline automatique.

Phases:
1. ACCUEIL - Nexus accueille, comprend le besoin
2. BRAINSTORM - Amine explore l'idée avec le user
3. VALIDATION - Nexus résume et demande GO
4. PREPARATION - Nexus prépare le prompt Bolt
5. GENERATION - Bolt génère après validation user
"""

from dataclasses import dataclass, field
from typing import Optional, Any
from enum import Enum
import uuid
from datetime import datetime

# Import branding centralisé
from .branding import (
    COMPANY, NEXUS_BRANDING, WELCOME_MESSAGES, AGENT_NAMES,
    ALGERIA_CONTEXT, PREFERRED_STACK,
    get_text, get_welcome_message, get_error_message
)


class ConversationPhase(str, Enum):
    """Phases de la conversation guidée"""
    ACCUEIL = "accueil"          # Meta accueille
    BRAINSTORM = "brainstorm"    # Analyst explore
    CADRAGE = "cadrage"          # PM définit scope
    ARCHITECTURE = "architecture" # Architect propose
    UX = "ux"                    # UX Designer
    VALIDATION = "validation"    # Résumé avant création
    CREATION = "creation"        # Archon crée
    PREPARATION = "preparation"  # Prépare prompt Bolt
    GENERATION = "generation"    # Bolt génère


class AgentRole(str, Enum):
    """Les agents qui peuvent parler au user"""
    ORCHESTRATOR = "orchestrator"
    ANALYST = "analyst"
    PM = "pm"
    ARCHITECT = "architect"
    UX = "ux"
    DEVELOPER = "developer"
    PO = "po"
    QA = "qa"


# Personnalités des agents IA Factory - Noms algériens, multilingue (FR, EN, AR, Darija)
AGENT_PERSONAS = {
    AgentRole.ORCHESTRATOR: {
        "name": AGENT_NAMES["orchestrator"]["name"],  # Nexus
        "title": {"fr": "Chef de projet", "en": "Project Manager", "ar": "�
دير ال�
شروع", "dz": "Chef ta3 projet", "ber": "ⴰⵏⴱⴷⴰⴷ ⵏ ⵓⵙⴽⴰⵔ"},
        "avatar": NEXUS_BRANDING["avatar"],  # 🧭
        "personality": AGENT_NAMES["orchestrator"]["personality"],
        "greeting": {
            "fr": "Salut! Je suis Nexus, ton chef de projet chez IA Factory. Décris-moi ton idée et on la construit ensemble!",
            "en": "Hi! I'm Nexus, your project manager at IA Factory. Tell me your idea and we'll build it together!",
            "ar": "Tu parles en arabe. Adapte-toi au style du user.",
رحبا! أنا Nexus، �
دير �
شروعك في IA Factory. أخبرني بفكرتك ونبنيها �
عا!",
            "dz": "Saha! Ana Nexus, chef de projet ta3ek f'IA Factory. Goul-li l'idée ta3ek w nbniouha ensemble!",
            "ber": "ⴰⵣⵓⵍ! ⵏⴽⴽ ⴷ Nexus, ⴰⵏⴱⴷⴰⴷ ⵏ ⵓⵙⴽⴰⵔ ⵏⵏⴽ ⴳ IA Factory. ⵉⵏⵉ-ⴰⵢⵉ ⵜⴰⵡⵏⴳⵉⵎⵜ ⵏⵏⴽ!",
        },
    },
    AgentRole.ANALYST: {
        "name": AGENT_NAMES["analyst"]["name"],  # Amine
        "title": {"fr": "Business Analyst", "en": "Business Analyst", "ar": "�
حلل الأع�
ال", "dz": "Analyst", "ber": "ⴰⵎⵙⴼⵔⵓ"},
        "avatar": "🔍",
        "personality": AGENT_NAMES["analyst"]["personality"],
        "greeting": {
            "fr": "Hey! Moi c'est Amine, l'analyst. Dis-moi ce que tu veux construire!",
            "en": "Hey! I'm Amine, the analyst. Tell me what you want to build!",
            "ar": "Tu parles en arabe. Adapte-toi au style du user.",
رحبا! أنا أ�
ين، ال�
حلل. قل لي �
ا تريد بناءه!",
            "dz": "Wesh! Ana Amine. Goul-li wach rak theb tcréé!",
            "ber": "ⴰⵣⵓⵍ! ⵏⴽⴽ ⴷ Amine. ⵉⵏⵉ-ⴰⵢⵉ ⵎⴰⵜⵜⴰ ⵜⴱⵖⵉⴷ ⴰⴷ ⵜⵙⴽⵔⴷ!",
        },
    },
    AgentRole.PM: {
        "name": AGENT_NAMES["pm"]["name"],  # Sarah
        "title": {"fr": "Product Manager", "en": "Product Manager", "ar": "�
ديرة ال�
نتج", "dz": "PM", "ber": "ⵜⴰⵏⴱⴷⴰⴷⵜ ⵏ ⵓⴼⴰⵔⵙ"},
        "avatar": "📋",
        "personality": AGENT_NAMES["pm"]["personality"],
        "greeting": {
            "fr": "Salut! Sarah, PM. On va définir ensemble ce qu'on construit.",
            "en": "Hi! Sarah, PM. Let's define what we're building together.",
            "ar": "Tu parles en arabe. Adapte-toi au style du user.",
رحبا! سارة، �
ديرة ال�
نتج. دعنا نحدد �
ا نبنيه �
عا.",
            "dz": "Saha! Ana Sarah, PM. Rah ndéfiniwou wach rah nbniou ensemble.",
            "ber": "ⴰⵣⵓⵍ! ⵏⴽⴽ ⴷ Sarah, PM. ⴰⴷ ⵏⵙⵜⵉ ⵎⴰⵜⵜⴰ ⴰⴷ ⵏⵙⴽⵔ.",
        },
    },
    AgentRole.ARCHITECT: {
        "name": AGENT_NAMES["architect"]["name"],  # Karim
        "title": {"fr": "Architecte Technique", "en": "Technical Architect", "ar": "ال�
هندس ال�
ع�
اري", "dz": "Architect", "ber": "ⴰⵎⴱⵏⵉ ⴰⵜⵉⵇⵏⵉ"},
        "avatar": "🏗️",
        "personality": AGENT_NAMES["architect"]["personality"],
        "greeting": {
            "fr": "Karim, l'architecte. Je te propose les meilleures options techniques.",
            "en": "Karim, the architect. I'll suggest the best technical options.",
            "ar": "Tu parles en arabe. Adapte-toi au style du user.",
، ال�
هندس ال�
ع�
اري. سأقترح أفضل الخيارات التقنية.",
            "dz": "Ana Karim, l'architect. Rah nchouf-lek les meilleures options techniques.",
            "ber": "ⵏⴽⴽ ⴷ Karim, ⴰⵎⴱⵏⵉ. ⴰⴷ ⴰⴽ-ⵙⵙⵓⵎⵔⵖ ⵉⴼⵔⴷⵉⵙⵏ ⵉⴳⴳⵓⵜⵏ.",
        },
    },
    AgentRole.UX: {
        "name": AGENT_NAMES["ux"]["name"],  # Lina
        "title": {"fr": "UX Designer", "en": "UX Designer", "ar": "�
ص�
�
ة تجربة ال�
ستخد�
", "dz": "Designer UX", "ber": "ⵜⴰⵎⵙⵓⵏⴰⵢⵜ UX"},
        "avatar": "🎨",
        "personality": AGENT_NAMES["ux"]["personality"],
        "greeting": {
            "fr": "Coucou! Lina, UX. On parle de l'expérience utilisateur!",
            "en": "Hey! Lina, UX. Let's talk about user experience!",
            "ar": "Tu parles en arabe. Adapte-toi au style du user.",
رحبا! لينا، �
ص�
�
ة UX. لنتحدث عن تجربة ال�
ستخد�
!",
            "dz": "Coucou! Ana Lina, UX. Rah nahkiou 3la l'expérience utilisateur!",
            "ber": "ⴰⵣⵓⵍ! ⵏⴽⴽ ⴷ Lina, UX. ⴰⴷ ⵏⵙⵉⵡⵍ ⵖⴼ ⵜⵉⵔⵎⵉⵜ ⵏ ⵓⵎⵙⵙⵎⵔⵙ!",
        },
    },
    AgentRole.DEVELOPER: {
        "name": AGENT_NAMES["developer"]["name"],  # Yacine
        "title": {"fr": "Lead Developer", "en": "Lead Developer", "ar": "ال�
طور الرئيسي", "dz": "Dev Lead", "ber": "ⴰⵏⴰⵡ ⵏ ⵉⵙⵏⴼⴰⵔⵏ"},
        "avatar": "💻",
        "personality": AGENT_NAMES["developer"]["personality"],
        "greeting": {
            "fr": "Yacine, dev lead. C'est faisable, on va le faire!",
            "en": "Yacine, dev lead. It's doable, let's build it!",
            "ar": "Tu parles en arabe. Adapte-toi au style du user.",
طور الرئيسي. �
�
كن، هيا نبنيه!",
            "dz": "Ana Yacine, dev lead. Momkin, yalla nbniouha!",
            "ber": "ⵏⴽⴽ ⴷ Yacine, dev lead. ⵉⵖⵢ ⴰⴷ ⵉⵜⵜⵓⵙⴽⵔ, ⴰⴷ ⵜ-ⵏⵙⴽⵔ!",
        },
    },
    AgentRole.PO: {
        "name": AGENT_NAMES["po"]["name"],  # Nadia
        "title": {"fr": "Product Owner", "en": "Product Owner", "ar": "�
الكة ال�
نتج", "dz": "PO", "ber": "ⵜⴰⵎⴱⴰⴱⵜ ⵏ ⵓⴼⴰⵔⵙ"},
        "avatar": "📝",
        "personality": AGENT_NAMES["po"]["personality"],
        "greeting": {
            "fr": "Nadia, PO. Je transforme tout en tâches concrètes.",
            "en": "Nadia, PO. I'll turn everything into concrete tasks.",
            "ar": "Tu parles en arabe. Adapte-toi au style du user.",
الكة ال�
نتج. سأحول كل شيء إلى �
ها�
 �
ل�
وسة.",
            "dz": "Ana Nadia, PO. Rah ntransformi koulech l'tâches concrètes.",
            "ber": "ⵏⴽⴽ ⴷ Nadia, PO. ⴰⴷ ⵙⴱⴷⴷⵍⵖ ⴽⵓⵍⵛⵉ ⵖⵔ ⵜⵉⵡⵓⵔⵉⵡⵉⵏ.",
        },
    },
    AgentRole.QA: {
        "name": AGENT_NAMES["qa"]["name"],  # Mehdi
        "title": {"fr": "QA Engineer", "en": "QA Engineer", "ar": "�
هندس ض�
ان الجودة", "dz": "QA", "ber": "ⴰⵎⵙⴳⴳⴰⴷ ⵏ ⵜⵖⴰⵔⴰ"},
        "avatar": "🧪",
        "personality": AGENT_NAMES["qa"]["personality"],
        "greeting": {
            "fr": "Mehdi, QA. On n'oublie rien!",
            "en": "Mehdi, QA. We won't miss anything!",
            "ar": "Tu parles en arabe. Adapte-toi au style du user.",
هدي، �
هندس الجودة. لن ننسى شيئا!",
            "dz": "Ana Mehdi, QA. Ma nnessawch walo!",
            "ber": "ⵏⴽⴽ ⴷ Mehdi, QA. ⵓⵔ ⵏⵜⵜⵓ ⵡⴰⵍⵓ!",
        },
    },
}


AGENT_CHAIN = [
    {"phase": ConversationPhase.ACCUEIL, "agent": AgentRole.ORCHESTRATOR, "goal": "Accueil + cadrage rapide"},
    {"phase": ConversationPhase.BRAINSTORM, "agent": AgentRole.ANALYST, "goal": "Clarifier le besoin"},
    {"phase": ConversationPhase.VALIDATION, "agent": AgentRole.ORCHESTRATOR, "goal": "Valider la direction"},
    {"phase": ConversationPhase.PREPARATION, "agent": AgentRole.ORCHESTRATOR, "goal": "Preparer le prompt Bolt"},
    {"phase": ConversationPhase.GENERATION, "agent": AgentRole.ORCHESTRATOR, "goal": "Generer le livrable"},
]


def detect_language(text: str) -> str:
"""
    Détecte la langue du texte (fr, en, ar, dz, ber)
    Supporte: Français, English, العربية, Darija, ⵜⴰⵎⴰⵣⵉⵖⵜ (Tamazight/Amazigh)
"""
    lower = text.lower()

    # Caractères Tifinagh (Amazigh/Berbère) → ber
    # Range Unicode: U+2D30 à U+2D7F
    if any('\u2D30' <= c <= '\u2D7F' for c in text):
        return "ber"

    # Mots clés Amazigh en latin (Kabyle, Chaoui, etc.)
    # Note: On utilise des mots plus longs/distinctifs pour éviter les faux positifs
    # Par exemple "ur" est dans "bonjour" donc on l'enlève
    ber_keywords = ["azul", "tanmirt", "amek", "nekk", "kemm", "netta",
                    "tamurt", "taqbaylit", "tamazight", "imazighen", "amazigh",
                    "aqvayli", "weltma", "axxam", "taddart",
                    "bghigh", "zemregh", "skker", "akken", "iswi", "tifawt"]
    # Vérifier les mots complets uniquement (avec espaces)
    ber_count = sum(1 for w in ber_keywords if f" {w} " in f" {lower} " or lower == w or lower.startswith(f"{w} ") or lower.endswith(f" {w}"))
    if ber_count >= 1:  # Un seul mot amazigh suffit
        return "ber"

    # Caractères arabes classiques → ar
    if any('\u0600' <= c <= '\u06FF' for c in text):
        return "ar"

    # Mots clés Darija algérienne
    dz_keywords = ["wesh", "wach", "rak", "rahi", "nheb", "tcréé", "khoya", "sahbi",
                   "ta3", "ta3i", "ta3ek", "kho", "saha", "yalla", "hadi", "hadik",
                   "nchouf", "goul", "dir", "bezaf", "bark", "3la", "m3a", "khedma"]
    dz_count = sum(1 for w in dz_keywords if w in lower)
    if dz_count >= 1:  # Un seul mot darija suffit
        return "dz"

    # Mots clés français courants
    fr_keywords = ["je", "veux", "créer", "une", "application", "salut", "bonjour",
                   "merci", "projet", "faire", "aide", "moi", "comment", "pourquoi"]
    en_keywords = ["i", "want", "create", "an", "app", "hello", "hi", "thanks",
                   "project", "make", "build", "help", "please", "how", "what"]

    fr_count = sum(1 for w in fr_keywords if f" {w} " in f" {lower} ")
    en_count = sum(1 for w in en_keywords if f" {w} " in f" {lower} ")

    if en_count > fr_count:
        return "en"
    return "fr"  # Défaut: français


def get_full_welcome_message(lang: str = "fr") -> str:
"""
    Retourne le message de bienvenue complet de IA Factory Algeria
    Utilise les messages du branding.py
"""
    return get_welcome_message(lang, returning=False)


@dataclass
class Message:
    """Un message dans la conversation"""
    id: str
    role: str  # "user" | "agent"
    agent: Optional[AgentRole]  # Quel agent parle (si role=agent)
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)


@dataclass
class ProjectState:
    """État du projet en cours de définition"""
    name: str = ""
    type: str = ""  # frontend, backend, fullstack
    description: str = ""
    features: list = field(default_factory=list)
    stack: list = field(default_factory=list)
    constraints: list = field(default_factory=list)
    decisions: dict = field(default_factory=dict)  # Décisions prises avec chaque agent
    archon_project_id: Optional[str] = None
    bolt_prompt: Optional[str] = None


@dataclass
class ConversationSession:
    """Une session de conversation complète"""
    id: str
    user_id: str
    phase: ConversationPhase
    active_agent: AgentRole
    messages: list = field(default_factory=list)
    project: ProjectState = field(default_factory=ProjectState)
    created_at: datetime = field(default_factory=datetime.now)
    language: str = "fr"  # Detected language (fr, en, ar)

    def add_message(self, role: str, content: str, agent: Optional[AgentRole] = None, metadata: dict = None):
        msg = Message(
            id=str(uuid.uuid4()),
            role=role,
            agent=agent,
            content=content,
            metadata=metadata or {}
        )
        self.messages.append(msg)
        return msg


class ConversationManager:
"""
    Gère les conversations multi-agents.

    Chaque agent a sa personnalité et son rôle.
    Le user parle à UN agent à la fois.
    L'orchestrator coordonne les transitions.
"""

    def __init__(self):
        self.sessions: dict[str, ConversationSession] = {}

    def create_session(self, user_id: str) -> ConversationSession:
        """Crée une nouvelle session de conversation"""
        session = ConversationSession(
            id=str(uuid.uuid4()),
            user_id=user_id,
            phase=ConversationPhase.ACCUEIL,
            active_agent=AgentRole.ORCHESTRATOR
        )
        self.sessions[session.id] = session
        return session

    def get_session(self, session_id: str) -> Optional[ConversationSession]:
        return self.sessions.get(session_id)

    def delete_session(self, session_id: str) -> bool:
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False

    def get_agent_info(self, agent: AgentRole, lang: str = "fr") -> dict:
        """Retourne les infos d'un agent pour l'affichage (multilingue)"""
        persona = AGENT_PERSONAS.get(agent, {})
        title = persona.get("title", "")
        if isinstance(title, dict):
            title = title.get(lang, title.get("fr", ""))
        return {
            "role": agent.value,
            "name": persona.get("name", agent.value),
            "title": title,
            "avatar": persona.get("avatar", "🤖"),
        }

    def get_agent_greeting(self, agent: AgentRole, lang: str = "fr") -> str:
        """Retourne le greeting d'un agent dans la bonne langue"""
        persona = AGENT_PERSONAS.get(agent, {})
        greeting = persona.get("greeting", "")
        if isinstance(greeting, dict):
            return greeting.get(lang, greeting.get("fr", "Bonjour!"))
        return greeting

    def determine_next_phase(self, session: ConversationSession, user_message: str) -> tuple[ConversationPhase, AgentRole]:
"""
        Détermine la prochaine phase et l'agent actif basé sur le contexte.
        Le user peut dire "GO", "suivant", ou répondre aux questions.
"""
        lower = user_message.lower().strip()
        current_phase = session.phase
        project = session.project

        # Commandes explicites du user
        if lower in ["go", "ok", "oui", "yes", "valide", "confirme", "c'est bon", "parfait"]:
            # Passer à la phase suivante
            return self._advance_phase(current_phase, project)

        if lower in ["non", "modifier", "changer", "revenir", "retour"]:
            # Revenir en arrière ou rester
            return self._handle_rejection(current_phase)

        if lower.startswith("parle à ") or lower.startswith("je veux parler à"):
            # User veut parler à un agent spécifique
            agent = self._extract_agent_request(lower)
            if agent:
                return current_phase, agent

        # Logique automatique basée sur l'état du projet
        return self._auto_determine_next(session)

    def _advance_phase(self, current: ConversationPhase, project: ProjectState) -> tuple[ConversationPhase, AgentRole]:
        """Avance à la phase suivante - MODE RAPIDE: moins d'étapes"""
        # Flow RAPIDE: Accueil -> Brainstorm -> Validation -> Generation
        phase_flow = {
            ConversationPhase.ACCUEIL: (ConversationPhase.BRAINSTORM, AgentRole.ANALYST),
            ConversationPhase.BRAINSTORM: (ConversationPhase.VALIDATION, AgentRole.ORCHESTRATOR),  # Skip PM, Architect, UX
            ConversationPhase.CADRAGE: (ConversationPhase.VALIDATION, AgentRole.ORCHESTRATOR),
            ConversationPhase.ARCHITECTURE: (ConversationPhase.VALIDATION, AgentRole.ORCHESTRATOR),
            ConversationPhase.UX: (ConversationPhase.VALIDATION, AgentRole.ORCHESTRATOR),
            ConversationPhase.VALIDATION: (ConversationPhase.PREPARATION, AgentRole.ORCHESTRATOR),
            ConversationPhase.CREATION: (ConversationPhase.PREPARATION, AgentRole.ORCHESTRATOR),
            ConversationPhase.PREPARATION: (ConversationPhase.GENERATION, AgentRole.ORCHESTRATOR),
            ConversationPhase.GENERATION: (ConversationPhase.GENERATION, AgentRole.ORCHESTRATOR),  # Fin
        }
        return phase_flow.get(current, (current, AgentRole.ORCHESTRATOR))

    def _handle_rejection(self, current: ConversationPhase) -> tuple[ConversationPhase, AgentRole]:
        """Gère le refus du user - revient en arrière ou reste"""
        if current == ConversationPhase.VALIDATION:
            return ConversationPhase.BRAINSTORM, AgentRole.ANALYST
        return current, AgentRole.ORCHESTRATOR

    def _extract_agent_request(self, message: str) -> Optional[AgentRole]:
        """Extrait le nom de l'agent demandé"""
        agent_keywords = {
            "analyst": AgentRole.ANALYST,
            "amine": AgentRole.ANALYST,
            "pm": AgentRole.PM,
            "sarah": AgentRole.PM,
            "architect": AgentRole.ARCHITECT,
            "karim": AgentRole.ARCHITECT,
            "ux": AgentRole.UX,
            "lina": AgentRole.UX,
            "dev": AgentRole.DEVELOPER,
            "yacine": AgentRole.DEVELOPER,
            "po": AgentRole.PO,
            "nadia": AgentRole.PO,
            "qa": AgentRole.QA,
            "mehdi": AgentRole.QA,
        }
        for keyword, agent in agent_keywords.items():
            if keyword in message.lower():
                return agent
        return None

    def _auto_determine_next(self, session: ConversationSession) -> tuple[ConversationPhase, AgentRole]:
        """Détermine automatiquement la suite basé sur le contexte"""
        project = session.project
        current = session.phase

        # Si on est en ACCUEIL et qu'on a une description, passer au brainstorm
        if current == ConversationPhase.ACCUEIL and project.description:
            return ConversationPhase.BRAINSTORM, AgentRole.ANALYST

        # Rester dans la phase actuelle par défaut
        return current, session.active_agent

    def get_phase_prompt(self, phase: ConversationPhase, agent: AgentRole, project: ProjectState, lang: str = "fr") -> str:
        """
        Genere le system prompt pour l'agent actif selon la phase.
        L'agent doit etre CONVERSATIONNEL, pas generer du JSON.
        Utilise les donnees du branding IA Factory Algeria.
        """
        persona = AGENT_PERSONAS.get(agent, {})
        title = persona.get('title', {})
        if isinstance(title, dict):
            title = title.get(lang, title.get('fr', ''))

        # Contexte algerien du branding
        payment_providers = ", ".join(ALGERIA_CONTEXT["payment_providers"])
        cities = ", ".join(ALGERIA_CONTEXT["popular_cities"][:4])

        # Stack preferee du branding
        frontend = PREFERRED_STACK["frontend"]
        backend = PREFERRED_STACK["backend"]
        default_stack = f"{frontend['framework']} + {frontend['bundler']} + {frontend['styling']} + {backend['framework']}"

        # Language instructions based on detected language
        lang_instructions = {
            "fr": "Tu parles en francais. Tu peux utiliser du darija algerien si le user le fait.",
            "en": "You speak in English. Adapt to the user's style.",
            "ar": "Tu parles en arabe. Adapte-toi au style du user.",
            "dz": "Tu parles en darija algerienne. Tu peux mixer avec le francais si besoin.",
            "ber": "Tu parles en francais avec quelques mots en tamazight si le user le fait.",
        }
        lang_rule = lang_instructions.get(lang, lang_instructions["fr"])

        # IMPORTANT: Forcer francais pour les reponses par defaut
        response_lang_rule = "\nIMPORTANT: Reponds TOUJOURS dans la langue du user."

        pro_direct_rules = """
MODE PRO DIRECT:
- Donne UNE seule meilleure solution (pas d'options A/B, pas de listes de choix).
- Reponse courte et guidee, sans blabla.
- Format obligatoire:
  Decision: ...
  Plan: 1) ... 2) ... 3) ...
  Besoin: ... (UNE seule question si bloquant, sinon "Aucun")
- Tu utilises des hypotheses par defaut si info manquante et tu avances.
- Tu poses UNE question a la fois, uniquement si indispensable pour avancer.
- Tu reponds dans la langue de l'utilisateur.
"""

        base = f"""Tu es {persona.get('name', agent.value)}, {title} chez {COMPANY['name']}.
{COMPANY['logo_emoji']} {get_text(COMPANY['tagline'], lang)}

PERSONNALITE: {persona.get('personality', 'Professionnel et sympathique')}

REGLES IMPORTANTES:
- {lang_rule}{response_lang_rule}
- Tu poses UNE question a la fois
- Tu attends la reponse avant de continuer
- Tu es conversationnel, pas formel
- Tu NE generes JAMAIS de code
- Tu t'adaptes aux reponses du user
- Tu connais bien le contexte algerien
{pro_direct_rules}

CONTRAINTES IA FACTORY ALGERIA (a mentionner si pertinent):
- Paiement: {payment_providers} (pas Stripe, pas PayPal)
- Monnaie: {ALGERIA_CONTEXT['currency']}
- Telephone: {ALGERIA_CONTEXT['phone_prefix']}
- Villes principales: {cities}
- Langues supportees: {', '.join(ALGERIA_CONTEXT['languages'])}
- Stack par defaut: {default_stack}

CHAINE AGENTS (phases actives):
- accueil: orchestrator (Accueil + cadrage rapide)
- brainstorm: analyst (Clarifier le besoin)
- validation: orchestrator (Valider la direction)
- preparation: orchestrator (Preparer le prompt Bolt)
- generation: orchestrator (Generer le livrable)

CONTEXTE PROJET ACTUEL:
{self._format_project_context(project)}
"""

        phase_instructions = {
            ConversationPhase.ACCUEIL: """
PHASE: ACCUEIL
Tu accueilles le user et tu proposes directement une direction.
- Tu demandes UNE info bloquante max
- Tu donnes une decision et un plan court
""",
            ConversationPhase.BRAINSTORM: """
PHASE: BRAINSTORM (tu es l'Analyst)
Tu clarifies rapidement l'idee:
- Tu assumes les details manquants
- Tu proposes une solution unique
- Tu poses UNE seule question bloquante si necessaire
""",
            ConversationPhase.CADRAGE: """
PHASE: CADRAGE (tu es le PM)
Tu definis un MVP unique, sans options.
- Tu imposes un scope clair et court
- Tu livres un plan en 3-5 etapes
""",
            ConversationPhase.ARCHITECTURE: """
PHASE: ARCHITECTURE (tu es l'Architect)
Tu proposes UNE architecture directe:
- Stack unique (par defaut: {default_stack})
- Decisions simples et executables
""",
            ConversationPhase.UX: """
PHASE: UX (tu es l'UX Designer)
Tu proposes un parcours utilisateur direct.
- Tu donnes un flow simple
- Tu listes les ecrans essentiels
- Tu gardes une seule question si besoin
""",
            ConversationPhase.VALIDATION: """
PHASE: VALIDATION
Tu résumes TOUT ce qui a été décidé:
- Description du projet
- Features retenues
- Stack technique
- Prochaines étapes

Demande au user: "Confirme pour lancer."
""",
            ConversationPhase.CREATION: """
PHASE: CRÉATION
Le projet est en cours de création dans Archon.
Informe le user de l'avancement.
""",
            ConversationPhase.PREPARATION: """
PHASE: PRÉPARATION
Tu prépares les instructions pour Bolt.
Montre au user ce que tu vas demander à Bolt.
Demande: "Confirme si je lance."
""",
            ConversationPhase.GENERATION: """
PHASE: GÉNÉRATION
Bolt génère le code.
Le user voit son projet prendre forme!
""",
        }

        return base + phase_instructions.get(phase, "")

    def _format_project_context(self, project: ProjectState) -> str:
        """Formate le contexte projet pour le prompt"""
        parts = []
        if project.name:
            parts.append(f"- Nom: {project.name}")
        if project.type:
            parts.append(f"- Type: {project.type}")
        if project.description:
            parts.append(f"- Description: {project.description}")
        if project.features:
            parts.append(f"- Features: {', '.join(project.features)}")
        if project.stack:
            parts.append(f"- Stack: {', '.join(project.stack)}")
        if project.constraints:
            parts.append(f"- Contraintes: {', '.join(project.constraints)}")
        if project.decisions:
            parts.append(f"- Décisions: {project.decisions}")

        return "\n".join(parts) if parts else "Aucun contexte encore"

    def extract_project_info_from_messages(self, messages: list[Message]) -> ProjectState:
"""
        Extrait les informations projet des messages de conversation.
        Analyse le contenu pour détecter type, features, stack, etc.
"""
        project = ProjectState()
        full_text = " ".join(m.content for m in messages if m.role == "user").lower()

        # Détection du type
        if any(w in full_text for w in ["frontend", "react", "vue", "ui", "interface"]):
            project.type = "frontend"
            project.stack = ["react", "vite", "tailwind"]
        if any(w in full_text for w in ["backend", "api", "server", "fastapi", "base de données"]):
            if project.type == "frontend":
                project.type = "fullstack"
                project.stack.extend(["fastapi", "postgresql"])
            else:
                project.type = "backend"
                project.stack = ["fastapi", "postgresql"]
        if not project.type:
            project.type = "fullstack"
            project.stack = ["react", "vite", "tailwind", "fastapi", "postgresql"]

        # Détection des features
        feature_keywords = {
            "authentification": "auth",
            "login": "auth",
            "inscription": "auth",
            "paiement": "payment",
            "facturation": "billing",
            "facture": "billing",
            "dashboard": "dashboard",
            "tableau de bord": "dashboard",
            "chat": "chat",
            "messagerie": "chat",
            "notification": "notifications",
            "profil": "profile",
            "utilisateur": "users",
            "admin": "admin",
            "statistiques": "analytics",
            "recherche": "search",
            "panier": "cart",
            "commande": "orders",
            "produit": "products",
            "counter": "counter",
            "compteur": "counter",
            "todo": "todo",
            "liste": "list",
        }
        for keyword, feature in feature_keywords.items():
            if keyword in full_text and feature not in project.features:
                project.features.append(feature)

        # Contraintes algériennes
        if any(w in full_text for w in ["algérie", "algeria", "dz", "dzd", "dinar"]):
            project.constraints.append("locale:dz")
        if any(w in full_text for w in ["chargily", "paiement", "payment"]):
            project.constraints.append("payment:chargily")
        if any(w in full_text for w in ["darija", "arabe", "arabic"]):
            project.constraints.append("i18n:ar,fr,darija")

        # Description (premier message user)
        user_messages = [m for m in messages if m.role == "user"]
        if user_messages:
            project.description = user_messages[0].content[:500]

        return project

    def build_bolt_prompt(self, project: ProjectState) -> str:
        """Construit le prompt final pour Bolt"""
        parts = [
            f"# Projet: {project.name or 'Mon Projet'}",
            f"\n## Type: {project.type}",
            f"\n## Description\n{project.description}",
        ]

        if project.features:
            parts.append(f"\n## Features à implémenter\n- " + "\n- ".join(project.features))

        if project.stack:
            parts.append(f"\n## Stack technique\n- " + "\n- ".join(project.stack))

        if project.constraints:
            parts.append(f"\n## Contraintes\n- " + "\n- ".join(project.constraints))

        if project.decisions:
            parts.append(f"\n## Décisions prises")
            for agent, decisions in project.decisions.items():
                parts.append(f"\n### {agent}\n{decisions}")

        parts.append("\n\n## Instructions")
        parts.append("Génère le code complet pour ce projet avec tous les fichiers nécessaires.")
        parts.append("Utilise les meilleures pratiques et une architecture propre.")

        return "\n".join(parts)


# Instance globale
conversation_manager = ConversationManager()