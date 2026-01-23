"""
Sync Services - Synchronisation BMAD et Bolt vers Archon KB
"""

import hashlib
from pathlib import Path
from datetime import datetime
from typing import Any

import httpx
from pydantic import BaseModel


class SyncResult(BaseModel):
    """Résultat d'une synchronisation"""
    source: str
    files_synced: int
    files_skipped: int
    files_failed: int
    timestamp: datetime
    details: list[dict] = []


class BMadSync:
    """
    Synchroniseur BMAD → Archon KB.
    Indexe automatiquement les artefacts BMAD (PRDs, specs, workflows).
    """

    # Patterns de fichiers BMAD à indexer
    PATTERNS = [
        "**/*.md",
        "**/*.yaml",
        "**/*.yml",
        "**/prd-*.md",
        "**/spec-*.md",
        "**/workflow-*.md",
    ]

    # Types de documents par pattern
    TYPE_MAP = {
        "prd": "prd",
        "spec": "spec",
        "workflow": "workflow",
        "architecture": "architecture",
        "story": "story",
        "epic": "epic",
    }

    def __init__(
        self,
        archon_url: str = "http://localhost:8181",
        cache_file: str = ".bmad_sync_cache.json"
    ):
        self.archon_url = archon_url
        self.cache_file = cache_file
        self._cache: dict[str, str] = {}
        self._load_cache()

    def _load_cache(self):
        """Charge le cache des fichiers déjà synchronisés"""
        import json
        try:
            cache_path = Path(self.cache_file)
            if cache_path.exists():
                self._cache = json.loads(cache_path.read_text())
        except Exception:
            self._cache = {}

    def _save_cache(self):
        """Sauvegarde le cache"""
        import json
        Path(self.cache_file).write_text(json.dumps(self._cache, indent=2))

    def _get_file_hash(self, path: Path) -> str:
        """Calcule le hash MD5 d'un fichier"""
        content = path.read_bytes()
        return hashlib.md5(content).hexdigest()

    def _detect_type(self, path: Path) -> str:
        """Détecte le type de document BMAD"""
        name = path.stem.lower()
        for prefix, doc_type in self.TYPE_MAP.items():
            if prefix in name:
                return doc_type
        return "doc"

    async def sync_artifacts(
        self,
        bmad_path: str,
        force: bool = False
    ) -> int:
        """
        Synchronise les artefacts BMAD vers Archon KB.

        Args:
            bmad_path: Chemin du dossier BMAD
            force: Force la re-synchronisation même si non modifié

        Returns:
            Nombre de fichiers synchronisés
        """
        path = Path(bmad_path)
        if not path.exists():
            raise ValueError(f"Path does not exist: {bmad_path}")

        synced = 0

        async with httpx.AsyncClient(base_url=self.archon_url, timeout=30.0) as client:
            for pattern in self.PATTERNS:
                for file_path in path.glob(pattern):
                    if not file_path.is_file():
                        continue

                    file_hash = self._get_file_hash(file_path)
                    cache_key = str(file_path)

                    # Skip si déjà sync et non modifié
                    if not force and cache_key in self._cache:
                        if self._cache[cache_key] == file_hash:
                            continue

                    try:
                        content = file_path.read_text(encoding="utf-8")
                        doc_type = self._detect_type(file_path)

                        await client.post("/api/ingest", json={
                            "content": content,
                            "type": doc_type,
                            "metadata": {
                                "source": "bmad",
                                "path": str(file_path),
                                "filename": file_path.name,
                                "synced_at": datetime.utcnow().isoformat()
                            }
                        })

                        self._cache[cache_key] = file_hash
                        synced += 1
                    except Exception:
                        pass  # Skip failed files

        self._save_cache()
        return synced

    async def sync_single(self, file_path: str) -> bool:
        """Synchronise un seul fichier"""
        path = Path(file_path)
        if not path.exists():
            return False

        async with httpx.AsyncClient(base_url=self.archon_url, timeout=30.0) as client:
            try:
                content = path.read_text(encoding="utf-8")
                doc_type = self._detect_type(path)

                response = await client.post("/api/ingest", json={
                    "content": content,
                    "type": doc_type,
                    "metadata": {
                        "source": "bmad",
                        "path": str(path),
                        "filename": path.name,
                        "synced_at": datetime.utcnow().isoformat()
                    }
                })
                return response.status_code == 200
            except Exception:
                return False


