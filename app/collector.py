import logging

import feedparser

from app.classifier import classify_article
from app.config import FEEDS_FILE
from app.database import save_article
from app.metadata import extract_image_url, extract_summary


def load_feeds(file_path):
    """
    Load RSS feed URLs from a text file.
    Each line in the file should contain one RSS URL.
    """

    feeds = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                url = line.strip()

                if url:
                    feeds.append(url)
    except Exception as error:
        logging.error(f"Feeds file not found: '{file_path}': {error}")

    return feeds


def fetch_feed(feed_url):
    """
    Fetch articles from a single RSS feed.
    """
    feed = feedparser.parse(feed_url)

    if feed.bozo:
        logging.warning(f"Possible feed parsing issue: {feed_url}")

    return feed


def process_feeds():
    """
    Read all feeds, extract articles, classify them, and save new articles.
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
                title = str(entry.get("title") or "").strip()
                link = str(entry.get("link") or "").strip()
                published = str(entry.get("published") or "").strip()

                if not title or not link:
                    continue

                summary = extract_summary(entry)
                image_url = extract_image_url(entry)

                category = classify_article(title, summary, source_name)

                was_saved = save_article(
                    title=title,
                    link=link,
                    source=source_name,
                    category=category,
                    summary=summary,
                    image_url=image_url,
                    published=published,
                )

                if was_saved:
                    new_articles_from_source += 1
                    total_new_articles += 1

                    logging.info(f"New article saved: {title}")
                    logging.info(f"Category: {category}")

            logging.info(
                f"New articles from source '{source_name}': "
                f"{new_articles_from_source}"
            )

        except Exception:
            logging.exception(f"Error processing feed: '{feed_url}'")

    logging.info(f"Total new articles saved: {total_new_articles}")

    return total_new_articles
