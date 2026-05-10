from app.rag.retriever import retrieve_context


TEST_CASES = [
    ("active users", "active users"),
    ("count active users", "active users"),
    ("active usr", "active users"),
    ("ctive users", "active users"),

    ("revenue", "revenue"),
    ("total sales", "revenue"),
    ("income", "revenue"),

    ("orders", "orders"),
    ("total orders", "orders"),

    ("school", None),
    ("banana", None),
    ("weather today", None),
]


def get_metric(question):
    docs = retrieve_context(question)

    if not docs:
        return None

    return docs[0].metadata.get("metric_name")


def test_retriever_success_rate():
    correct = 0

    for question, expected in TEST_CASES:
        predicted = get_metric(question)

        if predicted == expected:
            correct += 1

    success_rate = correct / len(TEST_CASES)

    assert success_rate >= 0.9