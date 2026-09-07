# Ask Your Database — Natural Language to SQL Tool

An AI-powered tool that lets you ask questions about a database in plain English and instantly get back the SQL query **and** the results — no SQL knowledge required to use it.

Built to bridge the gap between business questions and databases: type "Who are the top 5 customers by spending?" and get a working SQL query, a results table, and a chart, all generated on the fly.

##  How it works

1. You type a question in plain English (e.g. *"Which genre has the most tracks?"*)
2. The app reads the database schema automatically and sends it, along with your question, to Google's Gemini API
3. Gemini generates a SQL query
4. The app validates the query is safe (read-only, no DELETE/DROP/UPDATE) and runs it
5. Results are displayed as a table, with an automatic chart when the data supports it

## Tech Stack

- **Python** — core logic
- **SQLite** — database engine (using the [Chinook sample database](https://github.com/lerocha/chinook-database), a fictional digital media store)
- **Gemini API** — natural language to SQL translation
- **Streamlit** — web interface
- **Pandas** — data handling and display

## Running it locally

1. Clone this repository
