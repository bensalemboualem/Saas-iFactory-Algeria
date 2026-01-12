"""
DARIJA_NLP - Convertisseur Arabizi → Arabe
==========================================
Translitération de l'arabizi (arabe en caractères latins)
vers l'arabe standard pour la darija algérienne
"""

import re
from typing import Dict, List, Tuple, Optional


# ============================================
# MAPPING ARABIZI → ARABE
# ============================================

# Mapping principal : lettres arabes
# Ordre important : patterns longs avant courts
ARABIZI_MAP: Dict[str, str] = {
    # Digraphes et trigraphes (DOIVENT être en premier)
    "tch": "تش",      # comme dans "match"
    "dj": "ج",        # djazair → جزائر
    "dji": "جي",
    "kh": "خ",        # khouya → خويا
    "gh": "غ",        # ghali → غالي
    "ch": "ش",        # chhal → شحال
    "sh": "ش",        # shukran
    "th": "ث",        # thalatha
    "dh": "ذ",        # dhahab
    
    # Chiffres représentant des lettres arabes
    "3'": "غ",        # 3' = غ (parfois utilisé)
    "3": "ع",         # 3abd → عبد
    "7'": "خ",        # 7' = خ (parfois utilisé)
    "7": "ح",         # 7bibti → حبيبتي
    "9": "ق",         # 9alb → قلب
    "5": "خ",         # 5ouya → خويا
    "2": "ء",         # as2al → أسأل
    "6": "ط",         # 6ayeb → طايب
    "8": "ه",         # 8adi → هذي
    
    # Lettres simples
    "a": "ا",
    "b": "ب",
    "t": "ت",
    "j": "ج",
    "h": "ه",         # ou ح selon contexte
    "d": "د",
    "r": "ر",
    "z": "ز",
    "s": "س",
    "f": "ف",
    "q": "ق",
    "k": "ك",
    "l": "ل",
    "m": "م",
    "n": "ن",
    "w": "و",
    "y": "ي",
    "i": "ي",
    "o": "و",
    "u": "و",
    "e": "ا",         # neutre
    "p": "ب",         # pas de P en arabe
    "v": "ف",         # pas de V en arabe
    "g": "ڨ",         # son G algérien (guaf)
    "x": "كس",
    "c": "س",         # ou ك selon contexte
}

# Mapping pour voyelles longues
LONG_VOWELS: Dict[str, str] = {
    "aa": "ا",
    "ee": "ي",
    "ii": "ي",
    "oo": "و",
    "ou": "و",
    "uu": "و",
}


# ============================================
# DICTIONNAIRE DARIJA → ARABE
# ============================================

