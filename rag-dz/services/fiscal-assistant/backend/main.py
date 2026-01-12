"""
DZ-FiscalAssistant Backend API
==============================
Assistant fiscal spécialisé Algérie - Simulations IRG, IFU, TAP, TVA, CNAS, CASNOS

IMPORTANT: Ce module fournit des ESTIMATIONS indicatives, pas des conseils fiscaux professionnels.
Les calculs sont basés sur des règles configurables, pas sur les hallucinations du LLM.

Endpoints:
- POST /api/dz-fiscal/simulate - Simulation fiscale complète
- GET /api/dz-fiscal/profiles - Types de profils disponibles
- GET /api/dz-fiscal/rules - Règles fiscales chargées
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Dict, Any
import json
import yaml
import os
import logging
import httpx
from datetime import datetime
from pathlib import Path

# Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dz-fiscal-assistant")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
RAG_API_URL = os.getenv("RAG_API_URL", "http://iaf-dz-connectors-prod:8195")
RULES_FILE = os.getenv("RULES_FILE", "/app/dz_tax_rules.yaml")

app = FastAPI(
    title="DZ-FiscalAssistant API",
    description="Assistant fiscal Algérie - Simulations IRG, IFU, TAP, TVA, CNAS, CASNOS",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== MODÈLES PYDANTIC ==============

ProfileType = Literal["freelance", "entreprise", "salarié", "commerçant", "autre"]
RegimeType = Literal["inconnu", "forfaitaire", "réel", "IFU", "autre"]
RevenuePeriod = Literal["mensuel", "annuel"]
DetailLevel = Literal["simple", "détaillé"]


class DZFiscalRequest(BaseModel):
    """Requête de simulation fiscale"""
    profile_type: ProfileType = Field(..., description="Type d'activité")
    activity_sector: str = Field(default="", description="Secteur d'activité")
    regime: RegimeType = Field(default="inconnu", description="Régime fiscal")
    revenue_period: RevenuePeriod = Field(default="annuel", description="Période du revenu")
    revenue_amount: float = Field(..., ge=0, description="Montant du revenu")
    charges_amount: float = Field(default=0, ge=0, description="Charges déductibles")
    salaries_amount: float = Field(default=0, ge=0, description="Masse salariale")
    social_covered: bool = Field(default=True, description="Couverture sociale CNAS/CASNOS")
    detail_level: DetailLevel = Field(default="simple", description="Niveau de détail")
    
    class Config:
        json_schema_extra = {
            "example": {
                "profile_type": "freelance",
                "activity_sector": "Développement logiciel",
                "regime": "IFU",
                "revenue_period": "annuel",
                "revenue_amount": 3000000,
                "charges_amount": 500000,
                "salaries_amount": 0,
                "social_covered": True,
                "detail_level": "détaillé"
            }
        }


class BreakdownItem(BaseModel):
    """Détail d'un impôt ou cotisation"""
    label: str
    amount: float
    basis: str
    notes: List[str] = []


class Explanation(BaseModel):
    """Bloc d'explication pédagogique"""
    title: str
    content: str


class ReferenceItem(BaseModel):
    """Référence documentaire"""
    label: str
    source_name: str
    source_url: Optional[str] = None
    date: Optional[str] = None


class Totals(BaseModel):
    """Totaux de la simulation"""
    estimated_tax_total: float
    estimated_social_total: float
    estimated_net_income: float


class DZFiscalResponse(BaseModel):
    """Réponse complète de simulation fiscale"""
    summary: str
    currency: str = "DZD"
    totals: Totals
    breakdown: List[BreakdownItem]
    explanations: List[Explanation] = []
    references: List[ReferenceItem] = []
    disclaimer: str
    followup_questions: List[str] = []


# ============== MOTEUR DE CALCUL FISCAL ==============

