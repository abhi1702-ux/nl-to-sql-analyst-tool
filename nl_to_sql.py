"""
nl_to_sql.py
The AI brain of the project:
Takes a plain-English question, sends it + the database schema to Gemini,
and gets back a SQL query.
"""

import os
import re
from dotenv import load_dotenv
from google import genai

from schema_extractor import get_schema_text

load_dotenv()  # reads GEMINI_API_KEY from the local .env file

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def build_prompt(question: str, schema: str) -> str:
    """Builds the instruction we send to the AI model."""
    return f"""You are an expert SQL generator for a SQLite database.

Here is the database schema:
{schema}

    Rules:
    - Only output a single valid SQLite SQL query.
    - Do NOT include explanations, comments, or markdown formatting (no ```sql).
    - Only generate SELECT queries. Never generate INSERT, UPDATE, DELETE, or DROP.
    - Use proper JOINs when a question requires data from multiple tables.
    - When the question involves "most", "least", "top", "highest", or "lowest",
      always include the relevant COUNT/SUM/AVG numeric column in the SELECT
      (not just the name), so the result shows both the item and its number.
    - For "which X has the most/least Y" questions, don't just return the top
      single row — include ORDER BY and a reasonable LIMIT (e.g. 10) so the
      result shows several rows for context, unless the question explicitly
      asks for only one.

Question: {question}

SQL query:"""


def clean_sql(raw_text: str) -> str:
    """Removes markdown fences or stray text if the model adds them anyway."""
    text = raw_text.strip()
    text = re.sub(r"^```sql", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"^```", "", text).strip()
    text = re.sub(r"```$", "", text).strip()
    return text


def question_to_sql(question: str) -> str:
    """Takes a natural language question, returns a SQL query string."""
    schema = get_schema_text()
    prompt = build_prompt(question, schema)
    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
    )
    sql = clean_sql(interaction.output_text)
    return sql

if __name__ == "__main__":
    test_question = "Who are the top 5 customers by total spending?"
    sql = question_to_sql(test_question)
    print("Question:", test_question)
    print("Generated SQL:\n", sql)
