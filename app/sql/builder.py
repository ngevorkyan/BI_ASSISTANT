def build_sql(metric_data: dict, segment: str = "all") -> str:
    sql = metric_data["base_sql"]

    segment_filter = metric_data.get("segments", {}).get(segment)

    if segment_filter:
        sql += f" WHERE {segment_filter}"

    return sql