import json
from pathlib import Path
from functools import lru_cache


BASE_DIR = Path(__file__).resolve().parent


@lru_cache(maxsize=128)
def load_metric(metric_name: str) -> dict:
    file_path = BASE_DIR / f"{metric_name}.json"

    if not file_path.exists():
        raise ValueError(f"Metric not found: {metric_name}")

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)