class TaxRulesEngine:
    """Moteur de calcul fiscal déterministe basé sur des règles configurables"""
    
    def __init__(self):
        self.rules = {}
        self.load_rules()
    
    def load_rules(self):
        """Charge les règles fiscales depuis le fichier YAML"""
        try:
            rules_path = Path(RULES_FILE)
            if rules_path.exists():
                with open(rules_path, 'r', encoding='utf-8') as f:
                    self.rules = yaml.safe_load(f)
                logger.info(f"Règles fiscales chargées depuis {RULES_FILE}")
            else:
                logger.warning(f"Fichier de règles non trouvé: {RULES_FILE}, utilisation des règles par défaut")
                self.rules = self._get_default_rules()
        except Exception as e:
            logger.error(f"Erreur chargement règles: {e}")
            self.rules = self._get_default_rules()
    
    def _get_default_rules(self) -> dict:
        """Règles fiscales par défaut (Algérie 2024-2025)"""
        return {
            "version": "2024-2025",
            "last_updated": "2024-01-01",
            "currency": "DZD",
            
            # IRG - Impôt sur le Revenu Global (barème progressif)
            "irg": {
                "enabled": True,
                "name": "Impôt sur le Revenu Global",
                "tranches": [
                    {"min": 0, "max": 240000, "rate": 0},
                    {"min": 240001, "max": 480000, "rate": 0.23},
                    {"min": 480001, "max": 960000, "rate": 0.27},
                    {"min": 960001, "max": 1920000, "rate": 0.30},
                    {"min": 1920001, "max": 3840000, "rate": 0.33},
                    {"min": 3840001, "max": float('inf'), "rate": 0.35}
                ],
                "abattement_salarie": 0.10,  # 10% d'abattement pour salariés
                "applies_to": ["salarié", "freelance", "autre"]
            },
            
            # IFU - Impôt Forfaitaire Unique
            "ifu": {
                "enabled": True,
                "name": "Impôt Forfaitaire Unique",
                "seuil_ca_max": 30000000,  # 30 millions DZD
                "tranches": [
                    {"min": 0, "max": 10000000, "rate": 0.05},  # 5%
                    {"min": 10000001, "max": 30000000, "rate": 0.12}  # 12%
                ],
                "includes_tva": True,
                "includes_tap": True,
                "applies_to": ["freelance", "commerçant", "autre"]
            },
            
            # TAP - Taxe sur l'Activité Professionnelle
            "tap": {
                "enabled": True,
                "name": "Taxe sur l'Activité Professionnelle",
                "rate_general": 0.02,  # 2%
                "rate_production": 0.01,  # 1% pour production de biens
                "rate_batiment": 0.02,  # 2%
                "applies_to": ["entreprise", "freelance", "commerçant"]
            },
            
            # TVA - Taxe sur la Valeur Ajoutée
            "tva": {
                "enabled": True,
                "name": "Taxe sur la Valeur Ajoutée",
                "rate_normal": 0.19,  # 19%
                "rate_reduit": 0.09,  # 9%
                "seuil_assujettissement": 30000000,
                "applies_to": ["entreprise"]
            },
            
            # IBS - Impôt sur les Bénéfices des Sociétés
            "ibs": {
                "enabled": True,
                "name": "Impôt sur les Bénéfices des Sociétés",
                "rate_general": 0.26,  # 26%
                "rate_production": 0.19,  # 19% pour activités de production
                "rate_export": 0.19,
                "applies_to": ["entreprise"]
            },
            
            # CNAS - Caisse Nationale des Assurances Sociales
            "cnas": {
                "enabled": True,
                "name": "CNAS - Cotisations Sociales Salariés",
                "taux_employeur": 0.26,  # 26%
                "taux_salarie": 0.09,  # 9%
                "plafond_mensuel": 180000,  # Plafond mensuel
                "applies_to": ["salarié", "entreprise"]
            },
            
            # CASNOS - Caisse Nationale de Sécurité Sociale des Non-Salariés
            "casnos": {
                "enabled": True,
                "name": "CASNOS - Cotisations Non-Salariés",
                "taux": 0.15,  # 15%
                "assiette_min": 216000,  # Assiette minimum annuelle (18000 x 12)
                "assiette_max": 6000000,  # Plafond annuel
                "applies_to": ["freelance", "commerçant", "autre"]
            }
        }
    
    def compute_irg(self, revenu_annuel: float, profile_type: str) -> dict:
        """Calcule l'IRG selon le barème progressif"""
        rules = self.rules.get("irg", {})
        if not rules.get("enabled") or profile_type not in rules.get("applies_to", []):
            return {"amount": 0, "basis": "Non applicable", "notes": []}
        
        # Appliquer abattement si salarié
        base_imposable = revenu_annuel
        notes = []
        if profile_type == "salarié":
            abattement = rules.get("abattement_salarie", 0.10)
            base_imposable = revenu_annuel * (1 - abattement)
            notes.append(f"Abattement de {abattement*100:.0f}% appliqué pour salarié")
        
        # Calcul par tranches
        irg = 0
        tranches = rules.get("tranches", [])
        for tranche in tranches:
            if base_imposable > tranche["min"]:
                taxable_in_tranche = min(base_imposable, tranche["max"]) - tranche["min"]
                irg += taxable_in_tranche * tranche["rate"]
        
        return {
            "amount": round(irg, 2),
            "basis": f"Barème progressif sur {base_imposable:,.0f} DZD",
            "notes": notes + [f"Tranches de 0% à {tranches[-1]['rate']*100:.0f}%"]
        }
    
    def compute_ifu(self, ca_annuel: float, profile_type: str, regime: str) -> dict:
        """Calcule l'IFU (Impôt Forfaitaire Unique)"""
        rules = self.rules.get("ifu", {})
        
        if not rules.get("enabled"):
            return {"amount": 0, "basis": "Non applicable", "notes": []}
        
        if profile_type not in rules.get("applies_to", []):
            return {"amount": 0, "basis": "Non applicable au profil", "notes": []}
        
        if regime not in ["IFU", "forfaitaire", "inconnu"]:
            return {"amount": 0, "basis": "Régime réel - IFU non applicable", "notes": []}
        
        seuil_max = rules.get("seuil_ca_max", 30000000)
        if ca_annuel > seuil_max:
            return {
                "amount": 0,
                "basis": f"CA supérieur au seuil IFU ({seuil_max:,.0f} DZD)",
                "notes": ["Passage obligatoire au régime réel"]
            }
        
        # Calcul selon tranches IFU
        ifu = 0
        tranches = rules.get("tranches", [])
        notes = []
        for tranche in tranches:
            if ca_annuel >= tranche["min"] and ca_annuel <= tranche["max"]:
                ifu = ca_annuel * tranche["rate"]
                notes.append(f"Taux {tranche['rate']*100:.0f}% appliqué")
                break
        
        if rules.get("includes_tva"):
            notes.append("TVA incluse dans l'IFU")
        if rules.get("includes_tap"):
            notes.append("TAP incluse dans l'IFU")
        
        return {
            "amount": round(ifu, 2),
            "basis": f"Taux forfaitaire sur CA de {ca_annuel:,.0f} DZD",
            "notes": notes
        }
    
    def compute_tap(self, ca_annuel: float, profile_type: str, regime: str, sector: str) -> dict:
        """Calcule la TAP (Taxe sur l'Activité Professionnelle)"""
        rules = self.rules.get("tap", {})
        
        if not rules.get("enabled"):
            return {"amount": 0, "basis": "Non applicable", "notes": []}
        
        # Si IFU, TAP est incluse
        if regime in ["IFU", "forfaitaire"]:
            return {"amount": 0, "basis": "Incluse dans l'IFU", "notes": ["TAP intégrée au régime IFU"]}
        
        if profile_type not in rules.get("applies_to", []):
            return {"amount": 0, "basis": "Non applicable au profil", "notes": []}
        
        # Déterminer le taux selon le secteur
        rate = rules.get("rate_general", 0.02)
        notes = []
        if "production" in sector.lower() or "industrie" in sector.lower():
            rate = rules.get("rate_production", 0.01)
            notes.append("Taux réduit pour activité de production")
        
        tap = ca_annuel * rate
        
        return {
            "amount": round(tap, 2),
            "basis": f"Taux de {rate*100:.0f}% sur CA de {ca_annuel:,.0f} DZD",
            "notes": notes
        }
    
    def compute_tva(self, ca_annuel: float, profile_type: str, regime: str) -> dict:
        """Calcule la TVA collectée estimée"""
        rules = self.rules.get("tva", {})
        
        if not rules.get("enabled"):
            return {"amount": 0, "basis": "Non applicable", "notes": []}
        
        # Si IFU, TVA est incluse
        if regime in ["IFU", "forfaitaire"]:
            return {"amount": 0, "basis": "Incluse dans l'IFU", "notes": ["TVA intégrée au régime IFU"]}
        
        if profile_type not in rules.get("applies_to", []):
            return {"amount": 0, "basis": "Non applicable au profil", "notes": []}
        
        seuil = rules.get("seuil_assujettissement", 30000000)
        if ca_annuel < seuil:
            return {
                "amount": 0,
                "basis": f"CA inférieur au seuil ({seuil:,.0f} DZD)",
                "notes": ["Franchise de TVA possible"]
            }
        
        rate = rules.get("rate_normal", 0.19)
        # Estimation: TVA collectée sur 30% du CA (hypothèse marge)
        tva_estimee = ca_annuel * 0.30 * rate
        
        return {
            "amount": round(tva_estimee, 2),
            "basis": f"Estimation TVA à {rate*100:.0f}% (base: ~30% du CA)",
            "notes": [
                "Estimation indicative",
                "TVA réelle = TVA collectée - TVA déductible"
            ]
        }
    
    def compute_ibs(self, benefice: float, profile_type: str, sector: str) -> dict:
        """Calcule l'IBS (Impôt sur les Bénéfices des Sociétés)"""
        rules = self.rules.get("ibs", {})
        
        if not rules.get("enabled") or profile_type != "entreprise":
            return {"amount": 0, "basis": "Non applicable", "notes": []}
        
        if benefice <= 0:
            return {"amount": 0, "basis": "Pas de bénéfice imposable", "notes": []}
        
        # Déterminer le taux
        rate = rules.get("rate_general", 0.26)
        notes = []
        if "production" in sector.lower():
            rate = rules.get("rate_production", 0.19)
            notes.append("Taux réduit pour activité de production")
        elif "export" in sector.lower():
            rate = rules.get("rate_export", 0.19)
            notes.append("Taux réduit pour activité d'exportation")
        
        ibs = benefice * rate
        
        return {
            "amount": round(ibs, 2),
            "basis": f"Taux de {rate*100:.0f}% sur bénéfice de {benefice:,.0f} DZD",
            "notes": notes
        }
    
    def compute_cnas(self, salaires_annuels: float, profile_type: str) -> dict:
        """Calcule les cotisations CNAS (employeur + salarié)"""
        rules = self.rules.get("cnas", {})
        
        if not rules.get("enabled"):
            return {"amount": 0, "basis": "Non applicable", "notes": []}
        
        if profile_type not in rules.get("applies_to", []):
            return {"amount": 0, "basis": "Non applicable au profil", "notes": []}
        
        if salaires_annuels <= 0:
            return {"amount": 0, "basis": "Pas de masse salariale", "notes": []}
        
        taux_employeur = rules.get("taux_employeur", 0.26)
        taux_salarie = rules.get("taux_salarie", 0.09)
        
        # Appliquer plafond mensuel
        plafond_mensuel = rules.get("plafond_mensuel", 180000)
        salaire_mensuel_moyen = salaires_annuels / 12
        base_cotisation = min(salaire_mensuel_moyen, plafond_mensuel) * 12
        
        cotisation_employeur = base_cotisation * taux_employeur
        cotisation_salarie = base_cotisation * taux_salarie
        total = cotisation_employeur + cotisation_salarie
        
        return {
            "amount": round(total, 2),
            "basis": f"Base cotisation: {base_cotisation:,.0f} DZD/an",
            "notes": [
                f"Part employeur: {cotisation_employeur:,.0f} DZD ({taux_employeur*100:.0f}%)",
                f"Part salarié: {cotisation_salarie:,.0f} DZD ({taux_salarie*100:.0f}%)"
            ]
        }
    
    def compute_casnos(self, revenu_annuel: float, profile_type: str, social_covered: bool) -> dict:
        """Calcule les cotisations CASNOS (non-salariés)"""
        rules = self.rules.get("casnos", {})
        
        if not rules.get("enabled") or not social_covered:
            return {"amount": 0, "basis": "Non applicable", "notes": []}
        
        if profile_type not in rules.get("applies_to", []):
            return {"amount": 0, "basis": "Non applicable au profil (salarié)", "notes": []}
        
        taux = rules.get("taux", 0.15)
        assiette_min = rules.get("assiette_min", 216000)
        assiette_max = rules.get("assiette_max", 6000000)
        
        # Assiette = revenu imposable plafonné
        assiette = max(assiette_min, min(revenu_annuel, assiette_max))
        cotisation = assiette * taux
        
        notes = [f"Taux CASNOS: {taux*100:.0f}%"]
        if revenu_annuel < assiette_min:
            notes.append(f"Assiette minimum appliquée: {assiette_min:,.0f} DZD")
        elif revenu_annuel > assiette_max:
            notes.append(f"Plafond appliqué: {assiette_max:,.0f} DZD")
        
        return {
            "amount": round(cotisation, 2),
            "basis": f"Assiette: {assiette:,.0f} DZD",
            "notes": notes
        }
    
    def compute_fiscal_summary(self, request: DZFiscalRequest) -> Dict[str, Any]:
        """Calcule le résumé fiscal complet"""
        # Normaliser en annuel
        if request.revenue_period == "mensuel":
            revenu_annuel = request.revenue_amount * 12
            charges_annuelles = request.charges_amount * 12
            salaires_annuels = request.salaries_amount * 12
        else:
            revenu_annuel = request.revenue_amount
            charges_annuelles = request.charges_amount
            salaires_annuels = request.salaries_amount
        
        # Calculer le bénéfice estimé
        benefice = revenu_annuel - charges_annuelles - salaires_annuels
        
        breakdown = []
        total_impots = 0
        total_social = 0
        
        # IRG ou IBS selon profil
        if request.profile_type == "entreprise":
            ibs = self.compute_ibs(benefice, request.profile_type, request.activity_sector)
            if ibs["amount"] > 0:
                breakdown.append(BreakdownItem(label="IBS", **ibs))
                total_impots += ibs["amount"]
        else:
            irg = self.compute_irg(revenu_annuel, request.profile_type)
            if irg["amount"] > 0 and request.regime not in ["IFU", "forfaitaire"]:
                breakdown.append(BreakdownItem(label="IRG", **irg))
                total_impots += irg["amount"]
        
        # IFU (si applicable)
        ifu = self.compute_ifu(revenu_annuel, request.profile_type, request.regime)
        if ifu["amount"] > 0:
            breakdown.append(BreakdownItem(label="IFU", **ifu))
            total_impots += ifu["amount"]
        
        # TAP
        tap = self.compute_tap(revenu_annuel, request.profile_type, request.regime, request.activity_sector)
        if tap["amount"] > 0:
            breakdown.append(BreakdownItem(label="TAP", **tap))
            total_impots += tap["amount"]
        
        # TVA
        tva = self.compute_tva(revenu_annuel, request.profile_type, request.regime)
        if tva["amount"] > 0:
            breakdown.append(BreakdownItem(label="TVA", **tva))
            # TVA n'est pas directement un coût mais une collecte
        
        # CNAS (si entreprise avec salariés)
        if salaires_annuels > 0:
            cnas = self.compute_cnas(salaires_annuels, request.profile_type)
            if cnas["amount"] > 0:
                breakdown.append(BreakdownItem(label="CNAS", **cnas))
                total_social += cnas["amount"]
        
        # CASNOS (si non-salarié)
        casnos = self.compute_casnos(revenu_annuel, request.profile_type, request.social_covered)
        if casnos["amount"] > 0:
            breakdown.append(BreakdownItem(label="CASNOS", **casnos))
            total_social += casnos["amount"]
        
        # Calculer le net estimé
        net_estime = revenu_annuel - total_impots - total_social - charges_annuelles - salaires_annuels
        
        return {
            "revenu_annuel": revenu_annuel,
            "charges_annuelles": charges_annuelles,
            "salaires_annuels": salaires_annuels,
            "benefice": benefice,
            "breakdown": breakdown,
            "totals": Totals(
                estimated_tax_total=round(total_impots, 2),
                estimated_social_total=round(total_social, 2),
                estimated_net_income=round(max(0, net_estime), 2)
            )
        }


