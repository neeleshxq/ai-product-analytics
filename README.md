# AI Product Analytics Platform

An AI-powered natural-language analytics platform that enables users to query structured tabular data using business questions instead of manually writing SQL. The system combines **schema-aware LLM-based SQL generation, SQL validation, analytical query execution, KPI analysis, and data-grounded insight generation** in an interactive Streamlit application.

## Architecture

```text id="f7k8y2"
CSV / Tabular Data
        ↓
Dynamic CSV Loader
        ↓
DuckDB
        ↓
Schema Extraction
        ↓
Schema-Aware Gemini
        ↓
Natural Language → SQL
        ↓
SQLGlot Validation
        ↓
SQL Execution
        ↓
Pandas / KPI Analytics
        ↓
Data-Grounded Insights
        ↓
Streamlit Dashboard

        ↕
Evaluation Layer
SQL Validity · Execution Success · Error Analysis · Latency
```

The LLM handles **user-intent understanding and SQL generation**, while **DuckDB remains the source of truth for data retrieval and numerical computation**.

## Key Features

* **Natural Language → SQL** — converts analytical questions into DuckDB-compatible SQL.
* **Schema-Aware Generation** — dynamically extracts tables, columns, and data types and provides them as context to Gemini.
* **SQL Validation** — parses generated queries with SQLGlot before execution.
* **Read-Only Query Enforcement** — blocks destructive DML/DDL operations such as `INSERT`, `UPDATE`, `DELETE`, `DROP`, and `ALTER`.
* **Dynamic CSV Ingestion** — automatically discovers CSV files and loads them into DuckDB tables.
* **KPI & Analytical Processing** — processes query results using Pandas for business-level analysis.
* **Data-Grounded Insights** — generates explanations based on the actual query results.
* **Evaluation Pipeline** — measures SQL validity, execution success, errors, and query latency.

## Dataset

The platform is designed to work with **general CSV/tabular datasets**. For demonstration and evaluation, this project uses the **Olist Brazilian E-Commerce Public Dataset**.

Primary Olist tables used include:

```text id="gj6k1x"
customers
orders
order_items
products
order_payments
order_reviews
```

CSV files are automatically discovered from the `data/` directory, allowing the same pipeline to be used with other compatible tabular datasets without changing the core ingestion architecture.

## Example Workflow

**User Question**

```text id="7o4t5d"
What are the top 5 product categories by revenue?
```

**Processing**

```text id="w2x6t3"
Natural Language Question
          ↓
Schema-Aware Prompt
          ↓
Gemini SQL Generation
          ↓
SQLGlot Parsing & Validation
          ↓
DuckDB Query Execution
          ↓
Pandas Result Analysis
          ↓
Data-Grounded Business Insight
```

The dashboard displays the generated SQL, query results, and the resulting analytical insight.

## Evaluation

A predefined benchmark of analytical questions is stored in:

```text id="y5f1c9"
evaluation_questions.json
```

The evaluation pipeline records:

| Metric            | Description                                       |
| ----------------- | ------------------------------------------------- |
| SQL Validity      | Whether generated SQL passes validation           |
| Execution Success | Whether the validated query executes successfully |
| Error Analysis    | Captures SQL generation and execution failures    |
| Latency           | Measures query processing time                    |

This provides a repeatable framework for analyzing failures in the natural-language-to-SQL pipeline.

## Tech Stack

| Component             | Technology       |
| --------------------- | ---------------- |
| Language              | Python           |
| LLM                   | Gemini API       |
| Database              | DuckDB           |
| SQL Validation        | SQLGlot          |
| Data Processing       | Pandas           |
| Dashboard             | Streamlit        |
| Demonstration Dataset | Olist E-Commerce |

## Project Structure

```text id="6sj2b8"
ai-product-analytics/
├── data/
│   └── CSV files
│
├── src/
│   ├── database.py       # DuckDB setup and CSV ingestion
│   ├── schema.py         # Database schema extraction
│   ├── llm.py            # Gemini SQL and insight generation
│   ├── sql.py            # SQL parsing and validation
│   ├── analytics.py      # Data and KPI analysis
│   ├── insights.py       # Data-grounded insight generation
│   └── evaluation.py     # NL-to-SQL evaluation
│
├── app.py
├── config.py
├── evaluation_questions.json
└── requirements.txt
```

## Setup

Clone the repository and install dependencies:

```bash id="j5p7d4"
git clone <repository-url>
cd ai-product-analytics
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```text id="4t3z6a"
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=gemini-3.8-flash
```

Place the CSV files you want to analyze inside `data/` and launch the application:

```bash id="s0w4f1"
streamlit run app.py
```

## License

MIT
