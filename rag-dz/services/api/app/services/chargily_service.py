"""
Chargily Payment Service for Algeria
Supports: CIB, EDAHABIA, BaridiMob
Documentation: https://dev.chargily.com
"""
import httpx
import logging
import hmac
import hashlib
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel
from ..config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class CheckoutRequest(BaseModel):
    """Request model for creating checkout"""
    amount: int  # Amount in DZD (centimes)
    currency: str = "dzd"
    description: str
    success_url: str
    failure_url: str
    webhook_endpoint: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    locale: str = "fr"  # fr, ar, en


class CheckoutResponse(BaseModel):
    """Response model from Chargily"""
    id: str
    checkout_url: str
    status: str
    amount: int
    currency: str


class ChargilyService:
    """
    Service for Chargily payment integration

    Usage:
        checkout = await chargily_service.create_checkout(
            amount=5000,  # 5000 DZD
            description="100 Credits IA Factory",
            success_url="https://iafactory.dz/payment/success",
            failure_url="https://iafactory.dz/payment/failure",
            metadata={"user_id": "xxx", "credits": 100}
        )
    """

    def __init__(self):
        self.api_key = settings.chargily_api_key
        self.secret_key = settings.chargily_secret_key
        self.mode = settings.chargily_mode

        # Set API URL based on mode
        if self.mode == "live":
            self.api_url = "https://pay.chargily.net/api/v2"
        else:
            self.api_url = "https://pay.chargily.net/test/api/v2"

        self.headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    async def create_checkout(
        self,
        amount: int,
        description: str,
        success_url: str,
        failure_url: str,
        webhook_endpoint: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        locale: str = "fr"
    ) -> CheckoutResponse:
        """
        Create a checkout session

        Args:
            amount: Amount in DZD (NOT centimes for Chargily v2)
            description: Payment description
            success_url: Redirect URL on success
            failure_url: Redirect URL on failure
            webhook_endpoint: Optional webhook URL
            metadata: Additional data (user_id, credits, etc.)
            locale: Language (fr, ar, en)

        Returns:
            CheckoutResponse with checkout_url for redirect
        """
        payload = {
            "amount": amount,
            "currency": "dzd",
            "description": description,
            "success_url": success_url,
            "failure_url": failure_url,
            "locale": locale
        }

        if webhook_endpoint:
            payload["webhook_endpoint"] = webhook_endpoint

        if metadata:
            payload["metadata"] = metadata

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/checkouts",
                    json=payload,
                    headers=self.headers,
                    timeout=30.0
                )

                if response.status_code == 201:
                    data = response.json()
                    logger.info(f"Checkout created: {data.get('id')}")
                    return CheckoutResponse(
                        id=data["id"],
                        checkout_url=data["checkout_url"],
                        status=data["status"],
                        amount=data["amount"],
                        currency=data["currency"]
                    )
                else:
                    logger.error(f"Chargily error: {response.status_code} - {response.text}")
                    raise Exception(f"Chargily API error: {response.status_code}")

        except httpx.RequestError as e:
            logger.error(f"Chargily request error: {e}")
            raise Exception(f"Payment service unavailable: {e}")

    async def get_checkout(self, checkout_id: str) -> Dict[str, Any]:
        """Get checkout details by ID"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_url}/checkouts/{checkout_id}",
                    headers=self.headers,
                    timeout=30.0
                )

                if response.status_code == 200:
                    return response.json()
                else:
                    raise Exception(f"Checkout not found: {checkout_id}")

        except httpx.RequestError as e:
            logger.error(f"Chargily request error: {e}")
            raise

    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        """
        Verify webhook signature from Chargily

        Args:
            payload: Raw request body bytes
            signature: Signature from X-Chargily-Signature header

        Returns:
            True if signature is valid
        """
        if not settings.chargily_webhook_secret:
            logger.warning("Webhook secret not configured")
            return False

        expected = hmac.new(
            settings.chargily_webhook_secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected, signature)

    async def handle_webhook(self, event_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle webhook events from Chargily

        Events:
            - checkout.paid: Payment successful
            - checkout.failed: Payment failed
            - checkout.expired: Checkout expired
        """
        checkout_id = data.get("id")
        metadata = data.get("metadata", {})

        result = {
            "event": event_type,
            "checkout_id": checkout_id,
            "metadata": metadata,
            "processed_at": datetime.utcnow().isoformat()
        }

        if event_type == "checkout.paid":
            logger.info(f"Payment successful for checkout: {checkout_id}")
            result["status"] = "success"
            result["amount"] = data.get("amount")

        elif event_type == "checkout.failed":
            logger.warning(f"Payment failed for checkout: {checkout_id}")
            result["status"] = "failed"

        elif event_type == "checkout.expired":
            logger.info(f"Checkout expired: {checkout_id}")
            result["status"] = "expired"

        else:
            logger.warning(f"Unknown webhook event: {event_type}")
            result["status"] = "unknown"

        return result

    @property
    def is_configured(self) -> bool:
        """Check if Chargily is properly configured"""
        return bool(self.api_key and self.secret_key)


# Global instance
chargily_service = ChargilyService()
