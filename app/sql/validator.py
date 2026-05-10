import sqlglot


def validate_sql(sql: str) -> bool:
    if not sql or not sql.strip():
        raise ValueError("Generated SQL is empty.")

    try:
        sqlglot.parse_one(sql)
        return True
    except Exception as e:
        raise ValueError(f"Invalid SQL generated: {sql}") from e