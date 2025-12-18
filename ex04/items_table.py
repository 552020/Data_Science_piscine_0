#!/usr/bin/env python3

import os
import psycopg2
from getpass import getpass
from dotenv import load_dotenv

# Get the directory where this script is located (not where it's run from)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the project root directory (one level up from where the script is located)
project_root = os.path.dirname(script_dir)
# Path to the item directory relative to project root
item_dir = os.path.join(project_root, "item")
item_file = os.path.join(item_dir, "item.csv")

# Check if item.csv exists
if not os.path.exists(item_file):
    print(f"Error: item.csv not found in {item_dir}")
    print(f"Expected location: {item_file}")
    exit(1)

print(f"Found item.csv: {item_file}")

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
print(f"\nConnecting to database '{db_name}' as user '{db_user}'...")
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

# Table name must be "items" (as per Exercise 04 requirements)
table_name = "items"

# Check if table already exists (for informative feedback)
cur.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = %s
    );
""", (table_name,))
table_exists = cur.fetchone()[0]

# Create table
print(f"\nCreating table: {table_name}")

# Create table with appropriate data types
# Based on item.csv structure: product_id, category_id, category_code, brand
# Using at least 3 different data types: INTEGER, BIGINT, TEXT
create_table_sql = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    product_id      INTEGER,
    category_id     BIGINT,
    category_code   TEXT,
    brand           TEXT
);
"""

try:
    cur.execute(create_table_sql)
    conn.commit()
    
    # Provide feedback based on whether table existed before
    if table_exists:
        print(f"  ✓ Table '{table_name}' already exists, skipped")
    else:
        print(f"  ✓ Table '{table_name}' created successfully")
except psycopg2.Error as e:
    print(f"  ✗ Failed to create table '{table_name}': {e}")
    conn.rollback()
    cur.close()
    conn.close()
    exit(1)

# Import data
print(f"\nImporting data into table: {table_name}")

try:
    # Use COPY FROM STDIN with CSV format (client-side, like \copy in psql)
    with open(item_file, 'r') as f:
        # Use copy_expert with COPY FROM STDIN syntax
        copy_sql = f"""
        COPY {table_name} (product_id, category_id, category_code, brand)
        FROM STDIN
        WITH (FORMAT csv, HEADER true, DELIMITER ',')
        """
        cur.copy_expert(copy_sql, f)
    
    conn.commit()
    
    # Get row count for feedback
    cur.execute(f"SELECT COUNT(*) FROM {table_name};")
    row_count = cur.fetchone()[0]
    print(f"  ✓ Imported {row_count:,} rows into '{table_name}'")
    
except psycopg2.Error as e:
    print(f"  ✗ Failed to import data into '{table_name}': {e}")
    conn.rollback()
except IOError as e:
    print(f"  ✗ Failed to read CSV file '{item_file}': {e}")
    conn.rollback()

# Close connection
cur.close()
conn.close()
print("\n✓ Connection closed successfully")

