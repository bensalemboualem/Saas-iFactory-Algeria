"""
IAFactory Video Studio Pro - Agent Contrôleur Qualité (QualityController)
Vérifie et valide la qualité du contenu avant production
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from enum import Enum
import json
import logging

from pydantic import BaseModel, Field

from . import (
    BaseAgent, 
    AgentConfig, 
    AgentResponse,
    JSONOutputMixin,
    MultilingualMixin,
    CostTrackingMixin
)
from .scriptwriter import VideoScript
from config import settings


logger = logging.getLogger(__name__)


# === ENUMS ===

class QualityLevel(str, Enum):
    EXCELLENT = "excellent"  # 9-10
    GOOD = "good"  # 7-8
    ACCEPTABLE = "acceptable"  # 5-6
    NEEDS_WORK = "needs_work"  # 3-4
    REJECTED = "rejected"  # 0-2


class IssueType(str, Enum):
    CONTENT = "content"  # Problème de contenu
    STRUCTURE = "structure"  # Problème de structure
    TIMING = "timing"  # Problème de timing
    LANGUAGE = "language"  # Problème de langue
    CULTURAL = "cultural"  # Problème culturel
    LEGAL = "legal"  # Problème légal
    BRAND = "brand"  # Problème de marque
    TECHNICAL = "technical"  # Problème technique


class IssueSeverity(str, Enum):
    CRITICAL = "critical"  # Bloque la production
    MAJOR = "major"  # Doit être corrigé
    MINOR = "minor"  # Amélioration suggérée
    INFO = "info"  # Information


# === MODÈLES DE DONNÉES ===

class QualityIssue(BaseModel):
    """Un problème détecté."""
    id: str
    type: IssueType
    severity: IssueSeverity
    location: str  # Ex: "hook", "segment_2", "cta"
    description: str
    suggestion: str
    auto_fixable: bool = False


class QualityScore(BaseModel):
    """Score de qualité par critère."""
    criterion: str
    score: float  # 0-10
    weight: float  # Poids dans le score global
    comments: str


class QualityReport(BaseModel):
    """Rapport de contrôle qualité complet."""
    report_id: str = Field(default_factory=lambda: f"qc_{datetime.now().strftime('%Y%m%d%H%M%S')}")
    script_id: str
    
    # Verdict global
    overall_level: QualityLevel
    overall_score: float  # 0-10
    approved: bool
    
    # Scores détaillés
    scores: List[QualityScore]
    
    # Problèmes détectés
    issues: List[QualityIssue]
    critical_issues: int
    major_issues: int
    minor_issues: int
    
    # Recommandations
    recommendations: List[str]
    auto_fixes_available: List[str]
    
    # Métriques
    viral_potential_score: float
    engagement_prediction: float
    platform_optimization_score: float
    
    # Metadata
    reviewed_at: datetime = Field(default_factory=datetime.utcnow)
    reviewer_agent: str = "QualityController"


class QualityCheckRequest(BaseModel):
    """Requête de contrôle qualité."""
    script: VideoScript
    target_market: str = "dz"
    language: str = "fr"
    platform: str = "tiktok"
    brand_guidelines: Optional[str] = None
    strict_mode: bool = False  # Mode strict = plus exigeant
    auto_fix: bool = True  # Appliquer les corrections auto


# === AGENT QUALITY CONTROLLER ===

class QualityControllerAgent(BaseAgent, JSONOutputMixin, MultilingualMixin, CostTrackingMixin):
    """
    Agent Contrôleur Qualité - Valide le contenu avant production.
    
    Contrôles effectués:
    - Qualité du contenu et du storytelling
    - Respect des guidelines de marque
    - Optimisation plateforme
    - Vérification culturelle (marché cible)
    - Détection de problèmes légaux
    - Score de viralité
    """
    
    DEFAULT_CONFIG = AgentConfig(
        name="QualityController",
        model=settings.CLAUDE_MODEL_SONNET,
        temperature=0.3,  # Précis et cohérent
        max_tokens=4000,
        system_prompt="""Tu es un expert en contrôle qualité de contenu vidéo pour le marché algérien et francophone.

MISSION: Évaluer rigoureusement chaque script avant production pour garantir la qualité et la viralité.

CRITÈRES D'ÉVALUATION:

1. **Hook (Accroche)** - 3 premières secondes cruciales
   - Captation immédiate de l'attention
   - Curiosité ou émotion déclenchée
   - Promesse claire

2. **Structure** - Architecture du contenu
   - Progression logique
   - Rythme adapté à la plateforme
   - Montée en tension

3. **Contenu** - Qualité du message
   - Valeur apportée à l'audience
   - Originalité
   - Clarté

4. **CTA (Call-to-Action)** - Engagement final
   - Clarté de l'action demandée
   - Motivation à agir
   - Facilité d'exécution

5. **Optimisation Plateforme** - Adaptation technique
   - Durée appropriée
   - Format adapté
   - Hashtags/SEO

6. **Sensibilité Culturelle** - Respect du marché
   - Pas de contenu offensant
   - Respect des valeurs locales
   - Authenticité

7. **Légalité** - Conformité
   - Pas de plagiat
   - Pas de diffamation
   - Respect du droit d'auteur

SCORING: Chaque critère noté de 0 à 10.
- 9-10: Excellent
- 7-8: Bon
- 5-6: Acceptable
- 3-4: À retravailler
- 0-2: Rejeté

OUTPUT: Rapport JSON structuré avec verdict, scores, problèmes et recommandations."""
    )
    
    # Poids des critères dans le score global
    CRITERIA_WEIGHTS = {
        "hook": 0.20,
        "structure": 0.15,
        "content": 0.20,
        "cta": 0.10,
        "platform_optimization": 0.15,
        "cultural_sensitivity": 0.10,
        "legal_compliance": 0.10,
    }
    
    def __init__(self, config: Optional[AgentConfig] = None):
        super().__init__(config or self.DEFAULT_CONFIG)
    
    async def process(self, input_data: QualityCheckRequest) -> AgentResponse:
        """
        Effectue le contrôle qualité complet d'un script.
        """
        start_time = datetime.utcnow()
        
        try:
            prompt = self._build_review_prompt(input_data)
            
            response = await self.call_llm(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            # Parser le rapport
            report = self.parse_json_output(response["content"], QualityReport)
            
            # Appliquer les auto-fixes si demandé
            if input_data.auto_fix and report.auto_fixes_available:
                report = await self._apply_auto_fixes(report, input_data.script)
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            return AgentResponse(
                success=True,
                data=report.model_dump(),
                tokens_used=response.get("tokens_used", 0),
                processing_time=processing_time,
                agent_name=self.name
            )
            
        except Exception as e:
            logger.error(f"QualityController error: {e}")
            return AgentResponse(
                success=False,
                data=None,
                agent_name=self.name,
                error=str(e)
            )
    
    def _build_review_prompt(self, request: QualityCheckRequest) -> str:
        """Construit le prompt de revue qualité."""
        
        script = request.script
        script_json = json.dumps(script.model_dump(), ensure_ascii=False, indent=2)
        
        market_context = {
            "dz": "Algérie - Culture musulmane, humour local, Darija/Français, sensibilités religieuses",
            "fr": "France - Culture européenne, laïcité, diversité",
            "ch": "Suisse - Qualité premium, multilingue, précision",
            "mena": "MENA - Culture arabe, valeurs familiales, diversité régionale"
        }
        
        prompt = f"""
CONTRÔLE QUALITÉ - Script Vidéo

## Informations du projet
- **ID Script**: {script.id}
- **Titre**: {script.title}
- **Plateforme**: {request.platform}
- **Marché cible**: {request.target_market} - {market_context.get(request.target_market, "International")}
- **Langue**: {request.language}
- **Durée cible**: {script.duration_target}s
- **Mode strict**: {"Oui" if request.strict_mode else "Non"}

{f"**Guidelines de marque**: {request.brand_guidelines}" if request.brand_guidelines else ""}

## Script à évaluer

```json
{script_json}
```

## Ta mission

Effectue un contrôle qualité complet selon les 7 critères:

1. **Hook** (poids: 20%) - L'accroche capture-t-elle l'attention instantanément?
2. **Structure** (poids: 15%) - Le contenu est-il bien structuré?
3. **Contenu** (poids: 20%) - Le message est-il de qualité?
4. **CTA** (poids: 10%) - L'appel à l'action est-il efficace?
5. **Optimisation plateforme** (poids: 15%) - Adapté à {request.platform}?
6. **Sensibilité culturelle** (poids: 10%) - Respecte le marché {request.target_market}?
7. **Conformité légale** (poids: 10%) - Pas de problèmes juridiques?

## Format de réponse (JSON)

