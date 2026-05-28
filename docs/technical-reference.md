# NewsWatch Bot

NewsWatch Bot is a Linux-based Python project designed to collect, store, classify, search, summarize, and organize news from RSS feeds.

The project started as a command-line RSS collector and has evolved into a centralized news intelligence platform with structured data, automatic background collection, logging, categorization, a FastAPI + HTML/CSS/JavaScript interface, article preview pages, keyword search, reload API routes, collector execution history, AI-generated article summaries, a daily intelligence briefing, and future support for topic grouping, source comparison, automation, and production deployment.

The long-term goal is not only to provide a technical dashboard, but to build a public-facing news intelligence platform that helps users understand what is happening across multiple sources without manually opening many different news websites.

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
- Anthropic API (Claude Haiku) for AI summaries and daily briefings
- Future topic-based grouping
- Future source comparison
- Future automation and notifications
- Future production deployment with PostgreSQL

The final objective is to centralize relevant news from multiple sources into a single platform, allowing articles to be collected, filtered, searched, categorized, reviewed, refreshed, interpreted, and summarized with AI.

The platform helps users quickly understand:

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
Phase 8B-4 — Brazil Brief, classifier refinement, AI integration
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
- World Brief block filtered by foreign sources
- Brazil Brief block filtered by Brazilian sources
- Improved keyword classifier with word-boundary matching and priority-based tiebreak
- AI-generated summaries for articles in relevant categories
- AI-generated daily briefing using all relevant articles from the last 24 hours
- `systemd timer` for batch AI summary processing every 15 minutes
- `systemd timer` for daily briefing generation every 2 hours

Next planned phase:

```text
Phase 9 — Public-facing layout redesign
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
- Classify articles using rule-based keyword matching with word-boundary matching
- Apply explicit priority order to break classifier ties
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
- Display a World Brief block filtered by foreign sources
- Display a Brazil Brief block filtered by Brazilian sources
- Generate AI summaries for articles in Politics, Economy, Security, and International categories
- Use longer AI summaries (2–3 lines) for Politics, Economy, and Security
- Use shorter AI summaries (1 line) for International
- Generate a structured daily briefing with four sections: General Scenario, World, Brazil, and Why It Matters Today
- Store AI summaries directly in the `articles` table
- Store generated daily briefings in a dedicated `daily_briefings` table
- Track AI usage with input and output token counts and model used
- Process pending AI summaries automatically every 15 minutes
- Generate a new daily briefing automatically every 2 hours

---

## Planned Features

- Redesign the public reading interface with intelligence-platform aesthetics
- Keep technical collector/status information in an internal admin area
- Add topic-based news grouping
- Add AI-generated key points and full "why this matters" sections per article
- Compare coverage from multiple sources when possible
- Add source reliability and attribution notes
- Add JSON API endpoints for public article/topic listing
- Improve JavaScript interactions further
- Update article lists dynamically without full page reload
- Improve category classification through AI-assisted reclassification
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
systemd timer (collector, every 15 minutes)
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

AI processing architecture:

```text
systemd timer (ai-processor, every 15 minutes)
   ↓
newswatch-ai-processor.service
   ↓
python -m app.ai_processor
   ↓
SQLite query for pending relevant articles
   ↓
Anthropic API (Claude Haiku) — one call per article
   ↓
ai_summary column on articles table
```

Daily briefing generation architecture:

```text
systemd timer (briefing, every 2 hours)
   ↓
newswatch-briefing.service
   ↓
python -m app.briefing_processor
   ↓
SQLite query for last 24h articles with ai_summary
   ↓
Anthropic API (Claude Haiku) — one consolidation call
   ↓
daily_briefings table
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

The collector runs independently from the FastAPI web application. The AI processor and the briefing generator also run independently. This separation keeps background workloads from blocking the public web interface and prepares the project for a more production-oriented deployment model.

---

## Product Direction

The current interface should be understood as an internal prototype while the public layout is being redesigned.

The long-term product direction is to evolve NewsWatch Bot into a public-facing centralized news intelligence platform.

The future platform should provide:

