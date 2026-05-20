"""Topic-based alerts — watches news for items relevant to a French grade-12
student interested in finance, astronomy and coding/tech.

The module returns *interesting* items (last 24h) using Google News RSS keyword
searches. The orchestrator deduplicates against the general news feed and
highlights any urgent alerts at the top of the email.
"""
from __future__ import annotations

from typing import Any

from . import news


# Keyword groups. Each key becomes a section label in the email.
ALERT_TOPICS: dict[str, list[str]] = {
    "Parcoursup / Terminale (France)": [
        "Parcoursup",
        "Baccalauréat 2026",
        "Terminale réforme",
        "bourse lycéen France",
    ],
    "Finance scholarships & insight": [
        "spring insight banking 2026",
        "finance scholarship lycéen",
        "JP Morgan insight programme",
        "Goldman Sachs student programme",
    ],
    "Astronomy / space opportunities": [
        "astronomy summer school 2026",
        "ESA Academy",
        "Olympiades astronomie",
        "CNES jeunes",
    ],
    "Coding / AI programs & contests": [
        "coding summer school 2026",
        "AI scholarship high school",
        "hackathon Paris lycéen",
        "Apple Swift student challenge",
    ],
}


def get_alerts(max_per_topic: int = 2) -> dict[str, list[dict[str, Any]]]:
    """Return a dict {topic: [articles...]} of new items in the last 24h."""
    out: dict[str, list[dict[str, Any]]] = {}
    for topic, queries in ALERT_TOPICS.items():
        items: list[dict[str, Any]] = []
        seen_urls: set[str] = set()
        for q in queries:
            for art in news.fetch_google_news_rss(q, language="en", country="FR",
                                                   max_items=max_per_topic, hours=24):
                if art["url"] in seen_urls:
                    continue
                seen_urls.add(art["url"])
                items.append(art)
            # also try in French for France-specific topics
            for art in news.fetch_google_news_rss(q, language="fr", country="FR",
                                                   max_items=max_per_topic, hours=24):
                if art["url"] in seen_urls:
                    continue
                seen_urls.add(art["url"])
                items.append(art)
        if items:
            out[topic] = items[:max_per_topic * 2]
    return out


def format_alerts_html(alerts: dict[str, list[dict[str, Any]]]) -> str:
    if not alerts:
        return "<p><em>No new relevant alerts in the last 24 hours.</em></p>"

    parts = []
    for topic, items in alerts.items():
        parts.append(f"<h4 style='margin-bottom:4px;color:#b94700'>&#9888; {topic}</h4><ul style='margin-top:4px'>")
        for it in items:
            src = f" <span style='color:#888'>({it['source']})</span>" if it.get("source") else ""
            parts.append(
                f"<li><a href=\"{it['url']}\">{it['title']}</a>{src}</li>"
            )
        parts.append("</ul>")
    return "\n".join(parts)


if __name__ == "__main__":
    from pprint import pprint
    pprint(get_alerts())
