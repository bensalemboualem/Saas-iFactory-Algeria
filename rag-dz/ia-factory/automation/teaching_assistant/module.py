"""
IA Factory Automation - Teaching Assistant Module
MVP Assistant pédagogique pour établissements scolaires DZ
Quick win avec clients existants (Prof-DZ)
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import os
import json

router = APIRouter(prefix="/teaching", tags=["Teaching Assistant"])


class Subject(str, Enum):
    MATH = "Mathématiques"
    PHYSICS = "Physique"
    CHEMISTRY = "Chimie"
    BIOLOGY = "Biologie"
    FRENCH = "Français"
    ARABIC = "Arabe"
    ENGLISH = "Anglais"
    HISTORY = "Histoire"
    GEOGRAPHY = "Géographie"
    PHILOSOPHY = "Philosophie"
    ISLAMIC_STUDIES = "Éducation Islamique"
    COMPUTER_SCIENCE = "Informatique"


class Level(str, Enum):
    PRIMAIRE = "Primaire"
    CEM = "CEM"
    LYCEE = "Lycée"
    BAC = "Terminale BAC"
    UNIVERSITE = "Université"


class ContentType(str, Enum):
    LESSON = "Cours"
    EXERCISE = "Exercice"
    EXAM = "Examen"
    QUIZ = "Quiz"
    REVISION = "Révision"
    HOMEWORK = "Devoir"


class DifficultyLevel(str, Enum):
    EASY = "Facile"
    MEDIUM = "Moyen"
    HARD = "Difficile"
    ADVANCED = "Avancé"


class LanguageMode(str, Enum):
    FRENCH = "Français"
    ARABIC = "Arabe"
    BILINGUAL = "Bilingue"


# ===== MODELS =====

class LessonRequest(BaseModel):
    """Requête de génération de cours"""
    subject: Subject
    level: Level
    topic: str
    subtopics: List[str] = Field(default_factory=list)
    duration_minutes: int = Field(default=60, ge=15, le=180)
    language: LanguageMode = LanguageMode.FRENCH
    include_examples: bool = True
    include_exercises: bool = True


class ExerciseRequest(BaseModel):
    """Requête de génération d'exercices"""
    subject: Subject
    level: Level
    topic: str
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
    num_exercises: int = Field(default=5, ge=1, le=20)
    include_solutions: bool = True
    language: LanguageMode = LanguageMode.FRENCH


class ExamRequest(BaseModel):
    """Requête de génération d'examen"""
    subject: Subject
    level: Level
    topics: List[str]
    duration_minutes: int = Field(default=120, ge=30, le=240)
    total_points: int = Field(default=20)
    difficulty_distribution: Dict[str, int] = Field(
        default={"easy": 30, "medium": 50, "hard": 20}
    )
    include_barème: bool = True
    language: LanguageMode = LanguageMode.FRENCH


class StudentProgress(BaseModel):
    """Suivi de progression élève"""
    student_id: str
    student_name: str
    level: Level
    subjects: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    weaknesses: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    recommended_focus: List[str] = Field(default_factory=list)


class GeneratedContent(BaseModel):
    """Contenu pédagogique généré"""
    id: str
    content_type: ContentType
    subject: Subject
    level: Level
    topic: str
    content: str
    metadata: Dict[str, Any]
    created_at: datetime
    language: LanguageMode


# ===== TEMPLATES PÉDAGOGIQUES DZ =====

LESSON_TEMPLATES = {
    Subject.MATH: """
# {topic}
## Niveau: {level}

### 🎯 Objectifs du cours
{objectives}

### 📚 Prérequis
{prerequisites}

### 📖 Cours

#### 1. Définitions
{definitions}

#### 2. Propriétés et Théorèmes
{properties}

#### 3. Démonstrations
{proofs}

### 💡 Exemples

{examples}

### ✏️ Exercices d'application

{exercises}

### 📝 À retenir
{summary}

---
*Généré par IA Factory - Teaching Assistant*
""",
    
    Subject.PHYSICS: """
# {topic}
## Niveau: {level}

### 🎯 Objectifs
{objectives}

### 📚 Prérequis
{prerequisites}

### 📖 Cours

#### 1. Introduction et contexte
{introduction}

#### 2. Lois et formules
{formulas}

#### 3. Applications
{applications}

### 🔬 Expériences et observations
{experiments}

### 💡 Exemples résolus
{examples}

### ✏️ Exercices
{exercises}

### 📝 Résumé
{summary}

---
*Généré par IA Factory - Teaching Assistant*
"""
}

