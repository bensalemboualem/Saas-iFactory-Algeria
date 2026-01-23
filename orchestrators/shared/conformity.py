"""
Conformity Checker for IA Factory Algérie.
Vérifie la conformité du code généré avec les règles IA Factory.
"""

import re
from typing import Callable
from enum import Enum

from pydantic import BaseModel, Field


class ConformityLevel(str, Enum):
    """Niveaux de sévérité des violations"""
    CRITICAL = "critical"   # Bloque le déploiement
    HIGH = "high"           # Doit être corrigé avant merge
    MEDIUM = "medium"       # Avertissement important
    LOW = "low"             # Suggestion


class ConformityViolation(BaseModel):
    """Violation de conformité détectée"""
    rule: str
    level: ConformityLevel
    message: str
    file_path: str | None = None
    line_number: int | None = None
    suggestion: str | None = None


class ConformityResult(BaseModel):
    """Résultat de l'analyse de conformité"""
    is_compliant: bool
    violations: list[ConformityViolation] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    passed_rules: list[str] = Field(default_factory=list)
    score: float = 100.0  # 0-100


# ============ RÈGLES DE CONFORMITÉ ============

class ConformityRules:
    """
    Règles de conformité pour IA Factory Algérie.
    """

    @staticmethod
    def no_stripe(code: str) -> bool:
        """Stripe interdit - Utiliser Chargily uniquement"""
        # Ignorer les commentaires mentionnant "pas Stripe"
        code_no_comments = re.sub(r'#.*|//.*|/\*[\s\S]*?\*/|"""[\s\S]*?"""', '', code)
        return "stripe" not in code_no_comments.lower()

    @staticmethod
    def chargily_required(code: str) -> bool:
        """Chargily doit être utilisé pour les paiements"""
        if re.search(r'payment|checkout|billing|invoice', code, re.IGNORECASE):
            return "chargily" in code.lower()
        return True

    @staticmethod
    def rls_enabled(code: str) -> bool:
        """RLS doit être activé sur les tables Supabase"""
        if "CREATE TABLE" in code.upper():
            return "ENABLE ROW LEVEL SECURITY" in code.upper()
        return True

    @staticmethod
    def tenant_via_jwt(code: str) -> bool:
        """Tenant ID doit venir du JWT, pas des headers"""
        return "X-Tenant-ID" not in code

    @staticmethod
    def i18n_support(code: str) -> bool:
        """Support i18n requis (fr, ar, darija)"""
        # Vérifier si c'est du code frontend
        if re.search(r'\.tsx?$|\.jsx?$|component|page', code, re.IGNORECASE):
            return any(lang in code for lang in ["fr", "ar", "en", "i18n", "locale", "useTranslation"])
        return True

    @staticmethod
    def rtl_support(code: str) -> bool:
        """Support RTL requis pour l'arabe"""
        if "ar" in code.lower() and re.search(r'\.tsx?$|\.jsx?$|\.css$', code, re.IGNORECASE):
            return any(rtl in code.lower() for rtl in ["rtl", "direction", "dir="])
        return True

    @staticmethod
    def no_hardcoded_secrets(code: str) -> bool:
        """Pas de secrets en dur dans le code"""
        secret_patterns = [
            r'api[_-]?key\s*=\s*["\'][a-zA-Z0-9]{20,}["\']',
            r'secret\s*=\s*["\'][a-zA-Z0-9]{20,}["\']',
            r'password\s*=\s*["\'][^"\']{8,}["\']',
            r'sk_live_[a-zA-Z0-9]+',  # Stripe live key
            r'pk_live_[a-zA-Z0-9]+',  # Stripe live key
        ]
        for pattern in secret_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                return False
        return True

    @staticmethod
    def env_for_config(code: str) -> bool:
        """Configuration via variables d'environnement"""
        if re.search(r'api_key|secret|password|database_url', code, re.IGNORECASE):
            return "os.getenv" in code or "process.env" in code or "os.environ" in code
        return True

    @staticmethod
    def dzd_currency(code: str) -> bool:
        """Devise DZD pour les montants"""
        if re.search(r'amount|price|montant|prix', code, re.IGNORECASE):
            # Vérifier que USD/EUR ne sont pas utilisés par défaut
            non_dzd = re.search(r'currency\s*[=:]\s*["\']?(USD|EUR|usd|eur)["\']?', code)
            return not non_dzd or "DZD" in code
        return True

    @staticmethod
    def no_console_log_sensitive(code: str) -> bool:
        """Pas de console.log avec données sensibles"""
        sensitive_patterns = [
            r'console\.log.*password',
            r'console\.log.*secret',
            r'console\.log.*token',
            r'console\.log.*api_key',
            r'print\(.*password',
            r'print\(.*secret',
        ]
        for pattern in sensitive_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                return False
        return True

    @staticmethod
    def async_await_usage(code: str) -> bool:
        """Utiliser async/await pour les opérations I/O"""
        # Si on a des appels HTTP ou DB, vérifier async
        if re.search(r'httpx|requests|supabase|database', code, re.IGNORECASE):
            if ".get(" in code or ".post(" in code:
                return "async" in code or "await" in code
        return True

    @staticmethod
    def error_handling(code: str) -> bool:
        """Gestion des erreurs requise"""
        if re.search(r'async def|def \w+.*http|api', code, re.IGNORECASE):
            return "try:" in code or "except" in code or "catch" in code or "HTTPException" in code
        return True


