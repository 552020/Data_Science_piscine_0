# Exercise 04: Items table

## Requirements

- Create a table named `items` using the column names provided in the `item.csv` file
- The table must contain at least **three different data types**
- The CSV file is located in the `item/` folder at the root of the repository

**Turn-in directory:** `ex04/`  
**Files to turn in:** `items_table.*` (any file starting with "items_table." - e.g., `items_table.py`, `items_table.sh`, etc.)

## Approach

We're using a Python script (`items_table.py`) to create the table and import the data. This approach is:
- Consistent with Exercise 03
- Reusable code structure
- Easy to maintain and extend
- Common in data science workflows

The script will:
1. Find `item.csv` in the `item/` directory (at the root of the repository)
2. Create a table named `items` with appropriate data types
3. Import the data into the table

## Table Structure

The `item.csv` file contains the following columns:
- `product_id`: INTEGER
- `category_id`: BIGINT
- `category_code`: TEXT
- `brand`: TEXT

**Data types used:** INTEGER, BIGINT, TEXT (3 different data types, meeting the requirement)

## Setup

### Virtual Environment

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

This will install all required packages:
- `psycopg2-binary` - PostgreSQL adapter for Python
- `python-dotenv` - For loading `.env` file

### Environment Variables (.env file)

The script reads database credentials from a `.env` file located in the same directory as the script (`ex04/.env`). Create this file with the following format:

```bash
DB_USER=your_login
DB_PASSWORD=your_password
```

**Note:** The `.env` file should be added to `.gitignore` (it's already included in the project's `.gitignore`) to avoid committing sensitive credentials.

If the `.env` file doesn't exist or `DB_PASSWORD` is not set, the script will prompt you to enter the password interactively.

## Usage

**Run the script:**
```bash
python3 items_table.py
```

The script will:
1. Connect to the PostgreSQL database (`piscineds`)
2. Create the `items` table if it doesn't exist
3. Import data from `item/item.csv`
4. Display the number of rows imported

**Database connection:**
- The script reads database credentials from `.env` file (in `ex04/` directory) or prompts for password
- Default user: `slombard` (or set `DB_USER` in `.env`)
- Database: `piscineds`
- Host: `localhost`
- Port: `5432`

## Implementation Details

### Table Creation: `CREATE TABLE IF NOT EXISTS`

The script uses `CREATE TABLE IF NOT EXISTS` when creating the table. This is considered best practice because:
- **Atomic operation**: No race condition between checking if a table exists and creating it
- **Standard SQL pattern**: Widely used and recognized in database automation scripts
- **Idempotent**: The script can be run multiple times safely without errors
- **Simpler code**: No need for complex error handling for "table already exists" cases

The script checks if a table exists before creation (for informative feedback only), but relies on `IF NOT EXISTS` for the actual creation to ensure atomicity and follow best practices.

### Data Import

The script uses PostgreSQL's `COPY FROM STDIN` command (via `copy_expert()` in psycopg2) to import data:
- **Client-side operation**: Works with regular database users (no superuser required)
- **CSV format**: Handles headers and proper delimiter
- **Efficient**: Fast bulk import of data

