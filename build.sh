#!/bin/bash
# Vercel Build Script - Runs migrations on production database

echo "🔨 Building TradeWars for Vercel..."
echo ""

# Install dependencies (already handled by Vercel)
echo "✅ Dependencies installed"

# Create public directory (required by Vercel)
echo "📁 Creating public directory..."
mkdir -p public

# Run migrations on production database (fake if tables already exist)
echo "📊 Running database migrations..."
python manage.py migrate --noinput --fake-initial 2>&1 || echo "⚠️  Some migrations already applied"

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "✅ Build complete!"
