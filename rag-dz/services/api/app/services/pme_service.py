"""
PME Analyzer PRO V2 - Service IA
=================================
Logique métier avec IA + RAG pour analyse PME algérienne
"""

import uuid
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Optional

from ..models.pme_models import (
    # Enums
    LegalForm, FiscalRegime, ActivitySector, RiskLevel, DeclarationType,
    # Inputs
    CompanyInput, FiscalSimulationInput,
    # Outputs
    CompanyProfile, FiscalAnalysis, SocialChargesAnalysis,
    Declaration, DeclarationCalendar, Risk, RiskAnalysis,
    ChecklistItem, ActionPlan, RAGSource, RAGContext,
    TaxDetail, AuditReport, QuickAnalysisResponse
)


# ============================================
# Constants - Données Algériennes
# ============================================

WILAYA_CODES = {
    "Adrar": "01", "Chlef": "02", "Laghouat": "03", "Oum El Bouaghi": "04",
    "Batna": "05", "Béjaïa": "06", "Biskra": "07", "Béchar": "08",
    "Blida": "09", "Bouira": "10", "Tamanrasset": "11", "Tébessa": "12",
    "Tlemcen": "13", "Tiaret": "14", "Tizi Ouzou": "15", "Alger": "16",
    "Djelfa": "17", "Jijel": "18", "Sétif": "19", "Saïda": "20",
    "Skikda": "21", "Sidi Bel Abbès": "22", "Annaba": "23", "Guelma": "24",
    "Constantine": "25", "Médéa": "26", "Mostaganem": "27", "M'Sila": "28",
    "Mascara": "29", "Ouargla": "30", "Oran": "31", "El Bayadh": "32",
    "Illizi": "33", "Bordj Bou Arréridj": "34", "Boumerdès": "35",
    "El Tarf": "36", "Tindouf": "37", "Tissemsilt": "38", "El Oued": "39",
    "Khenchela": "40", "Souk Ahras": "41", "Tipaza": "42", "Mila": "43",
    "Aïn Defla": "44", "Naâma": "45", "Aïn Témouchent": "46", "Ghardaïa": "47",
    "Relizane": "48", "El M'Ghair": "49", "El Meniaa": "50", "Ouled Djellal": "51",
    "Bordj Badji Mokhtar": "52", "Béni Abbès": "53", "Timimoun": "54",
    "Touggourt": "55", "Djanet": "56", "In Salah": "57", "In Guezzam": "58"
}

LEGAL_FORM_NAMES = {
    LegalForm.EURL: "Entreprise Unipersonnelle à Responsabilité Limitée",
    LegalForm.SARL: "Société à Responsabilité Limitée",
    LegalForm.SPA: "Société Par Actions",
    LegalForm.SNC: "Société en Nom Collectif",
    LegalForm.SCS: "Société en Commandite Simple",
    LegalForm.AUTO_ENTREPRENEUR: "Auto-Entrepreneur",
    LegalForm.MICRO_ENTREPRISE: "Micro-Entreprise",
    LegalForm.PROFESSION_LIBERALE: "Profession Libérale",
    LegalForm.ARTISAN: "Artisan",
}

CAPITAL_MINIMUMS = {
    LegalForm.EURL: "100 000 DA",
    LegalForm.SARL: "100 000 DA",
    LegalForm.SPA: "1 000 000 DA (ou 5 000 000 DA si appel public à l'épargne)",
    LegalForm.SNC: "Pas de minimum légal",
    LegalForm.SCS: "Pas de minimum légal",
    LegalForm.AUTO_ENTREPRENEUR: "Non applicable",
    LegalForm.MICRO_ENTREPRISE: "Non applicable",
    LegalForm.PROFESSION_LIBERALE: "Non applicable",
    LegalForm.ARTISAN: "Non applicable",
}


# ============================================
# Tax Rates - Taux d'imposition 2025
# ============================================

