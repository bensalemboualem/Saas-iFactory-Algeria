"""
Advanced RAG Features for BBC School IA Program
Features for Minister Demo: Quiz, Budget, Comparison, Timeline, etc.
"""

import re
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta


class EducationLevel(str, Enum):
    """Education levels with Arabic names"""
    PRIMARY = "primaire"
    MIDDLE = "college"
    HIGH = "lycee"
    TEACHERS = "enseignants"


class Language(str, Enum):
    """Supported languages"""
    FRENCH = "fr"
    ARABIC = "ar"
    ENGLISH = "en"


# ============================================
# BBC SCHOOL PROGRAM DATA
# ============================================

BBC_PROGRAM_DATA = {
    "program_name": "Programme National IA - BBC School Algérie",
    "launch_date": "2026-02-03",
    "pilot_duration_months": 18,
    "total_schools": 50,
    "total_teachers": 200,
    "total_students_target": 5000,

    "budget": {
        "total_da": 12_500_000,
        "total_usd": 92_592,  # ~135 DA/USD
        "exchange_rate": 135,
        "breakdown": {
            "infrastructure": {"da": 4_000_000, "percent": 32},
            "formation_enseignants": {"da": 3_500_000, "percent": 28},
            "equipement_tech": {"da": 2_500_000, "percent": 20},
            "contenu_pedagogique": {"da": 1_500_000, "percent": 12},
            "suivi_evaluation": {"da": 1_000_000, "percent": 8}
        },
        "per_school": 250_000,
        "per_teacher": 17_500,
        "per_student": 2_500
    },

    "levels": {
        "primaire": {
            "name_fr": "Primaire",
            "name_ar": "ابتدائي",
            "modules": 4,
            "total_hours": 40,
            "age_range": "8-11 ans",
            "modules_list": ["P1", "P2", "P3", "P4"]
        },
        "college": {
            "name_fr": "Collège",
            "name_ar": "متوسط",
            "modules": 6,
            "total_hours": 80,
            "age_range": "12-15 ans",
            "modules_list": ["C1", "C2", "C3", "C4", "C5", "C6"]
        },
        "lycee": {
            "name_fr": "Lycée",
            "name_ar": "ثانوي",
            "modules": 8,
            "total_hours": 120,
            "age_range": "16-18 ans",
            "modules_list": ["L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8"]
        },
        "enseignants": {
            "name_fr": "Enseignants",
            "name_ar": "معلمين",
            "modules": 3,
            "total_hours": 60,
            "levels": {
                "niveau1": {"hours": 40, "name": "Fondamentaux IA"},
                "niveau2": {"hours": 60, "name": "Pédagogie IA"},
                "niveau3": {"hours": 80, "name": "Expert IA"}
            }
        }
    },

    "modules": {
        "L1": {
            "name": "Fondamentaux de l'IA",
            "duration_hours": 12,
            "credits": 3,
            "difficulty": "Débutant",
            "prerequisites": [],
            "objectives": [
                "Comprendre l'histoire de l'IA",
                "Définir Machine Learning vs Deep Learning",
                "Identifier les applications quotidiennes de l'IA"
            ],
            "project": "Chatbot simple avec règles",
            "assessment": "Quiz + Projet pratique"
        },
        "L2": {
            "name": "LLM et Transformers",
            "duration_hours": 16,
            "credits": 4,
            "difficulty": "Intermédiaire",
            "prerequisites": ["L1"],
            "objectives": [
                "Comprendre l'architecture Transformer",
                "Maîtriser le Prompt Engineering",
                "Fine-tuner un modèle FR/AR"
            ],
            "project": "Assistant IA multilingue",
            "assessment": "Projet + Présentation orale"
        },
        "L3": {
            "name": "Vision par Ordinateur",
            "duration_hours": 14,
            "credits": 3,
            "difficulty": "Intermédiaire",
            "prerequisites": ["L1"],
            "objectives": [
                "Comprendre les CNN",
                "Implémenter détection d'objets",
                "Créer système de reconnaissance"
            ],
            "project": "App reconnaissance images",
            "assessment": "Projet technique"
        },
        "L4": {
            "name": "NLP Avancé",
            "duration_hours": 16,
            "credits": 4,
            "difficulty": "Avancé",
            "prerequisites": ["L2"],
            "objectives": [
                "Traitement texte arabe",
                "Analyse de sentiments",
                "Génération de texte"
            ],
            "project": "Analyseur de sentiments AR/FR",
            "assessment": "Projet + Rapport écrit"
        },
        "L5": {
            "name": "IA Générative",
            "duration_hours": 14,
            "credits": 3,
            "difficulty": "Avancé",
            "prerequisites": ["L2", "L3"],
            "objectives": [
                "Comprendre GANs et Diffusion",
                "Générer images et audio",
                "Éthique de l'IA générative"
            ],
            "project": "Générateur d'art IA",
            "assessment": "Portfolio créatif"
        },
        "L6": {
            "name": "Éthique et Société IA",
            "duration_hours": 10,
            "credits": 2,
            "difficulty": "Tous niveaux",
            "prerequisites": [],
            "objectives": [
                "Identifier les biais algorithmiques",
                "Comprendre RGPD et vie privée",
                "Débattre impact sociétal IA"
            ],
            "project": "Analyse de cas éthiques",
            "assessment": "Débat + Essai"
        },
        "L7": {
            "name": "Projet Intégrateur",
            "duration_hours": 20,
            "credits": 5,
            "difficulty": "Avancé",
            "prerequisites": ["L1", "L2", "L3", "L4"],
            "objectives": [
                "Concevoir solution IA complète",
                "Travailler en équipe",
                "Présenter à un jury"
            ],
            "project": "Startup IA fictive",
            "assessment": "Pitch + Démo"
        },
        "L8": {
            "name": "IA et Carrières",
            "duration_hours": 8,
            "credits": 2,
            "difficulty": "Tous niveaux",
            "prerequisites": [],
            "objectives": [
                "Explorer métiers de l'IA",
                "Préparer portfolio",
                "Networking et stages"
            ],
            "project": "Portfolio personnel",
            "assessment": "Entretien simulation"
        },
        "C1": {
            "name": "Découverte de l'IA",
            "duration_hours": 12,
            "credits": 3,
            "difficulty": "Débutant",
            "prerequisites": [],
            "objectives": [
                "Définir l'Intelligence Artificielle",
                "Identifier l'IA au quotidien",
                "Premiers pas en programmation"
            ],
            "project": "Jeu interactif simple",
            "assessment": "Quiz ludique"
        },
        "P1": {
            "name": "L'IA autour de nous",
            "duration_hours": 10,
            "credits": 2,
            "difficulty": "Initiation",
            "prerequisites": [],
            "objectives": [
                "Reconnaître l'IA dans les jeux",
                "Comprendre les assistants vocaux",
                "Créer avec des outils IA simples"
            ],
            "project": "Dessin avec IA",
            "assessment": "Participation + Création"
        }
    },

    "timeline": [
        {"date": "2026-02-03", "event": "Lancement officiel", "phase": "Démarrage"},
        {"date": "2026-02-17", "event": "Formation formateurs Niveau 1", "phase": "Formation"},
        {"date": "2026-03-03", "event": "Début pilote 10 écoles", "phase": "Pilote"},
        {"date": "2026-06-15", "event": "Évaluation mi-parcours", "phase": "Évaluation"},
        {"date": "2026-09-01", "event": "Extension 25 écoles", "phase": "Extension"},
        {"date": "2027-01-15", "event": "Évaluation annuelle", "phase": "Évaluation"},
        {"date": "2027-06-01", "event": "Extension 50 écoles", "phase": "Extension"},
        {"date": "2027-08-01", "event": "Fin pilote - Rapport final", "phase": "Clôture"}
    ],

    "kpis": {
        "students_trained": {"target": 5000, "unit": "élèves"},
        "teachers_certified": {"target": 200, "unit": "enseignants"},
        "schools_equipped": {"target": 50, "unit": "établissements"},
        "satisfaction_rate": {"target": 85, "unit": "%"},
        "completion_rate": {"target": 75, "unit": "%"},
        "employment_rate": {"target": 60, "unit": "% (post-formation)"}
    }
}


