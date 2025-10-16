-- ============================================================
-- PRODUCTION DATABASE FIX - Add Missing Columns
-- Run this BEFORE running production_init.sql
-- This script is safe to run multiple times (uses IF NOT EXISTS)
-- ============================================================

-- Fix Event table - add missing columns if they don't exist
DO $$ 
BEGIN
    -- Add allow_short_selling if it doesn't exist
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name='app1_event' AND column_name='allow_short_selling') THEN
        ALTER TABLE app1_event ADD COLUMN allow_short_selling BOOLEAN DEFAULT false;
    END IF;
    
    -- Add max_trades_per_team if it doesn't exist
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name='app1_event' AND column_name='max_trades_per_team') THEN
        ALTER TABLE app1_event ADD COLUMN max_trades_per_team INTEGER NULL;
    END IF;
    
    -- Add trading_fee_percentage if it doesn't exist
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name='app1_event' AND column_name='trading_fee_percentage') THEN
        ALTER TABLE app1_event ADD COLUMN trading_fee_percentage NUMERIC(5,2) DEFAULT 0.00;
    END IF;
    
    -- Remove status column if it exists (it's a property, not a field)
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='app1_event' AND column_name='status') THEN
        ALTER TABLE app1_event DROP COLUMN status;
    END IF;
END $$;

-- Fix Stock table - add sector if it doesn't exist
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name='app1_stock' AND column_name='sector') THEN
        ALTER TABLE app1_stock ADD COLUMN sector VARCHAR(50) DEFAULT 'Technology';
    END IF;
END $$;

-- Verify the fix
SELECT 
    'app1_event' as table_name,
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'app1_event'
ORDER BY ordinal_position;

SELECT 
    'app1_stock' as table_name,
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'app1_stock'
ORDER BY ordinal_position;

-- ============================================================
-- SUCCESS! Now run production_init.sql to add the data
-- ============================================================
