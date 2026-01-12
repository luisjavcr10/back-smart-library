from app.core.config import settings
from sqlalchemy import create_engine, text

print(f"Original Env URL (approx): postgresql://...")
print(f"Settings URL: {settings.DATABASE_URL}")

try:
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("✅ Connection successful via Settings!")
except Exception as e:
    print(f"❌ Connection failed: {e}")
