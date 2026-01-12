"""
IA Factory Automation - Social Media Manager
Automatisation complète de la présence réseaux sociaux
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import json
import os

router = APIRouter(prefix="/social", tags=["Social Media Manager"])


class Platform(str, Enum):
    LINKEDIN = "LinkedIn"
    X = "X"
    INSTAGRAM = "Instagram"
    YOUTUBE = "YouTube"
    TIKTOK = "TikTok"
    FACEBOOK = "Facebook"


class ContentType(str, Enum):
    POST = "post"
    CAROUSEL = "carousel"
    VIDEO_SCRIPT = "video_script"
    THREAD = "thread"
    ARTICLE = "article"
    STORY = "story"


class ToneOfVoice(str, Enum):
    PROFESSIONAL = "Professionnel"
    INSPIRATIONAL = "Inspirant"
    EDUCATIONAL = "Éducatif"
    PROVOCATIVE = "Provocateur"
    CASUAL = "Décontracté"
    EXPERT = "Expert"


class ContentTheme(str, Enum):
    AI_INNOVATION = "Innovation IA"
    DZ_SUCCESS = "Success Stories DZ"
    TECH_TUTORIAL = "Tutoriel Tech"
    BEHIND_SCENES = "Coulisses"
    CLIENT_CASE = "Cas Client"
    INDUSTRY_INSIGHT = "Analyse Marché"
    PERSONAL_BRAND = "Personal Branding"
    PRODUCT_LAUNCH = "Lancement Produit"


class ContentRequest(BaseModel):
    """Requête de génération de contenu"""
    platforms: List[Platform]
    content_type: ContentType
    theme: ContentTheme
    topic: str
    key_messages: List[str] = Field(default_factory=list)
    tone: ToneOfVoice = ToneOfVoice.PROFESSIONAL
    include_hashtags: bool = True
    include_cta: bool = True
    language: str = "fr"
    market_focus: str = "DZ"  # DZ, CH, or both


class ScheduledPost(BaseModel):
    """Post programmé"""
    id: str
    platform: Platform
    content: str
    media_suggestion: Optional[str]
    hashtags: List[str]
    scheduled_time: datetime
    status: str = "scheduled"
    engagement_prediction: float = 0.0


class GeneratedContent(BaseModel):
    """Contenu généré"""
    platform: Platform
    content: str
    media_suggestions: List[str]
    hashtags: List[str]
    best_posting_times: List[str]
    engagement_tips: List[str]


class ContentCalendar(BaseModel):
    """Calendrier de contenu"""
    week_start: datetime
    week_end: datetime
    posts: List[ScheduledPost]
    theme_distribution: Dict[str, int]


class SocialMediaManager:
    """
    Gestionnaire de contenu réseaux sociaux
    Génère, planifie et optimise le contenu pour Boualem
    """
    
    # Templates de posts par plateforme
    PLATFORM_TEMPLATES = {
        Platform.LINKEDIN: {
            "max_chars": 3000,
            "optimal_chars": 1200,
            "hashtag_count": 5,
            "structure": """
{hook}

{story}

{insight}

{cta}

{hashtags}
""",
            "best_times": ["08:00", "12:00", "17:30"]
        },
        Platform.X: {
            "max_chars": 280,
            "optimal_chars": 250,
            "hashtag_count": 2,
            "structure": "{hook} {message} {hashtags}",
            "best_times": ["09:00", "12:00", "18:00", "21:00"]
        },
        Platform.INSTAGRAM: {
            "max_chars": 2200,
            "optimal_chars": 500,
            "hashtag_count": 15,
            "structure": """
{hook}

{story}

{cta}