# ============================================
# LANGUAGE DETECTION
# ============================================

class LanguageDetector:
    """Detect language from text"""

    ARABIC_PATTERN = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+')

    FRENCH_INDICATORS = [
        "combien", "comment", "pourquoi", "quand", "quel", "quelle",
        "module", "cours", "formation", "budget", "durée", "objectifs",
        "programme", "lycée", "collège", "primaire", "enseignant"
    ]

    ENGLISH_INDICATORS = [
        "how", "what", "when", "where", "why", "which",
        "module", "course", "training", "budget", "duration",
        "program", "school", "teacher", "student"
    ]

    @classmethod
    def detect(cls, text: str) -> Language:
        """Detect the language of input text"""
        # Check for Arabic characters
        if cls.ARABIC_PATTERN.search(text):
            return Language.ARABIC

        text_lower = text.lower()

        # Count language indicators
        french_count = sum(1 for word in cls.FRENCH_INDICATORS if word in text_lower)
        english_count = sum(1 for word in cls.ENGLISH_INDICATORS if word in text_lower)

        if french_count > english_count:
            return Language.FRENCH
        elif english_count > french_count:
            return Language.ENGLISH

        # Default to French
        return Language.FRENCH


# ============================================
# QUIZ GENERATOR
# ============================================

@dataclass
class QuizQuestion:
    """A quiz question with options"""
    question: str
    options: List[str]
    correct_answer: int  # Index of correct option
    explanation: str
    difficulty: str
    module: str
    topic: str


