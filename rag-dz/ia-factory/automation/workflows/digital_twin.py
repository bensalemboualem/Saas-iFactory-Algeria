"""
IA Factory Automation - Digital Twin Boualem
Clone IA authentique qui connaît Boualem, anticipe ses actions,
génère du contenu authentique et conseille stratégiquement
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, time
from enum import Enum
import json
import os

router = APIRouter(prefix="/twin", tags=["Digital Twin Boualem"])


class Context(str, Enum):
    BUSINESS = "business"
    TECHNICAL = "technical"
    PERSONAL = "personal"
    NETWORKING = "networking"
    STRATEGIC = "strategic"


class TaskType(str, Enum):
    EMAIL_REPLY = "email_reply"
    PROPOSAL_DRAFT = "proposal_draft"
    LINKEDIN_POST = "linkedin_post"
    CLIENT_MEETING_PREP = "client_meeting_prep"
    CODE_REVIEW = "code_review"
    STRATEGIC_DECISION = "strategic_decision"
    CONTENT_CREATION = "content_creation"


class Mood(str, Enum):
    FOCUSED = "focused"
    CREATIVE = "creative"
    STRATEGIC = "strategic"
    ENERGIZED = "energized"
    REFLECTIVE = "reflective"


# ===== PROFIL BOUALEM =====

BOUALEM_PROFILE = {
    "identity": {
        "name": "Boualem Chebaki",
        "title": "Fondateur & CEO IA Factory",
        "location": "Genève, Suisse 🇨🇭 + Alger, Algérie 🇩🇿",
        "mission": "Démocratiser l'IA en Algérie et accompagner les entreprises suisses",
        "tagline": "L'IA qui comprend votre contexte"
    },
    
    "background": {
        "experience_years": 15,
        "expertise": ["Python", "AI/ML", "RAG", "Multi-Agent Systems", "FastAPI"],
        "languages": ["Français", "Arabe", "Anglais"],
        "education": "Ingénieur Informatique",
        "previous_companies": ["Startups Tech", "Consulting", "Enterprise"],
        "entrepreneurial_ventures": 3
    },
    
    "personality": {
        "traits": [
            "Direct et pragmatique",
            "Orienté résultats",
            "Généreux en partage de connaissances",
            "Fier de ses racines algériennes",
            "Visionnaire mais réaliste"
        ],
        "communication_style": {
            "preferred": "Concis, percutant, avec exemples concrets",
            "avoid": "Jargon inutile, promesses vagues, buzzwords",
            "signature_phrases": [
                "L'action vaut mieux que la perfection",
                "Build in public",
                "Les excuses ne scalent pas",
                "L'IA amplifie, elle ne remplace pas"
            ]
        },
        "values": [
            "Excellence technique",
            "Impact local",
            "Souveraineté des données",
            "Entrepreneuriat algérien",
            "Automatisation intelligente"
        ]
    },
    
    "work_habits": {
        "peak_hours": ["06:00-09:00", "21:00-00:00"],
        "focus_blocks": 90,  # minutes
        "preferred_tools": ["VS Code", "Claude", "Cursor", "Notion", "Linear"],
        "meeting_style": "Court, structuré, avec action items",
        "response_time": {
            "urgent": "< 1h",
            "normal": "< 24h",
            "batch": "48h pour non-urgent"
        }
    },
    
    "business_context": {
        "company": "IA Factory",
        "markets": ["Suisse (B2B SaaS)", "Algérie (Transformation digitale)"],
        "ideal_clients": {
            "CH": "PME 50-500 employés, secteurs: finance, pharma, industrie",
            "DZ": "Grandes entreprises, ministères, banques, telecom"
        },
        "pricing_philosophy": "Premium pour la Suisse, accessible pour l'Algérie",
        "key_differentiators": [
            "Double culture CH/DZ",
            "Souveraineté des données",
            "Solutions sur-mesure",
            "Support bilingue"
        ]
    },
    
    "network": {
        "mentors": [],
        "partners": [],
        "key_clients": [],
        "strategic_contacts": {
            "Algérie Télécom": "Priorité haute - follow up en cours",
            "Infomaniak": "Partenaire hosting Suisse",
            "ICOSNET": "Partenaire hosting Algérie"
        }
    },
    
    "current_priorities": [
        "Multi-tenant infrastructure deployment",
        "Teaching Assistant MVP (quick win)",
        "Algérie Télécom follow-up (big deal)",
        "Content automation (leverage)",
        "Team expansion (DZ developers)"
    ],
    
    "writing_style": {
        "linkedin": {
            "tone": "Professionnel mais accessible",
            "structure": "Hook → Story → Insight → CTA",
            "emoji_usage": "Modéré (2-3 max)",
            "hashtags": "5 max, pertinents"
        },
        "email": {
            "tone": "Direct et respectueux",
            "structure": "Salutation → Point principal → Contexte → Next steps → Signature",
            "length": "Court (5-10 phrases max)"
        },
        "proposal": {
            "tone": "Professionnel et confiant",
            "focus": "ROI et résultats concrets",
            "avoid": "Survente, promesses irréalistes"
        }
    }
}


class MessageRequest(BaseModel):
    """Requête pour générer un message comme Boualem"""
    context: Context
    task_type: TaskType
    recipient: Optional[str] = None
    subject: str
    key_points: List[str] = Field(default_factory=list)
    tone_override: Optional[str] = None
    max_length: Optional[int] = None


class StrategicQuery(BaseModel):
    """Requête de conseil stratégique"""
    situation: str
    options: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    timeline: Optional[str] = None
    risk_tolerance: str = "moderate"


class AnticipatoryTask(BaseModel):
    """Tâche anticipée"""
    id: str
    task_type: TaskType
    description: str
    priority: int
    suggested_time: datetime
    estimated_duration: int  # minutes
    context: str
    auto_executable: bool


class DigitalTwin:
    """
    Digital Twin de Boualem
    Connaît son style, anticipe ses besoins, génère du contenu authentique
    """
    
    def __init__(self):
        self.profile = BOUALEM_PROFILE
        self.interaction_history: List[Dict] = []
        self.anticipated_tasks: List[AnticipatoryTask] = []
    
    async def generate_message(self, request: MessageRequest) -> Dict[str, Any]:
        """Génère un message dans le style de Boualem"""
        
        style = self.profile["writing_style"]
        personality = self.profile["personality"]
        
        # Sélectionner le style approprié
        if request.task_type == TaskType.EMAIL_REPLY:
            template = self._email_template(request)
        elif request.task_type == TaskType.LINKEDIN_POST:
            template = self._linkedin_template(request)
        elif request.task_type == TaskType.PROPOSAL_DRAFT:
            template = self._proposal_template(request)
        else:
            template = self._generic_template(request)
        
        # Appliquer le style Boualem
        message = self._apply_boualem_style(template, request.context)
        
        # Log interaction
        self.interaction_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": request.task_type.value,
            "context": request.context.value
        })
        
        return {
            "message": message,
            "style_applied": personality["communication_style"]["preferred"],
            "signature_phrase": self._get_relevant_phrase(request.context),
            "tips": self._get_context_tips(request.context)
        }
    
    def _email_template(self, request: MessageRequest) -> str:
        """Template email style Boualem"""
        
        greeting = f"Bonjour{f' {request.recipient}' if request.recipient else ''},"
        
        main_point = request.subject
        
        points = "\n".join([f"• {p}" for p in request.key_points]) if request.key_points else ""
        
        closing = """
