"""
iaFactory API Portal - Backend Main Router
Module 16 - Regroupement des routes développeur
"""

from fastapi import APIRouter
from .routers.dev_api_keys import router as api_keys_router
from .routers.dev_usage import router as usage_router
from .routers.dev_playground import router as playground_router

# Router principal du Developer Portal
dev_portal_router = APIRouter()

# Inclure tous les sous-routers
dev_portal_router.include_router(api_keys_router)
dev_portal_router.include_router(usage_router)
dev_portal_router.include_router(playground_router)


# Export pour intégration dans l'app principale
__all__ = ["dev_portal_router"]
