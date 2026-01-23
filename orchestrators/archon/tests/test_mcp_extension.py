"""Tests pour le MCP Extension"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from src.mcp_extension import (
    NexusMCPExtension, NEXUS_TOOLS, MCPTool, MCPToolResult
)


class TestNexusMCPExtension:
    """Tests de l'extension MCP Nexus"""

    @pytest.fixture
    def extension(self):
        """Extension MCP"""
        return NexusMCPExtension(
            meta_url="http://localhost:8100",
            archon_url="http://localhost:8181"
        )

    def test_tools_defined(self):
        """Test que les tools sont définis"""
        assert len(NEXUS_TOOLS) > 0
        for tool in NEXUS_TOOLS:
            assert isinstance(tool, MCPTool)
            assert tool.name
            assert tool.description
            assert tool.handler

    def test_get_tools(self, extension):
        """Test récupération des tools"""
        tools = extension.get_tools()
        assert len(tools) == len(NEXUS_TOOLS)

        for tool in tools:
            assert "name" in tool
            assert "description" in tool
            assert "inputSchema" in tool

    def test_nexus_route_tool_exists(self, extension):
        """Test que nexus_route existe"""
        assert "nexus_route" in extension.tools

    def test_nexus_lock_tool_exists(self, extension):
        """Test que nexus_lock existe"""
        assert "nexus_lock" in extension.tools

    def test_nexus_unlock_tool_exists(self, extension):
        """Test que nexus_unlock existe"""
        assert "nexus_unlock" in extension.tools

    def test_nexus_sync_bmad_tool_exists(self, extension):
        """Test que nexus_sync_bmad existe"""
        assert "nexus_sync_bmad" in extension.tools

    def test_nexus_task_status_tool_exists(self, extension):
        """Test que nexus_task_status existe"""
        assert "nexus_task_status" in extension.tools

    def test_nexus_check_permission_tool_exists(self, extension):
        """Test que nexus_check_permission existe"""
        assert "nexus_check_permission" in extension.tools

    @pytest.mark.asyncio
    async def test_execute_unknown_tool(self, extension):
        """Test exécution d'un tool inconnu"""
        result = await extension.execute("unknown_tool", {})
        assert result.success is False
        assert "Unknown tool" in result.error

    @pytest.mark.asyncio
    async def test_handle_route(self, extension):
        """Test handler route"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"target": "bmad", "confidence": 0.9}

        with patch('httpx.AsyncClient') as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_response
            mock_instance.__aenter__.return_value = mock_instance
            mock_instance.__aexit__.return_value = None
            mock_client.return_value = mock_instance

            result = await extension.handle_route({"request": "create workflow"})
            assert result["target"] == "bmad"

    @pytest.mark.asyncio
    async def test_handle_lock_success(self, extension):
        """Test handler lock réussi"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"resource": "test", "holder": "bolt"}

        with patch('httpx.AsyncClient') as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_response
            mock_instance.__aenter__.return_value = mock_instance
            mock_instance.__aexit__.return_value = None
            mock_client.return_value = mock_instance

            result = await extension.handle_lock({
                "resource": "test",
                "holder": "bolt"
            })
            assert result["locked"] is True

    @pytest.mark.asyncio
    async def test_handle_lock_conflict(self, extension):
        """Test handler lock en conflit"""
        mock_response = MagicMock()
        mock_response.status_code = 409

        with patch('httpx.AsyncClient') as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_response
            mock_instance.__aenter__.return_value = mock_instance
            mock_instance.__aexit__.return_value = None
            mock_client.return_value = mock_instance

            result = await extension.handle_lock({
                "resource": "test",
                "holder": "bmad"
            })
            assert result["locked"] is False

    @pytest.mark.asyncio
    async def test_handle_unlock(self, extension):
        """Test handler unlock"""
        mock_response = MagicMock()
        mock_response.status_code = 200

        with patch('httpx.AsyncClient') as mock_client:
            mock_instance = AsyncMock()
            mock_instance.delete.return_value = mock_response
            mock_instance.__aenter__.return_value = mock_instance
            mock_instance.__aexit__.return_value = None
            mock_client.return_value = mock_instance

            result = await extension.handle_unlock({
                "resource": "test",
                "holder": "bolt"
            })
            assert result["released"] is True

    @pytest.mark.asyncio
    async def test_handle_check_permission(self, extension):
        """Test handler check permission"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "allowed": True,
            "requires_validation": False
        }

        with patch('httpx.AsyncClient') as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_response
            mock_instance.__aenter__.return_value = mock_instance
            mock_instance.__aexit__.return_value = None
            mock_client.return_value = mock_instance

            result = await extension.handle_check_permission({
                "agent": "bolt",
                "path": "src/main.py",
                "operation": "write"
            })
            assert result["allowed"] is True
