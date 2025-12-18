# Exercise 03: Automatic table

## Requirements

- Automatically retrieve all CSV files from the `customer/` folder (at the root of the repository)
- Create a table for each CSV file
- Each table must be named after the corresponding CSV file (without its extension), e.g., `data_2022_oct` from `data_2022_oct.csv`

**Turn-in directory:** `ex03/`  
**Files to turn in:** `automatic_table.*` (any file starting with "automatic_table." - e.g., `automatic_table.py`, `automatic_table.sh`, etc.)

## Approach

We're using a Python script (`automatic_table.py`) to automate the table creation process. This approach is:
- More readable than complex bash loops
- Better suited for data operations
- Common in data science workflows
- Easier to maintain and extend

The script will:
1. Find all CSV files in `customer/` (at the root of the repository)
2. For each CSV file, create a table with the same name (without .csv extension)
3. Import the data into that table

This automates the manual process from Exercise 02.

## Implementation Details

### Table Creation: `CREATE TABLE IF NOT EXISTS`

The script uses `CREATE TABLE IF NOT EXISTS` when creating tables. This is considered best practice because:

- **Atomic operation**: No race condition between checking if a table exists and creating it
- **Standard SQL pattern**: Widely used and recognized in database automation scripts
- **Idempotent**: The script can be run multiple times safely without errors
- **Simpler code**: No need for complex error handling for "table already exists" cases

The script checks if a table exists before creation (for informative feedback only), but relies on `IF NOT EXISTS` for the actual creation to ensure atomicity and follow best practices.

## Setup: Virtual Environment

Before installing Python dependencies, it's recommended to create a virtual environment to isolate project dependencies:

**Create a virtual environment:**
```bash
python3 -m venv venv
```

**Activate the virtual environment:**
- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```
- On Windows:
  ```bash
  venv\Scripts\activate
  ```

**Deactivate the virtual environment (when done):**
```bash
deactivate
```

**Note:** The virtual environment should be activated before installing packages and running the script. The `venv/` directory should be added to `.gitignore` (it's already included in the project's `.gitignore`).

**Install dependencies from requirements.txt:**
```bash
pip install -r requirements.txt
```

This will install all required packages (currently `psycopg2-binary`) listed in the `requirements.txt` file.

## Python Libraries for PostgreSQL Connection

There are several options for connecting to PostgreSQL from Python:

### 1. psycopg2 / psycopg (Recommended)

**psycopg2** (or **psycopg** for version 3) is the PostgreSQL adapter for Python:
- Direct connection to PostgreSQL
- Execute SQL commands directly
- Can use PostgreSQL's `COPY` command for fast imports
- Good performance and control
- Well-suited for this automation task

**Installation (with virtual environment activated):**
```bash
pip install psycopg2-binary
```
or
```bash
pip install psycopg
```

### 2. sqlalchemy

**sqlalchemy** is a SQL toolkit and ORM:
- Works with PostgreSQL and other databases
- More abstraction layer
- Less direct control over SQL execution
- Good for complex applications

**Installation (with virtual environment activated):**
```bash
pip install sqlalchemy
```

### 3. pandas + sqlalchemy

**pandas** with **sqlalchemy** is common in data science:
- Read CSV files with pandas
- Write to database using sqlalchemy
- More convenient for data manipulation
- More overhead but easier data processing

**Installation (with virtual environment activated):**
```bash
pip install pandas sqlalchemy psycopg2-binary
```

**Recommendation:** For this exercise, **psycopg2** or **psycopg** is recommended because it provides direct SQL execution and can use PostgreSQL's `COPY` command for fast data imports, matching the manual process from Exercise 02.

