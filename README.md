# AI Product Analytics Platform

A lightweight natural-language analytics platform that converts business questions into schema-aware DuckDB SQL, validates and executes the SQL, and produces data-grounded insights.

## Stack

Python · DuckDB · Gemini · SQLGlot · Pandas · Streamlit

## Data

Put the selected Olist CSV files in `data/`:

- customers.csv
- orders.csv
- order_items.csv
- products.csv
- order_payments.csv
- order_reviews.csv

The loader discovers CSV files automatically, so more Olist tables can be added later.

## Run

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your Gemini API key.

Then:

```bash
streamlit run app.py
```

Click **Load / Refresh Data**, then ask a business question.

## Evaluation

After the data is loaded:

```bash
python -m src.evaluation
```

The benchmark reports SQL validity, execution success, errors, and latency.
