"""
FastAPI Router pour la gestion des Tokens (Carburant)
Endpoints pour redeem codes, consulter solde, historique
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import Optional
import logging

from . import repository as tokens_repo
from ..dependencies import get_current_tenant_id

logger = logging.getLogger(__name__)

# Router FastAPI
router = APIRouter(
    prefix="/api/tokens",
    tags=["tokens"],
)


class RedeemCodeRequest(BaseModel):
    """Requête pour échanger un code licence"""
    code: str = Field(..., description="Code de recharge (ex: IAFACTORY-WELCOME-1000)")


@router.post("/redeem")
async def redeem_licence_code(
    request: RedeemCodeRequest,
    tenant_id: str = Depends(get_current_tenant_id),
):
    """
    Échanger un code licence contre des tokens

    **Isolation Multi-Tenant**: Le tenant_id est automatiquement injecté.
    Les tokens sont crédités uniquement au tenant authentifié.

    **Exemple**:
    ```json
    {
      "code": "IAFACTORY-WELCOME-1000"
    }
    ```

    **Réponse succès**:
    ```json
    {
      "success": true,
      "tokens_credited": 1000,
      "new_balance": 1000,
      "total_purchased": 1000
    }
    ```

    **Codes disponibles** (test):
    - `IAFACTORY-WELCOME-1000`: 1000 tokens (promotion onboarding)
    - `SUISSE-PRO-5000`: 5000 tokens (prepaid Suisse)
    - `ALGERIE-STARTER-500`: 500 tokens (trial Algérie)
    - `ENTERPRISE-UNLIMITED-50000`: 50000 tokens (enterprise)
    """
    try:
        result = tokens_repo.redeem_code(
            code=request.code.strip().upper(),
            tenant_id=tenant_id
        )

        if result.get("success"):
            logger.info(
                f"✅ Code redeemed successfully: {request.code} by tenant {tenant_id} "
                f"- Credited: {result['tokens_credited']} tokens"
            )
            return jsonable_encoder(result)  # Encode datetime
        else:
            logger.warning(
                f"❌ Failed to redeem code: {request.code} by tenant {tenant_id} "
                f"- Reason: {result.get('error')}"
            )
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "Code invalide")
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur API redeem: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/balance")
async def get_token_balance(tenant_id: str = Depends(get_current_tenant_id)):
    """
    Consulter le solde de tokens du tenant

    **Isolation Multi-Tenant**: Seul le solde du tenant authentifié est retourné.

    **Réponse**:
    ```json
    {
      "balance_tokens": 1000,
      "total_purchased": 5000,
      "total_consumed": 4000,
      "last_purchase_at": "2025-12-16T21:00:00Z",
      "last_usage_at": "2025-12-16T22:00:00Z"
    }
    ```
    """
    try:
        balance = tokens_repo.get_balance(tenant_id)
        return jsonable_encoder(balance)  # Encode datetime automatiquement

    except Exception as e:
        logger.error(f"Erreur API balance: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
async def get_usage_history(
    tenant_id: str = Depends(get_current_tenant_id),
    limit: int = 20,
    offset: int = 0,
):
    """
    Consulter l'historique d'utilisation des tokens

    **Isolation Multi-Tenant**: Seul l'historique du tenant authentifié est retourné.

    **Paramètres**:
    - `limit`: Nombre max de résultats (défaut: 20)
    - `offset`: Offset pour pagination (défaut: 0)

    **Réponse**:
    ```json
    [
      {
        "id": "uuid",
        "provider": "openai",
        "model": "gpt-4o",
        "tokens_input": 150,
        "tokens_output": 300,
        "tokens_total": 450,
        "cost_tokens": 450,
        "balance_after": 550,
        "latency_ms": 1200,
        "created_at": "2025-12-16T22:00:00Z",
        "metadata": {}
      }
    ]
    ```
    """
    try:
        history = tokens_repo.get_usage_history(
            tenant_id=tenant_id,
            limit=min(limit, 100),  # Max 100
            offset=offset
        )
        return jsonable_encoder({"history": history, "count": len(history)})  # Encode datetime

    except Exception as e:
        logger.error(f"Erreur API history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """
    Health check du système de tokens

    **Réponse**:
    ```json
    {
      "status": "healthy",
      "service": "tokens",
      "ready": true
    }
    ```
    """
    return JSONResponse(
        content={
            "status": "healthy",
            "service": "tokens",
            "ready": True,
        }
    )
