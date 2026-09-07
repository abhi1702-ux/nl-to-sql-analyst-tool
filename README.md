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

2. Install dependencies

3. Add your own Gemini API key — create a file named `.env` in the project folder with: (Get a free key at [Google AI Studio](https://aistudio.google.com))

4. Run the app (streamlit run app.py)


## Example questions to try

- Who are the top 5 customers by total spending?
- Which genre has the most tracks?
- How many invoices were billed from each country?
- What are the 10 longest tracks in the database?
- Which employee supports the most customers?

## Safety

All AI-generated SQL is validated before execution — any query containing `DELETE`, `DROP`, `UPDATE`, `INSERT`, `ALTER`, or `TRUNCATE` is automatically blocked. Only read (`SELECT`) queries are allowed to run.

## Project Structure

├── app.py # Streamlit web interface
├── main.py # Command-line version
├── nl_to_sql.py # Converts English questions to SQL via Gemini
├── query_runner.py # Executes SQL and returns results
├── schema_extractor.py # Reads database structure automatically
├── chinook.db # Sample database (digital media store)
└── requirements.txt # Python dependencies


## Why I built this

As someone pursuing a career in data analytics, I wanted to build something that demonstrates full-stack analytical thinking — from prompt engineering and API integration to database querying and building a usable interface. This project brings together SQL, Python, and modern LLM tooling into one working tool.
