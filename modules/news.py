"""News module — combines NewsAPI (top headlines) and Google News RSS (keyword search)."""
from __future__ import annotations

import os
import urllib.parse
from datetime import datetime, timedelta, timezone
from typing import Any

import feedparser
import requests


# General-interest topics for the daily journal "latest news" section.
GENERAL_TOPICS = [
    ("World", "general"),
    ("Technology", "technology"),
    ("Business / Finance", "business"),
    ("Science", "science"),
]


def fetch_newsapi_top(category: str, country: str = "fr", page_size: int = 3) -> list[dict[str, Any]]:
    """Pull top headlines for a category from NewsAPI."""
    key = os.getenv("NEWSAPI_KEY")
    if not key:
        return []

    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "category": category,
        "country": country,
        "pageSize": page_size,
        "apiKey": key,
    }
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
    except Exception:
        return []

    articles = []
    for a in data.get("articles", []):
        if not a.get("title") or not a.get("url"):
            continue
        articles.append({
            "title": a["title"],
            "url": a["url"],
            "source": (a.get("source") or {}).get("name", ""),
            "published": a.get("publishedAt", ""),
            "description": a.get("description", "") or "",
        })
    return articles


def fetch_google_news_rss(query: str, language: str = "en", country: str = "FR",
                          max_items: int = 5, hours: int = 24) -> list[dict[str, Any]]:
    """Pull recent items from a Google News RSS feed for a keyword."""
    q = urllib.parse.quote_plus(query)
    url = f"https://news.google.com/rss/search?q={q}+when:{hours}h&hl={language}&gl={country}&ceid={country}:{language}"
    feed = feedparser.parse(url)

    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    items = []
    for entry in feed.entries[:max_items * 2]:
        try:
            pub = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        except Exception:
            pub = datetime.now(timezone.utc)
        if pub < cutoff:
            continue
        items.append({
            "title": entry.title,
            "url": entry.link,
            "source": getattr(entry, "source", {}).get("title", "") if hasattr(entry, "source") else "",
            "published": pub.isoformat(),
            "description": getattr(entry, "summary", "") or "",
        })
        if len(items) >= max_items:
            break
    return items


def get_daily_news() -> dict[str, list[dict[str, Any]]]:
    """Return a dict {topic_label: [articles...]} for the daily journal."""
    out: dict[str, list[dict[str, Any]]] = {}
    for label, category in GENERAL_TOPICS:
        articles = fetch_newsapi_top(category, country="fr", page_size=3)
        # If NewsAPI failed or returned nothing, fall back to Google News RSS.
        if not articles:
            articles = fetch_google_news_rss(label, language="en", country="FR", max_items=3)
        out[label] = articles[:3]
    return out


def format_news_html(news: dict[str, list[dict[str, Any]]]) -> str:
    parts = []
    for topic, articles in news.items():
        if not articles:
            continue
        parts.append(f"<h4 style='margin-bottom:4px'>{topic}</h4><ul style='margin-top:4px'>")
        for a in articles:
            src = f" <span style='color:#888'>({a['source']})</span>" if a.get("source") else ""
            parts.append(
                f"<li><a href=\"{a['url']}\">{a['title']}</a>{src}</li>"
            )
        parts.append("</ul>")
    if not parts:
        return "<p><em>No news retrieved.</em></p>"
    return "\n".join(parts)


if __name__ == "__main__":
    from pprint import pprint
    pprint(get_daily_news())
