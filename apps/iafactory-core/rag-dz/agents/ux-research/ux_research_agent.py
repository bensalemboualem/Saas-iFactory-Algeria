"""
UX Research Agent - User Feedback Collection for IA Factory Products
Agent d'interview UX pour collecter les retours utilisateurs
"""
from typing import Dict, Any, List, Optional
from ..core.base_agent import BaseAgent, AgentConfig, AgentResponse
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class InterviewPhase(str, Enum):
    ACCUEIL = "accueil"
    EXPLORATION = "exploration"
    FRICTION = "friction"
    SUGGESTIONS = "suggestions"
    CLOTURE = "cloture"


class FeedbackType(str, Enum):
    BUG = "bug"
    FEATURE_REQUEST = "feature_request"
    UX_ISSUE = "ux_issue"
    PERFORMANCE = "performance"
    PRAISE = "praise"
    OTHER = "other"


class FeedbackItem(BaseModel):
    """Item de feedback collecté"""
    type: FeedbackType
    description: str
    product: str
    severity: int = Field(ge=1, le=5, default=3)  # 1=mineur, 5=critique
    verbatim: Optional[str] = None
    phase: InterviewPhase


class InterviewState(BaseModel):
    """État de l'interview UX"""
    current_phase: InterviewPhase = InterviewPhase.ACCUEIL
    phase_exchanges: int = 0
    total_exchanges: int = 0
    products_discussed: List[str] = Field(default_factory=list)
    feedbacks: List[FeedbackItem] = Field(default_factory=list)
    satisfaction_score: Optional[int] = None  # 1-10
    nps_score: Optional[int] = None  # -100 to 100
    verbatims: List[str] = Field(default_factory=list)
    action_items: List[str] = Field(default_factory=list)


# Produits IA Factory
IAFACTORY_PRODUCTS = {
    "business_dz": {
        "name": "Business DZ",
        "description": "Conformité fiscale et juridique algérienne",
        "category": "business",
        "key_features": ["Conformité CNRC", "Fiscalité DZ", "Documents légaux"]
    },
    "rag_ecole": {
        "name": "RAG École",
        "description": "Gestion scolaire intelligente",
        "category": "education",
        "key_features": ["Gestion élèves", "Planning", "Notes et bulletins"]
    },
    "rag_islam": {
        "name": "RAG Islam",
        "description": "Connaissances islamiques FR/AR",
        "category": "education",
        "key_features": ["Coran", "Hadiths", "Fiqh", "Questions religieuses"]
    },
    "studio_creatif": {
        "name": "Studio Créatif",
        "description": "Création de contenu IA",
        "category": "creative",
        "key_features": ["Génération images", "Texte créatif", "Vidéo"]
    },
    "ia_finance": {
        "name": "IA Finance",
        "description": "Assistant financier personnel",
        "category": "finance",
        "key_features": ["Budget", "Investissement", "Analyse"]
    },
    "ia_marketing": {
        "name": "IA Marketing",
        "description": "Assistant marketing digital",
        "category": "marketing",
        "key_features": ["Content", "SEO", "Social Media"]
    },
    "ia_legal": {
        "name": "IA Legal",
        "description": "Assistant juridique",
        "category": "legal",
        "key_features": ["Contrats", "Conseils légaux", "Droit algérien"]
    },
    "ia_sales": {
        "name": "IA Sales",
        "description": "Assistant commercial",
        "category": "sales",
        "key_features": ["Prospection", "CRM", "Scripts vente"]
    },
    "ia_data": {
        "name": "IA Data",
        "description": "Analyse de données",
        "category": "data",
        "key_features": ["Visualisation", "Rapports", "Insights"]
    },
    "ia_startup": {
        "name": "IA Startup",
        "description": "Accompagnement entrepreneurs",
        "category": "business",
        "key_features": ["Business plan", "Pitch deck", "Validation marché"]
    },
    "chat_multimodal": {
        "name": "Chat Multimodal",
        "description": "Chat IA avec images et documents",
        "category": "core",
        "key_features": ["Multi-LLM", "Upload fichiers", "Vision"]
    }
}