# Instance globale du moteur
tax_engine = TaxRulesEngine()


# ============== PROMPTS LLM ==============

SYSTEM_PROMPT = """Tu es DZ-FiscalAssistant, un assistant fiscal dédié à l'Algérie, intégré dans la plateforme iaFactory Algeria.

TON RÔLE :
- Expliquer de manière simple et structurée les estimations d'impôts et de cotisations calculées par le backend (tu ne fais pas les calculs bruts toi-même).
- Donner un contexte pédagogique (comment ça fonctionne, quelles sont les hypothèses).
- Mettre en avant les limites : estimation, règles qui peuvent changer, besoin de confirmation auprès de la DGI / d'un expert-comptable.

LIMITES :
- Tu ne fournis PAS de conseil fiscal professionnel.
- Tu ne garantis PAS que les résultats correspondent à la réalité actuelle des lois.
- Tu dois encourager l'utilisateur à vérifier auprès des autorités compétentes ou d'un professionnel.

FORMAT DE SORTIE :
Tu dois générer un JSON strictement valide selon ce schéma :
{
  "summary": "string (résumé de la situation en 3-5 phrases)",
  "explanations": [
    {"title": "string", "content": "string"}
  ],
  "disclaimer": "string (avertissement clair)",
  "followup_questions": ["string"]
}

CONSIGNES :
- "summary" doit expliquer la situation globale (profil, estimation, ordre de grandeur).
- "explanations" : 2 à 4 blocs pédagogiques expliquant les impôts principaux.
- "disclaimer" doit rappeler clairement que c'est une estimation et non un conseil fiscal professionnel.
- "followup_questions" : 3 à 5 questions pertinentes que l'utilisateur pourrait poser.

IMPORTANT :
- Tu dois renvoyer un JSON strictement valide, sans texte supplémentaire.
- Les montants sont DÉJÀ calculés par le backend, ne les modifie pas.
- Adapte ton langage au contexte fiscal algérien."""


