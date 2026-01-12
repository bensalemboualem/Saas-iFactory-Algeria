"""
IAFactory MCP Registry - Complete Application & Agent Registry
Connects ALL 27 apps, 15+ agents, and workflows via MCP

This is the central registry for the entire IAFactory ecosystem.
"""
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum

from app.mcp.server import mcp_server, MCPTool, MCPAgent

logger = logging.getLogger(__name__)


class AppCategory(str, Enum):
    """Application categories"""
    MEDIA = "media"
    BUSINESS = "business"
    LEGAL = "legal"
    FINANCE = "finance"
    PRODUCTIVITY = "productivity"
    COMMUNICATION = "communication"
    ANALYTICS = "analytics"
    DEVELOPER = "developer"
    RAG = "rag"
    WORKFLOW = "workflow"


class AgentType(str, Enum):
    """Agent types"""
    BMAD = "bmad"
    RAG = "rag"
    BUSINESS = "business"
    FINANCE = "finance"
    LEGAL = "legal"
    PRODUCTIVITY = "productivity"
    MEDIA = "media"
    SPECIALIZED = "specialized"
    WORKFLOW = "workflow"  # For orchestrator and workflow agents


@dataclass
class AppDefinition:
    """Application definition for MCP"""
    name: str
    path: str
    category: AppCategory
    description: str
    port: Optional[int] = None
    api_prefix: Optional[str] = None
    tools: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    active: bool = True


@dataclass
class AgentDefinition:
    """Agent definition for MCP"""
    name: str
    agent_type: AgentType
    path: str
    description: str
    model: str = "claude-3-5-sonnet"
    tools: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)


@dataclass
class WorkflowDefinition:
    """Workflow definition for MCP"""
    name: str
    path: str
    description: str
    stages: List[str] = field(default_factory=list)
    agents_involved: List[str] = field(default_factory=list)