# Questions par phase
PHASE_QUESTIONS = {
    InterviewPhase.ACCUEIL: [
        "Quel(s) produit(s) IA Factory utilisez-vous ou avez-vous testé ?",
        "Depuis combien de temps utilisez-vous ces produits ?",
        "Dans quel contexte les utilisez-vous (personnel, professionnel) ?"
    ],
    InterviewPhase.EXPLORATION: [
        "Comment utilisez-vous {product} au quotidien ?",
        "Pouvez-vous me décrire la dernière fois que vous l'avez utilisé ?",
        "Qu'est-ce qui vous a amené à choisir cette solution ?",
        "À quelle fréquence utilisez-vous ce produit ?"
    ],
    InterviewPhase.FRICTION: [
        "Y a-t-il des moments où vous vous êtes senti bloqué ou frustré ?",
        "Si vous pouviez changer une seule chose, ce serait quoi ?",
        "Qu'est-ce qui manque pour que ce soit parfait pour vous ?",
        "Avez-vous rencontré des bugs ou des erreurs ?",
        "Y a-t-il des fonctionnalités que vous n'utilisez pas ? Pourquoi ?"
    ],
    InterviewPhase.SUGGESTIONS: [
        "Quelles fonctionnalités aimeriez-vous voir ajoutées ?",
        "Comment imaginez-vous le produit idéal ?",
        "Y a-t-il d'autres outils que vous utilisez en complément ?",
        "Recommanderiez-vous ce produit à un ami ou collègue ?"
    ],
    InterviewPhase.CLOTURE: [
        "Sur une échelle de 1 à 10, quelle est votre satisfaction globale ?",
        "Y a-t-il autre chose que vous aimeriez partager ?",
        "Souhaitez-vous être informé des nouvelles fonctionnalités ?"
    ]
}

# Techniques de relance
PROBING_TECHNIQUES = {
    "clarification": "Pouvez-vous m'en dire plus sur... ?",
    "exemple": "Avez-vous un exemple précis ?",
    "emotion": "Comment vous êtes-vous senti à ce moment ?",
    "impact": "Quel impact cela a eu sur votre travail ?",
    "alternative": "Comment faisiez-vous avant ?",
    "frequence": "À quelle fréquence cela arrive-t-il ?",
    "solution": "Comment avez-vous contourné le problème ?"
}


