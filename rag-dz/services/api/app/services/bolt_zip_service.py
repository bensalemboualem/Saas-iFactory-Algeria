"""
Service pour générer les fichiers ZIP des projets Bolt
"""
import logging
import os
import zipfile
import shutil
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import asyncpg

from app.models.bolt_workflow import ProjectSynthesis, AgentResult

logger = logging.getLogger(__name__)


class BoltZipService:
    """Service pour créer et gérer les ZIP des projets"""

    def __init__(self, db_pool: asyncpg.Pool):
        self.db_pool = db_pool
        self.zip_storage_dir = Path("/tmp/bolt_projects")  # À configurer via env
        self.zip_storage_dir.mkdir(parents=True, exist_ok=True)

    async def create_project_zip(
        self,
        workflow_id: str,
        generated_code: Optional[Dict[str, Any]] = None,
        synthesis: Optional[ProjectSynthesis] = None,
        agent_results: Optional[Dict[str, AgentResult]] = None,
        include_docs: bool = True,
        include_tests: bool = True,
        include_deployment: bool = True
    ) -> str:
        """
        Crée un fichier ZIP complet du projet

        Args:
            workflow_id: ID du workflow
            generated_code: Code généré (depuis mode direct ou synthesis)
            synthesis: Synthèse du projet (mode BMAD)
            agent_results: Résultats des agents (mode BMAD)
            include_docs: Inclure la documentation
            include_tests: Inclure les tests
            include_deployment: Inclure les configs de déploiement

        Returns:
            Chemin du fichier ZIP créé
        """
        try:
            # Créer un répertoire temporaire pour le projet
            project_dir = self.zip_storage_dir / f"project-{workflow_id}"

            # Nettoyer si existe déjà
            if project_dir.exists():
                shutil.rmtree(project_dir)

            project_dir.mkdir(parents=True)

            logger.info(f"Creating project structure in {project_dir}")

            # Créer la structure du projet
            await self._create_project_structure(
                project_dir=project_dir,
                generated_code=generated_code,
                synthesis=synthesis,
                agent_results=agent_results,
                include_docs=include_docs,
                include_tests=include_tests,
                include_deployment=include_deployment
            )

            # Créer le fichier ZIP
            zip_path = self.zip_storage_dir / f"project-{workflow_id}.zip"

            logger.info(f"Creating ZIP file: {zip_path}")

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(project_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, project_dir)
                        zipf.write(file_path, arcname)

            # Nettoyer le répertoire temporaire
            shutil.rmtree(project_dir)

            logger.info(f"ZIP created successfully: {zip_path}")

            return str(zip_path)

        except Exception as e:
            logger.error(f"Error creating project ZIP: {e}", exc_info=True)
            raise

    async def _create_project_structure(
        self,
        project_dir: Path,
        generated_code: Optional[Dict[str, Any]],
        synthesis: Optional[ProjectSynthesis],
        agent_results: Optional[Dict[str, AgentResult]],
        include_docs: bool,
        include_tests: bool,
        include_deployment: bool
    ):
        """Crée la structure complète du projet"""

        # 1. README.md principal
        await self._create_readme(project_dir, synthesis, generated_code)

        # 2. Documentation (si demandé)
        if include_docs:
            docs_dir = project_dir / "docs"
            docs_dir.mkdir(exist_ok=True)
            await self._create_documentation(docs_dir, synthesis, agent_results)

        # 3. Code source
        src_dir = project_dir / "src"
        src_dir.mkdir(exist_ok=True)
        await self._create_source_code(src_dir, generated_code, synthesis)

        # 4. Tests (si demandé)
        if include_tests:
            tests_dir = project_dir / "tests"
            tests_dir.mkdir(exist_ok=True)
            await self._create_tests(tests_dir, synthesis)

        # 5. Configuration de déploiement (si demandé)
        if include_deployment:
            await self._create_deployment_configs(project_dir, synthesis)

        # 6. Fichiers de configuration racine
        await self._create_root_configs(project_dir, synthesis)

    async def _create_readme(
        self,
        project_dir: Path,
        synthesis: Optional[ProjectSynthesis],
        generated_code: Optional[Dict[str, Any]]
    ):
        """Crée le README.md principal"""

        if synthesis:
            project_name = synthesis.project_name
            description = synthesis.description
            tech_stack = ", ".join(synthesis.tech_stack)
        else:
            project_name = "Generated Project"
            description = generated_code.get("prompt", "No description") if generated_code else "No description"
            tech_stack = ", ".join(generated_code.get("tech_stack", [])) if generated_code else "N/A"

        readme_content = f"""# {project_name}

{description}

## 🚀 Tech Stack

{tech_stack}

## 📋 Getting Started

### Prerequisites

- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- Docker (optional)

### Installation

1. Clone the repository
2. Install dependencies:

```bash
# Frontend
cd src/frontend
npm install

# Backend
cd src/backend
pip install -r requirements.txt
```

### Running the Application

```bash
# Development mode
npm run dev  # Frontend
python -m uvicorn main:app --reload  # Backend

# Production mode
docker-compose up -d
```

## 📚 Documentation

See the `docs/` directory for comprehensive documentation:

- [Architecture](docs/ARCHITECTURE.md)
- [API Design](docs/API_DESIGN.md)
- [Deployment](docs/DEPLOYMENT.md)

## 🧪 Testing

```bash
# Run all tests
npm test  # Frontend
pytest    # Backend

# With coverage
npm run test:coverage
pytest --cov
```

## 📦 Deployment

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for deployment instructions.

## 🤝 Contributing

This project was generated by Bolt SuperPower AI.

---

**Generated with Bolt-DIY + BMAD Agents**
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

        readme_path = project_dir / "README.md"
        readme_path.write_text(readme_content, encoding="utf-8")

    async def _create_documentation(
        self,
        docs_dir: Path,
        synthesis: Optional[ProjectSynthesis],
        agent_results: Optional[Dict[str, AgentResult]]
    ):
        """Crée les fichiers de documentation"""

        if not synthesis:
            return

        # ARCHITECTURE.md
        if synthesis.architecture:
            arch_path = docs_dir / "ARCHITECTURE.md"
            arch_path.write_text(
                f"# Architecture\n\n{synthesis.architecture}",
                encoding="utf-8"
            )

        # REQUIREMENTS.md
        if synthesis.requirements:
            req_path = docs_dir / "REQUIREMENTS.md"
            req_path.write_text(
                f"# Requirements\n\n{synthesis.requirements}",
                encoding="utf-8"
            )

        # API_DESIGN.md
        if synthesis.api_design:
            api_path = docs_dir / "API_DESIGN.md"
            api_path.write_text(
                f"# API Design\n\n{synthesis.api_design}",
                encoding="utf-8"
            )

        # UI_COMPONENTS.md
        if synthesis.ui_components:
            ui_path = docs_dir / "UI_COMPONENTS.md"
            ui_path.write_text(
                f"# UI Components\n\n{synthesis.ui_components}",
                encoding="utf-8"
            )

        # DEPLOYMENT.md
        if synthesis.deployment_strategy:
            deploy_path = docs_dir / "DEPLOYMENT.md"
            deploy_path.write_text(
                f"# Deployment Strategy\n\n{synthesis.deployment_strategy}",
                encoding="utf-8"
            )

        # TEST_PLAN.md
        if synthesis.test_plan:
            test_path = docs_dir / "TEST_PLAN.md"
            test_path.write_text(
                f"# Test Plan\n\n{synthesis.test_plan}",
                encoding="utf-8"
            )

        # AGENTS_CONTRIBUTIONS.md (si disponible)
        if agent_results:
            agents_path = docs_dir / "AGENTS_CONTRIBUTIONS.md"
            contributions_content = "# Agents Contributions\n\n"

            for agent_id, result in agent_results.items():
                contributions_content += f"## {result.agent_name}\n\n"
                contributions_content += f"{result.output or 'No output'}\n\n"
                contributions_content += "---\n\n"

            agents_path.write_text(contributions_content, encoding="utf-8")

    async def _create_source_code(
        self,
        src_dir: Path,
        generated_code: Optional[Dict[str, Any]],
        synthesis: Optional[ProjectSynthesis]
    ):
        """Crée les fichiers de code source"""

        if not generated_code:
            # Créer une structure minimale par défaut
            await self._create_default_structure(src_dir, synthesis)
            return

        # Parser le code généré et créer les fichiers
        raw_output = generated_code.get("raw_output", "")

        # Tenter de parser si c'est du JSON
        try:
            if raw_output.startswith("{"):
                files_structure = json.loads(raw_output)
                await self._create_files_from_json(src_dir, files_structure)
            else:
                # Créer un fichier unique avec tout le contenu
                await self._create_single_file_structure(src_dir, raw_output, synthesis)
        except json.JSONDecodeError:
            # Créer un fichier unique avec tout le contenu
            await self._create_single_file_structure(src_dir, raw_output, synthesis)

    async def _create_default_structure(
        self,
        src_dir: Path,
        synthesis: Optional[ProjectSynthesis]
    ):
        """Crée une structure de projet par défaut"""

        # Frontend
        frontend_dir = src_dir / "frontend"
        frontend_dir.mkdir(exist_ok=True)

        (frontend_dir / "src").mkdir(exist_ok=True)
        (frontend_dir / "public").mkdir(exist_ok=True)

        # package.json minimal
        package_json = {
            "name": "frontend",
            "version": "1.0.0",
            "scripts": {
                "dev": "vite",
                "build": "vite build"
            },
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0"
            }
        }

        (frontend_dir / "package.json").write_text(
            json.dumps(package_json, indent=2),
            encoding="utf-8"
        )

        # Backend
        backend_dir = src_dir / "backend"
        backend_dir.mkdir(exist_ok=True)

        (backend_dir / "app").mkdir(exist_ok=True)

        # requirements.txt minimal
        requirements = """fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