EXERCISE_TEMPLATES = {
    DifficultyLevel.EASY: """
### Exercice {num} (★)
{statement}

**Indice:** {hint}

<details>
<summary>Solution</summary>

{solution}

</details>
""",
    
    DifficultyLevel.MEDIUM: """
### Exercice {num} (★★)
{statement}

<details>
<summary>Solution</summary>

{solution}

</details>
""",
    
    DifficultyLevel.HARD: """
### Exercice {num} (★★★)
{statement}

<details>
<summary>Solution</summary>

{solution}

</details>
"""
}


class TeachingAssistant:
    """
    Assistant pédagogique IA
    Génère cours, exercices, examens adaptés au programme algérien
    """
    
    def __init__(self):
        self.content_db: Dict[str, GeneratedContent] = {}
        self.student_progress: Dict[str, StudentProgress] = {}
        
        # Curriculum DZ par niveau
        self.curriculum = self._load_curriculum()
    
    def _load_curriculum(self) -> Dict[str, Any]:
        """Charge le curriculum algérien"""
        return {
            Level.PRIMAIRE: {
                Subject.MATH: [
                    "Nombres entiers",
                    "Opérations de base",
                    "Géométrie plane simple",
                    "Mesures"
                ],
                Subject.FRENCH: [
                    "Lecture et compréhension",
                    "Écriture",
                    "Grammaire de base",
                    "Vocabulaire"
                ],
                Subject.ARABIC: [
                    "القراءة",
                    "الكتابة",
                    "النحو",
                    "الإملاء"
                ]
            },
            Level.CEM: {
                Subject.MATH: [
                    "Algèbre",
                    "Géométrie dans le plan",
                    "Statistiques descriptives",
                    "Équations"
                ],
                Subject.PHYSICS: [
                    "Mécanique",
                    "Électricité",
                    "Optique",
                    "Chaleur"
                ]
            },
            Level.LYCEE: {
                Subject.MATH: [
                    "Analyse (limites, dérivées)",
                    "Algèbre linéaire",
                    "Probabilités",
                    "Géométrie dans l'espace"
                ],
                Subject.PHYSICS: [
                    "Mécanique newtonienne",
                    "Électromagnétisme",
                    "Thermodynamique",
                    "Physique nucléaire"
                ]
            },
            Level.BAC: {
                Subject.MATH: [
                    "Intégrales",
                    "Équations différentielles",
                    "Nombres complexes",
                    "Suites et séries"
                ],
                Subject.PHYSICS: [
                    "Mécanique du point",
                    "Ondes mécaniques",
                    "Physique atomique",
                    "Radioactivité"
                ],
                Subject.PHILOSOPHY: [
                    "La conscience et l'inconscient",
                    "La liberté et le déterminisme",
                    "La morale et l'éthique",
                    "La connaissance"
                ]
            }
        }
    
    async def generate_lesson(self, request: LessonRequest) -> GeneratedContent:
        """Génère un cours complet"""
        
        content_id = f"lesson_{datetime.now().strftime('%Y%m%d%H%M%S')}_{request.subject.value[:4]}"
        
        # Sélectionner le template
        template = LESSON_TEMPLATES.get(request.subject, LESSON_TEMPLATES[Subject.MATH])
        
        # Générer le contenu
        objectives = self._generate_objectives(request.topic, request.level)
        prerequisites = self._generate_prerequisites(request.subject, request.level, request.topic)
        
        content_text = template.format(
            topic=request.topic,
            level=request.level.value,
            objectives=objectives,
            prerequisites=prerequisites,
            definitions=self._generate_definitions(request),
            properties=self._generate_properties(request),
            proofs="" if request.level == Level.PRIMAIRE else self._generate_proofs(request),
            examples=self._generate_examples(request) if request.include_examples else "",
            exercises=self._generate_exercises(request) if request.include_exercises else "",
            summary=self._generate_summary(request),
            # Physics-specific
            introduction=f"Introduction à {request.topic}",
            formulas=self._generate_formulas(request),
            applications=self._generate_applications(request),
            experiments=self._generate_experiments(request)
        )
        
        # Créer l'objet contenu
        content = GeneratedContent(
            id=content_id,
            content_type=ContentType.LESSON,
            subject=request.subject,
            level=request.level,
            topic=request.topic,
            content=content_text,
            metadata={
                "duration_minutes": request.duration_minutes,
                "subtopics": request.subtopics,
                "has_examples": request.include_examples,
                "has_exercises": request.include_exercises
            },
            created_at=datetime.now(),
            language=request.language
        )
        
        # Sauvegarder
        self.content_db[content_id] = content
        
        return content
    
    async def generate_exercises(self, request: ExerciseRequest) -> GeneratedContent:
        """Génère une série d'exercices"""
        
        content_id = f"exo_{datetime.now().strftime('%Y%m%d%H%M%S')}_{request.subject.value[:4]}"
        
        exercises_text = f"""
# Exercices: {request.topic}
## {request.subject.value} - {request.level.value}
### Difficulté: {request.difficulty.value}

---

"""
        
        for i in range(1, request.num_exercises + 1):
            template = EXERCISE_TEMPLATES[request.difficulty]
            
            exercise = template.format(
                num=i,
                statement=self._generate_exercise_statement(request, i),
                hint=self._generate_hint(request) if request.difficulty == DifficultyLevel.EASY else "",
                solution=self._generate_solution(request, i) if request.include_solutions else "À faire en classe"
            )
            
            exercises_text += exercise + "\n\n"
        
        content = GeneratedContent(
            id=content_id,
            content_type=ContentType.EXERCISE,
            subject=request.subject,
            level=request.level,
            topic=request.topic,
            content=exercises_text,
            metadata={
                "num_exercises": request.num_exercises,
                "difficulty": request.difficulty.value,
                "has_solutions": request.include_solutions
            },
            created_at=datetime.now(),
            language=request.language
        )
        
        self.content_db[content_id] = content
        
        return content
    
    async def generate_exam(self, request: ExamRequest) -> GeneratedContent:
        """Génère un examen complet avec barème"""
        
        content_id = f"exam_{datetime.now().strftime('%Y%m%d%H%M%S')}_{request.subject.value[:4]}"
        
        exam_text = f"""
# EXAMEN - {request.subject.value}
## {request.level.value}

**Durée:** {request.duration_minutes} minutes
**Barème:** {request.total_points} points

---

### Consignes
- La clarté et la rigueur de la rédaction seront prises en compte
- L'usage de la calculatrice {'est autorisé' if request.subject in [Subject.MATH, Subject.PHYSICS] else "n'est pas autorisé"}
- Les exercices sont indépendants

---

"""
        
        # Distribuer les points selon la difficulté
        points_distribution = self._calculate_points_distribution(
            request.total_points,
            request.difficulty_distribution
        )
        
        exercise_num = 1
        for difficulty, points in points_distribution.items():
            if points > 0:
                exam_text += f"""
## Partie {exercise_num}: ({points} points)

"""
                num_exercises = max(1, points // 4)
                for i in range(num_exercises):
                    exam_text += f"""
### Exercice {exercise_num}.{i+1} ({points // num_exercises} pts)

{self._generate_exam_exercise(request, difficulty)}

"""
                exercise_num += 1
        
        if request.include_barème:
            exam_text += """
---

## BARÈME DE CORRECTION

| Exercice | Points | Critères |
|----------|--------|----------|
"""
            for i in range(1, exercise_num):
                exam_text += f"| Exercice {i} | {request.total_points // (exercise_num - 1)} | Voir grille détaillée |\n"
        
        content = GeneratedContent(
            id=content_id,
            content_type=ContentType.EXAM,
            subject=request.subject,
            level=request.level,
            topic=", ".join(request.topics),
            content=exam_text,
            metadata={
                "duration_minutes": request.duration_minutes,
                "total_points": request.total_points,
                "topics": request.topics,
                "difficulty_distribution": request.difficulty_distribution
            },
            created_at=datetime.now(),
            language=request.language
        )
        
        self.content_db[content_id] = content
        
        return content
    
    async def analyze_student(self, student_id: str, results: List[Dict]) -> StudentProgress:
        """Analyse les résultats d'un élève et génère des recommandations"""
        
        progress = self.student_progress.get(student_id)
        
        if not progress:
            progress = StudentProgress(
                student_id=student_id,
                student_name=f"Élève {student_id}",
                level=Level.CEM
            )
        
        # Analyser les résultats
        for result in results:
            subject = result.get("subject")
            score = result.get("score", 0)
            topic = result.get("topic")
            
            if subject not in progress.subjects:
                progress.subjects[subject] = {"scores": [], "topics": {}}
            
            progress.subjects[subject]["scores"].append(score)
            
            if topic:
                if topic not in progress.subjects[subject]["topics"]:
                    progress.subjects[subject]["topics"][topic] = []
                progress.subjects[subject]["topics"][topic].append(score)
        
        # Identifier forces et faiblesses
        for subject, data in progress.subjects.items():
            avg_score = sum(data["scores"]) / len(data["scores"]) if data["scores"] else 0
            
            if avg_score >= 14:
                if subject not in progress.strengths:
                    progress.strengths.append(subject)
            elif avg_score < 10:
                if subject not in progress.weaknesses:
                    progress.weaknesses.append(subject)
                progress.recommended_focus.append(f"Renforcement en {subject}")
            
            # Analyser par topic
            for topic, scores in data["topics"].items():
                topic_avg = sum(scores) / len(scores)
                if topic_avg < 10:
                    progress.recommended_focus.append(f"Réviser: {topic}")
        
        self.student_progress[student_id] = progress
        
        return progress
    
    async def generate_personalized_exercises(
        self,
        student_id: str,
        subject: Subject
    ) -> GeneratedContent:
        """Génère des exercices personnalisés selon les faiblesses"""
        
        progress = self.student_progress.get(student_id)
        
        if not progress:
            raise ValueError("Student not found. Run analyze_student first.")
        
        # Trouver les topics faibles
        weak_topics = []
        if subject.value in progress.subjects:
            for topic, scores in progress.subjects[subject.value]["topics"].items():
                if sum(scores) / len(scores) < 12:
                    weak_topics.append(topic)
        
        if not weak_topics:
            weak_topics = ["Révision générale"]
        
        # Générer exercices ciblés
        request = ExerciseRequest(
            subject=subject,
            level=progress.level,
            topic=", ".join(weak_topics[:3]),
            difficulty=DifficultyLevel.MEDIUM,
            num_exercises=5,
            include_solutions=True
        )
        
        content = await self.generate_exercises(request)
        content.metadata["personalized_for"] = student_id
        content.metadata["targeting"] = weak_topics
        
        return content
    
    # ===== HELPER METHODS =====
    
    def _generate_objectives(self, topic: str, level: Level) -> str:
        return f"""
- Comprendre les concepts fondamentaux de {topic}
- Savoir appliquer les méthodes et techniques associées
- Être capable de résoudre des problèmes types
"""
    
    def _generate_prerequisites(self, subject: Subject, level: Level, topic: str) -> str:
        return f"- Maîtrise du niveau {level.value} précédent\n- Connaissances de base en {subject.value}"
    
    def _generate_definitions(self, request: LessonRequest) -> str:
        return f"**Définition:** {request.topic} désigne...\n\n*À compléter avec les définitions spécifiques*"
    
    def _generate_properties(self, request: LessonRequest) -> str:
        return "**Propriété 1:** ...\n\n**Propriété 2:** ..."
    
    def _generate_proofs(self, request: LessonRequest) -> str:
        return "**Démonstration:**\n\n*À développer*"
    
    def _generate_examples(self, request: LessonRequest) -> str:
        return f"""
**Exemple 1:**
Énoncé: ...
Solution: ...

**Exemple 2:**
Énoncé: ...
Solution: ...
"""
    
    def _generate_exercises(self, request: LessonRequest) -> str:
        return """
1. Exercice d'application directe
2. Exercice de compréhension
3. Problème de synthèse
"""
    
    def _generate_summary(self, request: LessonRequest) -> str:
        return f"- Point clé 1 sur {request.topic}\n- Point clé 2\n- Point clé 3"
    
    def _generate_formulas(self, request: LessonRequest) -> str:
        return "**Formule principale:** ...\n\n**Formules dérivées:** ..."
    
    def _generate_applications(self, request: LessonRequest) -> str:
        return "Application dans la vie quotidienne: ..."
    
    def _generate_experiments(self, request: LessonRequest) -> str:
        return "**Expérience à réaliser:**\n\nMatériel: ...\nProtocole: ...\nObservations: ..."
    
    def _generate_exercise_statement(self, request: ExerciseRequest, num: int) -> str:
        return f"Exercice sur {request.topic} (à compléter avec énoncé spécifique #{num})"
    
    def _generate_hint(self, request: ExerciseRequest) -> str:
        return "Pensez à utiliser la méthode vue en cours..."
    
    def _generate_solution(self, request: ExerciseRequest, num: int) -> str:
        return f"**Solution de l'exercice {num}:**\n\nÉtape 1: ...\nÉtape 2: ...\nRésultat: ..."
    
    def _calculate_points_distribution(
        self,
        total: int,
        distribution: Dict[str, int]
    ) -> Dict[str, int]:
        points = {}
        for difficulty, percentage in distribution.items():
            points[difficulty] = int(total * percentage / 100)
        return points
    
    def _generate_exam_exercise(self, request: ExamRequest, difficulty: str) -> str:
        return f"Exercice de niveau {difficulty} sur {', '.join(request.topics[:2])}\n\n(À compléter)"


# Instance globale
teaching_assistant = TeachingAssistant()


# ===== API ROUTES =====

@router.post("/lessons/generate")
async def generate_lesson(request: LessonRequest):
    """Génère un cours complet"""
    content = await teaching_assistant.generate_lesson(request)
    return {
        "id": content.id,
        "topic": content.topic,
        "content": content.content,
        "metadata": content.metadata
    }


@router.post("/exercises/generate")
async def generate_exercises(request: ExerciseRequest):
    """Génère une série d'exercices"""
    content = await teaching_assistant.generate_exercises(request)
    return {
        "id": content.id,
        "topic": content.topic,
        "content": content.content,
        "metadata": content.metadata
    }


@router.post("/exams/generate")
async def generate_exam(request: ExamRequest):
    """Génère un examen complet avec barème"""
    content = await teaching_assistant.generate_exam(request)
    return {
        "id": content.id,
        "subject": content.subject.value,
        "content": content.content,
        "metadata": content.metadata
    }


@router.post("/students/{student_id}/analyze")
async def analyze_student(student_id: str, results: List[Dict[str, Any]]):
    """Analyse les résultats d'un élève"""
    progress = await teaching_assistant.analyze_student(student_id, results)
    return progress


@router.get("/students/{student_id}/progress")
async def get_student_progress(student_id: str):
    """Récupère la progression d'un élève"""
    progress = teaching_assistant.student_progress.get(student_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Student not found")
    return progress


@router.post("/students/{student_id}/personalized-exercises")
async def personalized_exercises(student_id: str, subject: Subject):
    """Génère des exercices personnalisés pour un élève"""
    try:
        content = await teaching_assistant.generate_personalized_exercises(student_id, subject)
        return {
            "id": content.id,
            "targeting": content.metadata.get("targeting"),
            "content": content.content
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/curriculum/{level}")
async def get_curriculum(level: Level):
    """Récupère le curriculum pour un niveau"""
    curriculum = teaching_assistant.curriculum.get(level, {})
    return {
        "level": level.value,
        "subjects": {
            subject.value: topics 
            for subject, topics in curriculum.items()
        }
    }


@router.get("/content/{content_id}")
async def get_content(content_id: str):
    """Récupère un contenu généré par ID"""
    content = teaching_assistant.content_db.get(content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content


@router.get("/content")
async def list_content(
    content_type: Optional[ContentType] = None,
    subject: Optional[Subject] = None,
    level: Optional[Level] = None
):
    """Liste tous les contenus générés"""
    contents = list(teaching_assistant.content_db.values())
    
    if content_type:
        contents = [c for c in contents if c.content_type == content_type]
    if subject:
        contents = [c for c in contents if c.subject == subject]
    if level:
        contents = [c for c in contents if c.level == level]
    
    return [
        {
            "id": c.id,
            "type": c.content_type.value,
            "subject": c.subject.value,
            "level": c.level.value,
            "topic": c.topic,
            "created_at": c.created_at.isoformat()
        }
        for c in contents
    ]
