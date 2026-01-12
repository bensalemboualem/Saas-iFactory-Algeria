"""
Story Co-Pilot Agent
Transforme une idée brute en script structuré avec support Darija
Inspiré de MovieFlow.ai
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from anthropic import Anthropic
import os
import json


class Scene(BaseModel):
    """Représente une scène du script"""
    number: int
    title: str
    description: str
    dialogue: Optional[str] = None
    language: str = "fr"  # fr, ar, darija
    visual_description: str
    location: str
    time_of_day: str  # morning, afternoon, evening, night
    characters: List[str] = []
    duration_seconds: int = 30


class Script(BaseModel):
    """Script complet structuré"""
    title: str
    logline: str  # Pitch en une ligne
    genre: str
    target_duration_minutes: int = 5
    language: str = "fr"
    scenes: List[Scene] = []
    characters: List[Dict[str, str]] = []  # [{name, description, role}]

    def total_duration(self) -> int:
        """Durée totale en secondes"""
        return sum(scene.duration_seconds for scene in self.scenes)


class StoryCopilot:
    """
    AI Story Co-Pilot - Transforme idée → script détaillé

    Fonctionnalités:
    - Chat interactif pour affiner l'histoire
    - Support multilingue (FR/AR/Darija)
    - Structure en 3 actes
    - Génération personnages
    - Découpage scènes automatique
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=self.api_key)
        self.conversation_history = []

    async def chat(self, user_message: str) -> str:
        """
        Conversation interactive pour développer l'histoire

        Args:
            user_message: Message de l'utilisateur

        Returns:
            Réponse du co-pilot
        """
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        system_prompt = """Tu es un Story Co-Pilot expert en scénarisation.
Tu aides les utilisateurs à transformer leurs idées en scripts de films courts (2-5 min).

Contexte spécial: Tu travailles pour IA Factory Algérie.
- Support natif du français, arabe et darija (dialecte algérien)
- Contexte culturel algérien/maghrébin important
- Films courts pour réseaux sociaux et YouTube

Ta mission:
1. Poser des questions pertinentes pour affiner l'histoire
2. Suggérer des améliorations narratives
3. Structurer en 3 actes (setup, confrontation, résolution)
4. Créer des personnages attachants
5. Adapter le ton/style selon le genre

Genres courants: comédie, drame, action, romance, horreur, sci-fi, documentaire.
"""

        response = self.client.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=2000,
            system=system_prompt,
            messages=self.conversation_history
        )

        assistant_message = response.content[0].text

        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    async def generate_script(
        self,
        user_idea: str,
        genre: str = "drame",
        duration_minutes: int = 5,
        language: str = "fr",
        context: Optional[Dict[str, Any]] = None
    ) -> Script:
        """
        Génère un script complet depuis une idée

        Args:
            user_idea: Idée de base (quelques mots ou paragraphe)
            genre: comédie, drame, action, romance, horreur, sci-fi
            duration_minutes: Durée cible en minutes
            language: fr, ar, darija
            context: Contexte additionnel (personnages, lieu, époque)

        Returns:
            Script structuré complet
        """

        # Construire le prompt
        context_str = json.dumps(context, ensure_ascii=False) if context else "Aucun"

        prompt = f"""Génère un script de film court basé sur cette idée:

IDÉE: {user_idea}

CONTRAINTES:
- Genre: {genre}
- Durée cible: {duration_minutes} minutes
- Langue principale: {language}
- Contexte additionnel: {context_str}

STRUCTURE REQUISE (JSON):
{{
  "title": "Titre accrocheur du film",
  "logline": "Pitch en une ligne (max 30 mots)",
  "genre": "{genre}",
  "target_duration_minutes": {duration_minutes},
  "language": "{language}",
  "characters": [
    {{
      "name": "Nom du personnage",
      "description": "Description physique et psychologique",
      "role": "protagonist|antagonist|supporting"
    }}
  ],
  "scenes": [
    {{
      "number": 1,
      "title": "Titre court de la scène",
      "description": "Description narrative de la scène",
      "dialogue": "Dialogues si applicable (optionnel)",
      "language": "{language}",
      "visual_description": "Description visuelle détaillée pour génération image/vidéo",
      "location": "Lieu précis (ex: Café moderne à Alger)",
      "time_of_day": "morning|afternoon|evening|night",
      "characters": ["Nom1", "Nom2"],
      "duration_seconds": 30
    }}
  ]
}}

CONSIGNES SPÉCIALES:
1. Structure en 3 actes:
   - Acte 1 (25%): Setup, introduction personnages, monde
   - Acte 2 (50%): Confrontation, obstacles, développement
   - Acte 3 (25%): Résolution, climax, conclusion

2. Pour la langue darija:
   - Écrire en caractères latins (ex: "Saha rak? Labess hamdoullah")
   - Mélanger français/arabe selon naturel de conversation

3. Descriptions visuelles:
   - Très détaillées pour génération IA
   - Mentionner: éclairage, couleurs, composition, mood

4. Durée réaliste:
   - Introduction: 10-20 secondes
   - Scène dialogue: 30-60 secondes
   - Scène action: 20-40 secondes
   - Conclusion: 15-30 secondes

5. Contexte algérien:
   - Lieux réalistes (Alger, Oran, Constantine, etc.)
   - Références culturelles pertinentes
   - Personnages crédibles

Génère le script complet en JSON valide:"""

        response = self.client.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=4000,
            temperature=0.8,  # Créativité élevée
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        # Parser la réponse JSON
        script_json = self._extract_json(response.content[0].text)

        # Valider avec Pydantic
        script = Script(**script_json)

        return script

    def _extract_json(self, text: str) -> dict:
        """Extrait JSON de la réponse (peut contenir du texte avant/après)"""
        import re

        # Chercher bloc JSON
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            return json.loads(json_str)
        else:
            # Fallback: supposer que tout le texte est JSON
            return json.loads(text)

    async def refine_script(
        self,
        script: Script,
        feedback: str
    ) -> Script:
        """
        Affine un script existant selon feedback utilisateur

        Args:
            script: Script à améliorer
            feedback: Retours utilisateur (ex: "Rendre Karim plus drôle")

        Returns:
            Script amélioré
        """

        prompt = f"""Améliore ce script selon le feedback utilisateur.

SCRIPT ACTUEL:
{script.model_dump_json(indent=2, ensure_ascii=False)}

FEEDBACK UTILISATEUR:
{feedback}

Génère le script amélioré en JSON (même structure):"""

        response = self.client.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=4000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        script_json = self._extract_json(response.content[0].text)
        refined_script = Script(**script_json)

        return refined_script

    def reset_conversation(self):
        """Réinitialise l'historique de conversation"""
        self.conversation_history = []


