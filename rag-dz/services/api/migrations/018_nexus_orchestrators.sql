-- Migration 018: Tables Nexus Orchestrators
-- Pour le système d'orchestration Nexus (Meta, Archon, BMAD, Bolt)

-- ============================================
-- Table des tâches Nexus
-- ============================================
CREATE TABLE IF NOT EXISTS nexus_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'todo' CHECK (status IN ('todo', 'doing', 'review', 'done', 'blocked')),
    assigned_to TEXT,
    project_id UUID,
    priority INTEGER DEFAULT 0,
    created_by TEXT,
    tenant_id UUID NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- Table de la Knowledge Base
-- ============================================
CREATE TABLE IF NOT EXISTS nexus_knowledge (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('doc', 'code', 'url', 'artifact', 'prd', 'architecture')),
    source TEXT,
    embedding VECTOR(1536),
    metadata JSONB DEFAULT '{}',
    tenant_id UUID NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- Table des projets
-- ============================================
CREATE TABLE IF NOT EXISTS nexus_projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'paused', 'completed', 'archived')),
    tenant_id UUID NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- Table des locks (Single-Writer Rule)
-- ============================================
CREATE TABLE IF NOT EXISTS nexus_locks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resource TEXT NOT NULL,
    holder TEXT NOT NULL,
    lock_type TEXT DEFAULT 'exclusive' CHECK (lock_type IN ('exclusive', 'shared')),
    acquired_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL,
    metadata JSONB DEFAULT '{}',
    UNIQUE(resource, holder)
);

-- ============================================
-- Table des sessions orchestrateur
-- ============================================
CREATE TABLE IF NOT EXISTS nexus_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id TEXT NOT NULL UNIQUE,
    user_id UUID,
    tenant_id UUID NOT NULL,
    context JSONB DEFAULT '{}',
    last_orchestrator TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ
);

-- ============================================
-- Table des workflows BMAD
-- ============================================
CREATE TABLE IF NOT EXISTS nexus_workflows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    execution_id TEXT NOT NULL UNIQUE,
    workflow_type TEXT NOT NULL,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed', 'cancelled')),
    current_step INTEGER DEFAULT 0,
    steps JSONB DEFAULT '[]',
    input_data JSONB DEFAULT '{}',
    results JSONB DEFAULT '{}',
    error TEXT,
    tenant_id UUID NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

-- ============================================
-- Index pour performance
-- ============================================
CREATE INDEX IF NOT EXISTS idx_nexus_tasks_status ON nexus_tasks(status);
CREATE INDEX IF NOT EXISTS idx_nexus_tasks_tenant ON nexus_tasks(tenant_id);
CREATE INDEX IF NOT EXISTS idx_nexus_tasks_project ON nexus_tasks(project_id);
CREATE INDEX IF NOT EXISTS idx_nexus_tasks_assigned ON nexus_tasks(assigned_to);

CREATE INDEX IF NOT EXISTS idx_nexus_knowledge_type ON nexus_knowledge(type);
CREATE INDEX IF NOT EXISTS idx_nexus_knowledge_tenant ON nexus_knowledge(tenant_id);

CREATE INDEX IF NOT EXISTS idx_nexus_projects_status ON nexus_projects(status);
CREATE INDEX IF NOT EXISTS idx_nexus_projects_tenant ON nexus_projects(tenant_id);

CREATE INDEX IF NOT EXISTS idx_nexus_locks_resource ON nexus_locks(resource);
CREATE INDEX IF NOT EXISTS idx_nexus_locks_expires ON nexus_locks(expires_at);

CREATE INDEX IF NOT EXISTS idx_nexus_sessions_tenant ON nexus_sessions(tenant_id);
CREATE INDEX IF NOT EXISTS idx_nexus_sessions_expires ON nexus_sessions(expires_at);

CREATE INDEX IF NOT EXISTS idx_nexus_workflows_status ON nexus_workflows(status);
CREATE INDEX IF NOT EXISTS idx_nexus_workflows_tenant ON nexus_workflows(tenant_id);

-- ============================================
-- RLS obligatoire (sécurité multi-tenant)
-- ============================================
ALTER TABLE nexus_tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE nexus_knowledge ENABLE ROW LEVEL SECURITY;
ALTER TABLE nexus_projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE nexus_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE nexus_workflows ENABLE ROW LEVEL SECURITY;

-- Locks n'ont pas besoin de RLS (gérés par l'orchestrateur)

-- ============================================
-- Policies RLS - Isolation par tenant
-- ============================================

-- Tasks
CREATE POLICY "tenant_isolation_tasks" ON nexus_tasks
    FOR ALL USING (
        tenant_id = COALESCE(
            current_setting('app.tenant_id', true)::uuid,
            '00000000-0000-0000-0000-000000000000'::uuid
        )
    );

-- Knowledge
CREATE POLICY "tenant_isolation_knowledge" ON nexus_knowledge
    FOR ALL USING (
        tenant_id = COALESCE(
            current_setting('app.tenant_id', true)::uuid,
            '00000000-0000-0000-0000-000000000000'::uuid
        )
    );

-- Projects
CREATE POLICY "tenant_isolation_projects" ON nexus_projects
    FOR ALL USING (
        tenant_id = COALESCE(
            current_setting('app.tenant_id', true)::uuid,
            '00000000-0000-0000-0000-000000000000'::uuid
        )
    );

-- Sessions
CREATE POLICY "tenant_isolation_sessions" ON nexus_sessions
    FOR ALL USING (
        tenant_id = COALESCE(
            current_setting('app.tenant_id', true)::uuid,
            '00000000-0000-0000-0000-000000000000'::uuid
        )
    );

-- Workflows
CREATE POLICY "tenant_isolation_workflows" ON nexus_workflows
    FOR ALL USING (
        tenant_id = COALESCE(
            current_setting('app.tenant_id', true)::uuid,
            '00000000-0000-0000-0000-000000000000'::uuid
        )
    );

-- ============================================
-- Fonction de nettoyage des locks expirés
-- ============================================
CREATE OR REPLACE FUNCTION cleanup_expired_locks()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM nexus_locks WHERE expires_at < NOW();
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- Trigger pour updated_at automatique
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_nexus_tasks_updated_at
    BEFORE UPDATE ON nexus_tasks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_nexus_projects_updated_at
    BEFORE UPDATE ON nexus_projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_nexus_sessions_updated_at
    BEFORE UPDATE ON nexus_sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_nexus_workflows_updated_at
    BEFORE UPDATE ON nexus_workflows
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- Commentaires
-- ============================================
COMMENT ON TABLE nexus_tasks IS 'Tâches gérées par les orchestrateurs Nexus';
COMMENT ON TABLE nexus_knowledge IS 'Knowledge Base pour la recherche sémantique';
COMMENT ON TABLE nexus_projects IS 'Projets regroupant les tâches';
COMMENT ON TABLE nexus_locks IS 'Locks pour la Single-Writer Rule (Bolt seul écrit)';
COMMENT ON TABLE nexus_sessions IS 'Sessions utilisateur pour le contexte';
COMMENT ON TABLE nexus_workflows IS 'Exécutions de workflows BMAD';
