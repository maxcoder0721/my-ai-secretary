"""Google Calendar module — reads today's events."""
from __future__ import annotations

import json
import os
from datetime import datetime, timedelta
from typing import Any

import pytz
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def _load_credentials() -> Credentials | None:
    """Load OAuth credentials. Prefer GOOGLE_TOKEN_JSON env var (for GitHub Actions),
    fall back to local token.json (for local dev)."""
    token_json = os.getenv("GOOGLE_TOKEN_JSON")
    if token_json:
        try:
            info = json.loads(token_json)
            creds = Credentials.from_authorized_user_info(info, SCOPES)
        except Exception as e:
            print(f"[calendar] Could not parse GOOGLE_TOKEN_JSON: {e}")
            return None
    elif os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    else:
        return None

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except Exception as e:
            print(f"[calendar] Token refresh failed: {e}")
            return None
    return creds


def get_today_events() -> list[dict[str, Any]]:
    """Return today's calendar events (in user's timezone)."""
    creds = _load_credentials()
    if not creds:
        return [{"error": "Google Calendar not configured. See README."}]

    tz_name = os.getenv("USER_TIMEZONE", "Europe/Paris")
    tz = pytz.timezone(tz_name)
    now = datetime.now(tz)
    start = tz.localize(datetime(now.year, now.month, now.day, 0, 0, 0))
    end = start + timedelta(days=1)

    try:
        service = build("calendar", "v3", credentials=creds, cache_discovery=False)
        events_result = service.events().list(
            calendarId="primary",
            timeMin=start.isoformat(),
            timeMax=end.isoformat(),
            singleEvents=True,
            orderBy="startTime",
            maxResults=20,
        ).execute()
    except Exception as e:
        return [{"error": f"Calendar fetch failed: {e}"}]

    events = []
    for ev in events_result.get("items", []):
        start_info = ev.get("start", {})
        when = start_info.get("dateTime") or start_info.get("date") or ""
        # Try to format time only if dateTime is present
        time_str = ""
        if "dateTime" in start_info:
            try:
                dt = datetime.fromisoformat(start_info["dateTime"].replace("Z", "+00:00"))
                dt = dt.astimezone(tz)
                time_str = dt.strftime("%H:%M")
            except Exception:
                time_str = when
        else:
            time_str = "All day"

        events.append({
            "time": time_str,
            "title": ev.get("summary", "(no title)"),
            "location": ev.get("location", ""),
            "description": ev.get("description", "")[:200] if ev.get("description") else "",
        })
    return events


def format_calendar_html(events: list[dict[str, Any]]) -> str:
    if not events:
        return "<p><em>No events today — a clear schedule!</em></p>"
    if events and "error" in events[0]:
        return f"<p><em>{events[0]['error']}</em></p>"

    rows = []
    for e in events:
        loc = f" &mdash; <span style='color:#666'>{e['location']}</span>" if e["location"] else ""
        rows.append(
            f"<li><strong>{e['time']}</strong> — {e['title']}{loc}</li>"
        )
    return "<ul>" + "\n".join(rows) + "</ul>"


if __name__ == "__main__":
    from pprint import pprint
    pprint(get_today_events())
