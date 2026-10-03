from pathlib import Path
import sys

import streamlit as st
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")

from src.database import execute_query, get_connection, list_tables, load_csvs
from src.insights import create_insight
from src.llm import generate_sql
from src.schema import get_schema_text
from src.sql import validate_sql

st.set_page_config(page_title="AI Product Analytics Platform", layout="wide")
st.title("AI Product Analytics Platform")
st.caption("Natural-language product analytics with schema-aware SQL generation.")

with st.sidebar:
    st.header("Data")
    if st.button("Load / Refresh Data"):
        try:
            tables = load_csvs()
            st.success(f"Loaded {len(tables)} table(s).")
        except Exception as exc:
            st.error(str(exc))

    try:
        tables = list_tables()
        st.write("Tables")
        for table in tables:
            st.write(f"• {table}")
    except Exception:
        st.info("Load the CSV data first.")

question = st.text_area(
    "Ask a product analytics question",
    placeholder="Example: What are the top 10 product categories by revenue?",
    height=100,
)

if st.button("Analyze", type="primary"):
    if not question.strip():
        st.warning("Enter a question first.")
        st.stop()

    try:
        schema = get_schema_text()
        with st.spinner("Generating SQL..."):
            generated_sql = generate_sql(question, schema)

        valid, validated_sql = validate_sql(generated_sql)
        if not valid:
            st.error(f"SQL validation failed: {validated_sql}")
            st.code(generated_sql, language="sql")
            st.stop()

        st.subheader("Generated SQL")
        st.code(validated_sql, language="sql")

        with st.spinner("Executing query..."):
            df = execute_query(validated_sql)

        st.subheader("Results")
        st.dataframe(df, use_container_width=True)

        st.subheader("Data-Grounded Insight")
        with st.spinner("Generating insight..."):
            st.write(create_insight(question, df))

    except Exception as exc:
        st.error(f"Error: {exc}")