class QuizGenerator:
    """Generate dynamic quizzes for BBC School program"""

    QUIZ_TEMPLATES = {
        "L1": [
            {
                "question": "Quel scientifique est considéré comme le père de l'Intelligence Artificielle?",
                "options": ["Alan Turing", "Bill Gates", "Steve Jobs", "Mark Zuckerberg"],
                "correct": 0,
                "explanation": "Alan Turing a posé les bases théoriques de l'IA avec son test de Turing en 1950.",
                "topic": "Histoire IA"
            },
            {
                "question": "Quelle est la différence principale entre Machine Learning et programmation traditionnelle?",
                "options": [
                    "Le ML apprend à partir de données, la programmation suit des règles explicites",
                    "Il n'y a pas de différence",
                    "Le ML est plus lent",
                    "La programmation traditionnelle utilise des réseaux de neurones"
                ],
                "correct": 0,
                "explanation": "Le Machine Learning extrait des patterns des données plutôt que de suivre des règles codées manuellement.",
                "topic": "Fondamentaux ML"
            },
            {
                "question": "Lequel de ces exemples N'EST PAS une application de l'IA?",
                "options": [
                    "Calculatrice basique",
                    "Reconnaissance faciale",
                    "Traduction automatique",
                    "Recommandations Netflix"
                ],
                "correct": 0,
                "explanation": "Une calculatrice suit des règles mathématiques fixes, elle n'utilise pas d'IA.",
                "topic": "Applications IA"
            }
        ],
        "L2": [
            {
                "question": "Que signifie 'Transformer' dans le contexte des LLM?",
                "options": [
                    "Une architecture de réseau de neurones basée sur l'attention",
                    "Un robot qui se transforme",
                    "Un convertisseur de format de fichier",
                    "Un type de base de données"
                ],
                "correct": 0,
                "explanation": "Les Transformers utilisent le mécanisme d'attention pour traiter les séquences en parallèle.",
                "topic": "Architecture Transformer"
            },
            {
                "question": "Quel est l'objectif principal du Prompt Engineering?",
                "options": [
                    "Optimiser les instructions données à un LLM pour obtenir de meilleures réponses",
                    "Réparer les bugs dans le code",
                    "Créer des interfaces utilisateur",
                    "Gérer les bases de données"
                ],
                "correct": 0,
                "explanation": "Le Prompt Engineering consiste à formuler des instructions claires et précises pour guider le modèle.",
                "topic": "Prompt Engineering"
            }
        ],
        "L6": [
            {
                "question": "Qu'est-ce qu'un biais algorithmique?",
                "options": [
                    "Une discrimination systématique dans les résultats d'un algorithme",
                    "Une erreur de syntaxe dans le code",
                    "Un problème de performance",
                    "Un type de virus informatique"
                ],
                "correct": 0,
                "explanation": "Les biais algorithmiques reflètent souvent les biais présents dans les données d'entraînement.",
                "topic": "Biais IA"
            },
            {
                "question": "Pourquoi l'explicabilité de l'IA est-elle importante?",
                "options": [
                    "Pour comprendre comment l'IA prend ses décisions et garantir la confiance",
                    "Pour que l'IA soit plus rapide",
                    "Pour réduire les coûts",
                    "Pour augmenter la taille des modèles"
                ],
                "correct": 0,
                "explanation": "L'explicabilité permet aux utilisateurs de comprendre et faire confiance aux décisions de l'IA.",
                "topic": "Éthique IA"
            },
            {
                "question": "Quel principe éthique exige que les données personnelles soient protégées?",
                "options": [
                    "Le respect de la vie privée",
                    "L'efficacité",
                    "La rentabilité",
                    "La rapidité"
                ],
                "correct": 0,
                "explanation": "La protection des données personnelles est un droit fondamental encadré par des lois comme le RGPD.",
                "topic": "Vie privée"
            }
        ],
        "C1": [
            {
                "question": "Lequel de ces appareils utilise l'Intelligence Artificielle?",
                "options": [
                    "Un assistant vocal comme Siri ou Alexa",
                    "Une lampe de bureau",
                    "Un livre papier",
                    "Un crayon"
                ],
                "correct": 0,
                "explanation": "Les assistants vocaux utilisent l'IA pour comprendre et répondre aux questions.",
                "topic": "IA quotidienne"
            }
        ],
        "P1": [
            {
                "question": "Dans un jeu vidéo, l'IA peut aider à...",
                "options": [
                    "Faire bouger les personnages ennemis intelligemment",
                    "Allumer l'écran",
                    "Charger la manette",
                    "Brancher la console"
                ],
                "correct": 0,
                "explanation": "L'IA dans les jeux permet aux personnages non-joueurs de réagir de manière intelligente.",
                "topic": "IA dans les jeux"
            }
        ]
    }

    @classmethod
    def generate_quiz(
        cls,
        module: str,
        num_questions: int = 5,
        difficulty: str = "all"
    ) -> List[QuizQuestion]:
        """Generate a quiz for a specific module"""

        templates = cls.QUIZ_TEMPLATES.get(module, cls.QUIZ_TEMPLATES.get("L1", []))

        questions = []
        for i, template in enumerate(templates[:num_questions]):
            questions.append(QuizQuestion(
                question=template["question"],
                options=template["options"],
                correct_answer=template["correct"],
                explanation=template["explanation"],
                difficulty=difficulty if difficulty != "all" else "Intermédiaire",
                module=module,
                topic=template.get("topic", "Général")
            ))

        return questions

    @classmethod
    def to_dict(cls, questions: List[QuizQuestion]) -> List[Dict]:
        """Convert quiz questions to dictionary format"""
        return [
            {
                "question": q.question,
                "options": q.options,
                "correct_answer": q.correct_answer,
                "correct_letter": chr(65 + q.correct_answer),  # A, B, C, D
                "explanation": q.explanation,
                "difficulty": q.difficulty,
                "module": q.module,
                "topic": q.topic
            }
            for q in questions
        ]