# Exemple d'utilisation
if __name__ == "__main__":
    import asyncio

    async def demo():
        copilot = StoryCopilot()

        # Exemple 1: Génération directe
        print("=== GÉNÉRATION SCRIPT ===\n")

        script = await copilot.generate_script(
            user_idea="Un jeune entrepreneur algérien lance sa startup tech à Alger mais fait face à des obstacles bureaucratiques",
            genre="drame",
            duration_minutes=5,
            language="darija",
            context={
                "époque": "2025",
                "lieu_principal": "Alger, quartier El Biar",
                "ton": "inspirant et réaliste"
            }
        )

        print(f"Titre: {script.title}")
        print(f"Logline: {script.logline}")
        print(f"Durée totale: {script.total_duration()}s")
        print(f"\nPersonnages ({len(script.characters)}):")
        for char in script.characters:
            print(f"  - {char['name']}: {char['description']}")

        print(f"\nScènes ({len(script.scenes)}):")
        for scene in script.scenes:
            print(f"  {scene.number}. {scene.title} ({scene.duration_seconds}s)")
            print(f"     Lieu: {scene.location} ({scene.time_of_day})")

        # Exemple 2: Conversation interactive
        print("\n\n=== CONVERSATION INTERACTIVE ===\n")

        copilot.reset_conversation()

        response1 = await copilot.chat(
            "Je veux faire un film sur l'amitié entre deux enfants à Oran"
        )
        print(f"Co-Pilot: {response1}\n")

        response2 = await copilot.chat(
            "Genre comédie, avec des situations drôles liées à l'école"
        )
        print(f"Co-Pilot: {response2}\n")

    asyncio.run(demo())
