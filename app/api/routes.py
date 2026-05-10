from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.retriever import retrieve_context

router = APIRouter()


class AskRequest(BaseModel):
    user_input: str


def is_greeting(text: str) -> bool:
    greetings = [
        "hi",
        "hello",
        "hey",
        "yo",
        "good morning",
        "good evening"
    ]

    return text.lower().strip() in greetings


@router.post("/ask")
def ask(request: AskRequest):

    try:

        user_input = request.user_input

        # GREETING MODE
        if is_greeting(user_input):
            return {
                "type": "chat",
                "answer": "Hey 👋 I’m your BI assistant. Ask me something like: show active users, show revenue, or show orders."
            }

        # RAG RETRIEVAL
        docs = retrieve_context(user_input)

        if not docs:
            return {
                "type": "error",
                "answer": (
                    "I couldn't find matching metrics. "
                    "Try: active users, revenue, or orders."
                ),
                "sql": None
            }

        best_doc = docs[0].page_content

        sql = extract_sql(best_doc)

        return {
            "type": "sql",
            "question": user_input,
            "answer": "SQL query generated successfully:",
            "sql": sql,
            "matched_context": best_doc
        }

    except Exception as e:

        return {
            "type": "error",
            "answer": "Backend crashed.",
            "debug_error": str(e)
        }


def extract_sql(text: str) -> str:

    if "SQL:" in text:
        return text.split("SQL:", 1)[1].strip()

    return text.strip()