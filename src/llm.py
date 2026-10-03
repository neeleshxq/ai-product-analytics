import os
from google import genai

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing. Add it to .env")

client = genai.Client(api_key=api_key)


def generate_sql(question: str, schema_text: str) -> str:
    prompt = f"""
You are a careful product analytics SQL generator.

SQL dialect: DuckDB

DATABASE SCHEMA:
{schema_text}

USER QUESTION:
{question}

Rules:
- Return exactly one read-only SELECT query.
- Use only tables and columns present in the schema.
- Do not invent tables, columns, values, or relationships.
- Use DuckDB-compatible SQL.
- Prefer explicit joins and readable aliases.
- For revenue from Olist order_items, use price unless the question specifically asks about another monetary field.
- Return SQL only. No markdown or explanation.
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text.strip()


def generate_insight(question: str, result_text: str) -> str:
    prompt = f"""
You are a product analytics assistant.

Question:
{question}

Actual query result:
{result_text}

Write a concise business insight based ONLY on the supplied result.
Do not invent numbers or facts.
Mention a trend, comparison, or notable result only when directly supported by the data.
If the result is insufficient, say so.
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text.strip()