import pandas as pd


def summarize(df: pd.DataFrame):
    result = {"rows": len(df), "columns": list(df.columns)}
    numeric = df.select_dtypes(include="number")
    if not numeric.empty:
        result["numeric_summary"] = numeric.describe().round(2).to_dict()
    return result
