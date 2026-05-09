import hashlib
import logging
import sqlite3
from datetime import datetime, timezone

from app.config import DB_FILE


def create_database():
    """
    Create the SQLite database and the articles table if they don't exist.
    Also applies simple migrations for older database versions.
    """
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            link TEXT NOT NULL,
            source TEXT,
            category TEXT,
            summary TEXT,
            image_url TEXT,
            published TEXT,
            fetched_at TEXT NOT NULL
            )
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS collector_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            started_at TEXT NOT NULL,
            finished_at TEXT,
            status TEXT NOT NULL,
            new_articles INTEGER DEFAULT 0,
            duration_seconds REAL,
            error_message TEXT
            )
        """)
    
    migrate_database(cursor)

    connection.commit()
    connection.close()

    logging.info("Database checked successfully.")


def migrate_database(cursor):
    """
    Add new columns to an existing articles table if they do not exist.

    This allows the project to evolve without deleting the existing database.
    """
    cursor.execute("PRAGMA table_info(articles)")
    existing_columns = {column[1] for column in cursor.fetchall()}

    required_columns = {
        "category": "TEXT",
        "summary": "TEXT",
        "image_url": "TEXT",
    }

    for column_name, column_type in required_columns.items():
        if column_name not in existing_columns:
            cursor.execute(
                f"ALTER TABLE articles ADD COLUMN {column_name} {column_type}"
            )
            logging.info(f"Database migration applied: added column '{column_name}'.")

    cursor.execute("""
        UPDATE articles
        SET category = 'General'
        WHERE category IS NULL OR category = ''
    """)

def start_collector_run():
    """
    Register the beginning of a collector execution.
    """
    started_at = datetime.now(timezone.utc).isoformat()
    
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    
    cursor.execute(
        """
        INSERT INTO collector_runs (
            started_at,
            status
        )
        VALUES (?, ?)
        """,
        (started_at, "running"),
    )
    
    connection.commit()
    run_id = cursor.lastrowid
    connection.close()
    
    logging.info(f"Collector run registered: id={run_id}, status=running.")
    return run_id

def finish_collector_run(run_id, status, new_articles=0, error_message=None):
    """
    Update a collector execution with its final status.
    """
    
    finished_at = datetime.now(timezone.utc)
    finished_at_text = finished_at.isoformat()
    
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    
    cursor.execute(
        """
        SELECT started_at
        FROM collector_runs
        WHERE id = ?
        """,
        (run_id,),
    )
    
    row = cursor.fetchone()
    
    if row:
        started_at = datetime.fromisoformat(row[0])
        duration_seconds = (finished_at - started_at).total_seconds()
    else:
        duration_seconds = None
        
    cursor.execute(
        """
        UPDATE collector_runs
        SET
            finished_at = ?,
            status = ?,
            new_articles = ?,
            duration_seconds = ?,
            error_message = ?
        WHERE id = ?
        """,
        (
            finished_at_text,
            status,
            new_articles,
            duration_seconds,
            error_message,
            run_id,
        ),
    )
    
    connection.commit()
    connection.close()
    
    logging.info(
        f"Collector run finished: id={run_id},"
        f"status={status}, new_articles={new_articles},"
    )
    

def generate_article_id(link):
    """
    Generate a unique ID for an article based on its link.
    """
    return hashlib.sha256(link.encode("utf-8")).hexdigest()


def save_article(title, link, source, category, summary, image_url, published):
    """
    Save an article to the database.

    If the article already exists, it will not be inserted again.
    If an existing article has missing metadata, this function tries to enrich it.
    """
    article_id = generate_article_id(link)
    fetched_at = datetime.now(timezone.utc).isoformat()

    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
                INSERT INTO articles (
                    id, 
                    title, 
                    link, 
                    source, 
                    category, 
                    summary,
                    image_url,
                    published,
                    fetched_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                article_id,
                title,
                link,
                source,
                category,
                summary,
                image_url,
                published,
                fetched_at,
            ),
        )
        connection.commit()
        return True

    except sqlite3.IntegrityError:
        cursor.execute(
            """
                UPDATE articles
                SET
                    category = COALESCE(NULLIF(category, ''), ?),
                    summary = COALESCE(NULLIF(summary, ''), ?),
                    image_url = COALESCE(NULLIF(image_url, ''), ?)
                WHERE id = ?
            """,
            (category, summary, image_url, article_id),
        )

        connection.commit()
        return False

    finally:
        connection.close()
