from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")

CHROMA_PATH = str(BASE_DIR / "chroma_db")
METADATA_PATH = BASE_DIR / "app" / "metadata"

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")