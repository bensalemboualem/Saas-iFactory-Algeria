"""
Auth Client pour iafactory-gateway
Centralise JWT et auth via le gateway
"""
import httpx
from typing import Optional, Dict

class AuthClient:
    def __init__(self, gateway_url: str = "http://localhost:3001"):
        self.gateway_url = gateway_url
        self.client = httpx.AsyncClient(timeout=10.0)
    
    async def verify_jwt(self, token: str) -> Optional[Dict]:
        """Verifie un JWT via le gateway"""
        try:
            response = await self.client.get(
                f"{self.gateway_url}/api/auth/verify",
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError:
            return None
    
    async def generate_jwt(self, user_id: str, expires_in: str = "7d") -> str:
        """Genere un JWT via le gateway"""
        response = await self.client.post(
            f"{self.gateway_url}/api/auth/token",
            json={"userId": user_id, "expiresIn": expires_in}
        )
        response.raise_for_status()
        return response.json()["token"]
    
    async def get_current_user(self, token: str) -> Optional[Dict]:
        """Recupere user depuis JWT"""
        user_data = await self.verify_jwt(token)
        return user_data.get("user") if user_data else None

auth_client = AuthClient()
