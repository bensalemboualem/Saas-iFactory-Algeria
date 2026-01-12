# Catalogue des Agents IA - RAG-DZ / Nexus AI Platform

**Version:** 2.0.0
**Total Agents:** 40+
**Dernière mise à jour:** Décembre 2024

---

## Vue d'ensemble

Le projet RAG-DZ contient plus de 40 agents IA spécialisés, organisés par domaine d'expertise. Ces agents utilisent différents frameworks (Phidata, LangChain, custom) et peuvent être combinés pour créer des workflows complexes.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           NEXUS AI AGENTS                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   BUSINESS   │  │   FINANCE    │  │    LEGAL     │  │   TEACHING   │     │
│  │   4 agents   │  │   5 agents   │  │   2 agents   │  │   2 agents   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │     RAG      │  │  OPERATORS   │  │  TEMPLATES   │  │     API      │     │
│  │   6 agents   │  │   2 agents   │  │  15 agents   │  │   5 agents   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Agents par Catégorie

### 1. Business Agents

#### 1.1 AI Consultant
| Attribut | Valeur |
|----------|--------|
| **Fichier** | `agents/business/consultant/ai_consultant_agent.py` |
| **Framework** | Phidata |
| **Statut** | 🟢 Fonctionnel |
| **LLM** | GPT-4, Claude |

**Capacités:**
- Analyse de marché
- Recommandations stratégiques
- Études de concurrence
- Plans d'action business

**Utilisation:**
```python
from agents.business.consultant import AIConsultant

agent = AIConsultant(model="gpt-4")
response = agent.analyze_market("Secteur e-commerce Algérie 2024")
```

---

#### 1.2 Customer Support Agent
| Attribut | Valeur |
|----------|--------|
| **Fichier** | `agents/business/customer-support/customer_support_agent.py` |
| **Framework** | Phidata |
| **Statut** | 🟢 Fonctionnel |
| **LLM** | GPT-3.5-turbo, Claude Haiku |

**Capacités:**
- Réponses automatiques
- Escalation intelligente
- Analyse de sentiment
- Base de connaissances intégrée

---

#### 1.3 Data Analyst Agent
| Attribut | Valeur |
|----------|--------|
| **Fichier** | `agents/business/data-analysis/ai_data_analyst.py` |
| **Framework** | Phidata |
| **Statut** | 🟢 Fonctionnel |
| **LLM** | GPT-4 |

**Capacités:**
- Analyse de données
- Génération de rapports
- Visualisations
- Insights automatiques

---

### 2. Finance Agents

#### 2.1 Financial Coach
| Attribut | Valeur |
|----------|--------|
| **Fichier** | `agents/finance/financial_coach.py` |
| **Framework** | Phidata |
| **Statut** | 🟢 Fonctionnel |
| **LLM** | GPT-4 |

**Capacités:**
- Conseils financiers personnalisés
- Planification budgétaire
- Analyse de dépenses
- Recommandations d'investissement

---

#### 2.2 Investment Agent
| Attribut | Valeur |
|----------|--------|
| **Fichier** | `agents/templates/finance-startups/ai_investment_agent/` |
| **Framework** | Custom |
| **Statut** | 🔵 Template |

**Capacités:**
- Analyse de startups
- Due diligence automatisée
- Scoring d'investissement
- Comparaison de deals

---

#### 2.3 Startup Trends Agent
| Attribut | Valeur |
|----------|--------|
| **Fichier** | `agents/templates/finance-startups/ai_startup_trend_analysis_agent/` |
| **Framework** | Custom |
| **Statut** | 🔵 Template |

**Capacités:**
- Analyse de tendances
- Identification de secteurs émergents
- Prédictions de marché

---

### 3. Legal Agents

#### 3.1 Legal Team
| Attribut | Valeur |
|----------|--------|
| **Fichier** | `agents/legal/legal_team.py` |
| **Framework** | Phidata |
| **Statut** | 🟢 Fonctionnel |
| **LLM** | GPT-4 |

