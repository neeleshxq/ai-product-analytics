import re
import sqlglot
from sqlglot import exp

FORBIDDEN = {
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "TRUNCATE",
    "COPY", "ATTACH", "DETACH", "INSTALL", "LOAD", "EXPORT", "IMPORT"
}


def clean_sql(sql: str) -> str:
    sql = sql.strip()
    sql = re.sub(r"^```(?:sql)?\s*", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"\s*```$", "", sql)
    return sql.strip().rstrip(";").strip()


def validate_sql(sql: str):
    sql = clean_sql(sql)
    if not sql:
        return False, "Empty SQL."

    upper = sql.upper()
    for keyword in FORBIDDEN:
        if re.search(rf"\b{keyword}\b", upper):
            return False, f"Forbidden SQL operation: {keyword}"

    try:
        statements = sqlglot.parse(sql, read="duckdb")
        if len(statements) != 1:
            return False, "Only one SQL statement is allowed."
        tree = statements[0]
    except Exception as exc:
        return False, f"SQL syntax error: {exc}"

    if not isinstance(tree, (exp.Select, exp.Union)):
        return False, "Only read-only SELECT queries are allowed."

    return True, sql
