"""
schema_extractor.py
Reads the database structure (tables + columns) automatically.
This is what we'll later show the AI so it knows what data exists.
"""

import sqlite3

DB_PATH = "chinook.db"


def get_schema_text() -> str:
    """
    Returns a plain-text description of every table and its columns,
    formatted so an LLM can easily read it.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Get all table names
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cur.fetchall()]

    schema_lines = []
    for table in tables:
        cur.execute(f"PRAGMA table_info({table});")
        columns = cur.fetchall()  # each row: (cid, name, type, notnull, dflt, pk)
        col_descriptions = [f"{col[1]} ({col[2]})" for col in columns]
        schema_lines.append(f"Table: {table}")
        schema_lines.append(f"  Columns: {', '.join(col_descriptions)}")

    conn.close()
    return "\n".join(schema_lines)


if __name__ == "__main__":
    print(get_schema_text())
