import sqlite3
import os
from flask import g, current_app

DATABASE = os.path.join(os.path.dirname(__file__), "instance", "projects.db")


def get_db():
    """Open a new database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # lets us access columns by name like a dict
    return conn


def init_db():
    """Create the tables if they don't already exist."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            description TEXT,
            owner       TEXT,
            status      TEXT    DEFAULT 'Planning',
            milestone   TEXT,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # add a trigger so updated_at auto-updates on row changes
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS update_timestamp
        AFTER UPDATE ON projects
        FOR EACH ROW
        BEGIN
            UPDATE projects SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
        END
    """)

    conn.commit()
    conn.close()
    print("Database initialized.")
