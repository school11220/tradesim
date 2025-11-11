#!/bin/bash
# Quick verification script for production deployment

echo "🔍 Verifying TradeWars Production Deployment"
echo "============================================"
echo ""

echo "1️⃣ Checking root redirect..."
root_code=$(curl -s -o /dev/null -w "%{http_code}" https://tradesim-lyart.vercel.app/)
if [ "$root_code" = "302" ]; then
    echo "✅ Root redirects to team login"
else
    echo "⚠️  Root returned: $root_code"
fi
echo ""

echo "2️⃣ Checking admin panel accessibility..."
admin_code=$(curl -s -o /dev/null -w "%{http_code}" https://tradesim-lyart.vercel.app/admin/)
if [ "$admin_code" = "302" ]; then
    echo "✅ Admin panel accessible (redirects to login)"
elif [ "$admin_code" = "200" ]; then
    echo "✅ Admin panel accessible"
else
    echo "❌ Admin panel error: $admin_code"
fi
echo ""

echo "3️⃣ Checking MarketNews admin..."
news_admin_code=$(curl -s -o /dev/null -w "%{http_code}" https://tradesim-lyart.vercel.app/admin/app1/marketnews/)
if [ "$news_admin_code" = "302" ]; then
    echo "✅ MarketNews admin accessible (redirects to login)"
elif [ "$news_admin_code" = "200" ]; then
    echo "✅ MarketNews admin accessible"
elif [ "$news_admin_code" = "500" ]; then
    echo "❌ MarketNews admin error 500 - Database migration may not have run"
    echo "   Wait 2 minutes for Vercel build to complete, then try again"
else
    echo "⚠️  MarketNews admin returned: $news_admin_code"
fi
echo ""

echo "4️⃣ Checking price update API..."
api_response=$(curl -s https://tradesim-lyart.vercel.app/api/update-prices-real)
updated_count=$(echo "$api_response" | grep -o '"updated_count":[0-9]*' | cut -d':' -f2)
if [ ! -z "$updated_count" ] && [ "$updated_count" -gt "50" ]; then
    echo "✅ Price updates working (${updated_count} stocks updated)"
elif [ ! -z "$updated_count" ]; then
    echo "⚠️  Price updates partial (${updated_count} stocks updated)"
else
    echo "⚠️  Could not verify price updates"
fi
echo ""

echo "5️⃣ Checking team login page..."
team_login=$(curl -s https://tradesim-lyart.vercel.app/team/login | grep -o "TradeWars" | head -1)
if [ "$team_login" = "TradeWars" ]; then
    echo "✅ Team login page loads"
else
    echo "❌ Team login page issue"
fi
echo ""

echo "============================================"
echo "✅ Verification Complete!"
echo ""
echo "📝 Next Steps:"
echo "   1. Login to admin: https://tradesim-lyart.vercel.app/admin"
echo "   2. Go to Market News and create test news items"
echo "   3. Login as team and visit /team/news to verify"
echo ""
echo "🎯 If MarketNews admin shows 500 error:"
echo "   - Wait 2 minutes for Vercel build to finish"
echo "   - Check build logs: https://vercel.com/YOUR_USERNAME/tradesim"
echo "   - Run this script again"
