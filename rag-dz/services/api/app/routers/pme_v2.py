"""
PME Analyzer PRO V2 - Router FastAPI
=====================================
Endpoints complets pour l'analyse PME algérienne avec IA + RAG
"""

import io
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from ..models.pme_models import (
    # Enums
    LegalForm, FiscalRegime, ActivitySector, RiskLevel,
    # Inputs
    CompanyInput, FiscalSimulationInput,
    # Outputs
    PMEAnalysisResponse, QuickAnalysisResponse, PDFExportResponse,
    AuditReport, AuditHistoryItem, FiscalAnalysis, DeclarationCalendar,
    SocialChargesAnalysis, RiskAnalysis, ActionPlan
)
from ..services.pme_service import pme_analyzer_service

router = APIRouter(prefix="/api/pme/v2", tags=["PME Analyzer PRO V2"])


# ============================================
# In-Memory Storage (à remplacer par PostgreSQL)
# ============================================

audits_db: dict[str, AuditReport] = {}


# ============================================
# Helper Models
# ============================================

class SimpleAnalysisInput(BaseModel):
    """Input simplifié pour analyse rapide"""
    company_name: str
    wilaya: str
    sector: str
    legal_form: str
    annual_revenue: Optional[float] = None
    employees_count: int = 0
    has_rc: bool = False
    has_tva: bool = False
    has_cnas: bool = False
    has_casnos: bool = False


class FiscalSimulationRequest(BaseModel):
    """Requête de simulation fiscale"""
    annual_revenue: float
    annual_expenses: float = 0
    employees_count: int = 0
    average_salary: float = 50000
    legal_form: str = "SARL"
    sector: str = "Commerce"
    has_tva: bool = False


class ComplianceCheckRequest(BaseModel):
    """Requête de vérification conformité"""
    company_name: str
    has_rc: bool = False
    has_nif: bool = False
    has_nis: bool = False
    has_cnas: bool = False
    has_casnos: bool = False
    has_tva: bool = False
    employees_count: int = 0
    legal_form: str = "SARL"


# ============================================
# Main Endpoints
# ============================================

