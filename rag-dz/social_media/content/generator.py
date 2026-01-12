from datetime import datetime
from typing import Dict, List

class ContentGenerator:
    """Génère du contenu pour réseaux sociaux"""
    
    CONTACTS = {
        "CH": {"email": "contact@iafactory.ch", "hashtags": "#IAFactory #SwissAI #GenAI"},
        "DZ": {"email": "contact@iafactoryalgeria.com", "hashtags": "#IAFactory #AlgeriaAI #GenAI"}
    }
    
    def generate_linkedin_post(self, topic: str, market: str = "CH") -> Dict:
        contact = self.CONTACTS[market]
        
        templates = {
            "rag": f"""🚀 Comment l'IA transforme la recherche documentaire?

Notre système RAG permet de:
✅ Rechercher dans vos documents en langage naturel
✅ Obtenir des réponses précises avec sources
✅ Gagner 70% de temps

Intéressé? Contactez-nous: {contact['email']}

{contact['hashtags']}""",

            "teaching": f"""🎓 L'IA au service des enseignants

Notre AI Teaching Assistant:
📚 Génère des exercices adaptés
✍️ Corrige automatiquement
📊 Suit la progression

Résultat: 70% de temps gagné!

{contact['email']}
{contact['hashtags']}""",

            "general": f"""🏭 IA Factory - AI for All

Solutions IA sur mesure pour votre entreprise.

💡 RAG Systems
🤖 Multi-Agents
📊 Analytics IA

{contact['email']}
{contact['hashtags']}"""
        }
        
        content = templates.get(topic, templates["general"])
        
        return {
            "platform": "linkedin",
            "content": content,
            "market": market,
            "created": datetime.now().isoformat()
        }
    
    def generate_week_content(self, market: str = "CH") -> List[Dict]:
        topics = ["rag", "teaching", "general", "rag", "teaching"]
        return [self.generate_linkedin_post(t, market) for t in topics]
