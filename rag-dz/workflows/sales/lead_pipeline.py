from datetime import datetime
from typing import Dict, List

class LeadPipeline:
    CONTACTS = {
        "CH": "contact@iafactory.ch",
        "DZ": "contact@iafactoryalgeria.com"
    }
    
    def __init__(self):
        self.leads: List[Dict] = []
    
    def add_lead(self, lead: Dict) -> Dict:
        lead_id = f"LEAD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        score = self.score_lead(lead)
        
        entry = {
            "id": lead_id,
            "name": lead.get("name"),
            "company": lead.get("company"),
            "email": lead.get("email"),
            "market": lead.get("market", "CH"),
            "score": score,
            "status": "HOT" if score >= 70 else "WARM" if score >= 40 else "COLD",
            "created": datetime.now().isoformat(),
            "contact": self.CONTACTS[lead.get("market", "CH")]
        }
        
        self.leads.append(entry)
        return entry
    
    def score_lead(self, lead: Dict) -> int:
        score = 50
        
        if lead.get("budget"):
            score += 20
        if lead.get("timeline") in ["immediate", "1-3 months"]:
            score += 15
        if lead.get("company_size", 0) > 50:
            score += 10
        if lead.get("source") == "referral":
            score += 15
        
        return min(score, 100)
    
    def get_hot_leads(self) -> List[Dict]:
        return [l for l in self.leads if l["status"] == "HOT"]
    
    def get_by_market(self, market: str) -> List[Dict]:
        return [l for l in self.leads if l["market"] == market]

if __name__ == "__main__":
    pipeline = LeadPipeline()
    
    lead1 = pipeline.add_lead({
        "name": "Jean Dupont",
        "company": "Swiss Corp",
        "email": "jean@swiss.ch",
        "market": "CH",
        "budget": "25000 CHF",
        "timeline": "immediate"
    })
    print(f"Lead CH: {lead1}")
    
    lead2 = pipeline.add_lead({
        "name": "Ahmed Benali",
        "company": "Algérie Télécom",
        "email": "ahmed@at.dz",
        "market": "DZ",
        "budget": "1000000 DZD"
    })
    print(f"Lead DZ: {lead2}")
