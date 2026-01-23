"""Tests pour les Sync Services"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from pathlib import Path
import tempfile
import os

from src.sync import BMadSync, BoltSync, install_git_hook


class TestBMadSync:
    """Tests du synchroniseur BMAD"""

    @pytest.fixture
    def mock_client(self):
        """Mock HTTP client"""
        mock = AsyncMock()
        mock.post = AsyncMock(return_value=MagicMock(status_code=200))
        mock.__aenter__ = AsyncMock(return_value=mock)
        mock.__aexit__ = AsyncMock()
        return mock

    @pytest.fixture
    def temp_bmad_dir(self):
        """Crée un dossier temporaire avec des fichiers BMAD"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Créer des fichiers de test
            (Path(tmpdir) / "prd-feature.md").write_text("# PRD Feature\nContent")
            (Path(tmpdir) / "spec-api.md").write_text("# API Spec\nContent")
            (Path(tmpdir) / "workflow-deploy.md").write_text("# Deploy Workflow\nContent")
            (Path(tmpdir) / "readme.md").write_text("# README\nContent")
            yield tmpdir

    def test_detect_type_prd(self):
        """Test détection type PRD"""
        sync = BMadSync()
        assert sync._detect_type(Path("prd-feature.md")) == "prd"

    def test_detect_type_spec(self):
        """Test détection type Spec"""
        sync = BMadSync()
        assert sync._detect_type(Path("spec-api.md")) == "spec"

    def test_detect_type_workflow(self):
        """Test détection type Workflow"""
        sync = BMadSync()
        assert sync._detect_type(Path("workflow-deploy.md")) == "workflow"

    def test_detect_type_default(self):
        """Test détection type par défaut"""
        sync = BMadSync()
        assert sync._detect_type(Path("readme.md")) == "doc"

    @pytest.mark.asyncio
    async def test_sync_artifacts(self, temp_bmad_dir, mock_client):
        """Test synchronisation des artefacts"""
        with patch('httpx.AsyncClient', return_value=mock_client):
            sync = BMadSync("http://localhost:8181")
            sync._cache = {}  # Clear cache

            count = await sync.sync_artifacts(temp_bmad_dir)
            assert count == 4  # 4 fichiers md

    @pytest.mark.asyncio
    async def test_sync_artifacts_with_cache(self, temp_bmad_dir, mock_client):
        """Test que les fichiers en cache sont ignorés"""
        with patch('httpx.AsyncClient', return_value=mock_client):
            sync = BMadSync("http://localhost:8181")

            # Premier sync
            count1 = await sync.sync_artifacts(temp_bmad_dir)
            assert count1 == 4

            # Deuxième sync - devrait être 0 (tous en cache)
            count2 = await sync.sync_artifacts(temp_bmad_dir)
            assert count2 == 0

    @pytest.mark.asyncio
    async def test_sync_artifacts_force(self, temp_bmad_dir, mock_client):
        """Test force resync"""
        with patch('httpx.AsyncClient', return_value=mock_client):
            sync = BMadSync("http://localhost:8181")

            # Premier sync
            await sync.sync_artifacts(temp_bmad_dir)

            # Force sync
            count = await sync.sync_artifacts(temp_bmad_dir, force=True)
            assert count == 4


class TestBoltSync:
    """Tests du synchroniseur Bolt"""

    @pytest.fixture
    def mock_client(self):
        """Mock HTTP client"""
        mock = AsyncMock()
        mock.post = AsyncMock(return_value=MagicMock(status_code=200))
        mock.__aenter__ = AsyncMock(return_value=mock)
        mock.__aexit__ = AsyncMock()
        return mock

    def test_should_ignore_node_modules(self):
        """Test ignore node_modules"""
        sync = BoltSync()
        assert sync._should_ignore(Path("node_modules/package/index.js")) is True

    def test_should_ignore_pycache(self):
        """Test ignore __pycache__"""
        sync = BoltSync()
        assert sync._should_ignore(Path("src/__pycache__/module.pyc")) is True

    def test_should_not_ignore_src(self):
        """Test ne pas ignorer src/"""
        sync = BoltSync()
        assert sync._should_ignore(Path("src/main.py")) is False

    @pytest.mark.asyncio
    async def test_sync_file(self, mock_client):
        """Test sync d'un fichier individuel"""
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
            f.write(b"print('hello')")
            f.flush()

            with patch('httpx.AsyncClient', return_value=mock_client):
                sync = BoltSync("http://localhost:8181")
                result = await sync.sync_file(f.name)
                assert result is True

            os.unlink(f.name)

    @pytest.mark.asyncio
    async def test_sync_file_non_code(self, mock_client):
        """Test que les fichiers non-code sont ignorés"""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            f.write(b"hello")
            f.flush()

            with patch('httpx.AsyncClient', return_value=mock_client):
                sync = BoltSync("http://localhost:8181")
                result = await sync.sync_file(f.name)
                assert result is False

            os.unlink(f.name)


class TestGitHook:
    """Tests pour l'installation du hook Git"""

    def test_install_git_hook(self):
        """Test installation du hook"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Créer structure .git
            git_dir = Path(tmpdir) / ".git" / "hooks"
            git_dir.mkdir(parents=True)

            result = install_git_hook(tmpdir)
            assert result is True

            hook_path = git_dir / "post-commit"
            assert hook_path.exists()

    def test_install_git_hook_no_git(self):
        """Test installation sans dossier .git"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Pas de .git - devrait créer le dossier
            result = install_git_hook(tmpdir)
            assert result is True
