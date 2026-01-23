"""Tests pour le système de crédits"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from shared.credits import (
    CreditSystem,
    CreditOperation,
    CreditTransaction,
    CreditBalance,
    CREDIT_RATES,
    TIER_LIMITS,
    get_credit_system,
)


class TestCreditOperation:
    """Tests des opérations de crédit"""

    def test_operation_values(self):
        """Test valeurs des opérations"""
        assert CreditOperation.CHAT_MESSAGE.value == "chat_message"
        assert CreditOperation.CODE_GENERATION.value == "code_generation"
        assert CreditOperation.IMAGE_GENERATION.value == "image_generation"
        assert CreditOperation.VIDEO_GENERATION.value == "video_generation"

    def test_gov_operations(self):
        """Test opérations GOV"""
        assert CreditOperation.GOV_AGENT_CNAS.value == "gov_agent_cnas"
        assert CreditOperation.GOV_AGENT_DGI.value == "gov_agent_dgi"


class TestCreditRates:
    """Tests des tarifs"""

    def test_chat_rate(self):
        """Test tarif chat"""
        assert CREDIT_RATES["chat_message"] == 1
        assert CREDIT_RATES["chat_with_rag"] == 2

    def test_code_rates(self):
        """Test tarifs code"""
        assert CREDIT_RATES["code_generation"] == 5
        assert CREDIT_RATES["code_edit"] == 3

    def test_image_rates(self):
        """Test tarifs images"""
        assert CREDIT_RATES["image_generation"] == 20

    def test_video_rates(self):
        """Test tarifs vidéo (coûteux)"""
        assert CREDIT_RATES["video_generation"] == 100

    def test_gov_rates(self):
        """Test tarifs agents GOV"""
        assert CREDIT_RATES["gov_agent_cnas"] == 3
        assert CREDIT_RATES["gov_agent_sonelgaz"] == 3


class TestTierLimits:
    """Tests des limites par tier"""

    def test_free_tier(self):
        """Test tier free"""
        free = TIER_LIMITS["free"]
        assert free["monthly_credits"] == 100
        assert "chat" in free["features"]

    def test_starter_tier(self):
        """Test tier starter"""
        starter = TIER_LIMITS["starter"]
        assert starter["monthly_credits"] == 500
        assert "gov_agents" in starter["features"]

    def test_pro_tier(self):
        """Test tier pro"""
        pro = TIER_LIMITS["pro"]
        assert pro["monthly_credits"] == 2000
        assert "images" in pro["features"]

    def test_business_tier(self):
        """Test tier business"""
        business = TIER_LIMITS["business"]
        assert business["monthly_credits"] == 10000
        assert "all" in business["features"]

    def test_enterprise_tier(self):
        """Test tier enterprise (illimité)"""
        enterprise = TIER_LIMITS["enterprise"]
        assert enterprise["monthly_credits"] == -1  # Illimité
        assert "priority" in enterprise["features"]


class TestCreditSystem:
    """Tests du système de crédits"""

    @pytest.fixture
    def system(self):
        """Système avec mock Supabase"""
        with patch.dict("os.environ", {
            "SUPABASE_URL": "https://test.supabase.co",
            "SUPABASE_SERVICE_KEY": "test_key"
        }):
            return CreditSystem()

    def test_get_rate(self, system):
        """Test récupération du tarif"""
        assert system.get_rate(CreditOperation.CHAT_MESSAGE) == 1
        assert system.get_rate("code_generation") == 5
        assert system.get_rate("unknown") == 1  # Default

    @pytest.mark.asyncio
    async def test_check_balance(self, system):
        """Test vérification du solde"""
        with patch.object(system, '_get_client', new_callable=AsyncMock) as mock:
            mock_client = MagicMock()
            mock_client.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value = MagicMock(
                data={"balance": 500}
            )
            mock.return_value = mock_client

            balance = await system.check_balance("user_123")
            assert balance == 500

    @pytest.mark.asyncio
    async def test_can_afford_true(self, system):
        """Test can_afford quand assez de crédits"""
        with patch.object(system, 'check_balance', new_callable=AsyncMock) as mock:
            mock.return_value = 100

            result = await system.can_afford("user_123", CreditOperation.CHAT_MESSAGE)
            assert result is True

    @pytest.mark.asyncio
    async def test_can_afford_false(self, system):
        """Test can_afford quand pas assez de crédits"""
        with patch.object(system, 'check_balance', new_callable=AsyncMock) as mock:
            mock.return_value = 1

            result = await system.can_afford("user_123", CreditOperation.VIDEO_GENERATION)
            assert result is False

    @pytest.mark.asyncio
    async def test_deduct_success(self, system):
        """Test déduction réussie"""
        with patch.object(system, '_get_client', new_callable=AsyncMock) as mock_client_getter:
            mock_client = MagicMock()
            mock_client.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value = MagicMock(
                data={"user_id": "user_123", "balance": 100, "tier": "free", "monthly_limit": 100, "monthly_used": 0}
            )
            mock_client.table.return_value.update.return_value.eq.return_value.execute.return_value = MagicMock()
            mock_client.table.return_value.insert.return_value.execute.return_value = MagicMock()
            mock_client_getter.return_value = mock_client

            transaction = await system.deduct(
                "user_123",
                CreditOperation.CHAT_MESSAGE,
                description="Test deduction"
            )

            assert transaction is not None
            assert transaction.user_id == "user_123"
            assert transaction.amount == 1
            assert transaction.balance_before == 100
            assert transaction.balance_after == 99

    @pytest.mark.asyncio
    async def test_deduct_insufficient_funds(self, system):
        """Test déduction sans fonds suffisants"""
        with patch.object(system, 'get_balance_info', new_callable=AsyncMock) as mock:
            mock.return_value = CreditBalance(
                user_id="user_123",
                balance=5,
                tier="free",
                monthly_limit=100
            )

            transaction = await system.deduct(
                "user_123",
                CreditOperation.VIDEO_GENERATION  # Coûte 100
            )

            assert transaction is None

    @pytest.mark.asyncio
    async def test_add_credits(self, system):
        """Test ajout de crédits"""
        with patch.object(system, '_get_client', new_callable=AsyncMock) as mock_client_getter:
            mock_client = MagicMock()
            mock_client.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value = MagicMock(
                data={"user_id": "user_123", "balance": 50, "tier": "free", "monthly_limit": 100, "monthly_used": 0}
            )
            mock_client.table.return_value.update.return_value.eq.return_value.execute.return_value = MagicMock()
            mock_client.table.return_value.insert.return_value.execute.return_value = MagicMock()
            mock_client_getter.return_value = mock_client

            transaction = await system.add_credits(
                "user_123",
                100,
                "chargily",
                "payment_123"
            )

            assert transaction is not None
            assert transaction.amount == -100  # Négatif = crédit
            assert transaction.balance_after == 100  # Plafonné à max_balance


class TestCreditTransaction:
    """Tests du modèle CreditTransaction"""

    def test_transaction_creation(self):
        """Test création transaction"""
        transaction = CreditTransaction(
            id="tx_123",
            user_id="user_123",
            operation="chat_message",
            amount=1,
            balance_before=100,
            balance_after=99
        )
        assert transaction.id == "tx_123"
        assert transaction.amount == 1

    def test_transaction_with_metadata(self):
        """Test transaction avec métadonnées"""
        transaction = CreditTransaction(
            id="tx_123",
            user_id="user_123",
            operation="add_chargily",
            amount=-100,
            balance_before=50,
            balance_after=150,
            metadata={"payment_id": "pay_123"}
        )
        assert "payment_id" in transaction.metadata


class TestCreditBalance:
    """Tests du modèle CreditBalance"""

    def test_balance_creation(self):
        """Test création balance"""
        balance = CreditBalance(
            user_id="user_123",
            balance=500,
            tier="pro",
            monthly_limit=2000,
            monthly_used=100
        )
        assert balance.balance == 500
        assert balance.tier == "pro"

    def test_balance_defaults(self):
        """Test valeurs par défaut"""
        balance = CreditBalance(
            user_id="user_123",
            balance=100
        )
        assert balance.tier == "free"
        assert balance.monthly_limit == 100
        assert balance.monthly_used == 0
