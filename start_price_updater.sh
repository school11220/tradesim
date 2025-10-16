#!/bin/bash

# Stock Price Auto-Updater Runner
# This script runs the stock price updater in the background

echo "🚀 Starting Stock Price Auto-Updater..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
fi

# Run the updater
echo "📊 Starting continuous price updates..."
echo "   Press Ctrl+C to stop"
echo ""

python manage.py update_stock_prices --continuous --interval 30

echo ""
echo "⏹️  Auto-updater stopped"
