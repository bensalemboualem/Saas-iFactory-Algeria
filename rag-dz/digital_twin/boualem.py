"""
Digital Twin de Boualem - Génère du contenu authentique
"""

from typing import Dict
from datetime import datetime

class BoualemTwin:
    """Clone IA de Boualem pour génération de contenu"""
    
    STYLE = {
        "tone": "professionnel mais accessible",
        "values": ["innovation", "souveraineté", "accessibilité"],
        "signature_ch": "Boualem Chebaki\nIA Factory\ncontact@iafactory.ch",
        "signature_dz": "Boualem Chebaki\nIA Factory Algeria\ncontact@iafactoryalgeria.com"
    }
    
    def generate_email(self, context: Dict, market: str = "CH") -> Dict:
        signature = self.STYLE["signature_ch"] if market == "CH" else self.STYLE["signature_dz"]
        
        return {
            "subject": f"Re: {context.get('topic', 'Votre projet IA')}",
            "body": f"""Bonjour {context.get('name', '')},

Merci pour votre intérêt pour IA Factory.

{context.get('message', 'Je serais ravi de discuter de votre projet.')}

N'hésitez pas à me contacter pour en discuter.

Cordialement,

{signature}""",
            "generated_at": datetime.now().isoformat()
        }
    
    def generate_proposal_intro(self, client: Dict, market: str = "CH") -> str:
        return f"""Suite à nos échanges, j'ai le plaisir de vous présenter notre proposition pour {client.get('company', 'votre entreprise')}.

Chez IA Factory, notre mission est de rendre l'IA accessible à tous. Nous avons développé des solutions concrètes qui génèrent des résultats mesurables.

Cette proposition détaille comment nous pouvons vous accompagner."""
