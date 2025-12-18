# Exercise 02: First table

## Requirements

- Create a PostgreSQL table using the data from a CSV file located in the `customer` folder
- The table must be named after the CSV file (without the file extension), e.g., `data_2022_oct`
- The column names must exactly match the ones in the CSV file
- The data types must be appropriate
- You must use **at least six different data types**
- A DATETIME column as the **first column** is mandatory

**Turn-in directory:** `ex02/`  
**Files to turn in:** `table.*` (any file starting with "table." - e.g., `table.sql`, `table.py`, `table.sh`, etc.)

**Be careful:** PostgreSQL data types are not exactly the same as those in MariaDB.

## Important: Schema Permissions

If you encounter a **"permission denied for schema public"** error when trying to create a table, you need to grant schema-level permissions to your user.

In Exercise 00, we granted database-level privileges, but PostgreSQL also requires schema-level permissions to create tables. To fix this:

1. Connect as the database owner (check with `\l+ piscineds` to see who owns it). If you installed PostgreSQL via Homebrew on macOS, the default user is your system username (e.g., `stefano`). To connect as the default user, simply omit the `-U` flag:
   ```bash
   psql -d piscineds -h localhost
   ```
   When prompted for a password, just press Enter (the default user has no password).

2. Grant schema permissions:
   ```sql
   GRANT USAGE ON SCHEMA public TO your_login;
   GRANT CREATE ON SCHEMA public TO your_login;
   ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO your_login;
   ```

Replace `your_login` with your actual student login.

**Alternative: Change Database Ownership**

Instead of granting schema permissions, you can change the database ownership, which automatically includes all necessary permissions:

1. Connect as the current database owner (check with `\l+ piscineds` to see who owns it). If you installed PostgreSQL via Homebrew on macOS, the default user is your system username (e.g., `stefano`). To connect as the default user, simply omit the `-U` flag:
   ```bash
   psql -d piscineds -h localhost
   ```
   When prompted for a password, just press Enter (the default user has no password).

2. Change ownership:
   ```sql
   ALTER DATABASE piscineds OWNER TO your_login;
   ```

3. **Disconnect and reconnect:** You must disconnect (`\q`) and reconnect to the database for the ownership change to take full effect:
   ```bash
   psql -U your_login -d piscineds -h localhost -W
   ```

4. Verify ownership change:
   ```sql
   \l+ piscineds
   ```
   You should see `your_login` as the owner in the "Owner" column.

For a detailed manual process, see `table.md` in this directory.

## Importing CSV Data into PostgreSQL

There are several ways to import CSV data into PostgreSQL. Here are the most common approaches:

### 1. SQL `COPY` or `\copy` Command (PostgreSQL Native)

**`COPY`** (server-side):
- Requires the CSV file to be accessible by the PostgreSQL server
- Fast and efficient for large files
- Requires superuser privileges or file system access

**`\copy`** (client-side):
- Works from your local machine
- More flexible for development
- No special privileges needed

**Example:**
```sql
-- First create the table structure
CREATE TABLE data_2022_oct (
    datetime_column TIMESTAMP,
    -- ... other columns
);

-- Then import data using \copy (client-side)
\copy data_2022_oct FROM 'data/customer/data_2022_oct.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
```

### 2. Python Scripts (Recommended for Data Science)

Python is commonly used in data science workflows for importing and processing data.

**Using `psycopg2` or `psycopg`:**
- Direct connection to PostgreSQL
- Execute SQL commands from Python
- Good for automation

**Using `pandas` + `sqlalchemy`:**
- Read CSV with pandas
- Infer data types automatically
- Write to database using sqlalchemy
- Very common in data science workflows

**Example structure:**
```python
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Read CSV
df = pd.read_csv('data/customer/data_2022_oct.csv')

# Create table and import data
engine = create_engine('postgresql://user:password@localhost/piscineds')
df.to_sql('data_2022_oct', engine, if_exists='replace', index=False)
```

### 3. GUI Tools (DBeaver, pgAdmin)

- Import wizards for one-off imports
- Good for quick manual imports
- Not ideal for automation or reproducible workflows

### 4. SQL Scripts

- Create table structure manually
- Use COPY or \copy to import data
- Good for documentation and reproducibility

## Recommendation