# ============================================
# MODULE COMPARATOR
# ============================================

class ModuleComparator:
    """Compare two or more modules"""

    @classmethod
    def compare(cls, module_ids: List[str]) -> Dict[str, Any]:
        """Compare multiple modules"""

        comparison = {
            "modules": [],
            "comparison_table": []
        }

        for module_id in module_ids:
            module = BBC_PROGRAM_DATA["modules"].get(module_id)
            if module:
                comparison["modules"].append({
                    "id": module_id,
                    "name": module["name"],
                    "duration_hours": module["duration_hours"],
                    "credits": module["credits"],
                    "difficulty": module["difficulty"],
                    "prerequisites": module["prerequisites"],
                    "project": module["project"],
                    "objectives": module["objectives"]
                })

        # Create comparison table
        if len(comparison["modules"]) >= 2:
            headers = ["Critère"] + [m["id"] for m in comparison["modules"]]
            rows = [
                ["Nom"] + [m["name"] for m in comparison["modules"]],
                ["Durée (heures)"] + [str(m["duration_hours"]) for m in comparison["modules"]],
                ["Crédits"] + [str(m["credits"]) for m in comparison["modules"]],
                ["Difficulté"] + [m["difficulty"] for m in comparison["modules"]],
                ["Prérequis"] + [", ".join(m["prerequisites"]) or "Aucun" for m in comparison["modules"]],
                ["Projet"] + [m["project"] for m in comparison["modules"]]
            ]
            comparison["comparison_table"] = {"headers": headers, "rows": rows}

        return comparison

    @classmethod
    def to_markdown_table(cls, comparison: Dict) -> str:
        """Convert comparison to markdown table"""
        if not comparison.get("comparison_table"):
            return "Pas assez de modules pour comparer."

        table = comparison["comparison_table"]
        headers = table["headers"]
        rows = table["rows"]

        # Build markdown table
        md = "| " + " | ".join(headers) + " |\n"
        md += "| " + " | ".join(["---"] * len(headers)) + " |\n"

        for row in rows:
            md += "| " + " | ".join(row) + " |\n"

        return md


