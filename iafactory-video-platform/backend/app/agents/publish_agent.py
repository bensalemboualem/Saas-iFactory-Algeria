"""
Publish Agent - Publication multi-plateforme
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from app.agents.base import BaseAgent, AgentTask, AgentResult
from app.core.config import settings


class PublishAgent(BaseAgent):
    """
    Agent de publication multi-plateforme.

    Plateformes supportées:
    - YouTube
    - TikTok
    - Instagram (Reels, Feed, Story)
    - Facebook
    - LinkedIn
    - Twitter/X
    - Pinterest
    - Snapchat

    Responsabilités:
    - Upload des vidéos
    - Optimise les métadonnées par plateforme
    - Planifie les publications
    - Gère les authentifications OAuth
    - Récupère les analytics
    """

    @property
    def agent_type(self) -> str:
        return "publish"

    @property
    def capabilities(self) -> List[str]:
        return [
            "publish_video",
            "schedule_publish",
            "optimize_metadata",
            "generate_thumbnail",
            "get_analytics",
            "list_connected_accounts",
            "batch_publish"
        ]

    # Limites par plateforme
    PLATFORM_LIMITS = {
        "youtube": {
            "max_title": 100,
            "max_description": 5000,
            "max_tags": 500,  # caractères totaux
            "max_duration": 43200,  # 12 heures
            "formats": ["mp4", "mov", "avi", "wmv", "flv", "webm"],
            "max_size_gb": 256
        },
        "tiktok": {
            "max_title": 150,
            "max_description": 2200,
            "max_duration": 600,  # 10 minutes
            "formats": ["mp4", "webm"],
            "max_size_gb": 4
        },
        "instagram_reels": {
            "max_title": 0,  # Pas de titre, juste caption
            "max_description": 2200,
            "max_duration": 90,
            "formats": ["mp4"],
            "max_size_gb": 1
        },
        "instagram_feed": {
            "max_description": 2200,
            "max_duration": 60,
            "formats": ["mp4"],
            "max_size_gb": 0.25
        },
        "linkedin": {
            "max_title": 200,
            "max_description": 3000,
            "max_duration": 600,
            "formats": ["mp4"],
            "max_size_gb": 5
        },
        "twitter": {
            "max_description": 280,
            "max_duration": 140,
            "formats": ["mp4"],
            "max_size_gb": 0.512
        },
        "facebook": {
            "max_title": 255,
            "max_description": 63206,
            "max_duration": 14400,  # 4 heures
            "formats": ["mp4", "mov"],
            "max_size_gb": 10
        }
    }

    def __init__(self):
        super().__init__()
        self._connected_accounts = {}

    async def _execute_task(self, task: AgentTask) -> AgentResult:
        """Exécute une tâche de publication"""

        handlers = {
            "publish_video": self._publish_video,
            "schedule_publish": self._schedule_publish,
            "optimize_metadata": self._optimize_metadata,
            "generate_thumbnail": self._generate_thumbnail,
            "get_analytics": self._get_analytics,
            "list_connected_accounts": self._list_connected_accounts,
            "batch_publish": self._batch_publish,
        }

        handler = handlers.get(task.task_type)
        return await handler(task)

    async def _publish_video(self, task: AgentTask) -> AgentResult:
        """
        Publie une vidéo sur une plateforme.
        """
        video_path = task.input_data.get("video_path")
        platform = task.input_data.get("platform", "youtube")
        title = task.input_data.get("title", "")
        description = task.input_data.get("description", "")
        tags = task.input_data.get("tags", [])
        thumbnail_path = task.input_data.get("thumbnail_path")
        privacy = task.input_data.get("privacy", "public")
        platform_settings = task.input_data.get("platform_settings", {})

        if not video_path:
            return AgentResult(
                task_id=task.task_id,
                success=False,
                error_message="video_path is required"
            )

        # Validation des limites de la plateforme
        limits = self.PLATFORM_LIMITS.get(platform, {})
        validation_errors = self._validate_content(
            platform, title, description, tags, limits
        )

        if validation_errors:
            return AgentResult(
                task_id=task.task_id,
                success=False,
                error_message=f"Validation errors: {', '.join(validation_errors)}"
            )

        # TODO: Appel réel à l'API de la plateforme
        publish_result = {
            "publish_id": f"pub_{task.task_id[:8]}",
            "platform": platform,
            "video_path": video_path,
            "title": title[:limits.get("max_title", 100)] if limits.get("max_title") else None,
            "description": description[:limits.get("max_description", 2000)],
            "tags": tags,
            "privacy": privacy,
            "status": "published",
            "platform_post_id": f"platform_{task.task_id[:8]}",
            "platform_url": f"https://{platform}.com/video/{task.task_id[:8]}",
            "published_at": datetime.utcnow().isoformat()
        }

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"publish_result": publish_result}
        )

    async def _schedule_publish(self, task: AgentTask) -> AgentResult:
        """
        Planifie une publication pour plus tard.
        """
        video_path = task.input_data.get("video_path")
        platform = task.input_data.get("platform")
        scheduled_time = task.input_data.get("scheduled_time")  # ISO format
        metadata = task.input_data.get("metadata", {})

        if not scheduled_time:
            return AgentResult(
                task_id=task.task_id,
                success=False,
                error_message="scheduled_time is required"
            )

        try:
            scheduled_dt = datetime.fromisoformat(scheduled_time.replace("Z", "+00:00"))
        except ValueError:
            return AgentResult(
                task_id=task.task_id,
                success=False,
                error_message="Invalid scheduled_time format"
            )

        # Vérifier que c'est dans le futur
        if scheduled_dt <= datetime.utcnow():
            return AgentResult(
                task_id=task.task_id,
                success=False,
                error_message="scheduled_time must be in the future"
            )

        schedule_result = {
            "schedule_id": f"sched_{task.task_id[:8]}",
            "platform": platform,
            "video_path": video_path,
            "scheduled_time": scheduled_time,
            "metadata": metadata,
            "status": "scheduled"
        }

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"schedule_result": schedule_result}
        )

    async def _optimize_metadata(self, task: AgentTask) -> AgentResult:
        """
        Optimise les métadonnées pour une plateforme spécifique.
        Utilise l'IA pour générer titres, descriptions, tags optimisés.
        """
        platform = task.input_data.get("platform", "youtube")
        content_summary = task.input_data.get("content_summary", "")
        target_audience = task.input_data.get("target_audience", "general")
        language = task.input_data.get("language", "fr")
        existing_metadata = task.input_data.get("existing_metadata", {})

        limits = self.PLATFORM_LIMITS.get(platform, {})

        # TODO: Utiliser LLM pour optimiser
        # Pour le moment, génération basique
        optimized = {
            "title": self._generate_platform_title(
                content_summary, platform, limits.get("max_title", 100)
            ),
            "description": self._generate_platform_description(
                content_summary, platform, limits.get("max_description", 2000)
            ),
            "tags": self._generate_platform_tags(
                content_summary, platform, language
            ),
            "hashtags": self._generate_hashtags(content_summary, platform),
            "platform": platform,
            "optimized_for": {
                "seo": True,
                "engagement": True,
                "discoverability": True
            }
        }

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"optimized_metadata": optimized}
        )

    async def _generate_thumbnail(self, task: AgentTask) -> AgentResult:
        """
        Génère une miniature optimisée pour une plateforme.
        """
        video_path = task.input_data.get("video_path")
        platform = task.input_data.get("platform", "youtube")
        title_text = task.input_data.get("title_text")
        style = task.input_data.get("style", "modern")

        # Dimensions par plateforme
        thumbnail_sizes = {
            "youtube": (1280, 720),
            "tiktok": (1080, 1920),
            "instagram": (1080, 1080),
            "linkedin": (1200, 627),
            "twitter": (1200, 675),
            "facebook": (1200, 630)
        }

        size = thumbnail_sizes.get(platform, (1280, 720))

        # TODO: Extraire frame + ajouter texte/design avec Pillow ou IA
        thumbnail_result = {
            "thumbnail_id": f"thumb_{task.task_id[:8]}",
            "platform": platform,
            "size": size,
            "style": style,
            "has_text": bool(title_text),
            "path": f"thumbnails/thumb_{task.task_id[:8]}.jpg"
        }

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"thumbnail": thumbnail_result}
        )

    async def _get_analytics(self, task: AgentTask) -> AgentResult:
        """
        Récupère les analytics d'une publication.
        """
        platform = task.input_data.get("platform")
        platform_post_id = task.input_data.get("platform_post_id")
        metrics = task.input_data.get("metrics", ["views", "likes", "comments", "shares"])

        if not platform_post_id:
            return AgentResult(
                task_id=task.task_id,
                success=False,
                error_message="platform_post_id is required"
            )

        # TODO: Appel réel à l'API de la plateforme
        analytics = {
            "platform": platform,
            "post_id": platform_post_id,
            "metrics": {
                "views": 0,
                "likes": 0,
                "comments": 0,
                "shares": 0,
                "watch_time_hours": 0,
                "average_view_duration": 0,
                "engagement_rate": 0
            },
            "demographics": {
                "top_countries": [],
                "age_groups": [],
                "gender_split": {}
            },
            "updated_at": datetime.utcnow().isoformat()
        }

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"analytics": analytics}
        )

    async def _list_connected_accounts(self, task: AgentTask) -> AgentResult:
        """Liste les comptes connectés pour la publication"""

        # TODO: Récupérer depuis la DB
        accounts = [
            {
                "platform": "youtube",
                "account_name": "My Channel",
                "connected": True,
                "expires_at": None
            },
            {
                "platform": "tiktok",
                "account_name": "@myaccount",
                "connected": True,
                "expires_at": None
            }
        ]

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"accounts": accounts}
        )

    async def _batch_publish(self, task: AgentTask) -> AgentResult:
        """
        Publie sur plusieurs plateformes en une fois.
        """
        video_path = task.input_data.get("video_path")
        platforms = task.input_data.get("platforms", [])
        base_metadata = task.input_data.get("metadata", {})
        auto_optimize = task.input_data.get("auto_optimize", True)

        if not platforms:
            return AgentResult(
                task_id=task.task_id,
                success=False,
                error_message="At least one platform is required"
            )

        results = []
        for platform in platforms:
            # Optimiser les métadonnées si demandé
            if auto_optimize:
                optimize_result = await self._optimize_metadata(AgentTask(
                    task_type="optimize_metadata",
                    input_data={
                        "platform": platform,
                        "content_summary": base_metadata.get("description", ""),
                        "existing_metadata": base_metadata
                    }
                ))
                metadata = optimize_result.output_data.get("optimized_metadata", base_metadata)
            else:
                metadata = base_metadata

            # Publier
            publish_result = await self._publish_video(AgentTask(
                task_type="publish_video",
                input_data={
                    "video_path": video_path,
                    "platform": platform,
                    **metadata
                }
            ))

            results.append({
                "platform": platform,
                "success": publish_result.success,
                "result": publish_result.output_data if publish_result.success else None,
                "error": publish_result.error_message
            })

        successful = sum(1 for r in results if r["success"])

        return AgentResult(
            task_id=task.task_id,
            success=successful > 0,
            output_data={
                "batch_results": results,
                "total_platforms": len(platforms),
                "successful": successful,
                "failed": len(platforms) - successful
            }
        )

    def _validate_content(
        self,
        platform: str,
        title: str,
        description: str,
        tags: List[str],
        limits: Dict
    ) -> List[str]:
        """Valide le contenu selon les limites de la plateforme"""
        errors = []

        max_title = limits.get("max_title", 0)
        if max_title and len(title) > max_title:
            errors.append(f"Title exceeds {max_title} characters")

        max_desc = limits.get("max_description", 0)
        if max_desc and len(description) > max_desc:
            errors.append(f"Description exceeds {max_desc} characters")

        max_tags = limits.get("max_tags", 0)
        if max_tags and len(",".join(tags)) > max_tags:
            errors.append(f"Tags exceed {max_tags} characters total")

        return errors

    def _generate_platform_title(
        self,
        content: str,
        platform: str,
        max_length: int
    ) -> str:
        """Génère un titre optimisé pour la plateforme"""
        # TODO: Utiliser LLM
        title = content[:max_length - 3] + "..." if len(content) > max_length else content
        return title

    def _generate_platform_description(
        self,
        content: str,
        platform: str,
        max_length: int
    ) -> str:
        """Génère une description optimisée"""
        # TODO: Utiliser LLM
        return content[:max_length]

    def _generate_platform_tags(
        self,
        content: str,
        platform: str,
        language: str
    ) -> List[str]:
        """Génère des tags optimisés"""
        # TODO: Utiliser LLM
        return ["video", "content", language]

    def _generate_hashtags(self, content: str, platform: str) -> List[str]:
        """Génère des hashtags pour les réseaux sociaux"""
        # TODO: Utiliser LLM pour générer des hashtags pertinents
        return ["#video", "#content"]

    def get_best_posting_time(
        self,
        platform: str,
        timezone: str = "Europe/Paris"
    ) -> Dict[str, Any]:
        """
        Recommande le meilleur moment pour publier.
        Basé sur les données générales d'engagement.
        """
        best_times = {
            "youtube": {
                "weekday": ["15:00", "17:00", "21:00"],
                "weekend": ["10:00", "14:00", "20:00"]
            },
            "tiktok": {
                "weekday": ["12:00", "19:00", "21:00"],
                "weekend": ["11:00", "19:00", "22:00"]
            },
            "instagram": {
                "weekday": ["11:00", "13:00", "19:00"],
                "weekend": ["10:00", "14:00", "19:00"]
            },
            "linkedin": {
                "weekday": ["08:00", "12:00", "17:00"],
                "weekend": ["10:00"]  # Moins actif le weekend
            },
            "twitter": {
                "weekday": ["09:00", "12:00", "17:00"],
                "weekend": ["11:00", "14:00"]
            }
        }

        return {
            "platform": platform,
            "timezone": timezone,
            "recommended_times": best_times.get(platform, {})
        }
