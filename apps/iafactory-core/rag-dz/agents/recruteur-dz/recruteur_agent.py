"""
Recruteur DZ Agent - AI Recruitment & Candidate Evaluation for Algerian Market
Agent d'entretien de recrutement utilisant la méthodologie STAR
"""
from typing import Dict, Any, List, Optional
from ..core.base_agent import BaseAgent, AgentConfig, AgentResponse
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class InterviewMode(str, Enum):
    EVALUATION = "evaluation"      # Évaluation candidat (pour recruteurs)
    SIMULATION = "simulation"      # Simulation entretien (pour candidats)
    SCREENING = "screening"        # Pré-qualification rapide


class InterviewPhase(str, Enum):
    INTRODUCTION = "introduction"
    EXPERIENCE = "experience"
    TECHNICAL = "technical"
    SOFT_SKILLS = "soft_skills"
    MOTIVATION = "motivation"
    CLOSING = "closing"


class SkillCategory(str, Enum):
    TECHNICAL = "technical"
    SOFT = "soft"
    CULTURE_FIT = "culture_fit"


class SkillEvaluation(BaseModel):
    """Évaluation d'une compétence"""
    name: str
    category: SkillCategory
    score: int = Field(ge=1, le=5)  # 1-5
    comment: str = ""
    verbatim: Optional[str] = None


class CandidateProfile(BaseModel):
    """Profil du candidat"""
    name: Optional[str] = None
    position: str = ""
    experience_years: Optional[int] = None
    education: Optional[str] = None
    languages: List[str] = Field(default_factory=lambda: ["FR"])
    current_salary: Optional[str] = None
    expected_salary: Optional[str] = None
    availability: Optional[str] = None
    mobility: bool = True


class InterviewState(BaseModel):
    """État de l'entretien en cours"""
    mode: InterviewMode = InterviewMode.EVALUATION
    current_phase: InterviewPhase = InterviewPhase.INTRODUCTION
    phase_exchanges: int = 0
    total_exchanges: int = 0
    evaluations: List[SkillEvaluation] = Field(default_factory=list)
    red_flags: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    verbatims: List[str] = Field(default_factory=list)
    candidate: CandidateProfile = Field(default_factory=CandidateProfile)
    recommendation: Optional[str] = None  # "recommended", "review", "reserve", "rejected"


# Catégories d'emploi en Algérie
JOB_CATEGORIES = {
    "tech": {
        "name": "IT & Tech",
        "skills": ["programmation", "architecture", "devops", "data", "sécurité", "mobile", "web"],
        "questions": [
            "Décrivez un projet technique complexe que vous avez géré. Quels défis avez-vous rencontrés ?",
            "Comment restez-vous à jour avec les nouvelles technologies ?",
            "Parlez-moi d'un bug critique que vous avez résolu. Quelle était votre démarche ?"
        ]
    },
    "commercial": {
        "name": "Commercial & Vente",
        "skills": ["négociation", "prospection", "gestion compte", "closing", "CRM"],
        "questions": [
            "Décrivez votre plus grande réussite commerciale. Comment l'avez-vous obtenue ?",
            "Comment gérez-vous un client difficile ou une objection ?",
            "Quel est votre process de prospection ?"
        ]
    },
    "finance": {
        "name": "Finance & Comptabilité",
        "skills": ["comptabilité", "analyse financière", "reporting", "conformité", "fiscalité"],
        "questions": [
            "Parlez-moi d'une situation où vous avez identifié une anomalie comptable.",
            "Comment gérez-vous les clôtures mensuelles sous pression ?",
            "Quelle est votre expérience avec les normes IFRS/SCF algérien ?"
        ]
    },
    "marketing": {
        "name": "Marketing & Communication",
        "skills": ["digital", "content", "branding", "analytics", "réseaux sociaux"],
        "questions": [
            "Décrivez une campagne marketing que vous avez menée. Quels résultats ?",
            "Comment mesurez-vous le ROI de vos actions marketing ?",
            "Comment adaptez-vous votre communication au marché algérien ?"
        ]
    },
    "management": {
        "name": "Management & Direction",
        "skills": ["leadership", "stratégie", "team building", "décision", "gestion P&L"],
        "questions": [
            "Comment motivez-vous une équipe en difficulté ?",
            "Parlez-moi d'une décision difficile que vous avez dû prendre.",
            "Comment gérez-vous les conflits au sein de votre équipe ?"
        ]
    },
    "operations": {
        "name": "Opérations & Logistique",
        "skills": ["planification", "optimisation", "qualité", "supply chain", "lean"],
        "questions": [
            "Comment avez-vous amélioré un process opérationnel ?",
            "Parlez-moi d'une situation de crise logistique que vous avez gérée.",
            "Quelle est votre approche pour réduire les coûts opérationnels ?"
        ]
    },
    "rh": {
        "name": "Ressources Humaines",
        "skills": ["recrutement", "formation", "relations sociales", "paie", "droit social"],
        "questions": [
            "Comment évaluez-vous un candidat au-delà du CV ?",
            "Parlez-moi d'un conflit social que vous avez géré.",
            "Comment construisez-vous un plan de formation ?"
        ]
    }
}

