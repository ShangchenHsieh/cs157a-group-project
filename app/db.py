# app/db.py
"""
Neo4j connection helper.

Reads connection settings from the project's env file (via python-dotenv)
and provides a simple driver/session helper for the rest of the codebase.

Usage:
    from app.db import get_driver, close_driver, session

    with session() as s:
        s.run("MATCH (n) RETURN count(n)")
"""
from contextlib import contextmanager
import os
from typing import Iterator, Optional

from neo4j import GraphDatabase, Driver
from dotenv import load_dotenv, find_dotenv


# Compute project root and attempt multiple dotenv locations:
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1) explicit project-root "env" (legacy)
_legacy_env_path = os.path.join(_ROOT, "env")
if os.path.exists(_legacy_env_path):
    load_dotenv(_legacy_env_path, override=False)

# 2) explicit project-root ".env"
_dot_env_path = os.path.join(_ROOT, ".env")
if os.path.exists(_dot_env_path):
    load_dotenv(_dot_env_path, override=False)

# 3) fallback: walk up from CWD and import-time file to find any ".env"
_found = find_dotenv(usecwd=True)
if _found:
    load_dotenv(_found, override=False)

_driver: Optional[Driver] = None


def get_driver() -> Driver:
    """Return a singleton Neo4j driver, creating it if needed."""
    global _driver
    if _driver is None:
        uri = os.getenv("DATABASE_URI")
        user = os.getenv("DATABASE_USER")
        password = os.getenv("DATABASE_PASSWORD")
        database = os.getenv("NEO4J_DATABASE", "neo4j")

        missing = [name for name, val in [
            ("DATABASE_URI", uri),
            ("DATABASE_USER", user),
        ] if not val]
        if missing:
            searched = [p for p in (_legacy_env_path, _dot_env_path, _found) if p]
            hint = (
                "Could not find required env vars. "
                f"Missing: {', '.join(missing)}. "
                "Looked for env files at: " + (", ".join(searched) if searched else "(none)") + ". "
                "Either create cs157c_group_project/.env (recommended) or set shell env vars."
            )
            raise RuntimeError(hint)

        _driver = GraphDatabase.driver(uri, auth=(user, password))
        # Optionally validate connectivity early:
        with _driver.session(database=database) as s:
            s.run("RETURN 1")
    return _driver


@contextmanager
def session() -> Iterator:
    """Context-managed Neo4j session using the configured database."""
    drv = get_driver()
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    with drv.session(database=database) as s:
        yield s


def close_driver() -> None:
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None