TAX_RATES = {
    # IFU (selon tranches de CA)
    "IFU_PRODUCTION": {
        "0-1M": 0.00,      # Exonéré
        "1M-5M": 0.05,     # 5%
        "5M-10M": 0.08,    # 8%
        "10M-15M": 0.12,   # 12%
    },
    "IFU_SERVICES": {
        "0-1M": 0.00,
        "1M-5M": 0.08,
        "5M-10M": 0.10,
        "10M-15M": 0.12,
    },
    "IFU_COMMERCE": {
        "0-1M": 0.00,
        "1M-5M": 0.05,
        "5M-10M": 0.08,
        "10M-15M": 0.12,
    },
    
    # Régime réel
    "IBS": 0.19,           # Impôt sur les bénéfices des sociétés (19% ou 23%)
    "IBS_REINVESTED": 0.09, # IBS sur bénéfices réinvestis
    "IRG_SALARIES": {       # IRG sur salaires (barème progressif)
        "0-120000": 0.00,
        "120001-360000": 0.20,
        "360001-1440000": 0.30,
        "1440001+": 0.35,
    },
    
    # TVA
    "TVA_NORMAL": 0.19,
    "TVA_REDUIT": 0.09,
    
    # TAP - Taxe sur l'activité professionnelle
    "TAP_PRODUCTION": 0.01,
    "TAP_SERVICES": 0.02,
    "TAP_COMMERCE": 0.02,
    "TAP_BTP": 0.02,
    
    # Charges sociales
    "CNAS_EMPLOYER": 0.26,
    "CNAS_EMPLOYEE": 0.09,
    "CASNOS": 0.15,
    "FORMATION": 0.01,
    "OEUVRES_SOCIALES": 0.005,
    "ACCIDENT_TRAVAIL": 0.0125,
}


# ============================================
# PME Analyzer Service
# ============================================

