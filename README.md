# Piscine datascience - 0
## Creation of a DB

This project focuses on learning database creation and management using PostgreSQL. You will set up a PostgreSQL database and learn to create tables from CSV files.

## Project Structure

- `ex00/` - Create Postgres DB
- `ex01/` - Show me your DB
- `ex02/` - First table
- `ex03/` - Automatic table
- `ex04/` - Items table

## Exercise 00: Create Postgres DB

For this exercise, you can use PostgreSQL directly if it is installed on your campus machine or on a VM. Otherwise, you must use Docker Compose.

### Requirements

- The username must be your student login
- The name of the database must be `piscineds`
- The password must be `mysecretpassword`

We must be able to connect to your PostgreSQL database with the following command:

```bash
psql -U your_login -d piscineds -h localhost -W
```

### Database Creation

To create a PostgreSQL database, you need to first connect to the PostgreSQL server. PostgreSQL requires you to be connected to a database to run SQL commands - you can't run commands without a database connection. PostgreSQL comes with a default database called `postgres` that always exists and serves as the entry point for administrative tasks. You connect to `postgres` first, then run commands to create your new database.

#### Steps

1. **Connect to the default `postgres` database:**
   ```bash
   psql -d postgres
   ```

2. **Create a new user with your student login as the username:**
   ```sql
   CREATE USER your_login WITH PASSWORD 'mysecretpassword';
   ```
   Replace `your_login` with your actual student login.
   
   **Note:** You will see `CREATE ROLE` as the response. This is correct - in PostgreSQL, `CREATE USER` is an alias for `CREATE ROLE`. PostgreSQL uses "roles" for both users and groups, and when you create a user, it creates a role with login privileges.
   
   **About `WITH PASSWORD`:** `WITH` is a keyword in SQL that is used to specify additional options or clauses. In this context, `WITH PASSWORD` sets the password for the user. `WITH` can be combined with other keywords in different SQL contexts (e.g., `WITH GRANT OPTION`, `WITH TIME ZONE`, etc.). See the `docs/` folder for more SQL syntax documentation.

3. **Verify the user has been created:**
   ```sql
   \du
   ```
   This command lists all users. You should see your user in the list.

4. **Create the `piscineds` database:**
   ```sql
   CREATE DATABASE piscineds;
   ```

5. **Verify the database has been created:**
   ```sql
   \l
   ```
   This command lists all databases. You should see `piscineds` in the list.
   
   **Note on results:** When you run `\l`, you will see several databases:
   - `piscineds` - Your newly created database (owned by your user)
   - `postgres` - The default administrative database
   - `template0` and `template1` - Template databases used by PostgreSQL when creating new databases (these are system databases)
   
   The presence of `piscineds` in the list confirms it was created successfully.

6. **Grant the user appropriate permissions on the database:**
   ```sql
   GRANT ALL PRIVILEGES ON DATABASE piscineds TO your_login;
   ```
   Replace `your_login` with your actual student login.

7. **Verify the permissions have been granted:**
   ```sql
   \l+
   ```
   This shows detailed information about databases including owners and permissions. You can also verify by attempting to connect in the next step.

8. **Exit the `postgres` database connection:**
   ```sql
   \q
   ```

9. **Verify you can connect to your new database:**
   ```bash
   psql -U your_login -d piscineds -h localhost -W
   ```
   Enter the password `mysecretpassword` when prompted. You should see the `piscineds=#` prompt.

The database must be accessible via `psql` using the connection command specified in the requirements.

### What is psql?

`psql` is the command-line interface (CLI) tool for PostgreSQL. It's an interactive terminal-based front-end to PostgreSQL that allows you to:

- Connect to PostgreSQL databases
- Execute SQL queries and commands
- Manage database objects (tables, users, schemas, etc.)
- View and manipulate data
- Run scripts and batch operations

#### Basic Usage

When you run `psql` without arguments, it attempts to connect to a database with the same name as your system username. If that database doesn't exist, you'll get an error.

To connect to a specific database:
```bash
psql -d database_name
```

To connect with a specific user:
```bash
psql -U username -d database_name
```

To connect to a remote host:
```bash
psql -h hostname -U username -d database_name
```

#### Common Options

- `-U` or `--username`: Specify the database user
- `-d` or `--dbname`: Specify the database name
- `-h` or `--host`: Specify the host (default is localhost)
- `-p` or `--port`: Specify the port (default is 5432)
- `-W` or `--password`: Prompt for password
- `-c`: Execute a single command and exit
- `-f`: Execute commands from a file

#### Example

```bash
psql -U your_login -d piscineds -h localhost -W
```

This connects to the `piscineds` database on localhost using `your_login` as the username, and prompts for a password.

If you choose to use Docker, your setup must follow the same standards and good practices as required in the Inception project.
# Data_Science_piscine_0
