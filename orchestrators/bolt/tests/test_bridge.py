"""Tests pour le Bolt Bridge"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

from src.bridge import (
    BoltBridge,
    Provider,
    Template,
    Project,
    GenerationResult,
    CommandResult,
)


class TestBoltBridge:
    """Tests du BoltBridge"""

    @pytest.fixture
    def bridge(self):
        """Fixture bridge"""
        return BoltBridge(
            base_url="http://localhost:5173",
            default_provider=Provider.ANTHROPIC
        )

    def test_init(self, bridge):
        """Test initialisation"""
        assert bridge.base_url == "http://localhost:5173"
        assert bridge.default_provider == Provider.ANTHROPIC
        assert bridge.client is not None

    @pytest.mark.asyncio
    async def test_health_success(self, bridge):
        """Test health check success"""
        with patch.object(bridge.client, 'get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = MagicMock(
                json=lambda: {"status": "healthy"}
            )

            result = await bridge.health()
            assert result["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_health_error(self, bridge):
        """Test health check error"""
        with patch.object(bridge.client, 'get', new_callable=AsyncMock) as mock_get:
            mock_get.side_effect = Exception("Connection refused")

            result = await bridge.health()
            assert result["status"] == "error"
            assert "Connection refused" in result["error"]

    @pytest.mark.asyncio
    async def test_create_project(self, bridge):
        """Test création de projet"""
        with patch.object(bridge.client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value = MagicMock(
                json=lambda: {
                    "id": "proj-123",
                    "name": "test-project",
                    "template": "react",
                    "path": "/projects/test-project",
                    "created_at": datetime.utcnow().isoformat(),
                    "files": []
                },
                raise_for_status=lambda: None
            )

            project = await bridge.create_project("test-project", Template.REACT)

            assert project.id == "proj-123"
            assert project.name == "test-project"
            assert project.template == "react"

    @pytest.mark.asyncio
    async def test_generate_code_success(self, bridge):
        """Test génération de code"""
        with patch.object(bridge.client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value = MagicMock(
                json=lambda: {
                    "files": {"src/main.py": "print('hello')"},
                    "messages": ["Generated successfully"],
                    "tokensUsed": 100
                },
                raise_for_status=lambda: None
            )

            result = await bridge.generate_code("Create a hello world")

            assert result.success is True
            assert "src/main.py" in result.files
            assert result.tokens_used == 100

    @pytest.mark.asyncio
    async def test_generate_code_error(self, bridge):
        """Test génération de code avec erreur"""
        with patch.object(bridge.client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.side_effect = Exception("API Error")

            result = await bridge.generate_code("Create something")

            assert result.success is False
            assert "API Error" in result.messages[0]

    @pytest.mark.asyncio
    async def test_edit_file(self, bridge):
        """Test édition de fichier"""
        with patch.object(bridge.client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value = MagicMock(
                json=lambda: {
                    "content": "updated content",
                    "messages": []
                },
                raise_for_status=lambda: None
            )

            result = await bridge.edit_file(
                "proj-123",
                "src/main.py",
                "Add a comment"
            )

            assert result.success is True
            assert "src/main.py" in result.files

    @pytest.mark.asyncio
    async def test_execute_command(self, bridge):
        """Test exécution de commande"""
        with patch.object(bridge.client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value = MagicMock(
                json=lambda: {
                    "exitCode": 0,
                    "stdout": "Success",
                    "stderr": ""
                },
                raise_for_status=lambda: None
            )

            result = await bridge.execute_command("proj-123", "npm test")

            assert result.success is True
            assert result.exit_code == 0
            assert result.stdout == "Success"

    @pytest.mark.asyncio
    async def test_run_tests_auto_detect(self, bridge):
        """Test auto-détection commande de test"""
        with patch.object(bridge, 'get_project', new_callable=AsyncMock) as mock_proj:
            mock_proj.return_value = Project(
                id="proj-123",
                name="test",
                template="react",
                path="/test",
                created_at=datetime.utcnow()
            )

            with patch.object(bridge, 'read_file', new_callable=AsyncMock) as mock_read:
                mock_read.return_value = '{"scripts": {"test": "jest"}}'

                with patch.object(bridge, 'execute_command', new_callable=AsyncMock) as mock_exec:
                    mock_exec.return_value = CommandResult(
                        success=True,
                        exit_code=0,
                        stdout="Tests passed",
                        stderr="",
                        duration_ms=1000
                    )

                    result = await bridge.run_tests("proj-123")

                    # Vérifie que npm test est utilisé
                    mock_exec.assert_called_once_with("proj-123", "npm test")


class TestProvider:
    """Tests de l'enum Provider"""

    def test_provider_values(self):
        """Test valeurs des providers"""
        assert Provider.ANTHROPIC.value == "anthropic"
        assert Provider.OPENAI.value == "openai"
        assert Provider.DEEPSEEK.value == "deepseek"
        assert Provider.GROQ.value == "groq"


class TestTemplate:
    """Tests de l'enum Template"""

    def test_template_values(self):
        """Test valeurs des templates"""
        assert Template.REACT.value == "react"
        assert Template.NEXTJS.value == "nextjs"
        assert Template.FASTAPI.value == "fastapi"

    def test_iafactory_templates(self):
        """Test templates IA Factory"""
        assert Template.IAFACTORY_FASTAPI.value == "iafactory-fastapi"
        assert Template.IAFACTORY_NEXTJS.value == "iafactory-nextjs"
        assert Template.IAFACTORY_GOV_AGENT.value == "iafactory-gov-agent"


class TestModels:
    """Tests des modèles Pydantic"""

    def test_generation_result(self):
        """Test GenerationResult"""
        result = GenerationResult(
            success=True,
            files={"main.py": "code"},
            tokens_used=50
        )
        assert result.success is True
        assert result.files["main.py"] == "code"
        assert result.tokens_used == 50

    def test_command_result(self):
        """Test CommandResult"""
        result = CommandResult(
            success=True,
            exit_code=0,
            stdout="output",
            stderr="",
            duration_ms=100
        )
        assert result.success is True
        assert result.exit_code == 0

    def test_project(self):
        """Test Project"""
        project = Project(
            id="123",
            name="test",
            template="react",
            path="/test",
            created_at=datetime.utcnow()
        )
        assert project.id == "123"
        assert project.files == []
