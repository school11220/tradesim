#!/bin/bash

# Quick Demo: Watch stock prices change in real-time
# This updates prices every 5 seconds with higher volatility for dramatic effect

echo "╔══════════════════════════════════════════════════════════╗"
echo "║   🎬 STOCK PRICE DEMO - Real Market Simulation          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "This demo will update stock prices every 5 seconds"
echo "with ±3% volatility for dramatic effect."
echo ""
echo "Open your browser to http://127.0.0.1:8000/team/stocks"
echo "and watch the prices change live!"
echo ""
echo "Press Ctrl+C to stop"
echo ""
sleep 3

# Activate venv if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run with demo settings
python manage.py update_stock_prices --continuous --interval 5 --volatility 0.03
