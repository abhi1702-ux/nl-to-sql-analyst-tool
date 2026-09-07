"""
query_runner.py
The 'engine' of our project: runs a SQL query against chinook.db and
returns the results in a readable form.
"""

import sqlite3

DB_PATH = "chinook.db"


def run_query(sql: str):
    """Run a SQL SELECT query and return (columns, rows)."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(sql)
    columns = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    conn.close()
    return columns, rows


def print_results(sql: str):
    """Run a query and pretty-print it like a table."""
    columns, rows = run_query(sql)
    print(" | ".join(columns))
    print("-" * 50)
    for row in rows:
        print(" | ".join(str(v) for v in row))


if __name__ == "__main__":
    # Example: top 5 customers by country count
    example_sql = """
    SELECT Country, COUNT(*) as num_customers
    FROM Customer
    GROUP BY Country
    ORDER BY num_customers DESC
    LIMIT 5;
    """
    print_results(example_sql)
