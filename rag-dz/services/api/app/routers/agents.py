"""
IA Factory Agents Router - Professional Multi-Agent API
All agents accessible via unified REST endpoints
"""

import os
import sys
from typing import Dict, Any, Optional, List
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from datetime import datetime
import logging
import asyncio

# Add ia-factory-agents to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'ia-factory-agents'))

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/agents", tags=["AI Agents"])

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class AgentRequest(BaseModel):
    """Base request for all agents"""
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    language: str = "fr"
    country: str = "algeria"  # algeria or switzerland

class FinancialCoachRequest(AgentRequest):
    """Financial Coach Agent Request"""
    monthly_income: float
    monthly_expenses: float
    savings_goal: Optional[float] = None
    debt: float = 0
    goals: List[str] = Field(default_factory=list)

class BudgetPlannerRequest(AgentRequest):
    """Budget Planner Request"""
    income: float
    expense_categories: Dict[str, float] = Field(default_factory=dict)

class ContractAnalysisRequest(AgentRequest):
    """Contract Analysis Request"""
    contract_text: str
    contract_type: str = "general"

class RecruitmentRequest(AgentRequest):
    """Recruitment Agent Request"""
    job_title: str
    job_description: str
    required_skills: List[str] = Field(default_factory=list)
    experience_years: int = 0
    location: str = "Alger"

class RealEstateRequest(AgentRequest):
    """Real Estate Agent Request"""
    property_type: str  # apartment, house, commercial, land
    transaction_type: str  # buy, rent, sell
    location: str
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    surface_min: Optional[float] = None
    rooms: Optional[int] = None

class TravelRequest(AgentRequest):
    """Travel Agent Request"""
    destination: str
    departure_city: str = "Alger"
    travel_dates: Optional[str] = None
    travelers: int = 1
    budget: Optional[float] = None
    preferences: List[str] = Field(default_factory=list)

class TeachingRequest(AgentRequest):
    """Teaching Agent Request"""
    subject: str
    level: str  # primaire, college, lycee, universite, professionnel
    topic: str
    learning_style: str = "visual"  # visual, auditory, kinesthetic

class AgentResponse(BaseModel):
    """Unified Agent Response"""
    success: bool
    agent: str
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    tokens_used: Optional[int] = None
    duration_ms: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.now)

# ============================================================================
# LLM CLIENT (DeepSeek/OpenAI/Claude)
# ============================================================================

async def call_llm(
    messages: List[Dict[str, str]],
    model: str = "gpt-4o-mini",
    temperature: float = 0.7,
    max_tokens: int = 2000
) -> Dict[str, Any]:
    """Universal LLM caller with auto-fallback: OpenAI -> Claude -> DeepSeek"""
    from openai import AsyncOpenAI

    # Try OpenAI first (fast and reliable)
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        try:
            client = AsyncOpenAI(api_key=openai_key)
            start_time = datetime.now()
            completion = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            duration = (datetime.now() - start_time).total_seconds() * 1000
            return {
                "content": completion.choices[0].message.content,
                "tokens": completion.usage.total_tokens if completion.usage else 0,
                "duration_ms": duration,
                "provider": "openai"
            }
        except Exception as e:
            logger.warning(f"OpenAI failed: {e}, trying Claude...")

    # Try Claude second (high quality)
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if anthropic_key:
        try:
            import anthropic
            client = anthropic.AsyncAnthropic(api_key=anthropic_key)
            start_time = datetime.now()
            response = await client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=max_tokens,
                messages=messages
            )
            duration = (datetime.now() - start_time).total_seconds() * 1000
            return {
                "content": response.content[0].text,
                "tokens": response.usage.input_tokens + response.usage.output_tokens,
                "duration_ms": duration,
                "provider": "anthropic"
            }
        except Exception as e:
            logger.warning(f"Claude failed: {e}, trying DeepSeek...")

    # Try DeepSeek last (cheap fallback)
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    if deepseek_key:
        try:
            client = AsyncOpenAI(api_key=deepseek_key, base_url="https://api.deepseek.com")
            start_time = datetime.now()
            completion = await client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            duration = (datetime.now() - start_time).total_seconds() * 1000
            return {
                "content": completion.choices[0].message.content,
                "tokens": completion.usage.total_tokens if completion.usage else 0,
                "duration_ms": duration,
                "provider": "deepseek"
            }
        except Exception as e:
            logger.error(f"DeepSeek failed: {e}")

    return {"content": "Erreur: Aucun provider LLM disponible", "tokens": 0, "duration_ms": 0, "provider": "none"}

