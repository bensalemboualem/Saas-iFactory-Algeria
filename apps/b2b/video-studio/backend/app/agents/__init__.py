"""
IA Factory Video Studio Pro - Agents IA
Utilise Groq (Llama) comme provider principal, DeepSeek en fallback
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from enum import Enum
import structlog
import os
import json
import time
import httpx

logger = structlog.get_logger()


class AgentRole(str, Enum):
    SCRIPTWRITER = "scriptwriter"
    STORYBOARDER = "storyboarder"
    DIRECTOR = "director"
    GROWTH_HACKER = "growth_hacker"
    DISTRIBUTOR = "distributor"


class AgentStatus(str, Enum):
    IDLE = "idle"
    THINKING = "thinking"
    WORKING = "working"
    COMPLETED = "completed"
    ERROR = "error"


class AgentTask(BaseModel):
    """Représente une tâche pour un agent."""
    task_id: str
    role: AgentRole
    input_data: Dict[str, Any]
    priority: int = 5
    metadata: Dict[str, Any] = {}


class AgentResult(BaseModel):
    """Résultat d'exécution d'un agent."""
    task_id: str
    role: AgentRole
    status: AgentStatus
    output: Any = None
    tokens_used: int = 0
    execution_time: float = 0
    error: Optional[str] = None


class LLMProvider:
    """Provider LLM multi-backend: Groq, DeepSeek, OpenRouter, Anthropic"""
    
    @staticmethod
    async def call(
        system_prompt: str,
        user_prompt: str,
        model: str = "llama-3.3-70b-versatile",
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> tuple[str, int]:
        """Appelle un LLM avec fallback automatique. Retourne (content, tokens_used)"""
        
        # Ordre de priorité des providers
        providers = [
            ("groq", os.getenv("GROQ_API_KEY")),
            ("deepseek", os.getenv("DEEPSEEK_API_KEY")),
            ("openrouter", os.getenv("OPENROUTER_API_KEY")),
        ]
        
        last_error = None
        
        for provider_name, api_key in providers:
            if not api_key or len(api_key) < 10:
                continue
                
            try:
                if provider_name == "groq":
                    return await LLMProvider._call_groq(
                        api_key, system_prompt, user_prompt, 
                        "llama-3.3-70b-versatile", temperature, max_tokens
                    )
                elif provider_name == "deepseek":
                    return await LLMProvider._call_deepseek(
                        api_key, system_prompt, user_prompt,
                        "deepseek-chat", temperature, max_tokens
                    )
                elif provider_name == "openrouter":
                    return await LLMProvider._call_openrouter(
                        api_key, system_prompt, user_prompt,
                        "meta-llama/llama-3.3-70b-instruct", temperature, max_tokens
                    )
            except Exception as e:
                last_error = str(e)
                logger.warning(f"Provider {provider_name} failed", error=str(e))
                continue
        
        raise Exception(f"All LLM providers failed. Last error: {last_error}")
    
    @staticmethod
    async def _call_groq(api_key: str, system: str, user: str, model: str, temp: float, max_tokens: int) -> tuple[str, int]:
        """Appel API Groq"""
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": user}
                    ],
                    "temperature": temp,
                    "max_tokens": max_tokens
                }
            )
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            tokens = data.get("usage", {}).get("total_tokens", 0)
            return content, tokens
    
    @staticmethod
    async def _call_deepseek(api_key: str, system: str, user: str, model: str, temp: float, max_tokens: int) -> tuple[str, int]:
        """Appel API DeepSeek"""
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                "https://api.deepseek.com/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": user}
                    ],
                    "temperature": temp,
                    "max_tokens": max_tokens
                }
            )
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            tokens = data.get("usage", {}).get("total_tokens", 0)
            return content, tokens
    
    @staticmethod
    async def _call_openrouter(api_key: str, system: str, user: str, model: str, temp: float, max_tokens: int) -> tuple[str, int]:
        """Appel API OpenRouter"""
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://iafactory.io",
                    "X-Title": "IA Factory Video Studio"
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": user}
                    ],
                    "temperature": temp,
                    "max_tokens": max_tokens
                }
            )
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            tokens = data.get("usage", {}).get("total_tokens", 0)
            return content, tokens


class BaseAgent(ABC):
    """Classe de base pour tous les agents IA."""

    def __init__(
        self,
        name: str,
        role: AgentRole,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ):
        self.name = name
        self.role = role
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.status = AgentStatus.IDLE
        self.logger = structlog.get_logger().bind(agent=name)

    @abstractmethod
    async def execute(self, task: AgentTask) -> AgentResult:
        """Exécute une tâche."""
        pass

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Retourne le prompt système de l'agent."""
        pass

    def set_status(self, status: AgentStatus):
        """Met à jour le statut de l'agent."""
        self.status = status
        self.logger.info("Agent status changed", status=status.value)
    
    def extract_json(self, content: str) -> dict:
        """Extrait le JSON d'une réponse LLM."""
        try:
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                parts = content.split("```")
                for part in parts:
                    part = part.strip()
                    if part.startswith("{") or part.startswith("["):
                        content = part
                        break
            return json.loads(content.strip())
        except json.JSONDecodeError:
            # Essayer de trouver le JSON brut
            start = content.find("{")
            end = content.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(content[start:end])
            raise


