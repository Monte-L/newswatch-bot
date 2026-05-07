# NewsWatch Bot

NewsWatch Bot is a Linux-based Python project designed to collect, store, classify, and organize news from RSS feeds.

The project started as a command-line RSS collector and is being gradually expanded into a local news aggregation system with structured data, logging, categorization, and a future FastAPI + HTML dashboard.

---

## Project Goal

The goal of this project is to build a local automated news aggregation system using:

- Python
- RSS feeds
- SQLite
- Linux automation
- Logging
- Modular Python structure
- Future FastAPI + HTML dashboard

The final objective is to centralize relevant news from multiple sources into a single local database, allowing articles to be filtered, categorized, reviewed, and updated from a local web interface.

---

## Current Status

Current project phase:

```text
Phase 5 — Modular Python structure
```

The collector is working and currently supports:

- RSS feed loading
- Article extraction
- SQLite storage
- Duplicate prevention
- Logging
- Category classification
- Summary extraction
- Image URL extraction when available
- Modular Python organization

The next planned phase is:

```text
Phase 6 — FastAPI + HTML dashboard
```

---

## Current Features

- Load RSS feed URLs from a text file
- Parse RSS feeds using Python
- Extract article title, link, source, and published date
- Store articles in a local SQLite database
- Prevent duplicate articles using a SHA-256 hash based on the article link
- Generate execution logs
- Extract article summaries from RSS feeds when available
- Clean HTML from RSS summaries
- Extract image URLs from RSS media fields when available
- Classify articles using rule-based keyword matching
- Organize the code into Python modules

---

## Planned Features

- FastAPI backend
- HTML dashboard
- Reload button to fetch news manually from the dashboard
- Automatic scheduled collection every 5 minutes
- Dashboard filters by source and category
- Local article preview page
- Improved category classification
- Better image extraction
- Optional summaries using AI in a future phase
- Telegram, Discord, or email notifications in a future phase
- Daily reports
- n8n automation integration in a later phase
- Metrics about collected articles, sources, categories, and bot execution status

---

## Architecture

Current architecture:

```text
RSS Feeds
   ↓
Python Collector
   ↓
Metadata Extraction
   ↓
Category Classification
   ↓
SQLite Database
   ↓
Log Files
```

Future architecture:

```text
RSS Feeds
   ↓
Python Collector
   ↓
SQLite Database
   ↓
FastAPI Backend
   ↓
HTML Dashboard
   ↓
User filters, reads, refreshes, and monitors news
```

---

## Project Structure

Current project structure:

```text
newswatch-bot/
├── app/
│   ├── __init__.py
│   ├── classifier.py
│   ├── collector.py
│   ├── config.py
│   ├── database.py
│   ├── logging_config.py
│   └── metadata.py
├── feeds.txt
├── logs/
│   └── newswatch.log
├── news_bot.py
├── news.db
├── README.md
└── requirements.txt
```

---

## Module Responsibilities

| File | Responsibility |
|---|---|
| `app/config.py` | Stores project configuration such as database path, feeds file path, and log file path |
| `app/logging_config.py` | Configures terminal and file logging |
| `app/database.py` | Handles SQLite database creation, migrations, article IDs, and article persistence |
| `app/classifier.py` | Classifies articles using rule-based keyword matching |
| `app/metadata.py` | Extracts summaries, cleans HTML, limits text length, and extracts image URLs |
| `app/collector.py` | Loads RSS feeds, parses articles, extracts metadata, classifies articles, and saves them |
| `news_bot.py` | Main entry point used to run the collector |

---

## Requirements

This project uses Python and a local virtual environment.

Main dependencies:

- `feedparser`
- `beautifulsoup4`

Future dashboard dependencies:

- `fastapi`
- `uvicorn`
- `jinja2`

---

## Setup

Clone or enter the project directory:

```bash
cd ~/projects/newswatch-bot
```

Create a Python virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Collector

Activate the virtual environment:

```bash
source venv/bin/activate
```

Run the bot:

```bash
python news_bot.py
```

The bot will:

1. Load RSS feeds from `feeds.txt`
2. Parse the feeds
3. Extract article metadata
4. Classify articles
5. Save new articles to SQLite
6. Skip duplicate articles
7. Write execution logs

---

## RSS Feeds

RSS feed URLs are stored in:

```text
feeds.txt
```

Example:

```text
https://feeds.bbci.co.uk/news/world/rss.xml
https://www.theguardian.com/world/rss
https://rss.nytimes.com/services/xml/rss/nyt/World.xml
```

To add or remove sources, edit `feeds.txt`.

The collector does not need code changes when RSS sources are updated.

---

## Database

The project uses SQLite as a local database.

Database file:

```text
news.db
```

Main table:

```text
articles
```

---

## Database Schema

```sql
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
);
```

---

## Article Fields

| Column | Description |
|---|---|
| `id` | Unique article identifier generated from the article link |
| `title` | Article title |
| `link` | Original article URL |
| `source` | RSS feed source name |
| `category` | Article category generated by keyword matching |
| `summary` | Short article summary extracted from the RSS feed when available |
| `image_url` | Image URL extracted from RSS media fields when available |
| `published` | Publication date provided by the RSS feed |
| `fetched_at` | UTC timestamp when the bot collected the article |

---

## Duplicate Prevention

The bot prevents duplicate articles by generating a SHA-256 hash from the article link.

Example:

```python
hashlib.sha256(link.encode("utf-8")).hexdigest()
```