# ============================================================================
# KNOWLEDGE BASES
# ============================================================================

FINANCIAL_KNOWLEDGE = {
    "algeria": {
        "currency": "DZD",
        "avg_salary": 40000,
        "inflation_rate": 9.3,
        "savings_rate_recommended": 20,
        "tax_brackets": "0-20%, 20-35%",
        "min_wage": 20000
    },
    "switzerland": {
        "currency": "CHF",
        "avg_salary": 6500,
        "inflation_rate": 1.7,
        "savings_rate_recommended": 15,
        "pillar_3a_max": 7056,
        "tax_varies": "Canton-dependent"
    }
}

LEGAL_KNOWLEDGE = {
    "algeria": {
        "main_codes": ["Code Civil", "Code du Commerce", "Code du Travail", "Code de la Famille"],
        "business_types": ["SARL", "SPA", "EURL", "SNC", "EI"],
        "labor_law": {"min_wage": 20000, "work_hours": "40h/semaine", "paid_leave": "30 jours/an"}
    },
    "switzerland": {
        "main_codes": ["Code Civil Suisse (CC)", "Code des Obligations (CO)", "Code Pénal Suisse (CP)"],
        "business_types": ["SA", "Sàrl", "Raison Individuelle", "SNC"],
        "labor_law": {"work_hours": "41-50h/semaine", "paid_leave": "4 semaines min", "trial_period": "1-3 mois"}
    }
}

REAL_ESTATE_KNOWLEDGE = {
    "algeria": {
        "avg_price_m2": {"alger": 180000, "oran": 120000, "constantine": 100000},
        "rental_yield": "4-6%",
        "notary_fees": "2.5%",
        "registration_tax": "5%"
    },
    "switzerland": {
        "avg_price_m2": {"geneve": 15000, "zurich": 14000, "lausanne": 12000},
        "rental_yield": "2-4%",
        "notary_fees": "0.5-1%",
        "property_tax": "Canton-dependent"
    }
}

# ============================================================================
# AGENT ENDPOINTS
# ============================================================================

@router.get("/health")
async def agents_health():
    """Health check for agents service"""
    return {
        "status": "healthy",
        "service": "ia-factory-agents",
        "version": "1.0.0",
        "agents_available": [
            "financial-coach", "budget-planner", "contract-analyst",
            "recruitment", "real-estate", "travel", "teaching"
        ],
        "markets": ["algeria", "switzerland"],
        "llm_providers": ["deepseek", "openai", "anthropic"]
    }