@router.post("/analyze", response_model=PMEAnalysisResponse)
async def analyze_company_full(input_data: CompanyInput):
    """
    🔍 Analyse PME complète avec IA + RAG
    
    Génère un rapport d'audit complet incluant:
    - Profil de l'entreprise
    - Analyse fiscale (IFU vs Réel, TVA, TAP, IBS)
    - Charges sociales (CNAS, CASNOS)
    - Analyse des risques
    - Calendrier des déclarations
    - Plan d'action personnalisé
    - Contexte RAG (réglementation algérienne)
    
    💰 Coût: 5 crédits
    """
    import time
    start = time.time()
    
    try:
        audit = pme_analyzer_service.run_full_analysis(input_data)
        
        # Sauvegarder en mémoire
        audits_db[audit.audit_id] = audit
        
        return PMEAnalysisResponse(
            success=True,
            audit=audit,
            processing_time=time.time() - start,
            credits_consumed=5,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/quick", response_model=QuickAnalysisResponse)
async def analyze_company_quick(input_data: SimpleAnalysisInput):
    """
    ⚡ Analyse PME rapide
    
    Version allégée pour un aperçu rapide:
    - Régime fiscal
    - TVA obligatoire ou non
    - Estimation des impôts
    - Top 3 des risques
    - Top 3 des actions
    
    💰 Coût: 1 crédit
    """
    try:
        # Convertir en CompanyInput
        company_input = CompanyInput(
            company_name=input_data.company_name,
            legal_form=LegalForm(input_data.legal_form),
            sector=ActivitySector(input_data.sector),
            wilaya=input_data.wilaya,
            annual_revenue=Decimal(str(input_data.annual_revenue)) if input_data.annual_revenue else None,
            employees_count=input_data.employees_count,
            has_rc=input_data.has_rc,
            has_tva=input_data.has_tva,
            has_cnas=input_data.has_cnas,
            has_casnos=input_data.has_casnos,
            include_rag_context=False,
        )
        
        result = pme_analyzer_service.run_quick_analysis(company_input)
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Valeur invalide: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# Fiscal Endpoints
# ============================================

@router.post("/fiscal/simulate")
async def simulate_fiscal(request: FiscalSimulationRequest):
    """
    📊 Simulation fiscale détaillée
    
    Simule les impôts et charges selon différents scénarios:
    - Comparaison IFU vs Régime Réel
    - Impact de la TVA
    - Charges sociales
    
    💰 Coût: 2 crédits
    """
    try:
        revenue = Decimal(str(request.annual_revenue))
        expenses = Decimal(str(request.annual_expenses))
        
        # Simulation IFU
        ifu_input = CompanyInput(
            company_name="Simulation",
            legal_form=LegalForm(request.legal_form),
            sector=ActivitySector(request.sector),
            wilaya="Alger",
            annual_revenue=revenue,
            employees_count=request.employees_count,
            has_tva=False,
        )
        
        # Simulation Réel
        reel_input = CompanyInput(
            company_name="Simulation",
            legal_form=LegalForm(request.legal_form),
            sector=ActivitySector(request.sector),
            wilaya="Alger",
            annual_revenue=revenue,
            employees_count=request.employees_count,
            has_tva=True,
        )
        
        ifu_fiscal = pme_analyzer_service.analyze_fiscal(ifu_input)
        reel_fiscal = pme_analyzer_service.analyze_fiscal(reel_input)
        ifu_social = pme_analyzer_service.analyze_social_charges(ifu_input)
        
        # Calcul bénéfice net estimé
        benefice_brut = revenue - expenses
        
        ifu_net = benefice_brut - ifu_fiscal.total_annual_taxes - ifu_social.total_social_charges
        reel_net = benefice_brut - reel_fiscal.total_annual_taxes - ifu_social.total_social_charges
        
        # Recommandation
        if revenue <= Decimal("15000000"):
            if expenses / revenue < Decimal("0.3"):
                recommendation = "IFU recommandé (charges faibles)"
            else:
                recommendation = "Régime réel à considérer (charges élevées = TVA déductible)"
        else:
            recommendation = "Régime réel obligatoire (CA > 15M DA)"
        
        return {
            "success": True,
            "simulation": {
                "revenue": float(revenue),
                "expenses": float(expenses),
                "benefice_brut": float(benefice_brut),
            },
            "ifu_scenario": {
                "regime": "IFU",
                "eligible": revenue <= Decimal("15000000"),
                "taxes": float(ifu_fiscal.total_annual_taxes),
                "social_charges": float(ifu_social.total_social_charges),
                "total_charges": float(ifu_fiscal.total_annual_taxes + ifu_social.total_social_charges),
                "benefice_net": float(ifu_net),
                "taux_prelevement": float((ifu_fiscal.total_annual_taxes + ifu_social.total_social_charges) / revenue * 100) if revenue > 0 else 0,
            },
            "reel_scenario": {
                "regime": "Réel",
                "taxes": float(reel_fiscal.total_annual_taxes),
                "tva_deductible": float(reel_fiscal.tva_deductible or 0),
                "social_charges": float(ifu_social.total_social_charges),
                "total_charges": float(reel_fiscal.total_annual_taxes + ifu_social.total_social_charges),
                "benefice_net": float(reel_net),
            },
            "comparison": {
                "difference_annuelle": float(abs(ifu_net - reel_net)),
                "meilleur_regime": "IFU" if ifu_net > reel_net else "Réel",
                "economie_potentielle": float(max(ifu_net, reel_net) - min(ifu_net, reel_net)),
            },
            "recommendation": recommendation,
            "credits_consumed": 2,
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/fiscal/regimes")
async def get_fiscal_regimes():
    """
    📋 Liste des régimes fiscaux algériens
    """
    return {
        "regimes": [
            {
                "code": "IFU",
                "name": "Impôt Forfaitaire Unique",
                "description": "Régime simplifié pour CA < 15M DA",
                "threshold": 15000000,
                "advantages": [
                    "Pas de TVA à collecter/déclarer",
                    "Comptabilité simplifiée",
                    "Déclaration annuelle unique",
                ],
                "disadvantages": [
                    "Pas de récupération de TVA sur achats",
                    "Limité aux petites entreprises",
                ],
            },
            {
                "code": "REEL",
                "name": "Régime Réel",
                "description": "Régime normal pour CA > 15M DA ou option",
                "threshold": 15000001,
                "advantages": [
                    "Récupération TVA sur achats",
                    "Déduction de toutes les charges",
                    "Crédibilité accrue",
                ],
                "disadvantages": [
                    "Comptabilité commerciale obligatoire",
                    "Déclarations mensuelles G50",
                    "Coût comptable plus élevé",
                ],
            },
        ],
        "thresholds": {
            "ifu_limit": 15000000,
            "tva_rate": 19,
            "tva_reduced_rate": 9,
        }
    }


@router.get("/fiscal/taxes")
async def get_tax_rates():
    """
    💰 Taux d'imposition en vigueur (2025)
    """
    return {
        "year": 2025,
        "corporate": {
            "IBS": {"rate": 19, "description": "Impôt sur les Bénéfices des Sociétés"},
            "IBS_reinvested": {"rate": 9, "description": "IBS sur bénéfices réinvestis"},
            "TAP_production": {"rate": 1, "description": "TAP activités de production"},
            "TAP_services": {"rate": 2, "description": "TAP services et commerce"},
        },
        "tva": {
            "normal": {"rate": 19, "description": "Taux normal"},
            "reduced": {"rate": 9, "description": "Taux réduit (produits de première nécessité)"},
        },
        "ifu": {
            "tranches": [
                {"from": 0, "to": 1000000, "rate": 0, "description": "Exonéré"},
                {"from": 1000001, "to": 5000000, "rate": 5, "description": "5% (ou 8% services)"},
                {"from": 5000001, "to": 10000000, "rate": 8, "description": "8% (ou 10% services)"},
                {"from": 10000001, "to": 15000000, "rate": 12, "description": "12%"},
            ]
        },
        "social": {
            "CNAS_employer": {"rate": 26, "description": "Part patronale CNAS"},
            "CNAS_employee": {"rate": 9, "description": "Part salariale CNAS"},
            "CASNOS": {"rate": 15, "description": "Cotisation non-salariés"},
            "formation": {"rate": 1, "description": "Taxe formation professionnelle"},
            "oeuvres_sociales": {"rate": 0.5, "description": "Contribution œuvres sociales"},
        }
    }


# ============================================
# Declaration Endpoints
# ============================================

@router.get("/declarations/calendar")
async def get_declaration_calendar(
    regime: str = Query("IFU", description="Régime fiscal (IFU ou REEL)"),
    has_employees: bool = Query(False, description="A des salariés"),
    has_casnos: bool = Query(False, description="Affilié CASNOS"),
):
    """
    📅 Calendrier des déclarations fiscales et sociales
    """
    calendar = {
        "year": datetime.now().year,
        "regime": regime,
        "monthly": [],
        "quarterly": [],
        "annual": [],
    }
    
    if regime.upper() == "REEL":
        calendar["monthly"].append({
            "name": "G50",
            "description": "Déclaration TVA + TAP + IRG/Salaires",
            "due_day": 20,
            "organism": "DGI",
            "online": "https://jibayatic.dz",
            "penalty": "10% + 3% par mois de retard",
        })
    
    if has_employees:
        calendar["monthly"].append({
            "name": "Déclaration CNAS",
            "description": "Cotisations sociales salariés",
            "due_day": 30,
            "organism": "CNAS",
            "online": "https://teledeclaration.cnas.dz",
        })
    
    if regime.upper() == "IFU":
        calendar["quarterly"].append({
            "name": "Acompte IFU",
            "description": "Acompte provisionnel trimestriel",
            "due_months": [3, 6, 9],
            "due_day": 20,
            "organism": "DGI",
        })
    
    if has_casnos:
        calendar["quarterly"].append({
            "name": "CASNOS",
            "description": "Cotisation non-salariés",
            "due_months": [3, 6, 9, 12],
            "due_day": 15,
            "organism": "CASNOS",
        })
    
    calendar["annual"].extend([
        {
            "name": "Bilan Fiscal",
            "description": "Liasse fiscale annuelle",
            "due_date": "30 avril N+1",
            "organism": "DGI",
            "documents": ["Bilan", "TCR", "Annexes", "Tableau amortissements"],
        },
        {
            "name": "DAS",
            "description": "Déclaration Annuelle des Salaires",
            "due_date": "31 janvier N+1",
            "organism": "DGI + CNAS",
            "documents": ["État 301 bis", "Récapitulatif IRG"],
        },
    ])
    
    return calendar


@router.get("/declarations/next")
async def get_next_deadlines(
    regime: str = Query("IFU"),
    has_employees: bool = Query(False),
    limit: int = Query(5, ge=1, le=20),
):
    """
    ⏰ Prochaines échéances fiscales
    """
    from datetime import date, timedelta
    
    today = date.today()
    deadlines = []
    
    # G50 si régime réel
    if regime.upper() == "REEL":
        next_g50 = date(today.year, today.month, 20)
        if next_g50 <= today:
            if today.month == 12:
                next_g50 = date(today.year + 1, 1, 20)
            else:
                next_g50 = date(today.year, today.month + 1, 20)
        
        deadlines.append({
            "name": "G50",
            "due_date": next_g50.isoformat(),
            "days_remaining": (next_g50 - today).days,
            "organism": "DGI",
            "priority": "high" if (next_g50 - today).days <= 5 else "normal",
        })
    
    # CNAS si salariés
    if has_employees:
        next_cnas = date(today.year, today.month, 30)
        if next_cnas <= today:
            if today.month == 12:
                next_cnas = date(today.year + 1, 1, 30)
            else:
                next_cnas = date(today.year, today.month + 1, 30)
        
        deadlines.append({
            "name": "CNAS",
            "due_date": next_cnas.isoformat(),
            "days_remaining": (next_cnas - today).days,
            "organism": "CNAS",
            "priority": "high" if (next_cnas - today).days <= 5 else "normal",
        })
    
    # Trier par date
    deadlines.sort(key=lambda x: x["days_remaining"])
    
    return {
        "today": today.isoformat(),
        "deadlines": deadlines[:limit],
        "alerts": [d for d in deadlines if d["days_remaining"] <= 5],
    }


# ============================================
# Compliance & Risk Endpoints
# ============================================

@router.post("/compliance/check")
async def check_compliance(request: ComplianceCheckRequest):
    """
    ✅ Vérification de conformité rapide
    
    Vérifie si l'entreprise est en règle:
    - Registre de Commerce
    - Identifiants fiscaux (NIF, NIS)
    - Affiliations sociales (CNAS, CASNOS)
    - TVA si applicable
    """
    issues = []
    score = 100
    
    # Vérifications
    if not request.has_rc:
        issues.append({
            "code": "RC_MISSING",
            "severity": "critical",
            "message": "Registre de Commerce manquant",
            "action": "Déposer dossier au CNRC",
            "penalty": "Exercice illégal",
        })
        score -= 30
    
    if not request.has_nif:
        issues.append({
            "code": "NIF_MISSING",
            "severity": "high",
            "message": "NIF non renseigné",
            "action": "Obtenir NIF aux impôts",
        })
        score -= 20
    
    if request.employees_count > 0 and not request.has_cnas:
        issues.append({
            "code": "CNAS_MISSING",
            "severity": "critical",
            "message": "Salariés non déclarés CNAS",
            "action": "Affilier les salariés immédiatement",
            "penalty": "Poursuites possibles",
        })
        score -= 25
    
    if request.legal_form in ["AUTO_ENTREPRENEUR", "PROFESSION_LIBERALE"] and not request.has_casnos:
        issues.append({
            "code": "CASNOS_MISSING",
            "severity": "high",
            "message": "Non affilié CASNOS",
            "action": "S'affilier à la CASNOS",
        })
        score -= 15
    
    score = max(0, score)
    
    return {
        "success": True,
        "company_name": request.company_name,
        "compliance_score": score,
        "status": "conforme" if score >= 80 else "non_conforme" if score < 50 else "à_améliorer",
        "issues_count": len(issues),
        "issues": issues,
        "recommendations": [i["action"] for i in issues[:3]],
    }


# ============================================
# Audit History Endpoints
# ============================================

@router.get("/audits", response_model=list[AuditHistoryItem])
async def list_audits(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """
    📋 Liste des audits réalisés
    """
    audits = list(audits_db.values())
    audits.sort(key=lambda x: x.generated_at, reverse=True)
    
    items = []
    for audit in audits[offset:offset + limit]:
        items.append(AuditHistoryItem(
            audit_id=audit.audit_id,
            company_name=audit.company_profile.company_name,
            generated_at=audit.generated_at,
            overall_score=audit.overall_score,
            compliance_score=audit.compliance_score,
            risk_level=audit.risk_analysis.overall_risk_level,
            pdf_url=audit.pdf_url,
        ))
    
    return items


@router.get("/audits/{audit_id}")
async def get_audit(audit_id: str):
    """
    📄 Récupérer un audit par ID
    """
    if audit_id not in audits_db:
        raise HTTPException(status_code=404, detail="Audit non trouvé")
    
    return {
        "success": True,
        "audit": audits_db[audit_id],
    }


@router.delete("/audits/{audit_id}")
async def delete_audit(audit_id: str):
    """
    🗑️ Supprimer un audit
    """
    if audit_id not in audits_db:
        raise HTTPException(status_code=404, detail="Audit non trouvé")
    
    del audits_db[audit_id]
    
    return {"success": True, "message": "Audit supprimé"}


# ============================================
# Export Endpoints
# ============================================

@router.post("/audits/{audit_id}/export/pdf")
async def export_audit_pdf(audit_id: str, background_tasks: BackgroundTasks):
    """
    📥 Exporter l'audit en PDF
    
    Génère un PDF professionnel contenant:
    - Résumé exécutif
    - Analyse fiscale détaillée
    - Tableau des risques
    - Plan d'action
    - Calendrier des échéances
    
    💰 Coût: 1 crédit
    """
    if audit_id not in audits_db:
        raise HTTPException(status_code=404, detail="Audit non trouvé")
    
    audit = audits_db[audit_id]
    
    # Pour l'instant, on retourne un placeholder
    # TODO: Intégrer reportlab ou weasyprint pour la génération PDF
    
    return PDFExportResponse(
        success=True,
        audit_id=audit_id,
        pdf_url=f"/api/pme/v2/audits/{audit_id}/download/pdf",
        filename=f"audit_{audit.company_profile.company_name}_{audit.generated_at.strftime('%Y%m%d')}.pdf",
        size_bytes=0,
        generated_at=datetime.now(),
    )


@router.get("/audits/{audit_id}/download/pdf")
async def download_audit_pdf(audit_id: str):
    """
    📥 Télécharger le PDF de l'audit
    """
    if audit_id not in audits_db:
        raise HTTPException(status_code=404, detail="Audit non trouvé")
    
    audit = audits_db[audit_id]
    
    # Générer un PDF simple (placeholder)
    # TODO: Implémenter avec reportlab
    pdf_content = f"""
    RAPPORT D'AUDIT PME
    ====================
    
    Entreprise: {audit.company_profile.company_name}
    Wilaya: {audit.company_profile.wilaya}
    Forme juridique: {audit.company_profile.legal_form_full_name}
    
    Score de conformité: {audit.compliance_score}/100
    Score global: {audit.overall_score}/100
    
    {audit.ai_summary}
    
    Généré le: {audit.generated_at.strftime('%d/%m/%Y à %H:%M')}
    Par: iaFactoryDZ - PME Analyzer Pro V2
    """.encode('utf-8')
    
    return StreamingResponse(
        io.BytesIO(pdf_content),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=audit_{audit_id}.pdf"
        }
    )


# ============================================
# Reference Data Endpoints
# ============================================

@router.get("/reference/wilayas")
async def get_wilayas():
    """
    🗺️ Liste des 58 wilayas d'Algérie
    """
    from ..services.pme_service import WILAYA_CODES
    
    return {
        "count": len(WILAYA_CODES),
        "wilayas": [
            {"code": code, "name": name}
            for name, code in sorted(WILAYA_CODES.items(), key=lambda x: x[1])
        ]
    }


@router.get("/reference/sectors")
async def get_sectors():
    """
    🏭 Secteurs d'activité
    """
    return {
        "sectors": [
            {"code": s.name, "name": s.value, "tap_rate": 2 if s.name not in ["INDUSTRIE", "ARTISANAT"] else 1}
            for s in ActivitySector
        ]
    }


@router.get("/reference/legal-forms")
async def get_legal_forms():
    """
    📋 Formes juridiques
    """
    from ..services.pme_service import LEGAL_FORM_NAMES, CAPITAL_MINIMUMS
    
    return {
        "legal_forms": [
            {
                "code": lf.name,
                "name": lf.value,
                "full_name": LEGAL_FORM_NAMES.get(lf, lf.value),
                "capital_minimum": CAPITAL_MINIMUMS.get(lf, "Non spécifié"),
            }
            for lf in LegalForm
        ]
    }


# ============================================
# Health Check
# ============================================

@router.get("/health")
async def health_check():
    """
    🏥 Vérifier l'état du service PME Analyzer
    """
    return {
        "status": "healthy",
        "service": "PME Analyzer PRO V2",
        "version": "2.0.0",
        "audits_in_memory": len(audits_db),
        "features": [
            "full_analysis",
            "quick_analysis",
            "fiscal_simulation",
            "compliance_check",
            "declaration_calendar",
            "pdf_export",
            "rag_integration",
        ],
        "credits_cost": {
            "full_analysis": 5,
            "quick_analysis": 1,
            "fiscal_simulation": 2,
            "pdf_export": 1,
        }
    }
