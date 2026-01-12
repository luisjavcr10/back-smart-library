import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL")
print(f"Testing direct psycopg connection to: {database_url}")

try:
    # Try connecting directly with psycopg, enforcing SSL
    # remove +psycopg if present
    clean_url = database_url.replace("+psycopg", "")
    with psycopg.connect(clean_url, sslmode="require") as conn:
        print("✅ Connection successful!")
        with conn.cursor() as cur:
            cur.execute("SELECT version()")
            print(f"Server version: {cur.fetchone()}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
