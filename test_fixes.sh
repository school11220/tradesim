#!/bin/bash
# Test all fixes

echo "🧪 Testing TradeWars Fixes"
echo "=========================="
echo ""

# Test 1: Root redirect
echo "1️⃣ Testing root redirect..."
root_status=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/)
if [ "$root_status" = "302" ]; then
    echo "✅ Root redirects correctly (302)"
else
    echo "❌ Root redirect failed (got $root_status)"
fi
echo ""

# Test 2: Individual user routes redirect
echo "2️⃣ Testing individual user route redirects..."
for route in "login" "signup" "dashboard" "portfolio"; do
    status=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/$route)
    if [ "$status" = "302" ]; then
        echo "✅ /$route redirects to team system"
    else
        echo "❌ /$route failed (got $status)"
    fi
done
echo ""

# Test 3: Team login loads
echo "3️⃣ Testing team login page..."
team_login=$(curl -s http://127.0.0.1:8000/team/login | grep -o "TradeWars" | head -1)
if [ "$team_login" = "TradeWars" ]; then
    echo "✅ Team login page loads"
else
    echo "❌ Team login page issue"
fi
echo ""

# Test 4: Check server logs for news page
echo "4️⃣ Checking recent news page requests..."
tail -20 server.log | grep "team/news" | tail -3
echo ""

echo "=========================="
echo "✅ Testing Complete!"