@router.post("/financial-coach", response_model=AgentResponse)
async def financial_coach(request: FinancialCoachRequest):
    """
    Financial Coach Agent - Personal finance advisor for PMEs and individuals

    Supports: Algeria (DZD) and Switzerland (CHF) markets
    """
    try:
        financial_data = FINANCIAL_KNOWLEDGE.get(request.country, FINANCIAL_KNOWLEDGE["algeria"])

        system_prompt = f"""Tu es un coach financier expert certifié, spécialisé en finances personnelles et PME.

CONTEXTE MARCHÉ: {request.country.upper()}
Données économiques: {financial_data}

SITUATION CLIENT:
- Revenu mensuel: {request.monthly_income} {financial_data['currency']}
- Dépenses mensuelles: {request.monthly_expenses} {financial_data['currency']}
- Capacité d'épargne: {request.monthly_income - request.monthly_expenses} {financial_data['currency']}
- Objectif épargne: {request.savings_goal or 'Non défini'}
- Dettes actuelles: {request.debt} {financial_data['currency']}
- Objectifs: {', '.join(request.goals) if request.goals else 'Non définis'}

ANALYSE COMPLÈTE:

1. 📊 DIAGNOSTIC BUDGET
   - Ratio dépenses/revenus
   - Santé financière globale
   - Points d'alerte

2. 💡 PLAN D'OPTIMISATION
   - Réduction des dépenses possibles
   - Postes à surveiller
   - Quick wins

3. 🎯 STRATÉGIE ÉPARGNE
   - Épargne de précaution (3-6 mois)
   - Épargne projet
   - Investissement long terme

4. 💳 GESTION DETTES
   - Priorisation remboursement
   - Stratégie avalanche/boule de neige
   - Négociation taux

5. 📈 INVESTISSEMENT
   - Options adaptées au profil
   - Diversification recommandée
   - Horizon temporel

6. 📋 OPTIMISATION FISCALE ({request.country.upper()})
   - Déductions possibles
   - Avantages fiscaux
   - Structuration optimale

7. ✅ PLAN D'ACTION 90 JOURS
   - Actions immédiates (J1-J7)
   - Actions court terme (S2-S4)
   - Actions moyen terme (M2-M3)

⚠️ DISCLAIMER: Ces conseils sont informatifs. Consultez un conseiller financier agréé pour des décisions importantes.

Langue: Français. Sois précis, actionnable et encourageant."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Analyse ma situation financière et crée mon plan personnalisé."}
        ]

        result = await call_llm(messages, temperature=0.6)

        savings_capacity = request.monthly_income - request.monthly_expenses
        savings_rate = (savings_capacity / request.monthly_income * 100) if request.monthly_income > 0 else 0

        return AgentResponse(
            success=True,
            agent="financial-coach",
            content=result["content"],
            metadata={
                "country": request.country,
                "currency": financial_data["currency"],
                "savings_capacity": savings_capacity,
                "savings_rate": round(savings_rate, 1),
                "debt_to_income": round(request.debt / request.monthly_income * 100, 1) if request.monthly_income > 0 else 0,
                "financial_health": "good" if savings_rate >= 20 else "warning" if savings_rate >= 10 else "critical"
            },
            tokens_used=result.get("tokens"),
            duration_ms=result.get("duration_ms")
        )
    except Exception as e:
        logger.error(f"Financial coach error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/budget-planner", response_model=AgentResponse)
async def budget_planner(request: BudgetPlannerRequest):
    """
    Budget Planner Agent - 50/30/20 budget methodology
    """
    try:
        financial_data = FINANCIAL_KNOWLEDGE.get(request.country, FINANCIAL_KNOWLEDGE["algeria"])

        system_prompt = f"""Tu es un expert en planification budgétaire.

MÉTHODE: Règle 50/30/20
- 50% Besoins essentiels (loyer, nourriture, transport, santé)
- 30% Envies (loisirs, shopping, sorties)
- 20% Épargne et investissement

REVENU MENSUEL: {request.income} {financial_data['currency']}

RÉPARTITION IDÉALE:
- Besoins: {request.income * 0.5} {financial_data['currency']}
- Envies: {request.income * 0.3} {financial_data['currency']}
- Épargne: {request.income * 0.2} {financial_data['currency']}

CATÉGORIES ACTUELLES:
{request.expense_categories}

Crée:
1. 📊 Budget détaillé par catégorie avec montants précis
2. 📈 Comparaison situation actuelle vs idéale
3. ⚠️ Alertes sur les dépassements
4. ✅ Ajustements concrets à faire
5. 📱 Outils de suivi recommandés

Format: Tableaux clairs et actions concrètes."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Crée mon plan budgétaire détaillé."}
        ]

        result = await call_llm(messages, temperature=0.5)

        return AgentResponse(
            success=True,
            agent="budget-planner",
            content=result["content"],
            metadata={
                "income": request.income,
                "ideal_needs": request.income * 0.5,
                "ideal_wants": request.income * 0.3,
                "ideal_savings": request.income * 0.2,
                "method": "50/30/20"
            },
            tokens_used=result.get("tokens"),
            duration_ms=result.get("duration_ms")
        )
    except Exception as e:
        logger.error(f"Budget planner error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/contract-analyst", response_model=AgentResponse)
