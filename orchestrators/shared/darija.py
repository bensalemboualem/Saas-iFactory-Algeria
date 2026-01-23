"""
Darija (Algerian Arabic) Support for IA Factory.
Provides translation and content generation in Darija dialect.
"""

import os
import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel


# ============ DARIJA TRANSLATIONS ============

DARIJA_TRANSLATIONS = {
    # Greetings
    "hello": "Salam",
    "welcome": "Marhba bik",
    "goodbye": "Bslama",
    "good_morning": "Sbah lkhir",
    "good_evening": "Msa lkhir",

    # Common phrases
    "yes": "Ih",
    "no": "La",
    "ok": "Wakha",
    "thank_you": "Sahit",
    "please": "3afak",
    "sorry": "Smahli",
    "no_problem": "Makanch mochkil",

    # Questions
    "how_are_you": "Labas 3lik?",
    "what_is_this": "Chnou hada?",
    "where": "Fin?",
    "when": "Imta?",
    "why": "3lach?",
    "how_much": "Bchhal?",

    # Actions
    "wait": "Stenna",
    "come": "Arwah",
    "go": "Sir",
    "look": "Chouf",
    "listen": "Sme3",
    "understand": "Fhemt",
    "want": "Bghit",
    "need": "Khassni",

    # UI Elements
    "login": "Dkhol",
    "logout": "Khrej",
    "submit": "Sift",
    "cancel": "Annuler",
    "save": "Hfed",
    "delete": "Mhhi",
    "edit": "Beddel",
    "search": "9elleb",
    "loading": "Stenna...",
    "error": "Kayn mochkil",
    "success": "Temmam",

    # Business
    "invoice": "Facture",
    "payment": "Khlass",
    "price": "Thaman",
    "total": "L'majmou3",
    "discount": "Tkhfid",
    "tax": "Dariba",

    # Numbers (informal)
    "zero": "Sifr",
    "one": "Wahed",
    "two": "Jouj",
    "three": "Tlata",
    "four": "Rb3a",
    "five": "Khamsa",
    "six": "Setta",
    "seven": "Sb3a",
    "eight": "Tmanya",
    "nine": "Ts3oud",
    "ten": "3achra",
    "hundred": "Mya",
    "thousand": "Alf",

    # Time
    "today": "Lyoum",
    "yesterday": "Lbareh",
    "tomorrow": "Ghodwa",
    "now": "Daba",
    "later": "Men ba3d",
    "morning": "Sbah",
    "evening": "L3chiya",
    "night": "Lil",

    # Expressions
    "good": "Mezyan",
    "bad": "Khayeb",
    "a_lot": "Bezaf",
    "a_little": "Chwiya",
    "fast": "Degya",
    "slow": "B'chwiya",
    "easy": "Sahel",
    "difficult": "S3ib",

    # Tech/App specific
    "app": "Application",
    "account": "Compte",
    "password": "Mot de passe",
    "email": "Email",
    "phone": "Telephone",
    "message": "Message",
    "notification": "Notification",
    "settings": "Paramètres",
    "help": "L'msa3da",
}

# Darija conversation starters for AI
DARIJA_PROMPTS = {
    "assistant_intro": "Salam! Ana l'assistant dyal IA Factory. Kifach n9der n3awnek lyoum?",
    "ask_clarification": "Mafehmtech mezyan. T9der t3awedli 3afak?",
    "processing": "Stenna chwiya, rani nkheddem 3la talabek...",
    "done": "Temmam! Hak l'jawab:",
    "error_occurred": "Smahli, kayn mochkil. 3awed jarreb men ba3d.",
    "anything_else": "Kayn chi haja khra bghiti?",
    "goodbye": "Bslama! Ila l'li9a!",
}


class DarijaContent(BaseModel):
    """Content in Darija"""
    original: str  # Original text (FR/EN)
    darija: str    # Darija translation
    phonetic: str | None = None  # Optional phonetic guide


