"""
Règles UI obligatoires pour IA Factory Algérie
Toute interface générée DOIT respecter ces règles

Version: 1.0.0
"""

import re
from typing import Any
from dataclasses import dataclass, field
from enum import Enum


class Severity(str, Enum):
    """Niveau de sévérité des violations"""
    ERROR = "error"      # Bloquant - doit être corrigé
    WARNING = "warning"  # Non-bloquant mais recommandé
    INFO = "info"        # Information


@dataclass
class UIViolation:
    """Violation d'une règle UI"""
    code: str
    message: str
    severity: Severity
    suggestion: str | None = None
    line: int | None = None


@dataclass
class UIValidationResult:
    """Résultat de validation UI"""
    valid: bool
    violations: list[UIViolation] = field(default_factory=list)
    score: int = 100  # Score de conformité 0-100

    def to_dict(self) -> dict:
        return {
            "valid": self.valid,
            "score": self.score,
            "violations": [
                {
                    "code": v.code,
                    "message": v.message,
                    "severity": v.severity.value,
                    "suggestion": v.suggestion,
                    "line": v.line
                }
                for v in self.violations
            ]
        }


# ============ CONFIGURATION UI IA FACTORY ============

UI_RULES = {
    # Responsive mobile-first
    "responsive": {
        "enabled": True,
        "breakpoints": {
            "mobile": "320px",
            "tablet": "768px",
            "desktop": "1024px",
            "wide": "1280px"
        },
        "mobile_first": True
    },

    # 4 langues obligatoires
    "i18n": {
        "languages": ["fr", "ar", "darija", "en"],
        "default": "fr",
        "rtl": ["ar"],
        "fallback": "fr"
    },

    # Couleur principale - Vert Algérien
    "colors": {
        "primary": {
            "DEFAULT": "#00a651",
            "dark": "#008c45",
            "light": "#00c767"
        },
        "accent": {
            "DEFAULT": "#10b981",
            "dark": "#059669"
        }
    },

    # Thème Dark (par défaut)
    "themes": {
        "dark": {
            "background": "#020617",
            "backgroundAlt": "#0a0a0a",
            "card": "#0f172a",
            "cardHover": "#1e293b",
            "header": "#0a0a0a",
            "glass": "rgba(255,255,255,0.08)",
            "textPrimary": "#ffffff",
            "textSecondary": "rgba(255,255,255,0.7)",
            "textMuted": "rgba(255,255,255,0.5)",
            "border": "rgba(255,255,255,0.12)",
            "borderLight": "rgba(255,255,255,0.08)",
            "shadow": "0 20px 60px rgba(0,0,0,0.55)"
        },
        "light": {
            "background": "#f7f5f0",
            "backgroundAlt": "#ffffff",
            "card": "#ffffff",
            "cardHover": "#f1f5f9",
            "header": "#f7f5f0",
            "glass": "rgba(0,0,0,0.04)",
            "textPrimary": "#1a1a1a",
            "textSecondary": "rgba(0,0,0,0.7)",
            "textMuted": "rgba(0,0,0,0.5)",
            "border": "rgba(0,0,0,0.08)",
            "borderLight": "rgba(0,0,0,0.05)",
            "shadow": "0 20px 60px rgba(15,23,42,0.25)"
        }
    },

    # Activation thème
    "theme_config": {
        "attribute": "data-theme",  # <html data-theme="dark">
        "default": "dark",
        "storage_key": "iafactory-theme"
    },

    # Règles Algérie
    "algeria": {
        "payment": "chargily",  # JAMAIS Stripe
        "currency": "DZD",
        "min_amount": 75,  # Minimum Chargily
        "forbidden_providers": ["stripe", "paypal", "square"]
    }
}


# ============ VALIDATION UI ============