# Questions soft skills universelles
SOFT_SKILLS_QUESTIONS = {
    "communication": "Comment décririez-vous votre style de communication ? Donnez-moi un exemple.",
    "teamwork": "Parlez-moi d'un projet où vous avez dû collaborer étroitement avec d'autres.",
    "adaptability": "Décrivez une situation où vous avez dû vous adapter rapidement à un changement.",
    "problem_solving": "Racontez-moi un problème complexe que vous avez résolu. Quelle démarche ?",
    "leadership": "Avez-vous déjà pris l'initiative sur un projet ? Racontez.",
    "stress_management": "Comment gérez-vous le stress et les deadlines serrées ?"
}

# Red flags à détecter
RED_FLAGS = [
    "incohérences dans le parcours",
    "critique excessive des anciens employeurs",
    "réponses vagues ou évasives",
    "aucune question sur le poste",
    "attentes salariales irréalistes",
    "manque d'exemples concrets",
    "attitude négative générale",
    "refus de répondre à certaines questions"
]

# Questions par phase
PHASE_QUESTIONS = {
    InterviewPhase.INTRODUCTION: [
        "Pouvez-vous vous présenter brièvement ?",
        "Qu'est-ce qui vous a attiré vers ce poste ?"
    ],
    InterviewPhase.EXPERIENCE: [
        "Parlez-moi de votre poste actuel ou dernier poste.",
        "Quelle a été votre plus grande réalisation professionnelle ?",
        "Pourquoi souhaitez-vous quitter/avez-vous quitté votre emploi ?"
    ],
    InterviewPhase.SOFT_SKILLS: [
        "Comment gérez-vous le stress et les deadlines ?",
        "Parlez-moi d'un conflit au travail et comment vous l'avez résolu.",
        "Comment décririez-vous votre style de travail ?"
    ],
    InterviewPhase.MOTIVATION: [
        "Où vous voyez-vous dans 3-5 ans ?",
        "Qu'est-ce qui vous motive au quotidien ?",
        "Quelles sont vos attentes salariales ?"
    ],
    InterviewPhase.CLOSING: [
        "Avez-vous des questions sur le poste ou l'entreprise ?",
        "Quelle est votre disponibilité ?",
        "Y a-t-il autre chose que vous aimeriez nous partager ?"
    ]
}


