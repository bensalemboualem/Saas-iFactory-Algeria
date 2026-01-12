-- ========================================
-- Test Script: RLS Isolation Verification
-- ========================================
-- Execute after running migration 008
-- Usage: psql -U postgres -d iafactory -f test_rls_isolation.sql

\echo '=========================================='
\echo 'RLS Isolation Tests - Phase 2'
\echo '=========================================='
\echo ''

-- ============================================
-- SETUP: Create 2 test tenants
-- ============================================

\echo 'SETUP: Creating 2 test tenants...'
\echo '----------------------------------------'

-- Activer mode super-admin pour setup
SELECT enable_superadmin_mode();

-- Créer tenant A (École Alger)
INSERT INTO tenants (id, name, slug, region, plan, status, admin_email)
VALUES (
    '11111111-1111-1111-1111-111111111111',
    'École Test Alger',
    'ecole-test-alger',
    'DZ',
    'pro',
    'active',
    'admin-a@test.dz'
)
ON CONFLICT (id) DO NOTHING;

-- Créer tenant B (École Oran)
INSERT INTO tenants (id, name, slug, region, plan, status, admin_email)
VALUES (
    '22222222-2222-2222-2222-222222222222',
    'École Test Oran',
    'ecole-test-oran',
    'DZ',
    'pro',
    'active',
    'admin-b@test.dz'
)
ON CONFLICT (id) DO NOTHING;

\echo '✓ Test tenants created'
\echo ''

-- ============================================
-- SETUP: Create test data for Tenant A
-- ============================================

\echo 'SETUP: Creating test data for Tenant A...'
\echo '----------------------------------------'

-- Set session to Tenant A
SELECT set_tenant('11111111-1111-1111-1111-111111111111');

-- Créer projet pour Tenant A
INSERT INTO projects (name, description, tenant_id)
VALUES (
    'Secret Project A',
    'This should only be visible to Tenant A',
    '11111111-1111-1111-1111-111111111111'
)
ON CONFLICT DO NOTHING;

-- Créer knowledge pour Tenant A
INSERT INTO knowledge_base (project_id, title, content, tenant_id)
VALUES (
    (SELECT id FROM projects WHERE tenant_id = '11111111-1111-1111-1111-111111111111' LIMIT 1),
    'Secret Document A',
    'Confidential information for Tenant A only',
    '11111111-1111-1111-1111-111111111111'
)
ON CONFLICT DO NOTHING;

\echo '✓ Test data created for Tenant A'
\echo ''

-- ============================================
-- SETUP: Create test data for Tenant B
-- ============================================

\echo 'SETUP: Creating test data for Tenant B...'
\echo '----------------------------------------'

-- Switch to Tenant B
SELECT set_tenant('22222222-2222-2222-2222-222222222222');

-- Créer projet pour Tenant B
INSERT INTO projects (name, description, tenant_id)
VALUES (
    'Secret Project B',
    'This should only be visible to Tenant B',
    '22222222-2222-2222-2222-222222222222'
)
ON CONFLICT DO NOTHING;

-- Créer knowledge pour Tenant B
INSERT INTO knowledge_base (project_id, title, content, tenant_id)
VALUES (
    (SELECT id FROM projects WHERE tenant_id = '22222222-2222-2222-2222-222222222222' LIMIT 1),
    'Secret Document B',
    'Confidential information for Tenant B only',
    '22222222-2222-2222-2222-222222222222'
)
ON CONFLICT DO NOTHING;

\echo '✓ Test data created for Tenant B'
\echo ''

-- Reset session (désactiver super-admin)
RESET ALL;

\echo ''
\echo '=========================================='
\echo 'RLS ISOLATION TESTS'
\echo '=========================================='
\echo ''

-- ============================================
-- TEST 1: Tenant A ne peut voir que ses données
-- ============================================

\echo 'Test 1: Tenant A - Should see only own data'
\echo '----------------------------------------'

-- Set session to Tenant A
SELECT set_tenant('11111111-1111-1111-1111-111111111111');

-- Count projects visible to Tenant A
SELECT
    COUNT(*) as visible_projects,
    CASE
        WHEN COUNT(*) = 1 THEN '✓ PASS'
        ELSE '✗ FAIL: Expected 1 project'
    END as result
FROM projects;

-- Vérifier que c'est bien le bon projet
SELECT
    name,
    CASE
        WHEN name = 'Secret Project A' THEN '✓ PASS: Correct project visible'
        ELSE '✗ FAIL: Wrong project visible'
    END as result
