-- Migration 003: Tables pour Bolt SuperPower Workflow System
-- Date: 2025-01-19
-- Description: Crée les tables pour gérer les workflows Bolt-DIY avec orchestration BMAD

-- ============================================================
-- Table: bolt_workflows
-- Description: Stocke les workflows de génération de projets
-- ============================================================

CREATE TABLE IF NOT EXISTS bolt_workflows (
    id SERIAL PRIMARY KEY,
    workflow_id UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    mode VARCHAR(20) NOT NULL CHECK (mode IN ('direct', 'bmad')),
    user_description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'orchestrating', 'generating', 'completed', 'failed')),
    current_agent VARCHAR(50),
    agents_completed JSONB DEFAULT '[]'::jsonb,
    tech_stack JSONB,
    archon_project_id INTEGER,
    knowledge_source_id VARCHAR(100),
    zip_file_path TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Index pour recherche rapide par workflow_id
CREATE INDEX IF NOT EXISTS idx_bolt_workflow_id ON bolt_workflows(workflow_id);

-- Index pour recherche par statut
CREATE INDEX IF NOT EXISTS idx_bolt_workflow_status ON bolt_workflows(status);

-- Index pour recherche par archon_project_id
CREATE INDEX IF NOT EXISTS idx_bolt_archon_project ON bolt_workflows(archon_project_id);

-- Index pour recherche par date de création
CREATE INDEX IF NOT EXISTS idx_bolt_workflow_created_at ON bolt_workflows(created_at DESC);

-- Index pour recherche par mode
CREATE INDEX IF NOT EXISTS idx_bolt_workflow_mode ON bolt_workflows(mode);


-- ============================================================
-- Table: agent_executions
-- Description: Stocke les exécutions individuelles des agents BMAD
-- ============================================================

CREATE TABLE IF NOT EXISTS agent_executions (
    id SERIAL PRIMARY KEY,
    workflow_id UUID NOT NULL,
    agent_name VARCHAR(100) NOT NULL,
    agent_id VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'running', 'completed', 'failed')),
    input_context JSONB,
    output_result TEXT,
    output_summary TEXT,
    execution_time_seconds INTEGER,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT,
    CONSTRAINT fk_workflow
        FOREIGN KEY (workflow_id)
        REFERENCES bolt_workflows(workflow_id)
        ON DELETE CASCADE
);

-- Index composite pour recherche par workflow et agent
CREATE INDEX IF NOT EXISTS idx_agent_workflow_agent
    ON agent_executions(workflow_id, agent_name);

-- Index pour recherche par statut
CREATE INDEX IF NOT EXISTS idx_agent_status ON agent_executions(status);

-- Index pour recherche par date de début
CREATE INDEX IF NOT EXISTS idx_agent_started_at ON agent_executions(started_at DESC);


-- ============================================================
-- Table: workflow_artifacts
-- Description: Stocke les fichiers/artefacts générés par les workflows
-- ============================================================

CREATE TABLE IF NOT EXISTS workflow_artifacts (
    id SERIAL PRIMARY KEY,
    workflow_id UUID NOT NULL,
    artifact_type VARCHAR(50) NOT NULL
        CHECK (artifact_type IN ('documentation', 'code', 'test', 'config', 'diagram', 'zip')),
    file_name VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    file_size_bytes BIGINT,
    mime_type VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb,
    CONSTRAINT fk_workflow_artifacts
        FOREIGN KEY (workflow_id)
        REFERENCES bolt_workflows(workflow_id)
        ON DELETE CASCADE
);

-- Index pour recherche par workflow
CREATE INDEX IF NOT EXISTS idx_artifacts_workflow ON workflow_artifacts(workflow_id);

-- Index pour recherche par type
CREATE INDEX IF NOT EXISTS idx_artifacts_type ON workflow_artifacts(artifact_type);


-- ============================================================
-- Fonctions utilitaires
-- ============================================================

-- Fonction pour obtenir le statut complet d'un workflow
CREATE OR REPLACE FUNCTION get_workflow_status(p_workflow_id UUID)
RETURNS JSON AS $$
DECLARE
    v_result JSON;
BEGIN
    SELECT json_build_object(
        'workflow', row_to_json(w.*),
        'agents', (
            SELECT json_agg(row_to_json(a.*))
            FROM agent_executions a
            WHERE a.workflow_id = p_workflow_id
            ORDER BY a.started_at
        ),
        'artifacts', (
            SELECT json_agg(row_to_json(ar.*))
            FROM workflow_artifacts ar
            WHERE ar.workflow_id = p_workflow_id
        )
    ) INTO v_result
    FROM bolt_workflows w
    WHERE w.workflow_id = p_workflow_id;

    RETURN v_result;
END;
$$ LANGUAGE plpgsql;


-- Fonction pour calculer la progression d'un workflow BMAD
CREATE OR REPLACE FUNCTION calculate_workflow_progress(p_workflow_id UUID)
RETURNS INTEGER AS $$
DECLARE
    v_total_agents INTEGER;
    v_completed_agents INTEGER;
    v_progress INTEGER;
BEGIN
    -- Compter le nombre total d'agents
    SELECT COUNT(*) INTO v_total_agents
    FROM agent_executions
    WHERE workflow_id = p_workflow_id;

    -- Si aucun agent, retourner 0
    IF v_total_agents = 0 THEN
        RETURN 0;
    END IF;

    -- Compter les agents complétés
    SELECT COUNT(*) INTO v_completed_agents
    FROM agent_executions
    WHERE workflow_id = p_workflow_id
        AND status = 'completed';

    -- Calculer le pourcentage
    v_progress := ROUND((v_completed_agents::NUMERIC / v_total_agents::NUMERIC) * 100);

    RETURN v_progress;
