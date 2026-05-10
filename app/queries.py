import sqlite3
from typing import Optional

from app.config import DB_FILE


def get_connection():
    """
    Create a SQLite connection configured to return rows as dictionary-like objects.
    """
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def get_recent_articles(
    limit: int = 50,
    category: Optional[str] = None,
    source: Optional[str] = None,
    search: Optional[str] = None,
):
    """
    Return recent articles from the database.

    Optional filters:
    - category
    - source
    - search
    """

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            id,
            title,
            link,
            source,
            category,
            summary,
            image_url,
            published,
            fetched_at
        FROM articles
        WHERE fetched_at >= datetime('now', '-3 days')
    """

    params = []

    if category:
        query += " AND category = ?"
        params.append(category)

    if source:
        query += " AND source = ?"
        params.append(source)

    if search:
        query += """
            AND (
                title LIKE ?
                OR summary LIKE ?
                OR source LIKE ?
                OR category LIKE ?
            )
        """

        search_pattern = f"%{search}%"
        params.extend(
            [
                search_pattern,
                search_pattern,
                search_pattern,
                search_pattern,
            ]
        )

    query += """ 
        ORDER BY fetched_at DESC 
        LIMIT ?
    """
    params.append(limit)

    cursor.execute(query, params)
    articles = cursor.fetchall()

    connection.close()
    return [dict(article) for article in articles]


def get_categories():
    """
    Return available article categories.
    """
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
            SELECT DISTINCT category
            FROM articles
            WHERE category IS NOT NULL
            AND category != ''
            ORDER BY category
    """)

    categories = [row["category"] for row in cursor.fetchall()]

    connection.close()
    return categories


def get_sources():
    """
    Return available news sources.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
            SELECT DISTINCT source
            FROM articles
            WHERE source IS NOT NULL
            AND source != ''
            ORDER BY source
    """)

    sources = [row["source"] for row in cursor.fetchall()]

    connection.close()
    return sources


def get_article_counts():
    """
    Return basic dashboard metrics for articles collected in the last 3 days.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) count FROM articles WHERE fetched_at >= datetime('now', '-3 days')"
    )
    total_articles = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(DISTINCT source) AS total
        FROM articles
        WHERE source IS NOT NULL
        AND source != ''
        AND fetched_at >= datetime('now', '-3 days')
    """)
    total_sources = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(DISTINCT category) AS total
        FROM articles
        WHERE category IS NOT NULL
        AND category != ''
        AND fetched_at >= datetime('now', '-3 days')
    """)
    total_categories = cursor.fetchone()[0]

    connection.close()
    return {
        "total_articles": total_articles,
        "total_sources": total_sources,
        "total_categories": total_categories,
    }
    
def get_latest_collector_run():
    """
    Return the latest collector execution record.
    """
    
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
        SELECT
            id,
            started_at,
            finished_at,
            status,
            new_articles,
            duration_seconds,
            error_message
        FROM collector_runs
        ORDER BY id DESC
        LIMIT 1    
    """)
    
    collector_run = cursor.fetchone()
    
    connection.close()               
    
    if collector_run is None:
        return None
    
    return dict(collector_run)

WORLD_SOURCES = [
    "BBC News",
    "Business | The Guardian",
    "Deutsche Welle",
    "Deutsche Welle: DW.com - Europe",
    "Environment | The Guardian",
    "France 24 - International breaking news, top stories and headlines",
    "News | Euronews RSS",
    "NYT > Business",
    "NYT > Science",
    "NYT > Technology",
    "NYT > World News",
    "Technology | The Guardian",
    "World news | The Guardian",
    "World | Deutsche Welle",
]


def get_world_brief_articles(limit: int = 5):
    """
    Return recent articles from international sources for the World Brief section.
    """

    connection = get_connection()
    cursor = connection.cursor()

    placeholders = ",".join("?" * len(WORLD_SOURCES))

    cursor.execute(
        f"""
        SELECT
            id,
            title,
            source,
            category,
            published,
            fetched_at
        FROM articles
        WHERE source IN ({placeholders})
        ORDER BY fetched_at DESC
        LIMIT ?
        """,
        (*WORLD_SOURCES, limit),
    )

    articles = cursor.fetchall()

    connection.close()

    return [dict(article) for article in articles]
    

BRAZIL_SOURCES = [
    "Agência Pública",
    "CNN Brasil",
    "Feed Últimas",
    "Folha de S.Paulo - Em cima da hora - Principal",
    "Intercept Brasil",
    "UOL Noticias",
]


def get_brazil_brief_articles(limit: int = 5):
    """
    Return recent Brazilian articles for the Brazil Brief section.
    """

    connection = get_connection()
    cursor = connection.cursor()

    placeholders = ",".join("?" * len(BRAZIL_SOURCES))

    cursor.execute(
        f"""
        SELECT
            id,
            title,
            source,
            category,
            published,
            fetched_at
        FROM articles
        WHERE source IN ({placeholders})
        ORDER BY fetched_at DESC
        LIMIT ?
        """,
        (*BRAZIL_SOURCES, limit),
    )

    articles = cursor.fetchall()

    connection.close()

    return [dict(article) for article in articles]


def get_article_by_id(article_id: str):
    """
    Return a single article by its ID.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            title,
            link,
            source,
            category,
            summary,
            image_url,
            published,
            fetched_at
        FROM articles
        WHERE id = ?
    """,
        (article_id,),
    )

    article = cursor.fetchone()

    connection.close()

    if article is None:
        return None

    return dict(article)
