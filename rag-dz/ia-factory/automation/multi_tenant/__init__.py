"""
IA Factory Automation - Multi-tenant Package
"""

from .infrastructure import router as infra_router
from .infrastructure import MultiTenantManager, TIER_RESOURCES, SERVER_SPECS

__all__ = [
    "infra_router",
    "MultiTenantManager",
    "TIER_RESOURCES",
    "SERVER_SPECS"
]