def validate_ui(code: str, file_type: str = "auto") -> UIValidationResult:
    """
    Valide que le code respecte les règles UI IA Factory.

    Args:
        code: Code source à valider
        file_type: Type de fichier (tsx, jsx, css, html, auto)

    Returns:
        Résultat de validation avec violations
    """
    violations = []

    # Détection automatique du type
    if file_type == "auto":
        if "import React" in code or "from 'react'" in code:
            file_type = "tsx"
        elif "<style" in code or "{" in code and ":" in code:
            file_type = "css"
        elif "<html" in code or "<!DOCTYPE" in code:
            file_type = "html"
        else:
            file_type = "tsx"

    # === RESPONSIVE ===
    responsive_patterns = [
        r"@media",
        r"sm:|md:|lg:|xl:",  # Tailwind
        r"min-width|max-width",
        r"useMediaQuery|useBreakpoint",
        r"responsive|mobile-first"
    ]
    has_responsive = any(re.search(p, code, re.IGNORECASE) for p in responsive_patterns)

    if not has_responsive and len(code) > 500:
        violations.append(UIViolation(
            code="MISSING_RESPONSIVE",
            message="Pas de media queries ou classes responsive détectées",
            severity=Severity.ERROR,
            suggestion="Ajouter des breakpoints Tailwind (sm:, md:, lg:) ou des @media queries"
        ))

    # === I18N ===
    i18n_patterns = [
        r"useTranslation|useI18n|useLocale",
        r"t\(['\"]|t\(`",  # t('key') ou t(`key`)
        r"<Trans|<FormattedMessage",
        r"i18n|intl|locale",
        r"messages\[|translations\["
    ]
    has_i18n = any(re.search(p, code) for p in i18n_patterns)

    # Texte hardcodé en français (potentiel problème i18n)
    hardcoded_french = re.findall(r'["\']([A-ZÀ-Ÿ][a-zà-ÿ\s]{10,})["\']', code)

    if not has_i18n and hardcoded_french and len(code) > 300:
        violations.append(UIViolation(
            code="MISSING_I18N",
            message="Pas de système i18n détecté, texte hardcodé trouvé",
            severity=Severity.ERROR,
            suggestion="Utiliser useTranslation() de react-i18next ou équivalent"
        ))

    # === RTL SUPPORT ===
    rtl_patterns = [
        r"dir=['\"]rtl['\"]|dir=\{.*rtl",
        r"rtl:|ltr:",  # Tailwind RTL
        r"text-right|text-left",
        r"useDirection|useRTL",
        r"logical|inline-start|inline-end"
    ]
    has_rtl = any(re.search(p, code, re.IGNORECASE) for p in rtl_patterns)

    if not has_rtl and has_i18n:
        violations.append(UIViolation(
            code="MISSING_RTL",
            message="Support RTL non détecté (requis pour l'arabe)",
            severity=Severity.WARNING,
            suggestion="Ajouter dir={locale === 'ar' ? 'rtl' : 'ltr'} sur <html>"
        ))

    # === THEME DARK/LIGHT ===
    theme_patterns = [
        r"data-theme|theme-",
        r"dark:|light:",  # Tailwind dark mode
        r"useTheme|ThemeProvider",
        r"darkMode|dark-mode",
        r"prefers-color-scheme"
    ]
    has_theme = any(re.search(p, code, re.IGNORECASE) for p in theme_patterns)

    if not has_theme and len(code) > 500:
        violations.append(UIViolation(
            code="MISSING_THEME",
            message="Pas de support dark/light mode détecté",
            severity=Severity.WARNING,
            suggestion="Ajouter dark: classes Tailwind ou ThemeProvider"
        ))

    # === COULEUR PRIMAIRE ===
    primary_patterns = [
        r"#00a651|#008c45|#00c767",  # Couleurs exactes
        r"primary|--primary",
        r"bg-primary|text-primary"
    ]
    has_primary = any(re.search(p, code, re.IGNORECASE) for p in primary_patterns)

    # Vérifier couleurs interdites (autres verts qui ne sont pas le vert algérien)
    wrong_greens = re.findall(r'#(?:22c55e|16a34a|15803d|166534)', code, re.IGNORECASE)

    if wrong_greens:
        violations.append(UIViolation(
            code="WRONG_PRIMARY_COLOR",
            message=f"Couleurs non-conformes détectées: {wrong_greens}",
            severity=Severity.WARNING,
            suggestion="Utiliser #00a651 (vert algérien) comme couleur primaire"
        ))

    # === PAIEMENT ALGÉRIE ===
    forbidden_payment = []
    for provider in UI_RULES["algeria"]["forbidden_providers"]:
        if re.search(rf"\b{provider}\b", code, re.IGNORECASE):
            forbidden_payment.append(provider)

    if forbidden_payment:
        violations.append(UIViolation(
            code="FORBIDDEN_PAYMENT",
            message=f"Provider de paiement interdit: {forbidden_payment}",
            severity=Severity.ERROR,
            suggestion="Utiliser Chargily uniquement pour les paiements en Algérie"
        ))

    # Vérifier utilisation de Chargily si paiement détecté
    has_payment = re.search(r"payment|checkout|pay|purchase|buy", code, re.IGNORECASE)
    has_chargily = re.search(r"chargily", code, re.IGNORECASE)

    if has_payment and not has_chargily and not forbidden_payment:
        violations.append(UIViolation(
            code="MISSING_CHARGILY",
            message="Fonctionnalité paiement détectée sans Chargily",
            severity=Severity.INFO,
            suggestion="Intégrer Chargily pour les paiements (DZD uniquement)"
        ))

    # === CALCUL DU SCORE ===
    error_count = sum(1 for v in violations if v.severity == Severity.ERROR)
    warning_count = sum(1 for v in violations if v.severity == Severity.WARNING)

    score = 100 - (error_count * 20) - (warning_count * 5)
    score = max(0, min(100, score))

    return UIValidationResult(
        valid=error_count == 0,
        violations=violations,
        score=score
    )


