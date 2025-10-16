"""
Simple production initialization script
Run this in your production environment (Vercel, Railway, etc.)
"""
import os
import sys

# This script should be run from the project root
# python init_production.py

def init_production():
    """Initialize production database with stocks and event"""
    print("=" * 60)
    print("🚀 PRODUCTION DATABASE INITIALIZATION")
    print("=" * 60)
    
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demostocks.settings')
    import django
    django.setup()
    
    from app1.management.commands.init_trading_platform import Command
    
    print("\n📊 Running init_trading_platform command...")
    command = Command()
    command.handle()
    
    print("\n" + "=" * 60)
    print("✅ PRODUCTION INITIALIZATION COMPLETE!")
    print("=" * 60)
    print("\n🎯 Next Steps:")
    print("1. Go to your site's /admin panel")
    print("2. Create teams at /team/signup")
    print("3. Start trading at /team/stocks")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    try:
        init_production()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
