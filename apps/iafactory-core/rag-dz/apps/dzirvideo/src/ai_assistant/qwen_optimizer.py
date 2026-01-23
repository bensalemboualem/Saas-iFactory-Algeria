"""
Qwen 2.1 Script Optimizer for Dzir IA Video
Alternative gratuite à Claude API pour l'optimisation de scripts YouTube Shorts
Utilise Alibaba Qwen-max (gratuit via DashScope)
"""

import os
import logging
from typing import Optional, List
from dataclasses import dataclass

try:
    import dashscope
    from dashscope import Generation
    DASHSCOPE_AVAILABLE = True
except ImportError:
    DASHSCOPE_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class OptimizedScript:
    """Script optimisé avec métadonnées"""
    hook: str  # Hook accrocheur (3 premières secondes)
    main_content: str  # Contenu principal
    cta: str  # Call-to-action
    full_script: str  # Script complet
    title: str  # Titre optimisé SEO
    description: str  # Description YouTube
    tags: List[str]  # Tags SEO
    viral_score: int  # Score viral prédit (0-100)
    improvements: List[str]  # Suggestions d'amélioration


class QwenOptimizer:
    """
    Optimiseur de scripts utilisant Qwen 2.1 (Alibaba)

    Avantages vs Claude:
    - Gratuit (quota généreux)
    - Rapide (2-5 secondes)
    - Multilingue natif (FR/AR/EN)
    - Optimisé pour contenu court
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialiser l'optimiseur

        Args:
            api_key: Clé API DashScope (ou ALIBABA_DASHSCOPE_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("ALIBABA_DASHSCOPE_API_KEY")

        if not DASHSCOPE_AVAILABLE:
            logger.warning(
                "dashscope package not installed. Install with: pip install dashscope"
            )
            self.enabled = False
        elif not self.api_key:
            logger.warning(
                "No Alibaba DashScope API key provided. "
                "Set ALIBABA_DASHSCOPE_API_KEY or pass api_key parameter."
            )
            self.enabled = False
        else:
            dashscope.api_key = self.api_key
            self.enabled = True
            logger.info("Qwen Optimizer initialized successfully")

    def optimize_script(
        self,
        raw_idea: str,
        niche: str = "general",
        tone: str = "energetic",
        target_duration: int = 45,
        language: str = "fr"
    ) -> OptimizedScript:
        """
        Optimiser une idée brute en script viral YouTube Short

        Args:
            raw_idea: Idée de base (ex: "Comment l'IA va changer le monde")
            niche: Niche (tech, business, education, motivation)
            tone: Ton (energetic, calm, professional, funny)
            target_duration: Durée cible en secondes
            language: Langue (fr, ar, en)

        Returns:
            OptimizedScript avec hook, contenu, CTA, metadata
        """
        if not self.enabled:
            return self._fallback_optimization(raw_idea, niche, tone, target_duration)

        try:
            # Construire le prompt d'optimisation
            prompt = self._build_optimization_prompt(
                raw_idea, niche, tone, target_duration, language
            )

            # Appel API Qwen
            response = Generation.call(
                model="qwen-max",  # Ou qwen-plus pour + rapide
                prompt=prompt,
                temperature=0.7,
                top_p=0.8,
                max_tokens=1000
            )

            if response.status_code == 200:
                result_text = response.output.text
                return self._parse_result(result_text, raw_idea)
            else:
                logger.error(f"Qwen API error: {response.code} - {response.message}")
                return self._fallback_optimization(raw_idea, niche, tone, target_duration)

        except Exception as e:
            logger.error(f"Error calling Qwen API: {e}")
            return self._fallback_optimization(raw_idea, niche, tone, target_duration)

    def _build_optimization_prompt(
        self,
        raw_idea: str,
        niche: str,
        tone: str,
        target_duration: int,
        language: str
    ) -> str:
        """Construire le prompt d'optimisation pour Qwen"""

        language_map = {
            "fr": "français",
            "ar": "arabe",
            "en": "anglais"
        }
        lang_name = language_map.get(language, "français")

        niche_examples = {
            "tech": "IA, développement, startups tech",
            "business": "entrepreneuriat, marketing, ventes",
            "education": "apprentissage, productivité, compétences",
            "motivation": "mindset, success stories, inspiration"
        }
        niche_context = niche_examples.get(niche, "contenu général")

        prompt = f"""Tu es un expert en création de YouTube Shorts viraux en {lang_name}.
Transforme cette idée en script optimisé pour un Short de {target_duration} secondes.

IDÉE BRUTE:
{raw_idea}

CONTEXTE:
- Niche: {niche} ({niche_context})
- Ton: {tone}
- Durée: {target_duration} secondes
- Langue: {lang_name}

STRUCTURE REQUISE:

1. HOOK (3 premières secondes - CRUCIAL):
   - Phrase choc qui stoppe le scroll
   - Question provocante OU affirmation surprenante
   - Max 10 mots

2. CONTENU PRINCIPAL ({target_duration - 8} secondes):
   - 3 points clés maximum
   - Phrases courtes et percutantes
   - Exemples concrets si possible
   - Langage simple et direct

3. CALL-TO-ACTION (5 dernières secondes):
   - Incitation claire (like, abonne-toi, commente)
   - Création d'urgence ou curiosité

MÉTADONNÉES:

4. TITRE (max 60 caractères):
   - Mots-clés SEO
   - Émoji pertinent
   - Clickable mais pas clickbait

5. DESCRIPTION (100-150 caractères):
   - Résumé avec keywords
   - CTA supplémentaire

6. TAGS (10-15 tags):
   - Mix de tags génériques et spécifiques
   - Keywords en {lang_name}

7. SCORE VIRAL (0-100):
   - Évalue le potentiel viral selon:
     * Hook strength (30%)
     * Engagement potential (30%)
     * Share-ability (20%)
     * Niche fit (20%)

8. AMÉLIORATIONS:
   - 2-3 suggestions pour renforcer l'impact

FORMAT DE SORTIE (STRICT):
---
HOOK:
[ton hook de 3 secondes]

CONTENU:
[ton contenu principal]

CTA:
[ton call-to-action]

TITRE:
[titre optimisé]

DESCRIPTION:
[description SEO]

TAGS:
tag1, tag2, tag3, ...

SCORE:
[nombre entre 0-100]

AMÉLIORATIONS:
- [amélioration 1]
- [amélioration 2]
- [amélioration 3]
---

Génère maintenant le script optimisé."""

        return prompt

    def _parse_result(self, result_text: str, raw_idea: str) -> OptimizedScript:
        """Parser la réponse de Qwen"""

        # Extraction basique (parsing du format structuré)
        lines = result_text.strip().split("\n")

        hook = ""
        main_content = ""
        cta = ""
        title = ""
        description = ""
        tags = []
        viral_score = 75  # Default
        improvements = []

        current_section = None

        for line in lines:
            line = line.strip()

            if line.startswith("HOOK:"):
                current_section = "hook"
                hook = line.replace("HOOK:", "").strip()
            elif line.startswith("CONTENU:"):
                current_section = "content"
                main_content = line.replace("CONTENU:", "").strip()
            elif line.startswith("CTA:"):
                current_section = "cta"
                cta = line.replace("CTA:", "").strip()
            elif line.startswith("TITRE:"):
                current_section = "title"
                title = line.replace("TITRE:", "").strip()
            elif line.startswith("DESCRIPTION:"):
                current_section = "description"
                description = line.replace("DESCRIPTION:", "").strip()
            elif line.startswith("TAGS:"):
                current_section = "tags"
                tags_str = line.replace("TAGS:", "").strip()
                tags = [t.strip() for t in tags_str.split(",") if t.strip()]
            elif line.startswith("SCORE:"):
                current_section = "score"
                try:
                    viral_score = int(line.replace("SCORE:", "").strip())
                except:
                    viral_score = 75
            elif line.startswith("AMÉLIORATIONS:") or line.startswith("AMELIORATIONS:"):
                current_section = "improvements"
            elif line.startswith("-") and current_section == "improvements":
                improvements.append(line.replace("-", "").strip())
            elif line and current_section:
                # Continuer la section courante
                if current_section == "hook" and not line.startswith("---"):
                    hook += " " + line
                elif current_section == "content" and not line.startswith("---"):
                    main_content += " " + line
                elif current_section == "cta" and not line.startswith("---"):
                    cta += " " + line

        # Construire le script complet
        full_script = f"{hook}\n\n{main_content}\n\n{cta}"

        # Fallbacks si parsing échoué
        if not hook:
            hook = raw_idea[:50] + "..."
        if not title:
            title = raw_idea[:60]
        if not tags:
            tags = ["youtube", "shorts", "viral"]

        return OptimizedScript(
            hook=hook.strip(),
            main_content=main_content.strip(),
            cta=cta.strip(),
            full_script=full_script.strip(),
            title=title.strip(),
            description=description.strip(),
            tags=tags,
            viral_score=viral_score,
            improvements=improvements
        )

    def _fallback_optimization(
        self,
        raw_idea: str,
        niche: str,
        tone: str,
        target_duration: int
    ) -> OptimizedScript:
        """
        Mode fallback avec règles prédéfinies (si API indisponible)
        """
        logger.info("Using fallback optimization (rule-based)")

        # Hooks génériques selon la niche
        hooks = {
            "tech": f"⚡ Vous ne croirez pas ce que l'IA peut faire maintenant !",
            "business": f"💰 Ce secret a généré 100K€ en 30 jours",
            "education": f"🎓 La méthode que les profs cachent",
            "motivation": f"🔥 Si tu ne fais pas ça, tu le regretteras"
        }

        hook = hooks.get(niche, f"🚀 {raw_idea[:40]}...")

        # CTA génériques
        ctas = {
            "energetic": "👉 Like si tu veux la suite ! Abonne-toi pour plus !",
            "calm": "Si ça t'a plu, n'oublie pas de t'abonner 🙏",
            "professional": "Pour plus de conseils, abonne-toi à la chaîne.",
            "funny": "T'as kiffé ? Smash ce like ! 😂"
        }

        cta = ctas.get(tone, "Abonne-toi pour plus de contenu !")

        # Contenu basique
        main_content = raw_idea

        # Titre
        title = f"{raw_idea[:50]}..."

        # Tags
        tags = [niche, "youtube", "shorts", "viral", "2025"]

        return OptimizedScript(
            hook=hook,
            main_content=main_content,
            cta=cta,
            full_script=f"{hook}\n\n{main_content}\n\n{cta}",
            title=title,
            description=f"{raw_idea[:100]}...",
            tags=tags,
            viral_score=65,  # Score moyen pour fallback
            improvements=[
                "Ajouter des exemples concrets",
                "Rendre le hook plus percutant",
                "Ajouter des émojis pour engagement"
            ]
        )

    def analyze_script(self, script: str) -> dict:
        """
        Analyser un script existant

        Args:
            script: Script à analyser

        Returns:
            Analyse complète avec métriques
        """
        words = script.split()
        chars = len(script)

        # Estimation durée (150 mots/min en français)
        estimated_duration = (len(words) / 150) * 60

        # Détection hook (3 premières lignes)
        lines = script.split("\n")
        hook_candidate = lines[0] if lines else ""
        has_hook = len(hook_candidate) < 100 and ("?" in hook_candidate or "!" in hook_candidate)

        # Détection CTA
        cta_keywords = ["abonne", "like", "commente", "partage", "subscribe", "follow"]
        has_cta = any(keyword in script.lower() for keyword in cta_keywords)

        # Score viral basique
        viral_score = 50
        if has_hook:
            viral_score += 20
        if has_cta:
            viral_score += 15
        if 30 <= estimated_duration <= 60:
            viral_score += 15

        return {
            "word_count": len(words),
            "char_count": chars,
            "estimated_duration": estimated_duration,
            "has_hook": has_hook,
            "has_cta": has_cta,
            "viral_score": viral_score,
            "improvements": [
                "Ajouter un hook percutant" if not has_hook else "✓ Hook détecté",
                "Ajouter un CTA clair" if not has_cta else "✓ CTA présent",
                f"Ajuster la durée (actuellement {estimated_duration:.1f}s)"
                if estimated_duration > 60 else "✓ Durée optimale"
            ]
        }
