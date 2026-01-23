"""
YouTube Shorts Script Optimizer
Uses AI to create viral, engaging scripts
"""

import os
import json
import requests
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class OptimizedScript:
    """Optimized script output"""
    hook: str  # First 3 seconds - must grab attention
    main_content: str  # Core message (30-45 seconds)
    cta: str  # Call to action (last 5 seconds)
    full_script: str  # Complete script
    title: str  # Optimized title
    description: str  # YouTube description
    tags: List[str]  # SEO tags
    viral_score: int  # Predicted viral score (0-100)
    improvements: List[str]  # Suggested improvements


class ScriptOptimizer:
    """AI-powered script optimization for YouTube Shorts"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize with Claude API key"""
        self.api_key = api_key or os.getenv("CLAUDE_API_KEY")
        self.api_url = "https://api.anthropic.com/v1/messages"

    def optimize_script(
        self,
        raw_idea: str,
        niche: str = "general",
        tone: str = "energetic",
        target_duration: int = 45
    ) -> OptimizedScript:
        """
        Transform raw idea into optimized YouTube Short script

        Args:
            raw_idea: Basic idea or topic
            niche: Content niche (tech, business, education, etc.)
            tone: Script tone (energetic, calm, professional, funny)
            target_duration: Target duration in seconds (30-60)

        Returns:
            OptimizedScript with all components
        """

        # Create optimization prompt
        prompt = self._build_optimization_prompt(
            raw_idea, niche, tone, target_duration
        )

        # Call Claude API
        if self.api_key:
            result = self._call_claude_api(prompt)
        else:
            # Fallback: rule-based optimization
            result = self._fallback_optimization(raw_idea, niche, tone)

        return self._parse_result(result, raw_idea)

    def _build_optimization_prompt(
        self,
        raw_idea: str,
        niche: str,
        tone: str,
        target_duration: int
    ) -> str:
        """Build optimized prompt for Claude"""

        return f"""Tu es un expert en création de YouTube Shorts viraux.

CONTEXTE:
- Niche: {niche}
- Tone: {tone}
- Durée cible: {target_duration} secondes
- Idée de base: {raw_idea}

MISSION:
Transforme cette idée en script YouTube Short optimisé qui:
1. ACCROCHE dans les 3 premières secondes (hook viral)
2. RETIENT l'attention jusqu'à la fin
3. INCITE à l'action (like, follow, comment)

STRUCTURE OBLIGATOIRE:

**HOOK (3 secondes):**
- Question choc, statistique surprenante, ou affirmation provocante
- Doit donner envie de continuer
- Exemples: "Si tu penses que...", "90% des gens ignorent que...", "La vérité sur..."

**CONTENU PRINCIPAL ({target_duration - 8} secondes):**
- 3-5 points clés maximum
- Phrases courtes et percutantes
- Utilise des nombres, des exemples concrets
- Rythme rapide, pas de temps mort

**CALL TO ACTION (5 secondes):**
- Incitation claire (like, follow, comment)
- Promesse de valeur future
- Créer l'urgence ou la curiosité

OPTIMISATIONS SEO:
- Titre accrocheur (max 60 caractères)
- Description avec mots-clés
- 10-15 tags pertinents

FORMAT DE RÉPONSE (JSON strict):
{{
  "hook": "...",
  "main_content": "...",
  "cta": "...",
  "full_script": "...",
  "title": "...",
  "description": "...",
  "tags": ["tag1", "tag2", ...],
  "viral_score": 85,
  "improvements": ["conseil 1", "conseil 2", ...]
}}

GÉNÈRE MAINTENANT LE SCRIPT OPTIMISÉ:"""

    def _call_claude_api(self, prompt: str) -> Dict:
        """Call Claude API for script optimization"""

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        payload = {
            "model": "claude-sonnet-4-5-20250929",
            "max_tokens": 2048,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()

            # Extract text content
            result = response.json()
            text = result["content"][0]["text"]

            # Parse JSON from response
            # Claude might wrap JSON in markdown code blocks
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]

            return json.loads(text.strip())

        except Exception as e:
            print(f"Claude API error: {e}")
            # Fallback to rule-based
            return None

    def _fallback_optimization(
        self,
        raw_idea: str,
        niche: str,
        tone: str
    ) -> Dict:
        """Rule-based optimization when API unavailable"""

        # Simple hook templates
        hooks = {
            "tech": f"🚀 La vérité sur {raw_idea} que personne ne te dit...",
            "business": f"💰 Comment {raw_idea} peut changer ta vie en 2025",
            "education": f"📚 Si tu penses que {raw_idea}, tu te trompes.",
            "general": f"⚡ {raw_idea}: voici ce que tu dois savoir MAINTENANT"
        }

        hook = hooks.get(niche, hooks["general"])

        # Basic structure
        main_content = f"{raw_idea}. Voici les 3 choses essentielles à retenir pour réussir. Reste jusqu'à la fin pour le dernier conseil qui change tout."

        cta = "❤️ Like si c'est utile, Follow pour plus de contenu comme ça, et dis-moi en commentaire ce que tu veux voir ensuite!"

        full_script = f"{hook} {main_content} {cta}"

        # Generate title
        title = f"{raw_idea} - Ce que tu dois savoir"[:60]

        return {
            "hook": hook,
            "main_content": main_content,
            "cta": cta,
            "full_script": full_script,
            "title": title,
            "description": f"Tout sur {raw_idea}. {niche.title()} | Tips et conseils",
            "tags": [raw_idea.lower(), niche, "2025", "france", "algerie", "shorts"],
            "viral_score": 65,
            "improvements": [
                "Ajoute des chiffres concrets pour plus d'impact",
                "Utilise plus d'émojis pour capter l'attention",
                "Raccourcis les phrases pour un rythme plus dynamique"
            ]
        }

    def _parse_result(self, result: Dict, raw_idea: str) -> OptimizedScript:
        """Parse API result into OptimizedScript"""

        if not result:
            # Create minimal script from raw idea
            result = self._fallback_optimization(raw_idea, "general", "energetic")

        return OptimizedScript(
            hook=result.get("hook", ""),
            main_content=result.get("main_content", ""),
            cta=result.get("cta", ""),
            full_script=result.get("full_script", ""),
            title=result.get("title", ""),
            description=result.get("description", ""),
            tags=result.get("tags", []),
            viral_score=result.get("viral_score", 50),
            improvements=result.get("improvements", [])
        )

    def analyze_script(self, script: str) -> Dict:
        """
        Analyze existing script and provide optimization suggestions

        Returns:
            Dict with analysis and suggestions
        """

        word_count = len(script.split())
        char_count = len(script)

        # Rough duration estimate (150 words per minute for French)
        estimated_duration = (word_count / 150) * 60

        # Check for hook indicators
        has_hook = any(
            indicator in script.lower()
            for indicator in ["?", "si tu", "saviez-vous", "90%", "vérité"]
        )

        # Check for CTA
        has_cta = any(
            cta in script.lower()
            for cta in ["like", "follow", "commentaire", "abonne"]
        )

        # Viral score calculation
        score = 50  # Base score
        if has_hook:
            score += 15
        if has_cta:
            score += 10
        if 30 <= estimated_duration <= 60:
            score += 15
        if word_count < 100:
            score += 10

        return {
            "word_count": word_count,
            "char_count": char_count,
            "estimated_duration": round(estimated_duration, 1),
            "has_hook": has_hook,
            "has_cta": has_cta,
            "viral_score": min(score, 100),
            "suggestions": self._generate_suggestions(
                script, has_hook, has_cta, estimated_duration
            )
        }

    def _generate_suggestions(
        self,
        script: str,
        has_hook: bool,
        has_cta: bool,
        duration: float
    ) -> List[str]:
        """Generate improvement suggestions"""

        suggestions = []

        if not has_hook:
            suggestions.append("❌ Ajoute un HOOK accrocheur dans les 3 premières secondes")

        if not has_cta:
            suggestions.append("❌ Manque un appel à l'action (like, follow, comment)")

        if duration > 60:
            suggestions.append(f"⚠️ Script trop long ({duration:.0f}s). Vise 45-60 secondes max.")
        elif duration < 30:
            suggestions.append(f"⚠️ Script trop court ({duration:.0f}s). Ajoute plus de contenu.")

        if "?" not in script:
            suggestions.append("💡 Ajoute une question pour engager l'audience")

        emoji_count = sum(1 for char in script if ord(char) > 127000)
        if emoji_count < 3:
            suggestions.append("💡 Utilise plus d'émojis pour un impact visuel")

        return suggestions if suggestions else ["✅ Script bien structuré !"]


# Example usage
if __name__ == "__main__":
    optimizer = ScriptOptimizer()

    # Test optimization
    result = optimizer.optimize_script(
        raw_idea="L'IA va remplacer les développeurs",
        niche="tech",
        tone="energetic",
        target_duration=45
    )

    print("HOOK:", result.hook)
    print("\nSCRIPT COMPLET:", result.full_script)
    print("\nTITLE:", result.title)
    print("\nVIRAL SCORE:", result.viral_score)
    print("\nAMÉLIORATIONS:", "\n- ".join(result.improvements))
