"""
IA Factory Automation - Analytics Dashboard
Suivi complet des KPIs business, revenus et métriques clients
Objectif: 95%+ marges, 100 clients Year 1, 500K+ CHF profit
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta, date
from enum import Enum
from decimal import Decimal
import json
import os

router = APIRouter(prefix="/analytics", tags=["Analytics Dashboard"])


# ===== ENUMS =====

class Market(str, Enum):
    CH = "Suisse"
    DZ = "Algérie"
    ALL = "Global"


class TenantTier(str, Enum):
    STARTER = "Starter"
    PROFESSIONAL = "Professional"
    ENTERPRISE = "Enterprise"


class MetricPeriod(str, Enum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"


class RevenueType(str, Enum):
    MRR = "Monthly Recurring Revenue"
    ARR = "Annual Recurring Revenue"
    ONE_TIME = "One-time"
    SETUP = "Setup Fee"
    SUPPORT = "Support Premium"


class ClientStatus(str, Enum):
    PROSPECT = "Prospect"
    TRIAL = "Trial"
    ACTIVE = "Active"
    CHURNED = "Churned"
    PAUSED = "Paused"


# ===== MODELS =====

class RevenueMetrics(BaseModel):
    """Métriques de revenus"""
    mrr: float = Field(description="Monthly Recurring Revenue en CHF")
    arr: float = Field(description="Annual Recurring Revenue en CHF")
    mrr_growth: float = Field(description="Croissance MRR %")
    avg_revenue_per_client: float = Field(description="ARPC en CHF")
    ltv: float = Field(description="Lifetime Value estimée")
    cac: float = Field(description="Customer Acquisition Cost")
    ltv_cac_ratio: float = Field(description="Ratio LTV/CAC (objectif >3)")


class ClientMetrics(BaseModel):
    """Métriques clients"""
    total_clients: int
    active_clients: int
    trial_clients: int
    churned_clients: int
    churn_rate: float = Field(description="Taux de churn mensuel %")
    net_promoter_score: float = Field(description="NPS -100 à +100")
    client_satisfaction: float = Field(description="CSAT 0-100%")
    clients_by_tier: Dict[str, int]
    clients_by_market: Dict[str, int]


class InfrastructureMetrics(BaseModel):
    """Métriques infrastructure"""
    total_servers: int
    active_containers: int
    total_capacity: int = Field(description="Nombre max de clients supportés")
    utilization_rate: float = Field(description="Taux d'utilisation %")
    uptime_percentage: float = Field(description="Uptime SLA %")
    avg_response_time_ms: float
    infrastructure_cost_monthly: float
    cost_per_client: float
    margin_percentage: float


class LeadMetrics(BaseModel):
    """Métriques leads et pipeline"""
    total_leads: int
    hot_leads: int
    warm_leads: int
    cold_leads: int
    conversion_rate: float = Field(description="Taux de conversion %")
    avg_deal_size: float
    pipeline_value: float
    leads_by_source: Dict[str, int]
    avg_sales_cycle_days: int


class ContentMetrics(BaseModel):
    """Métriques contenu et social media"""
    posts_scheduled: int
    posts_published: int
    total_impressions: int
    total_engagements: int
    engagement_rate: float
    followers_growth: Dict[str, int]
    top_performing_content: List[Dict[str, Any]]


class TeachingMetrics(BaseModel):
    """Métriques Teaching Assistant"""
    total_schools: int
    active_students: int
    lessons_generated: int
    exercises_generated: int
    exams_generated: int
    avg_usage_per_school: float
    subjects_popularity: Dict[str, int]


class DashboardSummary(BaseModel):
    """Résumé exécutif du dashboard"""
    period: str
    generated_at: datetime
    market: Market
    
    # KPIs principaux
    revenue: RevenueMetrics
    clients: ClientMetrics
    infrastructure: InfrastructureMetrics
    leads: LeadMetrics
    content: ContentMetrics
    teaching: TeachingMetrics
    
    # Alertes et recommandations
    alerts: List[Dict[str, Any]]
    recommendations: List[str]
    
    # Objectifs vs Réalité
    goals_progress: Dict[str, Dict[str, Any]]


# ===== PRICING TIERS (from infrastructure.py) =====

TIER_PRICING = {
    TenantTier.STARTER: {
        "monthly_chf": 500,
        "setup_chf": 1000,
        "target_margin": 0.90
    },
    TenantTier.PROFESSIONAL: {
        "monthly_chf": 900,
        "setup_chf": 2500,
        "target_margin": 0.92
    },
    TenantTier.ENTERPRISE: {
        "monthly_chf": 2500,
        "setup_chf": 5000,
        "target_margin": 0.95
    }
}

# ===== OBJECTIFS YEAR 1 =====

YEAR1_GOALS = {
    "total_clients": 100,
    "mrr_target": 60000,  # 60K CHF/month
    "arr_target": 720000,  # 720K CHF/year
    "profit_target": 500000,  # 500K+ CHF
    "churn_rate_max": 5.0,  # <5% mensuel
    "nps_min": 50,  # NPS > 50
    "uptime_min": 99.5,  # 99.5% SLA
    "ltv_cac_min": 3.0  # LTV/CAC > 3
}


class AnalyticsDashboard:
    """
    Dashboard analytique complet pour IA Factory
    Agrège toutes les métriques business
    """
    
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), "data")
        os.makedirs(self.data_path, exist_ok=True)
    
    # ===== REVENUE ANALYTICS =====
    
    def calculate_revenue_metrics(
        self,
        clients: List[Dict],
        period: MetricPeriod = MetricPeriod.MONTH
    ) -> RevenueMetrics:
        """Calcule les métriques de revenus"""
        
        if not clients:
            return RevenueMetrics(
                mrr=0, arr=0, mrr_growth=0,
                avg_revenue_per_client=0, ltv=0, cac=0, ltv_cac_ratio=0
            )
        
        # Calculer MRR
        active_clients = [c for c in clients if c.get("status") == "active"]
        mrr = sum(
            TIER_PRICING.get(TenantTier(c.get("tier", "Starter")), {}).get("monthly_chf", 500)
            for c in active_clients
        )
        
        # ARR = MRR * 12
        arr = mrr * 12
        
        # ARPC
        arpc = mrr / len(active_clients) if active_clients else 0
        
        # LTV (assumption: 24 mois de rétention moyenne)
        avg_retention_months = 24
        ltv = arpc * avg_retention_months
        
        # CAC (estimation basée sur coûts marketing)
        # En mode bootstrap, CAC très bas
        estimated_cac = 200  # CHF par client
        
        # LTV/CAC ratio
        ltv_cac = ltv / estimated_cac if estimated_cac > 0 else 0
        
        # Croissance MRR (simulation - à connecter aux données réelles)
        mrr_growth = 15.0  # % mensuel objectif
        
        return RevenueMetrics(
            mrr=mrr,
            arr=arr,
            mrr_growth=mrr_growth,
            avg_revenue_per_client=arpc,
            ltv=ltv,
            cac=estimated_cac,
            ltv_cac_ratio=ltv_cac
        )
    
    # ===== CLIENT ANALYTICS =====
    
    def calculate_client_metrics(self, clients: List[Dict]) -> ClientMetrics:
        """Calcule les métriques clients"""
        
        total = len(clients)
        active = len([c for c in clients if c.get("status") == "active"])
        trial = len([c for c in clients if c.get("status") == "trial"])
        churned = len([c for c in clients if c.get("status") == "churned"])
        
        # Churn rate
        churn_rate = (churned / total * 100) if total > 0 else 0
        
        # Distribution par tier
        by_tier = {}
        for tier in TenantTier:
            by_tier[tier.value] = len([
                c for c in clients if c.get("tier") == tier.value
            ])
        
        # Distribution par marché
        by_market = {
            Market.CH.value: len([c for c in clients if c.get("market") == "CH"]),
            Market.DZ.value: len([c for c in clients if c.get("market") == "DZ"])
        }
        
        return ClientMetrics(
            total_clients=total,
            active_clients=active,
            trial_clients=trial,
            churned_clients=churned,
            churn_rate=churn_rate,
            net_promoter_score=65.0,  # À connecter aux enquêtes
            client_satisfaction=92.0,  # À connecter au support
            clients_by_tier=by_tier,
            clients_by_market=by_market
        )
    
    # ===== INFRASTRUCTURE ANALYTICS =====
    
    def calculate_infrastructure_metrics(
        self,
        servers: List[Dict],
        containers: List[Dict]
    ) -> InfrastructureMetrics:
        """Calcule les métriques infrastructure"""
        
        # Specs TOPTON i9-14900: 20 clients/serveur
        clients_per_server = 20
        total_servers = len(servers) if servers else 1
        total_capacity = total_servers * clients_per_server
        
        active_containers = len([c for c in containers if c.get("status") == "running"]) if containers else 0
        utilization = (active_containers / total_capacity * 100) if total_capacity > 0 else 0
        
        # Coût infrastructure
        # TOPTON i9-14900: ~900 USD + hosting ~50 CHF/mois
        server_cost = 50  # CHF/mois amortissement
        hosting_cost = 50  # CHF/mois
        total_infra_cost = (server_cost + hosting_cost) * total_servers
        
        cost_per_client = total_infra_cost / active_containers if active_containers > 0 else 0
        
        # Revenus estimés (500 CHF/client moyen)
        revenue_per_client = 500
        margin = ((revenue_per_client - cost_per_client) / revenue_per_client * 100) if revenue_per_client > 0 else 0
        
        return InfrastructureMetrics(
            total_servers=total_servers,
            active_containers=active_containers,
            total_capacity=total_capacity,
            utilization_rate=utilization,
            uptime_percentage=99.9,  # À connecter au monitoring
            avg_response_time_ms=45.0,  # À connecter à Prometheus
            infrastructure_cost_monthly=total_infra_cost,
            cost_per_client=cost_per_client,
            margin_percentage=margin
        )
    
    # ===== LEAD ANALYTICS =====
    
    def calculate_lead_metrics(self, leads: List[Dict]) -> LeadMetrics:
        """Calcule les métriques pipeline"""
        
        total = len(leads)
        hot = len([l for l in leads if l.get("category") == "HOT"])
        warm = len([l for l in leads if l.get("category") == "WARM"])
        cold = len([l for l in leads if l.get("category") == "COLD"])
        
        # Conversion rate (leads → clients)
        converted = len([l for l in leads if l.get("converted")])
        conversion_rate = (converted / total * 100) if total > 0 else 0
        
        # Pipeline value
        pipeline = sum(l.get("estimated_value", 0) for l in leads if not l.get("converted"))
        
        # Sources
        by_source = {}
        for lead in leads:
            source = lead.get("source", "Direct")
            by_source[source] = by_source.get(source, 0) + 1
        
        return LeadMetrics(
            total_leads=total,
            hot_leads=hot,
            warm_leads=warm,
            cold_leads=cold,
            conversion_rate=conversion_rate,
            avg_deal_size=1500.0,  # CHF moyen (setup + 2 mois)
            pipeline_value=pipeline,
            leads_by_source=by_source,
            avg_sales_cycle_days=14
        )
    
    # ===== CONTENT ANALYTICS =====
    
    def calculate_content_metrics(self, posts: List[Dict]) -> ContentMetrics:
        """Calcule les métriques social media"""
        
        scheduled = len([p for p in posts if p.get("status") == "scheduled"])
        published = len([p for p in posts if p.get("status") == "published"])
        
        impressions = sum(p.get("impressions", 0) for p in posts)
        engagements = sum(p.get("engagements", 0) for p in posts)
        
        engagement_rate = (engagements / impressions * 100) if impressions > 0 else 0
        
        # Top performers
        top = sorted(posts, key=lambda x: x.get("engagements", 0), reverse=True)[:5]
        
        return ContentMetrics(
            posts_scheduled=scheduled,
            posts_published=published,
            total_impressions=impressions,
            total_engagements=engagements,
            engagement_rate=engagement_rate,
            followers_growth={
                "LinkedIn": 250,
                "X": 150,
                "Instagram": 100
            },
            top_performing_content=[
                {"title": p.get("title", ""), "engagements": p.get("engagements", 0)}
                for p in top
            ]
        )
    
    # ===== TEACHING ANALYTICS =====
    
    def calculate_teaching_metrics(self, schools: List[Dict]) -> TeachingMetrics:
        """Calcule les métriques Teaching Assistant"""
        
        total_schools = len(schools)
        students = sum(s.get("students", 0) for s in schools)
        lessons = sum(s.get("lessons_generated", 0) for s in schools)
        exercises = sum(s.get("exercises_generated", 0) for s in schools)
        exams = sum(s.get("exams_generated", 0) for s in schools)
        
        avg_usage = (lessons + exercises + exams) / total_schools if total_schools > 0 else 0
        
        # Popularité par matière
        subjects = {}
        for school in schools:
            for subj, count in school.get("subjects_usage", {}).items():
                subjects[subj] = subjects.get(subj, 0) + count
        
        return TeachingMetrics(
            total_schools=total_schools,
            active_students=students,
            lessons_generated=lessons,
            exercises_generated=exercises,
            exams_generated=exams,
            avg_usage_per_school=avg_usage,
            subjects_popularity=subjects
        )
    
    # ===== GOALS TRACKING =====
    
    def track_goals_progress(
        self,
        revenue: RevenueMetrics,
        clients: ClientMetrics,
        infra: InfrastructureMetrics
    ) -> Dict[str, Dict[str, Any]]:
        """Suivi des objectifs Year 1"""
        
        return {
            "clients": {
                "target": YEAR1_GOALS["total_clients"],
                "current": clients.total_clients,
                "progress": (clients.total_clients / YEAR1_GOALS["total_clients"] * 100),
                "status": "on_track" if clients.total_clients >= YEAR1_GOALS["total_clients"] * 0.8 else "behind"
            },
            "mrr": {
                "target": YEAR1_GOALS["mrr_target"],
                "current": revenue.mrr,
                "progress": (revenue.mrr / YEAR1_GOALS["mrr_target"] * 100),
                "status": "on_track" if revenue.mrr >= YEAR1_GOALS["mrr_target"] * 0.8 else "behind"
            },
            "churn": {
                "target": YEAR1_GOALS["churn_rate_max"],
                "current": clients.churn_rate,
                "progress": 100 - clients.churn_rate,
                "status": "on_track" if clients.churn_rate <= YEAR1_GOALS["churn_rate_max"] else "warning"
            },
            "nps": {
                "target": YEAR1_GOALS["nps_min"],
                "current": clients.net_promoter_score,
                "progress": (clients.net_promoter_score / 100 * 100),
                "status": "on_track" if clients.net_promoter_score >= YEAR1_GOALS["nps_min"] else "behind"
            },
            "uptime": {
                "target": YEAR1_GOALS["uptime_min"],
                "current": infra.uptime_percentage,
                "progress": infra.uptime_percentage,
                "status": "on_track" if infra.uptime_percentage >= YEAR1_GOALS["uptime_min"] else "critical"
            },
            "margins": {
                "target": 95.0,
                "current": infra.margin_percentage,
                "progress": infra.margin_percentage,
                "status": "on_track" if infra.margin_percentage >= 90 else "warning"
            }
        }
    
    # ===== ALERTS & RECOMMENDATIONS =====
    
    def generate_alerts(
        self,
        clients: ClientMetrics,
        infra: InfrastructureMetrics,
        leads: LeadMetrics
    ) -> List[Dict[str, Any]]:
        """Génère des alertes automatiques"""
        
        alerts = []
        
        # Alert: Churn élevé
        if clients.churn_rate > 5:
            alerts.append({
                "level": "warning",
                "category": "churn",
                "message": f"Taux de churn à {clients.churn_rate}% - Objectif < 5%",
                "action": "Analyser les raisons de départ, contacter clients à risque"
            })
        
        # Alert: Capacité infrastructure
        if infra.utilization_rate > 80:
            alerts.append({
                "level": "info",
                "category": "infrastructure",
                "message": f"Utilisation serveurs à {infra.utilization_rate}%",
                "action": "Planifier l'ajout d'un nouveau serveur TOPTON"
            })
        
        # Alert: Pipeline faible
        if leads.hot_leads < 5:
            alerts.append({
                "level": "warning",
                "category": "sales",
                "message": f"Seulement {leads.hot_leads} leads chauds",
                "action": "Intensifier le contenu LinkedIn et les campagnes outreach"
            })
        
        # Alert: Uptime
        if infra.uptime_percentage < 99.5:
            alerts.append({
                "level": "critical",
                "category": "sla",
                "message": f"Uptime à {infra.uptime_percentage}% - SLA menacé",
                "action": "Investigation urgente des causes de downtime"
            })
        
        return alerts
    
    def generate_recommendations(
        self,
        revenue: RevenueMetrics,
        clients: ClientMetrics,
        goals: Dict
    ) -> List[str]:
        """Génère des recommandations stratégiques"""
        
        recs = []
        
        # Recommandations basées sur les objectifs
        if goals["clients"]["status"] == "behind":
            recs.append(
                "🎯 Accélérer l'acquisition: Cibler 5 écoles DZ supplémentaires cette semaine"
            )
        
        if revenue.ltv_cac_ratio < 3:
            recs.append(
                "💰 Améliorer LTV/CAC: Réduire CAC via referrals ou augmenter rétention"
            )
        
        if clients.clients_by_tier.get("Enterprise", 0) < 2:
            recs.append(
                "🏢 Upsell Enterprise: Identifier 3 clients Pro à upgrader"
            )
        
        # Recommandations marchés
        dz_clients = clients.clients_by_market.get("Algérie", 0)
        ch_clients = clients.clients_by_market.get("Suisse", 0)
        
        if dz_clients < ch_clients:
            recs.append(
                "🇩🇿 Développer marché DZ: Potentiel sous-exploité, focus Algérie Télécom"
            )
        
        # Recommandation infrastructure
        recs.append(
            "🖥️ Commander 2ème TOPTON i9-14900 quand utilisation > 70%"
        )
        
        return recs
    
    # ===== MAIN DASHBOARD =====
    
    def get_full_dashboard(
        self,
        market: Market = Market.ALL,
        period: MetricPeriod = MetricPeriod.MONTH
    ) -> DashboardSummary:
        """Génère le dashboard complet"""
        
        # Simulation de données (à connecter aux vraies sources)
        # En production: intégration Supabase, Stripe, etc.
        
        sample_clients = [
            {"id": "1", "name": "École Nouvelle Horizon", "tier": "Professional", "market": "DZ", "status": "active"},
            {"id": "2", "name": "BBC School", "tier": "Professional", "market": "DZ", "status": "active"},
            {"id": "3", "name": "PME Suisse Demo", "tier": "Starter", "market": "CH", "status": "trial"},
            {"id": "4", "name": "Algérie Télécom", "tier": "Enterprise", "market": "DZ", "status": "prospect"},
        ]
        
        sample_leads = [
            {"id": "1", "company": "Algérie Télécom", "category": "HOT", "source": "Meeting", "estimated_value": 50000},
            {"id": "2", "company": "Mobilis", "category": "WARM", "source": "LinkedIn", "estimated_value": 30000},
            {"id": "3", "company": "Startup XYZ", "category": "COLD", "source": "Website", "estimated_value": 5000},
        ]
        
        sample_posts = [
            {"id": "1", "title": "IA pour PME", "status": "published", "impressions": 5000, "engagements": 250},
            {"id": "2", "title": "Success Story DZ", "status": "published", "impressions": 8000, "engagements": 400},
            {"id": "3", "title": "Tutoriel RAG", "status": "scheduled", "impressions": 0, "engagements": 0},
        ]
        
        sample_schools = [
            {
                "id": "1", "name": "École Nouvelle Horizon", "students": 500,
                "lessons_generated": 120, "exercises_generated": 350, "exams_generated": 25,
                "subjects_usage": {"Mathématiques": 150, "Français": 100, "Physique": 80}
            },
            {
                "id": "2", "name": "BBC School", "students": 300,
                "lessons_generated": 80, "exercises_generated": 200, "exams_generated": 15,
                "subjects_usage": {"Anglais": 120, "Mathématiques": 60, "Informatique": 50}
            }
        ]
        
        # Calculer toutes les métriques
        revenue = self.calculate_revenue_metrics(sample_clients, period)
        clients = self.calculate_client_metrics(sample_clients)
        infra = self.calculate_infrastructure_metrics([], [])
        leads = self.calculate_lead_metrics(sample_leads)
        content = self.calculate_content_metrics(sample_posts)
        teaching = self.calculate_teaching_metrics(sample_schools)
        
        # Goals tracking
        goals = self.track_goals_progress(revenue, clients, infra)
        
        # Alerts & recommendations
        alerts = self.generate_alerts(clients, infra, leads)
        recommendations = self.generate_recommendations(revenue, clients, goals)
        
        return DashboardSummary(
            period=period.value,
            generated_at=datetime.now(),
            market=market,
            revenue=revenue,
            clients=clients,
            infrastructure=infra,
            leads=leads,
            content=content,
            teaching=teaching,
            alerts=alerts,
            recommendations=recommendations,
            goals_progress=goals
        )


# ===== API ENDPOINTS =====

dashboard = AnalyticsDashboard()


@router.get("/dashboard", response_model=DashboardSummary)
async def get_dashboard(
    market: Market = Query(default=Market.ALL, description="Filtre par marché"),
    period: MetricPeriod = Query(default=MetricPeriod.MONTH, description="Période d'analyse")
):
    """
    📊 Dashboard Exécutif Complet
    
    Retourne toutes les métriques business:
    - Revenus (MRR, ARR, LTV, CAC)
    - Clients (actifs, churn, NPS)
    - Infrastructure (utilisation, coûts, marges)
    - Pipeline (leads, conversion)
    - Content (engagement, reach)
    - Teaching (écoles, usage)
    """
    return dashboard.get_full_dashboard(market, period)


@router.get("/revenue")
async def get_revenue_metrics(
    period: MetricPeriod = Query(default=MetricPeriod.MONTH)
):
    """💰 Métriques de revenus uniquement"""
    full = dashboard.get_full_dashboard(period=period)
    return {
        "period": period.value,
        "metrics": full.revenue,
        "goals": full.goals_progress.get("mrr")
    }


@router.get("/clients")
async def get_client_metrics():
    """👥 Métriques clients uniquement"""
    full = dashboard.get_full_dashboard()
    return {
        "metrics": full.clients,
        "goals": {
            "clients": full.goals_progress.get("clients"),
            "churn": full.goals_progress.get("churn"),
            "nps": full.goals_progress.get("nps")
        }
    }


@router.get("/infrastructure")
async def get_infrastructure_metrics():
    """🖥️ Métriques infrastructure uniquement"""
    full = dashboard.get_full_dashboard()
    return {
        "metrics": full.infrastructure,
        "goals": {
            "uptime": full.goals_progress.get("uptime"),
            "margins": full.goals_progress.get("margins")
        },
        "recommendation": "TOPTON i9-14900 (~900 USD) supporte 20 clients avec 95%+ marges"
    }


@router.get("/pipeline")
async def get_pipeline_metrics():
    """📈 Métriques pipeline commercial"""
    full = dashboard.get_full_dashboard()
    return {
        "metrics": full.leads,
        "hot_opportunities": [
            {
                "company": "Algérie Télécom",
                "potential": "50K CHF",
                "next_step": "Relancer après meeting du 6 décembre",
                "priority": "CRITICAL"
            }
        ]
    }


@router.get("/teaching")
async def get_teaching_metrics():
    """🎓 Métriques Teaching Assistant"""
    full = dashboard.get_full_dashboard()
    return {
        "metrics": full.teaching,
        "active_schools": ["École Nouvelle Horizon", "BBC School"],
        "growth_potential": "Marketplace Teaching Assistant = Quick Win #1"
    }


@router.get("/alerts")
async def get_alerts():
    """🚨 Alertes actives"""
    full = dashboard.get_full_dashboard()
    return {
        "total_alerts": len(full.alerts),
        "alerts": full.alerts,
        "critical_count": len([a for a in full.alerts if a["level"] == "critical"]),
        "warning_count": len([a for a in full.alerts if a["level"] == "warning"])
    }


@router.get("/recommendations")
async def get_recommendations():
    """💡 Recommandations stratégiques"""
    full = dashboard.get_full_dashboard()
    return {
        "recommendations": full.recommendations,
        "top_3_priorities": [
            "1️⃣ Teaching Assistant Marketplace - Monétiser clients existants",
            "2️⃣ Multi-tenant Infrastructure - Commander TOPTON i9-14900",
            "3️⃣ Algérie Télécom - Relance post-meeting décembre"
        ]
    }


@router.get("/goals")
async def get_goals_progress():
    """🎯 Progression vers objectifs Year 1"""
    full = dashboard.get_full_dashboard()
    return {
        "year1_targets": YEAR1_GOALS,
        "current_progress": full.goals_progress,
        "overall_status": "on_track" if all(
            g["status"] == "on_track" for g in full.goals_progress.values()
        ) else "needs_attention"
    }


@router.post("/report/executive")
async def generate_executive_report(
    period: MetricPeriod = Query(default=MetricPeriod.MONTH)
):
    """
    📋 Génère un rapport exécutif complet
    
    Utilisable pour:
    - Réunions board
    - Rapports investisseurs
    - Bilans mensuels
    """
    full = dashboard.get_full_dashboard(period=period)
    
    return {
        "report_type": "Executive Summary",
        "period": period.value,
        "generated_at": datetime.now().isoformat(),
        
        "headline_metrics": {
            "mrr": f"{full.revenue.mrr:,.0f} CHF",
            "clients": full.clients.active_clients,
            "margin": f"{full.infrastructure.margin_percentage:.1f}%",
            "nps": full.clients.net_promoter_score
        },
        
        "key_achievements": [
            f"✅ {full.clients.active_clients} clients actifs",
            f"✅ Marge opérationnelle {full.infrastructure.margin_percentage:.0f}%",
            f"✅ NPS de {full.clients.net_promoter_score}"
        ],
        
        "challenges": [
            a["message"] for a in full.alerts if a["level"] in ["warning", "critical"]
        ],
        
        "next_steps": full.recommendations[:3],
        
        "90_day_roadmap": [
            "Jours 1-30: Déployer Teaching Assistant Marketplace",
            "Jours 31-60: Commander et configurer TOPTON i9-14900",
            "Jours 61-90: Signer 10 nouveaux clients (5 DZ, 5 CH)"
        ]
    }