For this exercise and to prepare for Exercise 03 (which requires automation), **using a Python script** is recommended because:
- It's common in data science workflows
- Allows for data type inference and validation
- Easy to automate for multiple files (needed in Exercise 03)
- Can handle data cleaning and transformation if needed

However, SQL `\copy` is also a valid and straightforward approach if you prefer working directly with SQL.

## Important: PostgreSQL Does NOT Auto-Detect Column Types

**Short answer:** PostgreSQL **does not auto-detect column types** during CSV import. You must either:
1. Create the table with explicit types first, or
2. Import into a temporary staging table with all text columns and cast afterwards.

### Details

When you run:
```sql
COPY my_table FROM 'file.csv' CSV HEADER;
```

PostgreSQL simply **reads strings** and inserts them into the table **according to the types already defined in the table schema**. It does not attempt to guess types.

If the string cannot be cast to the column type, the row fails.

### Recommended Workflow

#### Option A — Create the correct table schema first (best practice)

You decide the types and then import:

```sql
CREATE TABLE events (
    event_time      TIMESTAMPTZ,
    event_type      TEXT,
    product_id      BIGINT,
    price           NUMERIC(10,2),
    user_id         BIGINT,
    user_session    UUID
);

\copy events FROM 'events.csv' CSV HEADER;
```

This is clean and fast.

#### Option B — Import everything as text, then cast

If you do not know yet what types to use, create a staging table:

```sql
CREATE TABLE raw_events (
    event_time    TEXT,
    event_type    TEXT,
    product_id    TEXT,
    price         TEXT,
    user_id       TEXT,
    user_session  TEXT
);

\copy raw_events FROM 'events.csv' CSV HEADER;
```

Then transform:

```sql
INSERT INTO events (event_time, event_type, product_id, price, user_id, user_session)
SELECT
    event_time::TIMESTAMPTZ,
    event_type,
    product_id::BIGINT,
    price::NUMERIC(10,2),
    user_id::BIGINT,
    user_session::UUID
FROM raw_events;
```

## Data Type Choices

For the typical dataset structure (event_time, event_type, product_id, price, user_id, user_session), here are the data type options:

| CSV Column   | Suggested PostgreSQL Type | Alternative Options | Reason |
| ------------ | ------------------------- | ------------------- | ------- |
| event_time   | `TIMESTAMPTZ`             | `TIMESTAMP`         | Timestamp with timezone; you have "UTC" |
| event_type   | `TEXT`                    | `VARCHAR(n)`        | String values; enum optional if you want constraints |
| product_id   | `BIGINT`                  | `INTEGER`           | Large integer (use BIGINT if IDs can be very large) |
| price        | `NUMERIC(10,2)`           | `DECIMAL(10,2)`, `REAL`, `DOUBLE PRECISION` | Monetary precision (NUMERIC/DECIMAL better than FLOAT for money) |
| user_id      | `BIGINT`                  | `INTEGER`           | Large integer (use BIGINT if IDs can be very large) |
| user_session | `UUID`                    | `VARCHAR(64)`, `TEXT` | Proper UUID format if it's a UUID, otherwise VARCHAR/TEXT for hash strings |

### To Meet the "6 Different Data Types" Requirement

You need at least 6 different PostgreSQL data types. Here's a combination that works:

1. `TIMESTAMPTZ` (or `TIMESTAMP`) - for datetime
2. `TEXT` - for event_type
3. `INTEGER` - for product_id
4. `NUMERIC(10,2)` - for price
5. `BIGINT` - for user_id (different from INTEGER)
6. `VARCHAR(64)` or `UUID` - for user_session (different from TEXT)

This gives you 6 distinct types: TIMESTAMPTZ, TEXT, INTEGER, NUMERIC, BIGINT, and VARCHAR/UUID.

### Type Selection Guidelines

- **Timestamps:** Use `TIMESTAMPTZ` if you have timezone info, `TIMESTAMP` if you don't
- **Strings:** Use `TEXT` for variable-length strings, `VARCHAR(n)` if you know max length
- **Integers:** Use `INTEGER` for values up to ~2 billion, `BIGINT` for larger values
- **Decimals:** Use `NUMERIC`/`DECIMAL` for money/precise values, `REAL`/`DOUBLE PRECISION` for approximate values
- **UUIDs/Hashes:** Use `UUID` if it's a proper UUID, `VARCHAR(n)` or `TEXT` for hash strings

