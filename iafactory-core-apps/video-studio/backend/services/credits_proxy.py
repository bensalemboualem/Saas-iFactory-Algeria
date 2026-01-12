"""
IAFactory Video Studio Pro - Credits Proxy
Proxy vers le système de crédits centralisé de l'API principale

Ce service :
1. Vérifie les crédits via l'API IAFactory principale
2. Déduit les crédits pour chaque génération vidéo
3. Gère les erreurs 402 (crédits insuffisants)
"""

import os
import logging
from typing import Dict, Any, Optional
import httpx
from fastapi import HTTPException

logger = logging.getLogger(__name__)

# Configuration
IAFACTORY_API_URL = os.getenv("IAFACTORY_API_URL", "http://localhost:8000")
IAFACTORY_API_KEY = os.getenv("IAFACTORY_API_KEY", "")


class CreditsProxy:
    """
    Proxy pour le système de crédits IAFactory.

    Appelle l'API principale pour :
    - Vérifier le solde
    - Déduire les crédits
    - Calculer les coûts dynamiques
    """

    def __init__(self):
        self.api_url = IAFACTORY_API_URL
        self.api_key = IAFACTORY_API_KEY
        self._client = None

    @property
    def client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.api_url,
                timeout=30.0,
                headers={"X-API-Key": self.api_key} if self.api_key else {}
            )
        return self._client

    async def close(self):
        """Ferme le client HTTP."""
        if self._client:
            await self._client.aclose()
            self._client = None

    # ═══════════════════════════════════════════════════════════════════
    # BALANCE OPERATIONS
    # ═══════════════════════════════════════════════════════════════════

    async def get_balance(self, tenant_id: str, token: str = "") -> Dict[str, Any]:
        """
        Récupère le solde de crédits depuis l'API principale.

        Args:
            tenant_id: ID du tenant (utilisateur)
            token: JWT token pour l'authentification

        Returns:
            {"remaining": int, "total": int, "percentage_used": float, "plan": str}
        """
        try:
            headers = {}
            if token:
                headers["Authorization"] = f"Bearer {token}"

            response = await self.client.get(
                f"/api/credits/balance",
                headers=headers,
                params={"tenant_id": tenant_id}
            )

            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get balance: {response.status_code} - {response.text}")
                return {"remaining": 0, "total": 0, "percentage_used": 100, "plan": "free"}

        except Exception as e:
            logger.error(f"Error getting balance: {e}")
            return {"remaining": 0, "total": 0, "percentage_used": 100, "plan": "free"}

    async def check_credits(
        self,
        tenant_id: str,
        service: str,
        token: str = ""
    ) -> Dict[str, Any]:
        """
        Vérifie si l'utilisateur a assez de crédits pour un service.

        Args:
            tenant_id: ID du tenant
            service: Nom du service (ex: 'kling-ai', 'minimax-video')
            token: JWT token

        Returns:
            {"can_afford": bool, "cost": int, "remaining": int}
        """
        try:
            headers = {}
            if token:
                headers["Authorization"] = f"Bearer {token}"

            response = await self.client.get(
                f"/api/credits/check/{service}",
                headers=headers,
                params={"tenant_id": tenant_id}
            )

            if response.status_code == 200:
                return response.json()
            else:
                return {"can_afford": False, "cost": 0, "remaining": 0}

        except Exception as e:
            logger.error(f"Error checking credits: {e}")
            return {"can_afford": False, "cost": 0, "remaining": 0}

    # ═══════════════════════════════════════════════════════════════════
    # USAGE OPERATIONS
    # ═══════════════════════════════════════════════════════════════════

    async def deduct_credits(
        self,
        tenant_id: str,
        service: str,
        token: str = "",
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Déduit les crédits pour un service utilisé.

        Args:
            tenant_id: ID du tenant
            service: Nom du service (ex: 'kling-ai', 'sora-2')
            token: JWT token
            metadata: Données additionnelles (duration, resolution, etc.)

        Returns:
            {"deducted": int, "remaining": int, "service": str}

        Raises:
            HTTPException 402: Si crédits insuffisants
        """
        try:
            headers = {}
            if token:
                headers["Authorization"] = f"Bearer {token}"

            response = await self.client.post(
                f"/api/credits/use/{service}",
                headers=headers,
                json={
                    "tenant_id": tenant_id,
                    "metadata": metadata or {}
                }
            )

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 402:
                # Crédits insuffisants
                data = response.json()
                raise HTTPException(
                    status_code=402,
                    detail={
                        "error": "insufficient_credits",
                        "required": data.get("detail", {}).get("required", 0),
                        "remaining": data.get("detail", {}).get("remaining", 0),
                        "service": service,
                        "message": "Crédits insuffisants pour cette génération vidéo",
                        "upgrade_url": "/pricing"
                    }
                )
            else:
                logger.error(f"Failed to deduct credits: {response.status_code} - {response.text}")
                raise HTTPException(
                    status_code=500,
                    detail="Erreur lors de la déduction des crédits"
                )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error deducting credits: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Erreur système: {str(e)}"
            )

    async def get_dynamic_cost(
        self,
        service: str,
        duration_seconds: int = 5,
        resolution: str = "720p",
        token: str = ""
    ) -> int:
        """
        Calcule le coût dynamique basé sur durée et résolution.

        Args:
            service: Nom du service vidéo
            duration_seconds: Durée de la vidéo
            resolution: Résolution (480p, 720p, 1080p, 4k)
            token: JWT token

        Returns:
            Coût en crédits
        """
        try:
            response = await self.client.post(
                f"/api/credits/cost/dynamic",
                json={
                    "service": service,
                    "params": {
                        "duration_seconds": duration_seconds,
                        "resolution": resolution
                    }
                }
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("cost", 0)
            else:
                # Fallback: utiliser les coûts par défaut
                return self._get_fallback_cost(service, duration_seconds, resolution)

        except Exception as e:
            logger.warning(f"Error getting dynamic cost, using fallback: {e}")
            return self._get_fallback_cost(service, duration_seconds, resolution)

    def _get_fallback_cost(
        self,
        service: str,
        duration_seconds: int,
        resolution: str
    ) -> int:
        """Coûts de fallback si l'API n'est pas accessible."""
        base_costs = {
            "kling-ai": 2000,
            "kling-standard": 800,
            "runway-gen4": 900,
            "runway-video": 800,
            "runway-gen3": 700,
            "sora-2": 600,
            "veo-3": 700,
            "lumalabs-ray2": 600,
            "lumalabs": 500,
            "luma-video": 500,
            "hailuo": 450,
            "minimax-video": 400,
            "seadance": 400,
            "pika-labs": 350,
        }

        base = base_costs.get(service.lower(), 500)

        # Multiplicateur durée (base = 5 secondes)
        duration_mult = duration_seconds / 5.0

        # Multiplicateur résolution
        res_mult = {
            "480p": 0.7,
            "720p": 1.0,
            "1080p": 1.5,
            "4k": 2.5,
            "2160p": 2.5
        }.get(resolution, 1.0)

        return int(round(base * duration_mult * res_mult))

    # ═══════════════════════════════════════════════════════════════════
    # PLAN VERIFICATION
    # ═══════════════════════════════════════════════════════════════════

    async def check_plan_feature(
        self,
        tenant_id: str,
        feature: str,
        token: str = ""
    ) -> bool:
        """
        Vérifie si le plan du tenant inclut une fonctionnalité.

        Args:
            tenant_id: ID du tenant
            feature: Nom de la feature ('video', 'image', 'deep_agent')
            token: JWT token

        Returns:
            True si la feature est disponible
        """
        try:
            headers = {}
            if token:
                headers["Authorization"] = f"Bearer {token}"

            response = await self.client.get(
                f"/api/credits/plan/feature/{feature}",
                headers=headers,
                params={"tenant_id": tenant_id}
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("has_feature", False)
            else:
                return False

        except Exception as e:
            logger.error(f"Error checking plan feature: {e}")
            return False

    async def require_video_plan(self, tenant_id: str, token: str = ""):
        """
        Vérifie que le tenant a un plan Pro+ pour la vidéo.

        Raises:
            HTTPException 403: Si le plan ne permet pas la vidéo
        """
        has_video = await self.check_plan_feature(tenant_id, "video", token)

        if not has_video:
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "plan_upgrade_required",
                    "message": "La génération vidéo nécessite un plan Pro ou Enterprise",
                    "required_plan": "pro",
                    "upgrade_url": "/pricing"
                }
            )


# Instance globale
credits_proxy = CreditsProxy()