.
.
.
{hashtags}
""",
            "best_times": ["11:00", "14:00", "19:00"]
        }
    }
    
    # Hooks éprouvés style Boualem
    HOOKS_BOUALEM = [
        "🚀 Ce que personne ne vous dit sur l'IA en Algérie...",
        "J'ai généré 3 propositions commerciales en 10 minutes. Voici comment 👇",
        "💡 L'erreur que font 90% des entreprises DZ avec l'IA",
        "En 2024, j'ai automatisé 80% de mon business. Le résultat?",
        "🎯 3 outils IA qui m'ont fait gagner 20h/semaine",
        "L'IA ne remplace pas. Elle AMPLIFIE. Voici la preuve:",
        "De développeur à entrepreneur IA: le parcours qui a tout changé",
        "🔥 Pourquoi l'Algérie sera le prochain hub IA africain",
        "J'ai testé GPT-4, Claude, Gemini. Le gagnant est...",
        "La souveraineté des données: ce que les décideurs DZ doivent savoir"
    ]
    
    def __init__(self):
        self.scheduled_posts: Dict[str, ScheduledPost] = {}
        self.content_history: List[GeneratedContent] = []
    
    async def generate_content(
        self,
        request: ContentRequest
    ) -> List[GeneratedContent]:
        """Génère du contenu pour les plateformes demandées"""
        
        contents = []
        
        for platform in request.platforms:
            content = await self._generate_for_platform(
                platform=platform,
                request=request
            )
            contents.append(content)
            self.content_history.append(content)
        
        return contents
    
    async def _generate_for_platform(
        self,
        platform: Platform,
        request: ContentRequest
    ) -> GeneratedContent:
        """Génère du contenu pour une plateforme spécifique"""
        
        template = self.PLATFORM_TEMPLATES.get(platform)
        
        if not template:
            template = self.PLATFORM_TEMPLATES[Platform.LINKEDIN]
        
        # Générer hook personnalisé
        import random
        hook = random.choice(self.HOOKS_BOUALEM)
        
        # Adapter selon le thème
        if request.theme == ContentTheme.CLIENT_CASE:
            hook = f"🎯 Success Story: {request.topic}"
        elif request.theme == ContentTheme.TECH_TUTORIAL:
            hook = f"💡 Tutorial: {request.topic} - Thread 🧵"
        elif request.theme == ContentTheme.PRODUCT_LAUNCH:
            hook = f"🚀 Nouveau: {request.topic}!"
        
        # Générer le contenu principal
        story = self._generate_story(request)
        insight = self._generate_insight(request)
        cta = self._generate_cta(request.market_focus)
        
        # Hashtags intelligents
        hashtags = self._generate_hashtags(
            request.theme,
            request.market_focus,
            template["hashtag_count"]
        )
        
        # Assembler le contenu
        content = template["structure"].format(
            hook=hook,
            story=story,
            message=story[:200] if platform == Platform.X else story,
            insight=insight,
            cta=cta if request.include_cta else "",
            hashtags=" ".join(hashtags) if request.include_hashtags else ""
        )
        
        # Limiter aux caractères max
        if len(content) > template["max_chars"]:
            content = content[:template["max_chars"]-3] + "..."
        
        # Suggestions médias
        media = self._suggest_media(platform, request.content_type, request.theme)
        
        return GeneratedContent(
            platform=platform,
            content=content.strip(),
            media_suggestions=media,
            hashtags=hashtags,
            best_posting_times=template["best_times"],
            engagement_tips=self._get_engagement_tips(platform)
        )
    
    def _generate_story(self, request: ContentRequest) -> str:
        """Génère le corps du post"""
        
        # Story personnalisée selon le thème
        stories = {
            ContentTheme.AI_INNOVATION: f"""
L'IA transforme chaque industrie. En Algérie, nous construisons des solutions qui comprennent le contexte local.

{request.topic}

Ce n'est pas juste de la technologie. C'est une révolution dans la façon de travailler.
""",
            ContentTheme.DZ_SUCCESS: f"""
Quand on dit que l'Algérie peut innover, certains doutent.

Pourtant, {request.topic}

Les preuves sont là. Les talents aussi. Il suffit de les libérer.
""",
            ContentTheme.TECH_TUTORIAL: f"""
Voici comment implémenter {request.topic} en 3 étapes:

1️⃣ Configuration initiale
2️⃣ Intégration API
3️⃣ Automatisation

Simple, efficace, reproductible.
""",
            ContentTheme.CLIENT_CASE: f"""
Client: [Entreprise DZ]
Challenge: {request.topic}
Solution: IA Factory

Résultat:
→ -70% temps de traitement
→ +40% productivité
→ ROI en 3 mois
""",
            ContentTheme.PERSONAL_BRAND: f"""
15 ans de code.
3 entreprises créées.
1 mission: démocratiser l'IA en Algérie.

{request.topic}

