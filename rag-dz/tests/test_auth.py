import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_login_success(client):
    response = await client.post("/api/auth/login", json={"email": "user@test.dz", "password": "pass"})
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_login_fail(client):
    response = await client.post("/api/auth/login", json={"email": "user@test.dz", "password": "wrong"})
    assert response.status_code == 401
