# NewsWatch Bot

NewsWatch Bot is a Linux-based Python project designed to collect, store, classify, search, and organize news from RSS feeds.

The project started as a command-line RSS collector and is gradually evolving into a centralized news platform with structured data, automatic background collection, logging, categorization, a FastAPI + HTML/CSS/JavaScript interface, article preview pages, keyword search, reload API routes, collector execution history, and future support for AI summaries, topic grouping, source comparison, automation, and production deployment.

The long-term goal is not only to provide a technical dashboard, but to build a public-facing news platform that helps users understand what is happening across multiple sources without manually opening many different news websites.

---

## Project Goal

The goal of this project is to build an automated news aggregation and interpretation platform using:

- Python
- RSS feeds
- SQLite
- Linux automation
- systemd timers
- Logging
- Modular Python structure
- FastAPI
- HTML/CSS
- JavaScript
- Future AI-assisted summaries
- Future topic-based grouping
- Future source comparison
- Future automation and notifications
- Future production deployment with PostgreSQL

The final objective is to centralize relevant news from multiple sources into a single platform, allowing articles to be collected, filtered, searched, categorized, reviewed, refreshed, interpreted, and eventually summarized with AI.

The platform should help users quickly understand:

- What happened
- Why it matters
- Which sources are covering it
- What the key points are
- How different sources frame the same topic
- Where to read the original article

The original source link should always remain visible.

---

## Current Status

Current completed phase:

```text
Phase 7D — Automatic background collection and collector run history
```

The project is currently working with:

- Article listing
- Category filters
- Source filters
- Keyword search
- Manual reload button
- JavaScript-based reload using `fetch()`
- API route `POST /api/reload` returning JSON
- Loading state on the reload button
- Dynamic reload completion message
- Automatic dashboard refresh after reload
- Local article preview pages
- SQLite integration
- Article cards with source, category, summary, image, preview link, and original link
- Article ordering based on `fetched_at DESC`
- Automatic background collection using `systemd timer`
- A `systemd` one-shot service for collector execution
- Collector lock file to prevent overlapping runs
- Collector execution history stored in SQLite
- Collector run status tracking with `running`, `success`, `failed`, and `skipped` statuses

Next planned phase:

```text
Phase 8 — Public news platform interface direction
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
- Limit long RSS summaries for dashboard readability
- Extract image URLs from RSS media fields when available
- Classify articles using rule-based keyword matching
- Organize the code into Python modules
- Display articles in a FastAPI + HTML dashboard
- Filter articles by category
- Filter articles by source
- Search articles by keyword
- Show only recently collected articles in the dashboard
- Order dashboard articles by `fetched_at DESC`
- Manually reload news from the dashboard
- Provide a JSON API route for reloading news
- Use JavaScript to intercept the reload form submit event
- Reload news using `fetch()`
- Show a loading state on the reload button
- Disable the reload button while collection is running
- Show dynamic reload success or error messages in the dashboard
- Automatically refresh the dashboard after a successful reload
- Open local article preview pages
- Open original source articles
- Run the RSS collector automatically using a `systemd timer`
- Execute the collector through a `systemd` one-shot service
- Prevent overlapping collector executions using a lock file
- Register collector execution history in SQLite
- Track collector run status as `running`, `success`, `failed`, or `skipped`
- Track collector run duration in seconds
- Track how many new articles were saved by each collector run
- Track collector errors when a run fails
- Read the latest collector execution record from SQLite

---

## Planned Features

- Create a separate public reading interface for the news platform
- Keep technical collector/status information in an internal admin area
- Add topic-based news grouping
- Add AI-generated summaries and context
- Add AI-generated key points and “why this matters” sections
- Compare coverage from multiple sources when possible
- Add source reliability and attribution notes
- Add JSON API endpoints for public article/topic listing
- Improve JavaScript interactions further
- Update article lists dynamically without full page reload
- Improve category classification
- Improve RSS image extraction
- Normalize RSS published dates
- Add dashboard placeholder when no article image is available
- Add Telegram, Discord, or email notifications
- Add daily reports
- Add n8n automation integration
- Add Google Sheets export
- Add metrics about collected articles, sources, categories, and bot execution status
- Migrate to PostgreSQL for production deployment
- Deploy publicly with domain, HTTPS, and reverse proxy

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
Jinja2 HTML Templates
   ↓
HTML/CSS/JavaScript Interface
```

