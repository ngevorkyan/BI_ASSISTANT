def build_sql(metric_data: dict, segment: str = "all") -> str:
    sql = metric_data["base_sql"]

    segment_data = metric_data.get("segments", {}).get(segment)

    if isinstance(segment_data, dict):
        segment_filter = segment_data.get("filter")
    else:
        segment_filter = segment_data

    if segment_filter:
        sql += f" WHERE {segment_filter}"

    return sql