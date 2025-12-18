# Exercise 01: Show me your DB

## Requirements

- Find a way to easily visualize your database using a software tool
- The chosen software should allow you to browse and manipulate data easily, especially using record IDs

**Allowed functions:** pgAdmin, Postico, DBeaver or any other tool of your choice

## Tool Choice: DBeaver

We chose **DBeaver** as the database visualization tool for the following reasons:

1. **Free and Open Source** - No cost or licensing concerns
2. **Cross-platform** - Works on macOS, Linux, and Windows
3. **Comprehensive PostgreSQL Support** - Full feature set for PostgreSQL databases
4. **Easy Data Browsing** - Intuitive interface for viewing tables, records, and navigating by IDs
5. **Data Manipulation** - Allows easy editing and querying of data directly through the GUI
6. **Widely Used** - Popular tool in the data engineering community
7. **Easy Installation** - Can be installed via Homebrew on macOS

DBeaver provides all the functionality required for this exercise: easy visualization, browsing data by record IDs, and data manipulation capabilities.

**Note:** While DBeaver is more commonly used by data engineers and database administrators, data science students typically use Python-based tools (pandas, sqlalchemy) or Jupyter Notebooks with SQL magic commands for database work and analysis. However, for this exercise which specifically requires visualizing and browsing the database through a GUI, a tool like DBeaver is appropriate. For later exercises involving data analysis or automation, Python-based approaches would be more typical in data science workflows.

## Installation

Install DBeaver via Homebrew:

```bash
brew install --cask dbeaver-community
```

## Connection Setup

1. Open DBeaver
2. Create a new database connection
3. Select PostgreSQL as the database type
4. Enter connection details:
   - **Host:** localhost
   - **Port:** 5432
   - **Database:** piscineds
   - **Username:** your_login (your student login)
   - **Password:** mysecretpassword
5. Test connection and save

Once connected, you can browse tables, view data, and manipulate records using the intuitive GUI interface.

## Alternative: VSCode/Cursor Extensions

If you prefer to work within your code editor, VSCode and Cursor support database extensions that provide similar functionality:

### SQLTools

**SQLTools** is a popular extension that offers database management directly in your editor:

1. Install the **SQLTools** extension from the VSCode/Cursor marketplace
2. Install the **SQLTools PostgreSQL/Cockroach Driver** extension
3. Create a new connection with the same connection details as above
4. Browse tables, run queries, and view data within the editor

**Advantages:**
- Works directly in your code editor
- No need to switch between applications
- Integrated with your development workflow
- Free and open source

**Installation:**
- Search for "SQLTools" in the VSCode/Cursor extensions marketplace
- Also install "SQLTools PostgreSQL/Cockroach Driver" for PostgreSQL support

Other VSCode extensions like **PostgreSQL** (official) and **Database Client** are also available as alternatives.