À disposition pour en discuter.

Bien à vous,
Boualem

--
Boualem Chebaki
Fondateur, IA Factory
📧 boualem@iafactory.ch
🌐 www.iafactory.ch
"""
        
        return f"""
{greeting}

{main_point}

{points}

{closing}
""".strip()
    
    def _linkedin_template(self, request: MessageRequest) -> str:
        """Template LinkedIn style Boualem"""
        
        hooks = self.profile["personality"]["communication_style"]["signature_phrases"]
        import random
        hook = random.choice(hooks) if not request.key_points else request.key_points[0]
        
        story = request.subject
        
        insight = "💡 " + (request.key_points[1] if len(request.key_points) > 1 else "L'action vaut mieux que la perfection.")
        
        cta = """
📩 Vous voulez en savoir plus?
Commentez ou DM 👇

#IAFactory #IA #Automation #Algeria #Switzerland
"""
        
        return f"""
{hook}

{story}

{insight}

{cta}
""".strip()
    
    def _proposal_template(self, request: MessageRequest) -> str:
        """Template proposition style Boualem"""
        
        return f"""
PROPOSITION: {request.subject}

Pour: {request.recipient or '[Client]'}
De: Boualem Chebaki, IA Factory
Date: {datetime.now().strftime('%d/%m/%Y')}