Mon parcours n'est pas unique. Il est reproductible.
"""
        }
        
        return stories.get(request.theme, request.topic)
    
    def _generate_insight(self, request: ContentRequest) -> str:
        """Génère l'insight/takeaway"""
        
        insights = {
            ContentTheme.AI_INNOVATION: "💡 L'IA n'est pas le futur. C'est le présent. Et ceux qui attendent seront dépassés.",
            ContentTheme.DZ_SUCCESS: "💡 L'Algérie a tout pour réussir: talents, marché, ambition. Il manque juste l'exécution.",
            ContentTheme.TECH_TUTORIAL: "💡 La meilleure technologie est celle qui disparaît derrière l'usage.",
            ContentTheme.CLIENT_CASE: "💡 Chaque entreprise peut automatiser 80% de ses tâches répétitives.",
            ContentTheme.PERSONAL_BRAND: "💡 Votre expertise + IA = Superpouvoir professionnel."
        }
        
        return insights.get(request.theme, "💡 L'action vaut mieux que la perfection.")
    
    def _generate_cta(self, market_focus: str) -> str:
        """Génère l'appel à l'action"""
        
        ctas = {
            "DZ": """
📩 Vous voulez automatiser votre business?
→ contact@iafactory.dz
→ www.iafactory.dz/demo
""",
            "CH": """
📩 Parlons de votre transformation IA
→ contact@iafactory.ch
→ Calendly: iafactory.ch/meeting
""",
            "both": """
📩 Prêt à passer à l'action?
🇨🇭 contact@iafactory.ch
🇩🇿 contact@iafactory.dz
"""
        }
        
        return ctas.get(market_focus, ctas["both"])
    
    def _generate_hashtags(
        self,
        theme: ContentTheme,
        market: str,
        count: int
    ) -> List[str]:
        """Génère des hashtags pertinents"""
        
        base_hashtags = ["#IAFactory", "#IA", "#Automation"]
        
        theme_hashtags = {
            ContentTheme.AI_INNOVATION: ["#IntelligenceArtificielle", "#Tech", "#Innovation", "#FutureOfWork"],
            ContentTheme.DZ_SUCCESS: ["#Algeria", "#DZ", "#AfricaTech", "#StartupDZ", "#MadeInAlgeria"],
            ContentTheme.TECH_TUTORIAL: ["#Tutorial", "#DevTips", "#Coding", "#Python", "#API"],
            ContentTheme.CLIENT_CASE: ["#CaseStudy", "#DigitalTransformation", "#ROI", "#BusinessIA"],
            ContentTheme.PERSONAL_BRAND: ["#Entrepreneur", "#TechFounder", "#Leadership", "#Startup"]
        }
        
        market_hashtags = {
            "DZ": ["#Algerie", "#Alger", "#DZ"],
            "CH": ["#Suisse", "#Geneva", "#SwissTech"],
            "both": ["#Algeria", "#Suisse", "#Global"]
        }
        
        all_tags = (
            base_hashtags +
            theme_hashtags.get(theme, [])[:3] +
            market_hashtags.get(market, [])[:2]
        )
        
        return all_tags[:count]
    
    def _suggest_media(
        self,
        platform: Platform,
        content_type: ContentType,
        theme: ContentTheme
    ) -> List[str]:
        """Suggère des médias appropriés"""
        
        suggestions = []
        
        if platform == Platform.INSTAGRAM or platform == Platform.TIKTOK:
            suggestions.append("Vidéo courte (< 60s) avec texte en overlay")
        
        if platform == Platform.LINKEDIN:
            if content_type == ContentType.CAROUSEL:
                suggestions.append("Carousel PDF 5-10 slides, design épuré")
            else:
                suggestions.append("Image 1200x627 avec citation ou stat clé")
        
        if theme == ContentTheme.TECH_TUTORIAL:
            suggestions.append("Screen recording avec annotations")
            suggestions.append("Diagram explicatif (Excalidraw, Miro)")
        
        if theme == ContentTheme.CLIENT_CASE:
            suggestions.append("Before/After visualization")
            suggestions.append("Testimonial video du client (30s)")
        
        suggestions.append("Photo authentique Boualem (pas stock)")
        
        return suggestions
    
    def _get_engagement_tips(self, platform: Platform) -> List[str]:
        """Conseils d'engagement par plateforme"""
        
        tips = {
            Platform.LINKEDIN: [
                "Répondre à tous les commentaires dans l'heure",
                "Poser une question ouverte à la fin",
                "Taguer 2-3 personnes pertinentes",
                "Partager sur 3-5 groupes LinkedIn DZ/CH"
            ],
            Platform.X: [
                "Thread pour sujets complexes",
                "Répondre aux comptes influents",
                "Utiliser les spaces pour discussions live"
            ],
            Platform.INSTAGRAM: [
                "Stories quotidiennes (coulisses)",
                "Réels pour maximum de reach",
                "Hashtags dans premier commentaire"
            ]
        }
        
        return tips.get(platform, ["Engager authentiquement avec l'audience"])
    
    async def schedule_post(
        self,
        content: GeneratedContent,
        scheduled_time: datetime
    ) -> ScheduledPost:
        """Planifie un post pour publication"""
        
        post_id = f"post_{datetime.now().strftime('%Y%m%d%H%M%S')}_{content.platform.value}"
        
        post = ScheduledPost(
            id=post_id,
            platform=content.platform,
            content=content.content,
            media_suggestion=content.media_suggestions[0] if content.media_suggestions else None,
            hashtags=content.hashtags,
            scheduled_time=scheduled_time,
            status="scheduled",
            engagement_prediction=0.75  # À calculer avec ML
        )
        
        self.scheduled_posts[post_id] = post
        
        return post
    
    async def generate_weekly_calendar(
        self,
        week_start: datetime
    ) -> ContentCalendar:
        """Génère un calendrier de contenu pour la semaine"""
        
        posts = []
        themes_count = {theme.value: 0 for theme in ContentTheme}
        
        # Distribution recommandée par jour
        schedule = [
            (0, Platform.LINKEDIN, ContentTheme.AI_INNOVATION),  # Lundi
            (1, Platform.X, ContentTheme.TECH_TUTORIAL),         # Mardi
            (2, Platform.LINKEDIN, ContentTheme.CLIENT_CASE),    # Mercredi
            (3, Platform.INSTAGRAM, ContentTheme.BEHIND_SCENES), # Jeudi
            (4, Platform.LINKEDIN, ContentTheme.PERSONAL_BRAND), # Vendredi
        ]
        
        for day_offset, platform, theme in schedule:
            post_date = week_start + timedelta(days=day_offset)
            
            # Créer le post
            request = ContentRequest(
                platforms=[platform],
                content_type=ContentType.POST,
                theme=theme,
                topic=f"Automated content for {theme.value}",
                tone=ToneOfVoice.PROFESSIONAL,
                market_focus="DZ"
            )
            
            contents = await self.generate_content(request)
            
            if contents:
                post = await self.schedule_post(
                    contents[0],
                    post_date.replace(hour=9, minute=0)
                )
                posts.append(post)
                themes_count[theme.value] += 1
        
        return ContentCalendar(
            week_start=week_start,
            week_end=week_start + timedelta(days=6),
            posts=posts,
            theme_distribution=themes_count
        )


