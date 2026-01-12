"""
Avatar Agent - Génération de vidéos avec avatars parlants
"""
from typing import List, Dict, Any, Optional
from app.agents.base import BaseAgent, AgentTask, AgentResult
from app.core.config import settings


class AvatarAgent(BaseAgent):
    """
    Agent de génération d'avatars parlants.

    Providers supportés:
    - HeyGen
    - D-ID
    - Synthesia
    - Colossyan
    - Tavus
    - SadTalker (open source)

    Responsabilités:
    - Génère des vidéos avec avatars parlants
    - Synchronise les lèvres avec l'audio
    - Clone des voix et visages
    - Gère les expressions et émotions
    """

    @property
    def agent_type(self) -> str:
        return "avatar"

    @property
    def capabilities(self) -> List[str]:
        return [
            "generate_avatar_video",
            "lip_sync",
            "clone_face",
            "list_avatars",
            "create_custom_avatar",
            "animate_portrait"
        ]

    # Coûts approximatifs par minute de vidéo
    PROVIDER_COSTS = {
        "heygen": 100,      # ~$1.00 par minute
        "did": 80,          # ~$0.80 par minute
        "synthesia": 150,   # ~$1.50 par minute
        "colossyan": 120,   # ~$1.20 par minute
        "tavus": 200,       # ~$2.00 par minute (personnalisé)
        "sadtalker": 5,     # ~$0.05 (self-hosted)
    }

    # Avatars prédéfinis par provider
    DEFAULT_AVATARS = {
        "heygen": [
            {"id": "josh", "name": "Josh", "gender": "male", "style": "professional"},
            {"id": "sarah", "name": "Sarah", "gender": "female", "style": "professional"},
            {"id": "marcus", "name": "Marcus", "gender": "male", "style": "casual"},
        ],
        "did": [
            {"id": "amy", "name": "Amy", "gender": "female", "style": "friendly"},
            {"id": "jack", "name": "Jack", "gender": "male", "style": "professional"},
        ],
        "synthesia": [
            {"id": "anna", "name": "Anna", "gender": "female", "style": "corporate"},
            {"id": "james", "name": "James", "gender": "male", "style": "corporate"},
        ]
    }

    def __init__(self, default_provider: str = None):
        super().__init__()
        self.default_provider = default_provider or settings.DEFAULT_AVATAR_PROVIDER

    async def _execute_task(self, task: AgentTask) -> AgentResult:
        """Exécute une tâche de génération d'avatar"""

        handlers = {
            "generate_avatar_video": self._generate_avatar_video,
            "lip_sync": self._lip_sync,
            "clone_face": self._clone_face,
            "list_avatars": self._list_avatars,
            "create_custom_avatar": self._create_custom_avatar,
            "animate_portrait": self._animate_portrait,
        }

        handler = handlers.get(task.task_type)
        return await handler(task)

    async def _generate_avatar_video(self, task: AgentTask) -> AgentResult:
        """
        Génère une vidéo complète avec avatar parlant.

        Input:
        - script: Texte à dire
        - avatar_id: ID de l'avatar à utiliser
        - voice_id: ID de la voix (optionnel, utilise la voix de l'avatar par défaut)
        - provider: Provider à utiliser
        - background: URL ou couleur de fond
        """
        script = task.input_data.get("script", "")
        avatar_id = task.input_data.get("avatar_id")
        voice_id = task.input_data.get("voice_id")
        provider = task.input_data.get("provider", self.default_provider)
        background = task.input_data.get("background", "#ffffff")
        language = task.input_data.get("language", "fr")

        if not script:
            return AgentResult(
                task_id=task.task_id,
                success=False,
                error_message="Script is required"
            )

        # Estimation de la durée (environ 150 mots par minute)
        word_count = len(script.split())
        estimated_duration = max(10, (word_count / 150) * 60)  # en secondes

        # TODO: Appel réel à l'API du provider
        video_result = {
            "video_id": f"avatar_{task.task_id[:8]}",
            "provider": provider,
            "avatar_id": avatar_id,
            "voice_id": voice_id,
            "script": script[:100] + "..." if len(script) > 100 else script,
            "duration": estimated_duration,
            "language": language,
            "background": background,
            "resolution": "1080p",
            "url": f"https://placeholder.com/avatar_{task.task_id[:8]}.mp4",
            "local_path": None,
            "status": "completed"
        }

        # Calcul du coût basé sur la durée
        cost_per_minute = self.PROVIDER_COSTS.get(provider, 100)
        cost = int(cost_per_minute * (estimated_duration / 60))

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"video": video_result},
            cost_cents=cost,
            metadata={"estimated_duration": estimated_duration}
        )

    async def _lip_sync(self, task: AgentTask) -> AgentResult:
        """
        Synchronise les lèvres d'une vidéo existante avec un nouvel audio.
        Idéal pour: Wav2Lip, SadTalker
        """
        video_path = task.input_data.get("video_path")
        audio_path = task.input_data.get("audio_path")
        provider = task.input_data.get("provider", "sadtalker")

        if not video_path or not audio_path:
            return AgentResult(
                task_id=task.task_id,
                success=False,
                error_message="Both video_path and audio_path are required"
            )

        # TODO: Appel API ou processing local
        result = {
            "lip_synced_id": f"lipsync_{task.task_id[:8]}",
            "original_video": video_path,
            "audio": audio_path,
            "provider": provider,
            "local_path": None
        }

        cost = 10 if provider == "sadtalker" else 50

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"lip_synced_video": result},
            cost_cents=cost
        )

    async def _clone_face(self, task: AgentTask) -> AgentResult:
        """
        Clone un visage à partir d'images/vidéos pour créer un avatar personnalisé.
        """
        face_images = task.input_data.get("face_images", [])  # Liste d'URLs ou paths
        provider = task.input_data.get("provider", self.default_provider)
        avatar_name = task.input_data.get("name", "Custom Avatar")

        if len(face_images) < 1:
            return AgentResult(
                task_id=task.task_id,
                success=False,
                error_message="At least 1 face image is required"
            )

        # TODO: Appel API pour clonage
        cloned_avatar = {
            "avatar_id": f"custom_{task.task_id[:8]}",
            "name": avatar_name,
            "provider": provider,
            "source_images": len(face_images),
            "status": "created"
        }

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"avatar": cloned_avatar},
            cost_cents=500  # Création d'avatar personnalisé coûte plus
        )

    async def _list_avatars(self, task: AgentTask) -> AgentResult:
        """Liste les avatars disponibles pour un provider"""
        provider = task.input_data.get("provider", self.default_provider)
        include_custom = task.input_data.get("include_custom", True)

        avatars = self.DEFAULT_AVATARS.get(provider, [])

        # TODO: Récupérer les avatars personnalisés depuis la DB
        if include_custom:
            # Ajouter les avatars personnalisés
            pass

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={
                "provider": provider,
                "avatars": avatars,
                "total": len(avatars)
            }
        )

    async def _create_custom_avatar(self, task: AgentTask) -> AgentResult:
        """
        Crée un avatar personnalisé complet (visage + voix).
        """
        face_images = task.input_data.get("face_images", [])
        voice_samples = task.input_data.get("voice_samples", [])
        provider = task.input_data.get("provider", self.default_provider)
        avatar_name = task.input_data.get("name", "Custom Avatar")

        # Créer l'avatar avec visage
        avatar_result = await self._clone_face(AgentTask(
            task_type="clone_face",
            input_data={
                "face_images": face_images,
                "provider": provider,
                "name": avatar_name
            }
        ))

        if not avatar_result.success:
            return avatar_result

        avatar_data = avatar_result.output_data.get("avatar", {})

        # TODO: Cloner la voix si des samples sont fournis
        if voice_samples:
            avatar_data["has_custom_voice"] = True
            avatar_data["voice_samples"] = len(voice_samples)

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"avatar": avatar_data},
            cost_cents=avatar_result.cost_cents + (200 if voice_samples else 0)
        )

    async def _animate_portrait(self, task: AgentTask) -> AgentResult:
        """
        Anime une photo portrait (style photos qui parlent).
        Plus léger que la génération d'avatar complète.
        """
        portrait_path = task.input_data.get("portrait_path")
        audio_path = task.input_data.get("audio_path")
        animation_style = task.input_data.get("style", "natural")
        provider = task.input_data.get("provider", "sadtalker")

        if not portrait_path:
            return AgentResult(
                task_id=task.task_id,
                success=False,
                error_message="portrait_path is required"
            )

        # TODO: Utiliser SadTalker ou équivalent
        result = {
            "animated_portrait_id": f"portrait_{task.task_id[:8]}",
            "source_portrait": portrait_path,
            "audio": audio_path,
            "style": animation_style,
            "provider": provider,
            "local_path": None
        }

        cost = self.PROVIDER_COSTS.get(provider, 10)

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"animated_portrait": result},
            cost_cents=cost
        )

    def get_recommended_provider(
        self,
        use_case: str,
        budget: str = "medium"
    ) -> Dict[str, Any]:
        """
        Recommande un provider selon le cas d'usage et le budget.

        use_cases: corporate, casual, custom, budget
        budget: low, medium, high
        """
        recommendations = {
            "corporate": {
                "low": "did",
                "medium": "synthesia",
                "high": "synthesia"
            },
            "casual": {
                "low": "sadtalker",
                "medium": "heygen",
                "high": "heygen"
            },
            "custom": {
                "low": "sadtalker",
                "medium": "heygen",
                "high": "tavus"
            },
            "budget": {
                "low": "sadtalker",
                "medium": "did",
                "high": "heygen"
            }
        }

        provider = recommendations.get(use_case, {}).get(budget, "heygen")

        return {
            "provider": provider,
            "cost_per_minute": self.PROVIDER_COSTS.get(provider, 100),
            "avatars": self.DEFAULT_AVATARS.get(provider, [])
        }
