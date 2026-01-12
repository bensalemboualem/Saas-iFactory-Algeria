"""
API Catalog - Apps et Agents publics pour IA Factory Algeria

Ce router gère :
- Liste des apps publiées/cachées
- Liste des agents publiés/cachés
- Pricing complet (plans + apps + agents)
- Admin endpoints pour publier/cacher
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional, List
from pydantic import BaseModel
import asyncpg
import logging

from app.dependencies import get_db_pool, get_current_active_user, optional_user
from app.models.user import UserInDB

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/catalog", tags=["catalog"])


# ═══════════════════════════════════════════════════════════════════
# MODELS
# ═══════════════════════════════════════════════════════════════════

class AppItem(BaseModel):
    slug: str
    name: str
    name_ar: Optional[str] = None
    description: Optional[str] = None
    description_ar: Optional[str] = None
    icon: Optional[str] = None
    category: str
    url: Optional[str] = None
    is_free: bool = False
    credits_per_use: int = 0
    min_plan: str = "free"
    tags: Optional[List[str]] = None


class AgentItem(BaseModel):
    slug: str
    name: str
    name_ar: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    category: str
    credits_per_task: int = 100
    min_plan: str = "pro"


# ═══════════════════════════════════════════════════════════════════
# PUBLIC ENDPOINTS
# ═══════════════════════════════════════════════════════════════════

@router.get("/apps")
async def get_published_apps(
    category: Optional[str] = None,
    free_only: bool = False,
    db: asyncpg.Pool = Depends(get_db_pool)
):
    """
    Liste des apps publiées pour le marché algérien

    Args:
        category: Filtrer par catégorie (media, creative, ai, business)
        free_only: Afficher uniquement les apps gratuites

    Returns:
        Liste des apps avec métadonnées
    """
    query = """
        SELECT slug, name, name_ar, description, description_ar,
               icon, category, url, is_free, credits_per_use, min_plan, tags
        FROM app_catalog
        WHERE is_published = true
    """
    params = []
    param_idx = 1

    if category:
        query += f" AND category = ${param_idx}"
        params.append(category)
        param_idx += 1

    if free_only:
        query += " AND is_free = true"

    query += " ORDER BY sort_order ASC"

    rows = await db.fetch(query, *params)

    return {
        "apps": [dict(row) for row in rows],
        "total": len(rows),
        "categories": ["media", "creative", "ai", "business"],
        "currency": "DZD"
    }


@router.get("/agents")
async def get_published_agents(
    category: Optional[str] = None,
    db: asyncpg.Pool = Depends(get_db_pool)
):
    """
    Liste des agents IA publiés

    Args:
        category: Filtrer par catégorie (hr, finance, legal, sales)

    Returns:
        Liste des agents avec métadonnées
    """
    query = """
        SELECT slug, name, name_ar, description, icon, category,
               credits_per_task, min_plan
        FROM agent_catalog
        WHERE is_published = true
    """
    params = []

    if category:
        query += " AND category = $1"
        params.append(category)

    query += " ORDER BY sort_order ASC"

    rows = await db.fetch(query, *params)

    return {
        "agents": [dict(row) for row in rows],
        "total": len(rows),
        "categories": ["hr", "finance", "legal", "sales"],
        "currency": "DZD"
    }


@router.get("/apps/{slug}")
async def get_app_detail(
    slug: str,
    db: asyncpg.Pool = Depends(get_db_pool)
):
    """
    Détail d'une app spécifique

    Args:
        slug: Identifiant unique de l'app

    Returns:
        Détails complets de l'app
    """
    row = await db.fetchrow("""
        SELECT * FROM app_catalog WHERE slug = $1 AND is_published = true
    """, slug)

    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"App '{slug}' non trouvée"
        )

    return dict(row)


@router.get("/agents/{slug}")
async def get_agent_detail(
    slug: str,
    db: asyncpg.Pool = Depends(get_db_pool)
):
    """
    Détail d'un agent spécifique

    Args:
        slug: Identifiant unique de l'agent

    Returns:
        Détails complets de l'agent
    """
    row = await db.fetchrow("""
        SELECT * FROM agent_catalog WHERE slug = $1 AND is_published = true
    """, slug)

    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent '{slug}' non trouvé"
        )

    return dict(row)


@router.get("/pricing")
async def get_catalog_pricing(db: asyncpg.Pool = Depends(get_db_pool)):
    """
    Pricing complet : plans + apps + agents (DZD uniquement)

    Returns:
        Plans d'abonnement, apps payantes, agents, LLMs gratuits
    """

    # Plans d'abonnement
    plans = await db.fetch("""
        SELECT name, credits_monthly, price_dzd, features
        FROM subscription_plans
        WHERE is_active = true
        ORDER BY credits_monthly
    """)

    # Apps avec crédits
    apps = await db.fetch("""
        SELECT slug, name, name_ar, icon, credits_per_use, min_plan, category
        FROM app_catalog
        WHERE is_published = true AND credits_per_use > 0
        ORDER BY credits_per_use DESC
    """)

    # Agents avec crédits
    agents = await db.fetch("""
        SELECT slug, name, name_ar, icon, credits_per_task, min_plan, category
        FROM agent_catalog
        WHERE is_published = true
        ORDER BY credits_per_task DESC
    """)

    # LLMs gratuits (depuis service_pricing)
    free_llms = await db.fetch("""
        SELECT service_name
        FROM service_pricing
        WHERE service_type = 'llm' AND is_unlimited = true AND is_active = true
        ORDER BY service_name
    """)

    return {
        "currency": "DZD",
        "payment_methods": ["CIB", "EDAHABIA", "BaridiMob"],
        "plans": [dict(p) for p in plans],
        "apps": [dict(a) for a in apps],
        "agents": [dict(a) for a in agents],
        "free_llms": [row['service_name'] for row in free_llms]
    }


@router.get("/stats")
async def get_catalog_stats(db: asyncpg.Pool = Depends(get_db_pool)):
    """
    Statistiques du catalog (pour dashboard)

    Returns:
        Nombre d'apps, agents, services par type
    """

    # Apps
    apps_stats = await db.fetchrow("""
        SELECT
            COUNT(*) FILTER (WHERE is_published = true) as published,
            COUNT(*) FILTER (WHERE is_published = false) as hidden,
            COUNT(*) FILTER (WHERE is_free = true AND is_published = true) as free
        FROM app_catalog
    """)

    # Agents
    agents_stats = await db.fetchrow("""
        SELECT
            COUNT(*) FILTER (WHERE is_published = true) as published,
            COUNT(*) FILTER (WHERE is_published = false) as hidden
        FROM agent_catalog
    """)

    # Services (LLM, Video, Image)
    services_stats = await db.fetch("""
        SELECT
            service_type,
            COUNT(*) as total,
            SUM(CASE WHEN is_unlimited THEN 1 ELSE 0 END) as free
        FROM service_pricing
        WHERE is_active = true
        GROUP BY service_type
        ORDER BY total DESC
    """)

    return {
        "apps": dict(apps_stats),
        "agents": dict(agents_stats),
        "services": [dict(s) for s in services_stats]
    }


# ═══════════════════════════════════════════════════════════════════
# ADMIN ENDPOINTS
# ═══════════════════════════════════════════════════════════════════

@router.get("/admin/apps")
async def admin_list_all_apps(
    current_user: UserInDB = Depends(get_current_active_user),
    db: asyncpg.Pool = Depends(get_db_pool)
):
    """
    Admin: Liste TOUTES les apps (publiées + cachées)
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    rows = await db.fetch("""
        SELECT slug, name, category, is_published, is_free, credits_per_use, sort_order
        FROM app_catalog
        ORDER BY is_published DESC, sort_order ASC
    """)

    return {
        "apps": [dict(row) for row in rows],
        "total": len(rows)
    }


