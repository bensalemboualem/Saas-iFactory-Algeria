-- ============================================================
-- IAFactory Database Initialization
-- Creates dual schemas: lobe (main app) + gateway (API billing)
-- ============================================================

-- Create schemas
CREATE SCHEMA IF NOT EXISTS lobe;
CREATE SCHEMA IF NOT EXISTS gateway;

-- Grant privileges
GRANT ALL ON SCHEMA lobe TO iafactory;
GRANT ALL ON SCHEMA gateway TO iafactory;

-- Set default search path
ALTER DATABASE iafactory SET search_path TO lobe, gateway, public;

-- Log initialization
DO $$
BEGIN
  RAISE NOTICE 'IAFactory database initialized with schemas: lobe, gateway';
END $$;