- Public reading pages
- A prominent daily intelligence briefing as the entry point
- World Brief and Brazil Brief as scannable side feeds
- A live source feed with the most recently collected articles
- Search and navigation by category/topic
- Topic-based article grouping
- AI-generated summaries
- AI-generated context
- AI-generated key points
- "Why this matters" explanations
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
│   ├── ai.py
│   ├── ai_processor.py
│   ├── briefing_processor.py
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
├── .env
├── .gitignore
├── news_bot.py
├── news.db
├── README.md
└── requirements.txt
```

Runtime files such as `news.db`, `logs/newswatch.log`, `newswatch.lock`, `news.db.backup-*`, and `.env` are local development artifacts and should not be committed to GitHub.

---

## Module Responsibilities

| File | Responsibility |
|---|---|
| `app/config.py` | Stores project configuration such as database path, feeds file path, log file path, and lock file path |
| `app/logging_config.py` | Configures terminal and file logging |
| `app/database.py` | Handles SQLite database creation, migrations, article IDs, article persistence, collector run history, and the `daily_briefings` table |
| `app/classifier.py` | Classifies articles using rule-based keyword matching with word-boundary matching and priority-based tiebreak |
| `app/metadata.py` | Extracts summaries, cleans HTML, limits text length, and extracts image URLs |
| `app/collector.py` | Loads RSS feeds, parses articles, extracts metadata, classifies articles, and saves them |
| `app/queries.py` | Reads articles, categories, sources, article details, dashboard metrics, collector run status, World Brief, and Brazil Brief from SQLite |
| `app/runtime_lock.py` | Provides a lock file mechanism to prevent overlapping collector executions |
| `app/web.py` | Defines the FastAPI application, dashboard routes, article routes, reload routes, and API routes |
| `app/ai.py` | Provides AI summary generation for articles and daily briefing generation using the Anthropic API |
| `app/ai_processor.py` | Batch processor that picks pending articles and generates AI summaries; runs from `systemd` |
| `app/briefing_processor.py` | Generates and persists the daily briefing; runs from `systemd` |
| `news_bot.py` | Main command-line entry point used to run the collector manually or through systemd |
| `templates/index.html` | Main HTML template for the current interface |
| `templates/article_detail.html` | Local article preview page template |
| `static/style.css` | Interface and article page styling |
| `static/app.js` | Handles JavaScript behavior, reload API calls, loading state, dynamic messages, and automatic refresh |
| `feeds.txt` | Stores RSS feed URLs used by the collector |
| `.env` | Stores the `ANTHROPIC_API_KEY` for AI features (local only, ignored by Git) |
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
- `anthropic`
- `python-dotenv`

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
python -m pip install feedparser beautifulsoup4 fastapi uvicorn jinja2 anthropic python-dotenv
python -m pip freeze > requirements.txt
```

---

## Environment Configuration

The AI features require an Anthropic API key.

Create a `.env` file in the project root:

```text
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

The `.env` file is local only. It is listed in `.gitignore` and must never be committed to GitHub.

To confirm Git is ignoring the `.env` file:

```bash
git check-ignore -v .env
```

Expected output:

```text
.gitignore:NN:.env  .env
```

The project loads the key automatically using `python-dotenv` when `app/ai.py` is imported.

To test the key without using the AI features:

```bash
python -c "
from dotenv import load_dotenv
import os
load_dotenv()
key = os.getenv('ANTHROPIC_API_KEY')
print('OK' if key else 'KEY NOT FOUND')
"
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

## Running the AI Processor Manually

The AI processor generates AI summaries for articles that are pending and belong to relevant categories.

Activate the virtual environment:

```bash
source venv/bin/activate
```

Run the processor:

```bash
python -m app.ai_processor
```

Each run processes at most `MAX_ARTICLES_PER_RUN` articles (currently 30) to keep cost predictable.

The processor skips articles that:

- Already have an `ai_summary` value
- Have no source `summary` to summarize
- Belong to categories outside the relevant set

---

## Running the Briefing Generator Manually

The briefing generator consolidates AI summaries from the last 24 hours into a single structured daily briefing.

Activate the virtual environment:

```bash
source venv/bin/activate
```

Run the generator:

```bash
python -m app.briefing_processor
```

Each run produces one entry in the `daily_briefings` table. Older entries are retained for history.

---

## Automatic Background Execution with systemd

The project runs three coordinated `systemd` user timers.

| Timer | Frequency | Purpose |
|---|---|---|
| `newswatch-collector.timer` | every 15 minutes | Collect new articles from RSS feeds |
| `newswatch-ai-processor.timer` | every 15 minutes | Generate AI summaries for pending relevant articles |
| `newswatch-briefing.timer` | every 2 hours | Generate the consolidated daily briefing |