# ============ DÉFINITION DES RÈGLES ============

CONFORMITY_RULES: dict[str, dict] = {
    # Règles critiques
    "no_stripe": {
        "check": ConformityRules.no_stripe,
        "level": ConformityLevel.CRITICAL,
        "message": "Stripe est interdit. Utiliser Chargily pour les paiements en Algérie.",
        "suggestion": "Remplacer par ChargilyService de orchestrators/shared/chargily.py"
    },
    "no_hardcoded_secrets": {
        "check": ConformityRules.no_hardcoded_secrets,
        "level": ConformityLevel.CRITICAL,
        "message": "Secrets/clés API en dur détectés dans le code.",
        "suggestion": "Utiliser os.getenv() ou process.env pour charger les secrets depuis .env"
    },
    "rls_enabled": {
        "check": ConformityRules.rls_enabled,
        "level": ConformityLevel.CRITICAL,
        "message": "Row Level Security (RLS) doit être activé sur toutes les tables.",
        "suggestion": "Ajouter 'ALTER TABLE ... ENABLE ROW LEVEL SECURITY'"
    },

    # Règles importantes
    "tenant_via_jwt": {
        "check": ConformityRules.tenant_via_jwt,
        "level": ConformityLevel.HIGH,
        "message": "Le tenant_id doit être extrait du JWT, pas des headers X-Tenant-ID.",
        "suggestion": "Utiliser get_current_user() pour extraire le tenant du token"
    },
    "chargily_required": {
        "check": ConformityRules.chargily_required,
        "level": ConformityLevel.HIGH,
        "message": "Chargily doit être utilisé pour les fonctionnalités de paiement.",
        "suggestion": "Importer ChargilyService depuis orchestrators/shared/chargily.py"
    },
    "env_for_config": {
        "check": ConformityRules.env_for_config,
        "level": ConformityLevel.HIGH,
        "message": "Les configurations sensibles doivent utiliser des variables d'environnement.",
        "suggestion": "Utiliser os.getenv('VAR_NAME') ou process.env.VAR_NAME"
    },

    # Règles moyennes
    "i18n_support": {
        "check": ConformityRules.i18n_support,
        "level": ConformityLevel.MEDIUM,
        "message": "Support i18n requis pour le marché algérien (fr, ar, darija).",
        "suggestion": "Utiliser next-intl ou react-i18next avec les locales fr/ar/en"
    },
    "rtl_support": {
        "check": ConformityRules.rtl_support,
        "level": ConformityLevel.MEDIUM,
        "message": "Support RTL requis pour l'arabe.",
        "suggestion": "Ajouter dir='rtl' et utiliser des styles RTL-aware"
    },
    "dzd_currency": {
        "check": ConformityRules.dzd_currency,
        "level": ConformityLevel.MEDIUM,
        "message": "La devise par défaut doit être DZD (Dinar Algérien).",
        "suggestion": "Utiliser currency='DZD' et formater avec Intl.NumberFormat('fr-DZ')"
    },
    "error_handling": {
        "check": ConformityRules.error_handling,
        "level": ConformityLevel.MEDIUM,
        "message": "Gestion des erreurs manquante dans les fonctions API.",
        "suggestion": "Ajouter try/except avec HTTPException ou raise approprié"
    },

    # Règles basses
    "no_console_log_sensitive": {
        "check": ConformityRules.no_console_log_sensitive,
        "level": ConformityLevel.LOW,
        "message": "Console.log avec données potentiellement sensibles détecté.",
        "suggestion": "Supprimer les logs de debug avant la production"
    },
    "async_await_usage": {
        "check": ConformityRules.async_await_usage,
        "level": ConformityLevel.LOW,
        "message": "Utiliser async/await pour les opérations I/O.",
        "suggestion": "Convertir en fonctions async pour de meilleures performances"
    },
}