# ============================================
# BUDGET CALCULATOR
# ============================================

class BudgetCalculator:
    """Calculate budget for BBC School deployment"""

    BASE_COSTS = BBC_PROGRAM_DATA["budget"]

    @classmethod
    def calculate(
        cls,
        num_schools: int = 50,
        num_teachers: int = 200,
        num_students: int = 5000
    ) -> Dict[str, Any]:
        """Calculate detailed budget"""

        # Base calculations
        school_cost = num_schools * cls.BASE_COSTS["per_school"]
        teacher_cost = num_teachers * cls.BASE_COSTS["per_teacher"]
        student_cost = num_students * cls.BASE_COSTS["per_student"]

        total_da = school_cost + teacher_cost + student_cost
        total_usd = total_da / cls.BASE_COSTS["exchange_rate"]

        # Breakdown by category (proportional)
        breakdown = {}
        for category, data in cls.BASE_COSTS["breakdown"].items():
            percent = data["percent"] / 100
            breakdown[category] = {
                "da": round(total_da * percent),
                "usd": round(total_usd * percent),
                "percent": data["percent"]
            }

        return {
            "parameters": {
                "schools": num_schools,
                "teachers": num_teachers,
                "students": num_students
            },
            "costs_per_unit": {
                "per_school_da": cls.BASE_COSTS["per_school"],
                "per_teacher_da": cls.BASE_COSTS["per_teacher"],
                "per_student_da": cls.BASE_COSTS["per_student"]
            },
            "subtotals": {
                "schools_da": school_cost,
                "teachers_da": teacher_cost,
                "students_da": student_cost
            },
            "total": {
                "da": total_da,
                "usd": round(total_usd, 2),
                "formatted_da": f"{total_da:,.0f} DA",
                "formatted_usd": f"${total_usd:,.2f} USD"
            },
            "breakdown": breakdown,
            "exchange_rate": cls.BASE_COSTS["exchange_rate"],
            "comparison_pilot": {
                "pilot_budget_da": cls.BASE_COSTS["total_da"],
                "difference_da": total_da - cls.BASE_COSTS["total_da"],
                "ratio": round(total_da / cls.BASE_COSTS["total_da"], 2)
            }
        }

    @classmethod
    def to_markdown(cls, budget: Dict) -> str:
        """Format budget as markdown"""
        md = f"""## Budget Programme IA BBC School

### Paramètres
- Écoles: **{budget['parameters']['schools']}**
- Enseignants: **{budget['parameters']['teachers']}**
- Élèves: **{budget['parameters']['students']}**

### Coûts unitaires
| Élément | Coût (DA) |
|---------|-----------|
| Par école | {budget['costs_per_unit']['per_school_da']:,} DA |
| Par enseignant | {budget['costs_per_unit']['per_teacher_da']:,} DA |
| Par élève | {budget['costs_per_unit']['per_student_da']:,} DA |

### Sous-totaux
| Catégorie | Montant (DA) |
|-----------|--------------|
| Infrastructure écoles | {budget['subtotals']['schools_da']:,} DA |
| Formation enseignants | {budget['subtotals']['teachers_da']:,} DA |
| Support élèves | {budget['subtotals']['students_da']:,} DA |

### **TOTAL: {budget['total']['formatted_da']}** ({budget['total']['formatted_usd']})

### Répartition par poste
| Poste | Montant (DA) | % |
|-------|--------------|---|
"""
        for category, data in budget['breakdown'].items():
            md += f"| {category.replace('_', ' ').title()} | {data['da']:,} DA | {data['percent']}% |\n"

        md += f"""
### Comparaison avec le pilote
- Budget pilote initial: **{budget['comparison_pilot']['pilot_budget_da']:,} DA**
- Différence: **{budget['comparison_pilot']['difference_da']:+,} DA**
- Ratio: **{budget['comparison_pilot']['ratio']}x**
"""
        return md


