"""
Database Session Management with Multi-Tenant RLS Support
==========================================================
Configure automatiquement le tenant_id via RLS pour chaque session
"""

import hashlib
import psycopg
from contextlib import asynccontextmanager
import logging
from typing import Optional, AsyncGenerator
from .config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def sha256(s: str) -> str:
    """Hash SHA256 pour API keys"""
    return hashlib.sha256(s.encode()).hexdigest()


# ============================================
# SYNC DATABASE (Existant - pour migrations)
# ============================================

@asynccontextmanager
async def get_db_connection():
    """
    Connection synchrone PostgreSQL (pour migrations et scripts)
    """
    conn = psycopg.connect(settings.postgres_url, autocommit=True)
    try:
        yield conn
    finally:
        conn.close()


async def get_tenant_by_key(api_key: str) -> Optional[dict]:
    """
    Récupérer tenant depuis API key (existant)
    """
    if not api_key:
        return None

    key_hash = sha256(api_key)

    try:
        async with get_db_connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    SELECT t.id, t.name, k.plan, k.rate_limit_per_minute,
                           k.quota_tokens_monthly, k.quota_audio_seconds_monthly,
                           k.quota_ocr_pages_monthly
                    FROM api_keys k
                    JOIN tenants t ON k.tenant_id = t.id
                    WHERE k.key_hash = %s AND k.revoked = false AND t.status = 'active'
                """, (key_hash,))

                row = await cur.fetchone()
                if not row:
                    return None

                return {
                    "id": str(row[0]),
                    "name": row[1],
                    "plan": row[2],
                    "rate_limit_per_minute": row[3],
                    "quota_tokens": row[4],
                    "quota_audio_seconds": row[5],
                    "quota_ocr_pages": row[6]
                }
    except Exception as e:
        logger.error(f"Database error in get_tenant_by_key: {e}")
        return None


async def insert_usage(event: dict):
    """
    Insérer événement usage (existant)
    """
    try:
        async with get_db_connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    INSERT INTO usage_events (tenant_id, request_id, route, method,
                    tokens_input, tokens_output, audio_seconds, ocr_pages,
                    latency_ms, model_used, status_code)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    event.get("tenant_id"),
                    event.get("request_id"),
                    event.get("route"),
                    event.get("method", "POST"),
                    event.get("tokens_input", 0),
                    event.get("tokens_output", 0),
                    event.get("audio_seconds", 0),
                    event.get("ocr_pages", 0),
                    event.get("latency_ms", 0),
                    event.get("model_used", "unknown"),
                    event.get("status_code", 200)
                ))
    except Exception as e:
        logger.error(f"Failed to insert usage: {e}")


# ============================================
# ASYNC DATABASE WITH RLS SUPPORT (NOUVEAU)
# ============================================

class TenantAwareDBSession:
    """
    Session DB async avec support RLS multi-tenant

    Configure automatiquement set_tenant() au début de chaque session
    """

    def __init__(self, conn: psycopg.AsyncConnection, tenant_id: Optional[str] = None):
        self.conn = conn
        self.tenant_id = tenant_id
        self._tenant_configured = False

    async def __aenter__(self):
        """Début de session - configurer tenant_id via RLS"""
        if self.tenant_id and not self._tenant_configured:
            try:
                # Appeler fonction PostgreSQL set_tenant()
                await self.conn.execute(
                    "SELECT set_tenant(%s::UUID)",
                    (self.tenant_id,)
                )
                logger.debug(f"RLS tenant configured: {self.tenant_id}")
                self._tenant_configured = True

            except Exception as e:
                logger.error(f"Failed to set tenant {self.tenant_id}: {e}")
                raise

        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Fin de session"""
        # Session fermée par le pool
        pass