# Mots darija courants avec leur transcription arabe
DARIJA_WORDS: Dict[str, str] = {
    # Salutations
    "salam": "سلام",
    "salamo": "سلام",
    "salam3alikom": "السلام عليكم",
    "salam3likom": "السلام عليكم",
    "sbah": "صباح",
    "sba7": "صباح",
    "sbahkhir": "صباح الخير",
    "sba7lkhir": "صباح الخير",
    "msa": "مساء",
    "msalkhir": "مساء الخير",
    "bslama": "بالسلامة",
    "beslama": "بالسلامة",
    
    # Pronoms et questions
    "ana": "أنا",
    "nta": "نت",
    "nti": "نتي",
    "howa": "هو",
    "hiya": "هي",
    "7na": "حنا",
    "hna": "حنا",
    "houma": "هوما",
    "ntoma": "نتوما",
    "wach": "واش",
    "wash": "واش",
    "ach": "آش",
    "chkoun": "شكون",
    "chkon": "شكون",
    "kifach": "كيفاش",
    "ki": "كي",
    "kif": "كيف",
    "win": "وين",
    "fayn": "فين",
    "feen": "فين",
    "wa9tach": "وقتاش",
    "waqtach": "وقتاش",
    "3lach": "علاش",
    "3lah": "علاه",
    "alash": "علاش",
    "chhal": "شحال",
    "ch7al": "شحال",
    "9adach": "قداش",
    "gadach": "قداش",
    
    # Verbes courants
    "ndir": "ندير",
    "dir": "دير",
    "diri": "ديري",
    "dirli": "ديرلي",
    "roh": "روح",
    "rohi": "روحي",
    "rou7": "روح",
    "n7eb": "نحب",
    "nheb": "نحب",
    "7ab": "حب",
    "hab": "حب",
    "bghit": "بغيت",
    "bghiti": "بغيتي",
    "nebghi": "نبغي",
    "ra7": "راح",
    "rah": "راه",
    "rahi": "راهي",
    "kayn": "كاين",
    "kayna": "كاينة",
    "makaynch": "ماكاينش",
    "makanch": "ماكانش",
    "3andi": "عندي",
    "3andek": "عندك",
    "3andkom": "عندكم",
    "khdem": "خدم",
    "nkhdem": "نخدم",
    "koul": "كول",
    "kliti": "كليتي",
    "chreb": "شرب",
    "chrebt": "شربت",
    "chouf": "شوف",
    "choufi": "شوفي",
    "nchouf": "نشوف",
    "sme3": "سمع",
    "sme3t": "سمعت",
    "goul": "قول",
    "gouli": "قولي",
    "goulili": "قوليلي",
    "ngoul": "نقول",
    "9oul": "قول",
    "n9oul": "نقول",
    "kteb": "كتب",
    "nekteb": "نكتب",
    "9ra": "قرا",
    "ne9ra": "نقرا",
    "fhem": "فهم",
    "nefhem": "نفهم",
    "3ref": "عرف",
    "n3ref": "نعرف",
    "3awed": "عاود",
    "n3awed": "نعاود",
    
    # Adverbes et expressions
    "bzaf": "بزاف",
    "bezzaf": "بزاف",
    "chwiya": "شوية",
    "chewya": "شوية",
    "daba": "دابا",
    "drk": "دروك",
    "dork": "دروك",
    "derouk": "دروك",
    "lyoum": "ليوم",
    "ghda": "غدا",
    "ghodwa": "غدوة",
    "lbare7": "البارح",
    "lbar7": "البارح",
    "hna": "هنا",
    "lhih": "لهيه",
    "temma": "تما",
    "lahna": "لهنا",
    "temak": "تماك",
    "mlih": "مليح",
    "mli7": "مليح",
    "mezian": "مزيان",
    "khir": "خير",
    "hder": "هدر",
    "sahha": "صحة",
    "sa7a": "صحة",
    "saha": "صحة",
    "sahtkom": "صحتكم",
    "sa7tkom": "صحتكم",
    "y3aychek": "يعيشك",
    "ya3tik": "يعطيك",
    "ya3tik esa7a": "يعطيك الصحة",
    "baraka": "بركة",
    "allah ybarek": "الله يبارك",
    "nchallah": "نشاء الله",
    "inchallah": "إن شاء الله",
    "inchaallah": "إن شاء الله",
    "mabrouk": "مبروك",
    "mabrok": "مبروك",
    
    # Négation
    "ma": "ما",
    "machi": "ماشي",
    "mafish": "مافيش",
    "mafihch": "مافيهش",
    "makaynch": "ماكاينش",
    "manebghich": "مانبغيش",
    "mandirich": "ماندیرش",
    "la": "لا",
    "lala": "لالا",
    
    # Famille
    "khouya": "خويا",
    "khoya": "خويا",
    "5oya": "خويا",
    "khti": "ختي",
    "5ti": "ختي",
    "mama": "ماما",
    "yemma": "يما",
    "baba": "بابا",
    "babou": "بابو",
    "jeddi": "جدي",
    "jedi": "جدي",
    "mima": "ميمة",
    "lwalid": "لوالد",
    "lwalida": "لوالدة",
    "dar": "دار",
    "el3ayla": "العايلة",
    
    # Argent et commerce
    "flouss": "فلوس",
    "flous": "فلوس",
    "drahm": "دراهم",
    "dinar": "دينار",
    "chtara": "شطارة",
    "chtar": "شطار",
    "bya3": "بياع",
    "chriti": "شريتي",
    "nechri": "نشري",
    "bghali": "بغالي",
    "rkhis": "رخيص",
    
    # Travail et administration
    "khdma": "خدمة",
    "khedma": "خدمة",
    "bureau": "بيرو",
    "byro": "بيرو",
    "casnos": "كاسنوس",
    "cnas": "كناس",
    "daira": "دائرة",
    "baladia": "بلدية",
    "wilaya": "ولاية",
    "carte": "كارت",
    "tasjil": "تسجيل",
    "tesjil": "تسجيل",
    "dossier": "دوسي",
    "dossy": "دوسي",
    "papier": "بابي",
    "wra9": "وراق",
    "wraq": "وراق",
    
    # Nourriture
    "makla": "ماكلة",
    "el9ahwa": "القهوة",
    "kahwa": "قهوة",
    "atay": "اتاي",
    "lham": "لحم",
    "djaj": "دجاج",
    "7out": "حوت",
    "hout": "حوت",
    "khobz": "خبز",
    "kesra": "كسرة",
    "couscous": "كسكسي",
    "chorba": "شوربة",
    "rechta": "رشتة",
    
    # Transport
    "tomobil": "طوموبيل",
    "taxi": "تاكسي",
    "bus": "بيس",
    "tram": "ترام",
    "train": "تران",
    "metro": "ميترو",
    "gare": "ڨار",
    "aeropor": "ايروبور",
    "matat": "مطار",
}


