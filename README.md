## Running the project (quickstart)

This repository is a small social-network demo that uses Neo4j as the
back-end and a Python front-end. The instructions below show how to
start a local Neo4j instance, prepare your Python environment, populate
the database with sample data, and run the application.

### 1) Prepare Neo4j

You can run Neo4j locally (Desktop, installed package) 
Create a Neoo4j instance thorugh the Desktop GUI


### 2) Create an env file (project root)

Create a file named `env` (no leading dot) in the project root with the
following variables (replace the password with the real one):

```
DATABASE_URI=bolt://localhost:7687
DATABASE_USER=neo4j
DATABASE_PASSWORD=test
NEO4J_DATABASE=neo4j
```
Or modify the credential in `.env` to match you credentials of the DB

The project will load environment variables from `env` automatically.

### 3) Python environment & dependencies

Create and activate a virtual environment, then install requirements:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

requirements.txt includes `neo4j` and `python-dotenv`.

### 4) Populate the database with sample data

The repository includes `scripts/data_population_script.py`, which reads
`data/farmaciavernile.it.csv` and synthesizes additional users to reach
1000 nodes and 5000 relationships by default.

Run it from the project root (recommended form):

```bash
python3 -m scripts.data_population_script --csv data/farmaciavernile.it.csv --nodes 1000 --rels 5000
```

The script:
- Creates `:User` nodes with properties `username`, `name`, `email`, `password`.
- Creates `:FOLLOW` relationships between users (MERGE used so running
	the script multiple times is idempotent).

### 5) Run the application

From the project root, run the main app module:

```bash
python3 -m app.main
```

### 6) Verify data in Neo4j

Use the Neo4j Browser (http://localhost:7474) or `cypher-shell` and run:

```cypher
MATCH (u:User) RETURN count(u);
MATCH ()-[r:FOLLOWS]->() RETURN count(r);
```

