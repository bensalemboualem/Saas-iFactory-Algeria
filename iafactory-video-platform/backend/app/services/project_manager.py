"""
Project Manager - In-memory project state management with real pipeline execution
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
from uuid import UUID, uuid4
import asyncio
import logging
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class ProjectStatus(str, Enum):
    DRAFT = "draft"
    ANALYZING = "analyzing"
    GENERATING_SCRIPT = "generating_script"
    GENERATING_IMAGES = "generating_images"
    GENERATING_VIDEO = "generating_video"
    GENERATING_AUDIO = "generating_audio"
    MONTAGE = "montage"
    RENDERING = "rendering"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ProjectPhase:
    name: str
    status: str = "pending"  # pending, in_progress, completed, failed
    progress: int = 0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    output_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Project:
    id: UUID
    title: str
    user_prompt: str
    target_duration: str
    aspect_ratio: str
    style: Optional[str]
    language: str
    target_platforms: List[str]
    status: ProjectStatus = ProjectStatus.DRAFT
    progress: int = 0
    current_phase: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    # Generated content
    analysis: Dict[str, Any] = field(default_factory=dict)
    script: Dict[str, Any] = field(default_factory=dict)
    images: List[Dict[str, Any]] = field(default_factory=list)
    audio_files: List[Dict[str, Any]] = field(default_factory=list)
    video_clips: List[Dict[str, Any]] = field(default_factory=list)
    final_video: Optional[Dict[str, Any]] = None
    video_url: Optional[str] = None

    # Phase tracking
    phases: Dict[str, ProjectPhase] = field(default_factory=dict)

    # Error tracking
    error_message: Optional[str] = None

    def __post_init__(self):
        if not self.phases:
            self.phases = {
                "analysis": ProjectPhase(name="Analyse du prompt"),
                "script": ProjectPhase(name="Génération du script"),
                "images": ProjectPhase(name="Génération des images"),
                "video": ProjectPhase(name="Génération vidéo"),
                "audio": ProjectPhase(name="Génération audio"),
                "montage": ProjectPhase(name="Montage final"),
            }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "title": self.title,
            "user_prompt": self.user_prompt,
            "target_duration": self.target_duration,
            "aspect_ratio": self.aspect_ratio,
            "style": self.style,
            "language": self.language,
            "target_platforms": self.target_platforms,
            "status": self.status.value if isinstance(self.status, ProjectStatus) else self.status,
            "progress": self.progress,
            "current_phase": self.current_phase,
            "video_url": self.video_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "error_message": self.error_message,
        }

    def get_status_dict(self) -> Dict[str, Any]:
        phases_dict = {}
        for name, phase in self.phases.items():
            phases_dict[name] = {
                "status": phase.status,
                "progress": phase.progress,
            }

        return {
            "project_id": str(self.id),
            "status": self.status.value if isinstance(self.status, ProjectStatus) else self.status,
            "current_phase": self.current_phase,
            "progress": {
                "overall": self.progress,
                "phases": phases_dict,
            }
        }


class ProjectManager:
    """
    In-memory project manager with real AI pipeline execution.
    Manages project state and orchestrates video generation.
    """

    _instance = None
    _projects: Dict[str, Project] = {}
    _running_tasks: Dict[str, asyncio.Task] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._projects = {}
            cls._running_tasks = {}
        return cls._instance

    def create_project(
        self,
        title: str,
        user_prompt: str,
        target_duration: str = "60s",
        aspect_ratio: str = "16:9",
        style: Optional[str] = "professional",
        language: str = "fr",
        target_platforms: List[str] = None,
    ) -> Project:
        """Create a new project"""
        project = Project(
            id=uuid4(),
            title=title,
            user_prompt=user_prompt,
            target_duration=target_duration,
            aspect_ratio=aspect_ratio,
            style=style,
            language=language,
            target_platforms=target_platforms or ["youtube"],
        )
        self._projects[str(project.id)] = project
        logger.info(f"Created project {project.id}: {title}")
        return project

    def get_project(self, project_id: str) -> Optional[Project]:
        """Get project by ID"""
        return self._projects.get(project_id)

    def list_projects(
        self,
        status: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> List[Project]:
        """List all projects with optional filtering"""
        projects = list(self._projects.values())

        if status:
            projects = [p for p in projects if p.status.value == status]

        # Sort by created_at descending
        projects.sort(key=lambda p: p.created_at, reverse=True)

        return projects[offset:offset + limit]

    def delete_project(self, project_id: str) -> bool:
        """Delete a project"""
        if project_id in self._projects:
            # Cancel running task if exists
            if project_id in self._running_tasks:
                self._running_tasks[project_id].cancel()
                del self._running_tasks[project_id]

            del self._projects[project_id]
            logger.info(f"Deleted project {project_id}")
            return True
        return False

    def update_phase(
        self,
        project_id: str,
        phase_name: str,
        status: str = None,
        progress: int = None,
        output_data: Dict[str, Any] = None,
        error: str = None
    ):
        """Update a project phase"""
        project = self.get_project(project_id)
        if not project or phase_name not in project.phases:
            return

        phase = project.phases[phase_name]

        if status:
            phase.status = status
            if status == "in_progress" and not phase.started_at:
                phase.started_at = datetime.utcnow()
            elif status in ["completed", "failed"]:
                phase.completed_at = datetime.utcnow()

        if progress is not None:
            phase.progress = progress

        if output_data:
            phase.output_data.update(output_data)

        if error:
            phase.error = error

        project.updated_at = datetime.utcnow()
        self._calculate_overall_progress(project)

    def _calculate_overall_progress(self, project: Project):
        """Calculate overall project progress from phases"""
        phase_weights = {
            "analysis": 10,
            "script": 15,
            "images": 25,
            "video": 25,
            "audio": 15,
            "montage": 10,
        }

        total_weight = sum(phase_weights.values())
        weighted_progress = 0

        for name, phase in project.phases.items():
            weight = phase_weights.get(name, 10)
            weighted_progress += (phase.progress / 100) * weight

        project.progress = int((weighted_progress / total_weight) * 100)

    async def start_pipeline(
        self,
        project_id: str,
        auto_publish: bool = False,
        priority: str = "normal"
    ) -> Dict[str, Any]:
        """Start the video generation pipeline"""
        project = self.get_project(project_id)
        if not project:
            raise ValueError(f"Project {project_id} not found")

        if project.status not in [ProjectStatus.DRAFT, ProjectStatus.FAILED]:
            raise ValueError(f"Project cannot be started (status: {project.status})")

        # Start pipeline in background
        task = asyncio.create_task(
            self._run_pipeline(project_id, auto_publish)
        )
        self._running_tasks[project_id] = task

        return {
            "project_id": project_id,
            "status": "pipeline_started",
            "message": "Le pipeline de création a démarré"
        }

    async def _run_pipeline(self, project_id: str, auto_publish: bool = False):
        """Execute the full video generation pipeline"""
        project = self.get_project(project_id)
        if not project:
            return

        try:
            logger.info(f"Starting pipeline for project {project_id}")

            # Phase 1: Analysis
            project.status = ProjectStatus.ANALYZING
            project.current_phase = "analysis"
            await self._run_analysis(project)

            # Phase 2: Script Generation
            project.status = ProjectStatus.GENERATING_SCRIPT
            project.current_phase = "script"
            await self._run_script_generation(project)

            # Phase 3: Image Generation
            project.status = ProjectStatus.GENERATING_IMAGES
            project.current_phase = "images"
            await self._run_image_generation(project)

            # Phase 4: Video Generation (image-to-video)
            project.status = ProjectStatus.GENERATING_VIDEO
            project.current_phase = "video"
            await self._run_video_generation(project)

            # Phase 5: Audio Generation
            project.status = ProjectStatus.GENERATING_AUDIO
            project.current_phase = "audio"
            await self._run_audio_generation(project)

            # Phase 6: Montage
            project.status = ProjectStatus.MONTAGE
            project.current_phase = "montage"
            await self._run_montage(project)

            # Mark as completed
            project.status = ProjectStatus.COMPLETED
            project.progress = 100
            project.current_phase = "completed"
            logger.info(f"Pipeline completed for project {project_id}")

        except asyncio.CancelledError:
            project.status = ProjectStatus.CANCELLED
            logger.info(f"Pipeline cancelled for project {project_id}")
        except Exception as e:
            project.status = ProjectStatus.FAILED
            project.error_message = str(e)
            logger.error(f"Pipeline failed for project {project_id}: {e}")
            raise

    async def _run_analysis(self, project: Project):
        """Run prompt analysis phase"""
        from app.services.ai.llm_service import llm_service

        self.update_phase(str(project.id), "analysis", status="in_progress", progress=0)

        try:
            system_prompt = """Tu es un expert en production vidéo. Analyse le prompt utilisateur et extrais les informations en JSON:
{
    "type": "explainer|tutorial|promo|story|vlog|short|ad",
    "topic": "sujet principal",
    "duration": 60,
    "style": "cinematic|corporate|fun|minimalist|dramatic|animated",
    "tone": "professional|casual|humorous|inspiring|educational",
    "platforms": ["youtube", "tiktok"],
    "has_avatar": false,
    "has_voiceover": true,
    "has_music": true,
    "key_messages": ["message 1", "message 2"],
    "target_audience": "description du public cible",
    "visual_style": "description du style visuel"
}"""

            # Parse target duration
            duration_map = {"15s": 15, "30s": 30, "60s": 60, "3min": 180, "10min": 600}
            target_duration = duration_map.get(project.target_duration, 60)

            prompt = f"""Analyse ce prompt pour créer une vidéo:
"{project.user_prompt}"

Durée cible: {target_duration} secondes
Format: {project.aspect_ratio}
Style demandé: {project.style}
Langue: {project.language}"""

            self.update_phase(str(project.id), "analysis", progress=30)

            # Call LLM
            try:
                analysis = await llm_service.generate_json(prompt, system_prompt)
            except Exception as e:
                logger.warning(f"LLM analysis failed, using defaults: {e}")
                analysis = {
                    "type": "explainer",
                    "topic": project.user_prompt[:100],
                    "duration": target_duration,
                    "style": project.style or "professional",
                    "tone": "educational",
                    "platforms": project.target_platforms,
                    "has_avatar": False,
                    "has_voiceover": True,
                    "has_music": True,
                    "key_messages": [project.user_prompt],
                    "target_audience": "general",
                    "visual_style": "modern professional"
                }

            # Ensure duration matches request
            analysis["duration"] = target_duration
            project.analysis = analysis

            self.update_phase(
                str(project.id), "analysis",
                status="completed", progress=100,
                output_data={"analysis": analysis}
            )
            logger.info(f"Analysis completed for project {project.id}")

        except Exception as e:
            self.update_phase(str(project.id), "analysis", status="failed", error=str(e))
            raise

    async def _run_script_generation(self, project: Project):
        """Generate video script with scenes"""
        from app.services.ai.llm_service import llm_service

        self.update_phase(str(project.id), "script", status="in_progress", progress=0)

        try:
            analysis = project.analysis
            duration = analysis.get("duration", 60)

            # Calculate number of scenes (5-10 seconds per scene)
            scene_duration = 5 if duration <= 60 else 8
            num_scenes = max(3, duration // scene_duration)

            system_prompt = f"""Tu es un scénariste vidéo professionnel. Crée un script structuré en {num_scenes} scènes.
