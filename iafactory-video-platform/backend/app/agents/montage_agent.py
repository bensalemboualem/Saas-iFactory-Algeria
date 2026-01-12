"""
Montage Agent - Assemblage et édition vidéo
"""
from typing import List, Dict, Any, Optional
from app.agents.base import BaseAgent, AgentTask, AgentResult
from app.core.config import settings


class MontageAgent(BaseAgent):
    """
    Agent de montage vidéo.

    Utilise FFmpeg pour le processing vidéo.

    Responsabilités:
    - Assemble les clips selon la timeline
    - Ajoute les transitions
    - Synchronise audio/vidéo
    - Ajoute les overlays (texte, logo)
    - Applique les effets
    - Exporte dans différents formats
    """

    @property
    def agent_type(self) -> str:
        return "montage"

    @property
    def capabilities(self) -> List[str]:
        return [
            "assemble_timeline",
            "add_transitions",
            "add_text_overlay",
            "add_logo",
            "apply_effects",
            "sync_audio",
            "add_subtitles",
            "render_video",
            "create_variants"
        ]

    # Formats de sortie supportés
    OUTPUT_FORMATS = {
        "youtube": {"width": 1920, "height": 1080, "fps": 30, "bitrate": "8M"},
        "youtube_short": {"width": 1080, "height": 1920, "fps": 30, "bitrate": "6M"},
        "tiktok": {"width": 1080, "height": 1920, "fps": 30, "bitrate": "6M"},
        "instagram_reels": {"width": 1080, "height": 1920, "fps": 30, "bitrate": "6M"},
        "instagram_feed": {"width": 1080, "height": 1080, "fps": 30, "bitrate": "5M"},
        "instagram_story": {"width": 1080, "height": 1920, "fps": 30, "bitrate": "5M"},
        "linkedin": {"width": 1920, "height": 1080, "fps": 30, "bitrate": "6M"},
        "twitter": {"width": 1280, "height": 720, "fps": 30, "bitrate": "5M"},
    }

    def __init__(self):
        super().__init__()
        self.ffmpeg_path = settings.FFMPEG_PATH

    async def _execute_task(self, task: AgentTask) -> AgentResult:
        """Exécute une tâche de montage"""

        handlers = {
            "assemble_timeline": self._assemble_timeline,
            "add_transitions": self._add_transitions,
            "add_text_overlay": self._add_text_overlay,
            "add_logo": self._add_logo,
            "apply_effects": self._apply_effects,
            "sync_audio": self._sync_audio,
            "add_subtitles": self._add_subtitles,
            "render_video": self._render_video,
            "create_variants": self._create_variants,
        }

        handler = handlers.get(task.task_type)
        return await handler(task)

    async def _assemble_timeline(self, task: AgentTask) -> AgentResult:
        """
        Assemble tous les clips selon la timeline du script.
        """
        clips = task.input_data.get("clips", [])
        audio_tracks = task.input_data.get("audio_tracks", [])
        music_track = task.input_data.get("music_track")
        output_format = task.input_data.get("format", "youtube")

        if not clips:
            return AgentResult(
                task_id=task.task_id,
                success=False,
                error_message="No clips provided"
            )

        format_specs = self.OUTPUT_FORMATS.get(output_format, self.OUTPUT_FORMATS["youtube"])

        # Construction de la timeline
        timeline = {
            "timeline_id": f"timeline_{task.task_id[:8]}",
            "format": output_format,
            "specs": format_specs,
            "tracks": {
                "video": [],
                "audio": [],
                "music": [],
                "text": []
            },
            "total_duration": 0
        }

        # Ajouter les clips vidéo
        current_time = 0
        for clip in clips:
            clip_duration = clip.get("duration", 5)
            timeline["tracks"]["video"].append({
                "clip_id": clip.get("id"),
                "path": clip.get("path"),
                "start": current_time,
                "end": current_time + clip_duration,
                "duration": clip_duration
            })
            current_time += clip_duration

        timeline["total_duration"] = current_time

        # Ajouter les pistes audio
        for audio in audio_tracks:
            timeline["tracks"]["audio"].append({
                "audio_id": audio.get("id"),
                "path": audio.get("path"),
                "start": audio.get("start", 0),
                "end": audio.get("end", current_time),
                "volume": audio.get("volume", 1.0)
            })

        # Ajouter la musique de fond
        if music_track:
            timeline["tracks"]["music"].append({
                "music_id": music_track.get("id"),
                "path": music_track.get("path"),
                "start": 0,
                "end": current_time,
                "volume": music_track.get("volume", 0.3),
                "fade_in": 2,
                "fade_out": 3
            })

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"timeline": timeline}
        )

    async def _add_transitions(self, task: AgentTask) -> AgentResult:
        """Ajoute des transitions entre les clips"""
        timeline = task.input_data.get("timeline", {})
        transitions = task.input_data.get("transitions", [])
        default_transition = task.input_data.get("default_transition", "crossfade")
        transition_duration = task.input_data.get("duration", 0.5)

        # Types de transitions disponibles
        available_transitions = [
            "cut", "crossfade", "fade_black", "fade_white",
            "wipe_left", "wipe_right", "wipe_up", "wipe_down",
            "zoom_in", "zoom_out", "slide_left", "slide_right"
        ]

        video_clips = timeline.get("tracks", {}).get("video", [])
        applied_transitions = []

        for i in range(len(video_clips) - 1):
            # Utiliser la transition spécifiée ou la valeur par défaut
            trans = transitions[i] if i < len(transitions) else default_transition
            if trans not in available_transitions:
                trans = default_transition

            applied_transitions.append({
                "from_clip": video_clips[i].get("clip_id"),
                "to_clip": video_clips[i + 1].get("clip_id"),
                "type": trans,
                "duration": transition_duration,
                "position": video_clips[i].get("end")
            })

        timeline["transitions"] = applied_transitions

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"timeline": timeline}
        )

    async def _add_text_overlay(self, task: AgentTask) -> AgentResult:
        """Ajoute du texte sur la vidéo"""
        timeline = task.input_data.get("timeline", {})
        text_overlays = task.input_data.get("overlays", [])

        """
        Format overlay:
        {
            "text": "Titre",
            "start": 0,
            "end": 5,
            "position": "center",  # top, center, bottom, top_left, etc.
            "font_size": 48,
            "font_color": "#FFFFFF",
            "background_color": "#000000",
            "background_opacity": 0.5,
            "animation": "fade_in"  # fade_in, slide_up, typewriter, none
        }
        """

        for overlay in text_overlays:
            # Valeurs par défaut
            overlay.setdefault("font_size", 36)
            overlay.setdefault("font_color", "#FFFFFF")
            overlay.setdefault("position", "bottom")
            overlay.setdefault("animation", "fade_in")

            timeline["tracks"]["text"].append(overlay)

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"timeline": timeline}
        )

    async def _add_logo(self, task: AgentTask) -> AgentResult:
        """Ajoute un logo/watermark"""
        timeline = task.input_data.get("timeline", {})
        logo_path = task.input_data.get("logo_path")
        position = task.input_data.get("position", "bottom_right")
        opacity = task.input_data.get("opacity", 0.7)
        size = task.input_data.get("size", 100)  # pixels

        if not logo_path:
            return AgentResult(
                task_id=task.task_id,
                success=False,
                error_message="logo_path is required"
            )

        timeline["logo"] = {
            "path": logo_path,
            "position": position,
            "opacity": opacity,
            "size": size,
            "start": 0,
            "end": timeline.get("total_duration", 0)
        }

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"timeline": timeline}
        )

    async def _apply_effects(self, task: AgentTask) -> AgentResult:
        """Applique des effets visuels"""
        timeline = task.input_data.get("timeline", {})
        effects = task.input_data.get("effects", [])

        """
        Effets disponibles:
        - color_grade: {"preset": "cinematic", "intensity": 0.5}
        - brightness: {"value": 0.1}
        - contrast: {"value": 0.1}
        - saturation: {"value": 0.1}
        - blur: {"amount": 5}
        - vignette: {"intensity": 0.3}
        - stabilize: {}
        - speed: {"factor": 1.5}  # slow-mo ou accéléré
        """

        available_effects = [
            "color_grade", "brightness", "contrast", "saturation",
            "blur", "vignette", "stabilize", "speed", "denoise"
        ]

        applied_effects = []
        for effect in effects:
            effect_type = effect.get("type")
            if effect_type in available_effects:
                applied_effects.append(effect)

        timeline["effects"] = applied_effects

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"timeline": timeline}
        )

    async def _sync_audio(self, task: AgentTask) -> AgentResult:
        """Synchronise les pistes audio avec la vidéo"""
        timeline = task.input_data.get("timeline", {})
        auto_duck = task.input_data.get("auto_duck", True)
        normalize = task.input_data.get("normalize", True)

        # Auto-ducking: baisse la musique quand il y a de la voix
        if auto_duck:
            timeline["audio_settings"] = timeline.get("audio_settings", {})
            timeline["audio_settings"]["auto_duck"] = {
                "enabled": True,
                "duck_amount": -10,  # dB
                "attack": 0.3,       # secondes
                "release": 0.5      # secondes
            }

        # Normalisation du volume
        if normalize:
            timeline["audio_settings"]["normalize"] = {
                "enabled": True,
                "target_lufs": -14  # Standard pour YouTube
            }

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"timeline": timeline}
        )

    async def _add_subtitles(self, task: AgentTask) -> AgentResult:
        """Ajoute des sous-titres"""
        timeline = task.input_data.get("timeline", {})
        subtitles = task.input_data.get("subtitles", [])
        style = task.input_data.get("style", "default")

        """
        Format subtitles:
        [
            {"start": 0, "end": 2, "text": "Bonjour"},
            {"start": 2, "end": 5, "text": "Bienvenue dans cette vidéo"}
        ]
        """

        # Styles de sous-titres
        subtitle_styles = {
            "default": {
                "font_size": 24,
                "font_color": "#FFFFFF",
                "background_color": "#000000",
                "background_opacity": 0.7,
                "position": "bottom"
            },
            "modern": {
                "font_size": 28,
                "font_color": "#FFFFFF",
                "background_color": "none",
                "stroke_color": "#000000",
                "stroke_width": 2,
                "position": "center"
            },
            "karaoke": {
                "font_size": 32,
                "font_color": "#FFFF00",
                "highlight_color": "#FF0000",
                "position": "bottom"
            }
        }

        selected_style = subtitle_styles.get(style, subtitle_styles["default"])

        timeline["subtitles"] = {
            "segments": subtitles,
            "style": selected_style
        }

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"timeline": timeline}
        )

    async def _render_video(self, task: AgentTask) -> AgentResult:
        """
        Rend la vidéo finale.
        """
        timeline = task.input_data.get("timeline", {})
        output_path = task.input_data.get("output_path")
        output_format = task.input_data.get("format", "youtube")
        quality = task.input_data.get("quality", "high")

        if not timeline:
            return AgentResult(
                task_id=task.task_id,
                success=False,
                error_message="Timeline is required"
            )

        format_specs = self.OUTPUT_FORMATS.get(output_format, self.OUTPUT_FORMATS["youtube"])

        # Ajustement qualité
        if quality == "low":
            format_specs["bitrate"] = "2M"
        elif quality == "medium":
            format_specs["bitrate"] = "5M"
        # high utilise la valeur par défaut

        # TODO: Appel réel à FFmpeg pour le rendu
        # Pour le moment, simulation
        video_result = {
            "video_id": f"final_{task.task_id[:8]}",
            "output_path": output_path or f"output_{task.task_id[:8]}.mp4",
            "format": output_format,
            "specs": format_specs,
            "duration": timeline.get("total_duration", 0),
            "file_size": None,  # À calculer après rendu
            "status": "rendered"
        }

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"video": video_result}
        )

    async def _create_variants(self, task: AgentTask) -> AgentResult:
        """
        Crée des variantes de la vidéo pour différentes plateformes.
        """
        source_video = task.input_data.get("source_video")
        target_formats = task.input_data.get("formats", ["youtube", "tiktok", "instagram_reels"])

        if not source_video:
            return AgentResult(
                task_id=task.task_id,
                success=False,
                error_message="source_video is required"
            )

        variants = []
        for fmt in target_formats:
            if fmt not in self.OUTPUT_FORMATS:
                continue

            specs = self.OUTPUT_FORMATS[fmt]
            variants.append({
                "format": fmt,
                "specs": specs,
                "output_path": f"{source_video}_{fmt}.mp4",
                "status": "pending"
            })

        # TODO: Générer réellement les variantes avec FFmpeg

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={
                "source_video": source_video,
                "variants": variants,
                "total_variants": len(variants)
            }
        )

    def generate_ffmpeg_command(self, timeline: Dict[str, Any]) -> str:
        """
        Génère la commande FFmpeg pour le rendu.
        (Helper pour le debug et les tests)
        """
        # TODO: Implémenter la génération de commande FFmpeg complexe
        return "ffmpeg -i input.mp4 -c:v libx264 output.mp4"
