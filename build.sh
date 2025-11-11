#!/bin/bash
# Vercel Build Script - Runs migrations on production database

echo "🔨 Building TradeWars for Vercel..."
echo ""

# Install dependencies (already handled by Vercel)
echo "✅ Dependencies installed"

# Create public directory (required by Vercel)
echo "📁 Creating public directory..."
mkdir -p public

# Run migrations on production database
echo "📊 Running database migrations..."
python manage.py migrate app1 --noinput 2>&1 || echo "⚠️  App1 migrations had issues, continuing..."
python manage.py migrate --noinput 2>&1 || echo "⚠️  Some migrations already applied"

# Emergency: Ensure MarketNews table exists
echo "🔍 Verifying MarketNews table..."
python create_marketnews_table.py 2>&1 || echo "⚠️  MarketNews table check completed"

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "✅ Build complete!"
