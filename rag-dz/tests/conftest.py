import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../services/api")))
import pytest

from fastapi.testclient import TestClient
from services.api.main import app

@pytest.fixture(scope="module")
def client():
    if app is None or TestClient is None:
        pytest.skip("FastAPI app or TestClient not available")
    with TestClient(app) as c:
        yield c


from httpx import AsyncClient

@pytest.fixture(scope="module")
async def async_client():
    if app is None or AsyncClient is None:
        pytest.skip("FastAPI app or AsyncClient not available")
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac
