def is_greeting(text: str) -> bool:
    return text.lower().strip() in [
        "hi",
        "hello",
        "hey",
        "yo",
        "good morning",
        "good evening"
    ]


def parse_user_input(text: str) -> dict:
    text = text.lower().strip()

    metric = None
    segment = "all"

    if any(word in text for word in [
        "user",
        "users",
        "client",
        "clients",
        "customer",
        "customers"
    ]):
        metric = "users"

    if "inactive" in text:
        segment = "inactive"
    elif "active" in text:
        segment = "active"

    if any(phrase in text for phrase in [
        "all",
        "no filter",
        "without filter",
        "unfiltered",
        "non filtered",
        "non-filtered",
        "remove filter",
        "remove filters"
    ]):
        segment = "all"

    return {
        "metric": metric,
        "segment": segment
    }