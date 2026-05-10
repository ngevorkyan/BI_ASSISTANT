import requests

from app.config.settings import OLLAMA_MODEL


def generate_sql(question: str, context: str) -> str:
    prompt = f"""
You are a BI SQL assistant.

Your job:
Generate ONLY valid SQL.

Do not explain.
Do not say hello.
Do not ask for more metadata.
Use only the SQL logic from the context.

User question:
{question}

Available metadata and SQL examples:
{context}

Return only SQL:
"""

    response = requests.post(
        "http://ollama:11434/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    sql = response.json().get("response", "").strip()

    sql = sql.replace("```sql", "").replace("```", "").strip()

    return sql