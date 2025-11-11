#!/bin/bash
# Vercel Build Script - Runs migrations on production database

echo "🔨 Building TradeWars for Vercel..."
echo ""

# Install dependencies (already handled by Vercel)
echo "✅ Dependencies installed"

# Run migrations on production database
echo "📊 Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "✅ Build complete!"
