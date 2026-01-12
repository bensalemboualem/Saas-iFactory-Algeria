-- =============================================================================
-- IAFactory Video Platform - Database Initialization
-- =============================================================================

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- =============================================================================
-- PROJECTS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    user_prompt TEXT NOT NULL,
    target_duration VARCHAR(50) DEFAULT '60s',
    aspect_ratio VARCHAR(20) DEFAULT '16:9',
    style VARCHAR(100),
    language VARCHAR(10) DEFAULT 'fr',
    target_platforms JSONB DEFAULT '[]'::jsonb,
    status VARCHAR(50) DEFAULT 'draft',
    progress JSONB DEFAULT '{}'::jsonb,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);

CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_created_at ON projects(created_at DESC);

-- =============================================================================
-- SCRIPTS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS scripts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    synopsis TEXT,
    scenes JSONB NOT NULL DEFAULT '[]'::jsonb,
    total_duration INTEGER DEFAULT 0,
    version INTEGER DEFAULT 1,
    is_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);

CREATE INDEX idx_scripts_project_id ON scripts(project_id);

-- =============================================================================
-- SCRIPT VERSIONS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS script_versions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    script_id UUID NOT NULL REFERENCES scripts(id) ON DELETE CASCADE,
    version INTEGER NOT NULL,
    scenes JSONB NOT NULL,
    change_reason TEXT,
    changed_by VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_script_versions_script_id ON script_versions(script_id);

-- =============================================================================
-- ASSETS TABLE
-- =============================================================================
CREATE TYPE asset_type AS ENUM ('image', 'video', 'audio', 'voice', 'music', 'avatar', 'subtitle');

CREATE TABLE IF NOT EXISTS assets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    type asset_type NOT NULL,
    source VARCHAR(50) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_url VARCHAR(500),
    mime_type VARCHAR(100),
    file_size INTEGER,
    duration INTEGER,
    width INTEGER,
    height INTEGER,
    generation_prompt TEXT,
    generation_params JSONB DEFAULT '{}'::jsonb,
    voice_id VARCHAR(100),
    avatar_id VARCHAR(100),
    scene_id VARCHAR(50),
    quality_score INTEGER,
    is_selected INTEGER DEFAULT 0,
    generation_cost INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_assets_project_id ON assets(project_id);
CREATE INDEX idx_assets_type ON assets(type);
CREATE INDEX idx_assets_scene_id ON assets(scene_id);

-- =============================================================================
-- VIDEOS TABLE
-- =============================================================================
CREATE TYPE video_status AS ENUM ('pending', 'processing', 'rendering', 'completed', 'failed');

CREATE TABLE IF NOT EXISTS videos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    script_id UUID REFERENCES scripts(id),
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_url VARCHAR(500),
    duration INTEGER NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    fps INTEGER DEFAULT 30,
    bitrate INTEGER,
    codec VARCHAR(50) DEFAULT 'h264',
    file_size INTEGER,
    format VARCHAR(20) DEFAULT 'mp4',
    version INTEGER DEFAULT 1,
    variant VARCHAR(50),
    timeline JSONB DEFAULT '{}'::jsonb,
    status video_status DEFAULT 'pending',
    progress INTEGER DEFAULT 0,
    error_message TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

CREATE INDEX idx_videos_project_id ON videos(project_id);
CREATE INDEX idx_videos_status ON videos(status);

-- =============================================================================
-- PUBLISH JOBS TABLE
-- =============================================================================
CREATE TYPE platform_type AS ENUM (
    'youtube', 'tiktok', 'instagram_reels', 'instagram_post', 'instagram_story',
    'facebook', 'linkedin', 'twitter', 'pinterest', 'snapchat', 'twitch'
);

CREATE TYPE publish_status AS ENUM (
    'scheduled', 'pending', 'uploading', 'processing', 'published', 'failed', 'cancelled'
);

CREATE TABLE IF NOT EXISTS publish_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    video_id UUID NOT NULL REFERENCES videos(id) ON DELETE CASCADE,
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    platform platform_type NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    tags JSONB DEFAULT '[]'::jsonb,
    thumbnail_url VARCHAR(500),
    platform_settings JSONB DEFAULT '{}'::jsonb,
    scheduled_at TIMESTAMPTZ,
    is_scheduled BOOLEAN DEFAULT FALSE,
    status publish_status DEFAULT 'pending',
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    platform_post_id VARCHAR(255),
    platform_url VARCHAR(500),
    analytics JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    published_at TIMESTAMPTZ
);

CREATE INDEX idx_publish_jobs_video_id ON publish_jobs(video_id);
CREATE INDEX idx_publish_jobs_project_id ON publish_jobs(project_id);
CREATE INDEX idx_publish_jobs_platform ON publish_jobs(platform);
CREATE INDEX idx_publish_jobs_status ON publish_jobs(status);
CREATE INDEX idx_publish_jobs_scheduled_at ON publish_jobs(scheduled_at) WHERE is_scheduled = TRUE;

-- =============================================================================
-- CONNECTED ACCOUNTS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS connected_accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    platform platform_type NOT NULL,
    account_name VARCHAR(255) NOT NULL,
    account_id VARCHAR(255),
    access_token TEXT,
    refresh_token TEXT,
    token_expires_at TIMESTAMPTZ,
    scopes JSONB DEFAULT '[]'::jsonb,
    metadata JSONB DEFAULT '{}'::jsonb,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);

CREATE INDEX idx_connected_accounts_platform ON connected_accounts(platform);
CREATE INDEX idx_connected_accounts_is_active ON connected_accounts(is_active);

-- =============================================================================
-- USAGE & COSTS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS usage_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE SET NULL,
    provider VARCHAR(50) NOT NULL,
    operation VARCHAR(100) NOT NULL,
    cost_cents INTEGER DEFAULT 0,
    tokens_used INTEGER,
    duration_ms INTEGER,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_usage_logs_project_id ON usage_logs(project_id);
CREATE INDEX idx_usage_logs_provider ON usage_logs(provider);
CREATE INDEX idx_usage_logs_created_at ON usage_logs(created_at DESC);

-- =============================================================================
-- FUNCTIONS
-- =============================================================================

-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to tables
CREATE TRIGGER trigger_projects_updated_at
    BEFORE UPDATE ON projects
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trigger_scripts_updated_at
    BEFORE UPDATE ON scripts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trigger_connected_accounts_updated_at
    BEFORE UPDATE ON connected_accounts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

-- =============================================================================
-- SEED DATA (Optional - remove in production)
-- =============================================================================

-- Insert sample connected account for testing
-- INSERT INTO connected_accounts (platform, account_name, is_active)
-- VALUES ('youtube', 'Test Channel', true);

COMMIT;