**Capacités:**
- Rédaction de contrats
- Analyse juridique
- Conseil sur la conformité
- Recherche dans les textes de loi

**Spécialisation DZ:**
- Code du commerce algérien
- Code civil algérien
- Droit des sociétés DZ

---

### 4. RAG Agents

#### 4.1 Chat PDF
| Attribut | Valeur |
|----------|--------|
| **Fichier** | `agents/rag/chat-pdf/chat_pdf.py` |
| **Framework** | LangChain + Qdrant |
| **Statut** | 🟢 Fonctionnel |

**Capacités:**
- Upload de PDF
- Extraction de contenu
- Q&A sur documents
- Résumés automatiques

**Utilisation:**
```python
from agents.rag.chat_pdf import ChatPDF

agent = ChatPDF()
agent.load_document("rapport.pdf")
response = agent.ask("Quel est le résumé de ce document?")
```

---

#### 4.2 Hybrid Search
| Attribut | Valeur |
|----------|--------|
| **Fichier** | `agents/rag/hybrid-search/main.py` |
| **Framework** | Custom + Qdrant |
| **Statut** | 🟢 Fonctionnel |

**Capacités:**
- Recherche sémantique (vecteurs)
- Recherche full-text (BM25)
- Fusion des résultats
- Reranking

---

#### 4.3 Local RAG
| Attribut | Valeur |
|----------|--------|
| **Fichier** | `agents/rag/local-rag/local_rag_agent.py` |
| **Framework** | Ollama + Qdrant |
| **Statut** | 🟢 Fonctionnel |

**Capacités:**
- RAG entièrement local
- Pas de dépendance cloud
- Support Ollama (Llama, Mistral)
- Embeddings locaux

---

#### 4.4 Voice Support
| Attribut | Valeur |
|----------|--------|
| **Fichier** | `agents/rag/voice-support/customer_support_voice_agent.py` |
| **Framework** | Whisper + Phidata |
| **Statut** | 🟢 Fonctionnel |

**Capacités:**
- Support client vocal
- STT (Whisper)
- TTS (ElevenLabs/OpenAI)
- RAG pour réponses

---

### 5. Teaching Agents

#### 5.1 Teaching Team
| Attribut | Valeur |
|----------|--------|
| **Fichier** | `agents/teaching/teaching_team.py` |
| **Framework** | Phidata |
| **Statut** | 🟢 Fonctionnel |

**Capacités:**
- Création de cours
- Quiz automatiques
- Évaluation des étudiants
- Parcours personnalisés

---

### 6. Real Estate Agents

#### 6.1 Real Estate Team
| Attribut | Valeur |
|----------|--------|
| **Fichier** | `agents/real_estate/real_estate_team.py` |
| **Framework** | Phidata |
| **Statut** | 🟢 Fonctionnel |

**Capacités:**
- Évaluation de biens
- Recherche de propriétés
- Analyse de marché immobilier
- Génération d'annonces

---

### 7. Recruitment Agents

#### 7.1 Recruitment Team
| Attribut | Valeur |
|----------|--------|
| **Fichier** | `agents/recruitment/recruitment_team.py` |
| **Framework** | Phidata |
| **Statut** | 🟢 Fonctionnel |

**Capacités:**
- Screening de CVs
- Matching candidat/poste
- Questions d'entretien
- Évaluation des compétences

---

### 8. Travel Agent

#### 8.1 Travel Agent
| Attribut | Valeur |
|----------|--------|
| **Fichier** | `agents/travel/travel_agent.py` |
| **Framework** | Phidata |
| **Statut** | 🟢 Fonctionnel |

**Capacités:**
- Planification de voyages
- Recherche de vols/hôtels
- Itinéraires personnalisés
- Budget automatique

---

### 9. Operators