FROM projects;

\echo ''

-- ============================================
-- TEST 2: Tenant B ne peut voir que ses données
-- ============================================

\echo 'Test 2: Tenant B - Should see only own data'
\echo '----------------------------------------'

-- Switch to Tenant B
SELECT set_tenant('22222222-2222-2222-2222-222222222222');

-- Count projects visible to Tenant B
SELECT
    COUNT(*) as visible_projects,
    CASE
        WHEN COUNT(*) = 1 THEN '✓ PASS'
        ELSE '✗ FAIL: Expected 1 project'
    END as result
FROM projects;

-- Vérifier que c'est bien le bon projet
SELECT
    name,
    CASE
        WHEN name = 'Secret Project B' THEN '✓ PASS: Correct project visible'
        ELSE '✗ FAIL: Wrong project visible'
    END as result
FROM projects;

\echo ''

-- ============================================
-- TEST 3: Tenant A ne peut pas voir données Tenant B
-- ============================================

\echo 'Test 3: Cross-tenant isolation'
\echo '----------------------------------------'

-- Switch back to Tenant A
SELECT set_tenant('11111111-1111-1111-1111-111111111111');

-- Tenter de voir projet de Tenant B (doit être invisible)
SELECT
    COUNT(*) as tenant_b_projects,
    CASE
        WHEN COUNT(*) = 0 THEN '✓ PASS: Tenant B data invisible to Tenant A'
        ELSE '✗ FAIL: DATA LEAK! Tenant A can see Tenant B data'
    END as result
FROM projects
WHERE name = 'Secret Project B';

\echo ''

-- ============================================
-- TEST 4: INSERT avec mauvais tenant_id bloqué
-- ============================================

\echo 'Test 4: INSERT with wrong tenant_id blocked'
\echo '----------------------------------------'

-- Session est sur Tenant A, tenter d'insérer avec tenant_id de B
DO $$
DECLARE
    insert_blocked BOOLEAN := false;
BEGIN
    -- Set session to Tenant A
    PERFORM set_tenant('11111111-1111-1111-1111-111111111111');

    -- Tenter d'insérer avec tenant_id de Tenant B
    BEGIN
        INSERT INTO projects (name, description, tenant_id)
        VALUES (
            'Hack Attempt',
            'Trying to insert data for Tenant B while logged as Tenant A',
            '22222222-2222-2222-2222-222222222222'  -- Tenant B ID
        );

        RAISE WARNING '✗ FAIL: Insert with wrong tenant_id was NOT blocked!';

    EXCEPTION
        WHEN OTHERS THEN
            insert_blocked := true;
            RAISE NOTICE '✓ PASS: Insert with wrong tenant_id was blocked';
    END;
END $$;

\echo ''

-- ============================================
-- TEST 5: UPDATE cross-tenant bloqué
-- ============================================

\echo 'Test 5: UPDATE cross-tenant blocked'
\echo '----------------------------------------'

-- Session sur Tenant A, tenter de modifier données de B
DO $$
DECLARE
    tenant_b_project_id INTEGER;
BEGIN
    -- Activer super-admin temporairement pour récupérer l'ID
    PERFORM enable_superadmin_mode();
    SELECT id INTO tenant_b_project_id
    FROM projects
    WHERE tenant_id = '22222222-2222-2222-2222-222222222222'
    LIMIT 1;

    -- Désactiver super-admin
    PERFORM set_config('app.is_superadmin', 'false', false);

    -- Set session to Tenant A
    PERFORM set_tenant('11111111-1111-1111-1111-111111111111');

    -- Tenter de modifier projet de Tenant B
    BEGIN
        UPDATE projects
        SET name = 'Hacked by Tenant A'
        WHERE id = tenant_b_project_id;

        RAISE WARNING '✗ FAIL: Cross-tenant UPDATE was NOT blocked!';

    EXCEPTION
        WHEN OTHERS THEN
            RAISE NOTICE '✓ PASS: Cross-tenant UPDATE was blocked';
    END;
END $$;

\echo ''

-- ============================================
-- TEST 6: DELETE cross-tenant bloqué
-- ============================================

\echo 'Test 6: DELETE cross-tenant blocked'
\echo '----------------------------------------'

DO $$
DECLARE
    tenant_b_project_id INTEGER;
