import chromadb
from chromadb.utils import embedding_functions

from app.config.settings import CHROMA_PATH

embedding_function = embedding_functions.DefaultEmbeddingFunction()

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection(
    name="bi_metadata",
    embedding_function=embedding_function
)