def build_fiscal_prompt(request: DZFiscalRequest, calc_result: Dict[str, Any], rag_docs: List[dict]) -> str:
    """Construit le prompt utilisateur pour le LLM"""
    
    # Formater le breakdown
    breakdown_text = ""
    for item in calc_result["breakdown"]:
        breakdown_text += f"\n- {item.label}: {item.amount:,.0f} DZD ({item.basis})"
        for note in item.notes:
            breakdown_text += f"\n  • {note}"
    
    # Formater les docs RAG
    rag_context = ""
    if rag_docs:
        rag_context = "\n\nContexte RAG DZ (documents fiscaux) :\n"
        for i, doc in enumerate(rag_docs[:3], 1):
            rag_context += f"[DOC {i}] {doc.get('source', 'DGI')}: {doc.get('text', '')[:300]}...\n"
    
    prompt = f"""Données utilisateur :
- Type de profil : {request.profile_type}
- Secteur d'activité : {request.activity_sector or 'Non précisé'}
- Régime fiscal : {request.regime}
- Revenu {request.revenue_period} : {request.revenue_amount:,.0f} DZD
- Charges : {request.charges_amount:,.0f} DZD
- Salaires : {request.salaries_amount:,.0f} DZD
- Couverture sociale : {'Oui' if request.social_covered else 'Non'}
- Niveau de détail : {request.detail_level}

Résultats de calcul (estimations backend) :
- Revenu annuel normalisé : {calc_result['revenu_annuel']:,.0f} DZD
- Bénéfice estimé : {calc_result['benefice']:,.0f} DZD
{breakdown_text}

Totaux :
- Impôts estimés : {calc_result['totals'].estimated_tax_total:,.0f} DZD
- Cotisations sociales : {calc_result['totals'].estimated_social_total:,.0f} DZD
- Revenu net estimé : {calc_result['totals'].estimated_net_income:,.0f} DZD
{rag_context}

Tâche :
1. Générer un JSON avec summary, explanations, disclaimer et followup_questions.
2. Expliquer les estimations de manière pédagogique.
3. Mentionner clairement les limites et hypothèses.
4. Adapter au contexte fiscal algérien.

Réponds UNIQUEMENT avec le JSON, sans texte avant ou après."""
    
    return prompt