class MCPRegistry:
    """
    Central Registry for all IAFactory MCP components

    Manages:
    - 27 Applications
    - 15+ Agent Types with 15 Templates
    - Workflows (n8n, BMAD)
    - 60 API Routers
    """

    def __init__(self):
        self.apps: Dict[str, AppDefinition] = {}
        self.agents: Dict[str, AgentDefinition] = {}
        self.workflows: Dict[str, WorkflowDefinition] = {}
        self._initialized = False

    def initialize(self):
        """Initialize the complete registry"""
        if self._initialized:
            return

        self._register_all_apps()
        self._register_all_agents()
        self._register_all_workflows()
        self._register_mcp_tools()

        self._initialized = True
        logger.info(f"MCP Registry initialized: {len(self.apps)} apps, {len(self.agents)} agents, {len(self.workflows)} workflows")

    # ================================================
    # APPLICATION REGISTRY
    # ================================================

    def _register_all_apps(self):
        """Register all 27 applications"""

        # Media & Content Apps
        self.apps["video-studio"] = AppDefinition(
            name="Video Studio Pro",
            path="apps/video-studio",
            category=AppCategory.MEDIA,
            description="AI-powered multimedia content factory for podcasts, videos & shorts",
            port=3001,
            api_prefix="/api/studio",
            tools=["video_generate", "video_edit", "audio_generate", "thumbnail_create"],
            dependencies=["ffmpeg", "elevenlabs", "minimax", "suno"]
        )

        self.apps["dzirvideo"] = AppDefinition(
            name="DzirVideo",
            path="apps/dzirvideo",
            category=AppCategory.MEDIA,
            description="AI video generation focused on Algerian content",
            port=3002,
            api_prefix="/api/dzirvideo",
            tools=["dzir_video_create", "dzir_voice_clone", "dzir_subtitle"],
            dependencies=["video-studio"]
        )

        self.apps["news"] = AppDefinition(
            name="News DZ Aggregator",
            path="apps/news",
            category=AppCategory.MEDIA,
            description="Real-time Algerian press aggregator with 20+ sources",
            port=3003,
            tools=["news_fetch", "news_summarize", "news_translate"],
            dependencies=["rag"]
        )

        self.apps["sport"] = AppDefinition(
            name="Sport Magazine DZ",
            path="apps/sport",
            category=AppCategory.MEDIA,
            description="Sports magazine focused on Fennecs & Algerian football",
            port=3004,
            tools=["sport_news", "match_analysis", "player_stats"]
        )

        self.apps["can2025"] = AppDefinition(
            name="CAN 2025",
            path="apps/can2025",
            category=AppCategory.MEDIA,
            description="Africa Cup of Nations 2025 tournament tracker",
            port=3005,
            tools=["can_schedule", "can_standings", "can_predictions"]
        )

        # Business Apps
        self.apps["crm-ia"] = AppDefinition(
            name="CRM IA",
            path="apps/crm-ia",
            category=AppCategory.BUSINESS,
            description="AI-powered CRM for customer management",
            port=3010,
            api_prefix="/api/crm",
            tools=["crm_contact_add", "crm_lead_score", "crm_pipeline", "crm_forecast"],
            dependencies=["analytics"]
        )

        self.apps["pme-dz"] = AppDefinition(
            name="PME DZ Copilot",
            path="apps/pme-dz",
            category=AppCategory.BUSINESS,
            description="SME business copilot for Algerian businesses",
            port=3011,
            api_prefix="/api/pme",
            tools=["pme_analyze", "pme_growth", "pme_sales", "pme_onboard"],
            dependencies=["crm-ia", "analytics"]
        )

        self.apps["council"] = AppDefinition(
            name="Council",
            path="apps/council",
            category=AppCategory.BUSINESS,
            description="Multi-LLM council for decision making",
            port=3012,
            api_prefix="/api/council",
            tools=["council_debate", "council_vote", "council_consensus"]
        )

        self.apps["marketing"] = AppDefinition(
            name="Marketing Platform",
            path="apps/marketing",
            category=AppCategory.BUSINESS,
            description="Marketing automation and content creation",
            port=3013,
            tools=["marketing_campaign", "marketing_content", "marketing_analytics"]
        )

        self.apps["seo-dz-boost"] = AppDefinition(
            name="SEO DZ Boost",
            path="apps/seo-dz-boost",
            category=AppCategory.BUSINESS,
            description="SEO optimization for Algerian websites",
            port=3014,
            tools=["seo_audit", "seo_keywords", "seo_optimize"]
        )

        # Legal & Finance
        self.apps["legal-assistant"] = AppDefinition(
            name="Legal Assistant",
            path="apps/legal-assistant",
            category=AppCategory.LEGAL,
            description="AI legal consultation assistant",
            port=3020,
            api_prefix="/api/legal",
            tools=["legal_search", "legal_analyze", "legal_draft"],
            dependencies=["archon", "rag"]
        )

        # Productivity Apps
        self.apps["ia-chatbot"] = AppDefinition(
            name="IA Chatbot",
            path="apps/ia-chatbot",
            category=AppCategory.PRODUCTIVITY,
            description="AI chatbot interface for IAFactory",
            port=3030,
            tools=["chat_send", "chat_history", "chat_export"]
        )

        self.apps["ia-notebook"] = AppDefinition(
            name="Notebook LM",
            path="apps/ia-notebook",
            category=AppCategory.RAG,
            description="Document interrogation - NotebookLM alternative",
            port=3031,
            api_prefix="/api/notebook",
            tools=["notebook_upload", "notebook_query", "notebook_summarize"],
            dependencies=["archon", "rag"]
        )

        self.apps["ia-searcher"] = AppDefinition(
            name="IA Searcher",
            path="apps/ia-searcher",
            category=AppCategory.PRODUCTIVITY,
            description="AI-powered search interface",
            port=3032,
            tools=["search_web", "search_docs", "search_rag"]
        )

        self.apps["ia-voice"] = AppDefinition(
            name="IA Voice",
            path="apps/ia-voice",
            category=AppCategory.COMMUNICATION,
            description="Multilingual voice assistant (FR/AR)",
            port=3033,
            tools=["voice_stt", "voice_tts", "voice_command"]
        )

        self.apps["ia-agents"] = AppDefinition(
            name="IA Agents Marketplace",
            path="apps/ia-agents",
            category=AppCategory.DEVELOPER,
            description="Agent marketplace frontend",
            port=3034,
            tools=["agent_list", "agent_deploy", "agent_configure"]
        )

        self.apps["interview"] = AppDefinition(
            name="Interview Platform",
            path="apps/interview",
            category=AppCategory.PRODUCTIVITY,
            description="Interview scheduling and management",
            port=3035,
            tools=["interview_schedule", "interview_analyze", "interview_feedback"]
        )

        self.apps["prompt-creator"] = AppDefinition(
            name="Prompt Creator",
            path="apps/prompt-creator",
            category=AppCategory.DEVELOPER,
            description="Tool for creating and testing AI prompts",
            port=3036,
            tools=["prompt_create", "prompt_test", "prompt_optimize"]
        )

        # Workflow & Developer Apps
        self.apps["workflow-studio"] = AppDefinition(
            name="Workflow Studio",
            path="apps/workflow-studio",
            category=AppCategory.WORKFLOW,
            description="Workflow automation and orchestration designer",
            port=3040,
            tools=["workflow_create", "workflow_run", "workflow_monitor"],
            dependencies=["bmad", "archon", "bolt"]
        )

        self.apps["bmad"] = AppDefinition(
            name="BMAD Workflow Studio",
            path="apps/bmad",
            category=AppCategory.WORKFLOW,
            description="BMAD workflow application",
            port=3041,
            tools=["bmad_brainstorm", "bmad_plan", "bmad_review"]
        )

        self.apps["cockpit"] = AppDefinition(
            name="Cockpit Dashboard",
            path="apps/cockpit",
            category=AppCategory.ANALYTICS,
            description="Central control dashboard",
            port=3042,
            tools=["cockpit_metrics", "cockpit_alerts", "cockpit_control"]
        )

        self.apps["ithy"] = AppDefinition(
            name="Ithy",
            path="apps/ithy",
            category=AppCategory.RAG,
            description="Ithy integration application",
            port=3043,
            tools=["ithy_search", "ithy_analyze"]
        )

        # Developer Portals
        self.apps["api-portal"] = AppDefinition(
            name="API Portal",
            path="apps/api-portal",
            category=AppCategory.DEVELOPER,
            description="Developer portal for API documentation",
            port=3050,
            tools=["api_docs", "api_test", "api_keys"]
        )

        self.apps["dev-portal"] = AppDefinition(
            name="Dev Portal",
            path="apps/dev-portal",
            category=AppCategory.DEVELOPER,
            description="Developer dashboard and tools",
            port=3051,
            tools=["dev_deploy", "dev_logs", "dev_debug"]
        )

        self.apps["landing-pro"] = AppDefinition(
            name="Landing Pro",
            path="apps/landing-pro",
            category=AppCategory.BUSINESS,
            description="Production landing page for IAFactory",
            port=80,
            active=True
        )

        # === ALGERIAN SECTOR APPS (Manquants) ===

        self.apps["agriculture-dz"] = AppDefinition(
            name="Agriculture DZ",
            path="apps/agriculture-dz",
            category=AppCategory.BUSINESS,
            description="Agriculture intelligence for Algerian farmers - irrigation, crop analysis",
            port=3060,
            api_prefix="/api/agriculture",
            tools=["agri_weather", "agri_irrigation", "agri_crop_analysis", "agri_market_prices"],
            dependencies=["analytics", "rag"]
        )

        self.apps["commerce-dz"] = AppDefinition(
            name="Commerce DZ",
            path="apps/commerce-dz",
            category=AppCategory.BUSINESS,
            description="E-commerce platform for Algerian businesses",
            port=3061,
            api_prefix="/api/commerce",
            tools=["commerce_catalog", "commerce_orders", "commerce_payments", "commerce_delivery"],
            dependencies=["crm-ia", "payment"]
        )

        self.apps["education-dz"] = AppDefinition(
            name="Education DZ",
            path="apps/education-dz",
            category=AppCategory.BUSINESS,
            description="Educational platform with Algerian curriculum support",
            port=3062,
            api_prefix="/api/education",
            tools=["edu_course_create", "edu_quiz_generate", "edu_student_track", "edu_certificate"],
            dependencies=["rag", "ia-voice"]
        )

        self.apps["finance-dz"] = AppDefinition(
            name="Finance DZ",
            path="apps/finance-dz",
            category=AppCategory.FINANCE,
            description="Financial services for Algerian market - DZD, banking, taxes",
            port=3063,
            api_prefix="/api/finance",
            tools=["finance_currency", "finance_tax_calc", "finance_invoice", "finance_report"],
            dependencies=["analytics", "legal-assistant"]
        )

        self.apps["transport-dz"] = AppDefinition(
            name="Transport DZ",
            path="apps/transport-dz",
            category=AppCategory.BUSINESS,
            description="Transport and logistics for Algeria",
            port=3064,
            api_prefix="/api/transport",
            tools=["transport_route", "transport_track", "transport_schedule", "transport_cost"],
            dependencies=["analytics"]
        )

        self.apps["sante-dz"] = AppDefinition(
            name="Santé DZ",
            path="apps/sante-dz",
            category=AppCategory.BUSINESS,
            description="Healthcare platform for Algerian medical system",
            port=3065,
            api_prefix="/api/sante",
            tools=["sante_appointment", "sante_prescription", "sante_teleconsult", "sante_records"],
            dependencies=["ia-voice", "legal-assistant"]
        )

        self.apps["creative-studio"] = AppDefinition(
            name="Creative Studio",
            path="apps/creative-studio",
            category=AppCategory.MEDIA,
            description="All-in-one creative content generation studio",
            port=3066,
            api_prefix="/api/creative",
            tools=["creative_image", "creative_audio", "creative_text", "creative_brand"],
            dependencies=["video-studio", "dzirvideo"]
        )

        self.apps["pipeline-creator"] = AppDefinition(
            name="Pipeline Creator",
            path="apps/pipeline-creator",
            category=AppCategory.WORKFLOW,
            description="Visual pipeline builder for AI workflows",
            port=3067,
            api_prefix="/api/pipeline",
            tools=["pipeline_create", "pipeline_validate", "pipeline_deploy", "pipeline_monitor"],
            dependencies=["workflow-studio", "bmad"]
        )

        # MCP Dashboard
        self.apps["mcp-dashboard"] = AppDefinition(
            name="MCP Dashboard",
            path="apps/mcp-dashboard",
            category=AppCategory.ANALYTICS,
            description="Central MCP monitoring and health check dashboard",
            port=3099,
            tools=["mcp_health_check", "mcp_test_component", "mcp_metrics"],
            dependencies=[]
        )

    # ================================================
    # AGENT REGISTRY
    # ================================================

    def _register_all_agents(self):
        """Register all agents"""

        # BMAD Agents
        bmad_agents = [
            ("bmad-pm", "John", "Product Manager", ["product_strategy", "user_stories", "backlog"]),
            ("bmad-architect", "Winston", "System Architect", ["architecture", "tech_stack", "diagrams"]),
            ("bmad-developer", "Amelia", "Senior Developer", ["coding", "implementation", "debugging"]),
            ("bmad-analyst", "Mary", "Business Analyst", ["analysis", "requirements", "specifications"]),
            ("bmad-tester", "Murat", "Test Architect", ["testing", "qa", "automation"]),
        ]

        for agent_id, name, role, capabilities in bmad_agents:
            self.agents[agent_id] = AgentDefinition(
                name=f"{name} ({role})",
                agent_type=AgentType.BMAD,
                path=f"bmad/agents/{agent_id}",
                description=f"BMAD {role} agent",
                capabilities=capabilities,
                tools=[f"bmad_{cap}" for cap in capabilities]
            )

        # RAG Agents
        rag_agents = [
            ("rag-chat-pdf", "Chat PDF Agent", "PDF document querying"),
            ("rag-finance", "Finance RAG Agent", "Financial RAG analysis"),
            ("rag-hybrid", "Hybrid Search Agent", "Multi-modal search"),
            ("rag-local", "Local RAG Agent", "Offline RAG capabilities"),
            ("rag-voice", "Voice Support Agent", "RAG with voice interface"),
        ]

        for agent_id, name, desc in rag_agents:
            self.agents[agent_id] = AgentDefinition(
                name=name,
                agent_type=AgentType.RAG,
                path=f"agents/rag/{agent_id}",
                description=desc,
                capabilities=["search", "retrieve", "generate"],
                tools=["rag_query", "rag_index", "rag_summarize"]
            )

        # Business Agents
        business_agents = [
            ("consultant", "Business Consultant", "Business consulting and strategy"),
            ("customer-support", "Customer Support", "Automated customer service"),
            ("data-analysis", "Data Analyst", "Business data analysis"),
        ]

        for agent_id, name, desc in business_agents:
            self.agents[agent_id] = AgentDefinition(
                name=name,
                agent_type=AgentType.BUSINESS,
                path=f"agents/business/{agent_id}",
                description=desc,
                capabilities=["analyze", "recommend", "report"]
            )

        # Finance Startup Agents (Templates)
        finance_agents = [
            ("deep-research", "Deep Research Agent", "Market research and analysis"),
            ("financial-coach", "Financial Coach", "Personal financial coaching"),
            ("investment", "Investment Agent", "Portfolio management"),
            ("startup-trends", "Startup Trends", "Ecosystem trend analysis"),
            ("system-architect-r1", "System Architect R1", "Financial system design"),
        ]

        for agent_id, name, desc in finance_agents:
            self.agents[f"finance-{agent_id}"] = AgentDefinition(
                name=name,
                agent_type=AgentType.FINANCE,
                path=f"agents/templates/finance-startups/ai_{agent_id.replace('-', '_')}_agent",
                description=desc,
                model="claude-3-5-sonnet",
                capabilities=["analyze", "forecast", "recommend"]
            )

        # Productivity Agents (Templates)
        productivity_agents = [
            ("journalist", "Journalist Agent", "Automated journalism"),
            ("meeting", "Meeting Prep Agent", "Meeting preparation and summarization"),
            ("product-launch", "Product Launch Agent", "Launch intelligence"),
            ("web-scraping", "Web Scraping Agent", "Data extraction"),
            ("xai-finance", "XAI Finance", "Explainable AI for finance"),
        ]

        for agent_id, name, desc in productivity_agents:
            self.agents[f"productivity-{agent_id}"] = AgentDefinition(
                name=name,
                agent_type=AgentType.PRODUCTIVITY,
                path=f"agents/templates/productivity/{agent_id}",
                description=desc,
                capabilities=["automate", "analyze", "generate"]
            )

        # Specialized Agents
        specialized_agents = [
            ("discovery-dz", "Discovery DZ", "Algerian market discovery"),
            ("real-estate", "Real Estate Agent", "Property analysis"),
            ("recruitment", "Recruitment Agent", "HR automation"),
            ("recruteur-dz", "Recruteur DZ", "DZ-specific recruitment"),
            ("teaching", "Teaching Agent", "Educational content"),
            ("travel", "Travel Agent", "Travel planning"),
            ("ux-research", "UX Research", "User experience research"),
            ("video-operator", "Video Operator", "Automated video editing"),
            ("iafactory-operator", "IAFactory Operator", "Platform orchestration"),
        ]

        for agent_id, name, desc in specialized_agents:
            self.agents[agent_id] = AgentDefinition(
                name=name,
                agent_type=AgentType.SPECIALIZED,
                path=f"agents/{agent_id}",
                description=desc,
                capabilities=["specialized_task"]
            )

        # === LEGAL AGENTS (Nouveau) ===
        legal_agents = [
            ("legal-consultant", "Legal Consultant", "Consultation juridique générale",
             ["contract_review", "legal_advice", "compliance_check"]),
            ("legal-fiscal", "Fiscal Expert", "Expert fiscal algérien - TVA, IBS, TAP",
             ["tax_calculate", "fiscal_declare", "tax_optimize"]),
            ("legal-commercial", "Commercial Law Expert", "Droit commercial et des sociétés",
             ["company_create", "contract_draft", "dispute_resolve"]),
            ("legal-labor", "Labor Law Expert", "Droit du travail algérien",
             ["employment_contract", "dispute_resolve", "compliance_check"]),
        ]

        for agent_id, name, desc, capabilities in legal_agents:
            self.agents[agent_id] = AgentDefinition(
                name=name,
                agent_type=AgentType.LEGAL,
                path=f"agents/legal/{agent_id}",
                description=desc,
                model="claude-3-5-sonnet",
                capabilities=capabilities,
                tools=[f"legal_{cap}" for cap in capabilities]
            )

        # === MEDICAL AGENTS (Nouveau) ===
        medical_agents = [
            ("medical-triage", "Medical Triage", "Triage médical intelligent",
             ["symptom_check", "urgency_assess", "specialist_recommend"]),
            ("medical-pharma", "Pharmacist AI", "Assistant pharmacien",
             ["drug_interaction", "dosage_check", "generic_suggest"]),
            ("medical-teleconsult", "Teleconsultation", "Assistant téléconsultation",
             ["patient_intake", "history_collect", "report_generate"]),
        ]

        for agent_id, name, desc, capabilities in medical_agents:
            self.agents[agent_id] = AgentDefinition(
                name=name,
                agent_type=AgentType.SPECIALIZED,
                path=f"agents/medical/{agent_id}",
                description=desc,
                model="claude-3-5-sonnet",
                capabilities=capabilities,
                tools=[f"medical_{cap}" for cap in capabilities]
            )

        # === EDUCATION AGENTS (Nouveau) ===
        education_agents = [
            ("edu-tutor", "AI Tutor", "Tuteur IA personnalisé",
             ["lesson_explain", "quiz_generate", "progress_track"]),
            ("edu-curriculum", "Curriculum Designer", "Concepteur de programmes",
             ["syllabus_create", "content_adapt", "assessment_design"]),
            ("edu-examiner", "Exam Generator", "Générateur d'examens",
             ["exam_create", "grade_auto", "feedback_provide"]),
        ]

        for agent_id, name, desc, capabilities in education_agents:
            self.agents[agent_id] = AgentDefinition(
                name=name,
                agent_type=AgentType.SPECIALIZED,
                path=f"agents/education/{agent_id}",
                description=desc,
                model="claude-3-5-sonnet",
                capabilities=capabilities,
                tools=[f"edu_{cap}" for cap in capabilities]
            )

        # === ALGERIAN SECTOR AGENTS (Nouveau) ===
        dz_agents = [
            ("agri-advisor", "Agriculture Advisor DZ", "Conseiller agricole algérien",
             ["crop_recommend", "irrigation_plan", "weather_forecast", "market_analyze"]),
            ("commerce-advisor", "Commerce Advisor DZ", "Conseiller commercial",
             ["market_analyze", "pricing_optimize", "inventory_manage"]),
            ("transport-planner", "Transport Planner DZ", "Planificateur logistique",
             ["route_optimize", "cost_estimate", "delivery_track"]),
        ]

        for agent_id, name, desc, capabilities in dz_agents:
            self.agents[agent_id] = AgentDefinition(
                name=name,
                agent_type=AgentType.SPECIALIZED,
                path=f"agents/algeria/{agent_id}",
                description=desc,
                model="claude-3-5-sonnet",
                capabilities=capabilities,
                tools=[f"dz_{cap}" for cap in capabilities]
            )

        # === SAAS ESSENTIAL AGENTS (Nouveau) ===

        # Customer Success Agents
        saas_cs_agents = [
            ("cs-onboarding", "Onboarding Agent", "Guide nouveaux utilisateurs étape par étape",
             ["welcome_flow", "tutorial_guide", "feature_discover", "milestone_track"]),
            ("cs-retention", "Retention Agent", "Prédiction et prévention du churn",
             ["churn_predict", "engagement_score", "reactivation_campaign", "satisfaction_survey"]),
            ("cs-success-manager", "Customer Success Manager", "Accompagnement personnalisé clients",
             ["health_score", "expansion_opportunity", "quarterly_review", "renewal_prepare"]),
        ]

        for agent_id, name, desc, capabilities in saas_cs_agents:
            self.agents[agent_id] = AgentDefinition(
                name=name,
                agent_type=AgentType.BUSINESS,
                path=f"agents/saas/customer-success/{agent_id}",
                description=desc,
                model="claude-3-5-sonnet",
                capabilities=capabilities,
                tools=[f"cs_{cap}" for cap in capabilities]
            )

        # Sales Agents
        saas_sales_agents = [
            ("sales-qualifier", "Lead Qualifier", "Qualification automatique des leads",
             ["score_lead", "qualify_budget", "identify_champion", "assess_timeline"]),
            ("sales-proposal", "Proposal Generator", "Génération de propositions commerciales",
             ["proposal_draft", "pricing_customize", "roi_calculate", "demo_schedule"]),
            ("sales-closer", "Deal Closer", "Assistance à la négociation et closing",
             ["objection_handle", "discount_approve", "contract_prepare", "signature_collect"]),
        ]

        for agent_id, name, desc, capabilities in saas_sales_agents:
            self.agents[agent_id] = AgentDefinition(
                name=name,
                agent_type=AgentType.BUSINESS,
                path=f"agents/saas/sales/{agent_id}",
                description=desc,
                model="claude-3-5-sonnet",
                capabilities=capabilities,
                tools=[f"sales_{cap}" for cap in capabilities]
            )

        # Analytics Agents
        saas_analytics_agents = [
            ("analytics-dashboard", "Dashboard Builder", "Création automatique de dashboards",
             ["widget_create", "chart_suggest", "kpi_track", "alert_configure"]),
            ("analytics-insight", "Insight Generator", "Découverte automatique d'insights",
             ["anomaly_detect", "trend_identify", "correlation_find", "recommendation_generate"]),
            ("analytics-reporter", "Report Generator", "Rapports automatisés",
             ["report_schedule", "executive_summary", "cohort_analyze", "benchmark_compare"]),
        ]

        for agent_id, name, desc, capabilities in saas_analytics_agents:
            self.agents[agent_id] = AgentDefinition(
                name=name,
                agent_type=AgentType.BUSINESS,
                path=f"agents/saas/analytics/{agent_id}",
                description=desc,
                model="claude-3-5-sonnet",
                capabilities=capabilities,
                tools=[f"analytics_{cap}" for cap in capabilities]
            )

        # Support Agents
        saas_support_agents = [
            ("support-triage", "Ticket Triage", "Classification et routage des tickets",
             ["priority_assess", "category_assign", "agent_route", "sla_track"]),
            ("support-resolver", "Issue Resolver", "Résolution automatique des problèmes courants",
             ["solution_suggest", "kb_search", "workaround_provide", "escalation_decide"]),
            ("support-feedback", "Feedback Analyzer", "Analyse des retours clients",
             ["sentiment_analyze", "theme_extract", "nps_calculate", "improvement_suggest"]),
        ]

        for agent_id, name, desc, capabilities in saas_support_agents:
            self.agents[agent_id] = AgentDefinition(
                name=name,
                agent_type=AgentType.BUSINESS,
                path=f"agents/saas/support/{agent_id}",
                description=desc,
                model="claude-3-5-sonnet",
                capabilities=capabilities,
                tools=[f"support_{cap}" for cap in capabilities]
            )

        # Payment & Billing Agents
        saas_billing_agents = [
            ("billing-invoicer", "Invoice Agent", "Gestion automatique de la facturation",
             ["invoice_generate", "payment_remind", "dunning_manage", "proration_calculate"]),
            ("billing-subscription", "Subscription Manager", "Gestion des abonnements",
             ["plan_change", "addon_upsell", "usage_meter", "renewal_process"]),
            ("billing-revenue", "Revenue Analyst", "Analyse des revenus",
             ["mrr_calculate", "ltv_predict", "cohort_revenue", "forecast_generate"]),
        ]

        for agent_id, name, desc, capabilities in saas_billing_agents:
            self.agents[agent_id] = AgentDefinition(
                name=name,
                agent_type=AgentType.FINANCE,
                path=f"agents/saas/billing/{agent_id}",
                description=desc,
                model="claude-3-5-sonnet",
                capabilities=capabilities,
                tools=[f"billing_{cap}" for cap in capabilities]
            )

        # Marketing Agents
        saas_marketing_agents = [
            ("marketing-content", "Content Creator", "Génération de contenu marketing",
             ["blog_write", "social_post", "email_craft", "landing_page"]),
            ("marketing-seo", "SEO Optimizer", "Optimisation référencement",
             ["keyword_research", "content_optimize", "backlink_analyze", "serp_track"]),
            ("marketing-campaign", "Campaign Manager", "Gestion des campagnes",
             ["audience_segment", "ab_test", "budget_optimize", "conversion_track"]),
        ]

        for agent_id, name, desc, capabilities in saas_marketing_agents:
            self.agents[agent_id] = AgentDefinition(
                name=name,
                agent_type=AgentType.PRODUCTIVITY,
                path=f"agents/saas/marketing/{agent_id}",
                description=desc,
                model="claude-3-5-sonnet",
                capabilities=capabilities,
                tools=[f"marketing_{cap}" for cap in capabilities]
            )

        # Security & Compliance Agents
        saas_security_agents = [
            ("security-fraud", "Fraud Detector", "Détection de fraude en temps réel",
             ["transaction_analyze", "pattern_detect", "risk_score", "alert_trigger"]),
            ("security-compliance", "Compliance Monitor", "Conformité RGPD, données personnelles",
             ["data_audit", "consent_track", "breach_detect", "report_generate"]),
            ("security-access", "Access Manager", "Gestion des accès et permissions",
             ["permission_audit", "anomaly_detect", "session_monitor", "mfa_enforce"]),
        ]

        for agent_id, name, desc, capabilities in saas_security_agents:
            self.agents[agent_id] = AgentDefinition(
                name=name,
                agent_type=AgentType.SPECIALIZED,
                path=f"agents/saas/security/{agent_id}",
                description=desc,
                model="claude-3-5-sonnet",
                capabilities=capabilities,
                tools=[f"security_{cap}" for cap in capabilities]
            )

        # Integration Agents
        saas_integration_agents = [
            ("integration-connector", "API Connector", "Connexion à des services externes",
             ["api_connect", "data_sync", "webhook_manage", "oauth_handle"]),
            ("integration-etl", "ETL Pipeline", "Extraction, transformation, chargement",
             ["data_extract", "data_transform", "data_load", "schedule_run"]),
            ("integration-zapier", "Automation Hub", "Automatisations type Zapier",
             ["trigger_create", "action_chain", "condition_set", "error_handle"]),
        ]

        for agent_id, name, desc, capabilities in saas_integration_agents:
            self.agents[agent_id] = AgentDefinition(
                name=name,
                agent_type=AgentType.SPECIALIZED,
                path=f"agents/saas/integration/{agent_id}",
                description=desc,
                model="claude-3-5-sonnet",
                capabilities=capabilities,
                tools=[f"integration_{cap}" for cap in capabilities]
            )

        # Localization Agent (Important for Algeria)
        self.agents["localization-dz"] = AgentDefinition(
            name="Localization DZ",
            agent_type=AgentType.SPECIALIZED,
            path="agents/saas/localization",
            description="Traduction et adaptation pour l'Algérie (FR/AR/Darija)",
            model="claude-3-5-sonnet",
            capabilities=["translate_fr_ar", "adapt_cultural", "darija_support", "rtl_format"],
            tools=["localize_translate", "localize_adapt", "localize_validate"]
        )

        # === VOICE AI AGENT (Nouveau) ===
        # Agent vocal intelligent avec STT/TTS/NLP/OCR
        voice_ai_modes = [
            ("voice-hotline", "Voice Hotline Agent", "Agent vocal hotline/centre d'appels",
             ["call_handle", "complaint_register", "ticket_create", "transfer_agent"]),
            ("voice-secretary", "Voice Secretary Agent", "Secrétaire IA vocale personnelle",
             ["schedule_meeting", "reminder_set", "message_take", "call_manage"]),
            ("voice-restaurant", "Voice Restaurant Agent", "Prise de commandes restaurant",
             ["order_take", "menu_explain", "delivery_schedule", "payment_process"]),
            ("voice-ai-double", "AI Double Agent", "Clone IA vocal - apprend votre style",
             ["style_learn", "respond_as_user", "behavior_mimic", "preference_remember"]),
            ("voice-general", "Voice General Agent", "Agent vocal multilingue général",
             ["converse", "translate", "understand", "respond"]),
        ]

        for agent_id, name, desc, capabilities in voice_ai_modes:
            self.agents[agent_id] = AgentDefinition(
                name=name,
                agent_type=AgentType.SPECIALIZED,
                path=f"services/api/app/services/voice_ai_agent",
                description=desc,
                model="claude-3-5-sonnet",
                capabilities=capabilities + [
                    "stt_transcribe",  # Speech-to-Text
                    "tts_synthesize",  # Text-to-Speech
                    "nlp_analyze",     # NLP Analysis
                    "ocr_extract",     # OCR from documents
                    "multilingual",    # AR/FR/EN/Darija
                    "code_switching",  # Mixed language support
                    "emotion_detect",  # Emotion detection
                    "anticipate",      # Intent anticipation
                ],
                tools=[
                    "voice_process",      # Full pipeline: Audio → Response → Audio
                    "voice_stt",          # Speech-to-Text only
                    "voice_tts",          # Text-to-Speech only
                    "voice_understand",   # NLP analysis
                    "voice_ocr",          # Document OCR
                    "voice_learn",        # AI Double learning
                ]
            )

        # Core System Agents
        self.agents["archon"] = AgentDefinition(
            name="Archon",
            agent_type=AgentType.RAG,
            path="archon",
            description="Knowledge base and RAG system",
            capabilities=["index", "search", "retrieve", "knowledge_graph"],
            tools=["archon_create_kb", "archon_query", "archon_index"]
        )

        self.agents["bolt"] = AgentDefinition(
            name="Bolt.diy",
            agent_type=AgentType.PRODUCTIVITY,
            path="bolt-diy",
            description="AI code generation platform",
            capabilities=["generate", "preview", "deploy"],
            tools=["bolt_generate", "bolt_preview", "bolt_deploy"]
        )

        self.agents["orchestrator"] = AgentDefinition(
            name="Orchestrator",
            agent_type=AgentType.WORKFLOW,
            path="services/api/app/services/workflow_orchestrator",
            description="Workflow orchestration engine",
            capabilities=["orchestrate", "coordinate", "monitor"],
            tools=["workflow_start", "workflow_status", "workflow_cancel"]
        )

        # === POLVA SUPERAGENT ===
        self.agents["polva"] = AgentDefinition(
            name="POLVA SuperAgent",
            agent_type=AgentType.WORKFLOW,
            path="services/api/app/services/super_agent_polva",
            description="Polyvalent Omniscient Learning Virtual Assistant - Orchestrateur ultime avec accès à tous les agents",
            model="claude-3-5-sonnet",
            capabilities=[
                "omniscient_routing",      # Route vers n'importe quel agent
                "multi_agent_orchestration",  # Coordonne plusieurs agents
                "executive_decisions",     # Prend des décisions de haut niveau
                "global_memory",           # Mémoire persistante globale
                "context_awareness",       # Conscience du contexte
                "intent_detection",        # Détection d'intention avancée
                "multilingual",            # AR/FR/EN/Darija
                "voice_integration",       # Intégration vocale
                "learning",                # Apprentissage continu
            ],
            tools=[
                "polva_query",             # Requête principale
                "polva_orchestrate",       # Orchestration multi-agents
                "polva_executive",         # Décisions executive
                "polva_route",             # Routing preview
                "polva_memory",            # Accès mémoire
                "agent_list",              # Liste des agents
                "agent_delegate",          # Délégation à un agent
            ]
        )

    # ================================================
    # WORKFLOW REGISTRY
    # ================================================

    def _register_all_workflows(self):
        """Register all workflows"""

        # Main BMAD → Archon → Bolt Workflow
        self.workflows["bmad-to-bolt"] = WorkflowDefinition(
            name="BMAD to Bolt Pipeline",
            path="workflows/bmad-to-bolt",
            description="Complete project creation: brainstorm → plan → knowledge → code",
            stages=["brainstorm", "planning", "kb_creation", "prompt_generation", "code_generation", "deployment"],
            agents_involved=["bmad-pm", "bmad-architect", "bmad-developer", "archon", "bolt"]
        )

        # Media Reels Workflow
        self.workflows["media-reels"] = WorkflowDefinition(
            name="Media Reels Automation",
            path="workflows/delivery/n8n_workflow_media_reels.json",
            description="Automated media reels generation via n8n",
            stages=["content_fetch", "script_generate", "video_create", "publish"],
            agents_involved=["video-operator", "journalist"]
        )

        # Sales Workflow
        self.workflows["sales-pipeline"] = WorkflowDefinition(
            name="Sales Pipeline Automation",
            path="workflows/sales",
            description="Automated sales process",
            stages=["lead_capture", "qualification", "proposal", "closing"],
            agents_involved=["customer-support", "data-analysis"]
        )

        # RAG Workflow
        self.workflows["rag-pipeline"] = WorkflowDefinition(
            name="RAG Processing Pipeline",
            path="services/api/app/services/advanced_rag",
            description="Advanced RAG with hybrid search and reranking",
            stages=["query_decompose", "hybrid_search", "rerank", "generate"],
            agents_involved=["archon", "rag-hybrid"]
        )

        # Conversational Workflow
        self.workflows["conversational"] = WorkflowDefinition(
            name="Conversational AI Pipeline",
            path="services/api/app/services/conversational_orchestrator",
            description="Multi-modal conversation processing (NLP/STT/TTS/OCR)",
            stages=["input_process", "nlp_analyze", "context_build", "prompt_transform"],
            agents_involved=["orchestrator"]
        )

        # === SAAS WORKFLOWS (Nouveau) ===

        # Customer Onboarding Workflow
        self.workflows["customer-onboarding"] = WorkflowDefinition(
            name="Customer Onboarding Pipeline",
            path="workflows/saas/customer-onboarding",
            description="Onboarding complet: inscription → setup → formation → activation",
            stages=["signup", "profile_complete", "workspace_setup", "tutorial", "first_value", "activation"],
            agents_involved=["cs-onboarding", "support-triage", "analytics-insight"]
        )

        # Lead-to-Customer Workflow
        self.workflows["lead-to-customer"] = WorkflowDefinition(
            name="Lead to Customer Pipeline",
            path="workflows/saas/lead-to-customer",
            description="Conversion: lead → qualification → demo → proposal → closing",
            stages=["lead_capture", "qualification", "demo_schedule", "proposal_send", "negotiation", "closing"],
            agents_involved=["sales-qualifier", "sales-proposal", "sales-closer", "billing-subscription"]
        )

        # Support Escalation Workflow
        self.workflows["support-escalation"] = WorkflowDefinition(
            name="Support Ticket Pipeline",
            path="workflows/saas/support-escalation",
            description="Support: triage → auto-resolve → escalation → resolution → feedback",
            stages=["ticket_receive", "auto_triage", "auto_resolve", "escalate", "human_resolve", "feedback_collect"],
            agents_involved=["support-triage", "support-resolver", "support-feedback"]
        )

        # Legal Consultation Workflow
        self.workflows["legal-consultation"] = WorkflowDefinition(
            name="Legal Consultation Pipeline",
            path="workflows/legal/consultation",
            description="Consultation légale: intake → recherche → analyse → recommandation",
            stages=["client_intake", "case_research", "legal_analysis", "recommendation", "document_draft"],
            agents_involved=["legal-consultant", "legal-fiscal", "legal-commercial", "archon"]
        )

        # PME DZ Onboarding Workflow
        self.workflows["pme-onboarding"] = WorkflowDefinition(
            name="PME DZ Onboarding",
            path="workflows/algeria/pme-onboarding",
            description="Onboarding PME algérienne: diagnostic → setup → formation",
            stages=["company_register", "fiscal_setup", "bank_connect", "team_invite", "training"],
            agents_involved=["cs-onboarding", "legal-fiscal", "billing-subscription", "localization-dz"]
        )

        # Content Marketing Workflow
        self.workflows["content-marketing"] = WorkflowDefinition(
            name="Content Marketing Pipeline",
            path="workflows/marketing/content",
            description="Production contenu: research → create → optimize → publish → analyze",
            stages=["keyword_research", "content_plan", "content_create", "seo_optimize", "publish", "performance_analyze"],
            agents_involved=["marketing-seo", "marketing-content", "marketing-campaign", "analytics-reporter"]
        )

        # Subscription Billing Workflow
        self.workflows["subscription-lifecycle"] = WorkflowDefinition(
            name="Subscription Lifecycle",
            path="workflows/billing/subscription",
            description="Cycle de vie abonnement: création → facturation → renouvellement",
            stages=["plan_select", "payment_process", "invoice_generate", "usage_track", "renewal_remind", "renewal_process"],
            agents_involved=["billing-subscription", "billing-invoicer", "billing-revenue", "cs-retention"]
        )

        # Security Audit Workflow
        self.workflows["security-audit"] = WorkflowDefinition(
            name="Security Audit Pipeline",
            path="workflows/security/audit",
            description="Audit sécurité: scan → analyze → report → remediate",
            stages=["access_audit", "vulnerability_scan", "compliance_check", "report_generate", "remediation_plan"],
            agents_involved=["security-access", "security-compliance", "security-fraud", "analytics-reporter"]
        )

        # Data Integration Workflow
        self.workflows["data-integration"] = WorkflowDefinition(
            name="Data Integration Pipeline",
            path="workflows/integration/data",
            description="Intégration données: connect → extract → transform → load → validate",
            stages=["source_connect", "data_extract", "data_transform", "data_load", "quality_validate", "sync_schedule"],
            agents_involved=["integration-connector", "integration-etl", "analytics-insight"]
        )

        # Healthcare Consultation Workflow (Sante DZ)
        self.workflows["teleconsultation"] = WorkflowDefinition(
            name="Teleconsultation Pipeline",
            path="workflows/healthcare/teleconsult",
            description="Téléconsultation: triage → consultation → prescription → suivi",
            stages=["symptom_collect", "triage", "doctor_match", "consultation", "prescription", "followup"],
            agents_involved=["medical-triage", "medical-teleconsult", "medical-pharma"]
        )

    # ================================================
    # MCP TOOLS REGISTRATION
    # ================================================

    def _register_mcp_tools(self):
        """Register all MCP tools from apps and agents"""

        # Register app tools
        for app_id, app in self.apps.items():
            for tool_name in app.tools:
                mcp_server.register_tool(MCPTool(
                    name=tool_name,
                    description=f"{app.name}: {tool_name.replace('_', ' ')}",
                    agent=MCPAgent.ORCHESTRATOR,  # Route through orchestrator
                    parameters={
                        "app": {"type": "string", "const": app_id},
                        "input": {"type": "object"}
                    }
                ))

        # Register agent tools
        for agent_id, agent in self.agents.items():
            for tool_name in agent.tools:
                # Determine MCP agent type
                mcp_agent = self._get_mcp_agent(agent.agent_type, agent_id)

                mcp_server.register_tool(MCPTool(
                    name=f"{agent_id}_{tool_name}" if not tool_name.startswith(agent_id) else tool_name,
                    description=f"{agent.name}: {tool_name.replace('_', ' ')}",
                    agent=mcp_agent,
                    parameters={
                        "agent": {"type": "string", "const": agent_id},
                        "input": {"type": "object"}
                    }
                ))

        logger.info(f"Registered {len(mcp_server._tools)} MCP tools")

    def _get_mcp_agent(self, agent_type: AgentType, agent_id: str) -> MCPAgent:
        """Map agent type to MCP agent"""
        if agent_type == AgentType.BMAD:
            mapping = {
                "bmad-pm": MCPAgent.BMAD_PM,
                "bmad-architect": MCPAgent.BMAD_ARCHITECT,
                "bmad-developer": MCPAgent.BMAD_DEVELOPER,
                "bmad-analyst": MCPAgent.BMAD_ANALYST,
                "bmad-tester": MCPAgent.BMAD_TESTER,
            }
            return mapping.get(agent_id, MCPAgent.ORCHESTRATOR)

        if agent_type == AgentType.RAG or agent_id == "archon":
            return MCPAgent.ARCHON

        if agent_id == "bolt":
            return MCPAgent.BOLT

        return MCPAgent.ORCHESTRATOR

    # ================================================
    # QUERY METHODS
    # ================================================

    def get_app(self, app_id: str) -> Optional[AppDefinition]:
        """Get application by ID"""
        return self.apps.get(app_id)

    def get_agent(self, agent_id: str) -> Optional[AgentDefinition]:
        """Get agent by ID"""
        return self.agents.get(agent_id)

    def get_workflow(self, workflow_id: str) -> Optional[WorkflowDefinition]:
        """Get workflow by ID"""
        return self.workflows.get(workflow_id)

    def list_apps(self, category: AppCategory = None) -> List[AppDefinition]:
        """List all apps, optionally filtered by category"""
        if category:
            return [a for a in self.apps.values() if a.category == category]
        return list(self.apps.values())

    def list_agents(self, agent_type: AgentType = None) -> List[AgentDefinition]:
        """List all agents, optionally filtered by type"""
        if agent_type:
            return [a for a in self.agents.values() if a.agent_type == agent_type]
        return list(self.agents.values())

    def list_workflows(self) -> List[WorkflowDefinition]:
        """List all workflows"""
        return list(self.workflows.values())

    def get_dependencies(self, app_id: str) -> List[str]:
        """Get app dependencies"""
        app = self.apps.get(app_id)
        return app.dependencies if app else []

    def to_dict(self) -> Dict[str, Any]:
        """Export registry as dictionary"""
        return {
            "apps": {k: {
                "name": v.name,
                "category": v.category.value,
                "description": v.description,
                "tools": v.tools,
                "active": v.active
            } for k, v in self.apps.items()},
            "agents": {k: {
                "name": v.name,
                "type": v.agent_type.value,
                "description": v.description,
                "capabilities": v.capabilities
            } for k, v in self.agents.items()},
            "workflows": {k: {
                "name": v.name,
                "description": v.description,
                "stages": v.stages,
                "agents": v.agents_involved
            } for k, v in self.workflows.items()},
            "stats": {
                "total_apps": len(self.apps),
                "total_agents": len(self.agents),
                "total_workflows": len(self.workflows),
                "total_tools": len(mcp_server._tools)
            }
        }


# Singleton instance
mcp_registry = MCPRegistry()
