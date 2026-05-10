from rapidfuzz import fuzz

from app.rag.vector_store import collection


FUZZY_THRESHOLD = 85
MAX_DISTANCE = 1.5


def make_document(content, metadata, distance=None):
    return type(
        "Document",
        (),
        {
            "page_content": content,
            "metadata": metadata,
            "distance": distance
        }
    )()


def fuzzy_metric_match(question: str):
    q = question.lower().strip()

    all_items = collection.get()

    documents = all_items.get("documents", [])
    metadatas = all_items.get("metadatas", [])

    best_score = 0
    best_doc = None
    best_metadata = None

    for document, metadata in zip(documents, metadatas):
        metric_name = metadata.get("metric_name", "").lower()

        score = fuzz.partial_ratio(q, metric_name)

        if score > best_score:
            best_score = score
            best_doc = document
            best_metadata = metadata

    if best_score >= FUZZY_THRESHOLD:
        return make_document(
            best_doc,
            best_metadata,
            distance=0
        )

    return None


def retrieve_context(question: str, n_results: int = 3):
    total = collection.count()

    if total == 0:
        return []

    fuzzy_doc = fuzzy_metric_match(question)

    if fuzzy_doc:
        return [fuzzy_doc]

    n_results = min(n_results, total)

    results = collection.query(
        query_texts=[question],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    docs = []

    for content, metadata, distance in zip(documents, metadatas, distances):
        if distance <= MAX_DISTANCE:
            docs.append(
                make_document(
                    content,
                    metadata,
                    distance
                )
            )

    return docs