```json
{{
    "report_id": "qc_YYYYMMDDHHMMSS",
    "script_id": "{script.id}",
    "overall_level": "good|excellent|acceptable|needs_work|rejected",
    "overall_score": 7.5,
    "approved": true,
    "scores": [
        {{
            "criterion": "hook",
            "score": 8.0,
            "weight": 0.20,
            "comments": "Accroche percutante mais pourrait être plus..."
        }},
        ...
    ],
    "issues": [
        {{
            "id": "issue_1",
            "type": "content|structure|timing|language|cultural|legal|brand|technical",
            "severity": "critical|major|minor|info",
            "location": "hook",
            "description": "Description du problème...",
            "suggestion": "Comment corriger...",
            "auto_fixable": false
        }}
    ],
    "critical_issues": 0,
    "major_issues": 1,
    "minor_issues": 2,
    "recommendations": [
        "Recommandation 1...",
        "Recommandation 2..."
    ],
    "auto_fixes_available": [
        "fix_1: Correction automatique possible..."
    ],
    "viral_potential_score": 8.0,
    "engagement_prediction": 7.5,
    "platform_optimization_score": 8.5
}}
```

Génère le rapport de qualité maintenant:
"""
        
        return prompt

    async def _apply_auto_fixes(
        self, 
        report: QualityReport, 
        script: VideoScript
    ) -> QualityReport:
        """
        Applique les corrections automatiques possibles.
        """
        if not report.auto_fixes_available:
            return report
        
        # Les fixes auto sont appliquées par le ScriptWriter
        # Ici on met juste à jour le rapport
        logger.info(f"Auto-fixes disponibles: {report.auto_fixes_available}")
        
        return report

    async def quick_check(
        self, 
        script: VideoScript, 
        market: str = "dz"
    ) -> Dict:
        """
        Vérification rapide d'un script.
        Retourne un résumé simple: approuvé/rejeté + score.
        """
        request = QualityCheckRequest(
            script=script,
            target_market=market,
            strict_mode=False,
            auto_fix=False
        )
        
        result = await self.process(request)
        
        if result.success:
            data = result.data
            return {
                "approved": data.get("approved", False),
                "score": data.get("overall_score", 0),
                "level": data.get("overall_level", "unknown"),
                "critical_issues": data.get("critical_issues", 0),
                "viral_potential": data.get("viral_potential_score", 0)
            }
        
        return {
            "approved": False,
            "score": 0,
            "level": "error",
            "error": result.error
        }

    async def check_cultural_sensitivity(
        self, 
        content: str, 
        market: str = "dz"
    ) -> Dict:
        """
        Vérifie spécifiquement la sensibilité culturelle d'un contenu.
        """
        prompt = f"""
Analyse ce contenu pour le marché {market} et détecte tout problème de sensibilité culturelle:

CONTENU:
{content}

MARCHÉ: {market}
{"Algérie - Culture musulmane, respect des valeurs religieuses et familiales" if market == "dz" else ""}

Vérifie:
1. Respect des valeurs religieuses
2. Pas de contenu offensant
3. Langage approprié
4. Références culturelles correctes

Retourne en JSON:
{{
    "safe": true/false,
    "issues": ["..."],
    "suggestions": ["..."],
    "confidence": 0.95
}}
"""
        
        response = await self.call_llm(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        
        return self.parse_json_output(response["content"], dict)

    async def validate_for_platform(
        self, 
        script: VideoScript, 
        platform: str
    ) -> Dict:
        """
        Valide un script pour une plateforme spécifique.
        """
        platform_specs = {
            "tiktok": {"max_duration": 180, "optimal_duration": 30, "format": "vertical"},
            "instagram": {"max_duration": 90, "optimal_duration": 30, "format": "vertical"},
            "youtube_short": {"max_duration": 60, "optimal_duration": 45, "format": "vertical"},
            "youtube": {"max_duration": 3600, "optimal_duration": 600, "format": "horizontal"},
        }
        
        specs = platform_specs.get(platform, {})
        
        issues = []
        
        if script.duration_target > specs.get("max_duration", 9999):
            issues.append(f"Durée ({script.duration_target}s) dépasse le max ({specs['max_duration']}s)")
        
        score = 10.0 - len(issues) * 2
        
        return {
            "platform": platform,
            "valid": len(issues) == 0,
            "score": max(0, score),
            "specs": specs,
            "issues": issues,
            "optimizations_suggested": []
        }