Automatic collection architecture:

```text
systemd timer
   ↓
newswatch-collector.service
   ↓
news_bot.py
   ↓
Collector lock
   ↓
RSS Collector
   ↓
SQLite Database
   ↓
collector_runs execution history
```

Current reload flow:

```text
User clicks Reload News
   ↓
JavaScript intercepts the form submit event
   ↓
event.preventDefault() prevents the traditional page reload
   ↓
fetch() sends a POST request to /api/reload
   ↓
FastAPI runs the RSS collector
   ↓
The API returns a JSON response
   ↓
The interface shows a loading state and completion message
   ↓
The page refreshes automatically to display the updated article list
```

Future product-oriented architecture:

```text
RSS Feeds / Approved Sources
   ↓
Scheduled Background Collector
   ↓
PostgreSQL Database
   ↓
Article Classification
   ↓
Topic Grouping
   ↓
AI Summary and Interpretation Layer
   ↓
FastAPI Backend
   ↓
Public News Platform Interface
   ↓
Nginx or Caddy Reverse Proxy
   ↓
Public Domain + HTTPS
```

The collector runs independently from the FastAPI web application. This keeps background collection separate from the public web interface and prepares the project for a more production-oriented deployment model.

---

## Product Direction

The current interface should be understood as an initial prototype and internal/admin-style interface.

The long-term product direction is to evolve NewsWatch Bot into a public-facing centralized news platform.

The future platform should provide:

- Public reading pages
- Search and navigation by category/topic
- Latest news sections
- Topic-based article grouping
- AI-generated summaries
- AI-generated context
- AI-generated key points
- “Why this matters” explanations
- Source comparison when multiple sources cover the same topic
- Links and attribution to original sources
- A separate internal/admin/status area for monitoring collectors and system health

The project should avoid copying full articles without permission. The goal is to organize, summarize, contextualize, and interpret news while preserving source attribution and links to the original articles.

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
│   ├── runtime_lock.py
│   └── web.py
├── feeds.txt
├── logs/
│   └── newswatch.log
├── static/
│   ├── app.js
│   └── style.css
├── templates/
│   ├── index.html
│   └── article_detail.html
├── news_bot.py
├── news.db
├── README.md
└── requirements.txt
```

Runtime files such as `news.db`, `logs/newswatch.log`, and `newswatch.lock` are local development artifacts and should not be committed to GitHub.

---

## Module Responsibilities

| File | Responsibility |
|---|---|
| `app/config.py` | Stores project configuration such as database path, feeds file path, log file path, and lock file path |
| `app/logging_config.py` | Configures terminal and file logging |
| `app/database.py` | Handles SQLite database creation, migrations, article IDs, article persistence, and collector run history |
| `app/classifier.py` | Classifies articles using rule-based keyword matching |
| `app/metadata.py` | Extracts summaries, cleans HTML, limits text length, and extracts image URLs |
| `app/collector.py` | Loads RSS feeds, parses articles, extracts metadata, classifies articles, and saves them |
| `app/queries.py` | Reads articles, categories, sources, article details, dashboard metrics, and collector run status from SQLite |
| `app/runtime_lock.py` | Provides a lock file mechanism to prevent overlapping collector executions |
| `app/web.py` | Defines the FastAPI application, dashboard routes, article routes, reload routes, and API routes |
| `news_bot.py` | Main command-line entry point used to run the collector manually or through systemd |
| `templates/index.html` | Main HTML template for the current interface |
| `templates/article_detail.html` | Local article preview page template |
| `static/style.css` | Interface and article page styling |
| `static/app.js` | Handles JavaScript behavior, reload API calls, loading state, dynamic messages, and automatic refresh |
| `feeds.txt` | Stores RSS feed URLs used by the collector |
| `requirements.txt` | Lists Python dependencies required to run the project |

---

## Requirements

This project uses Python and a local virtual environment.

Main dependencies:

- `feedparser`
- `beautifulsoup4`
- `fastapi`
- `uvicorn`
- `jinja2`

The project also uses Python standard library modules such as:

- `sqlite3`
- `hashlib`
- `logging`
- `datetime`
- `pathlib`
- `typing`
- `urllib.parse`
- `re`
- `os`
- `contextlib`

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

## Running the Collector Manually

Activate the virtual environment:

```bash
source venv/bin/activate
```

Run the bot:

```bash
python news_bot.py
```

The bot will:

1. Configure logging
2. Acquire the collector lock
3. Create or verify database tables
4. Register a collector run as `running`
5. Load RSS feeds from `feeds.txt`
6. Parse the feeds
7. Extract article metadata
8. Clean and limit summaries
9. Extract image URLs when available
10. Classify articles
11. Save new articles to SQLite
12. Skip duplicate articles
13. Register the collector run as `success` or `failed`
14. Release the collector lock
15. Write execution logs

---

## Automatic Collection with systemd

The project can run the RSS collector automatically using a `systemd` user timer.

The timer calls a one-shot service that runs the collector entry point:

```text
newswatch-collector.timer
   ↓
