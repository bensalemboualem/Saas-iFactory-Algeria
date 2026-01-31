"""
Archon Branding - Configuration multilingue pour l'Algérie
Support: Arabe (ar), Français (fr), Anglais (en)
"""

from enum import Enum
from typing import Any


class Language(str, Enum):
    """Langues supportées"""
    AR = "ar"      # العربية
    FR = "fr"      # Français
    EN = "en"      # English
    DZ = "dz"      # Darija (dialecte algérien)
    BER = "ber"    # Tamazight/Amazigh


# ============ ARCHON BRANDING ============

ARCHON_BRANDING = {
    "name": "Archon",
    "title": {
        "ar": "أرشون - مدير المعرفة",
        "fr": "Archon - Gestionnaire de Connaissances",
        "en": "Archon - Knowledge Manager",
        "dz": "Archon - Gestionnaire ta3 el ma3rifa",
    },
    "description": {
        "ar": "مصدر الحقيقة لقاعدة المعرفة وإدارة المهام",
        "fr": "Source de vérité pour Knowledge Base et Task Management",
        "en": "Source of truth for Knowledge Base and Task Management",
        "dz": "Source ta3 el vérité l'KB w Task Management",
    },
    "avatar": "📚",
    "version": "1.0.0",
}


# ============ AGENT NAMES (Algerian Arabic Names) ============
# Ces agents peuvent être assignés aux tâches

ARCHON_AGENTS = {
    # === Knowledge Base Agents ===
    "kb_manager": {
        "name": {
            "ar": "منير",
            "fr": "Mounir",
            "en": "Mounir",
        },
        "title": {
            "ar": "مدير قاعدة المعرفة",
            "fr": "Gestionnaire KB",
            "en": "KB Manager",
        },
        "avatar": "📖",
        "personality": {
            "ar": "منظم يدير المعرفة بدقة",
            "fr": "L'organisé qui gère le savoir",
            "en": "The organizer who manages knowledge",
        },
    },
    "indexer": {
        "name": {
            "ar": "سمير",
            "fr": "Samir",
            "en": "Samir",
        },
        "title": {
            "ar": "مفهرس الوثائق",
            "fr": "Indexeur de Documents",
            "en": "Document Indexer",
        },
        "avatar": "🔍",
        "personality": {
            "ar": "الدقيق الذي يفهرس كل شيء",
            "fr": "Le précis qui indexe tout",
            "en": "The precise one who indexes everything",
        },
    },
    "searcher": {
        "name": {
            "ar": "نسرين",
            "fr": "Nesrine",
            "en": "Nesrine",
        },
        "title": {
            "ar": "باحثة المعلومات",
            "fr": "Chercheuse d'Informations",
            "en": "Information Searcher",
        },
        "avatar": "🎯",
        "personality": {
            "ar": "الذكية التي تجد كل شيء",
            "fr": "L'intelligente qui trouve tout",
            "en": "The smart one who finds everything",
        },
    },

    # === Task Management Agents ===
    "task_manager": {
        "name": {
            "ar": "عمر",
            "fr": "Omar",
            "en": "Omar",
        },
        "title": {
            "ar": "مدير المهام",
            "fr": "Gestionnaire de Tâches",
            "en": "Task Manager",
        },
        "avatar": "✅",
        "personality": {
            "ar": "المنظم الذي يتابع كل مهمة",
            "fr": "L'organisé qui suit chaque tâche",
            "en": "The organized one who tracks every task",
        },
    },
    "prioritizer": {
        "name": {
            "ar": "ليلى",
            "fr": "Leila",
            "en": "Leila",
        },
        "title": {
            "ar": "منظمة الأولويات",
            "fr": "Organisatrice des Priorités",
            "en": "Priority Organizer",
        },
        "avatar": "📊",
        "personality": {
            "ar": "الاستراتيجية التي ترتب الأولويات",
            "fr": "La stratège qui organise les priorités",
            "en": "The strategist who organizes priorities",
        },
    },

    # === Sync Agents ===
    "sync_master": {
        "name": {
            "ar": "كريم",
            "fr": "Karim",
            "en": "Karim",
        },
        "title": {
            "ar": "مدير التزامن",
            "fr": "Maître de Synchronisation",
            "en": "Sync Master",
        },
        "avatar": "🔄",
        "personality": {
            "ar": "الدقيق الذي يزامن كل شيء",
            "fr": "Le précis qui synchronise tout",
            "en": "The precise one who syncs everything",
        },
    },
    "git_watcher": {
        "name": {
            "ar": "ياسين",
            "fr": "Yacine",
            "en": "Yacine",
        },
        "title": {
            "ar": "مراقب Git",
            "fr": "Surveillant Git",
            "en": "Git Watcher",
        },
        "avatar": "👁️",
        "personality": {
            "ar": "اليقظ الذي يراقب التغييرات",
            "fr": "Le vigilant qui surveille les changements",
            "en": "The vigilant one watching changes",
        },
    },

    # === Project Agents ===
    "project_coordinator": {
        "name": {
            "ar": "فاطمة",
            "fr": "Fatima",
            "en": "Fatima",
        },
        "title": {
            "ar": "منسقة المشاريع",
            "fr": "Coordinatrice de Projets",
            "en": "Project Coordinator",
        },
        "avatar": "📋",
        "personality": {
            "ar": "المنظمة التي تنسق المشاريع",
            "fr": "L'organisée qui coordonne les projets",
            "en": "The organized one coordinating projects",
        },
    },
}