class RecruteurAgent(BaseAgent):
    """
    Agent de recrutement pour le marché algérien.
    Utilise la méthodologie STAR pour évaluer les candidats.
    """

    def __init__(self, config: AgentConfig = None):
        if config is None:
            config = AgentConfig(
                name="RecruteurDZ",
                model="deepseek-chat",
                temperature=0.5,
                max_tokens=1500,
                language="fr",
                system_prompt=self._build_system_prompt()
            )
        super().__init__(config)
        self.interview_state = InterviewState()
        self.job_position: Optional[str] = None
        self.job_category: Optional[str] = None
        self.required_skills: List[str] = []
        self.experience_level: Optional[str] = None

    def _build_system_prompt(self) -> str:
        return """Tu es IA Recruteur DZ, un agent d'interview spécialisé dans la pré-qualification et l'évaluation des candidats pour le marché de l'emploi algérien.

MÉTHODOLOGIE STAR:
Pour chaque question comportementale, pousse le candidat à structurer:
- Situation: Contexte
- Tâche: Responsabilité
- Action: Ce qu'il a fait
- Résultat: Outcome mesurable

CONTEXTE MARCHÉ ALGÉRIEN:
- Diplômes valorisés: Ingéniorat, Licence/Master, formations professionnelles
- Langues: Français, Arabe, Anglais (tech), Darija
- Secteurs en tension: IT/Tech, Finance, Commercial, Industrie
- Particularités: importance du réseau, stabilité valorisée, diaspora

RÈGLES:
✅ Rester professionnel et respectueux
✅ Poser des questions ouvertes
✅ Écouter activement
✅ Demander des exemples concrets
✅ S'adapter au niveau de français du candidat
✅ Utiliser la méthode STAR

❌ JAMAIS de questions discriminatoires (âge, religion, situation familiale, origine)
❌ JAMAIS de questions sur la santé ou le handicap
❌ JAMAIS de jugements personnels
❌ JAMAIS de promesses non autorisées

TON: Professionnel, bienveillant, neutre, objectif"""

    def reset_interview(self):
        """Réinitialise l'état de l'entretien"""
        self.interview_state = InterviewState()
        self.job_position = None
        self.job_category = None
        self.required_skills = []
        self.experience_level = None

    def set_job_context(self, position: str, category: str, skills: List[str], level: str):
        """Définit le contexte du poste"""
        self.job_position = position
        self.job_category = category
        self.required_skills = skills
        self.experience_level = level

    def _get_phase_config(self) -> Dict[InterviewPhase, tuple]:
        """Retourne la config min/max échanges par phase"""
        return {
            InterviewPhase.INTRODUCTION: (1, 2),
            InterviewPhase.EXPERIENCE: (3, 4),
            InterviewPhase.TECHNICAL: (3, 5),
            InterviewPhase.SOFT_SKILLS: (2, 3),
            InterviewPhase.MOTIVATION: (2, 3),
            InterviewPhase.CLOSING: (1, 2)
        }

    def _should_advance_phase(self) -> bool:
        """Détermine si on doit passer à la phase suivante"""
        config = self._get_phase_config()
        min_exchanges, _ = config.get(self.interview_state.current_phase, (2, 3))
        return self.interview_state.phase_exchanges >= min_exchanges

    def _advance_phase(self):
        """Passe à la phase suivante"""
        phases = list(InterviewPhase)
        current_idx = phases.index(self.interview_state.current_phase)
        if current_idx < len(phases) - 1:
            self.interview_state.current_phase = phases[current_idx + 1]
            self.interview_state.phase_exchanges = 0

    def _detect_red_flags(self, response: str) -> List[str]:
        """Détecte les red flags dans la réponse"""
        detected = []
        response_lower = response.lower()

        # Critique excessive
        negative_words = ["nul", "incompétent", "mauvais patron", "entreprise pourrie", "collègues idiots"]
        if any(word in response_lower for word in negative_words):
            detected.append("critique excessive des anciens employeurs")

        # Réponses vagues
        if len(response) < 50 and "?" not in response:
            detected.append("réponses courtes/évasives")

        # Incohérences (à améliorer avec contexte)
        if "en fait" in response_lower and "mais" in response_lower:
            detected.append("possible incohérence détectée")

        return detected

    def _evaluate_response(self, response: str, skill_name: str, category: SkillCategory) -> SkillEvaluation:
        """Évalue une réponse pour une compétence donnée"""
        score = 3  # Score par défaut

        # Critères positifs
        if len(response) > 200:
            score += 0.5  # Réponse détaillée
        if any(word in response.lower() for word in ["résultat", "impact", "chiffre", "%", "augmentation", "réduction"]):
            score += 1  # Résultats quantifiés
        if any(word in response.lower() for word in ["j'ai", "j'ai fait", "j'ai décidé", "j'ai mis en place"]):
            score += 0.5  # Actions concrètes

        # Critères négatifs
        if len(response) < 50:
            score -= 1  # Réponse trop courte
        if "je ne sais pas" in response.lower() or "peut-être" in response.lower():
            score -= 0.5

        return SkillEvaluation(
            name=skill_name,
            category=category,
            score=max(1, min(5, int(score))),
            comment="Évaluation automatique",
            verbatim=response[:200] if len(response) > 200 else response
        )

    def _calculate_global_score(self) -> float:
        """Calcule le score global pondéré"""
        if not self.interview_state.evaluations:
            return 0

        weights = {
            SkillCategory.TECHNICAL: 0.35,
            SkillCategory.SOFT: 0.35,
            SkillCategory.CULTURE_FIT: 0.30
        }

        category_scores = {cat: [] for cat in SkillCategory}
        for eval in self.interview_state.evaluations:
            category_scores[eval.category].append(eval.score)

        weighted_score = 0
        for cat, scores in category_scores.items():
            if scores:
                avg = sum(scores) / len(scores)
                weighted_score += avg * weights[cat]

        # Pénalité pour red flags
        penalty = len(self.interview_state.red_flags) * 0.3

        return max(1, min(5, weighted_score - penalty))

    def _determine_recommendation(self, score: float) -> str:
        """Détermine la recommandation basée sur le score"""
        if score >= 4:
            return "recommended"
        elif score >= 3:
            return "review"
        elif score >= 2.5:
            return "reserve"
        else:
            return "rejected"

    def generate_report(self) -> str:
        """Génère le rapport d'évaluation du candidat"""
        global_score = self._calculate_global_score()
        recommendation = self._determine_recommendation(global_score)
        self.interview_state.recommendation = recommendation

        # Grouper les évaluations par catégorie
        tech_evals = [e for e in self.interview_state.evaluations if e.category == SkillCategory.TECHNICAL]
        soft_evals = [e for e in self.interview_state.evaluations if e.category == SkillCategory.SOFT]
        culture_evals = [e for e in self.interview_state.evaluations if e.category == SkillCategory.CULTURE_FIT]

        def avg_score(evals):
            return sum(e.score for e in evals) / len(evals) if evals else 0

        recommendation_labels = {
            "recommended": "✅ Recommandé - Passer à l'étape suivante",
            "review": "🔄 À revoir - Besoin d'un 2ème entretien",
            "reserve": "⚠️ Réserve - Points à clarifier",
            "rejected": "❌ Non recommandé"
        }

        report = f"""## 📋 Rapport d'Évaluation Candidat

**Candidat** : {self.interview_state.candidate.name or 'Anonyme'}
**Poste** : {self.job_position or 'Non défini'}
**Catégorie** : {JOB_CATEGORIES.get(self.job_category, {}).get('name', 'Non définie')}
**Date** : {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Durée** : {self.interview_state.total_exchanges} échanges

---

### 👤 Profil Résumé
- **Formation** : {self.interview_state.candidate.education or 'Non renseignée'}
- **Expérience** : {self.interview_state.candidate.experience_years or '?'} années
- **Langues** : {', '.join(self.interview_state.candidate.languages)}

---

### 📊 Évaluation

#### Compétences Techniques ({len(tech_evals)} évaluées)
| Compétence | Note /5 | Commentaire |
|------------|---------|-------------|
"""
        for e in tech_evals:
            report += f"| {e.name} | {'⭐' * e.score} | {e.comment} |\n"

        report += f"""
**Score Technique** : {avg_score(tech_evals):.1f}/5

#### Soft Skills ({len(soft_evals)} évaluées)
| Compétence | Note /5 | Commentaire |
|------------|---------|-------------|
"""
        for e in soft_evals:
            report += f"| {e.name} | {'⭐' * e.score} | {e.comment} |\n"

        report += f"""
**Score Soft Skills** : {avg_score(soft_evals):.1f}/5

#### Culture Fit ({len(culture_evals)} évaluées)
| Critère | Note /5 | Commentaire |
|---------|---------|-------------|
"""
        for e in culture_evals:
            report += f"| {e.name} | {'⭐' * e.score} | {e.comment} |\n"

        report += f"""
**Score Culture Fit** : {avg_score(culture_evals):.1f}/5

---

### ✅ Points Forts
"""
        for strength in self.interview_state.strengths[:5]:
            report += f"- {strength}\n"

        if not self.interview_state.strengths:
            report += "- Aucun point fort notable détecté\n"

        report += f"""
### ⚠️ Points de Vigilance
"""
        for flag in self.interview_state.red_flags[:5]:
            report += f"- {flag}\n"

        if not self.interview_state.red_flags:
            report += "- Aucun red flag détecté\n"

        report += f"""
---

### 💰 Attentes
- **Salaire actuel** : {self.interview_state.candidate.current_salary or 'Non mentionné'}
- **Salaire attendu** : {self.interview_state.candidate.expected_salary or 'Non mentionné'}
- **Disponibilité** : {self.interview_state.candidate.availability or 'Non mentionnée'}
- **Mobilité** : {'Oui' if self.interview_state.candidate.mobility else 'Non'}

---

### 🎯 Recommandation

**Score Global** : {global_score:.1f}/5

**Avis** : {recommendation_labels.get(recommendation, 'Non défini')}

---

### 📝 Verbatims Importants
"""
        for v in self.interview_state.verbatims[:3]:
            report += f'> "{v[:150]}..."\n\n'

        return report

    async def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        Exécute un tour de l'entretien.

        Args:
            input_data: {
                "message": str,           # Réponse du candidat
                "action": str,            # "start", "continue", "report"
                "mode": str,              # "evaluation", "simulation", "screening"
                "position": str,          # Intitulé du poste
                "category": str,          # Catégorie (tech, commercial, etc.)
                "skills": List[str],      # Compétences recherchées
                "experience_level": str   # junior, mid, senior
            }
        """
        action = input_data.get("action", "continue")
        mode = input_data.get("mode", "evaluation")

        # Démarrage de l'entretien
        if action == "start":
            self.reset_interview()
            self.interview_state.mode = InterviewMode(mode)
            self.set_job_context(
                position=input_data.get("position", ""),
                category=input_data.get("category", "tech"),
                skills=input_data.get("skills", []),
                level=input_data.get("experience_level", "mid")
            )

            category_info = JOB_CATEGORIES.get(self.job_category, {})

            if mode == "simulation":
                welcome = f"""Bonjour ! 👋 Je suis IA Recruteur, et je vais vous aider à vous préparer pour votre entretien.

