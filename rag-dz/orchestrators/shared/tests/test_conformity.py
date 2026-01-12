"""Tests pour le Conformity Checker"""

import pytest

from shared.conformity import (
    ConformityChecker,
    ConformityResult,
    ConformityViolation,
    ConformityLevel,
    ConformityRules,
    CONFORMITY_RULES,
    get_conformity_checker,
)


class TestConformityRules:
    """Tests des règles individuelles"""

    def test_no_stripe_pass(self):
        """Test no_stripe avec code valide"""
        code = """
        from shared.chargily import ChargilyService
        service = ChargilyService()
        """
        assert ConformityRules.no_stripe(code) is True

    def test_no_stripe_fail(self):
        """Test no_stripe avec Stripe détecté"""
        code = """
        import stripe
        stripe.api_key = "sk_test_..."
        """
        assert ConformityRules.no_stripe(code) is False

    def test_no_stripe_comment_ignored(self):
        """Test no_stripe ignore les commentaires"""
        code = """
        # We don't use Stripe, only Chargily
        from shared.chargily import ChargilyService
        """
        assert ConformityRules.no_stripe(code) is True

    def test_rls_enabled_pass(self):
        """Test RLS avec ALTER TABLE correct"""
        code = """
        CREATE TABLE users (id UUID PRIMARY KEY);
        ALTER TABLE users ENABLE ROW LEVEL SECURITY;
        """
        assert ConformityRules.rls_enabled(code) is True

    def test_rls_enabled_fail(self):
        """Test RLS sans ENABLE"""
        code = """
        CREATE TABLE users (id UUID PRIMARY KEY);
        """
        assert ConformityRules.rls_enabled(code) is False

    def test_rls_enabled_not_applicable(self):
        """Test RLS non applicable (pas de CREATE TABLE)"""
        code = """
        def hello():
            return "world"
        """
        assert ConformityRules.rls_enabled(code) is True

    def test_tenant_via_jwt_pass(self):
        """Test tenant via JWT"""
        code = """
        def get_tenant(token: str):
            return decode_jwt(token)["tenant_id"]
        """
        assert ConformityRules.tenant_via_jwt(code) is True

    def test_tenant_via_jwt_fail(self):
        """Test tenant via header (interdit)"""
        code = """
        tenant_id = request.headers.get("X-Tenant-ID")
        """
        assert ConformityRules.tenant_via_jwt(code) is False

    def test_no_hardcoded_secrets_pass(self):
        """Test pas de secrets en dur"""
        code = """
        api_key = os.getenv("API_KEY")
        """
        assert ConformityRules.no_hardcoded_secrets(code) is True

    def test_no_hardcoded_secrets_fail(self):
        """Test secrets en dur détectés"""
        code = """
        api_key = "sk_live_abcdefghijklmnopqrstuvwxyz123456"
        """
        assert ConformityRules.no_hardcoded_secrets(code) is False

    def test_i18n_support_pass(self):
        """Test i18n présent"""
        code = """
        // Component.tsx
        import { useTranslation } from 'next-intl';
        const { t } = useTranslation();
        """
        assert ConformityRules.i18n_support(code) is True

    def test_dzd_currency_pass(self):
        """Test devise DZD"""
        code = """
        amount = 1000
        currency = "DZD"
        """
        assert ConformityRules.dzd_currency(code) is True

    def test_dzd_currency_fail(self):
        """Test devise USD (interdit par défaut)"""
        code = """
        amount = 1000
        currency = "USD"
        """
        assert ConformityRules.dzd_currency(code) is False

    def test_env_for_config_pass(self):
        """Test config via env"""
        code = """
        api_key = os.getenv("API_KEY")
        secret = os.environ.get("SECRET")
        """
        assert ConformityRules.env_for_config(code) is True