class PMEAnalyzerService:
    """Service d'analyse PME avec IA + RAG"""
    
    def __init__(self):
        self.rag_enabled = True
    
    # ========================================
    # Company Profile
    # ========================================
    
    def build_company_profile(self, input_data: CompanyInput) -> CompanyProfile:
        """Construire le profil de l'entreprise"""
        
        # Déterminer la catégorie de taille
        if input_data.employees_count == 0:
            size_category = "Micro-entreprise"
        elif input_data.employees_count < 10:
            size_category = "TPE (Très Petite Entreprise)"
        elif input_data.employees_count < 50:
            size_category = "Petite Entreprise"
        elif input_data.employees_count < 250:
            size_category = "Moyenne Entreprise"
        else:
            size_category = "Grande Entreprise"
        
        # Calculer l'âge
        age_years = None
        if input_data.creation_date:
            age_years = (date.today() - input_data.creation_date).days // 365
        
        # Registrations requises
        required_registrations = [
            "Registre de Commerce (CNRC)",
            "Numéro d'Identification Fiscale (NIF)",
            "Numéro d'Identification Statistique (NIS)",
        ]
        
        if input_data.employees_count > 0:
            required_registrations.append("CNAS (Caisse Nationale d'Assurance Sociale)")
        
        if input_data.legal_form in [LegalForm.AUTO_ENTREPRENEUR, LegalForm.PROFESSION_LIBERALE, LegalForm.ARTISAN]:
            required_registrations.append("CASNOS (Caisse des Non-Salariés)")
        
        return CompanyProfile(
            company_name=input_data.company_name,
            legal_form=input_data.legal_form,
            legal_form_full_name=LEGAL_FORM_NAMES.get(input_data.legal_form, str(input_data.legal_form)),
            sector=input_data.sector,
            wilaya=input_data.wilaya,
            wilaya_code=WILAYA_CODES.get(input_data.wilaya, "00"),
            creation_date=input_data.creation_date,
            age_years=age_years,
            employees_count=input_data.employees_count,
            size_category=size_category,
            has_rc=input_data.has_rc,
            rc_number=input_data.rc_number,
            nif=input_data.nif,
            nis=input_data.nis,
            capital_minimum=CAPITAL_MINIMUMS.get(input_data.legal_form),
            required_registrations=required_registrations,
        )
    
    # ========================================
    # Fiscal Analysis
    # ========================================
    
    def analyze_fiscal(self, input_data: CompanyInput) -> FiscalAnalysis:
        """Analyse fiscale complète"""
        
        revenue = input_data.annual_revenue or Decimal("0")
        threshold = Decimal("15000000")  # 15M DA
        
        # Déterminer le régime fiscal
        if input_data.legal_form in [LegalForm.AUTO_ENTREPRENEUR, LegalForm.MICRO_ENTREPRISE]:
            regime = FiscalRegime.MICRO_ENTREPRISE
        elif revenue <= threshold and input_data.legal_form not in [LegalForm.SPA]:
            regime = FiscalRegime.IFU
        else:
            regime = FiscalRegime.REEL
        
        # TVA obligatoire ?
        is_tva_required = revenue > threshold or input_data.has_tva
        
        # Calculer les impôts
        taxes = []
        total_taxes = Decimal("0")
        
        if regime == FiscalRegime.IFU:
            # Calcul IFU par tranches
            ifu_amount = self._calculate_ifu(revenue, input_data.sector)
            taxes.append(TaxDetail(
                name="Impôt Forfaitaire Unique",
                code="IFU",
                rate=float(ifu_amount / revenue * 100) if revenue > 0 else 0,
                base=revenue,
                amount=ifu_amount,
                frequency="annuel",
                due_date="20 janvier N+1",
                notes="Déclaration annuelle G12 au plus tard le 20 janvier"
            ))
            total_taxes += ifu_amount
            
        else:  # Régime réel
            # IBS ou IRG
            if input_data.legal_form in [LegalForm.SARL, LegalForm.EURL, LegalForm.SPA, LegalForm.SNC]:
                benefice = revenue * Decimal("0.15")  # Estimation 15% de marge
                ibs = benefice * Decimal(str(TAX_RATES["IBS"]))
                taxes.append(TaxDetail(
                    name="Impôt sur les Bénéfices des Sociétés",
                    code="IBS",
                    rate=TAX_RATES["IBS"] * 100,
                    base=benefice,
                    amount=ibs,
                    frequency="annuel",
                    due_date="20 avril N+1",
                ))
                total_taxes += ibs
            
            # TAP
            tap_rate = self._get_tap_rate(input_data.sector)
            tap = revenue * Decimal(str(tap_rate))
            taxes.append(TaxDetail(
                name="Taxe sur l'Activité Professionnelle",
                code="TAP",
                rate=tap_rate * 100,
                base=revenue,
                amount=tap,
                frequency="mensuel",
                due_date="20 du mois suivant",
            ))
            total_taxes += tap
        
        # TVA si applicable
        tva_collected = None
        tva_due = None
        if is_tva_required:
            tva_collected = revenue * Decimal(str(TAX_RATES["TVA_NORMAL"]))
            tva_deductible = revenue * Decimal("0.5") * Decimal(str(TAX_RATES["TVA_NORMAL"]))  # Estimation
            tva_due = tva_collected - tva_deductible
            taxes.append(TaxDetail(
                name="Taxe sur la Valeur Ajoutée",
                code="TVA",
                rate=TAX_RATES["TVA_NORMAL"] * 100,
                base=revenue,
                amount=tva_due,
                frequency="mensuel",
                due_date="20 du mois suivant (G50)",
            ))
        
        # Conseils d'optimisation
        optimization_tips = self._get_optimization_tips(regime, input_data)
        
        # Explication du régime
        regime_explanation = self._get_regime_explanation(regime, revenue)
        
        return FiscalAnalysis(
            regime=regime,
            regime_explanation=regime_explanation,
            is_tva_required=is_tva_required,
            tva_threshold=threshold,
            taxes=taxes,
            total_annual_taxes=total_taxes,
            effective_tax_rate=float(total_taxes / revenue * 100) if revenue > 0 else 0,
            tva_rate=TAX_RATES["TVA_NORMAL"] * 100,
            tva_collected=tva_collected,
            tva_deductible=tva_collected * Decimal("0.5") if tva_collected else None,
            tva_due=tva_due,
            optimization_tips=optimization_tips,
        )
    
    def _calculate_ifu(self, revenue: Decimal, sector: ActivitySector) -> Decimal:
        """Calculer l'IFU selon les tranches"""
        if sector in [ActivitySector.INDUSTRIE, ActivitySector.BTP, ActivitySector.ARTISANAT]:
            rates = TAX_RATES["IFU_PRODUCTION"]
        elif sector in [ActivitySector.SERVICES, ActivitySector.TECHNOLOGIE, ActivitySector.SANTE]:
            rates = TAX_RATES["IFU_SERVICES"]
        else:
            rates = TAX_RATES["IFU_COMMERCE"]
        
        ifu = Decimal("0")
        rev = float(revenue)
        
        if rev <= 1_000_000:
            ifu = Decimal("0")
        elif rev <= 5_000_000:
            ifu = revenue * Decimal(str(rates.get("1M-5M", 0.05)))
        elif rev <= 10_000_000:
            ifu = revenue * Decimal(str(rates.get("5M-10M", 0.08)))
        else:
            ifu = revenue * Decimal(str(rates.get("10M-15M", 0.12)))
        
        return ifu
    
    def _get_tap_rate(self, sector: ActivitySector) -> float:
        """Obtenir le taux TAP selon le secteur"""
        if sector in [ActivitySector.INDUSTRIE, ActivitySector.ARTISANAT]:
            return TAX_RATES["TAP_PRODUCTION"]
        elif sector == ActivitySector.BTP:
            return TAX_RATES["TAP_BTP"]
        else:
            return TAX_RATES["TAP_SERVICES"]
    
    def _get_regime_explanation(self, regime: FiscalRegime, revenue: Decimal) -> str:
        """Explication du régime fiscal"""
        if regime == FiscalRegime.IFU:
            return (
                f"Avec un chiffre d'affaires de {revenue:,.0f} DA (< 15 000 000 DA), "
                f"vous êtes éligible au régime IFU (Impôt Forfaitaire Unique). "
                f"Ce régime simplifié vous dispense de la TVA et de la comptabilité commerciale."
            )
        elif regime == FiscalRegime.REEL:
            return (
                f"Avec un chiffre d'affaires de {revenue:,.0f} DA (> 15 000 000 DA ou forme juridique SPA), "
                f"vous êtes soumis au régime réel. Vous devez tenir une comptabilité commerciale complète, "
                f"déclarer et reverser la TVA, et effectuer des déclarations mensuelles G50."
            )
        else:
            return "Régime micro-entreprise applicable."
    
    def _get_optimization_tips(self, regime: FiscalRegime, input_data: CompanyInput) -> list[str]:
        """Conseils d'optimisation fiscale"""
        tips = []
        
        if regime == FiscalRegime.IFU:
            tips.append("💡 Restez sous le seuil de 15M DA pour conserver le régime IFU")
            tips.append("📊 Envisagez le passage au réel si vos charges sont importantes (TVA déductible)")
        
        if input_data.employees_count > 0:
            tips.append("👥 Les salaires et charges sociales sont déductibles du bénéfice imposable")
            tips.append("📈 Optimisez avec des contrats ANEM (exonérations CNAS)")
        
        if input_data.sector == ActivitySector.TECHNOLOGIE:
            tips.append("💻 Explorez les exonérations pour les startups et activités innovantes")
        
        if not input_data.has_rc:
            tips.append("⚠️ Priorité : obtenez votre Registre de Commerce pour exercer légalement")
        
        tips.append("📅 Planifiez vos investissements en fin d'année pour maximiser les déductions")
        tips.append("🏦 Le réinvestissement des bénéfices bénéficie d'un taux IBS réduit (9%)")
        
        return tips
    
    # ========================================
    # Social Charges
    # ========================================
    
    def analyze_social_charges(self, input_data: CompanyInput) -> SocialChargesAnalysis:
        """Analyse des charges sociales"""
        
        employees = input_data.employees_count
        avg_salary = Decimal("50000")  # Salaire moyen estimé
        
        # CNAS
        monthly_cnas_employer = avg_salary * Decimal(str(TAX_RATES["CNAS_EMPLOYER"])) * employees
        monthly_cnas_employee = avg_salary * Decimal(str(TAX_RATES["CNAS_EMPLOYEE"])) * employees
        annual_cnas = (monthly_cnas_employer + monthly_cnas_employee) * 12
        
        # CASNOS (pour non-salariés)
        revenue = input_data.annual_revenue or Decimal("0")
        annual_casnos = Decimal("0")
        if input_data.legal_form in [LegalForm.AUTO_ENTREPRENEUR, LegalForm.PROFESSION_LIBERALE, LegalForm.ARTISAN, LegalForm.EURL]:
            base_casnos = min(revenue * Decimal("0.80"), Decimal("12000000"))  # Plafond
            annual_casnos = base_casnos * Decimal(str(TAX_RATES["CASNOS"]))
        
        # Autres charges
        formation = avg_salary * Decimal(str(TAX_RATES["FORMATION"])) * employees * 12
        oeuvres = avg_salary * Decimal(str(TAX_RATES["OEUVRES_SOCIALES"])) * employees * 12
        accident = avg_salary * Decimal(str(TAX_RATES["ACCIDENT_TRAVAIL"])) * employees * 12
        
        total = annual_cnas + annual_casnos + formation + oeuvres + accident
        
        return SocialChargesAnalysis(
            cnas_employer_rate=TAX_RATES["CNAS_EMPLOYER"] * 100,
            cnas_employee_rate=TAX_RATES["CNAS_EMPLOYEE"] * 100,
            monthly_cnas_employer=monthly_cnas_employer,
            monthly_cnas_employee=monthly_cnas_employee,
            annual_cnas_total=annual_cnas,
            casnos_rate=TAX_RATES["CASNOS"] * 100,
            annual_casnos=annual_casnos,
            oeuvres_sociales_rate=TAX_RATES["OEUVRES_SOCIALES"] * 100,
            formation_rate=TAX_RATES["FORMATION"] * 100,
            accident_travail_rate=TAX_RATES["ACCIDENT_TRAVAIL"] * 100,
            total_social_charges=total,
            breakdown={
                "CNAS Patronale": monthly_cnas_employer * 12,
                "CNAS Salariale": monthly_cnas_employee * 12,
                "CASNOS": annual_casnos,
                "Formation": formation,
                "Œuvres Sociales": oeuvres,
                "Accident du Travail": accident,
            }
        )
    
    # ========================================
    # Declaration Calendar
    # ========================================
    
    def build_declaration_calendar(self, input_data: CompanyInput, regime: FiscalRegime) -> DeclarationCalendar:
        """Construire le calendrier des déclarations"""
        
        monthly = []
        quarterly = []
        annual = []
        
        # Déclarations mensuelles
        if regime == FiscalRegime.REEL:
            monthly.append(Declaration(
                type=DeclarationType.G50,
                name="Déclaration G50",
                description="Déclaration mensuelle TVA, TAP, IRG/salaires",
                frequency="mensuel",
                due_day=20,
                organism="Direction des Impôts",
                penalty_rate=10.0,
                required_documents=["G50 rempli", "Relevé des ventes", "État des salaires"],
                online_platform="https://jibayatic.dz",
            ))
        
        if input_data.employees_count > 0:
            monthly.append(Declaration(
                type=DeclarationType.CNAS,
                name="Déclaration CNAS",
                description="Cotisations sociales mensuelles",
                frequency="mensuel",
                due_day=30,
                organism="CNAS",
                penalty_rate=5.0,
                required_documents=["Déclaration des salaires", "Bordereaux de cotisation"],
                online_platform="https://teledeclaration.cnas.dz",
            ))
        
        # Déclarations trimestrielles
        if regime == FiscalRegime.IFU:
            quarterly.append(Declaration(
                type=DeclarationType.IFU,
                name="Acompte IFU",
                description="Acompte trimestriel IFU",
                frequency="trimestriel",
                due_day=20,
                organism="Direction des Impôts",
                required_documents=["Relevé CA trimestriel"],
            ))
        
        if input_data.has_casnos or input_data.legal_form in [LegalForm.AUTO_ENTREPRENEUR, LegalForm.PROFESSION_LIBERALE]:
            quarterly.append(Declaration(
                type=DeclarationType.CASNOS,
                name="Cotisation CASNOS",
                description="Cotisation trimestrielle non-salariés",
                frequency="trimestriel",
                due_day=15,
                organism="CASNOS",
                required_documents=["Déclaration de revenus", "Bordereau de paiement"],
            ))
        
        # Déclarations annuelles
        annual.append(Declaration(
            type=DeclarationType.G50A,
            name="Bilan Fiscal Annuel",
            description="Liasse fiscale et bilan comptable",
            frequency="annuel",
            due_day=30,  # 30 avril
            organism="Direction des Impôts",
            penalty_rate=25.0,
            required_documents=["Bilan", "TCR", "Tableau des amortissements", "Annexes"],
        ))
        
        if input_data.employees_count > 0:
            annual.append(Declaration(
                type=DeclarationType.DAS,
                name="DAS (Déclaration Annuelle des Salaires)",
                description="État récapitulatif annuel des salaires",
                frequency="annuel",
                due_day=31,  # 31 janvier
                organism="Direction des Impôts + CNAS",
                required_documents=["État 301 bis", "Récapitulatif annuel"],
            ))
        
        # Prochaines échéances
        today = date.today()
        next_deadlines = []
        
        for decl in monthly:
            next_date = date(today.year, today.month, decl.due_day)
            if next_date <= today:
                next_date = date(today.year, today.month + 1 if today.month < 12 else 1, decl.due_day)
            next_deadlines.append({
                "declaration": decl.name,
                "due_date": next_date.isoformat(),
                "days_remaining": (next_date - today).days,
                "organism": decl.organism,
            })
        
        next_deadlines.sort(key=lambda x: x["days_remaining"])
        
        return DeclarationCalendar(
            company_name=input_data.company_name,
            fiscal_year=today.year,
            regime=regime,
            monthly_declarations=monthly,
            quarterly_declarations=quarterly,
            annual_declarations=annual,
            next_deadlines=next_deadlines[:5],
            reminders=[
                "📅 Programmez des rappels 5 jours avant chaque échéance",
                "💳 Privilégiez le paiement en ligne pour éviter les files d'attente",
                "📁 Conservez tous vos justificatifs pendant 10 ans",
            ]
        )
    
    # ========================================
    # Risk Analysis
    # ========================================
    
    def analyze_risks(self, input_data: CompanyInput) -> RiskAnalysis:
        """Analyse des risques de conformité"""
        
        risks = []
        
        # Risque RC
        if not input_data.has_rc:
            risks.append(Risk(
                code="RC_MISSING",
                title="Registre de Commerce manquant",
                description="L'entreprise n'a pas de Registre de Commerce valide",
                level=RiskLevel.CRITICAL,
                category="administratif",
                impact="Impossibilité d'exercer légalement, risque de fermeture",
                probability="Certain si non régularisé",
                mitigation="Déposer un dossier au CNRC de votre wilaya",
                penalty_amount=Decimal("500000"),
            ))
        
        # Risque TVA
        revenue = input_data.annual_revenue or Decimal("0")
        if revenue > Decimal("15000000") and not input_data.has_tva:
            risks.append(Risk(
                code="TVA_MISSING",
                title="Non-inscription à la TVA",
                description="CA > 15M DA mais non assujetti à la TVA",
                level=RiskLevel.HIGH,
                category="fiscal",
                impact="Redressement fiscal, pénalités de 25%",
                probability="Élevée lors d'un contrôle",
                mitigation="S'inscrire à la TVA auprès des impôts",
                penalty_amount=revenue * Decimal("0.25"),
            ))
        
        # Risque CNAS
        if input_data.employees_count > 0 and not input_data.has_cnas:
            risks.append(Risk(
                code="CNAS_MISSING",
                title="Non-affiliation CNAS",
                description="Salariés non déclarés à la CNAS",
                level=RiskLevel.CRITICAL,
                category="social",
                impact="Pénalités, poursuites pénales possibles",
                probability="Certain en cas de contrôle",
                mitigation="Affilier immédiatement tous les salariés",
            ))
        
        # Risque CASNOS
        if input_data.legal_form in [LegalForm.AUTO_ENTREPRENEUR, LegalForm.PROFESSION_LIBERALE] and not input_data.has_casnos:
            risks.append(Risk(
                code="CASNOS_MISSING",
                title="Non-affiliation CASNOS",
                description="Non affilié à la Caisse des Non-Salariés",
                level=RiskLevel.HIGH,
                category="social",
                impact="Pas de couverture sociale, pénalités",
                probability="Élevée",
                mitigation="S'affilier à la CASNOS de votre wilaya",
            ))
        
        # Risque documentation
        if not input_data.nif:
            risks.append(Risk(
                code="NIF_MISSING",
                title="NIF non renseigné",
                description="Numéro d'Identification Fiscale manquant",
                level=RiskLevel.MEDIUM,
                category="administratif",
                impact="Impossibilité de facturer légalement",
                probability="Modérée",
                mitigation="Obtenir le NIF auprès des impôts",
            ))
        
        # Calculer les scores
        critical_count = len([r for r in risks if r.level == RiskLevel.CRITICAL])
        high_count = len([r for r in risks if r.level == RiskLevel.HIGH])
        medium_count = len([r for r in risks if r.level == RiskLevel.MEDIUM])
        low_count = len([r for r in risks if r.level == RiskLevel.LOW])
        
        risk_score = min(100, critical_count * 30 + high_count * 20 + medium_count * 10 + low_count * 5)
        compliance_score = 100 - risk_score
        
        overall_level = RiskLevel.LOW
        if critical_count > 0:
            overall_level = RiskLevel.CRITICAL
        elif high_count > 0:
            overall_level = RiskLevel.HIGH
        elif medium_count > 0:
            overall_level = RiskLevel.MEDIUM
        
        # Grouper par catégorie
        risks_by_category = {}
        for risk in risks:
            if risk.category not in risks_by_category:
                risks_by_category[risk.category] = []
            risks_by_category[risk.category].append(risk)
        
        # Actions prioritaires
        priority_actions = [r.mitigation for r in sorted(risks, key=lambda x: (
            0 if x.level == RiskLevel.CRITICAL else
            1 if x.level == RiskLevel.HIGH else
            2 if x.level == RiskLevel.MEDIUM else 3
        ))[:3]]
        
        return RiskAnalysis(
            overall_risk_level=overall_level,
            risk_score=risk_score,
            risks=risks,
            risks_by_category=risks_by_category,
            critical_count=critical_count,
            high_count=high_count,
            medium_count=medium_count,
            low_count=low_count,
            priority_actions=priority_actions,
            compliance_score=compliance_score,
        )
    
    # ========================================
    # Action Plan
    # ========================================
    
    def build_action_plan(self, input_data: CompanyInput, risks: list[Risk]) -> ActionPlan:
        """Construire le plan d'action"""
        
        immediate = []
        short_term = []
        medium_term = []
        long_term = []
        
        # Actions immédiates basées sur les risques critiques
        for risk in risks:
            if risk.level == RiskLevel.CRITICAL:
                immediate.append(ChecklistItem(
                    id=f"action_{risk.code}",
                    title=f"Résoudre: {risk.title}",
                    description=risk.mitigation,
                    category=risk.category,
                    priority=1,
                    deadline_days=7,
                    organism=self._get_organism(risk.code),
                    documents_needed=self._get_documents_needed(risk.code),
                ))
            elif risk.level == RiskLevel.HIGH:
                short_term.append(ChecklistItem(
                    id=f"action_{risk.code}",
                    title=f"Traiter: {risk.title}",
                    description=risk.mitigation,
                    category=risk.category,
                    priority=2,
                    deadline_days=30,
                    organism=self._get_organism(risk.code),
                ))
        
        # Actions de base si pas de RC
        if not input_data.has_rc:
            immediate.insert(0, ChecklistItem(
                id="get_rc",
                title="Obtenir le Registre de Commerce",
                description="Déposer le dossier complet au CNRC",
                category="administratif",
                priority=1,
                deadline_days=7,
                estimated_cost="15 000 - 30 000 DA",
                organism="CNRC",
                documents_needed=[
                    "Copie acte de naissance",
                    "Copie CNI",
                    "Extrait de casier judiciaire",
                    "Contrat de location ou titre de propriété",
                    "Statuts de la société (si société)",
                ],
            ))
        
        # Actions à moyen terme
        medium_term.append(ChecklistItem(
            id="setup_accounting",
            title="Mettre en place la comptabilité",
            description="Choisir un comptable agréé et organiser la tenue comptable",
            category="comptabilité",
            priority=3,
            deadline_days=60,
            estimated_cost="20 000 - 50 000 DA/mois",
        ))
        
        # Actions à long terme
        long_term.append(ChecklistItem(
            id="digital_transformation",
            title="Digitalisation des processus",
            description="Passer aux déclarations en ligne (Jibayatic, CNAS)",
            category="optimisation",
            priority=4,
            deadline_days=90,
        ))
        
        total_items = len(immediate) + len(short_term) + len(medium_term) + len(long_term)
        
        return ActionPlan(
            immediate_actions=immediate,
            short_term_actions=short_term,
            medium_term_actions=medium_term,
            long_term_actions=long_term,
            total_estimated_cost="50 000 - 150 000 DA",
            total_items=total_items,
            completed_items=0,
        )
    
    def _get_organism(self, risk_code: str) -> str:
        """Organisme responsable"""
        mapping = {
            "RC_MISSING": "CNRC",
            "TVA_MISSING": "Direction des Impôts",
            "CNAS_MISSING": "CNAS",
            "CASNOS_MISSING": "CASNOS",
            "NIF_MISSING": "Direction des Impôts",
        }
        return mapping.get(risk_code, "Administration")
    
    def _get_documents_needed(self, risk_code: str) -> list[str]:
        """Documents nécessaires"""
        mapping = {
            "RC_MISSING": ["Acte de naissance", "CNI", "Casier judiciaire", "Contrat de location"],
            "TVA_MISSING": ["RC", "NIF", "Demande d'inscription TVA"],
            "CNAS_MISSING": ["RC", "NIF", "Liste des employés", "Contrats de travail"],
            "CASNOS_MISSING": ["RC", "NIF", "Déclaration de revenus"],
        }
        return mapping.get(risk_code, [])
    
    # ========================================
    # AI Summary
    # ========================================
    
    def generate_ai_summary(self, profile: CompanyProfile, fiscal: FiscalAnalysis, 
                           risks: RiskAnalysis) -> tuple[str, list[str], list[str]]:
        """Générer le résumé IA"""
        
        # Résumé principal
        summary = f"""
🏢 **{profile.company_name}** ({profile.legal_form_full_name})

📍 Basée à **{profile.wilaya}**, cette {profile.size_category.lower()} opère dans le secteur **{profile.sector.value}**.

💰 **Situation fiscale**: Régime **{fiscal.regime.value}** avec un taux effectif d'imposition de **{fiscal.effective_tax_rate:.1f}%**.
{"✅ Non assujetti à la TVA (IFU)" if not fiscal.is_tva_required else "⚠️ Assujetti à la TVA (19%)"}

⚠️ **Niveau de risque global**: {risks.overall_risk_level.value.upper()}
- Score de conformité: **{risks.compliance_score}/100**
- {risks.critical_count} risques critiques, {risks.high_count} risques élevés

{"🔴 ACTION URGENTE REQUISE" if risks.critical_count > 0 else "✅ Situation relativement saine"}
        """.strip()
        
        # Insights clés
        insights = []
        if fiscal.regime == FiscalRegime.IFU:
            insights.append(f"Le régime IFU vous simplifie la vie : pas de TVA, pas de comptabilité commerciale obligatoire")
        if profile.employees_count > 0:
            insights.append(f"Avec {profile.employees_count} salarié(s), vos charges CNAS représentent ~35% de la masse salariale")
        if risks.critical_count > 0:
            insights.append(f"⚠️ {risks.critical_count} risque(s) critique(s) nécessitent une action immédiate")
        insights.append(f"Votre impôt annuel estimé est de {fiscal.total_annual_taxes:,.0f} DA")
        
        # Recommandations
        recommendations = risks.priority_actions[:3] if risks.priority_actions else []
        recommendations.append("Conservez tous vos justificatifs pendant 10 ans minimum")
        recommendations.append("Planifiez vos déclarations fiscales pour éviter les pénalités (10-25%)")
        
        return summary, insights, recommendations
    
    # ========================================
    # Full Analysis
    # ========================================
    
    def run_full_analysis(self, input_data: CompanyInput) -> AuditReport:
        """Exécuter l'analyse complète"""
        
        # Construire tous les éléments
        profile = self.build_company_profile(input_data)
        fiscal = self.analyze_fiscal(input_data)
        social = self.analyze_social_charges(input_data)
        risks = self.analyze_risks(input_data)
        calendar = self.build_declaration_calendar(input_data, fiscal.regime)
        action_plan = self.build_action_plan(input_data, risks.risks)
        
        # Générer le résumé IA
        summary, insights, recommendations = self.generate_ai_summary(profile, fiscal, risks)
        
        # Calculer les scores
        fiscal_health = max(0, 100 - int(fiscal.effective_tax_rate * 2))
        overall_score = (risks.compliance_score + fiscal_health) // 2
        
        # RAG Context (simulé pour l'instant)
        rag_context = None
        if input_data.include_rag_context:
            rag_context = RAGContext(
                query_used=f"obligations fiscales {input_data.sector.value} {input_data.wilaya} Algérie",
                sources_count=3,
                sources=[
                    RAGSource(
                        title="Loi de Finances 2025",
                        source_name="Journal Officiel",
                        source_type="loi",
                        relevance_score=0.95,
                        excerpt="Article 20 : Les entreprises dont le CA est inférieur à 15 millions DA sont soumises à l'IFU...",
                    ),
                    RAGSource(
                        title="Guide du contribuable 2025",
                        source_name="DGI",
                        source_type="guide",
                        relevance_score=0.88,
                        excerpt="Les déclarations G50 doivent être déposées au plus tard le 20 de chaque mois...",
                    ),
                ],
                legal_references=["Loi 23-12 du 05/08/2023", "Décret 24-189"],
                key_articles=["Art. 282 CID", "Art. 20 LF 2025"],
            )
        
        return AuditReport(
            audit_id=str(uuid.uuid4()),
            generated_at=datetime.now(),
            version="2.0",
            company_profile=profile,
            fiscal_analysis=fiscal,
            social_charges=social,
            risk_analysis=risks,
            declaration_calendar=calendar,
            action_plan=action_plan,
            rag_context=rag_context,
            ai_summary=summary,
            key_insights=insights,
            recommendations=recommendations,
            compliance_score=risks.compliance_score,
            fiscal_health_score=fiscal_health,
            overall_score=overall_score,
            pdf_available=False,
        )
    
    def run_quick_analysis(self, input_data: CompanyInput) -> QuickAnalysisResponse:
        """Analyse rapide (moins de crédits)"""
        
        fiscal = self.analyze_fiscal(input_data)
        risks = self.analyze_risks(input_data)
        
        summary, insights, _ = self.generate_ai_summary(
            self.build_company_profile(input_data), fiscal, risks
        )
        
        return QuickAnalysisResponse(
            success=True,
            company_name=input_data.company_name,
            regime=fiscal.regime,
            is_tva_required=fiscal.is_tva_required,
            estimated_annual_taxes=fiscal.total_annual_taxes,
            risk_level=risks.overall_risk_level,
            top_3_risks=[r.title for r in risks.risks[:3]],
            top_3_actions=risks.priority_actions[:3],
            ai_summary=summary,
        )


# Singleton service
pme_analyzer_service = PMEAnalyzerService()
