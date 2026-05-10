FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
EXPOSE 8501

CMD sh -c "python -m app.ingestion.ingest && uvicorn app.main:app --host 0.0.0.0 --port 8000 & streamlit run chat_ui.py --server.address 0.0.0.0 --server.port 8501"