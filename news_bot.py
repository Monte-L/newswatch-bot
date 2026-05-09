import logging

from app.collector import process_feeds
from app.database import create_database
from app.logging_config import setup_logging
from app.runtime_lock import collector_lock

def main():
    setup_logging()
    
    logging.info("=" * 80)
    logging.info("NewsWatch Bot started.")
    
    try:
        with collector_lock() as lock_acquired:
            if not lock_acquired:
                logging.info("NewsWatch Bot skipped because another collection is running.")
                return
             
            create_database()
            process_feeds()
        
            logging.info("NewsWatch Bot finished.")
    except Exception:
        logging.exception("NewsWatch Bot failed.")
        raise
    
    finally:
        logging.info("=" * 80)
    
if __name__ == "__main__":
    main()