Each timer triggers a corresponding one-shot service:

```text
newswatch-collector.timer    → newswatch-collector.service    → python news_bot.py
newswatch-ai-processor.timer → newswatch-ai-processor.service → python -m app.ai_processor
newswatch-briefing.timer     → newswatch-briefing.service     → python -m app.briefing_processor
```

All services run independently from the FastAPI web process.

Useful commands:

Start all timers:

```bash
systemctl --user start newswatch-collector.timer
systemctl --user start newswatch-ai-processor.timer
systemctl --user start newswatch-briefing.timer
```

Stop all timers:

```bash
systemctl --user stop newswatch-collector.timer
systemctl --user stop newswatch-ai-processor.timer
systemctl --user stop newswatch-briefing.timer
```

Enable timers to start at boot:

```bash
systemctl --user enable newswatch-collector.timer
systemctl --user enable newswatch-ai-processor.timer
systemctl --user enable newswatch-briefing.timer
```

List NewsWatch timers and their next scheduled execution:

```bash
systemctl --user list-timers | grep newswatch
```

Check the status of a specific timer:

```bash
systemctl --user status newswatch-briefing.timer
```

Check the status of a specific service:

```bash
systemctl --user status newswatch-briefing.service
```

Read recent systemd logs for a service:

```bash
journalctl --user -u newswatch-ai-processor.service -n 60 --no-pager
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

- Daily Briefing block (placeholder, layout redesign in progress)
- World Brief block with recent international headlines
- Brazil Brief block with recent Brazilian headlines
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
- AI summary when available
- Original article link

This page uses metadata stored in SQLite and does not copy the full article content from the original source.

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

To add or remove sources, edit `feeds.txt`. The collector does not need code changes when RSS sources are updated.

Current feeds include a mix of:

- International news (BBC, Guardian, NYT, Deutsche Welle, France 24, Euronews)
- Brazilian news (UOL, Folha, CNN Brasil, Agência Pública, Intercept Brasil, Agência Brasil)
- Technology, business, environment, and science feeds from the same sources
- Public or institutional sources (NASA)

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
daily_briefings
```

SQLite is being used during the local prototype stage because it is simple, lightweight, and suitable for development.

PostgreSQL may be introduced later when the project is prepared for production deployment, public access, scheduled background collection, heavier usage, and AI-generated content at scale.

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
    fetched_at TEXT NOT NULL,
    ai_summary TEXT,
    ai_summary_at TEXT
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

Daily briefings table:

```sql
CREATE TABLE IF NOT EXISTS daily_briefings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    generated_at TEXT NOT NULL,
    content TEXT NOT NULL,
    articles_considered INTEGER NOT NULL,
    input_tokens INTEGER,
    output_tokens INTEGER,
    model_used TEXT
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
| `ai_summary` | AI-generated summary in Portuguese (only for relevant categories) |
| `ai_summary_at` | UTC timestamp when the AI summary was generated |

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

## Daily Briefings History

The project stores every generated daily briefing in the `daily_briefings` table.

Tracked fields:

| Column | Description |
|---|---|
| `id` | Unique briefing identifier |
| `generated_at` | UTC timestamp when the briefing was generated |
| `content` | The full briefing text |
| `articles_considered` | How many articles were used as input |
| `input_tokens` | Anthropic API input tokens consumed |
| `output_tokens` | Anthropic API output tokens generated |
| `model_used` | Model identifier used to generate the briefing |

Older briefings are retained for history and auditability rather than overwritten.

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

The project currently uses rule-based classification with word-boundary matching.

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
title + summary
```

The `source` field is intentionally excluded from the matched text to avoid the source name biasing classification (for example, the word "Brasil" in "CNN Brasil" should not affect category selection).

Each keyword is matched as a whole word using regex word boundaries (`\b`), which avoids false positives such as matching "ia" inside "Brasília" or "tech" inside "technical".

When multiple categories tie on score, a fixed priority order resolves the winner:

```text
International → Health → Sports → Environment → Security → Economy → Technology → Politics
```

The priority is intentional. More specific categories beat broader ones. Politics is the broadest topic and absorbs noise, so it is the last fallback before `General`.

Future improvements may include:

- AI-assisted reclassification of existing articles
- Multilingual keyword expansion
- Feed-based category defaults
- Weighted keyword scoring

---

## AI Integration