END;
$$ LANGUAGE plpgsql;


-- Fonction pour nettoyer les vieux workflows (plus de 30 jours)
CREATE OR REPLACE FUNCTION cleanup_old_workflows()
RETURNS INTEGER AS $$
DECLARE
    v_deleted_count INTEGER;
BEGIN
    WITH deleted AS (
        DELETE FROM bolt_workflows
        WHERE created_at < NOW() - INTERVAL '30 days'
            AND status IN ('completed', 'failed')
        RETURNING id
    )
    SELECT COUNT(*) INTO v_deleted_count FROM deleted;

    RETURN v_deleted_count;
END;
$$ LANGUAGE plpgsql;


-- ============================================================
-- Triggers
-- ============================================================

-- Trigger pour mettre à jour completed_at automatiquement
CREATE OR REPLACE FUNCTION update_workflow_completed_at()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status IN ('completed', 'failed') AND OLD.status NOT IN ('completed', 'failed') THEN
        NEW.completed_at := NOW();
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_workflow_completed_at
    BEFORE UPDATE ON bolt_workflows
    FOR EACH ROW
    EXECUTE FUNCTION update_workflow_completed_at();


-- ============================================================
-- Vues utiles
-- ============================================================

-- Vue pour les workflows actifs
CREATE OR REPLACE VIEW active_workflows AS
SELECT
    w.workflow_id,
    w.mode,
    w.status,
    w.current_agent,
    w.created_at,
    EXTRACT(EPOCH FROM (NOW() - w.created_at))::INTEGER as elapsed_seconds,
    calculate_workflow_progress(w.workflow_id) as progress_percent,
    (
        SELECT COUNT(*)
        FROM agent_executions ae
        WHERE ae.workflow_id = w.workflow_id
            AND ae.status = 'completed'
    ) as agents_completed_count,
    (
        SELECT COUNT(*)
        FROM agent_executions ae
        WHERE ae.workflow_id = w.workflow_id
    ) as total_agents_count
FROM bolt_workflows w
WHERE w.status IN ('pending', 'orchestrating', 'generating')
ORDER BY w.created_at DESC;


-- Vue pour les statistiques des workflows
CREATE OR REPLACE VIEW workflow_statistics AS
SELECT
    mode,
    status,
    COUNT(*) as count,
    AVG(EXTRACT(EPOCH FROM (completed_at - created_at)))::INTEGER as avg_duration_seconds,
    MIN(EXTRACT(EPOCH FROM (completed_at - created_at)))::INTEGER as min_duration_seconds,
    MAX(EXTRACT(EPOCH FROM (completed_at - created_at)))::INTEGER as max_duration_seconds
FROM bolt_workflows
WHERE completed_at IS NOT NULL
GROUP BY mode, status
ORDER BY mode, status;


-- ============================================================
-- Données de test (commentées par défaut)
-- ============================================================

/*
-- Exemple d'insertion d'un workflow de test
INSERT INTO bolt_workflows (mode, user_description, status, tech_stack, metadata)
VALUES (
    'bmad',
    'Créer une application de todo list collaborative',
    'pending',
    '["React", "TypeScript", "Supabase", "TailwindCSS"]'::jsonb,
    '{"constraints": {"budget": "low", "timeline": "1 week"}, "preferences": {"tech_stack": "modern"}}'::jsonb
);

-- Exemple d'insertion d'agents pour le workflow
INSERT INTO agent_executions (workflow_id, agent_name, agent_id, status)
SELECT
    workflow_id,
    agent,
    agent_id,
    'pending'
FROM bolt_workflows,
     (VALUES
         ('Architect Agent', 'architect'),
         ('PM Agent', 'pm'),
         ('Backend Dev Agent', 'backend'),
         ('Frontend Dev Agent', 'frontend'),
         ('DevOps Agent', 'devops'),
         ('QA Agent', 'qa')
     ) AS agents(agent, agent_id)
WHERE mode = 'bmad'
LIMIT 1;
*/


-- ============================================================
-- Permissions (à adapter selon vos besoins)
-- ============================================================

-- Exemple de permissions pour un rôle application
-- GRANT SELECT, INSERT, UPDATE, DELETE ON bolt_workflows TO app_role;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON agent_executions TO app_role;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON workflow_artifacts TO app_role;
-- GRANT USAGE, SELECT ON SEQUENCE bolt_workflows_id_seq TO app_role;
-- GRANT USAGE, SELECT ON SEQUENCE agent_executions_id_seq TO app_role;
-- GRANT USAGE, SELECT ON SEQUENCE workflow_artifacts_id_seq TO app_role;


-- ============================================================
-- Fin de la migration
-- ============================================================

-- Vérification de la migration
DO $$
BEGIN
    RAISE NOTICE 'Migration 003_bolt_workflows.sql complétée avec succès!';
    RAISE NOTICE 'Tables créées: bolt_workflows, agent_executions, workflow_artifacts';
    RAISE NOTICE 'Fonctions créées: get_workflow_status, calculate_workflow_progress, cleanup_old_workflows';
    RAISE NOTICE 'Vues créées: active_workflows, workflow_statistics';
END $$;
