"""Tests pour le Conflict Resolver"""

import pytest
from src.conflicts import (
    ConflictResolver, ConflictType, Resolution,
    Agent, VetoError, PRIORITY_RULES
)


class TestConflictResolver:
    """Tests du résolveur de conflits"""

    @pytest.fixture
    def resolver(self):
        return ConflictResolver()

    def test_file_creation_bolt_wins(self, resolver):
        """Test: Bolt gagne toujours pour création de fichiers"""
        result = resolver.resolve(
            ConflictType.FILE_CREATION,
            ["bmad", "bolt", "archon"]
        )
        assert result.winner == "bolt"
        assert "bmad" in result.losers
        assert "archon" in result.losers

    def test_documentation_bmad_wins(self, resolver):
        """Test: BMAD prioritaire pour documentation"""
        result = resolver.resolve(
            ConflictType.DOCUMENTATION,
            ["bolt", "bmad", "archon"]
        )
        assert result.winner == "bmad"

    def test_knowledge_update_archon_wins(self, resolver):
        """Test: Archon prioritaire pour KB"""
        result = resolver.resolve(
            ConflictType.KNOWLEDGE_UPDATE,
            ["bolt", "bmad", "archon"]
        )
        assert result.winner == "archon"

    def test_task_status_archon_only(self, resolver):
        """Test: Seul Archon peut modifier les statuts de tâches"""
        result = resolver.resolve(
            ConflictType.TASK_STATUS,
            ["bolt", "archon"]
        )
        assert result.winner == "archon"

    def test_single_writer_bolt_allowed(self, resolver):
        """Test: Bolt peut écrire"""
        assert resolver.check_single_writer("bolt", "write") is True
        assert resolver.check_single_writer("bolt", "create") is True
        assert resolver.check_single_writer("bolt", "modify") is True

    def test_single_writer_others_denied(self, resolver):
        """Test: Autres agents ne peuvent pas écrire"""
        assert resolver.check_single_writer("bmad", "write") is False
        assert resolver.check_single_writer("archon", "create") is False
        assert resolver.check_single_writer("validator", "modify") is False

    def test_single_writer_read_allowed_all(self, resolver):
        """Test: Tous peuvent lire"""
        assert resolver.check_single_writer("bmad", "read") is True
        assert resolver.check_single_writer("archon", "query") is True

    def test_veto_validator_on_code(self, resolver):
        """Test: Validator peut veto sur validation de code"""
        assert resolver.can_veto("validator", ConflictType.CODE_VALIDATION) is True

    def test_veto_security_on_files(self, resolver):
        """Test: Security peut veto sur fichiers"""
        assert resolver.can_veto("security", ConflictType.FILE_CREATION) is True
        assert resolver.can_veto("security", ConflictType.FILE_MODIFICATION) is True

    def test_veto_bmad_cannot(self, resolver):
        """Test: BMAD ne peut pas veto"""
        assert resolver.can_veto("bmad", ConflictType.FILE_CREATION) is False

    def test_write_permission_bolt_allowed(self, resolver):
        """Test: Bolt autorisé à écrire"""
        perm = resolver.get_write_permission("bolt", "src/main.py")
        assert perm["allowed"] is True

    def test_write_permission_others_denied(self, resolver):
        """Test: Autres agents refusés"""
        perm = resolver.get_write_permission("bmad", "src/main.py")
        assert perm["allowed"] is False

    def test_write_permission_protected_path(self, resolver):
        """Test: Chemins protégés nécessitent validation"""
        perm = resolver.get_write_permission("bolt", "migrations/001.sql")
        assert perm["allowed"] is True
        assert perm["requires_validation"] is True
        assert "security" in perm["validators"]

    def test_write_permission_auth_protected(self, resolver):
        """Test: auth/ est protégé"""
        perm = resolver.get_write_permission("bolt", "auth/login.py")
        assert perm["requires_validation"] is True
        assert "security" in perm["validators"]

    def test_resolution_has_timestamp(self, resolver):
        """Test: Resolution a un timestamp"""
        result = resolver.resolve(
            ConflictType.FILE_CREATION,
            ["bolt", "bmad"]
        )
        assert result.timestamp is not None

    def test_resolution_veto_possible(self, resolver):
        """Test: veto_possible quand validator présent"""
        result = resolver.resolve(
            ConflictType.CODE_VALIDATION,
            ["bolt", "validator"]
        )
        assert result.veto_possible is True
        assert "validator" in result.veto_by
