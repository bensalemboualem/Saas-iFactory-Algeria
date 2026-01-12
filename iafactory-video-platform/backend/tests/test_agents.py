"""
Tests for AI Agents
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.agents.base import BaseAgent, AgentTask, AgentResult, AgentState
from app.agents.script_agent import ScriptAgent
from app.agents.image_agent import ImageAgent
from app.agents.voice_agent import VoiceAgent


class TestBaseAgent:
    """Tests for BaseAgent"""

    def test_agent_task_creation(self):
        """Test AgentTask model creation"""
        task = AgentTask(
            task_id="test-123",
            task_type="generate",
            input_data={"prompt": "test"},
            priority=1,
        )
        assert task.task_id == "test-123"
        assert task.task_type == "generate"
        assert task.priority == 1

    def test_agent_result_success(self):
        """Test successful AgentResult"""
        result = AgentResult(
            task_id="test-123",
            success=True,
            data={"output": "generated content"},
        )
        assert result.success is True
        assert result.error is None

    def test_agent_result_failure(self):
        """Test failed AgentResult"""
        result = AgentResult(
            task_id="test-123",
            success=False,
            error="Generation failed",
        )
        assert result.success is False
        assert result.error == "Generation failed"


class TestScriptAgent:
    """Tests for ScriptAgent"""

    @pytest.fixture
    def script_agent(self, mock_openai):
        """Create ScriptAgent with mocked LLM"""
        with patch("app.agents.script_agent.llm_service") as mock_llm:
            mock_llm.generate = AsyncMock(
                return_value={
                    "content": """
                    Scene 1: Introduction
                    Narration: Welcome to our video about AI.
                    Visual: Futuristic cityscape
                    Duration: 5s

                    Scene 2: Main Content
                    Narration: AI is changing the world.
                    Visual: Technology montage
                    Duration: 10s
                    """
                }
            )
            agent = ScriptAgent()
            yield agent

    @pytest.mark.asyncio
    async def test_generate_script(self, script_agent, sample_project_data):
        """Test script generation"""
        task = AgentTask(
            task_id="script-1",
            task_type="generate_script",
            input_data={
                "prompt": sample_project_data["prompt"],
                "style": sample_project_data["style"],
                "duration": sample_project_data["duration"],
            },
        )

        result = await script_agent.execute(task)

        assert result.success is True
        assert "content" in result.data
        assert "scenes" in result.data

    @pytest.mark.asyncio
    async def test_parse_scenes(self, script_agent):
        """Test scene parsing from script content"""
        script_content = """
        Scene 1: Opening
        Narration: Hello world
        Visual: Beautiful landscape
        Duration: 5s

        Scene 2: Middle
        Narration: This is the main content
        Visual: Action sequence
        Duration: 10s
        """

        scenes = script_agent._parse_scenes(script_content)

        assert len(scenes) == 2
        assert scenes[0]["narration"] == "Hello world"
        assert scenes[1]["duration"] == 10


class TestImageAgent:
    """Tests for ImageAgent"""

    @pytest.fixture
    def image_agent(self, mock_httpx):
        """Create ImageAgent with mocked providers"""
        with patch("app.agents.image_agent.image_service") as mock_img:
            mock_img.generate = AsyncMock(
                return_value=[
                    {"url": "https://example.com/image1.png", "provider": "dalle"}
                ]
            )
            agent = ImageAgent()
            yield agent

    @pytest.mark.asyncio
    async def test_generate_image(self, image_agent):
        """Test image generation"""
        task = AgentTask(
            task_id="image-1",
            task_type="generate_image",
            input_data={
                "prompt": "A beautiful sunset over mountains",
                "style": "photorealistic",
                "size": "1024x1024",
            },
        )

        result = await image_agent.execute(task)

        assert result.success is True
        assert "images" in result.data
        assert len(result.data["images"]) > 0

    @pytest.mark.asyncio
    async def test_batch_generate_images(self, image_agent):
        """Test batch image generation for multiple scenes"""
        task = AgentTask(
            task_id="image-batch-1",
            task_type="generate_batch",
            input_data={
                "scenes": [
                    {"visual_description": "Scene 1 visual"},
                    {"visual_description": "Scene 2 visual"},
                ],
                "style": "cinematic",
            },
        )

        result = await image_agent.execute(task)

        assert result.success is True


class TestVoiceAgent:
    """Tests for VoiceAgent"""

    @pytest.fixture
    def voice_agent(self, mock_elevenlabs):
        """Create VoiceAgent with mocked TTS"""
        with patch("app.agents.voice_agent.audio_service") as mock_audio:
            mock_audio.text_to_speech = AsyncMock(
                return_value={
                    "audio_bytes": b"fake_audio_data",
                    "provider": "elevenlabs",
                }
            )
            agent = VoiceAgent()
            yield agent

    @pytest.mark.asyncio
    async def test_generate_voice(self, voice_agent):
        """Test voice generation"""
        task = AgentTask(
            task_id="voice-1",
            task_type="generate_voice",
            input_data={
                "text": "Hello, welcome to our video.",
                "voice_id": "rachel",
            },
        )

        result = await voice_agent.execute(task)

        assert result.success is True
        assert "audio_path" in result.data or "audio_bytes" in result.data

    @pytest.mark.asyncio
    async def test_generate_voice_for_scenes(self, voice_agent):
        """Test voice generation for multiple scenes"""
        task = AgentTask(
            task_id="voice-batch-1",
            task_type="generate_batch",
            input_data={
                "scenes": [
                    {"narration": "Scene 1 narration"},
                    {"narration": "Scene 2 narration"},
                ],
                "voice_id": "nova",
            },
        )

        result = await voice_agent.execute(task)

        assert result.success is True


class TestAgentErrorHandling:
    """Tests for agent error handling"""

    @pytest.mark.asyncio
    async def test_agent_handles_api_error(self):
        """Test that agents handle API errors gracefully"""
        with patch("app.agents.script_agent.llm_service") as mock_llm:
            mock_llm.generate = AsyncMock(side_effect=Exception("API Error"))

            agent = ScriptAgent()
            task = AgentTask(
                task_id="error-test",
                task_type="generate_script",
                input_data={"prompt": "test"},
            )

            result = await agent.execute(task)

            assert result.success is False
            assert "error" in result.error.lower() or result.error is not None

    @pytest.mark.asyncio
    async def test_agent_handles_invalid_input(self):
        """Test that agents handle invalid input"""
        agent = ScriptAgent()
        task = AgentTask(
            task_id="invalid-input",
            task_type="generate_script",
            input_data={},  # Missing required fields
        )

        result = await agent.execute(task)

        # Should fail gracefully
        assert result.success is False or "prompt" in str(result.error).lower()