newswatch-collector.service
   ↓
python news_bot.py
```

The collector runs independently from the FastAPI web process.

Useful commands:

Start the timer:

```bash
systemctl --user start newswatch-collector.timer
```

Stop the timer:

```bash
systemctl --user stop newswatch-collector.timer
```

Enable and start the timer:

```bash
systemctl --user enable --now newswatch-collector.timer
```

Check timer status:

```bash
systemctl --user status newswatch-collector.timer
```

List timers:

```bash
systemctl --user list-timers --all | grep newswatch
```

Run the collector service manually:

```bash
systemctl --user start newswatch-collector.service
```

Check service status:

```bash
systemctl --user status newswatch-collector.service
```

Read systemd logs:

```bash
journalctl --user -u newswatch-collector.service -n 60 --no-pager
```

The collector is also logged to:

```text
logs/newswatch.log
```

---

## Running the Web Interface

Activate the virtual environment:

```bash
source venv/bin/activate
```

Run the FastAPI app:

```bash
uvicorn app.web:app --reload
```

Open the interface in the browser:

```text
http://127.0.0.1:8000
```

The current interface displays:

- Total articles
- Total sources
- Total categories
- Article cards
- Search field
- Category filter
- Source filter
- Manual reload button
- JavaScript loading state
- Dynamic reload completion message
- Article preview links
- Original source links

---

## Manual Reload from the Interface

The current interface includes a manual reload button.

The primary reload flow uses JavaScript:

```text
User clicks Reload News
   ↓
JavaScript intercepts the form submit event
   ↓
event.preventDefault() prevents the traditional page reload
   ↓
fetch() sends a POST request to /api/reload
   ↓
FastAPI runs the RSS collector
   ↓
The API returns a JSON response
   ↓
The interface shows a loading state and completion message
   ↓
The page refreshes automatically to display the updated article list
```

API route:

```text
POST /api/reload
```

Example JSON response:

```json
{
  "status": "success",
  "new_articles": 12
}
```

If another collector run is already active, the API can return:

```json
{
  "status": "busy",
  "message": "Collector is already running.",
  "new_articles": 0
}
```

The project also keeps a traditional form fallback route:

```text
POST /reload
```

This route reloads news and redirects back to the interface with query parameters showing the reload result.

---

## Testing the Reload API with curl

With the FastAPI server running, the reload API can be tested from the terminal:

```bash
curl -X POST http://127.0.0.1:8000/api/reload
```

Expected response example:

```json
{
  "status": "success",
  "new_articles": 0
}
```

The number of new articles depends on whether the RSS feeds contain articles that are not already stored in the database.

The traditional reload fallback can be tested with:

```bash
curl -X POST -i http://127.0.0.1:8000/reload
```

Expected response example:

```text
HTTP/1.1 303 See Other
location: /?reloaded=1&new_articles=0
```

---

## Search

The current interface includes a keyword search field.

The search checks the following article fields:

- Title
- Summary
- Source
- Category

Search can be combined with category and source filters.

Example:

```text
/?q=economy
```

Example with category filter:

```text
/?q=brazil&category=International
```

Example with source filter:

```text
/?q=technology&source=BBC News
```

---

## Article Detail Page

The interface includes a local article preview page.

Route:

```text
GET /articles/{article_id}
```

The preview page displays:

- Article title
- Source
- Category
- Published date
- Image when available
- RSS summary when available
- Original article link

This page uses metadata stored in SQLite and does not copy the full article content from the original source.

Future AI summaries may be added to this page.

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

Current feeds include a mix of:

- International news
- Brazilian news
- Technology
- Business
- Environment
- Science
- Public or institutional sources

Future improvement:

```text
Allow comments in feeds.txt so sources can be grouped by category.
```

Example future format:

```text
# World news
https://feeds.bbci.co.uk/news/world/rss.xml

# Brazil
https://agenciabrasil.ebc.com.br/rss/ultimasnoticias/feed.xml

# Technology
https://feeds.bbci.co.uk/news/technology/rss.xml
```

---

## Database

The project currently uses SQLite as a local database.

Database file:

```text
news.db
```

Main tables:

```text
articles
collector_runs
```

SQLite is being used during the local prototype stage because it is simple, lightweight, and suitable for development.

PostgreSQL may be introduced later when the project is prepared for production deployment, public access, scheduled background collection, heavier usage, and AI-generated summaries.

---

## Database Schema

Articles table:

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

Collector execution history table:

```sql
CREATE TABLE IF NOT EXISTS collector_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at TEXT NOT NULL,
    finished_at TEXT,
    status TEXT NOT NULL,
    new_articles INTEGER DEFAULT 0,
    duration_seconds REAL,
    error_message TEXT
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

## Collector Run History

The project stores collector execution history in the `collector_runs` table.

This table is used to track background and manual collector executions, including runs started by:

- `python news_bot.py`
- `systemd timer`
- `POST /api/reload`
- Traditional fallback route `POST /reload`

Tracked fields include:

| Column | Description |
|---|---|
| `id` | Unique collector run identifier |
| `started_at` | UTC timestamp when the collector run started |
| `finished_at` | UTC timestamp when the collector run finished |
| `status` | Collector run status: `running`, `success`, `failed`, or `skipped` |
| `new_articles` | Number of new articles saved during the run |
| `duration_seconds` | Total execution time in seconds |
| `error_message` | Error message when a run fails or is skipped |

This execution history is intended for internal monitoring, admin/status pages, troubleshooting, and future automation alerts.

---

## Duplicate Prevention

The bot prevents duplicate articles by generating a SHA-256 hash from the article link.

Example:

```python
hashlib.sha256(link.encode("utf-8")).hexdigest()
```

This generated hash is stored as the article `id`.

Because `id` is the primary key, SQLite prevents the same article from being inserted more than once.

If an existing article is found again, the project can still enrich missing metadata such as category, summary, or image URL.

---

## Collector Lock

The project uses a lock file to prevent overlapping collector executions.

Lock file:

```text
newswatch.lock
```

The lock file is created when a collector run starts and removed when the run finishes.

This prevents situations such as:

```text
systemd timer starts a collection
   ↓
user clicks Reload News at the same time
   ↓
two collectors try to run together
```

If another collector execution is already active, the new execution is skipped and recorded with:

```text
status = skipped
```

The lock file is a runtime artifact and should not be committed to GitHub.

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
"software", "AI", "chip", "automation" → Technology
```

This approach is simple, transparent, and easy to improve later.

Future improvements may include:

- Better keyword sets
- Multiple languages
- Full-word matching
- Weighted keyword scoring
- Feed-based category defaults
- NLP or AI-assisted classification

---

## Metadata Extraction

The collector extracts additional metadata from RSS entries.

Currently supported metadata:

- Summary
- Cleaned plain-text summary
- Limited-length summary
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

Future metadata improvements:

- Search for images in `description` as well as `summary`
- Validate image URLs before returning them
- Add interface placeholder when no article image is available
- Normalize RSS published dates into a consistent format

---

## Filtering and Ordering

The current interface supports filtering by:

- Keyword search
- Category
- Source

The interface currently shows only recently collected articles.

The current implementation filters articles using the `fetched_at` field, which represents when the bot collected the article.

The interface orders articles by:

```sql
ORDER BY fetched_at DESC
```

This means the most recently collected articles appear first.

This is more stable than ordering by the RSS `published` field because RSS feeds may provide publication dates in different formats.

---

## JavaScript Behavior

The project currently uses `static/app.js` to improve the interface experience.

Current JavaScript behavior:

- Confirms that JavaScript is loaded in the browser
- Waits for the DOM to load
- Finds the reload form using `#reload-form`
- Captures the form submit event
- Uses `event.preventDefault()` to stop the traditional form submission
- Sends a `POST` request to `/api/reload` using `fetch()`
- Uses `async/await` for asynchronous code
- Parses the JSON response
- Changes the reload button text to `Reloading...`
- Disables the reload button while the collector is running
- Shows success, busy, or error messages in the interface
- Refreshes the page automatically after successful reload

This creates a better user experience while keeping a traditional `/reload` route available as a fallback.

---

## Future AI Summary Layer

A future phase may add AI-generated summaries to article preview pages and topic pages.

The AI summary should be based on available RSS metadata and/or permitted source content.

Potential future fields:

```sql
ai_summary TEXT
ai_key_points TEXT
ai_context TEXT
ai_importance TEXT
ai_generated_at TEXT
ai_model TEXT
content_policy TEXT
```

The goal is to provide a useful interpretation layer without copying full articles or replacing the original source.

Potential AI output:

- Short summary
- Key points
- Context
- Why this matters
- Related topics
- Source comparison
- Uncertainty or missing information

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
- When the collector lock is acquired
- When the database is checked
- When a collector run is registered
- How many feeds were loaded
- Which sources were processed
- Feed URLs being processed
- New articles saved
- Article categories
- Feed parsing warnings
- Processing errors
- Total number of new articles saved
- Collector run final status
- When the collector lock is released
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

Show the collector runs table schema:

```sql
.schema collector_runs
```

Count all stored articles:

```sql
SELECT COUNT(*) FROM articles;
```

Show recent articles:

```sql
SELECT title, source, category, published, fetched_at
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

Search articles manually in SQLite:

```sql
SELECT title, source, category
FROM articles
WHERE title LIKE '%economy%'
OR summary LIKE '%economy%'
ORDER BY fetched_at DESC
LIMIT 10;
```

Check latest collected articles:

```sql
SELECT title, source, fetched_at
FROM articles
ORDER BY fetched_at DESC
LIMIT 20;
```

Show recent collector runs:

```sql
SELECT
    id,
    status,
    new_articles,
    duration_seconds,
    started_at,
    finished_at,
    error_message
FROM collector_runs
ORDER BY id DESC
LIMIT 10;
```

Show the latest collector run:

```sql
SELECT
    id,
    status,
    new_articles,
    duration_seconds,
    started_at,
    finished_at,
    error_message
FROM collector_runs
ORDER BY id DESC
LIMIT 1;
```

Count collector runs by status:

```sql
SELECT status, COUNT(*)
FROM collector_runs
GROUP BY status
ORDER BY COUNT(*) DESC;
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

Run the collector manually:

```bash
python news_bot.py
```

Run the FastAPI app:

```bash
uvicorn app.web:app --reload
```

Test the reload API:

```bash
curl -X POST http://127.0.0.1:8000/api/reload
```

Test the traditional reload fallback:

```bash
curl -X POST -i http://127.0.0.1:8000/reload
```

Check Python syntax:

```bash
python -m py_compile news_bot.py app/*.py
```

Read recent logs:

```bash
tail -n 40 logs/newswatch.log
```

Check systemd timer:

```bash
systemctl --user status newswatch-collector.timer
```

Check systemd service:

```bash
systemctl --user status newswatch-collector.service
```

List NewsWatch timers:

```bash
systemctl --user list-timers --all | grep newswatch
```

Read systemd service logs:

```bash
journalctl --user -u newswatch-collector.service -n 60 --no-pager
```

Check Git status:

```bash
git status
```

Stage changes:

```bash
git add .
```

Commit changes:

```bash
git commit -m "Describe the change here"
```

---

## Git Ignore Recommendation

The following files and folders should not be committed to GitHub:

```gitignore
# Python virtual environment
venv/
.venv/

# Python cache
__pycache__/
*.pyc

# Local database
news.db

# Logs
logs/*.log

# Runtime lock file
newswatch.lock

# Editor/system files
.vscode/
.DS_Store
```

Reason:

- `venv/` and `.venv/` are local environment data
- `__pycache__/` is Python cache
- `*.pyc` files are compiled Python artifacts
- `logs/*.log` is runtime output
- `news.db` is a local database file
- `newswatch.lock` is a temporary runtime lock
- `.vscode/` is local editor configuration

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
- Prepare project for web interface

Status:

```text
Completed
```

---

### Phase 6A — FastAPI + HTML Interface

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

- Add reload button to the interface
- Call collector from FastAPI
- Show reload completion message
- Display number of new articles saved

Status:

```text
Completed
```

---

### Phase 6C — Article Detail Page

- Add local article preview page
- Route: `/articles/{article_id}`
- Show title, source, category, image, summary, and original link
- Add `Read preview` link to article cards

Status:

```text
Completed
```

---

### Phase 6D — Search

- Search articles by keyword
- Search title, summary, source, and category
- Combine search with category and source filters

Status:

```text
Completed
```

---

### Phase 6E — JavaScript Improvements

Completed features:

- Load `static/app.js` in the browser
- Capture the reload form submit event
- Prevent the default form reload with `event.preventDefault()`
- Call `POST /api/reload` using `fetch()`
- Receive and parse JSON responses
- Show `Reloading...` on the reload button
- Disable the reload button while the collector is running
- Show reload success, busy, or error messages in the interface
- Automatically refresh the interface after reload
- Improve filter and reload button layout with CSS

Status:

```text
Completed
```

---

### Phase 7 — Automatic Background Collection

Completed features:

- Create a `systemd` user service for collector execution
- Create a `systemd` user timer for scheduled collection
- Run the RSS collector automatically in the background
- Keep background collection independent from the FastAPI web process
- Add a lock file to prevent overlapping collector runs
- Register collector execution history in SQLite
- Track run status, duration, new article count, and error messages
- Register collector runs from terminal, systemd, API reload, and traditional reload fallback
- Add query support for reading the latest collector run

Status:

```text
Completed
```

---

### Phase 8 — Public News Platform Interface

Planned features:

- Rework the current dashboard into a public-facing news platform interface
- Separate public reading pages from internal/admin status views
- Add topic-based navigation
- Improve article cards for reading experience
- Add sections such as Latest News, Top Stories, Brazil, World, Economy, Technology, and Security
- Prepare the interface for future AI summaries and context blocks

Status:

```text
Planned
```

---

### Phase 9 — Topic Grouping

Planned features:

- Detect articles covering the same topic
- Group related articles from multiple sources
- Create topic pages
- Show source coverage for each topic
- Prepare topic groups for AI interpretation

Status:

```text
Planned
```

---

### Phase 10 — AI Summaries and Interpretation

Planned features:

- Generate AI summaries for articles or topics
- Extract key points
- Explain why an article or topic matters
- Add context and possible implications
- Store generated summaries in SQLite or PostgreSQL
- Avoid copying full articles without permission
- Preserve original source links and attribution

Status:

```text
Planned
```

---

### Phase 11 — Automation and Notifications

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

### Phase 12 — Production Planning

Planned features:

- Evaluate PostgreSQL migration
- Prepare deployment environment
- Configure reverse proxy
- Add HTTPS
- Use domain name
- Add backups
- Add monitoring
- Separate public interface from admin/status area

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
- systemd practice
- SQLite practice
- FastAPI practice
- HTML/CSS practice
- JavaScript practice
- Logging practice
- Infrastructure portfolio development
- Future deployment practice
- Future automation practice
- Future AI integration practice

NewsWatch Bot is not just a script. It is being developed as a centralized news platform that demonstrates automation, data persistence, modular design, background collection, search functionality, API usage, JavaScript interaction, execution history, and future AI-powered news interpretation.