This generated hash is stored as the article `id`.

Because `id` is the primary key, SQLite prevents the same article from being inserted more than once.

---

## Categories

The project currently uses rule-based classification.

Current categories:

- Politics
- Economy
- Technology
- Security
- International
- Health
- Sports
- Environment
- General

The classifier checks keywords in:

```text
title + summary + source
```

Example:

```text
"dollar", "inflation", "central bank" → Economy
"government", "congress", "president" → Politics
"police", "crime", "investigation" → Security
```

This approach is simple, transparent, and easy to improve later.

---

## Metadata Extraction

The collector extracts additional metadata from RSS entries.

Currently supported metadata:

- Summary
- Cleaned plain-text summary
- Image URL when available
- Category

The summary extraction checks common RSS fields such as:

```text
summary
description
content
```

The image extraction checks common RSS media fields such as:

```text
media_content
media_thumbnail
enclosures
links
summary HTML images
```

Not every RSS feed provides images. If no image is available, the `image_url` field remains empty.

---

## Logging

The project uses Python's built-in `logging` module.

Logs are written to:

```text
logs/newswatch.log
```

The log file records:

- When the bot starts
- When the database is checked
- How many feeds were loaded
- Which sources were processed
- Feed URLs being processed
- New articles saved
- Article categories
- Feed parsing warnings
- Processing errors
- Total number of new articles saved
- When the bot finishes

Useful log commands:

```bash
tail logs/newswatch.log
```

```bash
tail -n 40 logs/newswatch.log
```

```bash
tail -f logs/newswatch.log
```

To stop `tail -f`:

```text
CTRL + C
```

---

## Useful SQLite Commands

Open the database:

```bash
sqlite3 news.db
```

Show tables:

```sql
.tables
```

Show the articles table schema:

```sql
.schema articles
```

Count all stored articles:

```sql
SELECT COUNT(*) FROM articles;
```

Show recent articles:

```sql
SELECT title, source, category, published
FROM articles
ORDER BY fetched_at DESC
LIMIT 10;
```

Count articles by source:

```sql
SELECT source, COUNT(*)
FROM articles
GROUP BY source
ORDER BY COUNT(*) DESC;
```

Count articles by category:

```sql
SELECT category, COUNT(*)
FROM articles
GROUP BY category
ORDER BY COUNT(*) DESC;
```

Show articles that have images:

```sql
SELECT title, image_url
FROM articles
WHERE image_url IS NOT NULL
AND image_url != ''
LIMIT 10;
```

Exit SQLite:

```sql
.exit
```

---

## Development Commands

Activate the virtual environment:

```bash
source venv/bin/activate
```

Run the collector:

```bash
python news_bot.py
```

Check Python syntax:

```bash
python -m py_compile news_bot.py app/*.py
```

Read recent logs:

```bash
tail -n 40 logs/newswatch.log
```

---

## Git Ignore Recommendation

The following files and folders should not be committed to GitHub:

```gitignore
venv/
__pycache__/
*.pyc
logs/*.log
news.db
```

Reason:

- `venv/` is local environment data
- `__pycache__/` is Python cache
- `logs/*.log` is runtime output
- `news.db` is a local database file

---

## Roadmap

### Phase 1 — RSS Reader

- Load RSS feeds
- Parse articles
- Print articles in the terminal

### Phase 2 — SQLite Storage

- Create SQLite database
- Store articles
- Prevent duplicates

### Phase 3 — Logging

- Add professional logging
- Write logs to file
- Track execution status

### Phase 4 — Article Metadata

- Add category field
- Extract summaries
- Extract image URLs
- Improve article data quality

### Phase 5 — Modular Structure

- Split code into modules
- Separate collector, database, metadata, classifier, logging, and config
- Prepare project for web dashboard

### Phase 6 — FastAPI + HTML Dashboard

Planned features:

- Local dashboard at `http://127.0.0.1:8000`
- Display articles from SQLite
- Show title, source, category, summary, image, and original link
- Filter by source and category
- Add reload button to fetch news manually

### Phase 7 — Scheduling

Planned features:

- Run collector automatically every 5 minutes
- Use Linux cron or internal scheduler
- Track last execution time

### Phase 8 — Automation and Notifications

Planned features:

- Telegram alerts
- Discord alerts
- Email reports
- Daily summaries
- n8n automation integration
- Google Sheets export

---

## Ethical and Legal Notes

This project prioritizes RSS feeds and public metadata.

The collector should avoid:

- Copying full articles without permission
- Bypassing paywalls
- Ignoring robots.txt when scraping
- Sending excessive requests to websites
- Republishing restricted images or copyrighted content without permission

The recommended approach is to store:

- Title
- Source
- Link
- Published date
- Short RSS summary when available
- Image URL when provided by the feed
- Original source link

Full article extraction should only be added for sources that clearly allow it.

---

## Project Purpose

This project is intended for:

- Python practice
- Linux automation practice
- SQLite practice
- Logging practice
- Infrastructure portfolio development
- Future FastAPI dashboard development

NewsWatch Bot is not just a script. It is being developed as a small local news aggregation system that demonstrates automation, data persistence, modular design, and future web application integration. 

## Manual Reload from Dashboard

The dashboard includes a manual reload button.

When clicked, the FastAPI backend calls the RSS collector, fetches new articles, saves them to SQLite, and redirects back to the dashboard.

Route:

```text
POST /reload
After the reload finishes, the dashboard displays how many new articles were saved.
```