"""

        (backend_dir / "requirements.txt").write_text(requirements, encoding="utf-8")

        # main.py minimal
        main_py = """from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from Bolt SuperPower!"}
"""

        (backend_dir / "main.py").write_text(main_py, encoding="utf-8")

    async def _create_single_file_structure(
        self,
        src_dir: Path,
        content: str,
        synthesis: Optional[ProjectSynthesis]
    ):
        """Crée une structure avec tout le contenu dans un fichier"""

        generated_file = src_dir / "generated_code.txt"
        generated_file.write_text(content, encoding="utf-8")

        readme = src_dir / "README.md"
        readme.write_text(
            "# Generated Code\n\nThe generated code is in `generated_code.txt`.\n\n"
            "You may need to organize it into proper files and directories.",
            encoding="utf-8"
        )

    async def _create_files_from_json(
        self,
        src_dir: Path,
        files_structure: Dict[str, Any]
    ):
        """Crée les fichiers à partir d'une structure JSON"""

        for file_path, content in files_structure.items():
            full_path = src_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(str(content), encoding="utf-8")

    async def _create_tests(
        self,
        tests_dir: Path,
        synthesis: Optional[ProjectSynthesis]
    ):
        """Crée les fichiers de tests"""

        # Tests unitaires
        unit_dir = tests_dir / "unit"
        unit_dir.mkdir(exist_ok=True)

        test_example = """# Example Unit Test

def test_example():
    assert True, "Example test"
"""

        (unit_dir / "test_example.py").write_text(test_example, encoding="utf-8")

        # Tests d'intégration
        integration_dir = tests_dir / "integration"
        integration_dir.mkdir(exist_ok=True)

        integration_test = """# Example Integration Test

def test_integration_example():
    # TODO: Add integration tests
    pass
"""

        (integration_dir / "test_integration.py").write_text(integration_test, encoding="utf-8")

    async def _create_deployment_configs(
        self,
        project_dir: Path,
        synthesis: Optional[ProjectSynthesis]
    ):
        """Crée les configurations de déploiement"""

        # docker-compose.yml
        docker_compose = """version: '3.8'

services:
  backend:
    build: ./src/backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app

  frontend:
    build: ./src/frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
"""

        (project_dir / "docker-compose.yml").write_text(docker_compose, encoding="utf-8")

        # GitHub Actions
        github_dir = project_dir / ".github" / "workflows"
        github_dir.mkdir(parents=True, exist_ok=True)

        github_action = """name: CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          npm test
          pytest
"""

        (github_dir / "ci.yml").write_text(github_action, encoding="utf-8")

    async def _create_root_configs(
        self,
        project_dir: Path,
        synthesis: Optional[ProjectSynthesis]
    ):
        """Crée les fichiers de configuration racine"""

        # .gitignore
        gitignore = """# Dependencies
node_modules/
__pycache__/
*.pyc

# Environment
.env
.env.local

# Build
dist/
build/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
"""

        (project_dir / ".gitignore").write_text(gitignore, encoding="utf-8")

        # .env.example
        env_example = """# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/app

# API Keys
API_SECRET_KEY=change-me-in-production

# Frontend
VITE_API_URL=http://localhost:8000
"""

        (project_dir / ".env.example").write_text(env_example, encoding="utf-8")

    async def get_zip_info(self, zip_path: str) -> Dict[str, Any]:
        """Récupère les informations d'un fichier ZIP"""

        if not os.path.exists(zip_path):
            return {"error": "File not found"}

        stat = os.stat(zip_path)

        with zipfile.ZipFile(zip_path, 'r') as zipf:
            file_count = len(zipf.namelist())
            file_list = zipf.namelist()

        return {
            "path": zip_path,
            "size_bytes": stat.st_size,
            "size_mb": round(stat.st_size / (1024 * 1024), 2),
            "file_count": file_count,
            "files": file_list[:50],  # Limiter à 50 fichiers pour l'affichage
            "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat()
        }

    async def cleanup_old_zips(self, days: int = 7) -> int:
        """Nettoie les anciens fichiers ZIP"""

        count = 0
        cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)

        for zip_file in self.zip_storage_dir.glob("*.zip"):
            if zip_file.stat().st_ctime < cutoff_time:
                try:
                    zip_file.unlink()
                    count += 1
                    logger.info(f"Deleted old ZIP: {zip_file}")
                except Exception as e:
                    logger.error(f"Error deleting {zip_file}: {e}")

        logger.info(f"Cleaned up {count} old ZIP files")
        return count
