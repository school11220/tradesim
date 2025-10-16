-- ============================================================
-- PRODUCTION DATABASE FIX V2 - CORRECTED VERSION
-- Run this in Neon SQL Console
-- Safe to run multiple times
-- ============================================================

-- STEP 1: Fix Event table (add missing columns)
-- ============================================================
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name='app1_event' AND column_name='allow_short_selling') THEN
        ALTER TABLE app1_event ADD COLUMN allow_short_selling BOOLEAN DEFAULT false;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name='app1_event' AND column_name='max_trades_per_team') THEN
        ALTER TABLE app1_event ADD COLUMN max_trades_per_team INTEGER NULL;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name='app1_event' AND column_name='trading_fee_percentage') THEN
        ALTER TABLE app1_event ADD COLUMN trading_fee_percentage NUMERIC(5,2) DEFAULT 0.00;
    END IF;
END $$;

-- STEP 2: Fix Stock table (add missing columns)
-- ============================================================
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name='app1_stock' AND column_name='sector') THEN
        ALTER TABLE app1_stock ADD COLUMN sector VARCHAR(50) DEFAULT 'Technology';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name='app1_stock' AND column_name='created_at') THEN
        ALTER TABLE app1_stock ADD COLUMN created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
    END IF;
END $$;

-- STEP 3: Create Event (if not exists)
-- ============================================================
INSERT INTO app1_event (name, description, start_time, end_time, initial_capital, registration_open, is_active, allow_short_selling, max_trades_per_team, trading_fee_percentage, created_at, updated_at)
SELECT 
    'Stock Trading Competition 2025',
    'Annual stock trading competition for teams',
    NOW(),
    NOW() + INTERVAL '30 days',
    100000.00,
    true,
    true,
    false,
    NULL,
    0.00,
    NOW(),
    NOW()
WHERE NOT EXISTS (SELECT 1 FROM app1_event WHERE name = 'Stock Trading Competition 2025');

-- STEP 4: Create Settings (if not exists)
-- ============================================================
INSERT INTO app1_simulatorsettings (setting_name, setting_value, description)
SELECT 'default_user_balance', '10000', 'Default balance for new users'
WHERE NOT EXISTS (SELECT 1 FROM app1_simulatorsettings WHERE setting_name = 'default_user_balance');

INSERT INTO app1_simulatorsettings (setting_name, setting_value, description)
SELECT 'default_team_balance', '100000', 'Default balance for new teams'
WHERE NOT EXISTS (SELECT 1 FROM app1_simulatorsettings WHERE setting_name = 'default_team_balance');

-- STEP 5: Create Stocks (only basic columns - NO computed fields)
-- ============================================================
-- Technology Stocks
INSERT INTO app1_stock (symbol, name, sector, current_price, previous_close, is_active, last_updated, created_at)
SELECT 'AAPL', 'Apple Inc.', 'Technology', 150.50, 148.20, true, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM app1_stock WHERE symbol = 'AAPL');

INSERT INTO app1_stock (symbol, name, sector, current_price, previous_close, is_active, last_updated, created_at)
SELECT 'MSFT', 'Microsoft Corporation', 'Technology', 320.75, 318.50, true, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM app1_stock WHERE symbol = 'MSFT');

INSERT INTO app1_stock (symbol, name, sector, current_price, previous_close, is_active, last_updated, created_at)
SELECT 'GOOGL', 'Alphabet Inc.', 'Technology', 125.80, 124.30, true, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM app1_stock WHERE symbol = 'GOOGL');

INSERT INTO app1_stock (symbol, name, sector, current_price, previous_close, is_active, last_updated, created_at)
SELECT 'META', 'Meta Platforms Inc.', 'Technology', 305.25, 302.10, true, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM app1_stock WHERE symbol = 'META');

INSERT INTO app1_stock (symbol, name, sector, current_price, previous_close, is_active, last_updated, created_at)
SELECT 'NVDA', 'NVIDIA Corporation', 'Technology', 455.60, 450.20, true, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM app1_stock WHERE symbol = 'NVDA');

INSERT INTO app1_stock (symbol, name, sector, current_price, previous_close, is_active, last_updated, created_at)
SELECT 'ADBE', 'Adobe Inc.', 'Technology', 535.80, 532.40, true, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM app1_stock WHERE symbol = 'ADBE');

INSERT INTO app1_stock (symbol, name, sector, current_price, previous_close, is_active, last_updated, created_at)
SELECT 'CRM', 'Salesforce Inc.', 'Technology', 215.30, 213.80, true, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM app1_stock WHERE symbol = 'CRM');

