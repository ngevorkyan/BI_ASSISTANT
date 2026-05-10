from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="RAG BI Assistant")

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "BI Assistant is running",
        "docs": "/docs"
    }