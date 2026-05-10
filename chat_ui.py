import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"

st.title("💬 BI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask about your database...")

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    try:

        response = requests.post(
            API_URL,
            json={"user_input": user_input},
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        response_type = data.get("type")

        if response_type == "sql":

            sql = data.get("sql", "")

            answer = (
                "SQL query generated successfully:\n\n"
                "```sql\n"
                f"{sql}\n"
                "```"
            )

        elif response_type == "error":

            answer = data.get(
                "answer",
                "I couldn't find matching metrics."
            )

        else:

            answer = data.get(
                "answer",
                "Hey 👋 Ask me about your database."
            )

    except requests.exceptions.ConnectionError:

        answer = (
            "Backend is not running.\n\n"
            "Start it with:\n"
            "`uvicorn app.main:app --reload`"
        )

    except requests.exceptions.HTTPError as e:

        answer = (
            f"Backend returned an error:\n\n{e}\n\n"
            f"Response:\n{response.text}"
        )

    except Exception as e:

        answer = f"Unexpected error: {e}"

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    with st.chat_message("assistant"):
        st.markdown(answer)