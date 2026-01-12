"""
Discovery DZ Agent - Customer Discovery & Market Validation for Algerian Startups
Agent de validation marché utilisant la méthodologie Mom Test
"""
from typing import Dict, Any, List, Optional
from ..core.base_agent import BaseAgent, AgentConfig, AgentResponse
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)


class InterviewPhase(str, Enum):
    QUALIFICATION = "qualification"
    PROBLEM_EXPLORATION = "problem_exploration"
    CURRENT_SOLUTIONS = "current_solutions"
    VALUE_VALIDATION = "value_validation"
    CLOSING = "closing"


class SignalStrength(str, Enum):
    STRONG = "strong"
    MEDIUM = "medium"
    WEAK = "weak"


class Signal(BaseModel):
    """Signal détecté pendant l'interview"""
    type: SignalStrength
    indicator: str
    verbatim: Optional[str] = None
    phase: InterviewPhase


class InterviewState(BaseModel):
    """État de l'interview en cours"""
    current_phase: InterviewPhase = InterviewPhase.QUALIFICATION
    phase_exchanges: int = 0
    total_exchanges: int = 0
    signals: List[Signal] = Field(default_factory=list)
    verbatims: List[str] = Field(default_factory=list)
    problem_validated: Optional[bool] = None
    willingness_to_pay: Optional[str] = None
    current_spend: Optional[str] = None
    validation_score: Optional[int] = None


# Secteurs porteurs en Algérie
ALGERIAN_SECTORS = {
    "edtech": {
        "name": "EdTech",
        "opportunities": ["Formation professionnelle", "E-learning universitaire", "Préparation concours"],
        "challenges": ["Infrastructure internet", "Adoption digitale", "Paiement en ligne"]
    },
    "fintech": {
        "name": "FinTech",
        "opportunities": ["Mobile money", "Micro-crédit", "Transfert diaspora"],
        "challenges": ["Réglementation bancaire", "KYC/AML", "Confiance numérique"]
    },
    "agritech": {
        "name": "AgriTech",
        "opportunities": ["Irrigation intelligente", "Marketplace agricole", "Traçabilité"],
        "challenges": ["Connectivité rurale", "Formation agriculteurs", "Logistique"]
    },
    "ecommerce": {
        "name": "E-commerce",
        "opportunities": ["Marketplace locale", "Livraison dernier km", "Paiement à la livraison"],
        "challenges": ["Logistique", "Confiance client", "Retours produits"]
    },
    "b2b_services": {
        "name": "Services B2B",
        "opportunities": ["SaaS comptabilité", "CRM local", "RH digitalisée"],
        "challenges": ["Cycle de vente long", "Décideurs multiples", "Budget IT limité"]
    },
    "sante": {
        "name": "Santé",
        "opportunities": ["Télémédecine", "Gestion cabinet", "Pharmacie en ligne"],
        "challenges": ["Réglementation santé", "Confidentialité données", "Adoption médecins"]
    },
    "immobilier": {
        "name": "Immobilier",
        "opportunities": ["Marketplace location", "Estimation automatique", "Gestion locative"],
        "challenges": ["Données fiables", "Réglementation", "Informalité marché"]
    },
    "transport": {
        "name": "Transport & Logistique",
        "opportunities": ["VTC local", "Livraison express", "Fleet management"],
        "challenges": ["Réglementation transport", "Carburant", "Routes"]
    }
}

# Indicateurs de signaux
SIGNAL_INDICATORS = {
    SignalStrength.STRONG: [
        "problème mentionné spontanément",
        "solution de contournement élaborée",
        "budget déjà alloué",
        "émotion visible (frustration/enthousiasme)",
        "demande proactive de suivi",
        "recommandation spontanée de contacts"
    ],
    SignalStrength.MEDIUM: [
        "problème reconnu mais pas prioritaire",
        "intérêt poli",
        "ce serait bien d'avoir",
        "peut-être un jour"
    ],
    SignalStrength.WEAK: [
        "pas vraiment ce problème",
        "réponses courtes",
        "désengagement visible",
        "aucune solution actuelle"
    ]
}