# Instance globale
social_manager = SocialMediaManager()


# Routes API

@router.post("/generate", response_model=List[GeneratedContent])
async def generate_content(request: ContentRequest):
    """
    Génère du contenu pour les plateformes spécifiées
    Style Boualem authentique
    """
    return await social_manager.generate_content(request)


@router.post("/schedule")
async def schedule_post(
    platform: Platform,
    content_type: ContentType,
    theme: ContentTheme,
    topic: str,
    scheduled_time: datetime
):
    """
    Planifie un post pour publication ultérieure
    """
    request = ContentRequest(
        platforms=[platform],
        content_type=content_type,
        theme=theme,
        topic=topic
    )
    
    contents = await social_manager.generate_content(request)
    
    if not contents:
        raise HTTPException(status_code=500, detail="Failed to generate content")
    
    post = await social_manager.schedule_post(contents[0], scheduled_time)
    
    return {
        "status": "scheduled",
        "post_id": post.id,
        "scheduled_time": post.scheduled_time.isoformat(),
        "platform": post.platform.value
    }


@router.get("/calendar/weekly")
async def get_weekly_calendar(week_start: Optional[str] = None):
    """
    Génère le calendrier de contenu de la semaine
    """
    if week_start:
        start_date = datetime.fromisoformat(week_start)
    else:
        # Cette semaine
        today = datetime.now()
        start_date = today - timedelta(days=today.weekday())
    
    calendar = await social_manager.generate_weekly_calendar(start_date)
    
    return {
        "week": f"{calendar.week_start.strftime('%d/%m')} - {calendar.week_end.strftime('%d/%m/%Y')}",
        "total_posts": len(calendar.posts),
        "theme_distribution": calendar.theme_distribution,
        "posts": [
            {
                "id": p.id,
                "platform": p.platform.value,
                "scheduled": p.scheduled_time.isoformat(),
                "preview": p.content[:100] + "..."
            }
            for p in calendar.posts
        ]
    }


@router.get("/scheduled")
async def list_scheduled_posts(
    platform: Optional[Platform] = None,
    status: Optional[str] = None
):
    """Liste tous les posts planifiés"""
    posts = list(social_manager.scheduled_posts.values())
    
    if platform:
        posts = [p for p in posts if p.platform == platform]
    
    if status:
        posts = [p for p in posts if p.status == status]
    
    return posts


@router.get("/hooks")
async def get_hooks():
    """Retourne les hooks éprouvés style Boualem"""
    return {
        "hooks": social_manager.HOOKS_BOUALEM,
        "usage": "Utilisez ces hooks comme démarrage de vos posts"
    }


@router.get("/templates/{platform}")
async def get_platform_template(platform: Platform):
    """Retourne le template pour une plateforme"""
    template = social_manager.PLATFORM_TEMPLATES.get(platform)
    
    if not template:
        raise HTTPException(status_code=404, detail="Platform not found")
    
    return template
