"""
SECURITY TESTS: JWT Algorithm Validation

These tests ensure that JWT tokens with the 'none' algorithm are rejected.
This prevents the JWT signature bypass vulnerability.

Reference: https://www.invicti.com/web-vulnerability-scanner/vulnerabilities/jwt-signature-bypass-via-none-algorithm
"""
import pytest
import base64
import json
from jose import jwt

from app.core.security import (
    decode_token,
    create_access_token,
    _validate_jwt_algorithm,
    ALLOWED_JWT_ALGORITHMS,
)
from app.core.config import settings


class TestJWTAlgorithmValidation:
    """Test JWT algorithm security measures."""

    def test_none_algorithm_rejected_by_validator(self):
        """Test that _validate_jwt_algorithm rejects 'none' algorithm."""
        with pytest.raises(ValueError) as exc_info:
            _validate_jwt_algorithm("none")
        assert "not allowed" in str(exc_info.value).lower()

    def test_none_algorithm_case_insensitive(self):
        """Test that 'None', 'NONE', 'NoNe' are all rejected."""
        for variant in ["None", "NONE", "NoNe", "nOnE"]:
            with pytest.raises(ValueError):
                _validate_jwt_algorithm(variant)

    def test_allowed_algorithms_accepted(self):
        """Test that allowed algorithms pass validation."""
        for alg in ALLOWED_JWT_ALGORITHMS:
            result = _validate_jwt_algorithm(alg)
            assert result == alg

    def test_unknown_algorithm_rejected(self):
        """Test that unknown algorithms are rejected."""
        with pytest.raises(ValueError):
            _validate_jwt_algorithm("UNKNOWN_ALG")

    def test_decode_token_rejects_none_algorithm_token(self):
        """
        CRITICAL SECURITY TEST: Verify that tokens crafted with alg=none are rejected.

        This simulates an attacker trying to bypass signature verification by
        sending a token with the header {"alg": "none", "typ": "JWT"}.
        """
        # Create a forged token with alg=none
        header = {"alg": "none", "typ": "JWT"}
        payload = {
            "sub": "attacker@evil.com",
            "exp": 9999999999,  # Far future
            "type": "access"
        }

        # Encode header and payload as base64
        header_b64 = base64.urlsafe_b64encode(
            json.dumps(header).encode()
        ).rstrip(b'=').decode()

        payload_b64 = base64.urlsafe_b64encode(
            json.dumps(payload).encode()
        ).rstrip(b'=').decode()

        # Create unsigned token (alg=none means no signature)
        forged_token = f"{header_b64}.{payload_b64}."

        # This MUST return None (reject the token)
        result = decode_token(forged_token)
        assert result is None, "SECURITY FAILURE: Token with alg=none was accepted!"

    def test_decode_token_rejects_empty_signature(self):
        """Test that tokens with empty signatures are rejected."""
        # Create a token that looks valid but has no signature
        header = {"alg": "HS256", "typ": "JWT"}
        payload = {
            "sub": "attacker@evil.com",
            "exp": 9999999999,
            "type": "access"
        }

        header_b64 = base64.urlsafe_b64encode(
            json.dumps(header).encode()
        ).rstrip(b'=').decode()

        payload_b64 = base64.urlsafe_b64encode(
            json.dumps(payload).encode()
        ).rstrip(b'=').decode()

        # Token with empty signature
        forged_token = f"{header_b64}.{payload_b64}."

        result = decode_token(forged_token)
        assert result is None, "SECURITY FAILURE: Token with empty signature was accepted!"

    def test_valid_token_accepted(self):
        """Test that properly signed tokens are accepted."""
        token = create_access_token({"sub": "user@example.com"})
        result = decode_token(token)

        assert result is not None
        assert result.get("sub") == "user@example.com"
        assert result.get("type") == "access"

    def test_tampered_token_rejected(self):
        """Test that tokens with tampered payloads are rejected."""
        # Create a valid token
        token = create_access_token({"sub": "user@example.com"})

        # Tamper with the payload
        parts = token.split(".")
        payload = json.loads(base64.urlsafe_b64decode(parts[1] + "=="))
        payload["sub"] = "attacker@evil.com"

        tampered_payload = base64.urlsafe_b64encode(
            json.dumps(payload).encode()
        ).rstrip(b'=').decode()

        tampered_token = f"{parts[0]}.{tampered_payload}.{parts[2]}"

        result = decode_token(tampered_token)
        assert result is None, "SECURITY FAILURE: Tampered token was accepted!"


class TestRateLimitingSmokeTest:
    """Basic smoke tests for rate limiting (full tests require running server)."""

    def test_sensitive_endpoints_defined(self):
        """Verify that sensitive endpoints have rate limit configuration."""
        from app.main import SENSITIVE_ENDPOINTS

        required_endpoints = [
            "/api/v1/auth/login",
            "/api/v1/auth/register",
            "/api/v1/auth/forgot-password",
        ]

        for endpoint in required_endpoints:
            assert endpoint in SENSITIVE_ENDPOINTS, f"Missing rate limit for {endpoint}"
            config = SENSITIVE_ENDPOINTS[endpoint]
            assert "limit" in config
            assert "lockout_after" in config
            assert "lockout_duration" in config
