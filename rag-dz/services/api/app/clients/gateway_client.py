"""
Gateway Client pour iafactory-gateway
Remplace les services billing/credits locaux
"""
import httpx
from typing import Optional

class GatewayClient:
    def __init__(self, base_url: str = "http://localhost:3001"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def get_user_credits(self, user_id: str) -> int:
        """Recupere le solde de credits d un utilisateur"""
        response = await self.client.get(f"{self.base_url}/api/credits/{user_id}")
        response.raise_for_status()
        return response.json()["balance"]
    
    async def consume_credits(self, user_id: str, amount: int, reason: str) -> dict:
        """Consomme des credits"""
        response = await self.client.post(
            f"{self.base_url}/api/credits/consume",
            json={"user_id": user_id, "amount": amount, "reason": reason}
        )
        response.raise_for_status()
        return response.json()
    
    async def add_credits(self, user_id: str, amount: int, reason: str) -> dict:
        """Ajoute des credits"""
        response = await self.client.post(
            f"{self.base_url}/api/credits/add",
            json={"user_id": user_id, "amount": amount, "reason": reason}
        )
        response.raise_for_status()
        return response.json()
    
    async def call_llm(self, provider: str, model: str, messages: list, user_id: str) -> dict:
        """Appel LLM via gateway (facturation automatique)"""
        response = await self.client.post(
            f"{self.base_url}/api/llm/chat",
            json={
                "provider": provider,
                "model": model,
                "messages": messages,
                "user_id": user_id
            }
        )
        response.raise_for_status()
        return response.json()

gateway = GatewayClient()
