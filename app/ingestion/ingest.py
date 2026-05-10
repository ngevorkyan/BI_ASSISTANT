import json
from pathlib import Path

from app.config.settings import METADATA_PATH
from app.rag.vector_store import collection


def load_metadata_files():
    files = list(Path(METADATA_PATH).glob("*.json"))

    if not files:
        raise FileNotFoundError(f"No JSON files found in {METADATA_PATH}")

    documents = []
    ids = []
    metadatas = []

    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        metric_name = data.get("metric_name", file.stem)
        description = data.get("description", "")
        sql = data.get("sql", "")

        document = f"""
Metric name: {metric_name}
Description: {description}
SQL:
{sql}
""".strip()

        documents.append(document)
        ids.append(metric_name.lower().replace(" ", "_"))
        metadatas.append({
            "metric_name": metric_name,
            "source_file": file.name
        })

    return ids, documents, metadatas


def ingest():
    ids, documents, metadatas = load_metadata_files()

    existing = collection.get()

    if existing and existing.get("ids"):
        collection.delete(ids=existing["ids"])

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    print(f"Ingested {len(documents)} metadata files.")


if __name__ == "__main__":
    ingest()