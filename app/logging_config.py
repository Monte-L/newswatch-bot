import logging

from app.config import LOG_FILE, LOG_DIR

def setup_logging():
    """
    Configure application logging.
    
    Logs are writen both to the terminal and to a log file.
    """
    LOG_DIR.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler()
        ],
        force=True
    )