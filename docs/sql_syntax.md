# SQL Syntax Reference

This document provides a reference for SQL syntax used in PostgreSQL, particularly for database and user management.

## SQL Commands Used So Far

1. **Create a new user:**
   ```sql
   CREATE USER your_login WITH PASSWORD 'mysecretpassword';
   ```

2. **Grant privileges on a database:**
   ```sql
   GRANT ALL PRIVILEGES ON DATABASE piscineds TO your_login;
   ```

## Keywords

### WITH

`WITH` is a versatile keyword in SQL that is used in various contexts to specify additional options, clauses, or to create Common Table Expressions (CTEs).

#### Common Uses of WITH:

1. **WITH PASSWORD** - Sets a password when creating or altering a user/role
   ```sql
   CREATE USER username WITH PASSWORD 'password';
   ALTER USER username WITH PASSWORD 'newpassword';
   ```

2. **WITH GRANT OPTION** - Allows a user to grant privileges to others
   ```sql
   GRANT SELECT ON table_name TO username WITH GRANT OPTION;
   ```

3. **WITH TIME ZONE** - Specifies timezone-aware timestamp data type
   ```sql
   CREATE TABLE example (
       created_at TIMESTAMP WITH TIME ZONE
   );
   ```

4. **WITH (Common Table Expressions)** - Creates temporary named result sets
   ```sql
   WITH temp_table AS (
       SELECT * FROM users WHERE age > 18
   )
   SELECT * FROM temp_table;
   ```

5. **WITH OPTIONS** - Used in various CREATE statements for additional configuration
   ```sql
   CREATE DATABASE dbname WITH ENCODING 'UTF8';
   ```

## User and Role Management

### CREATE USER / CREATE ROLE

In PostgreSQL, `CREATE USER` is an alias for `CREATE ROLE`. Both commands create a new database role (user).

**Syntax:**
```sql
CREATE USER username WITH PASSWORD 'password';
-- or
CREATE ROLE username WITH PASSWORD 'password' LOGIN;
```

**Key differences:**
- `CREATE USER` automatically includes `LOGIN` privilege
- `CREATE ROLE` does not include `LOGIN` by default (you must specify it)

**Common options with WITH:**
- `WITH PASSWORD 'password'` - Set the user's password
- `WITH CREATEDB` - Allow user to create databases
- `WITH CREATEROLE` - Allow user to create roles
- `WITH SUPERUSER` - Grant superuser privileges
- `WITH LOGIN` - Allow user to log in (default for CREATE USER)

**Example:**
```sql
CREATE USER myuser WITH 
    PASSWORD 'secret123'
    CREATEDB
    CREATEROLE;
```

## Database Management

### CREATE DATABASE

Creates a new database.

**Syntax:**
```sql
CREATE DATABASE database_name;
```

**With options:**
```sql
CREATE DATABASE database_name
    WITH 
    OWNER = username
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8';
```

## Privilege Management

### GRANT

Grants privileges on database objects to users/roles.

**Syntax:**
```sql
GRANT privilege_type ON object_name TO username;
```

**Common privilege types:**
- `SELECT` - Read data
- `INSERT` - Insert data
- `UPDATE` - Update data
- `DELETE` - Delete data
- `ALL PRIVILEGES` - All privileges

**Examples:**
```sql
-- Grant all privileges on a database
GRANT ALL PRIVILEGES ON DATABASE dbname TO username;

-- Grant SELECT on a table
GRANT SELECT ON TABLE table_name TO username;

-- Grant with grant option
GRANT SELECT ON TABLE table_name TO username WITH GRANT OPTION;
```

**Note:** For psql meta-commands (commands starting with `\`), see the `postgres.md` file in the docs folder.

## Data Types

### Common PostgreSQL Data Types

- `INTEGER` or `INT` - Whole numbers
- `BIGINT` - Large whole numbers
- `VARCHAR(n)` - Variable-length character string (max n characters)
- `TEXT` - Variable-length character string (unlimited)
- `BOOLEAN` - True/false values
- `DATE` - Date values
- `TIMESTAMP` - Date and time
- `TIMESTAMP WITH TIME ZONE` - Date and time with timezone
- `NUMERIC(p,s)` or `DECIMAL(p,s)` - Exact numeric with precision and scale
- `REAL` - Single precision floating-point
- `DOUBLE PRECISION` - Double precision floating-point

## Notes

- PostgreSQL is case-insensitive for keywords, but case-sensitive for identifiers (unless quoted)
- Use single quotes for string literals: `'text'`
- Use double quotes for identifiers: `"TableName"`
- Semicolon (`;`) is required to end SQL statements

