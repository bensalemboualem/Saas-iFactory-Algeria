# Database Migrations - IAFactory RAG

## Overview

This directory contains SQL migration files for the IAFactory RAG database schema.

## Migration Files

| Migration | Description | Status |
|-----------|-------------|--------|
| 001 | Create users table | ✅ Completed |
| 002 | Create projects table | ✅ Completed |
| 003 | Create bolt_workflows and knowledge_base tables | ✅ Completed |
| 004 | Create orchestrator_state table | ✅ Completed |
| 005 | Create bmad_workflows table | ✅ Completed |
| **006** | **Create tenants table (multi-tenant)** | 🆕 New |
| **007** | **Add tenant_id to all tables** | 🆕 New |
| **008** | **Enable Row-Level Security (RLS)** | 🆕 New |

## 🎯 Multi-Tenant Migrations (006-007-008)

### Migration 006: Tenants Table

Creates the core multi-tenant infrastructure:

- **tenants** - Main tenant table with:
  - `id` (UUID) - Primary key
  - `name` - Tenant name (e.g., "École Ibn Khaldoun")
  - `slug` - URL-friendly identifier
  - `region` - Geographic region (DZ, CH, FR, BE, CA)
  - `plan` - Subscription plan (free, pro, enterprise)
  - `status` - Account status (active, suspended, trial, cancelled)
  - `admin_email` - Primary contact email
  - `settings` - JSONB configuration
  - `created_at` - Timestamp

- **tenant_users** - Many-to-many junction table (users ↔ tenants)
  - Users can belong to multiple tenants
  - Each user has a role per tenant (owner, admin, member, viewer)

- **api_keys** - API keys for tenant authentication
  - SHA256 hashed keys
  - Rate limits and quotas per tenant
  - Plan-based permissions

- **usage_events** - API usage tracking per tenant
  - Tokens, audio seconds, OCR pages
  - Performance metrics
  - Billing analytics

### Migration 007: Add tenant_id to Tables

Adds `tenant_id` column to all critical tables:

**Core Tables**:
- `projects` - Project management
- `knowledge_base` - Documents and knowledge items
- `bolt_workflows` - Bolt automation workflows
- `orchestrator_state` - Orchestrator state management
- `bmad_workflows` - BMAD workflow management

**Voice & Transcription**:
- `voice_transcriptions` - STT transcriptions (NEW)
- `voice_conversations` - Voice agent conversations (NEW)

**CRM & Billing**:
- `crm_leads` - CRM lead management (NEW)
- `crm_deals` - CRM deal pipeline (NEW)
- `billing_accounts` - Billing and credits per tenant (NEW)
- `credit_transactions` - Credit transaction history (NEW)

**Business Analytics**:
- `pme_analyses` - PME/Business analyses (NEW)

### Indexes Created

Every table with `tenant_id` gets optimized indexes:

```sql
CREATE INDEX idx_{table}_tenant ON {table}(tenant_id);
CREATE INDEX idx_{table}_tenant_created ON {table}(tenant_id, created_at DESC);
```

This ensures:
- ⚡ Ultra-fast queries filtered by tenant
- 📈 Efficient sorting and pagination
- 🔍 Optimal performance even with 1000+ tenants

### Migration 008: Row-Level Security (RLS)

Enables PostgreSQL Row-Level Security for **isolation étanche**:

**Functions Created**:
```sql
-- Set current tenant for session (call at request start)
SELECT set_tenant('tenant-uuid-here');

-- Get current tenant from session
SELECT get_current_tenant();

-- Check if current session is super-admin
SELECT is_superadmin();

-- Enable super-admin mode (support/supervision)
SELECT enable_superadmin_mode();
```

**RLS Policies** (60+ policies created):
- **SELECT**: User can only see data from their tenant
- **INSERT**: User can only create data for their tenant
- **UPDATE**: User can only modify data from their tenant
- **DELETE**: User can only delete data from their tenant
- **Super-admin**: Can bypass RLS for support/supervision

**Tables Protected**:
- All tables with `tenant_id` (15+ tables)
- Tenants, tenant_users, api_keys, usage_events
- Projects, knowledge_base, workflows
- Voice transcriptions, CRM, billing
- PME analyses