@asynccontextmanager
async def get_db_session_with_tenant(
    tenant_id: Optional[str] = None,
    is_superadmin: bool = False
) -> AsyncGenerator[psycopg.AsyncConnection, None]:
    """
    Récupérer session DB avec contexte tenant configuré automatiquement

    Args:
        tenant_id: UUID du tenant (depuis request.state.tenant_id)
        is_superadmin: Si True, active enable_superadmin_mode()

    Usage dans un router:
        @router.get("/api/projects")
        async def list_projects(request: Request):
            tenant_id = request.state.tenant_id

            async with get_db_session_with_tenant(tenant_id) as db:
                # RLS déjà configuré ici
                result = await db.execute("SELECT * FROM projects")
                # Retourne SEULEMENT les projets du tenant
                return result.fetchall()
    """
    # Créer connection async
    conn = await psycopg.AsyncConnection.connect(
        settings.postgres_url,
        autocommit=False  # Transaction par défaut
    )

    try:
        # Si super-admin, activer mode bypass RLS
        if is_superadmin:
            await conn.execute("SELECT enable_superadmin_mode()")
            logger.info("Super-admin mode enabled for session")

        # Si tenant_id fourni, configurer RLS
        elif tenant_id:
            await conn.execute(
                "SELECT set_tenant(%s::UUID)",
                (tenant_id,)
            )
            logger.debug(f"Tenant context set: {tenant_id}")

        # Retourner connection
        yield conn

        # Commit transaction si pas d'erreur
        await conn.commit()

    except Exception as e:
        # Rollback en cas d'erreur
        await conn.rollback()
        logger.error(f"Database session error: {e}")
        raise

    finally:
        # Fermer connection
        await conn.close()


# ============================================
# DEPENDENCY INJECTION POUR FASTAPI
# ============================================

async def get_db(request = None) -> AsyncGenerator[psycopg.AsyncConnection, None]:
    """
    FastAPI Dependency pour session DB avec tenant automatique

    Usage dans router:
        from fastapi import Depends
        from .database import get_db

        @router.get("/api/projects")
        async def list_projects(
            request: Request,
            db = Depends(get_db)
        ):
            # db a déjà le tenant_id configuré via RLS
            result = await db.execute("SELECT * FROM projects")
            return result.fetchall()
    """
    # Extraire tenant_id depuis request.state
    tenant_id = None
    is_superadmin = False

    if request:
        tenant_id = getattr(request.state, "tenant_id", None)
        is_superadmin = getattr(request.state, "is_superadmin", False)

    # Retourner session avec tenant configuré
    async with get_db_session_with_tenant(tenant_id, is_superadmin) as db:
        yield db


# ============================================
# HELPER FUNCTIONS
# ============================================

async def verify_tenant_exists(tenant_id: str) -> bool:
    """
    Vérifier qu'un tenant existe

    Usage:
        if not await verify_tenant_exists(tenant_id):
            raise HTTPException(404, "Tenant not found")
    """
    try:
        async with get_db_connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT 1 FROM tenants WHERE id = %s AND status = 'active'",
                    (tenant_id,)
                )
                return cur.fetchone() is not None
    except Exception as e:
        logger.error(f"Error verifying tenant {tenant_id}: {e}")
        return False


async def get_tenant_info(tenant_id: str) -> Optional[dict]:
    """
    Récupérer informations complètes d'un tenant

    Returns:
        {
            "id": "uuid",
            "name": "École Ibn Khaldoun",
            "slug": "ecole-ibn-khaldoun-alger",
            "region": "DZ",
            "plan": "pro",
            "status": "active"
        }
    """
    try:
        async with get_db_connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    SELECT id, name, slug, region, plan, status, created_at
                    FROM tenants
                    WHERE id = %s
                """, (tenant_id,))

                row = await cur.fetchone()
                if not row:
                    return None

                return {
                    "id": str(row[0]),
                    "name": row[1],
                    "slug": row[2],
                    "region": row[3],
                    "plan": row[4],
                    "status": row[5],
                    "created_at": row[6].isoformat() if row[6] else None
                }
    except Exception as e:
        logger.error(f"Error getting tenant info {tenant_id}: {e}")
        return None
