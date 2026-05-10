from app.rag.retriever import retrieve_context


TESTS = [
    ("active users", "active users"),
    ("count active users", "active users"),
    ("active user count", "active users"),
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


correct = 0

for question, expected in TESTS:
    predicted = get_metric(question)

    passed = predicted == expected

    if passed:
        correct += 1

    print(
        f"Question: {question} | Expected: {expected} | "
        f"Predicted: {predicted} | Pass: {passed}"
    )

success_rate = correct / len(TESTS) * 100

print("\nSuccess rate:", round(success_rate, 2), "%")