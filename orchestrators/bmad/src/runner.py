"""
BMAD Runner - Moteur d'exécution des agents BMAD
"""

import os
import re
from pathlib import Path
from enum import Enum
from typing import Any
from datetime import datetime

import httpx
from pydantic import BaseModel, Field


# ============ DYNAMIC TEMPLATE HELPERS ============

# Prefixes added by workflow templates - to be stripped for keyword extraction
WORKFLOW_PREFIXES = [
    "Analyze and structure these requirements:",
    "Create a comprehensive PRD for:",
    "Design the technical architecture for:",
    "Design the user experience for:",
    "Create user stories and acceptance criteria for:",
    "Implement the solution for:",
    "Create test plan and test cases for:",
    "Perform security review for:",
    "Create deployment plan for:",
]


def extract_user_task(task: str) -> str:
    """Extract the original user task by removing workflow prefixes"""
    task_clean = (task or "").strip()
    for prefix in WORKFLOW_PREFIXES:
        if task_clean.startswith(prefix):
            task_clean = task_clean[len(prefix):].strip()
            break
    return task_clean


def extract_keywords(task: str) -> list[str]:
    """Extract meaningful keywords from a task description"""
    # First extract the user's original task
    task_clean = extract_user_task(task)

    # Find words 4+ chars, excluding common stop words
    words = re.findall(r"[A-Za-zÀ-ÿ0-9_-]{4,}", task_clean.lower())
    stop_words = {
        # English common words
        "create", "new", "feature", "user", "make", "build", "implement",
        "develop", "want", "need", "should", "would", "could", "please",
        "help", "like", "that", "this", "from", "with", "have", "been",
        "being", "were", "will", "using", "based", "simple", "basic",
        # Workflow template words (backup filter)
        "analyze", "structure", "these", "requirements", "comprehensive",
        "design", "technical", "architecture", "experience", "stories",
        "acceptance", "criteria", "solution", "test", "plan", "cases",
        "security", "review", "deployment",
        # French common words
        "pour", "avec", "dans", "application", "crée", "créer", "faire",
        "ajouter", "nouveau", "nouvelle",
    }
    return [w for w in words if w not in stop_words][:15]


def detect_domain(task: str) -> dict[str, bool]:
    """Detect the domain/context of the task"""
    # Use cleaned task for detection
    lower = extract_user_task(task).lower()
    return {
        "auth": any(w in lower for w in ["login", "logout", "auth", "password", "session", "signup", "signin", "register", "connexion", "inscription"]),
        "payment": any(w in lower for w in ["payment", "pay", "chargily", "invoice", "facture", "paiement", "billing"]),
        "crud": any(w in lower for w in ["crud", "create", "read", "update", "delete", "list", "manage"]),
        "api": any(w in lower for w in ["api", "endpoint", "rest", "graphql"]),
        "ui": any(w in lower for w in ["ui", "ux", "interface", "design", "frontend", "component", "page"]),
        "search": any(w in lower for w in ["search", "filter", "sort", "query", "recherche"]),
        "notification": any(w in lower for w in ["notification", "email", "sms", "alert", "message"]),
        "file": any(w in lower for w in ["file", "upload", "download", "export", "import", "pdf", "csv"]),
        "dashboard": any(w in lower for w in ["dashboard", "stats", "analytics", "report", "tableau"]),
        "dz": any(w in lower for w in ["algérie", "algeria", "dz", "darija", "chargily", "cib", "edahabia"]),
        "frontend": any(w in lower for w in ["react", "vue", "angular", "svelte", "nextjs", "nuxt", "tailwind", "css", "html", "javascript", "typescript", "frontend", "component"]),
        "backend": any(w in lower for w in ["fastapi", "django", "flask", "express", "nestjs", "api", "backend", "server", "database", "postgresql", "mongodb"]),
    }


def get_feature_name(task: str) -> str:
    """Extract a feature name from the task"""
    keywords = extract_keywords(task)
    if keywords:
        return " ".join(keywords[:3]).title()
    return "Feature"


def is_billing_task(task: str) -> bool:
    """Check if task is related to billing/invoicing/payment"""
    # Use cleaned task for detection
    t = extract_user_task(task).lower()
    keys = ["invoice", "facture", "facturation", "paiement", "payment", "chargily", "cib", "edahabia"]
    return any(k in t for k in keys)


class Workflow(str, Enum):
    """Types de workflows BMAD"""
    QUICK = "quick-flow"          # Bugfix, hotfix
    FEATURE = "feature-flow"      # Feature standard
    METHOD = "method-flow"        # Feature complexe
    ENTERPRISE = "enterprise-flow" # Projet enterprise