**Simulation configurée :**
- 🎯 Poste visé : {self.job_position}
- 🏢 Secteur : {category_info.get('name', 'Non défini')}
- 📊 Niveau : {self.experience_level}

Je vais simuler un entretien réaliste. À la fin, vous recevrez un feedback détaillé.

---

**Commençons !**

{PHASE_QUESTIONS[InterviewPhase.INTRODUCTION][0]}"""
            else:
                welcome = f"""Bonjour ! 👋 Je suis IA Recruteur, votre assistant pour les entretiens de pré-qualification.

**Entretien configuré :**
- 🎯 Poste : {self.job_position}
- 🏢 Catégorie : {category_info.get('name', 'Non définie')}
- 📋 Compétences clés : {', '.join(self.required_skills[:5]) if self.required_skills else 'À évaluer'}
- 📊 Niveau : {self.experience_level}

---

**Phase 1 : Introduction**

{PHASE_QUESTIONS[InterviewPhase.INTRODUCTION][0]}"""

            return AgentResponse(
                content=welcome,
                metadata={
                    "phase": self.interview_state.current_phase.value,
                    "mode": mode,
                    "exchange": 0,
                    "action": "interview_started"
                }
            )

        # Génération du rapport
        if action == "report":
            report = self.generate_report()
            return AgentResponse(
                content=report,
                metadata={
                    "phase": "completed",
                    "global_score": self._calculate_global_score(),
                    "recommendation": self.interview_state.recommendation,
                    "action": "report_generated"
                }
            )

        # Continuer l'entretien
        user_message = input_data.get("message", "")

        # Détecter les red flags
        red_flags = self._detect_red_flags(user_message)
        self.interview_state.red_flags.extend(red_flags)

        # Capturer les verbatims importants
        if len(user_message) > 100:
            self.interview_state.verbatims.append(user_message)

        # Évaluer la réponse selon la phase
        if self.interview_state.current_phase == InterviewPhase.TECHNICAL:
            skill_name = self.required_skills[0] if self.required_skills else "Technique générale"
            eval = self._evaluate_response(user_message, skill_name, SkillCategory.TECHNICAL)
            self.interview_state.evaluations.append(eval)
        elif self.interview_state.current_phase == InterviewPhase.SOFT_SKILLS:
            eval = self._evaluate_response(user_message, "Communication", SkillCategory.SOFT)
            self.interview_state.evaluations.append(eval)
        elif self.interview_state.current_phase == InterviewPhase.MOTIVATION:
            eval = self._evaluate_response(user_message, "Motivation", SkillCategory.CULTURE_FIT)
            self.interview_state.evaluations.append(eval)

        # Détecter les points forts
        if len(user_message) > 200 and any(word in user_message.lower() for word in ["résultat", "réussi", "amélioré", "augmenté"]):
            self.interview_state.strengths.append(f"Bonne réponse phase {self.interview_state.current_phase.value}")

        # Mettre à jour les compteurs
        self.interview_state.phase_exchanges += 1
        self.interview_state.total_exchanges += 1

        # Construire le contexte pour le LLM
        category_info = JOB_CATEGORIES.get(self.job_category, {})
        technical_questions = category_info.get("questions", [])

        system_prompt = f"""{self._build_system_prompt()}