# ============================================
# TIMELINE GENERATOR
# ============================================

class TimelineGenerator:
    """Generate deployment timeline"""

    @classmethod
    def get_timeline(cls) -> List[Dict]:
        """Get the deployment timeline"""
        return BBC_PROGRAM_DATA["timeline"]

    @classmethod
    def to_mermaid(cls) -> str:
        """Generate Mermaid Gantt chart"""
        mermaid = """gantt
    title Programme National IA BBC School - Timeline
    dateFormat YYYY-MM-DD

    section Démarrage
    Lancement officiel :milestone, m1, 2026-02-03, 0d

    section Formation
    Formation formateurs N1 :a1, 2026-02-17, 30d
    Formation formateurs N2 :a2, after a1, 30d

    section Pilote
    Pilote 10 écoles :b1, 2026-03-03, 105d
    Évaluation mi-parcours :milestone, m2, 2026-06-15, 0d

    section Extension
    Extension 25 écoles :c1, 2026-09-01, 135d
    Évaluation annuelle :milestone, m3, 2027-01-15, 0d
    Extension 50 écoles :c2, 2027-06-01, 60d

    section Clôture
    Rapport final :d1, 2027-07-01, 30d
    Fin pilote :milestone, m4, 2027-08-01, 0d
"""
        return mermaid

    @classmethod
    def to_json(cls) -> Dict:
        """Generate JSON timeline for visualization"""
        events = []
        for item in BBC_PROGRAM_DATA["timeline"]:
            events.append({
                "date": item["date"],
                "title": item["event"],
                "phase": item["phase"],
                "color": {
                    "Démarrage": "#4CAF50",
                    "Formation": "#2196F3",
                    "Pilote": "#FF9800",
                    "Évaluation": "#9C27B0",
                    "Extension": "#00BCD4",
                    "Clôture": "#F44336"
                }.get(item["phase"], "#607D8B")
            })

        return {
            "title": "Programme National IA BBC School",
            "start_date": "2026-02-03",
            "end_date": "2027-08-01",
            "duration_months": 18,
            "events": events
        }