#### 9.1 IAFactory Operator
| Attribut | Valeur |
|----------|--------|
| **Fichier** | `agents/iafactory-operator/` |
| **Framework** | Custom |
| **Statut** | 🟢 Fonctionnel |

**Composants:**
```
agents/iafactory-operator/
├── pipeline/
│   ├── analyzer.py      # Analyse des requêtes
│   ├── executor.py      # Exécution des tâches
│   └── planner.py       # Planification
├── tools/
│   └── ...              # Outils spécialisés
└── main.py              # Point d'entrée
```

---

#### 9.2 Video Operator
| Attribut | Valeur |
|----------|--------|
| **Fichier** | `agents/video-operator/` |
| **Framework** | Custom |
| **Statut** | 🟢 Fonctionnel |

**Capacités:**
- Orchestration du pipeline vidéo
- Gestion des providers
- Monitoring de progression
- Gestion des erreurs

---

### 10. API Service Agents

Ces agents sont intégrés directement dans l'API principale.

| Agent | Fichier | Statut |
|-------|---------|--------|
| Email Agent | `services/api/app/services/email_agent_service.py` | 🟢 |
| Voice AI Agent | `services/api/app/services/voice_ai_agent.py` | 🟡 |
| Super Agent Polva | `services/api/app/services/super_agent_polva.py` | 🟡 |
| Agent Memory | `services/api/app/services/agent_memory.py` | 🟢 |

---

### 11. Archon Agents

Agents intégrés dans Archon UI pour la gestion de tâches et documents.

| Agent | Fichier | Statut |
|-------|---------|--------|
| Base Agent | `frontend/archon-ui/python/src/agents/base_agent.py` | 🟢 |
| Document Agent | `frontend/archon-ui/python/src/agents/document_agent.py` | 🟢 |
| RAG Agent | `frontend/archon-ui/python/src/agents/rag_agent.py` | 🟢 |

---

### 12. Template Agents

Ces agents sont des templates réutilisables pour créer de nouveaux agents.

#### Productivity Templates

| Template | Chemin | Description |
|----------|--------|-------------|
| Journalist | `agents/templates/productivity/journalist/` | Agent journaliste |
| Meeting | `agents/templates/productivity/meeting/` | Gestion de réunions |
| Product Launch | `agents/templates/productivity/product-launch/` | Lancement de produit |
| Web Scraping | `agents/templates/productivity/web-scraping/` | Scraping web |
| XAI Finance | `agents/templates/productivity/xai-finance/` | Finance explicable |

#### RAG Apps Templates

| Template | Chemin | Description |
|----------|--------|-------------|
| Agentic RAG | `agents/templates/rag-apps/agentic_rag_with_reasoning/` | RAG avec raisonnement |
| Autonomous RAG | `agents/templates/rag-apps/autonomous_rag/` | RAG autonome |
| Hybrid Search | `agents/templates/rag-apps/hybrid_search_rag/` | Recherche hybride |
| Local RAG | `agents/templates/rag-apps/local_rag_agent/` | RAG local |
| RAG as Service | `agents/templates/rag-apps/rag-as-a-service/` | RAG en service |

---

## Architecture des Agents

### Base Agent

Tous les agents héritent d'une classe de base commune:

```python
# agents/core/base_agent.py

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class BaseAgent(ABC):
    """Classe de base pour tous les agents."""

    def __init__(
        self,
        model: str = "gpt-4",
        temperature: float = 0.7,
        memory: bool = True,
        tools: Optional[list] = None
    ):
        self.model = model
        self.temperature = temperature
        self.memory = memory
        self.tools = tools or []

    @abstractmethod
    async def run(self, input: str, context: Optional[Dict] = None) -> Any:
        """Exécute l'agent avec l'input donné."""
        pass

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Retourne le system prompt de l'agent."""
        pass

    async def with_tools(self, tools: list) -> "BaseAgent":
        """Ajoute des outils à l'agent."""
        self.tools.extend(tools)
        return self
```