# ============ STATUS LABELS (i18n) ============

TASK_STATUS_LABELS = {
    "todo": {
        "ar": "للعمل",
        "fr": "À faire",
        "en": "To Do",
        "dz": "Bech yed'dir",
    },
    "doing": {
        "ar": "قيد العمل",
        "fr": "En cours",
        "en": "In Progress",
        "dz": "F'trig",
    },
    "done": {
        "ar": "منجز",
        "fr": "Terminé",
        "en": "Done",
        "dz": "Kmel",
    },
    "blocked": {
        "ar": "محظور",
        "fr": "Bloqué",
        "en": "Blocked",
        "dz": "Mbloki",
    },
}

PROJECT_STATUS_LABELS = {
    "active": {
        "ar": "نشط",
        "fr": "Actif",
        "en": "Active",
    },
    "paused": {
        "ar": "متوقف",
        "fr": "En pause",
        "en": "Paused",
    },
    "completed": {
        "ar": "مكتمل",
        "fr": "Terminé",
        "en": "Completed",
    },
    "archived": {
        "ar": "مؤرشف",
        "fr": "Archivé",
        "en": "Archived",
    },
}


# ============ ERROR MESSAGES (i18n) ============

ERROR_MESSAGES = {
    "not_found": {
        "ar": "غير موجود",
        "fr": "Non trouvé",
        "en": "Not found",
    },
    "unauthorized": {
        "ar": "غير مصرح",
        "fr": "Non autorisé",
        "en": "Unauthorized",
    },
    "server_error": {
        "ar": "خطأ في الخادم",
        "fr": "Erreur serveur",
        "en": "Server error",
    },
    "invalid_request": {
        "ar": "طلب غير صالح",
        "fr": "Requête invalide",
        "en": "Invalid request",
    },
    "connection_failed": {
        "ar": "فشل الاتصال",
        "fr": "Connexion échouée",
        "en": "Connection failed",
    },
    "kb_not_initialized": {
        "ar": "قاعدة المعرفة غير مهيأة",
        "fr": "Knowledge Base non initialisée",
        "en": "Knowledge Base not initialized",
    },
}


# ============ SUCCESS MESSAGES (i18n) ============

SUCCESS_MESSAGES = {
    "document_created": {
        "ar": "تم إنشاء الوثيقة بنجاح",
        "fr": "Document créé avec succès",
        "en": "Document created successfully",
    },
    "document_deleted": {
        "ar": "تم حذف الوثيقة",
        "fr": "Document supprimé",
        "en": "Document deleted",
    },
    "task_created": {
        "ar": "تم إنشاء المهمة",
        "fr": "Tâche créée",
        "en": "Task created",
    },
    "task_updated": {
        "ar": "تم تحديث المهمة",
        "fr": "Tâche mise à jour",
        "en": "Task updated",
    },
    "project_created": {
        "ar": "تم إنشاء المشروع",
        "fr": "Projet créé",
        "en": "Project created",
    },
    "sync_completed": {
        "ar": "اكتملت المزامنة",
        "fr": "Synchronisation terminée",
        "en": "Sync completed",
    },
    "sync_started": {
        "ar": "بدأت المزامنة",
        "fr": "Synchronisation démarrée",
        "en": "Sync started",
    },
}


# ============ UI LABELS (i18n) ============

