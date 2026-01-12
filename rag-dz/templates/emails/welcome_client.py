"""
IA FACTORY - Templates Emails
Emails automatisés pour le workflow client
"""

from datetime import datetime
from typing import Dict

class EmailTemplates:
    
    @staticmethod
    def welcome_email(client: Dict, access_url: str) -> Dict:
        """Email de bienvenue nouveau client"""
        
        subject = f"🎉 Bienvenue chez IA Factory, {client['company']}!"
        
        body = f"""
Bonjour {client['name']},

Votre plateforme IA Factory est maintenant active ! 🚀

═══════════════════════════════════════════════════════
ACCÈS À VOTRE ESPACE
═══════════════════════════════════════════════════════

🔗 URL: {access_url}
👤 Identifiant: {client['email']}
🔑 Mot de passe: (envoyé séparément)

═══════════════════════════════════════════════════════
PROCHAINES ÉTAPES
═══════════════════════════════════════════════════════

1️⃣ Connectez-vous et explorez l'interface
2️⃣ Uploadez vos premiers documents
3️⃣ Testez une recherche IA
4️⃣ Invitez vos collègues

═══════════════════════════════════════════════════════
VOTRE FORMATION
═══════════════════════════════════════════════════════

Une session de formation est prévue prochainement.
Vous recevrez une invitation calendrier séparée.

═══════════════════════════════════════════════════════
SUPPORT
═══════════════════════════════════════════════════════

📧 Email: support@iafactory.ch
📞 Téléphone: +41 XX XXX XX XX
📚 Documentation: docs.iafactory.ch

Notre équipe est disponible du lundi au vendredi, 9h-18h.

À très bientôt!

--
Boualem Chebaki
Fondateur, IA Factory
www.iafactory.ch

P.S. N'hésitez pas à répondre à cet email si vous avez la moindre question!
"""
        
        return {
            "to": client['email'],
            "subject": subject,
            "body": body,
            "html": EmailTemplates._to_html(body)
        }
    
    @staticmethod
    def proposal_followup(client: Dict, days_since: int = 3) -> Dict:
        """Email follow-up après envoi proposition"""
        
        subject = f"Suite à notre proposition - {client['company']}"
        
        body = f"""
Bonjour {client['name']},

Je me permets de revenir vers vous suite à la proposition que je vous ai envoyée il y a {days_since} jours.

Avez-vous eu l'occasion de la consulter?

Je reste disponible pour:
• Répondre à vos questions
• Clarifier certains points
• Organiser une démo complémentaire
• Discuter des conditions

N'hésitez pas à me contacter directement.

Cordialement,

--
Boualem Chebaki
IA Factory
+41 XX XXX XX XX
"""
        
        return {
            "to": client['email'],
            "subject": subject,
            "body": body
        }
    
    @staticmethod
    def hot_lead_alert(lead: Dict, score: int) -> Dict:
        """Alerte interne pour lead chaud"""
        
        subject = f"🔥 HOT LEAD ({score}/100): {lead['company']}"
        
        body = f"""
NOUVEAU LEAD CHAUD DÉTECTÉ!

═══════════════════════════════════════════════════════
INFORMATIONS LEAD
═══════════════════════════════════════════════════════

👤 Nom: {lead['name']}
🏢 Entreprise: {lead['company']}
📧 Email: {lead['email']}
📞 Téléphone: {lead.get('phone', 'N/A')}

═══════════════════════════════════════════════════════
QUALIFICATION
═══════════════════════════════════════════════════════

📊 Score: {score}/100
🎯 Besoin: {lead.get('need', 'Non spécifié')}
💰 Budget: {lead.get('budget', 'Non spécifié')}
⏰ Timeline: {lead.get('timeline', 'Non spécifié')}
📍 Source: {lead.get('source', 'Website')}

═══════════════════════════════════════════════════════
ACTION REQUISE
═══════════════════════════════════════════════════════

⚡ Contacter dans les 5 minutes!
📞 Appeler ou envoyer email personnalisé

Timestamp: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
"""
        
        return {
            "to": "boualem@iafactory.ch",
            "subject": subject,
            "body": body,
            "priority": "high"
        }
    
    @staticmethod
    def _to_html(text: str) -> str:
        """Convertit texte simple en HTML basique"""
        html = text.replace('\n', '<br>')
        html = html.replace('═', '─')
        return f"<html><body style='font-family: Arial, sans-serif;'>{html}</body></html>"
