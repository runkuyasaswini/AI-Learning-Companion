from pathlib import Path
import os

from dotenv import load_dotenv

# --------------------------------------------------
# Load .env from the project root
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_FILE, override=True)

# --------------------------------------------------
# TCS GenAI Configuration
# --------------------------------------------------

GENAI_API_KEY = os.getenv("GENAI_API_KEY")
GENAI_BASE_URL = os.getenv("GENAI_BASE_URL")
GENAI_MODEL = os.getenv("GENAI_MODEL")

# --------------------------------------------------
# RAG Configuration
# --------------------------------------------------

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2",
)

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
TOP_K = int(os.getenv("TOP_K", "6"))
FETCH_K = int(os.getenv("FETCH_K", "20"))

# --------------------------------------------------
# Debug (temporary)
# --------------------------------------------------

if __name__ == "__main__":
    print(f"ENV FILE        : {ENV_FILE}")
    print(f"ENV EXISTS      : {ENV_FILE.exists()}")
    print(f"GENAI_MODEL     : {GENAI_MODEL}")
    print(f"GENAI_BASE_URL  : {GENAI_BASE_URL}")
    print(f"API KEY LOADED  : {'Yes' if GENAI_API_KEY else 'No'}")