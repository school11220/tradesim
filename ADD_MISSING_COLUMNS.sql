-- ============================================================
-- COMPLETE MISSING COLUMNS FIX
-- This adds ALL missing columns that Django models expect
-- Run this ENTIRE script in Neon SQL Console
-- ============================================================

-- Fix SimulatorSettings table
DO $$ 
BEGIN
    -- Add last_updated if missing
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name='app1_simulatorsettings' AND column_name='last_updated') THEN
        ALTER TABLE app1_simulatorsettings ADD COLUMN last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW();
        RAISE NOTICE 'Added last_updated to SimulatorSettings';
    END IF;
END $$;

-- Update any NULL values
UPDATE app1_simulatorsettings 
SET last_updated = NOW() 
WHERE last_updated IS NULL;

-- Verify tables have all required columns
SELECT 'SimulatorSettings columns:' as check_name;
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'app1_simulatorsettings'
ORDER BY ordinal_position;

SELECT 'Stock columns:' as check_name;
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'app1_stock'
ORDER BY ordinal_position;

SELECT 'Event columns:' as check_name;
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'app1_event'
ORDER BY ordinal_position;

-- Final verification
SELECT 'Fix complete!' as status;
