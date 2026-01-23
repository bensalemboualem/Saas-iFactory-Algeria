"""
Router Intelligent - Routage des requêtes vers les orchestrateurs appropriés
"""

import re
from enum import Enum
from pydantic import BaseModel


class Target(str, Enum):
    BMAD = "bmad"
    ARCHON = "archon"
    BOLT = "bolt"
    META = "meta"


class RouteResult(BaseModel):
    target: Target
    action: str
    confidence: float
    reasoning: str


# Patterns de routage avec poids de confiance
# Note: BMAD gère la planification/design, Bolt exécute le code
PATTERNS: dict[Target, list[tuple[str, float]]] = {
    Target.BMAD: [
        # Workflow & Agile (EN)
        (r"\b(workflow|prd|architecture|story|sprint)\b", 0.9),
        (r"\b(plan|design|spec|requirement)\b", 0.8),
        (r"\b(agile|scrum|kanban|backlog)\b", 0.85),
        (r"\b(persona|epic|user.?story)\b", 0.9),
        # API & Features (EN)
        (r"\b(api|endpoint|route|service)\b", 0.85),
        (r"\b(feature|functionality|module)\b", 0.8),
        (r"\b(app|application|system)\b", 0.75),
        (r"\b(build|develop|create).*(api|app|system|feature)\b", 0.9),
        # Frontend/React patterns - VERY COMMON
        (r"\b(react|vue|angular|svelte|nextjs|nuxt)\b", 0.85),
        (r"\b(component|widget|ui|interface)\b", 0.8),
        (r"\b(page|screen|dashboard|form|button|modal)\b", 0.75),
        (r"\b(frontend|front.?end|client.?side)\b", 0.85),
        (r"(create|build|make)\s+(a|an|the)?\s*\w*\s*(component|page|app|form)", 0.9),
        (r"\b(counter|todo|calculator|chat|login)\b.*\b(app|component)?\b", 0.75),
        # French patterns (FR)
        (r"\b(cr[ée]+r?|développ|concevoir|planifier)\b", 0.85),
        (r"\b(fonctionnalit[ée]|module|service)\b", 0.8),
        (r"\b(application|système|plateforme)\b", 0.75),
        (r"\b(besoin|exigence|spécification)\b", 0.8),
        (r"\b(composant|bouton|formulaire|page)\b", 0.8),
        # Intent patterns - création de projet
        (r"(je veux|je voudrais|j'ai besoin|need|want).*(api|app|feature|service)", 0.9),
        (r"(créer?|build|make|develop).*(une?|an?|the)\s+\w+", 0.85),
    ],
    Target.ARCHON: [
        # Search & Knowledge (EN)
        (r"\b(search|find|query|knowledge)\b", 0.9),
        (r"\b(task|kb|database)\b", 0.85),
        (r"\b(rag|retrieval|embedding)\b", 0.9),
        (r"\b(document|index|crawl)\b", 0.8),
        # French patterns (FR)
        (r"\b(chercher|rechercher|trouver)\b", 0.9),
        (r"\b(tâche|base.?de.?donn[ée]+s)\b", 0.85),
    ],
    Target.BOLT: [
        # Code execution (EN) - specific implementation, not planning
        (r"\b(implement|write|code)\s+(this|the|a)\b", 0.9),
        (r"\b(deploy|git|commit|push)\b", 0.85),
        (r"\b(edit|refactor|modify)\s+(file|code|function)\b", 0.8),
        (r"\b(test|debug|fix|bug)\b", 0.85),
        (r"\b(execute|run|compile)\b", 0.8),
        # French patterns (FR)
        (r"\b(implémenter?|coder|programmer)\b", 0.85),
        (r"\b(exécuter|lancer|compiler)\b", 0.8),
        (r"\b(corriger|débugger|réparer)\b", 0.85),
    ],
}


def route(request: str, context: dict | None = None) -> RouteResult:
    """
    Route une requête vers l'orchestrateur approprié.

    Args:
        request: La requête utilisateur
        context: Contexte optionnel (session, projet, etc.)

    Returns:
        RouteResult avec la cible et le niveau de confiance
    """
    scores: dict[Target, float] = {t: 0.0 for t in Target}
    matched_patterns: dict[Target, list[str]] = {t: [] for t in Target}

    request_lower = request.lower()

    for target, patterns in PATTERNS.items():
        for pattern, weight in patterns:
            if re.search(pattern, request_lower):
                scores[target] = max(scores[target], weight)
                matched_patterns[target].append(pattern)

    # Bonus contextuel
    if context:
        current_target = context.get("current_target")
        if current_target and current_target in [t.value for t in Target]:
            target_enum = Target(current_target)
            scores[target_enum] = min(1.0, scores[target_enum] + 0.1)

    best = max(scores, key=scores.get)

    # Seuil de confiance minimum
    if scores[best] < 0.5:
        return RouteResult(
            target=Target.META,
            action="clarify",
            confidence=0.3,
            reasoning="Requête ambiguë - clarification nécessaire"
        )

    return RouteResult(
        target=best,
        action="process",
        confidence=scores[best],
        reasoning=f"Match patterns: {matched_patterns[best]}"
    )


def get_all_patterns() -> dict[str, list[str]]:
    """Retourne tous les patterns par cible pour documentation"""
    return {
        target.value: [p[0] for p in patterns]
        for target, patterns in PATTERNS.items()
    }