# Questions par phase
PHASE_QUESTIONS = {
    InterviewPhase.QUALIFICATION: [
        "Pouvez-vous me décrire votre activité ou rôle actuel ?",
        "Quels sont vos principaux défis au quotidien ?",
        "Depuis combien de temps êtes-vous dans ce domaine ?"
    ],
    InterviewPhase.PROBLEM_EXPLORATION: [
        "Racontez-moi la dernière fois que vous avez rencontré ce problème...",
        "À quelle fréquence cela arrive-t-il ?",
        "Quelles conséquences cela a-t-il sur votre activité ?",
        "Combien cela vous coûte en temps ou en argent ?",
        "Qu'est-ce qui se passe quand ce problème survient ?"
    ],
    InterviewPhase.CURRENT_SOLUTIONS: [
        "Comment gérez-vous ce problème aujourd'hui ?",
        "Avez-vous essayé d'autres solutions ? Lesquelles ?",
        "Qu'est-ce qui ne vous satisfait pas dans ces solutions ?",
        "Combien dépensez-vous actuellement pour résoudre ce problème ?"
    ],
    InterviewPhase.VALUE_VALIDATION: [
        "Si une solution existait, quels critères seraient essentiels pour vous ?",
        "Quel budget seriez-vous prêt à allouer pour résoudre définitivement ce problème ?",
        "Qui d'autre dans votre organisation serait concerné par cette décision ?"
    ],
    InterviewPhase.CLOSING: [
        "Connaissez-vous d'autres personnes confrontées au même problème ?",
        "Seriez-vous ouvert à tester une solution quand elle sera prête ?",
        "Comment préférez-vous être recontacté ?"
    ]
}


