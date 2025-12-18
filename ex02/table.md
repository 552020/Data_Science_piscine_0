# Manual Table Creation Process

This document describes the safest way to manually create a PostgreSQL table from a CSV file. This process gives you full control and helps you understand each step.

## Prerequisites

1. Ensure you have schema permissions (see Schema Permissions section below)
2. Have the CSV file ready in `data/customer/` directory
3. Know your database connection details

## Step-by-Step Process

### Step 1: Connect to the Database

Connect to your `piscineds` database:

```bash
psql -U your_login -d piscineds -h localhost -W
```

Enter your password when prompted.

### Step 2: Check Database Ownership

Check who owns the database - you'll need this information if you need to grant schema permissions:

```sql
\l piscineds
```

This will show you the database owner in the "Owner" column. Note the owner's name - if you need to grant schema permissions, you'll need to connect as this user (or as a superuser like `postgres`).

### Step 3: Check Schema Permissions

First, verify you can see the schemas:

```sql
\dn
```

You should see the `public` schema listed. If you get a "permission denied" error here or when creating tables, you need to grant schema permissions (see Schema Permissions section below).

**Important:** If you haven't granted schema permissions yet, you'll get a "permission denied for schema public" error when trying to create a table. Make sure to grant schema permissions first (see Schema Permissions section) before proceeding to create tables.

### Step 4: Create the Table Structure

Create the table with appropriate data types. For the typical CSV structure (event_time, event_type, product_id, price, user_id, user_session):

```sql
CREATE TABLE data_2022_oct (
    event_time      TIMESTAMPTZ,
    event_type      TEXT,
    product_id      INTEGER,
    price           NUMERIC(10,2),
    user_id         BIGINT,
    user_session    VARCHAR(64)
);
```

**Important:**
- Replace `data_2022_oct` with your actual table name (matching the CSV filename without extension)
- Ensure the first column is a DATETIME type (TIMESTAMPTZ or TIMESTAMP)
- Use at least 6 different data types
- Column names must exactly match the CSV header

### Step 5: Verify Table Creation

After creating the table, verify it was created successfully:

**Check that the table exists:**
```sql
\dt
```

Expected output:
```
             List of relations
 Schema |     Name      | Type  |  Owner   
--------+---------------+-------+----------
 public | data_2022_oct | table | slombard
(1 row)
```

You should see your table in the list with your user as the owner.

**Verify the table structure:**
```sql
\d data_2022_oct
```

Expected output:
```
                       Table "public.data_2022_oct"
    Column    |           Type           | Collation | Nullable | Default 
--------------+--------------------------+-----------+----------+---------
 event_time   | timestamp with time zone |           |          | 
 event_type   | text                     |           |          | 
 product_id   | integer                  |           |          | 
 price        | numeric(10,2)            |           |          | 
 user_id      | bigint                   |           |          | 
 user_session | character varying(64)    |           |          | 
```

This shows the table structure with all columns and their data types. Verify that:
- All columns are present
- Data types are correct
- The first column is a DATETIME type (TIMESTAMPTZ or TIMESTAMP)
- You have at least 6 different data types (TIMESTAMPTZ, TEXT, INTEGER, NUMERIC, BIGINT, VARCHAR)

**Check table is empty (before import):**
```sql
SELECT COUNT(*) FROM data_2022_oct;
```

Expected output:
```
 count 
-------
     0
(1 row)
```

This should return `0` since no data has been imported yet.

### Step 6: Import Data from CSV

Use the `\copy` command to import data. Make sure you're in the project root directory or adjust the path accordingly:

```sql
\copy data_2022_oct FROM '/full/path/to/data/customer/data_2022_oct.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
```

**Note:** Use the full absolute path to the CSV file, or run psql from the project root directory so you can use a relative path like `data/customer/data_2022_oct.csv`.

**Expected output:**
```
COPY 4102283
```

The number after `COPY` indicates how many rows were successfully imported. The exact number will vary depending on your CSV file. This confirms the import was successful.

### Step 7: Verify Data Import

Check the number of rows imported:

```sql
SELECT COUNT(*) FROM data_2022_oct;
```

View a few sample rows:

```sql
SELECT * FROM data_2022_oct LIMIT 5;
```

### Step 8: Exit psql

```sql
\q
```

## Schema Permissions

If you encounter a "permission denied for schema public" error, you need to grant schema permissions.

**Note:** In Exercise 00, we granted database-level privileges (`GRANT ALL PRIVILEGES ON DATABASE piscineds TO your_login`), but PostgreSQL also requires **schema-level privileges** to create tables. That's why you're getting this error even though database privileges were granted.

### Step 1: Find the Database Owner

Check who owns the database. You can do this in two ways:

**Option A: From within psql** (connect first, then run):
```bash
psql -U your_login -d piscineds -h localhost
```
Then inside psql:
```sql
\l piscineds
```

**Option B: One-liner from command line:**
```bash
psql -U your_login -d piscineds -h localhost -c "\l piscineds"
```

Both methods will show you the database owner in the "Owner" column.

### Step 2: Connect as the Database Owner or Superuser

Connect as the database owner (from Step 1) or as a superuser (usually `postgres`):

```bash
psql -U database_owner -d piscineds -h localhost
```

Or if you need to use the postgres superuser:

```bash
psql -U postgres -d piscineds -h localhost
```

### Step 3: Grant Schema Permissions

Once connected as the database owner or superuser, grant the necessary permissions:

```sql
-- Grant usage on the public schema
GRANT USAGE ON SCHEMA public TO your_login;

-- Grant create privileges on the public schema
GRANT CREATE ON SCHEMA public TO your_login;

-- Also ensure the user owns the database or has proper privileges
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO your_login;
```

Replace `your_login` with your actual student login.

### Step 4: Verify Permissions

After granting permissions, disconnect and reconnect as your user, then verify you can create tables:

```sql
-- Test creating a temporary table
CREATE TABLE test_permissions (id INTEGER);
DROP TABLE test_permissions;
```

If this works without errors, your permissions are set correctly.

## Troubleshooting

### Error: "permission denied for schema public"
- See Schema Permissions section above
- Make sure you've granted USAGE and CREATE on the schema

### Error: "relation does not exist"
- The table wasn't created successfully
- Check the CREATE TABLE command for syntax errors
- Verify you have schema permissions

### Error: "could not open file"
- Use the full absolute path to the CSV file
- Make sure the file exists and is readable
- Check file permissions

### Error: "invalid input syntax"
- Data type mismatch between CSV data and table schema
- Check that your data types match the actual data in the CSV
- Verify the CSV format (delimiters, headers, etc.)

## Advantages of Manual Process

1. **Full Control** - You see exactly what's happening at each step
2. **Learning** - Better understanding of PostgreSQL commands
3. **Debugging** - Easier to identify and fix issues
4. **Safety** - You can verify each step before proceeding
5. **Flexibility** - Easy to adjust data types or table structure

