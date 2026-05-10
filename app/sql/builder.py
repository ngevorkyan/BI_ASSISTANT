def build_sql(metric_data: dict, segment: str = "all", group_by: str | None = None) -> str:
    base_sql = metric_data["base_sql"]
    segments = metric_data.get("segments", {})
    dimensions = metric_data.get("dimensions", {})

    segment_data = segments.get(segment)
    if segment_data is None:
        segment_data = segments.get("all")

    if isinstance(segment_data, dict):
        segment_filter = segment_data.get("filter")
    else:
        segment_filter = segment_data

    if group_by:
        group_column = dimensions.get(group_by)

        if not group_column:
            raise ValueError(f"Unknown group by dimension: {group_by}")

        base_sql = base_sql.replace("COUNT(*)", f"{group_column}, COUNT(*)")

    if segment_filter:
        base_sql += f" WHERE {segment_filter}"

    if group_by:
        base_sql += f" GROUP BY {group_column}"

    return base_sql