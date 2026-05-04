import feedparser
import sqlite3
import hashlib
import logging
import re
from datetime import datetime, timezone
from pathlib import Path

from bs4 import BeautifulSoup

DB_FILE = 'news.db'
FEEDS_FILE = 'feeds.txt'
LOG_DIR = Path('logs')
LOG_FILE = LOG_DIR / 'newswatch.log'

CATEGORY_KEYWORDS = {
    "Politics":[
        "governo", "presidente", "congresso", "senado", "câmara",
        "ministro", "ministra", "stf", "supremo", "eleição", "eleições",
        "partido", "deputado", "senador", "prefeito", "governador",
        "política", "planalto"
    ],
    "Economy": [
        "economia", "inflação", "juros", "selic", "dólar", "euro",
        "mercado", "bolsa", "ibovespa", "banco central", "pib",
        "imposto", "receita", "fazenda", "preço", "combustível",
        "salário", "emprego", "desemprego"
    ],
    "Technology": [
        "tecnologia", "inteligência artificial", "ia", "software",
        "hardware", "internet", "celular", "aplicativo", "dados",
        "startup", "chip", "semicondutor", "robô", "automação"
    ],
    "Security": [
        "segurança", "polícia", "crime", "prisão", "operação",
        "investigação", "fraude", "golpe", "ataque", "hacker",
        "cibersegurança", "vazamento", "militar", "defesa"
    ],
    "International": [
        "internacional", "eua", "estados unidos", "china", "rússia",
        "ucrânia", "europa", "oriente médio", "israel", "gaza",
        "onu", "otan", "argentina", "mexico", "méxico"
    ],
    "Health": [
        "saúde", "hospital", "médico", "vacina", "doença",
        "vírus", "covid", "sus", "anvisa", "medicamento"
    ],
    "Sports": [
        "futebol", "esporte", "campeonato", "time", "jogo",
        "seleção", "copa", "atleta", "corrida", "olimpíada"
    ],
    "Environment": [
        "meio ambiente", "clima", "amazônia", "desmatamento",
        "chuva", "seca", "enchente", "queimada", "sustentabilidade",
        "energia renovável"
    ],
}

def setup_logging():
    """
    Configure application logging.

    Logs are written both to the terminal and to a log file.
    """
    LOG_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def load_feeds(file_path):
    """ 
    Load RSS feed URLs from a text file.
    Each line in the file should contain one RSS URL.
    """
    feeds = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                url = line.strip()
                if url:
                    feeds.append(url)

    except FileNotFoundError:
        logging.error(f"Feeds file not found: {file_path}")
    return feeds

