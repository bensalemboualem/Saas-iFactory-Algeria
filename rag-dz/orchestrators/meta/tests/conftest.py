"""Configuration pytest pour les tests Meta-Orchestrator"""

import sys
from pathlib import Path

import pytest

# Ajouter le dossier parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def anyio_backend():
    """Backend pour tests async"""
    return "asyncio"
