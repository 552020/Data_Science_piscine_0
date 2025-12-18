#!/usr/bin/env python3

import os
import psycopg2
from getpass import getpass
from dotenv import load_dotenv

# Get the directory where this script is located (not where it's run from)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Database connection parameters
# Load from .env file if it exists (in the same directory as the script)
env_file = os.path.join(script_dir, ".env")
load_dotenv(env_file)  # This loads variables from .env into os.environ

db_user = os.environ.get("DB_USER", "slombard")
db_password = os.environ.get("DB_PASSWORD")

# If password is still not set, prompt for it
if not db_password:
    db_password = getpass("Enter database password: ")

# Database connection details
db_name = "piscineds"
db_host = "localhost"
db_port = 5432

# Connect to database
print(f"Connecting to database '{db_name}' as user '{db_user}'...")
try:
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    print("✓ Connection successful!")
    cur = conn.cursor()
    
except psycopg2.Error as e:
    print(f"✗ Connection failed: {e}")
    exit(1)

# Test items table
table_name = "items"
print(f"\nTesting table: {table_name}")
print("=" * 80)

# Check if table exists
cur.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = %s
    );
""", (table_name,))
table_exists = cur.fetchone()[0]

if not table_exists:
    print(f"  ✗ Table '{table_name}' does NOT exist")
    cur.close()
    conn.close()
    exit(1)

print(f"  ✓ Table '{table_name}' exists")

# Get row count
try:
    cur.execute(f"SELECT COUNT(*) FROM {table_name};")
    row_count = cur.fetchone()[0]
    print(f"  ✓ Row count: {row_count:,}")
except psycopg2.Error as e:
    print(f"  ✗ Failed to count rows: {e}")
    cur.close()
    conn.close()
    exit(1)

# Get first 10 rows
try:
    cur.execute(f"SELECT * FROM {table_name} LIMIT 10;")
    rows = cur.fetchall()
    
    if rows:
        # Get column names
        colnames = [desc[0] for desc in cur.description]
        print(f"\n  First 10 rows:")
        print(f"  {' | '.join(colnames)}")
        print(f"  {'-' * 80}")
        
        for row in rows:
            # Format each row for display
            formatted_row = []
            for value in row:
                if value is None:
                    formatted_row.append("NULL")
                elif isinstance(value, str) and len(value) > 30:
                    formatted_row.append(value[:27] + "...")
                else:
                    formatted_row.append(str(value))
            print(f"  {' | '.join(formatted_row)}")
    else:
        print(f"  ⚠ Table is empty (no rows)")
        
except psycopg2.Error as e:
    print(f"  ✗ Failed to fetch rows: {e}")

print("\n" + "=" * 80)

# Close connection
cur.close()
conn.close()
print("\n✓ Connection closed successfully")

