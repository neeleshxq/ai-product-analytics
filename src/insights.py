from .llm import generate_insight


def create_insight(question, df):
    if df.empty:
        return "The query returned no rows, so there is no data-grounded insight to report."
    result_text = df.head(100).to_string(index=False)
    return generate_insight(question, result_text)
