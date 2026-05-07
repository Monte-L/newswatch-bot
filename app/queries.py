import sqlite3
from typing import Optional

from app.config import DB_FILE

def get_connection():
    """
    Create a SQLite connection configured to return rows as directionary-like objects.
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
        params.extend([
            search_pattern,
            search_pattern,
            search_pattern,
            search_pattern,
        ])
    
    query += """ 
        ORDER BY published DESC 
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

    cursor.execute("SELECT COUNT(*) count FROM articles WHERE fetched_at >= datetime('now', '-3 days')")
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

def get_article_by_id(article_id: str):
    """
    Return a single article by its ID.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
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
    """, (article_id,))

    article = cursor.fetchone()

    connection.close()

    if article is None:
        return None
    
    return dict(article)