async def contract_analyst(request: ContractAnalysisRequest):
    """
    Contract Analyst Agent - Legal document analysis for Algeria and Switzerland
    """
    try:
        legal_data = LEGAL_KNOWLEDGE.get(request.country, LEGAL_KNOWLEDGE["algeria"])

        system_prompt = f"""Tu es un expert juridique senior spécialisé en droit {request.country.upper()}.

SYSTÈME JURIDIQUE: {request.country.upper()}
Codes applicables: {', '.join(legal_data['main_codes'])}
Droit du travail: {legal_data['labor_law']}

TYPE DE CONTRAT: {request.contract_type}

ANALYSE DU CONTRAT:

1. 📋 SYNTHÈSE EXÉCUTIVE
   - Nature du contrat
   - Parties concernées
   - Objet principal
   - Durée et conditions

2. 📄 CLAUSES PRINCIPALES
   - Obligations de chaque partie
   - Conditions financières
   - Modalités d'exécution

3. ⚠️ POINTS D'ATTENTION CRITIQUES
   - Clauses abusives potentielles
   - Déséquilibres contractuels
   - Zones de risque

4. ✅ CONFORMITÉ LÉGALE
   - Respect du Code Civil
   - Respect du Code du Travail (si applicable)
   - Obligations légales manquantes

5. 🚨 RISQUES IDENTIFIÉS
   - Risques juridiques
   - Risques financiers
   - Risques opérationnels

6. 💡 RECOMMANDATIONS
   - Modifications suggérées
   - Clauses à ajouter
   - Points à négocier

7. 📝 CONCLUSION
   - Avis global
   - Note de risque (1-10)
   - Recommandation finale

⚠️ DISCLAIMER: Cette analyse est informative. Consultez un avocat pour validation juridique.

CONTRAT À ANALYSER:
{request.contract_text[:5000]}"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Analyse ce contrat en détail."}
        ]

        result = await call_llm(messages, temperature=0.3, max_tokens=3000)

        return AgentResponse(
            success=True,
            agent="contract-analyst",
            content=result["content"],
            metadata={
                "country": request.country,
                "contract_type": request.contract_type,
                "legal_system": legal_data["main_codes"],
                "analysis_depth": "comprehensive"
            },
            tokens_used=result.get("tokens"),
            duration_ms=result.get("duration_ms")
        )
    except Exception as e:
        logger.error(f"Contract analyst error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recruitment", response_model=AgentResponse)
async def recruitment_agent(request: RecruitmentRequest):
    """
    Recruitment Agent - AI-powered hiring assistant
    """
    try:
        system_prompt = f"""Tu es un expert RH senior spécialisé en recrutement ({request.country.upper()}).

POSTE À POURVOIR:
- Titre: {request.job_title}
- Localisation: {request.location}
- Expérience requise: {request.experience_years} ans
- Compétences: {', '.join(request.required_skills)}

DESCRIPTION:
{request.job_description}

GÉNÈRE:

1. 📋 FICHE DE POSTE OPTIMISÉE
   - Titre attractif
   - Missions principales
   - Compétences requises/souhaitées
   - Avantages du poste

2. 🎯 PROFIL CANDIDAT IDÉAL
   - Hard skills
   - Soft skills
   - Expérience type
   - Formation

3. 📝 GRILLE D'ENTRETIEN
   - Questions techniques (5)
   - Questions comportementales (5)
   - Mises en situation (3)
   - Points à vérifier

4. ✅ CRITÈRES D'ÉVALUATION
   - Grille de notation
   - Red flags à surveiller
   - Green flags à valoriser

5. 💰 BENCHMARK SALAIRE ({request.country.upper()})
   - Fourchette marché
   - Facteurs de variation
   - Package recommandé

6. 📢 STRATÉGIE SOURCING
   - Canaux recommandés
   - Messages d'approche
   - Timing optimal"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Crée le dossier de recrutement complet."}
        ]

        result = await call_llm(messages, temperature=0.6, max_tokens=2500)

        return AgentResponse(
            success=True,
            agent="recruitment",
            content=result["content"],
            metadata={
                "job_title": request.job_title,
                "location": request.location,
                "experience_years": request.experience_years,
                "skills_count": len(request.required_skills)
            },
            tokens_used=result.get("tokens"),
            duration_ms=result.get("duration_ms")
        )
    except Exception as e:
        logger.error(f"Recruitment agent error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/real-estate", response_model=AgentResponse)
