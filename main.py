"""
main.py
Ties everything together:
1. Take a natural language question
2. Convert it to SQL using Gemini
3. Validate it's safe (read-only)
4. Run it and show results
"""

from nl_to_sql import question_to_sql
from query_runner import run_query

# Words that should NEVER appear in AI-generated SQL (safety check)
FORBIDDEN_KEYWORDS = ["DELETE", "DROP", "UPDATE", "INSERT", "ALTER", "TRUNCATE"]


def is_safe_sql(sql: str) -> bool:
    """Checks that the SQL doesn't contain any data-modifying commands."""
    sql_upper = sql.upper()
    return not any(keyword in sql_upper for keyword in FORBIDDEN_KEYWORDS)


def ask(question: str):
    print(f"\nQuestion: {question}")

    sql = question_to_sql(question)
    print(f"Generated SQL:\n{sql}\n")

    if not is_safe_sql(sql):
        print("⚠️  Blocked: generated SQL contained a forbidden command.")
        return

    try:
        columns, rows = run_query(sql)
        print(" | ".join(columns))
        print("-" * 50)
        for row in rows:
            print(" | ".join(str(v) for v in row))
    except Exception as e:
        print(f"⚠️  Error running query: {e}")


if __name__ == "__main__":
    ask("Who are the top 5 customers by total spending?")