class BoltSync:
    """
    Synchroniseur Bolt → Archon KB.
    Indexe le code après chaque commit via hook post-commit.
    """

    # Extensions de code à indexer
    CODE_EXTENSIONS = {
        ".py", ".js", ".ts", ".tsx", ".jsx",
        ".go", ".rs", ".java", ".kt",
        ".vue", ".svelte", ".html", ".css", ".scss"
    }

    # Fichiers à ignorer
    IGNORE_PATTERNS = {
        "node_modules", "__pycache__", ".git", ".venv",
        "dist", "build", ".next", "coverage"
    }

    def __init__(
        self,
        archon_url: str = "http://localhost:8181",
        cache_file: str = ".bolt_sync_cache.json"
    ):
        self.archon_url = archon_url
        self.cache_file = cache_file
        self._cache: dict[str, str] = {}
        self._load_cache()

    def _load_cache(self):
        """Charge le cache"""
        import json
        try:
            cache_path = Path(self.cache_file)
            if cache_path.exists():
                self._cache = json.loads(cache_path.read_text())
        except Exception:
            self._cache = {}

    def _save_cache(self):
        """Sauvegarde le cache"""
        import json
        Path(self.cache_file).write_text(json.dumps(self._cache, indent=2))

    def _should_ignore(self, path: Path) -> bool:
        """Vérifie si le fichier doit être ignoré"""
        for part in path.parts:
            if part in self.IGNORE_PATTERNS:
                return True
        return False

    def _get_file_hash(self, path: Path) -> str:
        """Calcule le hash MD5"""
        return hashlib.md5(path.read_bytes()).hexdigest()

    async def sync_commit(
        self,
        repo_path: str,
        commit_sha: str | None = None
    ) -> SyncResult:
        """
        Synchronise les fichiers modifiés dans un commit.

        Args:
            repo_path: Chemin du repository
            commit_sha: SHA du commit (optionnel, utilise HEAD)

        Returns:
            Résultat de la synchronisation
        """
        import subprocess

        path = Path(repo_path)

        # Récupérer les fichiers modifiés
        if commit_sha:
            cmd = ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", commit_sha]
        else:
            cmd = ["git", "diff", "--name-only", "HEAD~1", "HEAD"]

        result = subprocess.run(
            cmd,
            cwd=path,
            capture_output=True,
            text=True
        )

        files = result.stdout.strip().split("\n") if result.stdout else []
        synced = 0
        skipped = 0
        failed = 0
        details = []

        async with httpx.AsyncClient(base_url=self.archon_url, timeout=30.0) as client:
            for file_name in files:
                file_path = path / file_name
                if not file_path.exists():
                    skipped += 1
                    continue

                if self._should_ignore(file_path):
                    skipped += 1
                    continue

                if file_path.suffix not in self.CODE_EXTENSIONS:
                    skipped += 1
                    continue

                try:
                    content = file_path.read_text(encoding="utf-8")
                    file_hash = self._get_file_hash(file_path)

                    await client.post("/api/ingest", json={
                        "content": content,
                        "type": "code",
                        "metadata": {
                            "source": "bolt",
                            "path": str(file_path),
                            "filename": file_path.name,
                            "language": file_path.suffix[1:],
                            "commit": commit_sha,
                            "synced_at": datetime.utcnow().isoformat()
                        }
                    })

                    self._cache[str(file_path)] = file_hash
                    synced += 1
                    details.append({"file": file_name, "status": "synced"})
                except Exception as e:
                    failed += 1
                    details.append({"file": file_name, "status": "failed", "error": str(e)})

        self._save_cache()

        return SyncResult(
            source="bolt",
            files_synced=synced,
            files_skipped=skipped,
            files_failed=failed,
            timestamp=datetime.utcnow(),
            details=details
        )

    async def sync_file(self, file_path: str) -> bool:
        """Synchronise un seul fichier de code"""
        path = Path(file_path)
        if not path.exists() or path.suffix not in self.CODE_EXTENSIONS:
            return False

        async with httpx.AsyncClient(base_url=self.archon_url, timeout=30.0) as client:
            try:
                content = path.read_text(encoding="utf-8")

                response = await client.post("/api/ingest", json={
                    "content": content,
                    "type": "code",
                    "metadata": {
                        "source": "bolt",
                        "path": str(path),
                        "filename": path.name,
                        "language": path.suffix[1:],
                        "synced_at": datetime.utcnow().isoformat()
                    }
                })
                return response.status_code == 200
            except Exception:
                return False


# ============ GIT HOOKS ============

POST_COMMIT_HOOK = """#!/bin/bash
# Nexus Bolt Sync - Post-commit hook
# Synchronise les fichiers modifiés vers Archon KB

COMMIT_SHA=$(git rev-parse HEAD)
REPO_PATH=$(git rev-parse --show-toplevel)

# Appeler le service de sync
curl -s -X POST "http://localhost:8100/sync/bolt" \\
    -H "Content-Type: application/json" \\
    -d "{\\"repo_path\\": \\"$REPO_PATH\\", \\"commit_sha\\": \\"$COMMIT_SHA\\"}" \\
    > /dev/null 2>&1 &

# Ne pas bloquer le commit
exit 0
"""


def install_git_hook(repo_path: str) -> bool:
    """
    Installe le hook post-commit pour la synchronisation Bolt.

    Args:
        repo_path: Chemin du repository Git

    Returns:
        True si installé avec succès
    """
    hooks_dir = Path(repo_path) / ".git" / "hooks"
    hook_path = hooks_dir / "post-commit"

    try:
        hooks_dir.mkdir(parents=True, exist_ok=True)
        hook_path.write_text(POST_COMMIT_HOOK)
        hook_path.chmod(0o755)
        return True
    except Exception:
        return False
