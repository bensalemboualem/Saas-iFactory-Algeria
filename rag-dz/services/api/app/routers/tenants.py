"""
Tenant Management Router - Multi-Tenant SaaS
=============================================
CRUD operations for tenants (organizations)
Super-admin only for tenant creation/deletion
"""

from fastapi import APIRouter, HTTPException, Depends, Request, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import logging
import uuid

from app.models.user import TenantCreate, TenantResponse
from app.database import get_db_session_with_tenant
from app.tenant_middleware import get_request_tenant_id, is_superadmin_request

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/tenants", tags=["Tenants"])


# ============================================
# SCHEMAS
# ============================================

class TenantUpdate(BaseModel):
    """Update tenant schema"""
    name: Optional[str] = None
    plan: Optional[str] = None
    settings: Optional[dict] = None


class TenantStats(BaseModel):
    """Tenant statistics"""
    user_count: int = 0
    project_count: int = 0
    document_count: int = 0
    total_tokens_used: int = 0


class TenantWithStats(TenantResponse):
    """Tenant with usage stats"""
    stats: Optional[TenantStats] = None


# ============================================
# ROUTES
# ============================================

@router.get("/current", response_model=TenantResponse)
async def get_current_tenant(request: Request):
    """
    Get current user's tenant information

    Requires: Authenticated user with tenant_id in JWT
    """
    tenant_id = get_request_tenant_id(request)

    if not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No tenant context"
        )

    try:
        async with get_db_session_with_tenant(tenant_id) as db:
            result = await db.execute("""
                SELECT id, name, slug, region, plan, status, created_at
                FROM tenants
                WHERE id = %s
            """, (tenant_id,))

            row = await result.fetchone()
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Tenant not found"
                )

            return TenantResponse(
                id=str(row[0]),
                name=row[1],
                slug=row[2],
                region=row[3],
                plan=row[4],
                status=row[5],
                created_at=row[6]
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching tenant: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch tenant"
        )


@router.get("/list", response_model=List[TenantResponse])
async def list_tenants(request: Request, limit: int = 50, offset: int = 0):
    """
    List all tenants (Super-admin only)

    Requires: Super-admin API key
    """
    if not is_superadmin_request(request):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super-admin access required"
        )

    try:
        async with get_db_session_with_tenant(is_superadmin=True) as db:
            result = await db.execute("""
                SELECT id, name, slug, region, plan, status, created_at
                FROM tenants
                WHERE status != 'deleted'
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
            """, (limit, offset))

            rows = await result.fetchall()

            return [
                TenantResponse(
                    id=str(row[0]),
                    name=row[1],
                    slug=row[2],
                    region=row[3],
                    plan=row[4],
                    status=row[5],
                    created_at=row[6]
                )
                for row in rows
            ]

    except Exception as e:
        logger.error(f"Error listing tenants: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list tenants"
        )


@router.post("/create", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
async def create_tenant(request: Request, tenant: TenantCreate):
    """
    Create a new tenant (Super-admin only)

    This is typically called during user registration
    when a new organization signs up
    """
    # For self-registration, super-admin check is optional
    # In production, you might want to restrict this

    tenant_id = str(uuid.uuid4())
    slug = tenant.slug or tenant.name.lower().replace(" ", "-")[:50]

    try:
        async with get_db_session_with_tenant(is_superadmin=True) as db:
            # Check if slug already exists
            check = await db.execute(
                "SELECT 1 FROM tenants WHERE slug = %s",
                (slug,)
            )
            if await check.fetchone():
                slug = f"{slug}-{tenant_id[:8]}"

            # Insert tenant
            await db.execute("""
                INSERT INTO tenants (id, name, slug, region, plan, status, created_at)
                VALUES (%s, %s, %s, %s, %s, 'active', NOW())
            """, (tenant_id, tenant.name, slug, tenant.region, tenant.plan))

            await db.commit()

            logger.info(f"Tenant created: {tenant.name} ({tenant_id})")

            return TenantResponse(
                id=tenant_id,
                name=tenant.name,
                slug=slug,
                region=tenant.region,
                plan=tenant.plan,
                status="active",
                created_at=datetime.utcnow()
            )

    except Exception as e:
        logger.error(f"Error creating tenant: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create tenant: {str(e)}"
        )


@router.put("/{tenant_id}", response_model=TenantResponse)
async def update_tenant(
    request: Request,
    tenant_id: str,
    update: TenantUpdate
):
    """
    Update tenant information

    Requires: Tenant owner/admin or super-admin
    """
    current_tenant = get_request_tenant_id(request)
    is_admin = is_superadmin_request(request)

    # Check permission: must be same tenant or super-admin
    if current_tenant != tenant_id and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )

    try:
        async with get_db_session_with_tenant(tenant_id, is_superadmin=is_admin) as db:
            # Build update query dynamically
            updates = []
            params = []

            if update.name:
                updates.append("name = %s")
                params.append(update.name)

            if update.plan:
                updates.append("plan = %s")
                params.append(update.plan)

            if update.settings:
                updates.append("settings = %s")
                params.append(update.settings)

            if not updates:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No fields to update"
                )

            updates.append("updated_at = NOW()")
            params.append(tenant_id)

            query = f"""
                UPDATE tenants
                SET {', '.join(updates)}
                WHERE id = %s
                RETURNING id, name, slug, region, plan, status, created_at
            """

            result = await db.execute(query, tuple(params))
            row = await result.fetchone()

            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Tenant not found"
                )

            await db.commit()

            return TenantResponse(
                id=str(row[0]),
                name=row[1],
                slug=row[2],
                region=row[3],
                plan=row[4],
                status=row[5],
                created_at=row[6]
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating tenant: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update tenant"
        )


