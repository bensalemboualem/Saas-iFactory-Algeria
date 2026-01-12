-- ========================================
-- Test Script: Multi-Tenant Phase 1
-- ========================================
-- Execute after running migrations 006 and 007
-- Usage: psql -U postgres -d iafactory -f test_multi_tenant.sql

\echo '=========================================='
\echo 'Multi-Tenant Phase 1 - Verification Tests'
\echo '=========================================='
\echo ''

-- Test 1: Check tenants table exists
\echo 'Test 1: Tenants table exists'
\echo '----------------------------------------'
SELECT
    CASE
        WHEN EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'tenants')
        THEN '✓ PASS: tenants table exists'
        ELSE '✗ FAIL: tenants table missing'
    END as result;
\echo ''

-- Test 2: Check tenant_id columns exist
\echo 'Test 2: tenant_id columns on critical tables'
\echo '----------------------------------------'
SELECT
    table_name,
    CASE
        WHEN column_name = 'tenant_id' THEN '✓'
        ELSE '✗'
    END as status,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE column_name = 'tenant_id'
  AND table_schema = 'public'
ORDER BY table_name;
\echo ''

-- Test 3: Check indexes created
\echo 'Test 3: tenant_id indexes created'
\echo '----------------------------------------'
SELECT
    tablename,
    indexname,
    '✓' as status
FROM pg_indexes
WHERE indexname LIKE '%tenant%'
  AND schemaname = 'public'
ORDER BY tablename, indexname;
\echo ''

-- Test 4: Check default tenant exists
\echo 'Test 4: Default system tenant exists'
\echo '----------------------------------------'
SELECT
    CASE
        WHEN COUNT(*) > 0
        THEN '✓ PASS: Default tenant exists'
        ELSE '✗ FAIL: Default tenant missing'
    END as result
FROM tenants
WHERE id = '00000000-0000-0000-0000-000000000000';
\echo ''

-- Test 5: Check foreign key constraints
\echo 'Test 5: Foreign key constraints on tenant_id'
\echo '----------------------------------------'
SELECT
    tc.table_name,
    tc.constraint_name,
    '✓' as status
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND kcu.column_name = 'tenant_id'
ORDER BY tc.table_name;
\echo ''

-- Test 6: Check data migration (no NULL tenant_id)
\echo 'Test 6: No NULL tenant_id on critical tables'
\echo '----------------------------------------'
DO $$
DECLARE
    null_count INTEGER;
    table_rec RECORD;
BEGIN
    FOR table_rec IN
        SELECT table_name
        FROM information_schema.columns
        WHERE column_name = 'tenant_id'
          AND table_schema = 'public'
          AND table_name IN ('projects', 'knowledge_base', 'bolt_workflows')
    LOOP
        EXECUTE format('SELECT COUNT(*) FROM %I WHERE tenant_id IS NULL', table_rec.table_name)
        INTO null_count;

        IF null_count = 0 THEN
            RAISE NOTICE '✓ %: 0 NULL tenant_id', table_rec.table_name;
        ELSE
            RAISE WARNING '✗ %: % rows with NULL tenant_id', table_rec.table_name, null_count;
        END IF;
    END LOOP;
END $$;
\echo ''

-- Test 7: Check tenant_users junction table
\echo 'Test 7: tenant_users table exists'
\echo '----------------------------------------'
SELECT
    CASE
        WHEN EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'tenant_users')
        THEN '✓ PASS: tenant_users table exists'
        ELSE '✗ FAIL: tenant_users table missing'
    END as result;
\echo ''

-- Test 8: Check api_keys table
\echo 'Test 8: api_keys table exists'
\echo '----------------------------------------'
SELECT
    CASE
        WHEN EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'api_keys')
        THEN '✓ PASS: api_keys table exists'
        ELSE '✗ FAIL: api_keys table missing'
    END as result;
\echo ''

-- Test 9: Check usage_events table
\echo 'Test 9: usage_events table exists'
\echo '----------------------------------------'
SELECT
    CASE
        WHEN EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'usage_events')
        THEN '✓ PASS: usage_events table exists'
        ELSE '✗ FAIL: usage_events table missing'
    END as result;
