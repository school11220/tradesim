-- ============================================================
-- DIAGNOSTIC SCRIPT - Run this FIRST in Neon
-- This tells us what's wrong so we can fix it
-- ============================================================

-- Check 1: What tables exist?
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' AND table_name LIKE 'app1%'
ORDER BY table_name;

-- Check 2: Event table columns
SELECT column_name, data_type, is_nullable
FROM information_schema.columns 
WHERE table_name = 'app1_event'
ORDER BY ordinal_position;

-- Check 3: Stock table columns
SELECT column_name, data_type, is_nullable
FROM information_schema.columns 
WHERE table_name = 'app1_stock'
ORDER BY ordinal_position;

-- Check 4: SimulatorSettings table columns
SELECT column_name, data_type, is_nullable
FROM information_schema.columns 
WHERE table_name = 'app1_simulatorsettings'
ORDER BY ordinal_position;

-- Check 5: Team table columns
SELECT column_name, data_type, is_nullable
FROM information_schema.columns 
WHERE table_name = 'app1_team'
ORDER BY ordinal_position;

-- Check 6: How much data exists?
SELECT 
    (SELECT COUNT(*) FROM app1_event) as event_count,
    (SELECT COUNT(*) FROM app1_simulatorsettings) as settings_count,
    (SELECT COUNT(*) FROM app1_stock) as stock_count,
    (SELECT COUNT(*) FROM app1_team) as team_count;

-- Check 7: What events exist?
SELECT id, name, is_active, registration_open, start_time, end_time
FROM app1_event;

-- Check 8: What stocks exist?
SELECT symbol, name, sector, current_price, is_active
FROM app1_stock
LIMIT 10;

-- Check 9: What settings exist?
SELECT setting_name, setting_value, description
FROM app1_simulatorsettings;
