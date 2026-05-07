from typing import Optional

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import create_database
from app.queries import (
    get_article_counts,
    get_categories,
    get_recent_articles,
    get_sources,
)

app = FastAPI(title="NewsWatch Bot Dashboard")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)

def dashboard(
    request: Request,
    category: Optional[str] = None,
    source: Optional[str] = None,
):
    """
    Render the main dashboard page.
    """
    create_database()  # Ensure database is initialized

    articles = get_recent_articles(
        limit=50,
        category=category,
        source=source,
    )

    categories = get_categories()
    sources = get_sources()
    counts = get_article_counts()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "articles": articles,
            "categories": categories,
            "sources": sources,
            "counts": counts,
            "selected_category": category,
            "selected_source": source,
        },
    )