class UXResearchAgent(BaseAgent):
    """
    Agent UX Research pour collecter les feedbacks utilisateurs IA Factory.
    Conduit des interviews qualitatives structurées.
    """

    def __init__(self, config: AgentConfig = None):
        if config is None:
            config = AgentConfig(
                name="UXResearch",
                model="deepseek-chat",
                temperature=0.7,
                max_tokens=1500,
                language="fr",
                system_prompt=self._build_system_prompt()
            )
        super().__init__(config)
        self.interview_state = InterviewState()
        self.current_product_focus: Optional[str] = None

    def _build_system_prompt(self) -> str:
        return """Tu es IA UX Research, un agent d'interview spécialisé dans la collecte de feedback utilisateurs pour les produits IA Factory.

OBJECTIFS:
1. Comprendre l'usage actuel des produits
2. Identifier les points de friction et frustrations
3. Découvrir les besoins non satisfaits
4. Collecter des suggestions d'amélioration
5. Évaluer la satisfaction générale

RÈGLES:
✅ Poser des questions ouvertes
✅ Écouter activement et reformuler
✅ Creuser avec "pourquoi" et "comment"
✅ Rester neutre, ne pas influencer
✅ S'adapter au niveau technique de l'utilisateur
✅ Être empathique face aux frustrations

❌ Questions fermées (oui/non)
❌ Suggérer des réponses
❌ Défendre ou justifier le produit
❌ Poser plusieurs questions à la fois
❌ Être condescendant
❌ Interrompre ou précipiter

TECHNIQUES DE RELANCE:
- Clarification: "Pouvez-vous m'en dire plus ?"
- Exemple: "Avez-vous un exemple précis ?"
- Émotion: "Comment vous êtes-vous senti ?"
- Impact: "Quel impact cela a eu ?"

TON: Professionnel, chaleureux, curieux, empathique"""

    def reset_interview(self):
        """Réinitialise l'état de l'interview"""
        self.interview_state = InterviewState()
        self.current_product_focus = None

    def _get_phase_config(self) -> Dict[InterviewPhase, tuple]:
        """Retourne la config min/max échanges par phase"""
        return {
            InterviewPhase.ACCUEIL: (1, 2),
            InterviewPhase.EXPLORATION: (3, 5),
            InterviewPhase.FRICTION: (3, 5),
            InterviewPhase.SUGGESTIONS: (2, 3),
            InterviewPhase.CLOTURE: (1, 2)
        }

    def _should_advance_phase(self) -> bool:
        """Détermine si on doit passer à la phase suivante"""
        config = self._get_phase_config()
        min_exchanges, _ = config.get(self.interview_state.current_phase, (2, 3))
        return self.interview_state.phase_exchanges >= min_exchanges

    def _advance_phase(self):
        """Passe à la phase suivante"""
        phases = list(InterviewPhase)
        current_idx = phases.index(self.interview_state.current_phase)
        if current_idx < len(phases) - 1:
            self.interview_state.current_phase = phases[current_idx + 1]
            self.interview_state.phase_exchanges = 0

    def _detect_feedback_type(self, response: str) -> List[FeedbackItem]:
        """Détecte et catégorise les feedbacks dans la réponse"""
        feedbacks = []
        response_lower = response.lower()

        # Détection bugs
        bug_keywords = ["bug", "erreur", "plante", "crash", "ne marche pas", "bloqué", "ne fonctionne pas"]
        if any(kw in response_lower for kw in bug_keywords):
            feedbacks.append(FeedbackItem(
                type=FeedbackType.BUG,
                description="Bug mentionné par l'utilisateur",
                product=self.current_product_focus or "général",
                severity=4,
                verbatim=response[:200],
                phase=self.interview_state.current_phase
            ))

        # Détection demandes fonctionnalités
        feature_keywords = ["j'aimerais", "il manque", "ce serait bien", "si seulement", "il faudrait"]
        if any(kw in response_lower for kw in feature_keywords):
            feedbacks.append(FeedbackItem(
                type=FeedbackType.FEATURE_REQUEST,
                description="Demande de fonctionnalité",
                product=self.current_product_focus or "général",
                severity=3,
                verbatim=response[:200],
                phase=self.interview_state.current_phase
            ))

        # Détection problèmes UX
        ux_keywords = ["pas intuitif", "compliqué", "difficile à trouver", "je ne comprends pas", "confus"]
        if any(kw in response_lower for kw in ux_keywords):
            feedbacks.append(FeedbackItem(
                type=FeedbackType.UX_ISSUE,
                description="Problème d'expérience utilisateur",
                product=self.current_product_focus or "général",
                severity=3,
                verbatim=response[:200],
                phase=self.interview_state.current_phase
            ))

        # Détection problèmes performance
        perf_keywords = ["lent", "rame", "charge longtemps", "timeout", "trop long"]
        if any(kw in response_lower for kw in perf_keywords):
            feedbacks.append(FeedbackItem(
                type=FeedbackType.PERFORMANCE,
                description="Problème de performance",
                product=self.current_product_focus or "général",
                severity=4,
                verbatim=response[:200],
                phase=self.interview_state.current_phase
            ))

        # Détection éloges
        praise_keywords = ["génial", "super", "j'adore", "excellent", "parfait", "top"]
        if any(kw in response_lower for kw in praise_keywords):
            feedbacks.append(FeedbackItem(
                type=FeedbackType.PRAISE,
                description="Retour positif",
                product=self.current_product_focus or "général",
                severity=1,
                verbatim=response[:200],
                phase=self.interview_state.current_phase
            ))

        return feedbacks

    def _extract_products_mentioned(self, response: str) -> List[str]:
        """Extrait les produits mentionnés dans la réponse"""
        products = []
        response_lower = response.lower()

        for product_id, product_info in IAFACTORY_PRODUCTS.items():
            product_name_lower = product_info["name"].lower()
            if product_name_lower in response_lower or product_id.replace("_", " ") in response_lower:
                products.append(product_info["name"])

        return products

    def _extract_satisfaction_score(self, response: str) -> Optional[int]:
        """Extrait le score de satisfaction si mentionné"""
        import re
        # Cherche des patterns comme "8/10", "8 sur 10", "note: 8"
        patterns = [
            r"(\d+)\s*/\s*10",
            r"(\d+)\s+sur\s+10",
            r"note\s*:\s*(\d+)",
            r"(\d+)\s+étoiles"
        ]

        for pattern in patterns:
            match = re.search(pattern, response.lower())
            if match:
                score = int(match.group(1))
                if 1 <= score <= 10:
                    return score

        return None

    def _generate_action_items(self) -> List[str]:
        """Génère les actions recommandées basées sur les feedbacks"""
        actions = []

        # Compter par type
        bug_count = len([f for f in self.interview_state.feedbacks if f.type == FeedbackType.BUG])
        feature_count = len([f for f in self.interview_state.feedbacks if f.type == FeedbackType.FEATURE_REQUEST])
        ux_count = len([f for f in self.interview_state.feedbacks if f.type == FeedbackType.UX_ISSUE])
        perf_count = len([f for f in self.interview_state.feedbacks if f.type == FeedbackType.PERFORMANCE])

        if bug_count > 0:
            actions.append(f"🐛 Investiguer les {bug_count} bug(s) signalé(s)")

        if perf_count > 0:
            actions.append(f"⚡ Analyser les {perf_count} problème(s) de performance")

        if ux_count > 0:
            actions.append(f"🎨 Revoir les {ux_count} point(s) UX problématiques")

        if feature_count > 0:
            actions.append(f"✨ Évaluer les {feature_count} demande(s) de fonctionnalité")

        # Actions basées sur le score
        if self.interview_state.satisfaction_score:
            if self.interview_state.satisfaction_score < 5:
                actions.append("🚨 Contact prioritaire - utilisateur insatisfait")
            elif self.interview_state.satisfaction_score >= 8:
                actions.append("⭐ Candidat pour témoignage client")

        return actions

    def generate_report(self) -> str:
        """Génère le rapport UX Research"""
        self.interview_state.action_items = self._generate_action_items()

        # Grouper feedbacks par type
        bugs = [f for f in self.interview_state.feedbacks if f.type == FeedbackType.BUG]
        features = [f for f in self.interview_state.feedbacks if f.type == FeedbackType.FEATURE_REQUEST]
        ux_issues = [f for f in self.interview_state.feedbacks if f.type == FeedbackType.UX_ISSUE]
        perf_issues = [f for f in self.interview_state.feedbacks if f.type == FeedbackType.PERFORMANCE]
        praises = [f for f in self.interview_state.feedbacks if f.type == FeedbackType.PRAISE]

        report = f"""## 📊 Rapport UX Research

**Date** : {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Produit(s) évalué(s)** : {', '.join(self.interview_state.products_discussed) or 'Non spécifié'}
**Échanges** : {self.interview_state.total_exchanges}

---

### 🎯 Usage Principal
"""
        if self.interview_state.products_discussed:
            for product in self.interview_state.products_discussed:
                product_info = next((p for p in IAFACTORY_PRODUCTS.values() if p["name"] == product), None)
                if product_info:
                    report += f"- **{product}** : {product_info['description']}\n"
        else:
            report += "- Produits non identifiés clairement\n"

        report += f"""
---

### 😤 Points de Friction ({len(bugs) + len(ux_issues) + len(perf_issues)} détectés)

#### 🐛 Bugs ({len(bugs)})
"""
        for bug in bugs[:5]:
            report += f"- {bug.description} (Sévérité: {bug.severity}/5)\n"
            if bug.verbatim:
                report += f'  > "{bug.verbatim[:100]}..."\n'

        report += f"""
#### 🎨 Problèmes UX ({len(ux_issues)})
"""
        for ux in ux_issues[:5]:
            report += f"- {ux.description}\n"

        report += f"""
#### ⚡ Performance ({len(perf_issues)})
"""
        for perf in perf_issues[:5]:
            report += f"- {perf.description}\n"

        report += f"""
---

### 💡 Suggestions & Demandes ({len(features)})
"""
        for feature in features[:5]:
            report += f"- {feature.description}\n"
            if feature.verbatim:
                report += f'  > "{feature.verbatim[:100]}..."\n'

        report += f"""
---

### ⭐ Points Positifs ({len(praises)})
"""
        for praise in praises[:5]:
            report += f"- {praise.description}\n"

        report += f"""
---

### 📈 Score Satisfaction
**{self.interview_state.satisfaction_score or '?'}/10**
"""
        if self.interview_state.satisfaction_score:
            if self.interview_state.satisfaction_score >= 8:
                report += "✅ Utilisateur satisfait\n"
            elif self.interview_state.satisfaction_score >= 5:
                report += "🔄 Satisfaction moyenne - points à améliorer\n"
            else:
                report += "⚠️ Utilisateur insatisfait - action requise\n"

        report += f"""
---

### 🔑 Insights Clés
"""
        # Générer insights basés sur les données
        if len(bugs) > 2:
            report += "- ⚠️ Plusieurs bugs signalés - stabilité à améliorer\n"
        if len(features) > 2:
            report += "- 💡 Forte demande de nouvelles fonctionnalités\n"
        if len(praises) > len(bugs + ux_issues):
            report += "- ✅ Retours globalement positifs\n"
        if len(self.interview_state.products_discussed) > 1:
            report += f"- 🔄 Utilisateur multi-produit ({len(self.interview_state.products_discussed)} produits)\n"

        report += f"""
---

### ⚡ Actions Recommandées
"""
        for action in self.interview_state.action_items:
            report += f"- [ ] {action}\n"

        report += f"""
---

### 📝 Verbatims Importants
"""
        for v in self.interview_state.verbatims[:5]:
            report += f'> "{v[:150]}..."\n\n'

        return report

    async def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        Exécute un tour de l'interview UX.

        Args:
            input_data: {
                "message": str,       # Réponse de l'utilisateur
                "action": str,        # "start", "continue", "report"
                "product": str        # Produit à évaluer (optionnel)
            }
        """
        action = input_data.get("action", "continue")

        # Démarrage de l'interview
        if action == "start":
            self.reset_interview()
            initial_product = input_data.get("product")
            if initial_product:
                self.current_product_focus = initial_product
                self.interview_state.products_discussed.append(initial_product)

            products_list = "\n".join([f"- {p['name']}: {p['description']}" for p in list(IAFACTORY_PRODUCTS.values())[:8]])

            welcome = f"""Bonjour ! 👋 Je suis l'assistant UX Research d'IA Factory.

