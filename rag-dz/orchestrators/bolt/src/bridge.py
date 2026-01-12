"""
Bolt Bridge - Interface vers bolt.diy pour la génération de code
SEUL WRITER autorisé dans l'architecture Nexus
"""

import os
from pathlib import Path
from typing import Any
from datetime import datetime
from enum import Enum

import httpx
from pydantic import BaseModel, Field


class Provider(str, Enum):
    """Providers LLM supportés par Bolt"""
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    DEEPSEEK = "deepseek"
    GROQ = "groq"
    GEMINI = "gemini"
    OLLAMA = "ollama"


class Template(str, Enum):
    """Templates de projets disponibles"""
    REACT = "react"
    NEXTJS = "nextjs"
    VUE = "vue"
    SVELTE = "svelte"
    ASTRO = "astro"
    FASTAPI = "fastapi"
    EXPRESS = "express"
    # Templates IA Factory
    IAFACTORY_FASTAPI = "iafactory-fastapi"
    IAFACTORY_NEXTJS = "iafactory-nextjs"
    IAFACTORY_GOV_AGENT = "iafactory-gov-agent"


class GenerationResult(BaseModel):
    """Résultat d'une génération de code"""
    success: bool
    files: dict[str, str] = Field(default_factory=dict)  # path -> content
    messages: list[str] = Field(default_factory=list)
    tokens_used: int = 0
    duration_ms: int = 0
    provider: str | None = None


class CommandResult(BaseModel):
    """Résultat d'une commande exécutée"""
    success: bool
    exit_code: int
    stdout: str
    stderr: str
    duration_ms: int


class Project(BaseModel):
    """Projet Bolt"""
    id: str
    name: str
    template: str
    path: str
    created_at: datetime
    files: list[str] = Field(default_factory=list)


