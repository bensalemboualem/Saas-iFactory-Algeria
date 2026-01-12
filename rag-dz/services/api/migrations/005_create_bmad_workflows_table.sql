-- Migration: Create bmad_workflows table
-- Created: 2025-11-19

CREATE TABLE IF NOT EXISTS bmad_workflows (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    orchestrator_state_id INTEGER REFERENCES orchestrator_state(id) ON DELETE SET NULL,

    -- Workflow identification
    workflow_name VARCHAR(255) NOT NULL,
    workflow_type VARCHAR(100) CHECK (workflow_type IN ('architect', 'pm', 'dev', 'ux-designer', 'tea', 'orchestrator')),

    -- Execution details
    agent_id VARCHAR(100),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    duration_seconds INTEGER,

    -- Status and results
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed', 'cancelled')),
    result JSONB,
    error_message TEXT,

    -- Input/Output
    input_data JSONB DEFAULT '{}',
    output_data JSONB DEFAULT '{}',

    -- Metadata
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_bmad_workflows_project_id ON bmad_workflows(project_id);
CREATE INDEX idx_bmad_workflows_orchestrator_state_id ON bmad_workflows(orchestrator_state_id);
CREATE INDEX idx_bmad_workflows_workflow_type ON bmad_workflows(workflow_type);
CREATE INDEX idx_bmad_workflows_status ON bmad_workflows(status);
CREATE INDEX idx_bmad_workflows_created_at ON bmad_workflows(created_at DESC);

-- Update trigger for updated_at
CREATE OR REPLACE FUNCTION update_bmad_workflows_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_bmad_workflows_updated_at
    BEFORE UPDATE ON bmad_workflows
    FOR EACH ROW
    EXECUTE FUNCTION update_bmad_workflows_updated_at();
