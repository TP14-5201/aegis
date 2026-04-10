# Aegis Backend

## Table of Contents
- [Prerequisites](#prerequisites)
- [Database Seeding](#database-seeding)

## Prerequisites
- Python > 3.10

#### Conda
```{bash}
cd backend
conda create -n aegis python=3.11 --y && conda activate aegis # if you are using conda
pip install -r requirements.txt
```

#### Venv
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

To learn more about the database schema, please read the Aegis Data Dictionary [document](https://docs.google.com/document/d/1n5D1F347cKoDv5rV5ZQbNClFlAJ23ZQ1uMhdrcXPgxA/edit?usp=sharing).