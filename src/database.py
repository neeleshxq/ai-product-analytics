from pathlib import Path
import re
import duckdb

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DB_PATH = ROOT / "analytics.duckdb"


def safe_table_name(filename: str) -> str:
    name = Path(filename).stem.lower()
    return re.sub(r"[^a-z0-9_]+", "_", name).strip("_")


def get_connection():
    return duckdb.connect(str(DB_PATH))


def load_csvs(con=None):
    own_connection = con is None
    con = con or get_connection()
    csv_files = sorted(DATA_DIR.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {DATA_DIR}")

    loaded = []
    try:
        for file in csv_files:
            table = safe_table_name(file.name)
            con.execute(
                f"CREATE OR REPLACE TABLE {table} AS "
                "SELECT * FROM read_csv_auto(?, header=true, sample_size=-1)",
                [str(file)],
            )
            loaded.append(table)
        return loaded
    finally:
        if own_connection:
            con.close()


def list_tables(con=None):
    own_connection = con is None
    con = con or get_connection()
    try:
        return [row[0] for row in con.execute("SHOW TABLES").fetchall()]
    finally:
        if own_connection:
            con.close()


def execute_query(sql: str):
    con = get_connection()
    try:
        return con.execute(sql).df()
    finally:
        con.close()