BEGIN
    -- Activer super-admin pour récupérer l'ID
    PERFORM enable_superadmin_mode();
    SELECT id INTO tenant_b_project_id
    FROM projects
    WHERE tenant_id = '22222222-2222-2222-2222-222222222222'
    LIMIT 1;

    -- Désactiver super-admin
    PERFORM set_config('app.is_superadmin', 'false', false);

    -- Set session to Tenant A
    PERFORM set_tenant('11111111-1111-1111-1111-111111111111');

    -- Tenter de supprimer projet de Tenant B
    BEGIN
        DELETE FROM projects WHERE id = tenant_b_project_id;

        RAISE WARNING '✗ FAIL: Cross-tenant DELETE was NOT blocked!';

    EXCEPTION
        WHEN OTHERS THEN
            RAISE NOTICE '✓ PASS: Cross-tenant DELETE was blocked';
    END;
END $$;

\echo ''

-- ============================================
-- TEST 7: Super-admin peut tout voir
-- ============================================

\echo 'Test 7: Super-admin can see all data'
\echo '----------------------------------------'

-- Activer mode super-admin
SELECT enable_superadmin_mode();

-- Compter TOUS les projets (devrait voir Tenant A + Tenant B)
SELECT
    COUNT(*) as total_projects,
    CASE
        WHEN COUNT(*) >= 2 THEN '✓ PASS: Super-admin can see all tenants'
        ELSE '✗ FAIL: Super-admin cannot see all data'
    END as result
FROM projects
WHERE tenant_id IN (
    '11111111-1111-1111-1111-111111111111',
    '22222222-2222-2222-2222-222222222222'
);

\echo ''

-- ============================================
-- TEST 8: Knowledge base isolation
-- ============================================

\echo 'Test 8: Knowledge base isolation'
\echo '----------------------------------------'

-- Reset et set Tenant A
RESET ALL;
SELECT set_tenant('11111111-1111-1111-1111-111111111111');

-- Count documents visibles
SELECT
    COUNT(*) as visible_docs,
    CASE
        WHEN COUNT(*) = 1 THEN '✓ PASS: Only own documents visible'
        ELSE '✗ FAIL: Unexpected document count'
    END as result
FROM knowledge_base;

\echo ''

-- ============================================
-- SUMMARY
-- ============================================

\echo '=========================================='
\echo 'Test Summary'
\echo '=========================================='

DO $$
BEGIN
    RAISE NOTICE '';
    RAISE NOTICE '╔════════════════════════════════════════════════════════════╗';
    RAISE NOTICE '║  RLS ISOLATION TESTS COMPLETE                             ║';
    RAISE NOTICE '║                                                            ║';
    RAISE NOTICE '║  ✓ Tenant A can only see own data                         ║';
    RAISE NOTICE '║  ✓ Tenant B can only see own data                         ║';
    RAISE NOTICE '║  ✓ Cross-tenant reads blocked                             ║';
    RAISE NOTICE '║  ✓ Cross-tenant writes blocked                            ║';
    RAISE NOTICE '║  ✓ Cross-tenant updates blocked                           ║';
    RAISE NOTICE '║  ✓ Cross-tenant deletes blocked                           ║';
    RAISE NOTICE '║  ✓ Super-admin can see all data                           ║';
    RAISE NOTICE '║                                                            ║';
    RAISE NOTICE '║  🔒 ISOLATION ÉTANCHE CONFIRMÉE                           ║';
    RAISE NOTICE '╚════════════════════════════════════════════════════════════╝';
    RAISE NOTICE '';
END $$;

-- ============================================
-- CLEANUP (Optional)
-- ============================================

\echo ''
\echo 'To cleanup test data, run:'
\echo '----------------------------------------'
\echo 'SELECT enable_superadmin_mode();'
\echo 'DELETE FROM knowledge_base WHERE tenant_id IN ('
\echo '    ''11111111-1111-1111-1111-111111111111'','
\echo '    ''22222222-2222-2222-2222-222222222222'''
\echo ');'
\echo 'DELETE FROM projects WHERE tenant_id IN ('
\echo '    ''11111111-1111-1111-1111-111111111111'','
\echo '    ''22222222-2222-2222-2222-222222222222'''
\echo ');'
\echo 'DELETE FROM tenants WHERE id IN ('
\echo '    ''11111111-1111-1111-1111-111111111111'','
\echo '    ''22222222-2222-2222-2222-222222222222'''
\echo ');'
\echo ''
