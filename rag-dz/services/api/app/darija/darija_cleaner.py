"""
DARIJA_NLP - Cleaner / Nettoyeur
================================
Nettoyage de texte darija/arabe/arabizi
Suppression bruit, répétitions, harakat
"""

import re
import unicodedata
from typing import List, Optional, Set, Tuple


# ============================================
# CONSTANTES ARABES
# ============================================

# Plages Unicode arabes
ARABIC_RANGE = '\u0600-\u06FF'
ARABIC_SUPPLEMENT = '\u0750-\u077F'
ARABIC_EXTENDED_A = '\u08A0-\u08FF'
ARABIC_PRESENTATION_A = '\uFB50-\uFDFF'
ARABIC_PRESENTATION_B = '\uFE70-\uFEFF'

# Pattern caractères arabes
ARABIC_PATTERN = f'[{ARABIC_RANGE}{ARABIC_SUPPLEMENT}{ARABIC_EXTENDED_A}]'

# Harakat (diacritiques arabes / voyelles)
HARAKAT = (
    '\u064B'  # FATHATAN
    '\u064C'  # DAMMATAN
    '\u064D'  # KASRATAN
    '\u064E'  # FATHA
    '\u064F'  # DAMMA
    '\u0650'  # KASRA
    '\u0651'  # SHADDA
    '\u0652'  # SUKUN
    '\u0653'  # MADDAH
    '\u0654'  # HAMZA ABOVE
    '\u0655'  # HAMZA BELOW
    '\u0656'  # SUBSCRIPT ALEF
    '\u0670'  # SUPERSCRIPT ALEF
)

# Tatweel (kashida - étirement)
TATWEEL = '\u0640'

# Normalisation des variantes d'alef
ALEF_VARIANTS = {
    'أ': 'ا',  # ALEF WITH HAMZA ABOVE
    'إ': 'ا',  # ALEF WITH HAMZA BELOW
    'آ': 'ا',  # ALEF WITH MADDA
    'ٱ': 'ا',  # ALEF WASLA
    'ٲ': 'ا',  # ALEF WITH WAVY HAMZA ABOVE
    'ٳ': 'ا',  # ALEF WITH WAVY HAMZA BELOW
}

# Normalisation ya/alef maqsura
YA_VARIANTS = {
    'ى': 'ي',  # ALEF MAKSURA → YA
    'ئ': 'ي',  # YA WITH HAMZA
}

# Normalisation ta marbuta
TA_MARBUTA = {
    'ة': 'ه',  # TA MARBUTA → HA (optionnel selon contexte)
}

# Mots de bruit à supprimer
NOISE_WORDS = {
    # Rires et expressions
    'hhh', 'hhhh', 'hhhhh', 'hahaha', 'haha', 'hihi', 'hoho',
    'lol', 'lool', 'loool', 'mdr', 'mdrrr', 'ptdr', 'xd', 'xdd',
    # Interjections vides
    'euh', 'euhhh', 'hmm', 'hmmm', 'mmm', 'ahh', 'ohh', 'bah',
    # Expressions internet
    'omg', 'wtf', 'btw', 'idk', 'tbh',
}

# Mots darija de remplissage (à garder mais normaliser)
FILLER_WORDS = {
    'wah', 'wllh', 'wlh', 'wallah', 'walah',
    'sah', 'sahha', 'sahhit', 'sahit',
    'ok', 'okay', 'oky', 'oki',
    'yaw', 'yaww', 'yaaw',
}


# ============================================
# FONCTIONS DE NETTOYAGE
# ============================================

def remove_harakat(text: str) -> str:
    """
    Supprimer les harakat (diacritiques/voyelles arabes).
    
    Les harakat sont les petits signes au-dessus/dessous des lettres
    qui indiquent les voyelles courtes.
    """
    if not text:
        return ""
    
    # Supprimer chaque haraka
    for h in HARAKAT:
        text = text.replace(h, '')
    
    return text


def remove_tatweel(text: str) -> str:
    """Supprimer les tatweel (kashida - étirements)."""
    return text.replace(TATWEEL, '')


def normalize_arabic_chars(text: str, normalize_ta_marbuta: bool = False) -> str:
    """
    Normaliser les variantes de caractères arabes.
    
    - أ/إ/آ → ا (alef)
    - ى → ي (ya)
    - ة → ه (optionnel)
    """
    if not text:
        return ""
    
    # Normaliser alef
    for old, new in ALEF_VARIANTS.items():
        text = text.replace(old, new)
    
    # Normaliser ya
    for old, new in YA_VARIANTS.items():
        text = text.replace(old, new)
    
    # Normaliser ta marbuta (optionnel)
    if normalize_ta_marbuta:
        for old, new in TA_MARBUTA.items():
            text = text.replace(old, new)
    
    return text