Mon rôle est de recueillir vos retours pour améliorer nos produits. Vos réponses sont précieuses et confidentielles.

**Nos principaux produits :**
{products_list}
...et plus encore !

---

**Pour commencer :**

{PHASE_QUESTIONS[InterviewPhase.ACCUEIL][0]}"""

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
                    "satisfaction_score": self.interview_state.satisfaction_score,
                    "feedbacks_count": len(self.interview_state.feedbacks),
                    "action": "report_generated"
                }
            )

        # Continuer l'interview
        user_message = input_data.get("message", "")

        # Extraire les produits mentionnés
        products = self._extract_products_mentioned(user_message)
        for product in products:
            if product not in self.interview_state.products_discussed:
                self.interview_state.products_discussed.append(product)
                self.current_product_focus = product

        # Détecter les feedbacks
        feedbacks = self._detect_feedback_type(user_message)
        self.interview_state.feedbacks.extend(feedbacks)

        # Extraire le score de satisfaction si présent
        satisfaction = self._extract_satisfaction_score(user_message)
        if satisfaction:
            self.interview_state.satisfaction_score = satisfaction

        # Capturer les verbatims importants
        if len(user_message) > 80:
            self.interview_state.verbatims.append(user_message)

        # Mettre à jour les compteurs
        self.interview_state.phase_exchanges += 1
        self.interview_state.total_exchanges += 1

        # Contexte produit pour le LLM
        product_context = ""
        if self.current_product_focus:
            for pid, pinfo in IAFACTORY_PRODUCTS.items():
                if pinfo["name"] == self.current_product_focus:
                    product_context = f"""