def validate_ui_strict(code: str) -> UIValidationResult:
    """
    Validation stricte - toutes les règles sont ERROR.
    Utilisé pour la validation finale avant déploiement.
    """
    result = validate_ui(code)

    # Convertir tous les warnings en errors
    for violation in result.violations:
        if violation.severity == Severity.WARNING:
            violation.severity = Severity.ERROR

    error_count = len(result.violations)
    result.valid = error_count == 0
    result.score = max(0, 100 - (error_count * 15))

    return result


# ============ GÉNÉRATEURS DE CONFIG ============

def get_tailwind_config() -> str:
    """Génère la config Tailwind avec les couleurs IA Factory"""
    return '''/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ['class', '[data-theme="dark"]'],
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#00a651',
          dark: '#008c45',
          light: '#00c767',
        },
        background: {
          dark: '#020617',
          light: '#f7f5f0',
        },
        card: {
          dark: '#0f172a',
          light: '#ffffff',
        },
        accent: {
          DEFAULT: '#10b981',
          dark: '#059669',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        arabic: ['Noto Sans Arabic', 'Arial', 'sans-serif'],
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
'''


def get_css_variables() -> str:
    """Génère les variables CSS pour les thèmes"""
    dark = UI_RULES["themes"]["dark"]
    light = UI_RULES["themes"]["light"]
    colors = UI_RULES["colors"]

    return f'''/* IA Factory Design System - CSS Variables */

:root,
[data-theme="light"] {{
  --color-primary: {colors["primary"]["DEFAULT"]};
  --color-primary-dark: {colors["primary"]["dark"]};
  --color-primary-light: {colors["primary"]["light"]};

  --color-background: {light["background"]};
  --color-background-alt: {light["backgroundAlt"]};
  --color-card: {light["card"]};
  --color-card-hover: {light["cardHover"]};
  --color-header: {light["header"]};
  --color-glass: {light["glass"]};

  --color-text-primary: {light["textPrimary"]};
  --color-text-secondary: {light["textSecondary"]};
  --color-text-muted: {light["textMuted"]};

  --color-border: {light["border"]};
  --color-border-light: {light["borderLight"]};
  --shadow: {light["shadow"]};
}}

[data-theme="dark"] {{
  --color-background: {dark["background"]};
  --color-background-alt: {dark["backgroundAlt"]};
  --color-card: {dark["card"]};
  --color-card-hover: {dark["cardHover"]};
  --color-header: {dark["header"]};
  --color-glass: {dark["glass"]};

  --color-text-primary: {dark["textPrimary"]};
  --color-text-secondary: {dark["textSecondary"]};
  --color-text-muted: {dark["textMuted"]};

  --color-border: {dark["border"]};
  --color-border-light: {dark["borderLight"]};
  --shadow: {dark["shadow"]};
}}

/* RTL Support */
[dir="rtl"] {{
  text-align: right;
}}

[dir="rtl"] .text-left {{
  text-align: right;
}}

[dir="rtl"] .text-right {{
  text-align: left;
}}

/* Utility classes */
.bg-primary {{ background-color: var(--color-primary); }}
.text-primary {{ color: var(--color-primary); }}
.border-primary {{ border-color: var(--color-primary); }}

.bg-card {{ background-color: var(--color-card); }}
.bg-background {{ background-color: var(--color-background); }}

.text-primary-content {{ color: var(--color-text-primary); }}
.text-secondary-content {{ color: var(--color-text-secondary); }}
.text-muted {{ color: var(--color-text-muted); }}
'''


