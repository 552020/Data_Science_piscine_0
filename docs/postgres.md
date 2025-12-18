# PostgreSQL

PostgreSQL is an open-source relational database management system (RDBMS).

It uses SQL (Structured Query Language) to manage and query data stored in tables.

## psql Commands Used So Far

1. **Connect to the default postgres database:**
   ```bash
   psql -d postgres
   ```

2. **List all users/roles:**
   ```sql
   \du
   ```
   **SQL equivalent:** `SELECT * FROM pg_roles;` or `SELECT * FROM pg_user;`

3. **List all databases:**
   ```sql
   \l
   ```
   **SQL equivalent:** `SELECT * FROM pg_database;`

4. **List all schemas:**
   ```sql
   \dn
   ```
   **SQL equivalent:** `SELECT * FROM pg_namespace;`

**Note:** Commands starting with `\` are psql meta-commands (backslash commands), not SQL. They are specific to the psql client tool.

## Useful psql Commands

### List Users/Roles
```sql
\du
```
**SQL equivalent:**
```sql
SELECT * FROM pg_roles;
```
or
```sql
SELECT * FROM pg_user;
```

### List Databases
```sql
\l
```
**SQL equivalent:**
```sql
SELECT * FROM pg_database;
```

### List Databases with Details
```sql
\l+
```
**SQL equivalent:** Same as `\l` but with additional details. You can query `pg_database` with more columns for detailed information.

### List Schemas
```sql
\dn
```
**SQL equivalent:**
```sql
SELECT * FROM pg_namespace;
```

### List Tables
```sql
\dt
```
**SQL equivalent:**
```sql
SELECT * FROM information_schema.tables WHERE table_schema = 'public';
```
or
```sql
SELECT * FROM pg_tables WHERE schemaname = 'public';
```

### Describe Table Structure
```sql
\d table_name
```
**SQL equivalent:**
```sql
SELECT * FROM information_schema.columns WHERE table_name = 'table_name';
```

### Exit psql
```sql
\q
```
**SQL equivalent:** None. This is a psql-specific command to exit the client.

### Import Data from CSV (\copy)

```sql
\copy table_name FROM 'file_path.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
```

**Note on `\copy` vs `COPY`:**

`\copy` is a psql meta-command (backslash command), not standard SQL. It's the client-side version of PostgreSQL's `COPY` command.

**SQL `COPY` (server-side):**
- Standard PostgreSQL SQL command
- File must be accessible by the PostgreSQL server
- Requires superuser privileges or file system access
- Syntax: `COPY table_name FROM 'file_path' WITH (FORMAT csv, HEADER true);`

**psql `\copy` (client-side):**
- psql meta-command (not SQL)
- File can be on your local machine
- psql reads the file and sends data to the server
- No special privileges needed
- Syntax: `\copy table_name FROM 'file_path' WITH (FORMAT csv, HEADER true);`

**Is there a standard SQL equivalent?**
No. `COPY` is PostgreSQL-specific. Other databases have similar commands (e.g., MySQL's `LOAD DATA INFILE`, SQL Server's `BULK INSERT`), but they're not standard SQL.

So `\copy` is a PostgreSQL/psql utility that makes it easier to import files from your local machine without needing server-side file access.

