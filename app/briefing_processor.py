import logging
from datetime import datetime, timezone

from app.ai import generate_daily_briefing
from app.queries import get_connection


# Janela de tempo dos artigos considerados pelo briefing.
# 24 horas cobre o "dia atual" mesmo perto da virada.
BRIEFING_WINDOW_HOURS = 24

# Limite máximo de artigos enviados ao prompt.
# Evita estourar contexto e mantém o custo previsível.
MAX_ARTICLES_IN_BRIEFING = 60


def get_articles_for_briefing(window_hours=BRIEFING_WINDOW_HOURS, limit=MAX_ARTICLES_IN_BRIEFING):
    """
    Return recent articles with AI summary, ready to feed the briefing.
    """
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        f"""
        SELECT
            id,
            title,
            source,
            category,
            ai_summary
        FROM articles
        WHERE ai_summary IS NOT NULL
          AND ai_summary != ''
          AND fetched_at >= datetime('now', '-{window_hours} hours')
        ORDER BY fetched_at DESC
        LIMIT ?
        """,
        (limit,),
    )

    articles = [dict(row) for row in cursor.fetchall()]

    connection.close()
    return articles


def save_briefing(briefing, articles_considered):
    """
    Persist a generated briefing into the daily_briefings table.
    """
    timestamp = datetime.now(timezone.utc).isoformat()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO daily_briefings (
            generated_at,
            content,
            articles_considered,
            input_tokens,
            output_tokens,
            model_used
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            timestamp,
            briefing["content"],
            articles_considered,
            briefing["input_tokens"],
            briefing["output_tokens"],
            briefing["model"],
        ),
    )

    connection.commit()
    briefing_id = cursor.lastrowid
    connection.close()

    logging.info(f"Briefing saved with id={briefing_id}.")
    return briefing_id


def generate_and_save_briefing():
    """
    Full pipeline: fetch articles, generate briefing, save.
    Returns the briefing id, or None if nothing was generated.
    """
    articles = get_articles_for_briefing()

    if not articles:
        logging.warning(
            "No articles with ai_summary in the last "
            f"{BRIEFING_WINDOW_HOURS} hours. Skipping briefing."
        )
        return None

    logging.info(f"Generating briefing from {len(articles)} articles.")

    briefing = generate_daily_briefing(articles)

    if briefing is None:
        logging.error("Briefing generation failed.")
        return None

    return save_briefing(briefing, articles_considered=len(articles))


if __name__ == "__main__":
    from app.logging_config import setup_logging

    setup_logging()
    generate_and_save_briefing()