INSERT INTO app1_stock (symbol, name, sector, current_price, previous_close, is_active, last_updated, created_at)
SELECT 'ORCL', 'Oracle Corporation', 'Technology', 98.45, 97.20, true, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM app1_stock WHERE symbol = 'ORCL');

INSERT INTO app1_stock (symbol, name, sector, current_price, previous_close, is_active, last_updated, created_at)
SELECT 'AMD', 'Advanced Micro Devices', 'Technology', 112.45, 110.80, true, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM app1_stock WHERE symbol = 'AMD');

-- Healthcare Stocks
INSERT INTO app1_stock (symbol, name, sector, current_price, previous_close, is_active, last_updated, created_at)
SELECT 'JNJ', 'Johnson & Johnson', 'Healthcare', 165.40, 164.20, true, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM app1_stock WHERE symbol = 'JNJ');

INSERT INTO app1_stock (symbol, name, sector, current_price, previous_close, is_active, last_updated, created_at)
SELECT 'UNH', 'UnitedHealth Group', 'Healthcare', 485.90, 483.50, true, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM app1_stock WHERE symbol = 'UNH');

INSERT INTO app1_stock (symbol, name, sector, current_price, previous_close, is_active, last_updated, created_at)
SELECT 'PFE', 'Pfizer Inc.', 'Healthcare', 32.75, 32.40, true, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM app1_stock WHERE symbol = 'PFE');

INSERT INTO app1_stock (symbol, name, sector, current_price, previous_close, is_active, last_updated, created_at)
SELECT 'ABT', 'Abbott Laboratories', 'Healthcare', 115.45, 114.30, true, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM app1_stock WHERE symbol = 'ABT');

INSERT INTO app1_stock (symbol, name, sector, current_price, previous_close, is_active, last_updated, created_at)
SELECT 'TMO', 'Thermo Fisher Scientific', 'Healthcare', 520.30, 518.70, true, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM app1_stock WHERE symbol = 'TMO');

INSERT INTO app1_stock (symbol, name, sector, current_price, previous_close, is_active, last_updated, created_at)
SELECT 'MRK', 'Merck & Co.', 'Healthcare', 108.65, 107.80, true, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM app1_stock WHERE symbol = 'MRK');

INSERT INTO app1_stock (symbol, name, sector, current_price, previous_close, is_active, last_updated, created_at)
SELECT 'ABBV', 'AbbVie Inc.', 'Healthcare', 155.70, 154.50, true, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM app1_stock WHERE symbol = 'ABBV');

INSERT INTO app1_stock (symbol, name, sector, current_price, previous_close, is_active, last_updated, created_at)
SELECT 'LLY', 'Eli Lilly and Company', 'Healthcare', 585.25, 582.40, true, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM app1_stock WHERE symbol = 'LLY');

INSERT INTO app1_stock (symbol, name, sector, current_price, previous_close, is_active, last_updated, created_at)
SELECT 'BMY', 'Bristol-Myers Squibb', 'Healthcare', 58.90, 58.40, true, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM app1_stock WHERE symbol = 'BMY');

-- Financial Stocks
INSERT INTO app1_stock (symbol, name, sector, current_price, previous_close, is_active, last_updated, created_at)
SELECT 'JPM', 'JPMorgan Chase & Co.', 'Financial', 145.80, 144.50, true, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM app1_stock WHERE symbol = 'JPM');

INSERT INTO app1_stock (symbol, name, sector, current_price, previous_close, is_active, last_updated, created_at)
SELECT 'BAC', 'Bank of America Corp', 'Financial', 32.45, 32.10, true, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM app1_stock WHERE symbol = 'BAC');

INSERT INTO app1_stock (symbol, name, sector, current_price, previous_close, is_active, last_updated, created_at)
SELECT 'WFC', 'Wells Fargo & Company', 'Financial', 45.75, 45.30, true, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM app1_stock WHERE symbol = 'WFC');

INSERT INTO app1_stock (symbol, name, sector, current_price, previous_close, is_active, last_updated, created_at)
SELECT 'GS', 'Goldman Sachs Group', 'Financial', 365.20, 363.50, true, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM app1_stock WHERE symbol = 'GS');

INSERT INTO app1_stock (symbol, name, sector, current_price, previous_close, is_active, last_updated, created_at)
SELECT 'MS', 'Morgan Stanley', 'Financial', 88.90, 88.20, true, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM app1_stock WHERE symbol = 'MS');

-- Add more stocks as needed (showing pattern for remaining sectors)

-- Verification
SELECT 'Database setup complete!' as status;
SELECT COUNT(*) as event_count FROM app1_event;
SELECT COUNT(*) as settings_count FROM app1_simulatorsettings;
SELECT COUNT(*) as stock_count FROM app1_stock;
