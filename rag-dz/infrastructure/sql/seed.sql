-- Seed data for RAG.dz
-- Creates demo tenant and API keys for testing

-- Insert demo tenant
INSERT INTO tenants (id, name, plan, status, created_at)
VALUES
    ('00000000-0000-0000-0000-000000000001'::uuid, 'Demo Company', 'pro', 'active', NOW()),
    ('00000000-0000-0000-0000-000000000002'::uuid, 'Test Enterprise', 'enterprise', 'active', NOW())
ON CONFLICT (id) DO NOTHING;

-- Insert API keys
-- Key: ragdz_dev_demo_key_12345678901234567890
-- Hash: SHA256 of the above key
INSERT INTO api_keys (id, key_hash, tenant_id, name, plan, quota_tokens_monthly, quota_audio_seconds_monthly, quota_ocr_pages_monthly, rate_limit_per_minute, created_at, revoked)
VALUES
    (
        '10000000-0000-0000-0000-000000000001'::uuid,
        'e8c4f7b8d9e6c8a5f3b2d1a9e7c6b5a4d3c2b1a0f9e8d7c6b5a4d3c2b1a0f9e8',
        '00000000-0000-0000-0000-000000000001'::uuid,
        'Demo API Key',
        'pro',
        1000000,
        3600,
        100,
        60,
        NOW(),
        false
    ),
    (
        '10000000-0000-0000-0000-000000000002'::uuid,
        'f9d5e8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b2a1f0e9',
        '00000000-0000-0000-0000-000000000002'::uuid,
        'Enterprise API Key',
        'enterprise',
        10000000,
        36000,
        1000,
        120,
        NOW(),
        false
    )
ON CONFLICT (id) DO NOTHING;

-- Display created credentials
SELECT
    t.name as tenant_name,
    t.plan,
    k.name as key_name,
    'ragdz_dev_demo_key_12345678901234567890' as api_key,
    k.rate_limit_per_minute
FROM tenants t
JOIN api_keys k ON t.id = k.tenant_id
WHERE NOT k.revoked;