async def real_estate_agent(request: RealEstateRequest):
    """
    Real Estate Agent - Property advisor for Algeria and Switzerland
    """
    try:
        re_data = REAL_ESTATE_KNOWLEDGE.get(request.country, REAL_ESTATE_KNOWLEDGE["algeria"])

        system_prompt = f"""Tu es un expert immobilier senior ({request.country.upper()}).

MARCHÉ: {request.country.upper()}
Prix moyens/m²: {re_data['avg_price_m2']}
Rendement locatif: {re_data['rental_yield']}
Frais de notaire: {re_data['notary_fees']}

RECHERCHE CLIENT:
- Type de bien: {request.property_type}
- Transaction: {request.transaction_type}
- Localisation: {request.location}
- Budget: {request.budget_min or 'Non défini'} - {request.budget_max or 'Non défini'}
- Surface min: {request.surface_min or 'Non définie'} m²
- Pièces: {request.rooms or 'Non défini'}

ANALYSE:

1. 📊 ÉTUDE DE MARCHÉ
   - Prix au m² dans la zone
   - Tendances du marché
   - Opportunités actuelles

2. 🏠 BIENS RECOMMANDÉS
   - Critères de recherche optimisés
   - Quartiers recommandés
   - Types de biens adaptés

3. 💰 ANALYSE FINANCIÈRE
   - Budget total (bien + frais)
   - Simulation crédit
   - Rendement potentiel (si investissement)

4. 📋 CHECKLIST VISITE
   - Points à vérifier
   - Questions à poser
   - Documents à demander

5. ⚖️ ASPECTS JURIDIQUES
   - Documents nécessaires
   - Procédure d'achat/location
   - Pièges à éviter

6. 💡 RECOMMANDATIONS
   - Stratégie de négociation
   - Timing optimal
   - Alternatives à considérer"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Aide-moi dans ma recherche immobilière."}
        ]

        result = await call_llm(messages, temperature=0.6)

        return AgentResponse(
            success=True,
            agent="real-estate",
            content=result["content"],
            metadata={
                "property_type": request.property_type,
                "transaction_type": request.transaction_type,
                "location": request.location,
                "market_data": re_data
            },
            tokens_used=result.get("tokens"),
            duration_ms=result.get("duration_ms")
        )
    except Exception as e:
        logger.error(f"Real estate agent error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/travel", response_model=AgentResponse)
async def travel_agent(request: TravelRequest):
    """
    Travel Agent - AI travel planner
    """
    try:
        system_prompt = f"""Tu es un agent de voyage expert avec 20 ans d'expérience.

DEMANDE VOYAGE:
- Destination: {request.destination}
- Départ: {request.departure_city}
- Dates: {request.travel_dates or 'Flexibles'}
- Voyageurs: {request.travelers}
- Budget: {request.budget or 'Non défini'}
- Préférences: {', '.join(request.preferences) if request.preferences else 'Aucune spécifiée'}

PLAN DE VOYAGE:

1. ✈️ OPTIONS TRANSPORT
   - Vols recommandés
   - Alternatives (train, bus)
   - Meilleurs prix/horaires

2. 🏨 HÉBERGEMENT
   - Hôtels recommandés par gamme
   - Quartiers conseillés
   - Alternatives (Airbnb, etc.)

3. 📅 ITINÉRAIRE DÉTAILLÉ
   - Jour par jour
   - Activités incontournables
   - Expériences uniques

4. 🍽️ GASTRONOMIE
   - Restaurants recommandés
   - Spécialités locales
   - Budget repas

5. 💡 CONSEILS PRATIQUES
   - Visa/formalités
   - Santé/vaccins
   - Sécurité
   - Pourboires

6. 💰 BUDGET DÉTAILLÉ
   - Transport
   - Hébergement
   - Activités
   - Repas
   - Total estimé