def get_i18n_config() -> str:
    """Génère la configuration i18n"""
    return '''// i18n.config.ts - IA Factory i18n Configuration

export const locales = ['fr', 'ar', 'darija', 'en'] as const;
export type Locale = (typeof locales)[number];

export const defaultLocale: Locale = 'fr';

export const localeNames: Record<Locale, string> = {
  fr: 'Français',
  ar: 'العربية',
  darija: 'الدارجة',
  en: 'English',
};

export const rtlLocales: Locale[] = ['ar'];

export function isRTL(locale: Locale): boolean {
  return rtlLocales.includes(locale);
}

export function getDirection(locale: Locale): 'ltr' | 'rtl' {
  return isRTL(locale) ? 'rtl' : 'ltr';
}

// Messages par défaut
export const defaultMessages = {
  fr: {
    common: {
      welcome: 'Bienvenue',
      login: 'Connexion',
      register: 'Inscription',
      logout: 'Déconnexion',
      dashboard: 'Tableau de bord',
      settings: 'Paramètres',
      save: 'Enregistrer',
      cancel: 'Annuler',
      delete: 'Supprimer',
      edit: 'Modifier',
      loading: 'Chargement...',
      error: 'Erreur',
      success: 'Succès',
    },
    payment: {
      amount: 'Montant',
      currency: 'DZD',
      pay: 'Payer',
      checkout: 'Finaliser la commande',
      processing: 'Traitement en cours...',
    },
  },
  ar: {
    common: {
      welcome: 'مرحبا',
      login: 'تسجيل الدخول',
      register: 'إنشاء حساب',
      logout: 'تسجيل الخروج',
      dashboard: 'لوحة التحكم',
      settings: 'الإعدادات',
      save: 'حفظ',
      cancel: 'إلغاء',
      delete: 'حذف',
      edit: 'تعديل',
      loading: 'جاري التحميل...',
      error: 'خطأ',
      success: 'نجاح',
    },
    payment: {
      amount: 'المبلغ',
      currency: 'دج',
      pay: 'ادفع',
      checkout: 'إتمام الطلب',
      processing: 'جاري المعالجة...',
    },
  },
  darija: {
    common: {
      welcome: 'مرحبا بيك',
      login: 'دخول',
      register: 'تسجيل',
      logout: 'خروج',
      dashboard: 'لوحة التحكم',
      settings: 'الإعدادات',
      save: 'سجل',
      cancel: 'إلغي',
      delete: 'حذف',
      edit: 'بدل',
      loading: 'راهو يحمل...',
      error: 'كاين مشكل',
      success: 'تمام',
    },
    payment: {
      amount: 'المبلغ',
      currency: 'دج',
      pay: 'خلص',
      checkout: 'كمل الطلبية',
      processing: 'راهي تتعالج...',
    },
  },
  en: {
    common: {
      welcome: 'Welcome',
      login: 'Login',
      register: 'Sign up',
      logout: 'Logout',
      dashboard: 'Dashboard',
      settings: 'Settings',
      save: 'Save',
      cancel: 'Cancel',
      delete: 'Delete',
      edit: 'Edit',
      loading: 'Loading...',
      error: 'Error',
      success: 'Success',
    },
    payment: {
      amount: 'Amount',
      currency: 'DZD',
      pay: 'Pay',
      checkout: 'Checkout',
      processing: 'Processing...',
    },
  },
};
'''


# ============ EXPORTS ============

__all__ = [
    "UI_RULES",
    "UIViolation",
    "UIValidationResult",
    "Severity",
    "validate_ui",
    "validate_ui_strict",
    "get_tailwind_config",
    "get_css_variables",
    "get_i18n_config",
]
