# NewsWatch Bot

NewsWatch Bot is a Linux-based Python project designed to collect, store, classify, and organize news from RSS feeds.

The project started as a command-line RSS collector and is gradually evolving into a local news aggregation system with structured data, logging, categorization, a FastAPI + HTML dashboard, and future support for search, scheduled collection, JavaScript interactions, AI summaries, and production deployment.

---

## Project Goal

The goal of this project is to build a local automated news aggregation system using:

- Python
- RSS feeds
- SQLite
- Linux automation
- Logging
- Modular Python structure
- FastAPI
- HTML/CSS
- Future JavaScript improvements
- Future AI-assisted summaries
- Future production deployment with PostgreSQL

The final objective is to centralize relevant news from multiple sources into a single local database, allowing articles to be filtered, categorized, reviewed, refreshed, and eventually summarized from a local web interface.

---

## Current Status

Current completed phase:

```text
Phase 6B — FastAPI Dashboard with Manual Reload Button
```

The dashboard is currently working with:

- Article listing
- Category filters
- Source filters
- Manual reload button
- Reload completion message
- SQLite integration
- Article cards with source, category, summary, image, and original link

Next planned phase:

```text
Phase 6C — Article Detail Page / Local Preview Page
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
- Display articles in a FastAPI + HTML dashboard
- Filter articles by category
- Filter articles by source
- Show only recently collected articles in the dashboard
- Manually reload news from the dashboard

---

## Planned Features

- Article detail / local preview page
- Search by keyword
- JavaScript-based reload without full page refresh
- JavaScript-based dynamic filtering
- Automatic scheduled collection every 5 minutes
- Improved category classification
- Better image extraction
- AI-generated article summaries in a future phase
- Telegram, Discord, or email notifications in a future phase
- Daily reports
- n8n automation integration in a later phase
- Metrics about collected articles, sources, categories, and bot execution status
- PostgreSQL migration when preparing for production deployment
- Public deployment with domain, HTTPS, and reverse proxy

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
FastAPI Backend
   ↓
HTML/CSS Dashboard
```

Future production-oriented architecture:

```text
RSS Feeds
   ↓
Background Collector
   ↓
PostgreSQL Database
   ↓
FastAPI Backend
   ↓
HTML/CSS/JavaScript Frontend
   ↓
Nginx or Caddy Reverse Proxy
   ↓
Public Domain + HTTPS
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
│   ├── metadata.py
│   ├── queries.py
│   └── web.py
├── feeds.txt
├── logs/
│   └── newswatch.log
├── static/
│   └── style.css
├── templates/
│   └── index.html
├── news_bot.py
├── news.db
├── README.md
└── requirements.txt
```

Future structure after the article detail page:

```text
newswatch-bot/
├── app/
│   ├── __init__.py
│   ├── classifier.py
│   ├── collector.py
│   ├── config.py
│   ├── database.py
│   ├── logging_config.py
│   ├── metadata.py
│   ├── queries.py
│   └── web.py
├── feeds.txt
├── logs/
│   └── newswatch.log
├── static/
│   └── style.css
├── templates/
│   ├── index.html
│   └── article_detail.html
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
| `app/queries.py` | Reads articles, categories, sources, and dashboard metrics from SQLite |
| `app/web.py` | Defines the FastAPI application and web routes |
| `news_bot.py` | Main command-line entry point used to run the collector |
| `templates/index.html` | Main dashboard HTML template |
| `static/style.css` | Dashboard styling |

---

## Requirements

This project uses Python and a local virtual environment.

Main dependencies:

- `feedparser`
- `beautifulsoup4`
- `fastapi`
- `uvicorn`
- `jinja2`

---

## Setup

Enter the project directory:

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

If dependencies need to be installed manually:

```bash
python -m pip install feedparser beautifulsoup4 fastapi uvicorn jinja2
python -m pip freeze > requirements.txt
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

## Running the Web Dashboard

Activate the virtual environment:

```bash
source venv/bin/activate
```

Run the FastAPI dashboard:

```bash
uvicorn app.web:app --reload
```

Open the dashboard in the browser:

```text
http://127.0.0.1:8000
```

The dashboard displays:

- Total articles
- Total sources
- Total categories
- Article cards
- Category filter
- Source filter
- Manual reload button
- Reload completion message
- Article source links

---

## Manual Reload from Dashboard

The dashboard includes a manual reload button.

When clicked, the FastAPI backend calls the RSS collector, fetches new articles, saves them to SQLite, and redirects back to the dashboard.

Route:

```text
POST /reload
```

After the reload finishes, the dashboard displays how many new articles were saved.

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

The project currently uses SQLite as a local database.

Database file:

```text
news.db
```

