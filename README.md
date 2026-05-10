# 💬 RAG SQL BI Assistant

A lightweight conversational BI assistant that uses:

* FastAPI
* Streamlit
* ChromaDB
* Retrieval-Augmented Generation (RAG)
* Fuzzy matching
* Local LLMs via Ollama

<img src="demo.png" width="700">

The project allows users to ask natural language questions like:

```text
active users
how many completed orders
revenue query
```

and receive SQL query logic back instead of executing queries directly.

---

# ✨ Features

## Conversational BI Interface

Users can interact with the assistant through a chat interface.

Examples:

```text
active users
```

```text
show revenue query
```

```text
orders
```

---

## Retrieval-Based SQL Generation

The assistant:

1. Retrieves matching metric metadata
2. Finds the most relevant business logic
3. Returns SQL query templates

It does NOT execute queries.

---

## Typo Handling

Supports:

* fuzzy matching
* typo correction
* partial matching
* synonym-style matching

Examples:

```text
ctive users
```

```text
active usr
```

```text
total sales
```

---

## Hallucination Prevention

Random words like:

```text
banana
school
weather
```

are rejected instead of producing fake SQL.

---

# 🏗 Architecture

```text
test_bi/
├── app/
│   ├── api/
│   ├── config/
│   ├── ingestion/
│   ├── metadata/
│   ├── rag/
│   ├── sql/
│   └── main.py
│
├── chroma_db/
├── tests/
├── chat_ui.py
├── requirements.txt
└── README.md
```

---

# 📁 Folder Explanations

## `app/api/`

Contains FastAPI routes.

Handles:

* user requests
* chat flow
* query responses
* retrieval orchestration

---

## `app/metadata/`

Stores BI metric definitions.

Example:

```json
{
  "metric_name": "active users",
  "description": "Returns count of active users",
  "sql": "SELECT COUNT(*) FROM users WHERE status = 'active';"
}
```

This acts as the knowledge base for retrieval.

---

## `app/ingestion/`

Reads metadata JSON files and inserts them into ChromaDB.

This process:

* creates embeddings
* stores metric context
* prepares retrieval

---

## `app/rag/`

Contains:

* vector store connection
* retriever logic
* fuzzy matching
* similarity filtering

---

## `app/sql/`

Responsible for:

* SQL generation
* validation
* future LLM orchestration

---

## `chroma_db/`

Persistent vector database storage.

Stores:

* embeddings
* vector metadata
* retrieval indexes

This folder is generated automatically after ingestion.

---

# 🧠 How Retrieval Works

The assistant follows this flow:

```text
User Question
      ↓
Fuzzy Matching
      ↓
Vector Similarity Search
      ↓
Best Matching Metric
      ↓
Return SQL Query
```

---

# 🧪 Automated Testing

The project includes retrieval evaluation tests.

Tests verify:

* typo handling
* synonym handling
* rejection of unrelated words
* metric accuracy

Run:

```bash
pytest -v
```

---

# 💻 Runs Fully Locally

This project runs entirely on the user's machine.

No cloud APIs are required.

Local components:

| Component  | Runs Locally |
| ---------- | ------------ |
| FastAPI    | ✅            |
| Streamlit  | ✅            |
| ChromaDB   | ✅            |
| Ollama     | ✅            |
| Embeddings | ✅            |

---

# 🔒 Privacy

Since everything runs locally:

* no SQL leaves the machine
* no metadata is uploaded
* no external LLM API required
* business logic stays private

---

# ⚡ Installation

## 1. Clone Repository

```bash
git clone <repo-url>
cd test_bi
```

---

## 2. Create Virtual Environment

Mac/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\\Scripts\\activate
```

---

## 3. Install Requirements

```bash
pip install -r requirements.txt
```

---

# 📦 Install Ollama

Install Ollama from:

```text
https://ollama.com
```

Then pull a model:

```bash
ollama pull llama3.2
```

Start Ollama:

```bash
ollama run llama3.2
```

Keep this terminal running.

---

# 🗂 Add Metadata

Place JSON metric files inside:

```text
app/metadata/
```

Example:

```json
{
  "metric_name": "revenue",
  "description": "Returns completed order revenue",
  "sql": "SELECT SUM(amount) FROM orders WHERE status='completed';"
}
```

---

# 🚀 Run Ingestion

This creates vector embeddings.

```bash
python -m app.ingestion.ingest
```

Expected output:

```text
Ingested 3 metadata files.
```

---

# ▶ Start Backend

```bash
uvicorn app.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Swagger docs:

```text
http://127.0.0.1:8000/docs
```

---

# 💬 Start Chat UI

In another terminal:

```bash
streamlit run chat_ui.py
```

Streamlit URL:

```text
http://localhost:8501
```

---

# 🧪 Example Queries

```text
active users
```

```text
count active users
```

```text
revenue query
```

```text
orders
```

---

# ❌ Example Rejections

```text
banana
```

```text
school
```

```text
weather today
```

These intentionally return:

```text
I couldn't find matching metrics.
```

---

# 📈 Evaluation

Run retrieval tests:

```bash
pytest -v
```

The goal is usually:

```text
90%+ retrieval accuracy
```

---

# 🛠 Current Tech Stack

| Technology | Purpose           |
| ---------- | ----------------- |
| FastAPI    | Backend API       |
| Streamlit  | Chat UI           |
| ChromaDB   | Vector storage    |
| RapidFuzz  | Typo handling     |
| Ollama     | Local LLM serving |
| SQLGlot    | SQL validation    |

---

# 🔮 Future Improvements

Potential enhancements:

## Better Embeddings

Replace default Chroma embeddings with:

* sentence-transformers
* bge-large
* Instructor embeddings

---

## Hybrid Retrieval

Combine:

* fuzzy matching
* embeddings
* rerankers
* metadata filters

---

## Real Database Execution

Future versions could:

* execute generated SQL
* connect to Snowflake
* connect to PostgreSQL
* connect to BigQuery

---

## Semantic Layers

Potential support for:

* metrics catalogs
* dbt models
* semantic metric layers
* governed BI definitions

---

## Production Features

Possible future additions:

* authentication
* conversation memory
* SQL lineage
* observability
* evaluation dashboards
* caching
* Docker deployment
* Kubernetes deployment

---

# 📌 Important Notes

## This project currently:

✅ retrieves SQL logic

✅ handles typos

✅ runs locally

✅ prevents most hallucinations

✅ supports conversational BI experimentation

---

## This project currently does NOT:

❌ execute SQL

❌ access real databases automatically

❌ guarantee production-grade security

❌ replace enterprise semantic models

---

# 🤝 Intended Use

This project is ideal for:

* conversational BI prototypes
* RAG experimentation
* SQL retrieval systems
* semantic metric exploration
* AI analytics assistants
* local AI workflows

---

# 📄 License

MIT License


