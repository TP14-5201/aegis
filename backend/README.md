# Aegis Backend

## Table of Contents
- [Prerequisites](#prerequisites)
    - [Conda](#conda)
    - [Venv](#venv)
- [Database Seeding](#database-seeding)
    - [Visual Way](#1-visual-way)
    - [Command Line Way](#2-command-line-way)
- [Testing](#testing)

## Prerequisites
- Python > 3.10

### Conda
```{bash}
cd backend
conda create -n aegis python=3.11 --y && conda activate aegis # if you are using conda
pip install -r requirements.txt
```

### Venv
```{bash}
cd backend
python -m venv .venv                                        
.venv\Scripts\activate # or: source .venv/bin/activate
pip install -r requirements.txt
```

## Database Seeding
When you are developing the application for the first time, you need to seed the database with data.

```{bash}
cd backend
python -m src.services.data_seeding
```

To have a quick check at the database, you can use:

### 1. Visual Way
If you want a spreadsheet-like view of your data, use a GUI tool:
- SQLite Viewer (Web): Open [SQLite Viewer](https://sqliteviewer.com/) and upload the `app.db` file.
- DB Browser for SQLite (Desktop): Download [DB Browser for SQLite](https://sqlitebrowser.org/) and open the `app.db` file.

### 2. Command Line Way
If you want to check the database using the command line, you can use:

```{bash}
cd backend
sqlite3 app.db
SELECT * FROM support_services LIMIT 10;
```

To learn more about the database schema, please read the Aegis Data Dictionary [document](https://docs.google.com/document/d/1n5D1F347cKoDv5rV5ZQbNClFlAJ23ZQ1uMhdrcXPgxA/edit?usp=sharing).

## Testing
After every changes or fixes in the backend directory, you MUST run the tests to make sure that the changes are not breaking any existing functionality. Additionallly, update the unit test files if needed under the `tests/` directory.

```{bash}
cd backend
pytest tests/ -v --cov=src --cov-report=term-missing
```