Main table:

```text
articles
```

SQLite is being used during the local prototype stage because it is simple, lightweight, and suitable for development.

PostgreSQL may be introduced later when the project is prepared for production deployment, public access, scheduled background collection, heavier usage, and AI-generated summaries.

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

## Dashboard Filtering

The dashboard supports filtering by:

- Category
- Source

The dashboard currently shows only recently collected articles.

The current implementation filters articles using the `fetched_at` field, which represents when the bot collected the article.

This is more stable than filtering by the RSS `published` field because RSS feeds may provide publication dates in different formats.

---

## Article Detail Page

Planned route:

```text
GET /articles/{article_id}
```

The future local article preview page will display:

- Article title
- Source
- Category
- Published date
- Image when available
- RSS summary when available
- Original article link

This page will use metadata stored in SQLite and will not copy the full article content from the original source.

Future AI summaries may be added to this page.

---

## Future AI Summary Layer

A future phase may add AI-generated summaries to article preview pages.

The AI summary should be based on available RSS metadata and/or permitted source content.

Potential future fields:

```sql
ai_summary TEXT
ai_key_points TEXT
ai_generated_at TEXT
ai_model TEXT
content_policy TEXT
```

The goal is to provide a useful interpretation layer without copying full articles or replacing the original source.

The original source link should always remain visible.

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

Run the dashboard:

```bash
uvicorn app.web:app --reload
```

Check Python syntax:

```bash
python -m py_compile news_bot.py app/*.py
```

Read recent logs:

```bash
tail -n 40 logs/newswatch.log
```

Check Git status:

```bash
git status
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

Status:

```text
Completed
```

---

### Phase 2 — SQLite Storage

- Create SQLite database
- Store articles
- Prevent duplicates

Status:

```text
Completed
```

---

### Phase 3 — Logging

- Add professional logging
- Write logs to file
- Track execution status

Status:

```text
Completed
```

---

### Phase 4 — Article Metadata

- Add category field
- Extract summaries
- Extract image URLs
- Improve article data quality

Status:

```text
Completed
```

---

### Phase 5 — Modular Structure

- Split code into modules
- Separate collector, database, metadata, classifier, logging, and config
- Prepare project for web dashboard

Status:

```text
Completed
```

---

### Phase 6A — FastAPI + HTML Dashboard

- Create FastAPI web app
- Add HTML template
- Add CSS styling
- Display articles from SQLite
- Add category and source filters

Status:

```text
Completed
```

---

### Phase 6B — Manual Reload Button

- Add reload button to dashboard
- Call collector from FastAPI
- Show reload completion message
- Display number of new articles saved

Status:

```text
Completed
```

---

### Phase 6C — Article Detail Page

Planned features:

- Add local article preview page
- Route: `/articles/{article_id}`
- Show title, source, category, image, summary, and original link
- Add `Read preview` link to article cards

Status:

```text
Next phase
```

---

### Phase 6D — Search

Planned features:

- Search articles by keyword
- Search title and summary
- Combine search with category and source filters

Status:

```text
Planned
```

---

### Phase 6E — JavaScript Improvements

Planned features:

- Reload news without full page refresh
- Show loading state
- Dynamic messages
- Improve filter interactions

Status:

```text
Planned
```

---

### Phase 7 — Scheduling

Planned features:

- Run collector automatically every 5 minutes
- Use Linux cron or internal scheduler
- Track last execution time

Status:

```text
Planned
```

---

### Phase 8 — Automation and Notifications

Planned features:

- Telegram alerts
- Discord alerts
- Email reports
- Daily summaries
- n8n automation integration
- Google Sheets export

Status:

```text
Planned
```

---

### Phase 9 — AI Summaries

Planned features:

- Generate AI summaries for article preview pages
- Extract key points
- Explain why an article matters
- Store generated summaries in SQLite or PostgreSQL
- Avoid copying full articles without permission

Status:

```text
Planned
```

---

### Phase 10 — Production Planning

Planned features:

- Evaluate PostgreSQL migration
- Prepare deployment environment
- Configure reverse proxy
- Add HTTPS
- Use domain name
- Add backups
- Add monitoring

Status:

```text
Planned
```

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

AI summaries should be used as a transformative interpretation layer and should not replace the original article.

The original source link should always remain visible.

---

## Project Purpose

This project is intended for:

- Python practice
- Linux automation practice
- SQLite practice
- FastAPI practice
- HTML/CSS practice
- Future JavaScript practice
- Logging practice
- Infrastructure portfolio development
- Future deployment practice

NewsWatch Bot is not just a script. It is being developed as a small local news aggregation system that demonstrates automation, data persistence, modular design, dashboard development, and future web application deployment.