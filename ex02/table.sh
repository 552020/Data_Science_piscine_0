#!/bin/bash

# Script to create a PostgreSQL table from a CSV file
# Usage: ./table.sh <csv_filename>
# Example: ./table.sh data_2022_oct.csv

# Check if arguments were provided
# $# is a special bash variable that holds the number of arguments passed to the script
# If $# equals 0, no arguments were provided, so we show usage and exit
if [ $# -eq 0 ]; then
    # $0 is the script name itself (e.g., ./table.sh)
    echo "Usage: $0 <csv_filename>"
    echo "Example: $0 data_2022_oct.csv"
    echo "Note: CSV files are expected to be in data/customer/ directory"
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# $1 is the first argument passed to the script (the CSV filename)
CSV_FILE="$1"
# Get the project root directory (one level up from where the script is located)
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CSV_PATH="$PROJECT_ROOT/data/customer/$CSV_FILE"

# Extract table name (filename without extension)
# basename is a standard Unix command that extracts the filename from a path
# The second argument (.csv) removes that suffix from the result
# Example: basename "data_2022_oct.csv" .csv returns "data_2022_oct"
TABLE_NAME=$(basename "$CSV_FILE" .csv)

# Database connection details

# Load from .env file if it exists in the same directory as the script
# .env file should contain: DB_USER=your_login, DB_PASSWORD=your_password
ENV_FILE="$SCRIPT_DIR/.env"
if [ -f "$ENV_FILE" ]; then
    # Source the .env file to load environment variables
    # This reads variables from .env file (format: KEY=value)
    set -a  # Automatically export all variables
    source "$ENV_FILE"
    set +a  # Stop automatically exporting
fi

DB_NAME="piscineds"
DB_USER="${DB_USER:-slombard}"  # Use DB_USER from .env or env var or default to slombard
DB_HOST="localhost"

# Password must be provided - either from .env file or interactively
# No default password is set for security
if [ -z "$DB_PASSWORD" ]; then
    # Prompt for password interactively (input is hidden with -s flag)
    # -s flag makes read silent (doesn't echo input to screen)
    # -p flag specifies the prompt message
    read -s -p "Enter database password: " DB_PASSWORD
    echo  # Print a newline after password input
    
    if [ -z "$DB_PASSWORD" ]; then
        echo "Error: Password is required"
        exit 1
    fi
fi

# Set PGPASSWORD environment variable for psql to use
# psql will automatically use this environment variable for authentication
export PGPASSWORD="$DB_PASSWORD"

# Check if CSV file exists
if [ ! -f "$CSV_PATH" ]; then
    echo "Error: CSV file not found: $CSV_PATH"
    echo ""
    echo "The script can be run from any directory."
    echo "Expected CSV file location: $PROJECT_ROOT/data/customer/$CSV_FILE"
    echo "Make sure the CSV file exists in the data/customer/ directory relative to the project root."
    exit 1
fi

echo "Creating table: $TABLE_NAME"
echo "From CSV file: $CSV_PATH"

# Create table with proper schema
# Using 6 different data types: TIMESTAMPTZ, TEXT, INTEGER, NUMERIC, BIGINT, VARCHAR
psql -U "$DB_USER" -d "$DB_NAME" -h "$DB_HOST" <<EOF
CREATE TABLE IF NOT EXISTS $TABLE_NAME (
    event_time      TIMESTAMPTZ,
    event_type      TEXT,
    product_id      INTEGER,
    price           NUMERIC(10,2),
    user_id         BIGINT,
    user_session    VARCHAR(64)
);
EOF

if [ $? -ne 0 ]; then
    echo "Error: Failed to create table"
    exit 1
fi

echo "Table created successfully"
echo "Importing data from CSV..."

# Import data using \copy
psql -U "$DB_USER" -d "$DB_NAME" -h "$DB_HOST" <<EOF
\copy $TABLE_NAME FROM '$CSV_PATH' WITH (FORMAT csv, HEADER true, DELIMITER ',');
EOF

if [ $? -eq 0 ]; then
    echo "Data imported successfully!"
    echo "Table: $TABLE_NAME"
    echo "Rows imported: $(psql -U "$DB_USER" -d "$DB_NAME" -h "$DB_HOST" -t -c "SELECT COUNT(*) FROM $TABLE_NAME;")"
else
    echo "Error: Failed to import data"
    exit 1
fi