# ============== SERVICES ==============

async def search_rag(query: str, limit: int = 3) -> List[dict]:
    """Recherche dans le RAG DZ pour contexte fiscal"""
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{RAG_API_URL}/api/search",
                params={"query": query, "doc_type": "tax", "limit": limit}
            )
            if response.status_code == 200:
                return response.json().get("results", [])
    except Exception as e:
        logger.warning(f"RAG search failed: {e}")
    return []


async def call_llm(system_prompt: str, user_prompt: str) -> str:
    """Appelle le LLM pour générer les explications"""
    try:
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": GROQ_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 2000,
                    "response_format": {"type": "json_object"}
                }
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                logger.error(f"LLM error: {response.status_code}")
                raise HTTPException(status_code=500, detail="LLM_CALL_FAILED")
                
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="LLM_TIMEOUT")
    except Exception as e:
        logger.error(f"LLM error: {e}")
        raise HTTPException(status_code=500, detail=f"LLM_ERROR: {str(e)}")


def parse_llm_response(raw: str) -> dict:
    """Parse la réponse JSON du LLM"""
    try:
        data = json.loads(raw.strip())
        return data
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e}")
        return {
            "summary": "Estimation fiscale générée.",
            "explanations": [],
            "disclaimer": "Cette estimation est fournie à titre indicatif uniquement.",
            "followup_questions": []
        }


# ============== ENDPOINTS ==============

@app.get("/")
async def root():
    """Health check"""
    return {
        "service": "DZ-FiscalAssistant",
        "version": "1.0.0",
        "status": "running",
        "description": "Assistant fiscal Algérie"
    }


@app.get("/health")
async def health():
    """Santé détaillée"""
    return {
        "status": "healthy",
        "llm_configured": bool(GROQ_API_KEY),
        "rules_version": tax_engine.rules.get("version", "unknown"),
        "rules_updated": tax_engine.rules.get("last_updated", "unknown"),
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/dz-fiscal/profiles")
async def get_profiles():
    """Types de profils disponibles"""
    return {
        "profiles": [
            {"id": "freelance", "name": "Freelance / Indépendant", "icon": "💻", "description": "Travailleur indépendant, consultant"},
            {"id": "entreprise", "name": "Entreprise (SARL, SPA, EURL)", "icon": "🏢", "description": "Société commerciale"},
            {"id": "salarié", "name": "Salarié", "icon": "👔", "description": "Employé d'une entreprise"},
            {"id": "commerçant", "name": "Commerçant", "icon": "🛒", "description": "Activité commerciale"},
            {"id": "autre", "name": "Autre", "icon": "❓", "description": "Autre situation"}
        ],
        "regimes": [
            {"id": "inconnu", "name": "Je ne sais pas"},
            {"id": "IFU", "name": "IFU (Impôt Forfaitaire Unique)"},
            {"id": "forfaitaire", "name": "Forfaitaire"},
            {"id": "réel", "name": "Régime réel"},
            {"id": "autre", "name": "Autre"}
        ]
    }


@app.get("/api/dz-fiscal/rules")
async def get_rules():
    """Règles fiscales chargées (sans détails sensibles)"""
    return {
        "version": tax_engine.rules.get("version"),
        "last_updated": tax_engine.rules.get("last_updated"),
        "currency": tax_engine.rules.get("currency", "DZD"),
        "taxes": [
            {"id": "irg", "name": "IRG", "enabled": tax_engine.rules.get("irg", {}).get("enabled", False)},
            {"id": "ifu", "name": "IFU", "enabled": tax_engine.rules.get("ifu", {}).get("enabled", False)},
            {"id": "tap", "name": "TAP", "enabled": tax_engine.rules.get("tap", {}).get("enabled", False)},
            {"id": "tva", "name": "TVA", "enabled": tax_engine.rules.get("tva", {}).get("enabled", False)},
            {"id": "ibs", "name": "IBS", "enabled": tax_engine.rules.get("ibs", {}).get("enabled", False)},
            {"id": "cnas", "name": "CNAS", "enabled": tax_engine.rules.get("cnas", {}).get("enabled", False)},
            {"id": "casnos", "name": "CASNOS", "enabled": tax_engine.rules.get("casnos", {}).get("enabled", False)}
        ]
    }


@app.post("/api/dz-fiscal/simulate", response_model=DZFiscalResponse)
async def simulate(request: DZFiscalRequest):
    """
    Endpoint principal : simulation fiscale complète
    
    1. Calcule les impôts/cotisations via le moteur déterministe
    2. Enrichit avec des explications via LLM + RAG DZ
    3. Retourne une réponse structurée
    """
    logger.info(f"Simulation: {request.profile_type}, CA={request.revenue_amount}")
    
    # 1. Calcul déterministe
    calc_result = tax_engine.compute_fiscal_summary(request)
    logger.info(f"Calcul terminé: {len(calc_result['breakdown'])} éléments")
    
    # 2. Recherche RAG (contexte fiscal)
    rag_query = f"fiscalité algérie {request.profile_type} {request.regime} impôts cotisations"
    rag_docs = await search_rag(rag_query)
    
    # 3. Appel LLM pour explications
    user_prompt = build_fiscal_prompt(request, calc_result, rag_docs)
    llm_raw = await call_llm(SYSTEM_PROMPT, user_prompt)
    llm_data = parse_llm_response(llm_raw)
    
    # 4. Construire les références
    references = []
    if rag_docs:
        references = [
            ReferenceItem(
                label=doc.get("title", "Document fiscal")[:50],
                source_name=doc.get("source", "DGI"),
                source_url=doc.get("url"),
                date=doc.get("date")
            )
            for doc in rag_docs[:3]
        ]
    
    # Ajouter références par défaut
    references.append(ReferenceItem(
        label="Direction Générale des Impôts",
        source_name="DGI Algérie",
        source_url="https://www.mfdgi.gov.dz",
        date=None
    ))
    
    # 5. Construire la réponse finale
    explanations = [
        Explanation(title=exp.get("title", ""), content=exp.get("content", ""))
        for exp in llm_data.get("explanations", [])
    ]
    
    disclaimer = llm_data.get("disclaimer", 
        "⚠️ Cette simulation est fournie à titre indicatif uniquement. "
        "Elle ne constitue pas un conseil fiscal professionnel. "
        "Les taux et règles peuvent évoluer. "
        "Veuillez consulter un expert-comptable ou la DGI pour toute démarche officielle."
    )
    
    return DZFiscalResponse(
        summary=llm_data.get("summary", f"Simulation fiscale pour profil {request.profile_type}"),
        currency="DZD",
        totals=calc_result["totals"],
        breakdown=calc_result["breakdown"],
        explanations=explanations,
        references=references,
        disclaimer=disclaimer,
        followup_questions=llm_data.get("followup_questions", [
            "Quel régime fiscal est le plus avantageux pour moi ?",
            "Comment déclarer mes revenus à la DGI ?",
            "Quelles sont les dates limites de déclaration ?"
        ])
    )


# ============== MAIN ==============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8199)