### Agent avec Mémoire

```python
from agents.core.base_agent import BaseAgent
from services.api.app.services.agent_memory import AgentMemory

class MemoryAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.memory = AgentMemory()

    async def run(self, input: str, context: Optional[Dict] = None) -> Any:
        # Récupérer le contexte de la mémoire
        history = await self.memory.get_relevant_context(input)

        # Exécuter avec contexte
        response = await self._execute(input, history, context)

        # Sauvegarder dans la mémoire
        await self.memory.save(input, response)

        return response
```

---

## Création d'un Nouvel Agent

### 1. Créer le fichier agent

```python
# agents/my_domain/my_agent.py

from agents.core.base_agent import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_system_prompt(self) -> str:
        return """
        Tu es un assistant spécialisé dans [DOMAINE].
        Tu dois:
        1. [Tâche 1]
        2. [Tâche 2]
        3. [Tâche 3]
        """

    async def run(self, input: str, context: Optional[Dict] = None) -> Any:
        # Implémentation
        pass
```

### 2. Ajouter des outils

```python
from phi.tools import tool

@tool
def my_custom_tool(query: str) -> str:
    """Description de l'outil."""
    # Implémentation
    return result

class MyAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(tools=[my_custom_tool], **kwargs)
```

### 3. Enregistrer l'agent

```python
# agents/__init__.py

from agents.my_domain.my_agent import MyAgent

AVAILABLE_AGENTS = {
    # ...existing agents...
    "my_agent": MyAgent,
}
```

---

## Configuration des Agents

### Variables d'Environnement

```bash
# LLM par défaut
DEFAULT_LLM_MODEL=gpt-4
DEFAULT_TEMPERATURE=0.7

# Mémoire
AGENT_MEMORY_ENABLED=true
AGENT_MEMORY_BACKEND=redis  # redis, qdrant, supabase

# Rate limiting
AGENT_MAX_TOKENS=8000
AGENT_RATE_LIMIT=100  # requests per minute
```

### Configuration YAML

```yaml
# config/agents.yaml

agents:
  ai_consultant:
    model: gpt-4
    temperature: 0.7
    max_tokens: 4000
    tools:
      - web_search
      - calculator

  customer_support:
    model: gpt-3.5-turbo
    temperature: 0.5
    max_tokens: 2000
    knowledge_base: customer_support_kb
```

---

## Métriques et Monitoring

### Métriques par Agent

| Métrique | Description |
|----------|-------------|
| `agent_requests_total` | Nombre total de requêtes |
| `agent_latency_seconds` | Latence moyenne |
| `agent_tokens_used` | Tokens consommés |
| `agent_errors_total` | Nombre d'erreurs |
| `agent_cost_usd` | Coût en USD |

### Dashboard

Accéder aux métriques via:
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`

---

## Bonnes Pratiques

### 1. System Prompts

- Être spécifique et concis
- Définir clairement le rôle
- Lister les contraintes
- Inclure des exemples

### 2. Gestion de la Mémoire

- Limiter la taille de l'historique
- Utiliser la mémoire sémantique pour les gros volumes
- Nettoyer régulièrement

### 3. Gestion des Erreurs

```python
from agents.core.exceptions import AgentError, RateLimitError

try:
    response = await agent.run(input)
except RateLimitError:
    await asyncio.sleep(60)
    response = await agent.run(input)
except AgentError as e:
    logger.error(f"Agent error: {e}")
    raise
```

### 4. Tests

```python
# tests/agents/test_my_agent.py

import pytest
from agents.my_domain.my_agent import MyAgent

@pytest.mark.asyncio
async def test_my_agent_basic():
    agent = MyAgent(model="gpt-3.5-turbo")
    response = await agent.run("Test input")
    assert response is not None
    assert len(response) > 0
```

---

*Catalogue des agents généré le 31 décembre 2024*