class BoltBridge:
    """
    Bridge vers bolt.diy pour la génération et exécution de code.
    C'est le SEUL composant autorisé à écrire du code (Single-Writer Rule).
    """

    def __init__(
        self,
        base_url: str = "http://localhost:5173",
        timeout: float = 120.0,
        default_provider: Provider = Provider.ANTHROPIC
    ):
        self.base_url = base_url
        self.default_provider = default_provider
        self.client = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
            headers={"Content-Type": "application/json"}
        )

    async def close(self):
        """Ferme le client HTTP"""
        await self.client.aclose()

    # ============ HEALTH ============

    async def health(self) -> dict:
        """Vérifie la santé de Bolt"""
        try:
            response = await self.client.get("/api/health")
            return response.json()
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def get_providers(self) -> list[str]:
        """Liste les providers LLM disponibles"""
        try:
            response = await self.client.get("/api/providers")
            return response.json().get("providers", [])
        except Exception:
            return [p.value for p in Provider]

    # ============ PROJECTS ============

    async def create_project(
        self,
        name: str,
        template: Template | str,
        description: str | None = None
    ) -> Project:
        """
        Crée un nouveau projet.

        Args:
            name: Nom du projet
            template: Template à utiliser
            description: Description optionnelle

        Returns:
            Projet créé
        """
        template_str = template.value if isinstance(template, Template) else template

        response = await self.client.post("/api/projects", json={
            "name": name,
            "template": template_str,
            "description": description
        })
        response.raise_for_status()
        return Project(**response.json())

    async def get_project(self, project_id: str) -> Project | None:
        """Récupère un projet par ID"""
        try:
            response = await self.client.get(f"/api/projects/{project_id}")
            response.raise_for_status()
            return Project(**response.json())
        except httpx.HTTPStatusError:
            return None

    async def list_projects(self) -> list[Project]:
        """Liste tous les projets"""
        response = await self.client.get("/api/projects")
        response.raise_for_status()
        return [Project(**p) for p in response.json()]

    async def delete_project(self, project_id: str) -> bool:
        """Supprime un projet"""
        try:
            response = await self.client.delete(f"/api/projects/{project_id}")
            return response.status_code == 200
        except Exception:
            return False

    # ============ CODE GENERATION ============

    async def generate_code(
        self,
        prompt: str,
        context: dict | None = None,
        provider: Provider | str | None = None,
        model: str | None = None,
        project_id: str | None = None
    ) -> GenerationResult:
        """
        Génère du code avec Bolt.

        Args:
            prompt: Description de ce qu'il faut générer
            context: Contexte (specs, fichiers existants, etc.)
            provider: Provider LLM à utiliser
            model: Modèle spécifique
            project_id: ID du projet cible

        Returns:
            Résultat de la génération
        """
        provider_str = (
            provider.value if isinstance(provider, Provider)
            else provider or self.default_provider.value
        )

        start_time = datetime.utcnow()

        try:
            response = await self.client.post("/api/generate", json={
                "prompt": prompt,
                "context": context or {},
                "provider": provider_str,
                "model": model,
                "projectId": project_id
            })
            response.raise_for_status()
            data = response.json()

            duration = (datetime.utcnow() - start_time).total_seconds() * 1000

            return GenerationResult(
                success=True,
                files=data.get("files", {}),
                messages=data.get("messages", []),
                tokens_used=data.get("tokensUsed", 0),
                duration_ms=int(duration),
                provider=provider_str
            )

        except Exception as e:
            duration = (datetime.utcnow() - start_time).total_seconds() * 1000
            return GenerationResult(
                success=False,
                messages=[str(e)],
                duration_ms=int(duration)
            )

    async def edit_file(
        self,
        project_id: str,
        file_path: str,
        instructions: str,
        provider: Provider | str | None = None
    ) -> GenerationResult:
        """
        Édite un fichier existant avec des instructions.

        Args:
            project_id: ID du projet
            file_path: Chemin du fichier à éditer
            instructions: Instructions d'édition
            provider: Provider LLM

        Returns:
            Résultat de l'édition
        """
        provider_str = (
            provider.value if isinstance(provider, Provider)
            else provider or self.default_provider.value
        )

        try:
            response = await self.client.post(
                f"/api/projects/{project_id}/edit",
                json={
                    "filePath": file_path,
                    "instructions": instructions,
                    "provider": provider_str
                }
            )
            response.raise_for_status()
            data = response.json()

            return GenerationResult(
                success=True,
                files={file_path: data.get("content", "")},
                messages=data.get("messages", [])
            )

        except Exception as e:
            return GenerationResult(
                success=False,
                messages=[str(e)]
            )

    async def write_file(
        self,
        project_id: str,
        file_path: str,
        content: str
    ) -> bool:
        """
        Écrit directement un fichier (sans génération LLM).

        Args:
            project_id: ID du projet
            file_path: Chemin du fichier
            content: Contenu à écrire

        Returns:
            True si succès
        """
        try:
            response = await self.client.put(
                f"/api/projects/{project_id}/files/{file_path}",
                json={"content": content}
            )
            return response.status_code == 200
        except Exception:
            return False

    async def read_file(
        self,
        project_id: str,
        file_path: str
    ) -> str | None:
        """Lit le contenu d'un fichier"""
        try:
            response = await self.client.get(
                f"/api/projects/{project_id}/files/{file_path}"
            )
            response.raise_for_status()
            return response.json().get("content")
        except Exception:
            return None

    # ============ COMMAND EXECUTION ============

    async def execute_command(
        self,
        project_id: str,
        command: str,
        timeout: int = 60
    ) -> CommandResult:
        """
        Exécute une commande dans le contexte d'un projet.

        Args:
            project_id: ID du projet
            command: Commande à exécuter
            timeout: Timeout en secondes

        Returns:
            Résultat de la commande
        """
        start_time = datetime.utcnow()

        try:
            response = await self.client.post(
                f"/api/projects/{project_id}/execute",
                json={"command": command, "timeout": timeout}
            )
            response.raise_for_status()
            data = response.json()

            duration = (datetime.utcnow() - start_time).total_seconds() * 1000

            return CommandResult(
                success=data.get("exitCode", 1) == 0,
                exit_code=data.get("exitCode", 1),
                stdout=data.get("stdout", ""),
                stderr=data.get("stderr", ""),
                duration_ms=int(duration)
            )

        except Exception as e:
            duration = (datetime.utcnow() - start_time).total_seconds() * 1000
            return CommandResult(
                success=False,
                exit_code=1,
                stdout="",
                stderr=str(e),
                duration_ms=int(duration)
            )

    async def run_tests(
        self,
        project_id: str,
        test_command: str | None = None
    ) -> CommandResult:
        """
        Exécute les tests d'un projet.

        Args:
            project_id: ID du projet
            test_command: Commande de test (auto-détectée si None)

        Returns:
            Résultat des tests
        """
        # Auto-détection de la commande de test
        if not test_command:
            project = await self.get_project(project_id)
            if project:
                # Vérifier package.json pour npm test
                pkg_content = await self.read_file(project_id, "package.json")
                if pkg_content:
                    test_command = "npm test"
                else:
                    # Sinon pytest par défaut
                    test_command = "pytest"
            else:
                test_command = "npm test"

        return await self.execute_command(project_id, test_command)

    async def install_dependencies(self, project_id: str) -> CommandResult:
        """Installe les dépendances du projet"""
        return await self.execute_command(project_id, "npm install", timeout=120)

    async def build(self, project_id: str) -> CommandResult:
        """Build le projet"""
        return await self.execute_command(project_id, "npm run build", timeout=120)

    # ============ DEPLOYMENT ============

    async def deploy(
        self,
        project_id: str,
        target: str = "preview",
        options: dict | None = None
    ) -> dict:
        """
        Déploie un projet.

        Args:
            project_id: ID du projet
            target: Cible (preview, production)
            options: Options de déploiement

        Returns:
            Résultat du déploiement
        """
        try:
            response = await self.client.post(
                f"/api/projects/{project_id}/deploy",
                json={
                    "target": target,
                    "options": options or {}
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============ GIT OPERATIONS ============

    async def git_commit(
        self,
        project_id: str,
        message: str
    ) -> CommandResult:
        """Effectue un git commit"""
        return await self.execute_command(
            project_id,
            f'git add . && git commit -m "{message}"'
        )

    async def git_push(self, project_id: str) -> CommandResult:
        """Effectue un git push"""
        return await self.execute_command(project_id, "git push")