# ============================================
# FONCTIONS DE DÉTECTION
# ============================================

def is_arabizi(text: str) -> bool:
    """
    Détecter si le texte est en arabizi.
    
    Critères:
    - Contient des caractères latins
    - Contient des chiffres utilisés comme lettres arabes (3, 7, 9, etc.)
    - OU contient des mots darija connus en latinisé
    """
    if not text:
        return False
    
    text_lower = text.lower()
    
    # Vérifier la présence de chiffres-lettres arabes
    if re.search(r'[3579]', text):
        return True
    
    # Vérifier les patterns arabizi typiques
    arabizi_patterns = [
        r'\bkh[oa]',      # khouya, khoya
        r'\b[a-z]*ch[a-z]*\b',  # chhal, wach
        r'\bgh[a-z]+\b',  # ghali
        r'\b3[a-z]+\b',   # 3abd
        r'\b7[a-z]+\b',   # 7bibti
        r'\bdj[a-z]+\b',  # djazair
    ]
    
    for pattern in arabizi_patterns:
        if re.search(pattern, text_lower):
            return True
    
    # Vérifier les mots darija connus
    words = text_lower.split()
    darija_count = sum(1 for w in words if w in DARIJA_WORDS)
    
    # Si plus de 20% des mots sont des mots darija connus
    if len(words) > 0 and darija_count / len(words) > 0.2:
        return True
    
    return False


def get_arabizi_score(text: str) -> float:
    """
    Calculer un score de probabilité que le texte soit de l'arabizi.
    
    Returns:
        float: Score entre 0 et 1
    """
    if not text:
        return 0.0
    
    text_lower = text.lower()
    words = text_lower.split()
    
    if not words:
        return 0.0
    
    score = 0.0
    
    # Points pour chiffres-lettres
    if re.search(r'[3]', text):
        score += 0.2
    if re.search(r'[7]', text):
        score += 0.2
    if re.search(r'[9]', text):
        score += 0.15
    if re.search(r'[5]', text):
        score += 0.1
    
    # Points pour digraphes arabizi
    if re.search(r'kh|gh|ch|sh|dj', text_lower):
        score += 0.2
    
    # Points pour mots darija connus
    darija_count = sum(1 for w in words if w in DARIJA_WORDS)
    score += min(darija_count / len(words), 0.4)
    
    return min(score, 1.0)


# ============================================
# CONVERSION ARABIZI → ARABE
# ============================================