class Scope(str, Enum):
    """Portée du projet"""
    BUGFIX = "bugfix"
    HOTFIX = "hotfix"
    FEATURE = "feature"
    REFACTOR = "refactor"
    GREENFIELD = "greenfield"
    MIGRATION = "migration"


class Complexity(str, Enum):
    """Niveau de complexité"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    ENTERPRISE = "enterprise"


class AgentResult(BaseModel):
    """Résultat d'exécution d'un agent"""
    agent: str
    status: str  # success, error, skipped
    output: str
    duration_ms: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict = Field(default_factory=dict)


class BMADRunner:
    """
    Runner pour exécuter les agents BMAD.
    Charge les prompts des agents et les exécute via LLM.
    """

    # Mapping agents BMAD standard
    AGENT_ROLES = {
        "analyst": "Business Analyst - Requirements gathering",
        "pm": "Product Manager - PRD creation",
        "architect": "System Architect - Technical design",
        "po": "Product Owner - Story creation",
        "developer": "Developer - Implementation",
        "ux": "UX Designer - User experience",
        "test": "QA Engineer - Testing",
        "security": "Security Auditor - Security review",
        "devops": "DevOps Engineer - Deployment",
    }

    # Prompts par défaut pour agents standard (mode simulation)
    DEFAULT_PROMPTS = {
        "analyst": "Tu es un Business Analyst expert. Analyse les besoins et génère des requirements structurés.",
        "pm": "Tu es un Product Manager. Crée des PRDs détaillés avec objectifs, features et métriques.",
        "architect": "Tu es un Architecte Système. Conçois des architectures scalables et maintenables.",
        "po": "Tu es un Product Owner. Crée des user stories avec critères d'acceptance.",
        "developer": "Tu es un Développeur Senior. Implémente du code propre et testé.",
        "ux": "Tu es un UX Designer. Crée des expériences utilisateur intuitives.",
        "test": "Tu es un QA Engineer. Définis des stratégies de test complètes.",
        "security": "Tu es un Security Auditor. Identifie les vulnérabilités et recommande des corrections.",
        "devops": "Tu es un DevOps Engineer. Automatise les déploiements et le monitoring.",
    }

    def __init__(
        self,
        bmad_path: str | None = None,
        llm_url: str = "http://localhost:8100/llm",
        simulation_mode: bool = False
    ):
        """
        Args:
            bmad_path: Chemin vers le dossier BMAD (contient les agents)
            llm_url: URL du service LLM (via meta-orchestrator)
            simulation_mode: Si True, génère des réponses simulées sans LLM
        """
        self.bmad_path = Path(bmad_path) if bmad_path else None
        self.llm_url = llm_url
        self.simulation_mode = simulation_mode or os.getenv("BMAD_SIMULATION", "false").lower() == "true"
        self.agents: dict[str, str] = {}
        self.custom_agents: dict[str, str] = {}

        # Charger les prompts par défaut
        self.agents = dict(self.DEFAULT_PROMPTS)

        if self.bmad_path and self.bmad_path.exists():
            self._load_agents()

    def _load_agents(self) -> None:
        """Charge les prompts des agents depuis le dossier BMAD"""
        # Chercher dans plusieurs emplacements possibles
        search_paths = [
            self.bmad_path / "src" / "agents",
            self.bmad_path / "agents",
            self.bmad_path / "bmad-agents",
        ]

        for agents_path in search_paths:
            if agents_path.exists():
                for agent_file in agents_path.glob("*.md"):
                    agent_name = agent_file.stem.replace("-agent", "").replace("_agent", "")
                    self.agents[agent_name] = agent_file.read_text(encoding="utf-8")

    def register_custom_agent(self, name: str, prompt: str) -> None:
        """Enregistre un agent custom"""
        self.custom_agents[name] = prompt

    def get_agent_prompt(self, agent_name: str) -> str | None:
        """Récupère le prompt d'un agent"""
        # Priorité aux agents custom
        if agent_name in self.custom_agents:
            return self.custom_agents[agent_name]
        return self.agents.get(agent_name)

    def list_agents(self) -> dict[str, str]:
        """Liste tous les agents disponibles"""
        all_agents = {**self.agents, **self.custom_agents}
        return {
            name: self.AGENT_ROLES.get(name, "Custom agent")
            for name in all_agents
        }

    def recommend_workflow(
        self,
        scope: Scope | str,
        complexity: Complexity | str = Complexity.MODERATE
    ) -> Workflow:
        """
        Recommande un workflow basé sur la portée et complexité.

        Args:
            scope: Portée du projet
            complexity: Niveau de complexité

        Returns:
            Workflow recommandé
        """
        scope = Scope(scope) if isinstance(scope, str) else scope
        complexity = Complexity(complexity) if isinstance(complexity, str) else complexity

        if scope in [Scope.BUGFIX, Scope.HOTFIX]:
            return Workflow.QUICK

        if scope == Scope.FEATURE:
            if complexity == Complexity.SIMPLE:
                return Workflow.QUICK
            if complexity == Complexity.ENTERPRISE:
                return Workflow.ENTERPRISE
            return Workflow.FEATURE

        if scope in [Scope.REFACTOR, Scope.GREENFIELD, Scope.MIGRATION]:
            if complexity == Complexity.ENTERPRISE:
                return Workflow.ENTERPRISE
            return Workflow.METHOD

        return Workflow.FEATURE

    async def run_agent(
        self,
        agent_name: str,
        task: str,
        context: dict | None = None,
        model: str | None = None
    ) -> AgentResult:
        """
        Exécute un agent BMAD sur une tâche.

        Args:
            agent_name: Nom de l'agent
            task: Description de la tâche
            context: Contexte additionnel (résultats précédents, etc.)
            model: Modèle LLM à utiliser (optionnel)

        Returns:
            Résultat de l'exécution
        """
        start_time = datetime.utcnow()

        # Récupérer le prompt de l'agent
        agent_prompt = self.get_agent_prompt(agent_name)
        if not agent_prompt:
            return AgentResult(
                agent=agent_name,
                status="error",
                output=f"Agent '{agent_name}' not found",
                duration_ms=0
            )

        # Mode simulation - génère des réponses structurées
        if self.simulation_mode:
            return self._simulate_agent_response(agent_name, task, context, start_time)

        # Construire le prompt final
        full_prompt = self._build_prompt(agent_prompt, task, context)

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    self.llm_url,
                    json={
                        "prompt": full_prompt,
                        "model": model,
                        "agent": agent_name,
                        "task_type": "bmad"
                    }
                )
                response.raise_for_status()
                result = response.json()

                duration = (datetime.utcnow() - start_time).total_seconds() * 1000

                return AgentResult(
                    agent=agent_name,
                    status="success",
                    output=result.get("response", ""),
                    duration_ms=int(duration),
                    metadata={
                        "model": result.get("model"),
                        "tokens": result.get("tokens")
                    }
                )

        except Exception as e:
            # Fallback to simulation mode if LLM unavailable
            duration = (datetime.utcnow() - start_time).total_seconds() * 1000
            return self._simulate_agent_response(agent_name, task, context, start_time, fallback=True)

    def _simulate_agent_response(
        self,
        agent_name: str,
        task: str,
        context: dict | None,
        start_time: datetime,
        fallback: bool = False
    ) -> AgentResult:
        """Génère une réponse simulée structurée pour un agent"""
        import random
        import time

        # Simuler un délai de traitement
        time.sleep(random.uniform(0.1, 0.3))
        duration = (datetime.utcnow() - start_time).total_seconds() * 1000

        # Réponses simulées par agent
        simulated_responses = {
            "analyst": self._simulate_analyst(task),
            "pm": self._simulate_pm(task),
            "architect": self._simulate_architect(task),
            "po": self._simulate_po(task),
            "developer": self._simulate_developer(task),
            "test": self._simulate_test(task),
            "security": self._simulate_security(task),
            "conformity-dz": self._simulate_conformity_dz(task),
            "darija-content": self._simulate_darija(task),
            "gov-integration": self._simulate_gov(task),
            "chargily-payment": self._simulate_chargily(task),
        }

        output = simulated_responses.get(agent_name, f"[{agent_name}] Tâche analysée: {task[:100]}...")

        return AgentResult(
            agent=agent_name,
            status="success",
            output=output,
            duration_ms=int(duration),
            metadata={
                "mode": "simulation" if not fallback else "fallback",
                "model": "simulated"
            }
        )

    def _simulate_analyst(self, task: str) -> str:
        """Dynamic analyst template based on task content"""
        keywords = extract_keywords(task)
        domain = detect_domain(task)
        feature_name = get_feature_name(task)
        kw_display = ", ".join(keywords[:8]) if keywords else "non spécifiés"


        # Build dynamic requirements based on detected domain
        requirements = []
        rf_num = 1

        if domain["auth"]:
            requirements.append(f"**RF-{rf_num:03d}**: Authentification utilisateur (login/logout/session)")
            rf_num += 1
            requirements.append(f"**RF-{rf_num:03d}**: Gestion des mots de passe (reset, validation)")
            rf_num += 1
        if domain["crud"]:
            requirements.append(f"**RF-{rf_num:03d}**: CRUD complet pour les entités principales")
            rf_num += 1
        if domain["search"]:
            requirements.append(f"**RF-{rf_num:03d}**: Recherche et filtrage des données")
            rf_num += 1
        if domain["notification"]:
            requirements.append(f"**RF-{rf_num:03d}**: Système de notifications (email/in-app)")
            rf_num += 1
        if domain["file"]:
            requirements.append(f"**RF-{rf_num:03d}**: Gestion des fichiers (upload/download)")
            rf_num += 1
        if domain["dashboard"]:
            requirements.append(f"**RF-{rf_num:03d}**: Dashboard avec statistiques")
            rf_num += 1
        # N'ajouter Chargily/DZ que si le prompt concerne la facturation/paiement
        if is_billing_task(task):
            requirements.append(f"**RF-{rf_num:03d}**: Intégration paiement Chargily (DZ)")
            rf_num += 1

        # Default requirement if none detected
        if not requirements:
            requirements.append(f"**RF-001**: Implémentation de {feature_name}")
            requirements.append("**RF-002**: Interface utilisateur intuitive")
            requirements.append("**RF-003**: Validation des données")

        reqs_text = "\n".join(f"{i+1}. {r}" for i, r in enumerate(requirements))

        # DZ constraints only if billing
        dz_section = ""
        if is_billing_task(task):
            dz_section = """
### Contraintes Algérie
- Paiement: Chargily uniquement (CIB/EDAHABIA)
- Langues: FR, AR, Darija
- Conformité: Réglementation DZ"""

        return f"""## Analyse des Requirements

### Contexte
{task}

### Mots-clés détectés
{kw_display}

### Requirements Fonctionnels
{reqs_text}

### Requirements Non-Fonctionnels
- Performance: Temps de réponse < 200ms
- Sécurité: Authentification JWT + validation input
- Disponibilité: 99.9% uptime
- Logs: Audit trail pour actions sensibles{dz_section}"""

    def _simulate_pm(self, task: str) -> str:
        """Dynamic PM/PRD template based on task content"""
        domain = detect_domain(task)
        feature_name = get_feature_name(task)

        # Build dynamic features table
        features = []
        if domain["auth"]:
            features.append(("Authentification JWT", "P0", "M"))
            features.append(("Gestion sessions", "P0", "S"))
        if domain["crud"]:
            features.append(("API REST CRUD", "P0", "M"))
        if domain["search"]:
            features.append(("Recherche/Filtres", "P1", "M"))
        if domain["ui"]:
            features.append(("Interface utilisateur", "P0", "L"))
        if domain["notification"]:
            features.append(("Notifications", "P1", "M"))
        if domain["file"]:
            features.append(("Gestion fichiers", "P1", "M"))
        if domain["dashboard"]:
            features.append(("Dashboard Stats", "P2", "M"))
        if is_billing_task(task):
            features.append(("Intégration Chargily", "P0", "L"))

        # Default features if none detected
        if not features:
            features.append((f"Core {feature_name}", "P0", "M"))
            features.append(("Validation données", "P0", "S"))
            features.append(("Tests unitaires", "P1", "S"))

        features_table = "\n".join(f"| {f[0]} | {f[1]} | {f[2]} |" for f in features)

        # Scope section - only add DZ if relevant
        scope_items = ["- Version MVP avec features essentielles"]
        if domain["auth"]:
            scope_items.append("- Authentification sécurisée")
        if is_billing_task(task):
            scope_items.append("- Support Algérie (paiement Chargily, langues)")
        scope_text = "\n".join(scope_items)

        return f"""# PRD - Document de Requirements Produit

## 1. Objectif
{task}

## 2. Périmètre
{scope_text}

## 3. Features Clés
| Feature | Priorité | Effort |
|---------|----------|--------|
{features_table}

## 4. Métriques de Succès
- Adoption: Objectif à définir selon le contexte
- Qualité: < 1 bug critique/sprint
- Performance: Temps réponse < 200ms"""

    def _simulate_architect(self, task: str) -> str:
        """Dynamic architect template based on task content"""
        domain = detect_domain(task)
        feature_name = get_feature_name(task)

        # Build dynamic endpoints based on domain
        endpoints = []
        if domain["auth"]:
            endpoints.extend([
                "POST /api/v1/auth/login",
                "POST /api/v1/auth/logout",
                "POST /api/v1/auth/register",
                "POST /api/v1/auth/refresh",
                "POST /api/v1/auth/password/reset",
            ])
        if domain["crud"]:
            resource = feature_name.lower().replace(" ", "-")
            endpoints.extend([
                f"GET /api/v1/{resource}",
                f"POST /api/v1/{resource}",
                f"GET /api/v1/{resource}/:id",
                f"PUT /api/v1/{resource}/:id",
                f"DELETE /api/v1/{resource}/:id",
            ])
        if domain["search"]:
            endpoints.append("GET /api/v1/search?q=...")
        if domain["file"]:
            endpoints.extend([
                "POST /api/v1/files/upload",
                "GET /api/v1/files/:id/download",
            ])
        if is_billing_task(task):
            endpoints.extend([
                "POST /api/v1/payments/chargily",
                "POST /api/v1/webhooks/chargily",
            ])

        # Default endpoints if none detected
        if not endpoints:
            endpoints = [
                f"GET /api/v1/{feature_name.lower().replace(' ', '-')}",
                f"POST /api/v1/{feature_name.lower().replace(' ', '-')}",
            ]

        endpoints_text = "\n".join(f"- {e}" for e in endpoints[:8])

        return f"""# Architecture Technique

## Stack Technologique
- **Backend**: FastAPI + Python 3.11
- **Database**: PostgreSQL + Supabase (RLS)
- **Cache**: Redis
- **Frontend**: Next.js 14 + TypeScript

## Diagramme de Composants
```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Frontend   │────▶│   API REST   │────▶│  PostgreSQL │
│  (Next.js)  │     │  (FastAPI)   │     │  (Supabase) │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                    ┌──────┴──────┐
                    │   Redis     │
                    │   (Cache)   │
                    └─────────────┘
```

## Feature: {feature_name}
{task}

## Endpoints API
{endpoints_text}

## Sécurité
- JWT avec refresh tokens
- Validation des inputs (Pydantic)
- Rate limiting: 100 req/min"""

    def _simulate_po(self, task: str) -> str:
        """Dynamic PO/Stories template based on task content"""
        domain = detect_domain(task)
        feature_name = get_feature_name(task)

        stories = []
        us_num = 1

        if domain["auth"]:
            stories.append(f"""### US-{us_num:03d}: Connexion utilisateur
**En tant que** visiteur
**Je veux** me connecter à mon compte
**Afin d'** accéder à mes données

**Critères d'acceptance:**
- [ ] Formulaire email + mot de passe
- [ ] Validation des champs
- [ ] Message d'erreur si échec
- [ ] Redirection après succès""")
            us_num += 1

            stories.append(f"""### US-{us_num:03d}: Inscription utilisateur
**En tant que** visiteur
**Je veux** créer un compte
**Afin de** utiliser l'application

**Critères d'acceptance:**
- [ ] Formulaire d'inscription
- [ ] Validation email unique
- [ ] Mot de passe sécurisé
- [ ] Email de confirmation""")
            us_num += 1

        if domain["crud"] or domain["search"]:
            stories.append(f"""### US-{us_num:03d}: Gestion {feature_name}
**En tant que** utilisateur authentifié
**Je veux** gérer mes {feature_name.lower()}
**Afin de** organiser mes données

**Critères d'acceptance:**
- [ ] Liste avec pagination
- [ ] Création via formulaire
- [ ] Modification et suppression
- [ ] Recherche/filtres""")
            us_num += 1

        if is_billing_task(task):
            stories.append(f"""### US-{us_num:03d}: Paiement via Chargily
**En tant que** utilisateur
**Je veux** effectuer un paiement
**Afin de** finaliser ma transaction

**Critères d'acceptance:**
- [ ] Redirection vers Chargily checkout
- [ ] Support CIB et EDAHABIA
- [ ] Confirmation de paiement
- [ ] Email de reçu""")
            us_num += 1

        # Default story if none generated
        if not stories:
            stories.append(f"""### US-001: {feature_name}
**En tant que** utilisateur
**Je veux** utiliser {feature_name.lower()}
**Afin de** accomplir ma tâche

**Critères d'acceptance:**
- [ ] Interface intuitive
- [ ] Validation des données
- [ ] Feedback utilisateur
- [ ] Gestion des erreurs""")

        stories_text = "\n\n".join(stories)

        return f"""# User Stories

## Epic: {feature_name}

{stories_text}"""

    def _simulate_developer(self, task: str) -> str:
        """Dynamic developer template based on task content"""
        domain = detect_domain(task)
        feature_name = get_feature_name(task)
        model_name = feature_name.replace(" ", "")
        user_task = extract_user_task(task)

        # Generate appropriate code sample based on stack
        if domain["frontend"]:
            # React/Frontend focused code
            component_name = model_name or "App"
            code_sample = f'''```tsx
// components/{component_name}.tsx
import React, {{ useState }} from 'react';

interface {component_name}Props {{
  // Define props
}}

export const {component_name}: React.FC<{component_name}Props> = (props) => {{
  const [items, setItems] = useState<string[]>([]);
  const [input, setInput] = useState('');

  const handleAdd = () => {{
    if (input.trim()) {{
      setItems([...items, input.trim()]);
      setInput('');
    }}
  }};

  return (
    <div className="p-4 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">{feature_name}</h1>
      <div className="flex gap-2 mb-4">
        <input
          type="text"
          value={{input}}
          onChange={{(e) => setInput(e.target.value)}}
          className="flex-1 px-3 py-2 border rounded-lg focus:outline-none focus:ring-2"
          placeholder="Add item..."
        />
        <button
          onClick={{handleAdd}}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
          Add
        </button>
      </div>
      <ul className="space-y-2">
        {{items.map((item, i) => (
          <li key={{i}} className="p-2 bg-gray-100 rounded">{{item}}</li>
        ))}}
      </ul>
    </div>
  );
}};
```'''
            next_steps = [
                "Ajouter la gestion d'état (useState/useReducer)",
                "Implémenter les composants UI avec Tailwind",
                "Ajouter la persistance (localStorage/API)",
                "Tests avec React Testing Library",
            ]
            sprint_setup = "- [x] Setup projet React + Vite\n- [x] Configuration Tailwind CSS"

        elif domain["auth"]:
            code_sample = f'''```python
# models/user.py
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: str
    email: EmailStr
    name: str
    created_at: datetime
    is_active: bool = True

# routes/auth.py
from fastapi import APIRouter, HTTPException
from passlib.hash import bcrypt

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(data: UserLogin):
    # Verify credentials and return JWT
    pass

@router.post("/register")
async def register(data: UserCreate):
    # Create user and send confirmation
    pass
```'''
            next_steps = None
            sprint_setup = None
        elif domain["crud"]:
            code_sample = f'''```python
# models/{model_name.lower()}.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class {model_name}Create(BaseModel):
    name: str
    description: Optional[str] = None

class {model_name}(BaseModel):
    id: str
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

# routes/{model_name.lower()}.py
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/{model_name.lower()}", tags=["{model_name.lower()}"])

@router.get("/")
async def list_{model_name.lower()}s():
    pass

@router.post("/")
async def create_{model_name.lower()}(data: {model_name}Create):
    pass
```'''
            next_steps = None
            sprint_setup = None
        else:
            code_sample = f'''```python
# Feature: {feature_name}
# Task: {user_task[:100]}

from pydantic import BaseModel
from datetime import datetime

class {model_name}(BaseModel):
    id: str
    # Add fields based on requirements
    created_at: datetime

# Implementation TODO:
# 1. Define data models
# 2. Create API endpoints
# 3. Add validation logic
# 4. Write tests
```'''
            next_steps = None
            sprint_setup = None

        # Dynamic next steps (only if not already set by frontend)
        if next_steps is None:
            next_steps = []
            if domain["auth"]:
                next_steps.extend(["Implémenter JWT tokens", "Ajouter password hashing", "Email de confirmation"])
            if domain["crud"]:
                next_steps.extend(["Endpoints CRUD complets", "Validation Pydantic", "Pagination"])
            if is_billing_task(task):
                next_steps.append("Intégration Chargily")
            if not next_steps:
                next_steps = ["Implémenter la logique métier", "Ajouter les validations", "Tests unitaires"]

        # Sprint setup (only if not already set by frontend)
        if sprint_setup is None:
            sprint_setup = "- [x] Setup projet FastAPI\n- [x] Configuration base de données"

        next_steps_text = "\n".join(f"{i+1}. {s}" for i, s in enumerate(next_steps[:5]))

        return f"""# Plan d'Implémentation

## Feature: {feature_name}
{user_task}

## Sprint 1: Foundation
{sprint_setup}
- [ ] Modèles de données
- [ ] Endpoints API
- [ ] Tests

## Code Généré

{code_sample}

## Prochaines étapes
{next_steps_text}"""

    def _simulate_test(self, task: str) -> str:
        """Dynamic test template based on task content"""
        domain = detect_domain(task)
        feature_name = get_feature_name(task)
        user_task = extract_user_task(task)

        # Build dynamic test cases
        test_cases = []
        t_num = 1

        if domain["frontend"]:
            test_cases.extend([
                (f"T-{t_num:03d}", f"Render {feature_name} component", "P0"),
                (f"T-{t_num+1:03d}", "User interaction (click, input)", "P0"),
                (f"T-{t_num+2:03d}", "State updates correctly", "P0"),
                (f"T-{t_num+3:03d}", "Accessibility (ARIA, keyboard)", "P1"),
            ])
            t_num += 4

        if domain["auth"]:
            test_cases.extend([
                (f"T-{t_num:03d}", "Login avec credentials valides", "P0"),
                (f"T-{t_num+1:03d}", "Login avec mauvais password", "P0"),
                (f"T-{t_num+2:03d}", "Inscription nouvel utilisateur", "P0"),
                (f"T-{t_num+3:03d}", "Reset password flow", "P1"),
            ])
            t_num += 4

        if domain["crud"]:
            test_cases.extend([
                (f"T-{t_num:03d}", f"Création {feature_name} valide", "P0"),
                (f"T-{t_num+1:03d}", f"Liste {feature_name} avec pagination", "P0"),
                (f"T-{t_num+2:03d}", f"Mise à jour {feature_name}", "P1"),
                (f"T-{t_num+3:03d}", f"Suppression {feature_name}", "P1"),
            ])
            t_num += 4

        if is_billing_task(task):
            test_cases.extend([
                (f"T-{t_num:03d}", "Paiement Chargily success", "P0"),
                (f"T-{t_num+1:03d}", "Gestion erreur paiement", "P0"),
                (f"T-{t_num+2:03d}", "Webhook Chargily", "P0"),
            ])
            t_num += 3

        if domain["search"]:
            test_cases.extend([
                (f"T-{t_num:03d}", "Recherche avec résultats", "P1"),
                (f"T-{t_num+1:03d}", "Recherche sans résultats", "P1"),
            ])
            t_num += 2

        # Default test cases
        if not test_cases:
            test_cases = [
                ("T-001", f"{feature_name} - cas nominal", "P0"),
                ("T-002", f"{feature_name} - validation erreur", "P0"),
                ("T-003", f"{feature_name} - edge cases", "P1"),
            ]

        test_table = "\n".join(f"| {t[0]} | {t[1]} | {t[2]} |" for t in test_cases[:8])

        # E2E scenarios
        e2e_scenarios = []
        if domain["auth"]:
            e2e_scenarios.append("login complet")
        if domain["crud"]:
            e2e_scenarios.append(f"création {feature_name.lower()}")
        if is_billing_task(task):
            e2e_scenarios.append("paiement Chargily")
        if not e2e_scenarios:
            e2e_scenarios = [f"parcours {feature_name.lower()}"]

        e2e_text = ", ".join(e2e_scenarios)

        # Adjust test frameworks based on stack
        if domain["frontend"]:
            unit_framework = "Jest + React Testing Library"
            integration_desc = "- Component integration tests\n- Mock API calls avec MSW"
        else:
            unit_framework = "pytest + pytest-asyncio"
            integration_desc = "- API endpoints avec TestClient\n- Database avec fixtures"

        return f"""# Stratégie de Test

## Feature: {feature_name}
{user_task}

## Tests Unitaires
- Coverage cible: 80%
- Framework: {unit_framework}

## Tests d'Intégration
{integration_desc}

## Tests E2E
- Playwright pour le frontend
- Scénarios critiques: {e2e_text}

## Cas de Test Prioritaires
| ID | Scénario | Priorité |
|----|----------|----------|
{test_table}"""

    def _simulate_security(self, task: str) -> str:
        return """# Audit de Sécurité

## Vulnérabilités Identifiées
| Sévérité | Issue | Recommandation |
|----------|-------|----------------|
| HIGH | Pas de rate limiting | Ajouter 100 req/min |
| MEDIUM | JWT sans expiration | Ajouter exp: 1h |
| LOW | Headers CORS trop permissifs | Restreindre origins |

## Conformité
- [x] OWASP Top 10 vérifié
- [x] Pas de secrets dans le code
- [x] RLS activé sur Supabase

## Recommandations
1. Activer 2FA pour admins
2. Logger les accès sensibles
3. Chiffrer les données PII"""

    def _simulate_conformity_dz(self, task: str) -> str:
        has_stripe = "stripe" in task.lower()
        has_paypal = "paypal" in task.lower()

        if has_stripe or has_paypal:
            return f"""# Conformité Algérie - ÉCHEC

## Violations Détectées
- ❌ **CRITIQUE**: Utilisation de {'Stripe' if has_stripe else 'PayPal'} détectée
- ⚠️ Stripe/PayPal non autorisés en Algérie

## Actions Requises
1. Remplacer par **Chargily** (seul provider autorisé)
2. Supporter CIB et EDAHABIA
3. Montant minimum: 75 DZD

## Code Correctif
```python
# Remplacer:
# from stripe import Stripe
# Par:
from chargily_pay import ChargilyClient
```"""
        else:
            return """# Conformité Algérie - VALIDÉ

## Vérifications Passées
- ✅ Paiement: Chargily détecté
- ✅ Devise: DZD supporté
- ✅ Langues: FR/AR configurées
- ✅ Pas de providers interdits

## Recommandations
- Ajouter support Darija
- Vérifier RTL pour l'arabe
- Tester avec CIB et EDAHABIA"""

    def _simulate_darija(self, task: str) -> str:
        return """# Localisation Darija

## Traductions Proposées

| Français | Darija | Arabe Phonétique |
|----------|--------|------------------|
| Facture | فاتورة | Fatura |
| Payer | خلص | Khless |
| Total | المجموع | Lmajmou3 |
| Confirmer | أكد | Akked |

## Expressions Courantes
- "Bienvenue" → "Marhba bik"
- "Merci" → "Sahit" / "Barak Allahu fik"
- "Au revoir" → "Bslama"

## Notes Culturelles
- Utiliser le vouvoiement par défaut
- Éviter l'arabe littéraire trop formel"""

    def _simulate_gov(self, task: str) -> str:
        return """# Intégration Gouvernementale DZ

## Systèmes Supportés
| Système | Status | Notes |
|---------|--------|-------|
| CNAS | ⚠️ Partiel | Parser à compléter |
| Sonelgaz | ⚠️ Partiel | API non officielle |
| CNRC | 📋 Planifié | Q2 2025 |
| Impôts | 📋 Planifié | Q3 2025 |

## Prérequis Techniques
- Certificat électronique DZ
- VPN vers réseau gouvernemental
- Signature numérique qualifiée"""

    def _simulate_chargily(self, task: str) -> str:
        return """# Intégration Chargily

## Configuration
```python
CHARGILY_CONFIG = {
    "api_key": "CHARGILY_API_KEY",
    "secret_key": "CHARGILY_SECRET_KEY",
    "mode": "live",  # or "test"
    "currency": "DZD",
    "min_amount": 75,
    "payment_methods": ["CIB", "EDAHABIA"]
}
```

## Endpoints à Implémenter
1. POST /payments/create - Créer un paiement
2. POST /webhooks/chargily - Recevoir les confirmations
3. GET /payments/:id/status - Vérifier le statut

## Flux de Paiement
1. Client clique "Payer"
2. Redirection vers checkout Chargily
3. Client entre ses infos carte
4. Webhook reçu avec statut
5. Mise à jour facture"""

    def _build_prompt(
        self,
        agent_prompt: str,
        task: str,
        context: dict | None = None
    ) -> str:
        """Construit le prompt final pour l'agent"""
        prompt_parts = [
            "# Agent Instructions",
            agent_prompt,
            "",
            "# Current Task",
            task,
        ]

        if context:
            prompt_parts.extend([
                "",
                "# Context from Previous Agents",
            ])
            for agent_name, result in context.items():
                prompt_parts.append(f"\n## {agent_name}:\n{result}")

        return "\n".join(prompt_parts)

    # ============ CONVENIENCE METHODS ============

    async def generate_prd(
        self,
        requirements: str,
        context: dict | None = None
    ) -> AgentResult:
        """Génère un PRD à partir des requirements"""
        return await self.run_agent(
            "pm",
            f"Generate a comprehensive PRD for the following requirements:\n\n{requirements}",
            context
        )

    async def generate_architecture(
        self,
        prd: str,
        context: dict | None = None
    ) -> AgentResult:
        """Génère l'architecture technique à partir du PRD"""
        ctx = context or {}
        ctx["prd"] = prd
        return await self.run_agent(
            "architect",
            f"Design the technical architecture based on this PRD:\n\n{prd}",
            ctx
        )

    async def generate_stories(
        self,
        architecture: str,
        context: dict | None = None
    ) -> AgentResult:
        """Génère les user stories à partir de l'architecture"""
        ctx = context or {}
        ctx["architecture"] = architecture
        return await self.run_agent(
            "po",
            f"Create user stories based on this architecture:\n\n{architecture}",
            ctx
        )

    async def analyze_requirements(
        self,
        raw_input: str,
        context: dict | None = None
    ) -> AgentResult:
        """Analyse et structure les requirements bruts"""
        return await self.run_agent(
            "analyst",
            f"Analyze and structure these requirements:\n\n{raw_input}",
            context
        )

    async def review_security(
        self,
        code_or_design: str,
        context: dict | None = None
    ) -> AgentResult:
        """Effectue une revue de sécurité"""
        return await self.run_agent(
            "security",
            f"Perform a security review of:\n\n{code_or_design}",
            context
        )