The project uses the Anthropic API (Claude Haiku) for two distinct tasks.

### Article summaries

Articles in the categories Politics, Economy, Security, and International receive an AI-generated summary in Portuguese.

The prompt length adapts to category:

- Politics, Economy, Security: 2 to 3 lines per article (high priority)
- International: 1 line per article

Summaries are written to be factual, direct, and free of opinion. Filler phrases like "O artigo fala sobre..." are avoided by prompt design.

Articles in other categories are stored normally and displayed in the source feed, but do not receive an AI summary. This keeps cost predictable and focuses interpretation effort on news that benefits most from it.

### Daily briefing

The daily briefing consolidates all relevant articles from the last 24 hours into a structured intelligence brief.

Structure of every briefing:

- **Cenário geral** — two lines synthesizing the overall tone of the day
- **Mundo** — three to four lines connecting the main international fios geopolitical and economic threads
- **Brasil** — three to four lines covering political, economic, and security movements in Brazil
- **Por que importa hoje** — two lines explaining what makes the day significant

The briefing is generated by passing every article's title, source, category, and `ai_summary` to a single Anthropic API call. The model is instructed to connect related stories rather than only paraphrasing each one.

### Cost model

Approximate cost per article summary:

- ~150 input tokens × $1/M = $0.00015
- ~50 output tokens × $5/M = $0.00025
- Total per article: about $0.0004

Approximate cost per daily briefing:

- ~3000 input tokens × $1/M = $0.003
- ~600 output tokens × $5/M = $0.003
- Total per briefing: about $0.006

With the default schedule (15-minute AI processor, 2-hour briefing) and an estimated 100 new relevant articles per day:

- Article summaries: about $0.05 per day
- Daily briefings: about $0.07 per day
- Total: under $5 per month

The `MAX_ARTICLES_PER_RUN` constant in `app/ai_processor.py` (currently 30) acts as a safety limit and caps the cost of any single run to a few cents.

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

## World Brief and Brazil Brief

The interface includes two curated side blocks.

### World Brief

Filtered by **source** rather than category. Only articles from foreign sources appear here:

- BBC News
- The Guardian (World, Business, Technology, Environment)
- New York Times (World, Business, Technology, Science)
- Deutsche Welle (and DW Europe)
- France 24
- Euronews

This separation makes the World Brief read as "what foreign newsrooms are saying", complementing the Brazil Brief.

### Brazil Brief

Filtered by **source** as well. Only articles from Brazilian sources appear:

- Agência Pública
- CNN Brasil
- Agência Brasil (Feed Últimas)
- Folha de S.Paulo
- Intercept Brasil
- UOL Notícias

This split avoids overlap between the two blocks and gives each one a clear identity.

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

The AI processor and the briefing generator log to systemd journal (visible with `journalctl --user`).

Useful log commands:

```bash
tail logs/newswatch.log
tail -n 40 logs/newswatch.log
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

Show the daily briefings table schema:

```sql
.schema daily_briefings
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

Show articles that already have an AI summary:

```sql
SELECT title, category, ai_summary
FROM articles
WHERE ai_summary IS NOT NULL
ORDER BY ai_summary_at DESC
LIMIT 10;
```

Count pending articles per category (relevant categories only):

```sql
SELECT category, COUNT(*)
FROM articles
WHERE category IN ('Politics', 'Economy', 'Security', 'International')
  AND (ai_summary IS NULL OR ai_summary = '')
GROUP BY category;
```

Show recent daily briefings:

```sql
SELECT
    id,
    generated_at,
    articles_considered,
    input_tokens,
    output_tokens,
    model_used
FROM daily_briefings
ORDER BY id DESC
LIMIT 5;
```

Read the latest daily briefing in full:

```sql
SELECT content
FROM daily_briefings
ORDER BY id DESC
LIMIT 1;
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

Run the AI processor manually:

```bash
python -m app.ai_processor
```

Run the daily briefing generator manually:

```bash
python -m app.briefing_processor
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

Check systemd timers:

```bash
systemctl --user list-timers | grep newswatch
```

Read systemd service logs:

