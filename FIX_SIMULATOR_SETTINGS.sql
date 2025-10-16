-- ============================================================
-- ADD MISSING last_updated COLUMN TO SIMULATOR SETTINGS
-- Run this in Neon SQL Console NOW
-- ============================================================

-- Add last_updated column to app1_simulatorsettings
ALTER TABLE app1_simulatorsettings 
ADD COLUMN IF NOT EXISTS last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW();

-- Update existing rows to have current timestamp
UPDATE app1_simulatorsettings 
SET last_updated = NOW() 
WHERE last_updated IS NULL;

-- Verify it worked
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'app1_simulatorsettings'
ORDER BY ordinal_position;

-- You should now see: setting_name, setting_value, description, last_updated