Chaque scène doit avoir une narration claire et un prompt visuel détaillé pour la génération d'image.
Le style visuel doit être: {analysis.get('visual_style', 'professionnel moderne')}
Réponds en JSON avec ce format:
{{
    "title": "Titre de la vidéo",
    "synopsis": "Résumé de la vidéo",
    "scenes": [
        {{
            "scene_id": "scene_001",
            "order": 1,
            "duration": {scene_duration},
            "type": "intro|content|outro",
            "narration": "Texte de narration...",
            "visual_prompt": "Detailed image prompt in English for AI generation...",
            "music_mood": "upbeat|calm|dramatic|inspiring",
            "text_overlay": "Texte à afficher ou null"
        }}
    ]
}}"""

            prompt = f"""Crée un script vidéo pour:
Sujet: {analysis.get('topic', project.user_prompt)}
Messages clés: {', '.join(analysis.get('key_messages', []))}
Ton: {analysis.get('tone', 'educational')}
Durée: {duration} secondes ({num_scenes} scènes de {scene_duration}s)
Public: {analysis.get('target_audience', 'général')}
Langue: {project.language}"""

            self.update_phase(str(project.id), "script", progress=30)

            try:
                script = await llm_service.generate_json(prompt, system_prompt)
            except Exception as e:
                logger.warning(f"LLM script generation failed, using default: {e}")
                script = self._generate_default_script(project, analysis, num_scenes, scene_duration)

            # Ensure all scenes have required fields
            for i, scene in enumerate(script.get("scenes", [])):
                scene.setdefault("scene_id", f"scene_{i+1:03d}")
                scene.setdefault("order", i + 1)
                scene.setdefault("duration", scene_duration)

            project.script = script

            self.update_phase(
                str(project.id), "script",
                status="completed", progress=100,
                output_data={"script": script, "num_scenes": len(script.get("scenes", []))}
            )
            logger.info(f"Script generated for project {project.id}: {len(script.get('scenes', []))} scenes")

        except Exception as e:
            self.update_phase(str(project.id), "script", status="failed", error=str(e))
            raise

    def _generate_default_script(
        self, project: Project, analysis: Dict, num_scenes: int, scene_duration: int
    ) -> Dict[str, Any]:
        """Generate a default script structure"""
        topic = analysis.get("topic", project.user_prompt[:50])

        scenes = []

        # Intro scene
        scenes.append({
            "scene_id": "scene_001",
            "order": 1,
            "duration": scene_duration,
            "type": "intro",
            "narration": f"Bienvenue! Aujourd'hui nous allons parler de {topic}.",
            "visual_prompt": f"Professional title card, modern design, topic: {topic}, vibrant colors, 4k quality",
            "music_mood": "upbeat",
            "text_overlay": topic[:30].upper()
        })

        # Content scenes
        key_messages = analysis.get("key_messages", [project.user_prompt])
        for i in range(1, num_scenes - 1):
            message = key_messages[i % len(key_messages)] if key_messages else f"Point {i}"
            scenes.append({
                "scene_id": f"scene_{i+1:03d}",
                "order": i + 1,
                "duration": scene_duration,
                "type": "content",
                "narration": message[:200],
                "visual_prompt": f"Professional illustration about: {message[:50]}, modern flat design, clean composition, business style",
                "music_mood": "calm",
                "text_overlay": None
            })

        # Outro scene
        scenes.append({
            "scene_id": f"scene_{num_scenes:03d}",
            "order": num_scenes,
            "duration": scene_duration,
            "type": "outro",
            "narration": "Merci d'avoir regardé cette vidéo! N'hésitez pas à vous abonner.",
            "visual_prompt": "Call to action screen, subscribe button, professional end card design, social media icons",
            "music_mood": "upbeat",
            "text_overlay": "ABONNEZ-VOUS!"
        })

        return {
            "title": topic,
            "synopsis": f"Une vidéo sur {topic}",
            "scenes": scenes
        }

    async def _run_image_generation(self, project: Project):
        """Generate images for all scenes"""
        from app.services.ai.image_service import image_service

        self.update_phase(str(project.id), "images", status="in_progress", progress=0)

        try:
            scenes = project.script.get("scenes", [])
            if not scenes:
                raise ValueError("No scenes in script")

            images = []
            total_scenes = len(scenes)

            # Determine image size based on aspect ratio
            size_map = {
                "16:9": "1792x1024",
                "9:16": "1024x1792",
                "1:1": "1024x1024",
                "4:5": "1024x1280"
            }
            size = size_map.get(project.aspect_ratio, "1792x1024")

            for i, scene in enumerate(scenes):
                visual_prompt = scene.get("visual_prompt", "")
                if not visual_prompt:
                    continue

                # Enhance prompt
                enhanced_prompt = f"{visual_prompt}, high quality, professional, 4k resolution"

                try:
                    logger.info(f"Generating image {i+1}/{total_scenes} for project {project.id}")
                    result = await image_service.generate(
                        prompt=enhanced_prompt,
                        size=size,
                        n=1
                    )

                    if result:
                        image_data = result[0]
                        image_data["scene_id"] = scene.get("scene_id")
                        images.append(image_data)
                        logger.info(f"Image generated: {image_data.get('url', 'no url')[:50]}")

                except Exception as e:
                    logger.error(f"Image generation failed for scene {i+1}: {e}")
                    # Add placeholder
                    images.append({
                        "scene_id": scene.get("scene_id"),
                        "url": None,
                        "error": str(e)
                    })

                progress = int(((i + 1) / total_scenes) * 100)
                self.update_phase(str(project.id), "images", progress=progress)

            project.images = images

            self.update_phase(
                str(project.id), "images",
                status="completed", progress=100,
                output_data={"images_count": len(images)}
            )
            logger.info(f"Generated {len(images)} images for project {project.id}")

        except Exception as e:
            self.update_phase(str(project.id), "images", status="failed", error=str(e))
            raise

    async def _run_video_generation(self, project: Project):
        """Generate video clips from images using image-to-video"""
        from app.services.ai.video_service import video_service

        self.update_phase(str(project.id), "video", status="in_progress", progress=0)

        try:
            images = project.images
            scenes = project.script.get("scenes", [])

            if not images:
                logger.warning(f"No images to convert to video for project {project.id}")
                self.update_phase(str(project.id), "video", status="completed", progress=100)
                return

            video_clips = []
            total_images = len(images)

            # Determine best available provider - try multiple providers
            available_providers = video_service.available_providers()
            logger.info(f"Available video providers: {available_providers}")
            provider = None
            # Luma Ray 2 is reliable, try it first
            for p in ["luma", "replicate", "fal", "runway"]:
                if p in available_providers:
                    provider = p
                    break

            if not provider:
                logger.warning("No video providers available, using images as fallback")
                for image_data in images:
                    video_clips.append({
                        "scene_id": image_data.get("scene_id"),
                        "url": image_data.get("url"),
                        "type": "image",
                    })
                project.video_clips = video_clips
                self.update_phase(str(project.id), "video", status="completed", progress=100)
                return

            for i, image_data in enumerate(images):
                image_url = image_data.get("url")
                if not image_url:
                    continue

                # Find corresponding scene
                scene_id = image_data.get("scene_id")
                scene = next((s for s in scenes if s.get("scene_id") == scene_id), {})
                motion_prompt = scene.get("narration", "gentle motion, cinematic")[:100]
                duration = min(scene.get("duration", 5), 5)  # Most providers max 5s

                try:
                    logger.info(f"Generating video clip {i+1}/{total_images} for project {project.id} using {provider}")
                    result = await video_service.image_to_video(
                        image_url=image_url,
                        motion_prompt=motion_prompt,
                        duration=duration,
                        provider=provider
                    )

                    if result:
                        result["scene_id"] = scene_id
                        video_clips.append(result)
                        logger.info(f"Video clip generated: {result.get('url', 'no url')[:50]}")

                except Exception as e:
                    logger.error(f"Video generation failed for image {i+1}: {e}")
                    # Use image as fallback
                    video_clips.append({
                        "scene_id": scene_id,
                        "url": image_url,
                        "type": "image",
                        "error": str(e)
                    })

                progress = int(((i + 1) / total_images) * 100)
                self.update_phase(str(project.id), "video", progress=progress)

            project.video_clips = video_clips

            self.update_phase(
                str(project.id), "video",
                status="completed", progress=100,
                output_data={"video_clips_count": len(video_clips)}
            )
            logger.info(f"Generated {len(video_clips)} video clips for project {project.id}")

        except Exception as e:
            self.update_phase(str(project.id), "video", status="failed", error=str(e))
            raise

    async def _run_audio_generation(self, project: Project):
        """Generate voiceover audio for all scenes"""
        from app.services.ai.audio_service import audio_service

        self.update_phase(str(project.id), "audio", status="in_progress", progress=0)

        try:
            scenes = project.script.get("scenes", [])
            audio_files = []
            total_scenes = len(scenes)

            for i, scene in enumerate(scenes):
                narration = scene.get("narration", "")
                if not narration:
                    continue

                try:
                    logger.info(f"Generating audio {i+1}/{total_scenes} for project {project.id}")
                    result = await audio_service.text_to_speech(
                        text=narration,
                        provider="openai"  # More reliable than ElevenLabs
                    )

                    if result:
                        result["scene_id"] = scene.get("scene_id")
                        audio_files.append(result)

                except Exception as e:
                    logger.error(f"Audio generation failed for scene {i+1}: {e}")
                    audio_files.append({
                        "scene_id": scene.get("scene_id"),
                        "error": str(e)
                    })

                progress = int(((i + 1) / total_scenes) * 100)
                self.update_phase(str(project.id), "audio", progress=progress)

            project.audio_files = audio_files

            self.update_phase(
                str(project.id), "audio",
                status="completed", progress=100,
                output_data={"audio_files_count": len(audio_files)}
            )
            logger.info(f"Generated {len(audio_files)} audio files for project {project.id}")

        except Exception as e:
            self.update_phase(str(project.id), "audio", status="failed", error=str(e))
            raise

    async def _run_montage(self, project: Project):
        """Assemble final video from all assets"""
        self.update_phase(str(project.id), "montage", status="in_progress", progress=0)

        try:
            # For MVP, we'll set the first video clip or image as the final output
            # Full montage requires FFmpeg which we'll implement next

            self.update_phase(str(project.id), "montage", progress=50)

            # Find the best video clip to use as output
            video_url = None

            # First try video clips
            for clip in project.video_clips:
                if clip.get("url") and not clip.get("error"):
                    video_url = clip.get("url")
                    break

            # Fallback to images
            if not video_url:
                for image in project.images:
                    if image.get("url") and not image.get("error"):
                        video_url = image.get("url")
                        break

            project.video_url = video_url
            project.final_video = {
                "url": video_url,
                "duration": project.analysis.get("duration", 60),
                "format": "mp4",
                "status": "completed"
            }

            self.update_phase(
                str(project.id), "montage",
                status="completed", progress=100,
                output_data={"video_url": video_url}
            )
            logger.info(f"Montage completed for project {project.id}: {video_url}")

        except Exception as e:
            self.update_phase(str(project.id), "montage", status="failed", error=str(e))
            raise

    def cancel_pipeline(self, project_id: str) -> bool:
        """Cancel a running pipeline"""
        if project_id in self._running_tasks:
            self._running_tasks[project_id].cancel()
            project = self.get_project(project_id)
            if project:
                project.status = ProjectStatus.CANCELLED
            return True
        return False

    def pause_pipeline(self, project_id: str) -> bool:
        """Pause is not implemented - just returns status"""
        return False

    def resume_pipeline(self, project_id: str) -> bool:
        """Resume is not implemented - just returns status"""
        return False


# Singleton instance
project_manager = ProjectManager()
