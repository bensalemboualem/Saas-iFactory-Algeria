"""
CRM PRO - Service IA
====================
Scoring intelligent, génération de messages, suggestions d'actions
HubSpot DZ/CH powered by IA
"""

import os
import uuid
import json
import logging
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional, List, Dict, Any, Tuple
import httpx

from ..models.crm_pro_models import (
    # Enums
    LeadStatus, LeadSource, LeadPriority, ActionType, Sector, InteractionType,
    # Models
    LeadPro, LeadProCreate, LeadProUpdate,
    LeadAIScoreResponse, LeadAIMessageResponse, LeadAINextActionResponse,
    Interaction, CRMStats, PipelineColumn, PipelineView,
    # Constants
    STATUS_COLORS, STATUS_NAMES, SOURCE_LABELS, DEFAULT_SCORING_WEIGHTS,
)

logger = logging.getLogger(__name__)


# ============================================
# IN-MEMORY STORAGE (Production: PostgreSQL)
# ============================================

leads_db: Dict[str, LeadPro] = {}
interactions_db: List[Interaction] = []


# ============================================
# CRM PRO SERVICE
# ============================================

class CRMProService:
    """Service CRM PRO avec IA intégrée"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        
    # ============================================
    # CRUD LEADS
    # ============================================
    
    def create_lead(self, data: LeadProCreate, user_id: Optional[str] = None) -> LeadPro:
        """
        Créer un nouveau lead avec scoring IA automatique
        """
        lead_id = f"lead_{uuid.uuid4().hex[:12]}"
        
        # Scoring IA
        score_result = self._calculate_score(data)
        
        # Déterminer statut automatique selon règles
        status = data.status or self._determine_status(data, score_result["score"])
        priority = data.priority or score_result["recommended_priority"]
        
        lead = LeadPro(
            id=lead_id,
            name=data.name,
            email=data.email,
            phone=data.phone,
            company=data.company,
            sector=data.sector,
            source=data.source,
            status=status,
            priority=priority,
            
            # Infos supplémentaires
            job_title=data.job_title,
            employees_count=data.employees_count,
            annual_revenue=data.annual_revenue,
            country=data.country,
            city=data.city,
            wilaya=data.wilaya,
            need_description=data.need_description,
            budget=data.budget,
            urgency=data.urgency,
            notes=data.notes,
            
            # Scoring IA
            score=score_result["score"],
            confidence=score_result["confidence"],
            score_reasons=score_result["reasons"],
            probability=score_result["probability"],
            
            # Actions IA
            next_action=score_result.get("next_action"),
            next_action_type=score_result.get("next_action_type"),
            
            # Métadonnées
            tags=data.tags or [],
            metadata=data.metadata or {},
            
            # Assignation
            assigned_to=user_id,
            
            # Timestamps
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        
        leads_db[lead_id] = lead
        
        # Log interaction création
        self._log_interaction(
            lead_id=lead_id,
            type=InteractionType.NOTE,
            content=f"Lead créé avec score IA: {score_result['score']}/100",
            user_id=user_id,
        )
        
        logger.info(f"Lead créé: {lead_id} - Score: {score_result['score']}")
        
        return lead
    
    def get_lead(self, lead_id: str) -> Optional[LeadPro]:
        """Récupérer un lead par ID"""
        return leads_db.get(lead_id)
    
    def update_lead(
        self, 
        lead_id: str, 
        data: LeadProUpdate,
        user_id: Optional[str] = None,
        rescore: bool = True,
    ) -> Optional[LeadPro]:
        """
        Mettre à jour un lead
        """
        lead = leads_db.get(lead_id)
        if not lead:
            return None
        
        old_status = lead.status
        
        # Appliquer les mises à jour
        update_dict = data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            if hasattr(lead, key):
                setattr(lead, key, value)
        
        lead.updated_at = datetime.utcnow()
        
        # Recalculer le score si demandé
        if rescore:
            score_result = self._calculate_score_from_lead(lead)
            lead.score = score_result["score"]
            lead.confidence = score_result["confidence"]
            lead.score_reasons = score_result["reasons"]
            lead.probability = score_result["probability"]
        
        # Log changement de statut
        if data.status and data.status != old_status:
            self._log_interaction(
                lead_id=lead_id,
                type=InteractionType.STATUS_CHANGE,
                content=f"Statut changé: {STATUS_NAMES.get(old_status, old_status)} → {STATUS_NAMES.get(data.status, data.status)}",
                user_id=user_id,
            )
        
        leads_db[lead_id] = lead
        
        return lead
    
    def delete_lead(self, lead_id: str) -> bool:
        """Supprimer un lead"""
        if lead_id in leads_db:
            del leads_db[lead_id]
            return True
        return False
    
    def list_leads(
        self,
        status: Optional[List[LeadStatus]] = None,
        source: Optional[List[LeadSource]] = None,
        sector: Optional[List[Sector]] = None,
        priority: Optional[List[LeadPriority]] = None,
        min_score: Optional[int] = None,
        max_score: Optional[int] = None,
        search: Optional[str] = None,
        assigned_to: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> Tuple[List[LeadPro], int]:
        """
        Liste paginée des leads avec filtres
        """
        leads = list(leads_db.values())
        
        # Filtres
        if status:
            leads = [l for l in leads if l.status in status]
        if source:
            leads = [l for l in leads if l.source in source]
        if sector:
            leads = [l for l in leads if l.sector in sector]
        if priority:
            leads = [l for l in leads if l.priority in priority]
        if min_score is not None:
            leads = [l for l in leads if l.score >= min_score]
        if max_score is not None:
            leads = [l for l in leads if l.score <= max_score]
        if assigned_to:
            leads = [l for l in leads if l.assigned_to == assigned_to]
        if search:
            search_lower = search.lower()
            leads = [l for l in leads if (
                search_lower in l.name.lower() or
                (l.email and search_lower in l.email.lower()) or
                (l.company and search_lower in l.company.lower()) or
                (l.phone and search_lower in l.phone)
            )]
        
        total = len(leads)
        
        # Tri
        reverse = sort_order == "desc"
        if sort_by == "score":
            leads.sort(key=lambda x: x.score, reverse=reverse)
        elif sort_by == "priority":
            priority_order = {LeadPriority.URGENT: 4, LeadPriority.HIGH: 3, LeadPriority.MEDIUM: 2, LeadPriority.LOW: 1}
            leads.sort(key=lambda x: priority_order.get(x.priority, 0), reverse=reverse)
        elif sort_by == "status":
            status_order = {LeadStatus.WARM: 6, LeadStatus.PROPOSAL: 5, LeadStatus.QUALIFY: 4, LeadStatus.NEW: 3, LeadStatus.WON: 2, LeadStatus.LOST: 1}
            leads.sort(key=lambda x: status_order.get(x.status, 0), reverse=reverse)
        else:  # created_at
            leads.sort(key=lambda x: x.created_at, reverse=reverse)
        
        # Pagination
        start = (page - 1) * page_size
        end = start + page_size
        leads = leads[start:end]
        
        return leads, total
    
    # ============================================
    # SCORING IA
    # ============================================
    
    def _calculate_score(self, data: LeadProCreate) -> Dict[str, Any]:
        """
        Calculer le score IA d'un lead
        Score de 0 à 100
        """
        score = 0
        reasons = []
        
        weights = DEFAULT_SCORING_WEIGHTS
        
        # Points de base selon les données fournies
        if data.email:
            score += weights["has_email"]
            reasons.append("Email fourni (+10)")
        
        if data.phone:
            score += weights["has_phone"]
            reasons.append("Téléphone fourni (+10)")
        
        if data.company:
            score += weights["has_company"]
            reasons.append("Entreprise identifiée (+15)")
        
        if data.sector:
            score += weights["has_sector"]
            reasons.append("Secteur renseigné (+10)")
        
        if data.budget:
            score += weights["has_budget"]
            reasons.append("Budget déclaré (+20)")
        
        if data.need_description and len(data.need_description) > 50:
            score += weights["has_need_description"]
            reasons.append("Besoin détaillé (+15)")
        
        # Taille entreprise
        if data.employees_count:
            if data.employees_count > 50:
                score += weights["employees_large"]
                reasons.append("Grande entreprise >50 employés (+15)")
            elif data.employees_count >= 10:
                score += weights["employees_medium"]
                reasons.append("Entreprise moyenne 10-50 employés (+10)")
        
        # Chiffre d'affaires
        if data.annual_revenue and data.annual_revenue > Decimal("100000000"):
            score += weights["high_revenue"]
            reasons.append("CA élevé >100M DZD (+20)")
        
        # Urgence
        if data.urgency and data.urgency.lower() in ["haute", "high", "urgent", "urgente"]:
            score += weights["urgency_high"]
            reasons.append("Urgence déclarée (+15)")
        
        # Source du lead
        if data.source == LeadSource.PME_ANALYZER:
            score += weights["source_pme"]
            reasons.append("Source PME Analyzer (+10)")
        elif data.source == LeadSource.REFERRAL:
            score += weights["source_referral"]
            reasons.append("Recommandation (+15)")
        
        # Plafonner à 100
        score = min(score, 100)
        
        # Calculer la confiance (basée sur la quantité de données)
        data_completeness = sum([
            1 for x in [data.email, data.phone, data.company, data.sector, 
                       data.budget, data.need_description, data.employees_count]
            if x is not None
        ]) / 7
        confidence = round(data_completeness, 2)
        
        # Probabilité de conversion
        probability = round(score / 100 * 0.7 + confidence * 0.3, 2)
        
        # Priorité recommandée
        if score >= 70:
            priority = LeadPriority.HIGH
        elif score >= 40:
            priority = LeadPriority.MEDIUM
        else:
            priority = LeadPriority.LOW
        
        # Prochaine action suggérée
        next_action, next_action_type = self._suggest_initial_action(data, score)
        
        return {
            "score": score,
            "confidence": confidence,
            "probability": probability,
            "reasons": reasons,
            "recommended_priority": priority,
            "next_action": next_action,
            "next_action_type": next_action_type,
        }
    
    def _calculate_score_from_lead(self, lead: LeadPro) -> Dict[str, Any]:
        """Recalculer le score à partir d'un lead existant"""
        data = LeadProCreate(
            name=lead.name,
            email=lead.email,
            phone=lead.phone,
            company=lead.company,
            sector=lead.sector,
            source=lead.source,
            job_title=lead.job_title,
            employees_count=lead.employees_count,
            annual_revenue=lead.annual_revenue,
            country=lead.country,
            city=lead.city,
            wilaya=lead.wilaya,
            need_description=lead.need_description,
            budget=lead.budget,
            urgency=lead.urgency,
        )
        return self._calculate_score(data)
    
    def _determine_status(self, data: LeadProCreate, score: int) -> LeadStatus:
        """
        Déterminer automatiquement le statut selon les règles
        """
        # Règles par score
        if score >= 85:
            return LeadStatus.PROPOSAL
        if score >= 70:
            return LeadStatus.WARM
        if score >= 30:
            return LeadStatus.QUALIFY
        
        # Règles par source
        if data.source == LeadSource.PME_ANALYZER:
            return LeadStatus.QUALIFY
        if data.source == LeadSource.REFERRAL:
            return LeadStatus.WARM
        
        return LeadStatus.NEW
    
    def _suggest_initial_action(
        self, 
        data: LeadProCreate, 
        score: int
    ) -> Tuple[str, ActionType]:
        """Suggérer la première action"""
        
        if score >= 70:
            if data.phone:
                return "Appeler dans les 24h pour qualifier le besoin", ActionType.CALL
            elif data.email:
                return "Envoyer une proposition personnalisée", ActionType.PROPOSAL
            else:
                return "Contacter via WhatsApp pour qualifier", ActionType.WHATSAPP
        
        elif score >= 40:
            if data.source == LeadSource.PME_ANALYZER:
                return "Proposer un audit PME gratuit", ActionType.AUDIT
            elif data.email:
                return "Envoyer un email de présentation", ActionType.EMAIL
            else:
                return "Envoyer un message WhatsApp de prise de contact", ActionType.WHATSAPP
        
        else:
            return "Demander plus d'informations pour qualifier", ActionType.FOLLOW_UP
    
    async def rescore_lead(self, lead_id: str) -> Optional[LeadAIScoreResponse]:
        """
        Recalculer le score d'un lead existant
        """
        lead = leads_db.get(lead_id)
        if not lead:
            return None
        
        result = self._calculate_score_from_lead(lead)
        
        # Mettre à jour le lead
        lead.score = result["score"]
        lead.confidence = result["confidence"]
        lead.score_reasons = result["reasons"]
        lead.probability = result["probability"]
        lead.updated_at = datetime.utcnow()
        
        # Log
        self._log_interaction(
            lead_id=lead_id,
            type=InteractionType.SCORE_UPDATE,
            content=f"Score recalculé: {result['score']}/100",
        )
        
        # Déterminer forces/faiblesses
        strengths = [r for r in result["reasons"] if "+" in r]
        weaknesses = []
        
        if not lead.email:
            weaknesses.append("Email manquant")
        if not lead.phone:
            weaknesses.append("Téléphone manquant")
        if not lead.company:
            weaknesses.append("Entreprise non identifiée")
        if not lead.budget:
            weaknesses.append("Budget non déclaré")
        
        opportunities = []
        if lead.source == LeadSource.PME_ANALYZER:
            opportunities.append("Lead qualifié via PME Analyzer - proposer Pack PME")
        if lead.sector in [Sector.COMMERCE, Sector.SERVICES]:
            opportunities.append("Secteur à fort potentiel pour iaFactory")
        
        return LeadAIScoreResponse(
            score=result["score"],
            confidence=result["confidence"],
            probability=result["probability"],
            reasons=result["reasons"],
            recommended_status=self._determine_status(
                LeadProCreate(name=lead.name, source=lead.source),
                result["score"]
            ),
            recommended_priority=result["recommended_priority"],
            strengths=strengths,
            weaknesses=weaknesses,
            opportunities=opportunities,
        )
    
    # ============================================
    # GÉNÉRATION MESSAGE IA
    # ============================================
    
    async def generate_message(
        self,
        lead_id: str,
        channel: str = "whatsapp",
        message_type: str = "first_contact",
        tone: str = "professional",
        language: str = "fr",
        context: Optional[str] = None,
    ) -> Optional[LeadAIMessageResponse]:
        """
        Générer un message personnalisé avec IA
        """
        lead = leads_db.get(lead_id)
        if not lead:
            return None
        
        # Construire le message selon le template
        message = self._generate_template_message(
            lead=lead,
            channel=channel,
            message_type=message_type,
            tone=tone,
            language=language,
        )
        
        # Alternatives
        alternatives = self._generate_message_alternatives(lead, channel, message_type)
        
        # Conseils
        tips = self._get_sending_tips(lead, channel)
        best_time = self._get_best_sending_time(lead)
        
        # Subject pour email
        subject = None
        if channel == "email":
            subject = self._generate_email_subject(lead, message_type)
        
        return LeadAIMessageResponse(
            message=message,
            subject=subject,
            channel=channel,
            message_type=message_type,
            alternatives=alternatives,
            best_time=best_time,
            tips=tips,
        )
    
    def _generate_template_message(
        self,
        lead: LeadPro,
        channel: str,
        message_type: str,
        tone: str,
        language: str,
    ) -> str:
        """Générer message selon template"""
        
        name = lead.name.split()[0] if lead.name else "Bonjour"
        company = lead.company or "votre entreprise"
        sector_label = lead.sector.value if lead.sector else "votre secteur"
        
        if message_type == "first_contact":
            if channel == "whatsapp":
                return f"""Bonjour {name} 👋

Je suis de iaFactoryDZ. J'ai vu que vous avez exprimé un intérêt pour nos solutions IA.

Nous accompagnons les PME algériennes dans leur transformation digitale avec des outils simples et puissants.

Auriez-vous 10 minutes pour un appel cette semaine ? Je pourrais vous montrer comment nous pouvons aider {company}.

À bientôt ! 🚀"""
            
            elif channel == "email":
                return f"""Bonjour {name},

Merci pour votre intérêt envers iaFactoryDZ.

Nous sommes spécialisés dans les solutions IA pour les PME, avec un focus particulier sur le marché algérien.

Nos outils permettent de :
• Analyser automatiquement vos documents (factures, contrats, rapports)
• Gérer votre base clients avec un CRM intelligent
• Automatiser vos processus administratifs

Seriez-vous disponible pour un appel de découverte de 15 minutes cette semaine ?

Cordialement,
L'équipe iaFactoryDZ"""
        
        elif message_type == "follow_up":
            return f"""Bonjour {name} 👋

Je me permets de revenir vers vous concernant votre demande sur iaFactoryDZ.

Avez-vous eu le temps de réfléchir à nos solutions pour {company} ?

Je reste disponible pour répondre à vos questions.

Bonne journée ! 🙂"""
        
        elif message_type == "proposal":
            return f"""Bonjour {name},

Suite à notre échange, voici ma proposition pour {company} :

📦 Pack PME iaFactory - 14 900 DA/mois
• Analyse de documents IA illimitée
• CRM intelligent avec scoring
• Support prioritaire
• Formation incluse

Cette offre est valable 7 jours.

Souhaitez-vous qu'on en discute ?

À bientôt ! 🚀"""
        
        elif message_type == "thank_you":
            return f"""Bonjour {name} 🙏

Merci d'avoir choisi iaFactoryDZ !

Nous sommes ravis de vous compter parmi nos clients.

Notre équipe est à votre disposition pour vous accompagner dans la prise en main de nos outils.

À très bientôt !
L'équipe iaFactory 🚀"""
        
        return f"Bonjour {name}, merci de votre intérêt pour iaFactoryDZ."
    
    def _generate_message_alternatives(
        self, 
        lead: LeadPro, 
        channel: str,
        message_type: str,
    ) -> List[str]:
        """Générer des alternatives de message"""
        name = lead.name.split()[0] if lead.name else "Bonjour"
        
        if message_type == "first_contact" and channel == "whatsapp":
            return [
                f"Salam {name} ! 🇩🇿 iaFactoryDZ ici. On aide les PME algériennes à digitaliser leurs process. Un café virtuel pour en parler ?",
                f"Bonjour {name}, je suis ravi de votre intérêt pour iaFactory. Puis-je vous appeler rapidement pour mieux comprendre vos besoins ?",
            ]
        return []
    
    def _generate_email_subject(self, lead: LeadPro, message_type: str) -> str:
        """Générer un objet d'email"""
        name = lead.name.split()[0] if lead.name else ""
        company = lead.company or "votre entreprise"
        
        subjects = {
            "first_contact": f"🚀 {name}, découvrez iaFactoryDZ pour {company}",
            "follow_up": f"📌 {name}, un suivi de votre demande",
            "proposal": f"📦 Proposition iaFactory pour {company}",
            "thank_you": f"🙏 Bienvenue chez iaFactoryDZ !",
        }
        return subjects.get(message_type, f"Message de iaFactoryDZ")
    
    def _get_sending_tips(self, lead: LeadPro, channel: str) -> List[str]:
        """Conseils d'envoi"""
        tips = []
        
        if channel == "whatsapp":
            tips.append("Envoyez entre 9h-12h ou 14h-17h pour un meilleur taux de réponse")
            tips.append("Évitez le vendredi après-midi")
        elif channel == "email":
            tips.append("Mardi et mercredi ont les meilleurs taux d'ouverture")
            tips.append("Envoyez avant 10h du matin")
        
        if lead.sector == Sector.COMMERCE:
            tips.append("Les commerçants sont plus disponibles en début de semaine")
        
        return tips
    
    def _get_best_sending_time(self, lead: LeadPro) -> str:
        """Meilleur moment pour envoyer"""
        now = datetime.utcnow()
        
        # Mardi ou mercredi à 9h
        days_until_tuesday = (1 - now.weekday()) % 7
        if days_until_tuesday == 0 and now.hour >= 9:
            days_until_tuesday = 7
        
        best_date = now + timedelta(days=days_until_tuesday)
        best_date = best_date.replace(hour=9, minute=0, second=0, microsecond=0)
        
        return best_date.strftime("%A %d %B à 9h00")
    
    # ============================================
    # SUGGESTION PROCHAINE ACTION
    # ============================================
    
    async def suggest_next_action(
        self,
        lead_id: str,
        context: Optional[str] = None,
    ) -> Optional[LeadAINextActionResponse]:
        """
        Suggérer la prochaine action pour un lead
        """
        lead = leads_db.get(lead_id)
        if not lead:
            return None
        
        # Logique de suggestion
        action, action_type, priority, reason = self._determine_next_action(lead)
        
        # Générer un script/guide
        script = self._generate_action_script(lead, action_type)
        
        # Alternatives
        alternatives = self._get_alternative_actions(lead)
        
        # Dates suggérées
        suggested_date = datetime.utcnow() + timedelta(hours=24)
        deadline = datetime.utcnow() + timedelta(days=3)
        
        return LeadAINextActionResponse(
            action=action,
            action_type=action_type,
            priority=priority,
            reason=reason,
            suggested_date=suggested_date,
            deadline=deadline,
            alternatives=alternatives,
            script=script,
        )
    
    def _determine_next_action(
        self, 
        lead: LeadPro
    ) -> Tuple[str, ActionType, LeadPriority, str]:
        """Déterminer la prochaine action selon le contexte"""
        
        # Lead chaud avec score élevé
        if lead.status == LeadStatus.WARM and lead.score >= 70:
            if lead.phone:
                return (
                    "Appeler pour proposer un rendez-vous de présentation",
                    ActionType.CALL,
                    LeadPriority.HIGH,
                    "Lead chaud avec score élevé - conversion potentielle imminente"
                )
            else:
                return (
                    "Envoyer une proposition commerciale par email",
                    ActionType.PROPOSAL,
                    LeadPriority.HIGH,
                    "Lead qualifié prêt pour une offre"
                )
        
        # Lead à qualifier
        if lead.status == LeadStatus.QUALIFY:
            if lead.source == LeadSource.PME_ANALYZER:
                return (
                    "Proposer un audit PME gratuit pour qualifier le besoin",
                    ActionType.AUDIT,
                    LeadPriority.MEDIUM,
                    "Lead venu de PME Analyzer - intérêt confirmé pour l'analyse"
                )
            else:
                return (
                    "Envoyer un message WhatsApp pour comprendre le besoin",
                    ActionType.WHATSAPP,
                    LeadPriority.MEDIUM,
                    "Besoin de qualifier le lead avant de proposer"
                )
        
        # Nouveau lead
        if lead.status == LeadStatus.NEW:
            return (
                "Premier contact pour se présenter et découvrir le besoin",
                ActionType.WHATSAPP if lead.phone else ActionType.EMAIL,
                LeadPriority.MEDIUM,
                "Nouveau lead à contacter rapidement"
            )
        
        # Lead en proposition
        if lead.status == LeadStatus.PROPOSAL:
            return (
                "Relancer pour connaître la décision",
                ActionType.FOLLOW_UP,
                LeadPriority.HIGH,
                "Proposition envoyée - besoin de suivi"
            )
        
        # Défaut
        return (
            "Analyser le dossier et définir la stratégie",
            ActionType.FOLLOW_UP,
            LeadPriority.LOW,
            "Lead à analyser"
        )
    
    def _generate_action_script(self, lead: LeadPro, action_type: ActionType) -> str:
        """Générer un script/guide pour l'action"""
        name = lead.name.split()[0] if lead.name else "le prospect"
        company = lead.company or "son entreprise"
        
        scripts = {
            ActionType.CALL: f"""📞 SCRIPT APPEL - {name}

1. INTRODUCTION (30s)
   "Bonjour {name}, c'est [Prénom] de iaFactoryDZ. 
   Je vous appelle suite à votre intérêt pour nos solutions IA."

2. DÉCOUVERTE (2min)
   - "Pouvez-vous me parler de {company} ?"
   - "Quels sont vos défis actuels en termes de gestion ?"
   - "Utilisez-vous des outils digitaux actuellement ?"

3. PITCH (1min)
   "iaFactory aide les PME algériennes à automatiser leur gestion 
   avec des outils IA simples. Par exemple, [cas d'usage adapté]."

4. CLOSE (30s)
   "Seriez-vous disponible pour une démo de 20 minutes cette semaine ?"

📌 OBJECTIONS COURANTES:
- "C'est cher" → "On a des formules à partir de 4900 DA/mois"
- "Je n'ai pas le temps" → "Justement, notre outil vous fait gagner du temps"
""",
            ActionType.WHATSAPP: f"""💬 MESSAGE WHATSAPP - {name}

Bonjour {name} 👋

Je suis [Prénom] de iaFactoryDZ.

J'ai vu votre intérêt pour nos solutions et je voulais savoir si vous aviez 5 minutes pour qu'on échange sur vos besoins ?

On aide les PME comme {company} à digitaliser leurs process avec l'IA. 🚀

Quel serait le meilleur moment pour vous ?
""",
            ActionType.AUDIT: f"""📊 PROPOSITION AUDIT PME - {name}

Sujet: Audit PME Gratuit pour {company}

Bonjour {name},

Dans le cadre de notre programme d'accompagnement des PME algériennes, nous vous proposons un audit gratuit de 30 minutes.

Ce diagnostic comprend:
✅ Analyse de vos process actuels
✅ Identification des opportunités d'automatisation  
✅ Recommandations personnalisées
✅ Estimation du ROI potentiel

Sans engagement de votre part.

Quand seriez-vous disponible ?
""",
        }
        
        return scripts.get(action_type, f"Contacter {name} pour {action_type.value}")
    
    def _get_alternative_actions(self, lead: LeadPro) -> List[Dict[str, Any]]:
        """Actions alternatives"""
        alternatives = []
        
        if lead.email:
            alternatives.append({
                "action": "Envoyer un email de présentation",
                "type": ActionType.EMAIL.value,
                "priority": "medium",
            })
        
        if lead.phone:
            alternatives.append({
                "action": "Programmer un appel de 10 minutes",
                "type": ActionType.CALL.value,
                "priority": "high",
            })
        
        alternatives.append({
            "action": "Ajouter une note et attendre",
            "type": ActionType.FOLLOW_UP.value,
            "priority": "low",
        })
        
        return alternatives[:3]
    
    # ============================================
    # INTERACTIONS
    # ============================================
    
    def _log_interaction(
        self,
        lead_id: str,
        type: InteractionType,
        content: str,
        user_id: Optional[str] = None,
        metadata: Optional[Dict] = None,
    ) -> Interaction:
        """Logger une interaction"""
        interaction = Interaction(
            id=f"int_{uuid.uuid4().hex[:12]}",
            lead_id=lead_id,
            type=type,
            content=content,
            user_id=user_id,
            metadata=metadata or {},
            created_at=datetime.utcnow(),
        )
        interactions_db.append(interaction)
        
        # Mettre à jour le lead
        lead = leads_db.get(lead_id)
        if lead:
            lead.interactions_count += 1
            lead.last_interaction = datetime.utcnow()
        
        return interaction
    
    def add_interaction(
        self,
        lead_id: str,
        type: InteractionType,
        content: str,
        user_id: Optional[str] = None,
        metadata: Optional[Dict] = None,
    ) -> Optional[Interaction]:
        """Ajouter une interaction manuellement"""
        if lead_id not in leads_db:
            return None
        return self._log_interaction(lead_id, type, content, user_id, metadata)
    
    def get_interactions(
        self, 
        lead_id: str,
        limit: int = 50,
    ) -> List[Interaction]:
        """Récupérer les interactions d'un lead"""
        return sorted(
            [i for i in interactions_db if i.lead_id == lead_id],
            key=lambda x: x.created_at,
            reverse=True,
        )[:limit]
    
    # ============================================
    # PIPELINE / KANBAN
    # ============================================
    
    def get_pipeline_view(self) -> PipelineView:
        """Vue Kanban du pipeline"""
        columns = []
        total_value = Decimal("0")
        
        for status in LeadStatus:
            leads_in_status = [l for l in leads_db.values() if l.status == status]
            status_value = sum(
                l.estimated_value or Decimal("0") 
                for l in leads_in_status
            )
            
            columns.append(PipelineColumn(
                status=status,
                name=STATUS_NAMES.get(status, status.value),
                color=STATUS_COLORS.get(status, "#666"),
                count=len(leads_in_status),
                total_value=status_value,
            ))
            
            if status not in [LeadStatus.WON, LeadStatus.LOST]:
                total_value += status_value
        
        total_leads = len(leads_db)
        won_count = len([l for l in leads_db.values() if l.status == LeadStatus.WON])
        closed_count = len([l for l in leads_db.values() if l.status in [LeadStatus.WON, LeadStatus.LOST]])
        
        conversion_rate = (won_count / closed_count * 100) if closed_count > 0 else 0.0
        
        return PipelineView(
            columns=columns,
            total_leads=total_leads,
            total_value=total_value,
            conversion_rate=round(conversion_rate, 1),
        )
    
    def move_lead_in_pipeline(
        self, 
        lead_id: str, 
        new_status: LeadStatus,
        user_id: Optional[str] = None,
    ) -> Optional[LeadPro]:
        """Déplacer un lead dans le pipeline"""
        lead = leads_db.get(lead_id)
        if not lead:
            return None
        
        old_status = lead.status
        lead.status = new_status
        lead.updated_at = datetime.utcnow()
        
        # Log
        self._log_interaction(
            lead_id=lead_id,
            type=InteractionType.STATUS_CHANGE,
            content=f"Pipeline: {STATUS_NAMES.get(old_status)} → {STATUS_NAMES.get(new_status)}",
            user_id=user_id,
        )
        
        return lead
    
    # ============================================
    # STATISTIQUES
    # ============================================
    
    def get_stats(self) -> CRMStats:
        """Statistiques globales du CRM"""
        now = datetime.utcnow()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        week_start = now - timedelta(days=now.weekday())
        week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
        
        leads = list(leads_db.values())
        
        # Compteurs
        total_leads = len(leads)
        leads_this_month = len([l for l in leads if l.created_at >= month_start])
        leads_this_week = len([l for l in leads if l.created_at >= week_start])
        
        # Par statut
        by_status = {}
        for status in LeadStatus:
            by_status[status.value] = len([l for l in leads if l.status == status])
        
        # Par source
        by_source = {}
        for source in LeadSource:
            count = len([l for l in leads if l.source == source])
            if count > 0:
                by_source[source.value] = count
        
        # Par secteur
        by_sector = {}
        for sector in Sector:
            count = len([l for l in leads if l.sector == sector])
            if count > 0:
                by_sector[sector.value] = count
        
        # Conversion
        won = len([l for l in leads if l.status == LeadStatus.WON])
        closed = len([l for l in leads if l.status in [LeadStatus.WON, LeadStatus.LOST]])
        conversion_rate = (won / closed * 100) if closed > 0 else 0.0
        
        # Score moyen
        avg_score = sum(l.score for l in leads) / total_leads if total_leads > 0 else 0.0
        
        # Valeurs
        pipeline_value = sum(
            l.estimated_value or Decimal("0") 
            for l in leads 
            if l.status not in [LeadStatus.WON, LeadStatus.LOST]
        )
        won_value = sum(
            l.estimated_value or Decimal("0")
            for l in leads
            if l.status == LeadStatus.WON
        )
        
        # Leads chauds
        hot_leads = len([l for l in leads if l.score >= 70])
        
        return CRMStats(
            total_leads=total_leads,
            leads_this_month=leads_this_month,
            leads_this_week=leads_this_week,
            by_status=by_status,
            by_source=by_source,
            by_sector=by_sector,
            conversion_rate=round(conversion_rate, 1),
            avg_score=round(avg_score, 1),
            total_pipeline_value=pipeline_value,
            total_won_value=won_value,
            hot_leads_count=hot_leads,
        )


# ============================================
# SINGLETON
# ============================================

crm_pro_service = CRMProService()