def remove_emojis(text: str) -> str:
    """Supprimer les emojis du texte."""
    if not text:
        return ""
    
    # Pattern pour les emojis (plages Unicode)
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & pictographs
        "\U0001F680-\U0001F6FF"  # Transport & map
        "\U0001F700-\U0001F77F"  # Alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric shapes
        "\U0001F800-\U0001F8FF"  # Supplemental arrows
        "\U0001F900-\U0001F9FF"  # Supplemental symbols
        "\U0001FA00-\U0001FA6F"  # Chess symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and pictographs
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251"  # Enclosed characters
        "]+",
        flags=re.UNICODE
    )
    
    return emoji_pattern.sub('', text)


def remove_urls(text: str) -> str:
    """Supprimer les URLs."""
    # Pattern pour les URLs
    url_pattern = r'https?://\S+|www\.\S+'
    return re.sub(url_pattern, '', text)


def remove_emails(text: str) -> str:
    """Supprimer les adresses email."""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.sub(email_pattern, '', text)


def remove_phone_numbers(text: str) -> str:
    """Supprimer les numéros de téléphone."""
    # Pattern pour numéros algériens et internationaux
    patterns = [
        r'\+?213\s*[0-9\s\-]{8,}',  # Algérie
        r'\+?41\s*[0-9\s\-]{8,}',   # Suisse
        r'\+?33\s*[0-9\s\-]{8,}',   # France
        r'0[567]\d{8}',             # Mobiles DZ
        r'0[23]\d{7,8}',            # Fixes DZ
    ]
    for pattern in patterns:
        text = re.sub(pattern, '', text)
    return text


def remove_repeated_chars(text: str, max_repeat: int = 2) -> str:
    """
    Réduire les répétitions de caractères.
    
    "salammmmmm" → "salamm" (max 2)
    "hhhhhh" → "hh"
    """
    if not text:
        return ""
    
    # Pattern pour 3+ répétitions du même caractère
    pattern = r'(.)\1{' + str(max_repeat) + r',}'
    return re.sub(pattern, r'\1' * max_repeat, text)


def remove_repeated_words(text: str) -> str:
    """
    Supprimer les mots répétés consécutifs.
    
    "salam salam salam" → "salam"
    "w w w" → "w"
    """
    if not text:
        return ""
    
    words = text.split()
    result = []
    prev_word = None
    
    for word in words:
        if word.lower() != prev_word:
            result.append(word)
        prev_word = word.lower()
    
    return ' '.join(result)


def clean_noise(text: str) -> str:
    """
    Nettoyer le bruit du texte.
    
    - Supprimer "hhh", "lol", "mdr"
    - Réduire répétitions
    - Normaliser espaces
    """
    if not text:
        return ""
    
    # Minuscules pour comparaison
    words = text.split()
    cleaned_words = []
    
    for word in words:
        # Vérifier si c'est un mot de bruit
        word_lower = word.lower()
        if word_lower not in NOISE_WORDS:
            # Réduire les répétitions dans le mot
            cleaned_word = remove_repeated_chars(word, max_repeat=2)
            cleaned_words.append(cleaned_word)
    
    # Supprimer les mots répétés
    result = ' '.join(cleaned_words)
    result = remove_repeated_words(result)
    
    return result


def clean_text(
    text: str,
    remove_emojis_flag: bool = True,
    remove_urls_flag: bool = True,
    remove_emails_flag: bool = True,
    remove_phones_flag: bool = True,
    remove_harakat_flag: bool = True,
    normalize_chars: bool = True,
    reduce_repeats: bool = True,
    remove_noise: bool = True,
) -> str:
    """
    Nettoyage complet du texte darija/arabe.
    
    Pipeline:
    1. Supprimer URLs
    2. Supprimer emails
    3. Supprimer numéros
    4. Supprimer emojis
    5. Supprimer harakat
    6. Supprimer tatweel
    7. Normaliser caractères arabes
    8. Réduire répétitions
    9. Nettoyer bruit
    10. Normaliser espaces
    """
    if not text:
        return ""
    
    # 1. URLs
    if remove_urls_flag:
        text = remove_urls(text)
    
    # 2. Emails
    if remove_emails_flag:
        text = remove_emails(text)
    
    # 3. Numéros de téléphone
    if remove_phones_flag:
        text = remove_phone_numbers(text)
    
    # 4. Emojis
    if remove_emojis_flag:
        text = remove_emojis(text)
    
    # 5. Harakat
    if remove_harakat_flag:
        text = remove_harakat(text)
    
    # 6. Tatweel
    text = remove_tatweel(text)
    
    # 7. Normaliser caractères arabes
    if normalize_chars:
        text = normalize_arabic_chars(text)
    
    # 8. Réduire répétitions
    if reduce_repeats:
        text = remove_repeated_chars(text)
    
    # 9. Nettoyer bruit
    if remove_noise:
        text = clean_noise(text)
    
    # 10. Normaliser espaces
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text


