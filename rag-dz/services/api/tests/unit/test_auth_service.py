"""
Unit tests for AuthService
"""
import pytest
from app.services.auth_service import auth_service, pwd_context


class TestAuthService:
    """Test suite for authentication service"""

    def test_hash_password(self):
        """Test password hashing"""
        password = "MySecurePassword123!"
        hashed = pwd_context.hash(password)

        assert hashed != password
        assert pwd_context.verify(password, hashed)

    def test_verify_password_correct(self):
        """Test password verification with correct password"""
        password = "CorrectPassword123!"
        hashed = pwd_context.hash(password)

        assert pwd_context.verify(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password"""
        password = "CorrectPassword123!"
        wrong_password = "WrongPassword123!"
        hashed = pwd_context.hash(password)

        assert pwd_context.verify(wrong_password, hashed) is False

    def test_create_access_token(self):
        """Test JWT token creation"""
        data = {"sub": "test@rag.dz", "user_id": 1}
        token = auth_service.create_access_token(data)

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_verify_token_valid(self):
        """Test JWT token verification with valid token"""
        data = {"sub": "test@rag.dz", "user_id": 1}
        token = auth_service.create_access_token(data)

        payload = auth_service.verify_token(token)

        assert payload is not None
        assert payload["sub"] == "test@rag.dz"
        assert payload["user_id"] == 1

    def test_verify_token_invalid(self):
        """Test JWT token verification with invalid token"""
        invalid_token = "invalid.token.here"

        payload = auth_service.verify_token(invalid_token)

        assert payload is None
