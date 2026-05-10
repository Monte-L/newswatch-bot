import logging
from datetime import datetime, timezone

from app.ai import RELEVANT_CATEGORIES, generate_article_summary, is_eligible_for_ai
from app.queries import get_connection


# Maximum number of articles to process per run.
# Acts as a safety limit to prevent runaway API usage.
MAX_ARTICLES_PER_RUN = 30


def get_pending_articles(limit):
    """
    Return articles that need an AI summary.

    Conditions:
    - Category is in RELEVANT_CATEGORIES
    - ai_summary is empty (not yet processed)
    - summary (RSS source text) exists, otherwise there is nothing to summarize
    """
    connection = get_connection()
    cursor = connection.cursor()

    placeholders = ",".join("?" * len(RELEVANT_CATEGORIES))

    cursor.execute(
        f"""
        SELECT id, title, summary, category, source
        FROM articles
        WHERE category IN ({placeholders})
          AND (ai_summary IS NULL OR ai_summary = '')
          AND summary IS NOT NULL
          AND summary != ''
        ORDER BY fetched_at DESC
        LIMIT ?
        """,
        (*RELEVANT_CATEGORIES, limit),
    )

    articles = [dict(row) for row in cursor.fetchall()]

    connection.close()
    return articles


def save_ai_summary(article_id, ai_summary):
    """
    Persist the generated summary back into the article row.
    """
    timestamp = datetime.now(timezone.utc).isoformat()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE articles
        SET ai_summary = ?,
            ai_summary_at = ?
        WHERE id = ?
        """,
        (ai_summary, timestamp, article_id),
    )

    connection.commit()
    connection.close()


def process_pending_articles(limit=MAX_ARTICLES_PER_RUN):
    """
    Process articles awaiting an AI summary.

    Returns a tuple (processed, failed).
    """
    articles = get_pending_articles(limit)

    if not articles:
        logging.info("No articles pending AI summary.")
        return 0, 0

    logging.info(f"Found {len(articles)} articles pending AI summary.")

    processed = 0
    failed = 0

    skipped = 0

    for article in articles:
        if not is_eligible_for_ai(article["category"], article["source"]):
            logging.info(
                f"Skipping (source-filtered): {article['title'][:80]} "
                f"({article['category']} from {article['source']})"
            )
            skipped += 1
            continue

        logging.info(
            f"Processing article: {article['title'][:80]} "
            f"({article['category']})"
        )

        ai_summary = generate_article_summary(
            article["title"],
            article["summary"],
            article["category"],
        )

        if ai_summary:
            save_ai_summary(article["id"], ai_summary)
            processed += 1
        else:
            failed += 1

    logging.info(
        f"AI processing complete. "
        f"Processed: {processed}, Failed: {failed}, Skipped: {skipped}."
    )

    return processed, failed


if __name__ == "__main__":
    from app.logging_config import setup_logging

    setup_logging()
    process_pending_articles()