ENTRETIEN EN COURS:
- Poste: {self.job_position}
- Catégorie: {category_info.get('name', 'Non définie')}
- Compétences recherchées: {', '.join(self.required_skills)}
- Niveau: {self.experience_level}
- Phase actuelle: {self.interview_state.current_phase.value}
- Échange dans cette phase: {self.interview_state.phase_exchanges}

QUESTIONS SUGGÉRÉES POUR CETTE PHASE:
{chr(10).join(f'- {q}' for q in PHASE_QUESTIONS.get(self.interview_state.current_phase, []))}

{f"QUESTIONS TECHNIQUES SPÉCIFIQUES:{chr(10)}" + chr(10).join(f'- {q}' for q in technical_questions) if self.interview_state.current_phase == InterviewPhase.TECHNICAL else ''}

RED FLAGS DÉTECTÉS: {len(self.interview_state.red_flags)}
ÉVALUATIONS FAITES: {len(self.interview_state.evaluations)}

INSTRUCTIONS:
1. Analyse la réponse du candidat (méthode STAR si applicable)
2. Note les points positifs et négatifs
3. Pose UNE question de suivi pertinente
4. Reste bienveillant mais professionnel
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Réponse du candidat:\n\n{user_message}\n\nGénère ta prochaine question (UNE seule):"}
        ]

        response = await self._call_llm(messages)

        # Vérifier si on doit avancer de phase
        should_advance = self._should_advance_phase()
        if should_advance and self.interview_state.current_phase != InterviewPhase.CLOSING:
            self._advance_phase()
            phase_names = {
                InterviewPhase.EXPERIENCE: "Parcours & Expérience",
                InterviewPhase.TECHNICAL: "Compétences Techniques",
                InterviewPhase.SOFT_SKILLS: "Soft Skills",
                InterviewPhase.MOTIVATION: "Motivations & Projet",
                InterviewPhase.CLOSING: "Questions & Clôture"
            }
            phase_indicator = f"\n\n---\n**Phase : {phase_names.get(self.interview_state.current_phase, self.interview_state.current_phase.value)}**\n"
            response_content = phase_indicator + response['content']
        else:
            response_content = response['content']

        # Check si entretien terminé
        is_complete = (
            self.interview_state.current_phase == InterviewPhase.CLOSING and
            self.interview_state.phase_exchanges >= 2
        )

        if is_complete:
            response_content += "\n\n---\n✅ **Entretien terminé !** Tapez 'rapport' pour générer l'évaluation complète."

        return AgentResponse(
            content=response_content,
            tokens_used=response.get('tokens'),
            metadata={
                "phase": self.interview_state.current_phase.value,
                "exchange": self.interview_state.total_exchanges,
                "evaluations_count": len(self.interview_state.evaluations),
                "red_flags_count": len(self.interview_state.red_flags),
                "is_complete": is_complete
            }
        )


# Export pour découverte CLI
__all__ = ['RecruteurAgent', 'InterviewState', 'CandidateProfile', 'JOB_CATEGORIES', 'PHASE_QUESTIONS']