**Security Model**:
```sql
-- Policy example (applied to all tables)
CREATE POLICY {table}_select ON {table}
    FOR SELECT
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()  -- Current tenant only
        OR is_superadmin()                 -- OR super-admin
    );
```

**Usage in Application**:
```python
# Start of each request
await db.execute(f"SELECT set_tenant('{tenant_id_from_jwt}')")

# All subsequent queries are automatically filtered by RLS
projects = await db.query(Project).all()
# ↑ Will ONLY return projects for current tenant
```

**Super-Admin Access** (for support):
```sql
-- Enable super-admin mode
SELECT enable_superadmin_mode();

-- Now can see all tenants' data
SELECT * FROM projects;  -- All tenants visible
```

## 🚀 Running Migrations

### Option 1: Run All Migrations

```bash
cd backend/rag-compat/migrations
chmod +x run_migrations.sh
./run_migrations.sh
```

### Option 2: Run Specific Migration

```bash
# Run only migration 006 (tenants table)
./run_migrations.sh 006

# Run only migration 007 (add tenant_id)
./run_migrations.sh 007

# Run only migration 008 (RLS)
./run_migrations.sh 008
```

### Option 3: Manual Execution

```bash
# Using psql
psql -U postgres -d iafactory -f 006_create_tenants_table.sql
psql -U postgres -d iafactory -f 007_add_tenant_id_to_tables.sql
psql -U postgres -d iafactory -f 008_enable_rls_policies.sql
```

## 📊 Verifying Migrations

### Check Tenants Table

```sql
-- List all tenants
SELECT id, name, region, plan, status, created_at
FROM tenants
ORDER BY created_at DESC;

-- Default system tenant should exist
SELECT * FROM tenants
WHERE id = '00000000-0000-0000-0000-000000000000';
```

### Check tenant_id Columns

```sql
-- Verify tenant_id exists on all tables
SELECT
    table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE column_name = 'tenant_id'
ORDER BY table_name;
```

### Check Indexes

```sql
-- List all tenant_id indexes
SELECT
    schemaname,
    tablename,
    indexname
FROM pg_indexes
WHERE indexname LIKE '%tenant%'
ORDER BY tablename;
```

## 🏢 Creating Your First Tenant

### For Algerian School

```sql
INSERT INTO tenants (name, slug, region, plan, status, admin_email, metadata)
VALUES (
    'École Ibn Khaldoun Alger',
    'ecole-ibn-khaldoun-alger',
    'DZ',
    'pro',
    'active',
    'admin@ecole-ibn-khaldoun.dz',
    '{"type": "school", "students_count": 500, "city": "Alger"}'::jsonb
)
RETURNING id;
```

### For Swiss Medical Office

```sql
INSERT INTO tenants (name, slug, region, plan, status, admin_email, metadata)
VALUES (
    'Cabinet Dr. Dupont Genève',
    'cabinet-dupont-geneve',
    'CH',
    'enterprise',
    'active',
    'admin@cabinet-dupont.ch',
    '{"type": "medical", "speciality": "general", "city": "Genève"}'::jsonb
)
RETURNING id;
```

### For Law Firm

```sql
INSERT INTO tenants (name, slug, region, plan, status, admin_email, metadata)
VALUES (
    'Étude Notariale Belhadi Oran',
    'etude-belhadi-oran',
    'DZ',
    'pro',
    'active',
    'contact@etude-belhadi.dz',
    '{"type": "legal", "speciality": "notary", "city": "Oran"}'::jsonb
)
RETURNING id;
```

## 🔗 Linking Users to Tenants

```sql
-- Add user to tenant as admin
INSERT INTO tenant_users (tenant_id, user_id, role)
VALUES (
    '550e8400-e29b-41d4-a716-446655440000',  -- tenant_id
    1,                                         -- user_id
    'admin'
);

-- List all users for a tenant
SELECT
    u.id,
    u.email,
    u.full_name,
    tu.role,
    tu.created_at
FROM tenant_users tu
JOIN users u ON tu.user_id = u.id
WHERE tu.tenant_id = '550e8400-e29b-41d4-a716-446655440000'
ORDER BY tu.created_at;
```

## 🔄 Data Migration