def arabizi_to_arabic(text: str, use_dictionary: bool = True) -> str:
    """
    Convertir du texte arabizi en arabe.
    
    Pipeline:
    1. Recherche de mots dans le dictionnaire
    2. Conversion des patterns longs (kh, gh, ch, etc.)
    3. Conversion des chiffres-lettres (3, 7, 9)
    4. Conversion lettre par lettre
    5. Nettoyage final
    
    Args:
        text: Texte en arabizi
        use_dictionary: Utiliser le dictionnaire de mots
    
    Returns:
        Texte en arabe
    """
    if not text:
        return ""
    
    result = text.lower()
    
    # 1. Remplacer les mots complets du dictionnaire
    if use_dictionary:
        words = result.split()
        converted_words = []
        
        for word in words:
            # Nettoyer la ponctuation
            prefix = ""
            suffix = ""
            clean_word = word
            
            # Extraire ponctuation début
            while clean_word and not clean_word[0].isalnum():
                prefix += clean_word[0]
                clean_word = clean_word[1:]
            
            # Extraire ponctuation fin
            while clean_word and not clean_word[-1].isalnum():
                suffix = clean_word[-1] + suffix
                clean_word = clean_word[:-1]
            
            # Vérifier le dictionnaire
            if clean_word.lower() in DARIJA_WORDS:
                converted_words.append(prefix + DARIJA_WORDS[clean_word.lower()] + suffix)
            else:
                # Conversion caractère par caractère
                converted = _convert_word(clean_word)
                converted_words.append(prefix + converted + suffix)
        
        result = ' '.join(converted_words)
    else:
        result = _convert_word(result)
    
    # Nettoyage final
    result = re.sub(r'\s+', ' ', result)
    result = result.strip()
    
    return result


def _convert_word(word: str) -> str:
    """Convertir un mot arabizi en arabe caractère par caractère."""
    if not word:
        return ""
    
    result = word.lower()
    
    # Convertir les voyelles longues d'abord
    for pattern, replacement in LONG_VOWELS.items():
        result = result.replace(pattern, replacement)
    
    # Convertir les patterns longs avant les courts
    # Trier par longueur décroissante
    sorted_patterns = sorted(ARABIZI_MAP.keys(), key=len, reverse=True)
    
    for pattern in sorted_patterns:
        if pattern in result:
            result = result.replace(pattern, ARABIZI_MAP[pattern])
    
    return result


def convert_with_context(text: str) -> Tuple[str, List[Tuple[str, str]]]:
    """
    Convertir avec tracking des conversions effectuées.
    
    Returns:
        Tuple[str, List[Tuple[str, str]]]: (texte converti, liste des conversions)
    """
    conversions = []
    result = text.lower()
    
    # Mots du dictionnaire
    words = result.split()
    for word in words:
        clean_word = re.sub(r'[^\w]', '', word)
        if clean_word.lower() in DARIJA_WORDS:
            conversions.append((clean_word, DARIJA_WORDS[clean_word.lower()]))
    
    # Patterns arabizi
    for pattern, replacement in ARABIZI_MAP.items():
        if pattern in result:
            conversions.append((pattern, replacement))
    
    converted = arabizi_to_arabic(text)
    
    return converted, conversions


# ============================================
# UTILITAIRES
# ============================================

def get_common_darija_words() -> List[str]:
    """Retourner la liste des mots darija courants."""
    return list(DARIJA_WORDS.keys())


def add_darija_word(arabizi: str, arabic: str) -> None:
    """Ajouter un mot au dictionnaire darija."""
    DARIJA_WORDS[arabizi.lower()] = arabic


def get_arabizi_examples() -> List[Tuple[str, str]]:
    """Retourner des exemples de conversion arabizi → arabe."""
    examples = [
        ("salam khoya kifach", "سلام خويا كيفاش"),
        ("wach rak lyoum", "واش راك ليوم"),
        ("n7eb ndir tasjil casnos", "نحب ندير تسجيل كاسنوس"),
        ("3andi mochkil m3a lkhedma", "عندي مشكل مع الخدمة"),
        ("bezaf mlih sahha", "بزاف مليح صحة"),
    ]
    return examples