UI_LABELS = {
    "search": {
        "ar": "بحث",
        "fr": "Rechercher",
        "en": "Search",
    },
    "filter": {
        "ar": "تصفية",
        "fr": "Filtrer",
        "en": "Filter",
    },
    "create": {
        "ar": "إنشاء",
        "fr": "Créer",
        "en": "Create",
    },
    "delete": {
        "ar": "حذف",
        "fr": "Supprimer",
        "en": "Delete",
    },
    "edit": {
        "ar": "تعديل",
        "fr": "Modifier",
        "en": "Edit",
    },
    "save": {
        "ar": "حفظ",
        "fr": "Enregistrer",
        "en": "Save",
    },
    "cancel": {
        "ar": "إلغاء",
        "fr": "Annuler",
        "en": "Cancel",
    },
    "loading": {
        "ar": "جاري التحميل...",
        "fr": "Chargement...",
        "en": "Loading...",
    },
    "no_results": {
        "ar": "لا توجد نتائج",
        "fr": "Aucun résultat",
        "en": "No results",
    },
    "documents": {
        "ar": "الوثائق",
        "fr": "Documents",
        "en": "Documents",
    },
    "projects": {
        "ar": "المشاريع",
        "fr": "Projets",
        "en": "Projects",
    },
    "tasks": {
        "ar": "المهام",
        "fr": "Tâches",
        "en": "Tasks",
    },
    "knowledge_base": {
        "ar": "قاعدة المعرفة",
        "fr": "Base de Connaissances",
        "en": "Knowledge Base",
    },
}


# ============ HELPER FUNCTIONS ============

def get_text(translations: dict, lang: str = "fr") -> str:
    """
    Récupère le texte dans la langue spécifiée.
    Fallback: fr -> en -> première valeur disponible
    """
    if lang in translations:
        return translations[lang]
    if "fr" in translations:
        return translations["fr"]
    if "en" in translations:
        return translations["en"]
    return next(iter(translations.values()), "")


def get_agent_info(agent_id: str, lang: str = "fr") -> dict[str, Any]:
    """
    Récupère les informations d'un agent dans la langue spécifiée.
    """
    agent = ARCHON_AGENTS.get(agent_id)
    if not agent:
        return {"name": agent_id, "title": agent_id, "avatar": "🤖"}

    return {
        "id": agent_id,
        "name": get_text(agent.get("name", {}), lang),
        "title": get_text(agent.get("title", {}), lang),
        "avatar": agent.get("avatar", "🤖"),
        "personality": get_text(agent.get("personality", {}), lang),
    }


def get_all_agents(lang: str = "fr") -> list[dict[str, Any]]:
    """
    Récupère tous les agents dans la langue spécifiée.
    """
    return [get_agent_info(agent_id, lang) for agent_id in ARCHON_AGENTS]


def get_status_label(status: str, status_type: str = "task", lang: str = "fr") -> str:
    """
    Récupère le label d'un statut dans la langue spécifiée.
    """
    labels = TASK_STATUS_LABELS if status_type == "task" else PROJECT_STATUS_LABELS
    return get_text(labels.get(status, {"fr": status, "en": status}), lang)


def get_error_message(error_type: str, lang: str = "fr") -> str:
    """
    Récupère un message d'erreur dans la langue spécifiée.
    """
    return get_text(ERROR_MESSAGES.get(error_type, ERROR_MESSAGES["server_error"]), lang)


def get_success_message(message_type: str, lang: str = "fr") -> str:
    """
    Récupère un message de succès dans la langue spécifiée.
    """
    return get_text(SUCCESS_MESSAGES.get(message_type, {}), lang)


def get_ui_label(label_key: str, lang: str = "fr") -> str:
    """
    Récupère un label UI dans la langue spécifiée.
    """
    return get_text(UI_LABELS.get(label_key, {"fr": label_key, "en": label_key}), lang)


def detect_language(text: str) -> str:
    """
    Détecte la langue du texte.
    """
    # Caractères arabes
    if any('\u0600' <= c <= '\u06FF' for c in text):
        return "ar"

    # Caractères Tifinagh (Amazigh)
    if any('\u2D30' <= c <= '\u2D7F' for c in text):
        return "ber"

    # Mots clés Darija
    dz_keywords = ["wesh", "kif", "rak", "raki", "ki", "wach", "bech", "goul", "had"]
    lower = text.lower()
    if any(kw in lower for kw in dz_keywords):
        return "dz"

    # Mots clés anglais
    en_keywords = ["the", "is", "are", "what", "how", "can", "please", "help"]
    if any(f" {kw} " in f" {lower} " for kw in en_keywords):
        return "en"

    # Défaut: français
    return "fr"


# ============ THEME CONFIGURATION ============

THEME_CONFIG = {
    "light": {
        "primary": "#1890ff",
        "background": "#ffffff",
        "text": "#000000",
        "border": "#d9d9d9",
        "success": "#52c41a",
        "warning": "#faad14",
        "error": "#ff4d4f",
    },
    "dark": {
        "primary": "#177ddc",
        "background": "#141414",
        "text": "#ffffff",
        "border": "#434343",
        "success": "#49aa19",
        "warning": "#d89614",
        "error": "#d32029",
    },
}


def get_theme(mode: str = "light") -> dict:
    """
    Récupère la configuration du thème.
    """
    return THEME_CONFIG.get(mode, THEME_CONFIG["light"])
