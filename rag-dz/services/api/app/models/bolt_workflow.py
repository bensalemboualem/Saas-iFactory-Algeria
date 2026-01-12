"""
Modèles Pydantic pour le système Bolt SuperPower
"""
from datetime import datetime
from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field, UUID4
from enum import Enum


class WorkflowMode(str, Enum):
    """Mode de workflow"""
    DIRECT = "direct"
    BMAD = "bmad"


class WorkflowStatus(str, Enum):
    """Statut du workflow"""
    PENDING = "pending"
    ORCHESTRATING = "orchestrating"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentStatus(str, Enum):
    """Statut d'exécution d'un agent"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class ExportFormat(str, Enum):
    """Format d'export"""
    ZIP = "zip"
    GITHUB = "github"
    GITLAB = "gitlab"


# ==================== Requêtes ====================

class DirectModeRequest(BaseModel):
    """Requête pour le mode direct"""
    prompt: str = Field(..., min_length=10, description="Prompt de génération")
    tech_stack: Optional[List[str]] = Field(default=None, description="Technologies à utiliser")
    save_to_archon: bool = Field(default=True, description="Sauvegarder dans Archon")
    export_format: ExportFormat = Field(default=ExportFormat.ZIP, description="Format d'export")


class ProjectConstraints(BaseModel):
    """Contraintes du projet"""
    budget: Literal["low", "medium", "high"] = Field(default="medium")
    timeline: str = Field(..., description="Timeline du projet (ex: '2 weeks')")
    team_size: int = Field(default=1, ge=1, description="Taille de l'équipe")


class ProjectPreferences(BaseModel):
    """Préférences du projet"""
    tech_stack: Literal["modern", "stable", "custom"] = Field(default="modern")
    deployment: Literal["cloud", "on-premise", "hybrid"] = Field(default="cloud")
    custom_tech: Optional[List[str]] = Field(default=None)


class BMADWorkflowRequest(BaseModel):
    """Requête pour le mode BMAD orchestré"""
    user_description: str = Field(..., min_length=20, description="Description du projet")
    constraints: ProjectConstraints = Field(..., description="Contraintes du projet")
    preferences: ProjectPreferences = Field(..., description="Préférences techniques")
    agents_to_use: List[str] = Field(
        default=["architect", "pm", "backend", "frontend", "devops", "qa"],
        description="Liste des agents à utiliser"
    )


class ExportZipRequest(BaseModel):
    """Requête pour l'export ZIP"""
    include_docs: bool = Field(default=True, description="Inclure la documentation")
    include_tests: bool = Field(default=True, description="Inclure les tests")
    include_deployment: bool = Field(default=True, description="Inclure les configs de déploiement")


# ==================== Réponses ====================

class AgentExecutionSummary(BaseModel):
    """Résumé d'exécution d'un agent"""
    agent: str = Field(..., description="Nom de l'agent")
    completed_at: Optional[datetime] = Field(None, description="Date de complétion")
    output_summary: Optional[str] = Field(None, description="Résumé de la sortie")
    status: AgentStatus = Field(..., description="Statut de l'agent")
    execution_time_seconds: Optional[int] = Field(None, description="Temps d'exécution")


class WorkflowResponse(BaseModel):
    """Réponse de création de workflow"""
    workflow_id: str = Field(..., description="ID unique du workflow")
    status: WorkflowStatus = Field(..., description="Statut du workflow")
    mode: WorkflowMode = Field(..., description="Mode du workflow")
    archon_project_id: Optional[int] = Field(None, description="ID du projet dans Archon")
    archon_url: Optional[str] = Field(None, description="URL du projet dans Archon")
    estimated_time_seconds: Optional[int] = Field(None, description="Temps estimé")
    message: str = Field(..., description="Message de statut")


class BMADWorkflowResponse(WorkflowResponse):
    """Réponse spécifique au mode BMAD"""
    current_agent: Optional[str] = Field(None, description="Agent en cours d'exécution")
    agents_completed: List[str] = Field(default_factory=list, description="Agents complétés")
    agents_pending: List[str] = Field(default_factory=list, description="Agents en attente")
    live_updates_url: str = Field(..., description="URL pour les mises à jour temps réel")


