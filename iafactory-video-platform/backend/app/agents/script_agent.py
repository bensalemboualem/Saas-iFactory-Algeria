"""
Script Agent - Génération de scripts vidéo professionnels
"""
from typing import List, Dict, Any
from app.agents.base import BaseAgent, AgentTask, AgentResult
from app.core.config import settings


class ScriptAgent(BaseAgent):
    """
    Agent de création de scripts.

    Responsabilités:
    - Génère des scripts structurés à partir du prompt
    - Crée une timeline avec des scènes
    - Génère les prompts visuels pour chaque scène
    - Écrit la narration/voix off
    - Optimise le script pour la durée cible
    """

    @property
    def agent_type(self) -> str:
        return "script"

    @property
    def capabilities(self) -> List[str]:
        return [
            "generate_script",
            "create_scenes",
            "write_narration",
            "generate_visual_prompts",
            "optimize_duration",
            "edit_script",
            "translate_script"
        ]

    def __init__(self, llm_provider: str = None):
        super().__init__()
        self.llm_provider = llm_provider or settings.DEFAULT_LLM_PROVIDER

    async def _execute_task(self, task: AgentTask) -> AgentResult:
        """Exécute une tâche de script"""

        handlers = {
            "generate_script": self._generate_full_script,
            "create_scenes": self._create_scenes,
            "write_narration": self._write_narration,
            "generate_visual_prompts": self._generate_visual_prompts,
            "optimize_duration": self._optimize_duration,
            "edit_script": self._edit_script,
            "translate_script": self._translate_script,
        }

        handler = handlers.get(task.task_type)
        return await handler(task)

    async def _generate_full_script(self, task: AgentTask) -> AgentResult:
        """
        Génère un script complet avec toutes les scènes.
        """
        topic = task.input_data.get("topic", "")
        duration = task.input_data.get("duration", 60)
        style = task.input_data.get("style", "professional")
        tone = task.input_data.get("tone", "educational")
        key_messages = task.input_data.get("key_messages", [])
        language = task.input_data.get("language", "fr")

        # Calcul du nombre de scènes
        scene_duration = 5 if duration <= 60 else 10
        num_scenes = max(3, duration // scene_duration)

        # Structure de base du script
        script = {
            "title": f"Video: {topic[:50]}",
            "synopsis": f"Une vidéo {style} sur {topic}",
            "language": language,
            "target_duration": duration,
            "style": style,
            "tone": tone,
            "scenes": []
        }

        # Génération des scènes
        # Structure: Intro (15%) -> Contenu (70%) -> Outro (15%)
        intro_scenes = max(1, int(num_scenes * 0.15))
        outro_scenes = max(1, int(num_scenes * 0.15))
        content_scenes = num_scenes - intro_scenes - outro_scenes

        scene_order = 1

        # Intro
        for i in range(intro_scenes):
            scene = {
                "scene_id": f"scene_{scene_order:03d}",
                "order": scene_order,
                "duration": scene_duration,
                "type": "intro",
                "narration": f"Bienvenue dans cette vidéo sur {topic}.",
                "visual_prompt": f"Opening shot, {style} style, topic: {topic}, professional lighting",
                "music_mood": "upbeat_intro",
                "text_overlay": topic[:30].upper() if scene_order == 1 else None,
                "speaker": "narrator",
                "camera_movement": "zoom_in",
                "transition_in": "fade",
                "transition_out": "cut"
            }
            script["scenes"].append(scene)
            scene_order += 1

        # Contenu principal
        for i in range(content_scenes):
            message = key_messages[i % len(key_messages)] if key_messages else f"Point clé {i+1}"
            scene = {
                "scene_id": f"scene_{scene_order:03d}",
                "order": scene_order,
                "duration": scene_duration,
                "type": "content",
                "narration": message[:200],
                "visual_prompt": f"Illustrating: {message[:50]}, {style} visual style, high quality",
                "music_mood": "background_subtle",
                "text_overlay": None,
                "speaker": "narrator",
                "camera_movement": "static" if i % 2 == 0 else "pan_right",
                "transition_in": "cut",
                "transition_out": "cut"
            }
            script["scenes"].append(scene)
            scene_order += 1

        # Outro
        for i in range(outro_scenes):
            scene = {
                "scene_id": f"scene_{scene_order:03d}",
                "order": scene_order,
                "duration": scene_duration,
                "type": "outro",
                "narration": "Merci d'avoir regardé cette vidéo. N'oubliez pas de vous abonner!",
                "visual_prompt": f"Closing shot, call to action, {style} style, subscribe button",
                "music_mood": "upbeat_outro",
                "text_overlay": "ABONNEZ-VOUS!",
                "speaker": "narrator",
                "camera_movement": "zoom_out",
                "transition_in": "cut",
                "transition_out": "fade"
            }
            script["scenes"].append(scene)
            scene_order += 1

        # Calcul de la durée totale
        script["total_duration"] = sum(s["duration"] for s in script["scenes"])

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={
                "script": script,
                "num_scenes": len(script["scenes"]),
                "total_duration": script["total_duration"]
            },
            cost_cents=10  # Coût LLM estimé
        )

    async def _create_scenes(self, task: AgentTask) -> AgentResult:
        """Crée les scènes individuelles pour un script existant"""
        script_id = task.input_data.get("script_id")
        modifications = task.input_data.get("modifications", {})

        # TODO: Implémenter la modification de scènes
        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"modified": True}
        )

    async def _write_narration(self, task: AgentTask) -> AgentResult:
        """Écrit ou améliore la narration pour une scène"""
        scene = task.input_data.get("scene", {})
        style = task.input_data.get("style", "professional")

        # TODO: Appel LLM pour améliorer la narration
        improved_narration = scene.get("narration", "")

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"narration": improved_narration}
        )

    async def _generate_visual_prompts(self, task: AgentTask) -> AgentResult:
        """Génère des prompts visuels optimisés pour chaque scène"""
        scenes = task.input_data.get("scenes", [])
        image_provider = task.input_data.get("image_provider", "dalle")

        enhanced_prompts = []
        for scene in scenes:
            base_prompt = scene.get("visual_prompt", "")

            # Amélioration du prompt selon le provider
            if image_provider == "dalle":
                enhanced = f"{base_prompt}, photorealistic, 4k, cinematic lighting"
            elif image_provider == "midjourney":
                enhanced = f"{base_prompt} --ar 16:9 --v 6 --style raw"
            elif image_provider == "flux":
                enhanced = f"{base_prompt}, ultra detailed, professional photography"
            else:
                enhanced = base_prompt

            enhanced_prompts.append({
                "scene_id": scene.get("scene_id"),
                "original_prompt": base_prompt,
                "enhanced_prompt": enhanced,
                "provider": image_provider
            })

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"visual_prompts": enhanced_prompts}
        )

    async def _optimize_duration(self, task: AgentTask) -> AgentResult:
        """Optimise le script pour atteindre la durée cible"""
        script = task.input_data.get("script", {})
        target_duration = task.input_data.get("target_duration", 60)

        current_duration = sum(s.get("duration", 0) for s in script.get("scenes", []))
        difference = target_duration - current_duration

        optimizations = []
        if abs(difference) > 5:
            if difference > 0:
                optimizations.append("Ajouter des scènes de transition")
            else:
                optimizations.append("Réduire la durée des scènes de contenu")

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={
                "current_duration": current_duration,
                "target_duration": target_duration,
                "optimizations": optimizations
            }
        )

    async def _edit_script(self, task: AgentTask) -> AgentResult:
        """Édite le script selon les instructions de l'utilisateur"""
        script = task.input_data.get("script", {})
        edit_instructions = task.input_data.get("instructions", "")

        # TODO: Utiliser LLM pour appliquer les modifications
        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"script": script, "edited": True}
        )

    async def _translate_script(self, task: AgentTask) -> AgentResult:
        """Traduit le script dans une autre langue"""
        script = task.input_data.get("script", {})
        target_language = task.input_data.get("target_language", "en")

        # TODO: Utiliser LLM pour la traduction
        translated_script = script.copy()
        translated_script["language"] = target_language

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={
                "script": translated_script,
                "source_language": script.get("language", "fr"),
                "target_language": target_language
            }
        )
