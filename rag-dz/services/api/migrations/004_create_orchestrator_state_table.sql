-- Migration: Create orchestrator_state table
-- Created: 2025-11-19

CREATE TABLE IF NOT EXISTS orchestrator_state (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,

    -- Agent tracking
    agents_consulted TEXT[] DEFAULT '{}',
    messages_count INTEGER DEFAULT 0,

    -- Project signals
    architecture_defined BOOLEAN DEFAULT FALSE,
    requirements_clear BOOLEAN DEFAULT FALSE,
    tech_stack_chosen BOOLEAN DEFAULT FALSE,
    ux_specified BOOLEAN DEFAULT FALSE,
    tests_planned BOOLEAN DEFAULT FALSE,

    -- Readiness assessment
    confidence_score INTEGER DEFAULT 0 CHECK (confidence_score >= 0 AND confidence_score <= 100),
    project_ready BOOLEAN DEFAULT FALSE,

    -- Knowledge base reference
    knowledge_base_id VARCHAR(255),
    knowledge_doc_path VARCHAR(500),

    -- Production order tracking
    production_ordered BOOLEAN DEFAULT FALSE,
    production_command JSONB,
    bolt_url VARCHAR(500),

    -- Status tracking
    status VARCHAR(50) DEFAULT 'analyzing' CHECK (status IN ('analyzing', 'ready', 'producing', 'completed', 'failed')),

    -- Metadata
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE UNIQUE INDEX idx_orchestrator_state_project_id ON orchestrator_state(project_id);
CREATE INDEX idx_orchestrator_state_status ON orchestrator_state(status);
CREATE INDEX idx_orchestrator_state_project_ready ON orchestrator_state(project_ready);
CREATE INDEX idx_orchestrator_state_created_at ON orchestrator_state(created_at DESC);

-- Update trigger for updated_at
CREATE OR REPLACE FUNCTION update_orchestrator_state_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_orchestrator_state_updated_at
    BEFORE UPDATE ON orchestrator_state
    FOR EACH ROW
    EXECUTE FUNCTION update_orchestrator_state_updated_at();
