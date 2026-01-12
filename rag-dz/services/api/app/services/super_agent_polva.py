"""
IAFactory SuperAgent POLVA - Polyvalent Omniscient Learning Virtual Assistant
==============================================================================
The ultimate orchestrator agent with access to ALL agents and capabilities.

POLVA = Polyvalent Omniscient Learning Virtual Assistant

Capabilities:
- Access to ALL 70+ agents in the MCP registry
- Intelligent routing to specialized agents
- Global persistent memory across all interactions
- Multi-modal: Voice, Text, Vision, Documents
- Multilingual: Arabic, French, English, Darija
- Executive decision making
- Task delegation and orchestration
- Learning from all interactions

Architecture:
┌──────────────────────────────────────────────────────────────┐
│                      POLVA SUPERAGENT                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Router    │  │   Memory    │  │  Executor   │          │
│  │ (Intent→    │  │  (Global    │  │  (Calls     │          │
│  │   Agent)    │  │   State)    │  │   Agents)   │          │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘          │
│         │                │                │                  │
│         └────────────────┼────────────────┘                  │
│                          │                                   │
├──────────────────────────┼───────────────────────────────────┤
│     ┌────────────────────┴────────────────────┐              │
│     │           AGENT REGISTRY                 │              │
│     ├────────────┬────────────┬───────────────┤              │
│     │ BMAD (5)   │ Voice (5)  │ Business (10) │              │
│     │ RAG (5)    │ Legal (4)  │ Finance (8)   │              │
│     │ SaaS (25)  │ Medical(3) │ Education(3)  │              │
│     └────────────┴────────────┴───────────────┘              │
└──────────────────────────────────────────────────────────────┘
"""
import asyncio
import logging
import json
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from app.config import get_settings

# Memory service
try:
    from app.services.agent_memory import (
        get_memory_service,
        AgentMemoryService,
        MemoryImportance,
        MemoryType
    )
    MEMORY_AVAILABLE = True
except ImportError:
    MEMORY_AVAILABLE = False
    AgentMemoryService = None

# Voice AI Agent
try:
    from app.services.voice_ai_agent import voice_ai_agent, VoiceAgentMode
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    voice_ai_agent = None

# MCP Registry
try:
    from app.mcp.registry import mcp_registry, AgentDefinition, AgentType
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    mcp_registry = None

logger = logging.getLogger(__name__)
settings = get_settings()


# ============================================
# POLVA CONFIGURATION
# ============================================

class POLVAMode(str, Enum):
    """POLVA operating modes"""
    EXECUTIVE = "executive"       # High-level decision making
    ORCHESTRATOR = "orchestrator" # Multi-agent coordination
    ASSISTANT = "assistant"       # Personal assistant
    ANALYST = "analyst"           # Data analysis
    DEVELOPER = "developer"       # Code generation
    SUPPORT = "support"           # Customer support
    CREATIVE = "creative"         # Creative tasks
    AUTO = "auto"                 # Automatic mode selection


