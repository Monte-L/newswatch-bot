import logging

from app.collector import process_feeds
from app.database import create_database, finish_collector_run, start_collector_run
from app.logging_config import setup_logging
from app.runtime_lock import collector_lock


def main():
    setup_logging()

    logging.info("=" * 80)
    logging.info("NewsWatch Bot started.")

    try:
        with collector_lock() as lock_acquired:
            if not lock_acquired:
                logging.info(
                    "NewsWatch Bot skipped because another collection is running."
                )
                return

            create_database()
            run_id = start_collector_run()
            try:
                total_new_articles = process_feeds()
                finish_collector_run(
                    run_id,
                    status="success",
                    new_articles=total_new_articles,
                )

                logging.info("NewsWatch Bot finished.")

            except Exception as error:
                finish_collector_run(
                    run_id,
                    status="failed",
                    new_articles=0,
                    error_message=str(error),
                )

                logging.exception("NewsWatch Bot failed.")
                raise
    finally:
        logging.info("=" * 80)


if __name__ == "__main__":
    main()
