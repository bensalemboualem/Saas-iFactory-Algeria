class EmailTemplates:
    CONTACTS = {"CH": "contact@iafactory.ch", "DZ": "contact@iafactoryalgeria.com"}
    
    @staticmethod
    def welcome(client, market, url):
        return {"to": client["email"], "subject": f"Bienvenue {client['company']}!", 
                "body": f"Votre accès: {url}\nContact: {EmailTemplates.CONTACTS[market]}"}
    
    @staticmethod
    def hot_lead(lead, score):
        return {"to": "contact@iafactory.ch", "subject": f"HOT LEAD ({score}): {lead['company']}",
                "body": f"{lead['name']} - {lead['email']}"}