---

CONTEXTE
{request.subject}

SOLUTION PROPOSÉE
{chr(10).join(['• ' + p for p in request.key_points]) if request.key_points else '• Solution sur-mesure adaptée à vos besoins'}

POURQUOI IA FACTORY
• 15 ans d'expertise en développement
• Double culture Suisse/Algérie
• Souveraineté des données garantie
• Support réactif et personnalisé

PROCHAINES ÉTAPES
1. Call de découverte (30 min)
2. Analyse détaillée de vos besoins
3. Proposition technique et commerciale

---

Boualem Chebaki
Fondateur, IA Factory
boualem@iafactory.ch | +41 XX XXX XX XX
""".strip()
    
    def _generic_template(self, request: MessageRequest) -> str:
        """Template générique"""
        return f"""
{request.subject}

{chr(10).join(['• ' + p for p in request.key_points]) if request.key_points else ''}

-- Boualem
""".strip()
    
    def _apply_boualem_style(self, content: str, context: Context) -> str:
        """Applique les touches stylistiques de Boualem"""
        
        # Raccourcir les phrases longues
        sentences = content.split(". ")
        styled_sentences = []
        
        for sentence in sentences:
            if len(sentence) > 150:
                # Découper
                parts = sentence.split(", ")
                if len(parts) > 2:
                    sentence = ". ".join([", ".join(parts[:2]), ", ".join(parts[2:])])
            styled_sentences.append(sentence)
        
        content = ". ".join(styled_sentences)
        
        # Ajouter une touche personnelle selon le contexte
        if context == Context.BUSINESS:
            content = content.replace("Je pense que", "Concrètement,")
            content = content.replace("peut-être", "")
        
        if context == Context.TECHNICAL:
            content = content.replace("on pourrait", "voici l'approche:")
        
        return content
    
    def _get_relevant_phrase(self, context: Context) -> str:
        """Retourne une phrase signature pertinente"""
        
        phrases = self.profile["personality"]["communication_style"]["signature_phrases"]
        
        context_phrases = {
            Context.BUSINESS: "L'action vaut mieux que la perfection",
            Context.TECHNICAL: "L'IA amplifie, elle ne remplace pas",
            Context.STRATEGIC: "Les excuses ne scalent pas",
            Context.PERSONAL: "Build in public",
            Context.NETWORKING: "L'action vaut mieux que la perfection"
        }
        
        return context_phrases.get(context, phrases[0])
    
    def _get_context_tips(self, context: Context) -> List[str]:
        """Conseils contextuels"""
        
        tips = {
            Context.BUSINESS: [
                "Toujours inclure next steps concrets",
                "Mentionner le ROI ou impact chiffré",
                "Proposer un call court (15-30 min)"
            ],
            Context.TECHNICAL: [
                "Inclure exemples de code si pertinent",
                "Référencer la documentation",
                "Proposer une démo live"
            ],
            Context.STRATEGIC: [
                "Lister les options avec pros/cons",
                "Définir les critères de décision",
                "Fixer une deadline de décision"
            ]
        }
        
        return tips.get(context, ["Rester concis et actionnable"])
    
    async def get_strategic_advice(self, query: StrategicQuery) -> Dict[str, Any]:
        """
        Conseil stratégique basé sur le profil et l'historique de Boualem
        """
        
        # Analyser la situation selon les valeurs de Boualem
        values = self.profile["personality"]["values"]
        priorities = self.profile["current_priorities"]
        
        # Évaluer chaque option
        evaluated_options = []
        
        for option in query.options:
            score = 0
            reasoning = []
            
            # Alignement avec les valeurs
            if "algérie" in option.lower() or "dz" in option.lower():
                score += 20
                reasoning.append("✓ Aligné avec l'impact local en Algérie")
            
            if "automatisation" in option.lower() or "ia" in option.lower():
                score += 15
                reasoning.append("✓ Utilise l'IA comme levier")
            
            if "roi" in option.lower() or "revenu" in option.lower():
                score += 15
                reasoning.append("✓ Focus sur les résultats business")
            
            # Vérifier les contraintes
            for constraint in query.constraints:
                if constraint.lower() in option.lower():
                    score -= 10
                    reasoning.append(f"⚠ Contrainte: {constraint}")
            
            evaluated_options.append({
                "option": option,
                "score": score,
                "reasoning": reasoning
            })
        
        # Trier par score
        evaluated_options.sort(key=lambda x: x["score"], reverse=True)
        
        # Recommandation
        best_option = evaluated_options[0] if evaluated_options else None
        
        return {
            "situation_analysis": f"Situation analysée selon les priorités actuelles de Boualem: {', '.join(priorities[:3])}",
            "evaluated_options": evaluated_options,
            "recommendation": {
                "choice": best_option["option"] if best_option else "Besoin de plus d'options",
                "confidence": min(best_option["score"] / 50 * 100, 100) if best_option else 0,
                "reasoning": best_option["reasoning"] if best_option else []
            },
            "boualem_would_say": self._get_relevant_phrase(Context.STRATEGIC),
            "next_steps": [
                "Valider avec les parties prenantes",
                "Définir les KPIs de succès",
                "Fixer le premier milestone (2 semaines max)"
            ]
        }
    
    async def anticipate_tasks(self, current_context: Dict[str, Any]) -> List[AnticipatoryTask]:
        """
        Anticipe les tâches que Boualem devrait faire
        basé sur son profil et le contexte actuel
        """
        
        now = datetime.now()
        tasks = []
        
        # Basé sur les priorités actuelles
        priorities = self.profile["current_priorities"]
        
        # Task 1: Follow-up Algérie Télécom (priorité haute)
        if "Algérie Télécom" in str(self.profile["network"]["strategic_contacts"]):
            tasks.append(AnticipatoryTask(
                id="task_001",
                task_type=TaskType.EMAIL_REPLY,
                description="Follow-up Algérie Télécom - relancer le contact",
                priority=1,
                suggested_time=now.replace(hour=9, minute=0),
                estimated_duration=15,
                context="Deal stratégique en cours",
                auto_executable=False
            ))
        
        # Task 2: LinkedIn post (maintenir la visibilité)
        tasks.append(AnticipatoryTask(
            id="task_002",
            task_type=TaskType.LINKEDIN_POST,
            description="Post LinkedIn quotidien - partager une insight IA",
            priority=2,
            suggested_time=now.replace(hour=8, minute=30),
            estimated_duration=20,
            context="Personal branding et génération de leads",
            auto_executable=True
        ))
        
        # Task 3: Revue de code (si projets en cours)
        tasks.append(AnticipatoryTask(
            id="task_003",
            task_type=TaskType.CODE_REVIEW,
            description="Review PR des développeurs",
            priority=3,
            suggested_time=now.replace(hour=10, minute=0),
            estimated_duration=30,
            context="Quality assurance",
            auto_executable=False
        ))
        
        # Task 4: Préparation meetings (basé sur calendrier)
        if current_context.get("upcoming_meetings"):
            for meeting in current_context["upcoming_meetings"][:2]:
                tasks.append(AnticipatoryTask(
                    id=f"task_meeting_{meeting.get('id', 'xxx')}",
                    task_type=TaskType.CLIENT_MEETING_PREP,
                    description=f"Préparer le meeting: {meeting.get('title', 'Client call')}",
                    priority=2,
                    suggested_time=meeting.get("time", now) - timedelta(hours=1),
                    estimated_duration=30,
                    context="Préparation client",
                    auto_executable=False
                ))
        
        # Trier par priorité
        tasks.sort(key=lambda x: x.priority)
        
        self.anticipated_tasks = tasks
        
        return tasks
    
    async def get_daily_brief(self) -> Dict[str, Any]:
        """
        Brief quotidien pour Boualem
        Résumé de ce qu'il doit faire aujourd'hui
        """
        
        now = datetime.now()
        
        # Générer les tâches anticipées
        tasks = await self.anticipate_tasks({})
        
        # Peak hours
        peak_hours = self.profile["work_habits"]["peak_hours"]
        
        # Priorities
        priorities = self.profile["current_priorities"]
        
        return {
            "date": now.strftime("%A %d %B %Y"),
            "greeting": self._get_greeting(now.hour),
            "focus_of_the_day": priorities[0],
            "peak_hours": peak_hours,
            "tasks_today": [
                {
                    "description": t.description,
                    "time": t.suggested_time.strftime("%H:%M"),
                    "duration": f"{t.estimated_duration} min",
                    "auto": "🤖" if t.auto_executable else "👤"
                }
                for t in tasks[:5]
            ],
            "motivation": self._get_relevant_phrase(Context.PERSONAL),
            "reminder": "L'action vaut mieux que la perfection. Commence par la tâche la plus impactante."
        }
    
    def _get_greeting(self, hour: int) -> str:
        """Greeting personnalisé selon l'heure"""
        if hour < 6:
            return "Nuit productive, Boualem 🌙"
        elif hour < 12:
            return "Bonjour Boualem ☀️"
        elif hour < 18:
            return "Bon après-midi Boualem 💪"
        else:
            return "Bonne soirée Boualem 🌅"


