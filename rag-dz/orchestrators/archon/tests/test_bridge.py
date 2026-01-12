"""Tests pour le Archon Bridge"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime

from src.bridge import (
    ArchonBridge, Document, SearchResult, Project, Task
)


class TestArchonBridge:
    """Tests du bridge Archon"""

    @pytest.fixture
    def mock_client(self):
        """Mock HTTP client"""
        mock = AsyncMock()
        mock.post = AsyncMock()
        mock.get = AsyncMock()
        mock.patch = AsyncMock()
        mock.delete = AsyncMock()
        mock.aclose = AsyncMock()
        return mock

    @pytest.fixture
    def bridge(self, mock_client):
        """Bridge avec mock client"""
        with patch('httpx.AsyncClient', return_value=mock_client):
            b = ArchonBridge("http://localhost:8181")
            b.client = mock_client
            return b

    @pytest.mark.asyncio
    async def test_health_success(self, bridge):
        """Test health check réussi"""
        bridge.client.get.return_value = MagicMock(
            json=lambda: {"status": "healthy"}
        )
        result = await bridge.health()
        assert result["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_health_error(self, bridge):
        """Test health check en erreur"""
        bridge.client.get.side_effect = Exception("Connection refused")
        result = await bridge.health()
        assert result["status"] == "error"

    @pytest.mark.asyncio
    async def test_search(self, bridge):
        """Test recherche KB"""
        bridge.client.post.return_value = MagicMock(
            json=lambda: {
                "results": [
                    {
                        "document": {
                            "id": "doc1",
                            "content": "Test content",
                            "type": "doc",
                            "metadata": {}
                        },
                        "score": 0.95,
                        "highlights": ["Test"]
                    }
                ]
            },
            raise_for_status=lambda: None
        )

        results = await bridge.search("test query")
        assert len(results) == 1
        assert results[0].score == 0.95
        assert results[0].document.id == "doc1"

    @pytest.mark.asyncio
    async def test_ingest(self, bridge):
        """Test ingestion document"""
        bridge.client.post.return_value = MagicMock(
            json=lambda: {
                "id": "new-doc",
                "content": "New content",
                "type": "doc",
                "metadata": {"source": "test"}
            },
            raise_for_status=lambda: None
        )

        doc = await bridge.ingest("New content", "doc", {"source": "test"})
        assert doc.id == "new-doc"
        assert doc.type == "doc"

    @pytest.mark.asyncio
    async def test_create_project(self, bridge):
        """Test création projet"""
        bridge.client.post.return_value = MagicMock(
            json=lambda: {
                "id": "proj1",
                "name": "Test Project",
                "description": "A test project",
                "status": "active"
            },
            raise_for_status=lambda: None
        )

        project = await bridge.create_project("Test Project", "A test project")
        assert project.id == "proj1"
        assert project.name == "Test Project"

    @pytest.mark.asyncio
    async def test_create_task(self, bridge):
        """Test création tâche"""
        bridge.client.post.return_value = MagicMock(
            json=lambda: {
                "id": "task1",
                "project_id": "proj1",
                "title": "Test Task",
                "description": "A test task",
                "status": "todo"
            },
            raise_for_status=lambda: None
        )

        task = await bridge.create_task("proj1", "Test Task", "A test task")
        assert task.id == "task1"
        assert task.status == "todo"

    @pytest.mark.asyncio
    async def test_update_task_status(self, bridge):
        """Test mise à jour statut tâche"""
        bridge.client.patch.return_value = MagicMock(
            json=lambda: {
                "id": "task1",
                "project_id": "proj1",
                "title": "Test Task",
                "description": "A test task",
                "status": "doing"
            },
            raise_for_status=lambda: None
        )

        task = await bridge.update_task_status("task1", "doing")
        assert task.status == "doing"

    @pytest.mark.asyncio
    async def test_list_projects(self, bridge):
        """Test liste projets"""
        bridge.client.get.return_value = MagicMock(
            json=lambda: [
                {"id": "p1", "name": "Project 1", "description": "Desc 1", "status": "active"},
                {"id": "p2", "name": "Project 2", "description": "Desc 2", "status": "active"}
            ],
            raise_for_status=lambda: None
        )

        projects = await bridge.list_projects()
        assert len(projects) == 2

    @pytest.mark.asyncio
    async def test_list_tasks(self, bridge):
        """Test liste tâches"""
        bridge.client.get.return_value = MagicMock(
            json=lambda: [
                {"id": "t1", "project_id": "p1", "title": "Task 1", "description": "D1", "status": "todo"},
                {"id": "t2", "project_id": "p1", "title": "Task 2", "description": "D2", "status": "doing"}
            ],
            raise_for_status=lambda: None
        )

        tasks = await bridge.list_tasks("p1")
        assert len(tasks) == 2

    @pytest.mark.asyncio
    async def test_close(self, bridge):
        """Test fermeture client"""
        await bridge.close()
        bridge.client.aclose.assert_called_once()
