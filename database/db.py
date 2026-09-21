import sqlite3
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parent

DATABASE_PATH = BASE_DIR / "learning_companion.db"


def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn