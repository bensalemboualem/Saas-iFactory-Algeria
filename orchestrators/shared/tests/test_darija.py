"""Tests pour le service Darija"""

import pytest
from pathlib import Path

from shared.darija import (
    DarijaService,
    DarijaContent,
    DARIJA_TRANSLATIONS,
    DARIJA_PROMPTS,
    get_darija_service,
)


class TestDarijaTranslations:
    """Tests des traductions Darija"""

    def test_translations_defined(self):
        """Test que les traductions sont définies"""
        assert len(DARIJA_TRANSLATIONS) > 0

    def test_common_words(self):
        """Test mots courants"""
        assert DARIJA_TRANSLATIONS["hello"] == "Salam"
        assert DARIJA_TRANSLATIONS["welcome"] == "Marhba bik"
        assert DARIJA_TRANSLATIONS["goodbye"] == "Bslama"
        assert DARIJA_TRANSLATIONS["yes"] == "Ih"
        assert DARIJA_TRANSLATIONS["no"] == "La"

    def test_ui_elements(self):
        """Test éléments UI"""
        assert DARIJA_TRANSLATIONS["login"] == "Dkhol"
        assert DARIJA_TRANSLATIONS["logout"] == "Khrej"
        assert DARIJA_TRANSLATIONS["loading"] == "Stenna..."
        assert DARIJA_TRANSLATIONS["error"] == "Kayn mochkil"
        assert DARIJA_TRANSLATIONS["success"] == "Temmam"

    def test_numbers(self):
        """Test nombres"""
        assert DARIJA_TRANSLATIONS["one"] == "Wahed"
        assert DARIJA_TRANSLATIONS["two"] == "Jouj"
        assert DARIJA_TRANSLATIONS["hundred"] == "Mya"


class TestDarijaPrompts:
    """Tests des prompts Darija"""

    def test_prompts_defined(self):
        """Test que les prompts sont définis"""
        assert len(DARIJA_PROMPTS) > 0

    def test_assistant_intro(self):
        """Test intro assistant"""
        intro = DARIJA_PROMPTS["assistant_intro"]
        assert "Salam" in intro
        assert "IA Factory" in intro

    def test_processing(self):
        """Test message processing"""
        processing = DARIJA_PROMPTS["processing"]
        assert "Stenna" in processing

    def test_error_message(self):
        """Test message erreur"""
        error = DARIJA_PROMPTS["error_occurred"]
        assert "mochkil" in error


class TestDarijaService:
    """Tests du service Darija"""

    @pytest.fixture
    def service(self, tmp_path):
        """Service avec traductions mock"""
        # Créer fichier de traductions temporaire
        i18n_path = tmp_path / "i18n"
        i18n_path.mkdir()

        darija_json = i18n_path / "darija.json"
        darija_json.write_text('{"common": {"hello": "Salam"}}')

        fr_json = i18n_path / "fr.json"
        fr_json.write_text('{"common": {"hello": "Bonjour"}}')

        return DarijaService(str(i18n_path))

    def test_translate_darija(self, service):
        """Test traduction vers Darija"""
        result = service.translate("hello", "darija", "common")
        assert result == "Salam"

    def test_translate_french(self, service):
        """Test traduction vers Français"""
        result = service.translate("hello", "fr", "common")
        assert result == "Bonjour"

    def test_translate_fallback(self, service):
        """Test fallback si non trouvé"""
        result = service.translate("unknown_key", "darija")
        assert result == "unknown_key"

    def test_shorthand_t(self, service):
        """Test méthode raccourcie t()"""
        result = service.t("hello")
        # Devrait utiliser les traductions inline
        assert result in ["Salam", "hello"]

    def test_get_darija_prompt(self, service):
        """Test récupération prompt"""
        intro = service.get_darija_prompt("assistant_intro")
        assert "Salam" in intro

    def test_format_currency(self, service):
        """Test formatage devise"""
        assert "DA" in service.format_currency(1000, "darija")
        assert "د.ج" in service.format_currency(1000, "ar")
        assert "DZD" in service.format_currency(1000, "fr")

    def test_detect_language_arabic(self, service):
        """Test détection arabe"""
        result = service.detect_language("مرحبا بك")
        assert result == "ar"

    def test_detect_language_darija(self, service):
        """Test détection Darija"""
        result = service.detect_language("Wesh labas 3lik?")
        assert result == "darija"

    def test_detect_language_french(self, service):
        """Test détection Français"""
        result = service.detect_language("Bonjour, comment allez-vous?")
        assert result == "fr"


class TestDarijaContent:
    """Tests du modèle DarijaContent"""

    def test_content_creation(self):
        """Test création contenu"""
        content = DarijaContent(
            original="Bonjour",
            darija="Salam"
        )
        assert content.original == "Bonjour"
        assert content.darija == "Salam"
        assert content.phonetic is None

    def test_content_with_phonetic(self):
        """Test avec phonétique"""
        content = DarijaContent(
            original="Comment vas-tu?",
            darija="Kifach rak?",
            phonetic="kee-fash rak"
        )
        assert content.phonetic == "kee-fash rak"


class TestGetDarijaService:
    """Tests du singleton"""

    def test_singleton(self):
        """Test que c'est un singleton"""
        service1 = get_darija_service()
        service2 = get_darija_service()
        assert service1 is service2
