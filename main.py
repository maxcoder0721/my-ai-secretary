"""Daily Secretary — main orchestrator.

Pulls weather, news, calendar, today's programs and topic-based alerts,
composes an HTML journal and emails it to RECIPIENT_EMAIL.

Run locally:
    python main.py

In production, run from GitHub Actions every morning at 7am Paris time.
"""
from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path

import pytz
from dotenv import load_dotenv

# Load .env if present (no-op on GitHub Actions where vars come from secrets).
load_dotenv()

from modules import alerts, calendar_module, emailer, news, programs, weather


def build_journal_html() -> tuple[str, str]:
    """Compose the daily journal. Returns (subject, html)."""
    tz = pytz.timezone(os.getenv("USER_TIMEZONE", "Europe/Paris"))
    now = datetime.now(tz)
    name = os.getenv("USER_NAME", "Leo")

    # Each section is independently resilient — one failure should not break the journal.
    try:
        weather_data = weather.get_weather()
        weather_html = weather.format_weather_html(weather_data)
    except Exception as e:
        weather_html = f"<p><em>Weather error: {e}</em></p>"

    try:
        events = calendar_module.get_today_events()
        calendar_html = calendar_module.format_calendar_html(events)
    except Exception as e:
        calendar_html = f"<p><em>Calendar error: {e}</em></p>"

    try:
        alerts_data = alerts.get_alerts()
        alerts_html = alerts.format_alerts_html(alerts_data)
    except Exception as e:
        alerts_html = f"<p><em>Alerts error: {e}</em></p>"

    try:
        daily_news = news.get_daily_news()
        news_html = news.format_news_html(daily_news)
    except Exception as e:
        news_html = f"<p><em>News error: {e}</em></p>"

    try:
        picks = programs.get_daily_programs(now.date(), n=5)
        programs_html = programs.format_programs_html(picks)
    except Exception as e:
        programs_html = f"<p><em>Programs error: {e}</em></p>"

    date_str = now.strftime("%A %d %B %Y")
    subject = f"Daily Journal — {date_str}"

    html = f"""
    <html><body style="font-family:-apple-system, Segoe UI, Helvetica, Arial, sans-serif;
                       max-width:680px; margin:0 auto; color:#222; line-height:1.5;">

      <h1 style="border-bottom:2px solid #444; padding-bottom:6px;">
        Good morning, {name} &#9728;
      </h1>
      <p style="color:#666; margin-top:-6px;">{date_str} &middot; Paris</p>

      <h2 style="color:#b94700">Alerts &amp; opportunities (last 24h)</h2>
      {alerts_html}

      <h2>Today's weather</h2>
      {weather_html}

      <h2>Today's schedule</h2>
      {calendar_html}

      <h2>News digest</h2>
      {news_html}

      <h2>Today's 5 programs to consider</h2>
      <p style="color:#555;font-size:13px">Rotating selection from a curated list. Always verify deadlines on the official site.</p>
      {programs_html}

      <hr style="margin-top:32px; border:0; border-top:1px solid #ddd">
      <p style="color:#888; font-size:12px;">
        Generated automatically by your Daily Secretary &middot;
        sources: Open-Meteo, NewsAPI, Google News, Google Calendar.
      </p>
    </body></html>
    """
    return subject, html


def main() -> int:
    subject, html = build_journal_html()

    # If --dry-run is passed, just print to stdout (used in CI smoke tests).
    if "--dry-run" in sys.argv:
        out = Path("journal_preview.html")
        out.write_text(html, encoding="utf-8")
        print(f"[dry-run] Wrote {out.resolve()}")
        print(f"[dry-run] Subject: {subject}")
        return 0

    emailer.send_email(subject, html)
    print(f"Sent: {subject}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
