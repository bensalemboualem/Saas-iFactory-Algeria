"""
Tests for API endpoints
"""
import pytest
from httpx import AsyncClient


class TestProjectsAPI:
    """Tests for /api/v1/projects endpoints"""

    @pytest.mark.asyncio
    async def test_create_project(self, client: AsyncClient, sample_project_data):
        """Test project creation"""
        response = await client.post("/api/v1/projects/", json=sample_project_data)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_project_data["title"]
        assert data["status"] == "draft"
        assert "id" in data

    @pytest.mark.asyncio
    async def test_get_project(self, client: AsyncClient, sample_project_data):
        """Test getting a project by ID"""
        # First create a project
        create_response = await client.post("/api/v1/projects/", json=sample_project_data)
        project_id = create_response.json()["id"]

        # Then get it
        response = await client.get(f"/api/v1/projects/{project_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == project_id
        assert data["title"] == sample_project_data["title"]

    @pytest.mark.asyncio
    async def test_get_nonexistent_project(self, client: AsyncClient):
        """Test getting a non-existent project"""
        response = await client.get("/api/v1/projects/nonexistent-id")

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_list_projects(self, client: AsyncClient, sample_project_data):
        """Test listing all projects"""
        # Create some projects
        await client.post("/api/v1/projects/", json=sample_project_data)
        await client.post("/api/v1/projects/", json={**sample_project_data, "title": "Project 2"})

        response = await client.get("/api/v1/projects/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2

    @pytest.mark.asyncio
    async def test_update_project(self, client: AsyncClient, sample_project_data):
        """Test updating a project"""
        # Create a project
        create_response = await client.post("/api/v1/projects/", json=sample_project_data)
        project_id = create_response.json()["id"]

        # Update it
        update_data = {"title": "Updated Title", "description": "Updated description"}
        response = await client.patch(f"/api/v1/projects/{project_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"

    @pytest.mark.asyncio
    async def test_delete_project(self, client: AsyncClient, sample_project_data):
        """Test deleting a project"""
        # Create a project
        create_response = await client.post("/api/v1/projects/", json=sample_project_data)
        project_id = create_response.json()["id"]

        # Delete it
        response = await client.delete(f"/api/v1/projects/{project_id}")

        assert response.status_code == 204

        # Verify it's gone
        get_response = await client.get(f"/api/v1/projects/{project_id}")
        assert get_response.status_code == 404


class TestScriptsAPI:
    """Tests for /api/v1/scripts endpoints"""

    @pytest.mark.asyncio
    async def test_generate_script(self, client: AsyncClient, sample_project_data):
        """Test script generation"""
        # Create a project first
        project_response = await client.post("/api/v1/projects/", json=sample_project_data)
        project_id = project_response.json()["id"]

        # Generate script
        response = await client.post(
            f"/api/v1/scripts/generate",
            json={"project_id": project_id, "prompt": sample_project_data["prompt"]}
        )

        assert response.status_code in [200, 201, 202]  # May be async

    @pytest.mark.asyncio
    async def test_get_script(self, client: AsyncClient):
        """Test getting a script"""
        # This would require a script to exist
        response = await client.get("/api/v1/scripts/nonexistent-id")

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_script(self, client: AsyncClient, sample_script_data):
        """Test updating a script"""
        # Would need to create a script first
        pass


class TestAssetsAPI:
    """Tests for /api/v1/assets endpoints"""

    @pytest.mark.asyncio
    async def test_generate_image(self, client: AsyncClient):
        """Test image generation"""
        response = await client.post(
            "/api/v1/assets/images/generate",
            json={"prompt": "A beautiful sunset", "size": "1024x1024"}
        )

        # May be async
        assert response.status_code in [200, 201, 202]

    @pytest.mark.asyncio
    async def test_generate_voice(self, client: AsyncClient):
        """Test voice generation"""
        response = await client.post(
            "/api/v1/assets/voice/generate",
            json={"text": "Hello world", "voice_id": "nova"}
        )

        assert response.status_code in [200, 201, 202]

    @pytest.mark.asyncio
    async def test_list_voices(self, client: AsyncClient):
        """Test listing available voices"""
        response = await client.get("/api/v1/assets/voices")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestVideosAPI:
    """Tests for /api/v1/videos endpoints"""

    @pytest.mark.asyncio
    async def test_render_video(self, client: AsyncClient, sample_timeline_data):
        """Test video rendering"""
        response = await client.post(
            "/api/v1/videos/render",
            json={"project_id": "test-project", "timeline": sample_timeline_data}
        )

        # Rendering is async
        assert response.status_code in [200, 202]

    @pytest.mark.asyncio
    async def test_get_render_status(self, client: AsyncClient):
        """Test getting render status"""
        response = await client.get("/api/v1/videos/status/nonexistent-task")

        # Should return status or 404
        assert response.status_code in [200, 404]


class TestPublishAPI:
    """Tests for /api/v1/publish endpoints"""

    @pytest.mark.asyncio
    async def test_publish_video(self, client: AsyncClient):
        """Test video publishing"""
        response = await client.post(
            "/api/v1/publish/",
            json={
                "project_id": "test-project",
                "platforms": ["youtube", "tiktok"],
                "title": "Test Video",
                "description": "Test description",
            }
        )

        # May need authentication
        assert response.status_code in [200, 202, 401, 403]

    @pytest.mark.asyncio
    async def test_get_publish_status(self, client: AsyncClient):
        """Test getting publish status"""
        response = await client.get("/api/v1/publish/status/nonexistent-id")

        assert response.status_code in [200, 404]


class TestHealthAPI:
    """Tests for health check endpoints"""

    @pytest.mark.asyncio
    async def test_health_check(self, client: AsyncClient):
        """Test health check endpoint"""
        response = await client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_ready_check(self, client: AsyncClient):
        """Test readiness check endpoint"""
        response = await client.get("/ready")

        assert response.status_code == 200


class TestAPIValidation:
    """Tests for API input validation"""

    @pytest.mark.asyncio
    async def test_create_project_invalid_data(self, client: AsyncClient):
        """Test project creation with invalid data"""
        response = await client.post("/api/v1/projects/", json={})

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_create_project_missing_title(self, client: AsyncClient):
        """Test project creation without title"""
        response = await client.post(
            "/api/v1/projects/",
            json={"description": "No title"}
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_generate_image_invalid_size(self, client: AsyncClient):
        """Test image generation with invalid size"""
        response = await client.post(
            "/api/v1/assets/images/generate",
            json={"prompt": "test", "size": "invalid"}
        )

        assert response.status_code in [400, 422]