@router.get("/{tenant_id}/stats", response_model=TenantStats)
async def get_tenant_stats(request: Request, tenant_id: str):
    """
    Get tenant usage statistics

    Requires: Tenant member or super-admin
    """
    current_tenant = get_request_tenant_id(request)
    is_admin = is_superadmin_request(request)

    if current_tenant != tenant_id and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )

    try:
        async with get_db_session_with_tenant(tenant_id, is_superadmin=is_admin) as db:
            # User count
            users = await db.execute(
                "SELECT COUNT(*) FROM users WHERE tenant_id = %s",
                (tenant_id,)
            )
            user_count = (await users.fetchone())[0] or 0

            # Project count
            projects = await db.execute(
                "SELECT COUNT(*) FROM projects WHERE tenant_id = %s",
                (tenant_id,)
            )
            project_count = (await projects.fetchone())[0] or 0

            # Document count
            docs = await db.execute(
                "SELECT COUNT(*) FROM documents WHERE tenant_id = %s",
                (tenant_id,)
            )
            document_count = (await docs.fetchone())[0] or 0

            # Total tokens (this month)
            tokens = await db.execute("""
                SELECT COALESCE(SUM(tokens_input + tokens_output), 0)
                FROM usage_events
                WHERE tenant_id = %s
                AND timestamp >= date_trunc('month', NOW())
            """, (tenant_id,))
            total_tokens = int((await tokens.fetchone())[0] or 0)

            return TenantStats(
                user_count=user_count,
                project_count=project_count,
                document_count=document_count,
                total_tokens_used=total_tokens
            )

    except Exception as e:
        logger.error(f"Error fetching tenant stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch stats"
        )


@router.delete("/{tenant_id}")
async def delete_tenant(request: Request, tenant_id: str):
    """
    Soft-delete a tenant (Super-admin only)

    Sets status to 'deleted', doesn't remove data
    """
    if not is_superadmin_request(request):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super-admin access required"
        )

    try:
        async with get_db_session_with_tenant(is_superadmin=True) as db:
            result = await db.execute("""
                UPDATE tenants
                SET status = 'deleted', updated_at = NOW()
                WHERE id = %s
                RETURNING id
            """, (tenant_id,))

            if not await result.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Tenant not found"
                )

            await db.commit()

            logger.warning(f"Tenant deleted: {tenant_id}")

            return {"message": "Tenant deleted", "tenant_id": tenant_id}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting tenant: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete tenant"
        )


# ============================================
# UTILITY FUNCTIONS
# ============================================

async def create_tenant_for_user(name: str, region: str = "DZ") -> str:
    """
    Create a new tenant during user registration

    Returns:
        tenant_id: UUID of created tenant
    """
    tenant_id = str(uuid.uuid4())
    slug = name.lower().replace(" ", "-")[:50]

    try:
        async with get_db_session_with_tenant(is_superadmin=True) as db:
            await db.execute("""
                INSERT INTO tenants (id, name, slug, region, plan, status)
                VALUES (%s, %s, %s, %s, 'free', 'active')
            """, (tenant_id, name, slug, region))

            await db.commit()

            logger.info(f"Auto-created tenant for registration: {name} ({tenant_id})")
            return tenant_id

    except Exception as e:
        logger.error(f"Failed to auto-create tenant: {e}")
        raise