class ConformityChecker:
    """
    Vérificateur de conformité pour le code généré.
    Utilisé par validator-qa pour valider le code avant merge.
    """

    def __init__(
        self,
        rules: dict | None = None,
        strict_mode: bool = False
    ):
        """
        Initialize the checker.

        Args:
            rules: Rules personnalisées (optionnel)
            strict_mode: Si True, les avertissements deviennent des erreurs
        """
        self.rules = rules or CONFORMITY_RULES
        self.strict_mode = strict_mode

    def check(self, code: str, file_path: str | None = None) -> ConformityResult:
        """
        Vérifie la conformité d'un code.

        Args:
            code: Code à vérifier
            file_path: Chemin du fichier (optionnel)

        Returns:
            ConformityResult
        """
        violations = []
        warnings = []
        passed_rules = []

        for rule_name, rule_config in self.rules.items():
            check_func = rule_config["check"]
            level = rule_config["level"]

            try:
                if not check_func(code):
                    violation = ConformityViolation(
                        rule=rule_name,
                        level=level,
                        message=rule_config["message"],
                        file_path=file_path,
                        suggestion=rule_config.get("suggestion")
                    )

                    if level in [ConformityLevel.CRITICAL, ConformityLevel.HIGH]:
                        violations.append(violation)
                    elif level == ConformityLevel.MEDIUM:
                        if self.strict_mode:
                            violations.append(violation)
                        else:
                            warnings.append(rule_config["message"])
                    else:
                        warnings.append(rule_config["message"])
                else:
                    passed_rules.append(rule_name)

            except Exception as e:
                warnings.append(f"Error checking rule {rule_name}: {e}")

        # Calculer le score
        total_rules = len(self.rules)
        critical_violations = len([v for v in violations if v.level == ConformityLevel.CRITICAL])
        high_violations = len([v for v in violations if v.level == ConformityLevel.HIGH])
        medium_count = len([w for w in warnings])

        # Score: critique = -30, high = -15, medium = -5
        penalty = (critical_violations * 30) + (high_violations * 15) + (medium_count * 5)
        score = max(0, 100 - penalty)

        return ConformityResult(
            is_compliant=len(violations) == 0,
            violations=violations,
            warnings=warnings,
            passed_rules=passed_rules,
            score=score
        )

    def check_multiple_files(
        self,
        files: dict[str, str]
    ) -> dict[str, ConformityResult]:
        """
        Vérifie plusieurs fichiers.

        Args:
            files: Dict {file_path: code}

        Returns:
            Dict {file_path: ConformityResult}
        """
        results = {}
        for file_path, code in files.items():
            results[file_path] = self.check(code, file_path)
        return results

    def get_summary(self, results: dict[str, ConformityResult]) -> dict:
        """
        Génère un résumé des résultats.

        Args:
            results: Résultats par fichier

        Returns:
            Résumé
        """
        total_violations = []
        total_warnings = []
        all_passed = True

        for file_path, result in results.items():
            total_violations.extend(result.violations)
            total_warnings.extend(result.warnings)
            if not result.is_compliant:
                all_passed = False

        avg_score = sum(r.score for r in results.values()) / len(results) if results else 100

        return {
            "is_compliant": all_passed,
            "total_files": len(results),
            "compliant_files": len([r for r in results.values() if r.is_compliant]),
            "total_violations": len(total_violations),
            "critical_violations": len([v for v in total_violations if v.level == ConformityLevel.CRITICAL]),
            "high_violations": len([v for v in total_violations if v.level == ConformityLevel.HIGH]),
            "total_warnings": len(total_warnings),
            "average_score": round(avg_score, 1),
            "violations": [v.model_dump() for v in total_violations]
        }

    def format_report(self, result: ConformityResult, file_path: str | None = None) -> str:
        """
        Formate un rapport lisible.

        Args:
            result: Résultat de conformité
            file_path: Chemin du fichier

        Returns:
            Rapport formaté
        """
        lines = []

        header = f"Conformity Report"
        if file_path:
            header += f" - {file_path}"
        lines.append(header)
        lines.append("=" * len(header))
        lines.append("")

        if result.is_compliant:
            lines.append("✅ Code is compliant")
        else:
            lines.append("❌ Code has violations")

        lines.append(f"Score: {result.score}/100")
        lines.append("")

        if result.violations:
            lines.append("VIOLATIONS:")
            for v in result.violations:
                icon = "🔴" if v.level == ConformityLevel.CRITICAL else "🟠"
                lines.append(f"  {icon} [{v.level.value.upper()}] {v.rule}")
                lines.append(f"      {v.message}")
                if v.suggestion:
                    lines.append(f"      → {v.suggestion}")
            lines.append("")

        if result.warnings:
            lines.append("WARNINGS:")
            for w in result.warnings:
                lines.append(f"  ⚠️ {w}")
            lines.append("")

        if result.passed_rules:
            lines.append(f"PASSED: {len(result.passed_rules)} rules")

        return "\n".join(lines)


# Singleton
_conformity_checker: ConformityChecker | None = None


def get_conformity_checker() -> ConformityChecker:
    """Get or create the conformity checker singleton"""
    global _conformity_checker
    if _conformity_checker is None:
        _conformity_checker = ConformityChecker()
    return _conformity_checker