# ============================================
# ADAPTIVE ASSISTANT
# ============================================

class AdaptiveAssistant:
    """Assistant that adapts to education level"""

    VOCABULARY = {
        "primaire": {
            "ia": "robot intelligent",
            "algorithme": "recette magique pour l'ordinateur",
            "données": "informations",
            "modèle": "cerveau artificiel",
            "entraînement": "apprentissage",
            "prédiction": "devinette intelligente"
        },
        "college": {
            "ia": "Intelligence Artificielle",
            "algorithme": "suite d'instructions",
            "données": "données",
            "modèle": "modèle d'apprentissage",
            "entraînement": "phase d'entraînement",
            "prédiction": "prédiction"
        },
        "lycee": {
            "ia": "Intelligence Artificielle",
            "algorithme": "algorithme",
            "données": "dataset",
            "modèle": "modèle de Machine Learning",
            "entraînement": "training",
            "prédiction": "inférence"
        },
        "enseignants": {
            "ia": "Intelligence Artificielle (IA)",
            "algorithme": "algorithme d'apprentissage",
            "données": "corpus de données d'entraînement",
            "modèle": "architecture neuronale",
            "entraînement": "fine-tuning et transfer learning",
            "prédiction": "inférence en temps réel"
        }
    }

    TONE = {
        "primaire": "amical et ludique avec des emojis 🎮🤖",
        "college": "pédagogique et engageant",
        "lycee": "professionnel mais accessible",
        "enseignants": "technique et précis"
    }

    @classmethod
    def get_system_prompt(cls, level: str) -> str:
        """Get adapted system prompt for education level"""
        vocab = cls.VOCABULARY.get(level, cls.VOCABULARY["college"])
        tone = cls.TONE.get(level, cls.TONE["college"])

        prompt = f"""Tu es un assistant pédagogique pour le Programme National IA BBC School.

NIVEAU: {level.upper()}
TON: {tone}

VOCABULAIRE ADAPTÉ:
"""
        for term, adaptation in vocab.items():
            prompt += f"- Utilise '{adaptation}' au lieu de '{term}'\n"

        prompt += """
RÈGLES:
1. Adapte ton langage au niveau de l'élève
2. Utilise des exemples concrets et familiers
3. Encourage et valorise les questions
4. Si le niveau est primaire, utilise des emojis appropriés
5. Pour les enseignants, sois précis et technique
"""
        return prompt


# ============================================
# MINISTER DEMO MODE
# ============================================

