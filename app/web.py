from typing import Optional
from urllib.parse import urlencode

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.collector import process_feeds
from app.database import create_database
from app.queries import (
    get_article_by_id,
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
    q: Optional[str] = None,
    reloaded: Optional[str] = None,
    new_articles: Optional[int] = None,
):
    """
    Render the main dashboard page.
    """
    create_database()  # Ensure database is initialized

    articles = get_recent_articles(
        limit=50,
        category=category,
        source=source,
        search=q,
    )

    categories = get_categories()
    sources = get_sources()
    counts = get_article_counts()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "articles": articles,
            "categories": categories,
            "sources": sources,
            "counts": counts,
            "selected_category": category,
            "selected_source": source,
            "search_query": q,
            "reloaded": reloaded,
            "new_articles": new_articles,
        },
    )

@app.get("/articles/{article_id}", response_class=HTMLResponse)
def article_detail(request: Request, article_id: str):
    """
    Render a local article preview page.
    """

    article = get_article_by_id(article_id)

    if article is None:
        raise HTTPException(status_code=404, detail="Artile not found")
    
    return templates.TemplateResponse(
        request=request,
        name="article_detail.html",
        context={
            "article": article,
        },
    )

@app.post("/reload")
def reload_news(
    category: Optional[str] = None,
    source: Optional[str] = None,
    q: Optional[str] = None,
):
    """
    Manually reload news from the dashboard.
    """
    create_database()  # Ensure database is initialized
    total_new_articles = process_feeds()

    params = {
        "reloaded": "1",
        "new_articles": str(total_new_articles),
    }

    if category:
        params["category"] = category
    
    if source:
        params["source"] = source

    if q:
        params["q"] = q
        
    redirect_url = "/?" + urlencode(params)

    return RedirectResponse(url=redirect_url, status_code=303)