```bash
journalctl --user -u newswatch-collector.service -n 60 --no-pager
journalctl --user -u newswatch-ai-processor.service -n 60 --no-pager
journalctl --user -u newswatch-briefing.service -n 60 --no-pager
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

# Database backups
news.db.backup-*

# Logs
logs/*.log

# Runtime lock file
newswatch.lock

# Environment variables (API keys, secrets)
.env

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
- `news.db.backup-*` are local backups created before risky operations
- `newswatch.lock` is a temporary runtime lock
- `.env` contains the Anthropic API key and other secrets
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

### Phase 8A — World Brief and Brazil Brief

- Add a World Brief block filtered by foreign sources
- Add a Brazil Brief block filtered by Brazilian sources
- Render both blocks in the dashboard
- Avoid overlap between the two blocks

Status:

```text
Completed
```

---

### Phase 8B — Classifier Refinement

- Rewrite the classifier with whole-word matching using regex word boundaries
- Add English keywords alongside Portuguese
- Remove ambiguous short keywords that caused false positives
- Apply explicit priority order to break category ties
- Stop using the `source` field in the matched text to avoid bias
- Reclassify all existing articles in the database

Status:

```text
Completed
```

---

### Phase 8C — AI Integration

- Add Anthropic API key configuration via `.env` and `python-dotenv`
- Add `app/ai.py` with article summary and daily briefing generation
- Add `ai_summary` and `ai_summary_at` columns to the `articles` table
- Add `daily_briefings` table to store generated briefings
- Add `app/ai_processor.py` for batch processing of pending articles
- Add `app/briefing_processor.py` for daily briefing generation
- Add a `systemd` timer for the AI processor (every 15 minutes)
- Add a `systemd` timer for the daily briefing (every 2 hours)
- Apply a per-run safety limit on the AI processor to keep cost predictable
- Skip articles outside the relevant categories
- Adapt summary length to category priority

Status:

```text
Completed
```

---

### Phase 9 — Public-facing Layout Redesign

Planned features:

- Redesign the home interface as an intelligence-platform layout
- Make the Daily Briefing the visual hero of the page
- Place World Brief and Brazil Brief as scannable side columns
- Move the live source feed below, with category-coded icons
- Apply a dark, technical aesthetic with serif-on-monospace typography contrast
- Add an atmospheric background layer (corner brackets, vertical rules, particle texture, indexed identifiers)
- Introduce a brand mark based on a "mission board" metaphor

Status:

```text
In progress
```

---

### Phase 10 — Topic Grouping

Planned features:

- Detect articles covering the same topic across sources
- Group related articles in topic pages
- Show source coverage for each topic
- Prepare topic groups for AI interpretation

Status:

```text
Planned
```

---

### Phase 11 — Deeper AI Interpretation

Planned features:

- AI-generated key points per article
- AI-generated context per article
- AI-generated "why this matters" explanations
- AI-assisted reclassification of existing articles
- Source comparison when multiple sources cover the same topic

Status:

```text
Planned
```

---

### Phase 12 — Automation and Notifications

Planned features:

- Telegram alerts
- Discord alerts
- Email reports
- Daily summaries delivered to external channels
- n8n automation integration
- Google Sheets export

Status:

```text
Planned
```

---

### Phase 13 — Production Planning

Planned features:

- Evaluate PostgreSQL migration
- Prepare deployment environment
- Configure reverse proxy
- Add HTTPS
- Use domain name
- Add backups
- Add monitoring
- Separate public interface from admin/status area
- Apply rate limiting on the AI processor and on public endpoints

Status:

```text
Planned
```

---

## Ethical and Legal Notes

This project prioritizes RSS feeds and public metadata.

The collector avoids:

- Copying full articles without permission
- Bypassing paywalls
- Ignoring robots.txt when scraping
- Sending excessive requests to websites
- Republishing restricted images or copyrighted content without permission

The project stores:

- Title
- Source
- Link
- Published date
- Short RSS summary when available
- Image URL when provided by the feed
- AI-generated summary derived only from the title and RSS summary

Full article extraction should only be added for sources that clearly allow it.

AI summaries are used as a transformative interpretation layer. They are generated from limited metadata (title plus short RSS summary) and never from the full article body, so they do not redistribute source content. The original source link should always remain visible.

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
- API integration practice (Anthropic API)
- Prompt design practice
- Infrastructure portfolio development
- Future deployment practice
- Future automation practice

NewsWatch Bot is not just a script. It is being developed as a centralized news intelligence platform that demonstrates automation, data persistence, modular design, background collection, search functionality, API usage, JavaScript interaction, execution history, AI-powered news interpretation, and infrastructure design for future deployment.
