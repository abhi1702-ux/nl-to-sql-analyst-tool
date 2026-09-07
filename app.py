"""
app.py
The web interface for our Natural Language -> SQL tool.
Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd

from nl_to_sql import question_to_sql
from query_runner import run_query

FORBIDDEN_KEYWORDS = ["DELETE", "DROP", "UPDATE", "INSERT", "ALTER", "TRUNCATE"]


def is_safe_sql(sql: str) -> bool:
    sql_upper = sql.upper()
    return not any(keyword in sql_upper for keyword in FORBIDDEN_KEYWORDS)


st.set_page_config(page_title="Ask Your Database", page_icon="🗄️")

st.title("🗄️ Ask Your Database")
st.write(
    "Type a question in plain English about the music store database "
    "(customers, invoices, tracks, artists, etc.) and get instant SQL + results."
)

with st.expander("💡 Example questions to try"):
    st.markdown(
        "- Who are the top 5 customers by total spending?\n"
        "- Which genre has the most tracks?\n"
        "- How many invoices were billed from each country?\n"
        "- What are the 10 longest tracks in the database?\n"
        "- Which employee supports the most customers?"
    )

question = st.text_input("Your question:", placeholder="e.g. Who are the top 5 customers by total spending?")

if st.button("Ask", type="primary") and question.strip():
    with st.spinner("Thinking..."):
        try:
            sql = question_to_sql(question)
        except Exception as e:
            st.error(f"Couldn't reach the AI model: {e}")
            st.stop()

    st.subheader("Generated SQL")
    st.code(sql, language="sql")

    if not is_safe_sql(sql):
        st.error("⚠️ Blocked: the generated SQL contained a forbidden command (safety check).")
    else:
        try:
            columns, rows = run_query(sql)
            df = pd.DataFrame(rows, columns=columns)

            st.subheader("Results")
            st.dataframe(df, use_container_width=True)

            numeric_cols = df.select_dtypes(include="number").columns
            if len(numeric_cols) > 0 and len(df) <= 20 and len(df) > 1:
                st.subheader("Quick chart")
                label_col = df.columns[0]
                value_col = numeric_cols[0]
                st.bar_chart(df.set_index(label_col)[value_col])

        except Exception as e:
            st.error(f"⚠️ Error running the generated query: {e}")