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

    return {
        "original_question": text,
        "segment": detect_segment(text)
    }


def detect_segment(text: str) -> str:
    """
    Only detects generic filter intent.
    Metric detection should come from RAG / metadata retrieval.
    """

    if contains_phrase(text, [
        "no filter",
        "without filter",
        "unfiltered",
        "non filtered",
        "non-filtered",
        "remove filter",
        "remove filters",
        "all"
    ]):
        return "all"

    words = text.split()

    for word in words:
        if word.endswith("ed"):
            return word

        if word.endswith("ive"):
            return word

    return "all"


def contains_phrase(text: str, phrases: list[str]) -> bool:
    return any(phrase in text for phrase in phrases)