from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_FILE = BASE_DIR / "news.db"
FEEDS_FILE = BASE_DIR / "feeds.txt"

LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "newswatch.log"

LOCK_FILE = BASE_DIR / "newswatch.lock"