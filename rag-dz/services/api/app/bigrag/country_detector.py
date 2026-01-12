"""
BIG RAG - Country Detector
==========================
Détection intelligente du pays (DZ/CH/GLOBAL) et de la langue
Basée sur patterns, mots-clés et analyse IA
"""

import re
import logging
from enum import Enum
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass, field
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


# ============================================
# ENUMS & MODELS
# ============================================

class Country(str, Enum):
    """Pays supportés"""
    DZ = "DZ"  # Algérie
    CH = "CH"  # Suisse
    FR = "FR"  # France (fallback francophone)
    GLOBAL = "GLOBAL"  # International


class Language(str, Enum):
    """Langues supportées"""
    FR = "fr"       # Français
    AR = "ar"       # Arabe
    DE = "de"       # Allemand
    IT = "it"       # Italien
    EN = "en"       # Anglais


class CountryDetectionResult(BaseModel):
    """Résultat de détection du pays"""
    country: Country = Field(..., description="Pays détecté")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confiance (0-1)")
    language: Language = Field(..., description="Langue détectée")
    signals: List[str] = Field(default_factory=list, description="Signaux détectés")
    secondary_country: Optional[Country] = Field(None, description="Pays secondaire")
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ============================================
# PATTERNS & KEYWORDS
# ============================================

# 🇩🇿 Patterns Algérie
DZ_PATTERNS = {
    # Organismes officiels
    "cnas": ("CNAS", 0.95),
    "casnos": ("CASNOS", 0.95),
    "cnr": ("CNR (retraite)", 0.85),
    "dgi": ("DGI (impôts)", 0.90),
    "caci": ("CACI (commerce)", 0.85),
    "cnrc": ("CNRC (registre commerce)", 0.90),
    "andi": ("ANDI (investissement)", 0.85),
    "anem": ("ANEM (emploi)", 0.85),
    "ansej": ("ANSEJ", 0.90),
    "angem": ("ANGEM", 0.85),
    "ons": ("ONS (statistiques)", 0.75),
    
    # Impôts et taxes DZ
    "ifu": ("IFU (impôt forfaitaire)", 0.95),
    "irg": ("IRG (impôt revenu)", 0.95),
    "ibs": ("IBS (impôt bénéfices)", 0.95),
    "tva 19%": ("TVA 19%", 0.90),
    "tva 9%": ("TVA 9%", 0.90),
    "tap": ("TAP (activité pro)", 0.90),
    "taic": ("TAIC", 0.85),
    "timbre fiscal": ("Timbre fiscal DZ", 0.80),
    
    # Monnaie et banque
    "dinar": ("Dinar algérien", 0.85),
    "dzd": ("DZD", 0.95),
    "da ": ("DA (Dinar)", 0.80),
    "banque d'algérie": ("Banque d'Algérie", 0.95),
    "bna": ("BNA", 0.75),
    "cpa": ("CPA", 0.75),
    "bea": ("BEA", 0.75),
    "badr": ("BADR", 0.85),
    
    # Géographie
    "wilaya": ("Wilaya", 0.95),
    "daïra": ("Daïra", 0.95),
    "commune": ("Commune", 0.60),
    "alger": ("Alger", 0.85),
    "oran": ("Oran", 0.85),
    "constantine": ("Constantine", 0.85),
    "annaba": ("Annaba", 0.80),
    "sétif": ("Sétif", 0.80),
    "blida": ("Blida", 0.80),
    
    # Termes légaux DZ
    "sarl algérie": ("SARL Algérie", 0.95),
    "eurl": ("EURL", 0.85),
    "spa algérie": ("SPA Algérie", 0.90),
    "code de commerce algérien": ("Code Commerce DZ", 0.95),
    "journal officiel": ("Journal Officiel DZ", 0.85),
    "jora": ("JORA", 0.95),
}

# 🇨🇭 Patterns Suisse
CH_PATTERNS = {
    # Organismes officiels
    "avs": ("AVS (assurance vieillesse)", 0.95),
    "ai ": ("AI (assurance invalidité)", 0.90),
    "lpp": ("LPP (prévoyance)", 0.95),
    "suva": ("SUVA (accidents)", 0.95),
    "afc": ("AFC (administration fiscale)", 0.90),
    "seco": ("SECO", 0.85),
    "ofsp": ("OFSP (santé publique)", 0.85),
    "srf": ("SRF", 0.75),
    "finma": ("FINMA", 0.90),
    
    # Impôts et taxes CH
    "tva 8.1%": ("TVA 8.1%", 0.95),
    "tva 7.7%": ("TVA 7.7%", 0.95),
    "tva 2.6%": ("TVA 2.6%", 0.95),
    "tva 2.5%": ("TVA 2.5%", 0.90),
    "impôt fédéral": ("Impôt fédéral", 0.90),
    "impôt cantonal": ("Impôt cantonal", 0.95),
    "icc": ("ICC (impôt capital)", 0.85),
    "impôt à la source": ("Impôt source CH", 0.85),
    
    # Monnaie et banque
    "franc suisse": ("Franc suisse", 0.95),
    "chf": ("CHF", 0.95),
    "sfr": ("SFr.", 0.90),
    "bnk": ("BNS", 0.85),
    "ubs": ("UBS", 0.80),
    "credit suisse": ("Credit Suisse", 0.85),
    "raiffeisen": ("Raiffeisen", 0.85),
    "postfinance": ("PostFinance", 0.90),
    
    # Géographie
    "canton": ("Canton", 0.90),
    "confédération": ("Confédération", 0.85),
    "commune suisse": ("Commune CH", 0.80),
    "zurich": ("Zurich", 0.85),
    "genève": ("Genève", 0.90),
    "lausanne": ("Lausanne", 0.85),
    "berne": ("Berne", 0.85),
    "bâle": ("Bâle", 0.80),
    "lugano": ("Lugano", 0.80),
    
    # Termes légaux CH
    "sàrl suisse": ("Sàrl Suisse", 0.95),
    "sa suisse": ("SA Suisse", 0.90),
    "raison individuelle": ("Raison individuelle", 0.85),
    "succursale": ("Succursale", 0.80),
    "registre du commerce": ("RC Suisse", 0.85),
    "ide": ("IDE (entreprises)", 0.90),
    "code des obligations": ("CO Suisse", 0.95),
    "loi fédérale": ("Loi fédérale", 0.90),
}

# Patterns de langue
ARABIC_PATTERN = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+')
GERMAN_PATTERNS = [
    r'\bund\b', r'\bdie\b', r'\bder\b', r'\bdas\b', r'\bist\b',
    r'\bfür\b', r'\bmit\b', r'\bauf\b', r'\bein\b', r'\beine\b',
    r'\bwird\b', r'\bsind\b', r'\bbei\b', r'\bnach\b', r'\büber\b',
    r'\bGmbH\b', r'\bAG\b', r'\bKanton\b', r'\bBundes\b',
]
ITALIAN_PATTERNS = [
    r'\bdella\b', r'\bnella\b', r'\bdel\b', r'\bnel\b', r'\bper\b',
    r'\bcon\b', r'\bsono\b', r'\bcome\b', r'\bquesto\b', r'\bquella\b',
    r'\bCantone\b', r'\bTicino\b',
]


# ============================================
# COUNTRY DETECTOR
# ============================================

class CountryDetector:
    """
    Détecteur de pays intelligent pour RAG multi-pays
    Utilise patterns, mots-clés et analyse linguistique
    """
    
    def __init__(self):
        self.dz_patterns = DZ_PATTERNS
        self.ch_patterns = CH_PATTERNS
        
    def detect(self, text: str) -> CountryDetectionResult:
        """
        Détection principale du pays et de la langue
        
        Args:
            text: Texte à analyser
            
        Returns:
            CountryDetectionResult avec pays, confiance, langue et signaux
        """
        if not text or len(text.strip()) < 3:
            return CountryDetectionResult(
                country=Country.GLOBAL,
                confidence=0.0,
                language=Language.FR,
                signals=["Texte trop court"],
            )
        
        text_lower = text.lower()
        
        # 1. Détecter la langue
        language = self._detect_language(text)
        
        # 2. Collecter les signaux DZ
        dz_signals, dz_score = self._collect_signals(text_lower, self.dz_patterns)
        
        # 3. Collecter les signaux CH
        ch_signals, ch_score = self._collect_signals(text_lower, self.ch_patterns)
        
        # 4. Bonus langue
        if language == Language.AR:
            dz_score += 0.30
            dz_signals.append("Texte en arabe (+0.30)")
        elif language == Language.DE:
            ch_score += 0.25
            ch_signals.append("Texte en allemand (+0.25)")
        elif language == Language.IT:
            ch_score += 0.15
            ch_signals.append("Texte en italien (+0.15)")
        
        # 5. Déterminer le pays
        all_signals = dz_signals + ch_signals
        
        if dz_score > ch_score and dz_score > 0.3:
            country = Country.DZ
            confidence = min(dz_score, 1.0)
            secondary = Country.CH if ch_score > 0.2 else Country.GLOBAL
            signals = dz_signals
        elif ch_score > dz_score and ch_score > 0.3:
            country = Country.CH
            confidence = min(ch_score, 1.0)
            secondary = Country.DZ if dz_score > 0.2 else Country.GLOBAL
            signals = ch_signals
        else:
            country = Country.GLOBAL
            confidence = max(0.5, 1.0 - max(dz_score, ch_score))
            secondary = Country.DZ if dz_score > ch_score else Country.CH
            signals = ["Aucun signal pays spécifique détecté"]
        
        logger.debug(f"Country detection: {country} (conf={confidence:.2f}), lang={language}")
        
        return CountryDetectionResult(
            country=country,
            confidence=round(confidence, 2),
            language=language,
            signals=signals[:10],  # Top 10 signaux
            secondary_country=secondary,
            metadata={
                "dz_score": round(dz_score, 2),
                "ch_score": round(ch_score, 2),
                "text_length": len(text),
            },
        )
    
    def _detect_language(self, text: str) -> Language:
        """Détecter la langue du texte"""
        
        # Arabe
        arabic_chars = len(ARABIC_PATTERN.findall(text))
        if arabic_chars > len(text) * 0.1:  # Plus de 10% de caractères arabes
            return Language.AR
        
        text_lower = text.lower()
        
        # Allemand
        german_count = sum(1 for p in GERMAN_PATTERNS if re.search(p, text_lower))
        if german_count >= 3:
            return Language.DE
        
        # Italien
        italian_count = sum(1 for p in ITALIAN_PATTERNS if re.search(p, text_lower))
        if italian_count >= 3:
            return Language.IT
        
        # Anglais (quelques indicateurs)
        english_words = ['the', 'is', 'are', 'have', 'has', 'this', 'that', 'with']
        english_count = sum(1 for w in english_words if f" {w} " in f" {text_lower} ")
        if english_count >= 3:
            return Language.EN
        
        # Par défaut: Français
        return Language.FR
    
    def _collect_signals(
        self, 
        text: str, 
        patterns: Dict[str, Tuple[str, float]]
    ) -> Tuple[List[str], float]:
        """
        Collecter les signaux et calculer le score
        
        Returns:
            Tuple (liste de signaux, score total)
        """
        signals = []
        total_score = 0.0
        
        for pattern, (label, weight) in patterns.items():
            if pattern in text:
                signals.append(f"{label} (+{weight:.2f})")
                total_score += weight
        
        return signals, total_score
    
    def detect_from_query(self, query: str) -> CountryDetectionResult:
        """Wrapper pour détection depuis une requête utilisateur"""
        return self.detect(query)
    
    def get_primary_index(self, result: CountryDetectionResult) -> str:
        """Retourne le nom de l'index Qdrant principal"""
        index_map = {
            Country.DZ: "rag_dz",
            Country.CH: "rag_ch",
            Country.GLOBAL: "rag_global",
            Country.FR: "rag_global",
        }
        return index_map.get(result.country, "rag_global")
    
    def get_secondary_index(self, result: CountryDetectionResult) -> str:
        """Retourne le nom de l'index Qdrant secondaire"""
        if result.secondary_country:
            index_map = {
                Country.DZ: "rag_dz",
                Country.CH: "rag_ch",
                Country.GLOBAL: "rag_global",
            }
            return index_map.get(result.secondary_country, "rag_global")
        return "rag_global"


# ============================================
# SINGLETON
# ============================================

country_detector = CountryDetector()


# ============================================
# UTILITY FUNCTIONS
# ============================================

async def detect_country(text: str) -> CountryDetectionResult:
    """
    Fonction utilitaire pour détection asynchrone
    
    Args:
        text: Texte à analyser
        
    Returns:
        CountryDetectionResult
    """
    return country_detector.detect(text)


def get_country_emoji(country: Country) -> str:
    """Retourne l'emoji du drapeau"""
    emojis = {
        Country.DZ: "🇩🇿",
        Country.CH: "🇨🇭",
        Country.FR: "🇫🇷",
        Country.GLOBAL: "🌍",
    }
    return emojis.get(country, "🌍")


def get_country_name(country: Country) -> str:
    """Retourne le nom du pays"""
    names = {
        Country.DZ: "Algérie",
        Country.CH: "Suisse",
        Country.FR: "France",
        Country.GLOBAL: "International",
    }
    return names.get(country, "International")
