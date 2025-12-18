# PostgreSQL

PostgreSQL is an open-source relational database management system (RDBMS).

It uses SQL (Structured Query Language) to manage and query data stored in tables.

**Note on metadata management:** SQL can query metadata (information about databases, users, tables, etc.) not because SQL inherently has meta-management capabilities, but because PostgreSQL stores this metadata in system catalog tables (like `pg_database`, `pg_roles`, `pg_tables`, etc.). Since SQL can query any table, you can query these system catalog tables to get information about the database system itself. The psql meta-commands are shortcuts that run SQL queries against these system catalogs.

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

4. **Exit psql:**
   ```sql
   \q
   ```
   **SQL equivalent:** None. This is a psql-specific command to exit the client.

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

