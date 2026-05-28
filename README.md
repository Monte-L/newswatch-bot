# NewsWatch Bot

NewsWatch Bot is a Python-based local news intelligence dashboard that collects RSS feeds, stores articles in SQLite, classifies them by category, displays them through a FastAPI web interface, and generates AI-assisted news summaries and daily briefings.

The project started as a command-line RSS collector and evolved into a structured news aggregation platform with background automation, search, filtering, article preview pages, execution tracking, and AI-powered interpretation.

## Project Goals

- Collect news from multiple RSS sources
- Store and organize articles in a local SQLite database
- Classify articles by topic using a rule-based classifier
- Provide a FastAPI + HTML/CSS/JavaScript dashboard
- Support keyword search, source filters, and category filters
- Run collection automatically in the background with systemd timers
- Prevent overlapping collector runs with a lock mechanism
- Generate AI summaries for relevant articles
- Generate a recurring daily intelligence briefing
- Prepare the project for future public deployment and automation

## Current Stack

- Python
- FastAPI
- SQLite
- Jinja2 templates
- HTML/CSS/JavaScript
- RSS feeds with `feedparser`
- BeautifulSoup
- systemd user services and timers
- Anthropic API for AI summaries and briefings
- python-dotenv for local environment configuration

## Main Features

- RSS feed collection from multiple public sources
- Article storage in SQLite
- Duplicate prevention using SHA-256 hashes
- Rule-based article classification
- Search by keyword
- Category and source filters
- Local article preview pages
- Original source links preserved for attribution
- Manual reload from the web dashboard
- JSON reload API route
- JavaScript reload flow with loading state and completion message
- Background collection through systemd timers
- Collector execution history stored in SQLite
- Lock file to prevent overlapping collector runs
- AI-generated article summaries for selected categories
- Daily briefing generation using recent summarized articles
- Separate World Brief and Brazil Brief sections

## Architecture

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
Jinja2 Templates
   ↓
HTML/CSS/JavaScript Dashboard
```

## Background Automation

```text
systemd timer
   ↓
newswatch-collector.service
   ↓
python news_bot.py
   ↓
Collector lock
   ↓
RSS collection
   ↓
SQLite persistence
   ↓
collector_runs history
```

## AI Processing Flow

```text
Pending relevant articles
   ↓
AI summary processor
   ↓
Anthropic API
   ↓
ai_summary stored in SQLite
   ↓
Daily briefing generator
   ↓
daily_briefings table
```

## Implemented Components

### Collector

The collector loads RSS feed URLs from `feeds.txt`, parses articles, extracts metadata, classifies them, prevents duplicates, and stores new articles in SQLite.

### Web Interface

The FastAPI application displays article cards, category filters, source filters, keyword search, local article previews, World Brief, Brazil Brief, and manual reload controls.

### Background Execution

The project uses systemd user timers and one-shot services to run the collector and AI processors independently from the web interface.

### AI Layer

The AI layer generates short article summaries and a structured daily briefing from recent relevant articles. API keys are stored locally in `.env` and must never be committed.

## Database Tables

```text
articles
collector_runs
daily_briefings
```

The database tracks collected articles, collector execution history, AI summaries, and generated daily briefings.

## Repository Structure

```text
newswatch-bot/
├── app/
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
├── static/
│   ├── app.js
│   └── style.css
├── templates/
│   ├── index.html
│   └── article_detail.html
├── feeds.txt
├── news_bot.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Local Setup

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a local `.env` file for AI features:

```text
ANTHROPIC_API_KEY=your-local-api-key
```

The `.env` file is ignored by Git and must not be committed.

## Running the Project

Run the collector manually:

```bash
python news_bot.py
```

Run the FastAPI interface:

```bash
uvicorn app.web:app --reload
```

Open the local dashboard:

```text
http://127.0.0.1:8000
```

Run the AI processor manually:

```bash
python -m app.ai_processor
```

Run the briefing generator manually:

```bash
python -m app.briefing_processor
```

## Security and Privacy Notes

Runtime and private files should not be committed:

```text
.env
news.db
logs/*.log
newswatch.lock
news.db.backup-*
venv/
__pycache__/
```

The project keeps original source links visible and avoids copying full articles. It works with RSS metadata, short summaries when available, and AI-generated interpretation.

## Skills Demonstrated

- Python project organization
- FastAPI application development
- SQLite database design
- RSS parsing and metadata extraction
- Modular backend structure
- HTML/CSS/JavaScript interface development
- Background automation with systemd
- Logging and execution history
- API integration
- Prompt design for AI summaries
- Cost-aware AI processing
- Technical documentation
- Product-oriented infrastructure planning

## Current Status

The project currently supports RSS collection, SQLite persistence, FastAPI dashboard display, search, filters, manual reload, background collection, execution history, AI article summaries, and daily briefing generation.

## Roadmap

- Improve the public-facing layout
- Separate public reading interface from internal/admin status views
- Add topic-based grouping
- Compare multiple sources covering the same topic
- Improve metadata extraction and image handling
- Add notifications through Telegram, Discord, or email
- Add n8n automation workflows
- Evaluate PostgreSQL for production deployment
- Prepare reverse proxy, HTTPS, backups, and public hosting

## Portfolio Summary

NewsWatch Bot demonstrates the ability to design and build a practical automation platform that combines Python, Linux scheduling, databases, web interfaces, background services, API integration, and AI-assisted information processing. It is a strong portfolio project for infrastructure, automation, Linux, and junior backend-oriented roles.
