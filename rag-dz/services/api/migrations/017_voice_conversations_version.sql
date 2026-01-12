-- Migration 017: Add version column to voice_conversations
-- Date: 2025-12-30
-- Purpose: Optimistic locking pour voice_conversations

-- Add version column if not exists
DO $$ BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'voice_conversations' AND column_name = 'version'
    ) THEN
        ALTER TABLE voice_conversations ADD COLUMN version INTEGER NOT NULL DEFAULT 1;
        RAISE NOTICE 'Added version column to voice_conversations';
    END IF;
END $$;

-- Create trigger to auto-increment version on update
CREATE OR REPLACE FUNCTION increment_voice_conversation_version()
RETURNS TRIGGER AS $$
BEGIN
    NEW.version := COALESCE(OLD.version, 0) + 1;
    NEW.updated_at := NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Drop existing trigger if exists and recreate
DROP TRIGGER IF EXISTS tr_voice_conversations_version ON voice_conversations;

CREATE TRIGGER tr_voice_conversations_version
    BEFORE UPDATE ON voice_conversations
    FOR EACH ROW
    EXECUTE FUNCTION increment_voice_conversation_version();

COMMENT ON COLUMN voice_conversations.version IS 'Optimistic locking version - auto-incremented on update';

DO $$ BEGIN
    RAISE NOTICE 'Migration 017 complete: voice_conversations now has version column';
END $$;
