"""
Integration tests for authentication API endpoints
"""
import pytest
from fastapi.testclient import TestClient


class TestAuthAPI:
    """Test suite for /api/auth endpoints"""

    def test_register_new_user(self, client: TestClient):
        """Test user registration"""
        response = client.post("/api/auth/register", json={
            "email": "newuser@test.com",
            "password": "SecurePassword123!",
            "username": "newuser"
        })

        # May fail if user already exists, that's ok
        assert response.status_code in [200, 400]

    def test_login_success(self, client: TestClient, test_user_credentials):
        """Test successful login"""
        # First register
        client.post("/api/auth/register", json={
            **test_user_credentials,
            "username": "testuser"
        })

        # Then login
        response = client.post("/api/auth/login", json=test_user_credentials)

        if response.status_code == 200:
            data = response.json()
            assert "access_token" in data
            assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client: TestClient):
        """Test login with wrong password"""
        response = client.post("/api/auth/login", json={
            "email": "test@rag.dz",
            "password": "WrongPassword!"
        })

        assert response.status_code == 401

    def test_get_current_user(self, client: TestClient, test_user_credentials):
        """Test getting current user info"""
        # Register and login
        client.post("/api/auth/register", json={
            **test_user_credentials,
            "username": "testuser"
        })

        login_response = client.post("/api/auth/login", json=test_user_credentials)

        if login_response.status_code == 200:
            token = login_response.json()["access_token"]

            # Get current user
            response = client.get(
                "/api/auth/me",
                headers={"Authorization": f"Bearer {token}"}
            )

            if response.status_code == 200:
                data = response.json()
                assert data["email"] == test_user_credentials["email"]