class DirectWorkflowResponse(WorkflowResponse):
    """Réponse spécifique au mode direct"""
    download_url: Optional[str] = Field(None, description="URL de téléchargement du ZIP")


class WorkflowStatusResponse(BaseModel):
    """Réponse de statut du workflow"""
    workflow_id: str = Field(..., description="ID du workflow")
    mode: WorkflowMode = Field(..., description="Mode du workflow")
    status: WorkflowStatus = Field(..., description="Statut actuel")
    progress_percent: int = Field(..., ge=0, le=100, description="Progression en pourcentage")
    current_step: Optional[str] = Field(None, description="Étape actuelle")
    agents_completed: List[AgentExecutionSummary] = Field(
        default_factory=list,
        description="Agents complétés"
    )
    agents_pending: List[str] = Field(default_factory=list, description="Agents en attente")
    archon_project_id: Optional[int] = Field(None, description="ID projet Archon")
    archon_url: Optional[str] = Field(None, description="URL projet Archon")
    download_url: Optional[str] = Field(None, description="URL de téléchargement")
    errors: List[str] = Field(default_factory=list, description="Erreurs rencontrées")
    created_at: datetime = Field(..., description="Date de création")
    completed_at: Optional[datetime] = Field(None, description="Date de complétion")


# ==================== Modèles Base de Données ====================

class BoltWorkflowDB(BaseModel):
    """Modèle DB pour bolt_workflows"""
    id: int
    workflow_id: str
    mode: WorkflowMode
    user_description: Optional[str] = None
    status: WorkflowStatus
    current_agent: Optional[str] = None
    agents_completed: List[str] = Field(default_factory=list)
    tech_stack: Optional[List[str]] = None
    archon_project_id: Optional[int] = None
    knowledge_source_id: Optional[str] = None
    zip_file_path: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


class AgentExecutionDB(BaseModel):
    """Modèle DB pour agent_executions"""
    id: int
    workflow_id: str
    agent_name: str
    agent_id: str
    status: AgentStatus
    input_context: Optional[Dict[str, Any]] = None
    output_result: Optional[str] = None
    output_summary: Optional[str] = None
    execution_time_seconds: Optional[int] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None

    class Config:
        from_attributes = True


# ==================== Modèles Internes ====================

class AgentTask(BaseModel):
    """Tâche pour un agent"""
    agent_id: str = Field(..., description="ID de l'agent")
    agent_name: str = Field(..., description="Nom de l'agent")
    context: Dict[str, Any] = Field(default_factory=dict, description="Contexte de la tâche")
    previous_results: Optional[Dict[str, Any]] = Field(None, description="Résultats des agents précédents")


class AgentResult(BaseModel):
    """Résultat d'exécution d'un agent"""
    agent_id: str = Field(..., description="ID de l'agent")
    agent_name: str = Field(..., description="Nom de l'agent")
    status: AgentStatus = Field(..., description="Statut")
    output: Optional[str] = Field(None, description="Sortie complète")
    summary: Optional[str] = Field(None, description="Résumé")
    execution_time: Optional[int] = Field(None, description="Temps d'exécution en secondes")
    error: Optional[str] = Field(None, description="Message d'erreur si échec")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Métadonnées additionnelles")


class ProjectSynthesis(BaseModel):
    """Synthèse du projet après orchestration"""
    project_name: str = Field(..., description="Nom du projet")
    description: str = Field(..., description="Description")
    tech_stack: List[str] = Field(..., description="Stack technique")
    architecture: Optional[str] = Field(None, description="Architecture définie")
    requirements: Optional[str] = Field(None, description="Requirements")
    api_design: Optional[str] = Field(None, description="Design API")
    ui_components: Optional[str] = Field(None, description="Composants UI")
    deployment_strategy: Optional[str] = Field(None, description="Stratégie de déploiement")
    test_plan: Optional[str] = Field(None, description="Plan de tests")
    full_documentation: str = Field(..., description="Documentation complète")
    agents_contributions: Dict[str, str] = Field(..., description="Contributions de chaque agent")
