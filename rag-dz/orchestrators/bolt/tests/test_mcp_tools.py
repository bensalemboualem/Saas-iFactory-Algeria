"""Tests pour les MCP Tools Bolt"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from src.mcp_tools import (
    BoltMCPServer,
    MCPToolDefinition,
    BOLT_TOOLS,
)
from src.bridge import BoltBridge, Provider, Template, Project, GenerationResult, CommandResult
from src.executor import BoltExecutor, Task, TaskStatus, ExecutionResult
from datetime import datetime


class TestBoltTools:
    """Tests des définitions de tools"""

    def test_tools_count(self):
        """Test nombre de tools"""
        assert len(BOLT_TOOLS) == 11

    def test_all_tools_have_name(self):
        """Test que tous les tools ont un nom"""
        for tool in BOLT_TOOLS:
            assert tool.name
            assert tool.name.startswith("bolt_")

    def test_all_tools_have_description(self):
        """Test que tous les tools ont une description"""
        for tool in BOLT_TOOLS:
            assert tool.description
            assert len(tool.description) > 10

    def test_all_tools_have_schema(self):
        """Test que tous les tools ont un schema"""
        for tool in BOLT_TOOLS:
            assert tool.input_schema
            assert tool.input_schema.get("type") == "object"
            assert "properties" in tool.input_schema

    def test_create_project_tool(self):
        """Test tool create_project"""
        tool = next(t for t in BOLT_TOOLS if t.name == "bolt_create_project")
        assert "name" in tool.input_schema["properties"]
        assert "template" in tool.input_schema["properties"]
        assert "name" in tool.input_schema["required"]
        assert "template" in tool.input_schema["required"]

    def test_generate_code_tool(self):
        """Test tool generate_code"""
        tool = next(t for t in BOLT_TOOLS if t.name == "bolt_generate_code")
        assert "prompt" in tool.input_schema["properties"]
        assert "provider" in tool.input_schema["properties"]
        assert "prompt" in tool.input_schema["required"]

    def test_edit_file_tool(self):
        """Test tool edit_file"""
        tool = next(t for t in BOLT_TOOLS if t.name == "bolt_edit_file")
        assert "project_id" in tool.input_schema["properties"]
        assert "file_path" in tool.input_schema["properties"]
        assert "instructions" in tool.input_schema["properties"]

    def test_execute_command_tool(self):
        """Test tool execute_command"""
        tool = next(t for t in BOLT_TOOLS if t.name == "bolt_execute_command")
        assert "project_id" in tool.input_schema["properties"]
        assert "command" in tool.input_schema["properties"]

    def test_deploy_tool(self):
        """Test tool deploy"""
        tool = next(t for t in BOLT_TOOLS if t.name == "bolt_deploy")
        props = tool.input_schema["properties"]
        assert "target" in props
        assert "enum" in props["target"]
        assert "preview" in props["target"]["enum"]
        assert "production" in props["target"]["enum"]


class TestMCPToolDefinition:
    """Tests du modèle MCPToolDefinition"""

    def test_creation(self):
        """Test création"""
        tool = MCPToolDefinition(
            name="test_tool",
            description="A test tool",
            input_schema={"type": "object", "properties": {}}
        )
        assert tool.name == "test_tool"
        assert tool.description == "A test tool"


class TestBoltMCPServer:
    """Tests du serveur MCP"""

    @pytest.fixture
    def mock_bridge(self):
        """Mock du BoltBridge"""
        bridge = MagicMock(spec=BoltBridge)
        return bridge

    @pytest.fixture
    def mock_executor(self, mock_bridge):
        """Mock du BoltExecutor"""
        executor = MagicMock(spec=BoltExecutor)
        executor.bolt = mock_bridge
        return executor

    @pytest.fixture
    def server(self, mock_bridge, mock_executor):
        """Fixture serveur MCP"""
        return BoltMCPServer(mock_bridge, mock_executor)

    def test_get_tools(self, server):
        """Test récupération des tools"""
        tools = server.get_tools()
        assert len(tools) == 11
        assert all("name" in t for t in tools)
        assert all("description" in t for t in tools)
        assert all("inputSchema" in t for t in tools)

    @pytest.mark.asyncio
    async def test_execute_unknown_tool(self, server):
        """Test exécution tool inconnu"""
        result = await server.execute("unknown_tool", {})
        assert "error" in result
        assert "Unknown tool" in result["error"]

    @pytest.mark.asyncio
    async def test_execute_create_project(self, server, mock_bridge):
        """Test exécution create_project"""
        mock_bridge.create_project = AsyncMock(return_value=Project(
            id="proj-123",
            name="test",
            template="react",
            path="/test",
            created_at=datetime.utcnow()
        ))

        result = await server.execute("bolt_create_project", {
            "name": "test",
            "template": "react"
        })

        assert result["id"] == "proj-123"
        mock_bridge.create_project.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_generate_code(self, server, mock_bridge):
        """Test exécution generate_code"""
        mock_bridge.generate_code = AsyncMock(return_value=GenerationResult(
            success=True,
            files={"main.py": "code"},
            tokens_used=100
        ))

        result = await server.execute("bolt_generate_code", {
            "prompt": "Create hello world"
        })

        assert result["success"] is True
        assert "main.py" in result["files"]

    @pytest.mark.asyncio
    async def test_execute_edit_file(self, server, mock_bridge):
        """Test exécution edit_file"""
        mock_bridge.edit_file = AsyncMock(return_value=GenerationResult(
            success=True,
            files={"src/main.py": "updated"}
        ))

        result = await server.execute("bolt_edit_file", {
            "project_id": "proj-123",
            "file_path": "src/main.py",
            "instructions": "Add comment"
        })

        assert result["success"] is True

    @pytest.mark.asyncio
    async def test_execute_command(self, server, mock_bridge):
        """Test exécution execute_command"""
        mock_bridge.execute_command = AsyncMock(return_value=CommandResult(
            success=True,
            exit_code=0,
            stdout="output",
            stderr="",
            duration_ms=100
        ))

        result = await server.execute("bolt_execute_command", {
            "project_id": "proj-123",
            "command": "npm test"
        })

        assert result["success"] is True
        assert result["exit_code"] == 0

    @pytest.mark.asyncio
    async def test_execute_run_tests(self, server, mock_bridge):
        """Test exécution run_tests"""
        mock_bridge.run_tests = AsyncMock(return_value=CommandResult(
            success=True,
            exit_code=0,
            stdout="All tests passed",
            stderr="",
            duration_ms=5000
        ))

        result = await server.execute("bolt_run_tests", {
            "project_id": "proj-123"
        })

        assert result["success"] is True

    @pytest.mark.asyncio
    async def test_execute_deploy(self, server, mock_bridge):
        """Test exécution deploy"""
        mock_bridge.deploy = AsyncMock(return_value={
            "success": True,
            "url": "https://preview.example.com"
        })

        result = await server.execute("bolt_deploy", {
            "project_id": "proj-123",
            "target": "preview"
        })

        assert result["success"] is True
        assert "url" in result

    @pytest.mark.asyncio
    async def test_execute_list_templates(self, server):
        """Test exécution list_templates"""
        result = await server.execute("bolt_list_templates", {})

        assert "standard_templates" in result
        assert "iafactory_templates" in result
        assert "react" in result["standard_templates"]

    @pytest.mark.asyncio
    async def test_execute_get_template(self, server):
        """Test exécution get_template"""
        result = await server.execute("bolt_get_template", {
            "template_id": "iafactory-fastapi"
        })

        assert "template" in result
        assert "files" in result
        assert result["template"]["id"] == "iafactory-fastapi"

    @pytest.mark.asyncio
    async def test_execute_get_template_not_found(self, server):
        """Test get_template non trouvé"""
        result = await server.execute("bolt_get_template", {
            "template_id": "nonexistent"
        })

        assert "error" in result
        assert "not found" in result["error"]

    @pytest.mark.asyncio
    async def test_execute_task(self, server, mock_executor):
        """Test exécution execute_task"""
        mock_executor.execute_task = AsyncMock(return_value=ExecutionResult(
            task_id="task-123",
            status=TaskStatus.COMPLETED
        ))

        result = await server.execute("bolt_execute_task", {
            "project_id": "proj-123",
            "title": "Test task",
            "description": "Do something"
        })

        assert result["status"] == "completed"

    @pytest.mark.asyncio
    async def test_execute_quick_fix(self, server, mock_executor):
        """Test exécution quick_fix"""
        mock_executor.execute_quick_fix = AsyncMock(return_value=ExecutionResult(
            task_id="fix-123",
            status=TaskStatus.COMPLETED
        ))

        result = await server.execute("bolt_quick_fix", {
            "project_id": "proj-123",
            "file_path": "src/main.py",
            "fix_description": "Fix the bug"
        })

        assert result["status"] == "completed"

    @pytest.mark.asyncio
    async def test_execute_git_commit(self, server, mock_bridge):
        """Test exécution git_commit"""
        mock_bridge.git_commit = AsyncMock(return_value=CommandResult(
            success=True,
            exit_code=0,
            stdout="[main abc123] commit message",
            stderr="",
            duration_ms=500
        ))

        result = await server.execute("bolt_git_commit", {
            "project_id": "proj-123",
            "message": "Initial commit"
        })

        assert result["success"] is True

    @pytest.mark.asyncio
    async def test_execute_with_exception(self, server, mock_bridge):
        """Test exécution avec exception"""
        mock_bridge.create_project = AsyncMock(side_effect=Exception("Connection error"))

        result = await server.execute("bolt_create_project", {
            "name": "test",
            "template": "react"
        })

        assert "error" in result
        assert "Connection error" in result["error"]
