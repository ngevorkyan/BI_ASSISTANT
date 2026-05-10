from fastapi import APIRouter
from pydantic import BaseModel

from app.parser.query_parser import is_greeting, parse_user_input
from app.metadata.loader import load_metric
from app.rag.retriever import retrieve_context
from app.sql.builder import build_sql

router = APIRouter()


class AskRequest(BaseModel):
    user_input: str


@router.post("/ask")
def ask(request: AskRequest):
    try:
        user_input = request.user_input.strip()

        if is_greeting(user_input):
            return {
                "type": "chat",
                "answer": (
                    "Hey 👋 I’m your BI assistant. "
                    "Ask me about your company's users, revenue et.c."
                )
            }

        parsed = parse_user_input(user_input)

        # Retrieve the best matching metric from metadata/RAG
        retrieved_docs = retrieve_context(user_input)
        metric = None

        if retrieved_docs:
            metric = retrieved_docs[0].metadata.get("metric_name")

        if metric:
            metric_data = load_metric(metric)

            sql = build_sql(
                metric_data=metric_data,
                segment=parsed["segment"]
            )

            return {
                "type": "sql",
                "question": user_input,
                "metric": metric,
                "segment": parsed["segment"],
                "answer": "SQL query generated successfully:",
                "sql": sql
            }

        return {
            "type": "error",
            "answer": (
                "I couldn't find matching metrics. "
                "Try asking me about users, revenue et.c."
            ),
            "sql": None
        }

    except Exception as e:
        return {
            "type": "error",
            "answer": "Backend crashed.",
            "debug_error": str(e)
        }