class DarijaService:
    """
    Service for Darija language support.
    Handles translations, content generation, and localization.
    """

    SUPPORTED_LANGS = ["fr", "ar", "darija", "en"]

    def __init__(self, translations_path: str | None = None):
        """
        Initialize the Darija service.

        Args:
            translations_path: Path to translations directory (default: ./i18n)
        """
        if translations_path:
            self.translations_path = Path(translations_path)
        else:
            self.translations_path = Path(__file__).parent / "i18n"

        self.translations: dict[str, dict] = {}
        self._load_all_translations()

    def _load_all_translations(self):
        """Load all translation files"""
        for lang in self.SUPPORTED_LANGS:
            file_path = self.translations_path / f"{lang}.json"
            if file_path.exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    self.translations[lang] = json.load(f)

        # Also load inline Darija translations
        if "darija" not in self.translations:
            self.translations["darija"] = {}

        # Merge with DARIJA_TRANSLATIONS
        self.translations["darija"]["inline"] = DARIJA_TRANSLATIONS

    def translate(
        self,
        key: str,
        lang: str = "darija",
        section: str = "common",
        default: str | None = None
    ) -> str:
        """
        Translate a key to the specified language.

        Args:
            key: Translation key
            lang: Target language (fr, ar, darija, en)
            section: Section in translation file (common, auth, etc.)
            default: Default value if not found

        Returns:
            Translated string
        """
        if lang not in self.translations:
            return default or key

        lang_dict = self.translations[lang]

        # Try section.key first
        if section in lang_dict and key in lang_dict[section]:
            return lang_dict[section][key]

        # Try inline translations for Darija
        if lang == "darija" and "inline" in lang_dict:
            if key in lang_dict["inline"]:
                return lang_dict["inline"][key]

        # Try flat key
        if key in lang_dict:
            return lang_dict[key]

        return default or key

    def t(self, key: str, lang: str = "darija") -> str:
        """Shorthand for translate"""
        return self.translate(key, lang)

    def get_darija_prompt(self, prompt_key: str) -> str:
        """
        Get a Darija conversation prompt.

        Args:
            prompt_key: Key from DARIJA_PROMPTS

        Returns:
            Darija prompt string
        """
        return DARIJA_PROMPTS.get(prompt_key, "")

    def format_currency(self, amount: float, lang: str = "darija") -> str:
        """
        Format currency amount in DZD.

        Args:
            amount: Amount in DZD
            lang: Language for formatting

        Returns:
            Formatted string
        """
        if lang == "darija":
            return f"{amount:,.0f} DA"
        elif lang == "ar":
            return f"{amount:,.0f} د.ج"
        else:
            return f"{amount:,.0f} DZD"

    def format_date(self, date_str: str, lang: str = "darija") -> str:
        """
        Format date string.

        Args:
            date_str: ISO date string
            lang: Target language

        Returns:
            Formatted date
        """
        from datetime import datetime

        try:
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))

            if lang == "darija":
                # Day/Month/Year format common in Algeria
                return dt.strftime("%d/%m/%Y")
            elif lang == "ar":
                return dt.strftime("%Y/%m/%d")
            else:
                return dt.strftime("%d/%m/%Y")
        except Exception:
            return date_str

    async def generate_darija_content(
        self,
        text_fr: str,
        llm_client: Any = None
    ) -> DarijaContent:
        """
        Generate Darija translation using LLM.

        Args:
            text_fr: French text to translate
            llm_client: LLM client for translation

        Returns:
            DarijaContent with translation
        """
        if not llm_client:
            # Fallback to simple word replacement
            darija_text = self._simple_translate(text_fr)
            return DarijaContent(
                original=text_fr,
                darija=darija_text
            )

        # Use LLM for translation
        prompt = f"""Traduis ce texte français en Darija algérien (dialecte algérien).

Règles:
- Utilise l'alphabet latin (pas l'arabe)
- Garde un style conversationnel et naturel
- Utilise les chiffres pour les sons arabes (3 = ع, 9 = ق, 7 = ح)
- Garde les termes techniques en français si nécessaire

Texte: {text_fr}

Traduction Darija:"""

        try:
            response = await llm_client.generate(prompt)
            darija_text = response.strip()

            return DarijaContent(
                original=text_fr,
                darija=darija_text
            )
        except Exception:
            return DarijaContent(
                original=text_fr,
                darija=self._simple_translate(text_fr)
            )

    def _simple_translate(self, text: str) -> str:
        """
        Simple word-by-word translation fallback.

        Args:
            text: Text to translate

        Returns:
            Partially translated text
        """
        result = text.lower()

        # Common French to Darija replacements
        replacements = {
            "bonjour": "salam",
            "merci": "sahit",
            "s'il vous plaît": "3afak",
            "oui": "ih",
            "non": "la",
            "comment": "kifach",
            "pourquoi": "3lach",
            "quand": "imta",
            "où": "fin",
            "bien": "mezyan",
            "beaucoup": "bezaf",
            "un peu": "chwiya",
            "maintenant": "daba",
            "aujourd'hui": "lyoum",
            "demain": "ghodwa",
            "hier": "lbareh",
        }

        for fr, dz in replacements.items():
            result = result.replace(fr, dz)

        return result

    def get_all_translations(self, lang: str) -> dict:
        """
        Get all translations for a language.

        Args:
            lang: Language code

        Returns:
            All translations dict
        """
        return self.translations.get(lang, {})

    def detect_language(self, text: str) -> str:
        """
        Simple language detection.

        Args:
            text: Text to analyze

        Returns:
            Detected language code
        """
        # Check for Arabic script
        if any("\u0600" <= char <= "\u06ff" for char in text):
            return "ar"

        # Check for common Darija patterns
        darija_markers = ["3", "7", "9", "wesh", "kifach", "bezaf", "daba"]
        text_lower = text.lower()
        if any(marker in text_lower for marker in darija_markers):
            return "darija"

        # Default to French (most common in Algeria)
        return "fr"


# Singleton instance
_darija_service: DarijaService | None = None


def get_darija_service() -> DarijaService:
    """Get or create the Darija service singleton"""
    global _darija_service
    if _darija_service is None:
        _darija_service = DarijaService()
    return _darija_service
