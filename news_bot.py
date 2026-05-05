import logging

from app.collector import process_feeds
from app.database import create_database
from app.logging_config import setup_logging

def main():
    setup_logging()
    
    logging.info("=" * 80)
    logging.info("NewsWatch Bot started.")
    
    create_database()
    process_feeds()
    
    logging.info("NewsWatch Bot finished.")
    logging.info("=" * 80)
    
if __name__ == "__main__":
    main()