# ============================================
# TOKENIZATION ARABE/DARIJA
# ============================================

def tokenize_arabic(text: str, keep_punctuation: bool = False) -> List[str]:
    """
    Tokenization simple pour texte arabe/darija.
    
    Sépare les mots sur les espaces et la ponctuation.
    """
    if not text:
        return []
    
    # Nettoyer le texte d'abord
    text = clean_text(text, remove_noise=False)
    
    if keep_punctuation:
        # Garder la ponctuation comme tokens séparés
        pattern = r'(\s+|[،؛؟!.,;:?!\-\(\)\[\]{}«»""\'\"]+)'
        tokens = re.split(pattern, text)
        tokens = [t.strip() for t in tokens if t.strip()]
    else:
        # Supprimer la ponctuation
        text = re.sub(r'[،؛؟!.,;:?!\-\(\)\[\]{}«»""\'\"]+', ' ', text)
        tokens = text.split()
    
    return tokens


def tokenize_sentences(text: str) -> List[str]:
    """
    Segmenter le texte en phrases.
    
    Détecte les fins de phrases arabes et latines.
    """
    if not text:
        return []
    
    # Patterns de fin de phrase
    sentence_end = r'[.!?؟。،]+'
    
    # Split sur les fins de phrase
    sentences = re.split(f'({sentence_end})', text)
    
    # Recombiner les phrases avec leur ponctuation
    result = []
    current = ""
    
    for part in sentences:
        if re.match(sentence_end, part):
            current += part
            if current.strip():
                result.append(current.strip())
            current = ""
        else:
            current += part
    
    if current.strip():
        result.append(current.strip())
    
    return result


# ============================================
# DÉTECTION DE CONTENU
# ============================================

def has_arabic(text: str) -> bool:
    """Vérifier si le texte contient des caractères arabes."""
    return bool(re.search(ARABIC_PATTERN, text))


def has_latin(text: str) -> bool:
    """Vérifier si le texte contient des caractères latins."""
    return bool(re.search(r'[a-zA-Z]', text))


def get_arabic_ratio(text: str) -> float:
    """Calculer le ratio de caractères arabes dans le texte."""
    if not text:
        return 0.0
    
    total_chars = len([c for c in text if c.isalpha()])
    if total_chars == 0:
        return 0.0
    
    arabic_chars = len(re.findall(ARABIC_PATTERN, text))
    return arabic_chars / total_chars


def count_words(text: str) -> int:
    """Compter le nombre de mots."""
    tokens = tokenize_arabic(text)
    return len(tokens)


# ============================================
# NORMALISATION AVANCÉE
# ============================================

def normalize_punctuation(text: str) -> str:
    """Normaliser la ponctuation arabe/latine."""
    replacements = {
        '،': ',',  # Virgule arabe → latine
        '؛': ';',  # Point-virgule arabe
        '؟': '?',  # Point d'interrogation arabe
        '٪': '%',  # Pourcentage arabe
        '٫': '.',  # Séparateur décimal arabe
        '٬': ',',  # Séparateur milliers arabe
        '«': '"',
        '»': '"',
        '"': '"',
        '"': '"',
        ''': "'",
        ''': "'",
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text


def normalize_numbers_arabic(text: str) -> str:
    """Convertir les chiffres arabes-indiens en chiffres arabes occidentaux."""
    arabic_to_western = {
        '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4',
        '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9',
    }
    
    for ar, west in arabic_to_western.items():
        text = text.replace(ar, west)
    
    return text


def clean_for_search(text: str) -> str:
    """
    Nettoyage optimisé pour la recherche.
    
    - Supprime tout le bruit
    - Normalise tous les caractères
    - Minuscules
    """
    text = clean_text(text)
    text = normalize_arabic_chars(text, normalize_ta_marbuta=True)
    text = normalize_punctuation(text)
    text = normalize_numbers_arabic(text)
    text = text.lower()
    return text