PRODUIT EN FOCUS: {pinfo['name']}
- Description: {pinfo['description']}
- Catégorie: {pinfo['category']}
- Fonctionnalités clés: {', '.join(pinfo['key_features'])}
"""
                    break

        system_prompt = f"""{self._build_system_prompt()}

INTERVIEW EN COURS:
- Phase actuelle: {self.interview_state.current_phase.value}
- Échange dans cette phase: {self.interview_state.phase_exchanges}
- Produits discutés: {', '.join(self.interview_state.products_discussed) or 'Aucun encore'}
{product_context}

QUESTIONS SUGGÉRÉES POUR CETTE PHASE:
{chr(10).join(f'- {q}' for q in PHASE_QUESTIONS[self.interview_state.current_phase])}

FEEDBACKS COLLECTÉS: {len(self.interview_state.feedbacks)}
- Bugs: {len([f for f in self.interview_state.feedbacks if f.type == FeedbackType.BUG])}
- Features: {len([f for f in self.interview_state.feedbacks if f.type == FeedbackType.FEATURE_REQUEST])}
- UX: {len([f for f in self.interview_state.feedbacks if f.type == FeedbackType.UX_ISSUE])}

INSTRUCTIONS:
1. Analyse la réponse de l'utilisateur
2. Identifie les feedbacks importants (bugs, frustrations, suggestions)
3. Pose UNE question de suivi pour creuser
4. Reste empathique si frustration exprimée
5. Ne défends pas le produit, juste écoute et comprends
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Réponse de l'utilisateur:\n\n{user_message}\n\nGénère ta prochaine question (UNE seule, empathique et ouverte):"}
        ]

        response = await self._call_llm(messages)

        # Vérifier si on doit avancer de phase
        should_advance = self._should_advance_phase()
        if should_advance and self.interview_state.current_phase != InterviewPhase.CLOTURE:
            self._advance_phase()
            phase_names = {
                InterviewPhase.EXPLORATION: "Exploration de l'Usage",
                InterviewPhase.FRICTION: "Points de Friction",
                InterviewPhase.SUGGESTIONS: "Suggestions & Besoins",
                InterviewPhase.CLOTURE: "Clôture"
            }
            phase_indicator = f"\n\n---\n**{phase_names.get(self.interview_state.current_phase, self.interview_state.current_phase.value)}**\n"
            response_content = phase_indicator + response['content']
        else:
            response_content = response['content']

        # Check si interview terminée
        is_complete = (
            self.interview_state.current_phase == InterviewPhase.CLOTURE and
            self.interview_state.phase_exchanges >= 2
        )

        if is_complete:
            response_content += "\n\n---\n✅ **Merci pour vos précieux retours !** Tapez 'rapport' pour générer le rapport complet."

        return AgentResponse(
            content=response_content,
            tokens_used=response.get('tokens'),
            metadata={
                "phase": self.interview_state.current_phase.value,
                "exchange": self.interview_state.total_exchanges,
                "feedbacks_count": len(self.interview_state.feedbacks),
                "products_discussed": self.interview_state.products_discussed,
                "is_complete": is_complete
            }
        )


# Export pour découverte CLI
__all__ = ['UXResearchAgent', 'InterviewState', 'FeedbackItem', 'IAFACTORY_PRODUCTS', 'PHASE_QUESTIONS']
