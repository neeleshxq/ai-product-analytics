from .database import get_connection, list_tables


def get_schema_text():
    con = get_connection()
    try:
        tables = list_tables(con)
        if not tables:
            return "No tables are loaded."

        parts = []
        for table in tables:
            columns = con.execute(
                """
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = ?
                ORDER BY ordinal_position
                """,
                [table],
            ).fetchall()
            lines = [f"TABLE {table}:"]
            lines += [f"  - {name}: {dtype}" for name, dtype in columns]
            parts.append("\n".join(lines))
        return "\n\n".join(parts)
    finally:
        con.close()
