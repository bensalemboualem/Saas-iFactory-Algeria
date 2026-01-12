"""Tests pour le service Chargily"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from shared.chargily import (
    ChargilyService,
    ChargilyPayment,
    ChargilyCheckout,
    PaymentStatus,
    PaymentMode,
    CREDIT_PACKS,
    get_credit_pack,
)


class TestChargilyPayment:
    """Tests du modèle ChargilyPayment"""

    def test_payment_creation(self):
        """Test création de paiement"""
        payment = ChargilyPayment(
            amount=10000,  # 100.00 DZD
            client_name="Test Client",
            client_email="test@example.com",
            description="Test payment",
            webhook_url="https://example.com/webhook"
        )
        assert payment.amount == 10000
        assert payment.currency == "DZD"
        assert payment.client_name == "Test Client"

    def test_payment_defaults(self):
        """Test valeurs par défaut"""
        payment = ChargilyPayment(
            amount=5000,
            client_name="Test",
            client_email="test@test.com",
            description="Test",
            webhook_url="https://test.com/hook"
        )
        assert payment.currency == "DZD"
        assert payment.locale == "fr"
        assert payment.metadata == {}


class TestChargilyService:
    """Tests du service Chargily"""

    @pytest.fixture
    def service(self):
        """Service avec clés mock"""
        with patch.dict("os.environ", {
            "CHARGILY_API_KEY": "test_key",
            "CHARGILY_SECRET_KEY": "test_secret",
            "CHARGILY_WEBHOOK_SECRET": "test_webhook_secret"
        }):
            return ChargilyService()

    def test_init_with_env(self, service):
        """Test initialisation avec env vars"""
        assert service.api_key == "test_key"
        assert service.secret_key == "test_secret"

    def test_init_without_key_fails(self):
        """Test échec sans clé API"""
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="CHARGILY_API_KEY"):
                ChargilyService()

    def test_dzd_to_centimes(self):
        """Test conversion DZD vers centimes"""
        assert ChargilyService.dzd_to_centimes(100.00) == 10000
        assert ChargilyService.dzd_to_centimes(50.50) == 5050
        assert ChargilyService.dzd_to_centimes(0) == 0

    def test_centimes_to_dzd(self):
        """Test conversion centimes vers DZD"""
        assert ChargilyService.centimes_to_dzd(10000) == 100.0
        assert ChargilyService.centimes_to_dzd(5050) == 50.5
        assert ChargilyService.centimes_to_dzd(0) == 0.0

    @pytest.mark.asyncio
    async def test_create_checkout(self, service):
        """Test création de checkout"""
        payment = ChargilyPayment(
            amount=10000,
            client_name="Test",
            client_email="test@test.com",
            description="Test",
            webhook_url="https://test.com/hook"
        )

        with patch.object(service.client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value = MagicMock(
                json=lambda: {
                    "id": "checkout_123",
                    "entity": "checkout",
                    "status": "pending",
                    "amount": 10000,
                    "currency": "DZD",
                    "checkout_url": "https://pay.chargily.net/checkout/123"
                },
                raise_for_status=lambda: None
            )

            checkout = await service.create_checkout(payment)

            assert checkout.id == "checkout_123"
            assert checkout.status == PaymentStatus.PENDING
            assert checkout.checkout_url == "https://pay.chargily.net/checkout/123"

    def test_verify_webhook(self, service):
        """Test vérification signature webhook"""
        import hmac
        import hashlib

        payload = b'{"id": "test"}'
        signature = hmac.new(
            b"test_webhook_secret",
            payload,
            hashlib.sha256
        ).hexdigest()

        assert service.verify_webhook(signature, payload) is True
        assert service.verify_webhook("invalid_signature", payload) is False


class TestCreditPacks:
    """Tests des packs de crédits"""

    def test_packs_defined(self):
        """Test que les packs sont définis"""
        assert len(CREDIT_PACKS) == 4

    def test_pack_starter(self):
        """Test pack Starter"""
        pack = get_credit_pack("pack_starter")
        assert pack is not None
        assert pack["credits"] == 100
        assert pack["price_dzd"] == 500

    def test_pack_pro(self):
        """Test pack Pro"""
        pack = get_credit_pack("pack_pro")
        assert pack is not None
        assert pack["credits"] == 500

    def test_pack_business(self):
        """Test pack Business"""
        pack = get_credit_pack("pack_business")
        assert pack is not None
        assert pack["credits"] == 2000

    def test_pack_enterprise(self):
        """Test pack Enterprise"""
        pack = get_credit_pack("pack_enterprise")
        assert pack is not None
        assert pack["credits"] == 10000

    def test_pack_not_found(self):
        """Test pack non trouvé"""
        pack = get_credit_pack("nonexistent")
        assert pack is None

    def test_all_packs_have_required_fields(self):
        """Test que tous les packs ont les champs requis"""
        required_fields = ["id", "name", "credits", "price_dzd", "price_centimes"]
        for pack in CREDIT_PACKS:
            for field in required_fields:
                assert field in pack, f"Pack missing {field}"
