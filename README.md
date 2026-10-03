# AI Product Analytics Platform

An AI-powered natural-language analytics platform that enables users to query structured e-commerce data using business questions instead of manually writing SQL. The system combines **schema-aware LLM-based SQL generation, SQL validation, analytical query execution, KPI analysis, and data-grounded insight generation** in an interactive Streamlit application.

## Architecture

```text
Olist E-Commerce Data
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
* **Dynamic Data Ingestion** — automatically discovers CSV files and loads them into DuckDB tables.
* **KPI & Analytical Processing** — processes query results using Pandas for business-level analysis.
* **Data-Grounded Insights** — generates explanations based on the actual query results.
* **Evaluation Pipeline** — measures SQL validity, execution success, errors, and query latency.

## Dataset

The project uses the **Olist Brazilian E-Commerce Public Dataset**, a relational e-commerce dataset containing customer, order, product, payment, and review information.

Primary tables include:

```text
customers
orders
order_items
products
order_payments
order_reviews
```

CSV files are automatically discovered from the `data/` directory and loaded into DuckDB.

## Example Workflow

**User Question**

```text
What are the top 5 product categories by revenue?
```

**Processing**

```text
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

```text
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

| Component       | Technology       |
| --------------- | ---------------- |
| Language        | Python           |
| LLM             | Gemini API       |
| Database        | DuckDB           |
| SQL Validation  | SQLGlot          |
| Data Processing | Pandas           |
| Dashboard       | Streamlit        |
| Dataset         | Olist E-Commerce |

## Project Structure

```text
ai-product-analytics/
├── data/
│   └── Olist CSV files
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

```bash
git clone <repository-url>
cd ai-product-analytics
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=gemini-3.8-flash
```

Add the Olist CSV files to `data/` and launch the application:

```bash
streamlit run app.py
```

## License

MIT
