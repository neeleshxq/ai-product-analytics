import json
import time
from pathlib import Path
import pandas as pd

from .database import execute_query
from .llm import generate_sql
from .schema import get_schema_text
from .sql import validate_sql

EVAL_FILE = Path(__file__).resolve().parent.parent / "evaluation_questions.json"


def run_evaluation():
    questions = json.loads(EVAL_FILE.read_text(encoding="utf-8"))
    schema = get_schema_text()
    results = []

    for item in questions:
        question = item["question"]
        start = time.perf_counter()
        row = {
            "question": question,
            "sql_valid": False,
            "executed": False,
            "error": "",
        }
        try:
            generated = generate_sql(question, schema)
            valid, message = validate_sql(generated)
            row["sql_valid"] = valid
            row["generated_sql"] = generated
            if valid:
                execute_query(message)
                row["executed"] = True
            else:
                row["error"] = message
        except Exception as exc:
            row["error"] = str(exc)
        row["latency_seconds"] = round(time.perf_counter() - start, 3)
        results.append(row)

    return pd.DataFrame(results)


if __name__ == "__main__":
    df = run_evaluation()
    print(df.to_string(index=False))
    print(f"\nSQL validity rate: {df['sql_valid'].mean() * 100:.2f}%")
    print(f"Execution success rate: {df['executed'].mean() * 100:.2f}%")
    print(f"Average latency: {df['latency_seconds'].mean():.3f}s")
