#!/bin/bash
# Vercel build hook to clear Python cache before deployment

echo "🧹 Cleaning Python cache..."

# Remove all __pycache__ directories
find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true

# Remove all .pyc files
find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Remove all .pyo files
find . -type f -name "*.pyo" -delete 2>/dev/null || true

echo "✅ Python cache cleared!"
