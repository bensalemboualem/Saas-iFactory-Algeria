"""
Conflict Resolver - Résolution des conflits entre orchestrateurs
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class ConflictType(str, Enum):
    """Types de conflits possibles"""
    FILE_CREATION = "file_creation"
    FILE_MODIFICATION = "file_modification"
    DOCUMENTATION = "documentation"
    KNOWLEDGE_UPDATE = "knowledge_update"
    TASK_STATUS = "task_status"
    CODE_VALIDATION = "code_validation"
    DEPLOYMENT = "deployment"


class Agent(str, Enum):
    """Agents orchestrateurs"""
    BOLT = "bolt"
    BMAD = "bmad"
    ARCHON = "archon"
    VALIDATOR = "validator"
    SECURITY = "security"


# Règles de priorité par type de conflit
# L'ordre définit la priorité (premier = plus prioritaire)
PRIORITY_RULES: dict[ConflictType, list[str]] = {
    # Bolt est le SEUL qui peut écrire du code
    ConflictType.FILE_CREATION: ["bolt"],
    ConflictType.FILE_MODIFICATION: ["bolt"],

    # BMAD gère la documentation métier
    ConflictType.DOCUMENTATION: ["bmad", "archon", "bolt"],

    # Archon est la source de vérité pour KB
    ConflictType.KNOWLEDGE_UPDATE: ["archon"],

    # Archon gère les statuts de tâches
    ConflictType.TASK_STATUS: ["archon"],

    # Validator et Security ont droit de veto
    ConflictType.CODE_VALIDATION: ["validator", "security", "bmad"],

    # Déploiement nécessite validation
    ConflictType.DEPLOYMENT: ["validator", "bolt"],
}

# Agents avec droit de VETO
VETO_AGENTS = {"validator", "security"}


class Resolution(BaseModel):
    """Résultat d'une résolution de conflit"""
    conflict_type: ConflictType
    winner: str
    losers: list[str]
    timestamp: datetime
    reasoning: str
    veto_possible: bool = False
    veto_by: list[str] = []


class VetoError(Exception):
    """Exception levée lors d'un veto"""
    def __init__(self, agent: str, reason: str):
        self.agent = agent
        self.reason = reason
        super().__init__(f"VETO by {agent}: {reason}")


class ConflictResolver:
    """Résolveur de conflits entre orchestrateurs"""

    def resolve(
        self,
        conflict_type: ConflictType,
        contestants: list[str],
        context: dict | None = None
    ) -> Resolution:
        """
        Résout un conflit entre plusieurs agents.

        Args:
            conflict_type: Type de conflit
            contestants: Liste des agents en conflit
            context: Contexte additionnel

        Returns:
            Resolution avec le gagnant et les perdants
        """
        priority = PRIORITY_RULES.get(conflict_type, contestants)

        # Trouver le gagnant selon la priorité
        winner = None
        for agent in priority:
            if agent in contestants:
                winner = agent
                break

        # Si aucun agent prioritaire, prendre le premier
        if not winner:
            winner = contestants[0]

        losers = [c for c in contestants if c != winner]

        # Vérifier si un veto est possible
        veto_possible = any(agent in VETO_AGENTS for agent in contestants)
        veto_agents = [agent for agent in contestants if agent in VETO_AGENTS]

        return Resolution(
            conflict_type=conflict_type,
            winner=winner,
            losers=losers,
            timestamp=datetime.utcnow(),
            reasoning=f"Priority rule: {priority[:3]}...",
            veto_possible=veto_possible,
            veto_by=veto_agents
        )

    def check_single_writer(self, agent: str, operation: str) -> bool:
        """
        Vérifie si l'agent respecte la règle Single-Writer.
        Seul Bolt peut écrire du code.

        Returns:
            True si autorisé, False sinon
        """
        write_operations = {"create", "modify", "delete", "write", "edit"}

        if operation.lower() in write_operations:
            return agent == Agent.BOLT.value

        return True

    def can_veto(self, agent: str, conflict_type: ConflictType) -> bool:
        """Vérifie si un agent peut exercer son droit de veto"""
        if agent not in VETO_AGENTS:
            return False

        # Validator peut veto sur la validation de code
        if agent == "validator" and conflict_type == ConflictType.CODE_VALIDATION:
            return True

        # Security peut veto sur tout ce qui touche au code
        if agent == "security" and conflict_type in [
            ConflictType.FILE_CREATION,
            ConflictType.FILE_MODIFICATION,
            ConflictType.CODE_VALIDATION,
            ConflictType.DEPLOYMENT
        ]:
            return True

        return False

    def apply_veto(
        self,
        resolution: Resolution,
        agent: str,
        reason: str
    ) -> Resolution:
        """
        Applique un veto à une résolution.

        Raises:
            VetoError: Si le veto est appliqué
        """
        if not self.can_veto(agent, resolution.conflict_type):
            return resolution

        raise VetoError(agent, reason)

    def get_write_permission(self, agent: str, path: str) -> dict:
        """
        Retourne les permissions d'écriture pour un agent sur un chemin.

        Returns:
            Dict avec allowed, requires_validation, validators
        """
        # Seul Bolt peut écrire du code
        if agent != Agent.BOLT.value:
            return {
                "allowed": False,
                "reason": "Only bolt-executor can write code",
                "requires_validation": False,
                "validators": []
            }

        # Vérifier les chemins protégés
        protected_critical = [
            "migrations/", "auth/", "services/chargily/", "agents/gov/"
        ]
        protected_important = ["config/", "middleware/", "models/"]

        validators = []

        for p in protected_critical:
            if path.startswith(p):
                validators = ["security", "validator"]
                break

        if not validators:
            for p in protected_important:
                if path.startswith(p):
                    validators = ["validator"]
                    break

        return {
            "allowed": True,
            "reason": "bolt-executor authorized",
            "requires_validation": len(validators) > 0,
            "validators": validators
        }
