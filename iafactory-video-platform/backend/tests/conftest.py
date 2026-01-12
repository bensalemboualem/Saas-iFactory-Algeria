from app.gateway_helper import call_llm_sync
# MIGRATED TO GATEWAY http://localhost:3001
"""
Pytest configuration and fixtures
"""
import pytest
import asyncio
from typing import AsyncGenerator, Generator
from unittest.mock import MagicMock, AsyncMock
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import get_db
from app.core.config import settings


# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """Create test database engine"""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
    )
    yield engine
    await engine.dispose()


@pytest.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session"""
    async_session = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create test HTTP client"""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
def mock_openai():
    """Mock OpenAI client"""
    mock = MagicMock()
    mock.chat.completions.create = AsyncMock(
        return_value=MagicMock(
            choices=[MagicMock(message=MagicMock(content="Test response"))]
        )
    )
    mock.images.generate = AsyncMock(
        return_value=MagicMock(
            data=[MagicMock(url="https://example.com/image.png")]
        )
    )
    return mock


@pytest.fixture
def mock_elevenlabs():
    """Mock ElevenLabs client"""
    mock = AsyncMock()
    mock.generate = AsyncMock(return_value=b"audio_bytes")
    return mock


@pytest.fixture
def mock_httpx():
    """Mock httpx for external API calls"""
    mock = AsyncMock()
    mock.post = AsyncMock(
        return_value=MagicMock(
            status_code=200,
            json=MagicMock(return_value={"id": "test_id", "status": "completed"}),
            content=b"test_content",
        )
    )
    mock.get = AsyncMock(
        return_value=MagicMock(
            status_code=200,
            json=MagicMock(return_value={"status": "succeeded", "output": "https://example.com/video.mp4"}),
            content=b"test_content",
        )
    )
    return mock


@pytest.fixture
def sample_project_data():
    """Sample project data for testing"""
    return {
        "title": "Test Video Project",
        "description": "A test video about technology",
        "prompt": "Create a 60-second video about AI advancements",
        "style": "professional",
        "duration": 60,
        "platforms": ["youtube", "tiktok"],
    }


@pytest.fixture
def sample_script_data():
    """Sample script data for testing"""
    return {
        "content": "In this video, we explore the latest AI advancements...",
        "scenes": [
            {
                "number": 1,
                "narration": "Welcome to our exploration of AI.",
                "visual_description": "Futuristic cityscape with AI elements",
                "duration": 5,
            },
            {
                "number": 2,
                "narration": "AI is transforming every industry.",
                "visual_description": "Montage of various industries using AI",
                "duration": 10,
            },
        ],
    }


@pytest.fixture
def sample_timeline_data():
    """Sample timeline data for testing"""
    return {
        "tracks": [
            {
                "type": "video",
                "clips": [
                    {"start": 0, "end": 5, "asset_id": "asset1"},
                    {"start": 5, "end": 15, "asset_id": "asset2"},
                ],
            },
            {
                "type": "audio",
                "clips": [
                    {"start": 0, "end": 15, "asset_id": "voice1"},
                ],
            },
            {
                "type": "music",
                "clips": [
                    {"start": 0, "end": 15, "asset_id": "music1", "volume": 0.3},
                ],
            },
        ],
    }
