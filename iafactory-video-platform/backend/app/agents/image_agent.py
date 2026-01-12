"""
Image Agent - Génération d'images avec multiples providers IA
"""
from typing import List, Dict, Any, Optional
from app.agents.base import BaseAgent, AgentTask, AgentResult
from app.core.config import settings
import asyncio


class ImageAgent(BaseAgent):
    """
    Agent de génération d'images.

    Providers supportés:
    - DALL-E 3 (OpenAI)
    - Stable Diffusion (Stability AI)
    - Flux (Replicate/FAL)
    - Leonardo AI
    - Ideogram
    - Midjourney (via API non-officielle)

    Responsabilités:
    - Génère des images à partir de prompts
    - Optimise les prompts selon le provider
    - Gère le upscaling et les variations
    - Sélectionne le meilleur provider selon le style
    """

    @property
    def agent_type(self) -> str:
        return "image"

    @property
    def capabilities(self) -> List[str]:
        return [
            "generate_image",
            "generate_batch",
            "upscale_image",
            "create_variations",
            "edit_image",
            "remove_background",
            "optimize_prompt"
        ]

    # Mapping provider -> coût approximatif en centimes
    PROVIDER_COSTS = {
        "dalle": 4,      # $0.04 par image
        "flux": 2,       # $0.02 par image
        "sdxl": 1,       # $0.01 par image
        "leonardo": 2,   # $0.02 par image
        "ideogram": 3,   # $0.03 par image
        "midjourney": 5  # $0.05 par image (estimation)
    }

    def __init__(self, default_provider: str = None):
        super().__init__()
        self.default_provider = default_provider or settings.DEFAULT_IMAGE_PROVIDER

    async def _execute_task(self, task: AgentTask) -> AgentResult:
        """Exécute une tâche de génération d'image"""

        handlers = {
            "generate_image": self._generate_single_image,
            "generate_batch": self._generate_batch,
            "upscale_image": self._upscale_image,
            "create_variations": self._create_variations,
            "edit_image": self._edit_image,
            "remove_background": self._remove_background,
            "optimize_prompt": self._optimize_prompt,
        }

        handler = handlers.get(task.task_type)
        return await handler(task)

    async def _generate_single_image(self, task: AgentTask) -> AgentResult:
        """Génère une seule image"""
        prompt = task.input_data.get("prompt", "")
        provider = task.input_data.get("provider", self.default_provider)
        size = task.input_data.get("size", "1024x1024")
        style = task.input_data.get("style", None)

        # Optimisation du prompt selon le provider
        optimized_prompt = self._optimize_prompt_for_provider(prompt, provider, style)

        # TODO: Appel réel à l'API du provider
        # Pour le moment, simulation
        image_result = {
            "image_id": f"img_{task.task_id[:8]}",
            "prompt": optimized_prompt,
            "provider": provider,
            "size": size,
            "url": f"https://placeholder.com/{size}",  # URL temporaire
            "local_path": None,
            "generation_params": {
                "prompt": optimized_prompt,
                "size": size,
                "style": style,
                "provider": provider
            }
        }

        cost = self.PROVIDER_COSTS.get(provider, 3)

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"image": image_result},
            cost_cents=cost
        )

    async def _generate_batch(self, task: AgentTask) -> AgentResult:
        """Génère plusieurs images en parallèle"""
        prompts = task.input_data.get("prompts", [])
        provider = task.input_data.get("provider", self.default_provider)
        size = task.input_data.get("size", "1024x1024")

        if not prompts:
            return AgentResult(
                task_id=task.task_id,
                success=False,
                error_message="No prompts provided"
            )

        # Génération en parallèle
        tasks = []
        for i, prompt in enumerate(prompts):
            sub_task = AgentTask(
                task_type="generate_image",
                input_data={
                    "prompt": prompt,
                    "provider": provider,
                    "size": size
                }
            )
            tasks.append(self._generate_single_image(sub_task))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        images = []
        total_cost = 0
        errors = []

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                errors.append(f"Image {i}: {str(result)}")
            elif result.success:
                images.append(result.output_data.get("image"))
                total_cost += result.cost_cents
            else:
                errors.append(f"Image {i}: {result.error_message}")

        return AgentResult(
            task_id=task.task_id,
            success=len(images) > 0,
            output_data={
                "images": images,
                "total_generated": len(images),
                "errors": errors if errors else None
            },
            cost_cents=total_cost
        )

    async def _upscale_image(self, task: AgentTask) -> AgentResult:
        """Upscale une image existante"""
        image_path = task.input_data.get("image_path")
        scale = task.input_data.get("scale", 2)  # 2x, 4x

        # TODO: Intégration Real-ESRGAN ou autre upscaler
        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={
                "upscaled_path": f"{image_path}_upscaled_{scale}x",
                "scale": scale
            },
            cost_cents=1
        )

    async def _create_variations(self, task: AgentTask) -> AgentResult:
        """Crée des variations d'une image existante"""
        image_path = task.input_data.get("image_path")
        num_variations = task.input_data.get("num_variations", 3)
        provider = task.input_data.get("provider", "dalle")

        # TODO: Appel API pour variations
        variations = [
            {"variation_id": f"var_{i}", "path": f"{image_path}_var{i}"}
            for i in range(num_variations)
        ]

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"variations": variations},
            cost_cents=num_variations * self.PROVIDER_COSTS.get(provider, 3)
        )

    async def _edit_image(self, task: AgentTask) -> AgentResult:
        """Édite une image avec un masque et un prompt"""
        image_path = task.input_data.get("image_path")
        mask_path = task.input_data.get("mask_path")
        edit_prompt = task.input_data.get("prompt", "")

        # TODO: Intégration DALL-E edit ou Stable Diffusion inpainting
        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"edited_path": f"{image_path}_edited"},
            cost_cents=5
        )

    async def _remove_background(self, task: AgentTask) -> AgentResult:
        """Supprime le fond d'une image"""
        image_path = task.input_data.get("image_path")

        # TODO: Intégration rembg ou API remove.bg
        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={"transparent_path": f"{image_path}_nobg.png"},
            cost_cents=1
        )

    async def _optimize_prompt(self, task: AgentTask) -> AgentResult:
        """Optimise un prompt pour un provider spécifique"""
        prompt = task.input_data.get("prompt", "")
        provider = task.input_data.get("provider", self.default_provider)
        style = task.input_data.get("style", None)

        optimized = self._optimize_prompt_for_provider(prompt, provider, style)

        return AgentResult(
            task_id=task.task_id,
            success=True,
            output_data={
                "original_prompt": prompt,
                "optimized_prompt": optimized,
                "provider": provider
            }
        )

    def _optimize_prompt_for_provider(
        self,
        prompt: str,
        provider: str,
        style: Optional[str] = None
    ) -> str:
        """Optimise le prompt selon le provider"""

        base_prompt = prompt.strip()

        # Ajout du style si spécifié
        if style:
            base_prompt = f"{base_prompt}, {style} style"

        if provider == "dalle":
            # DALL-E préfère les descriptions détaillées et naturelles
            return f"{base_prompt}, high quality, detailed, professional photography"

        elif provider == "flux":
            # Flux (via Replicate/FAL)
            return f"{base_prompt}, ultra realistic, 8k, sharp focus"

        elif provider == "sdxl":
            # Stable Diffusion XL
            return f"{base_prompt}, masterpiece, best quality, highly detailed"

        elif provider == "leonardo":
            # Leonardo AI
            return f"{base_prompt}, cinematic, dramatic lighting, 4k resolution"

        elif provider == "ideogram":
            # Ideogram (bon pour le texte)
            return f"{base_prompt}, clean design, professional"

        elif provider == "midjourney":
            # Midjourney style
            return f"{base_prompt} --ar 16:9 --v 6 --quality 2"

        return base_prompt

    def get_best_provider_for_style(self, style: str) -> str:
        """Recommande le meilleur provider selon le style"""
        style_mapping = {
            "photorealistic": "flux",
            "artistic": "midjourney",
            "corporate": "dalle",
            "animated": "leonardo",
            "text_heavy": "ideogram",
            "cinematic": "dalle",
            "minimalist": "dalle",
            "fantasy": "midjourney",
            "product": "flux"
        }
        return style_mapping.get(style.lower(), self.default_provider)
