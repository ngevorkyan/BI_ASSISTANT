from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="RAG SQL BI Assistant")

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "RAG SQL BI Assistant is running",
        "docs": "/docs"
    }