7. 📱 APPLICATIONS UTILES
   - Transport local
   - Traduction
   - Cartes offline"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Planifie mon voyage en détail."}
        ]

        result = await call_llm(messages, temperature=0.7)

        return AgentResponse(
            success=True,
            agent="travel",
            content=result["content"],
            metadata={
                "destination": request.destination,
                "departure": request.departure_city,
                "travelers": request.travelers
            },
            tokens_used=result.get("tokens"),
            duration_ms=result.get("duration_ms")
        )
    except Exception as e:
        logger.error(f"Travel agent error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/teaching", response_model=AgentResponse)
async def teaching_agent(request: TeachingRequest):
    """
    Teaching Agent - AI tutor for all subjects and levels
    """
    try:
        system_prompt = f"""Tu es un professeur expert et pédagogue exceptionnel.

COURS:
- Matière: {request.subject}
- Niveau: {request.level}
- Sujet: {request.topic}
- Style d'apprentissage préféré: {request.learning_style}

Langue: {request.language.upper()}

LEÇON STRUCTURÉE:

1. 🎯 OBJECTIFS D'APPRENTISSAGE
   - Ce que l'élève saura faire
   - Compétences développées
   - Prérequis

2. 📚 COURS THÉORIQUE
   - Explication claire et progressive
   - Concepts clés
   - Exemples concrets
   - Analogies pour mieux comprendre

3. 💡 POINTS IMPORTANTS
   - À retenir absolument
   - Erreurs fréquentes à éviter
   - Astuces mnémotechniques

4. ✏️ EXERCICES PRATIQUES
   - Exercice 1 (facile)
   - Exercice 2 (moyen)
   - Exercice 3 (difficile)
   - Solutions détaillées

5. 🔗 LIENS & RESSOURCES
   - Pour approfondir
   - Vidéos recommandées
   - Exercices supplémentaires

6. ✅ AUTO-ÉVALUATION
   - Quiz rapide (5 questions)
   - Réponses avec explications

Adapte ton style au profil {request.learning_style}:
- Visual: schémas, couleurs, mindmaps
- Auditory: explications verbales, rythme
- Kinesthetic: exemples pratiques, manipulation"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Enseigne-moi: {request.topic}"}
        ]

        result = await call_llm(messages, temperature=0.6, max_tokens=3000)

        return AgentResponse(
            success=True,
            agent="teaching",
            content=result["content"],
            metadata={
                "subject": request.subject,
                "level": request.level,
                "topic": request.topic,
                "learning_style": request.learning_style
            },
            tokens_used=result.get("tokens"),
            duration_ms=result.get("duration_ms")
        )
    except Exception as e:
        logger.error(f"Teaching agent error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# MULTI-AGENT ENDPOINT
# ============================================================================

class MultiAgentRequest(BaseModel):
    """Request for running multiple agents"""
    agents: List[str]  # List of agent names to run
    input_data: Dict[str, Any]
    parallel: bool = True

@router.post("/multi-agent", response_model=Dict[str, AgentResponse])
async def run_multi_agent(request: MultiAgentRequest):
    """
    Run multiple agents on the same input data
    Useful for comprehensive analysis
    """
    results = {}

    agent_map = {
        "financial-coach": (financial_coach, FinancialCoachRequest),
        "budget-planner": (budget_planner, BudgetPlannerRequest),
        "contract-analyst": (contract_analyst, ContractAnalysisRequest),
        "recruitment": (recruitment_agent, RecruitmentRequest),
        "real-estate": (real_estate_agent, RealEstateRequest),
        "travel": (travel_agent, TravelRequest),
        "teaching": (teaching_agent, TeachingRequest)
    }

    for agent_name in request.agents:
        if agent_name in agent_map:
            agent_func, request_class = agent_map[agent_name]
            try:
                agent_request = request_class(**request.input_data)
                results[agent_name] = await agent_func(agent_request)
            except Exception as e:
                logger.error(f"Error running {agent_name}: {e}")
                results[agent_name] = AgentResponse(
                    success=False,
                    agent=agent_name,
                    content=f"Error: {str(e)}",
                    metadata={"error": str(e)}
                )

    return results