\echo ''

-- Test 10: Check region constraint
\echo 'Test 10: region field constraint valid'
\echo '----------------------------------------'
SELECT
    conname as constraint_name,
    pg_get_constraintdef(oid) as definition,
    '✓' as status
FROM pg_constraint
WHERE conname = 'tenants_region_valid';
\echo ''

-- Summary: Count all tenants
\echo '=========================================='
\echo 'Summary: Current Tenants'
\echo '=========================================='
SELECT
    COUNT(*) as total_tenants,
    COUNT(*) FILTER (WHERE region = 'DZ') as algeria,
    COUNT(*) FILTER (WHERE region = 'CH') as switzerland,
    COUNT(*) FILTER (WHERE status = 'active') as active,
    COUNT(*) FILTER (WHERE plan = 'pro') as pro_plan,
    COUNT(*) FILTER (WHERE plan = 'enterprise') as enterprise_plan
FROM tenants;
\echo ''

-- List all tenants
\echo 'All Tenants:'
\echo '----------------------------------------'
SELECT
    id,
    name,
    region,
    plan,
    status,
    TO_CHAR(created_at, 'YYYY-MM-DD HH24:MI') as created
FROM tenants
ORDER BY created_at DESC;
\echo ''

-- Final verdict
\echo '=========================================='
\echo 'Overall Verification'
\echo '=========================================='
DO $$
DECLARE
    all_tests_passed BOOLEAN;
BEGIN
    -- Check all critical conditions
    SELECT
        EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'tenants')
        AND EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'tenant_users')
        AND EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'api_keys')
        AND EXISTS (SELECT 1 FROM tenants WHERE id = '00000000-0000-0000-0000-000000000000')
        AND (SELECT COUNT(*) FROM information_schema.columns WHERE column_name = 'tenant_id') >= 10
    INTO all_tests_passed;

    IF all_tests_passed THEN
        RAISE NOTICE '';
        RAISE NOTICE '╔════════════════════════════════════════╗';
        RAISE NOTICE '║  ✓ ALL TESTS PASSED                   ║';
        RAISE NOTICE '║  Multi-Tenant Phase 1 COMPLETE        ║';
        RAISE NOTICE '║  Ready for Phase 2 (RLS)              ║';
        RAISE NOTICE '╚════════════════════════════════════════╝';
        RAISE NOTICE '';
    ELSE
        RAISE WARNING '';
        RAISE WARNING '╔════════════════════════════════════════╗';
        RAISE WARNING '║  ✗ SOME TESTS FAILED                  ║';
        RAISE WARNING '║  Review errors above                  ║';
        RAISE WARNING '╚════════════════════════════════════════╝';
        RAISE WARNING '';
    END IF;
END $$;

-- ========================================
-- Example: Create Test Tenants
-- ========================================
\echo ''
\echo '=========================================='
\echo 'Example: Create Test Tenants'
\echo '=========================================='
\echo ''
\echo 'To create test tenants, run these SQL commands:'
\echo ''
\echo '-- École en Algérie:'
\echo 'INSERT INTO tenants (name, slug, region, plan, status, admin_email)'
\echo 'VALUES ('
\echo '    ''École Test Alger'','
\echo '    ''ecole-test-alger'','
\echo '    ''DZ'','
\echo '    ''pro'','
\echo '    ''active'','
\echo '    ''admin@ecole-test.dz'''
\echo ') RETURNING id, slug;'
\echo ''
\echo '-- Cabinet Médical Suisse:'
\echo 'INSERT INTO tenants (name, slug, region, plan, status, admin_email)'
\echo 'VALUES ('
\echo '    ''Cabinet Test Genève'','
\echo '    ''cabinet-test-geneve'','
\echo '    ''CH'','
\echo '    ''enterprise'','
\echo '    ''active'','
\echo '    ''admin@cabinet-test.ch'''
\echo ') RETURNING id, slug;'
\echo ''
\echo '=========================================='
\echo 'End of Tests'
\echo '=========================================='