class DiscoveryAgent(BaseAgent):
    """
    Agent de Customer Discovery pour startups algériennes.
    Utilise la méthodologie Mom Test pour valider les hypothèses business.
    """

    def __init__(self, config: AgentConfig = None):
        if config is None:
            config = AgentConfig(
                name="DiscoveryDZ",
                model="deepseek-chat",
                temperature=0.6,
                max_tokens=1500,
                language="fr",
                system_prompt=self._build_system_prompt()
            )
        super().__init__(config)
        self.interview_state = InterviewState()
        self.problem_hypothesis: Optional[str] = None
        self.target_profile: Optional[str] = None
        self.sector: Optional[str] = None

    def _build_system_prompt(self) -> str:
        return """Tu es IA Discovery DZ, un agent d'interview spécialisé dans le customer discovery et la validation de marché pour les entrepreneurs algériens.

MÉTHODOLOGIE MOM TEST:
- Parler du problème, pas de ta solution
- Questions sur le passé concret, pas le futur hypothétique
- Écouter plus que parler
- Chercher les faits, pas les opinions

RÈGLES:
✅ Creuser avec "pourquoi" et "comment"
✅ Demander des exemples concrets et récents
✅ Quantifier (fréquence, coût, temps)
✅ Noter les verbatims exacts
✅ S'adapter au darija si préféré

❌ NE JAMAIS pitcher ta solution
❌ NE JAMAIS poser des questions hypothétiques ("Est-ce que vous utiliseriez...")
❌ NE JAMAIS demander des opinions générales
❌ NE JAMAIS influencer les réponses

CONTEXTE ALGÉRIEN:
- Écosystème startup en développement
- Défis: financement, réglementation, paiement en ligne
- Opportunités: digitalisation, jeunesse connectée, diaspora

TON: Professionnel, curieux, empathique, neutre (pas de vente)"""

    def reset_interview(self):
        """Réinitialise l'état de l'interview"""
        self.interview_state = InterviewState()
        self.problem_hypothesis = None
        self.target_profile = None
        self.sector = None

    def set_context(self, problem: str, target: str, sector: str = None):
        """Définit le contexte de l'interview"""
        self.problem_hypothesis = problem
        self.target_profile = target
        self.sector = sector

    def _get_phase_config(self) -> Dict[str, int]:
        """Retourne la config min/max échanges par phase"""
        return {
            InterviewPhase.QUALIFICATION: (2, 3),
            InterviewPhase.PROBLEM_EXPLORATION: (4, 6),
            InterviewPhase.CURRENT_SOLUTIONS: (3, 4),
            InterviewPhase.VALUE_VALIDATION: (2, 3),
            InterviewPhase.CLOSING: (1, 2)
        }

    def _should_advance_phase(self) -> bool:
        """Détermine si on doit passer à la phase suivante"""
        config = self._get_phase_config()
        min_exchanges, max_exchanges = config.get(self.interview_state.current_phase, (2, 3))
        return self.interview_state.phase_exchanges >= min_exchanges

    def _advance_phase(self):
        """Passe à la phase suivante"""
        phases = list(InterviewPhase)
        current_idx = phases.index(self.interview_state.current_phase)
        if current_idx < len(phases) - 1:
            self.interview_state.current_phase = phases[current_idx + 1]
            self.interview_state.phase_exchanges = 0

    def _detect_signals(self, response: str) -> List[Signal]:
        """Détecte les signaux dans la réponse"""
        signals = []
        response_lower = response.lower()

        for strength, indicators in SIGNAL_INDICATORS.items():
            for indicator in indicators:
                if any(word in response_lower for word in indicator.split()):
                    signals.append(Signal(
                        type=strength,
                        indicator=indicator,
                        verbatim=response[:200] if len(response) > 200 else response,
                        phase=self.interview_state.current_phase
                    ))

        return signals

    def _calculate_validation_score(self) -> int:
        """Calcule le score de validation (1-10)"""
        score = 5  # Base neutre

        for signal in self.interview_state.signals:
            if signal.type == SignalStrength.STRONG:
                score += 1.5
            elif signal.type == SignalStrength.MEDIUM:
                score += 0.5
            elif signal.type == SignalStrength.WEAK:
                score -= 1

        # Bonus si budget mentionné
        if self.interview_state.current_spend:
            score += 1

        # Bonus si willingness to pay
        if self.interview_state.willingness_to_pay:
            score += 1

        return max(1, min(10, int(score)))

    def generate_report(self) -> str:
        """Génère le rapport final de l'interview"""
        score = self._calculate_validation_score()
        self.interview_state.validation_score = score

        strong_signals = [s for s in self.interview_state.signals if s.type == SignalStrength.STRONG]
        medium_signals = [s for s in self.interview_state.signals if s.type == SignalStrength.MEDIUM]
        weak_signals = [s for s in self.interview_state.signals if s.type == SignalStrength.WEAK]

        report = f"""## 📊 Rapport Discovery Interview

**Problème exploré** : {self.problem_hypothesis or 'Non défini'}
**Profil cible** : {self.target_profile or 'Non défini'}
**Secteur** : {self.sector or 'Non défini'}
**Date** : {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Échanges** : {self.interview_state.total_exchanges}

---

### ✅ Validation Problème
- **Problème confirmé** : {'Oui' if score >= 7 else 'Partiellement' if score >= 5 else 'Non'}
- **Budget actuel** : {self.interview_state.current_spend or 'Non mentionné'}
- **Disposition à payer** : {self.interview_state.willingness_to_pay or 'Non validée'}

---

### 🎯 Signaux Détectés

#### 🟢 Signaux Forts ({len(strong_signals)})
"""
        for s in strong_signals[:5]:
            report += f"- {s.indicator}\n"

        report += f"""
#### 🟡 Signaux Moyens ({len(medium_signals)})
"""
        for s in medium_signals[:3]:
            report += f"- {s.indicator}\n"

        report += f"""
#### 🔴 Signaux Faibles ({len(weak_signals)})
"""
        for s in weak_signals[:3]:
            report += f"- {s.indicator}\n"

        report += f"""
---

### 📊 Score de Validation
**{score}/10** - {'✅ Problem-Market Fit validé' if score >= 7 else '🔄 À approfondir' if score >= 5 else '⚠️ Hypothèse à revoir'}

---

### 🔑 Verbatims Importants
"""
        for v in self.interview_state.verbatims[:5]:
            report += f'> "{v[:150]}..."\n\n'

        report += f"""
---

### ➡️ Prochaines Étapes Recommandées
"""
        if score >= 7:
            report += """- [ ] Contacter les références obtenues
- [ ] Préparer un prototype/MVP
- [ ] Planifier des tests utilisateurs
"""
        elif score >= 5:
            report += """- [ ] Conduire 3-5 interviews supplémentaires
- [ ] Affiner l'hypothèse de problème
- [ ] Explorer d'autres segments
"""
        else:
            report += """- [ ] Pivoter vers un autre problème
- [ ] Requalifier le persona cible
- [ ] Rechercher un nouveau segment
"""

        return report

    async def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        Exécute un tour de l'interview de discovery.

        Args:
            input_data: {
                "message": str,  # Réponse de l'interviewé
                "action": str,   # "start", "continue", "report"
                "problem": str,  # Hypothèse de problème (pour start)
                "target": str,   # Profil cible (pour start)
                "sector": str    # Secteur (optionnel)
            }
        """
        action = input_data.get("action", "continue")

        # Démarrage de l'interview
        if action == "start":
            self.reset_interview()
            self.set_context(
                problem=input_data.get("problem", ""),
                target=input_data.get("target", ""),
                sector=input_data.get("sector", "")
            )

            welcome = f"""Bonjour ! 👋 Je suis IA Discovery, votre assistant pour les interviews de validation marché.