class MinisterDemoMode:
    """Pre-programmed demo responses for Minister presentation"""

    DEMO_RESPONSES = {
        "présentation": """# Programme National IA - BBC School Algérie 🇩🇿

## Vision
Former **5000 élèves** et **200 enseignants** à l'Intelligence Artificielle d'ici 2027.

## Points clés
- 🏫 **50 établissements** pilotes
- 📚 **500+ heures** de contenu pédagogique
- 🌍 **3 langues**: Français, Arabe, Anglais
- 💰 **Budget optimisé**: 12,5 millions DA

## Niveaux couverts
| Niveau | Modules | Heures |
|--------|---------|--------|
| Primaire | 4 | 40h |
| Collège | 6 | 80h |
| Lycée | 8 | 120h |
| Enseignants | 3 | 60h |

## Lancement: 3 Février 2026
""",
        "budget": BudgetCalculator.to_markdown(BudgetCalculator.calculate()),

        "timeline": TimelineGenerator.to_mermaid(),

        "kpis": """# Indicateurs de Performance (KPIs)

| KPI | Objectif | Unité |
|-----|----------|-------|
| Élèves formés | 5 000 | élèves |
| Enseignants certifiés | 200 | enseignants |
| Établissements équipés | 50 | écoles |
| Taux de satisfaction | 85% | % |
| Taux de complétion | 75% | % |
| Taux d'emploi post-formation | 60% | % |
""",
        "modules_lycee": """# Modules Lycée (8 modules - 120h)

| ID | Module | Heures | Crédits |
|----|--------|--------|---------|
| L1 | Fondamentaux IA | 12h | 3 |
| L2 | LLM et Transformers | 16h | 4 |
| L3 | Vision par Ordinateur | 14h | 3 |
| L4 | NLP Avancé | 16h | 4 |
| L5 | IA Générative | 14h | 3 |
| L6 | Éthique et Société | 10h | 2 |
| L7 | Projet Intégrateur | 20h | 5 |
| L8 | IA et Carrières | 8h | 2 |
""",
        "formation_enseignants": """# Formation Enseignants

## 3 Niveaux de certification

### Niveau 1: Fondamentaux IA
- **Durée**: 40 heures
- **Objectif**: Maîtriser les concepts de base
- **Certification**: Utilisateur IA

### Niveau 2: Pédagogie IA
- **Durée**: 60 heures
- **Objectif**: Intégrer l'IA dans l'enseignement
- **Certification**: Formateur IA

### Niveau 3: Expert IA
- **Durée**: 80 heures
- **Objectif**: Créer du contenu IA
- **Certification**: Expert & Mentor IA

**Total: 200 enseignants à former**
"""
    }

    QUICK_BUTTONS = [
        {"label": "📊 Présentation", "action": "présentation"},
        {"label": "💰 Budget", "action": "budget"},
        {"label": "📅 Timeline", "action": "timeline"},
        {"label": "📈 KPIs", "action": "kpis"},
        {"label": "🎓 Modules Lycée", "action": "modules_lycee"},
        {"label": "👨‍🏫 Formation Enseignants", "action": "formation_enseignants"}
    ]

    @classmethod
    def get_response(cls, action: str) -> str:
        """Get pre-programmed response"""
        return cls.DEMO_RESPONSES.get(action, "Action non reconnue.")

    @classmethod
    def get_buttons(cls) -> List[Dict]:
        """Get quick action buttons"""
        return cls.QUICK_BUTTONS


# ============================================
# MULTILINGUAL RESPONSES
# ============================================

ARABIC_RESPONSES = {
    "modules_count": """# عدد الوحدات حسب المستوى

| المستوى | عدد الوحدات | الساعات |
|---------|-------------|---------|
| ابتدائي | 4 | 40 |
| متوسط | 6 | 80 |
| ثانوي | 8 | 120 |
| معلمين | 3 | 60 |

**المجموع: 21 وحدة**
""",
    "program_start": """# تاريخ انطلاق البرنامج

📅 **3 فبراير 2026**

المراحل:
1. إطلاق رسمي
2. تدريب المدربين
3. المرحلة التجريبية (50 مدرسة)
4. التقييم والتوسع
""",
    "budget": """# الميزانية الإجمالية

💰 **12,500,000 دج** (حوالي 92,500 دولار)

التوزيع:
- البنية التحتية: 32%
- تدريب المعلمين: 28%
- المعدات التقنية: 20%
- المحتوى التعليمي: 12%
- المتابعة والتقييم: 8%
"""
}


def get_arabic_response(query: str) -> Optional[str]:
    """Get pre-defined Arabic response based on query"""
    query_lower = query.lower()

    if "وحدات" in query or "عدد" in query:
        return ARABIC_RESPONSES["modules_count"]
    elif "متى" in query or "تاريخ" in query or "انطلاق" in query:
        return ARABIC_RESPONSES["program_start"]
    elif "ميزانية" in query or "تكلفة" in query:
        return ARABIC_RESPONSES["budget"]

    return None