def create_database():
    """
    Create the SQLite database and the news table if it doesn't exist.
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
    
    migrate_database(cursor)

    connection.commit()
    connection.close()

    logging.info("Database checked successfully.")
    
def migrate_database(cursor):
    """
    Add new columns to an existing articles table if they don't exist.
    
    This allows the project to evolve without deleting the existing database or losing data.
    """
    
    cursor.execute("PRAGMA table_info(articles)")
    existing_columns = [column[1] for column in cursor.fetchall()]
    
    required_columns = {
        "category": "TEXT",
        "summary": "TEXT",
        "image_url": "TEXT"
    }
    
    for column_name, column_type in required_columns.items():
        if column_name not in existing_columns:
            cursor.execute(f"ALTER TABLE articles ADD COLUMN {column_name} {column_type}")
            logging.info(f"Database migration applied: added column '{column_name}'.")

    cursor.execute(
        """
               UPDATE articles
               SET category = 'General'
               WHERE category IS NULL OR category = ''
        """
    )
               

def generate_article_id(link):
    """
    Generate a unique ID for an article based on its link.
    """
    return hashlib.sha256(link.encode('utf-8')).hexdigest()

def clean_html(raw_html):
    """
    Convert HTML content into clean plain text.
    """
    
    if not raw_html:
        return ""
    
    soup = BeautifulSoup(raw_html, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    return re.sub(r'\s+', ' ', text)  # Replace multiple whitespace with a single space

def limit_text(text, max_length=500):
    """
    Limit long summaries to keep the database and dashboard clean.
    """
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length].rstrip() + "..."

def extract_summary(entry):
    """
    Extract and clean the article summary from an RSS entry.
    """
    summary = ""
    
    if entry.get("summary"):
        summary = entry.get("summary", "")
    elif entry.get("description"):
        summary = entry.get("description", "")
    elif entry.get("content"):
        content = entry.get("content", [])
        if isinstance(content, list) and content:
            summary = content[0].get("value", "")
    clean_summary = clean_html(summary)
    return limit_text(clean_summary)

def looks_like_image_url(url):
    """
    Check whether a URL appears to point to an image file.
    """
    
    if not url:
        return False
    image_extensions = [".jpg", ".jpeg", ".png", ".webp", ".gif"]
    return any(url.lower().split("?")[0].endswith(ext) for ext in image_extensions)

def extract_image_url(entry):
    """
    Try to extract an image URL from common RSS entry fields.
    """
    media_content = entry.get("media_content", [])
    
    for media in media_content:
        image_url = media.get("url")
        
        if image_url:
            return image_url
        
    media_thumbnail = entry.get("media_thumbnail", [])

    for media in media_thumbnail:
        image_url = media.get("url")
        
        if image_url:
            return image_url
       
    enclosures = entry.get("enclosures", [])
       
    for enclosure in enclosures:
           enclosure_type = enclosure.get("type", "")
           image_url = enclosure.get("href") or enclosure.get("url")
           
           if enclosure_type.startswith("image/") and image_url:
               return image_url
    links = entry.get("links", []) 
    
    for link in links:
        link_type = link.get("type", "")
        image_url = link.get("href", "")
        
        if link_type.startswith("image/") and image_url:
            return image_url
        if looks_like_image_url(image_url):
            return image_url
    summary_html = entry.get("summary", "")
    
    if summary_html:
        soup = BeautifulSoup(summary_html, "html.parser")
        image = soup.find("img")
        
        if image and image.get("src"):
            return image.get("src")
    return ""

def classify_article(title, summary, source):
    """
    CLassify an article using simple keyword matching.
    
    This is an initial rule_based classifier.
    Later, this can be improved with better NLP or manual categories per feed. 
    """
    
    text = f"{title} {summary} {source}".lower()
    
    best_category = "General"
    best_score = 0
    
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = 0
        
        for keyword in keywords:
            if keyword in text:
                score += 1
            
        if score > best_score:
            best_score = score
            best_category = category
    return best_category
    
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
    
    # Check if the article already exists
    try:
        cursor.execute("""
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
        """, (
            article_id, 
            title, 
            link, 
            source, 
            category, 
            summary, 
            image_url, 
            published, 
            fetched_at
        ))
        
        connection.commit()
        return True  # Article was saved
    
    
    except sqlite3.IntegrityError:
        cursor.execute("""
            UPDATE articles
            SET
                category = COALESCE(NULLIF(category, ''), ?),
                summary = COALESCE(NULLIF(summary, ''), ?),
                image_url = COALESCE(NULLIF(image_url, ''), ?)
                WHERE id = ?
        """, (
            category, 
            summary, 
            image_url, 
            article_id
        ))
        
        connection.commit()
        return False  # Article already existed, but may have been updated with new metadata
    finally:
        connection.close()

def fetch_feed(feed_url):
    """
    Fetch and parse a single RSS feed.
    """
    feed = feedparser.parse(feed_url)

    if feed.bozo:
        logging.warning(f"Possible feed parsing issue: {feed_url}")
    return feed

def process_feeds():
    """
    Read all feeds, extract articles, and save new articles to the database.
    """
    feeds = load_feeds(FEEDS_FILE)

    logging.info(f"Loaded {len(feeds)} RSS feeds.")
    
    total_new_articles = 0

    for feed_url in feeds:
        try:

            feed = fetch_feed(feed_url)
            source_name = feed.feed.get("title", "Unknown Source")

            logging.info(f"Processing source: {source_name}")
            logging.info(f"Feed URL: {feed_url}")
            
            new_articles_from_source = 0

            for entry in feed.entries:
                title = entry.get("title", "").strip()
                link = entry.get("link", "").strip()
                published = entry.get("published", "")

                if not title or not link:
                    continue  # Skip articles without a title or link
                
                summary = extract_summary(entry)
                image_url = extract_image_url(entry)
                category = classify_article(title, summary, source_name)
                
                was_saved = save_article(
                    title=title, 
                    link=link, 
                    source=source_name, 
                    published=published, 
                    category=category, 
                    summary=summary, 
                    image_url=image_url
                )
                if was_saved:
                    new_articles_from_source += 1
                    total_new_articles += 1
                    
                    logging.info(f"New article saved: {title}")
                    logging.info(f"Category: {category}")

            logging.info(
                f"New articles from source '{source_name}': {new_articles_from_source}"
            )

        except Exception as error:
            logging.exception(f"Error processing feed: '{feed_url}'")
    logging.info(f"Total new articles saved: {total_new_articles}")

    return total_new_articles

def main():
    setup_logging()

    logging.info("="*80)
    logging.info("NewsWatch Bot started.")

    create_database()
    process_feeds()

    logging.info("NewsWatch Bot finished.")
    logging.info("="*80)
    
if __name__ == "__main__":    
    main()