class TestConformityChecker:
    """Tests du checker complet"""

    @pytest.fixture
    def checker(self):
        """Checker instance"""
        return ConformityChecker()

    def test_compliant_code(self, checker):
        """Test code conforme"""
        code = """
        import os
        from shared.chargily import ChargilyService

        api_key = os.getenv("CHARGILY_API_KEY")
        service = ChargilyService(api_key)

        async def create_payment(amount: int):
            try:
                return await service.create_checkout(...)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        """
        result = checker.check(code)

        assert result.is_compliant is True
        assert len(result.violations) == 0
        assert result.score > 80

    def test_non_compliant_code(self, checker):
        """Test code non conforme"""
        code = """
        import stripe

        stripe.api_key = "sk_live_abc123xyz"

        def process_payment():
            currency = "USD"
            tenant = request.headers.get("X-Tenant-ID")
        """
        result = checker.check(code)

        assert result.is_compliant is False
        assert len(result.violations) > 0
        assert result.score < 50

    def test_violations_have_suggestions(self, checker):
        """Test que les violations ont des suggestions"""
        code = "import stripe"
        result = checker.check(code)

        for violation in result.violations:
            assert violation.suggestion is not None

    def test_check_multiple_files(self, checker):
        """Test vérification de plusieurs fichiers"""
        files = {
            "good.py": "from shared.chargily import ChargilyService",
            "bad.py": "import stripe"
        }

        results = checker.check_multiple_files(files)

        assert len(results) == 2
        assert results["good.py"].is_compliant is True
        assert results["bad.py"].is_compliant is False

    def test_get_summary(self, checker):
        """Test résumé"""
        files = {
            "a.py": "good code",
            "b.py": "import stripe"
        }
        results = checker.check_multiple_files(files)
        summary = checker.get_summary(results)

        assert "total_files" in summary
        assert summary["total_files"] == 2
        assert "average_score" in summary

    def test_format_report(self, checker):
        """Test formatage rapport"""
        code = "import stripe"
        result = checker.check(code)
        report = checker.format_report(result, "test.py")

        assert "Conformity Report" in report
        assert "test.py" in report
        assert "VIOLATIONS" in report

    def test_strict_mode(self):
        """Test mode strict"""
        checker = ConformityChecker(strict_mode=True)
        code = """
        # Code avec avertissement medium
        def api_call():
            response = requests.get(url)  # Pas de async
        """
        result = checker.check(code)

        # En mode strict, les warnings medium deviennent des violations
        # (selon le contenu du code)


class TestConformityResult:
    """Tests du modèle ConformityResult"""

    def test_result_creation(self):
        """Test création résultat"""
        result = ConformityResult(
            is_compliant=True,
            violations=[],
            warnings=[],
            passed_rules=["rule1", "rule2"],
            score=100.0
        )
        assert result.is_compliant is True
        assert result.score == 100.0

    def test_result_with_violations(self):
        """Test résultat avec violations"""
        violation = ConformityViolation(
            rule="no_stripe",
            level=ConformityLevel.CRITICAL,
            message="Stripe interdit"
        )
        result = ConformityResult(
            is_compliant=False,
            violations=[violation],
            score=70.0
        )
        assert result.is_compliant is False
        assert len(result.violations) == 1


class TestConformityViolation:
    """Tests du modèle ConformityViolation"""

    def test_violation_creation(self):
        """Test création violation"""
        violation = ConformityViolation(
            rule="test_rule",
            level=ConformityLevel.HIGH,
            message="Test message",
            file_path="test.py",
            line_number=10,
            suggestion="Fix it"
        )
        assert violation.rule == "test_rule"
        assert violation.level == ConformityLevel.HIGH
        assert violation.file_path == "test.py"
        assert violation.line_number == 10


class TestConformityLevel:
    """Tests des niveaux de sévérité"""

    def test_levels(self):
        """Test valeurs des niveaux"""
        assert ConformityLevel.CRITICAL.value == "critical"
        assert ConformityLevel.HIGH.value == "high"
        assert ConformityLevel.MEDIUM.value == "medium"
        assert ConformityLevel.LOW.value == "low"


class TestGetConformityChecker:
    """Tests du singleton"""

    def test_singleton(self):
        """Test que c'est un singleton"""
        checker1 = get_conformity_checker()
        checker2 = get_conformity_checker()
        assert checker1 is checker2
