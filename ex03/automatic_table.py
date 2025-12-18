#!/usr/bin/env python3

import os
import glob
import psycopg2
from getpass import getpass
from dotenv import load_dotenv

# Get the directory where this script is located (not where it's run from)
# __file__ gives us the script's path, which works regardless of current working directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the project root directory (one level up from where the script is located)
# This ensures we find the customer directory regardless of where the script is executed from
project_root = os.path.dirname(script_dir)
# Path to the customer directory relative to project root
customer_dir = os.path.join(project_root, "customer")

# Find all CSV files in the directory
csv_files = glob.glob(os.path.join(customer_dir, "*.csv"))

if not csv_files:
    print(f"Error: No CSV files found in {customer_dir}")
    print(f"Make sure the customer directory exists and contains CSV files.")
    print(f"Expected location: {customer_dir}")
    exit(1)

print(f"Found {len(csv_files)} CSV file(s):")
for csv_file in csv_files:
    print(f"  - {os.path.basename(csv_file)}")

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

# Create tables for each CSV file
print(f"\nCreating tables...")
for csv_file in csv_files:
    # Extract table name from filename (remove .csv extension)
    table_name = os.path.splitext(os.path.basename(csv_file))[0]
    
    # Check if table already exists (for informative feedback)
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = %s
        );
    """, (table_name,))
    table_exists = cur.fetchone()[0]
    
    # Create table with the same schema as ex02
    # Using IF NOT EXISTS is best practice: atomic operation, standard SQL pattern
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        event_time      TIMESTAMPTZ,
        event_type      TEXT,
        product_id      INTEGER,
        price           NUMERIC(10,2),
        user_id         BIGINT,
        user_session    VARCHAR(64)
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

# Import data into tables
print(f"\nImporting data into tables...")
for csv_file in csv_files:
    # Extract table name from filename (remove .csv extension)
    table_name = os.path.splitext(os.path.basename(csv_file))[0]
    
    print(f"Importing data into table: {table_name}")
    
    try:
        # Use COPY FROM STDIN with CSV format (client-side, like \copy in psql)
        # This works with regular users (no superuser required)
        # copy_expert allows us to use the full COPY syntax
        with open(csv_file, 'r') as f:
            # Use copy_expert with COPY FROM STDIN syntax
            # This matches the \copy command we used in the bash script
            copy_sql = f"""
            COPY {table_name} (event_time, event_type, product_id, price, user_id, user_session)
            FROM STDIN
            WITH (FORMAT csv, HEADER true, DELIMITER ',')
            """
            cur.copy_expert(copy_sql, f)
        
        conn.commit()
        
        # Get row count for feedback
        cur.execute(f"SELECT COUNT(*) FROM {table_name};")
        row_count = cur.fetchone()[0]
        print(f"  ✓ Imported {row_count} rows into '{table_name}'")
        
    except psycopg2.Error as e:
        print(f"  ✗ Failed to import data into '{table_name}': {e}")
        conn.rollback()
    except IOError as e:
        print(f"  ✗ Failed to read CSV file '{csv_file}': {e}")
        conn.rollback()

# Close connection
cur.close()
conn.close()
print("\n✓ Connection closed successfully")