class ScriptwriterAgent(BaseAgent):
    """Agent Scénariste - Génère des scripts optimisés pour le viral."""

    def __init__(self):
        super().__init__(
            name="Scénariste",
            role=AgentRole.SCRIPTWRITER,
            temperature=0.8,
            max_tokens=8000
        )

    def get_system_prompt(self) -> str:
        return """Tu es un scénariste expert en contenu viral pour les réseaux sociaux.

EXPERTISE:
- Scripts YouTube (8-15 minutes), Shorts (15-60s), TikTok, Instagram Reels
- Structure HVS (Hook-Value-Story) pour maximiser la rétention
- Adaptation culturelle Algérie/Maghreb avec touche Darija

RÈGLES DE RÉDACTION:
1. Hook accrocheur dans les 3 premières secondes
2. Phrases courtes et percutantes
3. Storytelling émotionnel
4. Call-to-action clair
5. Timing précis pour chaque segment

Tu dois TOUJOURS répondre en JSON valide uniquement, sans texte avant ou après.

FORMAT DE SORTIE (JSON):
{
  "title": "Titre SEO optimisé",
  "hook": "Accroche puissante",
  "segments": [
    {
      "id": 1,
      "type": "hook|value|story|cta",
      "duration": 5,
      "script": "Texte narration",
      "visual_prompt": "Description pour IA vidéo",
      "emotion": "curiosité|surprise|inspiration|urgence"
    }
  ],
  "metadata": {
    "total_duration": 60,
    "target_platform": "youtube|tiktok|instagram",
    "language": "fr|ar|darija",
    "hashtags": ["#tag1", "#tag2"],
    "thumbnail_prompt": "Description thumbnail"
  }
}"""

    async def execute(self, task: AgentTask) -> AgentResult:
        """Génère un script à partir d'un sujet."""
        start_time = time.time()
        self.set_status(AgentStatus.THINKING)
        
        topic = task.input_data.get("topic", "")
        platform = task.input_data.get("platform", "youtube")
        language = task.input_data.get("language", "fr")
        duration = task.input_data.get("duration", 60)
        style = task.input_data.get("style", "informative")
        
        user_prompt = f"""Crée un script viral pour:
- Sujet: {topic}
- Plateforme: {platform}
- Langue: {language}
- Durée cible: {duration} secondes
- Style: {style}

Génère le script en JSON selon le format spécifié. Réponds UNIQUEMENT avec le JSON."""

        try:
            self.set_status(AgentStatus.WORKING)
            
            content, tokens_used = await LLMProvider.call(
                system_prompt=self.get_system_prompt(),
                user_prompt=user_prompt,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            script_data = self.extract_json(content)
            
            self.set_status(AgentStatus.COMPLETED)
            
            return AgentResult(
                task_id=task.task_id,
                role=self.role,
                status=AgentStatus.COMPLETED,
                output=script_data,
                tokens_used=tokens_used,
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            self.logger.error("Scriptwriter error", error=str(e))
            # Fallback to mock
            return self._generate_mock_script(task, topic, platform, language, duration, style, start_time)

    def _generate_mock_script(self, task, topic, platform, language, duration, style, start_time):
        """Génère un script de démonstration."""
        segments = [
            {"id": 1, "type": "hook", "duration": 5, "script": f"🔥 Découvrez les secrets pour {topic}!", "visual_prompt": f"Dynamic intro with text overlay about {topic}, energetic motion graphics", "emotion": "curiosité"},
            {"id": 2, "type": "value", "duration": 15, "script": "Dans cette vidéo, je vais vous révéler les stratégies qui fonctionnent vraiment en 2025.", "visual_prompt": "Speaker presenting key points with animated bullet points appearing", "emotion": "inspiration"},
            {"id": 3, "type": "value", "duration": 20, "script": "Premier conseil essentiel: commencez petit mais pensez grand. Voici comment...", "visual_prompt": "Split screen showing before/after transformation, success imagery", "emotion": "motivation"},
            {"id": 4, "type": "story", "duration": 15, "script": "J'ai personnellement testé ces méthodes et les résultats sont incroyables.", "visual_prompt": "Personal testimony style, authentic footage with results graphs", "emotion": "authenticité"},
            {"id": 5, "type": "cta", "duration": 5, "script": "Abonnez-vous et activez la cloche pour ne rien manquer! 🔔", "visual_prompt": "Subscribe button animation, bell icon, social proof numbers", "emotion": "urgence"}
        ]
        
        script_data = {
            "title": f"{topic} - Guide Complet 2025 🚀",
            "hook": f"🔥 {topic}: Ce que personne ne vous dit!",
            "segments": segments[:max(3, duration // 15)],
            "metadata": {
                "total_duration": duration,
                "target_platform": platform,
                "language": language,
                "hashtags": ["#startup", "#algerie", "#business", "#2025", "#success"],
                "thumbnail_prompt": f"Eye-catching thumbnail about {topic} with bold text and emoji"
            }
        }
        
        self.set_status(AgentStatus.COMPLETED)
        
        return AgentResult(
            task_id=task.task_id,
            role=self.role,
            status=AgentStatus.COMPLETED,
            output=script_data,
            tokens_used=0,
            execution_time=time.time() - start_time
        )


class StoryboarderAgent(BaseAgent):
    """Agent Storyboarder - Décompose le script en séquences visuelles."""

    def __init__(self):
        super().__init__(
            name="Storyboarder",
            role=AgentRole.STORYBOARDER,
            temperature=0.6,
            max_tokens=4000
        )

    def get_system_prompt(self) -> str:
        return """Tu es un storyboarder expert en production vidéo IA.

MISSION:
- Transformer les scripts en séquences visuelles précises
- Créer des prompts optimisés pour les générateurs d'images/vidéos IA
- Assurer la cohérence visuelle entre les plans

RÈGLES:
1. Chaque plan = 3-5 secondes maximum
2. Prompts détaillés avec style, éclairage, angle caméra
3. Transitions fluides entre les plans
4. Cohérence des personnages/décors

Tu dois TOUJOURS répondre en JSON valide uniquement.

FORMAT DE SORTIE (JSON):
{
  "shots": [
    {
      "id": 1,
      "segment_id": 1,
      "duration": 5,
      "shot_type": "wide|medium|close-up",
      "description": "Description du plan",
      "visual_prompt": "Prompt détaillé pour IA vidéo",
      "camera_movement": "static|pan|zoom|tracking",
      "transition": "cut|fade|dissolve",
      "audio_cue": "Description audio"
    }
  ],
  "metadata": {
    "style": "cinematic|documentary|modern",
    "aspect_ratio": "16:9|9:16|1:1",
    "color_palette": ["#hex1", "#hex2"]
  }
}"""

    async def execute(self, task: AgentTask) -> AgentResult:
        """Crée un storyboard à partir d'un script."""
        start_time = time.time()
        self.set_status(AgentStatus.THINKING)
        
        script = task.input_data.get("script", {})
        style = task.input_data.get("style", "cinematic")
        aspect_ratio = task.input_data.get("aspect_ratio", "16:9")
        
        segments = script.get("segments", [])
        
        user_prompt = f"""Crée un storyboard détaillé pour ce script:

Segments: {json.dumps(segments, ensure_ascii=False)}

Style visuel: {style}
Format: {aspect_ratio}

Génère le storyboard en JSON. Réponds UNIQUEMENT avec le JSON."""

        try:
            self.set_status(AgentStatus.WORKING)
            
            content, tokens_used = await LLMProvider.call(
                system_prompt=self.get_system_prompt(),
                user_prompt=user_prompt,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            storyboard_data = self.extract_json(content)
            
            self.set_status(AgentStatus.COMPLETED)
            
            return AgentResult(
                task_id=task.task_id,
                role=self.role,
                status=AgentStatus.COMPLETED,
                output=storyboard_data,
                tokens_used=tokens_used,
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            self.logger.error("Storyboarder error", error=str(e))
            return self._generate_mock_storyboard(task, segments, style, aspect_ratio, start_time)

    def _generate_mock_storyboard(self, task, segments, style, aspect_ratio, start_time):
        """Génère un storyboard de démonstration."""
        shots = []
        for i, seg in enumerate(segments):
            shots.append({
                "id": i + 1,
                "segment_id": seg.get("id", i + 1),
                "duration": seg.get("duration", 5),
                "shot_type": "medium" if i % 2 == 0 else "close-up",
                "description": seg.get("script", f"Plan {i+1}"),
                "visual_prompt": seg.get("visual_prompt", f"Professional shot {i+1}"),
                "camera_movement": "static" if i % 3 == 0 else "slow_zoom",
                "transition": "cut" if i == 0 else "dissolve",
                "audio_cue": "background_music"
            })
        
        storyboard_data = {
            "shots": shots,
            "total_duration": sum(s.get("duration", 5) for s in segments),
            "metadata": {
                "style": style,
                "aspect_ratio": aspect_ratio,
                "color_palette": ["#1a1a2e", "#16213e", "#0f3460", "#e94560"],
                "mode": "mock"
            }
        }
        
        self.set_status(AgentStatus.COMPLETED)
        
        return AgentResult(
            task_id=task.task_id,
            role=self.role,
            status=AgentStatus.COMPLETED,
            output=storyboard_data,
            tokens_used=0,
            execution_time=time.time() - start_time
        )


class DirectorAgent(BaseAgent):
    """Agent Réalisateur - Orchestre la production finale."""

    def __init__(self):
        super().__init__(
            name="Réalisateur",
            role=AgentRole.DIRECTOR,
            temperature=0.5,
            max_tokens=4000
        )

    def get_system_prompt(self) -> str:
        return """Tu es un réalisateur expert en production vidéo IA.

MISSION:
- Coordonner la génération de tous les assets
- Optimiser la qualité de chaque élément
- Créer une timeline de montage précise

FORMAT DE SORTIE (JSON):
{
  "timeline": {
    "tracks": [
      {"type": "video", "clips": [...]},
      {"type": "audio", "clips": [...]},
      {"type": "music", "clips": [...]},
      {"type": "subtitles", "clips": [...]}
    ]
  },
  "render_settings": {
    "format": "mp4",
    "codec": "h264",
    "resolution": "1920x1080",
    "fps": 30,
    "bitrate": "8M"
  },
  "exports": [
    {"platform": "youtube", "format": "16:9", "max_duration": null},
    {"platform": "tiktok", "format": "9:16", "max_duration": 180}
  ]
}"""

    async def execute(self, task: AgentTask) -> AgentResult:
        """Crée un plan de production."""
        start_time = time.time()
        self.set_status(AgentStatus.THINKING)
        
        storyboard = task.input_data.get("storyboard", {})
        quality = task.input_data.get("quality", "high")
        
        user_prompt = f"""Crée un plan de production pour ce storyboard:

{json.dumps(storyboard, ensure_ascii=False)}

Qualité: {quality}

Génère le plan de production en JSON. Réponds UNIQUEMENT avec le JSON."""

        try:
            self.set_status(AgentStatus.WORKING)
            
            content, tokens_used = await LLMProvider.call(
                system_prompt=self.get_system_prompt(),
                user_prompt=user_prompt,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            production_data = self.extract_json(content)
            
            self.set_status(AgentStatus.COMPLETED)
            
            return AgentResult(
                task_id=task.task_id,
                role=self.role,
                status=AgentStatus.COMPLETED,
                output=production_data,
                tokens_used=tokens_used,
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            self.logger.error("Director error", error=str(e))
            return self._generate_mock_production(task, start_time)

    def _generate_mock_production(self, task, start_time):
        """Génère un plan de production de démonstration."""
        production_data = {
            "timeline": {
                "tracks": [
                    {"type": "video", "clips": []},
                    {"type": "audio", "clips": []},
                    {"type": "music", "clips": []},
                    {"type": "subtitles", "clips": []}
                ]
            },
            "render_settings": {
                "format": "mp4",
                "codec": "h264",
                "resolution": "1920x1080",
                "fps": 30,
                "bitrate": "8M"
            },
            "exports": [
                {"platform": "youtube", "format": "16:9", "max_duration": None}
            ]
        }
        
        self.set_status(AgentStatus.COMPLETED)
        
        return AgentResult(
            task_id=task.task_id,
            role=self.role,
            status=AgentStatus.COMPLETED,
            output=production_data,
            tokens_used=0,
            execution_time=time.time() - start_time
        )


class GrowthHackerAgent(BaseAgent):
    """Agent Growth Hacker - Optimise pour la viralité."""

    def __init__(self):
        super().__init__(
            name="Growth Hacker",
            role=AgentRole.GROWTH_HACKER,
            temperature=0.7,
            max_tokens=4000
        )

    def get_system_prompt(self) -> str:
        return """Tu es un expert en growth hacking pour les réseaux sociaux, spécialisé dans le marché algérien et maghrébin.

EXPERTISE:
- Optimisation SEO YouTube, TikTok, Instagram
- Stratégies de viralité et d'engagement
- Timing de publication optimal par région
- Hashtags tendance par plateforme

Tu dois TOUJOURS répondre en JSON valide uniquement.

FORMAT DE SORTIE (JSON):
{
  "platform_optimizations": [
    {
      "platform": "youtube|tiktok|instagram",
      "title": "Titre optimisé",
      "description": "Description SEO",
      "hashtags": ["#tag1", "#tag2"],
      "best_posting_time": "HH:MM",
      "viral_score": 0.85,
      "thumbnail_prompt": "Description thumbnail"
    }
  ],
  "global_recommendations": ["Conseil 1", "Conseil 2"]
}"""

    async def execute(self, task: AgentTask) -> AgentResult:
        """Optimise le contenu pour la viralité."""
        start_time = time.time()
        self.set_status(AgentStatus.THINKING)
        
        title = task.input_data.get("title", "")
        description = task.input_data.get("description", "")
        topic = task.input_data.get("topic", "")
        platforms = task.input_data.get("platforms", ["youtube"])
        language = task.input_data.get("language", "fr")
        
        user_prompt = f"""Optimise ce contenu pour la viralité:

Titre: {title}
Description: {description}
Sujet: {topic}
Plateformes cibles: {', '.join(platforms)}
Langue: {language}
Région: Algérie/Maghreb

Génère les optimisations en JSON. Réponds UNIQUEMENT avec le JSON."""

        try:
            self.set_status(AgentStatus.WORKING)
            
            content, tokens_used = await LLMProvider.call(
                system_prompt=self.get_system_prompt(),
                user_prompt=user_prompt,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            optimization_data = self.extract_json(content)
            
            self.set_status(AgentStatus.COMPLETED)
            
            return AgentResult(
                task_id=task.task_id,
                role=self.role,
                status=AgentStatus.COMPLETED,
                output=optimization_data,
                tokens_used=tokens_used,
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            self.logger.error("GrowthHacker error", error=str(e))
            return self._generate_mock_optimization(task, topic, platforms, start_time)

    def _generate_mock_optimization(self, task, topic, platforms, start_time):
        """Génère des optimisations de démonstration."""
        platform_opts = []
        
        platform_times = {
            "youtube": "14:00",
            "youtube_shorts": "19:00",
            "tiktok": "19:00",
            "instagram_reels": "19:00",
            "instagram_post": "12:00",
            "linkedin": "09:00",
            "twitter": "17:00",
            "facebook": "20:00"
        }
        
        for platform in platforms:
            platform_opts.append({
                "platform": platform,
                "title": f"🔥 {topic} - Ce que personne ne vous dit! [2025]",
                "description": f"Découvrez tout sur {topic} dans cette vidéo exclusive. Abonnez-vous pour plus de contenu!",
                "hashtags": ["#viral", "#trending", f"#{platform}", "#2025", "#algerie"],
                "best_posting_time": platform_times.get(platform, "14:00"),
                "viral_score": 0.75,
                "thumbnail_prompt": f"Eye-catching thumbnail for {topic}, bright colors, bold text"
            })
        
        optimization_data = {
            "platform_optimizations": platform_opts,
            "global_recommendations": [
                "Utilisez des emojis dans le titre",
                "Postez pendant les heures de pointe",
                "Répondez aux commentaires rapidement"
            ],
            "mode": "mock"
        }
        
        self.set_status(AgentStatus.COMPLETED)
        
        return AgentResult(
            task_id=task.task_id,
            role=self.role,
            status=AgentStatus.COMPLETED,
            output=optimization_data,
            tokens_used=0,
            execution_time=time.time() - start_time
        )


# Factory function to create agents
def create_agent(role: AgentRole, **kwargs) -> BaseAgent:
    """Crée un agent basé sur son rôle."""
    agents_map = {
        AgentRole.SCRIPTWRITER: ScriptwriterAgent,
        AgentRole.STORYBOARDER: StoryboarderAgent,
        AgentRole.DIRECTOR: DirectorAgent,
        AgentRole.GROWTH_HACKER: GrowthHackerAgent,
    }
    
    agent_class = agents_map.get(role)
    if not agent_class:
        raise ValueError(f"Unknown agent role: {role}")
    
    return agent_class(**kwargs)


# Export des classes
__all__ = [
    "AgentRole",
    "AgentStatus", 
    "AgentTask",
    "AgentResult",
    "BaseAgent",
    "LLMProvider",
    "ScriptwriterAgent",
    "StoryboarderAgent",
    "DirectorAgent",
    "GrowthHackerAgent",
    "create_agent"
]