@router.get("/admin/agents")
async def admin_list_all_agents(
    current_user: UserInDB = Depends(get_current_active_user),
    db: asyncpg.Pool = Depends(get_db_pool)
):
    """
    Admin: Liste TOUS les agents (publiés + cachés)
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    rows = await db.fetch("""
        SELECT slug, name, category, is_published, credits_per_task, sort_order
        FROM agent_catalog
        ORDER BY is_published DESC, sort_order ASC
    """)

    return {
        "agents": [dict(row) for row in rows],
        "total": len(rows)
    }


@router.put("/admin/apps/{slug}/publish")
async def admin_publish_app(
    slug: str,
    publish: bool = True,
    current_user: UserInDB = Depends(get_current_active_user),
    db: asyncpg.Pool = Depends(get_db_pool)
):
    """
    Admin: Publier ou cacher une app

    Args:
        slug: Identifiant de l'app
        publish: True pour publier, False pour cacher
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    result = await db.execute("""
        UPDATE app_catalog
        SET is_published = $1, updated_at = NOW()
        WHERE slug = $2
    """, publish, slug)

    if result == "UPDATE 0":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"App '{slug}' non trouvée"
        )

    logger.info(f"Admin {current_user.email}: App '{slug}' {'published' if publish else 'hidden'}")

    return {
        "slug": slug,
        "is_published": publish,
        "message": f"App {'publiée' if publish else 'cachée'} avec succès"
    }


@router.put("/admin/agents/{slug}/publish")
async def admin_publish_agent(
    slug: str,
    publish: bool = True,
    current_user: UserInDB = Depends(get_current_active_user),
    db: asyncpg.Pool = Depends(get_db_pool)
):
    """
    Admin: Publier ou cacher un agent

    Args:
        slug: Identifiant de l'agent
        publish: True pour publier, False pour cacher
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    result = await db.execute("""
        UPDATE agent_catalog
        SET is_published = $1
        WHERE slug = $2
    """, publish, slug)

    if result == "UPDATE 0":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent '{slug}' non trouvé"
        )

    logger.info(f"Admin {current_user.email}: Agent '{slug}' {'published' if publish else 'hidden'}")

    return {
        "slug": slug,
        "is_published": publish,
        "message": f"Agent {'publié' if publish else 'caché'} avec succès"
    }


@router.put("/admin/apps/{slug}/credits")
async def admin_update_app_credits(
    slug: str,
    credits_per_use: int,
    current_user: UserInDB = Depends(get_current_active_user),
    db: asyncpg.Pool = Depends(get_db_pool)
):
    """
    Admin: Modifier le coût en crédits d'une app
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    if credits_per_use < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credits must be >= 0"
        )

    await db.execute("""
        UPDATE app_catalog
        SET credits_per_use = $1, updated_at = NOW()
        WHERE slug = $2
    """, credits_per_use, slug)

    logger.info(f"Admin {current_user.email}: App '{slug}' credits updated to {credits_per_use}")

    return {
        "slug": slug,
        "credits_per_use": credits_per_use
    }