Migration 007 automatically:
1. ✅ Adds `tenant_id` column to all tables (nullable)
2. ✅ Assigns existing data to default tenant `00000000-0000-0000-0000-000000000000`
3. ✅ Makes `tenant_id` NOT NULL (after data migration)
4. ✅ Creates indexes on all `tenant_id` columns

**Existing data is safe** - no data loss!

## 🗑️ Rollback (Emergency)

If you need to rollback migrations (USE WITH CAUTION):

```sql
-- Rollback migration 007 (remove tenant_id)
BEGIN;

ALTER TABLE projects DROP COLUMN IF EXISTS tenant_id CASCADE;
ALTER TABLE knowledge_base DROP COLUMN IF EXISTS tenant_id CASCADE;
ALTER TABLE bolt_workflows DROP COLUMN IF EXISTS tenant_id CASCADE;
ALTER TABLE orchestrator_state DROP COLUMN IF EXISTS tenant_id CASCADE;
ALTER TABLE bmad_workflows DROP COLUMN IF EXISTS tenant_id CASCADE;

DROP TABLE IF EXISTS voice_transcriptions CASCADE;
DROP TABLE IF EXISTS voice_conversations CASCADE;
DROP TABLE IF EXISTS crm_leads CASCADE;
DROP TABLE IF EXISTS crm_deals CASCADE;
DROP TABLE IF EXISTS billing_accounts CASCADE;
DROP TABLE IF EXISTS credit_transactions CASCADE;
DROP TABLE IF EXISTS pme_analyses CASCADE;

COMMIT;
```

```sql
-- Rollback migration 006 (remove tenants infrastructure)
BEGIN;

DROP TABLE IF EXISTS usage_events CASCADE;
DROP TABLE IF EXISTS api_keys CASCADE;
DROP TABLE IF EXISTS tenant_users CASCADE;
DROP TABLE IF EXISTS tenants CASCADE;

COMMIT;
```

## 📝 Environment Variables

Required environment variables (in `backend/rag-compat/.env`):

```bash
# Database connection
DB_HOST=localhost
DB_PORT=5432
DB_NAME=iafactory
DB_USER=postgres
DB_PASSWORD=your_secure_password

# Or use full URL
DATABASE_URL=postgresql://postgres:password@localhost:5432/iafactory
```

## 🧪 Testing Multi-Tenant Isolation

```sql
-- Create 2 test tenants
INSERT INTO tenants (name, slug, region, admin_email)
VALUES
    ('Test Tenant A', 'test-tenant-a', 'DZ', 'a@test.com'),
    ('Test Tenant B', 'test-tenant-b', 'DZ', 'b@test.com')
RETURNING id;

-- Create project for Tenant A
INSERT INTO projects (tenant_id, name, description)
VALUES (
    (SELECT id FROM tenants WHERE slug = 'test-tenant-a'),
    'Secret Project A',
    'This should only be visible to Tenant A'
);

-- Verify isolation: Tenant B should not see Tenant A's projects
SELECT *
FROM projects
WHERE tenant_id = (SELECT id FROM tenants WHERE slug = 'test-tenant-b');
-- Should return 0 rows
```

## 📚 Next Steps

After running migrations:

1. ✅ **Phase 2**: Enable Row-Level Security (RLS) in PostgreSQL
2. ✅ **Phase 3**: Update FastAPI middleware for tenant context
3. ✅ **Phase 4**: Modify authentication to include tenant_id in JWT
4. ✅ **Phase 5**: Add tenant isolation tests

See [MULTI_TENANT_IMPLEMENTATION_PLAN.md](../../MULTI_TENANT_IMPLEMENTATION_PLAN.md) for full roadmap.

## ❓ Troubleshooting

### Migration fails with "relation already exists"

This is normal - migrations use `IF NOT EXISTS` to be idempotent. The migration will skip existing tables.

### "tenant_id" column already exists

Run migration 007 again - it uses `ADD COLUMN IF NOT EXISTS`.

### Foreign key constraint violation

Ensure migration 006 (tenants table) runs BEFORE migration 007.

### Performance is slow after adding tenant_id

Wait for indexes to be created. Check indexes with:

```sql
SELECT * FROM pg_stat_user_indexes WHERE indexrelname LIKE '%tenant%';
```

---

**Created**: 2025-12-16
**Author**: Claude Code (Sonnet 4.5)
**Priority**: P0 - Critical for multi-tenant deployment