**Contexte défini :**
- 🎯 Problème à valider : {self.problem_hypothesis}
- 👤 Profil cible : {self.target_profile}
{f'- 🏢 Secteur : {self.sector}' if self.sector else ''}

Je vais maintenant conduire l'interview selon la méthodologie Mom Test.

---

**Phase 1 : Contexte & Qualification**

{PHASE_QUESTIONS[InterviewPhase.QUALIFICATION][0]}"""

            return AgentResponse(
                content=welcome,
                metadata={
                    "phase": self.interview_state.current_phase.value,
                    "exchange": 0,
                    "action": "interview_started"
                }
            )

        # Génération du rapport
        if action == "report":
            report = self.generate_report()
            return AgentResponse(
                content=report,
                metadata={
                    "phase": "completed",
                    "validation_score": self.interview_state.validation_score,
                    "signals_count": len(self.interview_state.signals),
                    "action": "report_generated"
                }
            )

        # Continuer l'interview
        user_message = input_data.get("message", "")

        # Détecter les signaux dans la réponse
        signals = self._detect_signals(user_message)
        self.interview_state.signals.extend(signals)

        # Capturer les verbatims importants (réponses longues)
        if len(user_message) > 50:
            self.interview_state.verbatims.append(user_message)

        # Mettre à jour les compteurs
        self.interview_state.phase_exchanges += 1
        self.interview_state.total_exchanges += 1

        # Construire le contexte pour le LLM
        sector_context = ""
        if self.sector and self.sector in ALGERIAN_SECTORS:
            sector_info = ALGERIAN_SECTORS[self.sector]
            sector_context = f"""
CONTEXTE SECTEUR {sector_info['name'].upper()}:
- Opportunités: {', '.join(sector_info['opportunities'])}
- Défis: {', '.join(sector_info['challenges'])}
"""

        system_prompt = f"""{self._build_system_prompt()}

INTERVIEW EN COURS:
- Problème à valider: {self.problem_hypothesis}
- Profil cible: {self.target_profile}
- Phase actuelle: {self.interview_state.current_phase.value}
- Échange dans cette phase: {self.interview_state.phase_exchanges}
{sector_context}

QUESTIONS SUGGÉRÉES POUR CETTE PHASE:
{chr(10).join(f'- {q}' for q in PHASE_QUESTIONS[self.interview_state.current_phase])}

SIGNAUX DÉTECTÉS JUSQU'ICI: {len(self.interview_state.signals)} (Forts: {len([s for s in self.interview_state.signals if s.type == SignalStrength.STRONG])})

INSTRUCTIONS:
1. Analyse la réponse de l'interviewé
2. Pose UNE question de suivi pertinente basée sur sa réponse
3. Creuse les détails concrets (fréquence, coût, impact)
4. Reste dans le cadre de la phase actuelle
5. Si la réponse est riche en insights, note-le
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Réponse de l'interviewé:\n\n{user_message}\n\nGénère ta prochaine question (UNE seule, courte et ciblée):"}
        ]

        response = await self._call_llm(messages)

        # Vérifier si on doit avancer de phase
        should_advance = self._should_advance_phase()
        if should_advance and self.interview_state.current_phase != InterviewPhase.CLOSING:
            self._advance_phase()
            phase_indicator = f"\n\n---\n**Passage à la phase : {self.interview_state.current_phase.value.replace('_', ' ').title()}**\n"
            response_content = phase_indicator + response['content']
        else:
            response_content = response['content']

        # Check si interview terminée
        is_complete = (
            self.interview_state.current_phase == InterviewPhase.CLOSING and
            self.interview_state.phase_exchanges >= 2
        )

        if is_complete:
            response_content += "\n\n---\n✅ **Interview terminée !** Tapez 'rapport' pour générer le rapport de validation."

        return AgentResponse(
            content=response_content,
            tokens_used=response.get('tokens'),
            metadata={
                "phase": self.interview_state.current_phase.value,
                "exchange": self.interview_state.total_exchanges,
                "signals_detected": len(signals),
                "total_signals": len(self.interview_state.signals),
                "is_complete": is_complete
            }
        )


# Export pour découverte CLI
__all__ = ['DiscoveryAgent', 'InterviewState', 'Signal', 'ALGERIAN_SECTORS', 'PHASE_QUESTIONS']
