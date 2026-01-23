"""
Character Design Service
Génération de personnages consistants avec multiple poses de référence
Inspiré de MovieFlow.ai
"""

from typing import Optional, List, Dict
from pydantic import BaseModel, Field
import httpx
import os
import hashlib


class Character(BaseModel):
    """Personnage avec références visuelles multiples"""
    name: str
    description: str
    style: str = "realistic"  # realistic, anime, cartoon, 3d, sketch
    role: str = "supporting"  # protagonist, antagonist, supporting
    age: Optional[int] = None
    gender: Optional[str] = None
    ethnicity: str = "algerian"  # Pour personnages locaux

    # Références visuelles (6 angles)
    reference_images: Dict[str, str] = {}  # {angle: image_url}

    # Consistance
    seed: int = Field(default_factory=lambda: int.from_bytes(os.urandom(4), 'little'))
    character_id: str = ""

    # Détails visuels
    clothing: Optional[str] = None
    hair: Optional[str] = None
    distinctive_features: Optional[str] = None


class CharacterDesignService:
    """
    Service de génération de personnages consistants

    Utilise Fal.ai FLUX pour générer des character sheets
    avec multiples angles pour assurer consistance visuelle
    """

    REFERENCE_ANGLES = [
        "front_view",
        "side_view",
        "three_quarter_view",
        "back_view",
        "close_up_face",
        "full_body"
    ]

    STYLE_PRESETS = {
        "realistic": "photorealistic, highly detailed, 8k resolution, cinematic lighting",
        "anime": "anime style, cel shaded, vibrant colors, manga aesthetics",
        "cartoon": "cartoon style, cel animation, simplified features, expressive",
        "3d": "3D render, Pixar style, smooth surfaces, professional lighting",
        "sketch": "pencil sketch, character design sheet, clean lines, professional concept art",
        "algerian_traditional": "traditional Algerian clothing, realistic, cultural authenticity, detailed patterns"
    }

    def __init__(self, fal_api_key: Optional[str] = None):
        self.fal_api_key = fal_api_key or os.getenv("FAL_KEY")
        self.base_url = "https://queue.fal.run/fal-ai/flux-pro/v1.1"

    async def create_character(
        self,
        name: str,
        description: str,
        style: str = "realistic",
        role: str = "supporting",
        context: Optional[Dict] = None
    ) -> Character:
        """
        Crée un personnage complet avec références visuelles

        Args:
            name: Nom du personnage
            description: Description physique et psychologique
            style: Style visuel (realistic, anime, cartoon, etc.)
            role: Rôle narratif
            context: Contexte additionnel (époque, lieu, etc.)

        Returns:
            Character avec toutes les références générées
        """

        # Générer ID unique basé sur nom + description
        char_id = hashlib.md5(f"{name}{description}".encode()).hexdigest()[:12]

        # Créer le personnage
        character = Character(
            name=name,
            description=description,
            style=style,
            role=role,
            character_id=char_id
        )

        # Extraire détails du contexte
        if context:
            character.age = context.get("age")
            character.gender = context.get("gender")
            character.ethnicity = context.get("ethnicity", "algerian")
            character.clothing = context.get("clothing")
            character.hair = context.get("hair")
            character.distinctive_features = context.get("distinctive_features")

        # Générer les 6 vues de référence
        print(f"Génération du character sheet pour {name}...")

        for angle in self.REFERENCE_ANGLES:
            image_url = await self._generate_reference_image(
                character=character,
                angle=angle
            )
            character.reference_images[angle] = image_url
            print(f"  ✓ {angle}: {image_url}")

        return character

    async def _generate_reference_image(
        self,
        character: Character,
        angle: str
    ) -> str:
        """
        Génère une image de référence pour un angle spécifique

        Args:
            character: Personnage
            angle: Angle de vue

        Returns:
            URL de l'image générée
        """

        # Construire le prompt
        base_prompt = self._build_character_prompt(character)
        angle_description = self._get_angle_description(angle)
        style_preset = self.STYLE_PRESETS.get(character.style, "")

        full_prompt = f"""{base_prompt}

{angle_description}

{style_preset}

Character reference sheet, white background, professional character design, consistent appearance"""

        # Appeler Fal.ai
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                headers={
                    "Authorization": f"Key {self.fal_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "prompt": full_prompt,
                    "image_size": "portrait_4_3",
                    "num_inference_steps": 28,
                    "seed": character.seed,  # Même seed = consistance
                    "guidance_scale": 3.5,
                    "num_images": 1,
                    "enable_safety_checker": True
                },
                timeout=60.0
            )

            result = response.json()

            # Extraire URL image
            if "images" in result and len(result["images"]) > 0:
                return result["images"][0]["url"]
            else:
                raise Exception(f"Erreur génération image: {result}")

    def _build_character_prompt(self, character: Character) -> str:
        """Construit le prompt de base du personnage"""

        parts = [
            f"Character: {character.name}",
            f"Description: {character.description}"
        ]

        if character.age:
            parts.append(f"{character.age} years old")

        if character.gender:
            parts.append(f"{character.gender}")

        if character.ethnicity and character.ethnicity != "unspecified":
            parts.append(f"{character.ethnicity} ethnicity")

        if character.clothing:
            parts.append(f"Wearing: {character.clothing}")

        if character.hair:
            parts.append(f"Hair: {character.hair}")

        if character.distinctive_features:
            parts.append(f"Distinctive features: {character.distinctive_features}")

        return ", ".join(parts)

    def _get_angle_description(self, angle: str) -> str:
        """Description technique de chaque angle"""

        descriptions = {
            "front_view": "front view, facing camera directly, neutral expression, symmetrical pose",
            "side_view": "side profile view, 90 degrees, full side silhouette",
            "three_quarter_view": "three-quarter view, 45 degrees angle, showing depth",
            "back_view": "back view, rear profile, showing back details",
            "close_up_face": "close-up portrait, facial details, head and shoulders only",
            "full_body": "full body shot, standing pose, showing complete figure from head to toe"
        }

        return descriptions.get(angle, "")

    async def generate_scene_with_character(
        self,
        character: Character,
        scene_description: str,
        angle: str = "three_quarter_view"
    ) -> str:
        """
        Génère une scène avec le personnage
        Utilise les références pour maintenir consistance

        Args:
            character: Personnage à utiliser
            scene_description: Description de la scène
            angle: Angle de référence à utiliser

        Returns:
            URL de la vidéo/image générée
        """

        # Récupérer l'image de référence
        reference_image = character.reference_images.get(angle)

        if not reference_image:
            raise ValueError(f"Pas de référence pour angle {angle}")

        # Construire prompt avec référence
        prompt = f"""{scene_description}

Character reference: {character.name} - maintain exact appearance from reference
{self._build_character_prompt(character)}

Style: {character.style}
Maintain consistency with character design"""

        # TODO: Implémenter génération vidéo avec character reference
        # Utiliser Fal.ai ou autre service qui supporte image reference

        return "VIDEO_URL_HERE"

    def save_character_sheet(
        self,
        character: Character,
        output_path: str
    ):
        """
        Sauvegarde la fiche personnage en JSON

        Args:
            character: Personnage
            output_path: Chemin du fichier JSON
        """
        import json

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(
                character.model_dump(),
                f,
                indent=2,
                ensure_ascii=False
            )

        print(f"✓ Character sheet sauvegardé: {output_path}")

    @classmethod
    def load_character_sheet(cls, json_path: str) -> Character:
        """
        Charge une fiche personnage depuis JSON

        Args:
            json_path: Chemin du fichier JSON

        Returns:
            Character
        """
        import json

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return Character(**data)


# Exemple d'utilisation
if __name__ == "__main__":
    import asyncio

    async def demo():
        service = CharacterDesignService()

        # Créer un personnage algérien réaliste
        character = await service.create_character(
            name="Karim Benali",
            description="Jeune entrepreneur algérien de 28 ans, passionné de technologie, portant des vêtements modernes",
            style="realistic",
            role="protagonist",
            context={
                "age": 28,
                "gender": "male",
                "ethnicity": "algerian",
                "clothing": "smart casual, jeans and blazer",
                "hair": "short black hair, well-groomed beard",
                "distinctive_features": "warm smile, confident posture"
            }
        )

        print(f"\n✓ Personnage créé: {character.name}")
        print(f"  ID: {character.character_id}")
        print(f"  Style: {character.style}")
        print(f"  Seed: {character.seed}")
        print(f"  Références générées: {len(character.reference_images)}")

        # Sauvegarder
        service.save_character_sheet(character, "karim_benali.json")

        # Charger
        loaded = CharacterDesignService.load_character_sheet("karim_benali.json")
        print(f"\n✓ Personnage rechargé: {loaded.name}")

    # asyncio.run(demo())
    print("Demo CharacterDesignService - Décommenter asyncio.run(demo()) pour tester")