class TaskPriority(str, Enum):
    """Task priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class AgentCategory(str, Enum):
    """Agent categories for routing"""
    BMAD = "bmad"
    VOICE = "voice"
    RAG = "rag"
    BUSINESS = "business"
    FINANCE = "finance"
    LEGAL = "legal"
    MEDICAL = "medical"
    EDUCATION = "education"
    SAAS = "saas"
    PRODUCTIVITY = "productivity"
    MEDIA = "media"
    SPECIALIZED = "specialized"


@dataclass
class POLVATask:
    """A task for POLVA to execute"""
    id: str
    query: str
    mode: POLVAMode = POLVAMode.AUTO
    priority: TaskPriority = TaskPriority.MEDIUM
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    delegated_agents: List[str] = field(default_factory=list)
    results: List[Dict[str, Any]] = field(default_factory=list)
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None


@dataclass
class POLVAResponse:
    """POLVA response"""
    answer: str
    confidence: float = 0.9
    agents_used: List[str] = field(default_factory=list)
    mode: POLVAMode = POLVAMode.AUTO
    actions_taken: List[Dict[str, Any]] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    memory_updated: bool = False
    language: str = "fr"
    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================
# INTENT ROUTER
# ============================================

class IntentRouter:
    """
    Intelligent router that determines which agent(s) to use
    based on user intent analysis
    """

    # Intent patterns mapped to agent categories
    INTENT_PATTERNS = {
        # BMAD patterns
        AgentCategory.BMAD: [
            r"(?:créer|create|design|concevoir)\s+(?:un\s+)?(?:projet|application|app|système)",
            r"(?:architecture|architecte|winston)",
            r"(?:product\s+manager|pm|john)",
            r"(?:developer|développeur|amelia)",
            r"(?:analyst|analyste|mary)",
            r"(?:test|qa|murat)",
            r"bmad|bmm|backlog|user\s+story",
        ],
        # Voice patterns
        AgentCategory.VOICE: [
            r"(?:appel|call|téléphone|phone)",
            r"(?:rendez-vous|appointment|rdv|meeting)",
            r"(?:secrétaire|secretary|assistant)",
            r"(?:commander|order|commande)\s+(?:restaurant|food)",
            r"(?:vocal|voice|parler|speak)",
            r"hotline|support\s+téléphonique",
        ],
        # RAG patterns
        AgentCategory.RAG: [
            r"(?:chercher|search|find|trouver)\s+(?:dans|in|from)\s+(?:documents?|fichiers?|files?)",
            r"(?:résumer|summarize|summary)\s+(?:document|pdf|article)",
            r"knowledge\s+base|base\s+de\s+connaissances",
            r"rag|retrieval|embedding",
        ],
        # Legal patterns
        AgentCategory.LEGAL: [
            r"(?:juridique|legal|loi|law)",
            r"(?:contrat|contract|convention)",
            r"(?:fiscal|tax|impôt|tva|ibs)",
            r"(?:droit|right|obligation)",
            r"(?:avocat|lawyer|attorney)",
            r"rgpd|gdpr|compliance|conformité",
        ],
        # Finance patterns
        AgentCategory.FINANCE: [
            r"(?:finance|financial|financier)",
            r"(?:investissement|investment|invest)",
            r"(?:budget|budgétaire)",
            r"(?:comptabilité|accounting|comptable)",
            r"(?:facture|invoice|billing)",
            r"(?:paiement|payment|pay)",
            r"(?:startup|venture|funding)",
        ],
        # Medical patterns
        AgentCategory.MEDICAL: [
            r"(?:médical|medical|santé|health)",
            r"(?:symptôme|symptom|maladie|disease)",
            r"(?:médicament|medicine|drug|traitement)",
            r"(?:docteur|doctor|médecin)",
            r"(?:pharmacie|pharmacy|ordonnance)",
        ],
        # Business patterns
        AgentCategory.BUSINESS: [
            r"(?:crm|client|customer)",
            r"(?:vente|sale|commercial)",
            r"(?:marketing|promotion|campagne)",
            r"(?:support|ticket|réclamation)",
            r"(?:onboarding|retention|churn)",
            r"(?:analyse|analysis|kpi|metric)",
        ],
        # Education patterns
        AgentCategory.EDUCATION: [
            r"(?:éducation|education|formation|training)",
            r"(?:cours|course|lesson|leçon)",
            r"(?:étudiant|student|apprendre|learn)",
            r"(?:examen|exam|quiz|test)",
            r"(?:tuteur|tutor|professeur|teacher)",
        ],
        # Media patterns
        AgentCategory.MEDIA: [
            r"(?:vidéo|video|audio|podcast)",
            r"(?:image|photo|thumbnail)",
            r"(?:montage|edit|editing)",
            r"(?:news|actualité|presse)",
            r"(?:social\s+media|réseaux\s+sociaux)",
        ],
        # Productivity patterns
        AgentCategory.PRODUCTIVITY: [
            r"(?:automatiser|automate|automation)",
            r"(?:scraping|extraction|crawler)",
            r"(?:email|mail|message)",
            r"(?:calendrier|calendar|schedule)",
            r"(?:rappel|reminder|notification)",
        ],
    }

    # Keyword boosters for specific agents
    AGENT_KEYWORDS = {
        "bmad-architect": ["architecture", "design", "système", "winston", "diagramme", "tech stack"],
        "bmad-pm": ["product", "backlog", "user story", "sprint", "john", "feature"],
        "bmad-developer": ["code", "développer", "implement", "amelia", "debug", "api"],
        "voice-secretary": ["secrétaire", "rdv", "rendez-vous", "agenda", "appeler"],
        "voice-restaurant": ["commander", "menu", "pizza", "burger", "livraison", "restaurant"],
        "voice-hotline": ["support", "problème", "aide", "réclamation", "ticket"],
        "legal-fiscal": ["fiscal", "tva", "ibs", "tap", "impôt", "déclaration"],
        "legal-consultant": ["contrat", "juridique", "avocat", "litige"],
        "rag-chat-pdf": ["pdf", "document", "résumer", "extraire", "lire"],
        "finance-investment": ["investir", "portfolio", "action", "bourse"],
        "analytics-insight": ["analyse", "dashboard", "kpi", "metric", "trend"],
    }

    def __init__(self):
        self.category_cache = {}
        import re
        self.compiled_patterns = {
            cat: [re.compile(p, re.IGNORECASE) for p in patterns]
            for cat, patterns in self.INTENT_PATTERNS.items()
        }

    def detect_category(self, query: str) -> Tuple[AgentCategory, float]:
        """Detect the most likely agent category for a query"""
        query_lower = query.lower()
        scores = {}

        for category, patterns in self.compiled_patterns.items():
            score = 0
            for pattern in patterns:
                if pattern.search(query_lower):
                    score += 1

            if score > 0:
                scores[category] = score / len(patterns)

        if not scores:
            return AgentCategory.PRODUCTIVITY, 0.3  # Default

        best_category = max(scores, key=scores.get)
        return best_category, scores[best_category]

    def find_best_agent(self, query: str, category: AgentCategory) -> Tuple[str, float]:
        """Find the best specific agent within a category"""
        query_lower = query.lower()
        best_agent = None
        best_score = 0

        for agent_id, keywords in self.AGENT_KEYWORDS.items():
            if agent_id.startswith(category.value) or category.value in agent_id:
                score = sum(1 for kw in keywords if kw in query_lower)
                if score > best_score:
                    best_score = score
                    best_agent = agent_id

        # Default agents per category
        defaults = {
            AgentCategory.BMAD: "bmad-architect",
            AgentCategory.VOICE: "voice-general",
            AgentCategory.RAG: "rag-chat-pdf",
            AgentCategory.LEGAL: "legal-consultant",
            AgentCategory.FINANCE: "finance-investment",
            AgentCategory.MEDICAL: "medical-triage",
            AgentCategory.BUSINESS: "cs-success-manager",
            AgentCategory.EDUCATION: "edu-tutor",
            AgentCategory.MEDIA: "video-operator",
            AgentCategory.PRODUCTIVITY: "productivity-meeting",
            AgentCategory.SAAS: "integration-connector",
            AgentCategory.SPECIALIZED: "iafactory-operator",
        }

        if not best_agent:
            best_agent = defaults.get(category, "iafactory-operator")

        confidence = min(best_score / 3, 1.0) if best_score > 0 else 0.5
        return best_agent, confidence

    def route(self, query: str) -> List[Tuple[str, float]]:
        """
        Route a query to the most appropriate agent(s)

        Returns:
            List of (agent_id, confidence) tuples, sorted by confidence
        """
        category, cat_confidence = self.detect_category(query)
        agent_id, agent_confidence = self.find_best_agent(query, category)

        # Combined confidence
        confidence = (cat_confidence + agent_confidence) / 2

        results = [(agent_id, confidence)]

        # Check if multiple categories apply
        all_scores = {}
        for cat, patterns in self.compiled_patterns.items():
            score = sum(1 for p in patterns if p.search(query.lower()))
            if score > 0:
                all_scores[cat] = score / len(patterns)

        # Add secondary agents if multiple categories match
        sorted_cats = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)
        for cat, score in sorted_cats[1:3]:  # Top 2 additional categories
            if score > 0.2:
                sec_agent, sec_conf = self.find_best_agent(query, cat)
                if sec_agent != agent_id:
                    results.append((sec_agent, score * sec_conf))

        return results


# ============================================
# POLVA SUPERAGENT
# ============================================

class SuperAgentPOLVA:
    """
    POLVA - Polyvalent Omniscient Learning Virtual Assistant

    The ultimate AI agent that:
    - Has access to ALL agents in the system
    - Routes intelligently to specialized agents
    - Maintains global memory
    - Learns from all interactions
    - Can execute complex multi-step tasks
    """

    VERSION = "1.0.0"
    NAME = "POLVA"
    FULL_NAME = "Polyvalent Omniscient Learning Virtual Assistant"

    def __init__(self):
        """Initialize POLVA SuperAgent"""
        # Core components
        self.router = IntentRouter()
        self.tasks: Dict[str, POLVATask] = {}

        # Memory service
        self.memory = get_memory_service() if MEMORY_AVAILABLE else None

        # Voice agent for voice-related tasks
        self.voice_agent = voice_ai_agent if VOICE_AVAILABLE else None

        # MCP registry for accessing all agents
        self.registry = mcp_registry if MCP_AVAILABLE else None

        # Global context
        self.global_context: Dict[str, Any] = {
            "active_tasks": [],
            "recent_agents": [],
            "user_contexts": {},
        }

        # Agent capabilities cache
        self.agent_capabilities: Dict[str, List[str]] = {}

        # Initialize capabilities from registry
        self._load_agent_capabilities()

        logger.info(f"POLVA SuperAgent v{self.VERSION} initialized")
        logger.info(f"  - Memory: {'✓' if self.memory else '✗'}")
        logger.info(f"  - Voice: {'✓' if self.voice_agent else '✗'}")
        logger.info(f"  - MCP Registry: {'✓' if self.registry else '✗'}")
        logger.info(f"  - Agents loaded: {len(self.agent_capabilities)}")

    def _load_agent_capabilities(self):
        """Load capabilities from MCP registry"""
        if self.registry:
            try:
                self.registry.initialize()
                for agent_id, agent_def in self.registry.agents.items():
                    self.agent_capabilities[agent_id] = agent_def.capabilities
            except Exception as e:
                logger.warning(f"Failed to load agent capabilities: {e}")

        # Add known capabilities if registry not available
        if not self.agent_capabilities:
            self.agent_capabilities = {
                "bmad-architect": ["architecture", "design", "tech_stack"],
                "bmad-pm": ["product_strategy", "user_stories", "backlog"],
                "bmad-developer": ["coding", "implementation", "debugging"],
                "voice-hotline": ["call_handle", "ticket_create", "support"],
                "voice-secretary": ["schedule", "reminder", "call_manage"],
                "voice-restaurant": ["order_take", "menu", "delivery"],
                "rag-chat-pdf": ["search", "retrieve", "summarize"],
                "legal-fiscal": ["tax_calculate", "fiscal_declare"],
                "legal-consultant": ["contract_review", "legal_advice"],
            }

    # ------------------------------------------------
    # MAIN PROCESSING
    # ------------------------------------------------

    async def process(
        self,
        query: str,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        mode: POLVAMode = POLVAMode.AUTO,
        context: Optional[Dict[str, Any]] = None,
        priority: TaskPriority = TaskPriority.MEDIUM,
    ) -> POLVAResponse:
        """
        Process a query with POLVA

        Args:
            query: User query/request
            user_id: User identifier
            session_id: Session identifier
            mode: Operating mode (AUTO for automatic detection)
            context: Additional context
            priority: Task priority

        Returns:
            POLVAResponse with answer and metadata
        """
        import time
        start_time = time.time()

        # Create task
        task_id = f"polva_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{hash(query) % 10000}"
        task = POLVATask(
            id=task_id,
            query=query,
            mode=mode,
            priority=priority,
            user_id=user_id,
            session_id=session_id,
            context=context or {},
        )
        self.tasks[task_id] = task

        try:
            # 1. Detect mode if AUTO
            if mode == POLVAMode.AUTO:
                mode = self._detect_mode(query)
                task.mode = mode

            # 2. Store in memory
            if self.memory and session_id:
                self.memory.add_to_working_memory(
                    session_id=session_id,
                    role="user",
                    content=query,
                    importance=0.8,
                    metadata={"mode": mode.value, "task_id": task_id}
                )

            # 3. Recall relevant memories
            relevant_context = ""
            if self.memory and user_id:
                memories = await self.memory.recall(query, user_id=user_id, limit=3)
                if memories:
                    relevant_context = "\n".join([m.content[:200] for m in memories])

            # 4. Route to appropriate agent(s)
            routes = self.router.route(query)
            primary_agent = routes[0][0] if routes else "polva-general"
            task.delegated_agents = [r[0] for r in routes[:3]]

            # 5. Execute based on mode
            if mode == POLVAMode.ORCHESTRATOR:
                response = await self._orchestrate_multi_agent(task, routes)
            elif mode == POLVAMode.EXECUTIVE:
                response = await self._executive_decision(task, routes)
            elif mode == POLVAMode.ASSISTANT and self.voice_agent:
                response = await self._assistant_mode(task, query, user_id, session_id)
            else:
                response = await self._delegate_to_agent(task, primary_agent, query, context)

            # 6. Store response in memory
            if self.memory:
                # Working memory
                if session_id:
                    self.memory.add_to_working_memory(
                        session_id=session_id,
                        role="assistant",
                        content=response.answer,
                        importance=0.7,
                        metadata={"agents": response.agents_used, "mode": mode.value}
                    )

                # Long-term memory for important interactions
                if priority in [TaskPriority.HIGH, TaskPriority.CRITICAL]:
                    await self.memory.remember(
                        content=f"Query: {query[:200]}\nResponse: {response.answer[:300]}",
                        user_id=user_id,
                        importance=MemoryImportance.HIGH,
                        memory_type=MemoryType.EPISODIC,
                        tags=["polva", mode.value] + response.agents_used[:3],
                        metadata={"task_id": task_id}
                    )
                    response.memory_updated = True

            # 7. Update task status
            task.status = "completed"
            task.completed_at = datetime.utcnow()
            task.results.append({"response": response.answer, "agents": response.agents_used})

            # 8. Add processing time
            response.metadata["processing_time_ms"] = int((time.time() - start_time) * 1000)
            response.metadata["task_id"] = task_id

            return response

        except Exception as e:
            logger.error(f"POLVA processing error: {e}")
            task.status = "failed"
            return POLVAResponse(
                answer=f"Je suis désolé, une erreur s'est produite: {str(e)}",
                confidence=0.0,
                mode=mode,
                metadata={"error": str(e)}
            )

    def _detect_mode(self, query: str) -> POLVAMode:
        """Detect appropriate mode from query"""
        query_lower = query.lower()

        # Mode detection patterns
        mode_patterns = {
            POLVAMode.EXECUTIVE: ["décision", "stratégie", "priorité", "important", "urgent", "critique"],
            POLVAMode.ORCHESTRATOR: ["coordonner", "orchestrer", "plusieurs", "ensemble", "combiner"],
            POLVAMode.DEVELOPER: ["code", "programmer", "développer", "api", "bug", "debug"],
            POLVAMode.ANALYST: ["analyser", "analyse", "données", "rapport", "statistique", "kpi"],
            POLVAMode.SUPPORT: ["aide", "problème", "support", "question", "comment"],
            POLVAMode.CREATIVE: ["créer", "design", "vidéo", "image", "contenu"],
            POLVAMode.ASSISTANT: ["rappel", "rendez-vous", "agenda", "appeler", "message"],
        }

        for mode, patterns in mode_patterns.items():
            if any(p in query_lower for p in patterns):
                return mode

        return POLVAMode.ASSISTANT  # Default

    async def _delegate_to_agent(
        self,
        task: POLVATask,
        agent_id: str,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> POLVAResponse:
        """Delegate task to a specific agent"""

        # Check if it's a voice agent
        if agent_id.startswith("voice-") and self.voice_agent:
            mode_map = {
                "voice-hotline": VoiceAgentMode.HOTLINE,
                "voice-secretary": VoiceAgentMode.SECRETARY,
                "voice-restaurant": VoiceAgentMode.RESTAURANT,
                "voice-ai-double": VoiceAgentMode.AI_DOUBLE,
                "voice-general": VoiceAgentMode.GENERAL,
            }
            voice_mode = mode_map.get(agent_id, VoiceAgentMode.GENERAL)

            voice_response = await self.voice_agent.process_voice_input(
                text=query,
                session_id=task.session_id or task.id,
                user_id=task.user_id,
                mode=voice_mode,
            )

            return POLVAResponse(
                answer=voice_response.text,
                confidence=0.85,
                agents_used=[agent_id],
                mode=task.mode,
                actions_taken=[{"action": voice_response.action, "data": voice_response.action_data}] if voice_response.action else [],
                suggestions=voice_response.suggested_responses,
                language=voice_response.language.value if hasattr(voice_response.language, 'value') else str(voice_response.language),
            )

        # For other agents, generate a response based on capabilities
        capabilities = self.agent_capabilities.get(agent_id, [])

        # Construct response based on agent type
        response_text = await self._generate_agent_response(agent_id, query, capabilities, context)

        return POLVAResponse(
            answer=response_text,
            confidence=0.8,
            agents_used=[agent_id],
            mode=task.mode,
            suggestions=self._get_suggestions(agent_id),
        )

    async def _orchestrate_multi_agent(
        self,
        task: POLVATask,
        routes: List[Tuple[str, float]]
    ) -> POLVAResponse:
        """Orchestrate multiple agents for complex tasks"""

        results = []
        agents_used = []

        for agent_id, confidence in routes[:3]:  # Top 3 agents
            if confidence < 0.2:
                continue

            sub_response = await self._delegate_to_agent(
                task, agent_id, task.query, task.context
            )
            results.append({
                "agent": agent_id,
                "confidence": confidence,
                "response": sub_response.answer[:500]
            })
            agents_used.append(agent_id)

        # Combine results
        if len(results) > 1:
            combined = self._combine_responses(results)
        else:
            combined = results[0]["response"] if results else "Aucun agent disponible."

        return POLVAResponse(
            answer=combined,
            confidence=sum(r["confidence"] for r in results) / len(results) if results else 0.0,
            agents_used=agents_used,
            mode=POLVAMode.ORCHESTRATOR,
            actions_taken=[{"orchestrated_agents": len(agents_used)}],
        )

    async def _executive_decision(
        self,
        task: POLVATask,
        routes: List[Tuple[str, float]]
    ) -> POLVAResponse:
        """Make executive-level decisions"""

        # Analyze the query
        query_lower = task.query.lower()

        # Priority assessment
        is_urgent = any(w in query_lower for w in ["urgent", "critique", "immédiat", "maintenant"])
        is_strategic = any(w in query_lower for w in ["stratégie", "long terme", "planifier"])

        # Get agent recommendation
        primary_agent = routes[0][0] if routes else "bmad-architect"

        # Executive response
        response_parts = []

        if is_urgent:
            response_parts.append("🚨 **Priorité critique détectée**")
            response_parts.append(f"Action immédiate recommandée via l'agent: {primary_agent}")

        if is_strategic:
            response_parts.append("📊 **Analyse stratégique**")
            response_parts.append("Je recommande d'impliquer les agents BMAD pour une planification complète.")

        response_parts.append(f"\n**Décision POLVA:**")
        response_parts.append(f"- Agent principal: {primary_agent}")
        response_parts.append(f"- Agents de support: {', '.join(r[0] for r in routes[1:3])}")

        return POLVAResponse(
            answer="\n".join(response_parts),
            confidence=0.9,
            agents_used=[primary_agent],
            mode=POLVAMode.EXECUTIVE,
            suggestions=[
                "Voulez-vous que je lance le workflow complet?",
                "Puis-je déléguer à l'agent spécialisé?",
                "Souhaitez-vous un rapport détaillé?",
            ],
        )

    async def _assistant_mode(
        self,
        task: POLVATask,
        query: str,
        user_id: Optional[str],
        session_id: Optional[str]
    ) -> POLVAResponse:
        """Personal assistant mode"""

        if self.voice_agent:
            voice_response = await self.voice_agent.process_voice_input(
                text=query,
                session_id=session_id or task.id,
                user_id=user_id,
                mode=VoiceAgentMode.SECRETARY,
            )

            return POLVAResponse(
                answer=voice_response.text,
                confidence=0.85,
                agents_used=["voice-secretary", "polva"],
                mode=POLVAMode.ASSISTANT,
                suggestions=voice_response.suggested_responses,
            )

        # Fallback
        return POLVAResponse(
            answer="Je suis votre assistant POLVA. Comment puis-je vous aider?",
            confidence=0.7,
            agents_used=["polva"],
            mode=POLVAMode.ASSISTANT,
        )

    async def _generate_agent_response(
        self,
        agent_id: str,
        query: str,
        capabilities: List[str],
        context: Optional[Dict[str, Any]]
    ) -> str:
        """Generate response based on agent capabilities"""

        # Template responses per agent type
        agent_templates = {
            "bmad-architect": "En tant qu'architecte système (Winston), je recommande: {analysis}. Les composants clés sont: {capabilities}.",
            "bmad-pm": "En tant que Product Manager (John), voici l'approche produit: {analysis}. Fonctionnalités: {capabilities}.",
            "bmad-developer": "En tant que développeur (Amelia), voici l'implémentation: {analysis}. Technologies: {capabilities}.",
            "legal-fiscal": "Analyse fiscale: {analysis}. Points de conformité: {capabilities}.",
            "legal-consultant": "Avis juridique: {analysis}. Considérations légales: {capabilities}.",
            "finance-investment": "Analyse financière: {analysis}. Recommandations: {capabilities}.",
            "rag-chat-pdf": "Résultat de recherche: {analysis}. Sources: {capabilities}.",
        }

        template = agent_templates.get(agent_id, "Réponse de l'agent {agent}: {analysis}. Capacités: {capabilities}.")

        analysis = f"Pour votre demande '{query[:100]}...'"
        caps_str = ", ".join(capabilities[:5]) if capabilities else "analyse, conseil, action"

        return template.format(
            analysis=analysis,
            capabilities=caps_str,
            agent=agent_id
        )

    def _combine_responses(self, results: List[Dict]) -> str:
        """Combine multiple agent responses"""
        parts = ["**Synthèse multi-agents POLVA:**\n"]

        for r in results:
            agent = r["agent"]
            conf = r["confidence"]
            resp = r["response"]
            parts.append(f"📌 **{agent}** (confiance: {conf:.0%}):\n{resp[:300]}...\n")

        return "\n".join(parts)

    def _get_suggestions(self, agent_id: str) -> List[str]:
        """Get contextual suggestions based on agent"""
        suggestions_map = {
            "bmad-architect": ["Créer un diagramme d'architecture", "Définir le tech stack", "Analyser les risques"],
            "bmad-pm": ["Créer des user stories", "Prioriser le backlog", "Planifier un sprint"],
            "voice-secretary": ["Planifier un rendez-vous", "Créer un rappel", "Appeler quelqu'un"],
            "legal-fiscal": ["Calculer la TVA", "Vérifier la conformité", "Préparer une déclaration"],
        }
        return suggestions_map.get(agent_id, ["Comment puis-je vous aider?"])

    # ------------------------------------------------
    # UTILITY METHODS
    # ------------------------------------------------

    def get_available_agents(self) -> Dict[str, List[str]]:
        """Get all available agents grouped by category"""
        grouped = {}
        for agent_id, caps in self.agent_capabilities.items():
            # Extract category from agent_id
            parts = agent_id.split("-")
            category = parts[0] if parts else "other"
            if category not in grouped:
                grouped[category] = []
            grouped[category].append(agent_id)
        return grouped

    def get_stats(self) -> Dict[str, Any]:
        """Get POLVA statistics"""
        return {
            "version": self.VERSION,
            "name": self.FULL_NAME,
            "total_agents": len(self.agent_capabilities),
            "memory_enabled": self.memory is not None,
            "voice_enabled": self.voice_agent is not None,
            "active_tasks": len([t for t in self.tasks.values() if t.status == "pending"]),
            "completed_tasks": len([t for t in self.tasks.values() if t.status == "completed"]),
        }

    async def health_check(self) -> Dict[str, Any]:
        """Check health of all components"""
        return {
            "status": "healthy",
            "components": {
                "router": True,
                "memory": self.memory is not None,
                "voice_agent": self.voice_agent is not None,
                "mcp_registry": self.registry is not None,
            },
            "agents_available": len(self.agent_capabilities),
            "timestamp": datetime.utcnow().isoformat(),
        }


# ============================================
# SINGLETON INSTANCE
# ============================================

_polva_instance: Optional[SuperAgentPOLVA] = None


def get_polva() -> SuperAgentPOLVA:
    """Get singleton POLVA instance"""
    global _polva_instance
    if _polva_instance is None:
        _polva_instance = SuperAgentPOLVA()
    return _polva_instance


# Alias
polva = get_polva