# Instance globale
digital_twin = DigitalTwin()


# Routes API

@router.get("/profile")
async def get_profile():
    """Retourne le profil complet de Boualem"""
    return digital_twin.profile


@router.post("/generate-message")
async def generate_message(request: MessageRequest):
    """
    Génère un message dans le style authentique de Boualem
    """
    return await digital_twin.generate_message(request)


@router.post("/strategic-advice")
async def get_strategic_advice(query: StrategicQuery):
    """
    Obtient un conseil stratégique basé sur le profil de Boualem
    """
    return await digital_twin.get_strategic_advice(query)


@router.get("/daily-brief")
async def get_daily_brief():
    """
    Brief quotidien: tâches anticipées et focus du jour
    """
    return await digital_twin.get_daily_brief()


@router.get("/anticipated-tasks")
async def get_anticipated_tasks():
    """
    Retourne les tâches anticipées pour Boualem
    """
    tasks = await digital_twin.anticipate_tasks({})
    return {
        "tasks": [
            {
                "id": t.id,
                "type": t.task_type.value,
                "description": t.description,
                "priority": t.priority,
                "time": t.suggested_time.isoformat(),
                "duration": t.estimated_duration,
                "auto_executable": t.auto_executable
            }
            for t in tasks
        ]
    }


@router.get("/style-guide")
async def get_style_guide():
    """
    Guide de style pour écrire comme Boualem
    """
    return {
        "personality": digital_twin.profile["personality"],
        "writing_style": digital_twin.profile["writing_style"],
        "signature_phrases": digital_twin.profile["personality"]["communication_style"]["signature_phrases"],
        "avoid": digital_twin.profile["personality"]["communication_style"]["avoid"]
    }


@router.get("/priorities")
async def get_current_priorities():
    """
    Priorités actuelles de Boualem
    """
    return {
        "priorities": digital_twin.profile["current_priorities"],
        "focus": digital_twin.profile["current_priorities"][0],
        "strategic_contacts": digital_twin.profile["network"]["strategic_contacts"]
    }
